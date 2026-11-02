"""Write V1_delta_v3.csv: the 5 added and 25 changed claims rows of v3, plus the one row whose result field changed
without announcement. Asserts that every added/changed id is present."""
import sys, csv
sys.stdout.reconfigure(encoding='utf-8')
RV = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
S = "v1_scripts/"
A = {}
def a(i, v, m, verdict, note=""): A[i] = (v, m, verdict, note)
# ---- added
a("C-S3-11P", "12-utility SAIFI median 0.9640 (own from raw inputs; origin/main workbook (0.934 + 0.994)/2); Dominion rank 4", S + "a20; a11 values; origin/main docs/05:87 prints 'SAIFI 0.96'; public S3 render viewed (v1_text_v3/s3_public_v3.png): label 'median of the 12 (including Dominion): 0.96'", "MATCH", "resolves V1 P1 for SAIFI")
a("C-B-05", "103 counties; 33 Dominion-only; 31 on the map (off: 51600 Fairfax city, 51660 Harrisonburg city)", S + "a20: data/output/county_outage_map_dominion_only.csv (33 rows, map_flag ok 31); a14: mart.DIM_COUNTY", "MATCH", "resolves V1 U1/I4")
a("C-S5-14", "image viewed: SAIFI +6% (1.244 -> 1.320 = +6.1%), CAIDI -9% (120.48 -> 109.39 = -9.2%), labels 1.24/1.17/1.32, 120.5/105.9/109.4, adjusted 122/136/133 (122.4/135.7/133.1), r 0.70 n 10; 46 kV from 2020", S + "x11: picture extracted from the v3 adopted PPTX (sha256 f5935575944b, identical to work/powerbi/b6/s5_summary_v3.png and to the brief HTML image); a20: PUDL highest_distribution_voltage_kv 34.5 (2019) -> 46.0 (2020); docs/03 P7, origin/main docs/05:65; the percentages and adjusted values are V1's own recomputation (V1_coverage U3)", "MATCH", "resolves V1 U3 for the adopted deck; the same SAIFI chart and numbers (+6%, 1.24, 1.17, 1.32) also appear in the new public S5 screenshot, which no public-variant row covers (see summary)")
a("C-B-06", "109.4 min = 1 h 49 min; 144.4 min = 2 h 24 min; 2.784 ~ 3; 1.320 ~ 1.3", "arithmetic on V1-verified values", "MATCH", "resolves V1 U6")
a("C-B-07", "verbatim: 'cycles typically ranging from four to five years'; 'Nearly all of our neighborhood power lines are cleared on a four year cycle'", S + "e10: v1_sources/dominion_tree_trimming_faq/page.html (opened 1 Nov 2026, HTTP 200)", "MATCH", "resolves V1 U2")
# ---- changed
a("C-S3-01", "1.211 rank 4; 11-peer median 0.934 (adopted only)", "V1 a11; v3 adopted S3 text unchanged; public deck no longer prints 0.93 as a median", "MATCH")
a("C-S3-02", "110.44 rank 6; 11-peer median 99.47", "V1 a11", "MATCH", "stale '104.85' note removed, as V1 asked")
a("C-S4-08", "11.944 (7.9-16.9); 12 = 11.944 rounded", "V1 a14", "MATCH", "resolves V1 U5")
a("C-S4-09", "9.856; 19.867 on 1,065 storm county-days in the 31 mapped Dominion-only counties; 5.888-27.428", "V1 a14 (Dominion-only subset n = 1,065)", "MATCH")
a("C-S5-04", "+26.0% (19,803 -> 24,957); +52.1% (7,167 -> 10,903)", "V1 a16; used_in change only", "MATCH", "used_in now lists brief p6 text and chart, as V1 asked (checked in the v3 brief text)")
a("C-S5-07", "+65.4%; customers +8.0% all service types, +7.9% bundled only", "V1 a16", "MATCH", "the row now states both bases; V1 ROUNDING resolved")
a("C-S6-02", "verbatim (as of November 30, 2023; 12 months; 32%)", "V1 e01 (R-036); v3 brief text: p8 'as of November 30, 2023', A1 '(Nov 2023)', Q8 '(Nov 30, 2023)'", "MATCH", "used_in change only; dated beside -44% as the row says")
a("C-S7-10", "T13-T31: 19 tests, all PASS", "V1 a17 (test_results.csv)", "MATCH")
a("C-S8-01", "'(20M+ rows)'", "resume, Mercury bullet 1 (V1); used_in change only", "MATCH", "used_in now lists brief A1 and Q16 and qsheet items 2, 11, 14 (V1's items 1, 11, 14 before the reorder); all present in the v3 text")
a("C-Q-03", "'from 71% to 90%'", "resume (V1); used_in change only", "MATCH", "used_in now lists brief A1 and Q17, as V1 asked; present in the v3 text")
a("C-Q-06", "'$690M and 440 investments'", "resume (V1); used_in change only", "MATCH", "used_in now lists brief A1, as V1 asked; present in the v3 text")
a("C-Q-08", "'Travel Up to 25%'", "V1 e01 (R-009); used_in change only", "MATCH", "used_in now lists brief A1, as V1 asked; present in the v3 text")
a("C-Q-10", "shareholder approval on 3 Sep 2026: NOT CHECKED (both SEC 8-K URLs returned HTTP 403 'Your Request Originates from an Undeclared Automated Tool'); other parts as V1 (VA order by 11 Jan 2027, close H2 2027, approvals list, announced 18 May 2026)", S + "e10: v1_sources/sec_8k_dominion_20260903, sec_8k_nextera_20260903 (block pages saved); no producer-saved copy of either 8-K exists", "UNVERIFIABLE", "UNVERIFIABLE-BLOCKED; not worked around (no custom agent string, no mirror). Printed in qsheet item 19 as 'on September 3'. A person can open the two EDGAR URLs in a browser to close it")
a("C-S3-02P", "12-utility CAIDI median 104.85 (origin/main workbook) / 104.96 (own) -> 105; Dominion rank 6", S + "a20; origin/main docs/05:87 prints 'CAIDI 105'; public S3 render viewed: label 'median of the 12 (including Dominion): 105 min'", "MATCH", "resolves V1 P1 for CAIDI")
a("C-S3-04P", "values as V1; labels now as origin/main workbook: Mixed (Georgia Power, Duke Energy Florida), Own method (Dominion, Alabama Power), IEEE 1366 (other 8)", S + "a20 (origin/main workbook Peers standard column); v3 public A6 table text", "MATCH", "resolves V1 P2 (labels)")
a("C-S3-07", "10 of 12 IEEE every year 2014-25 (true); now adopted only", "V1 a11; x12 scan: absent from the v3 public deck (slides, notes, PDF); brief tags it 'If adopted' (p4 caveat, A1) and Q2 'Adopted:'", "MATCH", "resolves V1 P2 (count)")
a("C-S3-09", "Georgia Power and Duke Energy Florida 'Other' in 2013 only, IEEE 1366 2014-25", "V1 a11 recount from data/input; the two reliability inputs equal origin/main's (git diff --quiet origin/main, exit 0); v3 public A6 source text", "MATCH", "variant 'both': the public use is supported by origin/main's committed inputs and its workbook 'Mixed' label, but the row's source cites only D findings.md C6, not origin/main")
a("C-S4-05P", "printed 125.9/124.4/128.2 = origin/main workbook StormIndex predicted 125.94/124.44/128.25", "V1 a13 (git show origin/main workbook)", "MATCH", "now cites the workbook column; V1 ROUNDING (P3) resolved")
a("C-S4-20", "31 mapped Dominion-only 159.2 vs 68 shared 211.1 (customer-weighted)", "V1 a14", "MATCH", "'customer-weighted' now printed (brief p5)")
a("C-S5-11", "cards 2.68M, 144.4, 'Minutes per interruption' 109.4, 1.320, 53%", S + "x11: v3 adopted S5 picture viewed (= work/powerbi/b6/s5_summary_v3.png = brief image)", "MATCH", "resolves V1 I2 in the deck alt text, the screenshot card and brief p7")
a("C-S5-12", "Selected SAIDI VAR form present verbatim", S + "a20: powerbi/measures.dax lines 401-403, in the working tree and at the cited commit 859b52d (git show)", "MATCH", "the cite 400-402 is off by one: line 400 is '// Format: 0.0' and the RETURN line 403 falls outside it; the path is now right (V1 register hygiene)")
a("C-S7-05A", "31 PASS = 12 original build (T1-T6 reliability, T7-T9 NOAA storms, T10-T12 EIA-930 demand) + 19 new (T13-T31)", "V1 a17 (test_results.csv sql_file); v3 adopted S6 badge, source, notes and A4 text", "MATCH", "resolves V1 MISMATCH (I1)")
a("C-S6-06", "verbatim: 'The program has reduced average annual outage time by 44% for customers in these areas' (release dated 06/08/2026, RICHMOND, Va.--BUSINESS WIRE)", S + "e10: v1_sources/dominion_release_20260608/page.html (investors.dominionenergy.com, HTTP 200)", "MATCH", "resolves V1 UNVERIFIABLE; company-reported, no baseline stated, as the row says")
a("C-B-03", "years incl. 2015, 2017, 2018 and r .42, .20, -.11, -.19 now in the value list; all confirmed (Crossref/OpenAlex) except Powell -.19 (register only)", "V1 e01/e02", "MATCH", "resolves V1 U4")
a("C-B-01", "adopted 1,028 words: 0:35 1:11 0:57 1:04 0:54 1:17 0:56 1:00 = 7:54; public 994 words: 0:32 1:11 0:54 0:57 0:57 1:12 0:56 0:59 = 7:38", S + "a20: whitespace word counts of the v3 PPTX notes, slides 1-8, 130 wpm, seconds rounded half-up and summed", "MATCH", "resolves V1 I3")
# ---- unannounced (result field only)
a("C-S4-04P", "104.3732 + 0.051375 x; R2 0.4840 (not printed on origin/main)", "V1 a12; only the result field changed (not announced)", "MATCH", "unannounced change, non-key field only")
import csv as _c
old = {r["id"]: r for r in _c.DictReader(open(RV + r"\snapshot_v2_1035\claims.csv", encoding="utf-8"))}
new = {r["id"]: r for r in _c.DictReader(open(RV + r"\snapshot_v3_audit\claims.csv", encoding="utf-8"))}
need = [i for i in new if i not in old] + [i for i in new if i in old and any(new[i][f] != old[i][f] for f in new[i])]
assert set(need) == set(A), (set(need) ^ set(A))
with open(RV + r"\V1_delta_v3.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "checked_value", "method", "verdict", "note"])
    for i in A: w.writerow([i, *A[i]])
from collections import Counter
print("rows:", len(A), Counter(v[2] for v in A.values()))
