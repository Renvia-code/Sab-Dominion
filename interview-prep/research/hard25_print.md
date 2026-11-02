# The 25 hardest questions: print version

*Agent R · 2026-11-01 09:44 · for B: the version to print in the brief's appendix, sized for about two pages. It
compresses `research/hard25_answers.md`, which keeps the full cues, every locator, the variant notes and the N-number
sources. If a number changes, edit both files. Print from "Key" down.*

**Key**
- **C** = claim, **P** = proof, **L** = honest limit.
- ● = the brief requires it.
- *Adopted* = depends on adopting the repo upgrade; *Public-only* = the fallback line.
- `[you: …]` = only you can fill it.
- Ids point to the brief's "know every number" table and the repo docs (D = decision, P = data-quality note, T = test).

## Engineer

**Q1 ● Weather fit.** *"Ten points: what's the interval on r, the 2025 band, and why start in 2015?"*
- **C:** Thin, so it's an appendix check, not the headline.
- **P:**
  - r = 0.70, p = 0.025, 95% CI for r 0.12–0.92 [C-S4-15].
  - 2025: fit 145.3 vs actual 144.4, inside a band of about 122–168 [N-1].
  - The fit starts in 2015 because that's when outage recording became automated (D6) [N-2].
- **L:** Say "can't tell", not "no trend".
  - *Adopted:* the weather-adjusted slope range is −1.4 to +2.1 min/yr [C-S4-06]; storm county-days 464 → 791.
  - *Public-only:* r 0.70 on ten years; 465 → 796; no p.

**Q2 ● Major event days.** *"What's an MED, and why exclude it? What's Dominion's rule? Dominion vs FPL?"*
- **C:** An MED is a day so far above normal that it would swamp the year. Excluding MEDs shows everyday performance;
  storms are judged as storm response.
- **P:**
  - **2.5β:** the logs of five years of daily SAIDI; the threshold is T = e^(α+2.5β) [R-070].
  - **2025:** MEDs were 53% of all-event minutes (306.7 vs 144.4) [C-A3-01].
  - **Dominion's method:** it files under its own rule ("Other"); 10 of the 12 utilities use IEEE [N-5].
  - **All events:** Dominion's SAIFI ranks 6th of 12, against 4th ex-MED [N-3].
- **L:** "I don't know the written rule; I'd ask the reliability team." Ranks are indicative.
  - FPL: compare like with like (all events) and make no comment on the merger.

**Q3 ● County data** (*Adopted*). *"It counts every utility in a county. Whose minutes? Would you send crews by it? 90% of what?"*
- **C:** Right. It isn't Dominion's SAIDI, and I wouldn't target work with it.
- **P:**
  - **The county rule:** EIA-861 lists 103 Dominion counties, 33 of them Dominion-only (D15). The result holds in the
    Dominion-only counties (19.9×) [C-S4-09].
  - **Blank readings:** failed collection runs, never counted as zero (P20).
  - **Isaias:** 90% of the peak number out, all utilities, timed from the peak [C-S4-12].
- **L:** Targeting needs your outage records by feeder.
  - *Public-only:* there's no county outage data; NOAA's county reports carry the same caveat.

**Q4 Anything to explain?** *"130 → 133 is 2.8 minutes. Is it real? More frequent, or longer?"*
- **C:** 2025 was a stormier year with more interruptions. There's no clear underlying trend.
- **P:**
  - **The 2.8 minutes:** (144.4 − 136.0) ÷ 3, because 2025 replaced 2022 in the window [C-S2-03]. Single years have
    ranged from 117 to 150 [C-S4-05].
  - **2022 → 2025:** SAIFI +10%, CAIDI −4% [C-S2-05, C-S2-07]; storm county-days 718 → 791 [C-S2-16].
  - **Dominion's own reading:** "primarily due to increased storm activity" [C-S2-15].
- **L:** CAIDI is a ratio, not a measure of restoration speed.
  - *Adopted:* trend p-values 0.54 / 0.74 / 0.58 [C-S2-13].
  - *Public-only:* storm county-days 723 → 796; "no clear trend".

**Q5 The 12×** (*Adopted*). *"Isn't 12× circular, when storm reports come from damage? What's the unit of the CI?"*
- **C:** Partly, yes. It's an association, inflated by how storm reports are made.
- **P:**
  - **The levels:** 333 vs 27.9 customer-hours per 1,000 customers = 11.9× (7.9–16.9) [C-S4-08, N-6].
  - **The interval:** bootstrapped by whole days.
  - **It holds:** on non-major days (9.9×), in Dominion-only counties (19.9×) and in every year [C-S4-09].
  - **6,108 vs 6,530:** complete EAGLE-I days in 99 counties vs all NOAA days in 103 [N-7].
- **L:** The next test is weather measured independently of damage, such as wind gusts.
  - *Public-only:* the annual version, r 0.70.

**Q6 Meters.** *"What does a last gasp tell you? Could 2025's SAIFI be a measurement change?"*
- **C:** A last gasp marks when the outage starts, not when it ends. I can't rule out a measurement effect from public
  data.
- **P:**
  - 99.8% of meters are AMI [C-S6-01].
  - The end time needs a restore message or a ping, and the outage system stays the record.
  - Last gasps drop out when collectors lose power.
  - Recording became automated in 2015 (D6).
- **L:** Check first: roll-out timing against SAIFI, and circuits before and after their meter cut-over.

**Q7 Cause codes.** *"What will our cause codes show, vegetation especially? What goes wrong?"*
- **C:** It needs your outage records: a 30–60-day deliverable.
- **P:**
  - Expected causes: vegetation, equipment, weather, animals, vehicles, unknown.
  - Split blue-sky days from storm days, and use CEMIn for repeat outages.
  - Dominion trims on 4–5-year cycles [R-076].
- **L:** The data traps:
  - the cause is coded when the job closes
  - one device can hit many customers
  - the "unknown" share is itself a KPI

  Agree the definitions with engineering first.

**Q8 Hardening.** *"The worst feeders improve anyway. How would you know it's the program?"*
- **C:** A plain before-and-after overstates the effect (regression to the mean).
- **P:**
  - **Selection rule:** at least 500 customers, more than 2 minutes worse, over 5 years [C-S6-03].
  - **Reported results:** −32% (2023) [C-S6-02] and −44% (2026) [R-013].
  - **Design:** matched feeders with a pre-period, difference-in-differences, storm-normalized, reported with
    intervals.
  - **My experience:** the A/B test at Mercury [resume: Mercury b4].
- **L:** Frame it as making a good result harder to challenge, not as doubting it.

**Q9 ● Why EIA.** *"Why public EIA data and not the SCC filings?"*
- **C:** It's public, consistent across utilities, and it reproduces Dominion's own numbers.
- **P:**
  - Every utility files the same federal form, by state [R-072].
  - Virginia data gives 130.22 / 133.01 against the reported 130 / 133 [C-S2-17].
  - The SCC docket site blocked automated access, and its report to the Assembly shows the indices only as charts
    [R-020].
- **L:** Methods differ (Dominion files as "Other"), so ranks are indicative. The filed SCC report is the first thing
  I'd reconcile to.

**Q10 ● Data centers.** *"Did data centers cause the demand growth?"*
- **C:** Public data can't show that, and I don't claim it.
- **P:**
  - **The load shape, 2019 → 2025:** overnight +39–41% vs afternoon +27% [C-S5-01]; winter peaks [C-S5-02].
  - **Sales:** commercial sales +65% on 8% more customers [C-S5-07].
  - **Dominion's account:** 744 MW of data centers connected in 2025, and over 54 GW in contracting stages
    [R-040, R-054].
- **L:** The zone is wider than the territory and EIA has no customer IDs. Attribution needs meter data (D14).

## BI manager

**Q11 ● The model.** *"Walk me through the model and the year slicer, 3-year SAIDI and the roll-up."*
- **C:** A small star schema; every number comes from a customer-weighted measure.
- **P:**
  - **Tables:** FCT_RELIABILITY (utility × state × year) → DIM_UTILITY.
  - **Year slicer:** a disconnected 'Dashboard Year' table read with SELECTEDVALUE (default 2025) plus CALCULATE.
  - **3-year SAIDI:** the mean of the annual values (AVERAGEX), Dominion's convention [C-S2-02].
  - **Roll-up:** Σ customer-minutes ÷ Σ customers.
- **L:** DirectQuery while developing, Import to present (D13).
  - *Adopted, after the guide:* folder-parameter Import, so it opens offline.

**Q12 Power BI at work.** *"Where have you used Power BI at work? And Power Apps?"*
- **C:** `[you: the exact truth]`. If it's only this project, say so.
- **P:**
  - **At work:** Tableau [resume: Life Initiative b1; Cofoods BD b1]; Snowflake SQL [resume: Mercury b1].
  - **Power BI depth:** this model (Q11).
- **L:**
  - **Power Apps:** "not in production" `[you: …]`, plus a 30-day plan (an exceptions form).
  - **SharePoint:** skills line only `[you: …]`.

**Q13 Reconciliation.** *"133.0 vs 133: what did that prove? Which values?"*
- **C:** It shows I use the same definitions and filters as Dominion. It doesn't show the data is true.
- **P:** 12 values [C-S7-11]:
  - two 3-year averages vs the annual report
  - nine 2024–25 values vs EIA's files
  - 2025 commercial sales

  It confirms the row, the MED flag, the averaging, the vintage and the customer base. Tests run after every load
  [C-S7-10].
- **L:** It's a definitions check. A real reconciliation runs from outage events to daily SAIDI to the filed figure,
  with a written bridge.
  - *Public-only:* 130.2 / 133.0 vs 130 / 133; tests T1–T12.

**Q14 Governance and regulators.** *"What does 'governed' mean? Any regulatory reporting? Why doesn't your dashboard
SAIDI match the filed number?"*
- **C:**
  - **Experience:** `[you: the truth; no job bullet shows a filing]`.
  - **Governance:** owned definitions, change control, and checks that block bad data.
- **P:**
  - **What it takes:** a versioned glossary, sign-off, lineage, access rules, alerts.
  - **What I've done:** definitions written up for reuse [resume: Mercury b6]; the board's dashboard
    [resume: Life Initiative b1].
  - **Filed vs dashboard:** the filed number anchors. Write the bridge (population, MED rule, customers, vintage) and
    keep as-filed and revised versions side by side.
- **L:** The project has a decisions log, a dictionary and tests, but no owner or monitoring. Say so.

**Q15 EAGLE-I in SQL** (*Adopted*). *"How do 15-minute snapshots become events and customer-hours? What about
missing data?"*
- **C:** It's in the same SQL build, under tests T13–T31 [C-S7-10].
- **P:**
  - **Customer-hours:** Σ customers out × 0.25.
  - **Events:** gaps-and-islands (LAG, then a running SUM).
  - **"Held 1 hour":** the minimum of four readings.
  - **Time:** Eastern Standard Time all year.
  - **Bad data:** blanks are NULL, not zero (P20); impossible readings are NULL (P24).
  - **Size:** 11.6M rows [C-S7-12].
- **L:** Coverage grows over time, so compare a county with itself. There's no stuck-count rule yet.
  - *Public-only:* describe it as how you would do it.

**Q16 Mercury pipeline.** *"The 20M-row Snowflake pipeline: grain, loads, and which part was yours?"*
- **C:** `[you: what it fed and what you owned]`.
- **P:**
  - Policy, claims and billing data (20M+ rows) for the pilot [resume: Mercury b1].
  - `[you: the grain, incremental logic, scheduling, tests, one failure]`
- **L:** Claim only your part. Bridge: outage events → daily → annual indices.

**Q17 Real reconciliation.** *"That's model evaluation. Give me a real reconciliation. Were the sales lift and the
settlement cut yours?"*
- **C:** Evaluation and reconciliation are different, and I keep them apart.
- **P:**
  - **Evaluation:** a 150-question test set, 71% → 90% [resume: Mercury b3].
  - **At work:** `[you: one true break → cause → control]`.
  - **In the project (P18):** a co-op with SAIDI but no SAIFI would have diluted the group figure (1.849 vs 1.887).
    Fixed 27 Oct [N-8].
- **L:** Causal only where there was a control: the A/B test, +9% [resume: Mercury b4]. Elsewhere, "contributed to"
  [resume: Mercury b2; Cofoods BD b1].

**Q18 ● Do differently.** *"What would you do differently?"*
- **C:** Set rules before seeing results, as I did for the peer set (D10).
- **P:**
  1. Test aggregates for missing values first (P18).
  2. Show the all-events view beside ex-MED: the rank moves from 4th to 6th [N-3].
  3. Set one stated rule for windows and base years.
- **L:** `[you: one personal lesson]`. Never tell an upgrade change as a discovery story.

## HR

**Q19 Why move.** *"Why leave Mercury after seven months? Why a utility?"*
- **C:** `[you: the real reason, as a pull]`. One neutral line on Mercury.
- **P:**
  - **The Grid Resiliency programs:** Mainfeeder Hardening, Voltage Island Mitigation, Voltage Optimization,
    Intelligent Grid Devices/FLISR [R-035].
  - `[you: which one, and why]`
  - **My project:** rebuilt Dominion's numbers [C-S2-02].
- **L:** Never criticize Mercury.

**Q20 Three years.** *"'Three years of BI', but your data titles add up to under a year. And the Associate level?"*
- **C:** Here's how it adds up [N-9]:
  - **Data titles:** about 10 months (Mercury 7, Life Initiative 3).
  - **Analytics inside other roles:** about 28 (Cofoods BD 19, with the forecasting model and Tableau dashboards;
    finance internships about 9).
  - **Total:** about 38 months since April 2022, plus the MS.
- **L:** "Three years" counts all work, internships included; don't stretch it. Open to either level; earn the step up.

**Q21 Pushback.** *"Someone senior said your numbers were wrong. And our engineer's pushback?"*
- **C:** Listen, check, fix the source, document it, thank them.
- **P:**
  - `[you: a true STAR story; the resume has none]`
  - **Live:** "You're right, it counts every utility. I'd relabel it or cut it to Dominion-only counties." (Q3)
- **L:** Experts own the definitions; the analyst owns reproducibility.

**Q22 Least sure.** *"Which number are you least sure of? And what do you say when you don't know?"*
- **C:** Name one, and say why.
- **P:**
  - **Candidates:** the weather fit (CI 0.12–0.92) [C-S4-15]; Dominion's MED rule (Q2); *adopted:* the county minutes
    (Q3).
  - **"I don't know":** "Here's where I'd find out, and I'll come back by [time]." `[you: a time you did this]`
- **L:** Doubt builds credibility only when the fix comes in the same breath.

**Q23 Merger.** *"How do you feel about joining during the NextEra merger?"*
- **C:** Calm. Reliability work carries on, and integrations need exactly this definition work.
- **P:**
  - **Timeline:** Virginia's order is due by mid-January 2027; SC, NC, FERC and NRC approvals follow; close is expected
    in H2 2027 [C-Q-10].
  - **The company says** Dominion Energy Virginia stays separately regulated [C-Q-11].
- **L:** No view on the deal or on jobs, and no comment on FPL. Ask how priorities may shift.

**Q24 Thirty seconds.** *"No acronyms: what did you find?"*
- **Say:** "In 2025 the average Dominion customer in Virginia lost power about 1.3 times, for about an hour and fifty
  minutes each time: almost two and a half hours in the year, leaving out a few extreme storm days. The three-year
  average rose about three minutes, mostly because 2025 was stormier. Once storms are counted, there's no clear trend.
  This job is about showing clearly whether the programs that prevent outages are working." [C-S2-04, C-S2-06,
  C-S2-03]
- **L:** Stop at thirty seconds.

**Q25 Unglamorous work.** *"How do you recommend things without overstepping? Are you happy doing routine reports?"*
- **C:** Yes. Accurate recurring reports are the job.
- **P:**
  - **Habits:** write-ups for reuse [resume: Mercury b6]; handover notes [resume: Life Initiative b2]; the project's
    dictionary and decisions log.
  - **Raising ideas:** as questions, with the data, checked with the owners, and credit to them.
- **L:** Learn the planning context before recommending.
