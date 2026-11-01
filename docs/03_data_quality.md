# 03. Data quality

> **At a glance:** Quick read: these checks prevent misleading conclusions caused by duplicate utilities, inconsistent formatting, mis-mapped counties and implausible demand readings. A successful check does not prove the utility filing itself was correct.

Profiling findings on the raw files, the handling of each in SQL and the tests T1 to T12 that run after each load.

## Profiling findings

Found by profiling RAW (`sql/00_look_first.sql`) or by a test on the first load. Each is handled in SQL so that it applies to every subsequent load.

| # | Source | Finding | Handling | Location |
|---|---|---|---|---|
| P1 | EIA-861 2025 | Three header rows; blanks written as "." | File format `SKIP_HEADER = 3`, `NULL_IF = ('.')` | `01`, `FF_EIA_CSV` |
| P2 | EIA-861 2025 | Numbers carry thousands separators ("2,675,735") | `TRY_TO_NUMBER(REPLACE(x, ',', ''))` on every numeric column | `01`, `STG.RELIABILITY_2025` |
| P3 | EIA-861 2025 | IEEE 1366 and Other-standard metrics in two side-by-side column blocks; each utility fills one | Unpivot with `UNION ALL`; `standard` column records the block | `01` |
| P4 | EIA-861 2025 | Eight utilities report ex-MED values without all-events values | Retained: filter is `saidi_all IS NOT NULL OR saidi_ex_med IS NOT NULL` | `01` |
| P5 | PUDL | A row exists for both standards for every utility, including empty rows | Rows with no SAIDI under either standard are dropped | `01`, `STG.RELIABILITY_HIST` |
| P6 | PUDL and EIA union | Seven utilities filed under both standards in 2021 | De-duplicated with `QUALIFY ROW_NUMBER() ... = 1`; the IEEE row is kept so customers are counted once | `01`, `STG.RELIABILITY` |
| P7 | EIA-861 | Counting rule changes in 2015 (automated outage recording) and 2020 (46 kV lines included) shift Dominion's series | Not adjusted in data. Marked on trend charts. 2013 and 2014 excluded from the weather fit | charts, `07` |
| P8 | EIA-861 | Four utility-years where all-events SAIDI is lower than ex-MED SAIDI | Retained in `FCT_RELIABILITY` so the load matches EIA. The utilities concerned are in the `Other` peer group and outside the peer sets. T3 reports the count on every run | `04`, T3 |
| P9 | NOAA | Zone events (`cz_type = 'Z'`) reference a forecast zone, not a county | Mapped to counties through the NWS zone-county correlation file | `05`, `STG.NOAA_VA_EVENTS` |
| P10 | NOAA | 140 zone events reference zones renumbered after the lookup was published | Second pass matches `UPPER(cz_name)` to the county name. T9 confirms none remain unmapped | `05`, T9 |
| P11 | NOAA vs EIA | County name spellings differ between sources ("Alexandria City" vs "City of Alexandria"); James City and Charles City are county names | Both spellings are tried; `MIN(fips)` per EIA county. T7 confirms all 104 counties resolve | `05`, T7 |
| P12 | NOAA | One storm can produce many event rows in one county on one day | The index counts county-days, not events | `05`, `STORM_INDEX` |
| P13 | EIA-930 | Two hours on 18 October 2021 report 1.5 billion and 1.0 billion MW for a zone that peaks near 25,000 MW | Values above 60,000 MW set to NULL in staging; the reported value is retained in `demand_mw_reported`. T10 lists the rows | `06`, T10 |
| P14 | EIA-930 | 2,020 hours have no demand value (1,729 in 2018) | Left NULL. `hours_missing` recorded per year in `DOM_LOAD_ANNUAL`. T12 checks each full year has at least 8,700 reported hours | `06`, T12 |
| P15 | EIA-930 | Local time has 23-hour and 25-hour days at clock changes | Hourly logic keyed on `utc_ts`. T11 confirms no duplicate hour | `06`, T11 |
| P16 | EIA-930 | `EIA930_SUBREGION_2018_Jan_Jun.csv` is served as an HTML error page (subregion reporting starts July 2018) | Not loaded. The download script removes it | `scripts/download_eia930.sh` |
| P17 | EIA-861 vs annual report | EIA customers for Dominion VA are 2,675,735 and the annual report states 2,809k | Not an error. The report figure includes North Carolina. Stated on the scorecard | report |
| P18 | EIA-861 | Prince George Electric filed SAIDI but no SAIFI for 2025. A group denominator summing all members' customers would include its 13,341 customers and understate the co-op SAIFI (1.849 instead of 1.887) | `V_GROUP_INDEX` denominators sum only the customers of utilities that reported the numerator. The co-op index (each year relative to 2015) is unchanged to one decimal (137.4) | `02`, `V_GROUP_INDEX` |
| P19 | EIA-930 vs company reports | Dominion's earnings decks report DOM zone peaks of 22,189 MW (24 Dec 2022), 21,993 MW (28 Jul 2023) and 23,127 MW (16 Jul 2024). EIA-930 hourly maxima on the same days are 22,415, 22,050 and 23,220 MW, within 1.1% | Confirms EIA-930 as a proxy for the zone load. The difference is hourly-integrated EIA data against PJM's reported peak | `DOM_LOAD_ANNUAL`, `data/reference/dominion_ir_series.csv` |
| P20 | EAGLE-I | A blank customer count is a failed collection run, not zero customers out. Failures cluster in late 2025: 46% of August and 45% of October 2025 county readings are blank | Kept NULL, never zero (D16). Customer-hours skip them, so 2025 EAGLE-I totals are undercounted; the county-day panel uses complete county-days only (D20) | `09`, `STG.EAGLEI_VA_15MIN.failed_run`, Q12 |
| P21 | EAGLE-I | Rows with zero customers out appear only from 2022. Before that, a county with no outage has no row | Customer-hours are unaffected. Reading counts and failed-run shares are not comparable across 2022 | `09`, Q12 |
| P22 | EAGLE-I | The 2023 file names the count column `sum` instead of `customers_out` | The extract keeps the file as published; the raw load reads the sixth column by position | `scripts/extract_eaglei_va.py`, `09` |
| P23 | EAGLE-I | The modelled customer counts (`MCC.csv`) hold impossible values for small cities (Buena Vista 1, Waynesboro 6, Lexington 16), and the 2024 file's `total_customers` double-counts (Virginia sums to 4.9 million) | Customer basis = MCC unless missing or below half the county's ACS housing units, then housing units (7 counties). Virginia basis 4,002,493; the 103 Dominion counties 3,462,949 (D15) | `09`, `STG.VA_COUNTY_CUSTOMERS`, T17 |
| P24 | EAGLE-I | Readings above twice a county's customers, for example Fairfax city at up to 136,046 out on 2-4 March 2018 against 12,701 customers | Set to NULL in staging; the reported value is kept in `customers_out_reported`. 22 county-days, 484 readings (D16) | `09`, T19 |
| P25 | EAGLE-I | One-reading collection drops and short spikes in the territory total: on 18 June 2016 at 04:15 UTC it falls from 95,972 to 2,434 and returns to 183,062 the next reading; on 30 July 2019 Hampton Roads shows 159,742 out for 45 minutes | Restoration times count a level only when the series stays below it for 3 hours; events are ranked by the level held for one hour (`peak_sustained_1h`) (D17) | `09`, `FCT_OUTAGE_EVENT` |
| P26 | EAGLE-I | Fairfax city (51600) carries implausible readings for long periods in 2018-2020 (231 readings above half its customers in 2019; about 2,000 to 4,500 rows a year before and after, 24,000 to 30,000 in those years) | Left off the county map and out of the county-day panel (D20). It stays in the territory total, where any misplaced Fairfax County outages still belong | `09`, `county_outage_map.csv`, `scripts/storm_vs_calm_ratio.py` |
| P27 | EAGLE-I | Manassas, Harrisonburg and Bristol (municipal utilities) have almost no readings: fewer than 1,000 in 2015-2024 | Left off the county map and out of the panel (D20) | `09`, `county_outage_map.csv` |
| P28 | EIA-861 vs NOAA | EIA's 2025 Service Territory still lists "Bedford City" for Dominion, merged into Bedford County in 2013, and NOAA's zone lookup maps zone 34 to both 51019 and 51515. Every zone-34 storm therefore added two county-days to `STORM_INDEX` for one area: 38 extra county-days over 2013-2025 (1 in 2024, 5 in 2025), every one also a Bedford County day | **Fixed by D22**: `STORM_INDEX` folds 51515 into 51019. Storm county-days 2024 and 2025 are now 464 and 791 (were 465 and 796); the 2015-2024 correlation (0.70), the 2025 prediction (145.3) and the weather-adjusted 2025 value (133.1) are unchanged at the precision reported; the fit is 104.3 + 0.0518 x county-days (was 104.4 + 0.0514). Snowflake's MART still holds the pre-D22 index until the `STORM_INDEX` (sql/05) and `SAIDI_WEATHER_ADJUSTED` (sql/07) statements are re-run there | `05`, `STORM_INDEX`, T21 |
| P29 | DOE-417 | No utility or respondent column in any year; Area Affected is free text ("Virginia:", "HanoverCounty, Virginia", "Virginia; WestVirginia") | Matched to Dominion by area, date and size (D19) | `11`, `STG.DOE417_EVENTS` |
| P30 | DOE-417 | The 2023 file has 32 August rows with a blank begin date; at least one repeats a July event | Kept with a NULL begin date; they cannot be matched | `scripts/extract_doe417.py`, `11` |
| P31 | DOE-417 vs EAGLE-I | A report for 26 March 2024 (Hanover County, 50,000 customers, demand loss "160,000" MW) has no EAGLE-I event: the 103-county total stayed below 8,400 from 25 to 27 March | Left unmatched; one of the two sources is wrong and public data cannot say which | `11`, Q17 |
| P32 | EIA-861 | `data/input/Reliability_2025_States.csv` shows 16 co-op customer counts rounded to whole customers; the final 2025 file holds fractions (for example 56,980.6) | No effect on any Dominion figure; every Dominion value equals the final file | checked against `f8612025.zip` (S1) |
| P33 | EIA-930 | The July-December 2026 file has rows for 30 October 2026 but no demand values; the last value is the hour ending midnight on 29 October 2026 (04:00 UTC 30 October). The committed `data/output/dom_annual.csv` stops at 21 October | Every 2026 figure is stated "to 29 Oct 2026" (D21); the 2026 peaks are the same under both cut-offs | `06`, `10` |
| P34 | EIA-930 | `DOM_TOP50_HOURS` ranks with `ROW_NUMBER()` over `demand_mw`, and some hours tie (two hours at 23,134 MW in June 2025), so tied hours can swap rank numbers between builds. There is no tie at rank 50 in either ranking (24,120 vs 24,096 MW; 22,953 vs 22,941 MW), so which hours are in the top 50, and every count quoted from it, is stable | Not changed (sql/06 is the original build). A tie-breaker (`utc_ts`) in the `ORDER BY` would fix the numbering. The committed `dom_top50_hours.csv` is kept as exported on 1 November 2026 | `06` |

## Tests

Run after every load. A result other than the expected one stops the refresh until explained.

| Test | File | Check | Expected | Result, this build | If it fails |
|---|---|---|---|---|---|
| T1 | 04 | No duplicate utility-state-year in `FCT_RELIABILITY` | 0 rows | 0 | De-duplication in `STG.RELIABILITY` failed, or a new file overlaps years already loaded |
| T2 | 04 | SAIDI = SAIFI x CAIDI within 2% for every row | 0 rows | 0 | A column is mis-mapped in staging |
| T3 | 04 | All-events SAIDI not lower than ex-MED SAIDI | 4 rows (known source anomalies, P8) | 4 | A different count means new anomalous rows. Investigate before using peer figures |
| T4 | 04 | Dominion VA 2025 equals EIA's published values (306.7, 144.4, 2,675,735) | 0 rows | 0 | Wrong file or wrong column mapping. Stop the refresh |
| T5 | 04 | Row count and customer total by year | 13 rows, 940 to 1,175 reporting units per year, customers increasing each year. The step from 1,175 (2019) to 941 (2020) reflects a change in which filers appear in the reliability table | 13 | A year with materially fewer rows indicates a parse failure |
| T6 | 04 | No raw numeric value failed `TRY_TO_NUMBER` after separator removal | 0 rows | 0 | A new formatting variant in the source. Extend the `REPLACE` |
| T7 | 05 | Every Dominion county in the service territory resolves to a FIPS code | 0 rows | 0 | A county spelling changed. Extend the name mapping |
| T8 | 05 | The latest NOAA file covers a full year | 1 row, month 12 | 202512 | The NOAA file is partial. Wait, or state the cut-off on the chart |
| T9 | 05 | No zone event left without a county after both passes | 0 rows | 0 | Further zone renumbering. Refresh the zone lookup |
| T10 | 06 | Hours with reported demand above 60,000 MW | 2 rows (18 October 2021) | 2 | Additional anomalous rows. Review the dates |
| T11 | 06 | No UTC hour appears twice for the DOM zone | 0 rows | 0 | A file was loaded twice. Truncate and reload |
| T12 | 06 | Each full year 2019 to 2025 has at least 8,700 reported hours | 0 rows | 0 | A six-month file is missing or truncated |
| T13 | 09 | EAGLE-I raw row count equals the Virginia rows the extract wrote | 0 rows (11,608,442 loaded) | 0 | A file was loaded twice or truncated |
| T14 | 09 | Every EAGLE-I row has a Virginia county code and a parsable timestamp | 0 rows | 0 | A format change in the source |
| T15 | 09 | One row per county per 15-minute slot after staging | 0 rows | 0 | De-duplication in staging failed |
| T16 | 09 | Every EAGLE-I county code is a Census county or city | 0 rows | 0 | A FIPS code changed |
| T17 | 09 | 133 counties, 103 Dominion counties (EIA's 104 names less Bedford city), 30 to 40 Dominion-only | 1 row, 0 problems | 0 (33 Dominion-only) | The service territory file changed |
| T18 | 09 | Every Virginia utility-county in the service territory resolves to a FIPS code | 0 rows | 0 | A county spelling changed |
| T19 | 09 | County-days with readings above twice the customer basis (set to NULL) | 22 rows | 22 | New impossible readings: review before use |
| T20 | 09 | County-day panel complete: 103 counties x 4,018 days | 1 row, 0 problems | 0 | A day or county is missing |
| T21 | 09 | Panel storm days equal `STORM_INDEX` year by year (both count Bedford city as Bedford County, D22) | 0 rows | 0 | The two storm definitions have drifted. In Snowflake it fails until `STORM_INDEX` is rebuilt with D22 |
| T22 | 09 | Hourly customer-hours add up to the 15-minute total | 0 rows | 0 | Aggregation error |
| T23 | 09 | Restoration curves bounded 0 to 1 and start at the peak | 0 rows | 0 | Background or peak computed wrongly |
| T24 | 09 | Every year 2015-2025 has 1 to 20 proxy major event days | 0 rows | 0 | The 2.5 beta threshold misbehaves |
| T31 | 09 | County-year table: 103 x 11 rows, customer-hours equal the panel's | 1 row, 0 problems | 0 | Aggregation error |
| T25 | 11 | HURDAT2 track points parse; 200 to 400 storms since 2014 | 1 row, 0 problems | 0 | Format change in HURDAT2 |
| T26 | 11 | DOE-417: 3,702 rows; 2024 and 2025 equal the files' "Total Records" (622, 426) | 1 row, 0 problems | 0 | A summary file changed or failed to parse |
| T27 | 11 | One context row per territory outage event | 1 row, 0 problems | 0 | A join multiplied rows |
| T28 | 10 | Every month July 2018 to October 2026 has all 24 hours in the hour x month table | 0 rows | 0 | A six-month file is missing |
| T29 | 10 | Commercial sales 2025 = 60,088,202 + 4,532,591 MWh (EIA-861 2025) | 0 rows | 0 | Wrong file or class mapping |
| T30 | 10 | Virginia degree days: one HDD and one CDD per day from 2018, none negative | 1 row, 0 problems | 0 | A CPC file is missing |

T13 to T31 run in the DuckDB mirror (`scripts/run_local_duckdb_sources.py`, which reads the expected result from each test's comment). The Snowflake run of sql/09 to 11 follows the same files.

### Form of the tests

Each test is a `SELECT` that returns the expected row count when the data is sound. Any user with read access can run them. In Snowflake they can be scheduled as a `TASK` that writes results to a table the report reads (see `docs/07_governance_and_runbook.md`). The same checks translate directly to dbt tests.

### Not covered by the tests

- The accuracy of a utility's own filing. T2 checks internal consistency, not the reported customer count. EIA does not audit filings.
- Whether Dominion's own major-event rule excludes more or fewer days than IEEE 1366 would. Not testable from public data. Stated as a limitation on each peer chart.
- Outage causes, circuit-level detail and repeat-outage customers. Not available in any public source.
