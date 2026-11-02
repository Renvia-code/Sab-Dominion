# Company box, glossary and Dominion checks (V6 inputs from R)

*Agent R · 2026-11-01 13:01. For B to place. START_HERE belongs to the orchestrator.*

*How to read this file:*
- *The print text is the bulleted and quoted lines. The bracketed tags are sources, kept for checking; B can drop
  them in print.*
- *Tag key:*
  - *`R-nnn`: `research/claims_register.csv`*
  - *`C-…`: `interview-prep/claims.csv`*
  - *`docs/…` and `README`: this repository*
  - *`brief p.5`: `work/brief/build_brief_v3.py` line 407*
- ***NEW** marks a source that needed a new claims row. Every NEW row is now in the register as R-107 to R-131,
  with URL, access date and quote; §8 lists them.*
- *Web pages accessed 2026-11-01. US spelling. No pay figures. Pronouns for the candidate are they/them; the print
  text says "you".*

---

## 1. Company box (half a US Letter page at 10.5 pt; measured: 2,090 characters, about 26 lines at 100–105 per line)

**Dominion Energy at a glance (November 1, 2026)**

- Richmond-based regulated utility (NYSE: D): electricity for 3.6M in VA, NC, SC; gas for 500k in SC. [R-042]
- **Customers:** 2.68M = Virginia in EIA-861, the project's base (EIA files by state) · 2.8M = Dominion Energy
  Virginia incl. NC · 3.6M = all three states. [C-S7-07; docs/03 P17; R-107 NEW; R-042]
- **If a panelist says 2.8M:** "That includes North Carolina; my Virginia-only base is 2.68M." [R-107 NEW]
- **Leaders:** Robert Blue, chair, president and CEO · Ed Baine, executive vice president of utility operations
  and president, Dominion Energy Virginia. [R-064; R-108 NEW; R-109 NEW]
- **Q3 2026 (Oct 30):** operating EPS $1.28 vs $1.06; 2026 seen in the top half of $3.45–$3.69. [R-043; R-044]
- **Merger:** all-stock with NextEra; shareholders approved Sep 3; close expected in the second half of 2027.
  Pending: Virginia SCC case PUR-2026-00112 (rebuttal due Nov 2, hearings Nov 17, order by Jan 11), FERC
  EC26-131, NRC, NC, SC.
  [R-046; R-104; R-105; R-095; R-096; R-093; R-094; R-048]
- **FPL**, NextEra's Florida utility, is one of the 12 peers and has the lowest ex-MED SAIFI; after the merger, a
  sister company (§7). [R-110 NEW; R-124 NEW; docs/04 D10]
- **CVOW** (Coastal Virginia Offshore Wind, 2.6 GW): about 85% built; budget $11.65B; done by end-2027.
  [R-111 NEW; R-062; R-061]
- **Data centers:** 28% of Virginia Power's 2025 sales; 54+ GW in contracting stages, 12+ GW contracted.
  [R-112 NEW; R-054]
- **Rates:** base rates +$566M (2026) and +$210M (2027); typical bill +$11.24 a month (2026); allowed return on
  equity 9.8%, which the SCC can move by up to 50 basis points on factors including reliability.
  [R-057; R-058; R-059]
- **Grid Resiliency programs** (Grid Transformation Plan): [R-035]
  - **MFH, Mainfeeder Hardening:** rebuilds the three-phase main line from a substation; picks circuits with
    above-average outages (5 years) and 500+ customers at SAIDI 2+ min worse than the rest. [R-114 NEW; R-037]
  - **VIM, Voltage Island Mitigation:** adds a second transformer (or reroutes) at single-transformer
    substations, so every customer can be restored. 19 sites. [R-114 NEW; R-038]
  - **VO, Voltage Optimization:** tunes voltage with smart-meter readings. The goal is 1% energy savings.
    [R-039]
  - **FLISR, Fault Location, Isolation and Service Restoration:** isolates a fault and restores the rest.
    [R-115 NEW]
  - **SUP, Strategic Underground Program** (separate): about 2,900 miles of outage-prone lines buried by June
    2026, of about 4,000. Due 2029. [R-012, re-read on the primary page (the R-013 URL); R-034; R-035]

## 2. Glossary (≤ half a page; 22 terms; measured: 2,220 characters, 25–28 lines at 100–105 per line)

- **MED / ex-MED:** a day above the 2.5β threshold. Ex-MED drops those days, to show everyday performance.
  [R-070; R-020]
- **IEEE 1366:** standard for SAIFI, SAIDI, CAIDI and MEDs. 10 of 12 peers use it; Dominion files "Other".
  [R-074; R-072; R-125 NEW]
- **2.5β:** T_MED = e^(α+2.5β); α, β = mean and standard deviation of ln(daily SAIDI), prior five years.
  [R-070]
- **Storm county-day:** "a day with a NOAA wind, winter or tropical storm report in one of the 103 Virginia
  counties Dominion serves". [brief p.5]
- **EAGLE-I:** DOE's 15-minute county outage record, built at Oak Ridge National Laboratory (ORNL).
  [R-129 NEW; R-016; R-079]
- **PUDL:** Public Utility Data Liberation, Catalyst Cooperative's cleaned EIA data (2013–24 history).
  [R-116 NEW; docs/01 S2]
- **NCEI:** NOAA's National Centers for Environmental Information. It holds the Storm Events Database.
  [R-117 NEW; docs/01 S5]
- **HURDAT2:** the National Hurricane Center's (NHC) Atlantic storm tracks, used to tag tropical events.
  [R-118 NEW; docs/05]
- **CPC:** NOAA's Climate Prediction Center: daily heating/cooling degree days vs 65°F, population-weighted.
  [R-119 NEW]
- **PJM:** the regional transmission organization for VA, 12 other states and DC (grid and power market). [R-080]
- **DOM zone:** Dominion's PJM zone = its transmission and distribution area (NC, co-ops too): wider than retail.
  [R-113 NEW; R-112 NEW; co-ops: docs/07, inference]
- **CEMIn:** Customers Experiencing Multiple Interruptions: % of customers with n+ sustained interruptions.
  [R-130 NEW; R-074]
- **MAIFI:** Momentary Average Interruption Frequency Index: SAIFI for interruptions of 5 min or less.
  [R-130 NEW; R-074; R-072]
- **OMS:** outage management system, which detects customer outages. Dominion is installing a new one.
  [R-072; R-060]
- **AMI:** smart meters (hourly reads, sent daily). **Last gasp:** a meter's alert as it loses power.
  [R-073; R-120 NEW]
- **FLISR:** Fault Location, Isolation and Service Restoration. It isolates a fault and restores the rest.
  [R-115 NEW]
- **SCC:** Virginia State Corporation Commission: rates, reliability reports, the merger case.
  [R-057; R-019; R-096]
- **FERC:** Federal Energy Regulatory Commission; must approve the merger (docket EC26-131). [R-048; R-093]
- **NRC:** Nuclear Regulatory Commission; must approve the license transfers for four nuclear plants. [R-094]
- **DOE-417:** DOE's Electric Emergency Incident and Disturbance Report, by area, with no utility column.
  [R-121 NEW; R-023]
- **CI vs PI:** a confidence interval brackets the average (2025: 133.9–156.6); a prediction interval brackets one
  new year, so it is wider (122.3–168.2). [R-122 NEW; C-S4-19]
- **DuckDB:** in-process SQL database; the local mirror reruns everything without Snowflake, feeds Power BI.
  [R-123 NEW; README; docs/06]

**Spare lines, if there is room:**
- EAGLE-I = Environment for Analysis of Geo-Located Energy Information. [R-129 NEW]
- NHC tracks run 1851–2025, every six hours. [R-118 NEW]
- The four nuclear plants are Surry, North Anna, V.C. Summer and Millstone. [R-094]
- "Resampling whole days" means a bootstrap that redraws whole days 2,000 times. [C-S4-08]
- DOE-417 lists Isaias with 508,000 Virginia customers affected. [C-S4-24]

## 3. "What do you know about Dominion?" (about 45 seconds: 109 words before your line)

> "Dominion is a Richmond-based regulated utility, with about 3.6 million electric customers in Virginia and the
> Carolinas, about 2.7 million of them in Virginia. Three things stand out. First, demand: data centers are more
> than a quarter of Dominion Energy Virginia's sales, and the pipeline keeps growing. Second, reliability now has
> money attached. The Virginia State Corporation Commission, the SCC, can move Dominion's allowed return up or
> down by as much as half a point, on factors that include reliability. And Dominion's three-year SAIDI excluding
> major events rose from 130 to 133 minutes, mostly from storms, it says. Third, the proposed combination with
> NextEra; SCC hearings start November 17." [you: one sentence on why this team, in your own words]

Sources:
- 3.6 million: R-042.
- 2.7 million: C-S7-07.
- More than a quarter: R-112 (28%).
- The pipeline: R-054 and R-099.
- Half a point: R-059.
- 130 → 133: R-028.
- November 17: R-095.

## 4. Manual check on Monday, November 2 (10 minutes, by hand, in a normal browser)

**The rule.** An item has **moved** if there is something new and dated after November 1 on the merger,
leadership, a major outage, rates or CVOW, or anything that changes a line in the box. These do **not** count as
moving:
- the companies' rebuttal filing in the SCC case (it is due November 2 and is expected)
- routine community or customer-program releases

| # | Open this | Look for | Baseline on Nov 1 | Source |
|---|---|---|---|---|
| 1 | Dominion newsroom: https://news.dominionenergy.com/ (2 min) | The newest releases at the top | The newest is "Dominion Energy Announces Third-Quarter 2026 Results" (Oct 30); then the dividend (Oct 27) | R-127 NEW (opened) |
| 2 | Investor releases: https://investors.dominionenergy.com/ (1 min). Its "News" link leads to the newsroom in row 1. Also check Events & Presentations: https://investors.dominionenergy.com/events-and-presentations/default.aspx | Any new investor event or presentation after the Oct 30 call | The Q3 call on Oct 30 is the latest known event | R-127 NEW (opened; the event list loads in a browser) |
| 3 | NextEra newsroom: https://newsroom.nexteraenergy.com/news-releases (1.5 min) | Anything after Oct 23 that names Dominion, Virginia or the merger | Newest Oct 23 (an Iowa grid project); NextEra's Q3 results Oct 21 | R-128 NEW (opened) |
| 4 | Virginia SCC docket search: https://www.scc.virginia.gov/docketsearch. If that address fails, go to scc.virginia.gov and choose Docket Search. Enter case PUR-2026-00112 (2.5 min) | The newest filings and any order | Rebuttal due Nov 2; hearings from Nov 17; order by Jan 11, 2027. Staff (Oct 19): deny as proposed unless conditions are accepted | R-095; R-050; R-096. **Not opened**: the site refuses scripted requests |
| 5 | Federal Register: https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=EC26-131. For the NRC, search "North Anna" on the same site (1.5 min) | Any EC26-131 notice newer than Oct 21; any NRC order on the license transfer | Oct 21 notice of the companies' Oct 15 deficiency response; the NRC notice of Aug 27 | R-093; R-094. **Not opened** today: the site sends scripts to a bot check, but it works in a browser |
| 6 | FERC eLibrary: https://elibrary.ferc.gov/eLibrary/search. Type EC26-131 under Docket Number and sort by date (1.5 min) | An order, or a new deficiency letter | Deficiency letter Sep 23; response Oct 15; no order | R-093 (opened; a JavaScript app that works in a browser) |

**If something moved:** write one line per item on the update sheet in pen (date · what · where), and open with
"As of this morning…". **If nothing moved:** "As of this morning nothing has changed since the Q3 call; the SCC
hearing starts November 17."

**Prompt for an assistant (one paragraph, self-contained):**

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
> most one page, named 2026-11-02_dominion_update, in the same folder as this pack, in US spelling. If nothing
> moved, write nothing. Do not edit any other file.

Sources for the facts in the prompt:
- (1) R-127.
- (2) R-128.
- (3) R-095 and R-050.
- (4) R-093.
- (5) R-094.
- (6) R-095.

## 5. Salary (one instruction, no figure)

Before Tuesday, research a range for this role in the Richmond area from public pay data, such as the U.S. Bureau
of Labor Statistics' Occupational Employment and Wage Statistics tables (the latest estimates are for May 2025).
Write it here in pen: [you: your range]. If pay comes up, let the recruiter name the band first ("What range is
budgeted for this role?"). If you are asked to go first, give the range you wrote, as a range.
[R-131 NEW: pointer only; no figures were read or recorded]

## 6. Storm duty and travel (sheet 18)

- **The posting says:** "Hybrid 3-2 work schedule (three days in the office, two days of teleworking)" and "Travel
  Up to 25%". [R-009]
- **Storm duty:** the posting says nothing about it, and neither do the nine other Dominion postings read on
  November 1. The company's June 2026 hurricane release says only: "Dominion Energy employees conduct regular
  training and drilling exercises to prepare for hurricane season." [R-126 NEW]
- **So ask the recruiter what storm-season duty means for this role.**

## 7. "FPL's SAIFI is about half yours. Given the merger, what do you make of that?"

> "On frequency it's right. Counting all events, which doesn't depend on either company's major-event rule, FPL
> averaged 0.77 interruptions per customer a year over 2021–25, against Dominion's 1.53. But FPL's outages run
> longer, and over 2023–25 its all-events minutes, about 276, were above Dominion's 223."
>
> "Florida and Virginia differ in weather, grid and reporting method: FPL files IEEE 1366, Dominion its own. So
> I'd use FPL as a source of good questions, like what drives its low frequency, not as a verdict. What it means
> for the merger I'd leave to the people deciding it."

Sources:
- R-124 NEW, R-computed for D to confirm. FPL against Dominion:
  - all-events SAIFI 2021–25: 0.766 against 1.531, a ratio of 0.50
  - all-events SAIDI 2023–25: 275.7 against 223.0
  - all-events CAIDI 2021–25: 406.0, the highest of the 12, against 181.3
- Dominion's values match C-S3-08.
- The standards are from R-125 NEW.

**If pressed:**
- Excluding major events, FPL is the lowest of the 12 on both SAIFI (0.49, 2021–25) and SAIDI (47 minutes,
  2023–25). The two companies use different major-event rules, though. [R-124 NEW; R-125 NEW]
- NextEra itself says FPL's reliability is "more than 60% better than the national average". Quote it as their
  claim. [R-110 NEW]

## 8. NEW sources (register rows R-107 to R-131, all accessed 2026-11-01)

| Row | Source opened | Used for |
|---|---|---|
| R-107 | Dominion 2025 Annual Report, PDF p.19 and p.65 (q4cdn link as in R-028) | 2.8M; 2,809k accounts |
| R-108 | Dominion newsroom, joint release of Sep 14, 2026 (URL in the register) | Blue's title; Baine leads Virginia |
| R-109 | Dominion IR release of Jun 8, 2026 (the R-013 URL) | Baine's title |
| R-110 | Joint release of Sep 14, 2026 | FPL is NextEra's utility; NextEra's FPL claims |
| R-111, R-112, R-113 | Annual Report PDF p.3, p.20, p.5 | CVOW name; 28% data centers; the DOM zone |
| R-114 | Dominion Grid Resiliency page (the R-035 URL) | Mainfeeder and voltage-island definitions |
| R-115 | Dominion GT Plan Phase III booklet, PDF p.22 and p.19 (the R-027 URL) | FLISR expansion |
| R-116 | https://catalyst.coop/pudl/ | PUDL |
| R-117 | https://www.ncei.noaa.gov/ (and /stormevents/, heading only) | NCEI |
| R-118 | https://www.nhc.noaa.gov/data/ | NHC, HURDAT2 |
| R-119 | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/degree_days/ and ddayexp.shtml | CPC degree days |
| R-120 | DOE, *O&M Savings from AMI: Initial Results* (Dec 2012), p.6: https://www.energy.gov/sites/default/files/2017/08/f35/AMI_OM_report_final_12-13-20121.pdf | Last gasp |
| R-121 | https://doe417.pnnl.gov/ (landing page) | DOE-417 name |
| R-122 | NIST/SEMATECH e-Handbook 4.5.1.2: https://www.itl.nist.gov/div898/handbook/pmd/section5/pmd512.htm | CI vs PI |
| R-123 | https://duckdb.org/ | DuckDB |
| R-124, R-125 | The repo's `data/output/` files (R-computed; D to confirm) | FPL comparison; 10 of 12 on IEEE 1366 |
| R-126 | The R-013 release; the saved posting text | Storm duty |
| R-127, R-128 | Dominion newsroom and investor site; NextEra newsroom | Manual-check baselines |
| R-129 | Brelsford et al. 2024, doi:10.1038/s41597-024-03095-5; ORNL Constellation (the R-016 URL) | EAGLE-I expansion; DOE CESER |
| R-130 | EIA-861 instructions p.10; IEEE PES Boston slides p.48 and p.50 | CEMIn, MAIFI |
| R-131 | https://www.bls.gov/oes/current/oes_40060.htm (served the OEWS tables index) | Salary pointer |

**Tried and not used:**
- WAVY (a storm-role quote) returned 403.
- The Federal Register search sent the script to a bot check.
- The NCEI Storm Events pages load their text by JavaScript.
- A Penn State STAT 501 page failed on its certificate.

None of these was worked around.

## 9. Notes for B

1. **The assistant prompt in §4 is for screen use only.** Keep it out of the printed pack, which never says how it
   was made. The orchestrator decides whether it replaces the batch 7 block in `research/morning_prompt_2nov.md`,
   which has machine paths.
2. **FLISR: use one expansion.** The GT booklet says "fault location, isolation, and service restoration" and is
   used here. Dominion's web page drops "Service". Use the booklet's form everywhere, tied to the acronym (V6 §2a).
3. **CEMIn: one spelling.** Sheet 16 says "CEMI".
4. **2.8M.** The brief and the scorecard should say which count they use (docs/03 P17); the box gives all three.
5. **docs/06 says "Half the peers use a different reporting method".** The data say 2 of 12 (R-125; for_B.md §4
   already flags it).
6. **SUP mileage.** The box uses the June 2026 figure (about 2,900 miles). The one-pager's ~2,700 is the
   end-2025 figure (R-032). Both are company figures.
7. **Fit.** Measured with `work/scripts/r_final_fit_check.py` after stripping the tags (sizes in the §1 and §2
   headings). Half a Letter page at 10.5 pt holds about 26 lines. If the real layout runs over, drop the source
   tags and the spare lines first. Do not shorten the storm county-day line: it is the brief's wording, verbatim.
8. **Resume check.** `r5b_quote_check.py` finds 0 six-word sequences shared with the resume.
