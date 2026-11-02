# Start here: the Dominion interview pack

**The interview:** Dominion Energy, a panel of three, Tuesday, November 3, 2026.
Time, place and format: `[you: …]`.

This page is for you only. Read it first. Steps 1 to 5 run in order on Monday.

## 1. Monday first: adopt the upgrade, or use the public-repo version

On November 1 the project was extended on a local branch, `interview-upgrade-2026-11`. The
branch is not on your GitHub. It adds:

- EAGLE-I county outages: the storm vs calm county-day comparison, the ten largest events and the Isaias curve
- NOAA storm types, HURDAT2 and DOE-417 context
- the D22 storm recount (Bedford city counted once): 2024 = 464 and 2025 = 791, against 465 and 796 on your GitHub
- tests T13 to T31, decisions D15 to D22 and the trend tests (`scripts/trend_tests.py`)
- degree days, EIA-930 data to October 29, 2026
- the CSV exports behind an all-Import Power BI report

The pack comes in two versions of the deck. Choose one on Monday morning.

**Adopt (the main version).** Use it only if you do all of the following:

1. Read `05_repo/CHANGES.md` line by line (one line per commit: what and why).
2. Fetch the bundle into your own clone and rerun the checks on your laptop. The commands are in
   `05_repo/`. `[B: insert D's fetch and check steps here]`
3. Be able to explain every change yourself, above all:
   - `sql/09` and `sql/11`
   - `scripts/storm_vs_calm_ratio.py`: the 11.9× and its interval
   - `scripts/trend_tests.py`
4. Publish the branch from your own GitHub account.
5. Apply the Power BI template (`04_powerbi/APPLY_GUIDE.md`) and test it offline.

**Public-repo version (the fallback).** Use it if you do not adopt.

- Use the deck ending `_public`.
- In the brief, skip the parts marked "depends on adopting the upgrade".
- Do not show the Power BI template, which needs the branch's data.
- Do not show your original `.pbix` as it is either: some titles still make the stronger claims
  that the decision log retracts (for example "That gap is data centres").

**Deadline:** if you cannot explain every change by 10:30 on Monday, use the public-repo version
and move on.

## 2. What is in the pack

Use the v2 files only. The v0 and v1 files in the same folders are earlier drafts.

| File | What it is | Version |
|---|---|---|
| `01_deck/Dominion_reliability_deck_v2.pptx` | The talk: 8 main slides (about 8 minutes) and 6 appendix slides, with speaker notes | Adopted |
| `01_deck/Dominion_reliability_deck_v2_print_letter.pdf` | The same deck for printing: 14 pages, Letter landscape | Adopted |
| `01_deck/Dominion_reliability_deck_v2_public.pptx` and `…_v2_public_print_letter.pdf` | The same talk, using only what is on your GitHub today | Public-repo |
| `02_question_sheet/Dominion_question_sheet_v2.pdf` | One sheet, two sides: the 24 likeliest questions with answer cues, and 5 questions to ask | Both |
| `03_interview_brief/Dominion_interview_brief_v2.pdf` | The brief, 12 pages: the story and the numbers (pages 1–8), then A1 every number, A2–A3 the 25 hardest questions, A4 delivery | Both |
| `04_powerbi/` | The Power BI template, its data folder and `APPLY_GUIDE.md` | Adopted |
| `05_repo/` | The branch as a git bundle, `CHANGES.md` and the steps to check and publish it | Adopted |

Use them in this order: this page, then step 1 (the version), the brief once, the deck aloud, then
the sheet and the hard 25 by recall.

## 3. Fill in the `[you: …]` items

Every `[you: …]` is something only you can answer truthfully: a reason, a story, a date or a
logistics answer. Write each one in your own words, and never invent one. There are 22 on the
question sheet and 20 in the brief; many are the same item, so they come down to the list below.
"Sheet 6" is question 6 on the sheet; "Q19" is a hard question in the brief.

**Logistics** (the same answer in both files)
- Interview time, place and format; the panel's names and roles (brief p. 8, and the top of this page)
- The exact job title and team: confirm with the recruiter (brief p. 8)
- The hybrid schedule in Richmond (three days in the office, two remote): your answer, and your
  commute or relocation plan (sheet 20, brief p. 8)
- Work authorization and sponsorship: your answer, known before the panel (sheet 21, brief p. 8)
- Salary: your researched range for this role and level in Richmond, only if pressed. Keep it in
  your head; it is in no file (sheet 22, brief p. 8)
- Notice period and earliest start date (sheet 23)
- Travel (up to 25%) and storm-season hours you can commit to (sheet 18, brief A1)

**True stories** (situation, task, action, result; your resume does not hold these)
- A disagreement about a number or a definition: what you were responsible for, what you did, the
  outcome (sheet 6)
- A number that was wrong or nearly went out wrong: the check that caught it, the fix and the
  control you have used since (sheet 7)
- Overlapping deadlines, and how you ordered the work (sheet 4)
- Someone senior said your numbers were wrong (Q21)
- A time you said "I'll find out and come back" (Q22)
- One real break at work: cause, then control (Q17)
- One personal lesson (Q18)

**Facts only you know**
- Why Dominion: one personal reason (sheet 2). Why move: the real reason, said as a pull, and which
  Grid Resiliency program interests you and why (Q19)
- Power BI, Power Apps, SharePoint and the Power BI Service at work: the exact truth (sheet 13, Q12)
- The Mercury pipeline: what it fed, what you owned, the grain, incremental logic, scheduling, tests
  and one failure (Q16); who you worked with (sheet 8)
- Who used each dashboard you built, including The Life Initiative's (sheet 9, brief A1)
- One SQL query you can sketch on paper (sheet 11)
- Snowflake cost controls you have used (sheet 14)
- Any regulatory filing or governance work: the truth (Q14)
- The CSV and DataFolder route in Power BI: mention it only if you adopted the upgrade and tested it
  yourself (sheet 13)

## 4. The Monday plan (Monday, November 2)

Shift the times to your day `[you: …]`, but keep the order.

1. **Decide the variant first.** Everything after it depends on that choice.
2. **Drill by recall, not by rereading** (Roediger & Karpicke 2006; Rowland 2014: strong evidence).
   Rereading feels more certain, but recall practice is remembered better days later. Cover the
   answer, say it aloud, then check.
3. **Spread the drills** (Cepeda et al. 2006: strong). An afternoon round and an evening round beat
   one long block.
4. **Protect sleep** (Lim & Dinges 2010: strong). Going without sleep hit attention hardest
   (g = −0.78). The 20:00 stop is fixed.

| Time | Step | Done when |
|---|---|---|
| 08:30–09:00 | **News check.** Look for Dominion news since Sunday (steps below). Update "Dominion on a page" if anything moved. | Nothing moved, or the page is updated |
| 09:00–10:30 | **Step 1: adopt the upgrade or not (60–90 min).** Read CHANGES.md line by line. Fetch the bundle and rerun the checks on your laptop (step 1 above). If you adopt, publish it from your own GitHub account. | You can explain every change. If you can't by 10:30, use the public-repo version and move on. |
| 10:30–12:00 | **Adopted: apply the Power BI guide (60–90 min)** (step 6 below). Test it offline (Wi-Fi off): every page opens and the year slicer moves the cards. **Public-repo:** skip the report; practice explaining the model from deck slide 5 instead. | Adopted: the report opens offline, and the Summary page and the model view are printed for the Power BI questions. |
| 12:00–12:45 | Break | |
| 12:45–13:30 | **Read the brief once**, start to finish, for understanding. Mark anything you couldn't explain. | Marked list |
| 13:30–15:00 | **Give the deck aloud against an 8-minute timer, three times.** Record one run and listen back. Cut words, not slides. Also say the 30-second opener and the 60-second project story aloud. | A run of about 8:00, leaving 2 minutes for interruptions |
| 15:00–15:15 | Break | |
| 15:15–16:15 | **Drill the question sheet by recall.** Cover each answer, say it aloud in 60–90 seconds, then check. Mark misses. | Every sheet question answered aloud once |
| 16:15–17:15 | **Drill the hard 25.** The ● questions first, then the rest by panelist. Claim → proof → limit, aloud. | Misses marked |
| 17:15–17:45 | **Mock panel**, if someone can help. Three roles, 20 minutes, questions picked from the hard 25. If you're alone, shuffle them and time each answer. | Done |
| 17:45–18:30 | **Print** (step 5). Check page order. Pack the printouts, a laptop with the report working offline, charger, ID and directions. Interview time and place: `[you: …]`. | Bag packed |
| 19:30–20:00 | **Second drill round (spaced).** Only the misses, plus the opener. | Misses answered cleanly |
| **20:00** | **Stop.** No new material after this. Sleep. | |

**Tuesday morning (15 minutes):**
- Say the 30-second opener aloud twice.
- Reread the three takeaways.
- Check the news once.
- Leave early.

## 5. Printing

Print only the version you chose. Set the paper to US Letter and the scale to **Actual size**
(100%), not "Fit". Print in color if you can; every page also reads in black and white.

| What | File | Pages | Copies | Sides |
|---|---|---|---|---|
| Deck, one for each panelist to keep | `01_deck/…_v2_print_letter.pdf` (or `…_v2_public_print_letter.pdf`) | 14, landscape | 3 | Double-sided, flip on the short edge; staple top left |
| Deck, your copy to present from | the same file | 14 | 1 | Single-sided, so pages can lie side by side |
| Question sheet, for you only | `02_question_sheet/Dominion_question_sheet_v2.pdf` | 2 | 1 | Double-sided: one sheet |
| Brief, for you only | `03_interview_brief/Dominion_interview_brief_v2.pdf` | 12 | 1 | Double-sided; staple |
| Adopted only: the report's Summary page and the model view | from Power BI Desktop (step 6) | 2 | 1 | Single-sided |

Never hand over the sheet or the brief: they hold your answer cues and `[you: …]` notes. After
printing, check the page order and that nothing is cut off at the edges.

## 6. The Power BI steps (adopted version only)

The full guide is `04_powerbi/APPLY_GUIDE.md`. In short:

1. Update Power BI Desktop. The template was built and tested in version 2.159 (October 2026).
2. Copy `04_powerbi/data/` to `C:\DominionPowerBI\data\`.
3. Double-click `04_powerbi/Dominion_reliability_review.pbit`. When it asks for **DataFolder**,
   keep `C:\DominionPowerBI\data\` (the path must end with a backslash) and click **Load**.
4. File > Save As > `Dominion_reliability_review.pbix`.
5. Check four things: the Scorecard shows 2025 with 2.68M customers, SAIDI 144.4, SAIFI 1.320 and
   CAIDI 109.4; Data notes says "All 31 data tests pass" and "12 of 12"; on Fair comparison the
   dashed lines sit at SAIFI 0.93 and CAIDI 99.5; numbers show as 2,675,735.
6. Turn Wi-Fi off, reopen the `.pbix`, click through all 11 pages, and move the year slicer on
   Summary.
7. For the printouts: File > Export > Export to PDF and print page 1 (Summary); take a screenshot of
   the model view (Windows + Shift + S) and print it.

## 7. Publishing the upgrade (adopted version only)

`[B: D's steps from 05_repo/: fetch the bundle into your clone, rerun the checks, push the branch
from your own GitHub account]`

## If you are asked "Did you use AI tools?"

Panels in 2026 often ask, and the answer must be true. Here is a line to adapt in your own words:

> "Yes. I used AI assistants to help gather public data, write and test SQL and draft materials.
> I reviewed and reran everything, and I can walk you through any step."

Only say what is true for you. The printed deck, sheet and brief never mention how they were made.

## Monday-morning news check

Run this in a fresh assistant session opened at the repo root, or follow it by hand.

```text
Work in C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review.
Read first: interview-prep/research/freshness.md and interview-prep/research/dominion_on_a_page.md.

Task: find Dominion Energy news published after the last check in freshness.md (1 Nov 2026) on:
the NextEra merger (Virginia SCC case PUR-2026-00112, where rebuttal testimony was due 2 Nov; FERC
docket EC26-131; the NRC; North and South Carolina), Q3 2026 follow-ups or analyst events,
Virginia storms or outages, leadership changes, data-center or large-load rates, and CVOW.

Sources, primary first: news.dominionenergy.com releases, newsroom.nexteraenergy.com,
federalregister.gov, then Virginia news outlets. scc.virginia.gov blocks scripts; do not work
around any block. Cite only pages you opened, with the access date and a short quote.

If nothing moved: add one dated line to freshness.md ("2 Nov re-check: no change") and stop.

If something moved:
1. Append it to freshness.md with its source and quote.
2. Update dominion_on_a_page.md.
3. Make the same change in the "Dominion on a page" text of the highest-numbered
   interview-prep/work/brief/build_brief_v*.py, re-run that script with
   .venv\Scripts\python.exe -I, and confirm the brief PDF's page count did not change.
4. Add a row to interview-prep/research/claims_register.csv.

Research the company only: no searches about private individuals. Do not commit, push, upload or
publish anything. Finish with a three-line summary of what changed.
```
