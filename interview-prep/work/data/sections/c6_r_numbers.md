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
