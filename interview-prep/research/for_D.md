# For D: data source pointers (R6 scouting)

**Agent R · v1 · 2026-11-01 07:45 (machine clock).** Every URL below was opened or requested from this machine
today. Status codes are what this machine got back. "Blocked" means a bot-protection challenge or a 403: I did
not try to get around any block, and neither should you (brief §4, §10).

## 0. The short version

| # | Source | Reachable by script? | What it gives you | Action |
|---|---|---|---|---|
| 1 | **EAGLE-I county outages, 2014–2025** (figshare v4, 25 Feb 2026) | **No.** figshare's downloader answers with an AWS WAF JavaScript challenge (`x-amzn-waf-action: challenge`); OSTI does not connect; ORNL's own page works but downloads go through Globus (login) | 15-minute customers-out by county, one CSV per year, 78 MB to 1.44 GB each | ~~Owner action or OpenEI fallback~~ **Superseded (orchestrator, 07:40):** D downloads from DOE's public EAGLE-I Aviary endpoint (`eagle-i.doe.gov/api/aviary/download?file=…`); its MD5s match figshare's published MD5s (table in §1) |
| 1b | **Event-correlated outage dataset** (PNNL, built from EAGLE-I + DOE-417, 2014–2023) on OpenEI | **Yes** (HTTP 200, 31.3 MB zip) | Outages aggregated and linked to DOE-417 events; schema in the guideline DOCX | Optional now; no longer needed as a fallback |
| 2 | **EIA-861 2025 final** (released 7 Oct 2026) + Service Territory file | **Yes** | Sector sales and customers; **counties where each utility has distribution equipment** → the Dominion-county rule | Download; **re-check the repo's 2025 SAIDI 144.4 against final data** |
| 3 | **Virginia SCC** dockets (reliability reports, GT Plan) | **No.** scc.virginia.gov returns 403 to scripts and to WebFetch (both networks) | n/a | Record the gap (brief §10 default); use #3b and #3c |
| 3b | SCC Combined Annual Reports to the General Assembly (mirror at rga.lis.virginia.gov) | **Yes** | DEV SAIDI and SAIFI ex-major-events 2020–2024, **as charts only** (no numbers in the text layer) | Citation and context, not data |
| 3c | Dominion-hosted GT Plan documents (azureedge CDN) | **Yes** | Plan narrative, programme descriptions; the Phase III booklet has no SAIDI or SAIFI series | Context; low data value |
| 4 | **DOE-417 annual summaries** (moved to PNNL) | **Yes** | Major disturbances: date, area, customers affected, demand loss. **No utility-name column** | Download 2014–2025 |
| 5 | **PJM 2026 Load Forecast** (report, tables, data) | **Yes** | DOM-zone seasonal peaks, energy, large-load adjustments, 90/10, weather-normalised load | Download the tables XLSX |

---

## 1. EAGLE-I (priority 1)

**Canonical bundle:** figshare article 24237376, **version 4**, published 2026-02-25T18:52:23Z.
- Title: "The Environment for Analysis of Geo-Located Energy Information's Recorded Electricity Outages 2014-2025"
- DOI `10.6084/m9.figshare.24237376.v4`; licence **CC BY 4.0**
- Metadata (works): `https://api.figshare.com/v2/articles/24237376`; raw copy in `work/research_raw/r6_scout/figshare_24237376.json`
- The description says: "UPDATE 4/10/2025: Added 2024 outage data. UPDATE 2/24/2026: Added 2025 outage data."

| File | Bytes | md5 | Download URL (WAF-challenged to scripts) |
|---|---:|---|---|
| eaglei_outages_2014.csv | 78,056,250 | c7bfcf4b7fd26292f8d8801a26e8c52f | https://ndownloader.figshare.com/files/42547717 |
| eaglei_outages_2015.csv | 598,963,737 | 774d837e6a0d4f20aab5c82448538d37 | https://ndownloader.figshare.com/files/42547822 |
| eaglei_outages_2016.csv | 619,779,314 | 8e4e85e81db474a708278aabef1198ec | https://ndownloader.figshare.com/files/42547825 |
| eaglei_outages_2017.csv | 698,796,929 | 4faaeeb3b3e8e2d13d0e9238617ce3ce | https://ndownloader.figshare.com/files/42547828 |
| eaglei_outages_2018.csv | 999,210,542 | 726543e4a392e220108b035ba4c52e43 | https://ndownloader.figshare.com/files/42547879 |
| eaglei_outages_2019.csv | 1,102,778,792 | 0ff77af0106486eb7bdc6c5051bd916a | https://ndownloader.figshare.com/files/42547885 |
| eaglei_outages_2020.csv | 1,170,699,724 | 3b1e76e7ff0445da2b9a2fe4819c0e88 | https://ndownloader.figshare.com/files/42547894 |
| eaglei_outages_2021.csv | 1,141,058,232 | b5a5912be793ca22dddcc73ca2c3379d | https://ndownloader.figshare.com/files/42547891 |
| eaglei_outages_2022.csv | 1,187,596,176 | 0cd04f23ac90ec4ec20ce3a63dcfa25a | https://ndownloader.figshare.com/files/42547897 |
| eaglei_outages_2023.csv | 1,199,752,423 | 4ef3f9290884b4151a43333d28f67369 | https://ndownloader.figshare.com/files/44574907 |
| eaglei_outages_2024.csv | 1,444,846,424 | 13183facf56c196c061a238303c87973 | https://ndownloader.figshare.com/files/53581661 |
| eaglei_outages_2025.csv | 1,402,347,695 | cd2feb1282a42fb048cb6885398bc1cc | https://ndownloader.figshare.com/files/62164877 |
| MCC.csv (modelled customers per county, 2022) | 40,584 | 7e30d47d44cae46b3342cdabf7c84b7f | https://ndownloader.figshare.com/files/42547708 |
| coverage_history.csv (state coverage 2018–2022) | 11,965 | 33ef0c8549a95bcc1ef52b61c2463271 | https://ndownloader.figshare.com/files/42547714 |
| DQI.csv (data quality index by FEMA region, 2018–2022) | 4,338 | fca42544e0c3ee4a191985d1c6c19bc4 | https://ndownloader.figshare.com/files/42547705 |

- **Total:** 11.64 GB. The `Uri_Map.R` and `DQI_processing.R` scripts are also in the bundle; don't execute them.
- **Fields:** the ORNL page for 2025 says "FIPS code, county name, state name, total number of customers without
  power, and a date/timestamp". Search snippets say the 2024 file adds total customers per county; that is
  **unverified**, so check the header.
- **The md5 values are yours to verify against** if the owner downloads in a browser.
- **Filter early:** Virginia FIPS `51xxx`. Stream each CSV through DuckDB and keep only Virginia rows; never load a
  full year into pandas.

**The same data from ORNL (one DOI per year):**
- **2025:** Constellation page reachable (HTTP 200):
  `https://doi.ccs.ornl.gov/dataset/c09fce3f-5faa-54ef-878a-cb0af6851cb6`
  - DOI `10.13139/ORNLNCCS/3012826`; release date 19 Feb 2026
  - Parent DOI `10.13139/ORNLNCCS/1975203`
  - Download is only through the Globus file manager (needs a free Globus login):
    `https://app.globus.org/file-manager?destination_id=57618e0a-2c99-45ff-9694-24141b92fa17&destination_path=%2Fgen101%2Fworld-shared%2Fdoi-data%2FORNLNCCS%2F202602%2F10.13139_ORNLNCCS_3012826%2F`
- **Earlier years (OSTI IDs from search results):**
  - 2014–2022: 1975202
  - 2023: 2297398
  - 2024: 2500278

  OSTI does not connect from this machine or from WebFetch; doi.org redirects to OSTI.

**⚠ Superseded 07:40:** D found that DOE's public EAGLE-I Aviary download works without a challenge, and the
MD5s match figshare's. The options below are kept for the record only; **no owner action is needed**.

**Owner-action options (superseded):**
- (a) The owner downloads the Virginia-relevant years in a browser from the figshare page
  `https://figshare.com/articles/dataset/The_Environment_for_Analysis_of_Geo-Located_Energy_Information_s_Recorded_Electricity_Outages_2014-2022/24237376`
  and saves them to `data/raw/eaglei/`.
  - Minimum useful set: 2018–2025 plus `MCC.csv` and `coverage_history.csv`, about 9.6 GB.
  - Lean set: 2023–2025, about 4.1 GB.
- (b) A Globus transfer with the owner's login.
- (c) The OpenEI fallback below.

**1b. OpenEI fallback (reachable now):** "Event-correlated Outage Dataset in America".
- Publisher: PNNL; licence CC BY 4.0; data.gov metadata updated 27 Jul 2026.
- Landing page: `https://data.openei.org/submissions/6458`
- Data: `https://data.openei.org/files/6458/Outage_Dataset_R1.zip` (HTTP 200, 31,260,449 bytes, last modified
  24 Apr 2025). The page labels it "Outage Dataset v2".
- Schema: `https://data.openei.org/files/6458/Guideline_OEDI_Updated.docx`
- Per data.gov, it holds "aggregated outage data, merged outage data, and event-correlated data"; the EAGLE-I part
  spans 2014–2023, linked to DOE-417 events "based on geographic location as well as the start and end times of
  events".
- **Not opened yet:** check whether it keeps county × time series (good enough for A2 restoration curves) or only
  event summaries.

**Paper to cite:** Brelsford et al., *Scientific Data* (2024), "A dataset of recorded electricity outages by United
States county 2014–2022", `https://www.nature.com/articles/s41597-024-03095-5`. I (R3) will verify the coverage
figures quoted in search snippets ("3,044 of 3,226 counties by 2022", "80% to 90% of customers") before anyone
uses them.

---

## 2. EIA-861 (priority 2), including the county rule

- **Page:** `https://www.eia.gov/electricity/data/eia861/` (HTTP 200). It says: "Release date: October 7, 2026
  (final data)"; "Next release: August 2027 (early release data)".
- **2025 final zip:** `https://www.eia.gov/electricity/data/eia861/zip/f8612025.zip`. Older years: `zip/f8612024.zip`
  etc. The page also lists `zip/f8612023er.zip` (2023 early release).
- **Service Territory files** (in each annual zip), in EIA's words: "names of counties and states in which the
  utility has equipment to distribute electricity to ultimate customers. Time frame: 2001 to present."
  - Filter utility number **19876** (Virginia Electric & Power Co), state VA. That gives a defensible,
    documented **Dominion-county rule** for `DIM_COUNTY`.
  - Compare it with `data/reference/zone_county_correlation.csv`.
  - It does not give Dominion's *share* of customers in a county. Counties shared with other utilities, such as
    electric cooperatives, stay a stated limit.
- **⚠ Reconcile:** the repo's 2025 figures (SAIDI 144.4, SAIFI 1.320) may come from an earlier release via PUDL.
  Re-read the 2025 Reliability file in the final zip and confirm or correct them (feeds D1 and V1).
- **EIA-861M** (monthly) is listed separately at `https://www.eia.gov/electricity/data/eia861m/`. I did not open
  it today.

---

## 3. Virginia SCC: reliability reporting and the GT Plan (priority 3)

**Blocked:**
- `https://www.scc.virginia.gov/docketsearch/...` and `…/media/...` return **HTTP 403** to curl (browser user
  agent) and to WebFetch. Docket PDFs cannot be fetched by script.
- Brief §10 default applies: record the gap; the deck says what the reports would add (cause codes, regional
  indices, worst circuits).

**What the SCC itself says about the reports** (RD916, read today, PDF p. 11–13, printed p. 5–7):
- "At the electric distribution level, the Commission monitors service reliability through a number of measures,
  including the **Annual Reliability and Tree Trimming Report** required from each of Virginia's three
  investor-owned electric utilities"
- "The charts below show the reliability indices of the Commonwealth's two largest IOUs, DEV and APCo, over the past
  five years, based on data submitted by the companies in their annual reliability reports"
- Footnote 13: "the calculations of SAIFI and SAIDI indices omit the impacts of major weather-related events such
  as hurricanes and derechos"
- p. 7, on comparisons: "it is difficult to compare the performance of one utility to another because these
  metrics do not account for differences in utility infrastructure (e.g., underground vs. overhead), customer
  density, tree exposure, topography …"

Use that last quote for the peer caveat.

**Not found (gaps):**
- The Virginia rule or order that requires the Annual Reliability and Tree Trimming Report. It is not in
  20VAC5-312, which covers retail access. R3 continues the search.
- Dominion's filed reports themselves: not seen in any search result. *Inference:* they may be filed with the
  Division of Public Utility Regulation outside a public docket.

**3b. Reachable SCC reports (General Assembly mirror):**

| Report | URL | Holds |
|---|---|---|
| RD916 (1 Dec 2025): Combined Report incl. Annual Report on Grid Modernization, Reliability and Integration of Renewables | `https://rga.lis.virginia.gov/Published/2025/RD916/PDF` (HTTP 200, 483,451 B, 45 pp.; saved `work/research_raw/scc_combined/rd916_2025.pdf`) | DEV and APCo SAIDI and SAIFI ex-major-events, **2020–2024, charts only**; GT Plan status |
| RD861 (1 Dec 2024) | `https://rga.lis.virginia.gov/Published/2024/RD861/PDF` (not downloaded; landing page `…/2024/RD861`) | Same series, earlier window; a search snippet quotes a footnote "data provided by Dominion as of June 30, 2024" (unverified) |
| RD764 (2022) | `https://rga.lis.virginia.gov/Published/2022/RD764/PDF` (not downloaded) | Earlier window |

*Optional:* the chart values might be recoverable from the PDF's vector drawing commands. Only attempt it if cheap,
and label the result "read from SCC chart", never as a table value.

**GT Plan dockets** (case numbers from Dominion's own milestones page, read today; the SCC pages are blocked):
- Plan (2019): **PUR-2019-00154**
- Phase II: **PUR-2021-00127** (final order 7 Jan 2022)
- Phase III: **PUR-2023-00051**
- Phase IIIB update: **PUR-2025-00051**. A secondary summary (search snippet, not opened) says the final order of
  23 Sep 2025 capped mainfeeder hardening and OMS capital and "directed Dominion to provide updates on reliability
  performance as part of its next grid transformation plan filing". R2 will try to confirm.

**3c. Dominion-hosted GT documents (reachable, HTTP 200):**
- Milestones page: `https://www.dominionenergy.com/about/delivering-energy/electric-projects/energy-grid-transformation/significant-milestones`
- CDN files (append nothing; the `?rev=` query strings on the page are optional):
  - `https://cdn-dominionenergy-prd-001.azureedge.net/-/media/content/about/delivering-energy/electric-projects/grid-trans-milestones/gt-plan-phase-3-booklet-update.pdf`
    - 25,055,877 B, 40 pp.; saved `work/research_raw/dom_gt_docs/`
    - Reliability content is qualitative: a glossary (SAIDI, SAIFI, CAIDI, CMI) and p. 21 "Improve reliability on
      the worst performing mainfeeders"
    - **No metric series**
  - `…/gt-plan-phase-2.pdf`, `…/gt-plan-phase-2-factsheet.pdf`, `…/gt-plan-phase-2-final-order.pdf`
  - `…/gtp-scc-filing-vol-1-2019.pdf`, `…/gtp-scc-filing-vol-2-2019.pdf` (2019 petition and testimony)

---

## 4. DOE-417 (formerly OE-417) annual summaries (priority 4)

- **The old host is gone:** `www.oe.netl.doe.gov` no longer resolves (DNS failure here and via WebFetch).
- **New host (PNNL), confirmed:**
  - pattern `https://doe417.pnnl.gov/summaries/{YYYY}_Annual_Summary.xls` for **2000–2023**, `.xlsx` for
    **2024–2025**; a `.pdf` exists for every year
  - checked: 2014, 2018 and 2023 `.xls` (HTTP 200, `application/vnd.ms-excel`); 2024 and 2025 `.xlsx` (HTTP 200)
  - **2026 is not posted**: the URL returns the app's HTML shell
- **Format:**
  - **2023 and earlier (.xls, 11 columns):** Event Month, Date Event Began, Time Event Began, Date of Restoration,
    Time of Restoration, Area Affected, **NERC Region**, Alert Criteria, Event Type, Demand Loss (MW), Number of
    Customers Affected
  - **2024–2025 (.xlsx, 10 columns):** the same without NERC Region; 4 title rows, header on row 5. The 2025 file
    says "Total Records: 426 | Generated: 10/7/2026"
  - `xlrd` is in the `.venv`. The 2023 file triggers a harmless "file size not 512 + multiple" warning
- **⚠ No utility or respondent column in any year.**
  - Match events to Dominion by Area Affected (state or county names), date and size, and state the rule.
  - Rows with Area Affected "Virginia; West Virginia" (three in early 2025: 69,098, 51,000 and 51,273 customers)
    are probably **not Dominion**. *Inference:* Dominion Energy Virginia has no West Virginia retail customers;
    Appalachian Power serves both states. Exclude them or flag them.
- **ORNL's portal copy** (`https://openenergyhub.ornl.gov/explore/dataset/oe-417-annual-summaries/`) is **2023 only**
  ("for data discovery purposes"). Use the PNNL files instead.
- **Sample** downloaded for inspection only (2016, 2023, 2025) to `work/research_raw/doe417_peek/`. Re-download into
  `data/raw/doe417/` with a manifest.

---

## 5. PJM 2026 Load Forecast (priority 7, but cheap)

**Index page:** `https://www.pjm.com/planning/resource-adequacy-planning/load-forecast-dev-process` (HTTP 200).

**Files (all under `https://www.pjm.com`):**
- Report PDF (posted 14 Jan 2026): `/-/media/DotCom/library/reports-notices/load-forecast/2026-load-report.pdf` (HTTP 200)
- **Tables XLSX:** `/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx`
  - HTTP 200, 371,564 B, 34 sheets; peek copy in `work/research_raw/pjm_peek/`
- Data XLSX: `/-/media/DotCom/library/reports-notices/load-forecast/2026-load-report-data.xlsx`
- Supplement: `/-/media/DotCom/planning/res-adeq/load-forecast/load-forecast-supplement-2026.pdf`
- Mid-year update (informational): `/-/media/DotCom/planning/res-adeq/load-forecast/2026-mid-year-update-informational-only.xlsx`
- Accuracy: `…/2026-load-forecast-accuracy-report.pdf`, `…/2026-accuracy-report.xlsx`
- Seasonal peaks: `…/summer-2026-peaks-and-5cps.pdf`, `…/summer-2025-peaks-and-5cps.pdf`

**Tables with a `DOM` row (checked):**
- **B1** Summer Peak Load (MW) and Growth Rates. Columns "Metered 2025", "Unrestricted 2025", then 2026…
- **B2** Winter Peak Load (MW). The header row was not caught by my quick parse; read it yourself
- **E1** Annual Net Energy (GWh)
- **B9** Adjustments Above Embedded to Summer Peak Load (MW), "table updated 2/6/2026". This is where large-load and
  data-center adjustments sit
- **F3** Weather Normalized Load (MW)
- Also useful: **D1/D2** (90/10 extreme-weather peaks) and **B10** (coincident peak)

**Rules for using it:**
- Read the column headers before quoting any value; my peek was not a verification.
- Every PJM number used goes to `claims.csv` with the sheet and cell.
- The DOM zone is not Dominion's retail territory (same caveat as EIA-930).

---

## 6. Other sources noticed (lower priority)

- **ODIN real-time county outages** (ORNL), `https://openenergyhub.ornl.gov/explore/dataset/odin-real-time-outages-county/`.
  It has cause fields but is **live only** (131 records today), not history. Not useful for trends; a good
  "what utilities could share" talking point.
- **Census CO-EST2024-POP** county population: `https://www.census.gov/data/tables/time-series/demo/popest/2020s-counties-total.html`
  (linked from the PNNL dataset). This is for per-capita normalisation if ACS is slow.
- **usenergydata.org**: EIA-861-derived reliability charts. Secondary; don't cite it as a source.

## 7. Hand-back

Tell me (R) if you need:
- a source that failed here, retried later
- a specific claim checked (for example the EAGLE-I coverage figures)
- the Phase IIIB order wording, once anyone can open it

I'll log what you take in your ledger's hand-off section.
