# Findings (Agent D)

Each section: one-paragraph finding, the chart-ready table (file in `data/output/`), caveats, and
the exact query. Queries run against the DuckDB mirror built from the source files
(`scripts/run_local_duckdb_sources.py`); in Snowflake read `mart.` as `RELIABILITY.MART.` and
`stg.` as `RELIABILITY.STG.`. Public data only: nothing here is Dominion internal data.

## C6 R's numbered items N-1 to N-11, checked (batch 6)

Each item: R's value, D's value from D's own query, verdict. Source of R's items: `research/hard25_answers.md`, table "Numbers not yet in claims.csv".

| Item | What | Verdict |
|---|---|---|
| N-1 | 2025 band 122.3-168.2 = 95% prediction interval | CONFIRMED |
| N-2 | Dominion "Other" 2013-25; auto-recorded from 2015 | CONFIRMED |
| N-3 | All-events SAIFI 2021-25: 1.531, 6th of 12; 11-peer median 1.408 | CONFIRMED |
| N-4 | Ex-MED 11-peer medians 0.934 and 99.5 | CONFIRMED (C5-1) |
| N-5 | 10 of 12 IEEE 1366 every year 2014-25; Dominion and Alabama Power "Other" | CONFIRMED |
| N-6 | Storm 332.8 vs calm 27.86 | CONFIRMED (C5-2) |
| N-7 | 6,530 - 6,108 = 422 | CONFIRMED, wording sharpened (C5-3) |
| N-8 | Co-op SAIFI 1.887 vs 1.849 (13,341 customers) | CONFIRMED |
| N-9 | Resume month counts | NOT CHECKED: not a data item |
| N-11 | All-events SAIDI 2023-25: 223.0, 9th of 12 | CONFIRMED |

### N-1 The 2025 band around the storm-line prediction

**CONFIRMED, and it is a prediction interval.** Fit 2015-2024 (n = 10, after D22): SAIDI ex-MED = 104.2616 + 0.051820 x storm county-days; residual SD 8.67 minutes; t(0.975, 8 df) = 2.306. At 791 storm county-days the fit gives 145.25. The **95% prediction interval** for a single new year is **122.3 to 168.2** (+/-23.0): actual 2025 (144.4) lies inside it. The **95% confidence interval** for the line itself (the mean SAIDI of years with 791 storm county-days) is narrower, 133.9 to 156.6 (+/-11.3), and 144.4 lies inside that too. Say: "the 95% prediction interval for 2025 was about 122 to 168 minutes"; never call it a confidence interval. It assumes the 2015-2024 line and normal residuals; ten points, so treat it as rough.

Formula: prediction half-width = t x s x sqrt(1 + 1/n + (791 - mean x)^2 / Sxx); confidence half-width drops the "1 +".

```sql
SELECT year, storm_county_days, saidi_ex_med FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2025 ORDER BY year
```

### N-2 Dominion's reporting standard and automatic recording, 2013-2025

**CONFIRMED.** `standard` is "Other" in every year 2013-2025; `auto_recorded` is false in 2013, 2014 and true in 2015-2025. D6 starts the weather fit in 2015 for that reason. Wording: "recording became automated in 2015" is what EIA-861's flag says; "which shifts the level" is D6's reasoning, not something the flag measures.

```sql
SELECT year, standard, auto_recorded
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' ORDER BY year
```

### N-3 and N-11 All-events ranks (no MED rule); N-4 ex-MED medians

**N-3 CONFIRMED.** All-events SAIFI, mean of 2021-2025: Dominion **1.531, 6th-highest of the 12**; median of the other 11 **1.408**. Ex-MED: 1.211, 4th-highest (median of the 11: 0.934). So on all events the SAIFI rank moves from 4th to 6th of 12; Dominion stays above the median either way.

**N-11 CONFIRMED.** All-events SAIDI, mean of 2023-2025: Dominion **223.0 minutes, 9th-highest of the 12** (median of the other 11: 348.9); ex-MED 133.0, 4th-highest. Highest all-events SAIDI: Duke Energy Florida, LLC 922, Duke Energy Progress - (NC) 742, Duke Energy Carolinas, LLC 728. Which storms put them there is not in this table, so "hurricane-hit peers at the top" stays an inference, as R marks it.

**N-4 CONFIRMED** (findings § C5-1): 11-peer ex-MED medians SAIFI 0.934, CAIDI 99.5; 12-utility 0.964 and 105.0.

| Utility | All-events SAIDI 2023-25 | Rank | Ex-MED SAIDI 2023-25 | Rank | All-events SAIFI 2021-25 | Rank | Ex-MED SAIFI 2021-25 | Rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Duke Energy Florida, LLC | 922.0 | 1 | 83.0 | 8 | 1.408 | 7 | 0.994 | 6 |
| Duke Energy Progress - (NC) | 742.3 | 2 | 143.8 | 2 | 1.641 | 4 | 1.228 | 3 |
| Duke Energy Carolinas, LLC | 728.1 | 3 | 179.0 | 1 | 1.616 | 5 | 1.253 | 1 |
| Georgia Power Co | 722.7 | 4 | 140.8 | 3 | 1.705 | 1 | 1.243 | 2 |
| Dominion Energy South Carolina, Inc | 719.0 | 5 | 83.9 | 7 | 1.674 | 3 | 1.140 | 5 |
| Alabama Power Co | 348.9 | 6 | 110.0 | 5 | 1.674 | 2 | 0.934 | 7 |
| Florida Power & Light Co | 275.7 | 7 | 46.6 | 12 | 0.766 | 11 | 0.488 | 12 |
| PPL Electric Utilities Corp | 267.6 | 8 | 99.1 | 6 | 0.969 | 8 | 0.689 | 10 |
| **Virginia Electric & Power Co** | 223.0 | 9 | 133.0 | 4 | 1.531 | 6 | 1.211 | 4 |
| PECO Energy Co | 222.1 | 10 | 66.1 | 9 | 0.968 | 9 | 0.742 | 8 |
| Baltimore Gas & Electric Co | 166.6 | 11 | 64.2 | 10 | 0.961 | 10 | 0.710 | 9 |
| Potomac Electric Power Co | 90.4 | 12 | 48.3 | 11 | 0.729 | 12 | 0.569 | 11 |

Ranks: 1 = highest of the 12. Every utility has all five (SAIFI) and all three (SAIDI) years.

```sql
WITH u AS (
  SELECT f.utility_key, d.utility_name,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_all END)    AS saifi_all_2021_25,
         COUNT(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_all END)  AS n_saifi,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_all END)    AS saidi_all_2023_25,
         COUNT(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_all END)  AS n_saidi,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_ex_med_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_ex_med_2023_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')
  GROUP BY 1, 2)
SELECT utility_key, utility_name, utility_key = '19876|VA' AS is_dominion, n_saifi, n_saidi,
       saifi_all_2021_25, RANK() OVER (ORDER BY saifi_all_2021_25 DESC) AS saifi_all_rank,
       saidi_all_2023_25, RANK() OVER (ORDER BY saidi_all_2023_25 DESC) AS saidi_all_rank,
       saifi_ex_med_2021_25, RANK() OVER (ORDER BY saifi_ex_med_2021_25 DESC) AS saifi_ex_med_rank,
       saidi_ex_med_2023_25, RANK() OVER (ORDER BY saidi_ex_med_2023_25 DESC) AS saidi_ex_med_rank,
       MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saifi_all_2021_25 END) OVER () AS saifi_all_median_11,
       MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saidi_all_2023_25 END) OVER () AS saidi_all_median_11
FROM u ORDER BY saidi_all_2023_25 DESC
```

### N-5 Reporting standards in the peer set; docs/06 corrected

**CONFIRMED.** In every year 2014-2025, **10 of the 12 file under IEEE 1366**; Dominion and Alabama Power file under "Other" in every year 2013-2025. In 2013 two more filed "Other": Duke Energy Florida, LLC and Georgia Power Co (2013 only). No utility in the set filed both standards in any year, so the mart's de-duplication (keep the IEEE row) hides nothing here.

**docs/06 was wrong.** "Half the peers use a different reporting method" fits no reading: one of the 11 peers (Alabama Power) shares Dominion's "Other" filing and ten use IEEE 1366. Corrected in the repo, commit 29b179f: the docs/06 headline now reads "Ten of the twelve use IEEE 1366; Dominion and Alabama Power use their own rule", and docs/05 explains the `Changed` label. No other repo file said "half" (docs/04 D2 "Most large peers file under IEEE 1366" and docs/05 "Dominion, Alabama Power and some other utilities" are right).

**Where the pack stands (for B).** No slide, note, brief or question-sheet line quotes "half the peers": deck v2 slide 3 ("Methods differ: Dominion uses its own (non-IEEE) major-event rule, most peers IEEE 1366"), its notes, the brief v1 ("Most of these peers use the IEEE 1366 method") and the Power BI subtitle and alt text ("most peers by IEEE 1366") are right. What does need fixing: the brief v1 peer table and B's chart files `work/charts/v0/s3_peer_quadrant.csv` and `work/charts/v2/s3_peer_quadrant_v2*.csv` label **Georgia Power and Duke Energy Florida "Mixed"**; for the years compared (2015 on) both are IEEE 1366, so write "IEEE 1366" (footnote if wanted: "Other" in 2013 only). The same "Changed" label comes from the Power BI `Method` measure (next paragraph). Smaller: the public-variant CSVs carry CAIDI 2021-25 as SAIDI/SAIFI of the means (Georgia Power 113.6), the adopted one as the mean of annual CAIDI (114.2, as `peer_reliability_5yr.csv` and the DAX `CAIDI 5yr`); Dominion is 110.4 either way and its rank (6th) does not change.

**Power BI side effect, for B.** The Fair comparison page filters peer groups only, so the `Method` measure ("Major Storm Rule" column) sees 2013-2025 and shows **"Changed" for Georgia Power and Duke Energy Florida** because of 2013 alone, although every number in that table comes from 2015 onward. Fix option (B's call): evaluate the measure on the compared years, e.g. `CALCULATE(DISTINCTCOUNT(FCT_RELIABILITY[STANDARD]), FCT_RELIABILITY[YEAR] >= 2015)`, or add a year >= 2015 filter to that table. Deck v2, its notes and the Power BI subtitle/alt text say "most peers IEEE 1366", which is right.

| Utility | Years | IEEE 1366 years | "Other" years |
|---|---:|---:|---|
| Baltimore Gas & Electric Co | 13 | 13 | - |
| Dominion Energy South Carolina, Inc | 13 | 13 | - |
| Duke Energy Carolinas, LLC | 13 | 13 | - |
| Duke Energy Progress - (NC) | 13 | 13 | - |
| Florida Power & Light Co | 13 | 13 | - |
| PECO Energy Co | 13 | 13 | - |
| PPL Electric Utilities Corp | 13 | 13 | - |
| Potomac Electric Power Co | 13 | 13 | - |
| Duke Energy Florida, LLC | 13 | 12 | 2013 |
| Georgia Power Co | 13 | 12 | 2013 |
| Alabama Power Co | 13 | 0 | 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 |
| Virginia Electric & Power Co | 13 | 0 | 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 |

```sql
SELECT d.utility_name, f.utility_key,
       COUNT(*) AS years,
       COUNT(CASE WHEN f.standard = 'IEEE 1366' THEN 1 END) AS ieee_years,
       STRING_AGG(CASE WHEN f.standard = 'Other' THEN CAST(f.year AS VARCHAR) END, ', ' ORDER BY f.year) AS other_years
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')
GROUP BY 1, 2 ORDER BY ieee_years DESC, 1
```

```sql
-- before de-duplication: did any of the 12 file both standards in a year? (0 rows = no)
WITH s AS (
  SELECT utility_id || '|' || state AS utility_key, year, standard FROM stg.RELIABILITY_HIST
  UNION ALL
  SELECT utility_id || '|' || state, year, standard FROM stg.RELIABILITY_2025)
SELECT utility_key, year, COUNT(*) AS filings
FROM s WHERE utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')
GROUP BY 1, 2 HAVING COUNT(*) > 1
```

### N-6 and N-7 Storm vs calm levels; 6,530 against 6,108

**N-6 CONFIRMED** (findings § C5-2): storm 332.8 (95% CI 225.6 to 453.4) and calm 27.86 (23.09 to 33.22) customer-hours per 1,000 customers; R's rounded 333 and 27.9 are fine.

**N-7 CONFIRMED, with a wording fix** (findings § C5-3 has the query and the year table): 6,530 - 6,108 = 422 = **114** storm county-days in the four counties off the map **+ 308** with a failed EAGLE-I reading. In 2025 the gap is 791 - 677 = 114 as R says, but that 114 is 18 off-map + 96 failed-reading days; the off-map total over 2015-2025 is also 114, a coincidence that invites confusion. Suggested line: "The 422 are 114 in the four counties left off the map and 308 days with failed EAGLE-I readings, 96 of them in 2025."

### N-8 The co-op SAIFI denominator (P18)

**CONFIRMED.** Virginia co-ops, 2025, SAIFI ex-MED: **1.887** with the denominator limited to utilities that reported interruptions (what `V_GROUP_INDEX` returns: 1.887), **1.849** if all members' customers were counted. The difference is 13,341 customers of Prince George Electric Coop, which has no SAIFI for 2025 (P18: it filed SAIDI only). The fix date (27 Oct, commit 1635a8e) is R's citation; D did not re-check the commit.

```sql
SELECT
  SUM(f.cust_interruptions_ex_med)
    / SUM(CASE WHEN f.cust_interruptions_ex_med IS NOT NULL THEN f.customers END) AS saifi_reporters_only,  -- V_GROUP_INDEX rule
  SUM(f.cust_interruptions_ex_med) / SUM(f.customers)                            AS saifi_all_members,
  SUM(CASE WHEN f.cust_interruptions_ex_med IS NULL THEN f.customers END)        AS customers_without_saifi,
  STRING_AGG(CASE WHEN f.cust_interruptions_ex_med IS NULL THEN d.utility_name END, ', ') AS without_saifi
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE d.peer_group = 'Virginia co-op' AND f.year = 2025
```

```sql
SELECT year, saifi_ex_med FROM mart.V_GROUP_INDEX WHERE peer_group = 'Virginia co-op' AND year = 2025
```

### N-9 Resume month counts

**Not checked by D.** These come from the resume's dates, not from the data, and D does not read the resume. R or the orchestrator should confirm them with the candidate.

## C5 Numbers for the G2 revision (batch 5, after the V3 mock panel)

Repo commits for this batch: c0b2ea2 (`storm_vs_calm.csv`), 7133aba (peer medians without Dominion; D10 wording), 4fc9939 (`county_outage_map_dominion_only.csv`), d1bdff2 (docs/05 and README: 6,108 reconciled with 6,530). `scripts/check_output_metrics.py` asserts every number below that comes from a committed file.

### C5-1 Peers (S3): the twelve are Dominion and 11 peers

**Answer.** Yes, Dominion is one of the twelve. D10 names eleven utilities and then adds Dominion: "Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before results were computed. Southeast: Duke Carolinas, Duke Progress, Georgia Power, Alabama Power, Dominion SC. Mid-Atlantic (PJM): BGE, Pepco, PECO, PPL. Florida: FPL, Duke Energy Florida. Plus Dominion VA, so the twelve are Dominion and 11 peers." (docs/04; the clause "so the twelve are Dominion and 11 peers" was added in commit 7133aba to remove the ambiguity). The peer query returns 12 utilities, one of them Dominion. So the deck says **"12 large utilities (Dominion and 11 peers)"**.

**Medians without Dominion (the 11 peers), 2021-25 means of the annual ex-MED values:** SAIFI **0.934** (with Dominion 0.964), CAIDI **99.5** minutes (with Dominion 105.0). SAIDI 2023-25: **83.9** (with Dominion 91.5).

**Ranks do not change.** A rank is Dominion's place among the twelve, so it does not depend on which median is drawn: SAIFI 1.211 is **fourth-highest** of the 12 (three peers higher), CAIDI 110.4 is **sixth-highest** (five peers higher), SAIDI 2023-25 133.0 is fourth-highest. "Fourth-highest SAIFI" and "6th CAIDI" stand as long as they say "of the 12" ("fourth among 11 peers" would be wrong).

**Distance from the median.** Against the 11-peer medians Dominion is 30% above on SAIFI (against the 12-utility median: 26%), 11% above on CAIDI (5%) and 59% above on SAIDI 2023-25 (45%). It sits above both lines either way, so the quadrant is the same. The frequency gap reads larger and the restoration gap still modest: "restoration mid-pack" holds as a rank (6th of 12), but CAIDI is 11% above the 11-peer median, so say "mid-pack", not "at the median".

**Line for S3:** "Among 12 large utilities (Dominion and 11 peers), 2021-25: outages per customer 1.21, fourth-highest (peer median 0.93); minutes per outage 110, sixth-highest (peer median 99.5). Reporting methods differ, so the comparison is indicative."

**Chart-ready:** `data/output/peer_reliability_5yr.csv` (12 rows; new columns `median_saidi_2023_25_excl_dominion`, `median_saifi_2021_25_excl_dominion`, `median_caidi_2021_25_excl_dominion`; the old median columns are unchanged).

| Utility | SAIDI 2023-25 | Rank | SAIFI 2021-25 | Rank | CAIDI 2021-25 | Rank |
|---|---:|---:|---:|---:|---:|---:|
| Duke Energy Carolinas, LLC | 179.0 | 1 | 1.253 | 1 | 139.2 | 1 |
| Georgia Power Co | 140.8 | 3 | 1.243 | 2 | 114.2 | 4 |
| Duke Energy Progress - (NC) | 143.8 | 2 | 1.228 | 3 | 113.9 | 5 |
| **Virginia Electric & Power Co** | 133.0 | 4 | 1.211 | 4 | 110.4 | 6 |
| Dominion Energy South Carolina, Inc | 83.9 | 7 | 1.140 | 5 | 72.0 | 12 |
| Duke Energy Florida, LLC | 83.0 | 8 | 0.994 | 6 | 87.2 | 11 |
| Alabama Power Co | 110.0 | 5 | 0.934 | 7 | 125.3 | 3 |
| PECO Energy Co | 66.1 | 9 | 0.742 | 8 | 98.6 | 8 |
| Baltimore Gas & Electric Co | 64.2 | 10 | 0.710 | 9 | 99.5 | 7 |
| PPL Electric Utilities Corp | 99.1 | 6 | 0.689 | 10 | 136.7 | 2 |
| Potomac Electric Power Co | 48.3 | 11 | 0.569 | 11 | 90.1 | 10 |
| Florida Power & Light Co | 46.6 | 12 | 0.488 | 12 | 96.0 | 9 |
| Median of the 12 | 91.5 | | 0.964 | | 105.0 | |
| Median of the 11 peers | 83.9 | | 0.934 | | 99.5 | |

```sql
WITH u AS (
  SELECT f.utility_key, d.utility_name, d.peer_group,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_2023_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.caidi_ex_med END) AS caidi_2021_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')
  GROUP BY 1, 2, 3)
SELECT COUNT(*) AS utilities, COUNT(CASE WHEN utility_key = '19876|VA' THEN 1 END) AS dominion_rows,
       MEDIAN(saidi_2023_25) AS saidi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saidi_2023_25 END) AS saidi_med_11,
       MEDIAN(saifi_2021_25) AS saifi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saifi_2021_25 END) AS saifi_med_11,
       MEDIAN(caidi_2021_25) AS caidi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN caidi_2021_25 END) AS caidi_med_11
FROM u
```

```sql
WITH u AS (
  SELECT f.utility_key, d.utility_name, d.peer_group,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_2023_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.caidi_ex_med END) AS caidi_2021_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')
  GROUP BY 1, 2, 3)
SELECT utility_key, utility_name, utility_key = '19876|VA' AS is_dominion,
       saidi_2023_25, saifi_2021_25, caidi_2021_25,
       RANK() OVER (ORDER BY saidi_2023_25 DESC) AS saidi_rank,  -- 1 = highest of the 12
       RANK() OVER (ORDER BY saifi_2021_25 DESC) AS saifi_rank,
       RANK() OVER (ORDER BY caidi_2021_25 DESC) AS caidi_rank
FROM u ORDER BY saifi_2021_25 DESC
```

### C5-2 S4: storm and calm levels, with the ratio and its robustness

**Answer.** On county-days with a NOAA line-risk storm report, outage customer-hours per 1,000 customers averaged **332.8 (225.6 to 453.4)**; on calm county-days, **27.86 (23.09 to 33.22)** (95% intervals). Ratio **11.9 (7.9 to 16.9)** (printed: "11.9x (95% CI 7.9-16.9)"), from 6,108 storm and 373,851 calm county-days, 2015-2025. The levels and the ratio come from the same 2,000 resamples of whole days, so the ratio interval is not the ratio of the level intervals.

**Robustness line:** non-major days only 9.9 (8.6 to 11.3); the 31 Dominion-only counties on the map 19.9 (11.2 to 32.5); every year from 5.9 (2025) to 27.4 (2020), and every year's interval lies above 1 (lowest lower bound 2.2, 2018).

**Slide text (one visual, the two levels):** "Outage customer-hours per 1,000 customers per county-day: storm days 333, calm days 28 (about 12x; 95% CI 7.9-16.9). Holds on non-major days (9.9x), in Dominion-only counties (19.9x) and in every year 2015-2025." Caveat line: "EAGLE-I counts every utility's customers in a county; 99 of Dominion's 103 Virginia counties, complete days only. An association: storm reports partly follow damage."

**Chart-ready:** `data/output/storm_vs_calm.csv` (19 rows: `subset`, both counts, `storm_ch_per_1k` and `calm_ch_per_1k` with `_ci_low`/`_ci_high`, `ratio` with its interval, `ratio_label`). The small table for the slide (one decimal, rounded once from the unrounded values):

| Subset | Storm county-days | Storm days: customer-hours per 1,000 (95% CI) | Calm days (95% CI) | Ratio (95% CI) |
|---|---:|---:|---:|---:|
| All complete county-days, 2015-2025 | 6,108 | 332.8 (225.6 to 453.4) | 27.9 (23.1 to 33.2) | 11.9 (7.9 to 16.9) |
| Non-major days (proxy major event days removed) | 4,950 | 133.5 (116.6 to 151.9) | 13.5 (12.9 to 14.3) | 9.9 (8.6 to 11.3) |
| Dominion-only counties | 1,065 | 368.8 (217.2 to 558.3) | 18.6 (14.7 to 23.5) | 19.9 (11.2 to 32.5) |

Every year (the robustness line's "every year"):

| Year | Storm county-days | Calm county-days | Storm level | Calm level | Ratio (95% CI) |
|---:|---:|---:|---:|---:|---:|
| 2015 | 505 | 35,630 | 52.0 | 8.4 | 6.2 (2.8 to 11.9) |
| 2016 | 581 | 35,653 | 168.1 | 21.9 | 7.7 (4.1 to 13.4) |
| 2017 | 412 | 35,510 | 148.4 | 14.4 | 10.3 (5.7 to 17.3) |
| 2018 | 652 | 34,107 | 690.9 | 70.2 | 9.8 (2.2 to 24.5) |
| 2019 | 770 | 33,284 | 178.4 | 18.7 | 9.5 (6.5 to 13.4) |
| 2020 | 365 | 32,929 | 519.8 | 19.0 | 27.4 (6.8 to 62.5) |
| 2021 | 592 | 33,567 | 614.1 | 48.2 | 12.7 (2.5 to 33.2) |
| 2022 | 711 | 35,424 | 431.1 | 35.5 | 12.1 (5.2 to 23.9) |
| 2023 | 386 | 35,749 | 260.7 | 13.8 | 19.0 (12.2 to 28.2) |
| 2024 | 457 | 35,776 | 320.6 | 22.6 | 14.2 (7.4 to 24.1) |
| 2025 | 677 | 26,222 | 225.9 | 38.4 | 5.9 (3.0 to 10.6) |

**Caveats.** 2025 rests on 74% of its county-days (26,899 complete of 36,135) because failed EAGLE-I runs cluster in late 2025 (docs/03 P20); it is the lowest year (5.9x) and its interval still lies above 1. The tropical subset (93 storm county-days) is too small to quote (1.5 to 116.8). Outages that run past midnight land on a "calm" next day, which pulls the ratio down.

Query (the rows the bootstrap resamples; `scripts/storm_vs_calm_ratio.py`):

```sql
SELECT d.day, d.year, d.storm_day, d.storm_wind, d.storm_winter, d.storm_tropical, d.dominion_only_county,
       d.customer_hours_per_1k, t.is_med_proxy
FROM mart.FCT_COUNTY_DAY d
JOIN mart.FCT_TERRITORY_DAY t ON t.day = d.day
WHERE d.failed_readings = 0                                    -- complete county-days only
  AND d.county_fips NOT IN ('51600', '51683', '51660', '51520') -- D20: off the map
ORDER BY d.day, d.county_fips                                  -- fixed order: sums are bit-identical run to run
```

### C5-3 Storm county-days: 6,530 against 6,108

**Answer.** Both are right; they count different things. **6,530** is every storm county-day in Dominion's 103 Virginia counties, 2015-2025: the sum of the storm index (`storm_index.csv`, after D22) and of `storm_day` in the county-day table. **6,108** is the part of it the storm-vs-calm comparison can use: 114 fall in the four counties off the map (D20: Fairfax city, Manassas, Harrisonburg, Bristol) and 308 are days with at least one failed EAGLE-I reading (2018 15, 2019 66, 2020 57, 2021 74, 2025 96). 6,530 - 114 - 308 = 6,108.

**Labels for B (use exactly):**

- 6,530: "storm county-days, 2015-2025, Dominion's 103 Virginia counties (NOAA)". Long form: "county-days with a NOAA line-risk storm report, 2015-2025, all 103 Virginia counties Dominion serves (Bedford city counted in Bedford County)".
- 6,108: "storm county-days with complete outage readings, 2015-2025, 99 counties on the map (EAGLE-I)". Long form: "the storm county-days behind the 11.9x comparison: complete EAGLE-I readings, the 99 counties on the map".

Never put the two side by side without the label; the S4 slide uses only 6,108.

| Year | Storm county-days, 103 counties | In the 4 counties off the map | With a failed EAGLE-I reading | Complete, 99 counties |
|---:|---:|---:|---:|---:|
| 2015 | 521 | 16 | 0 | 505 |
| 2016 | 594 | 13 | 0 | 581 |
| 2017 | 419 | 7 | 0 | 412 |
| 2018 | 683 | 16 | 15 | 652 |
| 2019 | 848 | 12 | 66 | 770 |
| 2020 | 429 | 7 | 57 | 365 |
| 2021 | 673 | 7 | 74 | 592 |
| 2022 | 718 | 7 | 0 | 711 |
| 2023 | 390 | 4 | 0 | 386 |
| 2024 | 464 | 7 | 0 | 457 |
| 2025 | 791 | 18 | 96 | 677 |
| **2015-2025** | **6,530** | **114** | **308** | **6,108** |

```sql
SELECT year,
       COUNT(CASE WHEN storm_day THEN 1 END)                                                          AS storm_103_counties,
       COUNT(CASE WHEN storm_day AND county_fips IN ('51600', '51683', '51660', '51520') THEN 1 END)                             AS in_4_off_map,
       COUNT(CASE WHEN storm_day AND county_fips NOT IN ('51600', '51683', '51660', '51520') AND failed_readings > 0 THEN 1 END) AS with_failed_reading,
       COUNT(CASE WHEN storm_day AND county_fips NOT IN ('51600', '51683', '51660', '51520') AND failed_readings = 0 THEN 1 END) AS complete_99_counties
FROM mart.FCT_COUNTY_DAY GROUP BY year ORDER BY year
```

```sql
SELECT SUM(storm_county_days) AS storm_index_2015_25 FROM mart.STORM_INDEX WHERE year BETWEEN 2015 AND 2025
```

### C5-4 Storm county-days by year, 2013-2025, after D22

**Answer.** Confirmed: **2022 = 718** and **2025 = 791** after D22 (V2's 718 is the post-D22 value). 2022 to 2025: +73 (+10.2%). Before D22 the pair was 723 and 796. D22 lowered every year by 1 to 5, not only 2024 and 2025 (the 38 duplicate county-days of 2013-2025): any slide or note with 723, 796, 465 or 851 carries pre-D22 values. 2025 is the second-highest year; 2019 (848) is the highest.

**Chart-ready:** `data/output/storm_index.csv` (post-D22; also `storm_vs_saidi.csv`).

| Year | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| After D22 | 374 | 583 | 521 | 594 | 419 | 683 | 848 | 429 | 673 | 718 | 390 | 464 | 791 |
| Before D22 | 376 | 586 | 526 | 597 | 420 | 687 | 851 | 431 | 676 | 723 | 391 | 465 | 796 |
| Change | -2 | -3 | -5 | -3 | -1 | -4 | -3 | -2 | -3 | -5 | -1 | -1 | -5 |

```sql
SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year BETWEEN 2013 AND 2025 ORDER BY year
```

Before-D22 values: `git show 06631ad^:data/output/storm_index.csv` (the file as first committed).

### C5-5 The county map: Dominion-only counties, and the all-utilities version

**Answer.** Same A3 measure (outage minutes per customer a year on non-major days, 2015-2024 average). In the **31 Dominion-only counties on the map** (1,257,416 customers), where EAGLE-I counts Dominion customers alone: **159 minutes** (customer-weighted). The 68 shared counties: 211; all 99 on the map: 192; all 103: 195 (A3's figure). By county: Richmond city 58.9 to Charles City County 778.0; among the 13 with 20,000 or more customers, Richmond city 58.9 to Henrico County 276.6.

**Do not read the gap as Dominion against other utilities.** The Dominion-only counties are mostly cities and inner suburbs (Hampton Roads, Richmond, Arlington and Alexandria) plus a few small Tidewater counties, so the lower figure compares places, not utilities.

**Chart-ready:**

- `data/output/county_outage_map_dominion_only.csv`: the 33 Dominion-only rows (31 with `map_flag = 'ok'`; Fairfax city and Harrisonburg city are Dominion-only but off the map, D20). Title: "Outage minutes per customer a year, non-major days, 2015-2024 average: the 31 counties Dominion serves alone (EAGLE-I counts Dominion customers there)".
- `data/output/county_outage_map.csv`: all 103 (99 on the map). Title: "Outage minutes per customer a year, non-major days, 2015-2024 average: **all utilities** in each of Dominion's Virginia counties (EAGLE-I); 99 of 103 shown". Range on the map: Manassas Park city 30.0 to Nelson County 878.6; use one colour scale for both maps.
- No "start with these counties" line on either (G2).

| Counties | Number | Customers | Minutes a year, non-major days, 2015-2024 |
|---|---:|---:|---:|
| Dominion-only counties | 31 | 1,257,416 | 159.2 |
| Shared counties (Dominion and other utilities) | 68 | 2,137,355 | 211.1 |
| All counties on the map | 99 | 3,394,771 | 191.9 |
| All 103 Dominion counties (A3) | 103 | | 195.3 |

Dominion-only counties on the map, highest to lowest:

| County | Customers | Minutes, non-major, avg 2015-24 | Storm days a year |
|---|---:|---:|---:|
| Charles City County | 2,516 | 778.0 | 2.9 |
| Mathews County | 3,233 | 743.5 | 2.5 |
| Middlesex County | 4,296 | 674.8 | 3.2 |
| Gloucester County | 15,330 | 369.5 | 3.3 |
| New Kent County | 8,920 | 345.8 | 3.2 |
| Henrico County | 150,139 | 276.6 | 5.4 |
| Petersburg city | 14,894 | 268.8 | 1.3 |
| Falls Church city | 6,786 | 223.7 | 2.2 |
| Colonial Heights city | 8,524 | 207.6 | 1.7 |
| Charlottesville city | 20,605 | 204.8 | 2.0 |
| Poquoson city | 4,482 | 203.4 | 1.4 |
| Staunton city | 11,216 | 195.0 | 2.8 |
| York County | 28,029 | 173.2 | 3.2 |
| Waynesboro city | 10,510 | 170.9 | 3.1 |
| James City County | 32,899 | 168.6 | 3.5 |
| Hopewell city | 9,904 | 157.0 | 1.2 |
| Emporia city | 2,639 | 154.6 | 1.7 |
| Alexandria city | 67,166 | 149.4 | 3.3 |
| Arlington County | 111,055 | 147.2 | 5.5 |
| Virginia Beach city | 190,947 | 141.8 | 5.9 |
| Hampton city | 58,889 | 139.1 | 3.1 |
| Portsmouth city | 43,205 | 134.2 | 2.5 |
| Newport News city | 84,935 | 130.6 | 3.6 |
| Chesapeake city | 104,567 | 123.8 | 5.4 |
| Covington city | 2,882 | 117.1 | 2.7 |
| Fredericksburg city | 14,939 | 113.6 | 2.6 |
| Williamsburg city | 8,943 | 106.8 | 1.8 |
| Norfolk city | 116,644 | 104.8 | 4.5 |
| Buena Vista city | 2,949 | 99.6 | 3.4 |
| Lexington city | 2,808 | 95.0 | 3.1 |
| Richmond city | 112,565 | 58.9 | 1.7 |

**Caveats.** Dominion-only means EIA-861's 2025 Service Territory lists no other utility in the county (D15); small counties have noisy rates (Charles City County, 2,516 customers). 2025 is not averaged (failed EAGLE-I runs, P20).

```sql
WITH m AS (
WITH r AS (
  SELECT county_fips, SUM(readings) AS readings_2015_24
  FROM mart.FCT_COUNTY_DAY WHERE year BETWEEN 2015 AND 2024 GROUP BY 1
),
y AS (
  SELECT c.*, r.readings_2015_24,
         CASE WHEN c.county_fips = '51600' THEN 'excluded: implausible readings 2018-2020'
              WHEN r.readings_2015_24 < 1000 THEN 'excluded: almost no EAGLE-I readings (municipal utility)'
              ELSE 'ok' END AS map_flag
  FROM mart.FCT_COUNTY_YEAR c JOIN r USING (county_fips)
)
SELECT county_fips, county_label, dominion_only_county, MAX(customers_basis) AS customers_basis, map_flag,
       MAX(readings_2015_24) AS readings_2015_24,
       ROUND(60 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN customer_hours_non_med END) / MAX(customers_basis), 1) AS minutes_non_med_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2015_19,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2020_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN storm_days END), 1) AS storm_days_avg_2015_24
FROM y GROUP BY county_fips, county_label, dominion_only_county, map_flag
),
y AS (
  SELECT c.year, m.dominion_only_county, SUM(c.customer_hours_non_med) AS customer_hours_non_med,
         SUM(c.customers_basis) AS customers_basis, COUNT(*) AS counties
  FROM mart.FCT_COUNTY_YEAR c JOIN m USING (county_fips)
  WHERE m.map_flag = 'ok' AND c.year BETWEEN 2015 AND 2024
  GROUP BY GROUPING SETS ((c.year, m.dominion_only_county), (c.year))
)
SELECT CASE WHEN dominion_only_county THEN 'Dominion-only counties'
            WHEN NOT dominion_only_county THEN 'Shared counties (Dominion and other utilities)'
            ELSE 'All counties on the map' END AS counties_group,
       MAX(counties) AS counties, MAX(customers_basis) AS customers_basis,
       AVG(60 * customer_hours_non_med / customers_basis) AS minutes_non_med_avg_2015_24  -- customer-weighted each year, then the mean
FROM y GROUP BY 1 ORDER BY 2
```

```sql
SELECT AVG(60 * ch / basis) AS minutes_non_med_avg_2015_24
FROM (SELECT year, SUM(customer_hours_non_med) AS ch, SUM(customers_basis) AS basis
      FROM mart.FCT_COUNTY_YEAR WHERE year BETWEEN 2015 AND 2024 GROUP BY year)
```

```sql
SELECT * FROM (
WITH r AS (
  SELECT county_fips, SUM(readings) AS readings_2015_24
  FROM mart.FCT_COUNTY_DAY WHERE year BETWEEN 2015 AND 2024 GROUP BY 1
),
y AS (
  SELECT c.*, r.readings_2015_24,
         CASE WHEN c.county_fips = '51600' THEN 'excluded: implausible readings 2018-2020'
              WHEN r.readings_2015_24 < 1000 THEN 'excluded: almost no EAGLE-I readings (municipal utility)'
              ELSE 'ok' END AS map_flag
  FROM mart.FCT_COUNTY_YEAR c JOIN r USING (county_fips)
)
SELECT county_fips, county_label, dominion_only_county, MAX(customers_basis) AS customers_basis, map_flag,
       MAX(readings_2015_24) AS readings_2015_24,
       ROUND(60 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN customer_hours_non_med END) / MAX(customers_basis), 1) AS minutes_non_med_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2015_19,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2020_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN storm_days END), 1) AS storm_days_avg_2015_24
FROM y GROUP BY county_fips, county_label, dominion_only_county, map_flag
) WHERE dominion_only_county ORDER BY minutes_non_med_avg_2015_24 DESC
```

### C5-6 The 2025 storm line: 145.3 against 144.4

**Answer.** Confirmed. With the coefficients as printed, 104.3 + 0.0518 x 791 = 104.3 + 40.9738 = **145.2738**, which prints as 145.3. With the unrounded fit (2015-2024, n = 10, after D22): 104.2616 + 0.051820 x 791 = **145.2516**, also 145.3. Actual 2025 SAIDI ex-MED: 144.4, so 2025 sits 0.85 minutes (0.6%) below the line: "2025 sits on the storm line" is fair. r = 0.6973 (prints 0.70). Weather-adjusted 2025 = 144.4 - 145.2516 + 134.0014 (the 2015-2024 mean) = 133.1498, which prints as 133.1 (not 133.2: it is just below the half).

Before D22 the fit was 104.3732 + 0.051375 x 796 = 145.2680 (also 145.3), so the slide figure did not move.

**Chart-ready:** `data/output/saidi_weather_adjusted.csv` (`predicted_from_weather`, `fit_slope`, `fit_intercept`, `fit_mean`).

```sql
SELECT REGR_INTERCEPT(saidi_ex_med, storm_county_days) AS intercept,
       REGR_SLOPE(saidi_ex_med, storm_county_days)     AS slope,
       CORR(saidi_ex_med, storm_county_days)           AS r,
       COUNT(*) AS n, AVG(saidi_ex_med) AS mean_saidi
FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024
```

```sql
SELECT storm_county_days, saidi_ex_med FROM mart.V_STORM_VS_SAIDI WHERE year = 2025
```

## S2 base-year check

Question: does "the rise comes mostly from more frequent interruptions" hold whichever base year is used?
Source: EIA-861 via `mart.FCT_RELIABILITY` (Dominion Energy Virginia, utility 19876, VA, ex-MED, Dominion's own
major-event rule). 2025 values equal the EIA-861 2025 final file (released 7 Oct 2026).

### S2.1 SAIDI, SAIFI and CAIDI ex-MED, 2013 to 2025

```sql
SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2013 AND 2025 ORDER BY year
```

| Year | SAIDI (min) | SAIFI | CAIDI (min) | Customers |
|---:|---:|---:|---:|---:|
| 2013 | 106.0 | 1.052 | 100.8 | 2,358,445 |
| 2014 | 112.0 | 1.154 | 97.1 | 2,381,774 |
| 2015 | 119.6 | 1.155 | 103.6 | 2,420,939 |
| 2016 | 138.2 | 1.275 | 108.4 | 2,432,641 |
| 2017 | 117.4 | 1.100 | 106.7 | 2,456,901 |
| 2018 | 149.6 | 1.303 | 114.8 | 2,482,946 |
| 2019 | 149.9 | 1.244 | 120.5 | 2,507,580 |
| 2020 | 141.0 | 1.260 | 111.9 | 2,535,825 |
| 2021 | 133.6 | 1.162 | 115.0 | 2,567,152 |
| 2022 | 136.0 | 1.199 | 113.5 | 2,589,282 |
| 2023 | 123.3 | 1.165 | 105.9 | 2,612,104 |
| 2024 | 131.3 | 1.210 | 108.5 | 2,635,267 |
| 2025 | 144.4 | 1.320 | 109.4 | 2,675,735 |

SAIFI 2025 = 1.320 is the highest value in 2013-2025 (next: 2018, 1.303). CAIDI 2025 = 109.4 is below every year 2018-2022 (111.9 to 120.5) and above 2015-2017 and 2023-2024.

### S2.2 Log decomposition of the SAIDI change, every base year to 2025

ln(SAIDI2/SAIDI1) = ln(SAIFI2/SAIFI1) + ln(CAIDI2/CAIDI1). The share from frequency is ln(SAIFI ratio) / ln(SAIDI ratio);
it is only meaningful when SAIDI moved by more than about 2% (sql/02, V_TREND rule) and in the same direction as SAIFI.

```sql
WITH p AS (SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA')
SELECT a.year AS base_year, b.year AS end_year,
       ROUND(100 * (b.saidi_ex_med / a.saidi_ex_med - 1), 1) AS saidi_pct,
       ROUND(100 * (b.saifi_ex_med / a.saifi_ex_med - 1), 1) AS saifi_pct,
       ROUND(100 * (b.caidi_ex_med / a.caidi_ex_med - 1), 1) AS caidi_pct,
       ROUND(LN(b.saidi_ex_med / a.saidi_ex_med), 4) AS ln_saidi,
       ROUND(LN(b.saifi_ex_med / a.saifi_ex_med), 4) AS ln_saifi,
       ROUND(LN(b.caidi_ex_med / a.caidi_ex_med), 4) AS ln_caidi,
       ROUND(100 * LN(b.saifi_ex_med / a.saifi_ex_med) / LN(b.saidi_ex_med / a.saidi_ex_med)) AS pct_of_change_from_frequency
FROM p a JOIN p b ON b.year = 2025 AND a.year BETWEEN 2015 AND 2024
ORDER BY a.year
```

| Base year | SAIDI change | SAIFI change | CAIDI change | Share of ln change from frequency | Reading |
|---:|---:|---:|---:|---:|---|
| 2015 | +20.7% | +14.3% | +5.6% | 71% | mostly frequency |
| 2016 | +4.5% | +3.5% | +0.9% | 79% | mostly frequency |
| 2017 | +23.0% | +20.0% | +2.5% | 88% | mostly frequency |
| 2018 | -3.5% | +1.3% | -4.7% | n/m | SAIDI fell; frequency up, duration down more |
| 2019 | -3.7% | +6.1% | -9.2% | n/m | SAIDI fell; frequency up, duration down more |
| 2020 | +2.4% | +4.8% | -2.2% | 195% | frequency explains all of it; duration fell |
| 2021 | +8.1% | +13.6% | -4.9% | 164% | frequency explains all of it; duration fell |
| 2022 | +6.1% | +10.1% | -3.6% | 161% | frequency explains all of it; duration fell |
| 2023 | +17.1% | +13.3% | +3.3% | 79% | mostly frequency |
| 2024 | +10.0% | +9.1% | +0.8% | 91% | mostly frequency |

Pairs the brief needs:
- **2023 -> 2025** (the pair in the README): SAIDI +17.1%, SAIFI +13.3%, CAIDI +3.3%; 79% of the log change from frequency.
- **2022 -> 2025** (the pair that moves the 3-year average from 130.2 to 133.0, because (2023-25) - (2022-24) = (2025 - 2022)/3 = 2.78 min): SAIDI +6.1%, SAIFI +10.1%, CAIDI -3.6%. Frequency more than explains the rise; average restoration time fell.

### S2.3 Long run: 2015-17 mean vs 2023-25 mean, and OLS slopes 2015-2025 (n = 11)

```sql
SELECT
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saifi_ex_med END), 3) AS saifi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saifi_ex_med END), 3) AS saifi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN caidi_ex_med END), 1) AS caidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN caidi_ex_med END), 1) AS caidi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saidi_ex_med END), 1) AS saidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_2023_25,
  REGR_SLOPE(saifi_ex_med, year) AS saifi_slope, REGR_SLOPE(caidi_ex_med, year) AS caidi_slope, REGR_SLOPE(saidi_ex_med, year) AS saidi_slope
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2015 AND 2025
```

Slope standard errors and p-values: `scipy.stats.linregress` on the same 11 rows (two-sided, t with 9 df).

| Measure | 2015-17 mean | 2023-25 mean | Change | OLS slope per year | 95% CI | p |
|---|---:|---:|---:|---:|---|---:|
| SAIFI | 1.177 | 1.232 | +4.7% | 0.0043 | -0.0111 to 0.0196 | 0.54 |
| CAIDI (min) | 106.2 | 107.9 | +1.6% | 0.17 | -0.94 to 1.28 | 0.74 |
| SAIDI (min) | 125.1 | 133.0 | +6.3% | 0.64 | -1.87 to 3.15 | 0.58 |

Period-mean decomposition: ln SAIFI ratio 0.0457, ln CAIDI ratio 0.0159, so 74% of the 2015-17 -> 2023-25 rise in SAIDI is frequency (period means of the annual values; SAIDI of the means is not exactly SAIFI x CAIDI of the means, the gap is under 0.2%).

### S2.4 Answer

- **Yes for every base year in which SAIDI rose.** Against 2015, 2016, 2017, 2020, 2021, 2022, 2023 and 2024, SAIFI rose by more than CAIDI, or CAIDI fell. For 2022 -> 2025 (the pair behind 130.2 -> 133.0) frequency more than explains the rise: SAIFI +10.1%, CAIDI -3.6%.
- **Against 2018 and 2019 SAIDI is lower in 2025** (149.6 and 149.9 then, 144.4 now): frequency is still higher in 2025, duration is lower. So the safe wording is about the recent rise, not "reliability is worse than ever".
- **2025 frequency is a record for the series:** SAIFI 1.320 is the highest of 2013-2025. Restoration time (CAIDI 109) is mid-range: higher than 2015-17 and 2023-24, lower than 2018-22.
- **Long run, neither trend is statistically clear on 11 points** (SAIFI slope p = 0.54, CAIDI slope p = 0.74; both 95% intervals include zero). The 2015-17 -> 2023-25 rise in SAIDI (+6.3%) is 74% frequency, so the direction agrees with the short-run pairs; present the long run as direction, not proof.
- **Defensible sentence:** "Measured from 2022 or from 2023, most of the increase in outage minutes came from more interruptions per customer; average restoration time changed little (3.6% shorter than in 2022, 3.3% longer than in 2023). In 2025 interruptions per customer were the highest in EIA's 2013-2025 record."

## Q10 check: trend in the weather-adjusted SAIDI (sql/07)

```sql
SELECT year, weather_adjusted_saidi FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year
-- sql/07 Q10: SELECT ROUND(REGR_SLOPE(weather_adjusted_saidi, year), 2) FROM RELIABILITY.MART.SAIDI_WEATHER_ADJUSTED
```

- Slope **+0.34 minutes per year** over 2015-2025 (n = 11; SQL REGR_SLOPE and scipy agree: +0.338).
- Standard error 0.772; **95% CI -1.41 to +2.08 min/yr; p = 0.67**; R2 = 0.021.
- The adjusted series comes from a fit on the same 2015-2024 years (intercept 104.3, slope 0.0518 min per storm county-day, after decision D22), so it is model-based and its uncertainty is understated by this CI.
- **Wording to defend:** "After the exploratory weather adjustment, there is no clear trend since 2015: about +0.3 minutes a year, with a 95% range from roughly -1.4 to +2.1." B's "no clear trend since 2015" is right; avoid "flat" or "has not moved" (the README's older wording) because the interval is wide.

## B0 Bedford city check (storm index)

**Status: fixed by decision D22 (orchestrator ruling, 1 Nov 2026); see the D22 re-check section. The "pre-D22" columns below recompute the old index from staging.**

**Finding.** Yes, Bedford city was counted twice in the committed storm index. EIA-861's 2025 Service Territory file
still lists "Bedford City" for Dominion, so `STG.DOMINION_VA_COUNTIES` has 104 entries (103 real counties and cities
plus 51515), and NOAA's zone lookup maps forecast zone 34 to both Bedford County (51019) and the City of Bedford (51515).
Every zone-34 storm therefore adds two county-days for one area. The defunct code adds 38 county-days over 2013-2025 (1 in 2024, 5 in 2025); 38 of its 38 days are also Bedford County days. Folding 51515 into 51019 changes F04 and F05 slightly (table below); no conclusion changes. **Nothing has been changed:** the fix was later applied in `STORM_INDEX` itself (sql/05, decision D22).

Mapping:

```sql
SELECT d.eia_county, d.county_id_fips, z.zone, z.county_name AS noaa_lookup_name
FROM stg.DOMINION_VA_COUNTIES d
LEFT JOIN raw.NOAA_ZONE_COUNTY z ON z.state = 'VA' AND LPAD(z.fips, 5, '0') = d.county_id_fips
WHERE d.county_id_fips IN ('51019', '51515')
ORDER BY 2
```

| EIA county | FIPS | NOAA zone | NOAA lookup name |
|---|---|---|---|
| Bedford | 51019 | 34 | Bedford |
| Bedford City | 51515 | 34 | City of Bedford |

Storm county-days per year, committed and with 51515 folded into 51019:

```sql
WITH ev AS (
  SELECT year, county_id_fips, begin_yearmonth, begin_day
  FROM stg.NOAA_VA_EVENTS
  WHERE county_id_fips IN (SELECT county_id_fips FROM stg.DOMINION_VA_COUNTIES WHERE county_id_fips IS NOT NULL)
    AND line_risk <> 'other'
),
committed AS (SELECT year, COUNT(*) AS storm_county_days FROM (SELECT DISTINCT * FROM ev) GROUP BY 1),
city AS (
  SELECT year, COUNT(*) AS bedford_city_days,
         COUNT(*) FILTER (WHERE also_county) AS city_days_also_on_county
  FROM (
    SELECT DISTINCT c.year, c.begin_yearmonth, c.begin_day,
           EXISTS (SELECT 1 FROM ev k WHERE k.county_id_fips = '51019' AND k.year = c.year
                     AND k.begin_yearmonth = c.begin_yearmonth AND k.begin_day = c.begin_day) AS also_county
    FROM ev c WHERE c.county_id_fips = '51515')
  GROUP BY 1),
folded AS (
  SELECT year, COUNT(*) AS storm_county_days_folded
  FROM (SELECT DISTINCT year, CASE WHEN county_id_fips = '51515' THEN '51019' ELSE county_id_fips END AS fips,
                        begin_yearmonth, begin_day FROM ev)
  GROUP BY 1)
SELECT c.year, c.storm_county_days, COALESCE(b.bedford_city_days, 0) AS bedford_city_days,
       COALESCE(b.city_days_also_on_county, 0) AS city_days_also_on_county,
       f.storm_county_days_folded, c.storm_county_days - f.storm_county_days_folded AS difference
FROM committed c JOIN folded f USING (year) LEFT JOIN city b USING (year)
ORDER BY c.year
```

| Year | Pre-D22 (unfolded) | Bedford city days | ... also a Bedford County day | Folded (= mart.STORM_INDEX after D22) | Difference |
|---:|---:|---:|---:|---:|---:|
| 2013 | 376 | 2 | 2 | 374 | 2 |
| 2014 | 586 | 3 | 3 | 583 | 3 |
| 2015 | 526 | 5 | 5 | 521 | 5 |
| 2016 | 597 | 3 | 3 | 594 | 3 |
| 2017 | 420 | 1 | 1 | 419 | 1 |
| 2018 | 687 | 4 | 4 | 683 | 4 |
| 2019 | 851 | 3 | 3 | 848 | 3 |
| 2020 | 431 | 2 | 2 | 429 | 2 |
| 2021 | 676 | 3 | 3 | 673 | 3 |
| 2022 | 723 | 5 | 5 | 718 | 5 |
| 2023 | 391 | 1 | 1 | 390 | 1 |
| 2024 | 465 | 1 | 1 | 464 | 1 |
| 2025 | 796 | 5 | 5 | 791 | 5 |

Weather fit (2015-2024, n = 10) both ways:

```sql
-- same join as sql/05 Q6b and sql/07, run once with each storm count
SELECT s.year, s.storm_county_days, f.saidi_ex_med
FROM mart.STORM_INDEX s JOIN mart.FCT_RELIABILITY f ON f.year = s.year AND f.utility_key = '19876|VA'
ORDER BY s.year
```

Python: `scipy.stats.pearsonr` and `linregress` on the 2015-2024 rows; weather-adjusted = actual - predicted + 2015-2024 mean (sql/07).

| Quantity | Pre-D22 | 51515 folded into 51019 (D22) |
|---|---:|---:|
| Storm county-days 2024 -> 2025 (F04) | 465 -> 796 | 464 -> 791 |
| r, storm county-days vs SAIDI ex-MED (F05) | 0.696 (p = 0.025) | 0.697 (p = 0.025) |
| Fit slope, min per storm county-day | 0.0514 | 0.0518 |
| Fit intercept | 104.4 | 104.3 |
| Predicted 2025 SAIDI ex-MED (actual 144.4) | 145.3 | 145.3 |
| Weather-adjusted 2025 | 133.1 | 133.1 |
| Trend of weather-adjusted 2015-2025, min/yr (Q10) | +0.34 (p = 0.67) | +0.34 (p = 0.67) |

Committed outputs that would change with the fix: `mart.STORM_INDEX`, `V_STORM_VS_SAIDI`, `SAIDI_WEATHER_ADJUSTED`, `data/output/storm_index.csv`, `data/output/storm_vs_saidi.csv`, `data/output/saidi_weather_adjusted.csv`, the check comments in sql/05 and sql/07, `scripts/check_output_metrics.py` expectations, and every place that quotes 465, 796, 0.70 or 145.3.

## D22 re-check: numbers that depend on the storm index

Decision D22 (fix ordered by the orchestrator at 08:16) folds Bedford city (51515) into Bedford County (51019) in `STORM_INDEX` (sql/05). Everything downstream was rebuilt (`run_local_duckdb_sources.py`: T7-T31 pass; `check_output_metrics.py` passes with the D22 expectations) and the committed `storm_index.csv`, `storm_vs_saidi.csv` and `saidi_weather_adjusted.csv` were re-exported. Use the new F04 pair, **464 -> 791**, everywhere; the headline correlation, prediction and weather-adjusted value are unchanged at the precision quoted.

| Quantity | Pre-D22 | After D22 | Status |
|---|---|---|---|
| Storm county-days 2024 -> 2025 (F04) | 465 -> 796 | 464 -> 791 | changed |
| Storm county-days 2019 (record year) | 851 | 848 | changed |
| r, storm county-days vs SAIDI ex-MED, 2015-2024 (F05) | 0.696 (0.70) | 0.697 (0.70), p = 0.025 | unchanged at 2 dp |
| r with SAIFI ex-MED | 0.41 | 0.41 | unchanged |
| Fit slope, min per storm county-day | 0.0514 | 0.0518 | changed |
| Fit intercept | 104.4 | 104.3 | changed |
| Predicted 2025 SAIDI ex-MED | 145.27 (145.3) | 145.25 (145.3) | unchanged at 1 dp |
| Weather-adjusted 2025 | 133.13 (133.1) | 133.15 (SQL: 133.1) | unchanged at 1 dp |
| Weather-adjusted 2019 | 135.8 | 135.7 | changed |
| Q10 slope of weather-adjusted SAIDI, 2015-2025 | +0.34 min/yr, 95% CI -1.41 to +2.09, p 0.67 | +0.34 min/yr, 95% CI -1.41 to +2.08, p 0.67 | unchanged at 2 dp |
| A1 storm vs calm county-days | 11.9x (7.9 to 16.9) | 11.9x (7.9 to 16.9) | unchanged: the county-day panel already folded 51515 into 51019 |

```sql
SELECT s.year, s.storm_county_days, f.saidi_ex_med, f.saifi_ex_med
FROM mart.STORM_INDEX s JOIN mart.FCT_RELIABILITY f ON f.year = s.year AND f.utility_key = '19876|VA'
ORDER BY s.year
;
SELECT year, weather_adjusted_saidi FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year
```

Python: `scipy.stats.pearsonr` and `linregress` on the 2015-2024 rows (fit), and on 2015-2025 for the Q10 trend; the A1 ratio is read from the A1 section, re-run after D22. Snowflake: not rebuilt. `RELIABILITY.MART.STORM_INDEX`, `V_STORM_VS_SAIDI` and `SAIDI_WEATHER_ADJUSTED` in Snowflake still hold the pre-D22 values until the owner re-runs sql/05 and sql/07 (this run is add-only and does not replace existing objects). The Power BI workbook `powerbi/Dominion_Reliability_PowerBI_Data.xlsx` (sheet `StormIndex`) also holds pre-D22 values; the report should bind to `data/output/storm_vs_saidi.csv` instead.

## Quick checks for the orchestrator (batch 3, after D22)

### Q-1 Reconciliation scope: Virginia only vs Virginia + North Carolina

**Answer.** Virginia only gives **130.22 and 133.01**, which print as 130 and 133: both of the annual report's figures. Virginia + North Carolina, customer-weighted each year and then averaged over the three years (the scorecard's method), gives **129.492 and 132.502**, which print as **129** and 133 (132.502 is just above the half); pooling the three years instead gives 129.48 and 132.58 (129 and 133). So only the Virginia-only rebuild reproduces both printed numbers: with North Carolina the 2022-24 average prints as 129, not 130. North Carolina is 4.8% of the customers and had lower SAIDI in 2022 and 2024. The rise is about three minutes either way (+2.78 Virginia, +3.01 with North Carolina).

**Defensible line:** "Rebuilt from EIA-861, Virginia's rows reproduce both of Dominion's figures, 130 and 133. Adding North Carolina gives 129.5 and 132.5, so the printed figures fit Virginia; either way the rise is about three minutes. The report doesn't state its scope, so I'd confirm it with the reliability team."

**Caveat.** Dominion computes these from its own outage records, not from its EIA-861 filing, so a half-minute gap could also come from different customer counts or data vintages: this is consistency with a Virginia-only scope, not proof. R's note in `research/for_B.md` ("inference: probably system-wide") is not supported by this arithmetic.

| Year | Customers VA | Customers NC | SAIDI VA | SAIDI NC | SAIDI VA + NC | Standard |
|---:|---:|---:|---:|---:|---:|---|
| 2022 | 2,589,282 | 131,263 | 136.047 | 114.675 | 135.016 | Other |
| 2023 | 2,612,104 | 132,021 | 123.322 | 130.149 | 123.650 | Other |
| 2024 | 2,635,267 | 132,502 | 131.300 | 100.200 | 129.811 | Other |
| 2025 | 2,675,735 | 133,095 | 144.400 | 136.900 | 144.045 | Other |

| Three-year average | Virginia only | VA + NC (mean of annual values) | VA + NC (pooled) | Annual report |
|---|---:|---:|---:|---:|
| 2022-24 | 130.22 | 129.49 | 129.48 | 130 |
| 2023-25 | 133.01 | 132.50 | 132.58 | 133 |

```sql
WITH y AS (
  SELECT year,
         SUM(CASE WHEN state = 'VA' THEN customers END)                                   AS customers_va,
         SUM(CASE WHEN state = 'NC' THEN customers END)                                   AS customers_nc,
         SUM(CASE WHEN state = 'VA' THEN cust_minutes_ex_med END)
           / SUM(CASE WHEN state = 'VA' THEN customers END)                               AS saidi_va,
         SUM(CASE WHEN state = 'NC' THEN cust_minutes_ex_med END)
           / SUM(CASE WHEN state = 'NC' THEN customers END)                               AS saidi_nc,
         SUM(cust_minutes_ex_med) / SUM(customers)                                        AS saidi_va_nc,
         SUM(cust_minutes_ex_med) AS cust_minutes, SUM(customers) AS customers,
         STRING_AGG(DISTINCT standard, ', ')                                              AS standards
  FROM mart.FCT_RELIABILITY
  WHERE utility_id = 19876 AND state IN ('VA', 'NC') AND year BETWEEN 2022 AND 2025
  GROUP BY year ORDER BY year
)
SELECT p.period,
       AVG(y.saidi_va)    AS saidi_va_3yr,      -- mean of the annual customer-weighted values (the scorecard's method)
       AVG(y.saidi_va_nc) AS saidi_va_nc_3yr,
       SUM(y.cust_minutes) / SUM(y.customers) AS saidi_va_nc_pooled  -- sensitivity: three years pooled
FROM y JOIN (SELECT '2022-24' AS period, 2022 AS y0 UNION ALL SELECT '2023-25', 2023) p
  ON y.year BETWEEN p.y0 AND p.y0 + 2
GROUP BY p.period ORDER BY p.period
```

Both states file under EIA's "Other" standard (Dominion's own major-event rule) in every year shown, so the two states' ex-MED values are on the same basis. `cust_minutes_ex_med` = SAIDI x customers per state (`02_mart.sql`), so the VA + NC value is the customer-weighted SAIDI of the two states together.

### Q-2 Weather-fit arithmetic from the unrounded r (after D22)

**Answer.** r = **0.6973** (n = 10, 2015-2024). t = r x sqrt((n - 2) / (1 - r^2)) = **2.752** on 8 df, two-sided p = **0.0250**. 95% interval for r by Fisher z (z = atanh r, SE = 1 / sqrt(n - 3), z +/- 1.96 SE, back with tanh): **0.121 to 0.922**, i.e. 0.12 to 0.92. R's t = 2.77 and 0.13 to 0.92 are right for r = 0.70 exactly (t 2.772, interval 0.126 to 0.923); from the unrounded r they become t = 2.75 and 0.12 to 0.92.

Cross-check: `scipy.stats.linregress` on the same ten rows gives slope t = 2.752 and p = 0.0250, the same test as t for r.

```sql
SELECT CORR(saidi_ex_med, storm_county_days) AS r, COUNT(*) AS n
FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024
```

Defensible wording: "r = 0.70 on ten years (t = 2.75, p = 0.025); the 95% interval runs from about 0.12 to 0.92, so the data are consistent with anything from a weak to a very strong association. That is why the slide leads with the county-day comparison."

### Q-3 The peer-set rule (docs/04 D10), quoted exactly

> Twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before results were computed.

The rest of the decision, also verbatim:

> Southeast: Duke Carolinas, Duke Progress, Georgia Power, Alabama Power, Dominion SC. Mid-Atlantic (PJM): BGE, Pepco, PECO, PPL. Florida: FPL, Duke Energy Florida. Plus Dominion VA. Appalachian Power (VA) is held in a separate group and shown separately because its SAIDI exceeds 300 minutes and would compress the scale of every chart.

`DIM_UTILITY` assigns exactly these by EIA ID: 12 utility-states including Dominion VA, plus Appalachian Power (VA) in its own group.

| Peer group | Utility key | Utility |
|---|---|---|
| Appalachian Power (VA) | 733|VA | Appalachian Power Co |
| Dominion Energy Virginia | 19876|VA | Virginia Electric & Power Co |
| Florida IOU peer | 6455|FL | Duke Energy Florida, LLC |
| Florida IOU peer | 6452|FL | Florida Power & Light Co |
| Mid-Atlantic IOU peer | 1167|MD | Baltimore Gas & Electric Co |
| Mid-Atlantic IOU peer | 14940|PA | PECO Energy Co |
| Mid-Atlantic IOU peer | 14715|PA | PPL Electric Utilities Corp |
| Mid-Atlantic IOU peer | 15270|MD | Potomac Electric Power Co |
| Southeast IOU peer | 195|AL | Alabama Power Co |
| Southeast IOU peer | 17539|SC | Dominion Energy South Carolina, Inc |
| Southeast IOU peer | 5416|NC | Duke Energy Carolinas, LLC |
| Southeast IOU peer | 3046|NC | Duke Energy Progress - (NC) |
| Southeast IOU peer | 7140|GA | Georgia Power Co |

```sql
SELECT peer_group, utility_key, utility_name FROM mart.DIM_UTILITY
WHERE peer_group IN ('Dominion Energy Virginia', 'Southeast IOU peer', 'Mid-Atlantic IOU peer', 'Florida IOU peer', 'Appalachian Power (VA)')
ORDER BY peer_group, utility_name
```

## A1 County-day panel: storm days vs calm days

**Finding (S4 headline candidate).** On county-days with a NOAA damaging-wind, winter-storm or tropical report, outage customer-hours per 1,000 customers were **11.9 times** those of county-days without one (95% CI 7.9 to 16.9; 6,108 storm and 373,851 calm county-days in 99 Dominion counties, 2015-2025). In plain terms: an average storm county-day cost 333 customer-hours per 1,000 customers, a calm one 27.9. The gap holds on non-major days, in Dominion-only counties, in both halves of the period and in every year (table below). 67% of storm county-days had a heavy outage (10 or more customer-hours per 1,000 customers), against 15.1% of calm ones. This is an association: NOAA storm reports are partly triggered by damage, so the ratio is not the storm's causal effect.

Suggested slide line: "On county-days with a storm report, outages cost about 12 times as many customer-hours per 1,000 customers as on calm days (6,108 storm county-days, 2015-2025)."

```sql
SELECT d.county_fips, d.day, d.year, d.dominion_only_county, d.customer_hours_per_1k,
       d.storm_day, d.storm_wind, d.storm_winter, d.storm_tropical, t.is_med_proxy
FROM mart.FCT_COUNTY_DAY d
JOIN mart.FCT_TERRITORY_DAY t ON t.day = d.day
WHERE d.failed_readings = 0                                    -- complete county-days only
  AND d.county_fips NOT IN ('51600', '51683', '51660', '51520') -- A3 map exclusions (docs/03 P26, P27)
```

Ratio of means (storm / calm). 95% CI: 2,000 bootstrap resamples of whole days (seed 20261101), so county-days hit by the same storm move together. Complete county-days only (no failed EAGLE-I reading that day): 379,959 of 413,854.

| Subset | Storm county-days | Calm county-days | Mean storm | Mean calm | Ratio | 95% CI |
|---|---:|---:|---:|---:|---:|---|
| All complete county-days, 2015-2025 | 6,108 | 373,851 | 332.8 | 27.86 | 11.9 | 7.9 to 16.9 |
| Excluding proxy major event days | 4,950 | 365,133 | 133.5 | 13.54 | 9.9 | 8.6 to 11.3 |
| Dominion-only counties | 1,065 | 120,154 | 368.8 | 18.56 | 19.9 | 11.2 to 32.5 |
| 2015-2019 | 2,920 | 174,184 | 264.7 | 26.47 | 10.0 | 4.9 to 18.9 |
| 2020-2025 | 3,188 | 199,667 | 395.2 | 29.08 | 13.6 | 8.6 to 20.3 |
| Storm type: wind (thunderstorm, high wind, tornado) | 4,602 | 373,851 | 309.5 | 27.86 | 11.1 | 7.8 to 15.9 |
| Storm type: winter (ice, snow, sleet, blizzard) | 1,419 | 373,851 | 371.8 | 27.86 | 13.3 | 3.4 to 26.8 |
| Storm type: tropical | 93 | 373,851 | 1322.0 | 27.86 | 47.4 | 1.5 to 116.8 |

By year:

| Year | Storm county-days | Ratio | 95% CI |
|---:|---:|---:|---|
| 2015 | 505 | 6.2 | 2.8 to 11.9 |
| 2016 | 581 | 7.7 | 4.1 to 13.4 |
| 2017 | 412 | 10.3 | 5.7 to 17.3 |
| 2018 | 652 | 9.8 | 2.2 to 24.5 |
| 2019 | 770 | 9.5 | 6.5 to 13.4 |
| 2020 | 365 | 27.4 | 6.8 to 62.5 |
| 2021 | 592 | 12.7 | 2.5 to 33.2 |
| 2022 | 711 | 12.1 | 5.2 to 23.9 |
| 2023 | 386 | 19.0 | 12.2 to 28.2 |
| 2024 | 457 | 14.2 | 7.4 to 24.1 |
| 2025 | 677 | 5.9 | 3.0 to 10.6 |

**Chart-ready table:** `interview-prep/work/data/output/a1_storm_vs_calm.csv` (the two tables above, one row per subset or year).

**Caveats.**
- EAGLE-I counts every utility in a county; Dominion-only counties give the same reading.
- Storm flags are NOAA line-risk reports (wind, winter, tropical) on the event's begin date in that county (decision D5); a storm that starts at night and causes outages the next day counts the second day as calm, which biases the ratio down.
- County-days with any failed EAGLE-I reading are dropped (most of August to November 2025), and four counties with unusable EAGLE-I data (Fairfax city, Manassas, Harrisonburg, Bristol) are left out.
- No count model was fitted: the stratified ratio and its bootstrap interval already answer the slide's question, and every subset points the same way.

## A2 The ten largest outage events in Dominion counties, November 2014 to 2025

**Finding.** The ten largest outage events in the 103 counties Dominion serves were three tropical storms (Michael 2018, Isaias 2020, Matthew 2016), two winter storms (January 2022 snow, February 2021 ice) and five wind events. The largest, Michael (11-12 October 2018), had 545,548 customers out for a full hour (all utilities in those counties); half the excess was restored 15.8 hours after the peak and 90% after 60.5 hours. Winter storms took longest to restore: about 100 hours to 90% for both the January 2022 snowstorm and the February 2021 ice storm. There is no clear change in restoration speed: across the 47 events that kept 50,000 or more customers out for an hour, after allowing for event size, hours to 90% restored moved +4.6% a year (95% CI -0.5% to +9.8%, p = 0.07, not significant); the median was 19.6 hours in 2015-2019 (18 events) and 23.5 hours in 2020-2025 (29 events). Say "no evidence that restoration got faster", not "it got slower".

**Chart-ready tables** (`data/output/`): `outage_events_top10.csv` (this table), `fct_event_context.csv` (all 486 territory events with storm type, tropical cyclone and DOE-417 match), `fct_restoration_curve.csv` (hour-by-hour curves for the events that peaked at 50,000 or more; slice on `event_key`).

| # | Start (EST) | Peak (EST) | Storm type | Tropical cyclone | Peak out | Held 1 h | Hours above 10k | Customer-hours (m) | h50 | h90 | h99 | DOE-417 customers |
|---:|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 2018-10-11 | 2018-10-12 | tropical | Michael | 558,729 | 545,548 | 111.3 | 17.78 | 15.8 | 60.5 | 106.8 |  |
| 2 | 2018-03-01 | 2018-03-02 | wind |  | 419,136 | 401,776 | 106.0 | 13.16 | 18.8 | 55.0 | 104.5 |  |
| 3 | 2020-08-04 | 2020-08-04 | tropical | Isaias | 351,738 | 343,492 | 70.5 | 6.17 | 8.3 | 33.5 | 72.8 | 508,000 |
| 4 | 2022-01-03 | 2022-01-03 | winter |  | 314,644 | 308,015 | 150.0 | 13.69 | 21.3 | 102.8 | 167.0 |  |
| 5 | 2021-02-13 | 2021-02-13 | winter |  | 281,707 | 271,359 | 229.0 | 16.48 | 40.5 | 101.5 | 265.0 |  |
| 6 | 2016-10-08 | 2016-10-09 | tropical | Matthew | 269,298 | 265,401 | 74.3 | 8.01 | 11.3 | 52.8 | 77.8 |  |
| 7 | 2016-06-16 | 2016-06-16 | wind |  | 234,951 | 233,003 | 88.5 | 7.03 | 19.5 | 65.8 | 97.3 |  |
| 8 | 2025-06-19 | 2025-06-19 | wind |  | 225,609 | 209,475 | 31.0 | 2.09 | 4.5 | 22.0 | 36.8 |  |
| 9 | 2025-02-12 | 2025-02-16 | wind |  | 187,074 | 172,538 | 135.5 | 8.2 | 3.0 | 20.3 | 29.0 |  |
| 10 | 2018-05-14 | 2018-05-14 | wind |  | 159,532 | 151,385 | 27.8 | 1.45 | 4.5 | 20.0 | 50.0 | 112,000 |

```sql
SELECT ROW_NUMBER() OVER (ORDER BY peak_sustained_1h DESC) AS rank,
       start_day, CAST(peak_utc - INTERVAL '5 HOUR' AS DATE) AS peak_day, storm_type, tropical_cyclone,
       peak_customers_out, peak_sustained_1h,
       ROUND(hours_above_threshold, 1) AS hours_above_10k,
       ROUND(customer_hours / 1e6, 2)  AS customer_hours_m,
       ROUND(hours_to_50pct, 1) AS h50, ROUND(hours_to_90pct, 1) AS h90, ROUND(hours_to_99pct, 1) AS h99,
       doe417_customers_max, starts_on_med_proxy_day, event_key
FROM mart.FCT_EVENT_CONTEXT
ORDER BY peak_sustained_1h DESC
LIMIT 10
```

**Did restoration get faster?** Events with at least 50,000 customers out for an hour, 2015-2025:

```sql
SELECT event_key, year, start_day, peak_sustained_1h, hours_to_50pct, hours_to_90pct, storm_type
FROM mart.FCT_EVENT_CONTEXT
WHERE peak_sustained_1h >= 50000 AND hours_to_90pct IS NOT NULL
ORDER BY start_day
```

OLS on those 47 events: ln(hours) = a + b x (year - 2020) + c x ln(peak held 1 h); `numpy.linalg.lstsq`, t-based 95% CI.

| Measure | Change per year, size-adjusted | 95% CI | p |
|---|---:|---|---:|
| Hours to 50% restored | +1.2% | -4.6% to +7.4% | 0.68 |
| Hours to 90% restored | +4.6% | -0.5% to +9.8% | 0.07 |

Size matters more than the year: each doubling of the peak multiplies hours to 90% by 1.56. Spearman rank correlation of hours to 90% with year: rho = 0.17 (p = 0.25); Mann-Whitney 2015-19 vs 2020-25: p = 0.27.

**Restoration curve, Tropical Storm Isaias (peak 04 Aug 2020).** Chosen for the inset because it is the largest event with a matching DOE-417 report (Virginia, 508,000 customers affected; EAGLE-I's simultaneous peak for all utilities in the 103 counties was 351,738). Share of the excess over the pre-event background restored, by hours since the peak:

```sql
SELECT hour_since_peak, customers_out, ROUND(share_restored, 3) AS share_restored
FROM mart.FCT_RESTORATION_CURVE
WHERE event_key = (SELECT event_key FROM mart.FCT_EVENT_CONTEXT WHERE tropical_cyclone LIKE '%ISAIAS%')
ORDER BY hour_since_peak
```

| Hours since peak | Customers out (hourly max) | Share restored |
|---:|---:|---:|
| 0 | 351,738 | 0% |
| 6 | 224,838 | 36% |
| 12 | 140,213 | 60% |
| 24 | 93,942 | 74% |
| 36 | 26,380 | 93% |
| 48 | 16,110 | 96% |
| 72 | 6,319 | 99% |
| 96 | 1,806 | 100% |
| 120 | 439 | 100% |
| 144 | 556 | 100% |
| 167 | 623 | 100% |

**Caveats.**
- EAGLE-I counts every utility's customers in a county, so these events include co-op and municipal customers in the 103 counties Dominion serves (the Dominion-county rule is in `DIM_COUNTY.dominion_county_rule`). They are not Dominion's own event records.
- "Held 1 h" ranks events by the highest level held for four consecutive 15-minute readings, so a 45-minute spike (30 Jul 2019, 159,742 for under an hour in Hampton Roads) does not rank above multi-day storms. Restoration times ignore one-reading collection drops (the series must stay below the level for 3 hours).
- Hours to X% are measured from the peak, against the excess over the median of the 24 hours before the event. The 2025-02-12 event merges the 12 February and 15-16 February storms, because the territory never fell below 10,000 out for 3 hours in between.
- Storm type comes from NOAA line-risk reports in Dominion counties on the event's days; the tropical label also uses HURDAT2 tracks within 400 km of Richmond. DOE-417 has no utility column: the match rule is in sql/11 (decision D19).
- The trend test has few events and wide intervals; "no measurable change" is not "no change".

## A3 Non-major outage events and minutes by county, 2015-2025 (map table)

**Finding.** On days that are not proxy major event days, customers in the 103 Dominion counties (all utilities) averaged 195 outage minutes a year over 2015-2024, with a wide spread between counties: among counties with 20,000 or more customers, from 55 minutes (Prince William County) to 633 (Pittsylvania County). The highest are rural and exurban counties; the lowest are dense cities and inner suburbs. County outage events on non-major days rose from 9.5 per 10,000 customers a year (2015-2019 average) to 10.0 (2020-2024), and 59 of the 99 mapped counties had more events per customer in 2020-2024 than in 2015-2019. Counties with more storm days had more outage minutes (r = 0.19 across the 99 mapped counties; 0.49 across the 35 with 20,000 or more customers): an association, not a cause. 4 counties are left off the map: Fairfax city (implausible readings 2018-2020 (docs/03 P26)); Harrisonburg city (almost no EAGLE-I readings (municipal utility)); Bristol city (almost no EAGLE-I readings (municipal utility)); Manassas city (almost no EAGLE-I readings (municipal utility)).

**Chart-ready tables** (`data/output/`): `county_outage_map.csv` (one row per Dominion county with `map_flag`; join `county_fips` to `va_counties.topojson`), `fct_county_year.csv` (county x year, 2015-2025).

### A3.1 By year

```sql
SELECT year, SUM(events_non_med) AS events_non_med,
       ROUND(10000 * SUM(events_non_med) / SUM(customers_basis), 2) AS events_non_med_per_10k,
       ROUND(60 * SUM(customer_hours_non_med) / SUM(customers_basis), 1) AS minutes_non_med,
       ROUND(SUM(failed_share * customers_basis) / SUM(customers_basis), 3) AS failed_share
FROM mart.FCT_COUNTY_YEAR GROUP BY year ORDER BY year
```

| Year | Non-major county events | Per 10k customers | Outage minutes per customer, non-major days | Failed-reading share |
|---:|---:|---:|---:|---:|
| 2015 | 2,305 | 6.66 | 121.7 | 0.0% |
| 2016 | 3,102 | 8.96 | 176.9 | 0.0% |
| 2017 | 3,179 | 9.18 | 167.5 | 1.6% |
| 2018 | 3,842 | 11.09 | 200.2 | 16.6% |
| 2019 | 4,052 | 11.7 | 250.9 | 17.4% |
| 2020 | 3,719 | 10.74 | 197.4 | 3.6% |
| 2021 | 3,102 | 8.96 | 213.4 | 2.7% |
| 2022 | 3,571 | 10.31 | 214.7 | 0.0% |
| 2023 | 3,450 | 9.96 | 208.3 | 0.0% |
| 2024 | 3,434 | 9.92 | 201.5 | 0.0% |
| 2025 | 3,906 | 11.28 | 202.8 | 11.6% |

### A3.2 Map table (one row per county; top and bottom five shown, counties with 20,000+ customers)

```sql
WITH r AS (
  SELECT county_fips, SUM(readings) AS readings_2015_24
  FROM mart.FCT_COUNTY_DAY WHERE year BETWEEN 2015 AND 2024 GROUP BY 1
),
y AS (
  SELECT c.*, r.readings_2015_24,
         CASE WHEN c.county_fips = '51600' THEN 'excluded: implausible readings 2018-2020 (docs/03 P26)'
              WHEN r.readings_2015_24 < 1000 THEN 'excluded: almost no EAGLE-I readings (municipal utility)'
              ELSE 'ok' END AS map_flag
  FROM mart.FCT_COUNTY_YEAR c JOIN r USING (county_fips)
)
SELECT county_fips, county_label AS county_name, dominion_only_county, MAX(customers_basis) AS customers_basis, map_flag,
       MAX(readings_2015_24) AS readings_2015_24,
       ROUND(60 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN customer_hours_non_med END) / MAX(customers_basis), 1) AS minutes_non_med_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_avg_2015_24,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2015_19,
       ROUND(10000 * AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END) / MAX(customers_basis), 2) AS events_per_10k_2020_24,
       ROUND(10000 * (AVG(CASE WHEN year BETWEEN 2020 AND 2024 THEN events_non_med END)
           - AVG(CASE WHEN year BETWEEN 2015 AND 2019 THEN events_non_med END)) / MAX(customers_basis), 2) AS change_events_per_10k,
       ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2024 THEN storm_days END), 1) AS storm_days_avg_2015_24
FROM y
GROUP BY county_fips, county_label, dominion_only_county, map_flag
ORDER BY minutes_non_med_avg_2015_24 DESC
```

| County | Customers | Minutes, non-major, avg 2015-24 | Events per 10k, 2015-19 | 2020-24 | Storm days a year |
|---|---:|---:|---:|---:|---:|
| Pittsylvania County | 29,827 | 632.9 | 11.6 | 23.2 | 12.3 |
| Henry County | 26,850 | 520.9 | 17.13 | 14.75 | 12.9 |
| Albemarle County | 45,280 | 491.1 | 11.75 | 13.43 | 13.6 |
| Tazewell County | 21,376 | 454.7 | 18.53 | 19.27 | 6.9 |
| Fauquier County | 31,801 | 366.1 | 13.65 | 15.85 | 10.3 |
| Prince William County | 225,231 | 55.4 | 0.53 | 0.51 | 10.0 |
| Richmond city | 112,565 | 58.9 | 1.6 | 0.09 | 1.7 |
| Fairfax County | 513,143 | 91.3 | 0.14 | 0.23 | 15.2 |
| Loudoun County | 187,874 | 94.9 | 0.97 | 1.21 | 13.6 |
| Norfolk city | 116,644 | 104.8 | 2.31 | 2.14 | 4.5 |

**Caveats.**
- EAGLE-I counts every utility's customers in a county: Dominion-only counties (`dominion_only_county`) are the cleanest; elsewhere co-op customers are included. The customer basis is decision D15.
- 2025 is shown but not averaged: EAGLE-I collection failed for 46% of August and 45% of October 2025 county readings (failed-reading share 12% for the year), so 2025 minutes and events are undercounted.
- A county event is 1% or more of the county's customers out (at least 10), readings no more than an hour apart (decision D17); non-major = not starting on a proxy major event day (decision D18). The 1% threshold scales with county size, so events per customer compare a county with itself over time, not one county with another: map outage minutes per customer, and use the event counts for change. Small counties have noisy rates.
- EAGLE-I coverage of Virginia customers was 94-97% in 2018-2022 (its coverage history); earlier years are not published, so part of a rise from 2015 may be coverage. Present the change as "more events recorded", not as a proven change in the grid.

## A4 Load shape, seasonal peaks and sales by sector

**Finding.** In the PJM DOM zone, average demand rose 32% from 2019 to 2025, more at night than in the afternoon: the hours ending 1 to 5 a.m. grew 39.0% to 41.0% and the hours ending 1 to 5 p.m. 26.9% to 27.4%. Winter set the year's peak in 2019, 2022 and 2025 (2026 so far: winter 25,413 MW vs summer 25,384 MW). Weather does not explain the growth: holding Virginia's daily heating and cooling degree days and the weekday at their 2019-2025 pattern, average load rose from 11,438 MW (2019) to 15,235 MW (2025), +33%, against +32% unadjusted. Dominion's commercial sales per commercial customer rose from 156 MWh (2013) to 238 MWh (2025); residential use per customer fell slightly. Nothing here identifies which customers drove the growth (decision D14).

**Chart-ready tables** (`data/output/`): `dom_load_profile.csv` (24 rows, S5), `dom_load_hour_month.csv` (year x month x hour, heatmap), `dom_seasonal_peak.csv` (year x season with date and hour), `fct_sales_sector.csv` (year x class), `dom_load_daily.csv` (daily load with degree days).

### A4.1 Hour-of-day growth, 2019 to 2025 (S5)

```sql
SELECT hour_no, avg_mw_2019, avg_mw_2025, growth_pct FROM mart.DOM_LOAD_PROFILE ORDER BY hour_no
```

```sql
SELECT ROUND(100 * (AVG(CASE WHEN YEAR(data_date) = 2025 THEN demand_mw END)
                     / AVG(CASE WHEN YEAR(data_date) = 2019 THEN demand_mw END) - 1), 1) AS all_hours_growth_pct
FROM stg.EIA930_DOM_HOURLY
```

| Hour ending | Avg MW 2019 | Avg MW 2025 | Growth |
|---:|---:|---:|---:|
| 1 | 10,273 | 14,279 | +39.0% |
| 2 | 9,935 | 13,932 | +40.2% |
| 3 | 9,755 | 13,737 | +40.8% |
| 4 | 9,708 | 13,684 | +41.0% |
| 5 | 9,879 | 13,833 | +40.0% |
| 6 | 10,366 | 14,270 | +37.7% |
| 7 | 11,089 | 14,915 | +34.5% |
| 8 | 11,562 | 15,362 | +32.9% |
| 9 | 11,750 | 15,459 | +31.6% |
| 10 | 11,860 | 15,427 | +30.1% |
| 11 | 12,008 | 15,462 | +28.8% |
| 12 | 12,157 | 15,551 | +27.9% |
| 13 | 12,300 | 15,664 | +27.3% |
| 14 | 12,435 | 15,795 | +27.0% |
| 15 | 12,552 | 15,925 | +26.9% |
| 16 | 12,697 | 16,136 | +27.1% |
| 17 | 12,931 | 16,478 | +27.4% |
| 18 | 13,223 | 16,876 | +27.6% |
| 19 | 13,260 | 16,967 | +28.0% |
| 20 | 13,107 | 16,875 | +28.7% |
| 21 | 12,864 | 16,641 | +29.4% |
| 22 | 12,354 | 16,163 | +30.8% |
| 23 | 11,585 | 15,469 | +33.5% |
| 24 | 10,836 | 14,798 | +36.6% |

### A4.2 Seasonal peaks (winter = Dec, Jan, Feb of the same year; summer = Jun, Jul, Aug)

```sql
SELECT year,
       MAX(CASE WHEN season = 'winter' THEN peak_mw END) AS winter_peak_mw,
       MAX(CASE WHEN season = 'winter' THEN peak_date END) AS winter_peak_date,
       MAX(CASE WHEN season = 'summer' THEN peak_mw END) AS summer_peak_mw,
       MAX(CASE WHEN season = 'summer' THEN peak_date END) AS summer_peak_date
FROM mart.DOM_SEASONAL_PEAK GROUP BY year ORDER BY year
```

| Year | Winter peak MW | Date | Summer peak MW | Date | Higher |
|---:|---:|---|---:|---|---|
| 2018 | 16,204 | 2018-12-11 00:00:00 | 18,111 | 2018-07-05 00:00:00 | summer |
| 2019 | 19,803 | 2019-01-31 00:00:00 | 19,478 | 2019-07-20 00:00:00 | winter |
| 2020 | 17,468 | 2020-01-22 00:00:00 | 20,073 | 2020-07-20 00:00:00 | summer |
| 2021 | 17,985 | 2021-01-29 00:00:00 | 20,493 | 2021-08-12 00:00:00 | summer |
| 2022 | 22,415 | 2022-12-24 00:00:00 | 21,274 | 2022-08-09 00:00:00 | winter |
| 2023 | 19,635 | 2023-02-04 00:00:00 | 22,050 | 2023-07-28 00:00:00 | summer |
| 2024 | 22,152 | 2024-01-17 00:00:00 | 23,220 | 2024-07-16 00:00:00 | summer |
| 2025 | 24,957 | 2025-01-23 00:00:00 | 23,905 | 2025-06-24 00:00:00 | winter |
| 2026 | 25,413 | 2026-02-09 00:00:00 | 25,384 | 2026-07-03 00:00:00 | winter |

2018 starts on 1 July 2018 (no June, so its summer peak covers July and August only, and its winter peak is December 2018 only); 2026 runs to 30 October, so its winter is January and February only. The 2026 gap is 29 MW: call it a tie.

### A4.3 Sales by sector, Dominion Energy Virginia (EIA-861)

```sql
SELECT customer_class, year, ROUND(sales_mwh / 1e6, 2) AS sales_twh, customers, mwh_per_customer
FROM mart.FCT_SALES_SECTOR
WHERE customer_class IN ('residential', 'commercial', 'industrial') AND year IN (2013, 2019, 2025)
ORDER BY customer_class, year
```

| Class | Year | Sales TWh | Customers | MWh per customer |
|---|---:|---:|---:|---:|
| commercial | 2013 | 39.08 | 251,209 | 155.6 |
| commercial | 2019 | 45.13 | 260,250 | 173.4 |
| commercial | 2025 | 64.62 | 271,320 | 238.2 |
| industrial | 2013 | 6.39 | 477 | 13,404.4 |
| industrial | 2019 | 6.56 | 588 | 11,156.3 |
| industrial | 2025 | 5.5 | 1,009 | 5,452.9 |
| residential | 2013 | 28.8 | 2,105,500 | 13.7 |
| residential | 2019 | 29.83 | 2,245,174 | 13.3 |
| residential | 2025 | 30.01 | 2,408,901 | 12.5 |

```sql
SELECT year, customer_class, ROUND(100 * sales_mwh / SUM(sales_mwh) OVER (PARTITION BY year), 1) AS share_pct
FROM mart.FCT_SALES_SECTOR WHERE year IN (2013, 2025) ORDER BY year, customer_class
```

Share of retail sales: 2013 commercial 52.5%, industrial 8.6%, residential 38.7%, transportation 0.3%; 2025 commercial 64.3%, industrial 5.5%, residential 29.9%, transportation 0.3%.
Sales include delivery-only service (customers buying energy elsewhere); 2025 commercial delivery-only sales were 4.53 TWh of 64.62.
Industrial customer counts more than doubled while industrial sales fell; that looks like reclassification between classes and is not used.

### A4.4 Degree-day-normalised trend (exploratory)

```sql
SELECT data_date, year, iso_weekday, avg_mw, hdd, cdd
FROM mart.DOM_LOAD_DAILY
WHERE year BETWEEN 2019 AND 2025 AND hours_reported >= 20 AND hdd IS NOT NULL
```

OLS on 2,547 days (2019-2025, days with 20 or more reported hours): daily average MW on HDD, CDD, their squares, weekday and year dummies (R2 = 0.955; `numpy.linalg.lstsq`). Normalised average = the model's mean prediction for that year over all 2,547 days' weather and weekdays. Degree days are Virginia's population-weighted state values (NOAA CPC), used for a zone that also covers a sliver of North Carolina.

| Year | Actual avg MW | Normalised avg MW | HDD | CDD |
|---:|---:|---:|---:|---:|
| 2019 | 11,687 | 11,438 | 3,907 | 1,491 |
| 2020 | 11,510 | 11,658 | 3,705 | 1,265 |
| 2021 | 12,418 | 12,397 | 3,879 | 1,321 |
| 2022 | 13,118 | 13,003 | 4,202 | 1,217 |
| 2023 | 13,275 | 13,657 | 3,622 | 1,041 |
| 2024 | 14,199 | 14,225 | 3,727 | 1,278 |
| 2025 | 15,404 | 15,235 | 4,216 | 1,208 |

**Caveats.** The DOM zone (EIA-930) is larger than Dominion's retail territory and includes other utilities' load; hourly load by county or customer class is not public, so the night-time growth cannot be tied to a customer type from public data (the "first 90 days" question). Annual averages for 2019-2025 use full years; the normalisation is a descriptive model, not a forecast.

## E1 The EIA-930 cut-off for 2026 demand figures

**One cut-off for every 2026 figure: the last hour with data in the EIA-930 file downloaded on 1 November 2026, the hour ending midnight local time on 29 October 2026 (2026-10-30 04:00 UTC).** The file has rows for 30 October but no demand values yet (last row 2026-10-31 04:00 UTC). Every EIA-930 export in `data/output/` written by `scripts/export_powerbi_csv.py` comes from the rebuild with this cut-off. Write it as "to 29 Oct 2026" (I-03's "30 Oct" was the last row, not the last value).

The committed `data/output/dom_annual.csv` (the original snapshot, kept unchanged) stops a week earlier, at the hour ending midnight on 21 October 2026 (2026-10-22 04:00 UTC, shown as "22 Oct" in the repo): its 2026 row (7032 hours, 117.62 TWh, median 16160.0, average 16726.0) equals the rebuild cut at 21 October (7032 hours, 117.62 TWh, median 16160, average 16726). B should not use `dom_annual.csv` for 2026.

```sql
SELECT MAX(CASE WHEN demand_mw IS NOT NULL THEN utc_ts END)   AS last_valid_utc,
       MAX(CASE WHEN demand_mw IS NOT NULL THEN local_ts END) AS last_valid_local_hour_ending,
       MAX(utc_ts)                                            AS last_row_utc
FROM stg.EIA930_DOM_HOURLY
```

```sql
SELECT COUNT(*) AS hours, ROUND(SUM(demand_mw) / 1e6, 2) AS energy_twh, ROUND(MEDIAN(demand_mw)) AS median_mw,
       ROUND(AVG(demand_mw)) AS avg_mw, MAX(utc_ts) AS last_utc
FROM stg.EIA930_DOM_HOURLY
WHERE YEAR(data_date) = 2026 AND demand_mw IS NOT NULL AND data_date <= DATE '2026-10-21'  -- and '2026-10-29'
```

| 2026 figure | Committed snapshot (to 21 Oct) | Rebuild (to 29 Oct), use this |
|---|---:|---:|
| Hours reported | 7032 | 7224 |
| Energy, TWh | 117.62 | 120.49 |
| Median MW | 16,160 | 16,079 |
| Average MW | 16,726 | 16,679 |
| Summer peak MW (2026-07-03 00:00:00, hour ending 19) | 25,384 | 25,384 |
| Winter peak MW (2026-02-09 00:00:00, hour ending 8) | 25,413 | 25,413 |

The winter and summer peaks (25,413 vs 25,384 MW, a 29 MW tie) and the top-50 hours are the same under both cut-offs: no hour after 21 October comes near them. Only the 2026 totals, averages and medians differ.

| Export | Last timestamp in the data | Source |
|---|---|---|
| `dom_load_annual.csv` | 2026-10-30 04:00:00 | rebuild (sql/06), all years; 2026 row to the cut-off |
| `dom_top50_hours.csv` | 2026-09-04 20:00:00 | rebuild (sql/06); rank_today ranks every hour to the cut-off |
| `dom_load_profile.csv` | 2026-01-01 05:00:00 | rebuild (sql/07); uses 2019 and 2025 only |
| `dom_load_hour_month.csv` | 2026-10-01 | rebuild (sql/10); last month October 2026, partial |
| `dom_seasonal_peak.csv` | 2026-07-03 | rebuild (sql/10); 2026 winter = Jan-Feb only |
| `dom_load_daily.csv` | 2026-10-29 | rebuild (sql/10) |

Queries for the last timestamps:

```sql
SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL;  -- dom_load_annual.csv
SELECT MAX(utc_ts) FROM mart.DOM_TOP50_HOURS;  -- dom_top50_hours.csv
SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL AND YEAR(data_date) = 2025;  -- dom_load_profile.csv
SELECT MAX(make_date(year, month, 1)) FROM mart.DOM_LOAD_HOUR_MONTH WHERE hours_reported > 0;  -- dom_load_hour_month.csv
SELECT MAX(peak_date) FROM mart.DOM_SEASONAL_PEAK;  -- dom_seasonal_peak.csv
SELECT MAX(data_date) FROM mart.DOM_LOAD_DAILY WHERE hours_reported > 0;  -- dom_load_daily.csv
```

## A5 Reconciliation: rebuilt against reported

**Finding.** Every headline number rebuilt from public files matches its published source: the 3-year SAIDI (130.2 and 133.0 against the reported 130 and 133), the 2024 and 2025 EIA-861 values to the published decimals, the storm county-days rebuilt from the raw NOAA files, and 2025 commercial sales. EAGLE-I, an independent source built from utilities' outage maps, tracks EIA's SAIDI only loosely (2015-2024, n = 10: r = 0.65 on non-major days, p = 0.04; r = 0.53 for all events, p = 0.12) and sits at a different level, because it counts every utility in the 103 counties, uses a proxy major-event rule and misses failed collection runs. EAGLE-I is therefore used for where and when outages happened, never to restate Dominion's SAIDI.

**Chart-ready table:** `interview-prep/work/data/output/a5_reconciliation.csv`.

| Metric | Rebuilt | Reported | Difference | Reported source | Verdict |
|---|---:|---:|---:|---|---|
| 3-year SAIDI ex-MED, 2022-2024 | 130.200 | 130.000 | +0.200 | Dominion annual report (rounded); R checks the page | MATCH (rounding) |
| 3-year SAIDI ex-MED, 2023-2025 | 133.000 | 133.000 | +0.000 | Dominion annual report (rounded); R checks the page | MATCH (rounding) |
| SAIDI ex-MED 2025 | 144.400 | 144.400 | +0.000 | EIA-861 2025 final file | MATCH |
| SAIFI ex-MED 2025 | 1.320 | 1.320 | +0.000 | EIA-861 2025 final file | MATCH |
| CAIDI ex-MED 2025 | 109.394 | 109.394 | +0.000 | EIA-861 2025 final file | MATCH |
| SAIDI all events 2025 | 306.700 | 306.700 | +0.000 | EIA-861 2025 final file | MATCH |
| SAIDI ex-MED 2024 | 131.300 | 131.300 | +0.000 | EIA-861 2024 file (repo uses PUDL) | MATCH |
| SAIFI ex-MED 2024 | 1.210 | 1.210 | +0.000 | EIA-861 2024 file (repo uses PUDL) | MATCH |
| CAIDI ex-MED 2024 | 108.512 | 108.512 | -0.000 | EIA-861 2024 file (repo uses PUDL) | MATCH |
| SAIDI all events 2024 | 172.100 | 172.100 | +0.000 | EIA-861 2024 file (repo uses PUDL) | MATCH |
| Storm county-days 2024 (raw NOAA rebuild) | 464.000 | 464.000 | +0.000 | committed data/output/storm_index.csv | MATCH |
| Storm county-days 2025 (raw NOAA rebuild) | 791.000 | 791.000 | +0.000 | committed data/output/storm_index.csv | MATCH |
| Commercial sales 2025, MWh (bundled + delivery) | 64,620,793.000 | 64,620,793.000 | +0.000 | EIA-861 2025 Sales_Ult_Cust (60,088,202 + 4,532,591) | MATCH |

Queries:

```sql
SELECT year, saidi_all, saifi_all, saidi_ex_med, saifi_ex_med, caidi_ex_med, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year IN (2024, 2025) ORDER BY year
;
SELECT ROUND(AVG(CASE WHEN year BETWEEN 2022 AND 2024 THEN saidi_ex_med END), 1) AS saidi_3yr_2022_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_3yr_2023_25
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA'
;
SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year IN (2024, 2025) ORDER BY year
;
SELECT ROUND(SUM(sales_mwh)) AS mwh FROM mart.FCT_SALES_SECTOR WHERE year = 2025 AND customer_class = 'commercial'
```

EIA-861 values: `Reliability_2024.xlsx` and `Reliability_2025.xlsx` (sheet `Reliability_States`, Dominion VA row, Other Standard columns) read from `data/raw/eia861/f8612024.zip` and `f8612025.zip`. The annual-report figures are R's document check (claims register).

### A5.2 EAGLE-I minutes per customer against EIA SAIDI

```sql
WITH y AS (
  SELECT year, SUM(customer_hours) AS ch_all, SUM(CASE WHEN NOT is_med_proxy THEN customer_hours ELSE 0 END) AS ch_ex_med,
         SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) AS med_proxy_days
  FROM mart.FCT_TERRITORY_DAY GROUP BY year
),
basis AS (SELECT SUM(customers_basis) AS customers FROM mart.DIM_COUNTY WHERE dominion_county)
SELECT y.year, y.med_proxy_days, ROUND(60 * y.ch_all / b.customers, 1) AS eaglei_min_all, ROUND(60 * y.ch_ex_med / b.customers, 1) AS eaglei_min_ex_med,
       f.saidi_all, f.saidi_ex_med
FROM y CROSS JOIN basis b
JOIN mart.FCT_RELIABILITY f ON f.utility_key = '19876|VA' AND f.year = y.year
WHERE y.year BETWEEN 2015 AND 2025 ORDER BY y.year
```

| Year | Proxy MED days | EAGLE-I min, all days | EAGLE-I min, non-major days | EIA SAIDI all events | EIA SAIDI ex-MED |
|---:|---:|---:|---:|---:|---:|
| 2015 | 2.0 | 140.8 | 121.7 | 183.103 | 119.642 |
| 2016 | 15.0 | 494.4 | 176.9 | 199.918 | 138.225 |
| 2017 | 3.0 | 197.0 | 167.5 | 166.67 | 117.41 |
| 2018 | 18.0 | 842.8 | 200.2 | 266.763 | 149.604 |
| 2019 | 5.0 | 299.6 | 250.9 | 260.113 | 149.874 |
| 2020 | 6.0 | 349.2 | 197.4 | 316.999 | 140.989 |
| 2021 | 12.0 | 516.2 | 213.4 | 318.788 | 133.601 |
| 2022 | 14.0 | 555.2 | 214.7 | 421.475 | 136.047 |
| 2023 | 3.0 | 244.4 | 208.3 | 190.198 | 123.322 |
| 2024 | 10.0 | 312.7 | 201.5 | 172.1 | 131.3 |
| 2025 | 15.0 | 466.8 | 202.8 | 306.7 | 144.4 |

Pearson r over 2015-2024 (n = 10): all-events 0.53 (p = 0.116); non-major 0.65 (p = 0.041). 2025 is left out of r because EAGLE-I collection failed for much of August to November 2025.

**Caveats.** EAGLE-I's denominator is the customer basis of decision D15 (3.46 million in the 103 counties, all utilities) against EIA's 2.68 million Dominion customers; its major-event days are a proxy built the IEEE way (D18), not Dominion's own.

## A6 What one minute of SAIDI means (arithmetic only)

**Finding.** For Dominion Energy Virginia in 2025, one minute of SAIDI is one minute for each of its 2,675,735 Virginia customers: **2,675,735 customer-minutes, about 44,596 customer-hours**. The rise in the three-year average behind the scorecard (130.2 -> 133.0) is about 7.5 million customer-minutes, or 124 thousand customer-hours, at 2025 customer numbers. **No dollar value is given:** R's claims register has no verified DOE ICE Calculator or LBNL value-of-reliability source (checked 1 Nov 2026), so the brief's optional order-of-magnitude estimate is skipped.

| Quantity | SAIDI (min, ex-MED) | Customer-minutes | Customer-hours |
|---|---|---:|---:|
| One minute of SAIDI, 2025 | 1 x customers | 2,675,735 customer-minutes | 44,596 customer-hours |
| Three-year average, 2022-24 -> 2023-25 | 130.2 -> 133.0 = +2.78 min | 7,450,138 customer-minutes | 124,169 customer-hours |
| 2024 -> 2025 | 131.3 -> 144.4 = +13.1 min | 35,052,128 customer-minutes | 584,202 customer-hours |
| All of 2025, ex-MED | 144.4 min x 2,675,735 | 386,376,134 customer-minutes | 6,439,602 customer-hours |

```sql
SELECT year, customers, saidi_ex_med, cust_minutes_ex_med
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2022 AND 2025 ORDER BY year
```

**Caveats.** Customer counts differ by year (2022-2024 customers are not 2025's), so the step rows use 2025 customers as an illustration; `cust_minutes_ex_med` is the exact 2025 total. SAIDI is ex-MED (Dominion files under its own major-event rule), so outages on major event days are not in these customer-minutes. Customer-minutes say nothing about who was affected: one customer out for 100 minutes and 100 customers out for one minute count the same.
