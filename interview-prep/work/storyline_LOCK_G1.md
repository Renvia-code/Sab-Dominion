# Storyline lock (G1a), 2026-11-01 08:05, orchestrator

This file is authoritative for the deck (P1). It locks the **slide list and the claim on each slide**.
Detail, talk-track beats and claim ids stay in `storyline_v0.md`, which B keeps as the working file.
From now on, a slide's claim or order changes only by orchestrator decision, logged in
`MASTER_LEDGER.md` §5. Numbers come from D's `work/data/findings.md` / `reverify_2_2.md` (F-ids) and
R's `research/claims_register.csv`; every one goes into `claims.csv`.

G1 conditions met at 08:00:
- R1 role brief: in.
- EAGLE-I and sector sales: acquired and validated (14/14 checksums, T13–T24 pass).
- SCC reports: attempted, a recorded gap (403).
- D1: done; the 2025 values match the EIA-861 2025 final file.

The question shortlist (G1b) is locked when R5 `top40.md` lands.

## Main slides (8)

| # | Action title (≤ ~15 words; B may tighten, not change the claim) | The claim | Numbers (source) | Visual |
|---|---|---|---|---|
| S1 | Dominion Energy Virginia reliability: what public data shows, and where I'd look first | Title; "Independent analysis of public data"; candidate name; 3 November 2026. No phone, email or logo | none | type only |
| S2 | Outage minutes rose from 130 to 133 because interruptions became more frequent, not longer | The reported 3-year SAIDI ex-MED went 130 → 133. Rebuilt from EIA-861 it is 130.2 → 133.0, so the public data reconciles. The average moved because 2025 (144.4) replaced 2022 (136.0) in the window. Between those years SAIFI rose 10% (1.199 → 1.320) and CAIDI fell 4% (113.5 → 109.4). 2025's SAIFI is the highest of 2013–2025 | F01, findings S2.1–S2.2; C-S2-01 pending R's page check | B's choice per dataviz. It must show both the 2022→2025 split and 2025's SAIFI as the 13-year high |
| S3 | Among 12 peer utilities, Dominion restores at a mid-pack pace; frequency is the gap | 2021–25 means: SAIFI 1.21, 4th highest of 12 (median 0.96); CAIDI 110, 6th of 12 (median 105). Methods differ, so the comparison is indicative | F08 | quadrant scatter, as in v0 |
| S4 | County-days with storms had about 12 times the outage hours of calm days *(08:25, A1 is robust; B may tighten without changing the claim)* | D's A1: on county-days with a storm report, outage customer-hours per 1,000 customers were **11.9×** those of calm days (95% CI 7.9–16.9; 6,108 storm county-days). It holds on non-major days (9.9×), in Dominion-only counties and in every year. Composite figure: the county map (A3, non-major outage events per county, 2015–2025: "where I'd look first"; 4 counties left off for unreliable data, said in a note) with an inset restoration curve (Isaias: 90% restored in 33.5 h; restoration not clearly faster over time, p = 0.07, notes only). On the slide: EAGLE-I counts every utility in a county, and the Dominion-county rule is named. The annual fit r = 0.70 (n = 10) moves to appendix A2 and the notes | D A1, A2, A3 (findings.md); F05 | headline stat + map + inset curve; B lays it out per dataviz |
| S5 | Overnight demand grew faster than afternoon demand, and winter rivals summer for the yearly peak | PJM DOM zone (EIA-930) 2019→2025: hours ending 1–5 a.m. +39–41%, 1–5 p.m. about +27%. Winter set the yearly peak in 2019, 2022 and 2025 (2026 a tie to 30 Oct). Peak hour +26%, lowest hour +52%. Not attributed to data centers (D14) | F10–F12 (D's wording) | 24-hour growth profile and two stat tiles |
| S6 | With Dominion's outage, meter and circuit data, I would start where public data stops | 30/60/90 plan: reconcile → diagnose (cause codes, CEMI, vegetation, AMI last gasp) → prioritise and track. It ends on the Power BI programme-tracking deliverable. Programmes are named exactly as R's sources describe them (08:15: R-035 says the Strategic Underground Program is a separate programme from Grid Resiliency, so follow R). Optional fact: **99.8% of meters** are advanced (AMI) meters (EIA-861 2025; D's F15 counts meters, not customers), so restoration can be measured from meters. Nothing implies inside access | R2 facts; D F15 (AMI 99.8%, time-varying rates 1.0%) | 3-column diagram |
| S7 | Built like governed production reporting: tested, documented, and reconciled to the reported numbers | Sources → Snowflake RAW → STG → MART → tests → Power BI (Import). Tests T1–T24+, data dictionary, decisions D1–D14 + D15+, reconciliation 130.2/133.0. The new sources are named with row counts from D's manifests | docs/01, manifests, test runners | pipeline diagram |
| S8 | Three takeaways: frequency first, reliability net of weather, plan for a new load shape | Three takeaways, each with its number; the experience strip from the resume only (R1 map); a closing line | restated + resume lines | type + strip |

**Robustness and two-sided lines** (speaker notes and the brief, not the slide face):
- From 2023 to 2025, 79% of the change in log terms is frequency.
- 2025 SAIDI is below 2018 (149.6) and 2019 (149.9).
- No 2015–2025 trend is statistically clear (SAIFI p = 0.54, CAIDI p = 0.74, SAIDI p = 0.58): one year is not a trend. *(Corrected 08:15. The 08:05 text mislabelled the p-values; B caught it.)*
- The weather-adjusted SAIDI shows no clear trend since 2015 (+0.34 min/yr, 95% CI −1.41 to +2.09, p = 0.67).

## Appendix (≤ 6)

A1 definitions · A2 the weather fit (n = 10) · A3 major-event days ≈ half of all-event minutes in 2025
(306.7 vs 144.4) · A4 sources and tests · A5 limits (what public data cannot show → what internal data
answers) · A6 **the ten largest outage events in Dominion counties since 2014** (D's A2) if validated,
otherwise the 12-peer table. The peer table always appears in the brief.

## Changes after the lock (orchestrator)

- 08:15 p-values, S4 wording, SUP naming and AMI "of meters" (O-20).
- 08:25 **S4 headline = A1** (above). **Storm county-days 465 → 796 become 464 → 791** once D's D22
  Bedford-city de-duplication lands. Bedford city merged into Bedford County in 2013 and was counted
  twice (38 duplicate county-days, 2013–25). r = 0.70, 145.3, adjusted 133.1 and the Q10 slope are
  unchanged at their stated precision. Use D's re-exported numbers only; until then the v0 values stay
  in v0. **2026 demand cut-off: the hour ending midnight, 29 Oct 2026** (D's E1), for every 2026 figure.

## G2 revision (09:30): this section overrides the tables above where they differ

Triggered by the V3 mock panel (`work/reviews/V3_mock_panel.md`: 47 problems, 7 high; the talk ran
about 10¼ min) and the V2 truth audit (`work/reviews/V2_rulings.md`). Decision O-28. **Main slides, v2:**

| # | Claim (B tightens titles to ≤ ~15 words; the claim is fixed) | Visual | Fixes |
|---|---|---|---|
| S1 | Title, unchanged | type | — |
| S2 | **"Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions."** The 3-year average rose 2.8 minutes. 2025 replaced 2022 in the window; between those years SAIFI +10% and CAIDI −4%, and storm county-days 718 → 791 (D to confirm, post-D22). Dominion's own report attributes the rise "primarily" to storm activity (R-028), and the public data agrees: 2025 sits on the storm line, with no clear trend once storms are counted. | One chart: the hero 130 → 133 with a small "rebuilt from EIA-861: 130.2 → 133.0" tag, plus the 2022 → 2025 change bars. Drop the 13-year SAIFI line (the 1.320 vs 1.303 margin is thin; that goes to notes). | V3 P1–P4. No "because" and no "not longer". |
| S3 | Peers. Claim unchanged (restoration mid-pack; frequency is the gap), but say "**12 large utilities (Dominion and 11 peers)**" and give peer medians **excluding Dominion** (D recomputes). | quadrant scatter | V3 "12 peers are 11" |
| S4 | **County-days with storms had about 12× the outage hours of calm days.** Show the storm and calm levels with the CI, the robustness line (non-major 9.9×; Dominion-only counties; every year) and the all-utilities caveat. | ONE visual: the two levels, or the ratio with its CI. The map and the Isaias inset move to the appendix, the brief and Power BI, with the map **restricted or clearly labelled "all utilities"** and no "start with these counties" instruction. | V3 P11, P12 |
| S5 | **NEW: the Power BI report.** One governed page per question; Import with a folder parameter (adopted) or Import for presentation (D13, public-only); customer-weighted measures; year slicer; Data notes page with tests. | A real screenshot of a report page (B opens it in Power BI Desktop), a small star-schema thumbnail, 2–3 named DAX measures | V3 P29: the job's first duty |
| S6 | How it's built (formerly S7): the pipeline with EAGLE-I named (adopted). Test counts consistent per variant (T1–T31 adopted; T1–T12 public-only). V2 F13–F17 wording. | pipeline diagram | V3 "12 vs 31 tests", "EAGLE-I missing" |
| S7 | First 90 days (formerly S6), humble tone: questions I'd bring, and what I'd build. Ends on Power BI programme tracking. | 3-column diagram | V3 tone |
| S8 | Close: three takeaways matching S2–S4 (a stormier year with no clear underlying trend; frequency is the peer gap, so cause codes are the question; county-level storm views), the resume-true experience strip (V2 F10, F11) and the closing line. Use V3 P30's wording: "I've built a tested Snowflake → Power BI pipeline on public reliability data." | type + strip | V3 P2 (takeaways no longer pull against each other), P30 |

**Every "For Dominion:" line** becomes a humble "Why it matters" line, a question or a reporting
implication, never an instruction to Dominion's planners (V3 P18).

**Appendix (≤ 6):**
1. Definitions (plus the MED share line, 306.7 vs 144.4)
2. The weather fit (n = 10)
3. The load shape (formerly S5), with a humble line such as "I'd add winter and overnight views to reports"
4. Sources and tests
5. Limits
6. The ten largest events + the Isaias curve (adopted) / the peer table (public-only)

**Variants (O-26):** only the deck needs two builds. The brief and the question sheet are one version
each: variant-neutral answers (D13, P18 examples), with the upgrade material in the brief clearly
marked as "depends on adopting the upgrade" for the candidate.

**Timing target:** main talk ≈ 8 minutes, leaving two for interruptions.

## Never on any slide

- Causal language from a correlation.
- "Data centers caused".
- Anything implying access to Dominion systems.
- Power BI or Power Apps "at work" beyond the resume.
- Any pay figure.
- Phone or email.
- Dominion logo or branding.
