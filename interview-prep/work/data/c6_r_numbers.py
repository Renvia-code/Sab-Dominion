"""Batch 6: check R's numbered items N-1 to N-11 (research/hard25_answers.md, "Numbers not yet in claims.csv")
with D's own queries on the DuckDB mirror and the committed files. Writes sections/c6_r_numbers.md."""
import math
import sys
from pathlib import Path

import duckdb
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from export_powerbi_csv import PEERS  # noqa: E402

OUT = Path(__file__).resolve().parent / "sections" / "c6_r_numbers.md"
con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)
md = ["## C6 R's numbered items N-1 to N-11, checked (batch 6)", "",
      "Each item: R's value, D's value from D's own query, verdict. Source of R's items: `research/hard25_answers.md`, table "
      "\"Numbers not yet in claims.csv\".", ""]
verdicts = []


def sql_block(q):
    return ["```sql", q.strip(), "```", ""]


# ---------- N-1: the 2025 band ----------
Q1 = "SELECT year, storm_county_days, saidi_ex_med FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2025 ORDER BY year"
rows = [(int(y), float(x), float(s)) for y, x, s in con.execute(Q1).fetchall()]
fit = [(x, s) for y, x, s in rows if y <= 2024]
x0, y25 = next((x, s) for y, x, s in rows if y == 2025)
n = len(fit)
mx, my = sum(x for x, _ in fit) / n, sum(s for _, s in fit) / n
sxx = sum((x - mx) ** 2 for x, _ in fit)
slope = sum((x - mx) * (s - my) for x, s in fit) / sxx
intercept = my - slope * mx
sse = sum((s - intercept - slope * x) ** 2 for x, s in fit)
sd = math.sqrt(sse / (n - 2))
t = stats.t.ppf(0.975, n - 2)
yhat = intercept + slope * x0
lev = 1 / n + (x0 - mx) ** 2 / sxx
half_pi, half_ci = t * sd * math.sqrt(1 + lev), t * sd * math.sqrt(lev)
pi, ci = (yhat - half_pi, yhat + half_pi), (yhat - half_ci, yhat + half_ci)
ok1 = (round(pi[0], 1), round(pi[1], 1), round(half_pi, 1), round(sd, 2)) == (122.3, 168.2, 23.0, 8.67)
verdicts.append(("N-1", "CONFIRMED" if ok1 else "CORRECTED"))
md += ["### N-1 The 2025 band around the storm-line prediction", "",
       f"**{verdicts[-1][1]}, and it is a prediction interval.** Fit 2015-2024 (n = {n}, after D22): SAIDI ex-MED = {intercept:.4f} + "
       f"{slope:.6f} x storm county-days; residual SD {sd:.2f} minutes; t(0.975, {n - 2} df) = {t:.3f}. At 791 storm county-days the fit "
       f"gives {yhat:.2f}. The **95% prediction interval** for a single new year is **{pi[0]:.1f} to {pi[1]:.1f}** (+/-{half_pi:.1f}): "
       f"actual 2025 ({y25:.1f}) lies inside it. The **95% confidence interval** for the line itself (the mean SAIDI of years with 791 "
       f"storm county-days) is narrower, {ci[0]:.1f} to {ci[1]:.1f} (+/-{half_ci:.1f}), and 144.4 lies inside that too. Say: \"the 95% "
       "prediction interval for 2025 was about 122 to 168 minutes\"; never call it a confidence interval. It assumes the 2015-2024 "
       "line and normal residuals; ten points, so treat it as rough.", "",
       "Formula: prediction half-width = t x s x sqrt(1 + 1/n + (791 - mean x)^2 / Sxx); confidence half-width drops the \"1 +\".", ""]
md += sql_block(Q1)

# ---------- N-2: Dominion's standard and automatic recording ----------
Q2 = """SELECT year, standard, auto_recorded
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' ORDER BY year"""
d2 = con.execute(Q2).df()
other_all = (d2.standard == "Other").all() and list(d2.year) == list(range(2013, 2026))
auto_false = sorted(int(y) for y in d2[d2.auto_recorded == False].year)  # noqa: E712
auto_true = sorted(int(y) for y in d2[d2.auto_recorded == True].year)  # noqa: E712
ok2 = other_all and auto_false == [2013, 2014] and auto_true == list(range(2015, 2026))
verdicts.append(("N-2", "CONFIRMED" if ok2 else "CORRECTED"))
md += ["### N-2 Dominion's reporting standard and automatic recording, 2013-2025", "",
       f"**{verdicts[-1][1]}.** `standard` is \"Other\" in every year 2013-2025; `auto_recorded` is false in "
       f"{', '.join(map(str, auto_false))} and true in {auto_true[0]}-{auto_true[-1]}. D6 starts the weather fit in 2015 for that reason. "
       "Wording: \"recording became automated in 2015\" is what EIA-861's flag says; \"which shifts the level\" is D6's reasoning, "
       "not something the flag measures.", ""]
md += sql_block(Q2)

# ---------- N-3, N-11: all-events ranks; N-4 ex-MED medians ----------
PEER_ALL = f"""WITH u AS (
  SELECT f.utility_key, d.utility_name,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_all END)    AS saifi_all_2021_25,
         COUNT(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_all END)  AS n_saifi,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_all END)    AS saidi_all_2023_25,
         COUNT(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_all END)  AS n_saidi,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_ex_med_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_ex_med_2023_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ({PEERS})
  GROUP BY 1, 2)
SELECT utility_key, utility_name, utility_key = '19876|VA' AS is_dominion, n_saifi, n_saidi,
       saifi_all_2021_25, RANK() OVER (ORDER BY saifi_all_2021_25 DESC) AS saifi_all_rank,
       saidi_all_2023_25, RANK() OVER (ORDER BY saidi_all_2023_25 DESC) AS saidi_all_rank,
       saifi_ex_med_2021_25, RANK() OVER (ORDER BY saifi_ex_med_2021_25 DESC) AS saifi_ex_med_rank,
       saidi_ex_med_2023_25, RANK() OVER (ORDER BY saidi_ex_med_2023_25 DESC) AS saidi_ex_med_rank,
       MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saifi_all_2021_25 END) OVER () AS saifi_all_median_11,
       MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saidi_all_2023_25 END) OVER () AS saidi_all_median_11
FROM u ORDER BY saidi_all_2023_25 DESC"""
p = con.execute(PEER_ALL).df()
assert len(p) == 12 and (p.n_saifi == 5).all() and (p.n_saidi == 3).all()
dom = p[p.is_dominion].iloc[0]
ok3 = (round(dom.saifi_all_2021_25, 3), int(dom.saifi_all_rank), round(dom.saifi_all_median_11, 3),
       round(dom.saifi_ex_med_2021_25, 3), int(dom.saifi_ex_med_rank)) == (1.531, 6, 1.408, 1.211, 4)
ok11 = (round(dom.saidi_all_2023_25, 1), int(dom.saidi_all_rank), round(dom.saidi_ex_med_2023_25, 1), int(dom.saidi_ex_med_rank)) == (223.0, 9, 133.0, 4)
verdicts += [("N-3", "CONFIRMED" if ok3 else "CORRECTED"), ("N-4", "CONFIRMED (C5-1)")]
top3 = ", ".join(f"{r.utility_name} {r.saidi_all_2023_25:.0f}" for r in p.head(3).itertuples())
md += ["### N-3 and N-11 All-events ranks (no MED rule); N-4 ex-MED medians", "",
       f"**N-3 {verdicts[-2][1]}.** All-events SAIFI, mean of 2021-2025: Dominion **{dom.saifi_all_2021_25:.3f}, "
       f"{int(dom.saifi_all_rank)}th-highest of the 12**; median of the other 11 **{dom.saifi_all_median_11:.3f}**. Ex-MED: "
       f"{dom.saifi_ex_med_2021_25:.3f}, {int(dom.saifi_ex_med_rank)}th-highest (median of the 11: 0.934). So on all events the SAIFI rank moves "
       "from 4th to 6th of 12; Dominion stays above the median either way.", "",
       f"**N-11 {'CONFIRMED' if ok11 else 'CORRECTED'}.** All-events SAIDI, mean of 2023-2025: Dominion **{dom.saidi_all_2023_25:.1f} "
       f"minutes, {int(dom.saidi_all_rank)}th-highest of the 12** (median of the other 11: {dom.saidi_all_median_11:.1f}); ex-MED "
       f"{dom.saidi_ex_med_2023_25:.1f}, {int(dom.saidi_ex_med_rank)}th-highest. Highest all-events SAIDI: {top3}. Which storms put them "
       "there is not in this table, so \"hurricane-hit peers at the top\" stays an inference, as R marks it.", "",
       "**N-4 CONFIRMED** (findings § C5-1): 11-peer ex-MED medians SAIFI 0.934, CAIDI 99.5; 12-utility 0.964 and 105.0.", "",
       "| Utility | All-events SAIDI 2023-25 | Rank | Ex-MED SAIDI 2023-25 | Rank | All-events SAIFI 2021-25 | Rank | Ex-MED SAIFI 2021-25 | Rank |",
       "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
for r in p.itertuples():
    nm = f"**{r.utility_name}**" if r.is_dominion else r.utility_name
    md.append(f"| {nm} | {r.saidi_all_2023_25:.1f} | {r.saidi_all_rank} | {r.saidi_ex_med_2023_25:.1f} | {r.saidi_ex_med_rank} | "
              f"{r.saifi_all_2021_25:.3f} | {r.saifi_all_rank} | {r.saifi_ex_med_2021_25:.3f} | {r.saifi_ex_med_rank} |")
md += ["", "Ranks: 1 = highest of the 12. Every utility has all five (SAIFI) and all three (SAIDI) years.", ""]
md += sql_block(PEER_ALL)
verdicts.append(("N-11", "CONFIRMED" if ok11 else "CORRECTED"))

# ---------- N-5: reporting standard by utility and year ----------
Q5 = f"""SELECT d.utility_name, f.utility_key,
       COUNT(*) AS years,
       COUNT(CASE WHEN f.standard = 'IEEE 1366' THEN 1 END) AS ieee_years,
       STRING_AGG(CASE WHEN f.standard = 'Other' THEN CAST(f.year AS VARCHAR) END, ', ' ORDER BY f.year) AS other_years
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE f.utility_key IN ({PEERS})
GROUP BY 1, 2 ORDER BY ieee_years DESC, 1"""
Q5_BOTH = f"""-- before de-duplication: did any of the 12 file both standards in a year? (0 rows = no)
WITH s AS (
  SELECT utility_id || '|' || state AS utility_key, year, standard FROM stg.RELIABILITY_HIST
  UNION ALL
  SELECT utility_id || '|' || state, year, standard FROM stg.RELIABILITY_2025)
SELECT utility_key, year, COUNT(*) AS filings
FROM s WHERE utility_key IN ({PEERS})
GROUP BY 1, 2 HAVING COUNT(*) > 1"""
s5 = con.execute(Q5).df()
both = con.execute(Q5_BOTH).df()
always_ieee_14 = con.execute(f"""SELECT COUNT(*) FROM (
  SELECT utility_key FROM mart.FCT_RELIABILITY WHERE utility_key IN ({PEERS}) AND year BETWEEN 2014 AND 2025
  GROUP BY 1 HAVING COUNT(*) = 12 AND COUNT(CASE WHEN standard = 'IEEE 1366' THEN 1 END) = 12)""").fetchone()[0]
other_names = list(s5[s5.ieee_years == 0].utility_name)
changed = s5[(s5.ieee_years > 0) & s5.other_years.notna()]
ok5 = always_ieee_14 == 10 and len(other_names) == 2 and both.empty
verdicts.append(("N-5", "CONFIRMED" if ok5 else "CORRECTED"))
md += ["### N-5 Reporting standards in the peer set; docs/06 corrected", "",
       f"**{verdicts[-1][1]}.** In every year 2014-2025, **{always_ieee_14} of the 12 file under IEEE 1366**; Dominion and Alabama Power "
       f"file under \"Other\" in every year 2013-2025. In 2013 two more filed \"Other\": "
       f"{' and '.join(f'{r.utility_name}' for r in changed.itertuples())} (2013 only). No utility in the set filed both standards in "
       "any year, so the mart's de-duplication (keep the IEEE row) hides nothing here.", "",
       "**docs/06 was wrong.** \"Half the peers use a different reporting method\" fits no reading: one of the 11 peers (Alabama Power) "
       "shares Dominion's \"Other\" filing and ten use IEEE 1366. Corrected in the repo, commit 29b179f: the docs/06 headline now reads "
       "\"Ten of the twelve use IEEE 1366; Dominion and Alabama Power use their own rule\", and docs/05 explains the `Changed` label. "
       "No other repo file said \"half\" (docs/04 D2 \"Most large peers file under IEEE 1366\" and docs/05 \"Dominion, Alabama Power and "
       "some other utilities\" are right).", "",
       "**Where the pack stands (for B).** No slide, note, brief or question-sheet line quotes \"half the peers\": deck v2 slide 3 "
       "(\"Methods differ: Dominion uses its own (non-IEEE) major-event rule, most peers IEEE 1366\"), its notes, the brief v1 (\"Most of "
       "these peers use the IEEE 1366 method\") and the Power BI subtitle and alt text (\"most peers by IEEE 1366\") are right. What does "
       "need fixing: the brief v1 peer table and B's chart files `work/charts/v0/s3_peer_quadrant.csv` and `work/charts/v2/"
       "s3_peer_quadrant_v2*.csv` label **Georgia Power and Duke Energy Florida \"Mixed\"**; for the years compared (2015 on) both are "
       "IEEE 1366, so write \"IEEE 1366\" (footnote if wanted: \"Other\" in 2013 only). The same \"Changed\" label comes from the Power BI "
       "`Method` measure (next paragraph). Smaller: the public-variant CSVs carry CAIDI 2021-25 as SAIDI/SAIFI of the means (Georgia "
       "Power 113.6), the adopted one as the mean of annual CAIDI (114.2, as `peer_reliability_5yr.csv` and the DAX `CAIDI 5yr`); "
       "Dominion is 110.4 either way and its rank (6th) does not change.", "",
       "**Power BI side effect, for B.** The Fair comparison page filters peer groups only, so the `Method` measure (\"Major Storm Rule\" "
       "column) sees 2013-2025 and shows **\"Changed\" for Georgia Power and Duke Energy Florida** because of 2013 alone, although "
       "every number in that table comes from 2015 onward. Fix option (B's call): evaluate the measure on the compared years, e.g. "
       "`CALCULATE(DISTINCTCOUNT(FCT_RELIABILITY[STANDARD]), FCT_RELIABILITY[YEAR] >= 2015)`, or add a year >= 2015 filter to that "
       "table. Deck v2, its notes and the Power BI subtitle/alt text say \"most peers IEEE 1366\", which is right.", "",
       "| Utility | Years | IEEE 1366 years | \"Other\" years |", "|---|---:|---:|---|"]
for r in s5.itertuples():
    md.append(f"| {r.utility_name} | {r.years} | {r.ieee_years} | {r.other_years if isinstance(r.other_years, str) else '-'} |")
md += [""] + sql_block(Q5) + sql_block(Q5_BOTH)

# ---------- N-6, N-7: cross-references ----------
verdicts += [("N-6", "CONFIRMED (C5-2)"), ("N-7", "CONFIRMED, wording sharpened (C5-3)")]
md += ["### N-6 and N-7 Storm vs calm levels; 6,530 against 6,108", "",
       "**N-6 CONFIRMED** (findings § C5-2): storm 332.8 (95% CI 225.6 to 453.4) and calm 27.86 (23.09 to 33.22) customer-hours per "
       "1,000 customers; R's rounded 333 and 27.9 are fine.", "",
       "**N-7 CONFIRMED, with a wording fix** (findings § C5-3 has the query and the year table): 6,530 - 6,108 = 422 = **114** storm "
       "county-days in the four counties off the map **+ 308** with a failed EAGLE-I reading. In 2025 the gap is 791 - 677 = 114 as R "
       "says, but that 114 is 18 off-map + 96 failed-reading days; the off-map total over 2015-2025 is also 114, a coincidence that "
       "invites confusion. Suggested line: \"The 422 are 114 in the four counties left off the map and 308 days with failed EAGLE-I "
       "readings, 96 of them in 2025.\"", ""]

# ---------- N-8: co-op SAIFI denominators ----------
Q8 = """SELECT
  SUM(f.cust_interruptions_ex_med)
    / SUM(CASE WHEN f.cust_interruptions_ex_med IS NOT NULL THEN f.customers END) AS saifi_reporters_only,  -- V_GROUP_INDEX rule
  SUM(f.cust_interruptions_ex_med) / SUM(f.customers)                            AS saifi_all_members,
  SUM(CASE WHEN f.cust_interruptions_ex_med IS NULL THEN f.customers END)        AS customers_without_saifi,
  STRING_AGG(CASE WHEN f.cust_interruptions_ex_med IS NULL THEN d.utility_name END, ', ') AS without_saifi
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE d.peer_group = 'Virginia co-op' AND f.year = 2025"""
Q8_VIEW = "SELECT year, saifi_ex_med FROM mart.V_GROUP_INDEX WHERE peer_group = 'Virginia co-op' AND year = 2025"
r8 = con.execute(Q8).df().iloc[0]
v8 = con.execute(Q8_VIEW).fetchone()
ok8 = (round(r8.saifi_all_members, 3), round(r8.saifi_reporters_only, 3), int(r8.customers_without_saifi)) == (1.849, 1.887, 13341) \
    and round(float(v8[1]), 3) == 1.887
verdicts.append(("N-8", "CONFIRMED" if ok8 else "CORRECTED"))
md += ["### N-8 The co-op SAIFI denominator (P18)", "",
       f"**{verdicts[-1][1]}.** Virginia co-ops, 2025, SAIFI ex-MED: **{r8.saifi_reporters_only:.3f}** with the denominator limited to "
       f"utilities that reported interruptions (what `V_GROUP_INDEX` returns: {float(v8[1]):.3f}), **{r8.saifi_all_members:.3f}** if all "
       f"members' customers were counted. The difference is {int(r8.customers_without_saifi):,} customers of {r8.without_saifi}, which "
       "has no SAIFI for 2025 (P18: it filed SAIDI only). The fix date (27 Oct, commit 1635a8e) is R's citation; D did not re-check the commit.", ""]
md += sql_block(Q8) + sql_block(Q8_VIEW)

# ---------- N-9: not a data item ----------
verdicts.append(("N-9", "NOT CHECKED: not a data item"))
md += ["### N-9 Resume month counts", "",
       "**Not checked by D.** These come from the resume's dates, not from the data, and D does not read the resume. R or the "
       "orchestrator should confirm them with the candidate.", ""]

# ---------- summary ----------
md[4:4] = ["| Item | What | Verdict |", "|---|---|---|"] + [
    f"| {k} | {w} | {v} |" for (k, v), w in zip(sorted(verdicts, key=lambda kv: int(kv[0][2:])), [
        "2025 band 122.3-168.2 = 95% prediction interval", "Dominion \"Other\" 2013-25; auto-recorded from 2015",
        "All-events SAIFI 2021-25: 1.531, 6th of 12; 11-peer median 1.408", "Ex-MED 11-peer medians 0.934 and 99.5",
        "10 of 12 IEEE 1366 every year 2014-25; Dominion and Alabama Power \"Other\"", "Storm 332.8 vs calm 27.86",
        "6,530 - 6,108 = 422", "Co-op SAIFI 1.887 vs 1.849 (13,341 customers)", "Resume month counts",
        "All-events SAIDI 2023-25: 223.0, 9th of 12"])] + [""]
OUT.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
print(OUT)
for k, v in verdicts:
    print(k, v)
