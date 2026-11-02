# Master session brief: the Dominion Energy interview pack

**Launch:** open a new terminal (after the Snowflake environment variables are set, if they are), `cd`
to `C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review`, start
Claude Code on Opus 5.5, and send:

> Read `interview-prep/MASTER_PROMPT.md` in full and run it end to end.

Written 2026-11-01 by session b1a7f8c6, after reading the candidate's resume, this repo (README, docs
00 to 08, SQL, data), the decoded `.pbix` (report layout and data model), the local `CLAUDE.md`, the
`_setup/` Snowflake runbook, and the notes in `interview-prep/inputs/`.

---

## Fill in before launch (optional: blank is fine, the session works around each one)

| Item | Value |
|---|---|
| Interview date, time, place (on site, video) | **Tuesday 3 November 2026**; time and place: |
| Role title, and the posting link or pasted text | |
| Format, if known (rounds, who is on the panel, length, whether they asked for a presentation) | |
| Power BI Desktop on this PC | ☐ install it (free, `winget install Microsoft.PowerBI`) · ☐ don't; I'll apply changes on my laptop |
| PJM Data Miner API key (free registration; optional) | ☐ none · ☐ in user env var `PJM_API_KEY` |

---

## 0. Your job

You are the **orchestrator** of an autonomous run of 6 to 8 hours. The owner of this brief is the
candidate; `Saketh_Bollina_Resume.pdf` in the repo root is theirs. They live in Virginia and have an
interview at **Dominion Energy** for a mid-to-senior business-intelligence or data-analyst role
(confirm the exact role in R1).

You deliver the **interview pack** in §3:
- a short deck they can print and present
- a one-sheet bank of the most-asked questions with answers
- an interview brief (PDF, at most 12 pages): where the data came from, how it was built, what it
  does and how it helps Dominion, with every number explained
- an upgraded Power BI report

All of it rests on better public data, every number traces to a source, and every answer is true to
the candidate's real experience.

You keep the master ledger and run three Opus 5.5 agents, **R (research)**, **D (data)** and
**B (build)**, each with its own ledger. You sequence their work through the gates in §7, verify
everything (§8), and finish with a pack the candidate can print.

The owner explicitly asked for this multi-agent run: three Opus 5.5 agents, each with its own ledger.
That is the opt-in.

**Deadline: the interview is Tuesday 3 November 2026.** Finish the whole pack in this run, on Sunday
1 November, so Monday 2 November is free for study, rehearsal and printing.

Priorities, in order: **(1) every claim is true and defensible, (2) the candidate understands it,
(3) it is short and clear, (4) it looks high-end.** A beautiful deck with one wrong number loses the
interview. A plain deck the candidate can defend wins it.

---

## 1. The brief, in the owner's words

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

**What that means for the pack:**
- "Not too long" means the main deck fits a 10-minute talk.
- "Understand and present properly" means the interview brief (P3) matters as much as the deck. It
  is the candidate's one study document for 2 November.
- "Research backed, academic papers, psychologically" covers two things: the question bank's selection,
  and the delivery advice. Both cite verified sources in the interview brief, never on the printed sheet.
- "Internal instructions" means this brief, the ledgers and the research method stay inside
  `interview-prep/`. The deliverables never mention how they were made.

---

## 2. What exists now (read in this order)

| # | Path | What it is |
|---|---|---|
| 1 | `CLAUDE.md` (local) | Ownership (upstream is the candidate's GitHub; this machine's account can pull only, **never push**), local-only files, the two checks, Snowflake and MCP state |
| 2 | `README.md`, `docs/README.md`, `docs/00` to `docs/08` | The project: findings, sources, data dictionary, quality checks, decisions D1 to D14, measures, report spec, runbook, worked transformations. `docs/00_conventions.md` is binding for anything added to the repo |
| 3 | `_setup/README.md`, `_setup/logs/` | Snowflake CLI (connection `dominion`, key-pair) and the managed MCP server `RELIABILITY.MART.RELIABILITY_MCP`; what has and has not been run |
| 4 | `data/raw/README.md` | NOAA (13 files, 831,288 rows) and EIA-930 (17 files) are local and verified; manifests per folder |
| 5 | `Dominion Dashboards.pbix` (repo root, gitignored) | The candidate's current report. Decoded summary in §2.1 |
| 6 | `powerbi/measures.dax`, `powerbi/Dominion_Reliability_PowerBI_Data.xlsx` | The measures and the workbook behind the report's five Excel tables |
| 7 | `sql/00` to `sql/08`, `scripts/` | Snowflake pipeline (RAW, STG, MART, tests T1 to T12) and the local DuckDB runner |
| 8 | `Saketh_Bollina_Resume.pdf` | The candidate's resume: the **only** source for their experience |
| 9 | `interview-prep/inputs/2026-11-01_prior-chat-notes.md` | Earlier research on Dominion, the dashboard the owner pictured, and a review of the .pbix. **Leads, unverified** |

Another session set up Snowflake and the MCP server and organised `data/raw/` today. Read its notes
(items 1, 3, 4) before touching `data/`, `sql/`, `.mcp.json` or `_setup/`. Never move or rename what it
organised.

**Snowflake state per `CLAUDE.md` (01-11-2026):**
- The build is loaded and verified: `_setup/snowflake/20_verify_build.sql`, 32/32 PASS. **Do not
  re-run `load_and_build.sh`.**
- The MCP server, role, user and token exist, and the server lists its tool. But tool calls fail with
  "Access denied for trial accounts" until the owner adds a credit card to the trial account.
- Until then, query with `snow sql -c dominion -q "…"`. That runs as RENV with ACCOUNTADMIN, so the
  Snowflake rules in §4 apply.
- Re-read `CLAUDE.md` at Phase 0: the status may have moved on.

### 2.1 The .pbix as it stands (decoded 2026-11-01)

**Pages and format**
- Eight pages, 1920×1080, in PBIR format (`Report/definition/pages/<id>/visuals/<id>/visual.json`).
- Order: Scorecards, What Moved, Weather, Peer Comparision, Growth, Seasonal, Executive Dashboard-1,
  Executive Dashboard-2.

**Sources**
- 11 tables come from the candidate's **old Snowflake trial** (warehouse `SNOWFLAKE_LEARNING_WH`,
  `RELIABILITY.MART`). That is a different account from the one this workspace uses (see `CLAUDE.md`).
- 5 tables (LoadGrowth, Programmes2025, Headline, AmiEventStudy, Tests) come from
  `C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx`. That path does not exist on
  this PC.

**Model**
- 17 tables and 38 measures. The year slicer is a disconnected `Dashboard Year` table read with
  `SELECTEDVALUE(…, 2025)`.
- Two relationships: `FCT_RELIABILITY[UTILITY_KEY]` → `DIM_UTILITY` (M:1), and a meaningless
  auto-created `Headline[losses_pct]` → `Programmes2025[losses_pct]`.

**Issues.** Every issue in the prior review (inputs file, part C) is present in the file:
- the two executive pages have swapped titles
- the overclaiming titles are still there
- the "2023 = 100" axis label is wrong
- the peer slicer on the landing page can make the page contradict itself
- 11 visuals sum raw columns
- there are unused tables
- the "Selected" measures are parked in AmiEventStudy
- the Tests table is loaded but not shown
- alt text is on 0 visuals
- the Seasonal page has one chart

**Data level.** Everything is annual or PJM-zone level. Nothing is at county level, nothing covers
individual outage events or restoration curves, and nothing hourly goes below the DOM zone. That is
the "real quality data" gap.

**Tools on this PC (checked 2026-11-01)**
- Power BI Desktop is not installed.
- The Snowflake CLI `snow` is installed.
- The repo `.venv` (Python 3.12) has `duckdb` and `pandas`.

### 2.2 Findings already in the repo (the story's spine; D re-verifies every one before use)

- **Headline.** Dominion's reported rolling 3-year SAIDI ex-MED rose from 130 (2022–24) to 133
  (2023–25).
- **2023 to 2025, EIA-861, ex-MED:**

  | Measure | 2023 | 2025 | Change |
  |---|---:|---:|---:|
  | SAIDI | 123.3 | 144.4 | +17% |
  | SAIFI | 1.165 | 1.320 | +13% |
  | CAIDI | 105.9 | 109.4 | +3% |

  The rise comes mostly from **more interruptions**, not longer ones.
- **Storms.** Storm county-days went from 465 (2024) to 796 (2025). Over 2015–2024 they correlate
  r = 0.70 with SAIDI ex-MED (n = 10). The fit predicts 145.3 for 2025 against 144.4 actual.
  Exploratory only.
- **All events vs ex-MED.** In 2025 all-events SAIDI was 306.7 against 144.4 ex-MED.
- **Peers.** Dominion has the fourth-highest SAIDI of twelve peers over 2023–25; reporting methods
  differ, so treat this as indicative. Restoration is mid-pack; frequency is the gap. Since 2015,
  co-op SAIFI rose 37% against 14% for Dominion.
- **Demand (PJM DOM zone, EIA-930, 2019 to 2025).**
  - The highest hour rose about 26% and the lowest about 52%.
  - Night hours rose 41% and afternoon hours 27%.
  - The winter peak was at or above the summer peak in 2022, 2025 and 2026.
  - 47 of the top 50 hours fall at the end of 2025 or later.
- **Sales.** Commercial sales rose 65% since 2013 on 8% more customers. That is consistent with
  round-the-clock loads; the data does **not** attribute it to data centers (D14).
- **Smart meters.** Most customers have a smart meter, but almost none are on a time-varying rate.

---

## 3. The interview pack: what "done" means

Everything lands in `interview-prep/deliverables/`. P1 to P3 are printed or studied; P4 runs on the
candidate's laptop; P5 is the door in.

### P1. The deck (`01_deck/`)

**Purpose and length**
- A 10-minute walkthrough, presented on screen or from paper, plus a leave-behind for each
  interviewer.
- At most **8 main slides**, title and close included, plus an appendix of at most 6.

**Files**
- PPTX: 16:9, editable, with speaker notes on every main slide (a 60–80 second talk track).
- Print PDF: US Letter landscape, one slide per page.

**Print rules**
- The PDF reads in colour and survives grayscale: never carry meaning by colour alone.
- Body text at least 12 pt and chart labels at least 10 pt at print size.

**Every main slide has**
- an **action title** that states the finding (sentence case, about 15 words at most)
- one chart or one diagram
- one line on what it means for Dominion
- a source line (dataset, years, table or query)

**Storyline (proposed; B may improve it after R1, but keep the arc and the length)**
1. **Title.** "Dominion Energy Virginia reliability: what public data shows, and where I'd look
   first." Candidate name and date, and "Independent analysis of public data". Name only: no phone
   or email.
2. **Answer first.** The 3-year SAIDI went from 130 to 133, and the rise comes from more frequent
   interruptions, not longer ones. Give the three numbers.
3. **Frequency versus duration.** SAIFI and CAIDI trends, plus the peer scatter: restoration is
   mid-pack, frequency is the gap.
4. **Weather.** NOAA storm exposure and the new county-level outage view from EAGLE-I: a map and one
   major-event restoration curve. State the limits on the slide.
5. **Demand is changing shape.** Night load is up 41% and the winter peak now rivals summer. Explain
   why that matters for reliability and planning.
6. **What I'd do with Dominion's own data in the first 90 days.**
   - SAIFI drivers at circuit and feeder level, from cause codes
   - customers experiencing multiple interruptions (CEMI)
   - AMI "last gasp" signals to measure restoration
   - vegetation cycles
   - ranking hardening and undergrounding work by customer-minutes avoided per dollar
7. **How I built it.** One slide: public sources → Snowflake RAW, STG, MART → tests → Power BI
   (Import). Show the governance: tests, data dictionary, decisions log.
8. **Close.** Three takeaways and, if R1 supports it, one line on how the candidate's experience maps
   to the role.

**Appendix:** definitions (IEEE 1366, MED), methods, data sources and checks, limits, the weather fit.

**Visual system**
- Light and print-first.
- Colour meanings from `docs/00_conventions.md`: `#0A66C2` for the subject, `#B8BCC2` for context,
  `#6B7280` for second context, `#E8B117` for a third category, `#1F2A44` as the dark accent.
- One type family.
- No Dominion logo and no imitation of Dominion's branding.
- Charts follow the `dataviz` skill.

**Chart production.** Charts are rendered by script from D's outputs and saved with the script and a
data snapshot, so every chart can be reproduced. The dark command-centre look the owner pictured
(inputs, part B) sets the **content** of the new views: KPI cards, county map, restoration curves,
hourly heatmap, seasonal peaks, sector split, storm timeline. It does not set the printed style.

### P2. The question sheet (`02_question_sheet/`)

**Format**
- **One sheet**: US Letter, both sides allowed, as a print PDF with an editable source (DOCX or MD).
- About 20 to 24 questions, with body text at least 8.5 pt.

**Groups**
- Opening: tell me about yourself, why Dominion, why this role
- Behavioural (STAR)
- Technical BI: SQL, DAX and filter context, data modelling, Power BI performance and refresh,
  Snowflake
- Utility domain: SAIDI, SAIFI, CAIDI, MED, how you'd investigate rising SAIFI
- Role- and Dominion-specific, including how the candidate thinks about a company in a pending merger
- Five questions to ask the panel
- A closing line

**How questions are chosen.** R's frequency table (R5) picks them, not taste.

**Answers**
- Cue format, 2 to 4 lines each, about 60–90 seconds spoken.
- Each answer is a claim, then one proof point from the resume, then the tie to Dominion.
  Behavioural answers are STAR micro-scripts.
- No citations on the sheet; the sources sit in the interview brief's appendix.

**Logistics questions.** Start date, work authorisation and location get placeholders only
(`[you: …]`). Never assume an answer.

**Salary expectations.** Give the approach (research the market band, state a range, keep the focus on
total compensation and the role) with `[you: your range]`. **No figure appears in any file.**

### P3. The interview brief (`03_interview_brief/`; for the candidate only, never handed out)

**The owner's ask (2026-11-01):** one PDF, not too many pages, covering where the data came from, how
it was built, what it does and how it can be useful, "perfectly made". It is the candidate's single
study document for 2 November. Make it the best-designed piece in the pack.

**Format**
- US Letter portrait, at most **12 pages**: a main body of at most 8 and an appendix of at most 4.
- The same design system as the deck. It has a cover, a short contents list and page numbers.
- One idea per page. Diagrams are drawn, not written as text. Body text is 10.5 pt or larger.
- **Recommended build:** HTML and CSS, printed to PDF with headless Microsoft Edge
  (`msedge --headless --print-to-pdf=…`, present on every Windows 11 machine). This gives full
  control of the type. B may use another tool if the result is as good. Keep the HTML or MD source.

**Main body (at most 8 pages)**
1. **The project on one page:** the question, the answer and the three findings, in plain words.
2. **Where the data came from:**
   - One row per source: publisher, what it holds, years, level of detail (annual, county, hourly),
     how it was obtained, licence and limits.
   - A lineage diagram from each source to the charts it feeds.
3. **How it was built:**
   - A pipeline diagram: download → Snowflake RAW, STG, MART → tests → Power BI (Import).
   - The key decisions (D1 to D14 and the new ones) in plain words.
   - How the tests and reconciliations prove the numbers.
4. **What it does:** each dashboard page and each deck slide, the question it answers, and how to read
   it.
5. **How it helps Dominion:**
   - reliability planning, storm response and load planning
   - what becomes possible with internal data (OMS, AMI, cause codes, feeders)
   - the first 90 days
6. **Limits, stated plainly,** and why saying them out loud builds credibility.
7. **Dominion on a page.**
8. **Domain primer:** the definitions the candidate must be able to say without notes.

**Appendix (at most 4 pages):** know every number; the 25 hardest questions with answers; delivery
and rehearsal on one page.

**Section detail.** Fit everything to the page budget. The talk tracks also live in the deck's speaker
notes.

- **Know every number.** One row per figure in P1 and P2: the value, what it means in plain words, how
  it was computed (table, query or measure), the source, the caveat, and the likely follow-up with its
  answer.
- **The talk.** The track for each slide (the same text as the speaker notes), the project story in 60
  seconds and in 3 minutes, and a 30-second "tell me about yourself".
- **Domain primer (about 1 page).**
  - SAIDI, SAIFI, CAIDI, CEMI, MAIFI
  - MED and the IEEE 1366 2.5-beta method, and why the analysis uses ex-MED
  - EIA-861 versus Virginia SCC reporting
  - AMI, feeders, vegetation management, undergrounding
  - PJM and the DOM zone, and data-center load
- **Dominion on a page,** current to the run date: the business, Q3 2026, merger status and the
  approvals still pending, data-center demand, CVOW, rates and affordability, reliability programmes.
  Every line carries a source.
- **The 25 hardest questions** from the mock panel (V3), with answers. Include at least:
  - "your weather fit has ten points"
  - "why public EIA data and not the SCC filings"
  - "did data centers cause the demand growth"
  - "what is a major event day and why exclude it"
  - "walk me through your model and the year slicer"
  - "what would you do differently"
  - "your county outage data covers every utility in the county, not only Dominion"
- **Delivery, backed by research.** Each tip names the study it rests on (verified, §9):
  - the first minutes and rapport
  - answer first, then the support
  - stating limits up front (two-sided messages build credibility)
  - asking good questions
  - reappraising anxiety as excitement
  - handling "I don't know" as "here's how I'd find out"
  - pacing, the close and the follow-up note

  Leave out practices that failed replication (power posing, for one).
- **Rehearsal plan for 2 November:** what to rehearse, in what order, with times.

### P4. The upgraded Power BI report (`04_powerbi/`)

**Outcome:** a report the candidate opens **offline on their own laptop** that has:
- the full fix list from §2.1 and inputs part C, including the safer titles
- page names per `docs/06` and `docs/00`
- new pages from the new data:
  - county outages and restoration: EAGLE-I map and restoration curves
  - storms: NOAA county-day map and event timeline
  - demand and seasons: hourly heatmap, seasonal peaks, residential / commercial / industrial split
  - Data notes: the Tests table plus a reconciliation table
- Import mode everywhere, with the workbook location as a folder-path parameter. New tables come from
  CSV or Parquet in `data/output/`, or from this workspace's Snowflake account if it is built.

**Approach (B decides after a feasibility check)**
- **Always delivered:**
  - a click-by-click `APPLY_GUIDE.md` the candidate can follow in 60 to 90 minutes
  - `measures.dax` (updated, with every measure's purpose)
  - a theme JSON
  - the new data files
  - Power Query M for each new table
- **Optional:** a text-edited copy of the report (PBIR edits, or a PBIP project), but only if B can
  verify it opens.
- **If the owner allows installing Power BI Desktop here:** open files with
  `PBIDesktop.exe <file>`, take a screenshot with PowerShell, and look at the PNG. That is the
  verification loop. Never claim a report works without seeing it open.

### P5. `START_HERE.md` (in `deliverables/`)

- What is in the pack and in what order to use it.
- What to print: which PDFs, how many copies, single- or double-sided.
- **The plan for Monday 2 November, hour by hour:**
  - read the brief
  - rehearse the deck aloud against a timer
  - drill the question sheet
  - apply the Power BI guide and test it offline
  - print
  - stop early and sleep

  Then a short list for the morning of 3 November.
- A ready-to-paste prompt for a short Claude session on the morning of 2 November. It re-checks
  Dominion news (V5) and updates the brief's "Dominion on a page" if anything moved.
- The Power BI steps.
- Open items, including what only the candidate can fill in (`[you: …]` placeholders).
- How to push the repo upgrade from their own GitHub account if they want it public.

### Supporting work (not printed)

- `interview-prep/research/`: the dossiers, `claims_register.csv` and `question_bank.csv`.
- `interview-prep/claims.csv`: every number and factual claim in P1 to P3 (§8, V1).
- **The repo upgrade:**
  - new sources in `data/raw/<source>/`, gitignored, each with a `MANIFEST.csv`
  - small derived tables in `data/output/`
  - new SQL as `sql/09_…`, `sql/10_…`, with tests continuing at T13
  - docs 01, 02, 03, 04 (D15 onward), 05 and 08 updated

  All of it follows `docs/00_conventions.md`, so the public project itself gets stronger. An
  interviewer may open the GitHub repo.

---

## 4. Hard rules (every agent reads this section first)

**Truth**
1. Every number in P1 to P3 is in `claims.csv` with a source a reviewer can re-check. No row, no
   number.
2. Public data is never presented as Dominion's internal data. Nothing implies inside access.
3. No causal claim from a correlation. Use the safer wording from inputs part C. County outages from
   EAGLE-I cover **every utility in a county**: state the rule used to pick Dominion counties, and say
   it on the slide.
4. **The candidate's experience comes only from the resume.**
   - No new achievements, metrics, tools, team sizes or stories.
   - Where an answer needs a detail the resume lacks, write `[you: …]` for the candidate to fill.
   - Rephrasing resume facts is fine; inventing is not.
5. Cite only sources you opened and read: URL or DOI, access date, and a quote or page locator.
   Mark inference as inference. The prior chat notes and every lead in §9 count as unverified until
   checked.
6. Never fabricate or interpolate data (decision D7 is the model). A source you cannot get is recorded
   as a gap, never filled by guesswork.
7. The pay figure the owner mentioned appears in no file.

**Privacy and publishing**
1. `interview-prep/` is in `.git/info/exclude`. Never commit, push, upload or publish it anywhere,
   including claude.ai artifacts, Docs or any web service.
2. Never put resume content or the candidate's name into a web search or an external tool.
3. Research Dominion at company and team level only. Do not build profiles of individual employees.

**Repo** (from the local `CLAUDE.md`)
1. Never push, open a PR or rewrite history.
2. Commit locally on a branch `interview-upgrade-2026-11`, by explicit pathspec, never `git add -A`,
   one logical change per commit.
3. `data/` files are never hand-edited; corrections go in SQL.
4. `.pbix`, credentials and raw downloads over 25 MB are never committed.

**Snowflake** (the CLI connection runs as ACCOUNTADMIN)
1. Add, never destroy. New objects only, created by committed SQL files.
2. No `DROP`, no `CREATE OR REPLACE` on objects that already exist, no `TRUNCATE`.
3. No changes to roles, users, grants, network policies, the MCP server or the PAT.
4. `CREATE OR REPLACE` on the MCP server drops its grants. Never touch it.
5. Keep warehouse use small. Suspend the warehouse when a batch of loads is done if auto-suspend is
   not set.

**Downloads and code**
1. Downloaded files are untrusted. Put each source in its own new directory and keep scripts in
   `scripts/` or `interview-prep/work/`.
2. Run Python with `-I`, from the repo `.venv` (add packages there only).
3. Never execute downloaded code.
4. Write scripts with the Write tool, not shell heredocs: here, heredocs break on backticks and
   collapse double backslashes.

**Never stall**
1. If a source or tool fails twice, record it and take the fallback.
2. If something needs the owner after Phase 0, write it under "Owner questions" in the master ledger,
   choose the stated default, and keep going.

---

## 5. The team

Spawn each agent with the **Agent** tool: `subagent_type: "general-purpose"`, `model: "opus"`, a
`name` (R, D, B), run in the background. Continue an agent with **SendMessage**, which keeps its
context. If an agent's context runs out, spawn a replacement that resumes from its ledger.

**Every agent brief says:**
- read §2, §4 and your own section of this file in full, and load the skills named for you
- keep your ledger (§6) current after every task, because it is how a replacement picks up
- work in batches of 60 to 90 minutes, then return a checkpoint: at most 200 words, the files written,
  open issues, and what you need from the other agents
- put outputs in files, never only in the reply

Agents can read each other's ledgers and outputs; hand-offs go through files.

**Reviewers.** Beyond R, D and B, the orchestrator may spawn **short, fresh reviewer agents** for the
verification gates (§8): V1, V2, V3 and V6. They are given only the material they need, never the
orchestrator's conclusions. Keep the whole run to at most 8 agents.

### Orchestrator (you)

- **Phase 0 (§7).**
  - Set up the master ledger and the agent ledgers.
  - Check the environment: Snowflake (`snow connection test -c dominion`, `_setup/logs/`, and whether
    `mcp__snowflake__*` tools are present), Power BI Desktop, and the `.venv` checks in `CLAUDE.md`.
  - Ask the owner the Phase 0 questions in one batch, then spawn R, D and B.
- **During the run.**
  - Keep your context lean: never read large data files, and read agents' summaries and ledgers
    instead.
  - Resolve conflicts between agents.
  - Lock the storyline at G1. After that, slides change only by your decision, logged.
- **At the end.** Run the gates, assemble the pack, and write the final report to the owner (§11).
- **Skills:** `superpowers:dispatching-parallel-agents` and
  `superpowers:verification-before-completion`.

### Agent R: research

**Ledger:** `interview-prep/ledgers/R_RESEARCH.md` · **Outputs:** `interview-prep/research/`

- **R1. The role.**
  - If the owner filled in the posting, analyse it. Otherwise find Dominion's open BI and data-analyst
    postings (careers.dominionenergy.com, LinkedIn, Indeed; Richmond, Glen Allen and Virginia) and
    pick the most likely match, saying why and how sure.
  - Write `role_brief.md`: what the role does, the tools, the level, and each requirement mapped to a
    resume line and to the deck. Name gaps honestly, with how to address each one truthfully.
  - **Due first,** because B needs it for the storyline.
- **R2. Dominion dossier, current to the run date** (`dominion_dossier.md`, at most 6 pages, plus
  `dominion_on_a_page.md`).
  - Q3 2026 results and the 10-Q.
  - The NextEra merger: terms, approvals pending at FERC, NRC, the Virginia SCC, NCUC and the SC PSC,
    and the politics.
  - Data-center demand, contracts and the new large-load class; the IRP and PJM load forecast; the rate
    case.
  - CVOW; the Grid Transformation Plan, Strategic Underground Program and AMI.
  - Reliability performance and how Dominion reports it to the SCC; major storms 2013–2026 with
    customers affected.
  - Leadership, stated values and culture.
  - News from the last 60 days.
  - What a pending merger means for an analytics hire. Expect the question and prepare a calm,
    factual answer.
  - Primary sources first: SEC filings, Dominion IR, SCC dockets, company releases.
- **R3. Domain primer** (`domain_primer.md`).
  - IEEE 1366-2022 definitions and the 2.5-beta MED method.
  - CEMIn, MAIFI, CELID.
  - How utilities analyse reliability: cause codes, worst-performing circuits, vegetation cycles,
    estimated-restoration-time accuracy, storm restoration.
  - The Virginia SCC's reliability reporting rules and Dominion's filings.
  - PJM basics.
  - The peer-reviewed and lab literature on weather and outages and on reliability trends (§9).
- **R4. Interview science** (`interview_science.md`).
  - Cover:
    - meta-analyses on structured interviews and on behavioural vs situational questions
    - impression management and early rapport
    - interview anxiety and reappraisal
    - question-asking and liking
    - two-sided messages and credibility
    - graphical perception and data storytelling
    - panel interviews
  - For each finding give: the citation (with DOI, verified), the strength of evidence, and one
    practical rule.
  - Flag weak or failed findings so B leaves them out.
- **R5. Question bank** (`question_bank.csv`, plus `top40.md` for B).
  - Collect questions from Dominion interview reports for analyst roles (Glassdoor, Indeed; expect
    blocks, so use several sources), utility-analytics hiring content, BI and data-analyst question
    banks, and SQL, DAX and Power BI technical banks.
  - Deduplicate and count frequency. Rank by frequency × fit to the role.
  - Add a list of the hardest questions **this project** invites.
- **R6. Scouting for D, early.** Pointers to Dominion's annual reliability reports filed with the SCC,
  GT Plan filings, the latest EAGLE-I release, OE-417 and the PJM load forecast. Hand off through
  `research/for_D.md` within the first hour.
- **Also keep** `claims_register.csv`: id, claim, value, URL or DOI, accessed, quote or locator,
  confidence, used_in.
- **Skills:** none required. WebSearch and WebFetch are the tools; load WebSearch through ToolSearch
  if it is deferred.

### Agent D: data

**Ledger:** `interview-prep/ledgers/D_DATA.md` · **Outputs:** repo `data/`, `sql/`, `scripts/`,
`docs/`; working files in `interview-prep/work/data/`

- **D0. Baseline.**
  - Read the state (§2), run both `.venv` checks, and record the results.
  - Snowflake: the build is loaded and verified (§2). Confirm with a read-only count or two through
    `snow sql -c dominion`. Add new objects only by running new `sql/09_…`-style files, under the
    Snowflake rules in §4.
  - **DuckDB is always the local mirror and the fallback.** Nothing waits on Snowflake or the MCP
    server.
- **D1. Re-verify §2.2.** Recompute every figure from the repo's data and record the matches and
  mismatches. These feed `claims.csv`.
- **D2. Acquire, in priority order.** Each source gets its own folder under `data/raw/<source>/`, a
  `MANIFEST.csv` (file, rows, bytes, sha256, URL, downloaded_at), and licence and attribution in
  `docs/01_sources.md`.
  1. **EAGLE-I** county outage data (ORNL), 2014 to the latest release, filtered to Virginia early.
     It has 15-minute customers-out data and a published coverage or modelled-customers measure.
  2. **EIA-861** sales and customers by sector (residential, commercial, industrial) for Dominion VA
     (utility 19876), 2013–2025. Extend `pudl_sales.csv`. Add **EIA-861M** monthly sales for
     seasonality.
  3. **Dominion's annual reliability reports to the Virginia SCC** (PDF): cause breakdowns, regional
     indices, worst-circuit counts, with page references. If they hold cause codes, that is the
     biggest upgrade available. Also take reliability metrics from the GT Plan filings.
  4. **Storm context:** DOE **OE-417** events for Dominion (customers affected, duration) and NHC
     **HURDAT2** tracks for storms that affected Virginia, joined to the NOAA county-days already in
     the repo.
  5. **Geography:** Census cartographic-boundary counties for Virginia (GeoJSON or TopoJSON),
     county FIPS (see `data/reference/zone_county_correlation.csv`), and ACS county population and
     housing units.
  6. **Degree days** (NOAA) to weather-normalise load.
  7. Optional: PJM Data Miner `hrl_load_metered` for the DOM zone, only if `PJM_API_KEY` exists, to
     extend peak history before July 2018. Also the PJM 2026 Load Forecast Report's DOM table.
- **D3. Validate** (written up in `docs/03_data_quality.md`, tests T13 onward).
  - Check row counts, duplicates, coverage over time, ranges and units.
  - Reconcile against anchors:
    - EIA-861 SAIDI 144.4 for 2025
    - Dominion's 3-year 133.0
    - EAGLE-I peak customers out against OE-417 for big events
    - EAGLE-I coverage by year
  - Record every anomaly the way decision D7 did.
- **D4. Model.**
  - New objects, named per conventions, in DuckDB and in Snowflake if built:
    - `DIM_COUNTY`, including the Dominion-county rule as a column with its reason
    - an hourly or daily county outage fact (aggregate the 15-minute data; never ship it raw to
      Power BI)
    - `FCT_OUTAGE_EVENT` (event detection with a stated threshold)
    - `FCT_RESTORATION_CURVE` (percent of peak restored by hour since peak)
    - `FCT_COUNTY_DAY` (outage customer-hours with NOAA storm flags)
    - `DOM_LOAD_HOURLY`
    - `FCT_SALES_SECTOR`
  - Export small, Power BI-ready CSV or Parquet to `data/output/`.
  - New design choices go in `docs/04_decisions.md` as D15 onward.
- **D5. Analyses.** Each gets a one-paragraph finding, a chart-ready table and its caveats in
  `interview-prep/work/data/findings.md`.
  - **A1. County-day panel.** Outage customer-hours against storm presence and type. With thousands of
    county-days instead of ten annual points, this answers the "n = 10" objection. Keep the model
    explainable: stratified comparisons first, a simple count model only if it adds something.
  - **A2. The ten largest outage events** in Dominion counties since 2014: peak customers out,
    duration, time to restore 50, 90 and 99 percent, storm type, and whether restoration got faster
    over time.
  - **A3. Where frequency rose:** non-major outage events per county per year, 2015–2025, as a map.
  - **A4. Load:** hour × month × year heatmap, seasonal peaks, winter vs summer, a degree-day-adjusted
    trend, and the sector split (sales and customers, with commercial sales per customer).
  - **A5. Reconciliation:** rebuilt against reported values (EIA-861, annual report, SCC).
  - **A6. Optional:** what one minute of SAIDI means in customer-minutes (simple arithmetic), plus an
    order-of-magnitude value from the DOE ICE Calculator, clearly labelled as an estimate.
- **Known limit, said honestly:** hourly demand **by county** is not public. Show the DOM-zone hourly
  data, and present county-level load as something Dominion's AMI data would answer. That point
  belongs in the "first 90 days" slide.
- **Skills:** `xlsx` if the workbook changes.

### Agent B: build

**Ledger:** `interview-prep/ledgers/B_BUILD.md` · **Outputs:** `interview-prep/deliverables/`; chart
code in `interview-prep/work/charts/`

- **B0. Phase 1, needs nothing from the others.**
  - Load `dataviz` before any chart.
  - Build the design system: palette from the conventions, type, chart templates, and a print test
    page.
  - Draft storyline v0 from §2.2 and §3.
  - Write the exact Power BI fix plan from §2.1 and inputs part C.
  - Do a layout test proving that 22 Q&As fit on one sheet, two-sided, at 8.5 pt or larger.
  - **Safety net:** by G1, build a plain v0 deck and v0 brief from the verified §2.2 findings alone.
    A usable pack then exists whatever happens later in the run.
- **B1. Charts.** Reproducible scripts that read D's outputs and write print-resolution SVG and PNG,
  named by slide, each with its caption and source line. Every number on a chart goes into
  `claims.csv`.
- **B2. Deck v1** (`pptx` skill) with speaker notes, plus the print PDF.
- **B3. Question sheet v1** (`pdf`, and `docx` if DOCX), built from R's `top40.md` and the resume
  only.
- **B4. Interview brief v1 (P3).**
- **B5. Power BI upgrade (P4).**
- **B6. After V1 to V4:** revise to v2, run the print proofs, write `START_HERE.md`.
- **Skills:** `dataviz`, `pptx`, `pdf`, `docx`, `xlsx` as needed. `frontend-design` is not needed.
- **Optional:** the toolkit at `C:\Users\oni\Desktop\PROJECTS\renvia-technologies\claude+tools` (see
  its `README.md`) has design references. It is web-focused, and the dataviz skill governs charts.

---

## 6. Ledgers

**Master ledger:** `interview-prep/MASTER_LEDGER.md`. Same shape as the owner's existing ledgers (see
`renvia-technologies/claude+tools/MASTER_LEDGER.md`):
- **Header "Now":** a timestamp and two or three lines on where the run stands.
- **§0 How to use this ledger.** States: ○ not started · ◐ in progress · ✅ done · ⏸ waiting on the
  owner · ✖ dropped.
- **§1** The brief, verbatim (copy §1 of this file).
- **§2** Goal and definition of done (the P1 to P5 checklist).
- **§3** The step table: every task R1–R6, D0–D5, B0–B6, V1–V6, with owner, state, output path and
  notes.
- **§4** Gates and their outcomes.
- **§5** The decision log: every call made, with the reason.
- **§6** Owner questions, each with the default taken.
- **§7** Sources and data acquired, with links to the manifests.
- **§8** The change log, timestamped.

**Agent ledgers** (`interview-prep/ledgers/`): a "Now" line, then the task table, sources consulted,
outputs, issues and gaps, hand-offs to and from the other agents, and a resume-from-here note.

**Cadence:**
- The orchestrator updates the master ledger at every gate, after every agent checkpoint, and at least
  every 45 minutes.
- When context is compacted, the ledgers are the memory. Write them so a fresh session could finish
  the run from them alone.

---

## 7. Sequence, gates and time budget

| Phase | Time (guide) | Who | Work |
|---|---|---|---|
| 0. Setup | 0:00–0:25 | Orchestrator | Read §2; create the ledgers and folders (`research/`, `ledgers/`, `work/`, `deliverables/01_deck` … `04_powerbi`); environment checks; **one batch of owner questions** (below); spawn R, D, B together |
| 1. Foundations | 0:25–2:45 | R, D, B in parallel | R1 first, then R6, R2, R3, R4, R5 · D0, D1, D2, D3 · B0 |
| **G1** | ~2:45 | Orchestrator | Role brief in (or best inference stated); EAGLE-I and sector sales acquired and validated, and the SCC reports attempted; D1 re-verification done. **Lock the storyline** (slide list and the claim on each slide) and the question shortlist |
| 2. Build | 2:45–5:15 | D, B, R | D4, D5 · B1–B5 as D's outputs land · R finishes R2–R5 and drafts the answers' research backing |
| **G2** | ~5:15 | Orchestrator plus reviewers | v1 of P1–P4 exists → V1 number audit, V2 truth audit, V3 mock panel, V4 print proof, V5 freshness |
| 3. Fix and finish | 5:15–7:15 | B, with R and D on call | Fix every V finding; v2; P5; repo docs and local commits |
| **G3** | ~7:15 | Orchestrator plus reviewer | V6 candidate read; the definition-of-done checklist; final ledger update |
| 4. Report | ~7:30 | Orchestrator | Final report to the owner (§11) |

**Phase 0 owner questions.** Ask with AskUserQuestion, in one batch, while the owner is still at the
keyboard. Ask only what the fill-in table left blank or what you could not settle yourself:
- Should Power BI Desktop be installed on this PC?
- What is the posting, if still blank? Make this optional. The interview is on 3 November.
- Only if `CLAUDE.md` says the MCP server is still blocked: does the owner want to add a card to the
  Snowflake trial now? Optional; the run uses `snow sql` either way.

After Phase 0, never block on the owner (§4).

**Deadline.** The interview is Tuesday 3 November. The pack must be finished in this run, on 1
November. If the run starts late, compress Phase 3 rather than running into the night; the candidate
needs 2 November for study and print.

**If early:** spend the spare time in priority order: correctness checks, then the candidate's
understanding (more hard questions and practice answers, within the brief's page limit), then polish. Never lengthen the deck.

**If late:** cut in reverse priority: A6, then the optional P4 copy, then extra Power BI pages. P1,
P2, P3, the apply guide and V1–V4 are never cut.

---

## 8. Verification (nothing is done until it passes)

- **V1. Number audit.**
  - `interview-prep/claims.csv` columns: id, exact text, value, unit, used in (file, slide or line),
    source (table and query, or URL with locator), checked_by, result.
  - A reviewer who did not produce the number recomputes every row from the repo data or opens the
    source.
  - Any mismatch is fixed or the claim is cut. Coverage must be 100%.
- **V2. Truth audit.** A fresh reviewer gets the resume and P2 and P3, and flags every experience
  claim not supported by a resume line. Each one becomes a `[you: …]` or is removed.
- **V3. Mock panel.**
  - A fresh agent gets only the deck PDF, the resume and `role_brief.md`, and plays three
    interviewers:
    - the BI or analytics hiring manager
    - a distribution-reliability engineer
    - an HR / behavioural interviewer
  - It returns the 25 hardest questions and every place the deck overclaims, confuses or is weak.
  - R and B answer the questions in P3 and fix the deck.
- **V4. Print proof.**
  - Render every page of every PDF to PNG (PyMuPDF or `pdftoppm`) and look at each one.
  - Check: no clipping or overflow; minimum font sizes met; legible in grayscale (render a grayscale
    copy); the question sheet fits one sheet.
- **V5. Freshness.** Before finalising, re-check Dominion news from the last 7 days (merger, earnings,
  storms, leadership) and update P3 if anything moved. The 2 November prompt in P5 repeats this check
  the morning before the interview.
- **V6. Candidate read.** A fresh agent reads `START_HERE.md` and P3 as the candidate and tries to
  explain each slide back. It lists anything unclear or undefined, and B fixes those.

Use `superpowers:verification-before-completion` before any "done". Report failures as failures.

---

## 9. Research leads (all unverified: open, read and cite before use; URLs may have moved)

**Data**
- ORNL EAGLE-I county outage dataset: Brelsford et al., *Scientific Data* (2024), "A dataset of
  recorded electricity outages by United States county 2014–2022". The dataset is on figshare; look
  for newer years from ORNL or OSTI.
- EIA-861 and 861M (eia.gov/electricity/data/eia861); EIA-930 (already scripted).
- PJM Data Miner 2 (`hrl_load_metered`) and the PJM Load Forecast Report (January 2026).
- NOAA Storm Events (already local); NHC HURDAT2; DOE OE-417 annual summaries.
- Census cartographic boundary files and ACS 5-year.
- NOAA degree days.
- Virginia SCC docket search: Dominion annual reliability reports, GT Plan, biennial review. Do not
  assume case numbers; find them.
- NCUC for Dominion Energy North Carolina.
- Dominion IR: Q3 2026 release and slides, the 2025 10-K, the Q3 2026 10-Q.
- DOE ICE Calculator.

**Reliability literature**
- IEEE Std 1366-2022.
- Berkeley Lab (LBNL) work on US reliability trends: Larsen, LaCommare, Eto and Sweeney, including
  "Recent trends in power system reliability and implications for evaluating future investments in
  resiliency" (*Energy*, 2016).
- LBNL's updated value-of-service-reliability estimates (Sullivan et al., 2015).
- Do et al., "Spatiotemporal distribution of power outages with climate events and social
  vulnerability in the USA" (*Nature Communications*, 2023).

**Interview and presentation science**
- Schmidt and Hunter (1998), *Psychological Bulletin*.
- Sackett, Zhang, Berry and Lievens (2022), *Journal of Applied Psychology*, on revised selection
  validities: structured interviews rank at the top.
- Levashina, Hartwell, Morgeson and Campion (2014), *Personnel Psychology*, the structured-interview
  review.
- Barrick, Shaffer and DeGrassi (2009), *JAP*, on self-presentation tactics.
- Swider, Barrick, Harris and Stoverink (2011), *JAP*, on initial impressions.
- Huffcutt, Van Iddekinge and Roth (2011), the model of interviewee performance.
- McCarthy and Goffin (2004), on interview anxiety.
- Brooks (2014), *JEP: General*, "Get excited".
- Huang, Yeomans, Brooks, Minson and Gino (2017), *JPSP*, on question-asking and liking.
- Eisend (2006), the meta-analysis of two-sided messages.
- Cleveland and McGill (1984), *JASA*, "Graphical perception".
- Minto, *The Pyramid Principle* (practitioner source, labelled as such).
- **Exclude:** power posing, which failed replication (Ranehill et al., 2015).

**Dominion facts to re-verify:** everything in inputs part A, especially:
- the NextEra terms, the approvals still pending and the expected close
- the Q3 2026 figures and 2026 guidance
- the capital plan
- the data-center pipeline
- the CVOW schedule and cost
- the new large-load rate class
- the political intervention in the SCC case

---

## 10. Owner questions and blockers

| Situation | Default if the owner is silent |
|---|---|
| Power BI Desktop not installed and no answer | Deliver P4 as the apply guide plus files; skip the optional report copy |
| `snow` connection fails | DuckDB only; leave new Snowflake objects as SQL ready to run; note it in START_HERE |
| Snowflake MCP still refused (trial account) | Use `snow sql -c dominion`, or DuckDB. Never wait for the MCP server |
| Posting not found | Target the most likely Dominion BI or data-analyst role per R1, and state the assumption in START_HERE |
| Glassdoor or other sites block fetches | Use other sources and note the gap; never scrape around blocks |
| SCC reliability reports not findable or not parseable | Record the gap; the deck says what they would add |

PushNotification (load it through ToolSearch) may alert the owner when a question is queued or the
run finishes.

---

## 11. Finish

The final message to the owner is short:
- what is in the pack, with full paths to each deliverable
- what to print, with page counts
- what the candidate must fill in (every `[you: …]`)
- the Power BI steps
- what failed or was cut, and why
- the gates' results
- the local commits made (never pushed), and how to push from their own account if they want

**The definition-of-done checklist** (in master ledger §2) must be all ✅ or explicitly ✖ with a
reason:
- [ ] P1 deck: at most 8 main slides; PPTX with notes; print PDF proofed (V4)
- [ ] P2 question sheet: one sheet; 20–24 questions; answers only from the resume, `[you: …]`
  elsewhere (V2)
- [ ] P3 interview brief: at most 12 pages (8 + 4); covers sources, build, what it does and how it helps
  Dominion; every number explained; 25 hard questions answered (V3); delivery section cited;
  print-proofed (V4)
- [ ] P4 Power BI: apply guide, measures, theme and data files; any edited copy verified open, or
  marked unverified
- [ ] P5 START_HERE.md
- [ ] V1 audit: 100% of `claims.csv` rows checked and matching
- [ ] V5 freshness check done on the final day
- [ ] Repo upgrade: sources with manifests, tests T13+ pass, docs updated, local commits only
- [ ] Ledgers complete enough that a fresh session could continue from them
- [ ] Nothing from `interview-prep/` committed, pushed or published; no pay figure in any file
