"""B0: does Bedford city (FIPS 51515, part of Bedford County 51019 since 1 July 2013) double-count
in the storm index (F04: 465 -> 796) or the weather fit (F05: r = 0.70, 145.3)?

Read-only: computes the committed numbers and the alternative with 51515 folded into 51019.
Changes nothing in sql/ or data/. Writes sections/b0_bedford.md.
"""
from pathlib import Path

import duckdb
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "b0_bedford.md"
con = duckdb.connect(str(DB), read_only=True)
md = ["## B0 Bedford city check (storm index)", ""]


def run(sql):
    return con.execute(sql).df()


q_map = """SELECT d.eia_county, d.county_id_fips, z.zone, z.county_name AS noaa_lookup_name
FROM stg.DOMINION_VA_COUNTIES d
LEFT JOIN raw.NOAA_ZONE_COUNTY z ON z.state = 'VA' AND LPAD(z.fips, 5, '0') = d.county_id_fips
WHERE d.county_id_fips IN ('51019', '51515')
ORDER BY 2"""
m = run(q_map)
n_dom = run("SELECT COUNT(*) AS n FROM stg.DOMINION_VA_COUNTIES").n.iloc[0]

# storm county-days per year: as committed, Bedford city days, and with 51515 folded into 51019
q_days = """WITH ev AS (
  SELECT year, county_id_fips, begin_yearmonth, begin_day
  FROM stg.NOAA_VA_EVENTS
  WHERE county_id_fips IN (SELECT county_id_fips FROM stg.DOMINION_VA_COUNTIES WHERE county_id_fips IS NOT NULL)
    AND line_risk <> 'other'
),
committed AS (SELECT year, COUNT(*) AS storm_county_days FROM (SELECT DISTINCT * FROM ev) GROUP BY 1),
city AS (
  SELECT year, COUNT(*) AS bedford_city_days,
         COUNT(*) FILTER (WHERE also_county) AS city_days_also_on_county
  FROM (
    SELECT DISTINCT c.year, c.begin_yearmonth, c.begin_day,
           EXISTS (SELECT 1 FROM ev k WHERE k.county_id_fips = '51019' AND k.year = c.year
                     AND k.begin_yearmonth = c.begin_yearmonth AND k.begin_day = c.begin_day) AS also_county
    FROM ev c WHERE c.county_id_fips = '51515')
  GROUP BY 1),
folded AS (
  SELECT year, COUNT(*) AS storm_county_days_folded
  FROM (SELECT DISTINCT year, CASE WHEN county_id_fips = '51515' THEN '51019' ELSE county_id_fips END AS fips,
                        begin_yearmonth, begin_day FROM ev)
  GROUP BY 1)
SELECT c.year, c.storm_county_days, COALESCE(b.bedford_city_days, 0) AS bedford_city_days,
       COALESCE(b.city_days_also_on_county, 0) AS city_days_also_on_county,
       f.storm_county_days_folded, c.storm_county_days - f.storm_county_days_folded AS difference
FROM committed c JOIN folded f USING (year) LEFT JOIN city b USING (year)
ORDER BY c.year"""
d = run(q_days)
si = run("SELECT year, storm_county_days FROM mart.STORM_INDEX ORDER BY year")
assert (si.storm_county_days.values == d.storm_county_days_folded.values).all(), "after D22 mart.STORM_INDEX must equal the folded count"

md += ["**Status: fixed by decision D22 (orchestrator ruling, 1 Nov 2026); see the D22 re-check section. The \"pre-D22\" columns below recompute the old index from staging.**", "", "**Finding.** Yes, Bedford city was counted twice in the committed storm index. EIA-861's 2025 Service Territory file",
       f"still lists \"Bedford City\" for Dominion, so `STG.DOMINION_VA_COUNTIES` has {n_dom} entries (103 real counties and cities",
       "plus 51515), and NOAA's zone lookup maps forecast zone 34 to both Bedford County (51019) and the City of Bedford (51515).",
       "Every zone-34 storm therefore adds two county-days for one area. The defunct code adds "
       f"{int(d.difference.sum())} county-days over 2013-2025 ({int(d[d.year==2024].difference.iloc[0])} in 2024, {int(d[d.year==2025].difference.iloc[0])} in 2025); "
       f"{int(d.city_days_also_on_county.sum())} of its {int(d.bedford_city_days.sum())} days are also Bedford County days. "
       "Folding 51515 into 51019 changes F04 and F05 slightly (table below); no conclusion changes. **Nothing has been changed:** "
       "the fix was later applied in `STORM_INDEX` itself (sql/05, decision D22).", "",
       "Mapping:", "", "```sql", q_map, "```", ""]
md += ["| EIA county | FIPS | NOAA zone | NOAA lookup name |", "|---|---|---|---|"]
md += [f"| {r.eia_county} | {r.county_id_fips} | {r.zone} | {r.noaa_lookup_name} |" for r in m.itertuples()]
md += ["", "Storm county-days per year, committed and with 51515 folded into 51019:", "", "```sql", q_days, "```", "",
       "| Year | Pre-D22 (unfolded) | Bedford city days | ... also a Bedford County day | Folded (= mart.STORM_INDEX after D22) | Difference |",
       "|---:|---:|---:|---:|---:|---:|"]
md += [f"| {r.year} | {r.storm_county_days} | {r.bedford_city_days} | {r.city_days_also_on_county} | {r.storm_county_days_folded} | {r.difference} |"
       for r in d.itertuples()]

# F05 and the weather-adjusted series, both ways
q_fit = """-- same join as sql/05 Q6b and sql/07, run once with each storm count
SELECT s.year, s.storm_county_days, f.saidi_ex_med
FROM mart.STORM_INDEX s JOIN mart.FCT_RELIABILITY f ON f.year = s.year AND f.utility_key = '19876|VA'
ORDER BY s.year"""
j = run(q_fit).drop(columns="storm_county_days").merge(d[["year", "storm_county_days", "storm_county_days_folded"]], on="year")


def fit(col):
    t = j[j.year.between(2015, 2024)]
    r = stats.pearsonr(t[col], t.saidi_ex_med)
    lr = stats.linregress(t[col], t.saidi_ex_med)
    x25 = j[j.year == 2025][col].iloc[0]
    pred25 = lr.intercept + lr.slope * x25
    adj = j[j.year >= 2015].copy()
    adj["wa"] = adj.saidi_ex_med - (lr.intercept + lr.slope * adj[col]) + t.saidi_ex_med.mean()
    adj["wa"] = adj["wa"].round(1)
    tr = stats.linregress(adj.year, adj.wa)
    return dict(r=r.statistic, p=r.pvalue, slope=lr.slope, intercept=lr.intercept, x25=x25, pred25=pred25,
                wa25=adj[adj.year == 2025].wa.iloc[0], trend=tr.slope, trend_p=tr.pvalue)


a, b = fit("storm_county_days"), fit("storm_county_days_folded")
md += ["", "Weather fit (2015-2024, n = 10) both ways:", "", "```sql", q_fit, "```", "",
       "Python: `scipy.stats.pearsonr` and `linregress` on the 2015-2024 rows; weather-adjusted = actual - predicted + 2015-2024 mean (sql/07).", "",
       "| Quantity | Pre-D22 | 51515 folded into 51019 (D22) |", "|---|---:|---:|",
       f"| Storm county-days 2024 -> 2025 (F04) | {int(j[j.year==2024].storm_county_days.iloc[0])} -> {int(a['x25'])} | {int(j[j.year==2024].storm_county_days_folded.iloc[0])} -> {int(b['x25'])} |",
       f"| r, storm county-days vs SAIDI ex-MED (F05) | {a['r']:.3f} (p = {a['p']:.3f}) | {b['r']:.3f} (p = {b['p']:.3f}) |",
       f"| Fit slope, min per storm county-day | {a['slope']:.4f} | {b['slope']:.4f} |",
       f"| Fit intercept | {a['intercept']:.1f} | {b['intercept']:.1f} |",
       f"| Predicted 2025 SAIDI ex-MED (actual 144.4) | {a['pred25']:.1f} | {b['pred25']:.1f} |",
       f"| Weather-adjusted 2025 | {a['wa25']:.1f} | {b['wa25']:.1f} |",
       f"| Trend of weather-adjusted 2015-2025, min/yr (Q10) | {a['trend']:+.2f} (p = {a['trend_p']:.2f}) | {b['trend']:+.2f} (p = {b['trend_p']:.2f}) |",
       "", "Committed outputs that would change with the fix: `mart.STORM_INDEX`, `V_STORM_VS_SAIDI`, `SAIDI_WEATHER_ADJUSTED`, "
       "`data/output/storm_index.csv`, `data/output/storm_vs_saidi.csv`, `data/output/saidi_weather_adjusted.csv`, the check comments in sql/05 and sql/07, "
       "`scripts/check_output_metrics.py` expectations, and every place that quotes 465, 796, 0.70 or 145.3.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md[-14:]))
print(d.to_string())
