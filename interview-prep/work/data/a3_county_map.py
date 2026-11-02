"""A3: non-major outage events and outage minutes per customer by county and year, 2015-2025,
as a map table (EAGLE-I, all utilities in the 103 Dominion counties).

Reads the DuckDB mirror. Writes sections/a3_county_map.md. Exports (scripts/export_powerbi_csv.py):
fct_county_year.csv (county x year) and county_outage_map.csv (one row per county, query below).
"""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "a3_county_map.md"
con = duckdb.connect(str(DB), read_only=True)

Q_YEAR = """SELECT year, SUM(events_non_med) AS events_non_med,
       ROUND(10000 * SUM(events_non_med) / SUM(customers_basis), 2) AS events_non_med_per_10k,
       ROUND(60 * SUM(customer_hours_non_med) / SUM(customers_basis), 1) AS minutes_non_med,
       ROUND(SUM(failed_share * customers_basis) / SUM(customers_basis), 3) AS failed_share
FROM mart.FCT_COUNTY_YEAR GROUP BY year ORDER BY year"""
yr = con.execute(Q_YEAR).df()

# the map table: one row per Dominion county (the query is also the export's)
Q_MAP = """WITH r AS (
  SELECT county_fips, SUM(readings) AS readings_2015_24
  FROM mart.FCT_COUNTY_DAY WHERE year BETWEEN 2015 AND 2024 GROUP BY 1
),
y AS (
  SELECT c.*, r.readings_2015_24,
         CASE WHEN c.county_fips = '51600' THEN 'excluded: implausible readings 2018-2020 (docs/03 P26)'
              WHEN r.readings_2015_24 < 1000 THEN 'excluded: almost no EAGLE-I readings (municipal utility)'
              ELSE 'ok' END AS map_flag
  FROM mart.FCT_COUNTY_YEAR c JOIN r USING (county_fips)
)
SELECT county_fips, county_label AS county_name, dominion_only_county, MAX(customers_basis) AS customers_basis, map_flag,
       MAX(readings_2015_24) AS readings_2015_24,
       ROUND(60 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN customer_hours_non_med END) / MAX(customers_basis), 1) AS minutes_non_med_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2015_19,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2020_24,
       ROUND(10000 * (AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END)
           - AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END)) / MAX(customers_basis), 2) AS change_events_per_10k,
       ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN storm_days END), 1) AS storm_days_avg_2015_24
FROM y
GROUP BY county_fips, county_label, dominion_only_county, map_flag
ORDER BY minutes_non_med_avg_2015_24 DESC"""
m_all = con.execute(Q_MAP).df()
m = m_all[m_all.map_flag == 'ok']
excl = m_all[m_all.map_flag != 'ok']
big = m[m.customers_basis >= 20000]
rose = (m.change_events_per_10k > 0).sum()
top5 = big.head(5)
low5 = big.sort_values("minutes_non_med_avg_2015_24").head(5)
corr = m[["minutes_non_med_avg_2015_24", "storm_days_avg_2015_24"]].corr().iloc[0, 1]
corr_big = big[["minutes_non_med_avg_2015_24", "storm_days_avg_2015_24"]].corr().iloc[0, 1]
y1519 = yr[yr.year.between(2015, 2019)].events_non_med_per_10k.mean()
y2024 = yr[yr.year.between(2020, 2024)].events_non_med_per_10k.mean()

md = ["## A3 Non-major outage events and minutes by county, 2015-2025 (map table)", "",
      "**Finding.** On days that are not proxy major event days, customers in the 103 Dominion counties (all utilities) averaged "
      f"{yr[yr.year.between(2015, 2024)].minutes_non_med.mean():.0f} outage minutes a year over 2015-2024, with a wide spread between counties: among counties with "
      f"20,000 or more customers, from {low5.minutes_non_med_avg_2015_24.min():.0f} minutes ({low5.iloc[0].county_name}) to "
      f"{top5.minutes_non_med_avg_2015_24.max():.0f} ({top5.iloc[0].county_name}). The highest are rural and exurban counties; the lowest are dense cities "
      "and inner suburbs. "
      f"County outage events on non-major days rose from {y1519:.1f} per 10,000 customers a year (2015-2019 average) to {y2024:.1f} (2020-2024), and "
      f"{rose} of the {len(m)} mapped counties had more events per customer in 2020-2024 than in 2015-2019. Counties with more storm days had more outage "
      f"minutes (r = {corr:.2f} across the {len(m)} mapped counties; {corr_big:.2f} across the {len(big)} with 20,000 or more customers): an association, not a cause. "
      f"{len(excl)} counties are left off the map: " + "; ".join(f"{r.county_name} ({r.map_flag.split(': ')[1]})" for r in excl.itertuples()) + ".", "",
      "**Chart-ready tables** (`data/output/`): `county_outage_map.csv` (one row per Dominion county with `map_flag`; join `county_fips` to "
      "`va_counties.topojson`), `fct_county_year.csv` (county x year, 2015-2025).", "",
      "### A3.1 By year", "", "```sql", Q_YEAR, "```", "",
      "| Year | Non-major county events | Per 10k customers | Outage minutes per customer, non-major days | Failed-reading share |",
      "|---:|---:|---:|---:|---:|"]
md += [f"| {r.year} | {int(r.events_non_med):,} | {r.events_non_med_per_10k} | {r.minutes_non_med} | {r.failed_share:.1%} |" for r in yr.itertuples()]
md += ["", "### A3.2 Map table (one row per county; top and bottom five shown, counties with 20,000+ customers)", "", "```sql", Q_MAP, "```", "",
       "| County | Customers | Minutes, non-major, avg 2015-24 | Events per 10k, 2015-19 | 2020-24 | Storm days a year |",
       "|---|---:|---:|---:|---:|---:|"]
for r in list(top5.itertuples()) + list(low5.itertuples()):
    md.append(f"| {r.county_name} | {int(r.customers_basis):,} | {r.minutes_non_med_avg_2015_24} | {r.events_per_10k_2015_19} | {r.events_per_10k_2020_24} | {r.storm_days_avg_2015_24} |")
md += ["", "**Caveats.**",
       "- EAGLE-I counts every utility's customers in a county: Dominion-only counties (`dominion_only_county`) are the cleanest; elsewhere co-op "
       "customers are included. The customer basis is decision D15.",
       "- 2025 is shown but not averaged: EAGLE-I collection failed for 46% of August and 45% of October 2025 county readings "
       f"(failed-reading share {yr[yr.year == 2025].failed_share.iloc[0]:.0%} for the year), so 2025 minutes and events are undercounted.",
       "- A county event is 1% or more of the county's customers out (at least 10), readings no more than an hour apart (decision D17); "
       "non-major = not starting on a proxy major event day (decision D18). The 1% threshold scales with county size, so events per customer "
       "compare a county with itself over time, not one county with another: map outage minutes per customer, and use the event counts for change. "
       "Small counties have noisy rates.",
       "- EAGLE-I coverage of Virginia customers was 94-97% in 2018-2022 (its coverage history); earlier years are not published, so part "
       "of a rise from 2015 may be coverage. Present the change as \"more events recorded\", not as a proven change in the grid.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md[:3]))
print(yr.to_string())
print(m.head(8).to_string())
