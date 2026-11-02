"""Write interview-prep/claims_v3.csv for the v3 pack (the final candidate) and check it per variant (B owns the file).

v3 = the v2 rows (built below exactly as build_claims_v2.py builds them) plus ruling O-33 from the V1 number audit,
applied in V3_U / V3_NEW at the end of the row lists: public S3 cites origin/main docs/05 (medians of the 12, 0.96 and
105) and the workbook's "Mixed" labels; "10 of 12" is adopted-only; the test split (C-S7-05A); CAIDI is "minutes per
interruption"; the coverage rows U1-U6 and the used_in gaps; C-S5-12, C-S4-20, C-S4-04P, C-S4-05P, C-S5-07 notes;
C-Q-10, C-S6-06 and the trim cycle re-sourced by R (research/V1_followups.md). The v2 file, claims.csv, is left in
place. The checks below run on the v3 deliverables.

v2 adds a `variant` column: which deck build a row's text appears in (both | adopted | public). Rows used only in
the brief or the question sheet are `both` (those two documents are variant-neutral; the brief tags upgrade
material "If adopted"). The v1 rows (build_claims.py) are the base: kept, updated, split or retired below.

Checks, for each deliverable (adopted deck, public deck, brief, question sheet):
  1. coverage: every number printed (slides, tables, notes, brief, sheet) is covered by a row whose variant applies
     (adopted deck: both|adopted; public deck: both|public; brief and sheet: any row), apart from years, slide and
     page numbers, small counts and the ignore list;
  2. exact_text: every row's exact_text appears in at least one deliverable its variant applies to;
  3. stale values: pre-D22 storm counts never print in the adopted deck, upgrade numbers never print in the public
     deck;
  4. public findability: every number in the public deck is looked up on origin/main (work/v2/origin_main_corpus.py)
     and anything not findable is listed (derived arithmetic is allowed, and reported).

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\claims\\build_claims_v3.py
"""
from __future__ import annotations

import csv
import datetime as dt
import html as htmllib
import io
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "v2"))
import ds  # noqa: E402
import build_claims as c1  # noqa: E402  (the v1 rows)

IP = ds.REPO / "interview-prep"
DECK_A = IP / "deliverables" / "01_deck" / "Dominion_reliability_deck_v3.pptx"
DECK_P = IP / "deliverables" / "01_deck" / "Dominion_reliability_deck_v3_public.pptx"
BRIEF = IP / "deliverables" / "03_interview_brief" / "Dominion_interview_brief_v3.html"
QSHEET = IP / "deliverables" / "02_question_sheet" / "Dominion_question_sheet_v3.html"
OUT_CSV = IP / "claims_v3.csv"
HEADER = ["id", "exact_text", "value", "unit", "used_in", "source", "producer", "checked_by", "result", "variant"]
D, R, B, CV = "D", "R", "B", "resume"
CH2 = ds.WORK / "charts" / "v2"
CH3 = ds.WORK / "charts" / "v3"
WPM = 130


def origin_main_csv(path: str):
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show", f"origin/main:{path}"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw)))


def peer_values(variant: str) -> str:
    rows = list(csv.DictReader(open(CH2 / f"s3_peer_quadrant_v2_{variant}.csv", encoding="utf-8")))
    vals = []
    for d in rows:
        s, c, a = float(d["saifi_5yr_2021_25"]), float(d["caidi_5yr_2021_25"]), float(d["saidi_3yr_2023_25"])
        vals += [f"{s:.2f}", f"{c:.0f}", f"{a:.0f}"] + ([f"{c:.1f}", f"{a:.1f}"] if variant == "adopted" else [])
    return ";".join(vals)


def a2_public_values() -> str:
    """Public A2: storm county-days and SAIDI from origin/main storm_vs_saidi.csv; 'From the fit' from the public
    workbook's StormIndex sheet (predicted_saidi_from_weather), as the deck prints it."""
    import openpyxl
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show",
                          "origin/main:powerbi/Dominion_Reliability_PowerBI_Data.xlsx"], capture_output=True,
                         check=True).stdout
    ws = openpyxl.load_workbook(io.BytesIO(raw), data_only=True, read_only=True)["StormIndex"]
    wrows = list(ws.iter_rows(values_only=True))
    iy, ip = wrows[0].index("year"), wrows[0].index("predicted_saidi_from_weather")
    pred = {int(r[iy]): float(r[ip]) for r in wrows[1:] if r[iy] is not None}
    rows =[r for r in origin_main_csv("data/output/storm_vs_saidi.csv") if 2015 <= int(r["year"]) <= 2025]
    vals = []
    for r in rows:
        cd, sd = float(r["storm_county_days"]), float(r["saidi_ex_med"])
        vals += [f"{cd:,.0f}", f"{sd:.1f}", f"{pred[int(r['year'])]:.1f}"]
    return ";".join(vals)


def a6_values() -> str:
    rows = list(csv.DictReader(open(ds.REPO / "data" / "output" / "outage_events_top10.csv", encoding="utf-8")))
    vals = []
    for e in rows:
        d = dt.date.fromisoformat(e["peak_day"])
        vals += [str(d.day), f"{float(e['peak_customers_out']):,.0f}", f"{float(e['peak_sustained_1h']):,.0f}",
                 f"{float(e['hours_to_90pct']):.1f}"]
    return ";".join(vals + ["100", "20", "66", "558,729"])


# ----------------------------------------------------------------------------- v1 rows: updates and retirements
RETIRE = {
    "C-S3-03": "replaced by C-S3-10 ('Dominion and 11 peers'; G2)",
    "C-A1-02": "0.125 ÷ 0.158 no longer printed (public rule; A1 says it in words)",
    "C-A3-04": "MED minutes by year no longer printed (v2 A1 is definitions + the 2025 MED share)",
    "C-A3-05": "the MED stacked-column chart is not in v2",
    "C-S7-06": "'22 decisions' replaced by the D-range constants (C-S7-06A adopted, C-S7-06P public; V2 F13)",
    "C-S8-03": "S8 strip v2: F10/F11 resume-true strip; 'Validation and reconciliation' no longer printed",
    "C-S8-05": "S8 strip v2: three items; 'Requirements with operations and IT' no longer printed",
    "C-Q-12": "V2 F7: no discovery story on the sheet; Q13 uses D13 (C-Q-15)",
    "C-S4-14": "the S4 county map + inset chart is not in v2; the brief map is C-S4-22",
}
U = {  # id: {field: new value}
    "C-S1-01": dict(exact_text="November 3, 2026", used_in="deck S1 (both); brief cover; qsheet header (Tuesday, "
                    "November 3, 2026)", result="match; US date (O-30)"),
    "C-S2-01": dict(used_in="deck S1-S2, S6, notes (both); brief p2, p3, A1; qsheet O2, C1"),
    "C-S2-02": dict(used_in="deck S2, S6 public badge, A4 (both); brief p2, p3, p7, A1; qsheet O2, C1"),
    "C-S2-03": dict(used_in="deck S2 left column, chart, notes (both); brief p2, p3, A1"),
    "C-S2-04": dict(value="1.199;1.320;1.3", used_in="deck S2 chart, alt text, notes, A1 (both); brief p2, A1, "
                    "hard 25 Q24 ('about 1.3 times')"),
    "C-S2-05": dict(used_in="deck S2 chart, notes (both); brief p2, p3, A1; qsheet U3 ('SAIFI rose 10%', 'storm "
                    "county-days rose about 10%')"),
    "C-S2-06": dict(used_in="deck S2 chart (both); brief A1"),
    "C-S2-07": dict(used_in="deck S2 chart, notes (both); brief p2, p3, A1; qsheet U3 ('fell 4%')"),
    "C-S2-08": dict(used_in="deck S2 chart (both); brief p3 table"),
    "C-S2-09": dict(exact_text="only edges", value="1.320;1.303",
                    used_in="deck S2 notes (both); brief p2, p3, A1",
                    result="match; G2: the 13-year SAIFI line is dropped from the slide, the thin margin is in notes"),
    "C-S2-10": dict(used_in="deck A1 (both); brief p2, p3, A1"),
    "C-S2-13": dict(used_in="brief p2 (tagged If adopted; public-only says 'no clear trend' without p-values)",
                    source="scripts/trend_tests.py (D commit 94eb5e2, local branch); D findings.md S2.3"),
    "C-S2-15": dict(used_in="deck S2 notes (both); brief p3; qsheet U3 (closing words, quoted)"),
    "C-S2-16": dict(exact_text="718 → 791", value="718;791", unit="storm county-days (2022 → 2025, after D22)",
                    used_in="deck S2 chart and notes (adopted); brief p3 source, A1",
                    source="D findings.md C5-4; data/output/storm_vs_saidi.csv (after D22)", variant="adopted"),
    "C-S3-01": dict(exact_text="4th highest of the 12 (peer median 0.93)", value="1.21;0.93;0.934",
                    unit="SAIFI 2021-25 mean; median of the 11 peers",
                    used_in="deck S3 (both), alt text, notes; brief p2, p4, A1",
                    source="D findings.md C5-1 (adopted: peer_reliability_5yr.csv median_saifi_2021_25_excl_dominion "
                    "0.934, commit 7133aba); public: origin/main workbook Peers sheet, 6th of the 11 peers' values "
                    "(Alabama Power 0.934)", result="match in both variants"),
    "C-S3-02": dict(exact_text="mid-pack, 6th of the 12 (peer median 99.5)", value="110;99.5",
                    unit="CAIDI 2021-25 mean; median of the 11 peers", used_in="deck S3 (adopted); brief p4, A1",
                    source="D findings.md C5-1: median_caidi_2021_25_excl_dominion 99.5 (BGE), commit 7133aba",
                    variant="adopted"),
    "C-S3-04": dict(exact_text="[chart and table] peer quadrant (adopted S3) and the brief's peer table",
                    value=peer_values("adopted"), used_in="deck S3 chart (adopted); brief p4 chart and table",
                    source="data/output/peer_reliability_5yr.csv (D batch 5); method labels: workbook Peers sheet with "
                    "Georgia Power and Duke Energy Florida relabeled IEEE 1366 (D batch 6, N-5)", variant="adopted"),
    "C-S3-05": dict(exact_text="its 3-year SAIDI, 133.0, is 4th", used_in="brief p4; A1 ('133.0 · 4th of 12')"),
    "C-S3-06": dict(used_in="deck S3 source, A6 public source (both); brief p4, p7"),
    "C-S4-01": dict(used_in="deck A2 table (adopted); brief p5, A1", variant="adopted",
                    source="D findings.md C5-4; data/output/storm_vs_saidi.csv (2024 464, 2025 791, after D22)"),
    "C-S4-02": dict(used_in="deck S4 (public), A2 (both), notes; brief p2, p5, A1"),
    "C-S4-03": dict(exact_text="145.3", used_in="deck A2 (both), S4 public, notes; brief p5, A1",
                    source="D findings.md C5-6 (adopted: 104.2616 + 0.051820 x 791 = 145.25); public: origin/main "
                    "storm_vs_saidi.csv fit 104.3732 + 0.051375 x 796 = 145.27"),
    "C-S4-04": dict(used_in="deck A2 (adopted)", variant="adopted"),
    "C-S4-05": dict(used_in="deck A2 table (adopted)", variant="adopted"),
    "C-S4-15": dict(exact_text="95% CI 0.12 to 0.92", used_in="deck A2 and notes (adopted); brief A1 (tagged If "
                    "adopted), hard 25 Q1 (its public-only line: 'no p, CI or prediction interval'); not Q22 (proof "
                    "review fix 7)", variant="adopted",
                    result="match; public data gives the same CI (r 0.6957, n 10: 0.12 to 0.92), but it is not printed "
                    "on origin/main, so it stays upgrade-only"),
    "C-S4-06": dict(exact_text="+0.34 minutes a year, 95% CI −1.41 to +2.08, p = 0.67",
                    used_in="brief p2 (tagged If adopted)",
                    source="scripts/trend_tests.py (D commit 94eb5e2); D findings.md Q10 check (CI -1.41 to +2.08 "
                    "after D22)"),
    "C-S4-08": dict(exact_text="95% CI 7.9–16.9", value="11.9;7.9;16.9;2,000",
                    used_in="deck S4 (adopted), notes; brief p2, p5, A1", variant="adopted",
                    source="D findings.md C5-2; data/output/storm_vs_calm.csv row 1 (commit c0b2ea2), ratio_label "
                    "'11.9 (7.9 to 16.9)'; 2,000 resamples of whole days"),
    "C-S4-09": dict(exact_text="Holds on non-major days (9.9×), in Dominion-only counties (19.9×)",
                    used_in="deck S4 (adopted), notes; brief p5, A1", variant="adopted",
                    source="D findings.md C5-2 (storm_vs_calm.csv rows 2-3)"),
    "C-S4-10": dict(used_in="deck S4 source (adopted), A2 notes; brief p5, A1", variant="adopted",
                    value="6108;99;103",
                    source="D findings.md C5-3: 'storm county-days with complete outage readings, 2015-2025, 99 "
                    "counties on the map (EAGLE-I)'"),
    "C-S4-11": dict(exact_text="range from 55 minutes a year (Prince William County) to 633",
                    used_in="brief p5 (tagged If adopted); brief map labels"),
    "C-S4-12": dict(exact_text="33.5 hours from the peak to clear 90% of the outage", value="33.5;90",
                    used_in="deck A6 chart title, alt text, notes (adopted); brief p5",
                    source="data/output/outage_events_top10.csv (ISAIAS hours_to_90pct 33.5); P4 final wording "
                    "(orchestrator, after 09:35): share cleared = (peak - customers out) / (peak - pre-event level)",
                    variant="adopted"),
    "C-S4-13": dict(exact_text="+4.6% a year after allowing for size, p = 0.07", value="4.6;0.07;47;50,000",
                    used_in="deck A6 notes (adopted, 'plus 4.6 percent a year, p = 0.07'); brief p5",
                    variant="adopted"),
    "C-A6-01": dict(exact_text="[table] A6 ten largest outage events (Peak, Held 1 h, Hours to clear 90%)",
                    value=a6_values(), used_in="deck A6 table and notes (adopted)", variant="adopted",
                    source="data/output/outage_events_top10.csv (peak_customers_out, peak_sustained_1h, "
                    "hours_to_90pct); P4 wording (orchestrator 09:33 and after)"),
    "C-A1-01": dict(used_in="deck A1 (both); qsheet U1"),
    "C-A3-01": dict(used_in="deck A1, A4 (both); brief p7, A1; qsheet U2"),
    "C-A3-02": dict(used_in="deck A1 (both); brief A1, p7 caption; qsheet U2"),
    "C-A3-03": dict(used_in="brief A1; qsheet U2 ('162.3 of 306.7')"),
    "C-S5-01": dict(used_in="deck A3 (adopted), notes; brief p6", variant="adopted"),
    "C-S5-02": dict(used_in="deck A3 (both), notes; brief p6"),
    "C-S5-03": dict(exact_text="25,413", value="25,413;25,384",
                    used_in="deck A3 tile (adopted); brief p6 (tagged If adopted)", variant="adopted"),
    "C-S5-04": dict(exact_text="+26%", value="26;52;19,803;24,957;7,167;10,903",
                    used_in="deck A3 (both: 'Highest hour of the year +26%, lowest hour +52%'); brief p6, A1"),
    "C-S5-05": dict(used_in="deck A3 chart (adopted)", variant="adopted"),
    "C-S5-08": dict(used_in="deck A3 notes (adopted); brief p6 (tagged If adopted)", variant="adopted"),
    "C-S5-09": dict(exact_text="Oct 29", used_in="deck A3 source (adopted); brief p6 ('2026 to October 29')",
                    variant="adopted"),
    "C-S6-01": dict(exact_text="99.8% of meters", used_in="deck S7 card (both); brief p8, A1"),
    "C-S6-02": dict(exact_text="32% reduction in outage minutes on feeders hardened for at least 12 months (as of "
                    "November 30, 2023)", value="32;-32", used_in="brief p8, A1 ('−32%'), hard 25 Q8",
                    result="match; US date (O-30)"),
    "C-S6-04": dict(exact_text="Four programs", used_in="brief p8", result="match; US spelling (O-30)"),
    "C-S6-05": dict(exact_text="2.7M customer-minutes", value="2.7", used_in="brief A1"),
    "C-S7-01": dict(used_in="deck S6, A4 (both); brief p7, A1"),
    "C-S7-02": dict(used_in="deck S6, A4 (public); brief p7, A1", variant="public",
                    source="origin/main docs/01 (EIA-930 6,077,232 rows, July 2018 to 22 Oct 2026)"),
    "C-S7-03": dict(used_in="deck S6 (both); brief p7, A1"),
    "C-S7-05": dict(used_in="deck S6 badge (public); brief p7, A1", variant="public"),
    "C-S7-07": dict(used_in="deck A4, S6 notes public (both); brief p7, A1"),
    "C-S7-10": dict(exact_text="T13–T31 on the county outage, storm and load tables",
                    used_in="deck S6 source, A4 (adopted); brief p7, A1, hard 25 Q15", variant="adopted"),
    "C-S7-11": dict(used_in="deck S6 badge, A4, notes (adopted); brief p7, A1", variant="adopted"),
    "C-S7-12": dict(value="11608442;15;11.6;0.25", used_in="deck S6, A4 (adopted); brief p7, A1, hard 25 Q15 "
                    "('11.6M rows'; 'customers out × 0.25', a 15-minute reading in hours; the question is tagged "
                    "Adopted)", variant="adopted"),
    "C-S8-01": dict(used_in="deck S8 strip (both)"),
    "C-S8-02": dict(used_in="deck S8 strip (both): '→ what I'd do with cause codes in the first 90 days' (V2 F11: "
                    "future and conditional; the project has no cause codes)"),
    "C-S8-04": dict(used_in="deck S8 strip (both)"),
    "C-S8-06": dict(used_in="deck S8 source (both)"),
}

NEW = [
    # S2
    dict(id="C-S2-16P", exact_text="723 → 796", value="723;796", unit="storm county-days (2022 → 2025, before D22)",
         used_in="deck S2 chart (public); brief p3 source, A1", source="origin/main data/output/storm_vs_saidi.csv",
         producer=D, checked_by=B, result="match (origin/main tier A)", variant="public"),
    dict(id="C-S2-18", exact_text="2.8", value="2.8", unit="minutes (rise in the 3-year average)",
         used_in="deck S2 left column ('Rebuilt from EIA-861: 130.2 → 133.0'), notes (both); brief p2, p3, A1",
         source="133.0 - 130.2; (144.4 - 136.0) / 3 = 2.8", producer=B, checked_by=B, result="match", variant="both"),
    # S3
    dict(id="C-S3-02P", exact_text="mid-pack, 6th of the 12 (peer median 99.3)", value="110;99.3",
         unit="CAIDI 2021-25; median of the 11 peers (workbook)", used_in="deck S3 (public); brief p4 source note, A1",
         source="origin/main workbook Peers sheet: CAIDI from the 5-year means; 6th of the 11 peers' values (BGE and "
         "PECO 99.3)", producer=B, checked_by=B, result="match; derived from origin/main values", variant="public"),
    dict(id="C-S3-04P", exact_text="[chart and table] peer quadrant (public S3) and the A6 peer table",
         value=peer_values("public"), unit="SAIFI, CAIDI, SAIDI", used_in="deck S3 chart, A6 table (public)",
         source="origin/main powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers; method labels fixed per D "
         "batch 6 (N-5)", producer=D, checked_by=B, result="match", variant="public"),
    dict(id="C-S3-07", exact_text="10 of the 12 file IEEE 1366 every year 2014–25", value="10;12",
         unit="utilities", used_in="deck A6 source (public); brief p4, A1",
         source="D findings.md C6 N-5 (EIA-861 standard field); Dominion and Alabama Power file 'Other'",
         producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S3-08", exact_text="1.531", value="1.531;1.408;223.0;6;9", unit="all-events SAIFI 2021-25, median of "
         "the other 11; all-events SAIDI 2023-25; ranks", used_in="brief p4, A1 (answers only, not the slides)",
         source="D findings.md C6 N-3, N-11", producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S3-09", exact_text="filed “Other” in 2013 only", value="2013", unit="year",
         used_in="deck A6 source (public); brief p4", source="D findings.md C6 (batch 6 message, item 1)",
         producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S3-10", exact_text="Dominion and 11 peers", value="12;11", unit="utilities",
         used_in="deck S3 source, alt text, A6 title (both); brief p4, A1",
         source="docs/04 D10 (commit 7133aba adds 'so the twelve are Dominion and 11 peers'); D findings.md C5-1",
         producer=D, checked_by=B, result="match", variant="both"),
    # S4
    dict(id="C-S4-01P", exact_text="465 → 796", value="465;796", unit="storm county-days, 2024 → 2025 (before D22)",
         used_in="deck S4 (public), A2 table; brief p5, A1", source="origin/main data/output/storm_vs_saidi.csv",
         producer=D, checked_by=B, result="match (origin/main tier A)", variant="public"),
    dict(id="C-S4-04P", exact_text="SAIDI = 104.4 + 0.0514 × storm county-days", value="104.4;0.0514;0.48",
         unit="fit coefficients; R²", used_in="deck A2 (public), S4 chart note",
         source="origin/main docs/02:130, docs/08:131; OLS on origin/main storm_vs_saidi.csv 2015-2024",
         producer=D, checked_by=B, result="match", variant="public"),
    dict(id="C-S4-05P", exact_text="[table] A2 public: storm county-days, SAIDI ex-MED, from the fit, 2015-2025",
         value=a2_public_values(), unit="county-days; minutes", used_in="deck A2 table (public)",
         source="origin/main data/output/storm_vs_saidi.csv; fit 2015-2024 as printed", producer=B, checked_by=B,
         result="match", variant="public"),
    dict(id="C-S4-06A", exact_text="+0.3 minutes a year (95% range −1.4 to +2.1)", value="0.3;-1.4;2.1",
         unit="min/yr", used_in="deck A2 (adopted)", source="scripts/trend_tests.py (D commit 94eb5e2): +0.34, 95% CI "
         "-1.41 to +2.08", producer=D, checked_by=B, result="match at one decimal", variant="adopted"),
    dict(id="C-S4-16", exact_text="5.9", value="5.9;27.4", unit="ratio range across years",
         used_in="deck S4 notes (adopted); brief p5, A1", source="D findings.md C5-2 (every year 5.9 in 2025 to 27.4 "
         "in 2020; every interval above 1)", producer=D, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S4-17", exact_text="332.8", value="332.8;27.9;27.86;225.6;453.4;23.1;33.2;333;28;1,000",
         unit="outage customer-hours per 1,000 customers per county-day (95% intervals)",
         used_in="deck S4 chart, alt text, notes (adopted); brief p5, A1",
         source="D findings.md C5-2; data/output/storm_vs_calm.csv row 1 (commit c0b2ea2)", producer=D, checked_by=B,
         result="match", variant="adopted"),
    dict(id="C-S4-18", exact_text="6,530", value="6,530;422;114;308;96;74;6,108",
         unit="storm county-days: all (103 counties) and the panel (99 counties); the gap", used_in="deck S4 source "
         "('2025: 74% of county-days') (adopted); brief p5, A1", source="D findings.md C5-3, C6 N-7",
         producer=D, checked_by=B, result="match; labels as D's hand-off", variant="adopted"),
    dict(id="C-S4-19", exact_text="122.3", value="122.3;168.2;133.9;156.6;122;168", unit="minutes: 95% prediction "
         "interval for 2025; 95% CI of the line", used_in="deck A2 and notes ('about 122 to 168') (adopted); brief "
         "p5, A1, hard 25 Q1 ('about 122–168')",
         source="D findings.md C6 N-1 (named a prediction interval; never a confidence interval)", producer=D,
         checked_by=B, result="match; the public fit gives 122.2 to 168.3, so 'about 122–168' holds in both",
         variant="adopted"),
    dict(id="C-S4-24", exact_text="DOE-417 lists 508,000 customers affected in Virginia", value="508,000",
         unit="customers (DOE-417, Isaias)", used_in="deck A6 notes (adopted)",
         source="D findings.md A2 (DOE-417 508,000)", producer=D, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S4-20", exact_text="average 159 minutes a year, against 211 in the 68", value="31;159;211;68",
         unit="counties; minutes a year (non-major days, 2015-2024)", used_in="brief p5 (tagged If adopted)",
         source="D findings.md C5-5 (county_outage_map_dominion_only.csv, commit 4fc9939): a comparison of places",
         producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S4-21", exact_text="351,738", value="351,738", unit="customers out at the peak (Isaias)",
         used_in="deck A6 table (adopted); brief p5", source="data/output/outage_events_top10.csv", producer=D,
         checked_by=B, result="match", variant="adopted"),
    dict(id="C-S4-22", exact_text="[chart] brief county map, all utilities: classes and labels",
         value="150;250;350;500;55;633;99", unit="minutes per customer a year", used_in="brief p5 map",
         source="data/output/county_outage_map.csv (map_flag ok, 99 counties); charts/v2/b_county_map_all_utilities",
         producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S4-23", exact_text="(r = 0.70 over ten years)", value="0.70;10", unit="r; years",
         used_in="deck S4 title (public); brief p2", source="origin/main docs/02:130; storm_vs_saidi.csv 2015-2024",
         producer=D, checked_by=B, result="match", variant="public"),
    # S5 (new slide) and the Power BI page
    dict(id="C-S5-01P", exact_text="4 a.m. +41%; 4 p.m. +27%", value="41;27", unit="% load growth 2019 → 2025 at 4 a.m., 4 p.m.",
         used_in="deck A3 chart and tile (public); brief p6 chart and text, A1",
         source="origin/main docs/05:97 (4am +41%, 4pm +27%); dom_load_profile.csv", producer=D, checked_by=B,
         result="match", variant="public"),
    dict(id="C-S5-10", exact_text="18 tables", value="18;11;31", unit="tables; report pages; tests",
         used_in="deck S5 (adopted), notes; brief p7, A1",
         source="orchestrator 09:33 (the verified template: 18 tables through one DataFolder parameter; 11 pages; "
         "Data notes 31 tests, 12 of 12)", producer=B, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S5-11", exact_text="2.68M", value="2.68;144.4;109.4;1.320;53",
         unit="Power BI Summary cards, 2025", used_in="deck S5 screenshot and alt text (adopted); brief p7, A1",
         source="work/powerbi/b5/shots_v4/crop_p01.png (real Desktop render, 09:33); 2,675,735 customers (EIA-861)",
         producer=B, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S5-12", exact_text="SELECTEDVALUE('Dashboard Year'[Year], 2025)", value="text", unit="DAX",
         used_in="deck S5 code (adopted); brief p7; qsheet T3",
         source="deliverables/04_powerbi/measures.dax Selected SAIDI (VAR form, as in the candidate's .pbix; V2 F22)",
         producer=B, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S5-13", exact_text="FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025}", value="text", unit="DAX",
         used_in="deck S5 code (public)", source="origin/main powerbi/measures.dax (SAIDI 3yr ending 2025)",
         producer=B, checked_by=B, result="match", variant="public"),
    # S6 constants
    dict(id="C-S7-02A", exact_text="6,094,320", value="6,094,320", unit="rows (EIA-930, values to 29 Oct 2026)",
         used_in="deck S6, A4 (adopted); brief p7, A1", source="D hand-off batch 3 (08:41); local docs/01 S8",
         producer=D, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S7-05A", exact_text="31 tests pass", value="31;12;19", unit="tests (12 on the reliability mart)",
         used_in="deck S6 badge, notes (adopted); brief p7", source="data/output/test_results.csv (T1-T31 PASS)",
         producer=D, checked_by=B, result="match", variant="adopted"),
    dict(id="C-S7-06A", exact_text="D1–D22", value="22", unit="decisions logged", used_in="deck S6 badge, source "
         "(adopted); brief p7, A1", source="docs/04_decisions.md (local branch, D1-D22); V2 F13", producer=D,
         checked_by=B, result="match", variant="adopted"),
    dict(id="C-S7-06P", exact_text="D1–D14", value="14", unit="decisions logged", used_in="deck S6 badge, source "
         "(public); brief p7, A1", source="origin/main docs/04_decisions.md (D1-D14); V2 F13", producer=D,
         checked_by=B, result="match", variant="public"),
    dict(id="C-S7-13", exact_text="55,524", value="55,524;3,702;309,504;1851", unit="rows (HURDAT2, DOE-417, CPC "
         "degree days); HURDAT2 starts in 1851", used_in="deck A4 (adopted); brief p7 sources table (DOE-417 "
         "2014–2025, proof review fix 5)", source="D hand-off batch 3 (08:41); docs/01_sources.md S18 (DOE-417 "
         "2014 to 2025)", producer=D, checked_by=B, result="match", variant="adopted"),
    # question sheet
    dict(id="C-Q-13", exact_text="1.849 → 1.887", value="1.849;1.887;13,341", unit="co-op SAIFI 2025; customers",
         used_in="qsheet B4 (Q7); brief A1, hard 25 Q17", source="docs/03 P18; commit 1635a8e (27 Oct, the "
         "candidate's); D findings.md C6 N-8", producer=D, checked_by=B, result="match; V2 F8", variant="both"),
    dict(id="C-Q-14", exact_text="three days in the office, two remote", value="3;2", unit="days",
         used_in="qsheet R5; brief p8, A1 ('3-2')", source="R role brief (posting: hybrid 3 days in office, 2 remote)",
         producer=R, checked_by=B, result="match", variant="both"),
    dict(id="C-Q-15", exact_text="DirectQuery against Snowflake during development, Import for presentation "
         "(decision D13)", value="text", unit="text", used_in="qsheet T7 (Q13); deck S5 public, S6 public; brief p7",
         source="docs/04_decisions.md D13 (origin/main)", producer=D, checked_by=B, result="match; V2 F7",
         variant="both"),
    dict(id="C-Q-16", exact_text="about 38 months since April 2022", value="38;10;28;19;9;7;3",
         unit="months", used_in="brief hard 25 Q20",
         source="the resume's role dates, paraphrased in R hard25_answers.md N-9 (data titles 7 + 3; Cofoods BD 19; "
         "finance internships April to December 2022, 9)", producer=R, checked_by=B,
         result="match: 7 + 3 + 19 + 9 = 38; earliest role April 2022", variant="both"),
    # brief: research and Dominion's own statements (R)
    dict(id="C-S2-19", exact_text="Single years have ranged from 117 to 150", value="117;150;117.4;149.9",
         unit="minutes (SAIDI ex-MED, 2015-2025)", used_in="brief hard 25 Q4",
         source="data/output/storm_vs_saidi.csv (2017 117.4, the lowest; 2019 149.9, the highest; same on "
         "origin/main)", producer=D, checked_by=B, result="match", variant="both"),
    dict(id="C-S6-06", exact_text="−44% (2026)", value="-44;44", unit="% (average annual outage time, hardened "
         "areas)", used_in="brief hard 25 Q8", source="R-013 (Dominion release, June 2026: 'reduced average annual "
         "outage time by 44% for customers in these areas')", producer=R, checked_by=B,
         result="match; dated, beside the 2023 figure (C-S6-02)", variant="both"),
    dict(id="C-B-04", exact_text="744 MW of data centers connected in 2025, and over 54 GW in contracting stages",
         value="744;54", unit="MW; GW", used_in="brief hard 25 Q10",
         source="R-040 (Dominion Energy 2025 Annual Report, PDF p. 7: 11 data centers, 744 MW); R-054 (Q3 2026 "
         "earnings call, October 30, 2026: over 54 GW in contracting stages)", producer=R, checked_by=B,
         result="match", variant="both"),
    dict(id="C-B-03", exact_text="[A4] the delivery tips and their research citations",
         value="1999;2002;2006;2009;2010;2011;2014;2021;2022;2024;0.2;20:00", unit="citation years; effect size",
         used_in="brief A4", source="research/delivery_and_rehearsal.md (each with its DOI); claims_register R-081, "
         "R-082, R-088, R-091", producer=R, checked_by=B, result="match (R's Page A, compressed)", variant="both"),
    # brief talk table
    dict(id="C-B-01", exact_text="about 7:40", value="0:35;1:10;0:55;1:05;1:00;7:40;35;10;55;05;40;130",
         unit="minutes:seconds (speaker notes at about 130 words a minute)", used_in="brief p2 talk table",
         source="build_deck_v2.py notes word counts (adopted: 76, 154, 124, 138, 117, 143, 122, 131 = 1,005 words)",
         producer=B, checked_by=B, result="match: 1,005 / 130 = 7.7 minutes", variant="both"),
]


# ----------------------------------------------------------------------------- v3 (O-33): helpers
def mmss(sec: int) -> str:
    return f"{sec // 60}:{sec % 60:02d}"


def talk_times() -> dict:
    """S1-S8 speaker-note words in each v3 deck, counted as build_deck_v3.py counts them (whitespace split), and the
    seconds at WPM words a minute, rounded per slide: the brief's p2 table prints these, and its totals are their sums."""
    from pptx import Presentation
    out = {}
    for key, path in (("adopted", DECK_A), ("public", DECK_P)):
        prs = Presentation(str(path))
        words = [len(sl.notes_slide.notes_text_frame.text.split()) for sl in list(prs.slides)[:8]]
        out[key] = (words, [int(round(w * 60 / WPM)) for w in words])
    return out


def public_v3_peers() -> list[dict]:
    rows = list(csv.DictReader(open(CH3 / "s3_peer_quadrant_v3_public.csv", encoding="utf-8")))
    assert len(rows) == 12
    mixed = sorted(d["utility"] for d in rows if d["major_event_method"] == "Mixed")
    assert mixed == ["Duke Energy Florida", "Georgia Power"], mixed       # the workbook's labels, unchanged (O-33)
    return rows


def peer_values_v3_public() -> str:
    vals = []
    for d in public_v3_peers():
        s, c, a = float(d["saifi_5yr_2021_25"]), float(d["caidi_5yr_2021_25"]), float(d["saidi_3yr_2023_25"])
        vals += [f"{s:.2f}", f"{c:.0f}", f"{a:.0f}"]
    assert vals == peer_values("public").split(";"), "v3 public peer values differ from v2's"
    return ";".join(vals)


def public_medians() -> tuple:
    """Medians of the 12 (Dominion included), as origin/main docs/05:87 prints them: SAIFI 0.96, CAIDI 105."""
    rows = public_v3_peers()
    xs = sorted(float(d["saifi_5yr_2021_25"]) for d in rows)
    ys = sorted(float(d["caidi_5yr_2021_25"]) for d in rows)
    mx, my = (xs[5] + xs[6]) / 2, (ys[5] + ys[6]) / 2
    assert (f"{mx:.2f}", f"{my:.0f}") == ("0.96", "105"), (mx, my)
    docs05 = subprocess.run(["git", "-C", str(ds.REPO), "show", "origin/main:docs/05_metrics_and_measures.md"],
                            capture_output=True, check=True).stdout.decode("utf-8")
    assert "medians of the twelve peers: SAIFI 0.96, CAIDI 105" in docs05
    return xs[5], xs[6], mx, ys[5], ys[6], my


_T = talk_times()
_SA, _SP = _T["adopted"][1], _T["public"][1]
_MED = public_medians()

V3_RETIRE: dict[str, str] = {}
V3_U = {  # id: {field: new value}, applied after the v2 updates
    # 1. public S3 says nothing origin/main contradicts; the adopted deck keeps the 11-peer medians
    "C-S3-01": dict(used_in="deck S3 (adopted): right column, chart label, alt text, notes; brief p4 text, A1 "
                    "('median If adopted 0.93 (11 peers)')",
                    source="D findings.md C5-1 (peer_reliability_5yr.csv median_saifi_2021_25_excl_dominion 0.934, "
                    "commit 7133aba)",
                    result="match; v3 (O-33): adopted only; the public deck prints the 12-utility median (C-S3-11P)",
                    variant="adopted"),
    "C-S3-02": dict(used_in="deck S3 (adopted): right column, chart label, alt text; brief p4 text, A1 ('median If "
                    "adopted 99.5 (11 peers)')",
                    result="match: 99.5 is the median of the 11 peers' CAIDI 2021-25 means (BGE); v3 drops the stale "
                    "'104.85 rounds to 105' note, which is the 12-utility median (C-S3-02P)"),
    "C-S3-02P": dict(exact_text="mid-pack, 6th of the 12 (median 105)", value=f"110;105;{_MED[5]:.2f}",
                     unit="CAIDI 2021-25; median of the 12 utilities, Dominion included",
                     used_in="deck S3 (public): right column, chart label 'median of the 12 (including Dominion): 105 "
                     "min', alt text; brief p4 source note, A1 ('public-only 105 (all 12)')",
                     source="origin/main docs/05_metrics_and_measures.md:87 ('Quadrant lines | medians of the twelve "
                     f"peers: SAIFI 0.96, CAIDI 105'); origin/main workbook Peers sheet: ({_MED[3]:.1f} + "
                     f"{_MED[4]:.1f}) / 2 = {_MED[5]:.2f}",
                     result="match; v3 (O-33): the median origin/main prints (tier A), replacing the 11-peer 99.3"),
    "C-S3-04P": dict(value=peer_values_v3_public(), used_in="deck S3 chart, A6 table (public)",
                     source="origin/main powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers: values and method "
                     "labels as printed there ('Mixed' for Georgia Power and Duke Energy Florida, 'Own method' for "
                     "Dominion and Alabama Power; O-33); charts/v3/s3_peer_quadrant_v3_public",
                     result="match; A6 source explains Mixed: 'Other' in 2013 only, IEEE 1366 for 2014-25"),
    "C-S3-07": dict(used_in="brief p4 caveat box (tagged If adopted), A1 ('10 of 12', If adopted), hard 25 Q2 "
                    "('Adopted: 10 of the 12 use IEEE')",
                    result="match; v3 (O-33): adopted only and never in the public deck (origin/main's workbook labels "
                    "Georgia Power and Duke Energy Florida 'Mixed', and docs/06 says half the peers use a different "
                    "reporting method); the adopted deck says 'most peers IEEE 1366'",
                    variant="adopted"),
    "C-S3-09": dict(used_in="deck A6 source (public: 'Mixed: “Other” in 2013 only, IEEE 1366 for 2014–25'); brief p4 "
                    "source note",
                    source="D findings.md C6 (batch 6 message, item 1); for the public use, origin/main's committed "
                    "reliability inputs (identical to the branch's: V1 v3 delta) and its workbook Peers sheet, which "
                    "labels Georgia Power and Duke Energy Florida 'Mixed'",
                    result="match; v3: the public A6 keeps origin/main's 'Mixed' label and says what it means"),
    # 2. the test split
    "C-S7-05A": dict(value="31;12;19;6;3", unit="tests: 12 on the original build (T1-T6 reliability mart, T7-T9 NOAA "
                     "storms, T10-T12 EIA-930 demand) and 19 on the new tables (T13-T31)",
                     used_in="deck S6 badge ('Original build: 12 (6 reliability, 3 storm, 3 demand). New tables: 19.'), "
                     "source, notes, A4 ranges (adopted); brief p7, A1",
                     source="data/output/test_results.csv (T1-T31 PASS); docs/03: T1-T6 sql/04 reliability mart, "
                     "T7-T9 sql/05 NOAA storms, T10-T12 sql/06 EIA-930 demand",
                     result="match; v3 fixes V1 I1 ('12 on the reliability mart': only T1-T6 are)"),
    "C-S7-10": dict(exact_text="T13–T31 on the new tables",
                    used_in="deck S6 source ('T13–T31 the new tables'), A4 (adopted); brief p7 ('T13–T31 the new "
                    "tables'), A1",
                    result="match; v3: the ranges as docs/03 groups them (T1-T6, T7-T9, T10-T12, T13-T31)"),
    # 4. coverage and register hygiene
    "C-S4-04P": dict(result="match; R² 0.48 is computed from this fit on origin/main's CSV (0.484), not printed on "
                     "origin/main (V1 P3)"),
    "C-S4-05P": dict(source="origin/main powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet StormIndex, "
                     "predicted_saidi_from_weather (2017 125.94, 2023 124.44, 2024 128.25: a fit on SAIDI rounded to "
                     "1 dp); storm county-days and SAIDI ex-MED from origin/main data/output/storm_vs_saidi.csv",
                     result="match; 'From the fit' is the workbook's column, as printed on origin/main (a refit on the "
                     "CSV gives 126.0, 124.5 and 128.3: V1 P3)"),
    "C-S4-08": dict(value="11.9;7.9;16.9;2,000;12;11.944",
                    used_in="deck S4 title ('about 12 times'), right column, notes (adopted); brief p2, p5, A1, hard 25 "
                    "Q5 ('The 12×')",
                    result="match; 12 is 11.944 rounded (V1 U5)"),
    "C-S4-09": dict(used_in="deck S4 (adopted), notes; brief p5, A1, hard 25 Q3 ('in those 31 (19.9×)'), Q5",
                    source="D findings.md C5-2 (storm_vs_calm.csv rows 2-3; the Dominion-only subset is the 31 mapped "
                    "Dominion-only counties, 1,065 storm county-days)"),
    "C-S4-20": dict(exact_text="customer-weighted average of 159 minutes a year, against 211 in the 68",
                    unit="counties; customer-weighted average minutes a year (non-major days, 2015-2024)",
                    used_in="brief p5 (tagged If adopted: 'The 31 mapped counties Dominion serves alone have a "
                    "customer-weighted average of 159 minutes a year')",
                    result="match; customer-weighted means (simple means would be 225 and 361: V1); the 31 are the "
                    "mapped Dominion-only counties (C-B-05)"),
    "C-S5-04": dict(used_in="deck A3 (both: 'Highest hour of the year +26%, lowest hour +52%'); brief p6 text "
                    "('19,803 → 24,957 MW', '7,167 → 10,903 MW') and chart, A1"),
    "C-S5-07": dict(value="65.4;39.08;64.62;7.9;8.0;8",
                    result="match; the printed '8%' holds: +8.0% counting all service types, consistent with the "
                    "sales figure (bundled plus delivery-only); +7.9% counting bundled customers only (V1)"),
    "C-S5-11": dict(unit="Power BI Summary cards, 2025: customers served; SAIDI; minutes per interruption (CAIDI); "
                    "SAIFI; major-event share",
                    used_in="deck S5 screenshot and alt text (adopted); brief p7 image and caption, A1",
                    source="work/powerbi/b6/s5_summary_v3.png (the CAIDI card reads 'Minutes per interruption', "
                    "O-33); 2,675,735 customers (EIA-861)"),
    "C-S5-12": dict(source="powerbi/measures.dax:401-403, Selected SAIDI in VAR form (branch interview-upgrade-2026-11, "
                    "commit 859b52d); the same measure as the candidate's .pbix (V2 F22)"),
    # used_in gaps (V1 coverage section 1); sheet items by their printed number
    "C-Q-03": dict(used_in="qsheet item 4 (B8: '71% → 90%'), item 5 (B6: '71% to 90%'); brief A1, hard 25 Q17"),
    "C-Q-06": dict(used_in="qsheet item 9 (T1); brief A1 ('$690M · 440')"),
    "C-Q-08": dict(used_in="qsheet item 18 (R4); brief A1 ('25% · 3-2')"),
    "C-S8-01": dict(used_in="deck S8 strip (both); brief A1 ('20M+'), hard 25 Q16; qsheet items 2 (O1), 11 (T36), "
                    "14 (T17)"),
    # 8. R's follow-ups (research/V1_followups.md): all three verified, none cut
    "C-Q-10": dict(value="2027;2026-05;2026-09;2026-09-03",
                   used_in="qsheet item 19 (R2; also: announced May 2026, approved by shareholders on September 3, SC, "
                   "NC, FERC and NRC must also approve, closing expected in the second half of 2027); brief hard 25 "
                   "Q23 (timeline), A1 ('May 2026 → H2 2027')",
                   source="R-106: WWBT / 12 On Your Side, September 3, 2026 (20:41 UTC), "
                   "https://www.12onyourside.com/2026/09/03/dominion-shareholders-back-merger-with-nextera-energy/, "
                   "quoting Dominion: 'We are pleased that shareholders of Dominion Energy and NextEra Energy have "
                   "approved the proposed merger. Today's vote represents an important milestone'. Secondary: R-104, "
                   "R-105, SEC Form 8-K Item 5.07 of both companies, filed September 3, 2026 (vote counts in the "
                   "research files only, not printed). R-049 (CEO, Q3 call: Virginia final order by January 11, 2027; "
                   "close H2 2027), R-053 (mid-January 2027), R-048 (approvals required); Dominion release of May 18, "
                   "2026 (announcement)",
                   result="match; calendar as reported, no prediction; both companies' shareholders approved on "
                   "September 3, 2026 (R-106, fetched by the orchestrator, HTTP 200)"),
    "C-S6-02": dict(used_in="brief p8, A1 ('−32% outage minutes, feeders hardened 12+ months (Nov 2023)'), hard 25 Q8 "
                    "('(Nov 30, 2023)', beside −44%)"),
    "C-S6-06": dict(exact_text="−44% average annual outage time for customers in hardened areas",
                    unit="% (average annual outage time, customers in the hardened mainfeeder areas, Virginia)",
                    used_in="brief hard 25 Q8 ('Reported, two measures', beside −32% with its date), A1 ('−44% average "
                    "annual outage time, hardened areas (June 2026)')",
                    source="R-013, re-sourced to the primary: Dominion Energy release of June 8, 2026 on "
                    "investors.dominionenergy.com ('Dominion Energy prepares year-round for hurricane season ...'): "
                    "'Through its Mainfeeder Hardening Program, the company has replaced more than 8,000 older utility "
                    "poles and hardened over 350 miles of power lines in Virginia. The program has reduced average "
                    "annual outage time by 44% for customers in these areas.' (research/V1_followups.md §2)",
                    result="match (R, Nov 1, 2026); company-reported: no baseline years, major-event treatment or "
                    "comparison group stated; a different measure from −32% (C-S6-02), printed beside it with dates, "
                    "never as a trend"),
    "C-B-03": dict(value="1999;2002;2006;2009;2010;2011;2014;2015;2017;2018;2021;2022;2024;0.2;20:00;.42;.20;-.11;-.19",
                   unit="citation years; effect sizes (r, d)",
                   source="research/delivery_and_rehearsal.md (each with its DOI); claims_register R-081, R-082, R-088, "
                   "R-091; Barrick 2010 r = .42 and Swider 2011 r = .20, −.11 to −.19 (Crossref/OpenAlex, V1); Powell "
                   "2018 r = −.19 (register quote; no abstract retrievable); Ranehill 2015, Huang 2017",
                   result="match (R's Page A, compressed); V1 U4: the r-values and the three citation years added"),
    # 5. talk times per variant (V1 I3, U8)
    "C-B-01": dict(exact_text=f"{mmss(sum(_SA))} in all (adopted)",
                   value=";".join([mmss(s) for s in _SA] + [mmss(s) for s in _SP]
                                  + [mmss(sum(_SA)), mmss(sum(_SP)), str(WPM)]),
                   unit="minutes:seconds per slide and in all, adopted · public-only (speaker notes at about 130 "
                   "words a minute)",
                   used_in="brief p2 talk table (one time cell per slide: adopted · public) and its source line",
                   source="the v3 decks' speaker notes on S1-S8, whitespace word counts as build_deck_v3.py prints "
                   f"them: adopted {', '.join(map(str, _T['adopted'][0]))} = {sum(_T['adopted'][0]):,} words; public "
                   f"{', '.join(map(str, _T['public'][0]))} = {sum(_T['public'][0]):,} words; each slide's seconds "
                   "rounded, totals are their sums",
                   result="match; V1 I3 and U8: times per variant, recounted after the v3 note edits; no slot length "
                   "is printed"),
}

V3_NEW = [
    dict(id="C-S3-11P", exact_text="4th highest of the 12 (median 0.96)",
         value=f"1.21;0.96;{_MED[2]:.4f};{_MED[2]:.3f}", unit="SAIFI 2021-25; median of the 12 utilities, Dominion "
         "included", used_in="deck S3 (public): right column, chart label 'median of the 12 (including Dominion): "
         "0.96', alt text, notes ('a median of 0.96 for all twelve, Dominion included'); brief p4 source note, A1 "
         "('public-only 0.96 (all 12)')",
         source="origin/main docs/05_metrics_and_measures.md:87 ('Quadrant lines | medians of the twelve peers: SAIFI "
         f"0.96, CAIDI 105'); origin/main workbook Peers sheet: ({_MED[0]:.3f} + {_MED[1]:.3f}) / 2 = {_MED[2]:.4f}",
         producer=B, checked_by=B, result="match; v3 (O-33): the median origin/main prints (tier A)", variant="public"),
    dict(id="C-B-05", exact_text="33 of them Dominion-only (D15), 31 on the map", value="103;33;31",
         unit="counties: Dominion's EIA-861 counties; Dominion-only in all; Dominion-only on the EAGLE-I map",
         used_in="brief hard 25 Q3; brief p5 ('The 31 mapped counties Dominion serves alone')",
         source="data/output/county_outage_map_dominion_only.csv (commit 4fc9939): 33 rows, all dominion_only_county "
         "True; 31 with map_flag ok; off the map 51600 Fairfax city (implausible readings 2018-2020) and 51660 "
         "Harrisonburg city (almost no EAGLE-I readings, municipal utility); docs/04 D15",
         producer=D, checked_by=B, result="match; the 31 are the 33 less the two cities off the map (V1 U1, I4)",
         variant="both"),
    dict(id="C-S5-14", exact_text="[image] Summary page chart titles and point labels (adopted S5 screenshot; brief p7)",
         value="6;9;1.24;1.17;1.32;1.244;1.320;120.5;105.9;109.4;120.48;109.39;122;136;133;122.4;135.7;133.1;0.70;10;46",
         unit="% change since 2019 (SAIFI +6%, CAIDI −9%); SAIFI and CAIDI point labels; weather-adjusted SAIDI "
         "(minutes); scatter r and n; the 46 kV marker",
         used_in="deck S5 screenshot (adopted); brief p7 image: 'Outages per customer up 6% since 2019, most of it "
         "after 2023' (1.24, 1.17, 1.32), 'Minutes per interruption down 9% since 2019' (120.5, 105.9, 109.4), "
         "weather-adjusted 122, 136, 133, 'r = 0.70: association, not cause', markers '2015: Automated Outage "
         "Recording' and '2020: 46 kV lines added'",
         source="work/powerbi/b6/s5_summary_v3.png; EIA-861 Dominion Energy Virginia ex-MED: SAIFI 2019 1.244 → 2025 "
         "1.320 (+6.1%), CAIDI 2019 120.48 → 2025 109.39 (−9.2%); weather-adjusted SAIDI from the storm-day fit: "
         "2015 122.4, 2019 135.7, 2025 133.1 (V1 U3); markers: docs/03 P7, docs/05:65",
         producer=B, checked_by=B, result="match (V1 recomputed each; image only, no extractable text)",
         variant="adopted"),
    # V1 v3 delta, open item 1: the public S5 screenshot (the candidate's current report) had no public row
    dict(id="C-S5-14P", exact_text="[image] What moved page, frequency chart: title and point labels (public S5 "
         "screenshot)", value="6;1.24;1.17;1.32;1.244;1.165;1.320",
         unit="% change in SAIFI ex-MED since 2019; SAIFI point labels 2019, 2023, 2025 (interruptions per customer)",
         used_in="deck S5 screenshot (public): 'Outages per customer up 6% since 2019, most of it after 2023', point "
         "labels 1.24 (2019), 1.17 (2023), 1.32 (2025), '2019 Level' line",
         source="work/powerbi/b6/orig_whatmoved_saifi.png (the candidate's current report: read-only copy of the "
         "original .pbix, Import data); origin/main docs/06_powerbi_report.md:37 ('Two cards: outage frequency 2019 "
         "to 2025 (+6%)'); origin/main workbook Trend sheet saifi_ex_med: 2019 1.244, 2023 1.165, 2025 1.32",
         producer=B, checked_by=B, result="match: 1.320 / 1.244 = +6.1%, printed +6%; the labels are 1.244, 1.165 "
         "and 1.320 to two decimals (B read the Trend sheet with git show origin/main, Nov 1; image only, no "
         "extractable text)", variant="public"),
    dict(id="C-B-06", exact_text="about an hour and fifty minutes each time", value="109.4;144.4;2.8;1.3",
         unit="minutes, spelled out: CAIDI 2025 (1 h 49 min); SAIDI 2025 (2 h 24 min); the 3-year rise; SAIFI 2025",
         used_in="brief hard 25 Q24 ('about 1.3 times', 'about an hour and fifty minutes each time', 'almost two and "
         "a half hours in the year', 'rose about three minutes')",
         source="C-S5-11 (EIA-861 2025 ex-MED: CAIDI 109.4, SAIDI 144.4), C-S2-04 (SAIFI 1.320), C-S2-18 (2.8)",
         producer=B, checked_by=B, result="match: 109.4 min = 1 h 49 min; 144.4 min = 2 h 24 min; 2.8 is about three "
         "(V1 U6)", variant="both"),
    dict(id="C-B-07", exact_text="Dominion trims on 4–5-year cycles", value="4;5", unit="years (maintenance trim "
         "cycle)", used_in="brief hard 25 Q7",
         source="R-076, re-opened Nov 1, 2026: Dominion Energy, 'Virginia/North Carolina Tree Trimming and Powerlines "
         "FAQ' (dominionenergy.com): 'Our maintenance trimming is done on cycles typically ranging from four to five "
         "years'; 'Nearly all of our neighborhood power lines are cleared on a four year cycle.' "
         "(research/V1_followups.md §3)", producer=R, checked_by=B, result="match (V1 U2)", variant="both"),
]


def rows_v2() -> list[dict]:
    out = []
    for r in c1.ROWS:
        d = dict(zip(HEADER[:-1], r))
        d["variant"] = "both"
        if d["id"] in RETIRE:
            continue
        d.update(U.get(d["id"], {}))
        out.append(d)
    ids = {d["id"] for d in out}
    for n in NEW:
        assert n["id"] not in ids, n["id"]
        d = {k: "" for k in HEADER}
        d.update(n)
        out.append(d)
    assert len({d["id"] for d in out}) == len(out)
    for d in out:
        assert d["variant"] in ("both", "adopted", "public"), d
    return out


def rows_v3() -> list[dict]:
    out = [d for d in rows_v2() if d["id"] not in V3_RETIRE]
    ids = {d["id"] for d in out}
    missing = set(V3_U) - ids
    assert not missing, f"V3_U names rows that do not exist: {missing}"
    for d in out:
        for k, v in V3_U.get(d["id"], {}).items():
            assert k in HEADER, k
            d[k] = v
    for n in V3_NEW:
        assert n["id"] not in ids, n["id"]
        d = {k: "" for k in HEADER}
        d.update(n)
        out.append(d)
    assert len({d["id"] for d in out}) == len(out)
    for d in out:
        assert d["variant"] in ("both", "adopted", "public"), d
        assert all(d[k] for k in ("id", "exact_text", "value", "used_in", "source", "producer", "checked_by",
                                  "result")), d["id"]
    return out


# ----------------------------------------------------------------------------- deliverable text
def deck_text(path: Path) -> str:
    from pptx import Presentation
    prs = Presentation(str(path))
    out = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                out.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    out.extend(c.text for c in row.cells)
            if sh.shape_type == 13:     # picture: its alt text is printed nowhere, but it is part of the file
                out.append(sh._element.nvPicPr.cNvPr.get("descr", ""))
        if s.has_notes_slide:
            out.append(s.notes_slide.notes_text_frame.text)
    return " ".join(" ".join(out).split())


def html_text(path: Path) -> str:
    h = path.read_text(encoding="utf-8")
    h = re.sub(r"<style>.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<svg.*?</svg>", " ", h, flags=re.S)
    h = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", " ", h)
    h = re.sub(r"<span class='n'>\d+</span>", " ", h)
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", h)).split())


NUM = c1.NUM
IGNORE = set(c1.IGNORE)   # v1's list: standard and form numbers, utility 19876, page furniture; v2 adds none


def norm(t: str) -> str:
    return c1.norm(t)


def saidi_range_check():
    rows = list(csv.DictReader(open(ds.REPO / "data" / "output" / "storm_vs_saidi.csv", encoding="utf-8")))
    vals = {int(r["year"]): float(r["saidi_ex_med"]) for r in rows if 2015 <= int(r["year"]) <= 2025}
    lo, hi = min(vals, key=vals.get), max(vals, key=vals.get)
    assert (lo, round(vals[lo], 1), hi, round(vals[hi], 1)) == (2017, 117.4, 2019, 149.9), (lo, hi)


def main():
    saidi_range_check()
    rows = rows_v3()
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEADER)
        w.writeheader()
        w.writerows(rows)
    by_v = {v: sum(d["variant"] == v for d in rows) for v in ("both", "adopted", "public")}
    print(f"{OUT_CSV.name}: {len(rows)} rows {by_v}; retired from v1: {len(RETIRE)}; v3 updated {len(V3_U)}, "
          f"added {len(V3_NEW)}, retired {len(V3_RETIRE)}")
    print("talk times (brief p2):", {k: ([mmss(s) for s in v[1]], mmss(sum(v[1]))) for k, v in _T.items()})
    texts = {"deck_adopted": deck_text(DECK_A), "deck_public": deck_text(DECK_P), "brief": html_text(BRIEF),
             "qsheet": html_text(QSHEET)}
    applies = {"deck_adopted": {"both", "adopted"}, "deck_public": {"both", "public"},
               "brief": {"both", "adopted", "public"}, "qsheet": {"both", "adopted", "public"}}
    report = {}
    for name, txt in texts.items():
        covered = set()
        for d in rows:
            if d["variant"] in applies[name]:
                for fld in (d["exact_text"], d["value"]):
                    for m in NUM.findall(fld):
                        covered.add(norm(m))
        missing = set()
        for m in NUM.findall(txt):
            n = norm(m)
            try:
                v = float(n)
            except ValueError:
                continue
            if 2013 <= v <= 2026 and "." not in n:
                continue
            if v <= 14 and "." not in n and not m.endswith("%"):
                continue
            if n not in covered and n not in IGNORE:
                missing.add(m)
        report[name] = missing
        print(f"{name}: numbers not covered by an applicable row ({len(missing)}):", " ".join(sorted(missing)))
    # exact_text: present in a deliverable the row's variant applies to
    not_found = []
    for d in rows:
        probe = d["exact_text"].split("…")[0].strip()
        if not probe or probe.startswith("["):
            continue
        pool = [t for k, t in texts.items() if d["variant"] in applies[k]]
        if not any(probe in t for t in pool):
            not_found.append(f"{d['id']} {probe!r}")
    print(f"exact_text not found ({len(not_found)}):", *not_found, sep="\n  ")
    # stale and cross-variant leaks
    caidi_wording = ["minutes to restore", "time to restore", "restoration time", "restore each outage",
                     "how fast it comes back"]                                   # O-33 item 3, every deliverable
    stale = {"deck_adopted": ["723", "796", "465", "851", "6,077,232", "D1–D14", "12 tests pass", "Mixed",
                              "12 on the reliability mart", "T1–T12 on the reliability mart"] + caidi_wording,
             "deck_public": ["718", "791", "464", "848", "11.9", "EAGLE-I", "6,094,320", "T13", "D22", "D1–D22",
                             "12 of 12", "31 tests", "p = ", "2.68M", "18 tables", "Selected SAIDI",
                             "degree", "10 of 12", "10 of the 12", "ten of the twelve", "peer median", "median 0.93",
                             "99.3", "99.5", "0.934"] + caidi_wording,
             "brief": ["programme", "restored 33.5", "band of about", "mostly because", "blocked automated",
                       "27 Oct", "For answers only", "weather fit (CI", "4th of 12", "12 on the reliability mart",
                       "99.3", "leaving two minutes", "7:40"] + caidi_wording,
             "qsheet": ["718", "791", "723", "796", "six DirectQuery", "never an average of ratios",
                        "without a live connection", "in September"] + caidi_wording}
    n_stale = 0
    for name, bads in stale.items():
        for bad in bads:
            if re.search(rf"(?<![\d,.]){re.escape(bad)}(?![\d,])", texts[name], flags=re.I):
                print(f"  STALE or LEAK {bad!r} in {name}")
                n_stale += 1
    print(f"stale or leaked strings: {n_stale}")
    for name, txt in texts.items():                    # every remaining 'restor...' in context, for a human read
        for m in re.finditer(r"restor\w*", txt, flags=re.I):
            print(f"  restor* in {name}: …{txt[max(0, m.start() - 70):m.end() + 40]}…")
    # final scans of every deliverable's text (decks: slides, tables, alt text and speaker notes)
    scans = {
        "banned word": r"\b(AI assistant|Claude|ChatGPT|agent [BDR]\b|Agent [BDR]\b|orchestrator|ledger|claims\.csv|"
                       r"the brief requires|interview-prep|subagent)",
        "email": r"[\w.+-]+@[\w-]+\.[\w.]+",
        "phone": r"\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}",
        "machine path": r"[A-Z]:\\|/Users/|\\Users\\|AppData",
        "claim-id tag": r"\[(?:C|N|R)-[A-Z0-9-]+",
        "UK spelling": r"\b(programme|behaviour|colour|centre|analyse|prioritis|licence|normalis|organis|labelled|"
                       r"modelled|favour|summaris|minimis|recognis|authoris|optimis)",
        # a day before a month name; 'N Oct 12, 2018' is a table row number before a US date, not a day
        "day-month date": r"\b\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|"
                          r"Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b"
                          r"(?!\.?\s+\d{1,2},\s+\d{4})",
        "salary figure": r"\$\s?\d{2,3}(?:,\d{3}|[kK])\b",
    }
    for name, txt in texts.items():
        hits = {k: re.findall(p, txt, flags=re.I if k in ("banned word", "UK spelling") else 0)
                for k, p in scans.items()}
        bad = {k: v for k, v in hits.items() if v}
        print(f"scan {name}: {'clean' if not bad else bad}")
    for m in re.findall(r"\$\s?\d[\d,.]*\s?[kKmMbB]?", texts["qsheet"] + " " + texts["brief"]):
        if m not in ("$690M",):
            print(f"  CHECK dollar figure: {m!r}")
    # public deck: is every number printed on origin/main? Tier A = README, docs, sql, scripts, data/output, powerbi;
    # tier B = the raw input extracts, where a match is a source value or a coincidence and needs a look
    import origin_main_corpus as om
    tier_a, _ = om.load()
    rounded_a = set()          # every tier-A number with more decimals, rounded to 1-3 decimals as a slide prints it
    for x in re.findall(r"(?<![\w.])-?\d+\.\d{2,}", tier_a):
        for dp in (1, 2, 3):
            if len(x.split(".")[1]) > dp:
                rounded_a.add(f"{float(x):.{dp}f}")
    by_rounding, only_b, nowhere = [], [], []
    for m in sorted(set(NUM.findall(texts["deck_public"]))):
        n = m.lstrip("+").replace("−", "-")
        try:
            v = float(norm(m))
        except ValueError:
            continue
        if (2013 <= v <= 2026 and "." not in n) or (v <= 14 and "." not in n and not m.endswith("%")):
            continue
        tiers = {om.findable(n.rstrip("%")), om.findable(n)}
        if "A" in tiers:
            continue
        if "." in n and n.rstrip("%").lstrip("-") in rounded_a:
            by_rounding.append(m)
        elif "B" in tiers:
            only_b.append(m)
        else:
            nowhere.append(m)
    print(f"public deck numbers on origin/main tier A only after rounding ({len(by_rounding)}):", " ".join(by_rounding))
    print(f"public deck numbers matched only in origin/main's raw inputs ({len(only_b)}):", " ".join(only_b))
    print(f"public deck numbers not on origin/main ({len(nowhere)}):", " ".join(nowhere))


if __name__ == "__main__":
    main()
