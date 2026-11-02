# R1 Role brief: the Dominion Energy role

**Agent R · v1 · 2026-11-01 07:25 (machine clock, SLST)** · Light search only, per the owner ("on their
website … light search"). Sources opened are listed in §8 with locators. Pay figures are deliberately
left out of this file.

---

## 1. The most likely posting (confidence: high, about 80%)

| Field | Value | Source |
|---|---|---|
| Title | **Associate Business Intelligence Analyst / Business Intelligence Analyst (Richmond, Hybrid)** | S-R1-02, S-R1-03 |
| Employer, place | Dominion Energy, Richmond, VA | S-R1-02 |
| Team | Supports **Grid Resiliency programs** | S-R1-02 (responsibility 1; summary) |
| Type | Full-time, hybrid **3-2** (three days in the office, two teleworking); travel up to 25% | S-R1-02 |
| Levels | One posting, two levels: **Associate BI Analyst** (0–2 years in BI, data analytics, reporting or related) and **BI Analyst** (3–5 years). "Equivalent combinations of education and directly related experience may be considered" | S-R1-02 |
| Posted | 10 and 11 September 2026 (two copies; aggregator timestamps) | S-R1-02, S-R1-03; corroborated by a third-party tracker logging it 11 Sep 2026 09:36 UTC (S-R1-04) |
| Status today | **Closed.** Both aggregator copies say "job has closed"; the title is not among the 82 openings on careers.dominionenergy.com on 1 Nov (S-R1-01). Dominion's own page for it was not found (closed postings show "Sorry, this position is no longer posted", S-R1-05) | |
| Link | No Dominion URL recoverable. Read copies: `https://jobright.ai/jobs/info/6aa3a1d5c5a856ac7e33a91a` and `https://jobright.ai/jobs/info/6aa3788b83233ca167c8aba2` | |
| Visa | "At this time, Dominion Energy cannot transfer or sponsor a work visa or employment authorization for this position" | S-R1-02 |

**Why this one (evidence, strongest first):**
1. **The tools match the resume summary almost word for word.** The posting asks for "Power BI, SQL, Excel,
   Snowflake, Power Apps, SharePoint"; the resume summary names Power BI, SQL, Excel and Snowflake, and its
   skills list names SharePoint.
2. **The governance language matches too.** The posting asks for "data governance processes, business definitions,
   metadata, and data quality controls", "data validation, reconciliation, and quality assurance" and
   "business glossary concepts"; the resume's Mercury Insurance bullets 3 and 6 and its BI skills line use the
   same terms. *Inference:* the resume was tailored to this posting.
3. **The team fits the project.** The role supports Grid Resiliency programs and prefers "knowledge of electric
   utility operations, reliability metrics, grid modernization programs, or asset management practices". The
   candidate's project is a reliability (SAIDI/SAIFI/CAIDI) analysis of Dominion Energy Virginia.
4. **The timing fits.** Posted 10–11 Sep, interview 3 Nov: about 7–8 weeks, which is a normal cycle (*inference*).
5. The owner said the posting was "on their website". It was then; it is closed now.

**Alternatives considered (less likely):**
- *Business Performance Analyst (Mid/Senior)*, Richmond, job 1435094600: closed. Search snippets (not
  opened, because the page is gone) say it supported Distribution Asset & Program Management, presenting
  Electric Distribution data, with Excel, Power BI and Alteryx. **Second most likely.**
- *Senior Business Performance Analyst / BPA* (Corporate Disbursements), 1442333000: closed; payments, not grid.
- *Business Technology Analyst (I–III)*, 1356210500, and *Assoc Energy Data Analyst*, 1335327300 (metering/AMI):
  closed, older requisitions.
- Live analyst postings on 1 Nov (Financial Analyst DES3, BPA Primavera Scheduler) do not fit the resume's tools.

**Ask the candidate (one line, not a blocker):** `[you: confirm the exact title and requisition number from your
application email, and which level (Associate or BI Analyst) the recruiter mentioned]`. If it turns out to be the
Distribution BPA role, the analysis and storyline below still hold: both roles centre on distribution and
reliability data.

---

## 2. What the role does (the posting's own list, S-R1-02)

1. Design, develop, and maintain **Power BI** dashboards, reports, and analytical tools supporting Grid Resiliency programs
2. Analyze **operational, financial, reliability, and program performance data** to identify trends, risks, and opportunities
3. Support development of **regulatory reporting, annual reports, business plans, and executive presentations**
4. Collaborate with **engineering, operations, finance, regulatory, and IT** teams to define business requirements and analytical solutions
5. Develop and maintain **data governance** processes, business definitions, metadata, and data quality controls
6. Perform data **validation, reconciliation, and quality assurance** activities to ensure reporting accuracy
7. Support **forecasting, budgeting, capital planning**, and performance management activities
8. Create **automated reporting** processes and data pipelines that improve efficiency and reduce manual effort
9. Develop **statistical analyses**, business models, and performance metrics to support program decision-making
10. **Communicate** analytical findings and recommendations to stakeholders at all levels of the organization
11. Support **continuous improvement** initiatives through data-driven evaluation and performance monitoring

*Caveat:* the text is the aggregator's copy of the posting. The bullet wording is the same in both copies and
reads like the original, but Dominion's own page could not be opened to confirm it.

**What "Grid Resiliency programs" means in public terms** (corrected 07:55 from Dominion's own Grid Resiliency
page, S-R2-02; full detail in `dominion_dossier.md` §5):
- Dominion says: "Grid Resiliency and its programs are a part of Dominion Energy's Grid Transformation Plan."
- The page lists four programmes:
  - **Mainfeeder Hardening** (MFH)
  - **Voltage Island Mitigation** (a second transformer at single-transformer substations; 19 locations)
  - **Voltage Optimization** (uses smart-meter data; goal of 1% system-wide energy savings)
  - **Intelligent Grid Devices / FLISR** (fault location, isolation and restoration)
- **The Strategic Underground Program is separate:** "Underground conversions are not within the scope of Grid
  Resiliency programs."
- The page states how MFH success is measured: "an average of 32% reduction in outage minutes" on feeders
  hardened for at least 12 months (as of 30 Nov 2023).
- The page states the selection rule: feeders where at least 500 customers had SAIDI "significantly worse (more
  than 2 minutes)" than the rest.

**This is the BI analyst's world: selecting circuits by outage history, and measuring before and after.**

The June 2026 release (S-R1-11) gives the latest company-reported totals: SUP about 2,900 miles; MFH 8,000+ poles,
350+ miles, −44% average annual outage time.

---

## 3. Tools and the data platform

| Tool | Posting | Resume evidence | Note |
|---|---|---|---|
| Power BI | required | Summary; skills ("Power BI Dashboard Development"); **the Dominion project report** | The job bullets name **Tableau** for professional dashboards (The Life Initiative, Cofoods); Power BI is in the summary, the skills and the project. See gap G3 |
| SQL | required | Mercury bullet 1 (CTEs, window functions, multi-table joins); project SQL `sql/00`–`08` | strong |
| Excel | required | CCL Products bullet 1 (Excel model of discounting order), bullet 3 (five-year projection and capex phasing); skills "Excel (Advanced Modeling)" | strong |
| Snowflake | required | Mercury bullet 1 (Snowflake warehouse pipeline, 20M+ rows); project RAW, STG, MART build | strong; the closest match on the list |
| Power Apps | required | **not on the resume** | gap G2 |
| SharePoint | required | skills line only | gap G7 |

**Dominion's wider data platform (context, from a live posting, S-R1-06):** Dominion is hiring a platform
owner for **Informatica** (Data Catalog) and **Denodo** (data virtualization), "aligned with enterprise data
strategy", with "metadata, catalog, lineage, and data-quality concepts". It is useful vocabulary: a BI analyst
there likely consumes governed views and catalogued data (*inference*). Two live Electric Transmission postings
show analytics teams turning grid data into "consumable business intelligence" (S-R1-07) and building
"data-driven dashboards that help ET use asset data" (S-R1-08).

---

## 4. Level

- The posting has two levels: **Associate (0–2 years)** and **BI Analyst (3–5 years)**.
- The resume summary says 3 years. The dated roles are:
  - Mercury Insurance, Data Analyst: Apr 2026 to now
  - The Life Initiative, intern: Jul–Sep 2025
  - Cofoods, Associate Business Development: Jan 2023–Jul 2024, with forecasting and dashboards
  - Cofoods and CCL finance internships: 2022
  - MS Business Analytics: Jan 2026
- Roles titled data or BI add up to under a year. The 3 years counts analytics work inside business-development
  and finance roles.
- **The candidate sits on the boundary between the levels.**
- **Advice:** don't argue the level in the room. Show BI-Analyst-level work: an end-to-end governed pipeline,
  reconciliation to reported numbers, and a decision log. Know how the 3 years add up, in one sentence, from the
  resume (see G4).
- Only one other Dominion posting read today (Financial Analyst, DES3, S-R1-10) says "A Master's degree will
  count as one year of experience". That rule is **not** stated in the BI posting, so don't assume it applies.

---

## 5. Each requirement mapped to the resume and to the deck

Strength: **S** strong, **P** partial, **G** gap. Resume locators name the role and bullet number, paraphrased
(never quoted). Deck slides refer to the storyline in brief §3; B may renumber.

| # | Posting requirement (S-R1-02) | Resume evidence | Deck / pack evidence | Str. |
|---|---|---|---|---|
| Q1 | 0–2 or 3–5 years in BI, data analytics or reporting | Summary (3 years); Mercury; Life Initiative; Cofoods BD (forecasting model, Tableau dashboards) | n/a | P (boundary, G4) |
| Q2 | Data visualization, dashboard development, data modeling, reporting, business analytics | Life Initiative bullet 1 (board's executive reporting view in Tableau; $690M, 440 investments); Cofoods BD bullet 1 (Tableau dashboards, 8 accounts); Mercury bullet 6 (documented dashboards) | Slide 7 (model and report); the 8-page Power BI report and its upgrade (P4) | S |
| Q3 | Power BI, SQL, Excel, Snowflake, Power Apps, SharePoint | see §3 | Slide 7: Snowflake → Power BI | S, except Power Apps (G2) and SharePoint (G7) |
| Q4 | Enterprise databases, data warehouses, cloud data | Mercury bullet 1 (Snowflake, policy/claims/billing schemas); Life Initiative bullet 2 (AWS EC2, S3); Cofoods finance bullet 2 (SAP exports); skills (AWS, GCP, BigQuery) | Slide 7 (Snowflake RAW/STG/MART) | S |
| Q5 | Data governance, DQ management, metadata, business glossary | Mercury bullets 3 and 6 (validation, reconciliation, QA; metadata and business definitions); skills (Data Governance, DQ Controls, Metadata and Business Glossary Documentation) | Slide 7: tests (32/32 build checks), data dictionary (`docs/02`), decision log (`docs/04`), reconciliation to Dominion's reported 3-year SAIDI | S |
| Q6 | Analytical, problem-solving, critical thinking | Mercury bullet 2 (root-cause analysis of claims-cycle delays; 17% faster settlement); bullet 4 (A/B test, 9% lift); BU optimisation project (LP sensitivity sweep) | Slides 2–3 (decomposing SAIDI into frequency and duration) | S |
| Q7 | Interpret large, complex data; communicate to technical and non-technical audiences | Mercury bullets 1 (20M+ rows) and 5 (servicing reps, operations, IT); CCL bullet 3 (executive presentations); Cofoods BD bullet 3 (buyer conversations) | The deck itself; the "limits" line on each slide | S |
| Q8 | *Preferred:* capital programs, infrastructure, utility operations, engineering orgs or regulated industries | CCL bullet 3 (five-year projection and capex phasing, capital planning); insurance employer (Mercury) | Slide 6 (rank hardening and undergrounding by customer-minutes avoided per dollar) | P: no utility or engineering employment (G1, G6). Whether insurance work counts as "regulated industry" experience is `[you: …]` |
| Q9 | *Preferred:* electric utility operations, reliability metrics, grid modernization, asset management | The Dominion reliability project (public data) | Slides 2–6; the domain primer | P: self-study, not operational (G1) |
| Q10 | Manage multiple priorities; deliver on deadline | Summary; Mercury bullets 2–4 (RCA, evaluation and A/B test in one pilot); Cofoods BD bullet 4 (proposals and quotes across production and logistics) | n/a | S |

**Responsibilities → evidence**

| Resp. | Resume | Deck |
|---|---|---|
| 1 Power BI for Grid Resiliency | Project (Power BI); Tableau dashboards at two employers | The report and P4 upgrade; slides 4 and 6 tie to storm resilience and hardening |
| 2 Reliability and programme performance analysis | Mercury RCA (bullet 2) | Slides 2–4 |
| 3 Regulatory, annual, executive reporting | CCL executive presentations (bullet 3); Life Initiative quarterly and annual board reporting (bullet 1); skills line "Executive and Regulatory Reporting Support" | Slide 2 reconciles to the 3-year SAIDI Dominion reports (130 → 133); regulatory filing work itself is `[you: …]` (G5) |
| 4 Cross-functional requirements | Mercury bullet 5; Cofoods BD bullet 4 | Slide 6 (what I'd ask engineering and operations for) |
| 5 Governance, definitions, metadata, DQ | Mercury bullet 6 | Slide 7 |
| 6 Validation, reconciliation, QA | Mercury bullet 3 | Slide 7; brief appendix "know every number" |
| 7 Forecasting, budgeting, capital planning | Cofoods BD bullet 1 (demand forecast, statsmodels); CCL bullet 3 (capex phasing) | Slide 5 (demand shape: night load, winter peak) |
| 8 Automated reporting and pipelines | Mercury bullet 1; Life Initiative bullet 2 (n8n, about 40 documents a week); Cofoods finance bullets 1–2 (34% shorter quote-to-order cycle; 18% less daily reporting time) | Slide 7 (scripted pipeline, repeatable tests) |
| 9 Statistical analyses and KPIs | Mercury bullet 4 (sample size, significance); BU predictive and clustering projects | Slide 4 (weather fit, shown as exploratory, n = 10) |
| 10 Communicate to all levels | CCL bullet 3; Life Initiative bullet 1 | Whole deck; answer-first titles |
| 11 Continuous improvement via evaluation and monitoring | Mercury bullet 6 (reusable evaluation methodology, performance monitoring) | Slide 6 (first 90 days) |

---

## 6. Gaps, named honestly, with a truthful way to address each

| Gap | What is true | How to address it truthfully |
|---|---|---|
| **G1 No utility operations experience** | All utility knowledge comes from the self-directed public-data project | Say it plainly, then show the learning: "I don't have utility operations experience. To understand your reliability reporting I rebuilt it from public data, and here's what I'd need to learn first: OMS, AMI and the feeder hierarchy." The limits slide makes this credible |
| **G2 Power Apps** | Not on the resume | "I haven't built Power Apps in production." `[you: any exposure?]` Point to adjacent work: n8n automation, Power BI. Offer a concrete plan to learn it in the first weeks. Never claim it |
| **G3 Power BI at work** | Resume job bullets name Tableau; Power BI appears in the summary, skills and the project | Be precise: `[you: where, if anywhere, you have used Power BI professionally]`. The project shows Power BI depth (model, DAX measures, disconnected year slicer); Tableau shows professional dashboard delivery. Never stretch a Tableau bullet into Power BI |
| **G4 Years vs level** | Data- or BI-titled roles add up to under a year; 3 years includes analytics inside business roles | One honest sentence on how the 3 years add up, from the resume. Let the work show the level |
| **G5 Regulatory reporting** | Skills line claims "Executive and Regulatory Reporting Support"; no bullet shows a regulatory filing | `[you: what regulatory reporting you supported, if any]`. Otherwise: "I haven't filed to a regulator; I've reconciled my numbers to what Dominion files, and I know how EIA-861 differs from the SCC report" (R3) |
| **G6 Engineering collaboration** | Bullets show work with operations, IT, servicing, production and logistics, not engineering | Say how you work with domain experts: ask for definitions, check numbers with them, document them. Slide 6 lists what you'd ask engineering and operations for |
| **G7 SharePoint** | Skills line only | `[you: how you've used SharePoint]`; don't elaborate beyond that |
| **G8 Work authorization** | The posting says Dominion cannot sponsor or transfer a work visa for this position | `[you: your answer]`. Know it before the panel; nothing in the pack assumes it |
| **G9 Hybrid 3-2 in Richmond, travel up to 25%** | From the posting | `[you: commute or location answer]` |
| **G10 "Why leave Mercury after seven months?"** | Mercury role started Apr 2026 | Likely question (to R5). `[you: honest reason]`, framed toward Dominion: the grid-resiliency mission and utility analytics. Never criticise the current employer |

---

## 7. What this means for the storyline (for B, ahead of G1)

1. **Keep the reliability spine.** The team supports Grid Resiliency programs and prefers reliability-metrics
   knowledge; the planned arc (SAIDI → frequency vs duration → weather → demand → first 90 days → how built)
   fits the posting closely.
2. **Slide 6 (first 90 days) should speak this team's language:**
   - prioritise hardening and undergrounding by customer-minutes avoided per dollar; this is where
     "capital planning" and "program decision-making" (resp. 7, 9) meet mainfeeder hardening (Grid Resiliency)
     and SUP (a separate programme)
   - **measure programme outcomes properly.** Dominion's public measure is a before/after cut in outage minutes on
     feeders hardened for at least 12 months (−32% as of Nov 2023). A weather-adjusted comparison against similar
     unhardened feeders, as in the candidate's A/B-testing work, makes that number more defensible. Offer it as an
     idea, not a criticism
   - track the programmes' outcomes with governed KPIs (resp. 11)
   - automate the regulatory and annual reporting data flow (resp. 3, 8)

   Keep it "with Dominion's own data"; nothing implies inside knowledge.
3. **Slide 7 (how I built it) should use the posting's nouns:** governance, business definitions, metadata,
   data-quality controls, validation and reconciliation. It is the strongest match on the resume, so show the
   tests and the reconciliation to Dominion's reported 130 → 133.
4. **Slide 8 (close), one line on fit:**
   - candidate wording: "I build governed Snowflake → Power BI reporting, and I've already started learning
     your reliability data"
   - every claim in it traces to resume lines (Mercury bullets 1, 3, 6) and the project
5. **Likely panel of three (*inference*, consistent with V3):**
   - the BI or analytics lead in Grid Resiliency (Power BI, SQL, Snowflake depth)
   - a programme or engineering partner (reliability metrics, SUP and hardening outcomes)
   - HR or a second manager (behavioural, STAR, why Dominion, logistics)
6. **Words to avoid:**
   - "data centres caused" anything
   - anything that implies access to Dominion systems
   - claiming Power Apps, or Power BI at work, beyond the resume

---

## 8. Sources opened (accessed 2026-11-01)

| ID | Source | Locator / quote |
|---|---|---|
| S-R1-01 | Dominion careers search, all jobs: `https://careers.dominionenergy.com/search/?q=&locationsearch=&sortColumn=referencedate&sortDirection=desc` (pages `startrow` 0, 25, 50, 75), 07:02 | "Results 1 – 25 of 82"; newest 31 Oct, oldest 3 Oct 2026; no full-time BI or data-analyst title. Raw: `work/research_raw/careers_all/` |
| S-R1-02 | Jobright copy A of the BI posting: `https://jobright.ai/jobs/info/6aa3a1d5c5a856ac7e33a91a` | Title; "publishTime 2026-09-10 20:05:27"; 11 responsibilities; "Proficiency with Power BI, SQL, Excel, Snowflake, Power Apps, SharePoint, and other reporting and analytics tools"; "Knowledge of electric utility operations, reliability metrics, grid modernization programs, or asset management practices preferred"; "job has closed". Raw: `work/research_raw/jobright_bi/` |
| S-R1-03 | Jobright copy B: `https://jobright.ai/jobs/info/6aa3788b83233ca167c8aba2` | Same title and bullets; "publishTime 2026-09-11 20:47:16"; summary "… dashboards, reports, analytical tools, and data solutions supporting Grid Resiliency programs"; "job has closed" |
| S-R1-04 | Third-party job tracker issue: `https://github.com/VictorJimenez3/fable-job-search/issues/3627` | Title "Dominion Energy — Associate Business Intelligence Analyst/Business Intelligence Analyst (R · 2026-09-11 09:36 UTC"; corroborates the date only |
| S-R1-05 | Closed Dominion postings: `…/job/RICHMOND-Senior-Business-Performance-Analyst-VA-23219/1442333000/`, `…/RICHMOND-Business-Performance-Analyst-(MidSenior)-VA-23219/1435094600/`, `…/RICHMOND-Business-Technology-Analyst-(I-III)-VA-23219/1356210500/`, `…/RICHMOND-Assoc-Energy-Data-Analyst-(Richmond,-Hybrid)-VA-23219/1335327300/` | Each page: "Sorry, this position is no longer posted" |
| S-R1-06 | Live: Senior Software Engineer – Data Platform Owner/Admin, `https://careers.dominionenergy.com/job/RICHMOND-Senior-Software-Engineer-Data-Platform-OwnerAdmin-VA-23219/1444120100/` | "Informatica Data Catalog and Denodo Virtualization Platforms"; "aligned with enterprise data strategy"; "Metadata, catalog, lineage, and data-quality concepts" |
| S-R1-07 | Live: Intern – Power Systems Time-Series Analytics, `…/GLEN-ALLEN-Intern-Power-Systems-Time-Series-Analytics-VA-23060/1444045200/` | Engineering Analytics & Modeling team, Electric Transmission: "provide consumable business intelligence and help steer the future of how we monitor, plan, and manage the grid" |
| S-R1-08 | Live: Intern – ET Asset Analyst (Digital Solutions Team), `…/GLEN-ALLEN-Intern-ET-Asset-Analyst-%28Digital-Solutions-Team%29-VA-23060/1441549200/` | "develops custom applications and data-driven dashboards that help ET use asset data to make informed decisions" |
| S-R1-09 | Live: Assoc. BPA / BPA – Primavera Scheduler, `…/1442663000/` | Generic BPA duties ("Define and develop performance metrics … ensure data integrity as it relates to reporting and analytics"); "hybrid 3-2"; "cannot transfer or sponsor a work visa" |
| S-R1-10 | Live: Assoc. Financial Analyst / Financial Analyst, DES3, `…/1446352300/` | "(Note: A Master's degree will count as one year of experience …)" in that posting only |
| S-R1-11 | Dominion release, 8 Jun 2026, Business Wire 20260608871614, read via the StockTitan repost: `https://www.stocktitan.net/news/D/dominion-energy-prepares-year-round-for-hurricane-season-and-o7ahitzchhvw.html` (the Business Wire original returned 403) | "has buried about 2,900 miles of outage-prone power lines in Virginia, including about 300 miles in the last year"; "replaced more than 8,000 older utility poles and hardened over 350 miles of power lines"; "reduced average annual outage time by 44% for customers in these areas" |

**Seen only in search snippets, not opened (unverified; do not use as fact):**
- an intern posting "Intern – Associate Business Intelligence Analyst (Grid Resiliency)", req. 52958, posted 9 Sep 2026
- the Distribution BPA's team description
- an Indeed copy's street address
- the Grid Resiliency team's programme list (its source page returned 404)

**Not recorded on purpose:** names or profiles of individual Dominion employees (some aggregator pages list
them), and every pay figure.
