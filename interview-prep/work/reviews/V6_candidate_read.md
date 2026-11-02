# V6: the candidate's read of the v3 pack

**Reviewer role:** the candidate, studying on Monday 2 November for the Tuesday 3 November panel.
**Read in START_HERE's order:** START_HERE → brief (12 pp) → main deck (14 pp, plus speaker notes taken from the .pptx) → public deck (skimmed, plus notes) → question sheet (2 pp) → APPLY_GUIDE → 05_repo README and CHANGES.
**Method:** every PDF page was rendered at 110 dpi into `v6_pages/` and read as an image. Speaker notes were pulled from both .pptx files (`v6_pages/*_notes.txt`). The slide 5 screenshot was zoomed (`v6_pages/zoom_*.png`). When the pack made a claim I couldn't check from the printout, I checked it against the repo, the .pbit model and git. Read-only: the only things written are this file and `v6_pages/`. Nothing was committed or uploaded.

## Verdict

- **The numbers hold.** I found no true contradiction between the deck, the brief and the sheet. Every difference is either a stated version difference (adopted vs public) or a different base year. These all check out: the talk timings (1,028 notes words = 7:54; 994 = 7:38), the placeholder counts (22 and 20), the ranks, the medians, the A2 fit, the 6,530/6,108 bridge and the 53% MED share.
- **What would leave me stuck is not the numbers.**
  1. The adopted version asks me to stand behind work that someone else built with an AI assistant on 1 November. The plan gives me 90 minutes to review 3,700 changed lines, and the pack never gives me one sentence about who built it.
  2. The 42 `[you: …]` items have no slot in the Monday plan.
  3. Some engineer and BI-manager questions are not prepared at all:
     - the 2020 "46 kV lines added" line printed on the report screenshot;
     - proxy major event days;
     - 18 tables but 2 relationships;
     - the report's data actually comes from DuckDB CSVs, not Snowflake.
  4. There is no company page in the pack.

---

## 1. Each main slide, explained back (adopted deck)

For each slide below: what I'd say in about 60 seconds using only the pack, then what I could not explain.

### Slide 1: Title
**I'd say:** "Thank you for having me. To prepare, I rebuilt Dominion Energy Virginia's reported reliability numbers from EIA's public filings. For context I added NOAA storm records, the Department of Energy's EAGLE-I county outage records and EIA's hourly demand. Everything is public: I had no Dominion internal data, and I'll say where public data stops. Three findings, then the Power BI report, how it's built, and what I'd do in the first 90 days."
**Missing:** "PUDL" is on the title's data line and is never expanded anywhere in the pack. The brief names Catalyst Cooperative as the publisher, but nothing says what PUDL is.

### Slide 2: 130 → 133
**I'd say:**
- "Dominion's 2025 annual report gives a three-year SAIDI of 133 minutes for 2023–25, up from 130. SAIDI is average outage minutes per customer, leaving out major event days. The report says the rise is 'primarily due to increased storm activity'."
- "I rebuilt both figures from EIA filings: 130.2 and 133.0."
- "A three-year average moves when one year leaves and another joins. 2025, at 144.4, replaced 2022, at 136.0, and that is the 2.8 minutes."
- "Between those two years, storm county-days rose 10% (718 to 791). Interruptions per customer, SAIFI, rose 10%. Minutes per interruption, CAIDI, fell 4%. So it is frequency, in a stormier year, and the A2 fit puts 2025 on the storm line."
- "Two cautions: 2025's SAIFI only edges 2018's, and its SAIDI is below 2018 and 2019. One year isn't a trend."

**Missing:**
- **"Storm county-day" is never defined in the adopted talk.** It is the first bar on the chart, but neither the slide nor its notes define it. Slide 4 implies a meaning two slides later. The definition (a day with a NOAA wind, winter or tropical storm report in one of the 103 counties) is only in the brief, p. 5. The public deck does define it, in its slide 4 notes.
- "Excluding major events" is never explained in the talk. The explanation is only in deck A1 and brief Q2 (p. 10).
- "Sits on the storm line" depends on A2, which the panel will not have open.
- I could not survive "isn't 2020 a counting change?" (see §2e, item 1).

### Slide 3: Dominion and 11 peers
**I'd say:**
- "Is that unusual? I compared Dominion with 11 large investor-owned utilities in PJM and the Southeast, chosen by EIA ID before I looked at results."
- "Across is interruptions per customer; up is minutes per interruption. Both are 2021–25 averages, excluding major event days."
- "Dominion's interruption length, 110 minutes, is 6th of 12: mid-pack. Its frequency, 1.21 a year, is 4th highest, against an 11-peer median of 0.93."
- "Caveat: Dominion uses its own major-event rule, and most peers use IEEE 1366, so the ranks are indicative. With all events counted, its frequency ranks 6th."
- "Either way, the gap is how often customers lose power. The next question is which causes drive it, and that needs outage records."

**Missing:**
- **Why these 11?** The pack says only "selected by EIA ID before results (D10)". It gives no rule (a size cut-off? why FPL but not Appalachian Power, which also serves Virginia?).
- PJM is never expanded or explained.
- The pack never says plainly that IEEE 1366 is the standard that defines the indices and the 2.5β rule. I had to join deck A1 and brief Q2 myself.

### Slide 4: 11.9×
**I'd say:**
- "Weather is the obvious question, and county data answers it better than annual totals."
- "EAGLE-I, the Department of Energy's county outage record, counts customers out every 15 minutes."
- "On county-days with a NOAA storm report (6,108 of them with complete readings, in 99 counties), outage customer-hours per 1,000 customers averaged about 333. On calm days it was about 28. That is 11.9 times, with a 95% interval of 7.9 to 16.9 from resampling whole days."
- "It holds on non-major days (9.9×), in the counties Dominion serves alone (19.9×) and in every year."
- "Two cautions. EAGLE-I counts every utility's customers, so this isn't Dominion's SAIDI. And storm reports partly follow damage, so it's an association, not a cause."
- "Report reliability next to storm exposure, so a stormy year isn't read as a trend."

**Missing:**
- **"Non-major days": whose major days?** Dominion's major event day (MED) dates are not public. The repo uses *proxy* MEDs: 2.5β applied to daily EAGLE-I customer-hours across the 103 counties (decision D18, `docs/04`). The word "proxy" appears nowhere in the pack, and an engineer will ask.
- **Why resample *whole days*?** Counties on the same day are not independent. Neither the deck nor the brief says this.
- "99 counties on the map": the deck has no map. The map is only in the brief, p. 5.
- **I can't reproduce 11.9× myself on Monday.** `storm_vs_calm_ratio.py` needs README step 4 (about 3 GB) and `run_local_duckdb_sources.py`, and START_HERE marks both "if time allows".

### Slide 5: The Power BI report
**I'd say:**
- "The role's first duty is Power BI, so here's the report. It has 11 pages, one question each: summary, scorecard, what moved, weather, fair comparison, outages by county, storms, growth, demand, and data notes with the 31 tests and 12 reconciled values."
- "The core is a star: one fact table at utility × state × year, many-to-one to a utility dimension."
- "Measures are customer-weighted: sum the customer-minutes, sum the customers, divide once."
- "The KPI cards follow a disconnected year table through SELECTEDVALUE and CALCULATE, so the slicer sets the cards without filtering the trend charts."
- "Eighteen tables import from CSV exports through one DataFolder parameter, so it opens with no network. The same model could carry a program-tracking report."

**Missing:**
- **The slide says 18 tables but shows 2.** The template has 18 imported tables, 2 calculated tables and only 2 relationships: FCT_RELIABILITY→DIM_UTILITY and RESTORATION_CURVE→OUTAGE_EVENTS_TOP10. The other 16 tables stand alone. START_HERE tells me to print the model view for Q11, and that printout will contradict "a small star schema". The pack gives me no line for this.
- **The screenshot shows "2020: 46 kV lines added"** on both trend charts (zoomed: `v6_pages/zoom_deck_s5_screenshot.png`). It is also on brief p. 7. Nothing in the pack explains it.
- The screenshot's chart titles use 2019 as the base (SAIFI "+6%", CAIDI "−9%"), while slide 2 uses 2022 (+10%, −4%). The pack gives no line that bridges them.
- The screenshot text is about 4 pt at print size, so it is unreadable on the panel's copies.

### Slide 6: How it's built
**I'd say:**
- "Four public sources land in Snowflake as raw text, exactly as published. A staging layer types and cleans them, and a mart of facts, dimensions and views feeds the report."
- "Thirty-one tests pass. Twelve are on the original build: no duplicate keys, SAIDI = SAIFI × CAIDI, and 2025 matches EIA's published values. Nineteen are on the new tables."
- "There's a data dictionary, measures defined in the metrics guide, and a decisions log, D1–D22. The peers were fixed by EIA ID before results."
- "The first check was reconciliation: 12 of 12 rebuilt values match the published figures. That confirms the definitions, not the data."

**Missing:**
- **The diagram is not how the adopted report's data flows.**
  - The template's CSVs are exported from the local DuckDB mirror. The header of `scripts/export_powerbi_csv.py` says: "Source: the DuckDB mirror built from the source files…".
  - The new tables, EAGLE-I included, reach *my* Snowflake account only if I run README step 7. That step is optional and absent from START_HERE's checklist.
  - If asked "show me EAGLE-I in Snowflake" or "does Power BI read Snowflake?", I can't answer truthfully from the pack.
- DuckDB is never explained (why a local mirror exists).
- Tests T13–T31 are never listed, so I can't say what any of the 19 new tests checks.

### Slide 7: First 90 days
**I'd say:**
- "Public data narrows the question; Dominion's data answers it."
- "Month one: learn how outages, meter events and circuits are recorded, then rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filings. Deliverable: a reconciled baseline with written definitions."
- "Month two: interruptions by circuit and cause code, storm days apart from calm days, and customers interrupted repeatedly. Meter last-gasp and restore messages mark when outages start and end (99.8% of meters are smart), checked against the outage system. Deliverable: tested views and a dictionary."
- "Month three: a Power BI report tracking mainfeeder hardening against matched untreated feeders, weather-normalized, on a scheduled refresh."
- "Each of these is a question for whoever owns the definition, not a conclusion."

**Missing:**
- CEMIn and OMS are never expanded. The sheet spells it "CEMI".
- Mainfeeder hardening is never described in the deck. Only the brief, p. 8, gives its selection rule.
- Voltage island mitigation, voltage optimization and the Strategic Underground Program are names only. I can't say what any of them does.

### Slide 8: Close
**I'd say:**
- "Three takeaways. One: 2025 was stormier, with more interruptions, and once storms are counted there's no clear trend."
- "Two: frequency is the peer gap, so causes are the question, and that needs outage records by cause code."
- "Three: storm county-days carry far more outage hours, so report reliability beside storm exposure."
- "On fit: at Mercury I built a Snowflake pipeline over 20M+ rows and led a root-cause analysis on joined data. I've built a tested Snowflake → Power BI pipeline on public reliability data, and I'd like to do this work with your team."

**Missing:** "I've built" is true of the original project. In the adopted version, though, the deck's 31 tests, 18 tables and the EAGLE-I work were added on 1 November. The pack's only guidance is the cryptic "Never tell an upgrade change as a discovery story" (Q18) and START_HERE §8. I need one plain, true sentence about what was mine and what was added.

**Public deck:** slides 4–6 differ, and the brief's public-only lines cover them. However, slide 4's "465 → 796" (2024→2025, +71%) comes right after slide 2's "723 → 796, +10%" (2022→2025), and nothing bridges the two.

---

## 2. Everything unclear

### 2a. Terms used before they are defined, or never defined

| Term | First used | Defined? | Problem |
|---|---|---|---|
| MED / major event day / ex-MED | brief p. 2–5, deck s2 | brief Q2 (p. 10), deck A1, sheet 17 | The brief's story pages (2–8) say "excluding major event days" without saying what one is or why it is excluded. "ex-MED" first appears on p. 9. |
| IEEE 1366, 2.5β, α, β | brief p. 4, deck s3 | α and β are defined only on deck A1 and sheet 17; brief Q2 gives `T = e^(α+2.5β)` without saying what α and β are | Q2 can't be explained from the brief alone |
| Storm county-day | brief p. 2, deck s2 | brief p. 5; public deck s4 notes | The adopted talk never defines its main storm measure |
| EAGLE-I | brief p. 1, deck s1 | brief p. 5, deck s4 notes | OK after p. 5 |
| PUDL, ORNL, NCEI, NHC, CPC | brief p. 1/5/7, deck A4 | never | low |
| PJM; DOM zone "wider than the retail territory" | brief p. 4/6, deck s3/A3 | PJM never; DOM glossed, but never *why* it is wider | medium |
| CI vs prediction interval; "resampling whole days" | brief p. 2, 5 | numbers given, meaning never | Engineer Q1/Q5 |
| CEMIn / CEMI | brief p. 8, deck s7, sheet 16 | glossed "repeat interruptions"; never expanded; two spellings | medium |
| OMS, AMI, collectors | brief p. 8/10, deck s7 | never (notes say "the outage system") | low–medium |
| FLISR, voltage island mitigation, voltage optimization, Strategic Underground Program | brief p. 8, Q19 | FLISR spelled out on p. 8 but not tied to the acronym; the rest never | Q19 asks me to pick one |
| SCC | sheet 1 (my opening answer), brief p. 9 | never | I would open with an acronym I can't expand |
| FPL ↔ NextEra | brief p. 4, Q2, Q23 | never stated that FPL is NextEra's utility; the deal itself is never described | Q2/Q23 say "no comment on FPL" without saying why |
| DOE-417, HURDAT2 | brief p. 7, deck A4 | only the A6 speaker notes say what they were used for (storm types; DOE-417's 508,000 for Isaias) | "What did these add?" |
| "2015: Automated Outage Recording", "2020: 46 kV lines added" | brief p. 7 and deck s5 screenshots; D6 in Q1, Q6, A2 | 2015 stated as D6 without a source; **2020 never mentioned** | see §2e, item 1 |
| DuckDB | brief p. 7 (as a script name), deck s6 notes | never | see slide 6 |
| P18, "the co-op" | brief p. 9, Q17, sheet 7 | never says which co-op group or why the project compares with co-ops | It is offered as my own story |
| Bedford city (D22) | brief p. 3 | only in CHANGES.md (NOAA zone 34 mapped to both codes) | low–medium |
| "Held 1 h" | deck A6 | brief Q15 ("min of four readings") and A6 notes | OK if I find them |
| "Log terms" / log split | brief p. 2 | deck A1 only | brief alone no |
| "30-second opener", "60-second project story" | START_HERE plan, brief A4 | no text in the pack carries either label | Is the opener sheet 2 or Q24? The story does not exist. |
| "Dominion on a page" | START_HERE Monday plan, §9 | not in the pack; dropped from the v3 brief | see §2c |
| "An exceptions form" | brief Q12 | never | low |
| STAR | sheet header (S, T, A, R) vs brief A4 ("situation, your action, result") | inconsistent | low |
| Strength "moderate" | brief A4 (Huang 2017) | not one of the four defined strength levels | low |

### 2b. Numbers that differ, or could trip me

| # | What | Where | Issue |
|---|---|---|---|
| 1 | Three base years in one talk | s2: 2022→2025 (SAIFI +10%, CAIDI −4%). s5 screenshot: 2019→2025 (+6%, −9%). brief p. 2/A1: "79%" from 2023 | No bridging line. Q18 admits "set one stated rule" but gives me no sentence to say. |
| 2 | Storm county-days in the public deck | s2: 723→796 (+10%); s4: 465→796 (2024→2025, +71%) | Consecutive slides, no bridge |
| 3 | Q1 "storm county-days 464 → 791" | brief p. 10 | No years given, so it reads like the 2022→2025 pair (718→791) |
| 4 | CAIDI 110 vs 109.4; SAIFI 1.21 vs 1.320 | s3 (2021–25 means) vs s5 and A1 (2025) | Easy to cross-quote |
| 5 | Customers 2.68M vs Dominion's 2.8M / 3.6M | A1 and s5 vs the company's own figures | `docs/03` P17: the annual report's 2,809k includes NC. Not in the pack, and a Dominion panelist will know the bigger number. |
| 6 | Isaias 351,738 vs 508,000 | deck A6 vs the A6 speaker notes (DOE-417) | Peak-at-once vs total affected is explained only as "a net count" |
| 7 | Peer table windows | brief p. 4: SAIFI/CAIDI are 2021–25, SAIDI is 2023–25 | The columns don't multiply (Duke Carolinas 1.25 × 139.2 = 174 vs 179.0) |
| 8 | "Ten of the twelve file IEEE 1366" | START_HERE says the adopted deck says this | The deck says "most peers" (s3, A1). Only the brief says 10 of 12. |
| 9 | Load growth framing | brief p. 6: "4 a.m. +41% vs 4 p.m. +27%", axis "Hour of the day"; deck A3: "hours ending 1–5 a.m. +39–41%", axis "Hour ending" | Same data, two framings |
| 10 | EAGLE-I years | brief p. 7: 2014–2025; deck A4: Nov 2014–2025; map 2015–2024; s4 2015–2025 | low |
| 11 | Fit equation by version | adopted 104.3 + 0.0518×, R² 0.49; public 104.4 + 0.0514×, R² 0.48 | The brief gives only the adopted values |
| 12 | Georgia Power and Duke Florida: "IEEE 1366" vs "Mixed" | brief p. 4 vs public A6 | Footnoted, so fine |

**Checked and fine:**
- 130.2 and 133.0 are the means of {136.0, 123.3, 131.3} and {123.3, 131.3, 144.4}.
- 1.320 × 109.4 = 144.4, and 2.8 = (144.4 − 136.0) ÷ 3.
- Ranks 4th/6th/4th; medians 0.93/99.5 and 0.96/105.
- Every A2 fitted value; 6,530 is the sum of the 2015–25 storm county-days, and 6,108 = 6,530 − 114 − 308.
- 53% = 162.3 ÷ 306.7.
- The timings and the placeholder counts.

### 2c. Steps I couldn't follow, or that assume knowledge I might not have

**START_HERE**
1. **§1 "Explain every change" has no finish line.** The branch is 33 commits and 87 files. Excluding data, that is about 3,700 changed lines: Python 1,774, SQL 900, DAX 333, docs 423, M 181, shell 100. The four "above all" files alone are 976 lines: `sql/09` 580, `sql/11` 183, `storm_vs_calm_ratio.py` 86, `trend_tests.py` 127. That does not fit in 09:00–10:30 alongside the hash check, fetch, Python setup, checks and publishing.
2. **§1 is in the wrong order.**
   - Adopt condition 5 (the Power BI test) is scheduled 10:30–12:00, *after* the 10:30 deadline.
   - Condition 4 (publish) sits in the 09:00 block, *before* that test.
   - If the template fails at 11:00, my GitHub already shows 464/791 while I'm left presenting the public deck's 465/796.
3. **§8's line "I reviewed and reran everything" may be false.** The 11.9× and tests T7–T31 need README step 4 and the sources run, which §1 makes optional.
4. **§7 says what to type but not what the panel would see.** Pushing as is publishes all 33 commits with:
   - author and committer `.`, with the preparing machine's email;
   - timestamps of 1 Nov 2026, 07:47–11:47 **+0530**;
   - a `Co-Authored-By: Claude Opus 5.5` trailer.

   The squash route pushes branch `interview-upgrade` and stops there. Nothing says to merge it to `main`, so GitHub's front page would still show the old README (465/796, D1–D14).
5. **"Step" means two things.** §1 mixes README steps ("README step 1", "(step 2)", "(step 3)", "(step 5)") with START_HERE sections ("step 7 below", "step 6 below"). The plan's "(step 9/7/6/5)" and §6's "(step 1)" refer to START_HERE sections. I had to check each one.
6. **§9's news check can't be run by me as written.**
   - The path `C:\Users\oni\…` is the preparer's machine.
   - `interview-prep/research/*.md` and `work/brief/build_brief_v*.py` are not in the pack (§2 lists only 01–05).
   - The "Dominion on a page" text it says to edit is not in the v3 brief or in `build_brief_v3.py`. The one-pager's own header says "For P3 page 7", an old page number.
   - Sheet Q19, which also carries the merger dates, has no update route.
7. **Where and when do I write the `[you: …]` answers?** By hand on the printout, or in the HTML and then re-print? Salary is also contradictory: §3 says "keep it in your head; it is in no file", but brief p. 8 and sheet 22 both have a `[you: your range]` slot.
8. **Brief A4 step 2 vs START_HERE's public route.** The brief says "Apply the Power BI guide for your variant; print one report page and the model view". START_HERE says that on the public route I skip the template and print nothing from Power BI.
9. **Public route: the speaker notes invite the risky click.** I'm told to stay on the What moved page because other pages carry retracted titles and its CAIDI chart is mis-titled. But the public slide 5 notes list every page, which invites "show me Growth". There is no line for that, and nothing suggests simply retitling those charts in my own .pbix (about 10 minutes), which would remove the risk.
10. §2 refers to "v0, v1 and v2 files in the same folders". There are none. Harmless.

**APPLY_GUIDE**

11. I have no talk track for 11 pages and 60 visuals that I didn't build. Some page content is never explained anywhere: the Weather page's "co-op comparison", the Growth page's "time-varying rates", the "sales index".
12. If Route A fails, Route B takes 2–3 hours, which is not in the plan. The guide should say: if the template isn't open by 11:00, switch to the public version.
13. It assumes a Windows laptop (Power BI Desktop), and never says so.

**05_repo README**

14. **Steps 1–2 assume my local `main` is at `ec8ecb6`.** `git fetch origin` doesn't move local `main`. On an older clone, `main..interview-upgrade-2026-11` shows more than 33 commits and the stat totals differ, and I'd think the bundle was wrong. The fix: use `origin/main` or `ec8ecb6`, or add a fast-forward step.
15. It doesn't warn that uncommitted local changes can block `git switch`.
16. Step 3 hard-codes `py -3.12` although the heading says "3.11 or 3.12".
17. Step 4 has no time estimate (about 3 GB of downloads, extraction, then a 0.9 GB DuckDB build).
18. Steps 5 and 7: nothing says the template's CSVs come from DuckDB, or that Snowflake lacks the new tables without step 7. Deck slide 6 implies both.

### 2d. `[you: …]` placeholders without enough guidance

- **Sheet 11 `[you: one query you can sketch]`:** no query is offered. The pack has two good candidates, the 3-year SAIDI with AVERAGEX and the gaps-and-islands logic from Q15, but neither is written out as SQL.
- **Sheet 9 / A1 "Who used it? `[you: …]`" for the Power BI review:** the honest answer ("nobody yet; I built it for this application") is not suggested, so the slot invites invention.
- **Q19 `[you: which one, and why]`:** three of the four programs have no description, so I can't choose one with a reason.
- **Q12 "Power Apps … plus a 30-day plan (an exceptions form)":** what the form or the plan is, the pack never says.
- **Sheet 7 / Q17, "Project option (yours, P18)":** the numbers are there (1.849 → 1.887) but not the story: Prince George Electric filed SAIDI but no SAIFI, which would have added its 13,341 customers to the Virginia co-op benchmark's denominator. It is mine (my own commit `1635a8e`, 27 Oct), but the pack should remind me what happened.
- **Q18 "Never tell an upgrade change as a discovery story":** cryptic. It should say plainly what it means.
- **Sheet 22 / brief p. 8 `[you: your range]`:** no pointer on how to research a range, and it contradicts START_HERE.
- **Sheet 18 `[you: travel and storm-season hours…]`:** nothing says what storm duty means for an analyst here, so I would be committing blind.
- **START_HERE §4, talk length `[you: …]`:** if the slot is 5 minutes, "cut words, not slides" means dropping about 40% of 1,028 words, and there is no short version.

### 2e. Questions I'd be afraid of: the pack doesn't prepare me

1. **"Your charts mark '2020: 46 kV lines added'. The counting base changed mid-series, and your fit and trend tests run straight across it. 2020 is also your biggest residual (+14.5 in A2)."** `docs/03` P7 records it ("…2020 (46 kV lines included)… Not adjusted in data"). The pack never mentions 2020.
2. **"Dominion doesn't publish its MED dates. How do you know which EAGLE-I days were major?"** The answer is proxy MEDs (D18), which are not in the pack.
3. **"Show me EAGLE-I in Snowflake." / "Does the report read Snowflake?"** See slide 6.
4. **"Who built the EAGLE-I work, and when?"** It was done on 1 Nov with an AI assistant, and a push-as-is shows that on GitHub. I need one true sentence.
5. **"You call it a star schema; your model view shows 20 tables and 2 relationships."**
6. **"What do you know about Dominion?"** It isn't on the sheet, and the pack has no company page (no size, leaders, CVOW or Q3 results).
7. **"We serve 2.8 million customers. Where does 2.68 million come from?"** (P17)
8. **"Which test gives p = 0.54? With 11 points, could it detect anything?"** It is an OLS slope on year with a t-test on 9 df, per `trend_tests.py`. That is not in the pack.
9. **"Why these 11 peers? Why not Appalachian Power?"**
10. **"FPL's SAIFI is half yours. What do you make of that, given the merger?"**
11. **"What did DOE-417 and HURDAT2 add?"** This is answered only in the A6 speaker notes.
12. **"Confidence interval vs prediction interval? Why resample whole days?"**
13. **"What's voltage island mitigation?"**
14. **"Your peer table's SAIDI isn't SAIFI × CAIDI."**
15. **(Public route) "Can you click to the Growth page?"**

---

## 3. The Monday plan

### Is it realistic?

| Block | Planned | My estimate | Comment |
|---|---|---|---|
| 08:30 News check | 30 min | 10–30 | It can't be run as written (§2c, item 6). Do it by hand, and again Tuesday morning: SCC rebuttal testimony was due 2 Nov. |
| 09:00 Adopt or not | 60–90 | **2–2.5 h** | That covers the hash, fetch, Python setup, 3 checks, CHANGES, the 4 named files and publishing. The optional 3 GB rerun adds another 1–2 h. |
| 10:30 Power BI | 60–90 | 45–90 | Add 20 minutes if Desktop needs updating, and about 30 to learn 11 pages I didn't build. |
| 12:45 Brief once | 45 | 45–60 | A1–A3 are dense. The "marked list" it produces never gets a slot to be resolved. |
| 13:30 Deck ×3 | 90 | 90 | Fine. |
| 15:15 Sheet drill | 60 | 60 | Works only if the `[you: …]` items are already filled. |
| 16:15 Hard 25 | 60 | 60 | Same condition. |
| 17:15 Mock | 30 | 30 | Fine. |
| 17:45 Print | 45 | 45+ | Assumes a duplex colour printer at home. |
| 19:30 Second round | 30 | 30 | Fine. |

**Missing from the plan:**
- The `[you: …]` work: about 90–120 minutes for 7 true STAR stories and about 15 facts.
- Recruiter confirmation of time, place, format, panel and talk length. The deck can't be timed until I know the length.
- Resolving the brief's marked list.
- If adopted, one practice walk-through of the live report.
- If there is a screen, bringing the .pptx.

Demand is about 13–14 hours against about 10.5 hours of working blocks.

**What I'd cut if running late, in this order:**
1. Any re-download (README step 4).
2. The upgrade, if I can't explain the four named files by 10:30. Go public, and use 10:30–12:00 for the `[you: …]` stories.
3. The news check: cut to 10 minutes by hand, and redo it Tuesday.
4. The third deck run: do two, one recorded.
5. The hard 25: drill only the seven ● questions plus Q19–Q24.
6. The mock panel: replace with a self-shuffle.

Never cut: one timed run, the STAR stories, logistics, printing, the 20:00 stop. Better still, do the `[you: …]` items and the recruiter email on Sunday evening.

### Is the adopt-or-not decision clear?

- **What it means is clear.**
  - Adopted: the main deck (EAGLE-I slide 4, 31 tests, D22 counts, 11-peer medians), the template, and publishing the branch.
  - Public: the `_public` deck with its numbers, no template, and my own report on the What moved page only.
- **Which deck to print is clear** (§5).
- **How long it takes is understated** (see the table above).
- **What is not clear:**
  - "Every change" has no finish line.
  - The order is wrong: publishing comes before the template test, and the 10:30 deadline comes before condition 5.
  - What each publish option visibly leaves on GitHub.
  - What I may truthfully say about authorship in each case.
  - Whether adopting without publishing is allowed, and why publishing is required at all.
  - That slide 6's Snowflake claim needs README step 7.
- **As the candidate:** read literally, the 10:30 test almost always fails, so I land on the public version. The pack should say plainly that the public talk is complete and strong, so falling back is not a loss.

---

## 4. Top 10 fixes, ranked by how much they'd help on Tuesday

1. **Give me a scoped, honest adopt rule and one authorship sentence.** (START_HERE §1, §7, §8; brief Q18)
   - Replace "explain every change" with a named list: README "What's new", D22, the parts of `sql/09` behind s4 and A6, `storm_vs_calm_ratio.py`, `trend_tests.py`.
   - Move publishing after the Power BI test.
   - State what each publish option shows on GitHub: author `.`, the preparer's email, +0530 times on 1 Nov, the AI trailer on 33 commits; and that squash puts my name on 40k lines and needs a merge to `main`.
   - Drop "reran everything" from §8 unless step 4 and the sources run are done.
   - Write the sentence for "who built the November additions?".
2. **Make slide 6, the brief p. 7 and Q15 match the real data path** (sources → DuckDB mirror → CSV → Power BI Import; Snowflake has the original build, and the new tables only after README step 7). Either run step 7 on Monday, or redraw the slide and notes.
3. **Schedule and place the `[you: …]` work.**
   - Give it a 90–120-minute slot, ideally Sunday.
   - Say whether to write on the printout or edit the HTML and re-render.
   - Fix the salary contradiction.
   - Add the missing guidance: a sketchable query, "no users yet" for the review, a line on each program, the P18 story, the "exceptions form", a 5-minute cut of the talk.
4. **Arm me for the engineer's four traps** in A1, Q1, Q2 and Q5:
   - the 2020 46 kV counting change and the 2020 residual;
   - proxy MEDs behind "non-major days" (D18);
   - the trend test (OLS on year, t-test, 9 df, low power);
   - whole-day resampling, and CI vs prediction interval.
5. **Fix Q11 for the printed model view** (brief p. 7, Q11, sheet 10, s5 notes). It has 18 imported tables, 2 calculated tables and 2 relationships, and 16 tables serve single visuals. Give me an honest line, and stop calling the whole model a star.
6. **Add a half-page glossary.**
   - Cover: MED and ex-MED, IEEE 1366 and 2.5β with α and β, storm county-day, EAGLE-I and ORNL, PUDL, PJM and DOM (and why DOM is wider), CEMIn (one spelling), OMS, AMI and last gasp, FLISR and the other three programs, SCC, FERC and NRC, DOE-417, HURDAT2, CPC, CI vs PI.
   - Define storm county-day in slide 2's notes.
7. **Restore a company box.**
   - Sizes: 2.68M (VA, EIA) / 2.8M (VA+NC) / 3.6M (VA/NC/SC), from P17.
   - Also: leaders, the NextEra deal in one line, FPL as NextEra's utility, CVOW, the four programs.
   - Add "What do you know about Dominion?" to the sheet.
8. **Re-time the Monday plan.** Use realistic blocks, add the missing slots (`[you: …]`, recruiter, the marked list), add the cut list, and align brief A4 step 2 with the public route.
9. **Make the news check runnable by me.**
   - Remove the preparer's path and the dead "Dominion on a page" and build-script steps.
   - Give a 10-minute manual list: the Dominion and NextEra newsrooms, SCC case PUR-2026-00112, the Federal Register.
   - Say: "if something moved, correct brief A1 'May 2026 → H2 2027', Q23 and sheet 19 in pen".
   - Repeat it Tuesday morning.
10. **Small consistency fixes:**
    - bridge lines for the 2022 / 2019 / 2023 base years, and for the public deck's +10% vs 465→796;
    - "2024 → 2025" on Q1's 464→791;
    - name the 30-second opener and write the 60-second project story;
    - correct START_HERE's "ten of the twelve" claim about the adopted deck;
    - README step 2 against `origin/main` or `ec8ecb6`;
    - one spelling of CEMIn;
    - put Task back into STAR in brief A4.
