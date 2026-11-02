# V3 mock panel: Dominion reliability deck v1 (letter print)

**Reviewed:** 2026-11-01 · **Interview:** Tuesday 3 November 2026 · **Role:** Associate BI Analyst / BI Analyst, Grid Resiliency programs, Richmond

**Deck reviewed:** `snapshot_v1_0855/Dominion_reliability_deck_v1_print_letter.pdf`: 14 pages, 8 main slides plus A1–A6.

**Inputs used, and only these:**
- the printed deck
- the resume, read locally and cited by role and bullet in paraphrase, never quoted
- `research/role_brief.md`

**Method:**
- Every page was rendered at 150 dpi to `work/reviews/v3_pages/` (`p01.png`–`p14.png`, plus `p02_gray.png` and `p04_gray.png`) and read as an image.
- Charts were re-cropped at 300 dpi, and quotes come from the PDF text layer.
- Every printed number was re-added or re-derived; the workings are at the end.
- Values marked ≈ were read off chart images.

**Panel:**
- **BI**: the BI/analytics hiring manager
- **ENG**: a distribution-reliability engineer
- **HR**: the HR/behavioural interviewer

## Bottom line

- **What wins:** the build story on slides 6–7 is the deck's strength. It speaks the posting's language: reconciliation, tests, definitions, programme tracking.
- **The opening claim fails its own appendix.** Slide 2 says "because interruptions became more frequent, not longer". A1 measures from a different base year and finds interruptions got longer. A2 says 2025 is what the storm count predicts, with no storm-adjusted trend.
- **Slide 4 points at the wrong customers.** It tells Dominion which counties to start with, using EAGLE-I minutes that count every utility's customers.
- **Power BI never appears.** It is the job's first duty. Slide 8 claims professional Power BI work, but the resume's job history doesn't show it.
- **Several numbers don't reconcile in a deck selling reconciliation:**
  - 6,108 vs 6,530 storm county-days
  - 12 vs 31 tests
  - "12 peers" that are 11, with medians that include Dominion
- **As it stands the talk runs about 10¼ minutes with no interruptions.** Cut slide 5 and simplify slide 4 to fit.

---

## 1. The 25 hardest questions

### Distribution-reliability engineer (9)

**E1 · ENG.** *"Your headline says minutes went up 'because interruptions became more frequent, not longer'. Your appendix A1 splits 2023 to 2025 and gets 79% from frequency, so a fifth of the rise came from longer interruptions. Which is it? And why does A1 use a different base year from slide 2?"*
- **Why it's hard here:** both statements are in the handout.
  - On slide 2's own years (2022 → 2025) the log split gives about **160%** from frequency, because duration fell and offset it.
  - On A1's years (2023 → 2025), CAIDI rose about 3% (≈105.8 → 109.4).
  - The panel will suspect A1's base year was picked to avoid an odd-looking 160%.
- **A strong answer:**
  - Concede and correct on the spot. Against 2022, the year that left the 3-year window, CAIDI fell 4% and frequency explains more than all of the rise. Against 2023, both rose. "Driven by frequency" holds; "not longer" depends on the base year. A1 should use 2022 → 2025.
  - Show that CAIDI is a ratio. Extra short interruptions pull it down even if crews are no faster. Automation such as FLISR cuts the number of customers interrupted, which can push CAIDI up. It is not a restoration-speed measure.
  - Say what would settle it: interruption-level durations by cause from OMS.

**E2 · ENG.** *"Step back. 130 to 133 is 2.8 minutes on a three-year average. Your A2 table says 2025 is almost exactly what the storm count predicts, and there's no storm-adjusted trend. So is there anything here to explain? If not, why is 'frequency first' your first takeaway?"*
- **Why it's hard here:** the lead story and the appendix disagree.
  - Ex-MED SAIDI moves about ±11 minutes a year (SD of the 2015–24 values), so 2.8 minutes is noise.
  - 2025 had 791 storm county-days, second only to 2019, and the fit misses it by 0.9 minutes.
  - Slide 2's "For Dominion" line assumes something *is making* interruptions more frequent.
- **A strong answer:**
  - Agree at once. On public data, 2025 looks like a storm year, not a deteriorating system, and the move in the average is within normal variation.
  - Re-anchor "frequency first" on two things:
    - the peer gap on slide 3: 1.21 against a peer median below 1.0
    - the fact that hardening, vegetation and automation programmes act on frequency
  - Name the question you would really ask with Dominion data: are non-storm (blue-sky) interruptions rising underneath the weather, by cause?
  - Explain why you led with 130 → 133: it is the number Dominion reports, and rebuilding it was how you learned the data.

**E3 · ENG.** *"Walk me through 2.5 beta. You say Dominion doesn't use it for EIA, so what is Dominion's rule, and what does that do to your ranking? Where does Dominion rank on all-events SAIFI? And with the NextEra deal pending, FPL is your best dot. How would you make a Dominion-versus-FPL comparison fair?"*
- **Why it's hard here:**
  - A1 describes the method in one line and leaves out the logs.
  - The deck never states Dominion's rule and has no all-events peer view.
  - Slide 8 drops the "indicative" caveat.
  - FPL is a loaded comparison right now.
- **A strong answer:**
  - Give 2.5β precisely:
    - take five years of daily SAIDI and drop the zero days
    - take natural logs; α is their mean and β their standard deviation
    - T_MED = e^(α + 2.5β); any day above it in the next year is an MED
    - it is designed to flag only a few days a year
  - Dominion's rule:
    - State it exactly, with its source.
    - Or say: "I don't know the exact rule. EIA-861 records it as non-IEEE, and I'd get the definition from the filing or the reliability team."
    - Give the direction of the effect: a rule that excludes more days lowers ex-MED SAIFI, so ranks can move either way.
  - The robustness check is the **all-events** rank, which involves no MED rule. Compute it before Tuesday and quote it.
  - For FPL, check whether it uses the same MED method, and note the different climate, construction standards and territory. Compare like with like (all-events, same years, customer density), call it indicative, and don't editorialise.

**E4 · ENG.** *"EAGLE-I counts every utility in a county. Your map has Pittsylvania at 633 minutes a customer on ordinary days. Dominion's ex-MED SAIDI averaged about 134 over the same years. Whose customers are those? Would you send a hardening crew on this map? And your Isaias curve says 90% restored after 33.5 hours. 90% of what?"*
- **Why it's hard here:**
  - The slide prints the all-utilities caveat, then says "start with the counties that lose the most minutes on ordinary days".
  - About 71% of the shaded map area is at 250 minutes or more, roughly 2 to 5 times the system figure.
  - The slide never says how a "non-major day" was defined for EAGLE-I.
  - The inset is measured on net customers out, from the peak.
- **A strong answer:**
  - **No.** The map counts all utilities' customers (co-ops, munis, other IOUs) in any county where Dominion serves at least some customers. It is not Dominion's SAIDI and shouldn't be used to target work. The cut to Dominion-only counties is the defensible view.
  - Name EAGLE-I's limits:
    - 15-minute snapshots scraped from outage maps
    - coverage that changes over the years
    - gaps and stuck counts
    - no count of distinct interruptions, so no SAIFI
  - Say exactly how non-major days were set.
  - On Isaias: it is 90% of the **peak snapshot**, net of new outages, all utilities, timed from the peak. Utilities report "% of affected customers restored" against the cumulative count, which is a different, slower-looking curve.

**E5 · ENG.** *"A lot of NOAA storm reports, thunderstorm wind especially, are logged because trees and wires came down. Isn't your 12× partly circular? And what's the unit behind that 95% interval? County-days hit by the same storm aren't independent."*
- **Why it's hard here:**
  - A "storm report" partly selects on damage.
  - The method behind the CI isn't on the slide.
  - The deck's own counts disagree: 6,108 storm county-days on slide 4, 6,530 summed from A2.
- **A strong answer:**
  - Accept the reporting bias. The ratio is an association inflated by construction, which is why slide 8 calls it one. Don't defend causality.
  - Give the resampling unit exactly: date or storm, not county-day. If it was county-day, say the interval is too narrow and give the clustered one.
  - Offer a cleaner test as a next step, not a claim: weather measured independently of damage, such as station wind gusts.
  - Reconcile 6,108 against 6,530 in one sentence.

**E6 · ENG.** *"Your weather fit has ten points. What's the interval on r = 0.70 with n = 10? Your 2025 check came within 0.9 minutes, but what was the prediction interval? And why start in 2015 when you loaded storm data from 2013, and 2013 and 2014 were Dominion's two best years?"*
- **Why it's hard here:**
  - r's 95% CI is about 0.12–0.92. Dropping 2020 lifts r to 0.83; dropping 2019 cuts it to 0.57.
  - The 2025 prediction interval is about **±23 minutes** (≈122–168).
  - A3 shows ex-MED SAIDI at ≈106 in 2013 and ≈112 in 2014. A 2013 start roughly triples the raw slope (≈+2.0 against ≈+0.6 minutes a year, read off the chart).
- **A strong answer:**
  - Quantify first. The residual SD is about 9 minutes, so 2025 landing near 145 is consistent with the fit, not proof of it. With n = 10 the fit is a sanity check, which is what A2's own title says.
  - Give the real reason for 2015 (for example, aligning with the EAGLE-I window that starts in November 2014). Then show the result with a 2013 start, even if it shows a rise.
  - Say "can't tell", not "no trend". The interval (−1.4 to +2.1 minutes a year) allows about 20 minutes a decade.

**E7 · ENG.** *"You'd time restoration from meter 'last gasp'. What does a last gasp tell you, and what happens to those messages in a big storm? And with 99.8% AMI, how do you know 2025's record SAIFI isn't a measurement change, meters catching outages the old process missed?"*
- **Why it's hard here:**
  - Slide 6's wording confuses the start signal with restoration.
  - The AMI rollout overlaps the SAIFI rise, and the deck never considers a change in measurement.
- **A strong answer:**
  - A last gasp is the meter's power-loss message, so it marks the start. Restoration needs the power-restore message or a ping, and OMS stays the system of record for reported indices.
  - In widespread outages, collectors and backhaul lose power and last gasps are lost. AMI is a cross-check, not a replacement.
  - Explain the measurement effect: more automated detection usually raises *recorded* SAIFI and SAIDI, because small outages get captured and start times move earlier. To check it:
    - compare the AMI deployment timeline with the index
    - look at EIA-861's "recorded automatically" flag
    - compare circuits before and after their AMI cut-over
  - Don't call it deterioration until measurement change is ruled out.

**E8 · ENG.** *"Your last slide maps your root-cause work to 'SAIFI by cause'. There's no cause analysis in this deck. Tell me what you'd expect in our cause codes, vegetation in particular, and what will go wrong with the data."*
- **Why it's hard here:**
  - The arrow reads as if the work is done, but EIA-861 has no causes.
  - The candidate has no utility operations experience (role brief G1).
- **A strong answer:**
  - Frame it precisely: SAIFI by cause is a days 31–60 deliverable that needs Dominion's outage records. Public data can't do it (A5).
  - Show the domain:
    - the usual cause families: vegetation, equipment, lightning/weather, animals, vehicles/public, unknown
    - vegetation dominates storm days, and much of it is trees from **outside** the trimmed right-of-way
    - split blue-sky days from storm days
    - use CEMIn for repeat offenders
  - Name the data traps:
    - crews code the cause at closure, so coding is inconsistent
    - one device event affects many customers
    - the "unknown" share is itself a data-quality KPI
  - Agree the definitions with engineering before charting anything.

**E9 · ENG.** *"Mainfeeder hardening: we pick the worst feeders, and we say outage minutes fall by roughly a third after hardening. If you built the tracking report on your slide 6, how would you know it's the programme and not regression to the mean or a mild year?"*
- **Why it's hard here:**
  - Slide 6 proposes comparing with "similar untreated feeders and weather".
  - Dominion's published selection rule (feeders where at least 500 customers have SAIDI more than 2 minutes worse, per role brief §2) guarantees regression to the mean.
  - The panel may own the −32% (Nov 2023) and −44% (June 2026) figures, so critique has to sound like help.
- **A strong answer:**
  - Name the trap. Feeders chosen for a bad recent history improve on average anyway, so a plain before-and-after overstates the effect.
  - Give the design:
    - a multi-year pre-period
    - comparison feeders matched on pre-period SAIDI and SAIFI, exposure and region
    - difference-in-differences with storm normalisation and the same MED treatment
    - staggered completion dates
    - results reported with intervals
  - Frame it as making a good result harder to challenge at the regulator and the board. Use the A/B-test discipline from Mercury (sample size, significance thresholds).

### BI / analytics hiring manager (9)

**B1 · BI.** *"This is a BI job, and the first duty is Power BI. Where's the Power BI in this deck? Describe the model: tables, grain, relationships. How do you calculate the three-year rolling SAIDI? And if I roll SAIDI up from regions to system, how do you aggregate it?"*
- **Why it's hard here:**
  - Power BI appears as one box on slide 7, with no screenshot, model or measure.
  - The panel can't tell which tool drew the charts.
  - The aggregation question has a right and a wrong answer.
- **A strong answer:**
  - Have a printed report page and the model view ready:
    - a fact table at utility × state × year, with and without MED
    - dimensions for utility, year and geography
    - a disconnected year table for the slicer
  - Say which deck charts came from Power BI.
  - Rolling 3-year: AVERAGEX over the three selected years of the year-level measure, driven by the disconnected year. This matches Dominion's convention of a "mean of annual values".
  - Aggregation: never average SAIDI or CAIDI. Sum customer-minutes and customer interruptions, divide by customers served, and take CAIDI = SAIDI ÷ SAIFI at the aggregate.

**B2 · BI.** *"Your job bullets show Tableau at two employers; Power BI only shows up in your summary and skills. Where have you used Power BI at work? And the posting lists Power Apps. What have you built in it?"*
- **Why it's hard here:**
  - Slide 8 says "I build governed Snowflake → Power BI reporting" in the present tense.
  - Power Apps isn't on the resume (G2), and SharePoint appears only in the skills line (G7).
- **A strong answer:**
  - Be exact and truthful about where Power BI was used professionally, if anywhere. If it's only this project, say so, then show depth: model, measures, refresh.
  - Transfer, don't stretch. Tableau delivery to a board (Life Initiative) and to account teams (Cofoods) is the same job. The Power BI-specific skills are in the project.
  - On Power Apps: "not in production", plus a concrete 30-day plan tied to a use, such as an exceptions or field-update form feeding the report. Never claim it.

**B3 · BI.** *"You reconciled 13 of 13 values: 133.0 against 133. But you averaged three numbers Dominion reported to EIA and matched Dominion's own average. What did that prove? Which are the 13?"*
- **Why it's hard here:** the check is partly circular, and the 13 values aren't listed anywhere.
- **A strong answer:**
  - Recite the 13 from a card.
  - Say what it proves:
    - the right utility ID and state row
    - the MED flag
    - the averaging convention (mean of annual values, not pooled)
    - the vintage (2025 final plus PUDL)
    - the customer basis

    It is a definitions check, not an independent measurement.
  - Describe a real reconciliation at Dominion: OMS events → daily SAIDI → the annual filed figure, with a bridge for exclusions (MEDs, planned outages, momentaries, customer counts).

**B4 · BI.** *"Slide 7 says 12 tests pass; A4 says 31. Slide 4 says 6,108 storm county-days; your A2 column adds to 6,530. In a deck about reconciliation, which numbers are right, and what does that tell me about your QA?"*
- **Why it's hard here:** the handout contains both versions, and a BI manager adds columns.
- **A strong answer:**
  - Own it in one breath. Give the right figures and why they differ, without defensiveness:
    - 31 tests in total, 12 of them on the reliability mart
    - for the storm county-days: 99 against 103 counties, EAGLE-I gaps, or a different window
  - Name the control you'd add: every on-slide number pulled from one tested "figures" table with an ID, checked before anything is published.
  - Better still: fix the deck before Tuesday so the question never comes.

**B5 · BI.** *"'Governed production reporting.' What does governed mean to you? Who owns the SAIDI definition? If the MED rule changes mid-year, or EIA revises last year, what happens to your report? What happens when a refresh fails?"*
- **Why it's hard here:** the project shows no owner or steward, access control, change control or monitoring. Yet both the posting and the resume lean on governance language.
- **A strong answer:**
  - Define governance:
    - a named owner and steward for each definition
    - a business glossary with versioned definitions and effective dates
    - change control with sign-off
    - lineage from source to visual
    - access rules (RLS where needed)
    - data-quality checks that alert
  - Restatements: keep the as-filed and revised vintages side by side, never overwrite silently, and annotate the report.
  - Failure handling: tests gate the load, the report shows the last good refresh, and the owner is alerted. Then say plainly which of these the project has and which it doesn't.

**B6 · BI.** *"EAGLE-I is your biggest dataset, 11.6 million rows, and it's not on your pipeline slide. Was slide 4 built outside Snowflake? Walk me through the SQL that turns 15-minute snapshots into events and customer-hours, and how you handled missing intervals and stuck counts."*
- **Why it's hard here:**
  - Slide 7 shows three sources, while A4 says every number traces to a tested query.
  - A6's "held 1 hour" events need non-trivial window logic.
- **A strong answer:**
  - Say exactly where EAGLE-I was processed and which tests (T13–T31) cover it, and fix the diagram.
  - Walk through the SQL:
    - customer-hours = Σ customers_out × 0.25
    - events found by gaps-and-islands (LAG, or a running SUM to assign event IDs)
    - "held 1 hour" as a rolling minimum over four intervals
    - county FIPS mapping, including Virginia's independent cities
    - time zone and DST handling
  - Cover data quality:
    - missing intervals left null, not zero
    - stuck counts flagged (identical values over long runs)
    - coverage that changes by year

**B7 · BI.** *"Tell me about the Snowflake pipeline at Mercury, the 20-million-row one. What was the grain, how did loads run, how did you keep it current and reliable, and which part was yours?"*
- **Why it's hard here:**
  - Slide 8's whole experience mapping rests on a role that started in April 2026.
  - On the resume that pipeline feeds an AI pilot, and the manager will drill for ownership and mechanics.
- **A strong answer:**
  - Concrete mechanics:
    - the schemas and the fact grain
    - the incremental logic (merge on keys or watermarks)
    - scheduling and tests
    - one failure and how it was fixed
  - A clean split of ownership: "I wrote X; the platform team owned Y."
  - The bridge: the same pattern for outage events → daily → annual indices.

**B8 · BI.** *"Your Mercury bullet on validation and reconciliation is about scoring an AI system against a test set. That's model evaluation. Give me a real data reconciliation you've done at work: what against what, what broke, what you changed. And your resume credits your work with a sales lift and faster settlements. How do you know those were yours?"*
- **Why it's hard here:**
  - The resume puts the posting's governance words on an LLM-evaluation bullet; the role brief infers the resume was tailored.
  - The deck carefully says "an association", which invites the same test of the resume's causal claims.
- **A strong answer:**
  - Tell one specific, true reconciliation story: the break, the root cause, the control added. It might come from the SAP-export tracker at Cofoods, or from source-to-warehouse checks at Mercury, if that's what happened.
  - Separate model evaluation from data reconciliation without getting defensive about the keyword.
  - Attribution: claim causality only where there was a control (the A/B test). Otherwise say "contributed to" and name what else changed.

**B9 · BI.** *"Regulatory reporting: what have you actually supported? If a regulator asked why the SAIDI in your dashboard doesn't match the filed number, what would you say? And how would you automate the annual reliability report?"*
- **Why it's hard here:** the resume's skills line claims regulatory reporting support, and no bullet shows a filing (G5). These are posting responsibilities 3 and 8.
- **A strong answer:**
  - Be truthful: "I haven't filed with a regulator." Then name the adjacent work: board-level reporting, and the executive deck behind a credit facility.
  - Describe a reconciliation bridge to the filed figure, with every difference written down. The filed number is the anchor. The bridge checks:
    - the same population
    - the same MED rule
    - the same customer basis
    - the same vintage and timing
  - Automation: governed source tables → tested transformations → a parameterised report or export, with:
    - sign-off gates
    - an audit trail
    - frozen as-filed snapshots

### HR / behavioural (7)

**H1 · HR.** *"You joined Mercury in April. Why move after seven months, and why a utility?"*
- **Why it's hard here:** a short tenure, no utility background, and Mercury can't be criticised.
- **A strong answer:**
  - A pull, not a push. Grid resilience is a public-service mission with measurable outcomes, and the project shows weeks of self-directed interest.
  - Show you know the team. Name the four Grid Resiliency programmes and why one interests you:
    - mainfeeder hardening
    - voltage island mitigation
    - voltage optimization
    - intelligent grid devices/FLISR
  - One neutral sentence on Mercury, then stop.

**H2 · HR.** *"Your summary says three years of BI experience, and your data-titled roles add up to under a year. Walk me through the three. If we offered the Associate level, how would you feel?"*
- **Why it's hard here:** the posting has two levels, the deck reads senior, and the arithmetic is on paper (role brief G4).
- **A strong answer:**
  - One honest sentence that adds up: the data analyst role, the analytics inside the business-development and finance roles (forecasting model, dashboards, SAP-export automation), and the MS.
  - Don't argue the level. Say you're open to either and want to earn the step up with the work.
  - Point to the BI-Analyst-level evidence: an end-to-end tested pipeline, reconciliation and a decision log.

**H3 · HR.** *"Tell me about a time someone senior told you your numbers were wrong. What did you do? And earlier our engineer pushed back on your map. How would you handle that if you worked here?"*
- **Why it's hard here:**
  - The deck is solo work.
  - The engineer will already have challenged slide 2 or slide 4.
  - HR is watching how the candidate took it.
- **A strong answer:**
  - A real STAR story: listened, checked, found who was right, fixed the source and documented the definition.
  - Apply it live: "He's right that the map counts every utility. I'd relabel it or cut it." Thank, don't defend.
  - State the principle: domain experts own the definitions; the analyst owns reproducibility and the audit trail.

**H4 · HR.** *"Which number in this deck are you least sure of? And what do you say when a director asks you something you don't know?"*
- **Why it's hard here:**
  - The deck projects certainty: 13 of 13, all tests pass.
  - Admitting doubt in an interview is uncomfortable, though honest candidates exist: the EAGLE-I county minutes, the CI method, Dominion's MED rule.
- **A strong answer:**
  - Name one specifically and say why it's uncertain.
  - Model the move: "I don't know. Here's where I'd find out, and I'll come back by end of day." Never guess a number in the room.
  - Give one example of doing that in a past job.

**H5 · HR.** *"There's a pending merger with NextEra. Integration could mean new systems, new teams, changed priorities. How do you feel about joining now?"*
- **Why it's hard here:**
  - The uncertainty is real.
  - Slide 3 plots FPL, NextEra's Florida utility, as the best-frequency peer.
  - Any opinion on the deal or on jobs is a trap.
- **A strong answer:**
  - Be practical and calm. Reliability reporting and resiliency programmes carry on through any integration. Integrations also create exactly the definition and reconciliation work this deck shows: two companies' MED rules, cause codes and KPIs.
  - No opinion on the deal, and no FPL-versus-Dominion editorial: "different territories and methods; comparisons are indicative".
  - Ask a good question back: how does the team expect priorities or tools to shift over the next year?

**H6 · HR.** *"I'm not an engineer. In thirty seconds, no acronyms: what did you find, and why should I care?"*
- **Why it's hard here:** the main slides use SAIDI/SAIFI/CAIDI, MED, IEEE 1366, PJM, EAGLE-I, CI and CEMI. A plain version has to be rehearsed.
- **A strong answer:**
  - Something like: "In 2025 the average Dominion customer in Virginia lost power about 1.3 times, for about an hour and fifty minutes each time. That's about two and a half hours in the year, leaving out a few extreme storm days. Recent increases came from outages happening more often, not lasting longer, and a stormy year explains most of that."
  - Why it matters: preventing outages is what the hardening programmes buy, and the job is to show clearly whether they're working.
  - Stop at thirty seconds.

**H7 · HR.** *"Every slide ends 'For Dominion' and tells us where our gap is and that our plans need updating. Much of this job is building and maintaining reports other people ask for. How do you make a recommendation as a new analyst without overstepping, and are you happy doing the less glamorous work?"*
- **Why it's hard here:**
  - The deck's tone is a consultant's strategy review, but the level is associate or analyst.
  - HR is assessing fit and humility.
- **A strong answer:**
  - Recast the lines as questions you'd bring, not conclusions, checked first with the people who own the plans.
  - Value the maintenance: accurate recurring reports are the job. Give evidence of handover and documentation, such as the n8n workflow handover and the reusable evaluation framework.
  - Say how you raise ideas: data plus a one-page note to your manager, at the right time, with credit to the owners.

**Logistics (not counted).** HR will probably close on logistics: hybrid 3-2 in Richmond, up to 25% travel, and the posting's line that Dominion can't sponsor or transfer a work visa for this role (role brief §1, G8–G9). Answer each in one truthful sentence; nothing in the deck helps here.

---

## 2. Where the deck overclaims, confuses or is weak

Severity levels:
- **High:** could cost credibility or the offer if raised.
- **Medium:** likely to draw a challenge or lose part of the room.
- **Low:** polish.

| # | Slide | Exact quote or element | Problem | Severity | Fix |
|---|---|---|---|---|---|
| P1 | 2, A1 | Title "…rose from 130 to 133 because interruptions became more frequent, not longer"; A1 "2023→2025, 0.125 ÷ 0.158 = 79%" | "Because" is an accounting identity, not a cause. "Not longer" holds only against 2022 (CAIDI 113.5 → 109.4). A1 switches to a 2023 base, where 21% of the rise is longer interruptions (CAIDI ≈105.8 → 109.4, +3%). On slide 2's own years the log split is ≈160% from frequency. | **High** | Title: "The 3-year average rose 2.8 minutes (130 → 133); in the 2022 → 2025 swap behind it, frequency rose 10% and duration fell 4%." Put A1 on 2022 → 2025 and explain the >100% share (duration offset), or show both bases. |
| P2 | 2, 8, A2 | "For Dominion: the first question is what is making interruptions more frequent…"; takeaway 1 "Look at frequency first … the 2013–2025 high" | A 2.8-minute move against year-to-year swings of about ±11 minutes. A2 puts 2025 on the storm line (fit 145.3, actual 144.4), with no storm-adjusted trend. The deck's own appendix answers slide 2's question: the weather. Takeaways 1 ("frequency first") and 2 ("net out the weather") pull against each other. | **High** | Add to slide 2: "2025 was the second-stormiest year since 2015; storm counts explain it (A2)." Recast the question: "With cause codes: are non-storm interruptions rising under the weather?" Rest "frequency first" on the peer gap (slide 3), not on 2025. |
| P3 | 2 | Hero lines "130 → 133", "130.2 → 133.0", "136.0 → 144.4" | Three look-alike arrows. Two are the same quantity, and the third is single years that look like another average. A non-technical panellist loses the thread. | Medium | One hero number (130 → 133) with a small "rebuilt from EIA-861: 130.2 → 133.0" tag. Label the third "single years: 2022 136.0 vs 2025 144.4". |
| P4 | 2 | "SAIFI by year: 2025 is the highest of 2013–2025"; y-axis starts at 1.0 | 1.320 vs 1.303 (2018) is a 1.3% margin, and the truncated axis makes the swings look large. | Low | "2025 (1.320) edges 2018 (1.303)"; flag that the axis starts at 1.0. |
| P5 | 2 (print) | Decomposition bars and SAIFI line | In greyscale the SAIFI bar, the slide's point, prints mid-grey (≈100/255) while the SAIDI bar prints near-black (≈42): the emphasis flips. The SAIFI line is thin and pale on paper. | Low | Make SAIFI the darkest mark or label it "driver"; darken the line and the grey peer dots. |
| P6 | 3, 8 | "Among 12 peer utilities"; "4th of 12 peers"; "peer median 0.96", "peer median 105 min" | The chart has 12 dots *including* Dominion, so there are 11 peers. Read off the chart, both medians are 12-point medians that include Dominion. Without it they are ≈0.93 and ≈99 min, so Dominion's 110 min is ≈11% above the median peer, not ≈5%. | Medium | "Dominion vs 11 peers"; compute medians on the 11 only. |
| P7 | 3 | Title "Dominion restores at a mid-pack pace"; footer "restoration speed is already near the middle" | CAIDI is minutes per interruption, a ratio that moves with the outage mix, not restoration pace. Dominion sits upper-right (worse than the median on both axes), 6th-longest of 12. | Medium | "Average interruption length is mid-pack (6th of 12); frequency is 4th highest." |
| P8 | 3 | Four unlabelled dots; one label "Duke Progress (NC), Georgia Power" for two dots | The panel will ask "who's that?" and "is Appalachian Power in here?". | Low | Label every dot or list the peers in the footnote. |
| P9 | 3 | FPL plotted as the best-frequency peer | FPL is NextEra's utility. With the merger pending, the chart invites a Dominion-vs-acquirer comparison in the room. | Medium | Keep the dot but don't narrate it. Have a neutral line ready: different climate, design standards and MED method; ranks are indicative. |
| P10 | 3, 8, A1 | "so ranks are indicative" (slide 3) vs "4th of 12 peers" (slide 8) | The rank depends on the MED rule, and there is no rule-free (all-events) check. The caveat is dropped on the closing slide. | Medium | Add an all-events SAIFI rank line; carry "indicative" to slide 8. |
| P11 | 4 | Map "Minutes per customer", "Pittsylvania 633" + footer "start with the counties that lose the most minutes on ordinary days" | All-utility EAGLE-I minutes (about 71% of the shaded area is at 250 or more a year, measured from the render) are roughly 2–5× Dominion's ex-MED SAIDI (≈134 average over 2015–24). That steers Dominion toward counties whose minutes may belong to co-ops or other IOUs. "Non-major day" is undefined for EAGLE-I, and the legend has no "per year". | **High** | Restrict the map to Dominion-only counties, or title it "all utilities, not Dominion's SAIDI". Drop the "start with the counties" instruction. |
| P12 | 4 | Three visuals: 11.9× ratio, choropleth, Isaias inset | Three units (customer-hours per 1,000 customers; minutes per customer; % restored) and three windows (2015–25; 2015–24; Aug 2020). The inset doesn't support the title. Too much for 75 s. | **High** | One message, one visual: 11.9× with storm and calm levels, the robustness line and the caveat. Move the map and inset to the appendix (A6 already carries Isaias). |
| P13 | 4 vs A2 | "6,108 storm county-days, 2015–2025" | A2's storm county-day column sums to **6,530** for the same years. The gap is unexplained (99 vs 103 counties? EAGLE-I gaps?). | Medium | Reconcile and footnote the reason, or use one figure. |
| P14 | 4 | "(95% CI 7.9–16.9)" | The method and resampling unit aren't stated. County-days hit by the same storm aren't independent; resampled by county-day, the interval is too narrow. | Medium | Footnote "bootstrap by date (or storm)". If that isn't what was done, redo it or drop the CI. |
| P15 | 4 | "County-days with a storm report" | Many NOAA entries (thunderstorm wind above all) are logged from damage reports of trees and lines down. That partly selects on outages and inflates the ratio. | Medium | Add "storm reports are often damage-based" to the caveat; keep "association". |
| P16 | 4 (print) | Choropleth classes | Greyscale levels are 221 / 173 / 124 / 80 / 59. The two darkest classes (80 vs 59) are near-identical on paper, and "under 150" (221) is close to the white non-territory counties. The two darkest blues are close even in colour. | Medium | Four classes with wider steps; outline the territory; label two or three counties directly. |
| P17 | 4 | "Dominion-only counties (19.9×)" | The ratio inflates when the calm-day baseline is small (dense, well-served counties), and it hides the levels. | Low | Show storm and calm levels next to the ratio. |
| P18 | 5 | "For Dominion: less overnight slack and winter peaks: plans and reports built around summer afternoons need updating." | Tells Dominion's planners their plans are out of date, using zone data the footnote admits is wider than the territory. Too grand for this level. | **High** | "For reporting: I'd add winter and overnight views to load and outage dashboards." Or make it a question. |
| P19 | 5 | Whole slide | Load growth isn't a Grid Resiliency or reliability measure, and no link is drawn. It opens the data-centre attribution debate the deck can't settle (A5). | Medium | Link it in one line: per A6, the two winter storms took about 100 h to reach 90% restored, against 20–66 h for the other eight, and winter is now peak season. Or move the slide to the appendix. |
| P20 | 5 | "2026 to 29 Oct: 25,413 vs 25,384 MW" | Doesn't say which figure is winter. A 29 MW (0.1%) gap is a tie within data-revision noise. | Low | "2026 so far: winter 25,413 vs summer 25,384 MW, a tie". |
| P21 | 5 | "Peak hour +26%, lowest hour +52%."; "hours ending 1–5 a.m." | Undefined (annual highest and lowest hourly load?), "hour ending" is grid jargon, and the line is set in light grey. | Low | "Highest hour of the year +26%, lowest hour +52%". |
| P22 | 6 | "Restoration timed from meter “last gasp” (99.8% of meters are smart)." | A last gasp marks power loss, the *start*. The end needs the restore message or a ping, and OMS is the system of record. Last gasps drop in big storms when collectors lose power. The EIA-861 AMI file behind the 99.8% isn't in A4's register. | Medium | "Outage start and end from meter last-gasp and restore messages, checked against OMS times." Add the AMI file to A4. |
| P23 | 6 | "repeat interruptions (CEMI)" | Undefined acronym, and CEMIn needs an n. | Low | "customers with more than n interruptions (CEMIn)". |
| P24 | 6 | "Prioritise and track … track … mainfeeder hardening against similar untreated feeders and weather." | Right idea, but it misses the trap. Hardened feeders are chosen for bad history (Dominion's published rule), so they regress to the mean, and "similar" must mean matched on the pre-period. "Prioritise" also implies decision rights an analyst won't have. | Medium | "…against matched untreated feeders (same pre-period performance), weather-normalised"; "support the programme's selection rule". |
| P25 | 7 vs A4 | "12 tests pass" vs "T1–T12 … T13–T31 … (all pass)" | 12 or 31? An inconsistency on the slide about testing. | Medium | "31 tests pass (12 on the reliability mart)". |
| P26 | 7, A4, A6, 6 | Pipeline shows three sources; A4 title "Every number traces to a public source and a tested query" | EAGLE-I (11.6M rows, the largest, behind slide 4 and A6) and the EIA-861 Service Territory file are missing from the pipeline. HURDAT2 (A6) and the EIA-861 AMI file (slide 6) are missing from the register. | Medium | Add EAGLE-I to slide 7 and the missing sources to A4, or soften A4's title. |
| P27 | 7 | Title "Built like governed production reporting" | No owner or steward, access control, change control, refresh schedule or monitoring is shown, and it is a personal project. | Medium | "Built with production habits: tested, documented, reconciled". |
| P28 | 7 | "13 of 13 rebuilt values match the published figures, such as 133.0 vs 133" | The 13 aren't listed. Matching Dominion's average of Dominion's own filings checks definitions (ID, state row, MED flag, averaging convention), not truth. | Medium | List the 13 in a footnote or on A4. Describe the check as "confirms definitions and filters". |
| P29 | 7, whole deck | "Power BI: Import model and report" is the only Power BI content | The posting's first responsibility is Power BI, yet there is no report page, model view or measure anywhere, and nothing shows which tool drew the charts. | **High** | Add a report screenshot and the star schema (an appendix slide is enough), and name two or three DAX measures. |
| P30 | 8 | "I build governed Snowflake → Power BI reporting, and I've already started learning your reliability data." | A present-tense professional claim. The resume's job bullets show Snowflake (Mercury) and Tableau (two employers); Power BI appears only in the summary and skills. "Your reliability data" can be heard as internal data. | **High** | "I've built a tested Snowflake → Power BI pipeline on your public reliability filings." Claim Power BI at work only if true. |
| P31 | 8 | "Root-cause analysis on joined data → SAIFI by cause" | The other arrows point to things that exist (the mart, 133.0, the dictionary). There is no SAIFI by cause in the deck, and it can't be built from public data (A5). | Medium | "→ SAIFI by cause, with your outage records (days 31–60)". |
| P32 | 8 | Whole slide | 143 words and 22 numbers: three numeric takeaways, a claim, five mappings and a close. Too much for 75 s. | Medium | Takeaways without the numbers (already shown), three mappings, one closing line. |
| P33 | A1 | "IEEE 1366 marks a day … threshold set from the previous five years of daily SAIDI (the “2.5 beta” method)" | Leaves out the log step (T_MED = e^(α+2.5β) on ln daily SAIDI, zero days dropped). Fine on a slide; risky if that is the depth of knowledge. | Low | Add the formula in small type. |
| P34 | A1, 3 | "Dominion reports to EIA under its own major-event rule" | The rule is never stated, and the engineer will ask. | Medium | State it in one line with its source, or say "non-IEEE ('Other' in EIA-861)" and what that implies. |
| P35 | A2 | "2025 was left out: the fit gives 145.3, the actual was 144.4." | With n = 10 and residual SD ≈9 min, the 95% prediction interval is ≈122–168. A near-hit is weak validation that reads as precise. | Medium | "Fit 145 (95% PI ≈122–168); actual 144.4". |
| P36 | A2 | "Fit on 2015–2024 (n = 10) … r = 0.70" | The 95% CI on r is ≈0.12–0.92. Dropping 2020 gives r = 0.83; dropping 2019 gives 0.57. Fragile, though labelled exploratory. | Low | Quote the interval; keep "exploratory". |
| P37 | A2, A3 | "Adjusted for storm days, no clear trend since 2015 … (95% range −1.4 to +2.1)" | Why 2015, when storm data is loaded from 2013 (A4)? 2013 and 2014 were the two lowest ex-MED years on A3 (≈106, ≈112), and a 2013 start roughly triples the raw slope (≈+2.0 vs ≈+0.6 min a year, chart-read). The range allows about 20 minutes a decade: "no clear trend" means "can't tell". | Medium | State why 2015 (if it aligns with EAGLE-I, say so) and show the 2013-start result. Write "not distinguishable from zero". |
| P38 | A3 | "Major-event minutes swing most: 285 in 2022, 41 in 2024." | 2014 reads ≈40 on the same chart, so 41 isn't clearly the low. | Low | "from about 40 (2014, 2024) to 285 (2022)". |
| P39 | A4 | "SAIDI = SAIFI × CAIDI within 2%" | Why 2%? What fails at 1%? A BI manager will ask. | Low | Footnote the reason (rounding in utility-reported values) and how many rows fail. |
| P40 | A6 | "Customers out, held 1 hour"; "Hours from the peak"; "16 Feb 2025 Wind" plus "merges two storms" | The metric is undefined. Restoration is measured on all utilities' net customers out from the peak, not as "% of affected customers restored" the way utilities report it. The merged Feb 2025 event has 8.2m customer-hours (≈47 h per peak customer) against 20.3 h to reach 90%, and is typed "Wind". | Medium | Define "held 1 hour" and the restoration basis; split the Feb 2025 event or explain it. |
| P41 | whole deck | "For Dominion:" footer on all seven content slides | Consultant cadence. Slides 2, 3 and 5 prescribe company priorities, and slide 7 implies Dominion's reporting needs "the same discipline". | Medium | Rename the footer "What I'd check" and phrase each line as a question. |
| P42 | whole deck | IEEE 1366, PJM, PUDL, EAGLE-I, CI, CEMI, county-days, customer-hours, hour ending, RAW/STG/MART | Undefined acronyms and jargon on the main slides lose the HR panellist. | Medium | Define each on first use or say it aloud; keep the main slides to about three acronyms. |
| P43 | whole deck | Windows: 2022→2025, 2021–25, 2015–2025, 2019→2025, 2023→2025 (A1), 2015–2024, 2013–2025, Nov 2014–2025 | Eight windows and no stated rule, which invites "cherry-picking". | Medium | One footnote: each window is set by data availability or by Dominion's 3-year convention. Align A1 with slide 2. |
| P44 | whole deck | "programme", "Prioritise", "licence", "3 November 2026" | British spelling and date style for a US panel and a posting that says "programs". | Low | US spelling and "November 3, 2026". |
| P45 | whole deck (print) | Letter print | Content fills 66% of the page height (16:9 letterboxed on letter). Source lines are 10.1 pt mid-grey, and the protective caveats ("Methods differ…", "EAGLE-I counts every utility…", "not a storm attribution") are set in the same light grey, so they read as fine print. | Low | Set the caveats in body colour; print 2-up portrait, or use the margins for a takeaway. |
| P46 | 2–5 vs A1–A6 | No pointers from the main slides to the appendix | The handout reads as two halves: slide 2 never cites A1 or A2, and slide 4 never cites A6. | Low | Add "(see A2)"-style tags. |
| P47 | A6 vs 5 | Winter events reach 90% restored at 101.5–102.8 h, against 20–66 h for the other eight | The most role-relevant restoration finding (only two events) is buried and never tied to slide 5's winter peaks. | Low | One line on slide 5 or 8, flagged as two events. |

**Counts:** High **7** (P1, P2, P11, P12, P18, P29, P30) · Medium **25** · Low **15** · 47 items.

**What is clean (said fairly):**
- **Every main slide has a source line**, and the title says "Independent analysis of public data". Slide 6's source line says no Dominion data was used. Apart from P30's "your reliability data", nothing implies internal access.
- **Slide 2's arithmetic is right:**
  - the 3-year means come out at 130.2 and 133.0
  - the changes are +6%, +10% and −4%
  - 1.320 × 109.4 = 144.4
- **A2's fit recomputes exactly.**
- **The caveat language is careful:**
  - slide 8 calls the storm ratio "an association"
  - A2 calls itself exploratory
  - A3 says "not a storm attribution"
  - A5 is the most credible page in the pack

---

## 3. Win the room / lose the room

**Most likely to win it**

1. **Slide 7, how it was built.**
   - **Why:** it is the posting in one picture. Responsibilities 5, 6 and 8 (definitions, metadata, data-quality controls, validation and reconciliation, automated pipelines) become visible things: RAW/STG/MART in Snowflake, tests, a data dictionary, a decisions log fixed before results, and a reconciliation to the number Dominion reports. It is the BI manager's slide, and A4 backs it.
   - **Keep the win:** say "31 tests", put EAGLE-I in the diagram, and change "governed production" to "production habits".
2. **Slide 6, the 90-day plan.**
   - **Why:**
     - It speaks the team's language: reconcile to the filed figures, cause codes and vegetation, CEMI, mainfeeder hardening against untreated feeders, a Power BI programme-tracking report on a schedule.
     - It starts with reconciliation, not recommendations.
     - Its source line says no Dominion data was used.

     It answers "what would you do here?" before anyone asks.
   - **Keep the win:** fix the last-gasp sentence, define CEMI, and add "matched on the pre-period".
3. **Slide 3, peers.**
   - **Why:** one clean chart, one answer, and the method caveat on the slide. The frequency gap (1.21 against a median of ≈0.93–0.96) is big enough to survive the median quibble, and it gives "frequency first" firmer ground than 2025 does.
   - **Keep the win:** say 11 peers, take Dominion out of the medians, have the all-events rank ready, and don't narrate FPL.

Best page not presented: **A5 (limits)**. It does more for trust than any other page; promote one line of it to slide 6.

**Most likely to lose it**

1. **Slide 4, storms and map.**
   - Three visuals, three units and three windows.
   - County minutes from all utilities, running 2 to 5 times Dominion's system figure.
   - A "For Dominion: start with the counties…" instruction on top.

   The engineer can take it apart with one question, and it is also the slowest slide to present.
2. **Slide 2, the opener.**
   - Its first claim ("because … not longer") is contradicted by the deck's own A1, which uses a different base year.
   - It is undercut by A2: 2025 sits on the storm line, with no storm-adjusted trend.
   - If the engineer lands that in minute two, everything after is heard sceptically.

   Fix the title and add one line ("2025 was a storm year; see A2") and it turns into a win.
3. **Slide 5, load shape.**
   - It is off the Grid Resiliency brief.
   - It pulls the room into data-centre load growth the deck can't attribute (A5).
   - It uses zone data wider than the territory.
   - It closes by telling Dominion its plans need updating.

Runner-up: **slide 8**. It is dense, has a "SAIFI by cause" arrow to something that doesn't exist, and makes a present-tense Power BI claim the resume's job history doesn't show.

---

## 4. Timing

**Can the 8 main slides be presented in 10 minutes as they stand? Not reliably.** The estimates below assume a brisk ~140 words a minute and only what is needed to explain each slide's content.

| Slide | What has to be said | Words / numbers on slide | Seconds needed |
|---|---|---|---|
| 1 Title | who, what, public data only | 35 / 4 | 20 |
| 2 Minutes 130 → 133 | 3 hero pairs, 3 bars, SAIFI line, takeaway | 73 / 17 | 95 |
| 3 Peers | scatter axes and quadrants, 2 stats, caveat | 71 / 10 | 70 |
| 4 Storms | ratio and CI, robustness, caveat, map, inset | 72 / 11 | 110 |
| 5 Load shape | "hour ending", 2 stats, winter peak, note | 70 / 18 | 75 |
| 6 First 90 days | three phases and deliverables | 132 / 7 | 80 |
| 7 How built | pipeline, 4 boxes | 118 / 13 | 80 |
| 8 Close | 3 takeaways, claim, 5 mappings, close | 143 / 22 | 85 |
| **Total** | | **714 words / 102 numbers** | **≈615 s ≈ 10 min 15 s** |

That has no slack and assumes no interruptions. Panels usually interrupt on slide 2 or slide 4, so expect 11–12 minutes in the room.

**Cut or simplify, in this order:**

1. **Cut slide 5 to the appendix first** (saves ≈75 s).
   - It is the slide least connected to Grid Resiliency.
   - It carries a High tone item (P18).
   - Its takeaway on slide 8 can shrink to a clause or go.
2. **Simplify slide 4 to one visual** (saves ≈35 s). Keep 11.9× with storm and calm levels, the robustness line and the all-utilities caveat. Move the map and inset to the appendix.
3. **Trim slide 8's repeated numbers and slide 2's duplicate hero line** (saves ≈30 s).

That brings the talk to ≈8 minutes, leaving about two minutes for the question that will come anyway.

---

## Checks behind this review

- **Slide 2:**
  - (136.0 + 123.3 + 131.3) / 3 = 130.2 and (123.3 + 131.3 + 144.4) / 3 = 133.0
  - the changes are +6.2%, +10.1% and −3.6%
  - 1.199 × 113.5 = 136.1 and 1.320 × 109.4 = 144.4
  - all match the slide
- **Log split:**
  - 2022 → 2025: ln SAIDI ratio 0.060, ln SAIFI ratio 0.096, so ≈160% of the rise is from frequency.
  - 2023 → 2025 (A1): 0.125 / 0.158 = 79%, which implies 2023 SAIFI ≈1.165 and CAIDI ≈105.8, so CAIDI rose 3.4% to 2025.
- **A2:**
  - The refit is SAIDI = 104.2 + 0.0519 × storm county-days, with r = 0.697 and R² = 0.486. It matches the slide.
  - Residual SD is 8.7, so the 2025 prediction interval is ≈145 ± 23.
  - r's 95% CI is 0.12–0.92 (Fisher). Leave-one-out r runs from 0.57 (drop 2019) to 0.83 (drop 2020).
  - The 2015–24 ex-MED SAIDI values have mean 134.0 and SD 11.4.
- **Storm county-days**, 2015–2025, summed from A2's column: 6,530. Slide 4 says 6,108.
- **Slide 4 map (pixel count on the render):** the shaded area splits 11.5% under 150, 17.1% at 150–250, 26.2% at 250–350, 21.3% at 350–500 and 23.9% at 500+.
- **Slide 3 (chart-read):** the 12-point medians are 0.96 and 105, matching the slide. With Dominion removed they are ≈0.93 and ≈99. Dominion ranks 4th-highest on SAIFI and 6th-longest on CAIDI.
- **A3 (chart-read):**
  - ex-MED SAIDI ≈106 in 2013 and ≈112 in 2014
  - MED minutes in 2014 ≈40
  - the raw ex-MED slope is ≈+2.0 min a year for 2013–25 and ≈+0.6 for 2015–25
- **A6:** customer-hours per peak customer run from 9 to 61 h. The Feb 2025 event is ≈47 h against 20.3 h to reach 90%. The winter events reach 90% at 101.5–102.8 h.
- **Slide 5:** 25,413 − 25,384 = 29 MW, a 0.11% gap.
- **Print:**
  - Content occupies 104–508 pt of each 612 pt page height (66%).
  - Text is 10.1 pt for source lines and 12 pt for body text, with the caveats in #6b7280.
  - The charts are ~400 dpi rasters, so they stay sharp in print.
  - Greyscale on p04: the legend classes read 221, 173, 124, 80 and 59.
  - Greyscale on p02: the bars read SAIDI 42, SAIFI 100, CAIDI 188.
