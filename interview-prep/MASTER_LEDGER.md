# Master ledger: the Dominion Energy interview pack

**Opened:** 2026-11-01 06:39 (machine clock, SLST = UTC+5:30), orchestrator session f9e2a490 ·
**Brief:** `interview-prep/MASTER_PROMPT.md` · **Repo:** `client-apps/dominion-reliability-review`,
branch `interview-upgrade-2026-11` (local only, never pushed) · `interview-prep/` is in
`.git/info/exclude`: never committed, pushed, uploaded or published.

**Now (2026-11-01 14:20):** **Run complete.** G3 ✅; DoD-1 to DoD-10 ✅ (§2); the final report was sent to the owner.
- **Final pack:** `deliverables/`:
  - `01_deck/` `_adopted` and `_public` (pptx + Letter PDF);
  - `02_question_sheet/`, `03_interview_brief/`, `04_powerbi/`, `05_repo/` (bundle 55210174… at c17766a, 36 commits);
  - `START_HERE.md`.
- **Open for the owner:**
  - Q5: the candidate's adopt decision, made Monday per START_HERE §2.
  - Q4: the Snowflake pre-D22 objects.
  - Q6: the branch commits carry the owner's git identity; squash recommended.
  - An optional tidy-up: three October doc lines point at a deleted CHANGELOG.md.
- **Nothing is running.** Agents: R, D, B, V1, V2, V3 and V6 are idle (7 of 8 used).

---

## 0. How to use this ledger

- Single source of truth for the run. The orchestrator updates it at every gate, after every agent
  checkpoint, and at least every 45 minutes. A fresh session must be able to finish the run from this
  file, the three agent ledgers (`ledgers/`) and the brief.
- States: ○ not started · ◐ in progress · ✅ done · ⏸ waiting on the owner · ✖ dropped.
- Agent ledgers: `ledgers/R_RESEARCH.md`, `ledgers/D_DATA.md`, `ledgers/B_BUILD.md`.
- Hard rules: brief §4. Verification: brief §8. Nothing is "done" until its gate passes.

## 1. The brief, in the owner's words (verbatim)

2026-11-01, verbatim except one figure withheld at the owner's request:

> so this is my entire situation c:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\Saketh_Bollina_Resume.pdf
> this is me , now for this interview in virginia - where im based, we need to prepare the perfect high
> end level which is going to land me the job, i think i can print the final work which u do as a
> presentation deck - not too long as the interviewers might not entertain us, and i should also be able
> to udnerstand and present properly, you understand the job level role also , [target pay: withheld]
> now i think we lack major real quality data and real setup. im thining u can load all needed skills,
> research web for more needed info , we can chat back and forth and i was thinking we can make a highly
> detailed prompt for a fresh new session which maintain a master ledger and we can give it opus 5.5
> agents 3 of them for each massive task - like one for researrch one for finding and downloading high
> quality data and one for any other work and then we can give each agent also its own ledger, we need to
> plan sequence and let them do all the work end to end so we have perfeect needed fianl product. and i
> think one single sheet questionarire of highest asked questions for such roles - research backed, with
> best answers. we need to study all angles, psycoligcally and perfected, research backed, academic
> papers, highest quality data -- this is your internal instructions u dont need to mention this anywhere
> but your master ledger and your master prompt description perhaps. --- u need to think and refine adn
> eprfect and make the highly detailed prompt, i think we will let the session run for 6-8 hours and do
> all work thoroughly and in detail , verify and perfect and make the final needed materials.

> ok give me the detailed prompt, i have snowflake mcp in process of being setup

> so will it also make a interview preperation entire brief pdf not too many pages but where the data
> came from, how it was built, and what it does, how it can be useful - perfectly made in the best way
> i need it for my interview interview is on november 3rd

Phase 0 answers (2026-11-01 06:50):
> Power BI: Install it.
> Role: "i think its on their website u can do light search not too deep into it rather focus on teh main work"
> Format: "panel interview it will have 3 people"

## 2. Goal and definition of done

**Goal.** An interview pack the candidate can print and present on Tuesday 3 November 2026, finished in
this run on Sunday 1 November: P1 deck, P2 question sheet, P3 interview brief, P4 upgraded Power BI
report, P5 START_HERE. Priorities: (1) every claim true and defensible, (2) the candidate understands
it, (3) short and clear, (4) high-end look.

| # | Item | State | Notes |
|---|---|---|---|
| DoD-1 | P1 deck: ≤ 8 main slides; PPTX with notes; print PDF proofed (V4) | ✅ 14:15 | Adopted and public decks, 8 main + 6 appendix each.<br>• PPTX speaker notes: 7:57 and 7:23 at 130 wpm.<br>• Print PDFs: 14 pp, Letter landscape, min 10.12 pt, fonts embedded, no how-made words.<br>• Proofed by B on every page (`work/reviews/v4_pages_final/`), plus orchestrator renders (S5).<br>• V6 re-check: FIXED |
| DoD-2 | P2 question sheet: one sheet; 20–24 questions; answers only from the resume, `[you: …]` elsewhere (V2) | ✅ 14:15 | 2 pp (one sheet), min 9 pt; 24 questions + 5 to ask; 23 `[you: …]`.<br>• Experience from the resume (V2): the opener's "three years" = the resume's "3 years"; "AI pilot" is the resume's own (kept).<br>• Sheet Q19 = "What do you know about Dominion?" |
| DoD-3 | P3 interview brief: ≤ 12 pages (8 + 4); sources, build, what it does, how it helps Dominion; every number explained; 25 hard questions answered (V3); delivery section cited; print-proofed (V4) | ✅ 14:15 | 12 pp (8 + 4).<br>• Spec items 1–8 incl. "Dominion on a page" + glossary (p.2, O-38).<br>• Real data path (p.7, O-35); A1 every number; A2–A3 the 25 hardest; A4 delivery, cited, with the opener, the 60-second story and the 5-minute route.<br>• Logged deviations: p.2 and two tables at 10 pt; appendix 9 pt (O-29) |
| DoD-4 | P4 Power BI: apply guide, measures, theme and data files; any edited copy verified open, or marked unverified | ✅ 14:15 | APPLY_GUIDE (Windows note, 11:15 deadline, From column, model line), measures.dax, theme, `m/`, alt_text.<br>• `.pbit` 49e5f2cb verified open with all 11 pages (`work/powerbi/b6/shots_v3b/`, orchestrator viewed p2 and p11).<br>• Identical to c17766a:powerbi/ |
| DoD-5 | P5 START_HERE.md | ✅ 14:15 | Rewritten (O-34 to O-39; V6 re-check FIXED, and its new items applied): final names, no TODO; the manual news check plus a self-contained prompt; true authorship and AI-use lines |
| DoD-6 | V1 audit: 100% of `claims.csv` rows checked and matching | ✅ 14:12 | 155 rows, 155 MATCH, 0 pending.<br>• checked_by: V1 131, orchestrator 24, none by its producer (the merge script asserts it).<br>• C-F-03, C-F-04 and C-F-26 lean on web-search evidence because the primary sites blocked automated access; their verdicts say "pages not opened" |
| DoD-7 | V5 freshness check done on the final day | ✅ 09:13 | `research/freshness.md`; re-run by the 2 Nov morning prompt |
| DoD-8 | Repo upgrade: sources with manifests, tests T13+ pass, docs updated, local commits only | ✅ 14:05 (re-verified) | **Final, at c17766a:**<br>• 36 local commits, no upstream; origin has no interview-upgrade branch, and main is ec8ecb6.<br>• T1–T6 PASS with 130.2 / 133.0; "All committed-output checks passed."; T7–T31 "All 25 tests passed" (22.7 s); trend tests match the pack.<br>• 12 `data/raw/*/MANIFEST.csv` + the output manifest.<br>• Docs fixed under O-40.<br>• No blob > 25 MB; bundle 55210174… verifies.<br>**Earlier evidence:** fresh run by the orchestrator: T1–T6 PASS; T7–T31 "All 25 tests passed"; `check_output_metrics.py` 104 PASS; `trend_tests.py` matches the pack. 12 `data/raw/*/MANIFEST.csv`. Docs 01–08 + README updated. Branch at 2cbd7a8 with 33 local commits and no upstream; `git ls-remote` shows origin unchanged (main ec8ecb6, no new branch). No blob > 25 MB. Bundle verifies (complete history) |
| DoD-9 | Ledgers complete enough that a fresh session could continue from them | ✅ 14:20 | This ledger (Now, decisions O-01 to O-40, Q1–Q6, change log) plus `ledgers/R_RESEARCH.md`, `D_DATA.md`, `B_BUILD.md`, all current to the final build |
| DoD-10 | Nothing from `interview-prep/` committed, pushed or published; no pay figure in any file | ✅ 14:15 (re-verified) | `git ls-files` has 0 interview-prep paths; `.git/info/exclude` holds it; no Artifact, Docs or upload used.<br>• No pay figure in any deliverable.<br>• The job board's pay estimate ("salaryDesc") was found in three saved copies of the posting under `work/` and redacted in place. No file in interview-prep now carries a pay figure.<br>**Earlier evidence:** ✅ 12:05 | `git ls-files` has no interview-prep, .pbix, resume, _setup, .mcp.json or CLAUDE.md. No artifact, Docs or upload used. Pay scan of every deliverable: only the approach and `[you: …]`; no figure. The decks carry no phone or email; the printed pack has no how-made mentions ("AI"/"prompt" in the sheet are the resume's Mercury AI-pilot facts) |

## 3. Step table

| Step | Owner | State | Output | Notes |
|---|---|---|---|---|
| P0 Setup | Orch | ✅ | this ledger, `ledgers/`, folders | 06:39–06:55 |
| R1 Role (light search, per owner) | R | ✅ 07:25 | `research/role_brief.md` | BI Analyst, Grid Resiliency, ~80% sure (O-16) |
| R6 Scouting for D | R | ✅ 07:36 | `research/for_D.md` | SCC 403 gap (O-17) |
| R2 Dominion dossier | R | ✅ 08:20 | `research/dominion_dossier.md`, `research/dominion_on_a_page.md`, `research/for_B.md` | R-028 storm attribution (O-24) |
| R3 Domain primer | R | ✅ 08:58 | `research/domain_primer.md` | SCC rule origin = gap (403) |
| R4 Interview science | R | ✅ 08:58 | `research/interview_science.md` | reappraisal = small edge; power posing out |
| R5 Question bank | R | ✅ 08:45 | `research/question_bank.csv` (126), `research/top40.md` | 24 ★ locked at G1b (O-23) |
| R-reg Claims register | R | ○ | `research/claims_register.csv` | ongoing |
| D0 Baseline | D | ✅ 07:05 | `ledgers/D_DATA.md` | checks pass |
| D1 Re-verify §2.2 | D | ✅ 07:12 | `work/data/reverify_2_2.md` | 12 match; F12/F13 wording; F15 partial (O-11) |
| D2 Acquire sources | D | ✅ 07:56 | `data/raw/<source>/MANIFEST.csv` | EAGLE-I 2014–2025 (DOE Aviary, 14/14 checksums), EIA-861 + 861M, Census/ACS, HURDAT2, degree days, DOE-417 (PNNL), PJM tables. SCC = gap (O-17) |
| D3 Validate | D | ✅ 08:55 | `docs/03_data_quality.md`, tests T13–T31 | all pass locally; D22 fixed the Bedford double count (O-21); T21 fails in Snowflake only (Q4) |
| D4 Model | D | ✅ 08:55 | DuckDB + Snowflake (24 new objects, add-only), `data/output/` | `sql/09`–`11`; 25/25 counts equal DuckDB |
| D5 Analyses A1–A6 | D | ✅ 08:55 | `work/data/findings.md` | A1 11.9×; A2 ten largest + Isaias; A3 map; A4 load; A5 13/13; A6 arithmetic (no dollar value) |
| D-x Quick checks (scope VA vs VA+NC, fit t / r CI, peer rule) | D | ◐ | `work/data/findings.md` | asked 08:50 |
| B0 Design system, storyline v0, PBI fix plan, Q-sheet layout test, v0 safety-net pack | B | ✅ 08:08 | `work/design/`, `work/storyline_v0.md`, `work/powerbi_fix_plan.md`, `deliverables/01_deck/*_v0*`, `deliverables/03_interview_brief/*_v0*` | safety net exists: deck v0 (14 slides) + brief v0 (10 pp), proofed colour and grey |
| B1 Charts | B | ✅ | `work/charts/` | dataviz; automatic label-collision checks |
| B2 Deck v1 → v2 | B | ✅ v2 10:28 | `deliverables/01_deck/*_v2*` (adopted + public) | 14 pp each |
| B3 Question sheet v1 → v2 | B | ✅ v2 10:19 (top40 wording alignment pending) | `deliverables/02_question_sheet/*_v2*` | one sheet |
| B4 Interview brief v1 → v2 | B | ✅ v2 10:27 | `deliverables/03_interview_brief/*_v2*` | 12 pp (8 + 4) |
| B5 Power BI upgrade | B | ✅ 10:08 | `deliverables/04_powerbi/` + repo `powerbi/` (859b52d) | verified open in Desktop |
| B6 Print proofs (V4), START_HERE | B | ◐ | `work/reviews/V4_print_proof.md`, `deliverables/START_HERE.md` | after D's `05_repo/` |
| V1 Number audit | Reviewer | ✅ 10:58 (fixes pending in v3) | `work/reviews/V1_*` | 117/122 MATCH, 2 ROUNDING, 1 MISMATCH, 2 UNVERIFIABLE; ruling O-33 |
| V2 Truth audit | Reviewer | ✅ 09:08 (fixes pending in v2) | `work/reviews/V2_truth_audit.md`, `work/reviews/V2_rulings.md` | ownership framework O-26; fixes F7–F17 |
| V3 Mock panel (3 interviewers) | Reviewer | ✅ 09:17 (fixes pending in v2) | `work/reviews/V3_mock_panel.md` | storyline revision O-28; R answers the 25 hardest |
| V4 Print proof | Orch / B | ✅ 11:45 | `work/reviews/V4_print_proof.md`, `work/reviews/orch_spot/` | B: every page, color and gray, min sizes, fonts, ppi. Orchestrator spot check 10:40 |
| V5 Freshness | R | ✅ 09:13 | `research/freshness.md`, `research/morning_prompt_2nov.md` | nothing changes the deck; the 2 Nov morning prompt repeats the check |
| V6 Candidate read | Reviewer | ✅ 12:10 (re-check after the final rebuild) | `work/reviews/V6_candidate_read.md` | on v3 + START_HERE + APPLY_GUIDE + 05_repo README. The numbers hold; top-10 fixes → O-34 to O-39 |

## 4. Gates

| Gate | Target (machine clock) | State | Outcome |
|---|---|---|---|
| G1a storyline lock | ~09:25 | ✅ 08:05 | Conditions met at 08:00: R1 in; EAGLE-I (14/14 checksums) and sector sales validated (T13–T24 pass); SCC attempted (403 gap); D1 done; 2025 values match the EIA-861 final. Locked in `work/storyline_LOCK_G1.md` (O-19) |
| G1b question shortlist | when R5 lands | ✅ 08:50 | R's 24 ★ picks locked (O-23); sheet Q19 later swapped for "What do you know about Dominion?" (O-38) |
| G2 v1 + V1–V5 | ~11:55 | ✅ 11:00 (fixes flowing into v3) | V2 09:08: ownership → two variants (O-26/27). V3 09:17: storyline revision (O-28). V5 09:13: nothing moved. V1 10:58: 117/122 match; the public deck must not contradict the public repo (O-33). V4: orchestrator spot check 10:40 + B's full log due with v3. P4 verified open (10:08) and committed (859b52d) |
| G3 V6 + DoD | ~13:55 → ~15:30 | ✅ 14:20 | V6 12:10 → O-34 to O-40 → the final build. V6 re-check: all ten FIXED; its four new items fixed. V1 final: all rows MATCH after the fixes. DoD-1 to DoD-10 ✅ with fresh evidence |
| Final report | ~14:10 | ✅ 14:25 | Sent to the owner |

## 5. Decision log

| # | When | Decision | Reason |
|---|---|---|---|
| O-01 | 06:45 | This session started in `renvia-technologies`, so the repo's `.mcp.json` did not load: there are no `mcp__snowflake__*` tools here or in the agents. Read-only Snowflake queries go through the managed MCP server over HTTP (`_setup/snowflake/test_mcp.py` pattern, role MCP_READER); `snow sql -c dominion` (ACCOUNTADMIN) is used only to run new committed build files (`sql/09_…`+). DuckDB is the local mirror and fallback for all analysis. | Local `CLAUDE.md` (01-11): "Prefer the snowflake MCP tool for queries. `snow sql -c dominion` … use it only for builds." Never wait on Snowflake. |
| O-02 | 06:45 | MCP card question not asked. | Local `CLAUDE.md` says the MCP server works end to end since the card was added. |
| O-03 | 06:48 | Python packages added to `.venv` with `uv pip install --python .venv/Scripts/python.exe` (the venv has no pip): matplotlib, python-pptx, pymupdf, openpyxl, pyarrow, python-docx, pypdf, pdfplumber, shapely, statsmodels (+ deps). | Charts, PPTX, PDF proofing, SCC PDF parsing, count model. Installed once to avoid agents racing. |
| O-04 | 06:50 | R1 is a light search of Dominion's careers site only; no deep job-board trawl. | Owner: "light search not too deep … focus on the main work". |
| O-05 | 06:50 | Panel of three → V3 plays three interviewers; print 3 leave-behind decks + 1 for the candidate; deck must work on screen and on paper. | Owner: "panel interview it will have 3 people". |
| O-06 | 06:52 | Power BI Desktop: owner said install. Started `winget install --id 9NTXR16HNW1T --source msstore` (per-user Store build) in the background. | Enables B5's open-and-screenshot verification loop. |
| O-07 | 06:53 | Branch `interview-upgrade-2026-11` created from `main` (ec8ecb6), working tree clean. Git identity on this machine is user.name "." with the owner's noreply email; commits carry the Claude co-author trailer. | Brief §4 repo rule 2. Noted for START_HERE's push section. |
| O-09 | 06:57 | Owner asked to use the `claude+tools` toolkit and run end to end. B reads its README/CATALOG and the print-relevant skills (award-web-design typography and layout, web-interface-guidelines, accessibility); the web-motion and 3D parts don't apply to print. | Owner instruction; the brief marks the toolkit as optional and web-focused, so `dataviz` still governs charts. |
| O-10 | 07:00 | D is the only agent that commits during the run; B lists repo-bound edits (e.g. `powerbi/measures.dax`, `docs/06`) for the orchestrator to commit. | Avoids two agents racing on the git index; one logical change per commit. |
| O-11 | 07:35 | Brief §2.2 wording is superseded by D's re-verification (`work/data/reverify_2_2.md`, F01–F15): winter set the yearly peak in **2019**, 2022 and 2025 (2026 a 29 MW tie to 30 Oct); "night +41%" is the single 4 a.m. hour, so say "hours ending 1–5 a.m. rose 39–41%, 1–5 p.m. about 27%"; "47 of the top 50 hours" is within the EIA-930 record (Jul 2018–Dec 2025); time-varying-rate share is unverified, so it stays out until D verifies it. | Truth first; the .pbix titles carry the same errors (B fix plan F3). |
| O-12 | 07:35 | S5 title drops "now", because winter also peaked in 2019. | Avoids implying a new pattern the data doesn't show. |
| O-13 | 07:35 | **S2 base-year risk:** the 3-year average moves 130.2 → 133.0 only because 2025 replaces 2022, yet the frequency/duration split uses 2023 (a low year) as its base. D will decompose 2022→2025 as well as 2023→2025, with the 2015–2025 trend. G1 locks whichever framing holds under both bases. | A reliability engineer on the panel will ask "why 2023?". |
| O-14 | 07:35 | Print gold `#D5A20B` replaces `#E8B117` for printed marks (dataviz lightness band); `#E8B117` stays in the Power BI theme. Type: Segoe UI only. | B's palette check; deviation logged in DESIGN_SYSTEM.md. |
| O-15 | 07:35 | P4 must-fix **F1**: six .pbix tables are DirectQuery to the candidate's old Snowflake trial and never render offline (seen by B in Desktop). They move to Import from `data/output/*.csv` through a folder-path parameter. D exports the CSVs. | P4's outcome is "opens offline on the candidate's laptop". |
| O-16 | 07:35 | Role (R1, ~80% sure): **Associate BI Analyst / BI Analyst, Richmond, hybrid 3-2, supporting Grid Resiliency programs**. Posted 10–11 Sep 2026, now closed. Tools: Power BI, SQL, Excel, Snowflake, Power Apps, SharePoint. Tone is practical and at that level; the posting says Dominion cannot sponsor visas, so work authorisation stays `[you: …]` and is never assumed. | Owner asked for a light search; the posting matches the resume's wording. |
| O-17 | 07:40 | Virginia SCC docket site returns 403 to scripts: recorded as a gap, never worked around (brief §4, §10). A plain public PDF elsewhere (Dominion, rga.lis.virginia.gov) is a fair source. The deck and brief say what the SCC filings would add. | Brief §10 default. |
| O-18 | 07:40 | R's order changed to R2 → R5 → R3 → R4. | The question sheet (P2) depends wholly on R5; B can draft definitions from repo docs until R3 lands. |
| O-19 | 08:05 | **Storyline locked (G1a)**, `work/storyline_LOCK_G1.md`. S2 rests on **2022→2025**: the 3-year average moves only because 2025 (144.4) replaced 2022 (136.0), with SAIFI +10.1% and CAIDI −3.6%. 2025 SAIFI 1.320 is the highest of 2013–2025. "Mostly frequency" holds for every base year in which SAIDI rose (D, findings §S2). Two-sided lines go in the notes and the brief: 2023→2025 is 79% frequency; 2025 SAIDI is below 2018 and 2019; neither 11-year trend is significant (p 0.54, 0.74); weather-adjusted shows no clear trend (+0.34 min/yr, p = 0.67). S4's headline may switch to D's A1 county-day comparison if robust. A6 = the ten largest events if validated. | Defensible under the "why 2023?" question; locked early because the G1 conditions were met at 08:00. |
| O-20 | 08:15 | B's four lock queries ruled (lock file updated): (1) programme names follow R's sources (R-035: Strategic Underground Program is separate from Grid Resiliency); (2) "99.8% of meters are AMI", not customers; (3) p-values SAIFI 0.54, CAIDI 0.74, SAIDI 0.58 (the orchestrator had mislabelled them); (4) S4 title "Years with more storm days had more outage minutes; …", because "meant" read as causal. 2026 demand figures use one cut-off date stated by D. | Truth first; B's checks were right. |
| O-21 | 08:25 | **Bedford city double count → fix (D22).** It was a real duplicate: Bedford city merged into Bedford County in 2013, so every zone-34 storm was counted twice (38 county-days, 2013–25). The fix is a SQL change, re-exports, check-script expectations (465 → 464, 796 → 791) and doc updates. Snowflake stays add-only: never CREATE OR REPLACE the existing STORM_INDEX. | Truth first; a known double count stays in no number we present. r, 145.3, 133.1 and the Q10 slope are unchanged per D. |
| O-22 | 08:25 | **S4 headline = D's A1:** outage customer-hours per 1,000 customers on storm county-days are 11.9× calm days (95% CI 7.9–16.9; 6,108 storm county-days); robust on non-major days (9.9×), in Dominion-only counties and in every year. Composite: the A3 map plus an inset Isaias restoration curve (90% in 33.5 h). r = 0.70 (n = 10) moves to appendix A2. A6 = ten largest events. 2026 cut-off = the hour ending midnight, 29 Oct 2026. | Answers the "your weather fit has ten points" objection with thousands of county-days. |
| O-23 | 08:50 | **G1b question shortlist** = R's 24 ★ picks (`research/top40.md`), unchanged: O1, O2, O9; B8, B6, B2, B4, B1; T1, T4, T36, T3, T7, T17; U1, U2, U3; R4, R2; R5, R7, R6, R10 (`[you: …]`); C1; plus 5 asks and a closing line. T7's answer covers Power BI performance and refresh, from the project and general knowledge, never as work experience. | The brief: "R's frequency table picks them, not taste". This covers every required group. |
| O-24 | 09:00 | R-028: Dominion's own report attributes the 130 → 133 rise "primarily due to increased storm activity". S2 notes and the brief say ours is consistent (the rise is in frequency; storm county-days up), so the deck never seems to contradict Dominion. | Credibility with a panel from Dominion. |
| O-25 | 09:10 | D ran read-only pre-build checks, a comparison query and the warehouse suspend through `snow sql` (ACCOUNTADMIN) instead of the MCP HTTP route: accepted, because the brief's D0 allowed a read-only count that way and nothing was written. From now on, reads go through MCP HTTP or DuckDB. | The local CLAUDE.md reserves `snow sql` for builds; no harm done. |
| O-26 | 09:13 | **Ownership framework (V2 F1–F6, F9, F16).** The pack ships in two variants:<br>• **Adopted** (main): it presents the 1 Nov upgrade, valid only once the candidate reviews, reruns and publishes the branch from their own account on Monday (START_HERE step 1, using a git bundle and CHANGES.md).<br>• **Public-repo-only** (fallback): what their public `main` holds today.<br>No first-person stories of fixes the candidate didn't make; their own D13 and P18 are the true examples. Wording fixes F7–F17 apply to both variants. | Truth first: the candidate must not present work as theirs until they have adopted it, and the deck must not contradict their public repo. The owner's brief intended the repo upgrade to be published from the candidate's own account (P5). |
| O-27 | 09:13 | START_HERE (candidate-only) carries a short honest answer for "did you use AI tools?"; the printed P1–P3 still never mention how they were made. | Panels in 2026 commonly ask; every answer must be true (brief §4). This doesn't break the brief's "deliverables never mention how they were made", which concerns the printed pack. |
| O-28 | 09:21 | **G2 storyline revision** (lock file, "G2 revision"):<br>• **S2** re-claimed as "Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions", consistent with Dominion's own storm explanation, with no clear trend once storms are counted.<br>• **S3:** "Dominion and 11 peers", medians excluding Dominion.<br>• **S4:** one visual (storm vs calm levels); the map and inset move to the appendix, brief and Power BI, labelled "all utilities" or restricted to Dominion-only counties.<br>• **S5 NEW:** the Power BI report (a real screenshot, star schema, named measures).<br>• **S6** how it's built; **S7** first 90 days (humble); **S8** takeaways aligned.<br>• Load shape moves to the appendix. Every "For Dominion" instruction becomes a "Why it matters".<br>• Only the deck has two variants; the brief and the sheet are variant-neutral.<br>• Talk target ≈ 8 min. | V3 high items P1, P2, P11, P12, P18, P29, P30. The old S2 framing failed its own appendix; Power BI is the posting's first duty and was missing; the tone was too grand for the level. The brief allows storyline improvement while keeping the arc and length (8 main slides, ≤ 6 appendix). |
| O-29 | 09:46 | **Brief page budget:** ≤ 12 pages, main ≤ 8 (cover and contents included), appendix ≤ 4:<br>• A1: know every number (1 page)<br>• A2–A3: the 25 hardest (2 pages, compressed from R's ≈2.3 by tightening, never by dropping)<br>• A4: delivery and rehearsal (1 page)<br>The full Monday hour-by-hour plan goes to START_HERE. Running text ≥ 10.5 pt; appendix tables and Q&A ≥ 9 pt (logged deviation). | The brief's caps (§3 P3); R's material ran to about 5–6 appendix pages. |
| O-30 | 09:46 | US English across P1–P3 and START_HERE (program, color, analyze). | An American panel; the posting says "Grid Resiliency programs". |
| O-31 | 10:35 | B's v2 queries:<br>• The adopted deck cites D1–D22, the public deck D1–D14.<br>• The sheet's wording follows the current top40 ★ list (membership locked).<br>• Main-page tables at 10 pt are OK.<br>• Public S5 shows the candidate's own current report (a cached page with none of the known title errors), or the model plus measures and "live demo on my laptop"; never the upgraded template. | Each variant describes only what exists in that variant. |
| O-32 | 10:52 | Every Power BI table loads from `data/output/`. D exports the two workbook sheets to CSV by a committed script; B switches the two M queries and re-verifies the template opens. The candidate sets one folder and copies nothing. | Fewer steps on the candidate's laptop on Monday. |
| O-33 | 11:00 | **V1 fixes (v3):**<br>• The public deck states only true things the public GitHub won't contradict: medians "of the 12 (including Dominion)" 0.96/105 as origin/main prints them; "methods differ; Dominion uses its own rule" with no "10 of 12"; public A6 method labels as on GitHub with the footnote "Other in 2013 only".<br>• Test label "12 on the original build (6 reliability, 3 storm, 3 demand), 19 new".<br>• CAIDI = "minutes per interruption" everywhere, including the Power BI title.<br>• Claims rows added for every uncovered number.<br>• Talk times fit both variants.<br>• Unverifiable facts are verified by R or cut by 12:00. | Truth first. In the public variant the candidate must not contradict the repo a panelist can open, and must not repeat its known error either. |
| O-34 | 12:25 | **Adopt rule (V6 #1).**<br>• Adopting means: a scoped review (D's list, about 400 lines), the three light checks and the Power BI offline test, all before a stated decision time. That takes about 2–2.5 h and can be done on Sunday.<br>• Publishing is optional and comes after the Power BI test. The recommended route is a local squash onto main with an honest "How it was made" paragraph.<br>• Pushing the 33 commits, as a branch or a PR, is advised against: they carry the owner's GitHub no-reply identity (O-07), 1 Nov +05:30 times and the Claude trailer.<br>• Not publishing is allowed, because adopted slide 6 shows what was added on 1 Nov.<br>• START_HERE §8 gets an adopted and a public version and drops "reran everything".<br>• START_HERE says the public talk is complete. | V6 found:<br>• the old rule unrealistic: 3,818 changed lines, data excluded, to review in 90 min;<br>• its order wrong: publishing came before the test;<br>• nothing on what GitHub would show;<br>• no true authorship sentence. |
| O-35 | 12:25 | **Data path (V6 #2).** Adopted slide 6, brief p.7 and Q15 show: sources → downloads → SQL layers in the local DuckDB mirror → tests → CSV → Power BI Import.<br>• Snowflake holds the October build. The new tables reach it only through the optional load step.<br>• A provenance legend: "Original build, Oct 27–31, 2026" / "Added Nov 1, 2026".<br>• The authorship sentence ends the slide 6 notes and answers Q18. | The old slide had EAGLE-I flowing through Snowflake, but `export_powerbi_csv.py` exports from DuckDB. The legend keeps the adopted deck true without any how-made words. |
| O-36 | 12:25 | **`[you: …]` work (V6 #3).**<br>• A Sunday slot of 90–120 min, plus the recruiter email.<br>• The answers are written in pen on the printed sheet and brief; nothing is re-rendered.<br>• The pack prints no pay figure; the salary slot is the candidate's own, in pen. START_HERE §3 is reconciled to this. | The 42 items had no slot, and the salary instructions contradicted each other. |
| O-37 | 12:25 | **Engineer and BI traps (V6 #4–#5).** No new analysis on the final day.<br>• 2020 46 kV: the change can only raise 2020–25, and the test still finds no clear trend. Not adjusted; the robustness check is named.<br>• Proxy MEDs (D18).<br>• The trend test: OLS on year, t-test, 9 df, low power stated qualitatively.<br>• Whole-day resampling; CI vs PI.<br>• The model line: a small star at the core, summaries standing alone, conformed in production. | Each was a likely question with no prepared answer. A last-day computation adds risk without changing the answer. |
| O-38 | 12:25 | **P3 spec items 7–8 restored (V6 #6–#7).**<br>• One brief page holds "Dominion on a page" (company box, every line sourced) and the domain primer (glossary). The space comes from merging the cover with the one-page summary.<br>• A4 carries the named "30-second opener", "60-second project story" and "5-minute route".<br>• The sheet adds "What do you know about Dominion?" in place of its least likely question. | v3 had dropped MASTER_PROMPT P3 items 7 and 8. The cap stays at 12 pages. |
| O-39 | 12:25 | **Plan, news check, consistency (V6 #8–#10).**<br>• The plan is re-timed, with a cut list.<br>• The news check becomes a 10-minute manual list, plus a self-contained optional prompt, repeated on Tuesday.<br>• Consistency fixes: base-year bridges, the 2024→2025 label, CEMIn, STAR with Task, "ten of the twelve", README against `ec8ecb6`.<br>• Final files drop the version suffix. | V6 §2b–§3. |
| O-40 | 12:50 | **Repo docs follow the real data path.** D fixes, in three commits on the branch:<br>• docs/07:64: the 1 Nov Snowflake run was a test in a separate trial account.<br>• docs/07:14, :31, :42-44: the October report read Snowflake; the template imports CSV files, re-exported from DuckDB before a refresh.<br>• docs/04:221: the D22 T21 wording.<br>• The `run_local_duckdb.py` closing message.<br>• The sql/09 header and download_eaglei.sh comments.<br>Then the bundle is rebuilt and the README and CHANGES regenerated. | Published as they stood, these docs would tell a reader that the candidate's Snowflake holds the new tables and that the template reads Snowflake. Both are untrue (D's list in `work/v6_inputs/D_facts.md`). |
| O-41 | after the run | **A 2-page plain-English handout replaces the 14-page deck as the leave-behind.**<br>• Owner, after the run: the deck is too much to hand over and too technical.<br>• `01_deck/Dominion_handout_2page.{html,pdf}`: one sheet, front and back, with public numbers only. Page 1: the question, three findings, one chart (storm days and outage minutes by year, from `origin/main`). Page 2: the flow, the candidate's own report screenshot (the public deck's S5 image), three checks, a demand box and the GitHub link.<br>• Builder `work/handout/build_handout.py` checks: 2 pages; footers present; no acronyms or model terms printed; text at least 8.5 pt and at least 0.30 in from the edges; every printed number is a year, a tick or a public/both claims value.<br>• claims.csv now has 156 rows: 12 rows name the handout in used_in, plus a new row C-H-01 for its chart.<br>• START_HERE §1 and §5 changed: print 3 handouts; print the full deck once, only if a presentation is confirmed; the public-vs-adopted number note. | The owner asked for it. Plain language and fewer numbers suit a mixed panel. |
| O-42 | 2 Nov | **The owner lifted the no-publish rule: everything goes to the public repo `Renvia-code/Sab-Dominion`.**<br>• What it holds: the branch `interview-upgrade-2026-11` as `main`, plus all of `interview-prep/` and a root `HANDOFF.md`.<br>• The owner chose this when asked, after being told the repo is public and that the pack holds the answer cues and the note on how the extension was made.<br>• Left out of git: `*.pbix` (gitignored), `__pycache__`, and `work/v2/origin_main_tierB.txt` (56 MB, a text dump of the upstream repo, already in the history). The resume was never in `interview-prep/`.<br>• Raw data goes to Drive as `Sab-Dominion_data_raw.zip`, without `duckdb/` (rebuilt in about 25 s), `eaglei/downloads/` and `_downloads/`.<br>• The candidate's Claude gets a copy-paste prompt. | The candidate asked for the data and analysis behind slide 4 and wants to work on it with Claude. |
| O-08 | 06:53 | Tools present: LibreOffice (`C:\Program Files\LibreOffice\program\soffice.exe`, not on PATH), Edge (`C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`), node/npx, uv. Absent: PowerPoint, pdftoppm (use PyMuPDF for page renders). | Tells B how to make PDFs and proofs. |

## 6. Owner questions

| # | Asked | Question | Answer / default taken |
|---|---|---|---|
| Q1 | 06:50 | Install Power BI Desktop here? | **Install** (O-06) |
| Q2 | 06:50 | Which role / posting? | "Light search on their website, not too deep" (O-04) |
| Q3 | 06:50 | Interview format? | **Panel of 3** (O-05); time and place not given → START_HERE leaves `[you: time, place]` |
| Q5 | 09:13 (not asked; the default is taken) | Will the candidate adopt the 1 Nov repo upgrade, that is, review it, rerun it and publish it from their own GitHub account before Tuesday? | **Default:** build both variants (O-26). START_HERE makes the choice Monday's first step, with the adopted variant only if they publish. The final report raises it with the owner as the main open decision. |
| Q4 | 09:00 (not asked; after Phase 0 the run never blocks) | After D22, Snowflake's `MART.STORM_INDEX` and `SAIDI_WEATHER_ADJUSTED` still hold the pre-D22 values (465/796), so T21 fails in Snowflake. Correcting them in place needs `CREATE OR REPLACE`, which §4 forbids without the owner. | **Default taken: leave them, documented** (`docs/07`, D's ledger). DuckDB and `data/output/` are authoritative; Power BI imports from CSV (F1), so no deliverable reads them. The owner can run the replace later if wanted (START_HERE lists it). |
| Q6 | 12:25 (not asked; the default is taken) | The 33 branch commits carry the owner's git identity: name ".", the owner's GitHub no-reply email, 1 Nov +05:30 times and the Claude trailer. If the candidate pushes them as they are, GitHub shows them as the owner's commits on the candidate's repo. | **Default taken:** START_HERE and README step 8 recommend a local squash with an honest "How it was made" paragraph, and advise against pushing the 33 commits. Nothing in the bundle is rewritten (brief §4: never rewrite history). Raised in the final report. |

## 7. Sources and data acquired

| Source | Folder / manifest | Rows / files | State |
|---|---|---|---|
| NOAA Storm Events (existing) | `data/raw/noaa/` | 13 files, 831,288 rows | ✅ verified 01-11 by the setup session |
| EIA-930 (existing) | `data/raw/eia930/` | 17 files | ✅ verified 01-11 by the setup session |

## 8. Change log

- 2026-11-01 06:39 Phase 0 started. Read the brief in full, the prior chat notes, local `CLAUDE.md`.
- 06:41 Checks: `snow connection test -c dominion` OK (RENV, ACCOUNTADMIN, warehouse
  SNOWFLAKE_LEARNING_WH); `run_local_duckdb.py` T1–T6 PASS, rolling SAIDI 130.2 and 133.0;
  `check_output_metrics.py` all PASS (465 / 796 storm county-days, r = 0.696, 2025 prediction 145.27,
  actual 144.4, DOM min 7167 → 10903 MW). Network to eia.gov, pypi, figshare, careers site OK.
  `PJM_API_KEY` not set (PJM Data Miner skipped unless found later).
- 06:48 Folders created; venv packages installed (O-03).
- 06:50 Owner answered Phase 0 questions (§6).
- 06:52 Power BI Desktop install started in the background (O-06).
- 06:53 Branch `interview-upgrade-2026-11` created (O-07).
- 06:56 Power BI Desktop installed: `%LOCALAPPDATA%\Microsoft\WindowsApps\PBIDesktopStore.exe`,
  package Microsoft.MicrosoftPowerBIDesktop 2.159.883.0.
- 06:57 Owner, mid-turn: "use all needed skills and proceed end to end … `claude+tools`". B's brief
  points at the toolkit's README, CATALOG and the award-web-design, web-interface-guidelines and
  accessibility skills for the HTML brief; `dataviz` governs charts (O-09).
- 07:00 R, D, B spawned (general-purpose, Opus) with run-context briefs. D is the only committer
  during the run (O-10). Agent budget: 3 + up to 4 reviewers (V1, V2, V3, V6) + 1 spare = 8.
- 07:03 Orchestrator read the resume locally (2 pages) to judge role fit and truth checks. Notes for
  the gates: summary says "3 years of experience"; current role Data Analyst, Mercury Insurance, since
  Apr 2026 (Snowflake pipeline 20M+ rows, RCA −17% settlement time, eval 71% → 90%, A/B +9%); MS
  Business Analytics, Boston University, Jan 2026; Tableau is the dashboard tool in the bullets, Power
  BI appears in the summary and skills; no utility experience. The resume carries phone and email:
  the title slide uses the name only.
- 07:28 **B checkpoint 1** (batch 1 done): design system (Segoe UI, both print pipelines proven),
  `work/storyline_v0.md` (8 + 6), `work/powerbi_fix_plan.md` with the .pbix decoded and a copy opened in
  Desktop (original's hash unchanged). Found F1 (DirectQuery tables). D's ledger 07:17: D0 and D1 done
  (12 MATCH; F12, F13 wording; F15 partial); EAGLE-I from DOE Aviary (figshare is behind a bot challenge,
  not bypassed; MD5s match figshare), 6 of 12 years; EIA-861 2024/25 + 861M 2013–Aug 2026 acquired. R's
  ledger 07:28: R1 done (`research/role_brief.md`), R6 in progress.
- 07:36 Orchestrator read storyline v0 and R1 §1–2. Decisions O-11 to O-16. B resumed for batch 2
  (v0 safety-net pack). D asked for the S2 base-year check, B's CSV exports and the slope check. R asked
  to finish `for_D.md` first, then confirm 130/133 in Dominion's annual report and gather the
  Grid Resiliency programme facts.
- 07:40 **R checkpoint 1** (batch 1 done 07:36): R1 + R6 (`research/for_D.md`), claims register
  R-001 to R-027. Gaps: the Virginia SCC site returns 403 to scripts, so the filed reliability reports
  and GT Plan orders are a recorded gap (O-17); DOE-417 summaries are now at PNNL with no utility name;
  EIA-861 2025 final was released 7 Oct 2026. R's EAGLE-I "owner must download" options are superseded
  by D's DOE Aviary route. R resumed for batch 2 (R2, then R5; R3 and R4 in batch 3, O-18). D asked to
  check the repo's 2025 values against the final EIA-861 file.
- 07:56 **D checkpoint 1**:
  - S2 base-year check done.
  - Q10 slope confirmed.
  - 8 CSV exports and `va_counties.topojson` in `data/output/`.
  - 2025 values = EIA-861 2025 final; time-varying rates confirmed at 1.0% of customers.
  - Acquired: EAGLE-I (11.6M VA rows, 14/14 checksums), EIA-861/861M, Census/ACS, HURDAT2, degree days, DOE-417 (PNNL, 3,702 events), PJM tables.
  - `sql/09` EAGLE-I model, T13–T24 pass (DuckDB). 5 local commits.
  - Open: Bedford city possible duplicate storm days; DOE-417 matching (`sql/11`); `sql/09` in Snowflake.
- 08:05 **G1a: storyline locked** (O-19). D resumed for batch 2 in this order: Bedford check, A2 + restoration curve, A4, A3, A1, A5, docs. B told the lock (queued).
- 08:08 **B checkpoint 2.** The safety-net v0 pack exists and is proofed:
  - **Deck v0:** 14 slides, notes on all 8 main slides, smallest printed text 10.1 pt; S2, S6 and S8 already follow the lock.
  - **Brief v0:** 10 pages, body 10.5 pt.
  - **claims.csv:** 63 rows. C-S2-01 confirmed (R-028: Dominion 2025 Annual Report p. 10).
  - **Q-sheet layout test:** 22 Q&As fit two sides at 8.5 and 9 pt.
  - **Charts:** saving now checks automatically for label collisions.

  Orchestrator looked at deck p2 and brief p2: clean, the two-sided lines are present. Rulings (O-20): SUP named per R-035; "99.8% of meters"; p-values corrected in the lock (orchestrator's error); S4 title "Years with more storm days had more outage minutes; …"; one 2026 cut-off date, set by D. B resumed for batch 3: B5 Power BI, B1 charts as D lands, B3 when `top40.md` lands.
- 08:16 **D checkpoint 2:** batch 2 items 0–6 done; T1–T31 pass (DuckDB).
  - **Bedford** double count found: 38 county-days.
  - **A2:** ten largest events, plus the Isaias curve (90% restored in 33.5 h); restoration not clearly faster over time (p = 0.07).
  - **A4:** S5 figures confirmed; weather-adjusted growth +33%.
  - **A3:** 99 counties mapped, 4 left off.
  - **A1:** 11.9× (CI 7.9–16.9).
  - **A5:** 13/13 rebuilt values match.
  - **E1:** one 2026 cut-off at 29 Oct.
- 08:25 Rulings O-21 (fix Bedford as D22) and O-22 (S4 = A1); lock file updated. D resumed for batch 3: D22, docs, Snowflake add-only, A6 arithmetic. B told (queued).
- 08:45 **R checkpoint 2** (batch 2 done 08:40):
  - **R2:** dossier + on-a-page. C-S2-01 confirmed (R-028, p. 10: "primarily due to increased storm activity"; whether it covers VA only or VA + NC is not stated). Grid Resiliency = MFH, VIM, VO, IGD/FLISR; SUP is separate (R-035).
  - **R5:** `question_bank.csv` 126 rows; `top40.md` with 24 ★ picks, 5 asks and 32 hard questions.
  - **Blocked sites recorded:** Glassdoor, Indeed, Teal (403), Interview Query (429).
- 08:50 **G1b: question shortlist locked** = R's 24 ★ unchanged; T7's answer also covers performance (O-23). B told; R resumed for batch 3 (R3, R4; V5 ~11:30). D asked for: VA vs VA+NC scope, the weather-fit t and CI from the unrounded r, and the peer rule in one line.
- 08:55 **D checkpoint 3:**
  - **D22** committed (06631ad): storm county-days 464 → 791 (2019: 848). r 0.70, 145.3, 133.1, Q10 slope and A1 11.9× unchanged; fit 104.3 + 0.0518 × days.
  - **Docs** 01, 02, 05, 07, 08 updated.
  - **Snowflake:** sql/09–11 built (24 new objects, add-only, X-Small, 25/25 counts equal DuckDB, warehouse suspended); T21 fails there only because of Q4.
  - **A6:** 1 SAIDI minute = 2,675,735 customer-minutes ≈ 44,596 customer-hours; no dollar figure (no verified source).
  - **Open for B:** the workbook sheet `StormIndex` still shows 465/796/851.

  Working tree clean; all commits local.
- 09:10 **D quick checks:**
  - **Scope:** VA-only 130.22 / 133.01 print as 130 / 133; VA + NC 129.49 / 132.50 print as 129 / 133. The report's figures are consistent with Virginia only (an inference).
  - **Weather fit:** r = 0.6973, t = 2.752 (8 df), p = 0.025, 95% CI 0.121–0.922.
  - **Peer rule D10** quoted.
  - **Rule flag accepted (O-25):** D ran read-only checks and the warehouse suspend through `snow sql`.

  Relayed to R and B. D resumed for batch 4: README "what's new", P4 data completeness, on call for G2.
- 09:15 Reviewer prompts V1, V2, V3, V6 written to `work/reviews/REVIEWER_PROMPTS.md`. Plan:
  - V3 starts as soon as the deck v1 PDF exists.
  - V1 and V2 start in parallel once P2 and P3 v1 exist.
  - V4: B proofs every page, and the orchestrator spot-checks.
  - V5: R, at ~11:30.
  - V6 at G3.

  Agent budget: R, D, B + V1, V2, V3, V6 = 7 of 8.
- **Clock note:** the machine clock read 08:53 at the next check. The orchestrator entries stamped
  09:00–09:15 above were estimates and ran ahead of it; they happened between 08:45 and 08:53. From
  here on, every entry uses `date`.
- 08:52 **D checkpoint 4 (batch 4):**
  - README "What's new" (69cc362).
  - Data-notes tables `test_results.csv` (T1–T31 pass), `reconciliation.csv` (**12/12** match) and `storm_county_year.csv` (f444a31).
  - Corrected the T17/T19 comments (94dc884).
  - A5 is now cited as 12 of 12, not 13.

  D is idle, on call for G2. B told.
- 08:54 v1 files found: deck v1 (08:43; 14 pages, already follows the lock: S4 = 11.9×, A6 = ten largest events), question sheet v1 (08:48; 2 pages), brief v1 (08:43; 10 pages), P4 folder (`.pbit`, `measures.dax`, theme, M, alt text, data; 08:50). Snapshot taken to `work/reviews/snapshot_v1_0855/`.
- 08:55 **V3 mock panel and V2 truth audit launched** on the snapshot (fresh Opus reviewers; prompts per `work/reviews/REVIEWER_PROMPTS.md`). V1 waits for B's v1 checkpoint, so it audits the D22 values (464/791) and 12/12.
- 08:58 **R checkpoint 3** (batch 3):
  - **`domain_primer.md`:** A1 one-liners; EIA-861 vs SCC; analysis practice; PJM; literature.
  - **`interview_science.md`:** delivery table; DOIs checked in Crossref. Reappraisal is "a small edge" (d ≈ 0.2; replication mixed). Power posing out. Answer-first, "I don't know", pacing and the follow-up note have no verified study, so they stay as uncited advice.
  - **Claims register:** R-001 to R-091.
  - **Gaps:** the SCC rule for the Annual Reliability and Tree Trimming Report (403; a 1990 report is the likely origin, marked as inference); nothing on ETR accuracy.
- 09:00 R resumed for batch 4: V5 freshness now (the run is ahead; it is still the final day), a morning-prompt draft for START_HERE, then standing by to answer V3's questions.
- 09:08 **V2 truth audit** done (`work/reviews/V2_truth_audit.md`).
  - **Verdicts on 46 statements:** 23 supported, 6 rephrased-OK, 8 overstated, 9 unsupported.
  - **Resume claims are clean:** no invented achievements.
  - **Serious finding, ownership:** the 1 Nov upgrade (EAGLE-I, degree days, T13–T31, D22, the all-Import report) is on the local branch only, yet v1 presents it in the first person, and Q13/Q7 tell fix stories the candidate didn't live.
  - **Other findings:** "Power BI at work" ×3, 13 vs 12, p-values not in the repo, and smaller overstatements (F11–F17).
  - **Flags:** no salary figure, no phone or email, nothing on how the pack was made; commute/relocation for the hybrid 3-2 role not covered.
  - **Placeholders:** 25.
- 09:13 **Rulings O-26 and O-27** in `work/reviews/V2_rulings.md`. B told (queued); D resumed for the trend-test script, and the git bundle later.
- 09:16 **D:** `scripts/trend_tests.py` committed (94eb5e2).
  - SAIDI +0.64/yr (p 0.58), SAIFI +0.0043/yr (p 0.54), CAIDI +0.17/yr (p 0.74), weather-adjusted +0.34/yr (95% CI −1.41 to **+2.08**, p 0.67).
  - Post-D22 the upper bound is +2.08, not +2.09.
  - `check_output_metrics.py` asserts these values; docs/05 has a "Trend tests" section.

  B told. D is idle and on call; the bundle waits for the go.
- 09:16 **R checkpoint 4. V5 freshness done** (`research/freshness.md`): nothing from 25 Oct to 1 Nov changes the storyline or any deck number.
  - **Dated lines** added to `dominion_on_a_page.md`: dividend 66.75¢; a solar coalition opposes the merger in PUR-2026-00112; SC testimony; the Q3 call (CVOW 44 turbines installed, data-center pipeline +6 GW on the 54 GW pipeline); FERC deficiency letter 23 Sep, answered 15 Oct.
  - **Claims:** R-092 to R-099 added.
  - **Gaps:** what the SC testimony says, HSR antitrust status, and an Axios item that returned 403 and is unused.
  - **Morning prompt:** `research/morning_prompt_2nov.md` (193 words). It names neither the candidate nor the resume, and it covers the VA rebuttal testimony due 2 Nov.

  R is standing by for V3.
- 09:17 **V3 mock panel** done (`work/reviews/V3_mock_panel.md`): 25 hardest questions; 47 problems (7 high, 25 medium, 15 low); talk ≈ 10¼ min with no slack.
  - **High:** P1/P2, S2's "not longer" depends on the base year, and A2 shows 2025 on the storm line; P11/P12, the S4 map is all-utility and the slide crams three visuals; P18, S5's tone; P29, no Power BI anywhere (the job's first duty); P30, the S8 Power BI claim.
  - **Number mismatches:** 6,108 vs 6,530; 12 vs 31 tests; "12 peers" are 11 with medians including Dominion.
  - **Wins:** the build story (S6–S7).
- 09:21 **Storyline revised (O-28)**, in the "G2 revision" section of `work/storyline_LOCK_G1.md`. B, R and D were briefed:
  - **B:** deck v2 (two variants), sheet and brief v2, P4.
  - **R:** `hard25_answers.md` and `delivery_and_rehearsal.md`.
  - **D:** the peer medians excluding Dominion, the S4 levels, the 6,108/6,530 reconciliation, storm days by year, the Dominion-only map, and the S2 storm-line arithmetic.
- ~09:40 **D checkpoint 5** (findings §C5; commits c0b2ea2, 7133aba, 4fc9939, d1bdff2; 100 output checks + T1–T6 pass):
  - **Peers:** Dominion is one of the 12. Medians of the 11 peers: SAIFI 0.934, CAIDI 99.5. Ranks unchanged (4th SAIFI, 6th CAIDI).
  - **S4 levels:** storm 332.8 (225.6–453.4) vs calm 27.86 (23.09–33.22); ratio 11.9 (7.9–16.9); non-major 9.9×; Dominion-only counties 19.9×; every year 5.9–27.4×. 2025 readings are 74% complete.
  - **Counts:** 6,530 − 114 − 308 = 6,108.
  - **Storm days:** 2022 → 2025 = 718 → 791.
  - **Map:** Dominion-only 159 min vs shared counties 211 (places, not utilities).
  - **Storm line:** 145.3 confirmed.

  B told.
- 10:28 **B checkpoint 3 (v2 ready):**
  - **Decks:** v2 (adopted) and v2_public, 14 pp each.
  - **Sheet:** v2, one sheet two-sided.
  - **Brief:** v2, 12 pp (8 + 4).
  - **claims.csv:** 122 rows (75 both, 35 adopted, 12 public). B's checker finds no uncovered number or missing quote, and no variant leaks.
  - **P4:** done, verified open in Desktop (10:08).
  - **Open decisions:** D1–D22 vs D1–D14; sheet vs top40; 10 pt tables; public S5 has no Power BI file.
- 10:32 Orchestrator committed B's repo-bound Power BI files: **859b52d** (measures.dax with 77 measures, `powerbi/m/*.pq` with 18 queries + DataFolder, the theme, the `.pbit`, docs/06). Checked first: no local paths or account names; the DataFolder default is `C:\DominionPowerBI\data\` and is required on open; D's 29b179f text was kept in docs/06.
- 10:33 Snapshot `work/reviews/snapshot_v2_1035/`. **V1 number audit launched** (agent 7 of 8).
- 10:35 Rulings to B (O-31):
  - D1–D22 approved for the adopted deck.
  - The sheet aligns to the top40 ★ wording.
  - 10 pt tables approved.
  - Public S5 = a screenshot of the candidate's own report from cached Import data, or the model plus measures and "live demo".

  B's next tasks: the V4 proof log, START_HERE. D batch 7: the docs/05 notes, then the `deliverables/05_repo/` bundle, CHANGES.md and README.
- 10:40 **Orchestrator V4 spot check** of the snapshot: deck v2 pp. 2, 4, 5; brief p. 3; sheet side 1 (renders in `work/reviews/orch_spot/`).
  - **S2:** factual title, Dominion's storm attribution cited, sources present.
  - **S4:** one visual with CIs, robustness lines and the all-utilities caveat.
  - **S5:** a real Power BI screenshot, star schema and a DAX snippet.
  - **Brief p. 3:** two-sided, with "If adopted" tags and the public-repo numbers noted.
  - **Sheet:** STAR cues with `[you: …]` gaps; Tableau at work, Power BI in the project.

  No defects seen at this zoom. Gap: the Power BI template's on-screen titles are outside V1's scope, so B was asked for `work/reviews/P4_titles.md`, which the orchestrator will review.
- ~10:50 **D checkpoint 7:**
  - docs/05 notes committed (b0db94d).
  - **`deliverables/05_repo/`:** a whole-branch bundle (8.4 MB, tip e0b3712, 30 commits, no prerequisite), CHANGES.md and README (8 steps). Tested in a clean clone: fetch, T1–T6, output checks, trend tests and a squash all work.
  - **Extra commits:** 0a79adc (`requirements-sources.txt`) and e0b3712 (README fix).
  - **Found:** two template tables still read the workbook in `powerbi/`. D will export them to CSV by script (O-32), then B switches the two M queries.
  - `build_repo_deliverable.py` rebuilds the package; it is rebuilt after the final commits.
- ~11:05 **D:** a810494 adds `scripts/export_workbook_tables.py`, which writes `data/output/load_growth.csv` (13 rows) and `programmes_2025.csv` (6 rows).
  - Values are checked against the workbook formulas, and `check_output_metrics.py` covers them: TWh vs `fct_sales_sector`; 2025 commercial index 165.4; AMI 99.8%; TVR 1%.
  - Table names are unchanged, so the measures need no change. B switches the two M queries next.
  - The bundle is current at a810494 (31 commits) until the final rebuild.
- 10:58 **V1 number audit** done (`work/reviews/V1_summary.md`, `V1_coverage.md`, `V1_number_audit.csv`): 122 rows, 117 MATCH, 2 ROUNDING, 1 MISMATCH (C-S7-05A test-group label), 2 UNVERIFIABLE (C-Q-10 "shareholders approved in September": no source opened; C-S6-06: −44%, site blocked). No adopted-only number in the public deck.
  - **Most serious:** the public deck contradicts the public repo (medians 0.93/99.3 vs printed 0.96/105; "10 of 12 IEEE" vs "Mixed" and "half").
  - **Also:** CAIDI labelled "minutes to restore" (S5 screenshot, brief p. 7); uncovered numbers (33 Dominion-only, the screenshot's +6%/−9%, brief r-values and citation years, "4–5-year trim cycles"); talk times fit the adopted deck only; C-S4-05P source.
- 11:00 **Ruling O-33**, sent to B for v3 (final candidate). R resumed for batch 6 (verify or cut the three facts; results in `research/V1_followups.md`).
- 11:16 **R checkpoint 6:** all three facts verified, nothing cut. Relayed to B.
  - **Shareholders:** both companies approved on Sep 3, 2026 (SEC 8-K Item 5.07; R-104, R-105).
  - **−44%:** Dominion's Jun 8, 2026 release: average annual outage time for customers on hardened mainfeeders, VA, with no stated baseline or method (R-013 re-sourced).
  - **Trim cycles:** 4–5 years, neighborhood lines 4 (R-076).
- 11:45 **B checkpoint 4 (v3 complete):**
  - **v3 files:** decks ×2, sheet, brief.
  - **Claims:** `claims.csv` v3, 127 rows; 0 uncovered, 0 misses.
  - **Talk time:** 7:54 adopted, 7:38 public.
  - **V4 print proof** (`work/reviews/V4_print_proof.md`): every page looked at in color and gray. Decks 14 pp with text ≥ 10.12 pt; sheet 2 pp (one sheet); brief 12 pp with text ≥ 9 pt. Fonts embedded, images ≥ 305 ppi. Edge margins fixed.
  - **START_HERE:** written.
  - **P4:** rebuilt 11:10 and opened in Desktop with no errors (CSV switch; CAIDI as "minutes per interruption"). `work/reviews/P4_titles.md` written.
  - **Public S5** shows only the original report's frequency chart.
- 11:45 **Orchestrator reviewed `P4_titles.md`:** all-utilities labels, association wording, D's demand wording, CAIDI fixed, no pre-D22 numbers. Pass.
- 11:45 Committed **7867129** (Power BI: every table from `data/output`; CAIDI "minutes per interruption"; docs/06). Scanned the `.pbit` and text files first: no local paths, names or account identifiers.
- 11:47 Moved the superseded v0–v2 deliverables to `work/old_versions/` (moved, not deleted). `deliverables/` now holds only v3, P4, `05_repo` and START_HERE.
- 11:48 **V6 candidate read launched** (agent 7 of 8). D: README fix + bundle rebuild at 7867129. R: morning-prompt fix (a one-page insert on 2 Nov, never an edit of the brief; US spelling).
- 11:52 **R checkpoint 7:** `research/morning_prompt_2nov.md` final (223 words, US spelling; Edge one-page print tested). The orchestrator replaced START_HERE §9's embedded copy with it, plus a line on using the insert.
- ~11:58 **D checkpoint 8:**
  - **README:** the 05_repo Power BI step is now just "set DataFolder to `<clone>\data\output\`" (18 CSVs, no workbook copy). Repo README sentence fixed (2cbd7a8).
  - **Bundle:** rebuilt and verified at tip **2cbd7a8** (33 commits).
  - **Clean-clone test** passed again; all 18 template queries point at existing files.
- 12:00–12:05 **Orchestrator verification** (verification-before-completion):
  - **PDFs:** decks 14 pp, Letter landscape, min text 10.12 pt; sheet 2 pp (one sheet), min 9.0 pt; brief 12 pp, min 9.0 pt; all fonts embedded.
  - **Scans:** no pay figure, no contact details, no how-made mentions.
  - **claims.csv:** 127 rows; 5 added and 25 changed since V1's snapshot. The V1 agent was resumed for a delta audit on those 30 rows plus v3 coverage, and its verdicts will be merged into `checked_by`/`result`.
  - **Repo:** checks and git state verified (DoD-8, DoD-10 above).
- ~12:10 **V1 delta audit** (`work/reviews/V1_delta_v3.csv`; `V1_summary.md` "v3 delta"): 30 MATCH, 1 UNVERIFIABLE (C-Q-10, Sep 3 shareholder vote: sec.gov returned 403 to the reviewer, not worked around).
  - **The public deck now agrees with origin/main:** 0.96/105 including Dominion; "Methods differ"; "Mixed"; no "10 of 12"; no adopted-only numbers.
  - **Minor items:** the public S5 screenshot numbers lack rows; the C-S5-12 locator is off; brief p. 4 has the adopted medians without a tag.
  - R asked for a non-SEC source for C-Q-10. B started the claims-only fixes and the merge of V1 verdicts into `checked_by`/`result`; PDF changes wait for V6.
- ~12:15 **C-Q-10 verified** by the orchestrator, who did not produce it.
  - **Source:** R-106, WWBT/12 On Your Side, published 2026-09-03T20:41Z; fetched HTTP 200. It quotes Dominion: "We are pleased that shareholders of Dominion Energy and NextEra Energy have approved the proposed merger. Today's vote…"
  - **Vote counts** (8-K only; the reviewer was blocked) are cut from the printed pack if present. B told.
- 09:44 **R checkpoint 5:**
  - **Hard questions:** `research/hard25_answers.md` (full) and `hard25_print.md` (≈2.3 pp). V3's 25 merged with the brief's 7, all kept. Upgrade-dependent answers are marked, with public-only lines.
  - **H2 adds up honestly:** ≈10 months in data-titled roles, ≈38 months including internships.
  - **Delivery:** `research/delivery_and_rehearsal.md` (Page A delivery; Page B the Monday plan, with the adopt-or-not decision as step 1).
  - **Claims:** R-100 to R-103 added.
  - **Flags for D, N-1 to N-11:** all-events ranks 6th SAIFI and 9th SAIDI; the 2025 prediction band 122–168; Dominion files MED as "Other" while 10 of 12 use IEEE, which contradicts docs/06's "half the peers".
- 09:46 Rulings O-29 (brief page budget) and O-30 (US spelling). D resumed for batch 6 (N-1 to N-11, docs/06 fix); B told (queued).
- ~09:53 **D checkpoint 6** (findings §C6; docs/06 fixed in 29b179f):
  - R's data items N-1 to N-8 and N-11 confirmed; N-9 is resume dates, not checked by D.
  - 2025 prediction interval 122.3–168.2 (the fitted-line CI is 133.9–156.6).
  - All-events: SAIFI 6th of 12, SAIDI 9th.
  - 10 of 12 file IEEE every year 2014–25; Dominion files "Other".
  - Georgia Power and Duke Energy Florida are mislabelled "Mixed"/"Changed" in brief v1 and Power BI (they were "Other" in 2013 only).

  B told.
- 12:10 **V6 candidate read** (`work/reviews/V6_candidate_read.md`): the numbers hold, with no contradictions; the talk timings, placeholder counts, ranks, medians and bridges re-derived. Its top 10 is in §4.
- 12:10 **B checkpoint 5 (claims only):** `claims.csv` has 128 rows. V1's verdicts are merged (126); C-Q-10 orchestrator MATCH via R-106; the new row C-S5-14P is pending the orchestrator. The checker shows 0 uncovered, 0 misses, 0 stale. `producer_check` is a new column. No printed vote counts.
- 12:15 **Orchestrator checks on V6's claims:**
  - `.pbit`: 18 imported tables, 2 calculated, 2 relationships.
  - Branch: 33 commits, all ". <owner no-reply>", 1 Nov 07:47–11:47 +0530, 33 Claude trailers.
  - Diff from `ec8ecb6`: 87 files, +40,408; excluding `data/`, 55 files, +3,818 / −259.
  - Original build: 2026-10-27 (f4f75df) to 2026-10-31 (ec8ecb6).
  - The repo's docs/06:135 already gives the DuckDB → CSV path, and no repo doc says "star schema". **So no repo change and no bundle rebuild are needed for V6.**
- 12:20 **Rulings O-34 to O-39, owner question Q6.** Sent:
  - D: the facts file (items a–o) and the 05_repo README (steps 1–2, 4, 5, 7, 8).
  - R: the company box, glossary, Dominion answer, the manual news check, salary, storm duty, FPL.
  - B: the single final rebuild, with exact text for the model line, the authorship sentence and Q18.
- 12:30 **Correction to B:** the printed brief's Q18 points to START_HERE §8 and carries no AI words (O-27). The full sentence stays only in START_HERE and in the adopted slide 6 speaker notes, which are not printed.
- 12:35 **Orchestrator:** START_HERE rewritten; APPLY_GUIDE given the Windows note, the 11:15 deadline, a From column (8 October pages, 3 new) and the model line. C-S5-14P checked: MATCH (origin/main docs/06:37 "+6%"; workbook Trend SAIFI 1.244 / 1.165 / 1.32; 1.32 ÷ 1.244 = +6.1%).
- 12:45 **D checkpoint 9:** `work/v6_inputs/D_facts.md`, items a–o, every number sourced, [NEW] marked.
  - 2020 is a lasting step (max_kv 34.5 → 46.0 from 2020).
  - 103 proxy MED days; without them 9.9 (8.6–11.3).
  - 16 template CSVs come from DuckDB and 2 from the workbook; 11.9× is on no report page.
  - D10 answers the Appalachian Power question.
  - The review list is 393 lines. The light checks take about a second; the full rerun takes about 20 minutes of download plus a 22-second build.
  - 05_repo README regenerated and rehearsed on a fresh clone. The bundle is unchanged.
  - Five repo docs contradict the real data path → O-40.
- 12:50 **Orchestrator pre-check of D's [NEW] numbers** against the repo: all MATCH.
  - max_kv 35.0 (2013–14), 34.5 (2015–19), 46.0 (2020–25); auto_recorded from 2015.
  - Proxy MED days 2, 15, 3, 18, 5, 6, 12, 14, 3, 10, 15 = 103.
  - Non-major 9.856 (8.559–11.282).
  - `trend_tests.py` rerun: n 11, 9 df; SAIDI +0.64 (−1.87 to +3.15) p 0.58.
  - D10's "SAIDI exceeds 300 minutes"; seven co-ops (docs/02:115); 38 county-days (D22); co-op index 137 vs Dominion 114 (docs/05:77-78).
  - "137.4" has no repo source; flag it if printed.
- ~13:05 **D checkpoint 10 (O-40 done).** Commits 506e969 (docs), c49aeb1 (script message), c17766a (comments).
  - **Tip c17766a:** 36 commits on ec8ecb6, 88 files.
  - **Bundle:** SHA-256 55210174…, 8.5 MB, verifies.
  - **README and CHANGES** say 36; times come from the git log.
  - **Fresh-clone rehearsal:** the three checks pass and the squash tree matches. Full sources build T7–T31 PASS in 22.4 s.
  - `ls-remote` unchanged; review-list ranges unchanged; no pack text quotes a commit count.
  - **Left as is:** three October lines (docs/00:90, docs/07:44, :90) still point at the deleted CHANGELOG.md. They are the candidate's own public text, outside O-40, and are listed in the final report as an optional tidy-up.
- ~13:10 **R checkpoint 8:** `work/v6_inputs/R_company_glossary.md`. Register rows R-107 to R-131 are new; the resume check is clean (no shared 6-word runs); no name, no pay figure.
  - Company box: about 26 lines; 2.8M = DEV including NC (2,809k accounts).
  - Glossary: 22 terms.
  - "What do you know about Dominion?": 109 words.
  - Manual news check: 6 URLs with baselines, plus the assistant prompt.
  - Salary: no figure. Storm duty: "ask the recruiter" (the posting and nine others are silent).
  - FPL answer drafted.
  - **Not opened, and not worked around:** the SCC docket search, the Federal Register bot check, WAVY (403), and NCEI (JS).
- ~13:15 **Orchestrator verified R-124 and R-125** from `data/output` (the 12 = 4 Mid-Atlantic + 5 Southeast + 2 Florida + Dominion; Appalachian excluded). Both MATCH.
  - SAIFI-all 2021–25: FPL 0.766 vs 1.531.
  - Ex-MED SAIFI: FPL 0.488, lowest. Ex-MED SAIDI 2023–25: 46.64, lowest.
  - CAIDI-all: 406.0, highest of the 12.
  - SAIDI-all 2023–25: 275.7 vs 223.0.
  - IEEE 1366 every year 2014–25: 10 of 12; Dominion and Alabama Power file "Other".
  - R's docs/06 conflict exists only on origin/main; the branch's docs/06 was fixed in 29b179f, and the public deck says "methods differ" (O-33).
  - START_HERE §3 and §9 now carry R's storm-duty line, salary line, manual check and prompt.
- ~13:30 **B checkpoint 6 (final build).** Files drop the version suffix; v3 moved to `work/old_versions/`.
  - **Decks:** `_adopted`/`_public`, 14 pp each, min 10.12 pt. Speaker-note time: adopted 7:56, public 7:23.
  - **Sheet:** 2 pp, 23 `[you: …]`. **Brief:** 12 pp, 23 `[you: …]`.
  - **Brief text sizes:** body 10.5 pt; p.1 and p.8 tables 10 pt; p.2 (Dominion on a page + glossary) 10 pt so the brief stays at 12 pp, accepted like the 10 pt main-page tables (O-31); appendix 9 pt (O-29).
  - **Authorship sentence:** only in the adopted S6 notes; brief Q18 points to START_HERE §8.
  - **Claims:** 152 rows, 25 pending the orchestrator.
- 13:35–13:47 **Orchestrator verification of the final build:**
  - `verify_pack.py`: pages, sizes and fonts embedded; no pay figure; no contact details; decks and brief carry no how-made words.
  - **Sheet "AI" and "prompt":** the resume's own "AI pilot" and "prompt structure" (the candidate's pilot evaluation), not how-made wording. **Ruling: keep** (O-27 is about how the pack was made). No rebuild.
  - **Opener:** "three years" is the resume's own "3 years of experience", and the text follows sheet Q2 (V2-audited).
  - **START_HERE fixed to the final files:**
    - timings;
    - the merger lines (the brief now says "second half of 2027" and "H2 2027"; the old A1 row text is gone);
    - Q19 carries the programs;
    - the SQL sketch is sheet question 11.
  - **Claims:** 15 of the 25 pending rows checked and MATCH (C-B-01, C-F-05, 11, 14–25). Evidence is in `work/claims/merge_v1_verdicts.py` ORCH.
    - `run_local_duckdb_sources.py --quiet` at c17766a: "All 25 tests passed", 22.7 s; the tree stays clean.
    - `.pbit` 18 M queries → 18 CSVs (16 DuckDB + 2 workbook); the manifest is present.
  - Merge rerun: 142 MATCH, 10 pending.
- 13:40 **V1 resumed** for the 10 web-sourced rows (C-F-01–04, 06–10, 12) → `work/reviews/V1_delta_final.csv`. **V6 resumed** for its top-10 re-check → `work/reviews/V6_recheck.md`.
- 13:50 **Orchestrator visual check:**
  - The final template's evidence (`work/powerbi/b6/shots_v3b/`, 11 pages + open shot; the `.pbit` is identical to c17766a:powerbi/, 49e5f2cb).
  - The Scorecard and Data notes crops show the four START_HERE checks.
  - The printed adopted S5 and brief p.7 carry no en-IN digit grouping (the "26,75,735" appears only on this machine's Desktop render).
  - The fetch was read-only. `origin/audit-fixes-and-business-story` (3909fc3) is the candidate's own branch of Oct 30, already known; origin/main is still ec8ecb6.
  - 12 source MANIFEST.csv files (data/raw/*) plus the output manifest.
- ~14:00 **V1 final audit:** 6 MATCH, 1 MISMATCH, 3 UNVERIFIABLE.
  - **MISMATCH, C-F-06:** CVOW "done by end-2027" is an expectation.
  - **UNVERIFIABLE (sites blocked V1):** C-F-03 (Q3 release), C-F-04 (the case number via pv magazine), C-F-12 ("four nuclear plants", via the NRC notice).
  - **Wording notes:** $11.24 is a residential bill; VIM's 19 sites are planned; "expected by 2029"; Q23 "mid-January" vs p.2 "Jan 11".
- ~14:00 **V6 re-check:** all ten FIXED.
  - **New, would hurt:**
    1. A1's Appalachian Power line lacks D10's reason.
    2. "The same SQL runs in DuckDB" hides the translation.
    3. Sheet Q13 says "built … yourself".
    4. The SCC staff position is missing from the brief.
  - **Low:** README vs START_HERE timings; two "Q19"s; the timer wording; "on Monday" in S6 notes; three `[you: …]` items missing from START_HERE §3; "Virginia Power".
- ~14:10 **Orchestrator:**
  - **C-F-03 and C-F-04 confirmed from web-search results** quoting the primary filings: the Q3 8-K Ex. 99 ($1.28 vs $1.06; top half of $3.45–$3.69) and VPM's Oct 19 URL with PUR-2026-00112. Those pages were not opened; the verdicts say so.
  - **C-F-12 matched** from V1's two opened sources plus the Form 425 search result.
  - D10's Appalachian sentence and docs/02 "mountain terrain" are October text (ec8ecb6).
  - **The last batch went to B:** CVOW wording, residential, planned, "Expected by 2029", "Dominion Energy Virginia", Q23 Jan 11 plus the Oct 19 staff line, A1 Appalachian with D10 (and the comparison, a new row), the DuckDB translation line, sheet Q13, and the S6 notes "before the interview".
  - **START_HERE fixed:** the Q19 convention, the three `[you: …]` items, the timer, README-consistent timings, and review-list item 10 (`run_local_duckdb_sources.py` 46–79; 427 lines).
- ~14:20 **B checkpoint 7 (last batch):** all ten items applied; pages 14/14/2/12 held.
  - **Brief:** the p.7 screenshot narrowed to 4.4 in, and A1 leading 10.3 pt.
  - **Sheet:** Q13's answer trimmed 13 characters.
  - **Adopted S6:** one word longer, so the adopted talk runs 7:57.
  - **New claims rows:** C-F-26 (Oct 19 staff, source R-050), C-F-27 (Appalachian comparison), C-F-28 (translate() lines).
  - "Virginia Power" is gone from the whole pack.
- 14:05–14:15 **Orchestrator final verification:**
  - **Claims:** C-B-01 reverdicted (7:57); C-F-26, 27 and 28 MATCH. Merge: 155 rows, 155 MATCH, 0 pending.
  - **Wording:** `final_wording.py` shows 0 problems across 20 checks (new wording present, old wording gone in the PDFs, the S6 notes and START_HERE).
  - **Pack:** `verify_pack.py` finds 14/14/2/12 pages, min 10.12 / 9 / 9 pt, fonts embedded, no contact details, no how-made words outside the sheet's resume "AI pilot", 23/23 `[you: …]`, no TODO, no old names.
  - **Timing:** recount gives 7:57 / 7:23.
  - **Pay estimate:** the job board's "salaryDesc" in three saved posting copies (`work/research_raw/jobright_bi/` ×2, `work/reviews/v1_sources/jobright_posting/posting.html`) was redacted in place (`redact_pay.py`); 0 remain; the posting evidence ("Hybrid 3-2") is intact.
