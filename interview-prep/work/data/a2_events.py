"""A2: the ten largest outage events in Dominion counties (EAGLE-I, Nov 2014 to 2025), their
restoration, storm type, and whether restoration got faster over time; one restoration curve.

Reads the DuckDB mirror (sql/09 and sql/11 built). Writes sections/a2_events.md. The chart-ready
tables are written to data/output/ by scripts/export_powerbi_csv.py (outage_events_top10.csv,
fct_event_context.csv, fct_restoration_curve.csv); this script prints their queries.
"""
import math
from pathlib import Path

import duckdb
import numpy as np
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "a2_events.md"
con = duckdb.connect(str(DB), read_only=True)

Q_TOP = """SELECT ROW_NUMBER() OVER (ORDER BY peak_sustained_1h DESC) AS rank,
       start_day, CAST(peak_utc - INTERVAL '5 HOUR' AS DATE) AS peak_day, storm_type, tropical_cyclone,
       peak_customers_out, peak_sustained_1h,
       ROUND(hours_above_threshold, 1) AS hours_above_10k,
       ROUND(customer_hours / 1e6, 2)  AS customer_hours_m,
       ROUND(hours_to_50pct, 1) AS h50, ROUND(hours_to_90pct, 1) AS h90, ROUND(hours_to_99pct, 1) AS h99,
       doe417_customers_max, starts_on_med_proxy_day, event_key
FROM mart.FCT_EVENT_CONTEXT
ORDER BY peak_sustained_1h DESC
LIMIT 10"""
top = con.execute(Q_TOP).df()

Q_SET = """SELECT event_key, year, start_day, peak_sustained_1h, hours_to_50pct, hours_to_90pct, storm_type
FROM mart.FCT_EVENT_CONTEXT
WHERE peak_sustained_1h >= 50000 AND hours_to_90pct IS NOT NULL
ORDER BY start_day"""
ev = con.execute(Q_SET).df()
n = len(ev)
X = np.column_stack([np.ones(n), ev.year - 2020, np.log(ev.peak_sustained_1h)])
res = {}
for col in ("hours_to_50pct", "hours_to_90pct"):
    y = np.log(ev[col].clip(lower=0.25))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    s2 = resid @ resid / (n - X.shape[1])
    cov = s2 * np.linalg.inv(X.T @ X)
    se = math.sqrt(cov[1, 1])
    t = stats.t.ppf(0.975, n - X.shape[1])
    p = 2 * (1 - stats.t.cdf(abs(beta[1] / se), n - X.shape[1]))
    res[col] = dict(pct=100 * (math.exp(beta[1]) - 1), lo=100 * (math.exp(beta[1] - t * se) - 1),
                    hi=100 * (math.exp(beta[1] + t * se) - 1), p=p, size=beta[2])
early = ev[ev.year <= 2019]
late = ev[ev.year >= 2020]
rho, rho_p = stats.spearmanr(ev.year, ev.hours_to_90pct)
mw = stats.mannwhitneyu(early.hours_to_90pct, late.hours_to_90pct)

# restoration curve of one event: Isaias (largest event with a matching DOE-417 report)
Q_CURVE = """SELECT hour_since_peak, customers_out, ROUND(share_restored, 3) AS share_restored
FROM mart.FCT_RESTORATION_CURVE
WHERE event_key = (SELECT event_key FROM mart.FCT_EVENT_CONTEXT WHERE tropical_cyclone LIKE '%ISAIAS%')
ORDER BY hour_since_peak"""
cur = con.execute(Q_CURVE).df()
key_hours = cur[cur.hour_since_peak.isin([0, 6, 12, 24, 36, 48, 72, 96, 120, 144, 167])]
isa = top[top.tropical_cyclone.fillna("").str.contains("ISAIAS")].iloc[0]

md = ["## A2 The ten largest outage events in Dominion counties, November 2014 to 2025", "",
      "**Finding.** The ten largest outage events in the 103 counties Dominion serves were three tropical storms (Michael 2018, "
      "Isaias 2020, Matthew 2016), two winter storms (January 2022 snow, February 2021 ice) and five wind events. "
      f"The largest, Michael (11-12 October 2018), had {int(top.peak_sustained_1h.iloc[0]):,} customers out for a full hour "
      f"(all utilities in those counties); half the excess was restored {top.h50.iloc[0]} hours after the peak and 90% after {top.h90.iloc[0]} hours. "
      "Winter storms took longest to restore: about 100 hours to 90% for both the January 2022 snowstorm and the February 2021 ice storm. "
      f"There is no clear change in restoration speed: across the {n} events that kept 50,000 or more customers out for an hour, after allowing for event size, "
      f"hours to 90% restored moved {res['hours_to_90pct']['pct']:+.1f}% a year (95% CI {res['hours_to_90pct']['lo']:+.1f}% to {res['hours_to_90pct']['hi']:+.1f}%, "
      f"p = {res['hours_to_90pct']['p']:.2f}, not significant); the median was {early.hours_to_90pct.median():.1f} hours in 2015-2019 ({len(early)} events) and "
      f"{late.hours_to_90pct.median():.1f} hours in 2020-2025 ({len(late)} events). Say \"no evidence that restoration got faster\", not \"it got slower\".", "",
      "**Chart-ready tables** (`data/output/`): `outage_events_top10.csv` (this table), `fct_event_context.csv` (all 486 territory events "
      "with storm type, tropical cyclone and DOE-417 match), `fct_restoration_curve.csv` (hour-by-hour curves for the events that peaked at 50,000 "
      "or more; slice on `event_key`).", "",
      "| # | Start (EST) | Peak (EST) | Storm type | Tropical cyclone | Peak out | Held 1 h | Hours above 10k | Customer-hours (m) | h50 | h90 | h99 | DOE-417 customers |",
      "|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for r in top.itertuples():
    tc = r.tropical_cyclone.title() if isinstance(r.tropical_cyclone, str) else ""
    import pandas as pd
    doe = "" if pd.isna(r.doe417_customers_max) else f"{int(r.doe417_customers_max):,}"
    md.append(f"| {r.rank} | {r.start_day:%Y-%m-%d} | {r.peak_day:%Y-%m-%d} | {r.storm_type} | {tc} | {int(r.peak_customers_out):,} | {int(r.peak_sustained_1h):,} | "
              f"{r.hours_above_10k} | {r.customer_hours_m} | {r.h50} | {r.h90} | {r.h99} | {doe} |")
md += ["", "```sql", Q_TOP, "```", "",
       "**Did restoration get faster?** Events with at least 50,000 customers out for an hour, 2015-2025:", "",
       "```sql", Q_SET, "```", "",
       f"OLS on those {n} events: ln(hours) = a + b x (year - 2020) + c x ln(peak held 1 h); `numpy.linalg.lstsq`, t-based 95% CI.", "",
       "| Measure | Change per year, size-adjusted | 95% CI | p |", "|---|---:|---|---:|",
       f"| Hours to 50% restored | {res['hours_to_50pct']['pct']:+.1f}% | {res['hours_to_50pct']['lo']:+.1f}% to {res['hours_to_50pct']['hi']:+.1f}% | {res['hours_to_50pct']['p']:.2f} |",
       f"| Hours to 90% restored | {res['hours_to_90pct']['pct']:+.1f}% | {res['hours_to_90pct']['lo']:+.1f}% to {res['hours_to_90pct']['hi']:+.1f}% | {res['hours_to_90pct']['p']:.2f} |",
       "", f"Size matters more than the year: each doubling of the peak multiplies hours to 90% by {2 ** res['hours_to_90pct']['size']:.2f}. "
       f"Spearman rank correlation of hours to 90% with year: rho = {rho:.2f} (p = {rho_p:.2f}); Mann-Whitney 2015-19 vs 2020-25: p = {mw.pvalue:.2f}.", "",
       f"**Restoration curve, Tropical Storm Isaias (peak {isa.start_day:%d %b %Y}).** Chosen for the inset because it is the largest event with a matching "
       f"DOE-417 report (Virginia, {int(isa.doe417_customers_max):,} customers affected; EAGLE-I's simultaneous peak for all utilities in the 103 counties was "
       f"{int(isa.peak_customers_out):,}). Share of the excess over the pre-event background restored, by hours since the peak:", "",
       "```sql", Q_CURVE, "```", "",
       "| Hours since peak | Customers out (hourly max) | Share restored |", "|---:|---:|---:|"]
md += [f"| {int(r.hour_since_peak)} | {int(r.customers_out):,} | {r.share_restored:.0%} |" for r in key_hours.itertuples()]
md += ["", "**Caveats.**",
       "- EAGLE-I counts every utility's customers in a county, so these events include co-op and municipal customers in the 103 counties "
       "Dominion serves (the Dominion-county rule is in `DIM_COUNTY.dominion_county_rule`). They are not Dominion's own event records.",
       "- \"Held 1 h\" ranks events by the highest level held for four consecutive 15-minute readings, so a 45-minute spike (30 Jul 2019, "
       "159,742 for under an hour in Hampton Roads) does not rank above multi-day storms. Restoration times ignore one-reading collection drops "
       "(the series must stay below the level for 3 hours).",
       "- Hours to X% are measured from the peak, against the excess over the median of the 24 hours before the event. The 2025-02-12 event "
       "merges the 12 February and 15-16 February storms, because the territory never fell below 10,000 out for 3 hours in between.",
       "- Storm type comes from NOAA line-risk reports in Dominion counties on the event's days; the tropical label also uses HURDAT2 tracks "
       "within 400 km of Richmond. DOE-417 has no utility column: the match rule is in sql/11 (decision D19).",
       "- The trend test has few events and wide intervals; \"no measurable change\" is not \"no change\".", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
