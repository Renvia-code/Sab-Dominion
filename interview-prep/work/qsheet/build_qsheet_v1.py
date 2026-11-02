"""Question sheet v1 (P2): one US Letter sheet, two sides, two columns.

Content: R's 24 starred picks from research/top40.md (G1b locked 08:50; R's frequency x fit rule, not
taste), R's five questions to ask, and a closing line. Experience comes only from the resume (Mercury,
The Life Initiative, Cofoods, CCL, Boston University); anything the resume lacks is [you: ...]. Numbers
are in interview-prep/claims.csv (C-Q-* rows plus the deck rows they reuse). No salary figure.

Body 9.0 pt if the sheet is exactly two pages, else 8.5 pt (DESIGN_SYSTEM.md section 6).

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\qsheet\\build_qsheet_v1.py
Out:  interview-prep/deliverables/02_question_sheet/Dominion_question_sheet_v1.{html,pdf}
      interview-prep/work/proofs/qsheet_v1/ (PNG proofs, colour and greyscale)
"""
from __future__ import annotations

import html as htmllib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402
import pipeline  # noqa: E402

OUT = ds.REPO / "interview-prep" / "deliverables" / "02_question_sheet"
PROOFS = ds.WORK / "proofs" / "qsheet_v1"
STEM = "Dominion_question_sheet_v1"

# kind: "cue" = bold claim + body; "star" = four STAR lines; "fill" = a fill-in answer
GROUPS = [
    ("Opening", [
        dict(id="O1", q="Tell me about yourself.", kind="cue",
             claim="Business intelligence analyst: three years building dashboards, reporting and data pipelines.",
             body="Today I'm a Data Analyst at Mercury Insurance: I built a Snowflake pipeline across policy, claims "
                  "and billing (20M+ rows) and owned validation and reconciliation for an AI pilot. Before that: "
                  "Tableau board reporting at The Life Initiative, forecasting and dashboards at Cofoods, and an MS "
                  "in Business Analytics at Boston University."),
        dict(id="O2", q="Why do you want to work at Dominion Energy?", kind="cue",
             claim="Reliability reporting here matters, and I've already started on it.",
             body="The SCC can move Dominion's allowed return by up to 50 basis points on factors that include "
                  "reliability, so the numbers have to be right. I rebuilt your 3-year SAIDI from EIA-861 (130.2 and "
                  "133.0 against the reported 130 and 133) and want to do that work with your data. "
                  "[you: one personal reason]"),
        dict(id="O9", q="Why this role?", kind="cue",
             claim="It is the work I do: governed reporting, pointed at grid programmes.",
             body="The posting asks for Power BI, SQL, Excel and Snowflake, plus business definitions, metadata, "
                  "validation and reconciliation. At Mercury I built the Snowflake pipeline, owned validation and "
                  "reconciliation for a pilot, and documented metadata and business definitions so other teams "
                  "could reuse the method. Grid Resiliency programmes are selected and measured on outage history."),
    ]),
    ("Behavioural (STAR)", [
        dict(id="B8", q="How do you manage multiple priorities and deadlines? Give an example.", kind="star",
             star=["At Mercury this year: a root-cause analysis, a pilot's evaluation and an A/B test.",
                   "Deliver each to its deadline without cutting the checks. [you: the deadlines]",
                   "[you: how you ordered the work]; agreed sample size and significance thresholds with the "
                   "analytics manager.",
                   "Helped cut average settlement time by 17% over two months; grounded-answer accuracy 71% → 90%; "
                   "on-time renewals +9%."]),
        dict(id="B6", q="Tell me about your most complex or challenging data project.", kind="star",
             star=["Mercury's AI pilot needed a way to tell whether its answers were accurate and correctly cited.",
                   "I owned the evaluation methodology.",
                   "Scored answer accuracy and citation correctness against a 150-question test set; iterated on "
                   "chunking and prompt structure.",
                   "Grounded-answer accuracy rose from 71% to 90%; the framework is documented for reuse."]),
        dict(id="B2", q="Tell me about a disagreement with a colleague or team, and how you resolved it.",
             kind="star",
             star=["[you: a real disagreement, ideally about a number or a definition]",
                   "[you: what you were responsible for]",
                   "Cue: take it to the data and the definition; agree the test first, then let the result decide. "
                   "[you: what you did]",
                   "[you: the outcome, and what you would do again]"]),
        dict(id="B4", q="Tell me about a time something went wrong at work, or you made a mistake.", kind="star",
             star=["[you: a number you produced that was wrong, or nearly went out wrong]",
                   "Correct it before anyone relied on it, and say so early.",
                   "[you: the check that caught it, and the fix]. Project option, only if you own it: summed ratio "
                   "columns → customer-weighted measures.",
                   "[you: the outcome, and the control you have used since]"]),
        dict(id="B1", q="Tell me about a problem you solved, in a team or on your own.", kind="star",
             star=["Mercury had recurring claims-cycle delays.",
                   "Find what was driving them.",
                   "Joined claims, policy and vendor data; surfaced the appraisal bottlenecks behind the delays. "
                   "[you: who you worked with]",
                   "Helped cut average settlement time by 17% over two months."]),
    ]),
    ("Technical BI", [
        dict(id="T1", q="Walk me through a dashboard or report you built.", kind="cue",
             claim="Two: Tableau at work, Power BI on Dominion's public data.",
             body="At The Life Initiative I turned a flat website table into the board's standing executive "
                  "reporting view in Tableau: $690M across 440 investments, with demographic and socioeconomic "
                  "filters. In Power BI, this review: SAIDI, SAIFI and CAIDI measures on a Snowflake-built mart, "
                  "peer, weather and demand pages, KPI cards set by a year slicer. [you: who used each]"),
        dict(id="T4", q="What is a star schema (vs a snowflake schema)? Fact vs dimension tables?", kind="cue",
             claim="Facts hold measurements at one grain; dimensions describe them.",
             body="Here the fact is one row per utility, state and year, with customers, customer-minutes and "
                  "interruptions; dimensions hold descriptions such as utility name and peer group. A star joins each "
                  "dimension directly to the fact, many-to-one; a snowflake normalises dimensions into more tables. "
                  "Power BI works best with a star: FCT_RELIABILITY → DIM_UTILITY in the review."),
        dict(id="T36", q="How strong is your SQL? Walk me through a query you wrote.", kind="cue",
             claim="Strong: CTEs, window functions and multi-table joins in a working pipeline.",
             body="At Mercury I wrote the SQL for a Snowflake warehouse pipeline across policy, claims and billing "
                  "schemas, 20M+ rows, that kept a pilot's data current. In the review, SAIDI is total "
                  "customer-minutes ÷ total customers, never an average of ratios, and ROW_NUMBER ranks the 50 "
                  "highest demand hours. [you: one query you can sketch]"),
        dict(id="T3", q="What does CALCULATE do? Explain filter context.", kind="cue",
             claim="CALCULATE evaluates an expression under modified filters.",
             body="Filter context is every filter reaching a value: slicers, rows and columns, page and visual "
                  "filters. CALCULATE adds, overrides or removes filters, and turns row context into filter context. "
                  "In the review the KPI cards use CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = "
                  "SELECTEDVALUE('Dashboard Year'[Year], 2025)) on a disconnected year table: the slicer sets the "
                  "cards' year without filtering the page."),
        dict(id="T7", q="How do refreshes work in the Power BI Service, and how do you keep a report fast?",
             kind="cue",
             claim="A lean star-schema model first, then a refresh that runs on its own.",
             body="Performance: star schema, Import where the data allows, measures instead of summed columns, "
                  "Performance Analyzer to find the slow visual. Refresh: scheduled refresh in the Service, "
                  "incremental refresh for large tables, a gateway for on-premises sources. In the review, six "
                  "DirectQuery tables pointed at an old Snowflake trial and could not render offline; the fix: "
                  "Import from local CSVs through a DataFolder parameter (DirectQuery while building, Import to "
                  "present). [you: any Service use; don't stretch]"),
        dict(id="T17", q="What is a Snowflake virtual warehouse, and how do you control compute cost?", kind="cue",
             claim="Compute you size and pay for while it runs, separate from storage.",
             body="Size it to the job, set auto-suspend and auto-resume, keep loading and reporting on separate "
                  "warehouses, and cap credits with resource monitors. At Mercury I built a Snowflake warehouse "
                  "pipeline (20M+ rows); in the review, RAW, STG and MART layers. [you: cost controls you have "
                  "used]"),
    ]),
    ("Utility domain", [
        dict(id="U1", q="What are SAIDI, SAIFI and CAIDI, and how are they related?", kind="cue",
             claim="SAIDI = SAIFI × CAIDI: how often, times how long.",
             body="SAIFI = customer interruptions ÷ customers served. SAIDI = customer-minutes of interruption ÷ "
                  "customers served. CAIDI = SAIDI ÷ SAIFI, minutes per interruption. Dominion 2025, excluding major "
                  "events: 1.320 × 109.4 = 144.4 minutes. Sum minutes and customers before dividing."),
        dict(id="U2", q="What is a major event day, and why exclude it?", kind="cue",
             claim="A day extreme enough to swamp the trend, set aside by rule.",
             body="IEEE 1366's 2.5-beta method: from five years of daily SAIDI, a day is a major event day when its "
                  "SAIDI exceeds exp(α + 2.5β), α and β being the mean and standard deviation of ln(daily SAIDI). "
                  "Excluding them shows day-to-day performance. What it hides: in 2025 they were 53% of Dominion's "
                  "all-event minutes (162.3 of 306.7). Dominion reports under its own rule."),
        dict(id="U3", q="SAIFI is rising. How would you investigate it?", kind="cue",
             claim="Rule out measurement first, then follow interruptions to causes.",
             body="Check definitions, the major-event rule and whether detection changed (smart meters). Then "
                  "split by cause code, feeder and device, weather exposure and repeat customers (CEMI). From 2022 "
                  "to 2025, SAIFI rose 10% while CAIDI fell 4%, and storm county-days rose from 718 to 791: "
                  "consistent with Dominion's “primarily due to increased storm activity”. Confirming a cause needs "
                  "outage records."),
    ]),
    ("Role and Dominion", [
        dict(id="R4", q="Are you willing to travel or work outside normal hours (for example, storms)?",
             kind="fill",
             body="The posting lists travel up to 25%. [you: travel and storm-season hours you can commit to]"),
        dict(id="R2", q="How do you feel about joining while the NextEra merger is pending?", kind="cue",
             claim="Calm and factual: this team's work continues either way.",
             body="Announced May 2026, approved by shareholders in September; the Virginia SCC's final order is due "
                  "by mid-January 2027, and South Carolina, North Carolina, FERC and the NRC must also approve; "
                  "closing is expected in the second half of 2027. The company says Dominion Energy Virginia stays "
                  "separately regulated and accountable to the SCC. Integration makes reconciled, documented numbers "
                  "more valuable. No predictions, no politics."),
    ]),
    ("Logistics: fill in before Tuesday", [
        dict(id="R5", q="Are you comfortable with a hybrid schedule in Richmond?", kind="fill",
             body="The posting says three days in the office, two remote. [you: your answer]"),
        dict(id="R7", q="Will you now or in the future require sponsorship for employment authorization?",
             kind="fill",
             body="The posting says Dominion cannot sponsor or transfer a work visa for this position. "
                  "[you: your answer; know it before the panel]"),
        dict(id="R6", q="What are your salary expectations?", kind="fill",
             body="Approach: ask about the full scope and total compensation first; if pressed, give a researched "
                  "range for this role and level in Richmond. [you: your range]"),
        dict(id="R10", q="When could you start?", kind="fill", body="[you: notice period and earliest start date]"),
    ]),
    ("Closing", [
        dict(id="C1", q="Is there anything else you'd like us to know?", kind="cue",
             claim="Three lines: fit, proof, interest.",
             body="I build governed Snowflake → Power BI reporting. I've already rebuilt your reliability numbers "
                  "from public data: 130.2 and 133.0 against the reported 130 and 133. And I'd like to do this work "
                  "on Grid Resiliency programmes, with your data."),
    ]),
]

ASK = [  # R's five picks (A1, A2, A3, A6, A8), in R's order; A8 always last
    "What would success look like in this role after six to twelve months?",
    "Which reliability and programme metrics does the team report most often, and where do analysts spend most "
    "of their time today?",
    "How does the team evaluate programmes like mainfeeder hardening today, and what would you like to measure "
    "better?",
    "How do analysts here work with engineering and field teams day to day?",
    "What are the next steps in the process?",
]
CLOSE = ("Thank you for your time. I'd like to bring the same discipline to your reliability reporting: reconcile "
         "first, test every number, and make it easy to act on.")


def esc(s: str) -> str:
    """Escape, then mark every [you: ...] placeholder."""
    s = htmllib.escape(s, quote=False)
    return re.sub(r"\[you:[^\]]*\]", lambda m: f"<span class='ph'>{m.group(0)}</span>", s)


def build_html(body_pt: float) -> str:
    lead = round(body_pt * 1.247, 1)
    css = (HERE / "qsheet.css").read_text(encoding="utf-8")
    css = css.replace("--body: 8.5pt", f"--body: {body_pt}pt").replace("--lead: 10.6pt", f"--lead: {lead}pt")
    n_q = sum(len(items) for _, items in GROUPS)
    assert n_q == 24, n_q
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
             f"<title>Dominion question sheet</title><style>{css}</style></head><body>",
             "<header class='sheet'><h1>Interview questions and answer cues</h1>"
             "<span class='meta'>Dominion Energy · panel interview · Tuesday 3 November 2026</span></header>",
             "<p class='legend'>Each answer: claim → proof from your resume → tie to Dominion. STAR = situation, "
             "task, action, result. <span class='ph'>[you: …]</span> = only you can fill this in; do it before "
             "Tuesday.</p><div class='cols'>"]
    k = 0
    for name, items in GROUPS:
        parts.append(f"<h2>{esc(name)}</h2>")
        for it in items:
            k += 1
            parts.append(f"<div class='qa'><div class='q'><span class='n'>{k}</span>{esc(it['q'])}</div>")
            if it["kind"] == "star":
                parts.append("<ul class='star'>" + "".join(
                    f"<li><b>{letter}</b>{esc(line)}</li>" for letter, line in zip("STAR", it["star"])) + "</ul>")
            elif it["kind"] == "cue":
                parts.append(f"<p class='a'><b>{esc(it['claim'])}</b> {esc(it['body'])}</p>")
            else:
                parts.append(f"<p class='a'>{esc(it['body'])}</p>")
            parts.append("</div>")
    parts.append("<div class='ask'><b>Five questions to ask the panel</b> (ask two or three; the last one always "
                 "last)<ol>" + "".join(f"<li>{esc(a)}</li>" for a in ASK) + "</ol></div>")
    parts.append(f"<p class='close'>Closing line: {esc(CLOSE)}</p>")
    parts.append("</div></body></html>")
    return "".join(parts)


def words(it) -> int:
    txt = " ".join([it.get("claim", ""), it.get("body", "")] + it.get("star", []))
    return len(txt.split())


def main():
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    for name, items in GROUPS:
        print(name, [(it["id"], words(it)) for it in items])
    chosen = None
    for pt in (9.0, 8.5):
        html = OUT / f"{STEM}.html"
        html.write_text(build_html(pt), encoding="utf-8")
        pdf = pipeline.html_to_pdf(html, OUT / f"{STEM}.pdf")
        n = len(pymupdf.open(str(pdf)))
        print(f"{pt} pt -> {n} pages")
        if n == 2:
            chosen = pt
            break
    if chosen is None:
        raise SystemExit("does not fit on two sides even at 8.5 pt: trim answers (never drop a brief-required item)")
    print(f"body {chosen} pt; min sizes {pipeline.pdf_min_font_size(OUT / f'{STEM}.pdf')}")
    print("fonts:", pipeline.pdf_fonts(OUT / f"{STEM}.pdf"))
    for grey in (False, True):
        pipeline.pdf_to_pngs(OUT / f"{STEM}.pdf", PROOFS, dpi=110, grey=grey)


if __name__ == "__main__":
    main()
