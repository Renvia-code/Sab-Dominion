# Agent R (research) ledger

**Now (2026-11-01 13:01): the final round is done.** Output: `work/v6_inputs/R_company_glossary.md`. It holds:
1. the company box
2. a 22-term glossary
3. the 45-second "What do you know about Dominion?"
4. the manual 10-minute check with URLs and Nov 1 baselines, plus a self-contained assistant paragraph
5. salary: one instruction, no figure
6. storm duty and travel: the posting is silent, so "ask the recruiter"
7. the FPL two-liner
8. the NEW sources
9. notes for B

Every line carries an R-id, a C-id or a repo locator. The 25 new rows are in the register as R-107 to R-131
(`work/scripts/claims_final_r.jsonl`).

Findings that matter:
- **FPL's SAIFI is "about half" only on all events.** 2021–25: 0.766 vs 1.531. FPL's outages run longer, though:
  all-events CAIDI 406 (the highest of the 12) and all-events SAIDI 2023–25 of 276 vs Dominion's 223. Ex-MED, FPL
  is the lowest of the 12 on both indices. R computed this; D to confirm (R-124).
- **N-5 is confirmed by the data grid:** 10 of 12 peers use IEEE 1366 in every year 2014–2025; Dominion and Alabama
  Power report "Other" in every year (R-125).
- **The 2.8M is the annual report's Dominion Energy Virginia including North Carolina:** "approximately 2.8 million
  … in Virginia and North Carolina", and 2,809k average accounts (R-107).
- **Data centers were 28% of Virginia Power's 2025 sales** (R-112).
- **The DOM Zone "comprises Dominion Energy Virginia's transmission and distribution service areas"** (R-113).
- **FLISR:** the GT booklet spells it "fault location, isolation, and service restoration"; Dominion's web page
  drops "service" (R-115).
- **Storm duty:** the posting and nine other saved Dominion postings say nothing. WAVY returned 403 and was not used.

Fit, measured without tags:
- the box: 2,090 characters, about 26 lines
- the glossary: 2,220 characters, 25–28 lines
- the 45-second answer: 109 words

The resume 6-gram check is clean.

**12:04:** The auditor follow-up is done. For C-Q-10, a source outside sec.gov that a script can
fetch: WWBT (12 On Your Side), published 3 Sep 2026, 4:41 PM EDT. It says Dominion's shareholders "voted Thursday to
approve", and quotes Dominion's statement that "shareholders of Dominion Energy and NextEra Energy have approved".
- R-106; section 4 of `V1_followups.md`; raw in `research_raw/cq10_vote/`.
- The vote counts remain 8-K only (R-104, R-105).

Batch 7 closed at 11:48. `research/morning_prompt_2nov.md` has been rewritten.
- The Monday session never edits the brief or any existing deliverable.
- If something material moved, it writes `deliverables/03_interview_brief/2026-11-02_dominion_update.md`: per item,
  what moved, how to say it, and the source with its access date. It then saves the same content as HTML and prints
  a one-page PDF with headless Edge. The command was tested here and printed one page.
- If nothing moved, it says so and writes nothing.
- 223 words, US spelling, no name or resume. The orchestrator updates B's START_HERE copy.

Batch 6 closed at 11:16: (target ~11:55). V1's three unverified facts were all verified on primary
sources and none cut (`research/V1_followups.md`, for the orchestrator to relay to B):
1. **C-Q-10:** both companies' special meetings on 3 Sep 2026 approved, per the EDGAR 8-K Item 5.07 filings
   (R-104 Dominion, R-105 NextEra).
2. **C-S6-06 −44%:** Dominion's own release of 8 Jun 2026 on its IR site, quoted verbatim. It measures average annual
   outage time for customers in Mainfeeder Hardening areas, with no baseline, major-event treatment or comparison
   stated. R-013 now cites this primary source.
3. **Trim cycles:** the Dominion VA/NC FAQ was re-opened and both quotes are unchanged (R-076).

Register: R-001 to R-105.

Batch 5 closed at 09:45:
- ✅ **`research/hard25_answers.md`** (09:41), the full study version:
  - V3's 25 merged with the brief's seven (all kept). Merges: E1+E2, B3+B4, B5+B9.
  - Claim → Proof → Limit, with locators; the upgrade variants are marked.
  - Ten new numbers (N-1 to N-11) for D to confirm.
- ✅ **`research/hard25_print.md`** (09:44), the print version: about 2,000 words, roughly 2.3 pages at 10.5 pt in two
  columns. **Page-budget issue:** with "know every number" and the two delivery pages, the appendix comes to about
  5–6 pages against the brief's cap of 4. This is the orchestrator's call.
- ✅ **`research/delivery_and_rehearsal.md`** (09:44): Page A delivery plus the three-panelist block (about 500
  words); Page B the Monday plan with times (about 500 words). Four new verified sources, R-100 to R-103.
- **New findings from the all-events check (R computed, D to confirm):**
  - Dominion is 6th of 12 on all-events SAIFI (4th ex-MED) and 9th of 12 on all-events SAIDI.
  - EIA-861 lists Dominion's method as "Other" every year, and 10 of 12 report IEEE 1366.
  - docs/06's "Half the peers use a different reporting method" conflicts with that.
  - Automated recording starts in 2015 (matches D6).
- **Fixed:** H02's wrong "same IEEE 1366 basis" in `top40.md`/`question_bank.csv` (rebuilt 09:41; picks unchanged).

Batch 4 closed at 09:16:
- ✅ V5 `research/freshness.md` (09:13). Nothing changes the storyline or any deck number.
  - `dominion_on_a_page.md` gets dated (V5) lines:
    - FERC deficiency letter 23 Sep, response 15 Oct
    - NRC notice 27 Aug
    - VA rebuttal 2 Nov
    - SC: testimony received; hearing 8 Dec
    - dividend 66.75¢
    - CVOW >640 MW, $123M contingency unused
    - data-centre pipeline +6 GW since end-2025
  - The dossier §8 table is extended. Claims R-092–R-099.
- ✅ `research/morning_prompt_2nov.md` (09:14): 193 words; names no person and no resume; gives exact paths.
- 09:15 fix: the "+6 GW (13%)" belongs to the 54 GW pipeline, not the 12 GW under agreements. Corrected in the page,
  freshness.md and R-099.

Batch 3 closed at 08:58 (R3 and R4).
- ✅ R3 `research/domain_primer.md` (08:55); ✅ R4 `research/interview_science.md` (08:57)
- Claims register: R-001 to R-091
- 08:47 Applied the orchestrator's D update to `top40.md` (H01, H08, H13, T24), the dossier §5, `for_B.md` §1 and
  R-028. Changes:
  - **Scope:** consistent with Virginia only.
  - **Weather fit:** r = 0.6973, t = 2.752, p = 0.025, CI 0.121–0.922.
  - **Peer rule:** D10.
  - **Storm county-days:** 464 → 791. None of R's text quoted 465/796.

Earlier: batch 2 closed at 08:40 (R2 and R5); the orchestrator locked G1b from the 24 ★ picks unchanged (T7
also covers performance).

Brief: `interview-prep/MASTER_PROMPT.md` §2, §4, §5 "Agent R", §9. Outputs: `interview-prep/research/`.
States: ○ not started · ◐ in progress · ✅ done · ⏸ waiting · ✖ dropped.

## Task table

| Task | State | Output | Notes |
|---|---|---|---|
| R1 Role (light search, careers site only, per owner) | ✅ 07:25 | `research/role_brief.md` | **Associate BI Analyst / BI Analyst (Richmond, Hybrid)**, supporting **Grid Resiliency programs**; posted 10–11 Sep 2026; closed; text from aggregator copies (Jobright); ~80% sure. §2 corrected 07:55: SUP is not Grid Resiliency. Candidate to confirm the requisition `[you: …]` |
| R6 Scouting for D | ✅ 07:35 | `research/for_D.md` | EAGLE-I: settled by the orchestrator at 07:40. D uses DOE's Aviary download (MD5s match figshare), so the other options are marked superseded. SCC 403 is a recorded gap. DOE-417 is at PNNL. EIA-861 2025 final came out 7 Oct (D confirmed the 2025 values match). PJM tables OK |
| R2 Dominion dossier + on-a-page | ✅ 08:20 | `research/dominion_dossier.md`, `research/dominion_on_a_page.md`, `research/for_B.md` | B's checks done 07:58: C-S2-01 confirmed (R-028, printed p. 10, "primarily due to increased storm activity"; VA vs VA+NC scope not stated). Grid Resiliency = MFH, VIM, VO, IGD/FLISR; SUP is separate (R-035). Phase IIIB from the annual report p. 120 (R-060). Merger, Q3, GS-5, rates, CVOW: R-040 to R-067. Corrected: the Supreme Court appeal concerns Chesterfield, not the rate case |
| R5 Question bank | ✅ 08:45 | `research/question_bank.csv` (126 rows), `research/top40.md` | 86 panel questions, 8 asks, 32 hard project questions. 15 sources: 11 opened plus the posting; 3 snippet-only, counted half. Score = frequency × fit. Top 40 and 24 ★ sheet picks are set by a stated rule. The hard list holds the brief's seven plus the role-brief gaps. Built by `work/scripts/r5_build_bank.py` from `r5_questions.json` (rerunnable) |
| R3 Domain primer | ✅ 08:55 | `research/domain_primer.md` | A1 one-liners table first; then indices, 2.5-beta, EIA-861 vs SCC, analysis practice, grid vocabulary, PJM/DOM, literature (Larsen 2016, Do 2023, Brelsford 2024, EIA 2024 national). Claims R-071–R-080. SCC rule **not found** (not in 20VAC5; RD916 fn 12 cites none; SCC 403). The 1990 HD21 origin is marked as inference. Gaps: IEEE 1366-2022 text (paywalled), ETR accuracy |
| R4 Interview science | ✅ 08:57 | `research/interview_science.md` | Delivery-page table first (tip → study → strength → rule). 24 sources, each DOI checked in Crossref and abstract read (OpenAlex, Semantic Scholar or preprint); script `work/scripts/r_lit_lookup.py`. **Reappraisal: mixed and small.** Brooks 2014 is positive; Ganley 2021 found no effect (n = 300, maths); Bosshard & Gomez 2024 meta-analysis gives d = 0.23; the OSF direct replication (2019) has no results. Power posing is out (Ranehill 2015). Eisend 2006 and Huffcutt 2011 are metadata only, not relied on. Answer-first, "I don't know", pacing and follow-up have no verified study. Claims R-081–R-091 |
| Final round: company box and glossary | ✅ 13:01 | `work/v6_inputs/R_company_glossary.md` | Sections 1–7 as asked, plus NEW sources (§8) and notes for B (§9). New register rows R-107 to R-131. Pages opened 1 Nov: catalyst.coop/pudl, ncei.noaa.gov, nhc.noaa.gov/data, the CPC degree-day pages, duckdb.org, the NIST e-Handbook 4.5.1.2, the DOE 2012 AMI report (saved `research_raw/doe_ami_2012/`), the Dominion newsroom and investor site, the NextEra newsroom, FERC eLibrary (a JavaScript shell) and BLS OEWS (index only; no figures). Blocked and not worked around: the Federal Register search (bot check), WAVY (403), the NCEI Storm Events text (JavaScript), the Penn State STAT 501 page (certificate). Scripts: `r_final_pdf_grep.py`, `r_final_html_grep.py`, `r_final_standards_check.py`, `r_final_fit_check.py` |
| Claims register | ◐ | `research/claims_register.csv` | R-001 to R-131 (8 columns; shape checked after the final-round append of R-107 to R-131). R-028 scope updated 08:47; R-099 attribution fixed 09:15; R-100–R-103 (batch 5 studies) 09:39; R-104/R-105 shareholder votes and R-013 (primary IR URL), R-076 (re-opened) 11:15 |
| Batch 6: V1 follow-ups | ✅ 11:16 | `research/V1_followups.md` | All three verified, none cut. Sources: SEC EDGAR 8-K Item 5.07 for both companies (3 Sep 2026); Dominion IR release of 8 Jun 2026 (raw saved in `research_raw/v1_followups/`); Dominion VA/NC tree-trimming FAQ |
| V5 Freshness | ✅ 09:13 | `research/freshness.md`; `research/morning_prompt_2nov.md` (09:14) | Window 25 Oct–1 Nov. Primary sources: the Dominion release feed, Federal Register (FERC 21 Oct; NRC 27 Aug), NextEra releases. Secondary: Q3 call transcript, WTVR 28 Oct, pv magazine 27 Oct, NEPOOL. No storm, leadership or investor-day item found. Axios (403) not used. The morning re-check runs on 2 Nov via the prompt |
| Batch 5: hard 25 answers | ✅ 09:41 | `research/hard25_answers.md` | Inputs: V3, the G2 revision, V2 rulings, the resume (read locally; paraphrased, with locators). Merges: E1+E2, B3+B4, B5+B9; added the brief's SCC, data-centre and do-differently questions. Numbers: 464/791, 12 of 12, −1.4 to +2.1, r 0.6973 / t 2.752 / p 0.025. H2 adds up from resume dates (10 months data-titled, about 38 total). N-1 to N-11 await D. Resume-overlap check: no 6-word sequence shared |
| Batch 5: delivery and rehearsal | ✅ 09:41 | `research/delivery_and_rehearsal.md` | Page A: R4's table plus the three-panelist block (inference, Dixon 2002). Page B: Monday plan, Step 1 the adopt-or-not decision (60–90 min, time-boxed to 10:30), then Power BI guide, read the brief, deck ×3 at 8 min, sheet and hard-25 recall drills, mock panel, print, spaced second round, stop at 20:00. New sources: testing effect, spacing, sleep (R-100–R-103) |

## Sources consulted (all accessed 2026-11-01)

**Batch 1 (R1, R6)**

| ID | Title | URL | Used for |
|---|---|---|---|
| S-R1-01 | Dominion careers search (82 jobs) | https://careers.dominionenergy.com/search/?q=&locationsearch=&sortColumn=referencedate&sortDirection=desc | R1 |
| S-R1-02/03 | Jobright copies of the BI posting | https://jobright.ai/jobs/info/6aa3a1d5c5a856ac7e33a91a · https://jobright.ai/jobs/info/6aa3788b83233ca167c8aba2 | R1, R5 (S12) |
| S-R1-04 | Third-party tracker (date corroboration) | https://github.com/VictorJimenez3/fable-job-search/issues/3627 | R1 |
| S-R1-05..10 | Dominion postings (closed and live) | see role_brief §8 | R1 |
| S-R1-11 | Dominion release 8 Jun 2026 (via StockTitan) | https://www.stocktitan.net/news/D/dominion-energy-prepares-year-round-for-hurricane-season-and-o7ahitzchhvw.html | R1, R2 |
| S-R6-01..10 | figshare API, ORNL, data.gov, EIA-861, SCC RD916, Dominion GT pages, DOE-417 (PNNL), ORNL catalogue, PJM, VAC 20VAC5 list | see `research/for_D.md` | R6 |

**Batch 2**
- **R2:** sources D1–D15 are listed in `research/dominion_dossier.md` §12. They include:
  - the Dominion 2025 Annual Report
  - the Q3 2026 release (30 Oct) and the Q3 call transcript
  - the NextEra–Dominion joint release (18 May)
  - the Grid Resiliency and GT pages
  - WTVR, WTKR, Virginia Business, Loudoun Now
- **R5:** sources S01–S15 are listed in `research/top40.md` (Method), and each is marked as opened or snippet-only.
  New in this batch:
  - S13: IEEE PES Boston slides, downloaded
  - S15: Edureka's Power BI bank
  - R-068: CLIMB's process section, re-read for verbatim quotes

**Batch 3**
- **R3:** the sources table is in `research/domain_primer.md` §8:
  - the IEEE PES Boston slides
  - the EIA-861 instructions and EIA Today in Energy (id 66744)
  - SCC RD916 and HD21 (1990)
  - Dominion's VA tree-trimming page
  - Larsen 2016 (eScholarship preprint), Do 2023, Brelsford 2024
- **R4:** the sources table is in `research/interview_science.md`. It lists 24 entries; each DOI was checked in
  Crossref and the abstracts were read through OpenAlex, Semantic Scholar or a preprint. The OSF registration cyzgj
  was read through the OSF API.
- **Did not open:**
  - emp.lbl.gov returned 403 to WebFetch, so the eScholarship PDF was used instead
  - Elsevier abstracts for Eisend 2006 and Huffcutt 2011 were unreachable; neither is relied on

**Batch 4 (V5)**
- The sources table (V5-1 to V5-7) is in `research/freshness.md`:
  - the Dominion release feed and the 27 Oct dividend release
  - Federal Register: the FERC combined notice of 21 Oct (EC26-131 response) and the NRC notice of 27 Aug
  - NEPOOL (the FERC deficiency letter, 23 Sep)
  - WTVR 28 Oct; pv magazine USA 27 Oct
  - NextEra's release list
- The Q3 call transcript (D5) was re-read for verbatim quotes.
- **Did not open:** Axios Richmond (403), Energy News Beat (snippets only), MLex (paywall), Utility Dive's 21 Oct piece.

**Batch 5**
- Literature: Roediger & Karpicke 2006, Rowland 2014, Cepeda et al. 2006, Lim & Dinges 2010. Each DOI was checked in
  Crossref and the abstract read in OpenAlex; raw JSON is in `research_raw/lit_meta_b5/`. Claims R-100 to R-103.
- Local, read-only computations on committed data (no web):
  - `work/scripts/r5b_all_events_rank.py`: all-events ranks, medians without Dominion, EIA standard and
    auto-recorded flags
  - `work/scripts/r5b_fit_checks.py`: the 2025 prediction interval and the SD
  - `work/scripts/r5b_quote_check.py`: resume overlap, printed to the console only
- Repo docs read: docs/03 (P18, P20–P27), docs/04 (D6, D10, D13–D15), docs/05, docs/06, sql/09.

Raw downloads (untrusted; read only):
- `interview-prep/work/research_raw/`:
  - `careers_search/`, `careers_all/`, `careers_jobs/`, `jobright_bi/`
  - `r6_scout/`, `scc_combined/`, `dom_gt_docs/`, `doe417_peek/`, `pjm_peek/`
  - `dom_ar2025/`, `dom_web/`, `dom_q3_2026/`, `merger/`
  - `ieee_boston_pes/`, `eia861_instr/`, `scc_hd21_1990/`, `eia_tie_66744/`, `dom_veg/`, `larsen2016/`
  - `lit_meta/` (OpenAlex, Crossref and Semantic Scholar JSON)
  - `v5_fresh/` (V5 pages and the release feed)
  - `lit_meta_b5/` (batch-5 OpenAlex, Crossref and Semantic Scholar JSON)
  - `v1_followups/` (the Dominion 8 Jun 2026 release page, batch 6)
- Scripts in `interview-prep/work/scripts/`:
  - `r_*.py`: `r_pdf_grep.py` now forces UTF-8 output; new are `r_lit_lookup.py` and `r_update_claim.py`
  - `r5_build_bank.py` and `r5_questions.json`
  - `r34_lit_queries*.json`
  - `claims_batch2*.jsonl`, `claims_batch3*.jsonl`, `claims_batch4a.jsonl`, `claims_batch5a.jsonl`,
    `claims_update_0905.json` and `claims_update_0916.json`
  - batch 5: `r5b_lit_queries.json`, `r5b_all_events_rank.py`, `r5b_fit_checks.py`, `r5b_quote_check.py`

## Outputs

- `research/role_brief.md` (R1, 07:25; §2 corrected 07:55)
- `research/for_D.md` (R6, 07:35; EAGLE-I note 07:40)
- `research/for_B.md` (07:58; Phase IIIB 08:30; scope 08:47; §4 updated 08:57)
- `research/dominion_dossier.md`, `research/dominion_on_a_page.md` (R2, 08:20; dossier §5 scope 08:47)
- `research/question_bank.csv`, `research/top40.md` (R5, 08:40; D's numbers 08:47)
- `research/domain_primer.md` (R3, 08:55)
- `research/interview_science.md` (R4, 08:57)
- `research/freshness.md` (V5, 09:13), `research/morning_prompt_2nov.md` (09:14)
- `research/hard25_answers.md` (full, 09:41), `research/hard25_print.md` (print, 09:44),
  `research/delivery_and_rehearsal.md` (09:44): batch 5. If a number changes, edit both hard25 files.
- `research/claims_register.csv` (R-001 to R-131; R-107 to R-131 added in the final round)
- `work/v6_inputs/R_company_glossary.md` (final round, 13:01): the company box, the glossary, the 45-second
  answer, the manual check and assistant paragraph, salary, storm duty, the FPL answer, the NEW sources and the
  notes for B

## Issues and gaps

1. **The BI posting is closed.** The text comes from an aggregator, so it is quoted "as shown on Jobright". The
   candidate should confirm the requisition `[you: …]`.
2. **EAGLE-I: resolved** by the orchestrator (07:40). D uses DOE's Aviary download, and the other options are
   superseded.
3. **scc.virginia.gov returns 403** to scripts and to WebFetch. It is a recorded gap and was not worked around.
   Plain public PDFs on dominionenergy.com or rga.lis.virginia.gov are fair sources; none has been found yet
   for the filed reliability report.
4. **Not found:** the Virginia rule that requires the Annual Reliability and Tree Trimming Report.
   - It is not in 20VAC5, and RD916's footnote 12 cites no rule. The SCC site is 403 and was not worked around.
   - The 1990 SCC report HD21 (tree-trimming guidelines; annual data from 1990) is the likely root. That link is
     marked as inference (R-071).
5. **DOE-417 has no utility column.** Events are matched by area, date and size; the "Virginia; West Virginia"
   rows are probably APCo (*inference*).
6. **Privacy:** aggregator pages list named Dominion employees. They are recorded nowhere.
7. **Pay:** figures are omitted from every R file. The salary question has an approach and `[you: your range]`
   only, and the scan of R5's outputs found no pay, phone or email strings.
8. **Interview-report sites are blocked** and were not worked around:
   - Glassdoor, Indeed and Teal: 403
   - Interview Query: 429
   - the OMS question page: 403 after its redirect

   As a result, the Dominion-specific question evidence is CLIMB (opened, R-068) plus Glassdoor snippets
   (unverified, R-069, counted half).
9. **Other source failures:**
   - The SEC 10-Q is over WebFetch's 10 MB limit, so the release, the annual report and the call transcript
     were used instead.
   - Simplilearn's Power BI page returned 404; Edureka was used instead.
10. **Scope of Dominion's 130/133, closed 08:47:** the report doesn't state it. D's check shows the figures are
    consistent with Virginia only: VA gives 130.22/133.01, VA + NC would print 129. R-028 is updated.
11. **H01 statistics, closed 08:47:** now D's values from the unrounded r (r = 0.6973, t = 2.752, p = 0.025,
    CI 0.121–0.922). R's earlier 2.77 and 0.13 came from r = 0.70.
12. **Not sourced in this run:** estimated-restoration-time (ETR) accuracy. The primer says to ask the panel instead.
13. **No verified study** for answer-first, "I don't know", pacing or the follow-up note. The brief's practitioner
    lead (Minto) was not opened. B keeps these as advice without a citation.
14. **V5 gaps (09:13):**
    - **South Carolina:** the content of the 28 Oct testimony was not found; only its receipt is known (Q3 call).
    - **Hart-Scott-Rodino (HSR):** status not found.
    - **13–14 Oct DOE/PJM emergency order:** the Axios page returned 403, so it is not used.
    - **FERC and NRC:** no order found as of 1 Nov.
    - **Virginia rebuttal:** due 2 Nov. The morning prompt covers it.
15. **Batch 5 numbers awaiting D.** N-1 to N-11 in `hard25_answers.md` were computed read-only by R, and the ex-MED
    values reproduce C-S3-01. They need D's confirmation and `claims.csv` rows before print. N-7's split of the 422
    gap between the two filters is R's reading [I].
16. **docs/06 conflict.** The Fair comparison headline says "Half the peers use a different reporting method".
    EIA-861 shows Dominion VA and Alabama Power on "Other" and the other 10 on IEEE 1366 in every year 2014–2025
    (N-5). Passed to B and D.
17. **R's own error, fixed 09:41.** `top40.md` H02 said EIA-861 uses "the same IEEE 1366 basis for every utility", and
    it claimed SCC filings add cause and circuit detail, which is unverified. Corrected in `r5_questions.json` and
    rebuilt; the ★ picks are unchanged. The section is marked superseded by `hard25_answers.md`.
18. **The resume was read locally once in batch 5.** Nothing was quoted: a 6-word overlap check is clean, and only
    factual fragments of 5 words remain. Phone, email and name appear in no file.
19. **Final-round gaps (13:01):**
    - **SCC docket search:** not opened (403 to scripts). The manual check sends the candidate there in a normal
      browser.
    - **Federal Register search:** redirected to a bot check, so it was not opened today. R-093 and R-094 used pages
      opened earlier.
    - **NCEI Storm Events description:** loads by JavaScript and was not captured. The glossary line relies on
      the NCEI home page and repo docs/01 S5.
    - **DOM zone, co-ops part:** this comes from repo docs/07 note 4 and is marked as inference.
    - **R-124 and R-125:** computed by R; D should confirm them before print.
    - **The §4 assistant paragraph is for screen use only.** It is flagged to B because the printed pack never
      says how it was made.

## Hand-offs

- **To B:**
  - `top40.md` and `question_bank.csv` (08:45), for B3. The ★ picks follow the stated rule.
  - `dominion_on_a_page.md` for P3 p. 7.
  - `for_B.md` (C-S2-01 confirmed; slide 6 facts).
  - `domain_primer.md` (A1 table first) and `interview_science.md` (delivery table first), 08:57.
  - `morning_prompt_2nov.md` (09:14): the block goes into `START_HERE.md` unchanged. Also `freshness.md` and
    the V5 lines in `dominion_on_a_page.md` (09:13), for P3 p. 7.
- **From D (through the orchestrator, 08:4x):** all three needs answered and applied at 08:47: the scope check,
  the weather-fit statistics and the peer rule D10.
- **From the orchestrator:** all done.
  - 07:40 (two messages): for_D first; B's two checks early in R2; EAGLE-I superseded; SCC gap; batch order
    R2 → R5, then R3 → R4.
  - 08:4x: G1b locked; batch 3 is R3 then R4; V5 at ~11:30 on its go.
  - ~09:00: batch 4. V5 now (done 09:13); the morning prompt (done 09:14); then stand by for the V3 split.
  - ~09:25: batch 5, two items, both done at 09:41:
    - `hard25_answers.md`
    - `delivery_and_rehearsal.md`
- **To B (batch 5):** `for_B.md` §4 lists both files, the N-numbers and the docs/06 flag.
- **To D (through the orchestrator):** confirm N-1 to N-11; check the docs/06 "half the peers" headline.

## Resume from here

- **Last finished:** the final round (13:01): `work/v6_inputs/R_company_glossary.md` and register rows R-107 to
  R-131. Before that came batch 7 (morning prompt, 11:47), the C-Q-10 follow-up (12:04), batch 6 (11:16) and batch 5
  (09:41).
- **Next:** wait for the orchestrator and B's placement. Likely work:
  - **If D's check changes R-124 or R-125:** edit §1 (the FPL line) and §7 of `R_company_glossary.md`.
  - **If B's real layout overflows half a page:** the box and the glossary are about 26 lines each. Trim the
    source tags and the spare lines first.
  - **Final-round scripts:** each takes its file as an argument and prints UTF-8 even under `-I`.
    - `r_final_pdf_grep.py <pdf> <regex> [ctx]`
    - `r_final_html_grep.py <html> <regex> [ctx] [max]`
    - `r_final_standards_check.py <repo_root>`
    - `r_final_fit_check.py <md> [cpl]`
- **Earlier likely work, still open:**
  - **If D's checks change any N-number:** edit `hard25_answers.md`. The Q-ids that use them:
    - Q1: N-1, N-2
    - Q2: N-2, N-3, N-5, N-11
    - Q5: N-6, N-7
    - Q17: N-8
    - Q18: N-3
    - Q20: N-9
  - **V3 follow-ups.**
  - **The final V5 freshness check.**
- **Rules for any rework:**
  - experience from the resume only (`[you: …]` otherwise)
  - deck numbers from `claims.csv` or D
  - Dominion facts from the register
  - no 1 Nov discovery stories (V2)
- **Release feed (no browser needed):**
  https://news.dominionenergy.com/feed/PressRelease.svc/GetPressReleaseList?LanguageId=1&bodyType=0&pressReleaseDateFilter=3&pageSize=20&pageNumber=0&includeTags=true&year=2026&excludeSelection=1
- **Tools:**
  - WebSearch and WebFetch are deferred: load them with ToolSearch `select:WebFetch,WebSearch`
  - curl with a browser user agent works for the Dominion sites, eia.gov, pjm.com, rga.lis.virginia.gov,
    doe417.pnnl.gov and site.ieee.org
  - it does not work for scc.virginia.gov, osti.gov, figshare downloads, Glassdoor, Indeed or Teal
- **Scripts:**
  - `work/scripts/r_pdf_grep.py <pdf> <regex> [ctx] [--pages]`
  - `r_html_text.py <html> [regex] [--min N] [--max M]`
  - `r_append_claims.py <rows.jsonl>`
  - `r_update_claim.py <updates.json>`
  - `r_lit_lookup.py <queries.json> <raw_dir> <report.txt>`
  - `r5_build_bank.py <json> <out_dir> <stamp>`
- **Pipes:** Windows Python under `-I` can crash on a closed pipe (`OSError 22`) when piped to `head`. Write to a
  scratch file and read it instead.
