"""Write interview-prep/claims.csv (B owns it) and check coverage both ways.

1. Every row's exact_text must appear in at least one deliverable it names (deck text + notes, brief,
   question sheet).
2. Every number printed in the deck (slides and notes), the brief and the question sheet must be covered by
   some row (its exact_text or value), apart from years, slide numbers, page numbers and question numbers.

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\claims\\build_claims.py
"""
from __future__ import annotations

import csv
import html as htmllib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402

IP = ds.REPO / "interview-prep"
# claims.csv tracks the current deliverables (v1); the v0 files stay frozen as the safety net
DECK = IP / "deliverables" / "01_deck" / "Dominion_reliability_deck_v1.pptx"
BRIEF = IP / "deliverables" / "03_interview_brief" / "Dominion_interview_brief_v1.html"
QSHEET = IP / "deliverables" / "02_question_sheet" / "Dominion_question_sheet_v1.html"
HEADER = ["id", "exact_text", "value", "unit", "used_in", "source", "producer", "checked_by", "result"]

D, R, B, CV = "D", "R", "B", "resume"


def _peer_values():
    rows = list(csv.DictReader(open(ds.WORK / "charts" / "v0" / "s3_peer_quadrant.csv", encoding="utf-8")))
    vals = []
    for d in rows:
        vals += [f"{float(d['saifi_5yr_2021_25']):.2f}", f"{float(d['caidi_5yr_2021_25']):.0f}",
                 f"{float(d['saidi_3yr_2023_25']):.0f}"]
    return ";".join(vals)


def _a2_values():
    """A2 table after D22, recomputed exactly as build_deck_v1.py does (same snapshot, same coefficients)."""
    ch1 = ds.WORK / "charts" / "v1"
    rows = list(csv.DictReader(open(ch1 / "a2_weather_fit.csv", encoding="utf-8")))
    t = (ch1 / "a2_weather_fit.txt").read_text(encoding="utf-8").splitlines()[0].split()
    b0, b1 = float(t[3]), float(t[5])
    vals = []
    for d in rows:
        cd, sd = float(d["storm_county_days"]), float(d["saidi_ex_med"])
        fit = b0 + b1 * cd
        vals += [f"{cd:,.0f}", f"{sd:.1f}", f"{fit:.1f}", f"{sd - fit:+.1f}"]
    return ";".join(vals)


def _a6_values():
    """A6 table (ten largest outage events) as printed by build_deck_v1.py, plus the peak-day numbers."""
    import datetime as dt
    rows = list(csv.DictReader(open(ds.REPO / "data" / "output" / "outage_events_top10.csv", encoding="utf-8")))
    vals = []
    for e in rows:
        d = dt.date.fromisoformat(e["peak_day"])
        vals += [str(d.day), f"{float(e['peak_customers_out']):,.0f}", f"{float(e['hours_to_50pct']):.1f}",
                 f"{float(e['hours_to_90pct']):.1f}", f"{float(e['customer_hours']) / 1e6:.1f}"]
    return ";".join(vals + ["100"])   # notes: winter storms 'about 100 hours' to 90% (102.8, 101.5)


PEER_VALUES = _peer_values()
A2_VALUES = _a2_values()
A6_VALUES = _a6_values()
ROWS = [
    # ---------------------------------------------------------------- S1
    ("C-S1-01", "3 November 2026", "2026-11-03", "date", "deck S1; brief cover", "MASTER_PROMPT §1 (interview date)",
     "orchestrator", B, "match"),
    # ---------------------------------------------------------------- S2 (locked G1a: 2022 -> 2025)
    ("C-S2-01", "130 → 133", "130;133", "minutes (3-yr SAIDI ex-MED)",
     "deck S1-S2, S7, S8 notes; brief p2, p3, p8; qsheet O2, C1",
     "R-028: Dominion Energy 2025 Annual Report, printed p. 10 (PDF p. 20)", R, B,
     "match: page confirmed by R in research/for_B.md 07:58"),
    ("C-S2-02", "130.2 → 133.0", "130.2;133.0", "minutes", "deck S2, S7, A4; brief p2, p3, p8; qsheet O2, C1",
     "D F01 (mart.FCT_RELIABILITY, query F01); workbook sheet Reconciliation", D, B, "match"),
    ("C-S2-03", "136.0 → 144.4", "136.0;144.4", "minutes (SAIDI ex-MED 2022, 2025)",
     "deck S2 left column and chart, notes; brief p3, p8", "D findings.md S2.1; data/output/storm_vs_saidi.csv "
     "(136.047, 144.4)", D, B, "match"),
    ("C-S2-04", "1.199 → 1.320", "1.199;1.320", "interruptions per customer (SAIFI)", "deck S2 chart; brief p2, p3, p8",
     "D findings.md S2.1; data/output/storm_vs_saidi.csv", D, B, "match"),
    ("C-S2-05", "+10%", "10.1", "% (SAIFI 2022→2025)", "deck S2 chart, S8, notes; brief p2, p3, p8; qsheet U3",
     "D findings.md S2.2 (+10.1%)", D, B, "match: 1.320/1.199-1 = 10.09%"),
    ("C-S2-06", "113.5 → 109.4", "113.5;109.4", "minutes (CAIDI)", "deck S2 chart; brief p3, p8",
     "D findings.md S2.1 (113.5, 109.4); 136.047/1.199 = 113.47; 2025 reported 109.394", D, B, "match"),
    ("C-S2-07", "−4%", "-3.6;4", "% (CAIDI 2022→2025)", "deck S2 chart, notes; brief p2, p3, p8; qsheet U3 ('fell 4%')",
     "D findings.md S2.2 (-3.6%)", D, B, "match"),
    ("C-S2-08", "+6.1%", "6.1;+6%", "% (SAIDI 2022→2025)", "deck S2 chart; brief p3", "D findings.md S2.2 (+6.1%)", D, B,
     "match"),
    ("C-S2-09", "1.320, is the highest in EIA's 2013–2025 record", "1.320;1.32;1.303", "SAIFI",
     "deck S2 chart, notes, S8; brief p2, p3, p8", "D findings.md S2.1 (series 2013-2025)", D, B,
     "match: make_charts_v0.py asserts 2025 is the series maximum"),
    ("C-S2-10", "79%", "79", "% of the ln change from frequency, 2023→2025",
     "deck S2 notes, A1; brief p2, p3, App A", "D F03 (sql/03 Q1b); findings.md S2.2", D, B, "match"),
    ("C-S2-11", "+17.1%", "17.1;+13.3%;+3.3%", "% (SAIDI, SAIFI, CAIDI 2023→2025)", "brief p3 table",
     "D F02; findings.md S2.2", D, B, "match"),
    ("C-S2-12", "2018 (149.6) and 2019 (149.9)", "149.6;149.9", "minutes (SAIDI ex-MED)", "deck S2 notes; brief p2, p3",
     "D findings.md S2.1", D, B, "match"),
    ("C-S2-13", "SAIFI p = 0.54, CAIDI p = 0.74, SAIDI p = 0.58", "0.54;0.74;0.58", "p-value (OLS slope 2015-2025)",
     "deck S2 notes (in words); brief p2", "D findings.md S2.3", D, B,
     "match: the lock's robustness line pairs SAIDI/SAIFI with 0.54/0.74; D gives SAIFI 0.54, CAIDI 0.74, SAIDI 0.58"),
    # C-S2-14 (paraphrase 'attributes the increase primarily to increased storm activity') retired in v1:
    # replaced by the exact quote, C-S2-15
    ("C-S2-15", "This increase is primarily due to increased storm activity.", "quote", "text (exact quote)",
     "deck S2 notes; brief p3; qsheet U3 (closing words, quoted)",
     "R-028: Dominion Energy 2025 Annual Report, PDF p. 20 = printed p. 10 (Form 10-K "
     "Item 1, Dominion Energy Virginia segment). Scope VA-only vs VA+NC not stated in the report: not asserted", R, B,
     "match: verbatim per research/claims_register.csv R-028"),
    ("C-S2-16", "storm county-days were higher in 2025 than in 2022", "791;718", "storm county-days (2025 vs 2022)",
     "deck S2 notes ('791 against 718'); brief p3; qsheet U3 ('from 718 to 791')",
     "D F04 after D22: data/output/storm_vs_saidi.csv (2022 718, 2025 791)", D, B,
     "match; 'consistent with' Dominion's explanation, no causal claim"),
    ("C-S2-17", "The public Virginia data reproduces both reported figures to the minute", "130.22;133.01",
     "minutes (3-yr SAIDI ex-MED rebuilt from EIA-861, Virginia only: 2022-24, 2023-25)", "deck S2 notes; brief p3",
     "D findings.md quick check Q-1: Virginia only 130.22 and 133.01 (print 130 and 133); Virginia plus North "
     "Carolina 129.49 and 132.50 (print 129 and 133); R research/for_B.md §1 scope (08:47)", D, B,
     "match; an inference (consistent with a Virginia-only scope, not proof), so the deliverables never assert "
     "the scope"),
    # ---------------------------------------------------------------- S3 peers
    ("C-S3-01", "1.21 … 4th highest of 12 (peer median 0.96)", "1.211;4;0.964", "SAIFI 2021-25 mean",
     "deck S3, S8; brief p2, p4, p8", "D F08", D, B, "match: s3_peer_quadrant.csv; median of 12 = 0.964"),
    ("C-S3-02", "110 min … 6th of 12 (peer median 105)", "110.4;6;105.0", "minutes (CAIDI 2021-25 mean)",
     "deck S3; brief p2, p4, p8", "D F08", D, B, "match: chart script median 104.85 rounds to 105"),
    ("C-S3-03", "12 peer utilities", "12", "utilities", "deck S3, A6, S8; brief p2, p4, p10",
     "docs/04_decisions.md D10; D F07", D, B, "match"),
    ("C-S3-04", "[chart and table] peer points and Appendix B values", PEER_VALUES, "SAIFI, CAIDI, SAIDI",
     "deck S3 chart; brief p4, p10 (v1: deck A6 is the ten-largest-events table)",
     "powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers = D F07, F08; "
     "snapshot work/charts/v0/s3_peer_quadrant.csv", D, B, "match"),
    ("C-S3-05", "4th of 12, at 133.0 minutes", "133.0;4", "minutes (SAIDI 2023-25 mean)", "brief p4",
     "D F07", D, B, "match"),
    ("C-S3-06", "selected by EIA ID before results were computed", "12", "text (peer rule, quoted)",
     "deck S3 source; brief p4", "docs/04_decisions.md D10, quoted verbatim (D findings.md quick check Q-3)", D, B,
     "match: verbatim ('Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before "
     "results were computed.')"),
    # ---------------------------------------------------------------- S4 weather (v1: A1 headline, A3 map, A2 inset)
    ("C-S4-01", "464 → 791", "464;791", "storm county-days (2024 → 2025)", "deck A2 table; brief p5, p8",
     "D F04 after D22 (Bedford city counted once): data/output/storm_vs_saidi.csv re-exported 08:19; docs/04 D22; "
     "findings.md B0 D22 table", D, B, "match; supersedes the pre-D22 values in the frozen v0 files"),
    ("C-S4-02", "r = 0.70", "0.697;10;0.486;0.49;0.70", "correlation (2015-2024, n = 10)",
     "deck S4 notes, A2; brief p5, p8", "D F05 after D22 (r 0.697); findings.md B0 D22 table", D, B,
     "match: recomputed in make_charts_v1.py a2_fit r=0.6973 R2=0.4862"),
    ("C-S4-03", "the fit gives 145.3, the actual was 144.4", "144.4;145.25;145.3", "minutes", "deck A2; brief p5",
     "D F05 after D22 (145.3 unchanged)", D, B, "match"),
    ("C-S4-04", "SAIDI = 104.3 + 0.0518 × storm county-days", "104.26;0.0518;104.3", "fit coefficients", "deck A2",
     "D22 (intercept 104.3, slope 0.0518); make_charts_v1.py a2_fit", D, B, "match"),
    ("C-S4-05", "[table] A2 from the fit and difference, 2015-2025", A2_VALUES, "minutes", "deck A2",
     "B arithmetic: post-D22 fit x data/output/storm_vs_saidi.csv (work/charts/v1/a2_weather_fit.csv)", B, B, "match"),
    ("C-S4-15", "95% CI 0.12 to 0.92", "0.6973;2.752;2.75;0.025;0.121;0.12;0.922;0.92",
     "r = 0.70 on 2015-2024 (n = 10, 8 df): t, two-sided p, Fisher-z 95% CI for r",
     "deck A2 right column and notes ('0.12 to 0.92'); brief p5, p8 (p = 0.025)",
     "D findings.md quick check Q-2 (r 0.6973, t 2.752 on 8 df, p 0.0250, CI 0.121 to 0.922); recomputed and "
     "asserted in build_deck_v1.py", D, B, "match; the wide interval is why the deck calls the fit a check"),
    ("C-S4-06", "+0.34 minutes a year, 95% range −1.41 to +2.08, p = 0.67", "0.34;-1.41;2.08;0.67;+0.3;0.3;-1.4;+2.1",
     "min/yr", "deck A2 (rounded +0.3, −1.4, +2.1); brief p2, p5", "D findings.md Q10 (after D22: CI -1.41 to +2.08)",
     D, B, "match; v0 said +2.09 (pre-D22)"),
    ("C-S4-08", "11.9× … (95% CI 7.9–16.9)", "11.94;11.9;7.92;7.9;16.89;16.9;12;1000",
     "ratio of mean customer-hours per 1,000 customers, storm-report vs calm county-days, 2015-2025",
     "deck S4 title (about 12), tile, notes, S8; brief p2, p5, p8",
     "D findings.md A1; work/data/output/a1_storm_vs_calm.csv (bootstrap of days, 2,000 resamples)", D, B, "match"),
    ("C-S4-09", "Holds on non-major days (9.9×), in Dominion-only counties (19.9×) and in every year",
     "9.86;9.9;19.87;19.9;5.89;27.43", "ratio", "deck S4 tile, notes; brief p5", "D findings.md A1 (subsets, by year "
     "5.9 to 27.4)", D, B, "match"),
    ("C-S4-10", "6,108 storm county-days", "6108", "county-days (2015-2025, complete readings)", "deck S4, notes; brief p5",
     "D findings.md A1", D, B, "match"),
    ("C-S4-11", "from 55 a year (Prince William County) to 633 (Pittsylvania County)", "55.4;55;632.9;633;20000;99;103;4",
     "outage minutes per customer a year, non-major days, 2015-2024 avg; counties", "deck S4 chart, source, notes; "
     "brief p5", "D findings.md A3; data/output/county_outage_map.csv (map_flag ok = 99 of 103)", D, B, "match"),
    ("C-S4-12", "90% restored 33.5 hours after the peak", "33.5;90;8.3;351738;508000", "hours; customers",
     "deck S4 chart inset, notes, A6; brief p5", "D findings.md A2 (Isaias h90 33.5, h50 8.3; DOE-417 508,000); "
     "data/output/outage_events_top10.csv (peak_customers_out 351,738: EAGLE-I, all utilities in Dominion's "
     "counties; orchestrator 01-11 and README 'What's new'), fct_restoration_curve.csv", D, B,
     "match; v1 earlier printed the 1-hour sustained peak (343,492), replaced by the peak per the orchestrator"),
    ("C-S4-13", "hours to 90% restored +4.6% a year after allowing for size, p = 0.07", "4.6;0.07;47;50000",
     "%/yr; p; events", "deck S4 notes, A6 notes; brief p5", "D findings.md A2 (OLS on 47 events >= 50,000 held 1 h)",
     D, B, "match: 'no evidence that restoration got faster' per D"),
    ("C-S4-14", "[chart] S4 county map classes and Isaias curve", "per row", "minutes; % restored",
     "deck S4 chart; brief p5", "data/output/county_outage_map.csv, va_counties.geojson, fct_restoration_curve.csv; "
     "snapshot work/charts/v1/s4_county_map_isaias.csv", D, B, "match"),
    ("C-A6-01", "[table] A6 ten largest outage events", A6_VALUES, "customers; hours; million customer-hours",
     "deck A6 table and notes", "D findings.md A2; data/output/outage_events_top10.csv", D, B,
     "match: 3 tropical, 2 winter, 5 wind asserted in build_deck_v1.py"),
    # ---------------------------------------------------------------- A1, A3
    ("C-A1-01", "1.320 × 109.4 = 144.4", "144.4", "minutes", "deck A1; brief App A; qsheet U1",
     "D F02 (SAIFI 1.32, CAIDI 109.394); B arithmetic 1.32 x 109.394 = 144.40", B, B, "match"),
    ("C-A1-02", "0.125 ÷ 0.158 = 79%", "0.1249;0.1579", "ln ratio", "deck A1; brief App A",
     "B arithmetic on F02: ln(1.320/1.165) = 0.1249, ln(144.4/123.322) = 0.1579", B, B, "match"),
    ("C-A3-01", "306.7 vs 144.4", "306.7;144.4", "minutes (2025 all events vs ex-MED)",
     "deck A3, A4; brief p5, p8, p10; qsheet U2", "D F06; test T4", D, B, "match"),
    ("C-A3-02", "53%", "52.9", "% of 2025 all-event minutes on MED", "deck A3; brief p5, p8; qsheet U2", "D F06", D,
     B, "match: 162.3/306.7"),
    ("C-A3-03", "162.3", "162.3", "minutes (MED 2025)", "deck A3 chart and text; brief p5; qsheet U2",
     "data/output/storm_vs_saidi.csv storm_saidi (= all events minus ex-MED)", D, B, "match"),
    ("C-A3-04", "285 in 2022, 41 in 2024", "285.4;40.8", "minutes (MED)", "deck A3; brief p5",
     "data/output/storm_vs_saidi.csv storm_saidi", D, B, "match"),
    ("C-A3-05", "[chart] stacked columns 2013-2025", "per row", "minutes", "deck A3 chart",
     "data/output/storm_vs_saidi.csv; snapshot work/charts/v0/a3_exmed_vs_med.csv", D, B, "match"),
    # ---------------------------------------------------------------- S5 demand
    ("C-S5-01", "+39–41%", "39;41;39.0-41.0;about +27%;27;26.9-27.4", "% (2019→2025)",
     "deck S5, S8; brief p2, p6, p8", "D F11 (HE01-05, HE13-17); wording per orchestrator 07:40", D, B, "match"),
    ("C-S5-02", "Winter set the yearly peak in 2019, 2022 and 2025", "2019;2022;2025", "years",
     "deck S5, S8; brief p2, p6, p8", "D F12", D, B, "match"),
    ("C-S5-03", "25,413 MW winter vs 25,384 MW summer", "25413;25384", "MW (2026 to 29 Oct 2026)",
     "deck S5 right column, notes; brief p6", "D findings.md A4.2 and E1; data/output/dom_seasonal_peak.csv", D, B,
     "match; peaks identical under the 21 Oct and 29 Oct cut-offs (E1)"),
    ("C-S5-04", "rose 26% (19,803 → 24,957 MW) and the lowest 52% (7,167 → 10,903 MW)",
     "26.0;52.1;19803;24957;7167;10903", "% / MW", "deck S5; brief p6, p8", "D F10; data/output/dom_load_annual.csv",
     D, B, "match"),
    ("C-S5-05", "[chart] S5 hourly growth profile; brief peaks chart 2019-2026 (GW)", "per row", "%; GW",
     "deck S5 chart; brief p6", "data/output/dom_load_profile.csv, dom_seasonal_peak.csv; snapshots "
     "work/charts/v1/s5_hourly_growth_2019_2025.csv, s5_winter_summer_peaks_v1.csv", D, B, "match"),
    ("C-S5-08", "average load rose 33% (32% unadjusted)", "33;32", "% (2019 → 2025, degree-day normalised vs actual)",
     "deck S5 notes; brief p6", "D findings.md A4.4 (11,438 → 15,235 MW normalised; 11,687 → 15,404 actual)", D, B,
     "match: exploratory, said so in the brief source line"),
    ("C-S5-09", "2026 to the hour ending midnight, 29 Oct", "2026-10-29;29", "EIA-930 cut-off",
     "deck S5 right column, source, notes; brief p6, p8", "D findings.md E1 (last value 2026-10-30 04:00 UTC); "
     "storyline lock 08:25", D, B, "match"),
    ("C-S5-06", "Of the 50 highest hours … July 2018 to December 2025, 47 fell in 2025", "47;50", "hours",
     "brief p6; qsheet T36 (the 50 highest hours, ranked with ROW_NUMBER in sql/06)",
     "D F13 (wording per D)", D, B, "match"),
    ("C-S5-07", "rose 65% from 2013 to 2025 (39.08 → 64.62 TWh) on 8% more commercial customers",
     "65.4;39.08;64.62;7.9", "% / TWh", "brief p6", "D F14 (PUDL core_eia861__yearly_sales, 19876 VA, commercial)", D,
     B, "match"),
    # ---------------------------------------------------------------- S6 plan, role
    ("C-S6-01", "99.8% of meters", "99.8", "% of meters that are AMI (2025)", "deck S6 card 2, notes; brief p7",
     "D F15 (PUDL AMI 2025: 99.8% of 2,682,315 meters)", D, B,
     "match; the lock says 'of customers' but the measure is meters, so the text says meters"),
    ("C-S6-02", "32% reduction in outage minutes on feeders hardened for at least 12 months (as of 30 November 2023)",
     "32", "%", "deck S6 notes; brief p7", "R-036 (Dominion Grid Resiliency page, read 1 Nov 2026)", R, B, "match"),
    ("C-S6-03", "at least 500 customers whose average SAIDI is more than 2 minutes worse … last five years",
     "500;2;5", "customers; minutes; years", "deck S6 notes (five years); brief p7", "R-037", R, B, "match"),
    ("C-S6-04", "Four programmes … The Strategic Underground Program is separate", "4", "programmes", "brief p7",
     "R-035", R, B, "match; the lock's S6 lists SUP under Grid Resiliency, R-035 says SUP is outside it (flagged)"),
    ("C-S6-05", "about 2.7 million customer-minutes", "2.68", "million customer-minutes", "brief p8",
     "B arithmetic: 2,675,735 customers (D F06) x 1 minute", B, B, "match"),
    ("C-R-01", "Associate Business Intelligence Analyst / Business Intelligence Analyst (Richmond, hybrid: three days "
     "in the office, two remote)", "3-2", "text", "brief p7; qsheet R5", "R-002, R-009 (posting closed per R-008)",
     R, B, "match; worded 'most likely matches'"),
    ("C-R-02", "Power BI, SQL, Excel, Snowflake, Power Apps and SharePoint", "tools", "text",
     "brief p7; qsheet O9 (Power BI, SQL, Excel and Snowflake)",
     "R-003, R-004, R-006", R, B, "match"),
    # ---------------------------------------------------------------- S7 build
    ("C-S7-01", "831,288 rows", "831288;831,000", "rows (NOAA Storm Events 2013-2025)", "deck S7, A4; brief p10",
     "docs/01_sources.md S5; D F04", D, B, "match"),
    ("C-S7-02", "6,077,232 rows", "6077232", "rows (EIA-930)", "deck S7, A4; brief p10", "docs/01_sources.md S8", D, B,
     "match"),
    ("C-S7-03", "24,358 + 977 rows", "24358;977", "rows (PUDL reliability; EIA-861 2025)", "deck S7, A4; brief p10",
     "docs/01_sources.md S1, S2", D, B, "match"),
    ("C-S7-04", "11,803", "11803", "rows (EIA-861 Service Territory)", "deck A4; brief p10", "docs/01_sources.md S7", D,
     B, "match"),
    ("C-S7-05", "12 tests pass", "12", "tests", "deck S7, A4; brief p8, p10",
     "data/output/test_results.csv (T1-T31, all PASS; D commit f444a31): T1-T12 are the original pipeline's "
     "tests; D reverify_2_2.md header; docs/03", D, B, "match; v1 adds T13-T31 for the new sources (C-S7-10)"),
    ("C-S7-06", "22 decisions", "22", "decisions", "deck S7 badge, source, notes ('twenty-two'); brief p8",
     "docs/04_decisions.md D1-D22 (D15-D21 added with the new sources, D22 Bedford city, commit 06631ad)", D, B,
     "match; v1 earlier said 14 (D1-D14), stale once D15-D22 landed; 'peers fixed before any results' = D10 only"),
    ("C-S7-07", "2,675,735 customers", "2675735", "customers (2025)", "deck A4; brief p8, p10", "D F06; test T4", D, B,
     "match"),
    ("C-S7-08", "SAIDI = SAIFI × CAIDI within 2%", "2", "% (test T2)", "deck A4; brief p10", "docs/03 T2", D, B,
     "match"),
    ("C-S7-09", "Jul 2018–Oct 2026", "2018-07;2026-10", "EIA-930 coverage", "deck A4; brief p10",
     "docs/01_sources.md S8; D findings.md E1 (2026 values to 29 Oct)", D, B, "match"),
    ("C-S7-10", "T13–T31 check the county outage, storm and load tables (all pass)", "13;31", "tests",
     "deck A4; brief p8, p10", "data/output/test_results.csv (T13-T31 all PASS; D commit f444a31); "
     "docs/03_data_quality.md T13-T31", D, B, "match"),
    ("C-S7-11", "12 of 12 rebuilt values match the published figures", "12", "values",
     "deck S7 badge, notes ('twelve of twelve'); brief p2, p8",
     "data/output/reconciliation.csv (12 rows, all MATCH, incl. 130.2 vs 130 and 133.0 vs 133; D commit f444a31)",
     D, B, "match; supersedes the earlier 13 of 13 (two internal rows of findings A5 dropped by D)"),
    ("C-S7-12", "11,608,442", "11608442;15", "rows (EAGLE-I Virginia, Nov 2014-2025, 15-minute county readings)",
     "deck A4; brief p10 (and '15 minutes' p5)", "docs/01_sources.md S12; docs/03 T13; D ledger D2.1", D, B, "match"),
    # ---------------------------------------------------------------- S8 resume map
    ("C-S8-01", "Snowflake pipeline, 20M+ rows", "20M+", "rows", "deck S8, notes; qsheet O1, T36, T17",
     "Resume: Mercury Insurance, Data Analyst, bullet 1", CV, B, "match"),
    ("C-S8-02", "Root-cause analysis on joined data", "text", "text", "deck S8, notes",
     "Resume: Mercury Insurance bullet 2", CV, B, "match"),
    ("C-S8-03", "Validation and reconciliation", "text", "text", "deck S8, notes", "Resume: Mercury Insurance bullet 3",
     CV, B, "match"),
    ("C-S8-04", "Metadata and business definitions", "text", "text", "deck S8", "Resume: Mercury Insurance bullet 6", CV,
     B, "match"),
    ("C-S8-05", "Requirements with operations and IT", "text", "text", "deck S8", "Resume: Mercury Insurance bullet 5",
     CV, B, "match"),
    ("C-S8-06", "Mercury Insurance, Data Analyst, 2026 to present", "Apr 2026-present", "dates", "deck S8 source",
     "Resume: Professional Experience, Mercury Insurance", CV, B, "match"),
    # ---------------------------------------------------------------- question sheet (P2); reused rows above
    #  carry 'qsheet' in used_in
    ("C-Q-01", "three years building dashboards, reporting and data pipelines", "3", "years of experience",
     "qsheet O1", "Resume: Summary ('3 years of experience')", CV, B, "match"),
    ("C-Q-02", "Helped cut average settlement time by 17% over two months", "17;2", "%; months", "qsheet B1, B8",
     "Resume: Mercury Insurance bullet 2", CV, B, "match"),
    ("C-Q-03", "71% to 90%", "71;90", "% grounded-answer accuracy", "qsheet B6 ('71% to 90%'), B8 ('71% → 90%')",
     "Resume: Mercury Insurance bullet 3", CV, B, "match"),
    ("C-Q-04", "150-question test set", "150", "questions", "qsheet B6", "Resume: Mercury Insurance bullet 3", CV, B,
     "match"),
    ("C-Q-05", "on-time renewals +9%", "9;+9%", "% lift (A/B test)", "qsheet B8", "Resume: Mercury Insurance bullet 4",
     CV, B, "match"),
    ("C-Q-06", "$690M across 440 investments", "690;440", "$ million; investments", "qsheet T1",
     "Resume: The Life Initiative bullet 1 ('$690M and 440 investments')", CV, B, "match"),
    ("C-Q-07", "by up to 50 basis points", "50", "basis points (authorized ROE adjustment)", "qsheet O2",
     "R-059: 2025 Annual Report printed pp. 18-19 ('may include reliability')", R, B,
     "match; worded 'on factors that include reliability'"),
    ("C-Q-08", "travel up to 25%", "25", "% travel", "qsheet R4", "R-009 (posting: 'Travel Up to 25%')", R, B, "match"),
    ("C-Q-09", "cannot sponsor or transfer a work visa for this position", "text", "text", "qsheet R7",
     "R-010 (posting: 'cannot transfer or sponsor a work visa or employment authorization for this position')", R, B,
     "match"),
    ("C-Q-10", "the Virginia SCC's final order is due by mid-January 2027", "2027;2026-05;2026-09", "dates",
     "qsheet R2 (also: announced May 2026; shareholders approved September; SC, NC, FERC and NRC must also "
     "approve; closing expected in the second half of 2027)",
     "R-049 (CEO, Q3 call: VA final order by 11 Jan 2027; close H2 2027), R-053 (mid-January 2027), R-048 "
     "(approvals required); dossier §3 (D3 release 18 May 2026; D5/D8 shareholders approved September 2026)", R,
     B, "match; calendar as reported, no prediction"),
    ("C-Q-11", "The company says Dominion Energy Virginia stays separately regulated and accountable to the SCC",
     "text", "text", "qsheet R2", "R-052 (company response, 19 Oct 2026: 'remain locally led, separately regulated "
     "and fully accountable to the State Corporation Commission')", R, B, "match; attributed to the company"),
    ("C-Q-12", "six DirectQuery tables pointed at an old Snowflake trial", "6", "tables", "qsheet T7",
     "work/powerbi_fix_plan.md §0.1 (6 DirectQuery tables to the old trial) and F1 (Import from local CSVs via "
     "the DataFolder parameter); docs/04_decisions.md D13 (DirectQuery during development, Import for "
     "presentation)", B, B, "match; the project, never Power BI Service at work"),
]


def deck_text() -> str:
    from pptx import Presentation
    prs = Presentation(str(DECK))
    out = []
    for s in prs.slides:
        for sh in s.shapes:
            if sh.has_text_frame:
                out.append(sh.text_frame.text)
            if getattr(sh, "has_table", False) and sh.has_table:
                for row in sh.table.rows:
                    out.extend(c.text for c in row.cells)
        if s.has_notes_slide:
            out.append(s.notes_slide.notes_text_frame.text)
    return " ".join(" ".join(out).split())


def html_text(path: Path) -> str:
    h = path.read_text(encoding="utf-8")
    h = re.sub(r"<style>.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"<svg.*?</svg>", " ", h, flags=re.S)
    h = re.sub(r"<span class='n'>\d+</span>", " ", h)      # question-sheet question numbers 1-24
    return " ".join(htmllib.unescape(re.sub(r"<[^>]+>", " ", h)).split())


def brief_text() -> str:
    return html_text(BRIEF)


def qsheet_text() -> str:
    return html_text(QSHEET)


NUM = re.compile(r"(?<![\w.\-–])[−+-]?\d[\d,]*(?:\.\d+)?%?")
IGNORE = {"1366", "861", "930", "19876", "2.5", "30", "31", "60", "61", "90", "24", "25"}


def norm(t: str) -> str:
    return t.replace("−", "-").replace(",", "").rstrip("%").lstrip("+")


def main():
    with open(IP / "claims.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HEADER)
        w.writerows(ROWS)
    print(f"claims.csv: {len(ROWS)} rows")
    dt, bt, qt = deck_text(), brief_text(), qsheet_text()
    covered = set()
    for r in ROWS:
        for fld in (r[1], r[2]):
            for m in NUM.findall(fld):
                covered.add(norm(m))
    missing = {}
    for name, txt in (("deck", dt), ("brief", bt), ("qsheet", qt)):
        for m in NUM.findall(txt):
            n = norm(m)
            try:
                v = float(n)
            except ValueError:
                continue
            if 2013 <= v <= 2026 and "." not in n:      # years
                continue
            if v <= 14 and "." not in n and not m.endswith("%"):  # slide/page numbers, counts like 3, 12
                continue
            if n not in covered and n not in IGNORE:
                missing.setdefault(name, set()).add(m)
    for k, v in missing.items():
        print(f"numbers in the {k} not covered by a row ({len(v)}):", " ".join(sorted(v)))
    # exact_text presence (first 30 chars of each claim, rough)
    for r in ROWS:
        probe = r[1].split("…")[0].strip()
        if probe.startswith("["):
            continue
        if probe and probe not in dt and probe not in bt and probe not in qt:
            print(f"  not found verbatim: {r[0]} {probe!r}")
    # stale values that must never print again in v1 (pre-D22 storm county-days; the old reconciliation count;
    # the 1-hour Isaias figure)
    for bad in ("465", "796", "851", "13 of 13", "thirteen", "343,492", "545,548", "fourteen", "D1–D14",
                "14 decisions"):
        for name, txt in (("deck", dt), ("brief", bt), ("qsheet", qt)):
            if re.search(rf"(?<![\d,.]){re.escape(bad)}(?![\d,])", txt):
                print(f"  STALE {bad!r} in the {name}")
    # no salary figure anywhere: a dollar amount on the question sheet must be a resume figure
    for m in re.findall(r"\$\s?\d[\d,.]*\s?[kKmMbB]?", qt):
        if m not in ("$690M",):
            print(f"  CHECK dollar figure on the question sheet: {m!r}")


if __name__ == "__main__":
    main()
