# Agent B (build) ledger

**Now (2026-11-01 14:20): the orchestrator's last batch (V1 final audit, V6 re-check; items 1–10) is applied, rebuilt and checked.** Adopted deck 14:09, sheet 14:10, brief 14:11, claims.csv 155 rows (152 MATCH, 3 pending: C-F-26, C-F-27, C-F-28). Details in "Resume from here".

**Earlier (13:50): the final pack is built and checked (rulings O-34 to O-39 after V6).**
- **Final files** (`deliverables/`, no version suffix):
  - `01_deck/Dominion_reliability_deck_adopted.pptx` + `_adopted_print_letter.pdf` (13:16), 14 pages
  - `01_deck/Dominion_reliability_deck_public.pptx` + `_public_print_letter.pdf` (13:17), 14 pages
  - `02_question_sheet/Dominion_question_sheet.html/.pdf` (13:16), 2 pages
  - `03_interview_brief/Dominion_interview_brief.html/.pdf` (13:30), 12 pages
  - `claims.csv` (13:30, rerun identical at 13:4x): 152 rows, 127 MATCH, 25 "orchestrator (pending)"
- **v3 moved** to `work/old_versions/` (13:4x); v0–v2 were already there. START_HERE names only the final files.

**Earlier (2026-11-01 10:31): v2 is finished, checked and ready for V1.**
- **Final files:**
  - decks (both variants) 10:28, 14 pages each
  - brief 10:27, 12 pages
  - sheet 10:19, 2 pages
  - claims.csv 10:28: 122 rows (both 75, adopted 35, public 12), every result "match"
- **Fork checker** (`work/claims/build_claims_v2.py`):
  - 0 numbers not covered by a claim; 0 quoted texts missing from their documents
  - no stale or cross-variant values; scans clean
  - every public-deck number is on origin/main (17 only after rounding; −4% and +2.8 are derived)
- **I rechecked:**
  - all 8 fixes in the rebuilt brief and sheet
  - brief p7, p9, p10, p11
  - adopted S8 (F11 strip) and public A2 (workbook values)
  - the UK and process-word scan on all four documents: clean

**Earlier at 10:20:**
- **P4 (B5) is done and verified (10:08, `b5/shots_final6/`).** The template opens and loads, and all
  11 pages render in Desktop. The shipped `.pbit` (SHA-256 b33409e9…) differs from the verified one
  only in the DataFolder default.
- **10:08:** event labels use the peak day, "Oct 12, 2018 tropical (Michael)", matching deck A6.
- **Last changes in the 09:47–09:59 passes:**
  - US-style dates (O-30)
  - the reconciliation table on the Scorecard (as docs/06 designs it)
  - the storm-rule column over 2014–2025 (D batch 6: GA Power and Duke Energy Florida show IEEE 1366)
  - straight lines, and TWh on the sales chart
- **v2 of the deck, sheet and brief** was built by B's fork (agent a83381d6ed25cecf0). It applies
  the V2 rulings (`work/reviews/V2_rulings.md`) and the G2 revision (`storyline_LOCK_G1.md`,
  "G2 revision"): two deck variants, one brief and one sheet.
  - Deck v2, adopted and public: 10:08–10:09, 14 pages each.
  - Sheet v2: 09:52, 2 pages.
  - Brief v2: 10:08, 12 pages (8 main + 4 appendix, O-29).
  - claims.csv: 10:12, 116 claims (both 70, adopted 34, public 12).
- **10:16–10:20, my proof review.** I read all 12 brief pages and sheet side 2, and sent the fork
  8 fixes. It is applying them now:
  - **Brief:**
    - Q24 causal "mostly because" → "in a stormier year"
    - Q9 drops "SCC docket site blocked automated access"
    - Q17 "Fixed Oct 27"
    - p4 "If asked:"
    - p7 the sources row has four year entries
    - p2 "4th highest of 12"
    - Q22 drops the untagged CI for r
  - **Sheet:** Q13's "opens without a live connection" is untrue for public-only (the original
    .pbix has six DirectQuery tables).
  - **Checked and fine:**
    - public S5 (no screenshot; the measure matches origin/main `powerbi/measures.dax`)
    - 145.3 is the same in both variants
    - the S5 Summary screenshot is byte-identical in `shots_v4` and `shots_final6`
    - no UK spellings or day-month dates elsewhere
- **START_HERE draft** (`work/start_here_draft.md`) now has:
  - the file map
  - the `[you: …]` list (22 on the sheet, 20 in the brief, grouped)
  - printing
  - the Power BI steps

  D's bundle steps wait for `deliverables/05_repo/`.
- **Next:** check the fork's fix pass, then tell the orchestrator it is ready for V1, then B6.

**Reference.** Brief: `interview-prep/MASTER_PROMPT.md` §2–§5, "Agent B". Outputs: `interview-prep/deliverables/`.

**States:** ○ not started · ◐ in progress · ✅ done · ⏸ waiting · ✖ dropped.

## Task table

| Task | State | Output | Notes |
|---|---|---|---|
| B0 design system, storyline v0, P4 plan, Q-sheet test, v0 pack, claims v0 | ✅ 08:04 | `work/design/`, `work/storyline_v0.md`, `work/powerbi_fix_plan.md`, `work/qsheet/`, v0 deck and brief in `deliverables/` | unchanged |
| B1 charts v1 | ✅ (fork) | `work/charts/v1/make_charts_v1.py` | S4 A1 levels + map + Isaias inset; S5 24-hour profile |
| B2 deck v1 | ✅ 08:59 (fork) | `deliverables/01_deck/Dominion_reliability_deck_v1.{pptx,_print_letter.pdf}`; `work/deck/build_deck_v1.py` | D22 values, 12 of 12; superseded by v2 |
| B3 question sheet v1 | ✅ 08:59 (fork) | `deliverables/02_question_sheet/Dominion_question_sheet_v1.{html,pdf}` | 24 ★ picks (G1b), 9.0 pt, exactly 2 pages |
| B4 brief v1 | ✅ 08:59 (fork) | `deliverables/03_interview_brief/Dominion_interview_brief_v1.{html,pdf}`; `work/brief/build_brief_v1.py` | R-028 line in S2 notes and brief |
| claims.csv v1 | ✅ 09:00 (fork) | `claims.csv` (91 rows) | checker covers deck, notes, brief, sheet |
| **B5 Power BI upgrade (P4)** | ✅ verified 10:08 | `deliverables/04_powerbi/` | see "P4 detail" |
| v2 (V2 + G2) | ✅ 10:28 (fork; 8 fixes from my proof review applied and rechecked) | deck v2 (adopted, public), sheet v2, brief v2, claims `variant` column | S5 screenshot = `work/powerbi/b5/shots_v4/crop_p01.png` (Summary, identical to final6) |
| (a) sheet aligned to top40 ★ | ✅ 10:38 (fork) | sheet v2/v3 | no membership difference; Q1/Q2 and Q16/Q17 swapped, 7 rewordings, H02 fix |
| Ruling 4: public S5 = original report | ✅ 10:45 (fork); v3 crop 11:04 | `work/powerbi/b6/orig_whatmoved_saifi.png` | v3 shows only the original's SAIFI chart; its CAIDI chart says "minutes to restore" |
| P4 titles review + CSV switch + O-33 CAIDI | ✅ 11:10 | `work/reviews/P4_titles.md`; template 49e5f2cb… | verified `b6/shots_v3b/`; see "Repo-bound" for the recommit list |
| v3 (O-33, V1 fixes) | ✅ 11:35 (fork) | `deliverables/*_v3*`, `claims.csv` (= `claims_v3.csv`, 127 rows; v2 kept as `work/claims/claims_v2_1046.csv`) | checker 0 uncovered, 0 exact_text misses; R's three facts kept and re-sourced |
| (b) V4 print proof | ✅ 11:50 | `work/reviews/V4_print_proof.md`; `work/reviews/v4_pages/`; `work/reviews/v4_scripts/` | all four pass; v2 margins (sheet 0.135 in, brief 0.208 in) fixed in v3 |
| (c) B6 START_HERE | ✅ 11:50 | `deliverables/START_HERE.md` | v3 names, public S5 = frequency chart, peer-median difference between decks, talk 7:54/7:38, R's prompt unchanged |
| Final rebuild (O-34 to O-39, V6) | ✅ 13:30 (fork); checked 13:50 | final names in `deliverables/`; `claims.csv` 152 rows; builders `work/deck/build_deck_final.py`, `work/qsheet/build_qsheet_final.py`, `work/brief/build_brief_final.py`, `work/charts/final/make_charts_final.py`, `work/design/final_text.py`, `work/claims/build_claims_final.py` | proofs `work/reviews/v4_pages_final/`; checks `v4_scripts/final_checks.py`: 0 problems |

## P4 detail (B5)

**Build.** One command: `.venv/Scripts/python.exe -I interview-prep/work/powerbi/b5/pbi_build.py --ship`.
- **Input:** the File > Export template of a COPY of the original (`b5/pbit_src/`). The original `.pbix` is untouched.
- **Outputs:**
  - `b5/out/Dominion_reliability_review_verify.pbit`: DataFolder = this machine's staged folder.
  - `deliverables/04_powerbi/Dominion_reliability_review.pbit`: DataFolder default `C:\DominionPowerBI\data\`.
- **The build is deterministic** (uuid5/sha1 ids): two runs give identical packages. The shipped
  `.pbit` differs from the verified one only in the DataFolder default (`b5/diff_pbit.py`).

**Model.**
- 18 imported tables, all through the `DataFolder` text parameter, with no Snowflake source (D22 storms from `storm_vs_saidi.csv`).
- Plus `Dashboard Year` and `_Measures`.
- 77 measures, each with a description, and 5 calculated columns.
- 2 relationships.
- Auto date/time is off.

**Report.**
- F1–F12 of the fix plan.
- 11 pages: Summary, Scorecard, What moved, Weather, Fair comparison, Outages by county, Storms,
  Growth, Demand and seasons, Demand summary, Data notes.
- Alt text on all 60 visuals.

**Changes after 09:10 (V3/G2/D batch 5):**
- **Storm scatter:** limited to 2015–2024, so the trend line equals the fit (104.3 + 0.0518x, r = 0.697, asserted in the build). Before, the line was a 2013–2025 fit: 94.9 + 0.0626x.
- **SAIFI trend axes:** made continuous, so the 2015 and 2020 counting-change lines draw.
- **What moved:** the two charts are stacked at full width.
- **CAIDI 2015 line:** named as on the SAIFI chart.
- **Peer quadrant:** medians of the 11 peers excl. Dominion (SAIFI 0.934, CAIDI 99.5, read from `peer_reliability_5yr.csv`), as dashed constant lines and in the quadrant measures. This matches D's batch 5 and G2 S3.
- **County chart:** titled "All utilities…", with the subtitle "(not Dominion's SAIDI)".
- **Storms page:** subtitle says "all utilities".
- **Ten-events table:** shows both peaks (Isaias 351,738 and 343,492 held 1 h) and "Hours to clear 90%".
- **Isaias curve:** "33.5 hours from the peak to clear 90% of the outage", with the share-cleared definition from sql/09 and "not a utility's % restored".
- **New line charts:** straight segments.
- **Sales chart:** labelled in TWh.

**Evidence.** Each pass opened a template copy, pressed Load (MSAA), checked for error windows
(none) and shot every page. I looked at the PNGs.
- `b5/shots_final6/` (10:08, final): p03 (county page with peak-day event labels).
- `b5/shots_final5/` (09:59): p05 (Fair comparison: IEEE 1366 relabel, 11-peer lines) and p11 (US dates).
- `b5/shots_final4/` (09:53): p02 (Scorecard with the reconciliation table).
- `b5/shots_final3/` (09:47): p02, p04, p09 (straight lines, TWh).
- `b5/shots_final2/` (09:40): all pages. I looked at p05.
- `b5/shots_v4/` (09:33): p01, p06–p10.
- `b5/shots_v3/` (09:28): p01, p03, p06, p07, p11.
- The parameter prompt of the shipped template: `b5/shots_ship/param_dialog_ship.png`.

Scorecard and Data notes show 2.68M / 144.4 / 1.320 / 109.4 and "All 31 data tests pass" /
"12 of 12". This machine shows Indian digit grouping (26,75,735), a regional-format artifact.
Don't use p06 or p11 as deck screenshots.

**Docs in `deliverables/04_powerbi/`:**
- `APPLY_GUIDE.md`:
  - Route A: copy `data/`, open the `.pbit`, Load, Save As.
  - Route B: by hand.
  - The change list, a pages table and reading notes.
- `measures.dax` (purpose of each measure), `m/*.pq` (19), `theme_dominion_review.json`, `alt_text.csv`.
- ~~`data/` (16 CSVs + workbook + MANIFEST.csv)~~: retired 11:00 to `work/powerbi/b6/_retired/deliverables_04_powerbi_data_1101/`.
  The template now reads the 18 CSVs straight from the clone's `data\output\` (D a810494 exported the two workbook sheets).

**Changes after 10:31 (P4 titles review, CSV switch, O-33):**
- Headers "Reliability performance and weather" / "Electricity demand and grid planning"; Summary sub-header without "drivers".
- Hour-growth titles "hours ending 1 to 5 a.m. / 1 to 5 p.m."; profile title; columns colored by those hours.
- Reference labels "2019 level", "2015 level", "Average of all hours".
- CAIDI = "minutes per interruption" on both cards, both CAIDI titles and axes, the peer scatter (title and axis), the peer table column and the measure description.
- Review list: `work/reviews/P4_titles.md` (`b6/p4_titles.py` + `b6/make_p4_titles_md.py`).
- Evidence:
  - `b6/shots_p4final/` (10:50–10:54)
  - `b6/shots_p4final2/` (10:58–11:01; Growth and Demand summary viewed for the hour colors)
  - `b6/shots_v3/` (11:05–11:09; Summary, Scorecard, What moved and Fair comparison viewed)
  - `b6/shots_v3b/` (final)

## Repo-bound (for the orchestrator to commit; B never commits)

Committed in 859b52d (10:3x). **Changed since, for the recommit (11:10 build, SHA-256 49e5f2cb…):**

| Repo path | From | Change since 859b52d |
|---|---|---|
| `powerbi/Dominion_reliability_review.pbit` | `deliverables/04_powerbi/` | the CSV switch, F2 headers, Summary sub-header, reference labels, hour titles and colors, CAIDI wording; verified `b6/shots_v3b/` |
| `powerbi/m/LoadGrowth.pq`, `powerbi/m/Programmes2025.pq` | `deliverables/04_powerbi/m/` | read `load_growth.csv` and `programmes_2025.csv` (D a810494) |
| `powerbi/m/DataFolder.pq` | `deliverables/04_powerbi/m/` | default `C:\path\to\dominion-reliability-review\data\output\` |
| `powerbi/measures.dax` | `deliverables/04_powerbi/` | `Hour colour` (HE1–5 blue, HE13–17 gold) and the `CAIDI ex MED` description |
| `docs/06_powerbi_report.md` | `work/powerbi/repo_bound/docs/` | DataFolder = `data\output\`, the two CSVs, CAIDI wording, the gold rule |
| unchanged | | `powerbi/theme_dominion_review.json`, the other 16 `.pq` |

**Notes for D:**
- `docs/05` "Quadrant lines" row: the report now draws the 11-peer medians (G2 S3). Both sets are already stated there; adjust the wording if you want the report's choice named.
- `docs/05` (from 29b179f) explains why the `Method` measure shows "Changed" for Georgia Power and Duke Energy Florida. The measure now evaluates 2014–2025 and shows "IEEE 1366" for both. Please update that sentence, which `measures.dax` replaces.
- My docs/06 replacement already carries D's 29b179f headline (ten of twelve on IEEE 1366) and the medians note from 7133aba.
- The workbook `StormIndex` sheet is stale (pre-D22) and no longer read by the report. Leave it, or regenerate it by script.

## Issues and gaps

1. **(open)** The public-only variant and P4. The original `.pbix` still has the pre-fix titles,
   such as "That gap is data centres" (V2 F46). Its six DirectQuery tables point at a Snowflake trial
   that no longer exists, and the template needs the branch's CSVs. In public-only, Saketh should
   therefore show no Power BI file, or adopt first. START_HERE will say so.
   - 10:05: told the fork that public S5 must not use the upgraded screenshot. Instead it shows the
     original page list, the model and the measure (D13).
2. **(open, orchestrator)** F13 decision range: I told the fork adopted = "D1–D22", public = "D1–D14". The ruling text says D1–D14 for both.
3. **(note)** The "2020: 46 kV lines added" and "2015: Automated Outage Recording" lines are
   Saketh's own annotations (docs/06 design rule). Kept unverified.
4. Earlier issues 1–7 (SUP naming, 99.8% of meters, p-values, S4 wording, 2026 cut-off, composite
   model, HTML dialogs) are resolved by orchestrator rulings O-20 and G1b and D's E1.
5. **(open, orchestrator)** The sheet's 24 questions have not been re-synced to R's 09:40 top-40 list.
6. **(open, orchestrator)** The brief's main-body tables are 10 pt. O-29 sets 10.5 pt for running text and
   9 pt for appendix tables; I read tables as not running text.
7. **(note)** The S8 close line ("tested Snowflake → Power BI pipeline") differs from the wording of
   sheet Q24. Both follow the storyline table.
8. **Resolved by rulings:** issue 2 (D1–D22 adopted, D1–D14 public), issue 5 (the sheet is aligned to the top40 ★
   with no membership difference, 10:38) and issue 6 (10 pt tables approved).
9. **(open, R)** R's morning prompt is pasted unchanged into START_HERE §9, as ordered. Its step 3 edits the
   "Dominion on a page" text in `build_brief_v*.py`, which brief v2/v3 does not have; it also says "data-centre". R should revise it.
10. **(open, D)** `05_repo/README.md` lines 97–101 still say the template reads "16 CSV files and the workbook" and
    copy the workbook into `data\output\`. After the CSV switch it reads 18 CSVs and needs only DataFolder.
    Regenerate the bundle after the recommit.
11. **(note)** The original report's What moved CAIDI chart says "Minutes to restore each outage…", and the original is never
    modified. So public S5 shows only its SAIFI chart (`b6/orig_whatmoved_saifi.png`), and START_HERE tells Saketh how to
    speak to it.
12. **(note)** Measure names keep "colour" (Bar, Row, Dot, Change and Hour colour). They show only in the Fields pane, and
    O-30 covers P1–P3 and START_HERE. Left unchanged.

## Hand-offs

**To the fork:**
- 09:16 V2 task.
- 09:22 G2 re-plan.
- 09:33 S5 screenshots, measures and P4 wording.
- 09:38 D batch 5 numbers and the final Isaias wording.
- 10:05 the public S5 fix.
- 10:16 brief fixes 1–7.
- 10:20 sheet fix 8.
- 10:3x sheet alignment (a); 10:4x ruling 4 (public S5).
- 11:03 the v3 task (O-33 items 1–8).
- 11:08 the print-margin addendum.
- 11:10 both S5 images.
- 11:18 R's verdicts (keep all three).

**To the orchestrator:** the repo-bound table above, issues 1 and 2.

**From:**
- the orchestrator: V2 rulings 09:15, trend numbers 09:16, G2 09:30, D batch 5 09:37
- D: `findings.md` §C5, `peer_reliability_5yr.csv`, `scripts/trend_tests.py` (94eb5e2)
- V2: `work/reviews/V2_truth_audit.md`
- V3: `work/reviews/V3_mock_panel.md`

## Resume from here

**14:20 state: the last batch (items 1–10) is in. Builders backed up first to the session scratchpad (`pre_batch/`).**
- **Text changes:**
  - `work/design/final_text.py`: new RUNNER sentence (in BUILD_UP, so brief p7, and in Q15); AUTHORSHIP ends "…only if you did both before the interview]".
  - `work/brief/build_brief_final.py`: R_FIXES gain CVOW, rates, VIM, SUP and the Dominion Energy Virginia name. FIXES change Q19 to "(19 sites planned)", give Q15 the runner sentence, and give Q23 "January 11, 2027" plus the Oct 19 staff line. A1 has the Appalachian text. `checks()` now fails if any of these is missing, or if the old wording or "Virginia Power" is still printed.
  - `work/qsheet/build_qsheet_final.py`: Q13 has the new `[you: …]`.
- **To keep the page counts** (the first builds went to 14 pages for the brief and 3 sides for the sheet):
  - brief p7 screenshot 5.0 → 4.4 in wide;
  - A1 table line spacing 11 → 10.3 pt (the A2–A3 spacing; still 9 pt type);
  - sheet Q13 lost 13 characters (", briefly", "the").
- **Claims:**
  - Exact text updated: C-Q-10, C-F-04 (used_in Q23), C-F-06 to C-F-10, C-F-17.
  - New: C-F-26 (staff line; the source is R-050, since R-096 is the solar coalition), C-F-27 (Appalachian 1.602 vs 1.211 and 342.2 vs 133.0, computed from data/output/fct_reliability.csv) and C-F-28 (translate(), lines 46–79).
  - Checker: 0 uncovered, 0 misses, 0 stale. Merge: 155 rows, 152 MATCH, 3 pending.
- **Checks:**
  - Pages 14/14/2/12. Smallest text 10.12/10.12/9/9 pt. Edges 0.95/0.95/0.323/0.344 in.
  - How-made words clean; `[you: …]` 23/23, adopted S6 notes 1.
  - Talk 7:57 adopted (S6 1:16 → 1:17, from item 10's extra word) and 7:23 public. "Virginia Power" appears nowhere in the pack, the .pbit included.
- **For the orchestrator:**
  - The ORCH verdict for C-B-01 still quotes 76 s and 7:56.
  - START_HERE line 138 says 7:56.
  - D10 itself has no "mountain"; the terrain note is docs/02:93 at ec8ecb6.

**13:50 state: final pack built (fork, 13:16–13:30) and checked by me. Reported to the orchestrator.**
- **My checks (13:4x):**
  - `v4_proof.py work/reviews/v4_pages_final final`: decks 14 pp each, min 10.12 pt, edge 0.95 in, images ≥289 ppi; sheet 2 pp, 9.0 pt, edge 0.323 in; brief 12 pp, min 9.0 pt, edge 0.344 in; all fonts embedded. Contact sheets (colour) viewed: nothing clipped.
  - Brief sizes by page: p3–p7 body 10.5 pt; p2 (company box + glossary) 10 pt; p1/p8 tables 10 pt (approved, issue 6); A1–A4 (p9–p12) 9 pt (O-29).
  - `final_checks.py`: how-made words clean in all four PDFs; the authorship sentence only in the adopted S6 notes (it ends them, then one `[you: …]`); public S6 notes without it; `[you: …]` sheet 23, brief 23; talk 7:56 adopted, 7:23 public; required strings present; no star schema, commit count, bundle or SHA. 0 problems.
  - Metadata: PPTX and PDF author "Saketh Bollina", nothing else. The brief HTML's one "AI" match is inside base64 image data (false positive).
  - Claims: reran `build_claims_final.py` then `merge_v1_verdicts.py`; both outputs byte-identical to 13:30. 0 uncovered, 0 exact_text misses, 0 stale, 0 public numbers off origin/main. checked_by: V1 125 (96 v2 audit, 29 v3 delta), orchestrator 2 (C-Q-10, C-S5-14P), pending 25 (C-B-01 changed; new C-F-01…C-F-12, C-F-14…C-F-25; no C-F-13).
- **Open for the orchestrator:** "AI pilot" ×3 on the sheet (Q2, Q3, Q5; resume wording); brief p2 at 10 pt; why-2019 reason not printed (p3 prints only "2019: the report's long view (its chart titles)"), so no `[you: confirm this was your reason]`.
- **Resolved since 12:25:** issue 10 (`05_repo/README.md` now says 18 CSVs and DataFolder); issue 9 (START_HERE §9 rewritten by the orchestrator, no `build_brief` reference).

**12:25 state: final rebuild in progress (rulings O-34 to O-39 after V6, `work/reviews/V6_candidate_read.md`).**
- **Fork a83381d6ed25cecf0 has the task (12:21).**
  - Phase 1 is the items that need no new facts.
  - Phase 2 starts when `work/v6_inputs/D_facts.md` and `R_company_glossary.md` land.
  - Final names have no version suffix: `_adopted` / `_public`, `Dominion_question_sheet`, `Dominion_interview_brief`.
- **Correction 12:24 (O-27):**
  - The printed brief says only "Use the authorship sentence in START_HERE §8…".
  - The AI sentence appears only in the adopted s6 speaker notes.
- **Adopted S5 image:** now `b6/s5_summary_detail.png`, the cards and the CAIDI chart, cropped from the same render. Printed text: titles about 9 pt, card labels about 7.3 pt, axis about 4.8 pt. The full page measured 5 / 4 / 2.6 pt. Brief p7 keeps the full page.
- **Claims:** the builder marks new and changed rows "orchestrator (pending)", and `merge_v1_verdicts.py` keeps them pending.
- **My checks for the finals:**
  - `work/reviews/v4_scripts/v4_proof.py <out> final`
  - `work/reviews/v4_scripts/final_checks.py`: how-made words, [you:] counts, timings, required strings.
- **Open question for the orchestrator:** the sheet prints "AI pilot" three times (Mercury, from the resume). It is kept as the candidate's own work.
- **After the finals pass:** move the v3 files to `work/old_versions/`.

**12:08 state: claims work done (orchestrator, after the V1 v3 delta). PDFs wait for V6.**
- **Claims pipeline:** `work/claims/build_claims_v3.py` writes `claims_v3.csv` and runs the checks. `work/claims/merge_v1_verdicts.py` then writes `claims.csv`.
- **`claims.csv`** has 128 rows. `checked_by` is the independent checker:
  - V1 for 126 rows: 30 verdicts from `V1_delta_v3.csv`, 96 from `V1_number_audit.csv`.
  - The orchestrator for 2: C-Q-10 is MATCH via R-106 (WWBT, fetched with HTTP 200); C-S5-14P is pending its spot-check.
  - My own check is in the new `producer_check` column.
- **Changes in this round:**
  - New row C-S5-14P: the public S5 screenshot's +6%, 1.24, 1.17, 1.32 (origin/main docs/06:37 and the workbook Trend sheet 1.244, 1.165, 1.32, read by me).
  - C-S5-12 now cites lines 401–403.
  - C-Q-10 cites R-106 first; the 8-Ks are secondary, with no vote counts. No deliverable prints the vote counts: checked in the deck text, sheet and brief.
  - C-S3-09 now also cites origin/main (V1's open item 3).
- **Checker:** 0 uncovered, 0 exact_text misses, 0 stale, 0 public numbers off origin/main.
- **Backups:** `work/claims/claims_v2_1046.csv`, `work/claims/claims_v3_1135_premerge.csv`.
- **Queued for the single rebuild after V6:** brief p4 prints the adopted 11-peer medians (0.93 / 99.5) untagged. Tag them "If adopted", or add "(adopted version; the public repo prints 0.96/105 including Dominion)".

**11:50 state: v3 complete, checkpoint sent.** Final files:
- decks `_v3` and `_v3_public` (11:13)
- sheet v3 (11:34:28)
- brief v3 (11:34:47)
- `claims.csv` (copied from `claims_v3.csv`, 11:35)
- the template (11:10)
- P4_titles.md (11:11)
- V4 (11:50)

`build_claims_v3.py` writes `claims_v3.csv` only: copy it over `claims.csv` after any rerun. No Power BI process is open.

**Earlier, 11:10 state (v3 in progress, ruling O-33 from V1):**
- **P4.** The template was rebuilt at 11:04 (CSV switch, hour colors, CAIDI = "minutes per interruption") and verified in `b6/shots_v3/`.
  - `work/reviews/P4_titles.md` is regenerated by `b6/make_p4_titles_md.py` (with `b6/p4_titles.py` for the raw text).
  - Committed files changed since 859b52d: the pbit, `m/LoadGrowth.pq`, `m/Programmes2025.pq`, `m/DataFolder.pq`, `measures.dax`, `docs/06`.
- **Fork a83381d6ed25cecf0** is building v3 (O-33 items 1–8, plus the 0.30 in print margins).
  - Images: adopted S5 and brief p7 use `b6/s5_summary_v3.png`; public S5 uses `b6/orig_whatmoved_saifi.png`.
- **R's checks (11:16, `research/V1_followups.md`):** all three were verified and nothing was cut (relayed to the fork at 11:18).
  - C-Q-10: shareholders approved on Sep 3, 2026 (R-104, R-105).
  - C-S6-06: the −44% comes from Dominion's June 8, 2026 release; hardened mainfeeders, no baseline stated (R-013).
  - Trim cycles: 4–5 years, neighborhood lines on 4 (R-076).
- **Then:**
  - V4: `work/reviews/v4_scripts/v4_proof.py <out> v3`, view the contact sheets, write `work/reviews/V4_print_proof.md`.
  - START_HERE: v2 → v3 names; public S5 = frequency chart; the [you:] counts.
  - Ledger; checkpoint.

1. **P4** is done (10:08). No Power BI process is left open. To rebuild:
   `.venv/Scripts/python.exe -I interview-prep/work/powerbi/b5/pbi_build.py --ship`
2. **v2** is done (10:28) and checked. Rebuild commands:
   - decks: `work/deck/` generator with `--variant`
   - brief: `work/brief/build_brief_v2.py`
   - sheet: `work/qsheet/build_qsheet_v2.py`
   - claims and checker: `work/claims/build_claims_v2.py`
3. **V1 checkpoint** sent at 10:31 ("ready for V1"). Next: apply V1, V3 and V4 fixes as they arrive.
4. **B6 START_HERE:**
   - variant choice, with the adopt steps and D's bundle and CHANGES.md from `deliverables/05_repo/`
   - the AI-use answer (private)
   - the file map
   - the `[you: …]` list
   - the rehearsal plan (R's `research/delivery_and_rehearsal.md`)
   - print notes
