# The 25 hardest questions, with answers

*Agent R · 2026-11-01 09:41 · the full study version (print version: `research/hard25_print.md`). Written to the G2 storyline (`work/storyline_LOCK_G1.md`, "G2 revision") and the V2 rulings (`work/reviews/V2_rulings.md`).*

**How the 25 were chosen**
- Start: V3's mock panel (`work/reviews/V3_mock_panel.md`): E1–E9, B1–B9, H1–H7.
- Kept: all seven of the brief's required questions (MASTER_PROMPT §3), marked **●**. Four were already in V3's list (E6, E3, B1, E4); three are new.
- Merged, to make room for the three:
  - E1 + E2: same slide; the G2 title no longer says "not longer"
  - B3 + B4: reconciliation and QA; v2 fixes the count mismatches
  - B5 + B9: governance and regulatory reporting test the same claim

**How to use an answer (60–90 seconds spoken)**
- Each answer has three parts: **Claim** first, one or two pieces of **Proof**, then the honest **Limit**, answered in the same breath.
- The bullets are cues to expand aloud, not a script. Q24 is the one exception.
- **(adopted variant):** the answer depends on adopting the repo upgrade (EAGLE-I county data, tests T13–T31, decision D22).
- **Public-only:** the line to use if you don't adopt the upgrade.
- **`[you: …]`:** only you can fill it; the resume doesn't say.

**Locators**

| Locator | Points to |
|---|---|
| C-… | `claims.csv` |
| R-… | `research/claims_register.csv` |
| D1–D22 | `docs/04` decisions |
| P1–P34 | `docs/03` data-quality log |
| T1–T31 | tests |
| N-… | numbers not yet in `claims.csv`, listed at the end |
| "resume: Mercury b2" | the resume, that role, bullet 2, paraphrased (never quoted) |

---

## Distribution-reliability engineer

### Q1 ● · Weather fit · *"Your weather fit has ten points. What's the interval on r, what was the 2025 prediction interval, and why start in 2015?"*
(V3 E6)
- **Claim:** Agreed, ten points is thin. That's why the fit is a check in the appendix, not the headline.
- **Proof:**
  - **The fit:** r = 0.70 on 2015–2024 (t = 2.752 on 8 df, p = 0.025), but the 95% interval for r runs from 0.12 to 0.92 [C-S4-15].
  - **2025 held out:** the fit predicted 145.3 and the actual was 144.4 [C-S4-03]. That is inside a wide band (about 122–168) [N-1]: consistent with the fit, not proof of it.
  - **Why 2015:** Dominion's outage recording became automated in 2015, which shifts the level. I fit from there (decision D6; EIA-861 flag [N-2]).
- **Limit:** Say "can't tell", not "no trend": once storms are counted, the remaining slope isn't distinguishable from zero.
- **Variants:**
  - (adopted variant) Weather-adjusted SAIDI moves +0.3 min a year, with a 95% range of −1.4 to +2.1 [C-S4-06]. Storm county-days 464 → 791 (D22) [C-S4-01]. The stronger evidence is the county-day comparison (Q5).
  - Public-only: "r = 0.70 on ten years: a sanity check". Storm county-days 465 → 796. No t, p or intervals. "No clear trend once storms are counted", in words.

### Q2 ● · Major event days · *"What's a major event day, and why exclude it? What's Dominion's rule, and what does it do to your peer ranking? How would you compare Dominion and FPL fairly?"*
(V3 E3 with the brief's MED question)
- **Claim:** A major event day (MED) is a day so far above normal that it would swamp the year. Excluding MEDs shows everyday performance; storm days get judged separately, as storm response.
- **Proof:**
  - **The 2.5-beta rule:** take five years of daily SAIDI and log the values (zero days can't be logged, so they drop out). The threshold is T = e^(α + 2.5β), with α the mean and β the SD of the logs. Days above T in the next year are MEDs [R-070].
  - **What exclusion hides:** in 2025, MEDs were 53% of all-event minutes (306.7 vs 144.4) [C-A3-01, C-A3-02].
  - **Dominion's method:** Dominion reports to EIA under its own method ("Other") every year; 10 of the 12 utilities in the set use IEEE 1366 [N-2, N-5].
  - **A check that needs no MED rule (all events, 2021–25):**
    - SAIFI: Dominion is 6th of 12 (1.53 against a median of 1.41 for the other eleven). Excluding MEDs it is 4th (1.21 against 0.93) [N-3, C-S3-01].
    - Minutes: on all events Dominion is 9th of 12, with hurricane-hit peers at the top [N-11; the hurricane reading is an inference].
- **Limit:** "I don't know Dominion's written MED rule. EIA lists it as 'Other'; I'd ask the reliability team for the definition." The ranks depend on the rule, so I call them indicative.
- **FPL:** different climate and construction standards. Compare like with like (all events, same years), call it indicative, and add no comment on the merger.

### Q3 ● · County data · *"Your county outage data covers every utility in the county, not only Dominion. Whose minutes are those? Would you send a hardening crew on that map? And 90% of what, for Isaias?"*
(V3 E4) (adopted variant)
- **Claim:** Right. EAGLE-I counts every utility's customers in a county. It isn't Dominion's SAIDI, and I wouldn't target work with it.
- **Proof:**
  - **The county rule:** a Dominion county is one where EIA-861 lists Dominion. That gives 103 counties and cities, 33 of them served by Dominion alone (D15). The storm result holds in the Dominion-only counties (19.9×) [C-S4-09].
  - **EAGLE-I's limits:**
    - 15-minute snapshots scraped from outage maps
    - blank readings are failed runs, kept as missing, never zero (P20)
    - four counties left out (P26, P27)
    - no count of separate interruptions, so no SAIFI
  - **Isaias:** 90% of the peak number of customers out, across all utilities, net of new outages, timed from the peak [C-S4-12]. Utilities report "% of affected customers restored", which is a different curve.
- **Limit:** For targeting I'd use Dominion's outage records by feeder. The county view is context only.
- **Public-only:** the public project has no county outage data. The same caveat applies to the storm index: NOAA reports in the counties Dominion serves, which other utilities serve too.

### Q4 · Is there anything to explain? · *"130 to 133 is 2.8 minutes. Is there anything to explain? Did interruptions get more frequent or longer, and why does your appendix use a different base year?"*
(V3 E1 + E2)
- **Claim:** 2025 was a stormier year with more interruptions. On public data there's no clear underlying trend.
- **Proof:**
  - **The 2.8 minutes:** the 3-year average moved because 2025 (144.4) replaced 2022 (136.0): (144.4 − 136.0) ÷ 3 = 2.8 [C-S2-03]. Single years have ranged from 117 to 150 since 2015 [C-S4-05], so 2.8 is small.
  - **2022 → 2025:**
    - SAIFI +10% and CAIDI −4% [C-S2-05, C-S2-07]
    - storm county-days 718 → 791 [C-S2-16]
    - 2025 sits on the storm line: fit 145.3, actual 144.4 [C-S4-03]
    - Dominion's own report says the rise was "primarily due to increased storm activity" [C-S2-15]
  - **Base year:** the right comparison is 2022, the year that left the window. Against 2022, frequency explains more than all of the rise. Against 2023, both rose: SAIFI +13%, CAIDI +3%, 79% from frequency [C-S2-10, C-S2-11].
- **Limit:** CAIDI is a ratio. Extra short interruptions pull it down, and automation such as FLISR can push it up, so it isn't a pure restoration-speed measure. Settling the question needs interruption-level durations by cause.
- **Variants:**
  - (adopted variant) No 2015–2025 trend is statistically clear: SAIFI p = 0.54, CAIDI p = 0.74, SAIDI p = 0.58 (`scripts/trend_tests.py`) [C-S2-13].
  - Public-only: storm county-days 723 → 796; say "no clear trend" in words.

### Q5 · The 12× · *"Isn't your 12× partly circular, since storm reports get logged because trees and wires came down? And what's the unit behind the 95% interval?"*
(V3 E5) (adopted variant)
- **Claim:** Partly, yes. It's an association, inflated by how storm reports are made. I don't claim cause.
- **Proof:**
  - **The levels:** a storm county-day averaged 333 customer-hours per 1,000 customers and a calm one 27.9, so 11.9× (95% CI 7.9–16.9) [C-S4-08, N-6].
  - **The interval:** 2,000 bootstrap resamples of whole days, so county-days hit by the same storm move together. The unit is the day, not the county-day [findings A1].
  - **Robustness:** it holds on non-major days (9.9×), in Dominion-only counties (19.9×) and in every year [C-S4-09].
  - **6,108 vs 6,530:**
    - 6,108 counts storm county-days with complete EAGLE-I readings in 99 counties.
    - 6,530 counts every NOAA storm county-day in 103.
    - The gap of 422 matches those two filters (114 of it in 2025, when EAGLE-I collection often failed) [N-7].
- **Limit:** A cleaner test would use weather measured independently of damage, such as station wind gusts. That is a next step, not a claim. Storms that start at night count the next day as calm, which biases the ratio down [findings A1].
- **Public-only:** "The public project has the annual version: storm county-days against SAIDI, r = 0.70 on ten years. Same caveat: storm reports are often based on damage."

### Q6 · Meters · *"You'd time restoration from meter 'last gasps'. What does a last gasp tell you, and what happens to them in a big storm? With 99.8% smart meters, how do you know 2025's high SAIFI isn't a measurement change?"*
(V3 E7)
- **Claim:** A last gasp marks when an outage *starts*, not when it ends. From public data I can't rule out a measurement effect, so I'd check before calling anything worse.
- **Proof:**
  - **Meters:** 99.8% of Dominion Virginia's meters are AMI (2025) [C-S6-01].
  - **Restoration:** knowing when power came back needs the meter's restore message or a ping. The outage management system stays the system of record for reported indices.
  - **Big storms:** collectors and backhaul can lose power, so last gasps go missing. AMI is a cross-check, not a replacement.
  - **Measurement changes happen in this data:** recording became automated in 2015, which is why the weather fit starts there (D6) [N-2].
  - **The checks I'd run:**
    - compare the AMI roll-out timeline with SAIFI
    - read EIA-861's flag for whether outages are recorded automatically
    - compare circuits before and after their meter cut-over
- **Limit:** Public data can't separate better detection from a worse grid for 2025. I haven't checked the meter roll-out timeline.

### Q7 · Cause codes · *"Your plan mentions SAIFI by cause, but there's no cause analysis in this deck. What do you expect in our cause codes, vegetation especially, and what will go wrong with the data?"*
(V3 E8)
- **Claim:** Right, it needs your outage records. It's a 30–60-day deliverable; public data can't show cause.
- **Proof:**
  - **Expected cause families:** vegetation, equipment, lightning and weather, animals, vehicles and the public, unknown. Split blue-sky days from storm days, and use CEMIn to find customers with repeat outages [primer A1].
  - **Vegetation:** Dominion trims distribution lines on cycles of about four to five years, and nearly all neighborhood lines on four [R-076]. My first question: how much storm-day vegetation comes from outside the trimmed zone?
  - **Data traps:**
    - crews code the cause when they close the job, so coding varies
    - one device event affects many customers
    - the share coded "unknown" is itself a data-quality measure
- **Limit:** I haven't worked with utility cause codes. I'd agree the definitions with engineering before charting anything.

### Q8 · Mainfeeder hardening · *"We pick the worst feeders and report outage minutes down by about a third. If you built the tracking report, how would you know it's the program and not regression to the mean or a mild year?"*
(V3 E9)
- **Claim:** A plain before-and-after will overstate it, because feeders are chosen for a bad recent history. I'd build the comparison into the report.
- **Proof:**
  - **Dominion's selection rule:** groups of at least 500 customers whose SAIDI is more than 2 minutes worse, over the last five years [C-S6-03].
  - **Reported results:**
    - −32% outage minutes on feeders hardened for 12 months or more (as of 30 Nov 2023) [C-S6-02]
    - −44% average annual outage time in hardened areas (June 2026 release) [R-013]
  - **The design:**
    - a multi-year pre-period
    - comparison feeders matched on pre-period SAIDI and SAIFI, exposure and region
    - difference-in-differences with storm normalization and the same MED treatment
    - staggered completion dates
    - results reported with intervals
  - **My experience:** the A/B test at Mercury, where the analytics manager and I agreed the sample size and the significance level up front [resume: Mercury b4].
- **Limit:** Frame it as making a good result harder to challenge at the regulator, not as doubting it.

### Q9 ● · Why EIA · *"Why public EIA data and not Dominion's SCC filings?"*
(brief)
- **Claim:** EIA-861 is public, consistent across utilities and years, and it reproduces Dominion's own reported numbers.
- **Proof:**
  - **What it is:** the federal annual survey. Distribution utilities nationwide file the same form, by state, with and without major event days, under IEEE 1366 or their own method [R-072].
  - **It reconciles:** from Virginia data it reproduces the reported 130 and 133 to the minute (130.22, 133.01) [C-S2-17].
  - **It allows peers:** a peer comparison is possible, with methods stated [C-S3-06].
  - **The SCC filings:** each investor-owned utility files an Annual Reliability and Tree Trimming Report [R-019]. The docket site blocked automated access, so I didn't use them. The SCC's report to the General Assembly shows the indices only as charts, with major weather events left out [R-020; RD916 p. 12].
- **Limit:** Utilities report under IEEE 1366 or their own method, and Dominion uses its own, so peer ranks are indicative. With access, the filed SCC reports are the first thing I'd reconcile against.

### Q10 ● · Data centers · *"Did data centers cause the demand growth?"*
(brief)
- **Claim:** Public data can't show that, and I don't claim it.
- **Proof:**
  - **The load shape:** overnight load in the DOM zone grew 39–41% from 2019 to 2025, against about 27% in the afternoon [C-S5-01]. Winter set the yearly peak in 2019, 2022 and 2025 [C-S5-02].
  - **Sales:** commercial sales rose 65% from 2013 to 2025 on 8% more commercial customers [C-S5-07].
  - **Fit with Dominion's account:** that shape fits large round-the-clock loads. Dominion reports 11 data centers (744 MW) connected in 2025 and over 54 GW in contracting stages [R-040, R-054].
- **Limit:** The zone is wider than Dominion's territory, and EIA-861 doesn't identify customers. Attribution needs customer-class or meter data (decision D14).

## BI / analytics hiring manager

### Q11 ● · The model · *"Walk me through your model and the year slicer. How do you compute three-year SAIDI, and how would you roll SAIDI up from regions to the system?"*
(V3 B1)
- **Claim:** It's a small star schema with customer-weighted measures, and every number on a page comes from a measure.
- **Proof:**
  - **The tables:** the fact table FCT_RELIABILITY has one row per utility, state and year (customers, customer-minutes and customer interruptions, with and without MEDs). It joins many-to-one to DIM_UTILITY on UTILITY_KEY. The other tables are keyed by year or hour and have no relationships (docs/06).
  - **The year slicer:** it reads a disconnected 'Dashboard Year' table. Measures take SELECTEDVALUE (2025 if nothing is picked) and CALCULATE the base measure for that year, so the slicer drives the cards without filtering the model.
  - **Three-year SAIDI:** compute the customer-weighted SAIDI for each year, then take the mean of the three (AVERAGEX over years). That is Dominion's convention, which is why 130.2 and 133.0 reconcile [C-S2-02; docs/05].
  - **Roll-up:** within a year, divide total customer-minutes by total customers. Don't average regional SAIDIs. CAIDI = SAIDI ÷ SAIFI at the rolled-up level (docs/05).
- **Limit / storage mode:** I developed it in DirectQuery against Snowflake and switched to Import for presentation (D13).
  - (adopted variant, once you've applied the Power BI guide) It imports from a folder of CSVs through a folder-path parameter, so it opens offline.
  - Public-only: "Import for presentation; DirectQuery in development (D13)."
- **Bring:** a printed report page and the model view.

### Q12 · Power BI at work · *"Your job bullets show Tableau; Power BI is only in your summary and skills. Where have you used Power BI at work? And what have you built in Power Apps?"*
(V3 B2)
- **Claim:** `[you: the exact truth about professional Power BI use]`. If it's only this project, say so plainly, then show depth.
- **Proof:**
  - **At work:**
    - the board's investment dashboard, rebuilt in Tableau, at the Life Initiative [resume: Life Initiative b1]
    - Tableau account dashboards at Cofoods [resume: Cofoods BD b1]
    - Snowflake SQL at Mercury [resume: Mercury b1]
  - **Power BI depth in the project:** the model, customer-weighted DAX measures, the year slicer, and a Data notes page with the tests (Q11).
  - **Transfer:** it's the same job: governed definitions, a model, a refresh, one page per question.
- **Limit:**
  - **Power Apps** isn't on the resume. Say "Not in production" and `[you: any real exposure]`. Offer a 30-day plan: a small exceptions or field-update form feeding the report. Never claim it.
  - **SharePoint** is in the skills line only: `[you: what you've done with it]`.

### Q13 · Reconciliation · *"You matched 133.0 to 133. What did that prove, and which values did you check? And what tells me your QA catches mismatches?"*
(V3 B3 + B4)
- **Claim:** It proves I'm measuring what Dominion reports, with the same definitions and filters. It doesn't prove the underlying data is true.
- **Proof:**
  - **The 12 values** (`data/output/reconciliation.csv`) [C-S7-11]:
    - the two 3-year averages against the annual report (130.2 vs 130; 133.0 vs 133)
    - nine 2024–25 values against EIA's own files: SAIDI, SAIFI and CAIDI ex-MED, all-events SAIDI, and 2025 customers
    - 2025 commercial sales
  - **What it confirms:**
    - the right utility and state row (Virginia)
    - the MED flag
    - the averaging convention (mean of annual values)
    - the vintage (2025 final)
    - the customer basis
  - **QA:** tests run after every load [C-S7-05, C-S7-10], and the reconciliation sits on the report's Data notes page.
- **Limit:** It's a check of definitions, not an independent measurement. At Dominion a real reconciliation would run from outage events to daily SAIDI to the filed figure, with a written bridge for MEDs, planned outages, momentaries and customer counts.
- **Variants:**
  - (adopted variant) "12 of 12"; tests T1–T31.
  - Public-only: "the rebuild matches the reported 130 and 133 (130.2, 133.0)"; tests T1–T12; the Scorecard page's reconciliation table.

### Q14 · Governance and regulators · *"What does 'governed' mean to you, and what regulatory reporting have you actually supported? If a regulator asked why your dashboard's SAIDI doesn't match the filed number, what would you say?"*
(V3 B5 + B9)
- **Claim:**
  - **Experience:** `[you: the truth; no job bullet shows a regulatory filing]`.
  - **Governance:** definitions with owners, change control, and checks that stop bad data reaching a report.
- **Proof:**
  - **What governance means:**
    - a named owner for each definition
    - a glossary with versions and effective dates
    - sign-off on changes
    - lineage from source to visual
    - access rules
    - quality checks that alert
  - **What I've done:**
    - at Mercury, wrote up the evaluation method and its definitions for other teams to reuse [resume: Mercury b6]
    - the board's investment dashboard at the Life Initiative [resume: Life Initiative b1]
    - the projection model behind an executive case for a credit facility at CCL [resume: CCL b3]
  - **Filed vs dashboard:** the filed number is the anchor. Write the bridge: same population, same MED rule, same customer basis, same vintage. Keep as-filed and revised vintages side by side, and never overwrite silently.
- **Limit:** The project has a decisions log, a data dictionary and tests [C-S7-06]. It has no owner, access control or monitoring, because it's a personal project; say so.
  - (adopted variant) decisions D1–D22.
  - Public-only: decisions D1–D14.

### Q15 · EAGLE-I in SQL · *"Walk me through the SQL that turns 15-minute snapshots into events and customer-hours. How did you handle missing intervals and bad readings?"*
(V3 B6) (adopted variant)
- **Claim:** It's in the same SQL build as the rest, covered by tests T13–T31 [C-S7-10].
- **Proof:**
  - **Customer-hours:** the sum of customers out × 0.25, because each reading stands for a quarter hour.
  - **Events:** gaps-and-islands. LAG on the timestamp flags a new event after a gap (60 minutes per county, 180 for the territory), and a running SUM assigns event IDs.
  - **"Held 1 hour":** the minimum over the current reading and the next three.
  - **Days:** Eastern Standard Time all year, so there are no daylight-saving jumps.
  - **Data quality:**
    - blanks are failed runs, kept NULL, never zero (P20, D16)
    - readings above twice a county's customers are set to NULL (P24)
    - one-reading drops and spikes are handled (P25)
    - four counties are left out (P26, P27)
  - **Scale:** 11,608,442 rows, Nov 2014–2025 [C-S7-12].
- **Limit:** EAGLE-I is scraped from outage maps and its coverage grows over time, so compare a county with itself. There's no rule yet for counts stuck at one value; I'd add one.
- **Public-only:** EAGLE-I isn't in the public repo. If you're asked about snapshot data, describe this as how you would do it.

### Q16 · The Mercury pipeline · *"Tell me about the Snowflake pipeline at Mercury, the 20-million-row one. Grain, loads, keeping it current, and which part was yours?"*
(V3 B7)
- **Claim:** `[you: one sentence on what it fed and what you owned]`.
- **Proof:**
  - **From the resume:** a Snowflake pipeline over the policy, claims and billing data (20M+ rows) that fed the AI pilot and kept its data up to date, written in SQL [resume: Mercury b1; C-S8-01].
  - **Mechanics:** `[you: the fact grain; the incremental logic (merge on keys or a watermark); scheduling; tests; one failure and how you fixed it]`.
  - **Ownership:** `[you: "I wrote X; the platform team owned Y."]`
- **Limit:** Claim only the ownership you had. Bridge: the same pattern maps outage events to daily and then annual indices.

### Q17 · Real reconciliation · *"Your Mercury validation bullet is scoring an AI system against a test set. That's model evaluation. Give me a real data reconciliation: what against what, what broke, what you changed. And how do you know the sales lift and faster settlements were yours?"*
(V3 B8)
- **Claim:** Model evaluation and data reconciliation are different, and I keep them separate.
- **Proof:**
  - **The evaluation:** I scored the AI system's answers and citations on a 150-question test set, and accuracy went from 71% to 90% [resume: Mercury b3; C-Q-03, C-Q-04].
  - **A data reconciliation at work:** `[you: one true story: the break, the root cause, the control you added]`. If it's true, the daily SAP inventory exports at Cofoods are a candidate [resume: Cofoods Finance b2].
  - **In the project (P18):**
    - Prince George Electric filed SAIDI but no SAIFI for 2025.
    - A group denominator over all members' customers would understate the co-op SAIFI (1.849 instead of 1.887) [N-8].
    - Denominators now count only utilities that reported the numerator. Corrected 27 Oct (commit 1635a8e).
  - **Attribution:**
    - **Causal only where there was a control:** the A/B test (+9% on-time renewals) [resume: Mercury b4; C-Q-05].
    - **Otherwise "contributed to":** the settlement-time cut [resume: Mercury b2; C-Q-02] and the sales lift [resume: Cofoods BD b1]. `[you: what else changed at the time]`
- **Limit:** Don't defend the keyword. Name the difference and move on.

### Q18 ● · Do differently · *"What would you do differently?"*
(brief)
- **Claim:** Set the rules before seeing results, everywhere, as I did for the peer set.
- **Proof** (pick two that are true for you):
  1. **Test aggregates for missing values first.** P18 showed that one utility with customers but no SAIFI dilutes a group figure. I'd write that rule as a test before building group views (docs/03 P18).
  2. **Show the all-events view next to ex-MED from the start.** Dominion uses its own MED method, and on all events its SAIFI rank moves from 4th to 6th of 12 [N-3].
  3. **Fix comparison windows and base years up front, in one stated rule.** That's how the peer set was chosen: by EIA ID, before results (D10) [C-S3-06].
- **Limit:** `[you: one personal lesson]`. Never tell a change from the upgrade as a discovery story.

## HR / behavioral

### Q19 · Why move · *"You joined Mercury in April. Why move after seven months, and why a utility?"*
(V3 H1)
- **Claim:** `[you: your real reason, framed as a pull toward this work]`. One neutral sentence on Mercury, then stop.
- **Proof:**
  - **The pull:** grid resilience is public-service work with measurable outcomes. This role reports on the Grid Resiliency programs: Mainfeeder Hardening, Voltage Island Mitigation, Voltage Optimization, and Intelligent Grid Devices/FLISR [R-035].
  - `[you: which program interests you, and why]`
  - **Evidence of interest:** I rebuilt Dominion's reported reliability numbers from public data [C-S2-02].
- **Limit:** Never criticize Mercury, and don't over-explain the tenure (April 2026 to now) [C-S8-06].

### Q20 · Three years · *"Your summary says three years of BI experience, but your data-titled roles add up to under a year. Walk me through the three. How would you feel about the Associate level?"*
(V3 H2)
- **Claim:** Fair question. Here's how it adds up, from the dates on my resume [N-9]:

| Bucket | Roles | Months |
|---|---|---|
| Data-titled | Data Analyst, Mercury (Apr 2026 to now, 7) and Data Analytics Intern, Life Initiative (Jul–Sep 2025, 3) | about 10 |
| Analytics inside other roles | Business Development Associate, Cofoods (Jan 2023–Jul 2024, 19): the demand-forecasting model and Tableau account dashboards [resume: Cofoods BD b1]; two finance internships (Apr–Dec 2022, about 9): Excel modeling and scripts automating SAP inventory reporting [resume: CCL b1–b3; Cofoods Finance b1–b2] | about 28 |
| Total since April 2022 | 26 months full-time and about 12 as an intern, plus the MS in Business Analytics (Jan 2026) | about 38 (three years) |

- **Proof:** "Three years" is all my work since 2022, internships included. About ten months of it carried a data title. Don't stretch it further.
- **Limit / level:** "I'm open to either level, and I'd rather earn the step up with the work." Point to the evidence: a tested pipeline, reconciliation to the reported figures, and a decisions log.

### Q21 · Pushback · *"Tell me about a time someone senior said your numbers were wrong. What did you do? And how would you handle our engineer's pushback on your county view?"*
(V3 H3)
- **Claim:** Listen, check, fix the source, document the definition, and thank the person.
- **Proof:**
  - **The story:** `[you: a real STAR story: what was challenged, what you checked, who was right, what changed]`. The resume doesn't contain one.
  - **Live:** "You're right that the county data counts every utility. I'd label it 'all utilities' or cut it to Dominion-only counties" (Q3). Thank the engineer; don't defend.
- **Limit / principle:** Domain experts own the definitions. The analyst owns reproducibility and the audit trail.

### Q22 · Least sure · *"Which number are you least sure of? And what do you say when a director asks something you don't know?"*
(V3 H4)
- **Claim:** Name one, specifically, and say why.
- **Proof:** pick one:
  - the weather fit (r = 0.70 on ten points; interval 0.12–0.92) [C-S4-15]
  - Dominion's MED rule, which I haven't seen written down (Q2)
  - (adopted variant) the county outage minutes, which count every utility (Q3)
- **The "I don't know" move:** "I don't know. Here's where I'd find out, and I'll come back to you by [time]." Never guess a number in the room. `[you: one time you did this at work]`
- **Limit:** Admitting doubt builds credibility only when the fix comes in the same breath.

### Q23 · The merger · *"There's a pending merger with NextEra. How do you feel about joining now?"*
(V3 H5)
- **Claim:** Calm and practical. Reliability reporting and the resiliency programs carry on through any integration, and integrations create exactly this definition and reconciliation work.
- **Proof:**
  - **The process, stated as facts:**
    - announced May 2026
    - Virginia's final order due by mid-January 2027
    - South Carolina, North Carolina, FERC and the NRC also have to approve
    - close expected in the second half of 2027 [C-Q-10]
  - **The company's position:** Dominion Energy Virginia stays separately regulated and accountable to the SCC [C-Q-11].
- **Limit:**
  - Give no view on the deal or on jobs, and no FPL-versus-Dominion comment: "different territories and methods; comparisons are indicative".
  - Ask back: "How does the team expect priorities or tools to shift over the next year?"

### Q24 · Thirty seconds · *"I'm not an engineer. In thirty seconds, no acronyms: what did you find, and why should I care?"*
(V3 H6)
- **Say:** "In 2025 the average Dominion customer in Virginia lost power about 1.3 times, for about an hour and fifty minutes each time: almost two and a half hours in the year, leaving out a few extreme storm days. The three-year average went up by about three minutes, mostly because 2025 was stormier, with more outages. Once storms are counted, there's no clear trend. This job is about showing clearly whether the programs that prevent outages are working." [C-S2-04, C-S2-06, C-S2-03, C-S2-01]
- **Limit:** Stop at thirty seconds, and don't let acronyms creep back in.

### Q25 · The unglamorous work · *"Much of this job is building and maintaining reports other people ask for. How do you make a recommendation as a new analyst without overstepping, and are you happy doing the less glamorous work?"*
(V3 H7)
- **Claim:** Yes. Accurate recurring reports are the job. Ideas go to my manager as questions, with the data, at the right time.
- **Proof:**
  - **Handover and documentation habits:**
    - the evaluation method and definitions written up for other teams to reuse [resume: Mercury b6]
    - handover notes for the n8n automation [resume: Life Initiative b2]
    - the project's data dictionary and decisions log
  - **How I raise an idea:** a one-page note with the data, framed as a question (for example, "are blue-sky interruptions rising under the weather?"), checked first with the people who own the plan, with credit to them.
- **Limit:** I don't know Dominion's planning context yet; recommendations come after I've learned it.

---

## Numbers not yet in `claims.csv` (for B and D)

All accessed or computed on 2026-11-01. R computed these read-only from committed files. D to confirm before print.

| Id | Value | Source and method |
|---|---|---|
| N-1 | 2025 95% prediction interval 122.3–168.2 (±23.0) around 145.25; residual SD 8.67 | `data/output/storm_vs_saidi.csv`, fit 2015–24 (r 0.6973, p 0.0250, matching C-S4-04 and C-S4-15); `work/scripts/r5b_fit_checks.py` |
| N-2 | Dominion VA in EIA-861: standard "Other" 2013–2025; recorded automatically False 2013–14, True 2015–25 | `data/output/fct_reliability.csv` (`standard`, `auto_recorded`); `work/scripts/r5b_all_events_rank.py`. D6 gives the same reason for the 2015 start |
| N-3 | All-events SAIFI mean 2021–25: Dominion 1.531, 6th of 12; median of the other 11 is 1.408 (ex-MED: 4th, 1.211 vs 0.934) | same script; the ex-MED values reproduce C-S3-01 exactly |
| N-4 | Ex-MED medians of the 11 others: SAIFI 0.934, CAIDI 99.5 (12-point medians 0.964 and 105.0) | same script; matches V3's ≈0.93 and ≈99 |
| N-5 | 10 of 12 utilities report under IEEE 1366 in every year 2014–2025; Dominion VA and Alabama Power report "Other" | same file. **Conflicts with docs/06** ("Half the peers use a different reporting method", Fair comparison headline), which D or B should check |
| N-6 | Storm vs calm levels: 332.8 vs 27.86 customer-hours per 1,000 customers | `work/data/findings.md` A1 table |
| N-7 | 6,530 − 6,108 = 422 storm county-days; 2025: 791 vs 677 (114) | C-S4-05 (A2 storm index, 103 counties) vs findings A1 by-year (complete readings, 99 counties). [I] The attribution to the two filters is R's reading; D to confirm |
| N-8 | P18: 1.849 vs 1.887 (13,341 customers of Prince George Electric) | `docs/03_data_quality.md` P18; commit 1635a8e, 27 Oct 2026 |
| N-9 | Resume month counts: data-titled 10; full-time 26; internships about 12; total about 38 | resume dates, paraphrased (Mercury Apr 2026–; Life Initiative Jul–Sep 2025; Cofoods BD Jan 2023–Jul 2024; Cofoods Finance Jul–Dec 2022; CCL Apr–Jul 2022) |
| N-11 | All-events SAIDI mean 2023–25: Dominion 223.0, 9th of 12 (ex-MED 133.0, 4th) | `r5b_all_events_rank.py` |

*(N-10 was not needed: the 117–150 range is C-S4-05.)*
