"""A4: load shape and sales by sector. PJM DOM zone (EIA-930) and Dominion VA retail sales (EIA-861).

Reads the DuckDB mirror (sql/06, 07, 10 built). Writes sections/a4_load.md. The chart-ready tables
are exported to data/output/ by scripts/export_powerbi_csv.py.
"""
from pathlib import Path

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "a4_load.md"
con = duckdb.connect(str(DB), read_only=True)
md = ["## A4 Load shape, seasonal peaks and sales by sector", ""]

# 1. hour-of-day growth
Q_PROF = "SELECT hour_no, avg_mw_2019, avg_mw_2025, growth_pct FROM mart.DOM_LOAD_PROFILE ORDER BY hour_no"
prof = con.execute(Q_PROF).df()
night = prof[prof.hour_no.between(1, 5)]
aft = prof[prof.hour_no.between(13, 17)]
Q_ALL = """SELECT ROUND(100 * (AVG(CASE WHEN YEAR(data_date) = 2025 THEN demand_mw END)
                     / AVG(CASE WHEN YEAR(data_date) = 2019 THEN demand_mw END) - 1), 1) AS all_hours_growth_pct
FROM stg.EIA930_DOM_HOURLY"""
allg = con.execute(Q_ALL).fetchone()[0]

# 2. seasonal peaks
Q_PEAK = """SELECT year,
       MAX(CASE WHEN season = 'winter' THEN peak_mw END) AS winter_peak_mw,
       MAX(CASE WHEN season = 'winter' THEN peak_date END) AS winter_peak_date,
       MAX(CASE WHEN season = 'summer' THEN peak_mw END) AS summer_peak_mw,
       MAX(CASE WHEN season = 'summer' THEN peak_date END) AS summer_peak_date
FROM mart.DOM_SEASONAL_PEAK GROUP BY year ORDER BY year"""
pk = con.execute(Q_PEAK).df()

# 3. sector split
Q_SECT = """SELECT customer_class, year, ROUND(sales_mwh / 1e6, 2) AS sales_twh, customers, mwh_per_customer
FROM mart.FCT_SALES_SECTOR
WHERE customer_class IN ('residential', 'commercial', 'industrial') AND year IN (2013, 2019, 2025)
ORDER BY customer_class, year"""
sect = con.execute(Q_SECT).df()
Q_SHARE = """SELECT year, customer_class, ROUND(100 * sales_mwh / SUM(sales_mwh) OVER (PARTITION BY year), 1) AS share_pct
FROM mart.FCT_SALES_SECTOR WHERE year IN (2013, 2025) ORDER BY year, customer_class"""
share = con.execute(Q_SHARE).df()

# 4. degree-day-normalised trend
Q_DAILY = """SELECT data_date, year, iso_weekday, avg_mw, hdd, cdd
FROM mart.DOM_LOAD_DAILY
WHERE year BETWEEN 2019 AND 2025 AND hours_reported >= 20 AND hdd IS NOT NULL"""
d = con.execute(Q_DAILY).df()
years = sorted(d.year.unique())
cols = [np.ones(len(d)), d.hdd, d.cdd, d.hdd ** 2, d.cdd ** 2]
cols += [(d.iso_weekday == k).astype(float) for k in range(2, 8)]
cols += [(d.year == y).astype(float) for y in years[1:]]
X = np.column_stack(cols)
beta, *_ = np.linalg.lstsq(X, d.avg_mw.astype(float), rcond=None)
r2 = 1 - ((d.avg_mw - X @ beta) ** 2).sum() / ((d.avg_mw - d.avg_mw.mean()) ** 2).sum()
norm = {}
for y in years:
    Xy = X.copy()
    Xy[:, -len(years) + 1:] = 0
    if y != years[0]:
        Xy[:, 11 + years.index(y) - 1] = 1
    norm[y] = float((Xy @ beta).mean())
actual = d.groupby("year").avg_mw.mean().to_dict()
dd = d.groupby("year")[["hdd", "cdd"]].sum()

md += ["**Finding.** In the PJM DOM zone, average demand rose "
       f"{allg:.0f}% from 2019 to 2025, more at night than in the afternoon: the hours ending 1 to 5 a.m. grew "
       f"{night.growth_pct.min():.1f}% to {night.growth_pct.max():.1f}% and the hours ending 1 to 5 p.m. "
       f"{aft.growth_pct.min():.1f}% to {aft.growth_pct.max():.1f}%. Winter set the year's peak in 2019, 2022 and 2025 "
       f"(2026 so far: winter {int(pk[pk.year==2026].winter_peak_mw.iloc[0]):,} MW vs summer {int(pk[pk.year==2026].summer_peak_mw.iloc[0]):,} MW). "
       f"Weather does not explain the growth: holding Virginia's daily heating and cooling degree days and the weekday at their 2019-2025 pattern, "
       f"average load rose from {norm[2019]:,.0f} MW (2019) to {norm[2025]:,.0f} MW (2025), +{100 * (norm[2025] / norm[2019] - 1):.0f}%, "
       f"against +{100 * (actual[2025] / actual[2019] - 1):.0f}% unadjusted. Dominion's commercial sales per commercial customer rose from "
       f"{sect[(sect.customer_class=='commercial') & (sect.year==2013)].mwh_per_customer.iloc[0]:.0f} MWh (2013) to "
       f"{sect[(sect.customer_class=='commercial') & (sect.year==2025)].mwh_per_customer.iloc[0]:.0f} MWh (2025); residential use per customer fell slightly. "
       "Nothing here identifies which customers drove the growth (decision D14).", "",
       "**Chart-ready tables** (`data/output/`): `dom_load_profile.csv` (24 rows, S5), `dom_load_hour_month.csv` (year x month x hour, heatmap), "
       "`dom_seasonal_peak.csv` (year x season with date and hour), `fct_sales_sector.csv` (year x class), `dom_load_daily.csv` (daily load with degree days).", "",
       "### A4.1 Hour-of-day growth, 2019 to 2025 (S5)", "", "```sql", Q_PROF, "```", "", "```sql", Q_ALL, "```", "",
       "| Hour ending | Avg MW 2019 | Avg MW 2025 | Growth |", "|---:|---:|---:|---:|"]
md += [f"| {int(r.hour_no)} | {int(r.avg_mw_2019):,} | {int(r.avg_mw_2025):,} | {r.growth_pct:+.1f}% |" for r in prof.itertuples()]
md += ["", "### A4.2 Seasonal peaks (winter = Dec, Jan, Feb of the same year; summer = Jun, Jul, Aug)", "", "```sql", Q_PEAK, "```", "",
       "| Year | Winter peak MW | Date | Summer peak MW | Date | Higher |", "|---:|---:|---|---:|---|---|"]
for r in pk.itertuples():
    hi = "winter" if r.winter_peak_mw > r.summer_peak_mw else "summer"
    md.append(f"| {r.year} | {int(r.winter_peak_mw):,} | {r.winter_peak_date} | {int(r.summer_peak_mw):,} | {r.summer_peak_date} | {hi} |")
md += ["", "2018 starts on 1 July 2018 (no June, so its summer peak covers July and August only, and its winter peak is December 2018 only); "
       "2026 runs to 30 October, so its winter is January and February only. The 2026 gap is 29 MW: call it a tie.", "",
       "### A4.3 Sales by sector, Dominion Energy Virginia (EIA-861)", "", "```sql", Q_SECT, "```", "",
       "| Class | Year | Sales TWh | Customers | MWh per customer |", "|---|---:|---:|---:|---:|"]
md += [f"| {r.customer_class} | {r.year} | {r.sales_twh} | {int(r.customers):,} | {r.mwh_per_customer:,.1f} |" for r in sect.itertuples()]
md += ["", "```sql", Q_SHARE, "```", "",
       "Share of retail sales: " + "; ".join(f"{int(y)} " + ", ".join(f"{c} {s}%" for c, s in zip(g.customer_class, g.share_pct)) for y, g in share.groupby("year")) + ".",
       "Sales include delivery-only service (customers buying energy elsewhere); 2025 commercial delivery-only sales were 4.53 TWh of 64.62.",
       "Industrial customer counts more than doubled while industrial sales fell; that looks like reclassification between classes and is not used.", "",
       "### A4.4 Degree-day-normalised trend (exploratory)", "", "```sql", Q_DAILY, "```", "",
       f"OLS on {len(d):,} days (2019-2025, days with 20 or more reported hours): daily average MW on HDD, CDD, their squares, weekday and year dummies "
       f"(R2 = {r2:.3f}; `numpy.linalg.lstsq`). Normalised average = the model's mean prediction for that year over all {len(d):,} days' weather and weekdays. "
       "Degree days are Virginia's population-weighted state values (NOAA CPC), used for a zone that also covers a sliver of North Carolina.", "",
       "| Year | Actual avg MW | Normalised avg MW | HDD | CDD |", "|---:|---:|---:|---:|---:|"]
md += [f"| {y} | {actual[y]:,.0f} | {norm[y]:,.0f} | {int(dd.loc[y, 'hdd']):,} | {int(dd.loc[y, 'cdd']):,} |" for y in years]
md += ["", "**Caveats.** The DOM zone (EIA-930) is larger than Dominion's retail territory and includes other utilities' load; hourly load by "
       "county or customer class is not public, so the night-time growth cannot be tied to a customer type from public data (the \"first 90 days\" "
       "question). Annual averages for 2019-2025 use full years; the normalisation is a descriptive model, not a forecast.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md[:4]))
print(prof.to_string())
print({y: (round(actual[y]), round(norm[y])) for y in years}, r2)
