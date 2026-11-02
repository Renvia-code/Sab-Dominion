"""Interview brief, final (P3): brief v3 plus rulings O-34 to O-39 (after V6, work/reviews/V6_candidate_read.md).

Final structure (12 pages; main body 8, appendix 4):
  1 the cover merged with the project on one page (contents, the answer first, the eight-minute talk)
  2 Dominion on a page (R's company box, top half) and the glossary (R's, bottom half): spec items 7 and 8
  3 Finding 1, with the two-sided lines; 4 Finding 2; 5 Finding 3; 6 Finding 4 (hour ending); 7 the report and the
  build (the model line, the real data path); 8 the role and the first 90 days
  A1 know every number; A2-A3 the 25 hardest (R's file, with FIXES); A4 delivery and rehearsal, with the
  "30-second opener", the "60-second project story" and the "5-minute route"
The authorship sentence is never printed (correction 1 to C.3): Q18 points to START_HERE section 8.

v3 notes follow. Brief v3: brief v2 plus ruling O-33 from the V1 number audit (CAIDI is
"minutes per interruption"; the test split; public-only medians and method labels as origin/main prints them; the 31
mapped vs 33 Dominion-only counties; talk times for both deck variants) and the print-proof margins (every text item
at least 0.30 in from every page edge). One variant-neutral version (G2, O-28); HTML + print CSS -> Edge PDF.

O-29 page budget: 12 pages at most. Main body 8 (cover and contents included):
  1 cover + contents, 2 the answer first and the 8-minute talk, 3 Finding 1 (130 -> 133), 4 Finding 2 (Dominion and
  11 peers), 5 Finding 3 (weather), 6 Finding 4 (load shape), 7 the Power BI report and how it's built, 8 the role
  and the first 90 days.
Appendix 4: A1 "Know every number", A2-A3 "The 25 hardest" (R's research/hard25_print.md laid out in two columns;
  claim-id tags stripped, wording otherwise R's), A4 "Delivery and rehearsal" (R's Page A, compressed, plus a short
  rehearsal outline; Page B goes to START_HERE).
Material that depends on adopting the 1 Nov upgrade is tagged "If adopted", with the public-only line beside it.
Type: running text 10.5 pt; main-body tables 10 pt; appendix tables and Q&A 9 pt; nothing below 9 pt (O-29).
US English and US dates (O-30). Every number is in interview-prep/claims.csv.

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\brief\\build_brief_final.py
Out:  interview-prep/deliverables/03_interview_brief/Dominion_interview_brief.{html,pdf}
      interview-prep/work/proofs/brief_final/
"""
from __future__ import annotations

import base64
import csv
import html as htmllib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402
import pipeline  # noqa: E402
from final_text import MODEL_LINE, Q18_RULE, Q18_WHO, BUILD_UP, OPENER, STORY, ROUTE, RUNNER  # noqa: E402

CH1 = ds.WORK / "charts" / "v1"
CH2 = ds.WORK / "charts" / "v2"
CHF = ds.WORK / "charts" / "final"
OUT = ds.REPO / "interview-prep" / "deliverables" / "03_interview_brief"
PROOFS = ds.WORK / "proofs" / "brief_final"
STEM = "Dominion_interview_brief"
V6IN = ds.WORK / "v6_inputs"                  # D_facts.md (D) and R_company_glossary.md (R)
RESEARCH = ds.REPO / "interview-prep" / "research"
SHOT = ds.WORK / "powerbi" / "b6" / "s5_summary_v3.png"    # O-33: the card reads "Minutes per interruption"
DECK = ds.REPO / "interview-prep" / "deliverables" / "01_deck"
DECK_STEMS = (("adopted", "Dominion_reliability_deck_adopted"), ("public", "Dominion_reliability_deck_public"))
EDGE_MIN_PT = 21.6                                           # 0.30 in from every page edge (print-proof addendum)
UP = "<span class='up'>If adopted</span>"

EXTRA_CSS = """
:root { --small: 9pt; --small-lh: 12pt; }
@page {
  margin: 0.55in 0.7in 0.65in 0.7in;
  @bottom-left { content: "Dominion Energy Virginia reliability · interview brief"; font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; vertical-align: top; padding-top: 3pt; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; vertical-align: top; padding-top: 3pt; }
}
@page apx {
  margin: 0.4in 0.45in 0.55in 0.45in;
  @bottom-left { content: "Dominion Energy Virginia reliability · interview brief"; font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; vertical-align: top; padding-top: 3pt; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; vertical-align: top; padding-top: 3pt; }
}
.apx-page { page: apx; }
h1 { font-size: 18pt; margin-bottom: 7pt; }
.lede { font-size: 12pt; line-height: 16pt; margin-bottom: 9pt; }
td, th { padding: 2pt 6pt 2pt 0; }
.figures { margin: 6pt 0 8pt; }
.cover-kicker { font-size: 10.5pt; font-weight: 600; color: var(--subject); margin: 0.9in 0 10pt; }
.cover h1 { font-size: 30pt; line-height: 1.1; max-width: 6.6in; margin-bottom: 14pt; }
.cover .who { font-size: 13pt; line-height: 18pt; margin: 18pt 0 0; }
.cover .who strong { font-size: 15pt; }
.contents { margin-top: 0.55in; border-top: 1.5pt solid var(--ink); padding-top: 8pt; }
.contents ol { list-style: none; margin: 0; padding: 0; }
.contents li { display: grid; grid-template-columns: 1fr auto; gap: 12pt; padding: 4pt 0;
               border-bottom: 0.5pt solid var(--rule); font-size: 10.5pt; }
.contents li span.p { color: var(--muted); font-variant-numeric: tabular-nums; }
.contents li.apx { color: var(--ink-2); }
.cover .small { margin-top: 14pt; max-width: 6.4in; font-size: 10pt; line-height: 14pt; }
.cover h1 { font-size: 30pt; }
h2 { margin-top: 10pt; }
table { font-size: 10pt; line-height: 13pt; }
.figure .value { font-size: 32pt; }
ul.tight { margin: 2pt 0 8pt; padding-left: 14pt; }
ul.tight li { margin: 0 0 4pt; }
figure.chart { margin: 6pt 0 2pt; }
figure.chart svg { margin: 0 auto; }
figure.chart.w50 svg { width: 5.0in; }
figure.chart.w52 svg { width: 5.2in; }
figure.chart.w54 svg { width: 5.4in; }
.say { background: var(--tint); border-radius: 3pt; padding: 7pt 10pt; margin: 10pt 0 6pt; }
.say strong { color: var(--ink); }
td.k { white-space: nowrap; font-weight: 600; color: var(--ink); }
.up { display: inline-block; font-size: 9pt; line-height: 11pt; font-weight: 600; color: #7A5A00; background: #FBF1D3;
      padding: 0 3pt; border-radius: 2pt; white-space: nowrap; }
.upg { border-left: 2pt solid var(--third); padding: 1pt 0 1pt 9pt; margin: 8pt 0; }
.code { font-family: Consolas, "Cascadia Mono", monospace; font-size: 9.5pt; line-height: 12.5pt; background: var(--tint);
        padding: 6pt 9pt; border-radius: 3pt; white-space: pre; margin: 4pt 0 6pt; }
img.shot { display: block; width: 4.4in; margin: 2pt auto 2pt; border: 0.5pt solid var(--rule); }  /* final batch: was 5.0in; room for the runner sentence */
.apx-page table, .apx-page { font-size: 9pt; line-height: 11pt; }
.apx-page h1 { font-size: 16pt; margin-bottom: 5pt; }
.apx-page td, .apx-page th { padding: 1.5pt 5pt 1.5pt 0; }
.knum td:first-child { font-weight: 600; color: var(--ink); }
.h25 { column-count: 2; column-gap: 0.2in; font-size: 9pt; line-height: 10.3pt; }
.apx-page h2 { margin-top: 6pt; }
.h25 h3 { font-size: 10pt; line-height: 12pt; margin: 3pt 0 1pt; color: var(--subject); break-after: avoid; }
.h25 .q { break-inside: auto; margin: 0 0 2.5pt; }
.h25 .q p { orphans: 2; widows: 2; }
.h25 .q p { margin: 0; text-wrap: auto; orphans: 1; widows: 1; }
.h25 .q p.hq { font-weight: 600; color: var(--ink); }
.h25 .q p.hq i { font-weight: 400; color: var(--ink-2); }
.h25key { font-size: 9pt; line-height: 11.4pt; color: var(--ink-2); margin: 0 0 5pt; }
.dl td { vertical-align: top; }
td.tt, th.tt { white-space: nowrap; font-variant-numeric: tabular-nums; }
.knum td { padding-top: 1pt; padding-bottom: 1pt; }
.apx-page table.knum { line-height: 10.3pt; }   /* final batch: was 11pt, as A2-A3 (10.3pt); room for the Appalachian line */
table.peers td { padding-top: 1.5pt; padding-bottom: 1.5pt; }
/* final: Finding 1's change chart has empty space under its last bar */
figure.chart.trim { margin-bottom: -22pt; }
.f1 h2 { margin-top: 6pt; }
/* final: page 1 is the cover and the project on one page */
.cover2 .cover-kicker { margin: 0 0 4pt; }
.cover2 h1 { font-size: 20pt; line-height: 1.12; margin-bottom: 6pt; }
.cover2 .lede { font-size: 11.5pt; line-height: 15pt; }
.cover2 .figure .value { font-size: 26pt; }
.contents.c2 { margin-top: 0; padding-top: 4pt; border-top-width: 1pt; }
.contents.c2 ol { column-count: 2; column-gap: 0.3in; }
.contents.c2 li { break-inside: avoid; padding: 1pt 0; }
.c2small { margin: 4pt 0 5pt; font-size: 10pt; line-height: 13pt; color: var(--ink-2); }
.cover2 .lede { margin-bottom: 4pt; }
.cover2 .figures { margin: 4pt 0 4pt; }
.cover2 .figure .value { font-size: 28pt; }
.cover2 h2 { margin-top: 6pt; }
.cover2 table td, .cover2 table th { padding-top: 1.5pt; padding-bottom: 1.5pt; }
/* final: page 2, Dominion on a page (top) and the glossary (bottom) */
@page cgp { margin: 0.42in 0.6in 0.6in 0.6in; }
.cg { page: cgp; font-size: 10pt; line-height: 12.4pt; }
.cg .cbox { background: var(--tint); border-radius: 3pt; padding: 6pt 9pt 2pt; margin: 0 0 4pt; }
.cg .cbox > ul { column-count: 2; column-gap: 0.2in; }
.cg .cbox ul, .cg ul.gl { margin: 1pt 0 2pt; padding-left: 11pt; }
.cg .cbox li, .cg ul.gl li { margin: 0 0 1.5pt; }
.cg .cbox li li { break-inside: avoid; }
.cg h2 { margin: 6pt 0 3pt; }
.cg .cbox h2 { margin: 0 0 3pt; }
.cg .cbox ul ul { margin: 1pt 0 1pt; }
.cg ul.gl { column-count: 2; column-gap: 0.25in; padding-left: 0; list-style: none; }
.cg ul.gl li { break-inside: avoid; }
.cg table.gl td { padding: 1.5pt 6pt 1.5pt 0; }
.cg table.gl td:first-child { white-space: nowrap; font-weight: 600; color: var(--ink); }
/* final: A4's three named pieces */
.say3 { background: var(--tint); border-radius: 3pt; padding: 5pt 8pt 1pt; margin: 2pt 0 6pt; }
.say3 p { margin: 0 0 4pt; }
"""


# ----------------------------------------------------------------------------- helpers
def svg(path: Path) -> str:
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s, flags=re.S)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    return s.strip()


def page(inner: str, cls: str = "") -> str:
    return f'<section class="page {cls}">{inner}</section>'


def ph(s: str) -> str:
    return re.sub(r"\[you:[^\]]*\]", lambda m: f"<span class='placeholder'>{m.group(0)}</span>", s)


def peers_rows() -> str:
    """D's peer file (batch 5) with the method labels fixed in batch 6 (Georgia Power and Duke Energy Florida:
    IEEE 1366; 'Other' in 2013 only)."""
    rows = list(csv.DictReader(open(CH2 / "s3_peer_quadrant_v2_adopted.csv", encoding="utf-8")))
    rows.sort(key=lambda d: -float(d["saifi_5yr_2021_25"]))
    assert sum(d["major_event_method"] == "IEEE 1366" for d in rows) == 10
    out = []
    for d in rows:
        cls = ' class="is-subject"' if d["utility"] == "Dominion Energy Virginia" else ""
        out.append(f"<tr{cls}><td>{d['utility']}</td><td>{d['major_event_method']}</td>"
                   f"<td class='r'>{float(d['saifi_5yr_2021_25']):.2f}</td>"
                   f"<td class='r'>{float(d['caidi_5yr_2021_25']):.1f}</td>"
                   f"<td class='r'>{float(d['saidi_3yr_2023_25']):.1f}</td></tr>")
    return "".join(out)


WPM = 130


def mmss(sec: float) -> str:
    s = int(round(sec))
    return f"{s // 60}:{s % 60:02d}"


def talk_times() -> dict[str, tuple[list[int], int]]:
    """Speaker-note words on S1-S8 of each v3 deck, counted as the deck builder counts them (whitespace split), read
    at WPM words a minute (O-33 item 5: one time column per variant, recounted after the v3 note edits)."""
    from pptx import Presentation
    out = {}
    for key, stem in DECK_STEMS:
        prs = Presentation(str(DECK / f"{stem}.pptx"))
        words = [len(sl.notes_slide.notes_text_frame.text.split()) for sl in list(prs.slides)[:8]]
        assert len(words) == 8 and all(w > 0 for w in words), (key, words)
        out[key] = (words, sum(words))
    return out


# ----------------------------------------------------------------------------- the 25 hardest (R's print file)
TAG = re.compile(r"\s*\[(?:C|N|R)-[A-Za-z0-9-]+(?:,\s*(?:C|N|R)-[A-Za-z0-9-]+)*\]")
RESUME_TAG = re.compile(r"\s*\[resume:[^\]]*\]")
FIXES = [  # (old, new): D batch 6 naming, the final Isaias wording and the v2 proof review; each applies once
    ("inside a band of about 122–168", "inside its 95% prediction interval, about 122–168"),
    ("**Isaias:** 90% of the peak number out, all utilities, timed from the peak",
     "**Isaias:** 33.5 hours from the peak to clear 90% of the outage (a net count, all utilities)"),
    ("mostly because 2025 was stormier", "in a stormier year"),                       # Q24: no causal wording
    ("The SCC docket site blocked automated access, and its report", "The SCC's report"),   # Q9: no research method
    ("the weather fit (CI 0.12–0.92) [C-S4-15]", "the weather fit (ten points)"),     # Q22: CI is upgrade-only
    ("465 → 796; no p.", "465 → 796; no p, CI or prediction interval."),             # Q1: none is on origin/main
    # v3 (O-33): the IEEE count is adopted-only (origin/main labels Georgia Power and Duke Energy Florida "Mixed")
    ("it files under its own rule (\"Other\"); 10 of the 12 utilities use IEEE [N-5].",
     "it files under its own rule (\"Other\"), so methods differ. *Adopted:* 10 of the 12 use IEEE [N-5]."),
    # v3 (O-33, U1): 33 Dominion-only counties in all, 31 of them on the EAGLE-I map
    ("33 of them Dominion-only (D15). The result holds in the\n    Dominion-only counties (19.9×)",
     "33 of them Dominion-only (D15), 31 on the map. The result holds\n    in those 31 (19.9×)"),
    # v3 (C-S6-06 re-sourced to Dominion's release of June 8, 2026): two measures, each with its date, not a trend
    ("**Reported results:** −32% (2023) [C-S6-02] and −44% (2026) [R-013].",
     "**Reported, two measures:** −32% outage minutes, feeders hardened 12+ months (Nov 30, 2023)\n"
     "    [C-S6-02]; −44% average annual outage time for customers in hardened areas (Dominion, June 2026)\n"
     "    [R-013]."),
    # final (O-34 to O-39, after V6): phase 1
    ("storm county-days 464 → 791.", "storm county-days 2024 → 2025: 464 → 791."),              # Q1
    ("- **C:** A small star schema; every number comes from a customer-weighted measure.",       # Q11: C.1
     f"- **C:** {MODEL_LINE} *Public-only:* the same core; the other tables, keyed by year or hour, all\n"
     "  stand alone."),
    ("  - **Tables:** FCT_RELIABILITY (utility × state × year) → DIM_UTILITY.",
     "  - **Counts** (*adopted*): 18 imported tables, 2 calculated (Dashboard Year, _Measures), 2 relationships."),
    ("- **C:** It's in the same SQL build, under tests T13–T31 [C-S7-10].",                      # Q15: slide 6's path
     "- **C:** It's sql/09, the same SQL as the rest, run in the local DuckDB mirror with all 31 tests;\n"
     "  it reaches Snowflake only through one optional step [C-S7-10].\n"
     f"  {RUNNER}"),                                                                           # final batch item 8
    ("Never tell an upgrade change as a discovery story.",                                        # Q18: C.3, corrected
     f"{Q18_RULE}\n  - *Who built the November additions?* {Q18_WHO}"),
    # final: phase 2, from work/v6_inputs/D_facts.md and R's research
    ("The fit starts in 2015 because that's when outage recording became automated (D6) [N-2].",  # Q1: D (a)
     "The fit starts in 2015, when outage recording in the filings became automated (D6, P7) [N-2].\n"
     "    From 2020 they count lines up to 46 kV (not adjusted; it can only push SAIFI and SAIDI up): 2020 sits\n"
     "    14.5 above the line, and the trend test across it still finds no rise (p 0.58)."),
    ("the threshold is T = e^(α+2.5β) [R-070].",                                                 # Q2: D (b)
     "a day is major above T = e^(α+2.5β), α and β the mean\n"
     "    and standard deviation of those logs [R-070]. *Adopted:* EAGLE-I's proxy MEDs (D18) apply the same rule to\n"
     "    daily customer-hours in the 103 counties: 103 days in 2015–25, 2 to 18 a year; stand-ins, not Dominion's."),
    ("**The interval:** bootstrapped by whole days.",                                            # Q5: D (c), (d)
     "**The interval:** 2,000 resamples of whole days: one storm hits many counties on the same day, so\n"
     "    single county-days would make it too narrow."),
    ("**6,108 vs 6,530:** complete EAGLE-I days in 99 counties vs all NOAA days in 103 [N-7].",
     "**6,108 vs 6,530:** complete EAGLE-I days in 99 counties vs all NOAA days in 103 [N-7].\n"
     "  - **CI vs PI:** a CI is for an average or the line (133.9–156.6 at 791); a PI is for one new year,\n"
     "    so wider (122.3–168.2).\n"
     "  - **Trend test:** 11 yearly points, t-test on 9 df: SAIDI p 0.58, slope −1.87 to +3.15 min/yr.\n"
     "    Eleven points catch only a large, steady change: \"can't tell\", not \"nothing changed\"."),
    ("plus a 30-day plan (an exceptions form).",                                                 # Q12: R's answer file
     "plus a 30-day plan: a small form for logging exceptions or\n    field updates that feeds the report."),
    ("**In the project (P18):** a co-op with SAIDI but no SAIFI would have diluted the group figure (1.849 vs 1.887).\n"
     "    Fixed 27 Oct [N-8].",                                                                    # Q17: D (m)
     "**In the project (P18):** for 2025, Prince George Electric filed SAIDI but no SAIFI; its 13,341\n"
     "    customers would have diluted the co-op SAIFI (1.849, not 1.887). I changed V_GROUP_INDEX to count only\n"
     "    customers of utilities that reported the measure (Oct 27) [N-8]."),
    ("**The Grid Resiliency programs:** Mainfeeder Hardening, Voltage Island Mitigation, Voltage Optimization,\n"
     "    Intelligent Grid Devices/FLISR [R-035].",                                               # Q19: R-035, 038, 039
     "**The Grid Resiliency programs** [R-035]: Mainfeeder Hardening rebuilds main lines to stronger\n"
     "    standards; Voltage Island Mitigation adds a second transformer at single-transformer substations (19\n"
     "    sites planned); Voltage Optimization tunes voltage with smart-meter readings (goal: 1% energy savings);\n"
     "    Intelligent Grid Devices (FLISR) isolate a fault and restore the rest."),
    ("no comment on FPL.", "no comment on FPL (Florida Power & Light, NextEra's utility)."),     # Q23: R-110
    # final batch (V1 final audit, V6 re-check), item 6: the same deadline as p. 2, and the SCC staff's Oct 19 position
    # (R-050: "Staff concludes that the Merger as proposed in the Joint Petition should be denied by the Commission")
    ("Virginia's order is due by mid-January 2027; SC, NC, FERC and NRC approvals follow; close is expected\n"
     "    in H2 2027 [C-Q-10].",
     "Virginia's order is due by January 11, 2027; SC, NC, FERC and NRC approvals follow; close is\n"
     "    expected in H2 2027 [C-Q-10]. On Oct 19 the SCC staff recommended denying the merger as proposed unless\n"
     "    the companies accept conditions [R-050]."),
]


def md_inline(s: str) -> str:
    s = TAG.sub("", s)
    s = RESUME_TAG.sub("", s)
    s = s.replace("`[you:", "[you:").replace("]`", "]")
    s = htmllib.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return ph(s)


def hard25_html() -> tuple[str, int]:
    md = (RESEARCH / "hard25_print.md").read_text(encoding="utf-8")
    for old, new in FIXES:
        assert md.count(old) == 1, old
        md = md.replace(old, new)
    lines = md.splitlines()
    i0 = lines.index("## Engineer")
    out, q, part, nq = [], None, None, 0

    def close_part():
        nonlocal part
        if part is not None:
            label, text, items = part
            body = " ".join(x for x in [text] if x)
            if items:
                body = (body + " " if body else "") + " · ".join(items)
            q.append(f"<b>{label}:</b> {md_inline(body)}")
            part = None

    def close_q():
        nonlocal q
        close_part()
        if q is not None:          # header line, then claim, proof and limit run in one paragraph
            out.append(f"<div class='q'><p class='hq'>{md_inline(q[0])}</p><p>" + " ".join(q[1:]) + "</p></div>")
            q = None

    prev_blank = False
    for raw in lines[i0:]:
        blank = not raw.strip()
        if raw.startswith("## "):
            close_q()
            out.append(f"<h3>{htmllib.escape(raw[3:])}</h3>")
        elif raw.startswith("**Q"):
            close_q()
            nq += 1
            q = [raw]                                         # header kept raw until the question closes
        elif q is not None and part is None and len(q) == 1 and raw.strip() and not raw.startswith((" ", "-")):
            q[0] += " " + raw.strip()                         # the header wraps onto a second line
        elif re.match(r"- \*\*(C|P|L|Say):\*\*", raw):
            close_part()
            m = re.match(r"- \*\*(C|P|L|Say):\*\*\s*(.*)", raw)
            part = [m.group(1), m.group(2).strip(), []]
        elif re.match(r"\s{2}(?:- |\d+\. )", raw):            # a sub-item
            part[2].append(re.sub(r"^\s{2}(?:- |\d+\. )", "", raw).strip())
        elif re.match(r"\s{4}\S", raw):                       # a wrapped sub-item
            part[2][-1] += " " + raw.strip()
        elif re.match(r"\s{2}\S", raw):                       # wrapped part text, or a paragraph after a list
            if part[2] and prev_blank:
                part[2].append(raw.strip())
            elif part[2]:
                part[2][-1] += " " + raw.strip()
            else:
                part[1] += " " + raw.strip()
        elif not blank:
            raise ValueError(f"unparsed line in hard25_print.md: {raw!r}")
        prev_blank = blank
    close_q()
    return "".join(out), nq


# ----------------------------------------------------------------------------- page 2: R's company box and glossary
RTAG = re.compile(r"\s*\[[^\]]*?(?:R-\d{3}|C-[A-Z0-9]|docs/|README|brief p\.)[^\]]*\]")
R_FIXES = [  # (old, new) on R's print text (13:00 version), each applied once: pointers into R's own file
    (" (§7).", " (Q2 in A2)."),
    (" See §7.", " See Q2 in A2."),
    ("Virginia SCC case", "Virginia State Corporation Commission (SCC) case"),      # SCC's first use in the brief
    ("**Storm county-day:** \"a day with", "**Storm county-day:** a day with"),     # it quotes the brief itself
    ("counties Dominion serves\". [brief p.5]", "counties Dominion serves. [brief p.5]"),
    # orchestrator: any "10 of 12" in the brief is tagged If adopted (O-33); the 12 include Dominion
    ("10 of 12 peers use it;", "If adopted: 10 of the 12 utilities use it;"),
    ("is one of the 12 peers", "is one of the 11 peers"),           # Dominion and 11 peers, as everywhere else
    # orchestrator and R's note 2: FLISR expanded as the GT booklet words it, everywhere
    ("FLISR, Fault Location, Isolation and Service Restoration:", "FLISR, fault location, isolation, and service "
     "restoration:"),
    ("**FLISR:** Fault Location, Isolation and Service Restoration.", "**FLISR:** fault location, isolation, and "
     "service restoration."),
    # final batch (V1 final audit, V6 re-check), items 1-5: the sources' own wording; each must apply (checks() below)
    ("budget $11.65B; done by end-2027.", "budget $11.65B; completion expected by end-2027."),     # R-061, R-098
    ("typical bill +$11.24 a month (2026)", "typical residential bill +$11.24 a month (2026)"),   # R-058
    ("can be restored. 19 sites.", "can be restored. 19 sites planned."),                         # R-114, R-038
    ("of about 4,000. Due 2029.", "of about 4,000. Expected by 2029."),                           # R-012
    ("28% of Virginia Power's 2025 sales", "28% of Dominion Energy Virginia's 2025 sales"),       # R-112, a name
]


def r_sections() -> dict[str, str]:
    md = (V6IN / "R_company_glossary.md").read_text(encoding="utf-8")
    for old, new in R_FIXES:                       # R revises the file; a fix whose text is gone is reported, not fatal
        n = md.count(old)
        assert n <= 1, old
        if n:
            md = md.replace(old, new)
        else:
            print("  R fix not applicable (text not in R's file):", ascii(old))
    parts = re.split(r"^## (\d)\. .*$", md, flags=re.M)
    sec = {parts[i]: parts[i + 1] for i in range(1, len(parts), 2)}
    sec["2"] = sec["2"].split("**Spare lines, if there is room:**")[0]   # R: drop tags first, then the spare lines
    return sec


def r_inline(s: str) -> str:
    s = RTAG.sub("", s).strip()
    s = htmllib.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    return ph(s.replace("If adopted:", UP))


def r_list(body: str) -> tuple[str, str]:
    """R's bullets ('- ' and '  - ', wrapped lines indented) as nested <li>s; returns (bold title line, list HTML)."""
    title, items = "", []
    for raw in body.splitlines():
        if not raw.strip() or raw.strip() == "---":
            continue
        m = re.match(r"^( *)- (.*)$", raw)
        if m:
            items.append([len(m.group(1)) // 2, m.group(2)])
        elif raw.startswith(" ") and items:
            if RTAG.sub("", raw).strip():
                items[-1][1] += " " + raw.strip()
        elif re.fullmatch(r"\*\*.+\*\*", raw.strip()):
            title = raw.strip().strip("*")
        else:
            raise ValueError(f"unparsed line in R's file: {raw!r}")
    out, open_sub = [], False
    for k, (lvl, txt) in enumerate(items):
        if lvl == 0:
            if open_sub:
                out.append("</ul></li>")
                open_sub = False
            elif k:
                out.append("</li>")
            out.append(f"<li>{r_inline(txt)}")
        else:
            if not open_sub:
                out.append("<ul>")
                open_sub = True
            out.append(f"<li>{r_inline(txt)}</li>")
    out.append("</ul></li>" if open_sub else "</li>")
    return title, "".join(out)


def company_glossary_html() -> str:
    sec = r_sections()
    title, box = r_list(sec["1"])
    _, gl = r_list(sec["2"])
    assert title.startswith("Dominion Energy at a glance") and gl.count("<li>") == 22, (title, gl.count("<li>"))
    assert "§" not in box + gl and not re.search(r"\bR-\d{3}|\bC-[A-Z]", box + gl), "a pointer or a tag would print"
    return (f'<p class="section-no">Dominion on a page</p>'
            f'<div class="cbox"><h2>{htmllib.escape(title)}</h2><ul>{box}</ul></div>'
            f'<h2>Glossary</h2><ul class="gl">{gl}</ul>')


# ----------------------------------------------------------------------------- pages
def build_html() -> str:
    css = (ds.WORK / "design" / "brief.css").read_text(encoding="utf-8") + EXTRA_CSS
    shot = base64.b64encode(SHOT.read_bytes()).decode("ascii")
    h25, nq = hard25_html()
    assert nq == 25, nq
    T = talk_times()
    secs_a = [int(round(w * 60 / WPM)) for w in T["adopted"][0]]
    secs_p = [int(round(w * 60 / WPM)) for w in T["public"][0]]
    tt = [f"<td class='r tt'>{mmss(a)} · {mmss(p)}</td>" for a, p in zip(secs_a, secs_p)]
    ta, tp = sum(secs_a), sum(secs_p)            # the table adds up: totals are the sums of the printed slide times
    print("talk words:", T, "->", mmss(ta), mmss(tp))
    P = []

    # ------------------------------------------------------------------ 1 cover merged with the project on one page
    P.append(page(f"""
<div class="c2head">
 <div><p class="cover-kicker">Interview brief · Saketh Bollina · panel interview, Tuesday, November 3, 2026</p>
 <h1>Dominion Energy Virginia reliability: what public data shows, and where I'd look first</h1></div>
</div>
<div class="contents c2"><ol>
<li><span>The project on one page, and the talk</span><span class="p">1</span></li>
<li><span>Dominion on a page, and the glossary</span><span class="p">2</span></li>
<li><span>Finding 1 · 130 → 133: a stormier year</span><span class="p">3</span></li>
<li><span>Finding 2 · Frequency is the peer gap</span><span class="p">4</span></li>
<li><span>Finding 3 · Weather: on the storm line</span><span class="p">5</span></li>
<li><span>Finding 4 · Demand: nights and winters</span><span class="p">6</span></li>
<li><span>The Power BI report, and the build</span><span class="p">7</span></li>
<li><span>The role, and the first 90 days</span><span class="p">8</span></li>
<li class="apx"><span>A1 · Know every number</span><span class="p">9</span></li>
<li class="apx"><span>A2–A3 · The 25 hardest questions</span><span class="p">10</span></li>
<li class="apx"><span>A4 · Delivery and rehearsal</span><span class="p">12</span></li>
</ol></div>
<p class="small c2small">All figures come from public data or Dominion's own publications; none is internal. {UP} marks
material that depends on adopting the repo upgrade; <span class="placeholder">[you: …]</span> is yours to fill in.</p>
<p class="section-no">The project on one page</p>
<p class="lede">Dominion's reported outage minutes rose from 130 to 133; rebuilt from public EIA-861 data they are
130.2 and 133.0. 2025 had more storms and more interruptions, and once storms are counted there is no clear
underlying trend. Against its peers, Dominion's gap is how often customers lose power, not how long.</p>
<div class="figures">
 <div class="figure is-subject"><div class="value subject">+2.8</div><div class="label">minutes: the rebuilt 3-year
 average, 130.2 → 133.0. 2025 (144.4) replaced 2022 (136.0) in the window</div></div>
 <div class="figure"><div class="value">+10%</div><div class="label">both storm county-days and interruptions per
 customer (SAIFI), 2022 → 2025; minutes per interruption (CAIDI) −4%</div></div>
 <div class="figure"><div class="value">4th highest</div><div class="label">of 12 on frequency (SAIFI 2021–25: 1.21);
 6th of 12 on minutes per interruption. Peer medians differ by deck: page 4</div></div>
</div>
<h2>The eight-minute talk, slide by slide</h2>
<table>
<tr><th>#</th><th>Slide</th><th>Say it in one line</th><th class="r tt">Adopted ·<br>public</th></tr>
<tr><td class="k">1</td><td>Title</td><td>Independent analysis of public data; nothing internal.</td>{tt[0]}</tr>
<tr><td class="k">2</td><td>130 → 133</td><td>2025 replaced 2022 in the window; SAIFI +10%, CAIDI −4%, storm county-days
+10%. Dominion attributes the rise “primarily” to storms; 2025 sits on the storm line.</td>{tt[1]}</tr>
<tr><td class="k">3</td><td>Dominion and 11 peers</td><td>Length mid-pack (6th of 12), frequency 4th highest; methods
differ, so ranks are indicative.</td>{tt[2]}</tr>
<tr><td class="k">4</td><td>Storms</td><td>{UP} Storm county-days had about 12 times the outage hours of calm days
(11.9×, 95% CI 7.9–16.9), an association. Public-only: r = 0.70 over ten years.</td>{tt[3]}</tr>
<tr><td class="k">5</td><td>The Power BI report</td><td>One page per question; customer-weighted measures; a year slicer;
Import (D13).</td>{tt[4]}</tr>
<tr><td class="k">6</td><td>How it's built</td><td>RAW → STG → MART, tests, a dictionary, a decisions log; reconciled
to 130 and 133.</td>{tt[5]}</tr>
<tr><td class="k">7</td><td>First 90 days</td><td>The questions I'd bring, ending on a Power BI program-tracking
report.</td>{tt[6]}</tr>
<tr><td class="k">8</td><td>Close</td><td>Three takeaways, then: “I've built a tested Snowflake → Power BI pipeline on
public reliability data.”</td>{tt[7]}</tr>
</table>
<p class="source">Speaker notes at about {WPM} words a minute: {mmss(ta)} in all (adopted), {mmss(tp)} (public-only).
A 5-minute slot: A4.</p>
""", "cover2"))

    # ------------------------------------------------------------------ 2 Dominion on a page + glossary (R)
    P.append(page(company_glossary_html(), "cg"))

    # ------------------------------------------------------------------ 3 finding 1
    P.append(page(f"""
<p class="section-no">Finding 1</p>
<h1>Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions</h1>
<p>SAIDI, the average outage minutes per customer, is SAIFI (how often a customer loses power) times CAIDI (how long
each interruption lasts). Dominion's 2025 Annual Report gives a 3-year SAIDI, excluding major events, of 133 minutes
for 2023–25, up from 130 for 2022–24, and explains it (p. 10): “This increase is primarily due to increased storm
activity.” The public Virginia data reproduces both: 130.2 and 133.0.</p>
<p>A 3-year average moves when a year leaves the window: 2025 (144.4 minutes) replaced 2022 (136.0), a rise of 2.8
minutes in the average. The weather fit (Finding 3) puts 2025 on the storm line, so the public data agrees with
Dominion's reading: once storms are counted there is no clear underlying trend.</p>
<figure class="chart w50 trim">{svg(CH2 / "s2_change_2022_2025_adopted.svg")}</figure>
<p class="source">Source: EIA-861 2025 final and PUDL 2013–2024, Dominion Energy Virginia, excluding major event days;
NOAA Storm Events. Storm county-days 718 → 791 count Bedford city once (D22, {UP}); the public repo has 723 → 796,
also +10%. Reported figures: Dominion Energy 2025 Annual Report, p. 10.</p>
<h2>Three base years, three answers: say which one you mean</h2>
<table>
<tr><th>Base year → 2025</th><th class="r">SAIDI</th><th class="r">SAIFI</th><th class="r">CAIDI</th>
<th class="r">Share from frequency</th></tr>
<tr><td>2019: the report's long view (its chart titles)</td><td class="r">−3.7%</td><td class="r">+6.1%</td>
<td class="r">−9.2%</td><td class="r">SAIDI fell</td></tr>
<tr class="is-subject"><td>2022: the two years that swap (slide 2)</td><td class="r">+6.1%</td><td class="r">+10.1%</td>
<td class="r">−3.6%</td><td class="r">more than all of it</td></tr>
<tr><td>2023: the latest 3-year window</td><td class="r">+17.1%</td><td class="r">+13.3%</td><td class="r">+3.3%</td>
<td class="r">79%</td></tr>
</table>
<p class="source">From every base, interruptions per customer rose more than minutes per interruption.</p>
<h2>Say it carefully: the two-sided lines</h2>
<ul class="tight">
<li>If asked “so reliability got worse?”: “2025 had more storms and more interruptions, and Dominion attributes the
rise primarily to storms. With outage records, I'd check whether non-storm interruptions are rising underneath.”</li>
<li>2025's SAIFI (1.320) only edges 2018's (1.303), and 2025's outage minutes (144.4) are below 2018 (149.6) and
2019 (149.9). One year is not a trend.</li>
<li>No 2015–2025 trend is statistically clear, with or without adjusting for storm days. {UP} SAIFI p = 0.54,
CAIDI p = 0.74, SAIDI p = 0.58 (scripts/trend_tests.py); storm-adjusted, about +0.34 minutes a year (95% CI −1.41 to
+2.08, p = 0.67). Public-only: say “no clear trend” without p-values.</li>
</ul>
""", "f1"))

    # ------------------------------------------------------------------ 4 finding 2
    P.append(page(f"""
<p class="section-no">Finding 2</p>
<h1>Among 12 large utilities (Dominion and 11 peers), interruption length is mid-pack; frequency is the gap</h1>
<p>Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before results were computed
(decision D10); means of 2021–2025, excluding major event days. Dominion's SAIFI of 1.21 is the 4th highest of the 12;
its CAIDI of 110 minutes is 6th, mid-pack; its 3-year SAIDI, 133.0, is 4th. {UP} The chart's lines are the medians of
the 11 peers, 0.93 and 99.5; the public repo prints 0.96 and 105, the medians of all 12 including Dominion.</p>
<figure class="chart w54">{svg(CH2 / "s3_peer_quadrant_v2_adopted.svg")}</figure>
<table class="peers">
<tr><th>Utility</th><th>Major-event method</th><th class="r">SAIFI 2021–25</th><th class="r">CAIDI 2021–25</th>
<th class="r">SAIDI 2023–25</th></tr>
{peers_rows()}
</table>
<p class="source">Source: EIA-861 / PUDL, excluding major event days, means of annual values; the chart and the table's
method labels are the adopted deck's. Georgia Power and Duke Energy Florida filed “Other” in 2013 only (public
workbook: “Mixed”). Public-only, the deck prints the medians as the public repo does (docs/05).</p>
<div class="say"><strong>The caveat to raise yourself:</strong> methods differ. Dominion reports under its own
major-event rule, so ranks are indicative ({UP} 10 of the 12 file IEEE 1366 every year 2014–25; public-only, give
no count). If asked: with all events, Dominion's SAIFI (1.531) ranks 6th of 12 (median of the other 11, 1.408), its
SAIDI 2023–25 (223.0) 9th. Either way, the gap is frequency, not interruption length.</div>
"""))

    # ------------------------------------------------------------------ 5 finding 3
    P.append(page(f"""
<p class="section-no">Finding 3</p>
<h1>Weather: years with more storm days had more outage minutes, and 2025 sits on the storm line</h1>
<p>A storm county-day is a day with a NOAA wind, winter or tropical storm report in one of the 103 Virginia counties
Dominion serves. Over 2015–2024, storm county-days and SAIDI excluding major events move together: r = 0.70 (n = 10).
A fit made without 2025 gives 145.3 minutes for 2025's storm count, against 144.4 actual. Ten points is thin, so this
is a check, not a forecast. {UP} p = 0.025; 95% CI for r 0.12 to 0.92; the 95% prediction interval for 2025 was 122.3
to 168.2 (the confidence interval of the line itself, 133.9 to 156.6). Storm county-days 2024 → 2025: 464 → 791
{UP}; 465 → 796 on the public repo.</p>
<div class="upg"><p>{UP} <strong>County-days with a storm report had about 12 times the outage hours of calm
days.</strong> EAGLE-I, the Department of Energy's county outage record, counts the customers out every 15 minutes.
On 6,108 storm county-days with complete outage readings (99 counties on the map), outage customer-hours per 1,000
customers averaged 332.8 (95% interval 225.6–453.4), against 27.9 (23.1–33.2) on calm county-days: 11.9 times (95%
CI 7.9–16.9, resampling whole days). It holds on non-major days (9.9×), in the counties Dominion serves alone
(19.9×) and in every year (5.9× to 27.4×, every interval above 1). It is an association: EAGLE-I counts every
utility's customers, and storm reports partly follow damage. 6,108 is the NOAA count of 6,530 less 114 storm
county-days in four counties off the map and 308 with a failed reading (96 of them in 2025, when only 74% of
county-days are complete).</p></div>
<figure class="chart w52">{svg(CH2 / "b_county_map_all_utilities.svg")}</figure>
<p class="source">{UP} Source: EAGLE-I (ORNL for DOE), customers of all utilities in 99 of Dominion's 103 Virginia
counties (four cities left off: unusable data). Counties with 20,000 or more customers range from 55 minutes a year
(Prince William County) to 633 (Pittsylvania County). Not Dominion's SAIDI.</p>
<ul class="tight">
<li>{UP} The 31 mapped counties Dominion serves alone have a customer-weighted average of 159 minutes a year,
against 211 in the 68 shared counties. That compares places (mostly cities and inner suburbs against rural
counties), not utilities.</li>
<li>{UP} Isaias, August 2020: 33.5 hours from the peak to clear 90% of the outage (351,738 customers out at the
peak; a net count, all utilities, not a utility's “% of affected customers restored”). Across 47 events with 50,000
or more customers out, there is no evidence that clearing got faster (+4.6% a year after allowing for size,
p = 0.07).</li>
<li>What none of this can say: which circuits, which causes, or whether hardened lines held up. That needs outage
records by circuit and cause.</li>
</ul>
"""))

    # ------------------------------------------------------------------ 6 finding 4
    P.append(page(f"""
<p class="section-no">Finding 4</p>
<h1>Overnight demand grew faster than afternoon demand, and winter rivals summer for the yearly peak</h1>
<p>EIA-930 hourly demand for the PJM Dominion (DOM) zone, which is wider than Dominion's retail territory. From 2019
to 2025, average load in the hour ending 4 a.m. rose 41%, against 27% in the hour ending 4 p.m.; across the hours
ending 1–5 a.m. the rise was 39–41%. The highest hour of the year rose 26% (19,803 → 24,957 MW) and the lowest 52% (7,167 → 10,903 MW). Winter set
the yearly peak in 2019, 2022 and 2025.</p>
<figure class="chart w54">{svg(CHF / "a3_load_profile_hour_ending.svg")}</figure>
<p class="source">Source: EIA-930 hourly demand, PJM DOM zone; 2019 and 2025 full years. Winter = December–February,
summer = June–August.</p>
<ul class="tight">
<li>Of the 50 highest hours in the EIA-930 record from July 2018 to December 2025, 47 fell in 2025.</li>
<li>Commercial electricity sales in Dominion's Virginia territory rose 65% from 2013 to 2025 (39.08 → 64.62 TWh) on
8% more commercial customers (EIA-861).</li>
<li>{UP} Holding Virginia's daily heating and cooling degree days and the weekday fixed, average load rose 33% (32%
unadjusted), so weather does not explain it. 2026 to October 29: winter 25,413 MW against summer 25,384 MW, a tie.</li>
</ul>
<div class="say"><strong>Don't say “data centers caused it”.</strong> Growth around the clock is consistent with large
constant loads, but these data cannot identify customers. Say: “less overnight slack, and winter readiness matters as
much as summer.” In reports, I'd add winter and overnight views.</div>
"""))

    # ------------------------------------------------------------------ 7 Power BI + how it's built
    P.append(page(f"""
<p class="section-no">The report and the build</p>
<h1>The Power BI report, and how the analysis is built</h1>
<img class="shot" alt="The report's Summary page for 2025: year slicer, five cards, SAIFI and CAIDI since 2013 against
their 2019 levels, actual and weather-adjusted SAIDI, and the storm-day scatter" src="data:image/png;base64,{shot}">
<p class="source">{UP} The Summary page, 2025: customers served 2.68M, SAIDI 144.4, minutes per interruption 109.4,
SAIFI 1.320, major-event share 53%. Public-only: slide 5 shows your report's What moved page; the .pbix is not on
GitHub by design.</p>
<p><strong>The model</strong> ({UP} the template): {MODEL_LINE} SAIDI is customer-minutes over customers within a
year, and the 3-year figure is the mean of the three annual values, as Dominion reports it. Public-only, your own
report: the same core; its other tables are keyed by year or hour and stand alone; DirectQuery against Snowflake
during development, Import for presentation (decision D13).</p>
<p><strong>The build.</strong> Public files land as raw text exactly as published (RAW), are typed and cleaned (STG),
and become facts, dimensions and views (MART). The October build runs this SQL in Snowflake, and
scripts/run_local_duckdb.py rebuilds the core mart locally. Tests run after each load; all pass: T1–T6 the
reliability mart, T7–T9 NOAA storms, T10–T12 EIA-930 demand. {UP} {BUILD_UP} A data dictionary covers every table
and column; measures are defined in docs/05. Decisions are logged (D1–D14; {UP} D1–D22); the peer set was chosen by
EIA ID before results. Reconciled: 130.2 and 133.0 against 130 and 133, and test T4 matches 2025 to EIA's published
306.7, 144.4 and 2,675,735 customers ({UP} 12 of 12 values: a check of definitions).</p>
<table>
<tr><th>Source</th><th>Publisher</th><th>Years</th><th class="r">Rows</th></tr>
<tr><td>EIA-861 Reliability, 2025 final · PUDL EIA-861</td><td>EIA · Catalyst Cooperative</td><td>2025 · 2013–2024</td><td class="r">977 · 24,358</td></tr>
<tr><td>NOAA Storm Events</td><td>NOAA NCEI</td><td>2013–2025</td><td class="r">831,288</td></tr>
<tr><td>EIA-930 hourly demand</td><td>EIA</td><td>Jul 2018–Oct 2026</td><td class="r">6,077,232 · {UP} 6,094,320</td></tr>
<tr><td>{UP} EAGLE-I county outages · DOE-417 · HURDAT2 · CPC degree days</td><td>ORNL for DOE · DOE · NOAA · NOAA</td>
<td>2014–2025 · 2014–2025 · 1851–2025 · 2018–2026</td><td class="r">11,608,442 · 3,702 · 55,524 · 309,504</td></tr>
</table>
"""))

    # ------------------------------------------------------------------ 8 role + 90 days + limits
    P.append(page("""
<p class="section-no">The role</p>
<h1>The role, and what I would do in the first 90 days</h1>
<p>The posting that most likely matches this interview is <strong>Associate Business Intelligence Analyst / Business
Intelligence Analyst</strong> (Richmond, hybrid: three days in the office, two remote). It supports <strong>Grid
Resiliency programs</strong> with Power BI dashboards and reports, and asks for Power BI, SQL, Excel, Snowflake, Power
Apps and SharePoint, with reliability metrics as preferred knowledge.
<span class="placeholder">[you: confirm the exact title and team with the recruiter]</span></p>
<ul class="tight">
<li>Four programs: mainfeeder hardening, voltage island mitigation, voltage optimization, and intelligent grid devices
(FLISR: fault location, isolation, and service restoration). The Strategic Underground Program is separate.</li>
<li>Mainfeeder hardening selects feeders with at least 500 customers whose average SAIDI is more than 2 minutes worse
than the rest, with above-average outages over the last five years. Dominion reports a 32% reduction in outage
minutes on feeders hardened for at least 12 months (as of November 30, 2023).</li>
</ul>
<h2>First 90 days: the questions I'd bring, and what I'd build</h2>
<table>
<tr><th>Days</th><th>What I'd do</th><th>Deliverable</th></tr>
<tr><td class="k">1–30 · Learn, reconcile</td><td>Learn how outages, meter events and circuits are recorded and
reported. Rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filed figures.</td><td>A reconciled
baseline with written definitions</td></tr>
<tr><td class="k">31–60 · Ask about frequency</td><td>Interruptions by circuit and cause code, storm days apart from
calm; repeat interruptions (CEMIn). Outage times from meter last-gasp and restore messages (99.8% of meters are
smart), checked against OMS.</td><td>Tested views and a data dictionary</td></tr>
<tr class="is-subject"><td class="k">61–90 · Track</td><td>Track mainfeeder hardening against matched untreated
feeders (same pre-period performance), weather-normalized, in support of the program's selection rule.</td>
<td><strong>A Power BI program-tracking report on a scheduled refresh</strong></td></tr>
</table>
<p class="source">Check each of these first with the people who own the definitions: they are questions, not
conclusions.</p>
<h2>What public data cannot show, and what would answer it</h2>
<table>
<tr><th>Public data limit</th><th>What would answer it (Dominion data, by type)</th></tr>
<tr><td>One number per utility per year (EIA-861)</td><td>Outage records by event, circuit and cause</td></tr>
<tr><td>Storms counted by county, not by line</td><td>Outage records with cause codes and circuit location</td></tr>
<tr><td>Methods differ between utilities</td><td>Dominion's daily SAIDI and its filing method</td></tr>
<tr><td>The DOM zone is wider than the retail territory</td><td>Meter interval data by circuit</td></tr>
<tr><td>No customer identities: load growth cannot be attributed</td><td>Customer class and large-load records</td></tr>
</table>
<h2>Logistics</h2>
<ul class="tight">
<li>Time, place and format: <span class="placeholder">[you: …]</span> · Panel names and roles:
<span class="placeholder">[you: …]</span></li>
<li>Hybrid 3-2 in Richmond: <span class="placeholder">[you: commute or relocation plan for a hybrid 3-2 schedule in
Richmond]</span> · Work authorization, if asked: <span class="placeholder">[you: …]</span></li>
<li>Salary, if asked: ask about the full scope first; give a researched range only if pressed.
<span class="placeholder">[you: your range]</span></li>
</ul>
"""))

    # ------------------------------------------------------------------ 9 A1 know every number
    K = [  # (number, plain meaning · how computed · source, caveat → likely follow-up)
        ("130 → 133 · 130.2 → 133.0", "Reported 3-year SAIDI ex-MED, 2022–24 → 2023–25 (Annual Report p. 10); "
         "rebuilt as the mean of three annual values. 2022 left the window (136.0), 2025 joined (144.4)",
         "(144.4 − 136.0) ÷ 3 = 2.8. “Primarily due to increased storm activity” → is it real? (Q4)"),
        ("1.199 → 1.320 · 113.5 → 109.4", "SAIFI +10% and CAIDI (SAIDI ÷ SAIFI) −4%, 2022 → 2025 · EIA-861",
         "SAIFI only edges 2018 (1.303); CAIDI is a ratio, not restoration speed"),
        ("718 → 791 · 723 → 796", "Storm county-days 2022 → 2025, +10% (If adopted · public) · NOAA",
         "D22 counts Bedford city once: 38 fewer county-days over 2013–25"),
        ("145.3 vs 144.4 · r = 0.70", "2025 from the storm-day fit (2015–2024, n = 10) vs actual. Fit: If adopted "
         "104.3 + 0.0518 × storm county-days, R² 0.49; public-only 104.4 + 0.0514 ×, R² 0.48",
         "If adopted: 95% prediction interval 122.3–168.2; p = 0.025; CI for r 0.12–0.92 (Q1)"),
        ("1.21 · 4th highest · 110 · 6th", "SAIFI and CAIDI 2021–25 ex-MED, of the 12; medians If adopted 0.93 and 99.5 (11 "
         "peers), public-only 0.96 and 105 (all 12); 3-year SAIDI 133.0, also 4th",
         "All events: SAIFI 1.531, 6th (median 1.408); SAIDI 223.0, 9th"),
        ("Windows", "Slide 3: 2021–25 means (1.21, 110) and a 2023–25 SAIDI; slide 5: 2025 (1.320, 109.4)",
         "Don't cross-quote. Peer SAIDI ≠ SAIFI × CAIDI: different windows; year by year T2 holds within 2%"),
        ("Dominion + 11 peers", "Large investor-owned utilities in PJM and the Southeast, fixed by EIA ID before "
         "results (D10); no size cut-off; a national set was turned down. Appalachian Power is its own group, not a "
         "peer: your October decision D10 (mostly mountain territory; its SAIDI, over 300 minutes, would compress "
         "every chart). Its SAIFI and SAIDI are both above Dominion's, so leaving it out doesn't flatter Dominion.",
         "If adopted: 10 of 12 file IEEE 1366 every year 2014–25; Dominion and Alabama Power file “Other” → ranks "
         "indicative (Q2)"),
        ("11.9× (7.9–16.9) · 9.9× · 19.9×", "If adopted: outage customer-hours per 1,000 customers, storm vs calm "
         "county-days (332.8 vs 27.9); non-major days (proxy MEDs removed) · Dominion-only counties",
         "An association; EAGLE-I counts all utilities. Every year 5.9–27.4×, each interval above 1 (Q3, Q5)"),
        ("6,108 vs 6,530", "If adopted: storm county-days with complete readings (99 counties) vs all (103)",
         "422 = 114 off the map + 308 failed (96 in 2025)"),
        ("Nov 2014 → 2025", "If adopted: EAGLE-I starts Nov 1, 2014: county-days use 2015–25; the map 2015–24",
         "2025 not averaged: 46% of August and 45% of October readings failed"),
        ("351,738 vs 508,000", "If adopted: Isaias: most customers out at one moment (EAGLE-I, all utilities) vs "
         "customers affected over the event (DOE-417)", "A peak vs a total: both true"),
        ("3,702 · 55,524", "If adopted: DOE-417 incident reports 2014–25, a second size for named events · HURDAT2 "
         "track points since 1851", "Tropical if a track passes within 400 km of Richmond; Isaias 59 km"),
        ("306.7 vs 144.4", "2025 SAIDI with and without major event days; MEDs 53% (162.3)",
         "Dominion vs FPL: compare like with like (Q2)"),
        ("2.68M · 2.8M · 3.6M", "Customers: EIA-861 Virginia 2025, 2,675,735; Dominion Energy Virginia with North "
         "Carolina; Dominion Energy, three states", "EIA's count is the SAIDI base (P17); one SAIDI minute ≈ 2.7M "
         "customer-minutes"),
        ("T1–T12 · D1–D14", "Tests, all pass (T1–T6 reliability, T7–T9 storms, T10–T12 demand); decisions logged. "
         "If adopted: T13–T31 (31 in all), D1–D22, 12 of 12 reconciled", "Reconciliation is a definitions check (Q13)"),
        ("99.8%", "Smart meters as a share of all meters, 2025 · EIA-861", "A last gasp marks the start (Q6)"),
        ("500 · 2 min · 5 yr · −32% · −44%", "Mainfeeder selection rule. Reported: −32% outage minutes, feeders "
         "hardened 12+ months (Nov 2023); −44% average annual outage time, hardened areas (June 2026)",
         "Two measures, not a trend; −44% has no stated baseline. Before/after overstates it (Q8)"),
        ("+41% · +27% · +26% · +52%", "Load 2019 → 2025: hours ending 4 a.m. and 4 p.m., top hour, lowest hour · "
         "EIA-930", "Not attributable to data centers (Q10)"),
        ("1.849 → 1.887", "Co-op SAIFI 2025 before and after matching denominators (P18)",
         "A co-op filed SAIDI but no SAIFI (Q17)"),
        ("20M+ · 71% → 90% · 17% · +9%", "Mercury: rows; grounded-answer accuracy; settlement time; renewals",
         "Causal only for the A/B test (Q17)"),
        ("$690M · 440", "The Life Initiative: investments in the board's Tableau view", "Who used it? [you: …]"),
        ("25% · 3-2", "Travel up to 25%; three office days, two remote · the posting", "[you: your answers]"),
    ]   # the SCC's 50 basis points and the merger calendar are in the company box (page 2)
    rows = "".join(f"<tr><td>{htmllib.escape(a)}</td><td>{ph(htmllib.escape(b))}</td><td>{ph(htmllib.escape(c))}</td>"
                   f"</tr>" for a, b, c in K)
    rows = rows.replace("If adopted: ", UP + " ").replace("If adopted", UP)   # the tag is the label: no colon after it
    P.append(page(f"""
<p class="section-no">Appendix A1</p>
<h1>Know every number</h1>
<table class="knum">
<tr><th style="width:1.75in">Number</th><th>Plain meaning · how computed · source</th><th style="width:2.55in">Caveat →
likely follow-up</th></tr>
{rows}
</table>
""", "appendix apx-page"))

    # ------------------------------------------------------------------ 10-11 A2-A3 the 25 hardest
    P.append(page(f"""
<p class="section-no">Appendix A2–A3</p>
<h1>The 25 hardest questions, by panelist</h1>
<p class="h25key"><b>C</b> claim, <b>P</b> proof, <b>L</b> honest limit; ● drill first; <i>Adopted</i> / <i>Public-only</i>
the variant's line; <span class="placeholder">[you: …]</span> only you can fill it; D, P and T are the repo's decisions,
data-quality notes and tests. Q numbers match A1.</p>
<div class="h25">{h25}</div>
""", "appendix apx-page"))

    # ------------------------------------------------------------------ 12 A4 delivery and rehearsal
    P.append(page(f"""
<p class="section-no">Appendix A4</p>
<h1>Delivery and rehearsal</h1>
<div class="say3">
<p><b>30-second opener</b> (sheet 2, “Tell me about yourself”): “{OPENER}” {ph("[you: one line on why this role]")}</p>
<p><b>60-second project story:</b> “{STORY}”</p>
<p><b>5-minute route</b> (cut words, not slides): {ROUTE}</p>
</div>
<p class="h25key">Strength: <b>strong</b> = meta-analysis or large review; <b>single</b> = one study; <b>mixed</b> =
replications disagree; <b>practice</b> = common advice with no study verified (kept and labeled, never cited).</p>
<table class="dl">
<tr><th>Tip</th><th>Rests on</th><th>Strength</th><th>Do this</th></tr>
<tr><td><b>The first minutes count</b></td><td>Barrick, Swider &amp; Stewart 2010</td><td>single</td><td>Open with the
30-second opener; early impressions tracked final ratings (r = .42).</td></tr>
<tr><td><b>Sell with facts; never stretch</b></td><td>Swider et al. 2011; Barrick et al. 2009</td><td>single +
strong</td><td>Real results helped (r = .20); “image creation” hurt (r = −.11 to −.19). Use the resume's numbers
exactly.</td></tr>
<tr><td><b>Expect past-behavior questions</b></td><td>Sackett et al. 2022; Taylor &amp; Small 2002</td><td>strong</td>
<td>Have 5–6 true STAR stories: situation, task, action, result, with the action yours.</td></tr>
<tr><td><b>State the limit, then answer it</b></td><td>O'Keefe 1999</td><td>strong</td><td>A limit builds credibility
only with its answer: “ten points is thin, so the headline uses county-days”.</td></tr>
<tr><td><b>Ask a follow-up question</b></td><td>Huang et al. 2017</td><td>single (conversations, not
interviews)</td><td>At “Any questions?”, first follow up on something a panelist said.</td></tr>
<tr><td><b>Rehearse aloud</b></td><td>Powell, Stanley &amp; Brown 2018</td><td>strong</td><td>Anxiety and scores
correlate at r = −.19. Rehearse to a mock panel.</td></tr>
<tr><td><b>Call the nerves “excitement”</b></td><td>Brooks 2014; Bosshard &amp; Gomez 2024; Ganley et al. 2021</td>
<td>mixed, small</td><td>Say “I'm excited”, not “calm down”: a small pooled effect (d ≈ 0.2); a math replication
found nothing.</td></tr>
<tr><td><b>Answer first</b> · <b>“I don't know” → how I'd find out</b> · <b>Pace, close, thank</b></td><td>none
verified</td><td>practice</td><td>Claim, one proof, then the limit. Never guess a number; say where you'd look.
Pause after each answer; send a thank-you note within a day.</td></tr>
</table>
<h2>Three interviewers</h2>
<p>The panel research is mixed (Dixon et al. 2002), so these are inference: make each answer complete on its own,
answer the asker, then turn to the others; take a challenge with thanks, concede what's right, then answer.</p>
<table class="dl">
<tr><th>Panelist</th><th>Listens for</th><th>Lead with</th><th>Questions</th></tr>
<tr><td><b>BI manager</b></td><td>How it's built; checked numbers; Power BI</td><td>The model, the measures, the
reconciliation</td><td>Q11–Q18</td></tr>
<tr><td><b>Engineer</b></td><td>Exact definitions; honest limits</td><td>Precise terms, a fast concession, the data
that would settle it</td><td>Q1–Q10</td></tr>
<tr><td><b>HR</b></td><td>Plain words, fit, how you take pushback</td><td>No acronyms (Q24), true STAR stories, calm
on the merger</td><td>Q19–Q25</td></tr>
</table>
<h2>Rehearsal outline for Monday</h2>
<ol class="tight">
<li>Decide the variant first (adopted or public-only); everything after depends on it.</li>
<li>Adopted: apply the Power BI guide. Public-only: skip the template and print nothing from Power BI. Either way,
know your report's model for Q11.</li>
<li>Read this brief once, for understanding; mark anything you couldn't explain.</li>
<li>Say the deck aloud against an 8-minute timer, three times; record one run. Then the 5-minute route once.</li>
<li>Drill the sheet and the 25 hardest by recall: cover, say it aloud, check (Roediger &amp; Karpicke 2006; Rowland
2014: strong). Spread it: an afternoon round, then an evening round of the misses (Cepeda et al. 2006: strong).</li>
<li>Stop at 20:00 and sleep (Lim &amp; Dinges 2010: strong). Tuesday: say the 30-second opener twice and leave
early.</li>
</ol>
""", "appendix apx-page"))

    out = ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
           "<meta name='viewport' content='width=device-width, initial-scale=1'>"
           "<title>Dominion interview brief</title>"
           f"<style>{css}</style></head><body>{''.join(P)}</body></html>")
    return out


UK = re.compile(r"\b(programme|behaviour|colour|centre|analyse|prioritis|licence|normalis|organis|labelled|"
                r"modelled|favour|summaris|minimis|recognis|authoris|optimis)", re.I)
BANNED = re.compile(r"\b(AI assistant|Claude|agent [BDR]\b|Agent [BDR]\b|orchestrator|ledger|claims\.csv|the brief "
                    r"requires|interview-prep)", re.I)


def checks(html: str):
    text = re.sub(r"<style>.*?</style>", "", html, flags=re.S)
    text = re.sub(r"data:image/png;base64,[A-Za-z0-9+/=]+", "", text)
    text = re.sub(r"<svg.*?</svg>", "", text, flags=re.S)
    plain = re.sub(r"<[^>]+>", " ", text)
    bad = UK.findall(plain)
    assert not bad, f"UK spellings (O-30): {bad}"
    bad = BANNED.findall(plain)
    assert not bad, f"banned words: {bad}"
    assert not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", plain), "email address"
    assert not re.search(r"\(?\d{3}\)?[ .-]\d{3}[ .-]\d{4}", plain), "phone number"
    assert not re.search(r"[A-Z]:\\|/Users/|\\Users\\", plain), "machine path"
    assert not re.search(r"\[(?:C|N|R)-[A-Z0-9-]+", plain), "claim-id tag left in print"
    dm = re.findall(r"\b\d{1,2}\s(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|"
                    r"Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\b(?!\.?\s+\d{1,2},\s+\d{4})", plain)
    assert not dm, f"day-month dates (O-30 wants month-day): {dm}"
    # final (correction 1 to C.3): no "AI" or "assistant" anywhere in the printed brief; no "star schema" (C.1); no
    # commit count, bundle or hash (the branch changes)
    for pat, why_ in ((r"\bAI\b", "AI"), (r"assistant", "assistant"), (r"star schema", "star schema"),
                      (r"\b\d+ commits\b", "commit count"), (r"bundle", "bundle"), (r"\bSHA\b|SHA-?\d", "SHA")):
        hits = re.findall(pat, plain, flags=re.I if why_ != "AI" else 0)
        assert not hits, f"{why_} printed in the brief: {hits}"
    for must in ("30-second opener", "60-second project story", "5-minute route", "The core is a small star",
                 htmllib.escape(Q18_RULE, quote=False), "Use the authorship sentence in START_HERE",
                 # final batch: every fix must have applied
                 "completion expected by end-2027", "typical residential bill +$11.24", "19 sites planned.",
                 "(19 sites planned)", "Expected by 2029.", "28% of Dominion Energy Virginia's 2025 sales",
                 "Virginia's order is due by January 11, 2027",
                 "On Oct 19 the SCC staff recommended denying the merger as proposed unless the companies accept "
                 "conditions", "Appalachian Power is its own group, not a peer"):
        assert must in " ".join(plain.split()), f"missing from the brief: {must!r}"
    assert " ".join(plain.split()).count(" ".join(htmllib.escape(RUNNER, quote=False).split())) == 2, \
        "the runner sentence must print twice (p. 7 and Q15)"
    for gone in ("Virginia Power", "mid-January", "done by end-2027", "Due 2029", "is apart"):
        assert gone not in plain, f"still printed: {gone!r}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    html_text = build_html()
    checks(html_text)
    html = OUT / f"{STEM}.html"
    html.write_text(html_text, encoding="utf-8")
    pdf = pipeline.html_to_pdf(html, OUT / f"{STEM}.pdf")
    import pymupdf
    doc = pymupdf.open(str(pdf))
    n = len(doc)
    doc.set_metadata({"title": "Dominion interview brief", "author": "Saketh Bollina", "subject": "", "keywords": "",
                      "creator": "", "producer": ""})
    tmp = pdf.with_suffix(".tmp.pdf")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf)
    print(f"pages: {n}")
    doc = pymupdf.open(str(pdf))
    for k, pg in enumerate(doc, start=1):
        first = [ln for ln in pg.get_text().splitlines() if ln.strip()][:2]
        print(f"  p{k}: {' | '.join(first)[:90]}")
    doc.close()
    for old in PROOFS.glob(f"{STEM}_p*.png"):
        old.unlink()
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=90, grey=grey)
    mins = pipeline.pdf_min_font_size(pdf)
    print("min sizes:", mins)
    print("fonts:", pipeline.pdf_fonts(pdf))
    assert n <= 12, f"O-29: the brief is {n} pages (12 at most)"
    doc = pymupdf.open(str(pdf))           # print-proof: every word at least 0.30 in from every page edge
    edges = []
    for pg in doc:
        W, H = pg.rect.width, pg.rect.height
        edges += [min(w[0], w[1], W - w[2], H - w[3]) for w in pg.get_text("words")]
    doc.close()
    print(f"min distance from a page edge: {min(edges):.2f} pt ({min(edges) / 72:.3f} in)")
    assert min(edges) >= EDGE_MIN_PT, f"text closer than 0.30 in to a page edge: {min(edges):.2f} pt"


if __name__ == "__main__":
    main()
