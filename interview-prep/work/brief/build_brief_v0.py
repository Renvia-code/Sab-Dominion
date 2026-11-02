"""Safety-net v0 interview brief (P3): HTML + print CSS -> Edge PDF, US Letter portrait.

Cover with contents, 7 body pages, 2 appendix pages. Charts are the v0 chart SVGs, inlined so the
text stays text. Every number is in interview-prep/claims.csv. Placeholders the candidate fills in
are marked [you: ...].

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\brief\\build_brief_v0.py
Out:  interview-prep/deliverables/03_interview_brief/Dominion_interview_brief_v0.{html,pdf}
      interview-prep/work/proofs/brief_v0/ (PNG proofs, colour and greyscale)
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402
import pipeline  # noqa: E402

CH = ds.WORK / "charts" / "v0"
OUT = ds.REPO / "interview-prep" / "deliverables" / "03_interview_brief"
PROOFS = ds.WORK / "proofs" / "brief_v0"
STEM = "Dominion_interview_brief_v0"

EXTRA_CSS = """
.cover-kicker { font-size: 10.5pt; font-weight: 600; color: var(--subject); margin: 0.9in 0 10pt; }
.cover h1 { font-size: 30pt; line-height: 1.1; max-width: 6.6in; margin-bottom: 14pt; }
.cover .who { font-size: 13pt; line-height: 18pt; margin: 18pt 0 0; }
.cover .who strong { font-size: 15pt; }
.contents { margin-top: 0.7in; border-top: 1.5pt solid var(--ink); padding-top: 8pt; }
.contents ol { list-style: none; margin: 0; padding: 0; }
.contents li { display: grid; grid-template-columns: 1fr auto; gap: 12pt; padding: 4pt 0;
               border-bottom: 0.5pt solid var(--rule); font-size: 10.5pt; }
.contents li span.p { color: var(--muted); font-variant-numeric: tabular-nums; }
.contents li.apx { color: var(--ink-2); }
.cover .small { margin-top: 14pt; max-width: 6.4in; }
.figures.two { grid-template-columns: repeat(2, 1fr); }
.figure .value { font-size: 32pt; }
ul.tight { margin: 2pt 0 8pt; padding-left: 14pt; }
ul.tight li { margin: 0 0 4pt; }
figure.chart { margin: 6pt 0 2pt; }
figure.chart.narrow svg { width: 6.1in; }
.say { background: var(--tint); border-radius: 3pt; padding: 7pt 10pt; margin: 10pt 0 6pt; }
.say strong { color: var(--ink); }
td.k { white-space: nowrap; font-weight: 600; color: var(--ink); }
.nowrap { white-space: nowrap; }
h1 { font-size: 20pt; }
"""


def svg(stem: str) -> str:
    s = (CH / f"{stem}.svg").read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>", "", s, flags=re.S)
    s = re.sub(r"<metadata>.*?</metadata>", "", s, flags=re.S)
    return s.strip()


def peers_rows():
    rows = list(csv.DictReader(open(CH / "s3_peer_quadrant.csv", encoding="utf-8")))
    rows.sort(key=lambda d: -float(d["saifi_5yr_2021_25"]))
    out = []
    for d in rows:
        cls = ' class="is-subject"' if d["utility"] == "Dominion Energy Virginia" else ""
        out.append(f"<tr{cls}><td>{d['utility']}</td><td>{d['major_event_method']}</td>"
                   f"<td class='r'>{float(d['saifi_5yr_2021_25']):.2f}</td>"
                   f"<td class='r'>{float(d['caidi_5yr_2021_25']):.0f}</td>"
                   f"<td class='r'>{float(d['saidi_3yr_2023_25']):.0f}</td></tr>")
    return "".join(out)


def page(inner: str, cls: str = "") -> str:
    return f'<section class="page {cls}">{inner}</section>'


def build_html() -> str:
    css = (ds.WORK / "design" / "brief.css").read_text(encoding="utf-8") + EXTRA_CSS
    P = []

    # ------------------------------------------------------------------ 1 cover + contents
    P.append(page("""
<p class="cover-kicker">Interview brief</p>
<h1>Dominion Energy Virginia reliability: what public data shows, and where I'd look first</h1>
<p class="lede">Independent analysis of public data, for the panel interview on Tuesday 3 November 2026.</p>
<p class="who"><strong>Saketh Bollina</strong></p>
<div class="contents"><ol>
<li><span>The answer first, and the ten-minute talk</span><span class="p">2</span></li>
<li><span>Finding 1 · Outage minutes rose because interruptions became more frequent</span><span class="p">3</span></li>
<li><span>Finding 2 · Against twelve peers, frequency is the gap</span><span class="p">4</span></li>
<li><span>Finding 3 · Weather: storm days and outage minutes move together</span><span class="p">5</span></li>
<li><span>Finding 4 · Demand is changing shape: nights and winters</span><span class="p">6</span></li>
<li><span>The role, and the first 90 days</span><span class="p">7</span></li>
<li><span>How the analysis is built, and the numbers to know</span><span class="p">8</span></li>
<li class="apx"><span>Appendix A · Definitions, and what public data cannot show</span><span class="p">9</span></li>
<li class="apx"><span>Appendix B · The twelve-peer table, sources and tests</span><span class="p">10</span></li>
</ol></div>
<p class="small">Every figure comes from public data (EIA-861 and PUDL, NOAA Storm Events, EIA-930) or Dominion's
own publications. No Dominion internal data was used. Items marked
<span class="placeholder">[you: …]</span> are for you to fill in.</p>
""", "cover"))

    # ------------------------------------------------------------------ 2 answer first
    P.append(page("""
<p class="section-no">The answer first</p>
<h1>Frequency, weather and a new load shape</h1>
<p class="lede">Dominion's reported outage minutes rose from 130 to 133. Rebuilt from public EIA-861 data they are
130.2 and 133.0, so the public data reconciles. The rise came from customers losing power more often, not from
longer outages.</p>
<div class="figures">
 <div class="figure is-subject"><div class="value subject">+10%</div><div class="label">interruptions per customer
 (SAIFI), 2022 → 2025: 1.199 → 1.320, the highest of 2013–2025</div></div>
 <div class="figure"><div class="value">4th of 12</div><div class="label">on frequency among twelve peers (SAIFI
 2021–25: 1.21 vs median 0.96); restoration time 6th of 12</div></div>
 <div class="figure"><div class="value">+39–41%</div><div class="label">average load in the hours ending 1–5 a.m.,
 2019 → 2025, against about +27% for 1–5 p.m. (PJM DOM zone)</div></div>
</div>
<h2>The ten-minute talk, slide by slide</h2>
<table>
<tr><th>#</th><th>Slide</th><th>Say it in one line</th></tr>
<tr><td class="k">1</td><td>Title</td><td>Independent analysis of public data; nothing internal.</td></tr>
<tr><td class="k">2</td><td>130 → 133: more frequent, not longer</td><td>2025 replaced 2022 in the 3-year window; between
them SAIFI rose 10% and CAIDI fell 4%.</td></tr>
<tr><td class="k">3</td><td>Twelve peers</td><td>Mid-pack on restoration time (6th of 12), 4th highest on
frequency.</td></tr>
<tr><td class="k">4</td><td>Weather</td><td>More storm days, more outage minutes (r = 0.70 over ten years): an
association, not a cause.</td></tr>
<tr><td class="k">5</td><td>Demand shape</td><td>Small hours +39–41%, afternoons about +27%; winter set the peak in
2019, 2022 and 2025.</td></tr>
<tr><td class="k">6</td><td>First 90 days</td><td>Reconcile, diagnose, prioritise and track; ends in a Power BI
programme-tracking report.</td></tr>
<tr><td class="k">7</td><td>How it's built</td><td>Snowflake RAW → STG → MART, tests, dictionary, decisions;
reconciled to 130 and 133.</td></tr>
<tr><td class="k">8</td><td>Close</td><td>Frequency first, net of weather, plan for a new load shape.</td></tr>
</table>
<h2>Say it carefully: the two-sided lines</h2>
<ul class="tight">
<li>Measured from 2023 instead of 2022, 79% of the change (in log terms) is still frequency.</li>
<li>2025's outage minutes (144.4) are still below 2018 (149.6) and 2019 (149.9).</li>
<li>Over 2015–2025 no trend is statistically clear (SAIFI p = 0.54, CAIDI p = 0.74, SAIDI p = 0.58): one year
is not a trend.</li>
<li>Adjusted for storm days, there is no clear trend since 2015: about +0.34 minutes a year, 95% range −1.41 to
+2.09.</li>
</ul>
"""))

    # ------------------------------------------------------------------ 3 finding 1
    P.append(page(f"""
<p class="section-no">Finding 1</p>
<h1>Outage minutes rose from 130 to 133 because interruptions became more frequent, not longer</h1>
<p>SAIDI, the average outage minutes per customer, is SAIFI (how often a customer loses power) times CAIDI (how
long each interruption lasts). Dominion's 2025 Annual Report gives a 3-year SAIDI, excluding major events, of 133
minutes for 2023–25, up from 130 for 2022–24, and attributes the increase primarily to increased storm activity
(p. 10). The public rebuild gives 130.2 and 133.0.</p>
<p>A 3-year average moves only when a year leaves the window: 2025 (144.4 minutes) replaced 2022 (136.0). Between
those two years SAIFI rose 10% and CAIDI fell 4%, so the whole rise is frequency. 2025's SAIFI, 1.320, is the
highest in EIA's 2013–2025 record (the next highest is 1.303 in 2018).</p>
<figure class="chart narrow">{svg("s2_lock_2022_2025_saifi")}</figure>
<p class="source">Source: EIA-861 2025 final and PUDL (EIA-861) 2013–2024, Dominion Energy Virginia (utility 19876),
excluding major event days. Reported figures: Dominion Energy 2025 Annual Report, p. 10.</p>
<h2>The same answer from either base year</h2>
<table>
<tr><th>Base year → 2025</th><th class="r">SAIDI</th><th class="r">SAIFI</th><th class="r">CAIDI</th>
<th class="r">Share from frequency</th></tr>
<tr class="is-subject"><td>2022 (the year that left the window)</td><td class="r">+6.1%</td><td class="r">+10.1%</td>
<td class="r">−3.6%</td><td class="r">all of it</td></tr>
<tr><td>2023</td><td class="r">+17.1%</td><td class="r">+13.3%</td><td class="r">+3.3%</td><td class="r">79%</td></tr>
</table>
<div class="say"><strong>If asked “so reliability got worse?”</strong> “Customers lost power more often in 2025
than in any year of EIA's 2013–2025 record, while restoration time was flat to lower. One year isn't a trend, and
2025's minutes are still below 2018 and 2019, so I'd look at what drove the extra interruptions, by circuit and
cause, before calling it a trend.”</div>
"""))

    # ------------------------------------------------------------------ 4 finding 2
    P.append(page(f"""
<p class="section-no">Finding 2</p>
<h1>Among 12 peer utilities, Dominion restores at a mid-pack pace; frequency is the gap</h1>
<p>Twelve large investor-owned utilities in PJM and the Southeast, chosen by EIA ID before any result was seen.
Averages of 2021–2025, excluding major event days. Dominion's SAIFI of 1.21 is the 4th highest of 12 (peer median
0.96); its CAIDI of 110 minutes is 6th of 12 (median 105). Its nearest neighbours are Duke Energy Progress and
Georgia Power. On 3-year SAIDI (2023–25) Dominion is also 4th of 12, at 133.0 minutes.</p>
<figure class="chart">{svg("s3_peer_quadrant")}</figure>
<p class="source">Source: EIA-861 / PUDL 2021–2025, excluding major event days; means of annual values. The full
table is in Appendix B.</p>
<div class="say"><strong>The caveat to raise yourself:</strong> utilities set aside major event days differently.
Most of these peers use the IEEE 1366 method; Dominion reports under its own rule, so the ranking is indicative,
not exact. The pattern still matches Finding 1: the gap is how often customers lose power, not how fast it comes
back.</div>
"""))

    # ------------------------------------------------------------------ 5 finding 3
    P.append(page(f"""
<p class="section-no">Finding 3</p>
<h1>Years with more storm days had more outage minutes (r = 0.70 over ten years)</h1>
<p>A storm county-day is a day on which NOAA recorded a wind, winter or tropical storm in a Virginia county
Dominion serves. There were 796 in 2025, up from 465 in 2024. Over 2015–2024 the correlation with SAIDI excluding
major events is 0.70 (n = 10, R² 0.48). A straight-line fit made without 2025 gives 145.3 minutes for 2025; the
actual was 144.4. So 2025 looks like a stormy year more than a break in the trend, consistent with Dominion's own
explanation.</p>
<figure class="chart">{svg("s4_storm_days_vs_saidi")}</figure>
<p class="source">Source: NOAA Storm Events 2015–2025 (wind, winter and tropical event types) by county in Dominion's
Virginia service territory (EIA-861); EIA-861 SAIDI excluding major event days; least-squares fit on 2015–2024.</p>
<h2>Two more things to know</h2>
<ul class="tight">
<li>Adjusted for storm days, there is no clear trend since 2015 (+0.34 minutes a year, 95% range −1.41 to +2.09,
p = 0.67). The adjustment is exploratory: ten points.</li>
<li>Major event days are set aside from these figures. In 2025 they were 53% of all-event outage minutes (162.3 of
306.7); they swing most from year to year (285 minutes in 2022, 41 in 2024).</li>
</ul>
<div class="say"><strong>What it cannot say:</strong> which circuits, which causes, or whether hardened lines held
up. That needs outage records with cause codes and circuit locations.</div>
"""))

    # ------------------------------------------------------------------ 6 finding 4
    P.append(page(f"""
<p class="section-no">Finding 4</p>
<h1>Overnight demand grew faster than afternoon demand, and winter rivals summer for the yearly peak</h1>
<p>EIA-930 hourly demand for the PJM Dominion (DOM) zone, which is wider than Dominion's retail territory. From
2019 to 2025, average load in the hours ending 1–5 a.m. rose 39–41%, against about 27% in the hours ending
1–5 p.m. The highest hour of the year rose 26% (19,803 → 24,957 MW) and the lowest 52% (7,167 → 10,903 MW).
Winter set the yearly peak in 2019, 2022 and 2025; 2026 so far is a near-tie (25,413 MW winter vs 25,384 MW
summer).</p>
<figure class="chart">{svg("s5_winter_summer_peaks")}</figure>
<p class="source">Source: EIA-930 hourly demand, PJM DOM zone, July 2018–October 2026 (2026 year to date). Winter =
December–February, summer = June–August.</p>
<ul class="tight">
<li>Of the 50 highest hours in the EIA-930 record from July 2018 to December 2025, 47 fell in 2025.</li>
<li>Commercial electricity sales in Dominion's Virginia territory rose 65% from 2013 to 2025 (39.08 → 64.62 TWh)
on 8% more commercial customers (EIA-861).</li>
</ul>
<div class="say"><strong>Don't say “data centers caused it”.</strong> Growth around the clock is consistent with
large constant loads, but these data cannot identify customers. Say: “less overnight slack, and winter readiness
matters as much as summer.”</div>
"""))

    # ------------------------------------------------------------------ 7 role + 90 days
    P.append(page("""
<p class="section-no">The role</p>
<h1>The role, and what I would do in the first 90 days</h1>
<p>The posting that most likely matches this interview is <strong>Associate Business Intelligence Analyst /
Business Intelligence Analyst</strong> (Richmond, hybrid: three days in the office, two remote). It supports
<strong>Grid Resiliency programmes</strong> with Power BI dashboards and reports, and asks for Power BI, SQL, Excel,
Snowflake, Power Apps and SharePoint, with reliability metrics as preferred knowledge.
<span class="placeholder">[you: confirm the exact title and team with the recruiter]</span></p>
<h2>Grid Resiliency, from Dominion's own description</h2>
<ul class="tight">
<li>Four programmes: mainfeeder hardening, voltage island mitigation, voltage optimisation, and intelligent grid
devices (fault location, isolation and restoration). The Strategic Underground Program is separate.</li>
<li>Mainfeeder hardening selects feeders with at least 500 customers whose average SAIDI is more than 2 minutes
worse than the rest, and with above-average outages over the last five years.</li>
<li>Dominion reports a 32% reduction in outage minutes on feeders hardened for at least 12 months (as of 30 November
2023).</li>
</ul>
<h2>First 90 days</h2>
<table>
<tr><th>Days</th><th>What I'd do</th><th>Deliverable</th></tr>
<tr><td class="k">1–30 · Reconcile</td><td>Learn how outages, meter events and circuits are recorded and reported.
Rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filed figures.</td><td>A reconciled baseline
with written definitions</td></tr>
<tr><td class="k">31–60 · Diagnose</td><td>Interruptions by circuit and cause code, vegetation included; customers
interrupted repeatedly (CEMI). Restoration timed from meter “last gasp”: 99.8% of Dominion's meters were smart
meters in 2025.</td><td>Tested views and a data dictionary</td></tr>
<tr class="is-subject"><td class="k">61–90 · Prioritise, track</td><td>Rank feeders by customer-minutes; track
mainfeeder hardening against similar untreated feeders and weather, building on Dominion's published before/after
measure.</td><td><strong>A Power BI programme-tracking report on a scheduled refresh</strong></td></tr>
</table>
<h2>Logistics</h2>
<ul class="tight">
<li>Time, place and format: <span class="placeholder">[you: …]</span></li>
<li>Panel names and roles: <span class="placeholder">[you: …]</span></li>
<li>Work authorisation, if asked: <span class="placeholder">[you: …]</span></li>
<li>Salary, if asked: give a researched range only if pressed. <span class="placeholder">[you: your range]</span></li>
</ul>
"""))

    # ------------------------------------------------------------------ 8 build + numbers to know
    P.append(page("""
<p class="section-no">How it's built</p>
<h1>Built like governed production reporting, and the numbers to know</h1>
<p>Public files land in Snowflake as raw text exactly as published (RAW), are typed and cleaned (STG), and become
facts, dimensions and views (MART) that Power BI imports. Twelve tests run after each load (T1–T12, all pass). A
data dictionary gives every column and measure a business definition, and a decisions log records fourteen choices
(D1–D14), such as which storm types count and which peers to use, made before results were seen. The first check
was reconciliation: 130.2 and 133.0 rebuilt against 130 and 133 reported.</p>
<h2>Numbers to know</h2>
<table>
<tr><th>Number</th><th>What it is</th><th>Source</th></tr>
<tr><td class="k">130 → 133</td><td>Reported 3-year SAIDI ex-MED, 2022–24 → 2023–25 (minutes)</td><td>Annual Report p. 10</td></tr>
<tr><td class="k">130.2 → 133.0</td><td>The same, rebuilt from EIA-861</td><td>EIA-861 / PUDL</td></tr>
<tr><td class="k">136.0 → 144.4</td><td>SAIDI ex-MED, 2022 → 2025, the swap that moves the average</td><td>EIA-861</td></tr>
<tr><td class="k">1.199 → 1.320</td><td>SAIFI 2022 → 2025 (+10%); 2025 the highest of 2013–2025</td><td>EIA-861</td></tr>
<tr><td class="k">113.5 → 109.4</td><td>CAIDI 2022 → 2025, minutes per interruption (−4%)</td><td>EIA-861</td></tr>
<tr><td class="k">1.21 · 4th of 12</td><td>SAIFI 2021–25 vs peers (median 0.96)</td><td>EIA-861 / PUDL</td></tr>
<tr><td class="k">110 · 6th of 12</td><td>CAIDI 2021–25 vs peers (median 105)</td><td>EIA-861 / PUDL</td></tr>
<tr><td class="k">465 → 796</td><td>Storm county-days, 2024 → 2025</td><td>NOAA Storm Events</td></tr>
<tr><td class="k">r = 0.70</td><td>Storm county-days vs SAIDI ex-MED, 2015–2024, n = 10</td><td>NOAA, EIA-861</td></tr>
<tr><td class="k">306.7 vs 144.4</td><td>2025 SAIDI with and without major event days (53% MED)</td><td>EIA-861</td></tr>
<tr><td class="k">+39–41%</td><td>Load, hours ending 1–5 a.m., 2019 → 2025 (1–5 p.m. about +27%)</td><td>EIA-930</td></tr>
<tr><td class="k">+26% · +52%</td><td>Highest and lowest hour of the year, 2019 → 2025</td><td>EIA-930</td></tr>
<tr><td class="k">2019, 2022, 2025</td><td>Years winter set the yearly peak (2026 a near-tie so far)</td><td>EIA-930</td></tr>
<tr><td class="k">2,675,735</td><td>Dominion Energy Virginia customers, 2025</td><td>EIA-861</td></tr>
</table>
<p class="source">One SAIDI minute across 2,675,735 customers is about 2.7 million customer-minutes.</p>
"""))

    # ------------------------------------------------------------------ 9 appendix A
    P.append(page("""
<p class="section-no">Appendix A</p>
<h1>Definitions, and what public data cannot show</h1>
<table>
<tr><th>Term</th><th>Meaning</th></tr>
<tr><td class="k">SAIDI</td><td>Outage minutes per customer per year. SAIDI = SAIFI × CAIDI. Dominion 2025:
1.320 × 109.4 = 144.4 minutes.</td></tr>
<tr><td class="k">SAIFI</td><td>Interruptions per customer per year: how often.</td></tr>
<tr><td class="k">CAIDI</td><td>Minutes per interruption: how long.</td></tr>
<tr><td class="k">Major event days</td><td>Days set aside so one extreme storm does not swamp the trend. IEEE 1366 marks
a day when its SAIDI exceeds a threshold set from the previous five years of daily SAIDI (the “2.5 beta” method).
Dominion reports under its own rule.</td></tr>
<tr><td class="k">ex-MED</td><td>Excluding major event days: the headline series in this brief.</td></tr>
<tr><td class="k">CEMI</td><td>Customers experiencing multiple interruptions: a count from outage records.</td></tr>
<tr><td class="k">Log split</td><td>ln(SAIDI ratio) = ln(SAIFI ratio) + ln(CAIDI ratio); the frequency share is
ln(SAIFI ratio) ÷ ln(SAIDI ratio). 2023 → 2025: 0.125 ÷ 0.158 = 79%.</td></tr>
</table>
<h2>What public data cannot show, and what would answer it</h2>
<table>
<tr><th>Public data limit</th><th>What would answer it (Dominion data, by type)</th></tr>
<tr><td>One number per utility per year (EIA-861)</td><td>Outage records by event, circuit and cause</td></tr>
<tr><td>Storms counted by county, not by line</td><td>Outage records with cause codes and circuit location</td></tr>
<tr><td>Methods differ between utilities</td><td>Dominion's daily SAIDI and its filing method</td></tr>
<tr><td>The DOM zone is wider than the retail territory</td><td>Meter interval data by circuit</td></tr>
<tr><td>No customer identities: load growth cannot be attributed</td><td>Customer class and large-load records</td></tr>
</table>
""", "appendix"))

    # ------------------------------------------------------------------ 10 appendix B
    P.append(page(f"""
<p class="section-no">Appendix B</p>
<h1>The twelve-peer table, sources and tests</h1>
<table>
<tr><th>Utility</th><th>Major-event method</th><th class="r">SAIFI 2021–25</th><th class="r">CAIDI 2021–25</th>
<th class="r">SAIDI 2023–25</th></tr>
{peers_rows()}
</table>
<p class="source">EIA-861 / PUDL, excluding major event days; means of annual values; sorted by SAIFI. Peers chosen by
EIA ID before results.</p>
<h2>Sources</h2>
<table>
<tr><th>Source</th><th>Publisher</th><th>Years</th><th class="r">Rows</th></tr>
<tr><td>EIA-861 Reliability, 2025 final</td><td>EIA</td><td>2025</td><td class="r">977</td></tr>
<tr><td>PUDL EIA-861 reliability</td><td>Catalyst Cooperative</td><td>2013–2024</td><td class="r">24,358</td></tr>
<tr><td>EIA-861 Service Territory</td><td>EIA</td><td>2025</td><td class="r">11,803</td></tr>
<tr><td>NOAA Storm Events</td><td>NOAA NCEI</td><td>2013–2025</td><td class="r">831,288</td></tr>
<tr><td>EIA-930 hourly demand</td><td>EIA</td><td>Jul 2018–Oct 2026</td><td class="r">6,077,232</td></tr>
</table>
<p><strong>Tests after each load (T1–T12, all pass):</strong> no duplicate keys; SAIDI = SAIFI × CAIDI within 2%;
Dominion 2025 equals EIA's published 306.7, 144.4 and 2,675,735 customers; every county mapped; full years; no
duplicate hours.</p>
""", "appendix"))

    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<title>Dominion interview brief</title>"
            f"<style>{css}</style></head><body>{''.join(P)}</body></html>")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    html = OUT / f"{STEM}.html"
    html.write_text(build_html(), encoding="utf-8")
    pdf = pipeline.html_to_pdf(html, OUT / f"{STEM}.pdf")
    import pymupdf
    n = len(pymupdf.open(str(pdf)))
    print(f"pages: {n}")
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=90, grey=grey)
    print("min sizes:", pipeline.pdf_min_font_size(pdf))
    print("fonts:", pipeline.pdf_fonts(pdf))


if __name__ == "__main__":
    main()
