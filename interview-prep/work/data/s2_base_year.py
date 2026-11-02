"""S2 base-year check and the sql/07 Q10 slope (orchestrator requests 1 and 3, 2026-11-01).

Reads the DuckDB database built from the source files (scripts/run_local_duckdb_sources.py) and
writes interview-prep/work/data/sections/s2_base_year.md, with the SQL behind every number.
In Snowflake, read `mart.` as RELIABILITY.MART.
"""
import math
from pathlib import Path

import duckdb
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "s2_base_year.md"
OUT.parent.mkdir(exist_ok=True)
con = duckdb.connect(str(DB), read_only=True)
md = []

# 1. Annual series
q_series = """SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2013 AND 2025 ORDER BY year"""
s = con.execute(q_series).df()
md += ["## S2 base-year check", "",
       "Question: does \"the rise comes mostly from more frequent interruptions\" hold whichever base year is used?",
       "Source: EIA-861 via `mart.FCT_RELIABILITY` (Dominion Energy Virginia, utility 19876, VA, ex-MED, Dominion's own",
       "major-event rule). 2025 values equal the EIA-861 2025 final file (released 7 Oct 2026).", "",
       "### S2.1 SAIDI, SAIFI and CAIDI ex-MED, 2013 to 2025", "", "```sql", q_series, "```", "",
       "| Year | SAIDI (min) | SAIFI | CAIDI (min) | Customers |", "|---:|---:|---:|---:|---:|"]
for r in s.itertuples():
    md.append(f"| {r.year} | {r.saidi_ex_med:.1f} | {r.saifi_ex_med:.3f} | {r.caidi_ex_med:.1f} | {int(r.customers):,} |")
mx = s[s.year.between(2013, 2025)].saifi_ex_med.max()
md += ["", f"SAIFI 2025 = {s[s.year==2025].saifi_ex_med.iloc[0]:.3f} is the highest value in 2013-2025 (next: 2018, 1.303). "
       f"CAIDI 2025 = {s[s.year==2025].caidi_ex_med.iloc[0]:.1f} is below every year 2018-2022 (111.9 to 120.5) and above 2015-2017 and 2023-2024.", ""]

# 2. Decomposition for every base year into 2025
q_dec = """WITH p AS (SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA')
SELECT a.year AS base_year, b.year AS end_year,
       ROUND(100 * (b.saidi_ex_med / a.saidi_ex_med - 1), 1) AS saidi_pct,
       ROUND(100 * (b.saifi_ex_med / a.saifi_ex_med - 1), 1) AS saifi_pct,
       ROUND(100 * (b.caidi_ex_med / a.caidi_ex_med - 1), 1) AS caidi_pct,
       ROUND(LN(b.saidi_ex_med / a.saidi_ex_med), 4) AS ln_saidi,
       ROUND(LN(b.saifi_ex_med / a.saifi_ex_med), 4) AS ln_saifi,
       ROUND(LN(b.caidi_ex_med / a.caidi_ex_med), 4) AS ln_caidi,
       ROUND(100 * LN(b.saifi_ex_med / a.saifi_ex_med) / LN(b.saidi_ex_med / a.saidi_ex_med)) AS pct_of_change_from_frequency
FROM p a JOIN p b ON b.year = 2025 AND a.year BETWEEN 2015 AND 2024
ORDER BY a.year"""
d = con.execute(q_dec).df()
md += ["### S2.2 Log decomposition of the SAIDI change, every base year to 2025", "",
       "ln(SAIDI2/SAIDI1) = ln(SAIFI2/SAIFI1) + ln(CAIDI2/CAIDI1). The share from frequency is ln(SAIFI ratio) / ln(SAIDI ratio);",
       "it is only meaningful when SAIDI moved by more than about 2% (sql/02, V_TREND rule) and in the same direction as SAIFI.", "",
       "```sql", q_dec, "```", "",
       "| Base year | SAIDI change | SAIFI change | CAIDI change | Share of ln change from frequency | Reading |",
       "|---:|---:|---:|---:|---:|---|"]
for r in d.itertuples():
    if abs(r.ln_saidi) < 0.02:
        reading = "SAIDI flat; share not meaningful. Frequency up, duration down"
        share = "n/m"
    elif r.ln_saidi < 0:
        reading = "SAIDI fell; frequency up, duration down more"
        share = "n/m"
    else:
        share = f"{int(r.pct_of_change_from_frequency)}%"
        reading = ("frequency explains all of it; duration fell" if r.ln_caidi < 0 else
                   "mostly frequency" if r.pct_of_change_from_frequency >= 50 else "mostly duration")
    md.append(f"| {r.base_year} | {r.saidi_pct:+.1f}% | {r.saifi_pct:+.1f}% | {r.caidi_pct:+.1f}% | {share} | {reading} |")
md += ["", "Pairs the brief needs:",
       f"- **2023 -> 2025** (the pair in the README): SAIDI {d[d.base_year==2023].saidi_pct.iloc[0]:+.1f}%, SAIFI {d[d.base_year==2023].saifi_pct.iloc[0]:+.1f}%, CAIDI {d[d.base_year==2023].caidi_pct.iloc[0]:+.1f}%; {int(d[d.base_year==2023].pct_of_change_from_frequency.iloc[0])}% of the log change from frequency.",
       f"- **2022 -> 2025** (the pair that moves the 3-year average from 130.2 to 133.0, because (2023-25) - (2022-24) = (2025 - 2022)/3 = {(s[s.year==2025].saidi_ex_med.iloc[0]-s[s.year==2022].saidi_ex_med.iloc[0])/3:.2f} min): "
       f"SAIDI {d[d.base_year==2022].saidi_pct.iloc[0]:+.1f}%, SAIFI {d[d.base_year==2022].saifi_pct.iloc[0]:+.1f}%, CAIDI {d[d.base_year==2022].caidi_pct.iloc[0]:+.1f}%. "
       "Frequency more than explains the rise; average restoration time fell.", ""]

# 3. Long run: period means and OLS slopes
q_long = """SELECT
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saifi_ex_med END), 3) AS saifi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saifi_ex_med END), 3) AS saifi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN caidi_ex_med END), 1) AS caidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN caidi_ex_med END), 1) AS caidi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saidi_ex_med END), 1) AS saidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_2023_25,
  REGR_SLOPE(saifi_ex_med, year) AS saifi_slope, REGR_SLOPE(caidi_ex_med, year) AS caidi_slope, REGR_SLOPE(saidi_ex_med, year) AS saidi_slope
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2015 AND 2025"""
l = con.execute(q_long).df().iloc[0]
sub = s[s.year.between(2015, 2025)]
fits = {k: stats.linregress(sub.year, sub[k]) for k in ("saifi_ex_med", "caidi_ex_med", "saidi_ex_med")}
tcrit = stats.t.ppf(0.975, len(sub) - 2)


def ci(f):
    return f.slope - tcrit * f.stderr, f.slope + tcrit * f.stderr


md += ["### S2.3 Long run: 2015-17 mean vs 2023-25 mean, and OLS slopes 2015-2025 (n = 11)", "",
       "```sql", q_long, "```", "",
       "Slope standard errors and p-values: `scipy.stats.linregress` on the same 11 rows (two-sided, t with 9 df).", "",
       "| Measure | 2015-17 mean | 2023-25 mean | Change | OLS slope per year | 95% CI | p |",
       "|---|---:|---:|---:|---:|---|---:|"]
rows = [("SAIFI", l.saifi_2015_17, l.saifi_2023_25, fits["saifi_ex_med"], "{:.4f}"),
        ("CAIDI (min)", l.caidi_2015_17, l.caidi_2023_25, fits["caidi_ex_med"], "{:.2f}"),
        ("SAIDI (min)", l.saidi_2015_17, l.saidi_2023_25, fits["saidi_ex_med"], "{:.2f}")]
for name, a, b, f, fmt in rows:
    lo, hi = ci(f)
    md.append(f"| {name} | {a} | {b} | {100*(b/a-1):+.1f}% | {fmt.format(f.slope)} | {fmt.format(lo)} to {fmt.format(hi)} | {f.pvalue:.2f} |")
lr_sf = math.log(l.saifi_2023_25 / l.saifi_2015_17)
lr_cd = math.log(l.caidi_2023_25 / l.caidi_2015_17)
md += ["", f"Period-mean decomposition: ln SAIFI ratio {lr_sf:.4f}, ln CAIDI ratio {lr_cd:.4f}, so {100*lr_sf/(lr_sf+lr_cd):.0f}% of the 2015-17 -> 2023-25 rise in SAIDI "
       "is frequency (period means of the annual values; SAIDI of the means is not exactly SAIFI x CAIDI of the means, the gap is under 0.2%).", ""]

# 4. Answer
md += ["### S2.4 Answer", "",
       "- **Yes for every base year in which SAIDI rose.** Against 2015, 2016, 2017, 2020, 2021, 2022, 2023 and 2024, SAIFI rose by more than CAIDI, or CAIDI fell. "
       "For 2022 -> 2025 (the pair behind 130.2 -> 133.0) frequency more than explains the rise: SAIFI +10.1%, CAIDI -3.6%.",
       "- **Against 2018 and 2019 SAIDI is lower in 2025** (149.6 and 149.9 then, 144.4 now): frequency is still higher in 2025, duration is lower. "
       "So the safe wording is about the recent rise, not \"reliability is worse than ever\".",
       "- **2025 frequency is a record for the series:** SAIFI 1.320 is the highest of 2013-2025. Restoration time (CAIDI 109) is mid-range: higher than 2015-17 and 2023-24, lower than 2018-22.",
       f"- **Long run, neither trend is statistically clear on 11 points** (SAIFI slope p = {fits['saifi_ex_med'].pvalue:.2f}, CAIDI slope p = {fits['caidi_ex_med'].pvalue:.2f}; "
       f"both 95% intervals include zero). The 2015-17 -> 2023-25 rise in SAIDI ({100*(l.saidi_2023_25/l.saidi_2015_17-1):+.1f}%) is {100*lr_sf/(lr_sf+lr_cd):.0f}% frequency, "
       "so the direction agrees with the short-run pairs; present the long run as direction, not proof.",
       "- **Defensible sentence:** \"Measured from 2022 or from 2023, most of the increase in outage minutes came from more interruptions per customer; "
       "average restoration time changed little (3.6% shorter than in 2022, 3.3% longer than in 2023). "
       "In 2025 interruptions per customer were the highest in EIA's 2013-2025 record.\"", ""]

# 5. Q10 slope
q10 = """SELECT year, weather_adjusted_saidi FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year"""
w = con.execute(q10).df()
f = stats.linregress(w.year, w.weather_adjusted_saidi)
lo, hi = f.slope - stats.t.ppf(0.975, len(w) - 2) * f.stderr, f.slope + stats.t.ppf(0.975, len(w) - 2) * f.stderr
sql_slope = con.execute("SELECT REGR_SLOPE(weather_adjusted_saidi, year) FROM mart.SAIDI_WEATHER_ADJUSTED").fetchone()[0]
fit_i, fit_s = con.execute("SELECT REGR_INTERCEPT(saidi_ex_med, storm_county_days), REGR_SLOPE(saidi_ex_med, storm_county_days) "
                           "FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024").fetchone()
md += ["## Q10 check: trend in the weather-adjusted SAIDI (sql/07)", "",
       "```sql", q10, "-- sql/07 Q10: SELECT ROUND(REGR_SLOPE(weather_adjusted_saidi, year), 2) FROM RELIABILITY.MART.SAIDI_WEATHER_ADJUSTED", "```", "",
       f"- Slope **{sql_slope:+.2f} minutes per year** over 2015-2025 (n = {len(w)}; SQL REGR_SLOPE and scipy agree: {f.slope:+.3f}).",
       f"- Standard error {f.stderr:.3f}; **95% CI {lo:+.2f} to {hi:+.2f} min/yr; p = {f.pvalue:.2f}**; R2 = {f.rvalue**2:.3f}.",
       f"- The adjusted series comes from a fit on the same 2015-2024 years (intercept {fit_i:.1f}, slope {fit_s:.4f} min per storm county-day, after decision D22), so it is model-based and its uncertainty is understated by this CI.",
       "- **Wording to defend:** \"After the exploratory weather adjustment, there is no clear trend since 2015: about +0.3 minutes a year, with a 95% range from roughly "
       f"{lo:+.1f} to {hi:+.1f}.\" B's \"no clear trend since 2015\" is right; avoid \"flat\" or \"has not moved\" (the README's older wording) because the interval is wide.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
