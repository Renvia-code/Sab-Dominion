# D facts for the V6 rebuild (items a to o)

Agent D, 1 November 2026, about 12:50; updated 12:58 after the three fix commits. No new analysis, no Snowflake. Line
numbers are at the branch tip `c17766a`; the fix commits changed lines in place, so no range cited here moved. Each block gives **Say** (plain words the candidate can use) and **Facts** (every number with
its source: path:line, script and output, or claims id). **[NEW]** = not yet in `interview-prep/claims.csv`. The only
things measured today are the timings in (e) and (o) and the check that the query in (l) returns 130.2 and 133.0.
November work is worded without "I": the trend tests, EAGLE-I and DuckDB parts were added on 1 November.

## (a) "2020: 46 kV lines added"

**Say:** "Dominion's EIA filings carry two counting changes: from 2015, outages are recorded automatically, and from 2020,
lines up to 46 kV are counted. The repo marks both on the charts and does not adjust for them, because the filings say what
changed but not by how much. Counting more lines can only add interruptions, so from 2020 on the change can only push SAIFI
and SAIDI up. 2020 is the year furthest above the storm line, 14.5 minutes. The trend test runs straight across the change,
so if anything it leans toward finding a rise, and it still finds none (p 0.58). The first check I'd run: the fit and the
trend test again with a step from 2020 on."

**Facts:**
- P7, quoted: "Counting rule changes in 2015 (automated outage recording) and 2020 (46 kV lines included) shift Dominion's
  series | Not adjusted in data. Marked on trend charts. 2013 and 2014 excluded from the weather fit" [docs/03_data_quality.md:19].
  Chart note: "2020: lines up to 46 kV included from this year. Both are changes in what is counted" [docs/05_metrics_and_measures.md:65].
- In the filings, Dominion's highest distribution voltage included (`max_kv`) is 35.0 [NEW] in 2013-14, 34.5 [NEW] in
  2015-2019 and 46.0 in every year 2020-2025; `auto_recorded` is false in 2013-14 and true from 2015
  [data/output/fct_reliability.csv:6915-6927; field meaning docs/02_data_dictionary.md:78-79]. So 2020 starts a lasting
  step, not a one-year blip.
- "Can only raise SAIFI and SAIDI": logic, not measured. More lines counted add customer interruptions; the customer count
  does not change. CAIDI can move either way.
- A2 residuals: 2020 is 141.0 against 126.5 from the fit, +14.5. The later years are -5.5, -5.4, -1.1, +3.0 and -0.9
  (2021-2025) [C-S4-05]. So the years after 2020 do not sit consistently above the line. This is not a test, because the
  line was fitted across the change.
- SAIDI trend: +0.64 a year [NEW], 95% CI -1.87 to +3.15 [NEW], p 0.58 [C-S2-13] (`scripts/trend_tests.py` output; docs/05:152).
- The 2015 marker: decision D6 says "the 2015 change to automated outage recording shifts the level", so the weather fit
  starts in 2015 [docs/04_decisions.md:73].
- The robustness check has not been run. The plan is to refit the trend tests and the weather fit with a 0/1 term for 2020
  onward. Dropping 2020 alone does not remove the change, because 2021-2025 are also on the 46 kV basis (above).

## (b) Proxy major event days (D18)

**Say (D18 in two sentences):** "Dominion's own major event days aren't public, so for the EAGLE-I work the repo builds
stand-ins the IEEE 1366 way. A day is a proxy major event day when outage customer-hours across Dominion's 103 counties
exceed e to the power of alpha plus 2.5 beta. Alpha and beta are the mean and standard deviation of the log of daily
customer-hours over the previous five years. The proxies approximate Dominion's ex-MED basis but are not it, so they're
never presented as Dominion's SAIDI."

**Count:** 103 proxy major event days in 2015-2025, between 2 and 18 a year. There were 15 in 2025. Isaias' 4 and 5 August
2020 are two of them.

**If asked "Dominion doesn't publish its MED dates. How do you know which EAGLE-I days were major?":** "I don't know
Dominion's days, and the work doesn't claim to. It uses stand-ins built with the IEEE method on EAGLE-I's county data: 103
days over eleven years. The storm comparison holds with them removed, at 9.9 times instead of 11.9. With Dominion's real
major-event dates, that's the first thing I'd swap in."

**Facts:**
- D18 [docs/04_decisions.md:177-183]. SQL [sql/09_eaglei_outages.sql:285-320]: 2015 uses its own year; 2016-2019 use the
  years available from 2015 (lines 289-290).
- Per year 2015-2025: 2, 15, 3, 18, 5, 6, 12, 14, 3, 10, 15, 103 in all [NEW]. Source: findings.md:1247-1257, query at
  findings.md:1231-1243; the total is also in work/data/logs/sf_vs_duckdb_2026-11-01.md:15. "2 to 18 a year" [NEW] is at
  docs/05_metrics_and_measures.md:120.
- Isaias: 4 August 2020 had 4,184,567 customer-hours [NEW], against a 2020 threshold of 409,595 [NEW] built from 2015-2019.
  4 and 5 August are proxy days; 6 August is not [docs/08_transformations.md:168].
- Test T24: every year 2015-2025 has 1 to 20 proxy days [docs/03_data_quality.md:77].
- Without proxy days the ratio is 9.9 [C-S4-09], 95% interval 8.6 to 11.3 [NEW]. With all days it is 11.9 [C-S4-08]
  [data/output/storm_vs_calm.csv rows 1-2; docs/05:116].

## (c) The trend test

**Say:** "The test fits a straight line through the yearly values against the year, 2015 to 2025: eleven points, ordinary
least squares. It then checks whether the slope differs from zero with a t-test on 9 degrees of freedom, which is the same
as scipy's linregress. None of the four slopes is clear: SAIDI p 0.58, SAIFI 0.54, CAIDI 0.74, weather-adjusted SAIDI
0.67. Eleven points can only pick up a large, steady change. SAIDI's slope could be anywhere from about minus 1.9 to plus
3.2 minutes a year, so 'no clear trend' means the data can't tell, not that nothing changed."

**Facts:**
- Method: OLS against the year, giving the slope, its 95% CI and a two-sided p from a t test on n - 2 = 9 df, "the same
  statistics as scipy.stats.linregress" [scripts/trend_tests.py:3-6; code 81-93; series 101-113]. It reads only the
  committed `data/output/fct_reliability.csv` (19876|VA) and `saidi_weather_adjusted.csv` and uses the standard library
  only [trend_tests.py:8-10].
- Output of `python -I scripts/trend_tests.py`, run today (the same table is at docs/05_metrics_and_measures.md:150-155):

  | Series | Slope a year | 95% CI | p |
  |---|---|---|---|
  | SAIDI ex-MED | +0.64 [NEW] | -1.87 to +3.15 [NEW] | 0.58 [C-S2-13] |
  | SAIFI ex-MED | +0.0043 [NEW] | -0.0111 to +0.0196 [NEW] | 0.54 [C-S2-13] |
  | CAIDI ex-MED | +0.17 [NEW] | -0.94 to +1.28 [NEW] | 0.74 [C-S2-13] |
  | Weather-adjusted SAIDI | +0.34 | -1.41 to +2.08 | 0.67 [C-S4-06] |

- Low power, in the script's own words: "Eleven annual points describe a direction; they cannot establish a trend, and the
  weather-adjusted series is itself model-based, so its interval is too narrow" [trend_tests.py:10-12; docs/05:157].

## (d) The 11.9x interval

**Say:** "The 7.9 to 16.9 range comes from resampling whole days. Draw the days of 2015 to 2025 at random with replacement,
and bring every county-day of each drawn day along. Recompute the storm and calm averages and their ratio, repeat 2,000
times, and keep the middle 95%, from the 2.5th to the 97.5th percentile. It has to be whole days because one storm hits
many counties on the same day, so counties on the same day aren't independent. Resampling single county-days would make
the interval too narrow."

**CI and PI, one line each:**
- "A confidence interval is the range for an average or a fitted line. It shows how sure we are of the 11.9, or of where
  the storm line sits at 791 storm county-days: 133.9 to 156.6."
- "A prediction interval is the range for one new year's value. It adds the year-to-year scatter, so it's wider: 122.3 to
  168.2 minutes for 2025, and the actual 144.4 is inside it."

**Facts:**
- `scripts/storm_vs_calm_ratio.py`:
  - line 23: B = 2000.
  - line 24: fixed seed 20261101 [NEW], so the interval reproduces.
  - lines 43-51: county-days are grouped by day, days are drawn with replacement
    (`rng.integers(0, len(g), size=(B, len(g)))`), and the 2.5th and 97.5th percentiles [NEW] are kept.
  - lines 6-7: "resamples whole days, because one storm hits many counties on the same day; the levels and the ratio use
    the same resamples".
- 11.9 (7.9 to 16.9), from 2,000 resamples [C-S4-08]. The levels are 332.8 (225.6 to 453.4) and 27.9 (23.1 to 33.2)
  [C-S4-17]. There are 6,108 storm county-days [C-S4-10] and 373,851 calm ones [NEW] [docs/05:116].
- PI 122.3 to 168.2 and CI of the line 133.9 to 156.6 [C-S4-19]; actual 144.4 [C-S2-03].

## (e) The real data path

**Slide 6 as a chain (boxes 1 to 5 in a row, box 6 off to the side):**
1. **Public files.** October: EIA-861 / PUDL, NOAA Storm Events, EIA-930. 1 November: EAGLE-I, DOE-417, HURDAT2, CPC
   degree days, Census, EIA-861M. Download scripts put them in `data/raw/` (not in Git); small extracts are committed in
   `data/input/`.
2. **One set of SQL, `sql/01` to `sql/11`.** RAW (text as published) → STG (typed, cleaned) → MART (facts, dimensions,
   views). Written for Snowflake.
3. **A DuckDB copy on a laptop.** The same SQL runs locally and covers everything, including the November tables. It runs
   all 31 tests and builds in 22 seconds.
4. **CSV exports in `data/output/`, committed.** 16 come from the DuckDB copy and 2 from the Excel workbook, with a manifest
   of rows and SHA-256, checked by `check_output_metrics.py`.
5. **The Power BI template.** It imports 18 tables from those 18 CSV files through one `DataFolder` setting and opens with
   no network.
6. *(side box)* **Snowflake.** The October build (`sql/01` to `08`: EIA-861, NOAA storms, EIA-930), where the original
   report was developed in DirectQuery (D13). The November tables reach it only through README step 7 (`sql/09` to `11`).

**Spoken version (two lines):** "The SQL is written for Snowflake, and the October build runs there. The same SQL also runs
in DuckDB, a local copy that builds everything, including the November tables, and runs all 31 tests. The report imports
CSV exports from that copy, so it opens offline, and the new tables go into Snowflake when sql/09 to 11 are run there."

**What a Snowflake account with the October build holds** (the CREATE statements of `sql/01` to `08` at `ec8ecb6`):
- RAW: EIA-861 2025 reliability, PUDL reliability, AMI and sales, EIA-861 service territory, NOAA storm events and the
  zone-county lookup, EIA-930 subregion.
- MART: `DIM_UTILITY`, `FCT_RELIABILITY`, `V_TREND`, `V_GROUP_INDEX`, `V_VA_COOP_PANEL`, `STORM_INDEX`,
  `DOM_LOAD_ANNUAL`, `DOM_TOP50_HOURS`, `DOM_LOAD_PROFILE`, `SAIDI_WEATHER_ADJUSTED`, `V_STORM_VS_SAIDI`.
- Tests T1-T12 run there (they are queries in `sql/04` to `06`). The role `BI_READER` and the user `POWERBI_SVC` come
  from `sql/08`.
- Its `STORM_INDEX` predates D22 (465 and 796) until that statement is run again [docs/03_data_quality.md:40].

**What step 7 adds** [docs/07_governance_and_runbook.md:54-62]:
- `sql/09`: 4 raw tables, 3 staging views and 8 mart tables (`DIM_COUNTY`, `FCT_OUTAGE_COUNTY_HOUR`,
  `FCT_TERRITORY_15MIN`, `FCT_COUNTY_DAY`, `FCT_TERRITORY_DAY`, `FCT_OUTAGE_EVENT`, `FCT_RESTORATION_CURVE`,
  `FCT_COUNTY_YEAR`); tests T13-T24 and T31.
- `sql/10`: `DOM_LOAD_HOUR_MONTH`, `DOM_SEASONAL_PEAK`, `DOM_LOAD_DAILY`, `FCT_SALES_SECTOR`; tests T28-T30.
- `sql/11`: `FCT_EVENT_CONTEXT`; tests T25-T27.
- `STORM_INDEX` (`sql/05`) and `SAIDI_WEATHER_ADJUSTED` (`sql/07`) also have to be run again for D22, or T21 fails
  [docs/03:74].
- Even after step 7, two things still don't come from Snowflake. The 11.9x is a Python bootstrap that reads the DuckDB file
  [scripts/storm_vs_calm_ratio.py:22]. The template still imports CSV files.

**Why a DuckDB copy:**
- Anyone can rerun the whole build and all 31 tests from a clone, with no Snowflake account, credentials or credits
  [README.md:96-103; CHANGES line for bd9505f].
- It is quick: the three light checks take about a second in all, and the full build takes 22 seconds.
- The template's CSV files come from it, so the report opens offline [scripts/export_powerbi_csv.py:1-2; D13].
- Snowflake stays the target: the SQL is in Snowflake's dialect, and the runner translates it
  [scripts/run_local_duckdb_sources.py:47].

**Facts:**
- Sources: docs/01_sources.md:9-30; README.md:15. "Snowflake SQL. The same files run on DuckDB" [sql/01_raw_staging.sql:3].
  Layers: docs/07:25-33.
- CSV origin [scripts/export_powerbi_csv.py:4-6; data/README.md:31; docs/06_powerbi_report.md:12, 135]. The split of 16
  [NEW] and 2 [NEW] was checked today by mapping the template's 18 queries (DataModelSchema) to the two export scripts. The
  2 from the workbook are `load_growth.csv` and `programmes_2025.csv`. The template does not import `storm_vs_calm.csv`, so
  the 11.9x is on no report page.
- Build: 22.1 s and 22.4 s [NEW], a 0.85 to 0.91 GB file (about 0.9 GB [NEW]), 25 tests (T7-T31) PASS. Measured today
  with `run_local_duckdb_sources.py --quiet` in two isolated copies, the second at the new tip `c17766a`.
- 31 tests [C-S7-05A]; 18 tables [C-S5-10]; DirectQuery during development, Import for presentation [C-Q-15; docs/04:131-135].

## (f) Why these 11 peers, and why not Appalachian Power

**Say:** "The twelve are Dominion and eleven large investor-owned utilities in PJM and the Southeast, fixed by EIA utility ID
before any results were computed. It's a judgement, not a formula: no size cut-off is written down. A national set of every
investor-owned utility with over a million customers was considered and turned down, because climate and vegetation differ
too much between regions to compare without a weather model. Appalachian Power is in the data but kept in its own group and
shown separately. Its SAIDI is over 300 minutes and would squash the scale of every chart."

**Facts:** D10 lists the set, the alternative and "Rankings are statements about this set only" [docs/04_decisions.md:107-113].
The EIA IDs are at sql/02_mart.sql:12-20, with Appalachian Power as utility 733 in Virginia at line 15; groups are assigned
by ID (D12, docs/04:125-127). The 300 minutes [NEW] is at docs/04:109. Twelve, Dominion and 11 peers [C-S3-10]; "selected by
EIA ID before results were computed" [C-S3-06].

## (g) "Your peer table's SAIDI isn't SAIFI x CAIDI"

**Say:** "The columns cover different years on purpose. SAIDI is the 2023-25 three-year average, the window Dominion
reports. SAIFI and CAIDI are 2021-25 five-year averages. Each column is the plain mean of the yearly values, so SAIFI times
CAIDI gives a 2021-25 figure, not the 2023-25 SAIDI. A product of averages isn't the average of products anyway. Year by
year the identity holds: test T2 checks SAIDI = SAIFI x CAIDI within 2% on every row."

**Facts:** `saidi_2023_25`, `saifi_2021_25` and `caidi_2021_25` are each an AVG of the annual ex-MED values
[scripts/export_powerbi_csv.py:84-92; data/README.md:31; docs/05:84-86]. T2 [docs/03_data_quality.md:55; C-S7-08]. V6's
example is Duke Carolinas: 1.25 x 139.2 = 174 [NEW], against a SAIDI of 179.0 [C-S3-04].

## (h) One rule for the base years

**Say (the bridge):** "Each base year answers a different question. 2022 to 2025 explains the reported change, because those
are the two years that swap when the average moves from 2022-24 to 2023-25. 2023 to 2025 runs from the start to the end of
the latest three-year window, and that's where the 79% comes from. 2019 to 2025 is the report's long view. From every base,
interruptions per customer rose more than minutes per interruption."

**Facts:**
- Slide 2, 2022 to 2025:
  - SAIDI went from 136.0 to 144.4, and (144.4 - 136.0) / 3 = 2.8 [C-S2-03, C-S2-18].
  - SAIFI rose 10% and CAIDI fell 4% [C-S2-05, C-S2-07].
  - Storm county-days went from 718 to 791, +10% [C-S2-16, C-S2-05].
- Brief p. 2, the 79%, 2023 to 2025:
  - SAIDI +17.1%, SAIFI +13.3%, CAIDI +3.3%, and 79% of the log change came from frequency [C-S2-10, C-S2-11].
  - The query is Q1b, which compares 2019→2023, 2023→2025 and 2015→2025 [sql/03_analysis.sql:14-24; docs/05:64].
- The report screenshot, 2019 to 2025:
  - SAIFI 1.24 to 1.32 (+6%), CAIDI 120.5 to 109.4 (-9%) [C-S5-14; docs/05:61-62]. The "2019 level" line is described at
    docs/06_powerbi_report.md:56-58.
  - If asked why 2019: it is the report's reference year, and the first full year of EIA-930's hourly demand, which starts
    in July 2018 [docs/01_sources.md:18]. So the reliability and load pages share one base.
  - The repo does not write down why 2019 was chosen. That was the candidate's own October choice, so they should check this
    reason against their memory.
- Public deck: slide 2's 723 → 796 is 2022 → 2025 [C-S2-16P]. Slide 4's 465 → 796 is 2024 → 2025, +71% [NEW] by V6's
  arithmetic [C-S4-01P]. Line: "Slide 2 compares the two years that swap in the average; slide 4 compares 2025 with the year
  before, and 2024 had far fewer storm county-days than 2022 (465 against 723)."
- Adopted equivalents: 718 → 791 and 464 → 791 [C-S2-16, C-S4-01]. The brief's Q1 "464 → 791" is 2024 → 2025.

## (i) EAGLE-I years

**Say:** "EAGLE-I's Virginia data starts on 1 November 2014, so the full years are 2015 to 2025. The county-day comparison
uses all of them. The county map averages 2015 to 2024, because 2025's readings are incomplete: almost half of the August
and October readings failed. So 2025 is shown but not averaged."

**Facts:**
- Coverage is 1 Nov 2014 to 31 Dec 2025 [docs/01_sources.md:22; C-S7-12 "Nov 2014-2025"]. Brief p. 7's "2014-2025" and
  deck A4's "Nov 2014-2025" both mean this; A4's is exact.
- The county-day panel covers 2015-2025 [sql/09_eaglei_outages.sql:229-236]. T20 checks 103 counties x 4,018 days [NEW]
  [docs/03_data_quality.md:73]. Slide 4 uses 2015-2025 [storm_vs_calm_ratio.py:1-2; C-S4-10].
- The map averages 2015-2024 [scripts/export_powerbi_csv.py:33-52; docs/05:117].
- The reason is written in D's findings, not in the repo: "2025 is shown but not averaged: EAGLE-I collection failed for 46%
  of August and 45% of October 2025 county readings" [findings.md:1013]. The repo states the fact at P20
  [docs/03_data_quality.md:32]. 46% and 45% are [NEW].

## (j) Isaias: 351,738 against 508,000

**Say:** "351,738 is the most customers out at one moment: one 15-minute reading on 4 August 2020, summed over every utility
in Dominion's 103 counties. 508,000 comes from a DOE-417 report and counts customers affected over the whole event, as the
utility reported them. People restored early and people who lost power later all count as affected, but they're never all
out at once, so the total is bigger than the peak. The DOE-417 report has no utility name. It's matched to Dominion's area by
area, date and size."

**Facts:**
- The peak was 351,738 at 13:30 UTC, and the level held for an hour was 343,492 [docs/08_transformations.md:156; C-S4-21,
  C-A6-01].
- The DOE-417 2020 summary has the report at row 203, area "Virginia:", 508,000 affected [C-S4-24]. The size ratio is 0.69
  [NEW], and the two definitions are given in the same paragraph [docs/08:170].
- The match rule is decision D19 [docs/04_decisions.md:187-193]. DOE-417 has no utility column (P29)
  [docs/03_data_quality.md:41].

## (k) What DOE-417 and HURDAT2 added (one line each)

- **DOE-417:** "The Energy Department's emergency incident and disturbance reports, 2014-2025, 3,702 rows. They give a
  second, independent size for named events, like Isaias' 508,000 customers affected, and are never used to count Dominion's
  major events." [docs/01_sources.md:28; docs/04:187-193; C-S7-13; C-S4-24]
- **HURDAT2:** "The National Hurricane Center's Atlantic storm tracks back to 1851, 55,524 track points. An outage event is
  labelled tropical when a track passes within 400 km of Richmond between a day before the event and its peak; Isaias passed
  59 km away." [docs/01_sources.md:26; docs/05_metrics_and_measures.md:125; docs/08:170; C-S7-13; 400 km and 59 km [NEW]]

## (l) One query to sketch (six lines)

```sql
SELECT year, saidi_ex_med,
       AVG(saidi_ex_med) OVER (ORDER BY year
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS saidi_3yr
FROM RELIABILITY.MART.FCT_RELIABILITY
WHERE utility_key = '19876|VA'
ORDER BY year;
```

**Say:** "Each year's SAIDI is already customer-weighted for Dominion, so the three-year figure is the plain mean of three
yearly values, which is Dominion's own definition. The window is the same as the five-year average in the repo's trend view,
with two preceding rows instead of four."

**Facts:**
- It returns 130.2 for 2024 and 133.0 for 2025. Checked today on the committed `data/output/fct_reliability.csv` with
  in-memory DuckDB: 130.22 and 133.01 [C-S2-02, C-S2-17].
- How it matches the repo:
  - The same window form as V_TREND's five-year average (`ROWS BETWEEN 4 PRECEDING AND CURRENT ROW`) [sql/02_mart.sql:64-65].
  - The same table and filter [sql/03_analysis.sql:16-17].
  - The same arithmetic as scripts/run_local_duckdb.py:101-110 and the DAX at powerbi/measures.dax:49, 53.
  - The rule is D1 [docs/04_decisions.md:17].
- Caveat: the 2013 and 2014 rows average fewer than three years. There is one row per year (T1).

## (m) P18, and what the co-op benchmark is

**Confirmed:**
- Commit `1635a8e` is the candidate's own. It is on `origin/main` with the same author identity as the rest of the October
  build, authored and committed on 27 Oct 2026 at 23:59 (-05:00).
- Message: "Match group-index denominators to reported numerators".
- Files: CHANGELOG.md, docs/02, docs/03, sql/00_look_first.sql and sql/02_mart.sql; +26 / -9 lines
  [`git show --stat 1635a8e`].

**Say (the story):** "For 2025, Prince George Electric filed SAIDI but no SAIFI. If the co-op SAIFI had summed every
member's customers, its 13,341 customers would have sat in the denominator with no interruptions behind them, and the co-op
figure would have read 1.849 instead of 1.887. So I changed V_GROUP_INDEX to count only the customers of utilities that
reported that measure. The co-op index against 2015 doesn't move, at 137.4 either way, because Prince George is missing in
every year."

**What the co-op benchmark is (D11):** "It's a Virginia benchmark: all of the state's electric co-ops combined and
customer-weighted, shown on the report's Weather page. As a check, a fixed panel of the seven co-ops with at least 10,000
customers that filed in every year 2015-2025 is used, dropping each co-op in turn. Both give the same direction. In 2025
the co-ops' SAIFI index is 137, against Dominion's 114 (2015 = 100)."

**Facts:**
- P18 [docs/03_data_quality.md:30; docs/08_transformations.md:77; sql/02_mart.sql:71-84]. 1.849, 1.887 and 13,341
  [C-Q-13]; 137.4 [NEW].
- D11 [docs/04_decisions.md:117-121]. The panel is in sql/03_analysis.sql:39-47, and the leave-one-out check is Q3d at
  sql/03:92-108. Seven co-ops and 10,000 customers are [NEW].
- The indexes 137 and 114 [NEW] are at docs/05_metrics_and_measures.md:77-78; the Weather page is at docs/06:64.

## (n) D22 in one line

"D22: Bedford city merged into Bedford County in 2013, but NOAA's zone lookup still maps zone 34 to both codes, so every
storm there was counted twice. The storm index now counts it once. That is 38 fewer storm county-days over 2013-2025 (2024:
465 to 464; 2025: 796 to 791), with r 0.70 and the 145.3 estimate unchanged."
[docs/04_decisions.md:213-221; docs/03_data_quality.md:40 (P28: 1 extra in 2024, 5 in 2025); sql/05_noaa_storms.sql:120-128;
C-S4-01, C-S4-01P, C-S4-02, C-S4-03; 38 [NEW]]

## (o) What to review before adopting (393 lines), and how long the checks take

| # | Read | Lines | Why |
|---|---|---|---|
| 1 | README.md:11-24 | 14 | "What's new": the first thing a visitor reads. Every number in it should be one you can defend |
| 2 | docs/04_decisions.md:147-203, 213-221 | 57 + 9 | D15-D20 and D22: the rules behind every new number (Dominion counties, NULL readings, events, proxy days, DOE-417 matching, counties off the map, Bedford) |
| 3 | docs/03_data_quality.md:32, 38-40, 66-86 | 1 + 3 + 21 | P20 (failed runs), P26-P28 (Fairfax, the municipal cities, Bedford), and what each of T13-T31 checks |
| 4 | docs/05_metrics_and_measures.md:108-126, 146-157 | 19 + 12 | every EAGLE-I figure with its calculation (including 11.9x), and the trend tests |
| 5 | sql/05_noaa_storms.sql:120-128; sql/07_weather_adjusted_and_profile.sql:38-40 | 9 + 3 | the D22 fold and its new expected values |
| 6 | sql/09_eaglei_outages.sql:1-15, 229-320, 322-334 | 15 + 92 + 13 | the header ("EAGLE-I counts every utility"); the county-day panel and the territory day with proxy days (slide 4); the event and restoration definitions (A6) |
| 7 | scripts/storm_vs_calm_ratio.py:1-72 | 72 | the 11.9x and its whole-day bootstrap |
| 8 | scripts/trend_tests.py:1-16, 81-93, 101-113 | 16 + 13 + 13 | what the trend test does. Skip lines 26-79, which compute the t distribution |
| 9 | scripts/export_powerbi_csv.py:1-11 | 11 | where the template's CSV files come from (the DuckDB copy) |

Skip, and rely on T7-T31 and the checks:
- the rest of sql/09: raw, staging, DIM_COUNTY and the hourly tables (16-228), the event SQL (335-483) and the tests
  (484-546);
- sql/10 and sql/11;
- the download and extract scripts;
- run_local_duckdb_sources.py (the dialect translation);
- the rest of export_powerbi_csv.py.

**Timings** [all NEW]. Wall clock, measured today on the preparing machine (Windows 11, Python 3.12.10), two runs each:

| Check | Time | Ends with |
|---|---|---|
| `run_local_duckdb.py` | 0.94 s and 0.96 s | T1-T6 PASS, "rolling SAIDI averages = 130.2 and 133.0" |
| `check_output_metrics.py` | 0.11 s and 0.12 s | "All committed-output checks passed." |
| `trend_tests.py` | 0.10 s and 0.13 s | the four p-values above |
| `run_local_duckdb_sources.py` (needs README step 4) | 22.1 s and 22.4 s, in isolated copies | 25 tests (T7-T31) PASS, 0.85 to 0.91 GB file |

All nine ranges were re-checked at the new tip `c17766a` and are unchanged. The three fix commits edited lines in place
(docs/04:221, docs/03:86, sql/09:3-5).

The EAGLE-I download (1.66 GB of zips) took about 14 minutes, going by the file times 07:06 to 07:20. Its extraction took
about 3 minutes (07:21 to 07:24).

## Repo docs that contradicted (e): fixed on the branch (coordinator's approval, rule O-40)

Three commits, each by explicit pathspec, none pushed:
- **`506e969`, docs:**
  - docs/07:64 now says the 1 November run of sql/09 to 11 was a test in a separate Snowflake trial account. Any other
    account, the project's own included, gets the November tables only through steps 1 to 3 of the yearly refresh.
  - docs/07:14 and :31: the October report reads the mart as `POWERBI_SVC`; the template imports the CSV files in
    `data/output/`.
  - docs/07:44: the annual refresh rebuilds the DuckDB mirror and exports the CSV files again before the template is
    refreshed.
  - docs/04:221 (D22): "in an account where sql/09 has run, T21 fails until sql/05 and sql/07 are run again".
  - Two more lines of the same kind: docs/07:85, where the Data notes page reads `test_results.csv`, not the workbook's
    Tests sheet; and docs/03:86, which now says "A Snowflake run of sql/09 to 11 uses the same files".
- **`c49aeb1`, scripts:** run_local_duckdb.py's closing message points at `run_local_duckdb_sources.py` for T7-T31.
  This changes the message only; the three light checks print the same results.
- **`c17766a`, comments:**
  - The sql/09 header now counts three staging views, eight mart tables and T31. It lists what the file reads from
    sql/05; it does not read `STG.DOMINION_VA_COUNTIES`.
  - download_eaglei.sh now says 11.6 GB of CSV and 1.66 GB zipped. It said 13.6 GB and about 1.4 GB.

Still in the docs, and outside rule O-40: docs/07:44 and :90 and docs/00_conventions.md:90 tell the reader to record each
load in `CHANGELOG.md`, which `origin/main` deleted on 31 October (c892d8f). All three lines were already on `ec8ecb6`: the
candidate's own October text, left unchanged.
