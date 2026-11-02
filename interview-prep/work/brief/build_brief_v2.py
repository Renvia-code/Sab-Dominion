"""Interview brief v2 (P3): HTML + print CSS -> Edge PDF, US Letter portrait. One variant-neutral version (G2, O-28).

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

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\brief\\build_brief_v2.py
Out:  interview-prep/deliverables/03_interview_brief/Dominion_interview_brief_v2.{html,pdf}
      interview-prep/work/proofs/brief_v2/
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

CH1 = ds.WORK / "charts" / "v1"
CH2 = ds.WORK / "charts" / "v2"
OUT = ds.REPO / "interview-prep" / "deliverables" / "03_interview_brief"
PROOFS = ds.WORK / "proofs" / "brief_v2"
STEM = "Dominion_interview_brief_v2"
RESEARCH = ds.REPO / "interview-prep" / "research"
SHOT = ds.WORK / "powerbi" / "b5" / "shots_v4" / "crop_p01.png"
UP = "<span class='up'>If adopted</span>"

EXTRA_CSS = """
:root { --small: 9pt; --small-lh: 12pt; }
@page {
  margin: 0.55in 0.7in 0.65in 0.7in;
  @bottom-left { content: "Dominion Energy Virginia reliability · interview brief"; font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; }
}
@page apx {
  margin: 0.45in 0.5in 0.6in 0.5in;
  @bottom-left { content: "Dominion Energy Virginia reliability · interview brief"; font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 400 9pt "Pack Sans", "Segoe UI", sans-serif; color: #6B7280; }
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
img.shot { display: block; width: 5.2in; margin: 2pt auto 2pt; border: 0.5pt solid var(--rule); }
.apx-page table, .apx-page { font-size: 9pt; line-height: 11pt; }
.apx-page h1 { font-size: 16pt; margin-bottom: 5pt; }
.apx-page td, .apx-page th { padding: 1.5pt 5pt 1.5pt 0; }
.knum td:first-child { font-weight: 600; color: var(--ink); }
.h25 { column-count: 2; column-gap: 0.2in; font-size: 9pt; line-height: 10.8pt; }
.h25 h3 { font-size: 10pt; line-height: 12pt; margin: 3pt 0 1pt; color: var(--subject); break-after: avoid; }
.h25 .q { break-inside: avoid; margin: 0 0 3.5pt; }
.h25 .q p { margin: 0; text-wrap: auto; orphans: 1; widows: 1; }
.h25 .q p.hq { font-weight: 600; color: var(--ink); }
.h25 .q p.hq i { font-weight: 400; color: var(--ink-2); }
.h25key { font-size: 9pt; line-height: 11.4pt; color: var(--ink-2); margin: 0 0 5pt; }
.dl td { vertical-align: top; }
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


# ----------------------------------------------------------------------------- the 25 hardest (R's print file)
TAG = re.compile(r"\s*\[(?:C|N|R)-[A-Za-z0-9-]+(?:,\s*(?:C|N|R)-[A-Za-z0-9-]+)*\]")
RESUME_TAG = re.compile(r"\s*\[resume:[^\]]*\]")
FIXES = [  # (old, new): D batch 6 naming, the final Isaias wording and the v2 proof review; each applies once
    ("inside a band of about 122–168", "inside its 95% prediction interval, about 122–168"),
    ("**Isaias:** 90% of the peak number out, all utilities, timed from the peak",
     "**Isaias:** 33.5 hours from the peak to clear 90% of the outage (a net count, all utilities)"),
    ("mostly because 2025 was stormier", "in a stormier year"),                       # Q24: no causal wording
    ("The SCC docket site blocked automated access, and its report", "The SCC's report"),   # Q9: no research method
    ("Fixed 27 Oct [N-8]", "Fixed Oct 27 [N-8]"),                                       # Q17: US date (O-30)
    ("the weather fit (CI 0.12–0.92) [C-S4-15]", "the weather fit (ten points)"),     # Q22: CI is upgrade-only
    ("465 → 796; no p.", "465 → 796; no p, CI or prediction interval."),             # Q1: none is on origin/main
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


# ----------------------------------------------------------------------------- pages
def build_html() -> str:
    css = (ds.WORK / "design" / "brief.css").read_text(encoding="utf-8") + EXTRA_CSS
    shot = base64.b64encode(SHOT.read_bytes()).decode("ascii")
    h25, nq = hard25_html()
    assert nq == 25, nq
    P = []

    # ------------------------------------------------------------------ 1 cover + contents
    P.append(page(f"""
<p class="cover-kicker">Interview brief</p>
<h1>Dominion Energy Virginia reliability: what public data shows, and where I'd look first</h1>
<p class="lede">Independent analysis of public data, for the panel interview on Tuesday, November 3, 2026.</p>
<p class="who"><strong>Saketh Bollina</strong></p>
<div class="contents"><ol>
<li><span>The answer first, and the eight-minute talk</span><span class="p">2</span></li>
<li><span>Finding 1 · Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions</span><span class="p">3</span></li>
<li><span>Finding 2 · Among 12 large utilities (Dominion and 11 peers), frequency is the gap</span><span class="p">4</span></li>
<li><span>Finding 3 · Weather: 2025 sits on the storm line</span><span class="p">5</span></li>
<li><span>Finding 4 · Demand is changing shape: nights and winters</span><span class="p">6</span></li>
<li><span>The Power BI report, and how the analysis is built</span><span class="p">7</span></li>
<li><span>The role, and the first 90 days</span><span class="p">8</span></li>
<li class="apx"><span>A1 · Know every number</span><span class="p">9</span></li>
<li class="apx"><span>A2–A3 · The 25 hardest questions</span><span class="p">10</span></li>
<li class="apx"><span>A4 · Delivery and rehearsal</span><span class="p">12</span></li>
</ol></div>
<p class="small">Every figure comes from public data (EIA-861 and PUDL, NOAA Storm Events, EIA-930 and, with the
upgrade, EAGLE-I county outages) or Dominion's own publications. No Dominion internal data was used. Material tagged
{UP} depends on adopting the repo upgrade; the public-only line is given beside it. Items marked
<span class="placeholder">[you: …]</span> are for you to fill in.</p>
""", "cover"))

    # ------------------------------------------------------------------ 2 answer first + talk
    P.append(page(f"""
<p class="section-no">The answer first</p>
<h1>A stormier year, a frequency gap, and storms by county</h1>
<p class="lede">Dominion's reported outage minutes rose from 130 to 133; rebuilt from public EIA-861 data they are
130.2 and 133.0. 2025 had more storms and more interruptions, and once storms are counted there is no clear
underlying trend. Against its peers, Dominion's gap is how often customers lose power, not how long.</p>
<div class="figures">
 <div class="figure is-subject"><div class="value subject">+2.8</div><div class="label">minutes: the rebuilt 3-year
 average, 130.2 → 133.0. 2025 (144.4) replaced 2022 (136.0) in the window</div></div>
 <div class="figure"><div class="value">+10%</div><div class="label">both storm county-days and interruptions per
 customer (SAIFI), 2022 → 2025; minutes per interruption (CAIDI) −4%</div></div>
 <div class="figure"><div class="value">4th highest</div><div class="label">of 12 on frequency (SAIFI 2021–25: 1.21 against an
 11-peer median of 0.93); 6th of 12 on minutes per interruption</div></div>
</div>
<h2>The eight-minute talk, slide by slide</h2>
<table>
<tr><th>#</th><th>Slide</th><th>Say it in one line</th><th class="r">Time</th></tr>
<tr><td class="k">1</td><td>Title</td><td>Independent analysis of public data; nothing internal.</td><td class="r">0:35</td></tr>
<tr><td class="k">2</td><td>130 → 133</td><td>2025 replaced 2022 in the window; SAIFI +10%, CAIDI −4%, storm county-days
+10%. Dominion attributes the rise “primarily” to storms, and 2025 sits on the storm line.</td><td class="r">1:10</td></tr>
<tr><td class="k">3</td><td>Dominion and 11 peers</td><td>Interruption length mid-pack (6th of 12); frequency 4th highest.
Methods differ, so ranks are indicative.</td><td class="r">0:55</td></tr>
<tr><td class="k">4</td><td>Storms</td><td>{UP} County-days with a storm report had about 12 times the outage hours
of calm days (11.9×, 95% CI 7.9–16.9): an association. Public-only: years with more storm days had more outage
minutes (r = 0.70, ten years).</td><td class="r">1:05</td></tr>
<tr><td class="k">5</td><td>The Power BI report</td><td>One page per question, customer-weighted measures, a year slicer.
Import for presentation (D13); {UP} through one folder parameter.</td><td class="r">0:55</td></tr>
<tr><td class="k">6</td><td>How it's built</td><td>RAW → STG → MART, tests, a data dictionary, a decisions log;
reconciled to the reported 130 and 133.</td><td class="r">1:05</td></tr>
<tr><td class="k">7</td><td>First 90 days</td><td>The questions I'd bring and what I'd build; it ends on a Power BI
program-tracking report.</td><td class="r">0:55</td></tr>
<tr><td class="k">8</td><td>Close</td><td>Three takeaways, then: “I've built a tested Snowflake → Power BI pipeline on
public reliability data.”</td><td class="r">1:00</td></tr>
</table>
<p class="source">Times are the speaker notes read at about 130 words a minute: about 7:40, leaving two minutes for
interruptions.</p>
<h2>Say it carefully: the two-sided lines</h2>
<ul class="tight">
<li>Measured from 2023 instead of 2022, 79% of the change (in log terms) is frequency.</li>
<li>2025's SAIFI (1.320) only edges 2018's (1.303), and 2025's outage minutes (144.4) are below 2018 (149.6) and
2019 (149.9). One year is not a trend.</li>
<li>No 2015–2025 trend is statistically clear. {UP} SAIFI p = 0.54, CAIDI p = 0.74, SAIDI p = 0.58
(scripts/trend_tests.py); public-only: say “no clear trend” without p-values.</li>
<li>Adjusted for storm days, there is no clear trend since 2015. {UP} About +0.34 minutes a year, 95% CI −1.41 to
+2.08, p = 0.67.</li>
</ul>
"""))

    # ------------------------------------------------------------------ 3 finding 1
    P.append(page(f"""
<p class="section-no">Finding 1</p>
<h1>Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions</h1>
<p>SAIDI, the average outage minutes per customer, is SAIFI (how often a customer loses power) times CAIDI (how long
each interruption lasts). Dominion's 2025 Annual Report gives a 3-year SAIDI, excluding major events, of 133 minutes
for 2023–25, up from 130 for 2022–24, and explains it (p. 10): “This increase is primarily due to increased storm
activity.” The public Virginia data reproduces both reported figures to the minute: 130.2 and 133.0.</p>
<p>A 3-year average moves when a year leaves the window: 2025 (144.4 minutes) replaced 2022 (136.0), a rise of 2.8
minutes in the average. Between those two years storm county-days rose 10%, SAIFI rose 10% and CAIDI fell 4%. The
weather fit (Finding 3) puts 2025 on the storm line, so the public data agrees with Dominion's reading: once storms
are counted there is no clear underlying trend.</p>
<figure class="chart w50">{svg(CH2 / "s2_change_2022_2025_adopted.svg")}</figure>
<p class="source">Source: EIA-861 2025 final and PUDL (EIA-861) 2013–2024, Dominion Energy Virginia (utility 19876),
excluding major event days; NOAA Storm Events. Storm county-days 718 → 791 count Bedford city once (decision D22,
{UP}); on the public repo they are 723 → 796, also +10%. Reported figures: Dominion Energy 2025 Annual Report,
p. 10.</p>
<h2>The same split from either base year</h2>
<table>
<tr><th>Base year → 2025</th><th class="r">SAIDI</th><th class="r">SAIFI</th><th class="r">CAIDI</th>
<th class="r">Share from frequency</th></tr>
<tr class="is-subject"><td>2022 (the year that left the window)</td><td class="r">+6.1%</td><td class="r">+10.1%</td>
<td class="r">−3.6%</td><td class="r">more than all of it</td></tr>
<tr><td>2023</td><td class="r">+17.1%</td><td class="r">+13.3%</td><td class="r">+3.3%</td><td class="r">79%</td></tr>
</table>
<div class="say"><strong>If asked “so reliability got worse?”</strong> “2025 had more storms and more interruptions
than 2022, and Dominion attributes the rise primarily to storms. Once storms are counted there's no clear trend:
2025's SAIFI only edges 2018's, and its outage minutes are below 2018 and 2019. With outage records, I'd check
whether non-storm interruptions are rising underneath.”</div>
"""))

    # ------------------------------------------------------------------ 4 finding 2
    P.append(page(f"""
<p class="section-no">Finding 2</p>
<h1>Among 12 large utilities (Dominion and 11 peers), interruption length is mid-pack; frequency is the gap</h1>
<p>Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before results were computed
(decision D10); means of 2021–2025, excluding major event days. Dominion's SAIFI of 1.21 is the 4th highest of the 12
(11-peer median 0.93); its CAIDI of 110 minutes is 6th, mid-pack (11-peer median 99.5); its 3-year SAIDI, 133.0, is
4th.</p>
<figure class="chart w54">{svg(CH2 / "s3_peer_quadrant_v2_adopted.svg")}</figure>
<table>
<tr><th>Utility</th><th>Major-event method</th><th class="r">SAIFI 2021–25</th><th class="r">CAIDI 2021–25</th>
<th class="r">SAIDI 2023–25</th></tr>
{peers_rows()}
</table>
<p class="source">Source: EIA-861 / PUDL, excluding major event days; means of annual values; sorted by SAIFI.
Georgia Power and Duke Energy Florida filed “Other” in 2013 only. The public repo's workbook computes CAIDI from the
5-year means, so its 11-peer median prints 99.3; the ranks are the same.</p>
<div class="say"><strong>The caveat to raise yourself:</strong> 10 of the 12 file IEEE 1366 every year 2014–25;
Dominion and Alabama Power file “Other” (their own major-event rules), so the ranking is indicative. If asked:
with all events included, Dominion's SAIFI (1.531) ranks 6th of 12 (median of the other 11, 1.408) and its
SAIDI 2023–25 (223.0) 9th. Either way, the gap is how often customers lose power, not how fast it comes back.</div>
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
<li>{UP} The 31 counties Dominion serves alone average 159 minutes a year, against 211 in the 68 shared counties.
That compares places (mostly cities and inner suburbs against rural counties), not utilities.</li>
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
to 2025, average load at 4 a.m. rose 41%, against 27% at 4 p.m.; across the hours ending 1–5 a.m. the rise was
39–41%. The highest hour of the year rose 26% (19,803 → 24,957 MW) and the lowest 52% (7,167 → 10,903 MW). Winter set
the yearly peak in 2019, 2022 and 2025.</p>
<figure class="chart w54">{svg(CH2 / "a3_load_profile_public.svg")}</figure>
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
<img class="shot" alt="The report's Summary page: year slicer, five cards, SAIFI and CAIDI trends, actual and
weather-adjusted SAIDI, and the storm-day scatter" src="data:image/png;base64,{shot}">
<p class="source">{UP} The Summary page of the upgraded report, year 2025: customers served 2.68M, SAIDI 144.4,
minutes to restore 109.4, SAIFI 1.320, major-event share 53%. Public-only: deck slide 5 shows the What moved page of
your current report. The .pbix is not on GitHub by design.</p>
<p><strong>The model.</strong> One fact table, FCT_RELIABILITY (utility × state × year), many-to-one to DIM_UTILITY
(names, peer groups); one page per question. Measures are customer-weighted: SAIDI is customer-minutes over
customers within a year, and the 3-year figure is the mean of the three annual values, as Dominion reports it. The
KPI cards follow a disconnected year table. Built in DirectQuery during development, Import for presentation
(decision D13). {UP} 18 tables imported through one DataFolder parameter, so it opens offline; 11 pages, ending on
Data notes (31 tests, 12 of 12 reconciled).</p>
<div class="code">Selected SAIDI =
VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)
RETURN CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = SelectedYear)</div>
<p><strong>The build.</strong> Public files land in Snowflake as raw text exactly as published (RAW), are typed and
cleaned (STG), and become facts, dimensions and views (MART). Tests T1–T12 run after each load and all pass ({UP}
T1–T31). A data dictionary covers every table and column; measures are defined in docs/05. Decisions are logged
(D1–D14; {UP} D1–D22); the peer set was chosen by EIA ID before results. Reconciled: 130.2 and 133.0 against 130 and
133, and test T4 matches 2025 to EIA's published 306.7, 144.4 and 2,675,735 customers ({UP} 12 of 12 values: a check
of definitions). scripts/run_local_duckdb.py rebuilds the core mart and runs its checks.</p>
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
(fault location, isolation and restoration). The Strategic Underground Program is separate.</li>
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
        ("130 → 133", "Reported 3-year SAIDI ex-MED, 2022–24 → 2023–25 · Annual Report p. 10",
         "“Primarily due to increased storm activity” → is it real? (Q4)"),
        ("130.2 → 133.0", "The same, rebuilt: mean of three annual values · EIA-861 / PUDL",
         "Same definitions, not proof the data is true (Q13)"),
        ("136.0 → 144.4", "SAIDI ex-MED 2022 (left the window) and 2025 (joined) · EIA-861",
         "(144.4 − 136.0) ÷ 3 = 2.8 minutes"),
        ("1.199 → 1.320 · 113.5 → 109.4", "SAIFI +10% and CAIDI (SAIDI ÷ SAIFI) −4%, 2022 → 2025 · EIA-861",
         "SAIFI only edges 2018 (1.303); CAIDI is a ratio, not restoration speed"),
        ("718 → 791 · 723 → 796", "Storm county-days 2022 → 2025, +10% (If adopted · public) · NOAA",
         "D22 counts Bedford city once"),
        ("145.3 vs 144.4 · r = 0.70", "2025 from the storm-day fit (2015–2024, n = 10) vs actual; the fit's r",
         "If adopted: 95% prediction interval 122.3–168.2; p = 0.025; CI for r 0.12–0.92 (Q1)"),
        ("79%", "Share of the 2023 → 2025 change from frequency (log split)", "From 2022: more than all of it"),
        ("1.21 · 4th highest of 12 · 133.0", "SAIFI 2021–25 ex-MED (11-peer median 0.93); SAIDI 2023–25, also 4th",
         "All events: SAIFI 1.531, 6th (median 1.408); SAIDI 223.0, 9th"),
        ("110 · 6th of 12", "CAIDI 2021–25: mid-pack; 11-peer median 99.5", "Public workbook median: 99.3"),
        ("10 of 12", "File IEEE 1366 every year 2014–25 · EIA-861",
         "Dominion, Alabama Power: “Other” → ranks indicative (Q2)"),
        ("11.9× (7.9–16.9) · 332.8 vs 27.9", "If adopted: outage customer-hours per 1,000 customers, storm vs calm "
         "county-days; the levels' intervals 225.6–453.4 and 23.1–33.2", "An association; EAGLE-I counts all utilities "
         "(Q3, Q5)"),
        ("9.9× · 19.9× · 5.9–27.4×", "If adopted: non-major days · Dominion-only counties · each year",
         "Every year's interval is above 1"),
        ("6,108 vs 6,530", "If adopted: storm county-days with complete readings (99 counties) vs all (103)",
         "422 = 114 off the map + 308 failed (96 in 2025)"),
        ("306.7 vs 144.4", "2025 SAIDI with and without major event days; MEDs 53% (162.3)",
         "Dominion vs FPL: compare like with like (Q2)"),
        ("2.68M", "Customers served, 2025: 2,675,735 · EIA-861", "One SAIDI minute ≈ 2.7M customer-minutes"),
        ("T1–T12 · D1–D14", "Tests, all pass; decisions logged (public). If adopted: T1–T31, D1–D22, and 12 of 12 "
         "values reconciled", "Reconciliation is a definitions check (Q13)"),
        ("Rows", "EIA-861 977 + 24,358 · NOAA 831,288 · EIA-930 6,077,232 (If adopted 6,094,320)",
         "If adopted: EAGLE-I 11,608,442; 18 tables, 11 pages"),
        ("99.8%", "Smart meters as a share of all meters, 2025 · EIA-861", "A last gasp marks the start (Q6)"),
        ("500 · 2 min · 5 yr · −32%", "Mainfeeder selection rule; reported cut on hardened feeders (2023)",
         "Before/after overstates it (Q8)"),
        ("+41% · +27% · +26% · +52%", "Load 2019 → 2025: 4 a.m., 4 p.m., top hour, lowest hour · EIA-930",
         "Not attributable to data centers (Q10)"),
        ("1.849 → 1.887", "Co-op SAIFI 2025 before and after matching denominators (P18)",
         "A co-op filed SAIDI but no SAIFI (Q17)"),
        ("50 basis points", "How far the SCC can move the allowed return (factors include reliability)",
         "Why the numbers have to be right"),
        ("20M+ · 71% → 90% · 17% · +9%", "Mercury: rows; grounded-answer accuracy; settlement time; renewals",
         "Causal only for the A/B test (Q17)"),
        ("$690M · 440", "The Life Initiative: investments in the board's Tableau view", "Who used it? [you: …]"),
        ("25% · 3-2", "Travel up to 25%; three office days, two remote · the posting", "[you: your answers]"),
        ("May 2026 → H2 2027", "NextEra merger announced; Virginia order by mid-January 2027; close expected",
         "No view on the deal (Q23)"),
    ]
    rows = "".join(f"<tr><td>{htmllib.escape(a)}</td><td>{ph(htmllib.escape(b))}</td><td>{ph(htmllib.escape(c))}</td>"
                   f"</tr>" for a, b, c in K)
    rows = rows.replace("If adopted", UP)
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
<p class="h25key"><b>C</b> = claim, <b>P</b> = proof, <b>L</b> = honest limit. ● = drill these first. <i>Adopted</i> =
depends on adopting the repo upgrade; <i>Public-only</i> = the fallback line. <span class="placeholder">[you: …]</span>
= only you can fill it. D = decision, P18 and the like = data-quality notes, T = tests (repo docs). Q numbers match
the “likely follow-up” column in A1.</p>
<div class="h25">{h25}</div>
""", "appendix apx-page"))

    # ------------------------------------------------------------------ 12 A4 delivery and rehearsal
    P.append(page(f"""
<p class="section-no">Appendix A4</p>
<h1>Delivery and rehearsal</h1>
<p class="h25key">Strength: <b>strong</b> = meta-analysis or large review; <b>single</b> = one study; <b>mixed</b> =
replications disagree; <b>practice</b> = common advice with no study verified (kept and labeled, never cited).</p>
<table class="dl">
<tr><th>Tip</th><th>Rests on</th><th>Strength</th><th>Do this</th></tr>
<tr><td><b>The first minutes count</b></td><td>Barrick, Swider &amp; Stewart 2010</td><td>single</td><td>Open with a
crisp 30-second answer on what you do and built; early impressions tracked final ratings (r = .42).</td></tr>
<tr><td><b>Sell with facts; never stretch</b></td><td>Swider et al. 2011; Barrick et al. 2009</td><td>single +
strong</td><td>Real results helped (r = .20); “image creation” hurt (r = −.11 to −.19). Use the resume's numbers
exactly.</td></tr>
<tr><td><b>Expect past-behavior questions</b></td><td>Sackett et al. 2022; Taylor &amp; Small 2002</td><td>strong</td>
<td>Every answer is scored on a scale. Have 5–6 true STAR stories: situation, <i>your</i> action, result.</td></tr>
<tr><td><b>State the limit, then answer it</b></td><td>O'Keefe 1999</td><td>strong</td><td>A limit builds credibility
only with its answer: “ten points is thin, so the headline uses county-days”.</td></tr>
<tr><td><b>Ask a follow-up question</b></td><td>Huang et al. 2017</td><td>moderate (conversations, not
interviews)</td><td>At “Any questions?”, first follow up on something a panelist said.</td></tr>
<tr><td><b>Rehearse aloud</b></td><td>Powell, Stanley &amp; Brown 2018</td><td>strong</td><td>Anxiety and scores
correlate at r = −.19. Rehearse to a mock panel; that it calms you is a reading, not a result.</td></tr>
<tr><td><b>Call the nerves “excitement”</b></td><td>Brooks 2014; Bosshard &amp; Gomez 2024; Ganley et al. 2021</td>
<td>mixed, small</td><td>Say “I'm excited”, not “calm down”: the pooled effect is small (d ≈ 0.2) and a math
replication found nothing.</td></tr>
<tr><td><b>Answer first</b> · <b>“I don't know” → how I'd find out</b> · <b>Pace, close, thank</b></td><td>none
verified</td><td>practice</td><td>Claim, one proof, then the limit. Never guess a number; say where you'd look and
when you'll come back. Pause after each answer, close in one line, send a thank-you note within a day.</td></tr>
<tr><td><s>Power posing</s></td><td>Ranehill et al. 2015</td><td>failed</td><td>Left out.</td></tr>
</table>
<h2>Three interviewers</h2>
<p>Panelists may score separately and then combine; the panel research is mixed (Dixon et al. 2002), so these rules
are inference. Make each answer complete on its own. Answer the asker, then turn to the others for your last
sentence. Take a challenge with thanks: concede what's right, then answer.</p>
<table class="dl">
<tr><th>Panelist</th><th>Listens for</th><th>Lead with</th><th>Questions</th></tr>
<tr><td><b>BI manager</b></td><td>How it's built; checked numbers; Power BI</td><td>The model, the measures, the
reconciliation; the printed report page</td><td>Q11–Q18</td></tr>
<tr><td><b>Engineer</b></td><td>Exact definitions; honest limits</td><td>Precise terms, a fast concession, the data
that would settle it</td><td>Q1–Q10</td></tr>
<tr><td><b>HR</b></td><td>Plain words, fit, how you take pushback</td><td>No acronyms (Q24), true STAR stories, calm
on the merger</td><td>Q19–Q25</td></tr>
</table>
<h2>Rehearsal outline for Monday</h2>
<ol class="tight">
<li>Decide the variant first (adopted or public-only); everything after depends on it.</li>
<li>Apply the Power BI guide for your variant; print one report page and the model view for Q11.</li>
<li>Read this brief once, for understanding; mark anything you couldn't explain.</li>
<li>Say the deck aloud against an 8-minute timer, three times; record one run. Cut words, not slides.</li>
<li>Drill the question sheet and the 25 hardest by recall: cover the answer, say it aloud, then check (Roediger &amp;
Karpicke 2006; Rowland 2014: strong).</li>
<li>Spread the drills: an afternoon round and an evening round of the misses (Cepeda et al. 2006: strong).</li>
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


if __name__ == "__main__":
    main()
