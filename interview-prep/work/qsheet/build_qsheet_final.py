"""Question sheet, final (rulings O-34 to O-39, after V6): sheet v3 with these changes, every new fact from
work/v6_inputs/D_facts.md (D) or work/v6_inputs/R_company_glossary.md (R), or already sourced:
  item 1  SCC expanded (V6 glossary table);
  item 7  the P18 story from D (m) (Prince George Electric, 13,341 customers);
  item 9  who used it: "[you: who used the Tableau view]; the Power BI report: nobody yet; I built it for this
          application" (V6 §2c);
  item 10 the question reworded so nothing prints "star schema" (reported to the orchestrator), and the model line
          MODEL_LINE_SHEET (C.1, variant-neutral: "most stand alone");
  item 11 D (l)'s query in place of "[you: one query you can sketch]";
  item 13 "a star-shaped model"; item 16 CEMIn (R note 3);
  item 18 R §6 (storm duty: ask the recruiter); item 19 R §3 "What do you know about Dominion?" replaces R2, the
          merger, the least likely of the 24 (O-38); item 22 R §5 (how to research a range; no figure).
Final files drop the version suffix (O-39).

v3 notes follow.

Question sheet v3 (P2), the final candidate: sheet v2 plus the print-proof margins (every text item at least
0.30 in from every page edge: the "Side N of 2" footer moves up inside a taller bottom margin, and the top margin
gives back the same 0.05 in, so the content area is unchanged) and C-Q-10's verified date (both companies'
shareholders approved the merger on September 3, 2026; SEC 8-K Item 5.07). One US Letter sheet, two sides, two
columns. One variant-neutral version (G2, O-28).

v2 notes follow.

The 24 questions are R's star list in research/top40.md (09:41), in R's order and wording within each group
(orchestrator ruling 2; asserted against the file at build time). Membership is unchanged (G1b). U2 carries R's
H02 fix (Dominion reports under "Other"). With the V2 rulings applied:
  F7 Q13 D13 only, no discovery story; F8 Q7 the candidate's own catch P18 (commit 1635a8e); F10 Q24 resume-true;
  F12 Q11 the 3-year figure is the mean of the annual values; F18 Q1/Q3 the evaluation methodology wording;
  F19 Q3 "here pointed at grid programs"; F20 Q4 [you: the deadlines]; F21 "grounded-answer accuracy";
  F22 Q12 the VAR form of Selected SAIDI; F23 "public filings"; logistics line on Q20;
  U3 storm county-days "rose about 10%" (true in both variants: 718 -> 791 and 723 -> 796).
O-30: US English and US dates. Experience only from the resume; anything it lacks is [you: ...]. No salary figure.

Body 9.0 pt on exactly two pages; the build fails rather than go below 9 pt (O-29).

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\qsheet\\build_qsheet_final.py
Out:  interview-prep/deliverables/02_question_sheet/Dominion_question_sheet.{html,pdf}
      interview-prep/work/proofs/qsheet_final/
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
from final_text import MODEL_LINE_SHEET  # noqa: E402

OUT = ds.REPO / "interview-prep" / "deliverables" / "02_question_sheet"
PROOFS = ds.WORK / "proofs" / "qsheet_final"
STEM = "Dominion_question_sheet"
# Two deliberate departures from R's star list (top40.md), both reported to the orchestrator:
REWORDED = {"T4": "What are star and snowflake schemas? Fact vs dimension tables?"}   # nothing prints "star schema"
REPLACED = {"R2": ("RK", "What do you know about Dominion?")}    # O-38: in place of the least likely question
EDGE_MIN_PT = 21.6     # 0.30 in from every page edge (print-proof addendum)
# v3 print margins: top 0.42 -> 0.37 in, bottom 0.45 -> 0.50 in (content height unchanged); the footer sits at the top
# of the bottom margin box instead of its middle, so it clears the bottom edge by more than 0.30 in
MARGIN_V2 = "margin: 0.42in 0.5in 0.45in 0.5in;"
MARGIN_V3 = "margin: 0.37in 0.5in 0.5in 0.5in;"
FOOTER_V2 = "color: #6B7280; }\n}"
FOOTER_V3 = "color: #6B7280; vertical-align: top; padding-top: 0; }\n}"

# kind: "cue" = bold claim + body; "star" = four STAR lines; "fill" = a fill-in answer
GROUPS = [
    ("Opening", [
        dict(id="O2", q="Why do you want to work at Dominion Energy?", kind="cue",
             claim="Reliability reporting here matters, and I've already started on it.",
             body="The Virginia State Corporation Commission (SCC) can move Dominion's allowed return by up to 50 "
                  "basis points on factors that include reliability, so the numbers have to be right. I rebuilt your reported 3-year SAIDI from your "
                  "public reliability filings (130.2 and 133.0 against the reported 130 and 133) and want to do that "
                  "work with your data. [you: one personal reason]"),
        dict(id="O1", q="Tell me about yourself.", kind="cue",
             claim="Business intelligence analyst: three years building dashboards, reporting and data pipelines.",
             body="Today I'm a Data Analyst at Mercury Insurance: I built a Snowflake pipeline across policy, claims "
                  "and billing (20M+ rows) and owned the evaluation methodology for an AI pilot: validation, "
                  "reconciliation and QA of its answers. Before that: Tableau board reporting at The Life "
                  "Initiative, forecasting and dashboards at Cofoods, and an MS in Business Analytics at Boston "
                  "University."),
        dict(id="O9", q="Why this role? / Why did you apply for this position?", kind="cue",
             claim="It is the work I do: governed reporting, here pointed at grid programs.",
             body="The posting asks for Power BI, SQL, Excel and Snowflake, plus business definitions, metadata, "
                  "validation and reconciliation. At Mercury I built the Snowflake pipeline, owned the evaluation "
                  "methodology for an AI pilot, and documented metadata and business definitions so other teams "
                  "could reuse the method. Grid Resiliency programs are selected and measured on outage history."),
    ]),
    ("Behavioral (STAR)", [
        dict(id="B8", q="How do you manage multiple priorities and deadlines? Give an example.", kind="star",
             star=["At Mercury this year: a root-cause analysis, a pilot's evaluation and an A/B test.",
                   "Deliver each to its deadline without cutting the checks. [you: the deadlines, and that they "
                   "overlapped]",
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
        dict(id="B2", q="Tell me about a disagreement or conflict with a colleague or team, and how you resolved it.",
             kind="star",
             star=["[you: a real disagreement, ideally about a number or a definition]",
                   "[you: what you were responsible for]",
                   "Cue: take it to the data and the definition; agree the test first, then let the result decide. "
                   "[you: what you did]",
                   "[you: the outcome, and what you would do again]"]),
        dict(id="B4", q="Tell me about a time something went wrong at work, or you made a mistake.", kind="star",
             star=["[you: a number you produced that was wrong, or nearly went out wrong]",
                   "Correct it before anyone relied on it, and say so early.",
                   "[you: the check that caught it, and the fix]. Project option (yours, P18, Oct 27): Prince George "
                   "Electric filed SAIDI but no SAIFI for 2025, so its 13,341 customers would have sat in the co-op "
                   "SAIFI's denominator; I matched the denominators (1.849 → 1.887).",
                   "[you: the outcome, and the control you have used since]"]),
        dict(id="B1", q="Tell me about a problem you solved, in a team or on your own.", kind="star",
             star=["Mercury had recurring claims-cycle delays.",
                   "Find what was driving them.",
                   "Joined claims, policy and vendor data; surfaced the appraisal bottlenecks behind the delays. "
                   "[you: who you worked with]",
                   "Helped cut average settlement time by 17% over two months."]),
    ]),
    ("Technical BI", [
        dict(id="T1", q="Walk me through a dashboard or report you built: who used it, which KPIs, how you designed "
                        "it.", kind="cue",
             claim="Two: Tableau at work, Power BI on Dominion's public data.",
             body="At The Life Initiative I turned a flat website table into the board's standing executive "
                  "reporting view in Tableau: $690M across 440 investments, with demographic and socioeconomic "
                  "filters. In Power BI, this review: SAIDI, SAIFI and CAIDI measures on a Snowflake-built mart, "
                  "peer, weather and demand pages, KPI cards set by a year slicer. [you: who used the Tableau view]; "
                  "the Power BI report: nobody yet; I built it for this application."),
        dict(id="T4", q=REWORDED["T4"], kind="cue",
             claim="Facts hold measurements at one grain; dimensions describe them.",
             body="A star joins each dimension directly to the fact, many-to-one; a snowflake normalizes dimensions "
                  "into more tables. Power BI works best with a star. In the review: " + MODEL_LINE_SHEET),
        dict(id="T36", q="How strong is your SQL? Walk me through a query you wrote.", kind="cue",
             claim="Strong: CTEs, window functions and multi-table joins in a working pipeline.",
             body="At Mercury I wrote the SQL for a Snowflake warehouse pipeline across policy, claims and billing "
                  "schemas, 20M+ rows, that kept a pilot's data current. In the review, within a year SAIDI = "
                  "customer-minutes ÷ customers; the 3-year figure is the mean of the three annual values, as the "
                  "reported 130 and 133 are: AVG(saidi_ex_med) OVER (ORDER BY year ROWS BETWEEN 2 PRECEDING AND "
                  "CURRENT ROW) on FCT_RELIABILITY for 19876|VA returns 130.2 for 2024 and 133.0 for 2025. "
                  "ROW_NUMBER ranks the 50 highest demand hours."),   # D (l), checked on fct_reliability.csv
        dict(id="T3", q="What does CALCULATE do? Explain filter context.", kind="cue",
             claim="CALCULATE evaluates an expression under modified filters.",
             body="Filter context is every filter reaching a value: slicers, rows and columns, page and visual "
                  "filters. CALCULATE adds, overrides or removes filters, and turns row context into filter context. "
                  "In the review the KPI cards use Selected SAIDI = VAR SelectedYear = SELECTEDVALUE('Dashboard "
                  "Year'[Year], 2025) RETURN CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = SelectedYear), on a "
                  "disconnected year table: the slicer sets the cards' year without filtering the page."),
        dict(id="T7", q="How do refreshes work in the Power BI Service (gateways, scheduled and incremental refresh)?",
             kind="cue",
             claim="A scheduled refresh in the Service, a gateway for on-premises sources, and incremental refresh "
                   "for large tables.",
             body="Incremental refresh reloads only recent date partitions. Performance: a star-shaped "   # final batch:
                  "model, "                                         # 13 characters cut so the item 9 wording fits
                  "Import where the data allows, measures instead of summed columns, Performance Analyzer for the "
                  "slow visual. In the review: "
                  "DirectQuery against Snowflake during development, Import for presentation (decision D13). "
                  "[you: mention the CSV / DataFolder route only if you adopted "
                  "the extension and tested the template yourself] [you: any Service use; don't stretch]"),
        dict(id="T17", q="What is a Snowflake virtual warehouse, and how do you control compute cost?", kind="cue",
             claim="Compute you size and pay for while it runs, separate from storage.",
             body="Size it to the job, set auto-suspend and auto-resume, keep loading and reporting on separate "
                  "warehouses, and cap credits with resource monitors. At Mercury I built a Snowflake warehouse "
                  "pipeline (20M+ rows); in the review, RAW, STG and MART layers. [you: cost controls you have "
                  "used]"),
    ]),
    ("Utility domain", [
        dict(id="U1", q="What are SAIDI, SAIFI and CAIDI, and how are they related? (Could you calculate them?)",
             kind="cue",
             claim="SAIDI = SAIFI × CAIDI: how often, times how long.",
             body="SAIFI = customer interruptions ÷ customers served. SAIDI = customer-minutes of interruption ÷ "
                  "customers served. CAIDI = SAIDI ÷ SAIFI, minutes per interruption. Dominion 2025, excluding major "
                  "events: 1.320 × 109.4 = 144.4 minutes. Sum minutes and customers before dividing."),
        dict(id="U3", q="SAIFI is rising. How would you investigate it?", kind="cue",
             claim="Rule out measurement first, then follow interruptions to causes.",
             body="Check definitions, the major-event rule and any detection change (smart meters). Split by cause "
                  "code, feeder and device, weather exposure and repeat customers (CEMIn). From 2022 to 2025 SAIFI "
                  "rose 10%, CAIDI fell 4%, and storm county-days rose about 10%: consistent "
                  "with Dominion's “primarily due to increased storm activity”. Confirming a cause needs outage "
                  "records."),
        dict(id="U2", q="What is a major event day, and why exclude it?", kind="cue",
             claim="A day extreme enough to swamp the trend, set aside by rule.",
             body="IEEE 1366's 2.5β method: from five years of daily SAIDI, a day is a major event day if its "
                  "SAIDI exceeds exp(α + 2.5β), α and β being the mean and standard deviation of ln(daily SAIDI). "
                  "Excluding them shows day-to-day performance. What it hides: in 2025, 53% of Dominion's "
                  "all-event minutes (162.3 of 306.7). Dominion uses its own method (“Other”): peer ranks are "
                  "indicative."),   # R's H02 fix (top40.md, 09:41): Dominion reports under 'Other'
    ]),
    ("Role and Dominion", [
        dict(id="R4", q="Are you willing to travel or work outside normal hours (e.g., storms)?",
             kind="fill",
             body="The posting lists travel up to 25% and says nothing about storm duty, so ask the recruiter what "
                  "storm-season duty means for this role. [you: travel and storm-season hours you can commit "
                  "to]"),    # R §6 (R-009, R-126)
        dict(id="RK", q=REPLACED["R2"][1], kind="cue",       # R §3, in R's words (45 seconds)
             claim="Dominion is a Richmond-based regulated utility, with about 3.6 million electric customers in "
                   "Virginia and the Carolinas, about 2.7 million of them in Virginia.",
             body="Three things stand out. First, demand: data centers are more than a quarter of Dominion Energy "
                  "Virginia's sales, and the pipeline keeps growing. Second, reliability now has money attached. The "
                  "Virginia State Corporation Commission, the SCC, can move Dominion's allowed return up or down by "
                  "as much as half a point, on factors that include reliability. And Dominion's three-year SAIDI "
                  "excluding major events rose from 130 to 133 minutes, mostly from storms, it says. Third, the "
                  "proposed combination with NextEra; SCC hearings start November 17. [you: one sentence on why "
                  "this team, in your own words]"),
    ]),
    ("Logistics: fill in before Tuesday", [
        dict(id="R5", q="Are you comfortable with a hybrid schedule in Richmond (location)?", kind="fill",
             body="The posting says three days in the office, two remote. [you: your answer] [you: commute or "
                  "relocation plan for a hybrid 3-2 schedule in Richmond]"),
        dict(id="R7", q="Will you now or in the future require sponsorship for employment authorization?",
             kind="fill",
             body="The posting says Dominion cannot sponsor or transfer a work visa for this position. "
                  "[you: your answer; know it before the panel]"),
        dict(id="R6", q="What are your salary expectations?", kind="fill",
             body="Research a Richmond range for this role from public pay data (Bureau of Labor Statistics wage "
                  "tables). Let them name the band first (“What range is budgeted for this role?”); if asked to go "
                  "first, give a range. [you: your range]"),  # R §5
        dict(id="R10", q="When could you start?", kind="fill", body="[you: notice period and earliest start date]"),
    ]),
    ("Closing", [
        dict(id="C1", q="Is there anything else you'd like us to know?", kind="cue",
             claim="Three lines: fit, proof, interest.",
             body="I build governed Snowflake pipelines and BI reporting. I've already rebuilt your reliability "
                  "numbers from public data: 130.2 and 133.0 against the reported 130 and 133. And I'd like to do "
                  "this work on Grid Resiliency programs, with your data."),
    ]),
]

ASK = [  # R's five picks (A1, A2, A3, A6, A8), in R's order; A8 always last
    "What would success look like in this role after six to twelve months?",
    "Which reliability and program metrics does the team report most often, and where do analysts spend most "
    "of their time today?",
    "How does the team evaluate programs like mainfeeder hardening today, and what would you like to measure "
    "better?",
    "How do analysts here work with engineering and field teams day to day?",
    "What are the next steps in the process?",
]
CLOSE = ("Thank you for your time. I'd like to bring the same discipline to your reliability reporting: reconcile "
         "first, test every number, and make it easy to act on.")

UK = re.compile(r"\b(programme|behaviour|colour|centre|analyse|prioritis|licence|normalis|organis|labelled|"
                r"modelled|favour|summaris|minimis|recognis)", re.I)
RESEARCH = ds.REPO / "interview-prep" / "research"


def r_star_list() -> list[tuple[str, str]]:
    """R's starred questions, as (id, wording), in the order of top40.md's 'Research backing, by sheet group'."""
    md = (RESEARCH / "top40.md").read_text(encoding="utf-8")
    sec = md.split("## Research backing, by sheet group", 1)[1].split("## Five questions to ask", 1)[0]
    return re.findall(r"^\*\*([A-Z]\d+)\. (.+?)\*\* ★", sec, flags=re.M)


def esc(s: str) -> str:
    """Escape, then mark every [you: ...] placeholder."""
    s = htmllib.escape(s, quote=False)
    return re.sub(r"\[you:[^\]]*\]", lambda m: f"<span class='ph'>{m.group(0)}</span>", s)


def build_html(body_pt: float) -> str:
    lead = round(body_pt * 1.247, 1)
    css = (HERE / "qsheet.css").read_text(encoding="utf-8")
    css = css.replace("--body: 8.5pt", f"--body: {body_pt}pt").replace("--lead: 10.6pt", f"--lead: {lead}pt")
    css = css.replace("8.5pt", "9pt")           # O-29: nothing below 9 pt anywhere (footer, meta, legend)
    assert css.count(MARGIN_V2) == 1 and css.count(FOOTER_V2) == 1, "qsheet.css changed: recheck the v3 margins"
    css = css.replace(MARGIN_V2, MARGIN_V3).replace(FOOTER_V2, FOOTER_V3)
    n_q = sum(len(items) for _, items in GROUPS)
    assert n_q == 24, n_q
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'>"
             f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
             f"<title>Dominion question sheet</title><style>{css}</style></head><body>",
             "<header class='sheet'><h1>Interview questions and answer cues</h1>"
             "<span class='meta'>Dominion Energy · panel interview · Tuesday, November 3, 2026</span></header>",
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
    out = "".join(parts)
    bad = UK.findall(re.sub(r"<style>.*?</style>", "", out, flags=re.S))
    assert not bad, f"UK spellings (O-30): {bad}"
    return out


def words(it) -> int:
    txt = " ".join([it.get("claim", ""), it.get("body", "")] + it.get("star", []))
    return len(txt.split())


def scan(pdf: Path, html: Path) -> None:
    """The final checks: 'AI' only in the resume's 'AI pilot' (items 2, 3 and 5, approved), never 'assistant', never
    'star schema', no hash, bundle or commit count; the model line and the replaced and reworded questions present."""
    import pymupdf
    doc = pymupdf.open(str(pdf))
    pdf_txt = " ".join(" ".join(pg.get_text().split()) for pg in doc)
    doc.close()
    html_txt = " ".join(re.sub(r"<[^>]+>", " ", re.sub(r"<style>.*?</style>", "", html.read_text(encoding="utf-8"),
                                                       flags=re.S)).split())
    for name, t in (("pdf", pdf_txt), ("html", html_txt)):
        t = t.replace("\xa0", " ")
        assert t.count("AI pilot") == 3 and not re.search(r"\bAI\b(?! pilot)", t), (name, "AI")
        for bad in (r"(?i)assistant", r"(?i)star schema", r"\bSHA\b", r"(?i)bundle", r"(?i)\b\d+ commits?\b",
                    r"\b[0-9a-f]{7,40}\b(?<!\d{7})", r"(?i)\bCEMI\b"):
            m = re.search(bad, t)
            assert not m, (name, bad, t[max(0, m.start() - 60):m.end() + 60])
        for need in ("The core is a small star", "What do you know about Dominion?", REWORDED["T4"],
                     "nobody yet; I built it for this application", "returns 130.2 for 2024 and 133.0 for 2025",
                     "ask the recruiter what storm-season duty means", "(CEMIn)"):
            assert need in t, (name, need)
    n_you = len(re.findall(r"\[you:", pdf_txt))
    print(f"scan: AI only in 'AI pilot' (3); no assistant, star schema, SHA, bundle, commit count or CEMI; "
          f"[you: …] items printed: {n_you}")


def main():
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    for name, items in GROUPS:
        print(name, [(it["id"], words(it)) for it in items])
    sheet, star = [(it["id"], it["q"]) for _, items in GROUPS for it in items], r_star_list()
    assert len(star) == 24, len(star)
    want = [REPLACED.get(i, (i, REWORDED.get(i, q))) for i, q in star]
    assert sheet == want, [(a, b) for a, b in zip(sheet, want) if a != b]
    print("questions match R's star list (wording and order) except:", REWORDED, REPLACED)
    chosen = None
    for pt in (9.0,):
        html = OUT / f"{STEM}.html"
        html.write_text(build_html(pt), encoding="utf-8")
        pdf = pipeline.html_to_pdf(html, OUT / f"{STEM}.pdf")
        n = len(pymupdf.open(str(pdf)))
        print(f"{pt} pt -> {n} pages")
        if n == 2:
            chosen = pt
            break
    if chosen is None:
        raise SystemExit("does not fit on two sides at 9 pt (O-29: nothing below 9 pt): trim answers, never drop a "
                         "brief-required item")
    pdf = OUT / f"{STEM}.pdf"
    doc = pymupdf.open(str(pdf))
    doc.set_metadata({"title": "Dominion question sheet", "author": "Saketh Bollina", "subject": "", "keywords": "",
                      "creator": "", "producer": ""})
    tmp = pdf.with_suffix(".tmp.pdf")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf)
    print(f"body {chosen} pt; min sizes {pipeline.pdf_min_font_size(pdf)}")
    print("fonts:", pipeline.pdf_fonts(pdf))
    doc = pymupdf.open(str(pdf))           # print-proof: every word at least 0.30 in from every page edge
    edges = []
    for pg in doc:
        W, H = pg.rect.width, pg.rect.height
        edges += [min(w[0], w[1], W - w[2], H - w[3]) for w in pg.get_text("words")]
    doc.close()
    print(f"min distance from a page edge: {min(edges):.2f} pt ({min(edges) / 72:.3f} in)")
    assert min(edges) >= EDGE_MIN_PT, f"text closer than 0.30 in to a page edge: {min(edges):.2f} pt"
    scan(pdf, OUT / f"{STEM}.html")
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=110, grey=grey)


if __name__ == "__main__":
    main()
