# V6 re-check: the final pack, read again as the candidate

**What this is:** the final pack after the rebuild (rulings O-34 to O-40), read again as the candidate. It records whether each of my V6 top-10 fixes landed, what is new and would still hurt on Tuesday, and every contradiction I found between START_HERE and the printed files.

**What I read:**
- START_HERE (rewritten).
- The brief (12 pp), the adopted deck (14 pp, with notes from the .pptx), the public deck (14 pp, with notes) and the sheet (2 pp). Each was rendered at 110 dpi into `v6_pages/final/` and read as images.
- APPLY_GUIDE, and the 05_repo README and CHANGES.

**What I checked in the repo (read-only):**
- **The bundle matches the README.** SHA-256 `5521017…bc2`, tip `c17766a`, 36 commits on `ec8ecb6`, 88 files (+40,414 / −293). Commit times run 07:47–12:51 +0530, and the Claude trailer is on all 36.
- **The review list is accurate.** All nine ranges land on the stated lines at `c17766a` and sum to 393.
- **`trend_tests.py` prints the brief's numbers exactly:**
  - SAIDI +0.64, −1.87 to +3.15, p 0.58;
  - SAIFI p 0.54;
  - CAIDI p 0.74;
  - weather-adjusted +0.34, −1.41 to +2.08, p 0.67.
- **The timings match.** The notes are 1,030 words (7:56) and 960 words (7:23). Every per-slide time on brief p. 1 matches to the second.
- **The sheet's Q11 query is real.** It runs on real columns (`saidi_ex_med` and `utility_key` `19876|VA`, in `sql/02`).

Nothing was edited except this file and the renders. Nothing was committed or uploaded.

## Verdict

All ten fixes landed. Four new items are worth a line each before printing. The first matters most: as printed, the Appalachian Power answer sounds like a peer chosen by its result. Nothing else would hurt on Tuesday.

## 1. My top 10, re-checked

| # | Fix (V6 §4) | Status | Evidence |
|---|---|---|---|
| 1 | Scoped adopt rule, one authorship sentence | **FIXED** | **START_HERE §2:** four conditions, the 393-line list (ranges verified), decision by 11:15, Sunday option, and "The public version is complete" (l. 46). **§7:** publishing is optional and comes after the Power BI test, by squash; "Don't push the branch's commits as they are" names the identity, the +05:30 times, the trailer and PR visibility. **§8:** an adopted sentence and a public sentence, plus "Never say 'I reran everything' unless…". **README step 8:** a squash template with a "How it was made" paragraph that must stay true. The sentence also closes the adopted s6 notes and brief Q18. |
| 2 | Slide 6, p. 7 and Q15 show the real data path | **FIXED** | **Adopted s6** is redrawn: Sources → Downloads → SQL layers → Tests → CSV exports → Power BI Import. It has a legend ("Original build, Oct 27–31, 2026" / "Added Nov 1, 2026") and a Snowflake box saying the new tables arrive only via README step 7. **s5's source line** says "16 from the local DuckDB mirror, 2 from the workbook". The same appears on brief p. 7 ("The build"), in Q15, and in README step 5 ("Neither Power BI nor these checks connect to Snowflake"). D's 16/2 correction is in all of them. |
| 3 | Schedule and place the `[you: …]` work | **FIXED** | **When and how:** START_HERE "In short", §3 and §4 give a Sunday slot of about 2 hours, written in pen on the printouts, with no re-render. **Salary:** reconciled (§3 "the pack prints no figure", sheet Q22, the brief p. 8 slot). **Missing guidance, all added:** sheet Q11 gives the query; sheet Q9 says "nobody yet; I built it for this application"; the programs are on brief p. 2, in Q19 and in the s7 notes; Q17 and sheet Q7 tell the P18 story; Q12 explains the exceptions form; A4 has a "5-minute route"; storm duty becomes a question for the recruiter (§3, sheet Q18). |
| 4 | The engineer's four traps | **FIXED** | **46 kV:** Q1 says "From 2020 they count lines up to 46 kV (not adjusted; it can only push SAIFI and SAIDI up): 2020 sits 14.5 above the line, and the trend test across it still finds no rise (p 0.58)". The adopted s5 notes repeat it. **Proxy MEDs:** the A1 11.9× row, Q2 ("103 days… 2 to 18 a year; stand-ins, not Dominion's") and the s4 notes. **The trend test:** Q5 ("11 yearly points, t-test on 9 df… catch only a large, steady change"). **Whole-day resampling and CI vs PI:** Q5, the glossary and the s4 notes. |
| 5 | An honest model line for Q11 | **FIXED** | The line ("small star at the core; the others are pre-built summaries, so most stand alone; conform in production") is on brief p. 7, in Q11, sheet Q10, s5 (slide and notes) and APPLY_GUIDE. Q11 adds the counts: "18 imported tables, 2 calculated (Dashboard Year, _Measures), 2 relationships". START_HERE §6.7 warns that the printout shows 20 tables and 2 relationships. This matches the .pbit. |
| 6 | Glossary, and storm county-day defined in the s2 notes | **FIXED** | **Brief p. 2 glossary** covers every term I listed: MED/ex-MED, IEEE 1366, 2.5β with α and β, storm county-day, EAGLE-I/ORNL, PUDL, NCEI, HURDAT2/NHC, CPC, PJM, DOM zone (and why it is wider), CEMIn, OMS, AMI/last gasp, FLISR, SCC, FERC, NRC, DOE-417, CI vs PI and DuckDB. **The company box** adds VIM, VO and SUP. **The s2 notes** in both decks now define storm county-day and MED. |
| 7 | Company box, and "What do you know about Dominion?" | **FIXED** | **Brief p. 2, "Dominion Energy at a glance (November 1, 2026)":** 2.68M / 2.8M / 3.6M with a ready line for "If a panelist says 2.8M", leaders, Q3, the all-stock merger and its dockets, FPL as NextEra's Florida utility, CVOW, data centres, rates and the 50 bp, and the programs. **Sheet Q19** answers the question. |
| 8 | Re-time the Monday plan | **FIXED** | START_HERE §4 adds a Sunday block. Monday runs 08:30–20:00 with a slot to clear the marked list (13:30–14:00), a cut list and a "Never cut" line. Brief A4 step 2 now matches the public route. One small timer mismatch remains (§3d). |
| 9 | A news check I can run | **FIXED** | START_HERE §9 gives six URLs with their Nov 1 baselines and says what counts as moved. It lists where to correct in pen: the merger line on p. 2, Q23 and sheet Q19; all three carry the fact. The check repeats on Tuesday, and the optional prompt has no local paths. |
| 10 | Small consistency fixes | **FIXED** | **Base years:** brief p. 3 "Three base years, three answers"; the adopted s5 and public s4/s5 notes bridge the base years and the 465→796 vs 723→796 pairs. **Q1** now reads "2024 → 2025: 464 → 791". **A4** names the 30-second opener and writes the 60-second story. **START_HERE §2** says "most peers use IEEE 1366 (the brief says ten of the twelve)". **README** compares against `ec8ecb6`. **CEMIn** has one spelling (sheet Q16), and **STAR** includes Task (A4). |

**Also closed from V6 §2:**
- A1 now has rows for: the "Windows"/cross-quoting caveat; 351,738 vs 508,000; DOE-417 and HURDAT2; the Nov 2014 start; 2.68M / 2.8M / 3.6M.
- README: `git status`/stash, Python 3.12, a step-4 time estimate.
- APPLY_GUIDE: the Windows requirement, the 11:15 deadline, where each page comes from.
- s4: "on the map" removed.
- s5: an unreadable screenshot replaced by a readable detail.
- The `sql/09` header now explains Eastern Standard Time.

## 2. New things that would leave me stuck on Tuesday (ranked; real hurt only)

1. **"Why not Appalachian Power?": the printed answer sounds like choosing peers by their result.**
   - **The problem:** Brief A1, row "Dominion + 11 peers", says "fixed by EIA ID before results (D10)… Appalachian Power (SAIDI over 300) is apart". Said aloud, "it's apart because its SAIDI is over 300" invites "so you dropped a utility for its result?", right after I've claimed the set was fixed before results.
   - **The real reason is dropped.** My own October decision (D10, `docs/04_decisions.md:109`) says it is "held in a separate group and shown separately because its SAIDI exceeds 300 minutes and would compress the scale of every chart". The brief omits that reason.
   - **"Shown separately" can't be claimed for the template:** no report page names Appalachian Power, because the pages filter by peer group (checked in the .pbit).
   - **Why it matters:** it is the obvious question from a Virginia panel.
   - **Fix (one line in A1 or Q2):** "It's in the data in its own group (D10): at over 300 minutes it would squash every chart's scale. That's a judgement on a known outlier, so I'd add it back as a sensitivity check."
2. **"The same SQL runs in DuckDB", but the review list tells me to skip the runner that explains how.**
   - **The claim:** brief p. 7, Q15, the adopted s6 notes and README step 5 all say the same SQL files run in DuckDB.
   - **What the runner actually does:** it skips the Snowflake-only statements (warehouses, file formats, stages, COPY INTO, LIST, PUT) and fills the raw tables from local files (`run_local_duckdb_sources.py`, docstring lines 9–10). CHANGES `cd71bae` also mentions "four more Snowflake-to-DuckDB translations".
   - **The gap:** START_HERE §2 says "Skip… the DuckDB runner". A BI manager who knows Snowflake will ask how Snowflake SQL runs on DuckDB, and I'd have no answer.
   - **Fix:**
     - add the runner's docstring (lines 1–13, 13 lines) to the review list;
     - add one clause to Q15: "the runner skips the Snowflake-only load statements, reads the raw files directly and translates a few functions".
3. **Sheet Q13 tells me never to mention what my adopted slide 5 shows.**
   - **The conflict:**
     - the sheet's Q13 slot reads "[you: mention the CSV / DataFolder route only if you have built and tested it yourself]", and I didn't build it, so by the sheet I never mention it;
     - START_HERE §3 (l. 177–178) says "only if you adopted the extension and tested it yourself";
     - adopted s5 prints "18 tables, one DataFolder parameter".
   - **Fix:** change the sheet's wording to "adopted and tested it yourself", which also keeps the word "built" out of my mouth.
4. **The SCC staff's position on the merger appears only in START_HERE.**
   - **Where it is:** START_HERE §9, row 4 (l. 326): "The commission's staff (Oct 19): deny as proposed unless conditions are accepted."
   - **Where it isn't:** the merger line on brief p. 2, Q23 and sheet Q19.
   - **Why it matters:** if a panelist raises it and I've studied only the printouts, I'm caught cold.
   - **Fix:** add one clause to the merger line on p. 2.

Nothing else rises to "would hurt".

## 3. Contradictions between START_HERE and the printed files

**Checked and consistent:**
- **The brief's page references.** The p. 1 table of contents matches every page (Dominion page p. 2 … A4 p. 12). Also consistent: "page 4" on p. 1 and "Q2 in A2" on p. 2.
- **START_HERE's Q references** all point to the right brief questions: Q12, Q14, Q16, Q17, Q18, Q19 (programs), Q21, Q22, Q23 ("close is expected in H2 2027"), and Q11 for the model view.
- **Sheet references:** question 11 is the query, question 19 is "What do you know about Dominion?", and the sheet's Q2 is the A4 opener.
- **Slide references:** slide 4 = 11.9×, slide 6 has the legend, slide 8 has the takeaways, and "slide 2" / "slide 5" in the base-year table.
- **The ● count is seven.** Every file name and page count in START_HERE §1 and §5 matches.
- **D's two corrections:** the 16/2 CSV split is in s5, brief p. 7 and the README. The 2.4 GB / 20 min / 22 s figures reached START_HERE, s6 ("22 s") and brief p. 7, but not the README (item b below).

**Found** (all low except item a, which is §2 item 3):

- **a. The DataFolder condition differs.** Sheet Q13 says "built and tested"; START_HERE §3 says "adopted… and tested". See §2 item 3.
- **b. The re-download size and time differ between START_HERE and the README.**
  - START_HERE §2 (l. 84–85) says "about 2.4 GB, about 20 minutes on a fast connection, then a 22-second build", and §8 (l. 296–297) says "about 20 minutes".
  - README step 4 is headed "(optional: about 3 GB, about half an hour)", gives "1.7 GB" of EAGLE-I zips and says "Allow about half an hour… 4 GB of free disk".
  - README step 5 says the full build takes "about 25 seconds".
  - This affects planning only, but they are the two files START_HERE tells me to follow.
- **c. "Q19" means two different questions.**
  - START_HERE §3 (l. 166–167), "(Q19). Q19 and the brief's Dominion page say what each one does", means the brief's "Why move".
  - §9 (l. 337), "the sheet's question 19", means "What do you know about Dominion?", which carries its own placeholder ("[you: one sentence on why this team…]").
  - Both are right, but v3's convention line ("Qn" = brief hard question; "sheet n" = the sheet) is gone. One line would restore it.
- **d. The rehearsal instructions differ.** Brief A4 outline step 4 says "against an 8-minute timer, three times… Then the 5-minute route once". START_HERE §4 (14:00–15:15, l. 202) says "against your talk-length timer, two or three times", with no 5-minute route.
- **e. "On Monday" vs Sunday.** The adopted s6 notes end "[you: say the last sentence only if you did both on Monday]", while START_HERE l. 62 says "Do it on Sunday if you can".
- **f. START_HERE §3's placeholder list misses three placeholders:**
  - brief A4's opener, "[you: one line on why this role]";
  - sheet Q19's "[you: one sentence on why this team, in your own words]";
  - START_HERE's own §8, "[you: what you have used AI tools for in your own work, if anything]".
- **g. Two names for one company.** Brief p. 2 says "28% of Virginia Power's 2025 sales"; everywhere else it is "Dominion Energy Virginia". The glossary never says they are the same company.
