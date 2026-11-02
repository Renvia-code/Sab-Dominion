# Storyline v0: the deck (P1)

Written 2026-11-01 07:15–07:35 by B for the G1 lock. Built from brief §2.2 and §3 P1, D's
re-verification (`work/data/reverify_2_2.md`, ids F01–F15), the committed repo outputs, and R1
(`research/role_brief.md`, read 07:30). D's new data (EAGLE-I, sector sales) was not in yet: where a
slide depends on it, the slide says so and gives the fallback the v0 safety-net deck uses. The
orchestrator locks this at G1; after that, slide changes go through the orchestrator.

**Shape:** 8 main slides (title and close included) + 6 appendix slides. 10-minute talk: title
30 s, slides 2–7 about 75 s each, close 60 s, leaving ~1 minute slack.
**Audience:** panel of three (BI/analytics hiring manager, a distribution-reliability engineer, an HR
interviewer). Each slide must make sense to the HR interviewer in plain words and survive the
engineer's follow-up.
**Every main slide:** action title (sentence case, ≤ ~15 words) · one chart or diagram · one line
"What it means for Dominion" · a source line (dataset, years, table or query).
**Claim ids** below (`C-S2-01` …) become rows in `interview-prep/claims.csv`.

**Role fit (R1, `research/role_brief.md`, read 07:30):** most likely the Associate BI Analyst / BI
Analyst posting (Richmond, hybrid) that **supports Grid Resiliency programs** (Strategic Underground
Program, mainfeeder hardening), asking for Power BI, SQL, Excel, Snowflake, governance (business
definitions, metadata, data-quality controls), validation and reconciliation, regulatory and executive
reporting, forecasting and capital planning, and reliability-metrics knowledge (preferred). The arc
stays; S6, S7 and S8 below use the posting's nouns. Words to avoid: anything implying access to
Dominion systems; "data centers caused"; Power BI or Power Apps at work beyond the resume (the resume's
job bullets name Tableau; Power BI is in its summary, skills and this project).

---

## Arc in one breath

Dominion's reported outage minutes went up (130 → 133). The public data reproduces that number,
and splitting it shows the rise came mostly from **customers losing power more often**, not from
slower restoration; against peers, restoration is mid-pack and **frequency is the gap**. Storms
explain part of the year-to-year swing, and county-level outage data shows where and how fast power
came back. Meanwhile **demand is changing shape** (nights and winters). Public data narrows the
question; **Dominion's own outage, meter and circuit data answers it**, and here is what I would do in
the first 90 days. The work is built like a production pipeline, tested and reconciled.

---

## Main slides

### S1. Title
- **Text:** "Dominion Energy Virginia reliability: what public data shows, and where I'd look first."
  Sub-line: "Independent analysis of public data". Name: Saketh Bollina. Date: 3 November 2026.
  Name only (no phone, no email). No logo, no Dominion branding.
- **Visual:** none beyond type; a quiet rule of the five source names along the foot
  (EIA-861 · PUDL · NOAA Storm Events · EIA-930 · DOE EAGLE-I if acquired).
- **Numbers:** none.

### S2. Answer first
- **Action title:** "Outage minutes rose from 130 to 133; the rise came mostly from more frequent interruptions"
- **Claim:** Dominion's rolling 3-year SAIDI ex-MED rose from 130 (2022–24) to 133 (2023–25). Rebuilt
  from EIA-861 the same figures are 130.2 and 133.0, so the public data reconciles to the annual
  report. Underneath, 2023→2025: SAIDI +17%, SAIFI +13%, CAIDI +3%. Because SAIDI = SAIFI × CAIDI,
  79% of the change (log terms) came from frequency, 21% from duration. This is arithmetic, not a
  cause.
- **Visual:** left, the headline "130 → 133" as typography with the reconciliation line; right, a
  3-bar chart of % change 2023→2025 (SAIDI, SAIFI = subject, CAIDI) with the identity
  "1.133 × 1.033 = 1.171" under it. Plain-word definitions under the bars (how often / how long per
  interruption / minutes per customer).
- **What it means for Dominion:** "The first question is what is making interruptions more frequent,
  before how to restore faster."
- **Source line:** "EIA-861 2025 final and PUDL 2013–2024, Dominion Energy Virginia (EIA 19876), ex-MED.
  mart.FCT_RELIABILITY; 3-year mean of annual values. Dominion 2025 Annual Report p. 10 (130, 133)."
- **Numbers and sources:**
  | id | Text | Source |
  |---|---|---|
  | C-S2-01 | 130 → 133 (reported) | Dominion 2025 Annual Report p. 10 (R to confirm the page in the PDF); repo docs/05 |
  | C-S2-02 | 130.2 → 133.0 (rebuilt) | F01: mart.FCT_RELIABILITY, query F01 |
  | C-S2-03 | SAIDI 123.3 → 144.4, +17% | F02 |
  | C-S2-04 | SAIFI 1.165 → 1.320, +13% | F02 |
  | C-S2-05 | CAIDI 105.9 → 109.4, +3% | F02 |
  | C-S2-06 | 79% frequency / 21% duration | F03 (log decomposition, sql/03 Q1b) |
- **Engineer's likely follow-up:** "Rolling averages overlap" → yes, 2023 and 2024 are in both; the
  annual values carry the signal (C-S2-03).
- **Open until G1 (orchestrator, 07:40): base-year risk.** The 3-year average moves 130.2 → 133.0
  only because 2025 (144.4) replaces 2022 (136.0) in the window; 2023 (123.3) is the low year, so a
  2023 base flatters the rise. D is decomposing 2022→2025 as well as 2023→2025, plus the 2015–2025
  SAIFI and CAIDI trend. v0 is built as drafted; the speaker notes keep one line for "what drives the
  3-year change" (2025 replacing 2022). G1 locks whichever framing holds under both bases.

### S3. Frequency versus duration, against peers
- **Action title:** "Among 12 peer utilities, Dominion restores at a mid-pack pace; frequency is the gap"
- **Claim:** 2021–25 averages: Dominion SAIFI 1.21 (4th highest of 12; peer median 0.96), CAIDI 110
  minutes (6th of 12; median 105). Reporting methods differ (Dominion uses its own major-event rule,
  most peers IEEE 1366), so the ranking is indicative.
- **Visual:** quadrant scatter, x = SAIFI 5-yr, y = CAIDI 5-yr, 12 dots; Dominion in subject blue and
  labelled; peers in context grey (labels only for the three nearest Dominion's quadrant); thin
  solid median lines in muted grey, labelled "peer median". Method caveat in the subtitle.
- **What it means for Dominion:** "Preventing interruptions is where the gap to peers is; restoration
  speed is already near the middle." (frames the 90-day plan; no causal claim)
- **Source line:** "EIA-861 / PUDL 2021–2025, ex-MED; 12 large IOUs in PJM and the Southeast chosen by
  EIA ID before results (decision D10); means of annual values (DAX SAIFI 5yr, CAIDI 5yr)."
- **Numbers and sources:** C-S3-01 SAIFI 1.211 rank 4/12, median 0.964 (F08); C-S3-02 CAIDI 110.4
  rank 6/12, median 105.0 (F08); C-S3-03 12 peers (docs/04 D10); C-S3-04 each peer's point (F08 query
  output, snapshot `work/charts/s3_peer_quadrant.csv`); optional C-S3-05 3-yr SAIDI 4th of 12 (F07).
- **Dependency:** none (repo data). Optional: R1 may show the role is reporting-heavy → keep the
  method caveat prominent.

### S4. Weather, and where the outages were
- **Action title (v1, if EAGLE-I lands):** "More storm days, more outage minutes; county data shows
  where power went out and how fast it came back" (trim to ≤ 15 words after D's numbers)
- **Action title (v0 fallback):** "Years with more storm days had more outage minutes (r = 0.70 over
  ten years)"
- **Claim (both):** storm county-days rose from 465 (2024) to 796 (2025); over 2015–2024 they
  correlate r = 0.70 with SAIDI ex-MED (n = 10, R² 0.48). The fit predicted 145.3 for 2025 against
  144.4 actual, a check on one year, not a forecast. Association, not cause.
- **Claim (v1 adds):** EAGLE-I county outage data (15-minute customers-out, ORNL/DOE) for the counties
  picked by D's Dominion-county rule: a choropleth of outage customer-hours (or non-major outage
  events per 10,000 customers) and the restoration curve of one major event (share of peak restored
  by hour since peak). **State on the slide:** EAGLE-I counts every utility in a county, not only
  Dominion; the county rule is D's (named in the source line).
- **Visual:** v1: map (sequential blue, 5 classes) + one restoration curve (subject line, 50/90/99%
  marks). v0: scatter of storm county-days vs SAIDI ex-MED, 2015–2024 grey dots, 2025 blue dot
  labelled "2025: predicted 145.3, actual 144.4", fit line in muted grey.
- **What it means for Dominion:** "Judge reliability trends net of weather, and plan storm crews by
  county exposure, not system averages." (inference; the speaker note says so)
- **Source line (v0):** "NOAA Storm Events 2015–2025 (line-risk types, decision D5), storm county-days
  in Dominion's Virginia counties (EIA-861 service territory); EIA-861 ex-MED. mart.STORM_INDEX,
  V_STORM_VS_SAIDI; OLS fit 2015–2024 (D6)."
- **Numbers and sources:** C-S4-01 465 → 796 (F04); C-S4-02 r = 0.70, n = 10, R² 0.48 (F05);
  C-S4-03 145.3 vs 144.4 (F05); C-S4-04 scatter points (data/output/storm_vs_saidi.csv, rebuilt by D
  from raw NOAA in F04/F05); v1 C-S4-1x from D's findings.md A1–A3 (county rule, peak customers out,
  hours to 50/90/99%).
- **Dependency:** D2.1/D4/D5 (EAGLE-I county table, Dominion-county rule, one event's restoration
  curve, ten-largest-events table). If not validated by G1, v0 stays and EAGLE-I goes to the
  appendix or the Power BI pages.

### S5. Demand is changing shape
- **Action title (orchestrator, 07:40: no "now", winter also peaked in 2019):** "Overnight demand
  grew faster than afternoon demand, and winter rivals summer for the yearly peak"
- **Claim:** PJM DOM zone (EIA-930), 2019→2025, **lead with the band**: average load in the hours
  ending 1–5 a.m. rose 39–41%; in the hours ending 1–5 p.m. about 27% (never the single 4 a.m. hour
  alone). Winter set the year's peak in 2019, 2022 and 2025, and 2026 is a near-tie so far (25,413 vs
  25,384 MW, to 30 Oct). The highest hour rose 26% and the lowest 52%. Round-the-clock growth is
  consistent with large constant loads; the data does not identify data centers (decision D14).
- **Visual:** v1: 24 columns of % growth by hour of day, 2019→2025 (night hours subject blue, others
  context grey), with two stat tiles at the side: "Winter set the peak in 2019, 2022, 2025" and
  "Lowest hour +52%". v0: winter vs summer peak by year 2019–2026 (paired columns: winter subject
  blue, summer gold, both direct-labelled; 2026 marked "to 30 Oct"), with the night/afternoon band
  (1–5 a.m. +39–41%, 1–5 p.m. about +27%) as stat tiles.
- **What it means for Dominion:** "Planning that assumes quiet nights and summer-only peaks needs
  revisiting: less overnight slack, and winter readiness matters as much as summer."
- **Source line:** "EIA-930 hourly demand, PJM DOM zone (wider than Dominion's retail territory),
  Jul 2018–Oct 2026; mart.DOM_LOAD_PROFILE, DOM_LOAD_ANNUAL; winter = Dec–Feb, summer = Jun–Aug."
- **Numbers and sources:** C-S5-01 hours ending 1–5 a.m. +39–41%, 1–5 p.m. about +27% (F11, band
  wording per D and the orchestrator); C-S5-02 winter peak
  years 2019, 2022, 2025, 2026 tie (F12; **the brief's "2022, 2025 and 2026" is incomplete**);
  C-S5-03 peak +26% (19,803 → 24,957 MW), floor +52% (7,167 → 10,903) (F10); optional C-S5-04
  commercial sales +65% on +8% customers (F14), C-S5-05 47 of the top 50 hours (Jul 2018–Dec 2025)
  fell in 2025 (F13, wording per D).
- **Dependency:** D's hour-of-day table (24 rows) and hour × month heatmap (v1). v0 uses
  `data/output/dom_annual.csv` (committed) and F10–F12.

### S6. What I'd do with Dominion's own data in the first 90 days
- **Action title:** "With Dominion's outage, meter and circuit data, I would start where public data
  stops"
- **Level (orchestrator, 07:40):** practical, Associate / BI Analyst level: learn, reconcile, build,
  track. No strategy talk; end on the Power BI programme-tracking deliverable (posting duty 1).
- **Claim (plan, no numbers needed):** a 30/60/90 diagram.
  - Days 1–30, **learn and reconcile:** learn the outage (OMS), meter (AMI) and circuit (GIS) data and
    how reliability is reported to the SCC; rebuild one year's SAIDI, SAIFI and CAIDI from source
    records and reconcile them to the filed figures, the way the public rebuild matched 133.0.
  - Days 31–60, **build:** governed views of SAIFI by circuit and cause code, customers with
    repeated interruptions (CEMI), and restoration times measured from AMI "last gasp" and restore
    signals; business definitions and data-quality checks written down as they are built.
  - Days 61–90, **track:** a Power BI programme-tracking report for Grid Resiliency work (the
    publicly described Strategic Underground Program and mainfeeder hardening): treated circuits'
    SAIFI and CEMI before and after, customer-minutes avoided per dollar, refreshed on a schedule
    rather than by hand.
- **Visual:** three-column diagram (phase · what I'd do · data · deliverable), the last column ending
  in "Power BI programme-tracking report"; a thin strip under it: "public data shows the trend →
  internal data shows the circuit".
- **What it means for Dominion:** "Each step turns a system-level trend into a circuit-level view the
  programme team can act on."
- **Source line:** "Plan; internal data named by type only. No Dominion internal data was used in this
  analysis."
- **Numbers:** optional C-S6-01 "one SAIDI minute ≈ 2.7 million customer-minutes" (2,675,735 customers
  × 1 minute; F06 customers; arithmetic, D A6).
- **Dependency:** R1 (role tools and duties) to tune the wording; R3 (domain primer) to check terms
  (CEMI-n, last gasp, cause codes). Never implies inside access.

### S7. How I built it
- **Action title:** "Built like governed production reporting: tested, documented, and reconciled to
  the reported numbers"
- **Claim:** public sources → Snowflake RAW (as published, all text) → STG (typed, cleaned) → MART
  (facts, dimensions, views) → tests → Power BI (Import). Governance in the posting's words:
  data-quality controls (tests T1–T12, + T13+ for new sources), business definitions and metadata (the
  data dictionary, docs/02), a decisions log (D1–D14 + new), validation and reconciliation to the annual
  report (130.2 / 133.0 vs 130 / 133), every chart reproducible from a script and a data snapshot.
- **Visual:** pipeline diagram left to right, with row counts under each source and three governance
  badges under the mart (tests, dictionary, decisions).
- **What it means for Dominion:** "The same discipline (reconcile first, test every load, document
  every decision) is what I'd bring to Dominion's reporting."
- **Source line:** "Repo dominion-reliability-review: sql/01–08 (+ new), docs/02–04, scripts/;
  row counts docs/01_sources.md."
- **Numbers and sources:** C-S7-01 NOAA 831,288 rows (docs/01, data/raw/README.md); C-S7-02 EIA-930
  6,077,232 rows (72,864 DOM) (docs/01); C-S7-03 EIA-861 2025 977 rows, PUDL reliability 24,358
  (docs/01); C-S7-04 tests T1–T12 pass (run_local_duckdb.py T1–T6; D's rebuild T7–T12, reverify
  header); C-S7-05 reconciliation 130.2/133.0 (F01); new sources' rows from D's manifests.

### S8. Close
- **Action title (v0):** "Three takeaways: look at frequency first, read reliability net of weather,
  plan for a new load shape"
- **Content:** three numbered takeaways, each one line with its number (+13% SAIFI; r = 0.70 but
  association only; overnight hours +39–41% / winter peaks). Then one fit line (R1 §7.4, every word
  traceable):
  "I build governed Snowflake → Power BI reporting, and I've already started learning your
  reliability data." Then one strip, "How my experience maps", from the resume only (rephrased, no
  new facts; locators per R1 §5):
  - Snowflake pipeline across policy, claims and billing schemas, 20M+ rows (Mercury bullet 1) → this
    mart.
  - Root cause analysis joining claims, policy and vendor data (Mercury bullet 2) → SAIFI drivers by
    cause code.
  - Validation, reconciliation and QA owned for a pilot (Mercury bullet 3) → tests and reconciliation.
  - Documentation with metadata and business definitions (Mercury bullet 6) → data dictionary and
    decisions log.
  - Partnering with operations and IT on requirements (Mercury bullet 5) → working with reliability
    engineers and programme teams.
  Never "Power BI at work" (R1 gap G3); Power BI evidence is this project. Practical and at
  Associate / BI Analyst level (orchestrator, 07:40). Nothing about visas or work authorisation in
  the deck; in P2/P3 that answer is `[you: …]` only.
- **Visual:** three takeaway blocks (number set as typography) + the experience strip.
- **What it means for Dominion:** the closing line "I would like to do this with your data."
  (the candidate may soften it).
- **Numbers:** restated from C-S2-04, C-S4-02, C-S5-01/02; resume facts C-S8-01… (source: resume
  line, e.g. "Mercury Insurance, bullet 1: 20M+ rows").
- **Dependency:** R1 role brief (requirements → resume lines). If R1 shows a different emphasis (for
  example forecasting or regulatory reporting), the strip reorders, the arc does not change.

---

## Appendix (6)

| # | Action title | Visual | Numbers (source) |
|---|---|---|---|
| A1 | "Definitions: SAIDI = SAIFI × CAIDI, and major event days are set aside by rule" | formula diagram + plain words; IEEE 1366 2.5-beta method in one line; Dominion files under its own rule (EIA "Other") | definitions per R3 `domain_primer.md` (IEEE 1366-2022) |
| A2 | "The weather fit is a check on one year, not a forecast" | scatter with fit line, n = 10, r = 0.70, R² 0.48, slope 0.051 min per county-day, 2025 out of sample | F05, docs/04 D6 |
| A3 | "Major-event days were about half of all-event outage minutes in 2025" | stacked columns by year, ex-MED vs major-event-day minutes (difference of EIA's two series, not a NOAA attribution) | 306.7 vs 144.4, 53% (F06); per-year values `data/output/storm_vs_saidi.csv` |
| A4 | "Every number traces to a public source and a tested query" | source table: publisher, years, grain, rows, licence; tests list | docs/01, sql/04–06 tests, D's manifests |
| A5 | "What public data cannot show, and what would answer it" | two-column table: limit → internal data that answers it | DOM zone ≠ retail territory; EAGLE-I = all utilities in a county; EIA-861 ≠ SCC filing method; annual points; no customer identities (D14) |
| A6 | "The twelve-peer comparison, with each utility's reporting method" | table: utility, region, method, SAIDI 2015–17, 2023–25, change, SAIFI 5yr, CAIDI 5yr; Dominion row tinted | F07/F08 query outputs |

Optional swap (only if R1 or D make it stronger): A6 → "Ten largest outage events since 2014 in
Dominion counties" (D's A2), keeping the peer table in the brief.

---

## Numbers the brief stated that need different wording (from D's F11–F13)

1. **Night growth:** lead with the band (orchestrator, 07:40): "hours ending 1–5 a.m. rose 39–41%;
   hours ending 1–5 p.m. about 27%". Not "night hours rose 41%", and not the single 4 a.m. hour alone
   (looks cherry-picked).
2. **Winter peaks:** winter beat summer in **2019**, 2022 and 2025; 2026 is a 29 MW tie to 30 Oct.
   The existing Power BI title ("higher in 2022, 2025 and 2026") must change too.
3. **Top 50 hours:** "of the 50 highest hours in the EIA-930 record (July 2018 to 31 Dec 2025), 47 fell
   in 2025". Not all-time; the record starts July 2018.
4. **Time-varying rates:** not yet verified (F15 partial). Leave out of v0; v1 only if D verifies it
   from the EIA-861 Dynamic Pricing file.

## Talk-track beats (full 60–80 s notes are written into the PPTX in B2)

- S2: "Dominion reported 133, up from 130. I rebuilt that from public EIA data and got 130.2 and
  133.0, so the data matches. Then I split it: SAIDI is how often times how long. Frequency rose
  13%, duration 3%: about four-fifths of the rise is frequency."
- S3: "Against twelve large peers chosen before I looked at results, Dominion restores in the middle
  of the pack but has the fourth-highest frequency. Methods differ, so it's indicative."
- S4: "Storms matter: more storm days, more outage minutes, r = 0.70 but only ten points, so it's a
  check, not a model. [v1: county data shows where and how fast.] It cannot say which circuits."
- S5: "Demand is changing shape: the small hours grew about 40%, afternoons about 27%, and winter
  rivals summer for the yearly peak. I don't attribute it to data centers; the data can't see
  customers."
- S6: "Public data narrows the question; your data answers it. First month reconcile, second
  diagnose, third prioritise."
- S7: "Built like production: raw, staged, mart, tests, dictionary, decisions, reconciled to the
  annual report."
- S8: three takeaways; experience map; close.

## What the safety-net v0 deck uses (by G1)

S1–S3, S6–S8 as above; S4 = v0 fallback (NOAA scatter); S5 = v0 (seasonal peaks + stat tiles);
appendix A1–A3 and A5 (A4 and A6 tables from repo docs). Every number from F01–F14 or the committed
`data/output/` files. No EAGLE-I, no new D data, no R facts beyond the repo's.
