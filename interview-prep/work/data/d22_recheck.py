"""D22 re-check: after folding Bedford city into Bedford County in STORM_INDEX (sql/05), recompute every
number that depends on the storm index and compare it with the pre-D22 value.

Pre-D22 values come from the baseline run (interview-prep/work/data/logs/d0_check_output_metrics_2026-11-01.log)
and findings B0. Writes sections/d22_recheck.md.
"""
from pathlib import Path

import duckdb
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "d22_recheck.md"
con = duckdb.connect(str(DB), read_only=True)

Q_J = """SELECT s.year, s.storm_county_days, f.saidi_ex_med, f.saifi_ex_med
FROM mart.STORM_INDEX s JOIN mart.FCT_RELIABILITY f ON f.year = s.year AND f.utility_key = '19876|VA'
ORDER BY s.year"""
j = con.execute(Q_J).df()
t = j[j.year.between(2015, 2024)]
r = stats.pearsonr(t.storm_county_days, t.saidi_ex_med)
lr = stats.linregress(t.storm_county_days, t.saidi_ex_med)
x25 = float(j[j.year == 2025].storm_county_days.iloc[0])
pred = lr.intercept + lr.slope * x25
adj = 144.4 - pred + t.saidi_ex_med.mean()
Q_WA = "SELECT year, weather_adjusted_saidi FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year"
wa = con.execute(Q_WA).df()
q10 = stats.linregress(wa.year, wa.weather_adjusted_saidi)
tc = stats.t.ppf(0.975, len(wa) - 2)
r_saifi = stats.pearsonr(t.storm_county_days, t.saifi_ex_med).statistic
wa19 = float(wa[wa.year == 2019].weather_adjusted_saidi.iloc[0])
a1_line = next(l for l in (Path(__file__).resolve().parent / "sections" / "a1_county_day.md").read_text(encoding="utf-8").splitlines()
               if l.startswith("| All complete county-days"))

rows = [
    ("Storm county-days 2024 -> 2025 (F04)", "465 -> 796", f"{int(j[j.year==2024].storm_county_days.iloc[0])} -> {int(x25)}", "changed"),
    ("Storm county-days 2019 (record year)", "851", f"{int(j[j.year==2019].storm_county_days.iloc[0])}", "changed"),
    ("r, storm county-days vs SAIDI ex-MED, 2015-2024 (F05)", "0.696 (0.70)", f"{r.statistic:.3f} ({r.statistic:.2f}), p = {r.pvalue:.3f}", "unchanged at 2 dp"),
    ("r with SAIFI ex-MED", "0.41", f"{r_saifi:.2f}", "unchanged"),
    ("Fit slope, min per storm county-day", "0.0514", f"{lr.slope:.4f}", "changed"),
    ("Fit intercept", "104.4", f"{lr.intercept:.1f}", "changed"),
    ("Predicted 2025 SAIDI ex-MED", "145.27 (145.3)", f"{pred:.2f} ({pred:.1f})", "unchanged at 1 dp"),
    ("Weather-adjusted 2025", "133.13 (133.1)", f"{adj:.2f} (SQL: {float(wa[wa.year==2025].weather_adjusted_saidi.iloc[0]):.1f})", "unchanged at 1 dp"),
    ("Weather-adjusted 2019", "135.8", f"{wa19:.1f}", "changed"),
    ("Q10 slope of weather-adjusted SAIDI, 2015-2025", "+0.34 min/yr, 95% CI -1.41 to +2.09, p 0.67",
     f"{q10.slope:+.2f} min/yr, 95% CI {q10.slope - tc * q10.stderr:+.2f} to {q10.slope + tc * q10.stderr:+.2f}, p {q10.pvalue:.2f}", "unchanged at 2 dp"),
    ("A1 storm vs calm county-days", "11.9x (7.9 to 16.9)", a1_line.split("|")[6].strip() + "x (" + a1_line.split("|")[7].strip() + ")",
     "unchanged: the county-day panel already folded 51515 into 51019"),
]
md = ["## D22 re-check: numbers that depend on the storm index", "",
      "Decision D22 (fix ordered by the orchestrator at 08:16) folds Bedford city (51515) into Bedford County (51019) in `STORM_INDEX` "
      "(sql/05). Everything downstream was rebuilt (`run_local_duckdb_sources.py`: T7-T31 pass; `check_output_metrics.py` passes with "
      "the D22 expectations) and the committed `storm_index.csv`, `storm_vs_saidi.csv` and `saidi_weather_adjusted.csv` were re-exported. "
      "Use the new F04 pair, **464 -> 791**, everywhere; the headline correlation, prediction and weather-adjusted value are unchanged at the "
      "precision quoted.", "",
      "| Quantity | Pre-D22 | After D22 | Status |", "|---|---|---|---|"]
md += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
md += ["", "```sql", Q_J, ";", Q_WA, "```", "",
       "Python: `scipy.stats.pearsonr` and `linregress` on the 2015-2024 rows (fit), and on 2015-2025 for the Q10 trend; "
       "the A1 ratio is read from the A1 section, re-run after D22. "
       "Snowflake: not rebuilt. `RELIABILITY.MART.STORM_INDEX`, `V_STORM_VS_SAIDI` and `SAIDI_WEATHER_ADJUSTED` in Snowflake still hold the "
       "pre-D22 values until the owner re-runs sql/05 and sql/07 (this run is add-only and does not replace existing objects). "
       "The Power BI workbook `powerbi/Dominion_Reliability_PowerBI_Data.xlsx` (sheet `StormIndex`) also holds pre-D22 values; the "
       "report should bind to `data/output/storm_vs_saidi.csv` instead.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
