# 04. Decisions

> **At a glance:** Quick read: I chose methods that support fairer comparisons, kept 2025 out of the weather model's 2015-2024 training set, and documented the remaining limitations. This is exploratory analysis, not causal attribution.

Design decisions, each with context, the decision, alternatives considered and consequences.

---

### D1. Aggregation uses additive numerators

**Context.** SAIDI, SAIFI and CAIDI are ratios published per utility. Comparisons across utilities or years require an aggregate.

**Decision.** `FCT_RELIABILITY` stores `cust_minutes_ex_med = saidi_ex_med x customers` and `cust_interruptions_ex_med = saifi_ex_med x customers`. Aggregates sum these and divide by summed customers. In DAX: `DIVIDE(SUM(minutes), SUM(customers))`.

**Alternatives.** `AVG(saidi)` across utilities. Rejected: it weights every utility equally regardless of size. For the Virginia co-ops in 2025 the simple average SAIFI is 2.44 and the customer-weighted figure is 1.89.

**Consequence.** Multi-year averages are averages of annual customer-weighted values (`AVERAGEX(VALUES(YEAR), [SAIDI ex MED])`), which matches Dominion's definition of its three-year figure and reproduces 133.0.

---

### D2. Ex-MED is the headline measure, with all-events shown alongside

**Context.** EIA publishes both. Dominion reports the ex-MED figure to the SCC and in its annual report.

**Decision.** Trends and comparisons use ex-MED. All-events appears on the scorecard and in the stacked bar chart so that the storm share is visible.

**Alternatives.** All-events as the headline. Rejected: the series is dominated by major storms and does not describe day-to-day performance.

**Consequence.** Dominion files under its own major-event rule (EIA "Other" standard). Most large peers file under IEEE 1366. The two are not reconciled by any public source. Each peer chart carries this caveat and the peer table shows the method per utility.

---

### D3. RAW tables are all VARCHAR

**Context.** Source files contain "." for blanks, thousands separators, mixed-case booleans and multiple header rows.

**Decision.** `COPY INTO` tables in which every column is `VARCHAR`. Typing is done in STG views with `TRY_*` functions; a value that fails typing becomes NULL and T6 reports it.

**Alternatives.** Typed RAW tables with `ON_ERROR = CONTINUE`. Rejected: rows are dropped without a record.

**Consequence.** RAW is an exact copy of the source. Typing rules can be changed without reloading.

---

### D4. Weather exposure is measured in county-days

**Context.** NOAA records one row per event. A single storm can produce many rows in one county on one day.

**Decision.** `STORM_INDEX` counts distinct (county, date) pairs with at least one line-risk event. 791 county-days in 2025 (D22).

**Alternatives.** Event counts (over-weight well-reported storms). Damage estimates (sparse and inconsistent). Heating and cooling degree days (temperature only and already quoted in the annual report).

**Consequence.** The index correlates 0.70 with SAIDI ex-MED over 2015 to 2024 and 0.41 with SAIFI. It measures exposure, not damage.

---

### D5. Event types classified as line risk

**Decision.** Wind: Thunderstorm Wind, High Wind, Strong Wind, Tornado. Winter: Ice Storm, Winter Storm, Heavy Snow, Blizzard, Sleet. Tropical: Hurricane, Hurricane (Typhoon), Tropical Storm, Tropical Depression. All other types (flood, heat, hail, lightning, drought) are classified `other` and excluded.

**Alternatives.** Include Lightning and Hail. Rejected: lightning reporting is inconsistent across years and hail rarely causes line outages. Include Flash Flood. Rejected: flood damage affects substations and appears in major event days, which ex-MED already excludes.

**Consequence.** The classification is one `CASE` expression in `STG.NOAA_VA_EVENTS`.

---

### D6. Weather fit window is 2015 to 2024

**Context.** `SAIDI_WEATHER_ADJUSTED` requires a fitted relationship between storm county-days and SAIDI.

**Decision.** Fit on 2015 to 2024 and predict 2025 out of sample.

**Alternatives.** Include 2013 and 2014. Rejected: the 2015 change to automated outage recording shifts the level. Include 2025. Rejected: 2025 is the year under test.

**Consequence.** Ten observations. Intercept 104.3, slope 0.052 minutes per county-day (D22). The fit is a check on one year, not a forecasting model.

---

### D7. Hourly demand above 60,000 MW is treated as a reporting error

**Context.** Two hours in October 2021 report over one billion MW for the DOM zone.

**Decision.** Values above 60,000 MW are set to NULL in `STG.EIA930_DOM_HOURLY`. The DOM zone has not exceeded 26,000 MW; PJM as a whole peaks near 150,000 MW. Reported values are retained in `demand_mw_reported`.

**Alternatives.** Replace with the mean of neighbouring hours. Rejected: fabricates data. Drop the rows. Rejected: removes the record of the anomaly.

---

### D8. Hourly data is keyed on UTC

**Decision.** `utc_ts` is the key for all hourly operations. Local time is retained for display.

**Reason.** Local time has 23-hour and 25-hour days at clock changes. T11 confirms no duplicate hours.

---

### D9. Top-50 hours are ranked at two reference dates

**Context.** Dominion's annual report states that 38 of the 50 highest peak loads in DOM Zone history occurred after 1 January 2025. The statement has a reference date.

**Decision.** `DOM_TOP50_HOURS` ranks hours as of 31 December 2025 (comparable with the report) and as of the load date. The report card uses the first.

**Consequence.** 47 of 50 as of end 2025 and 46 of 50 as of October 2026. The EIA record starts in July 2018, so earlier years present in Dominion's own ranking are absent, which accounts for 47 exceeding 38.

---

### D10. Peer set

**Decision.** Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before results were computed. Southeast: Duke Carolinas, Duke Progress, Georgia Power, Alabama Power, Dominion SC. Mid-Atlantic (PJM): BGE, Pepco, PECO, PPL. Florida: FPL, Duke Energy Florida. Plus Dominion VA, so the twelve are Dominion and 11 peers. Appalachian Power (VA) is held in a separate group and shown separately because its SAIDI exceeds 300 minutes and would compress the scale of every chart.

**Alternatives.** All investor-owned utilities with over one million customers nationally. Rejected: differences in climate and vegetation across regions would require a weather model outside the scope of this project.

**Consequence.** Rankings are statements about this set only. The peer table lists every member and its reporting method.

---

### D11. Two co-op benchmarks

**Decision.** `V_GROUP_INDEX` uses all Virginia cooperatives, customer-weighted; this is the series on the report. `V_VA_COOP_PANEL` is a balanced panel of the seven co-ops with at least 10,000 customers that filed in every year 2015 to 2025, used in `03_analysis.sql` Q3 to check that the result is not driven by entry and exit. Q3d repeats the comparison leaving each co-op out in turn.

**Consequence.** Both benchmarks give the same direction. The report states "all Virginia co-ops combined".

---

### D12. Peer groups are assigned by EIA utility ID

**Reason.** Utility names change (Virginia Electric & Power Co trades as Dominion Energy Virginia); IDs do not. `DIM_UTILITY.peer_group` is a `CASE` on `(utility_id, state)`.

---

### D13. DirectQuery during development, Import for presentation

**Decision.** The report was developed in DirectQuery against Snowflake. For presentation it is switched to Import so that it opens without a network connection or a running warehouse. The DirectQuery copy is retained separately.

**Consequence.** The Import file carries a snapshot date on its title page.

---

### D14. Scope limits

- This public-data project does not estimate the effect of the grid transformation programme. The weather-adjusted SAIDI series is a model-based comparison, not evidence of the programme's causal benefit; feeder-level project data would be required for that assessment.
- The project does not rank Dominion nationally. It places Dominion within a defined peer set with reporting methods stated.
- The project does not attribute load growth to data centres from the data. EIA-861 does not identify customers. It reports the shape of the growth (night hours rising faster than day hours and commercial sales rising far faster than commercial customer counts), which is consistent with round-the-clock load.

---

### D15. Dominion counties and the EAGLE-I customer basis

**Context.** EAGLE-I reports customers out by county for every utility in that county, not by utility. Dominion shares most of its counties with co-ops and municipal utilities. EAGLE-I's own customer counts (`MCC.csv`) hold impossible values for some small cities (P23).

**Decision.** A Dominion county is one where EIA-861's 2025 Service Territory lists utility 19876: 103 counties and cities (EIA's 104 names less Bedford city, merged into Bedford County in 2013). `DIM_COUNTY.dominion_only_county` marks the 33 where no other utility is listed, so EAGLE-I's counts there are Dominion customers; `dominion_county_rule` and `dominion_county_reason` carry the rule in words for every county. The customer basis per county is EAGLE-I's modelled count unless it is missing or below half the county's ACS housing units, in which case the housing units are used (7 counties).

**Alternatives.** Allocating EAGLE-I counts between utilities by customer share. Rejected: outages are not spread in proportion to customers, and nothing public says how they split.

**Consequence.** Every EAGLE-I figure is "all utilities in the 103 counties Dominion serves", stated on each chart. Dominion-only counties are the robustness check.

---

### D16. Failed EAGLE-I runs stay NULL; impossible readings are set to NULL

**Decision.** A blank count is a failed collection run and stays NULL (P20). A reading above twice the county's customer basis is set to NULL in staging with the reported value kept (P24). Nothing is interpolated (as D7).

**Consequence.** Totals skip failed runs, so periods with many failures (August to November 2025) are undercounted and flagged; the county-day panel uses complete county-days only.

---

### D17. Outage events and restoration times

**Decision.** A territory event is a run of 15-minute readings with 10,000 or more customers out in the 103 counties (about 0.3% of the basis), with gaps of up to 3 hours merged. A county event is 1% or more of the county's customers out (at least 10), gaps up to 1 hour merged. Restoration is measured from the peak against the excess over the median of the 24 hours before the event: hours to 50%, 90% and 99% restored, counting a level only when the series stays below it for the next 3 hours (P25). Events are ranked by `peak_sustained_1h`, the highest level held for four consecutive readings.

**Alternatives.** The first reading below the level (rejected: one failed reading ends the restoration early); ranking by the single highest reading (rejected: ranks a 45-minute spike above multi-day storms).

**Consequence.** The thresholds are stated on the event table. Because the county threshold scales with county size, county event counts compare a county with itself over time, not counties with each other; maps use outage minutes per customer.

---

### D18. Proxy major event days for EAGLE-I

**Context.** Dominion's own major event days are not public.

**Decision.** IEEE 1366's 2.5 beta method applied to daily EAGLE-I customer-hours in the 103 counties: a day is a proxy major event day when its customer-hours exceed exp(alpha + 2.5 beta), alpha and beta being the mean and standard deviation of ln(daily customer-hours) over the previous five years (2015 uses its own year).

**Consequence.** "Non-major" EAGLE-I figures approximate, but are not, Dominion's ex-MED basis. They are never presented as Dominion's SAIDI.

---

### D19. DOE-417 reports are matched to Dominion by area, date and size

**Context.** DOE-417 summaries have no utility column (P29).

**Decision.** A report is a Dominion-area report when Area Affected names Virginia after "West Virginia" is removed and names no other state except North Carolina; rows that add West Virginia, Kentucky, Tennessee and others are left out (Appalachian Power and other utilities serve those combinations). It matches a territory event when it began from one day before the event's start day to one day after its end day and reports customers affected (or a weather event with the count unknown). `size_ratio` = EAGLE-I peak / DOE-417 customers affected is shown, not filtered on: the two measure different things (simultaneous peak for all utilities, against customers affected over the event for the reporting utility).

**Consequence.** Matches are context for named events (Isaias: 508,000 customers affected), never a count of Dominion's major events.

---

### D20. Counties left off the county map and the county-day panel

**Decision.** Fairfax city (P26) and the three municipal-utility cities with almost no EAGLE-I readings, Manassas, Harrisonburg and Bristol (P27), are left off the county map and out of the county-day panel. The panel also drops county-days with any failed reading. All four stay in the territory total and in `FCT_COUNTY_YEAR`, with a `map_flag` in the map export.

**Consequence.** 99 counties are mapped; the panel keeps 379,959 of 413,854 county-days.

---

### D21. One cut-off for 2026 demand figures

**Decision.** Every 2026 figure from EIA-930 runs to the last hour with a value in the file downloaded on 1 November 2026: the hour ending midnight on 29 October 2026 (P33). The text says "to 29 Oct 2026".

**Consequence.** The 2026 peaks (winter 25,413 MW on 9 February, summer 25,384 MW on 3 July) are the same as in the committed 21 October snapshot; the 2026 totals, averages and medians differ slightly.

---

### D22. Bedford city counts as Bedford County in the storm index

**Context.** Bedford city (FIPS 51515) became part of Bedford County (51019) in 2013. EIA's 2025 Service Territory file still lists "Bedford City" for Dominion, and NOAA's zone-county lookup maps forecast zone 34 to both codes, so every zone-34 storm added two county-days for one area (P28).

**Decision.** `STORM_INDEX` (sql/05) folds 51515 into 51019 before counting county-days. The EAGLE-I county tables (sql/09) already did the same. A known double count stays in no presented number.

**Alternatives.** Leaving the index as first published and footnoting the difference. Rejected: the difference is small (38 county-days over 2013-2025), but it is a known error.

**Consequence.** Storm county-days 2024 and 2025 become 464 and 791 (were 465 and 796); 2019 becomes 848 (was 851). The 2015-2024 correlation with SAIDI ex-MED stays 0.70 (0.697), the 2025 prediction 145.3 and the weather-adjusted 2025 value 133.1; the fit becomes 104.3 + 0.0518 x county-days. `data/output/storm_index.csv`, `storm_vs_saidi.csv` and `saidi_weather_adjusted.csv` were re-exported and `scripts/check_output_metrics.py` expects the new values. A Snowflake account built before D22 keeps the pre-D22 values in `RELIABILITY.MART.STORM_INDEX`, `SAIDI_WEATHER_ADJUSTED` and the view `V_STORM_VS_SAIDI` that reads the index until the `STORM_INDEX` statement in sql/05 and the `SAIDI_WEATHER_ADJUSTED` statement in sql/07 are run again there. In an account where sql/09 has run, T21 fails until sql/05 and sql/07 are run again, because the county-day panel already counts Bedford once. The workbook `powerbi/Dominion_Reliability_PowerBI_Data.xlsx` (sheet `StormIndex`) also predates D22; storm figures should be taken from `data/output/storm_vs_saidi.csv`.
