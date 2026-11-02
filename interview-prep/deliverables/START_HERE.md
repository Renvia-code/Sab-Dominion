# Start here: the Dominion interview pack

**The interview:** Dominion Energy, a panel of three, Tuesday, November 3, 2026.
Time, place and format: `[you: …]`.

This page is for you only. It says what to do, in order, from the day you get the pack to Tuesday
morning.

**In short**
1. **The day you get this** (Sunday if you can): email the recruiter, print the question sheet and
   the brief, and write your `[you: …]` answers on them in pen (step 3, about 2 hours). If you have
   time, also run the adopt check (step 2), so Monday is all practice.
2. **Monday:** follow the plan in step 4. Choose the version by 11:15 at the latest.
3. **Tuesday morning:** the 20-minute routine at the end of step 4.

## 1. What is in the pack

| File | What it is | Version |
|---|---|---|
| `01_deck/Dominion_reliability_deck_adopted.pptx` | The talk: 8 main slides (about 8 minutes) and 6 appendix slides, with speaker notes | Adopted |
| `01_deck/Dominion_reliability_deck_adopted_print_letter.pdf` | The same deck for printing: 14 pages, Letter landscape | Adopted |
| `01_deck/Dominion_reliability_deck_public.pptx` and `…_public_print_letter.pdf` | The same talk, using only what is on your GitHub today | Public |
| `01_deck/Dominion_handout_2page.pdf` | **The leave-behind:** one sheet, two sides, in plain English. Page 1 what you found, page 2 what you built, with your GitHub link. Hand this over, not the 14-page deck | Public numbers |
| `02_question_sheet/Dominion_question_sheet.pdf` | One sheet, two sides: the 24 likeliest questions with answer cues, and 5 questions to ask | Both |
| `03_interview_brief/Dominion_interview_brief.pdf` | The brief, 12 pages: the story, the data, how it was built, Dominion on a page with a glossary, the role; then A1 every number, A2–A3 the 25 hardest questions, A4 delivery | Both |
| `04_powerbi/` | The Power BI template, its queries and measures, and `APPLY_GUIDE.md` | Adopted |
| `05_repo/` | The November 1 extension as a git bundle, `CHANGES.md`, and `README.md` with every command | Adopted |

Use them in this order: this page, the brief once, the deck aloud, then the sheet and the hard 25 by
recall.

## 2. Choose the version: public or adopted

**What happened on November 1.** The person who prepared this pack extended your project on a
branch, `interview-upgrade-2026-11`, using an AI coding assistant. You did not write the extension,
and it is not on your GitHub: `05_repo/` holds it as a git bundle. It adds:

- EAGLE-I county outages: the storm vs calm county-day comparison (slide 4: 11.9×), the ten
  largest events and the Isaias curve
- NOAA storm types, HURDAT2 and DOE-417 context
- the D22 storm recount (Bedford city counted once): 2024 = 464 and 2025 = 791, against 465 and
  796 on your GitHub
- tests T13 to T31, decisions D15 to D22 and the trend tests (`scripts/trend_tests.py`)
- degree days, and EIA-930 data to October 29, 2026
- an all-Import Power BI template that opens offline

**The public version is complete.** It is your own October work, already on your GitHub, and the
talk, the sheet and the brief all support it. Choosing it loses nothing that matters on Tuesday.

**The adopted version** is stronger on weather, but use it only if all four of these are true by
your decision time:

1. **You fetched the bundle** and its SHA-256 matches (`05_repo/README.md`, steps 1 and 2).
2. **The three light checks pass on your laptop** (README steps 3 and 5). Once Python is set up,
   all three together take about a second:
   - `run_local_duckdb.py`: the rolling SAIDI averages, 130.2 and 133.0
   - `check_output_metrics.py`: "All committed-output checks passed."
   - `trend_tests.py`: SAIFI p 0.54, CAIDI 0.74, SAIDI 0.58, adjusted 0.67
3. **You read the review list below** and can explain slide 4, appendix A6, the Bedford recount
   and the trend test in your own words.
4. **The Power BI template opens offline** and passes its four checks (step 6).

The whole check takes about 2 to 2.5 hours. Do it on Sunday if you can; otherwise on Monday,
08:45–11:15. **If any of the four isn't true by 11:15 on Monday, use the public version and move on.**

**The review list:** 427 lines, read on the branch in your clone. `05_repo/CHANGES.md` has one
line per commit if you want more.

| # | Read | Lines | Why |
|---|---|---|---|
| 1 | `README.md` 11–24 | 14 | "What's new", the first thing a visitor reads. Every number in it must be one you can defend |
| 2 | `docs/04_decisions.md` 147–203, 213–221 | 66 | D15–D20 and D22: the rules behind every new number |
| 3 | `docs/03_data_quality.md` 32, 38–40, 66–86 | 25 | the data problems found on November 1 (P20, P26–P28) and what each of T13–T31 checks |
| 4 | `docs/05_metrics_and_measures.md` 108–126, 146–157 | 31 | every EAGLE-I figure with its calculation, including 11.9×, and the trend tests |
| 5 | `sql/05_noaa_storms.sql` 120–128; `sql/07_weather_adjusted_and_profile.sql` 38–40 | 12 | the Bedford fix (D22) and its new expected values |
| 6 | `sql/09_eaglei_outages.sql` 1–15, 229–320, 322–334 | 120 | the header ("EAGLE-I counts every utility"); the county-day panel and the stand-in major event days behind slide 4; the event and restoration definitions behind A6 |
| 7 | `scripts/storm_vs_calm_ratio.py` 1–72 | 72 | the 11.9× and its whole-day resampling |
| 8 | `scripts/trend_tests.py` 1–16, 81–93, 101–113 | 42 | what the trend test does (skip lines 26–79, which compute the t distribution) |
| 9 | `scripts/export_powerbi_csv.py` 1–11 | 11 | where the template's CSV files come from (the DuckDB copy) |
| 10 | `scripts/run_local_duckdb_sources.py` 46–79 | 34 | how the same SQL runs in DuckDB: the Snowflake-only statements it drops and the date parsing it translates |

Skip the rest of `sql/09`, `sql/10`, `sql/11`, the download scripts and the rest of the DuckDB
runner: the tests T7–T31 and the checks cover them.

**Optional:**
- **Re-download the raw sources** (README step 4): about 3 GB on disk; allow about half an hour,
  including a build of about 25 seconds that runs T7–T31.
  - If you do it, you can say you reran everything.
  - If you skip it, say you "reran the checks".
- **Load the new tables into your Snowflake** (README step 7). It isn't needed for Tuesday.

**How the two versions differ**

| | Adopted | Public |
|---|---|---|
| Deck | `…_deck_adopted…` | `…_deck_public…` |
| Slide 4 | storm vs calm county-days (EAGLE-I), 11.9× | storm county-days by year |
| Storm county-days | 2024 = 464, 2025 = 791 | 465 and 796, as on your GitHub |
| Peer medians | the 11 peers without Dominion: SAIFI 0.93, CAIDI 99.5 | all 12, Dominion included, as your GitHub prints them: 0.96 and 105 |
| Peer reporting methods | "most peers use IEEE 1366" (the brief says ten of the twelve) | "methods differ" |
| Slide 6 | the real data path, marked "Original build" and "Added Nov 1, 2026" | your October build |
| Power BI | the template (step 6) | your own report, What moved page only |
| Brief | all of it | skip the parts tagged "If adopted"; the public line is beside each one |

Quote the deck you present.

**On the public version, your own report:** stay on the What moved page.
- Its other pages still carry titles that your decision log later retracted (for example "That gap
  is data centres").
- Six of its tables are DirectQuery: they show data only while your Snowflake account is reachable.
- Its CAIDI chart is titled "Minutes to restore each outage…". CAIDI is SAIDI ÷ SAIFI, minutes per
  interruption, so say that, and that you would retitle it.

If you have 10 spare minutes, retitle those charts in your own `.pbix` so any page is safe to show.
If someone asks for another page anyway, say its titles predate your decision log and offer What
moved.

## 3. The day you get this: the recruiter and your `[you: …]` answers

**Email the recruiter first.** Confirm:
- the time and place, and whether it is in person or on video
- the panel's names and roles
- how long your talk may run, and whether there is a screen or only paper
- the exact job title and team

You can't time the deck until you know the talk length.

**Then print the question sheet and the brief** (step 5) and write each `[you: …]` answer on them
in pen. Don't edit the HTML or re-print; your printout is your copy. It takes about 90 to 120
minutes.

Every `[you: …]` is something only you can answer truthfully: a reason, a story, a date or a
logistics answer. Write each one in your own words, and never invent one. The same item often
appears in both files, so they come down to the list below. "Q19" means hard question 19 in the
brief; "sheet question 19" means question 19 on the question sheet.

**Logistics**
- Interview time, place and format; the panel's names and roles (from the recruiter)
- How long the talk may run. The speaker notes read in about 8 minutes (7:57 adopted, 7:23 public).
  If the slot is 5 minutes, use the brief's "5-minute route" (A4).
- The exact job title and team (from the recruiter)
- The hybrid schedule in Richmond (three days in the office, two remote): your answer, and your
  commute or relocation plan
- Work authorization and sponsorship: your answer, known before the panel
- Pay: before Tuesday, research a range for this role in the Richmond area from public pay data, such
  as the U.S. Bureau of Labor Statistics' Occupational Employment and Wage Statistics tables. Write
  it in pen in the `[you: your range]` slot; the pack prints no figure. If pay comes up, let the
  recruiter name the band first ("What range is budgeted for this role?"). If you're asked to go
  first, give your range as a range.
- Notice period and earliest start date
- Travel and storm-season duty. The posting says "Travel Up to 25%" and nothing about storm duty, so
  ask the recruiter what storm-season duty means for this role, then write down what you can commit
  to.

**True stories** (situation, task, action, result; your resume doesn't hold these)
- A disagreement about a number or a definition: what you were responsible for, what you did,
  the outcome
- A number that was wrong or nearly went out wrong: the check that caught it, the fix, and the
  control you've used since
- Overlapping deadlines, and how you ordered the work
- Someone senior said your numbers were wrong (Q21)
- A time you said "I'll find out and come back" (Q22)
- One real break at work: cause, then control (Q17). Your own co-op fix of October 27 is a true
  project example; Q17 reminds you of the facts.
- One personal lesson (Q18)

**Facts only you know**
- Why Dominion: one personal reason. Why move: the real reason, said as a pull.
- One line on why this role, to end the 30-second opener (brief A4), and one sentence on why this
  team, to end sheet question 19 ("What do you know about Dominion?")
- What you have used AI tools for in your own work, if anything (step 8)
- Which Grid Resiliency program interests you, and why (Q19). Q19 and the brief's Dominion page say
  what each one does.
- Power BI, Power Apps, SharePoint and the Power BI Service at work: the exact truth (Q12)
- The Mercury pipeline: what it fed, what you owned, the grain, the incremental logic, scheduling,
  tests and one failure (Q16); who you worked with
- Who used each dashboard you built, including The Life Initiative's. For this project's report, if
  it's true, say "nobody yet; I built it for this application".
- One SQL query you can sketch on paper. The sheet's question 11 gives one from your project (the
  three-year SAIDI average, a window function); practice it, or use one of your own.
- Snowflake cost controls you have used
- Any regulatory filing or governance work: the truth (Q14)
- The CSV and DataFolder route in Power BI: mention it only if you adopted the extension and
  tested it yourself

## 4. The plan: the day you get this, Monday and Tuesday morning

Three rules, all with strong evidence behind them:
- **Drill by recall, not by rereading** (Roediger & Karpicke 2006; Rowland 2014). Cover the answer,
  say it aloud, then check.
- **Spread the drills** (Cepeda et al. 2006). An afternoon round and an evening round beat one long
  block.
- **Protect sleep** (Lim & Dinges 2010). The 20:00 stop is fixed.

**The day you get this (about 2 hours, plus 2–2.5 if you also run the adopt check):** the recruiter
email, then your `[you: …]` answers (step 3), then, if you have time, the adopt check (step 2).

**Monday, November 2.** Shift the times to your day `[you: …]`, but keep the order.

| Time | Step | Done when |
|---|---|---|
| 08:30–08:45 | **News check by hand** (step 9, 10 minutes) | Nothing moved, or the fix is in pen |
| 08:45–11:15 | **The adopt check** (step 2), unless you finished it on Sunday. If you choose the public version, use this time for your `[you: …]` stories and one walk through your own report's What moved page. | Version chosen by 11:15 |
| 11:15–11:45 | **Adopted:** walk through the template's 11 pages once. Eight are your own October pages, re-pointed to CSV; Outages by county, Storms and Data notes are new. Publish only if you want to (step 7). **Public:** say your slide 5 aloud with your report open. | You can say what each page answers |
| 11:45–12:30 | Lunch | |
| 12:30–13:30 | **Read the brief once**, start to finish, for understanding. Mark anything you can't explain. | A marked list |
| 13:30–14:00 | **Clear the marked list** using the glossary, A1 and the Dominion page | List cleared |
| 14:00–15:15 | **Give the deck aloud three times** against a timer set to your talk length (8 minutes unless the recruiter says otherwise); record one run and listen back. Cut words, not slides. Then say the **30-second opener** and the **60-second project story** (brief A4). | One run inside your time |
| 15:15–15:30 | Break | |
| 15:30–16:30 | **Drill the question sheet by recall.** Cover each answer, say it aloud in 60–90 seconds, then check. Mark misses. | Every sheet question answered aloud once |
| 16:30–17:30 | **Drill the hard 25.** The seven ● first, then Q19–Q24, then the rest. Claim, then proof, then limit, aloud. | Misses marked |
| 17:30–18:00 | **Mock panel**, if someone can help: three roles, 20 minutes, questions from the hard 25. If you're alone, shuffle them and time each answer. | Done |
| 18:00–18:45 | **Print the handouts** (step 5) and pack: the printouts, your laptop (with the report working offline if adopted), the `.pptx` on a USB stick in case there's a screen, charger, ID and directions | Bag packed |
| 18:45–19:30 | Dinner | |
| 19:30–20:00 | **Second drill round:** only the misses, plus the opener | Misses answered cleanly |
| **20:00** | **Stop.** No new material after this. Sleep. | |

**If you're running late, cut in this order:**
1. The re-download (README step 4; optional).
2. The adopted version: at 11:15, go public.
3. The news check: keep it to 10 minutes and redo it on Tuesday.
4. The third deck run: do two, and record one.
5. The hard 25: only the seven ● and Q19–Q24.
6. The mock panel: shuffle the questions yourself.

**Never cut:** one timed run, the true stories, logistics, printing, the 20:00 stop.

**Tuesday morning (20 minutes):**
- The news check again (step 9). Rebuttal testimony in the merger case was due November 2.
- Say the 30-second opener aloud twice.
- Reread the three takeaways on slide 8.
- Leave early.

## 5. Printing

Set the paper to US Letter and the scale to **Actual size** (100%), not "Fit". Print in color if
you can; every page also reads in black and white.

| What | File | Pages | Copies | Sides | When |
|---|---|---|---|---|---|
| Question sheet, for you only | `02_question_sheet/Dominion_question_sheet.pdf` | 2 | 1 | Double-sided: one sheet | The day you get this, to write on |
| Brief, for you only | `03_interview_brief/Dominion_interview_brief.pdf` | 12 | 1 | Double-sided; staple | The day you get this, to write on |
| Handout, one for each panelist to keep | `01_deck/Dominion_handout_2page.pdf` | 2 | 3 | Double-sided, flip on the long edge: one sheet each | Monday |
| Deck, your copy to present from (only if the recruiter confirms a presentation) | `01_deck/Dominion_reliability_deck_adopted_print_letter.pdf` or `…_public_print_letter.pdf`: only the version you chose | 14, landscape | 1 | Single-sided, so pages can lie side by side | Monday |
| Adopted only: the report's Summary page and the model view | from Power BI Desktop (step 6) | 2 | 1 | Single-sided | Monday |

Never hand over the sheet or the brief: they hold your answer cues and your `[you: …]` notes. After
printing, check the page order and that nothing is cut off at the edges.

**The handout uses the public numbers**, the ones your GitHub shows (storm days 465 and 796; peer
medians 0.96 and 105). If you present the adopted deck, its figures differ slightly (464 and 791;
0.93 and 99.5). Either keep the talk public, so the handout, the talk and GitHub agree, or say the
adopted figures aloud as a later recount. Before you hand it over, open your GitHub page once: the
handout sends the panel there.

## 6. The Power BI steps (adopted version only)

You need a Windows laptop with Power BI Desktop (free from the Microsoft Store). The full guide is
`04_powerbi/APPLY_GUIDE.md`. In short:

1. Update Power BI Desktop. The template was built and tested in version 2.159 (October 2026).
2. In your clone, switch to the branch: `git switch interview-upgrade-2026-11` (README step 1).
3. Double-click `04_powerbi/Dominion_reliability_review.pbit` (the branch has the same file in
   `powerbi\`). When it asks for **DataFolder**, the box already holds an example,
   `C:\path\to\dominion-reliability-review\data\output\`. Replace it with your clone's own
   `data\output\` folder (it must end with a backslash), then click **Load**. If you click Load
   with the example still there, every table fails with "Could not find a part of the path". Fix
   it with Transform data ▾ > Edit parameters > DataFolder, then **Apply changes**.
4. File > Save As > `Dominion_reliability_review.pbix` (`*.pbix` is gitignored).
5. Check four things:
   - The Scorecard shows 2025 with 2.68M customers, SAIDI 144.4, SAIFI 1.320 and CAIDI 109.4.
   - Data notes says "All 31 data tests pass" and "12 of 12".
   - On Fair comparison, the dashed lines sit at SAIFI 0.93 and CAIDI 99.5.
   - Numbers show as 2,675,735.
6. Turn Wi-Fi off, reopen the `.pbix`, click through all 11 pages, and move the year slicer on
   Summary.
7. For the printouts: File > Export > Export to PDF and print page 1 (Summary); take a screenshot of
   the model view (Windows + Shift + S) and print it. The model view shows 20 tables and 2
   relationships; the brief's Q11 gives you the line for that.

If the template isn't open and checked by 11:15 on Monday, use the public version. Don't start the
guide's Route B on Monday: it takes 2 to 3 hours.

## 7. Publishing the extension (adopted version only, optional)

- **Publish only after the Power BI test passes.**
- **Not publishing is fine.** Slide 6 of the adopted deck marks what was added on November 1, so
  the difference from your GitHub is stated. If asked, say the extension is on a branch you are
  still reviewing.
- **If you publish, squash it into one commit of your own** on `main`, with a message that keeps
  its "How it was made" paragraph true. `05_repo/README.md` step 8 has the commands and the message.
- **Don't push the branch's commits as they are,** to any branch or pull request. Each one carries the
  preparer's git identity (a GitHub no-reply address that links to the preparer's account),
  November 1 times at +05:30, and a `Co-Authored-By: Claude` line. GitHub keeps a pull request's
  commits visible even after a squash merge.

If `main` on GitHub has moved past `ec8ecb6`, README step 8 says what to rerun before you push.

## 8. If you're asked who built it, or whether you used AI tools

Panels in 2026 often ask, and the answer must be true. Lines to adapt in your own words:

**Adopted version**, for "Who built this?" or "Did you use AI tools?":

> "The October build is mine: the pipeline, the first 12 tests and the report. On November 1 it
> was extended with help, using an AI coding assistant: the county outage analysis, 19 more tests
> and this template. I reviewed those changes and reran the checks myself."

- Say the last sentence only if you did both.
- Never say "I reran everything" unless you also did the optional re-download and full build
  (README step 4, about half an hour).
- The same sentence ends the speaker notes of adopted slide 6.
- Never describe a November change as something you found. Say "the extension counts Bedford city
  once", not "I noticed…" (brief Q18).

**Public version:**

> "The analysis is the one on my GitHub, and I can walk you through any step. I had help preparing
> these slides, including an AI assistant."

Add `[you: what you have used AI tools for in your own work, if anything]`, and say only what is
true for you.

The printed deck, sheet and brief never mention how they were made.

## 9. The news check (Monday 08:30 and Tuesday morning, 10 minutes)

Open these six pages in a normal browser. It takes about 10 minutes.

**An item has moved** if something new, dated after November 1, appears on the merger, leadership, a
major outage, rates or CVOW, or anything changes a line on the brief's Dominion page. These don't
count: the companies' rebuttal filing in the SCC case (it is due November 2 and expected), and
routine community or customer-program releases.

| # | Open this | Look for | As of November 1 |
|---|---|---|---|
| 1 | Dominion newsroom: https://news.dominionenergy.com/ | The newest releases at the top | The newest is "Dominion Energy Announces Third-Quarter 2026 Results" (Oct 30), then the dividend (Oct 27) |
| 2 | Investor relations: https://investors.dominionenergy.com/ and Events & Presentations: https://investors.dominionenergy.com/events-and-presentations/default.aspx | Any investor event or presentation after the Oct 30 call | The Q3 call on Oct 30 is the latest |
| 3 | NextEra newsroom: https://newsroom.nexteraenergy.com/news-releases | Anything after Oct 23 that names Dominion, Virginia or the merger | Newest Oct 23 (an Iowa grid project); NextEra's Q3 results Oct 21 |
| 4 | Virginia SCC docket search: https://www.scc.virginia.gov/docketsearch (if that fails, go to scc.virginia.gov and choose Docket Search). Enter case PUR-2026-00112 | The newest filings and any order | Rebuttal due Nov 2; hearings from Nov 17; order by Jan 11, 2027. The commission's staff (Oct 19): deny as proposed unless conditions are accepted |
| 5 | Federal Register: https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=EC26-131, then search "North Anna" on the same site for the NRC | Any EC26-131 notice newer than Oct 21; any NRC order on the license transfer | Oct 21 notice of the companies' Oct 15 response; the NRC notice of Aug 27 |
| 6 | FERC eLibrary: https://elibrary.ferc.gov/eLibrary/search. Type EC26-131 under Docket Number and sort by date | An order, or a new deficiency letter | Deficiency letter Sep 23; response Oct 15; no order |

**If nothing moved,** you can say: "As of this morning nothing has changed since the Q3 call; the SCC
hearing starts November 17."

**If something moved,** write it in pen on the brief's Dominion page (date, what, where), and fix the
same fact wherever else it appears:
- the merger line on the Dominion page ("close expected in the second half of 2027")
- hard question Q23 (its timeline: "close is expected in H2 2027")
- the sheet's question 19, "What do you know about Dominion?"

Open the answer with "As of this morning…". You don't need to reprint anything.

**If someone runs the check for you with an assistant,** give them this prompt:

> Using only public web pages, check whether any of these facts, true on November 1, 2026, has changed:
> (1) Dominion Energy's newest press release is its third-quarter 2026 results of October 30 (newsroom:
> news.dominionenergy.com); (2) NextEra Energy's newest release is dated October 23
> (newsroom.nexteraenergy.com/news-releases); (3) in Virginia State Corporation Commission case
> PUR-2026-00112, the NextEra–Dominion merger, the companies' rebuttal testimony is due November 2, hearings begin
> November 17 and the final order is due by January 11, 2027, and on October 19 the commission's staff recommended
> denying the merger as proposed unless conditions are accepted; (4) at the Federal Energy Regulatory Commission,
> docket EC26-131 has a September 23 deficiency letter and the companies' October 15 response, and no order;
> (5) the Nuclear Regulatory Commission noticed the license-transfer application on August 27 and has issued no
> order; (6) South Carolina hearings begin December 8 with an order due by January 29, 2027, North Carolina
> hearings begin February 23, 2027, and closing is expected in the second half of 2027. For each fact, report
> "unchanged" or "moved", with the date, one sentence and the URL you opened. The rebuttal filing itself is
> expected and does not count as moved. Cite only pages you actually opened, do not get around any site that
> blocks automated access, and do not research individual people. If anything moved, write a single file of at
> most one page, named with today's date followed by _dominion_update (for example
> 2026-11-02_dominion_update), in the same folder as this pack, in US spelling. If nothing moved, write
> nothing. Do not edit any other file.
