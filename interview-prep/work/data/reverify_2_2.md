# D1. Re-verification of MASTER_PROMPT section 2.2

Recomputed 2026-11-01 by agent D from the source files: `data/input/` (EIA-861, PUDL) and the raw NOAA and
EIA-930 downloads in `data/raw/`, rebuilt in DuckDB by `scripts/run_local_duckdb_sources.py` (sql/01, 02, 05, 06, 07;
tests T7-T12 pass) and `scripts/run_local_duckdb.py` (T1-T6 pass). Database:
`data/raw/duckdb/reliability_local.duckdb`. Script: `interview-prep/work/data/d1_reverify.py`.
In Snowflake, read `mart.` as `RELIABILITY.MART.` and `stg.` as `RELIABILITY.STG.`.

| id | Figure in the brief | Recomputed | Verdict | Note |
|---|---|---|---|---|
| F01 | Rolling 3-yr SAIDI ex-MED 130 (2022-24) -> 133 (2023-25) | 130.2 -> 133.0 | **MATCH** | Mean of the annual customer-weighted values (one utility: mean of annual SAIDI). Annual report p.10 states 130 and 133 (document check is R's / A5). |
| F02 | SAIDI ex-MED 123.3 (2023) -> 144.4 (2025), +17%; SAIFI 1.165 -> 1.320, +13%; CAIDI 105.9 -> 109.4, +3% | SAIDI 123.322 -> 144.4 (+17.1%); SAIFI 1.165 -> 1.32 (+13.3%); CAIDI 105.856 -> 109.394 (+3.3%) | **MATCH** | CAIDI is the reported column (109.394 for 2025); SAIDI / SAIFI gives the same to 0.1. |
| F03 | The rise comes mostly from more interruptions, not longer ones | 79% from frequency, 21% from duration (log decomposition, 2023->2025) | **MATCH** | Same as sql/03 Q1b. Decomposition is arithmetic (SAIDI = SAIFI x CAIDI), not a cause. |
| F04 | Storm county-days 464 (2024) -> 791 (2025) (decision D22; 465 -> 796 before Bedford city was folded into Bedford County) | 464 -> 791 | **MATCH** | Rebuilt from the 13 raw NOAA files (831,288 rows) through sql/05 in DuckDB, not read from data/output. D22 folds Bedford city (51515) into Bedford County (51019), so the area counts once. |
| F05 | r = 0.70 between storm county-days and SAIDI ex-MED, 2015-2024 (n = 10); fit predicts 145.3 for 2025 vs 144.4 actual | r = 0.697 (R2 = 0.486, n = 10); predicted 145.25 (145.2516) vs actual 144.4 | **MATCH** | n = 10 annual points; exploratory. Slope 0.0518 min per county-day, intercept 104.3 (after D22). |
| F06 | 2025 all-events SAIDI 306.7 vs 144.4 ex-MED | 306.7 vs 144.4; major-event-day share 53%; customers 2,675,735 | **MATCH** | Test T4 asserts these exact values from Reliability_2025_States.csv. |
| F07 | Dominion has the fourth-highest SAIDI of twelve peers over 2023-25 | Dominion rank 4 of 12 (133.0 min); top three: Duke Energy Carolinas, LLC 179.0; Duke Energy Progress - (NC) 143.8; Georgia Power Co 140.8 | **MATCH** | Peer set D10 (11 IOUs + Dominion; Appalachian Power excluded). Mean of the three annual values, as the DAX measure SAIDI 2023 to 2025. Methods differ (IEEE 1366 vs own rule). |
| F08 | Peers: restoration is mid-pack; frequency is the gap (SAIFI 5yr, CAIDI 5yr, 2021-25) | Dominion SAIFI 5yr 1.211 (rank 4 highest of 12, median 0.964); CAIDI 5yr 110.4 (rank 6 of 12, median 105.0) | **MATCH** | Means of annual values 2021-25, as the DAX measures SAIFI 5yr and CAIDI 5yr. Docs quote medians 0.96 and 105. |
| F09 | Since 2015, co-op SAIFI rose 37% against 14% for Dominion (index 137 vs 114) | Dominion Energy Virginia: 1.155 -> 1.32, index 114.3; Virginia co-op: 1.373 -> 1.887, index 137.4 | **MATCH** | All Virginia co-ops combined, customer-weighted (V_GROUP_INDEX). Balanced-panel check is sql/03 Q3. |
| F10 | DOM zone highest hour +26%, lowest hour +52% (2019 -> 2025) | peak 19,803 -> 24,957 MW (+26.0%); floor 7,167 -> 10,903 MW (+52.1%) | **MATCH** | Rebuilt from the 17 raw EIA-930 files through sql/06. DOM is the PJM zone, wider than Dominion's retail territory. |
| F11 | Night hours rose 41% and afternoon hours 27% (2019 -> 2025) | HE01 +39.0%; HE02 +40.2%; HE03 +40.8%; HE04 +41.0%; HE05 +40.0%; HE13 +27.3%; HE14 +27.0%; HE15 +26.9%; HE16 +27.1%; HE17 +27.4% | **MATCH (wording)** | 41% is the single hour ending 04:00 local and 27% the hour ending 16:00 (sql/07). Safer wording: 'the 4 a.m. hour rose 41%, the 4 p.m. hour 27%'; hours ending 01-05 range +39.0% to +41.0%, hours ending 13-17 +26.9% to +27.4%. |
| F12 | The winter peak was at or above the summer peak in 2022, 2025 and 2026 | 2019 winter (19,803/19,478), 2020 summer (17,468/20,073), 2021 summer (17,985/20,493), 2022 winter (22,415/21,274), 2023 summer (19,635/22,050), 2024 summer (22,152/23,220), 2025 winter (24,957/23,905), 2026 winter (25,413/25,384) | **MISMATCH (incomplete)** | Winter (Dec-Feb of the calendar year) beat summer (Jun-Aug) in 2019, 2022, 2025 and 2026, not only 2022, 2025, 2026. 2026 is to 30 Oct 2026 and the gap is 29 MW (25,413 vs 25,384): call it a tie. |
| F13 | 47 of the top 50 hours fall at the end of 2025 or later | ranked to 31 Dec 2025: 2024 = 3; ranked to 31 Dec 2025: 2025 = 47; ranked to load date (30 Oct 2026): 2025 = 4; ranked to load date (30 Oct 2026): 2026 = 46 | **MISMATCH (wording)** | Correct statement: of the 50 highest hours in the EIA-930 record (July 2018 to 31 Dec 2025), 47 fell in 2025 and 3 in 2024. Ranked to 30 Oct 2026: 46 in 2026, 4 in 2025. The record starts July 2018, so this is not 'all-time'. |
| F14 | Commercial sales rose 65% since 2013 on 8% more customers | sales 39.08 -> 64.62 TWh (index 165.4); customers 251,209 -> 271,163 (index 107.9; all service types 108.0) | **MATCH** | PUDL core_eia861__yearly_sales (EIA-861), utility 19876 VA, commercial class; sales sum bundled + delivery service types. Not attributable to data centers from this data (D14). |
| F15 | Most customers have a smart meter, but almost none are on a time-varying rate | 2019 AMI 19.1% of 2,525,177 meters; 2020 AMI 27.6% of 2,557,904 meters; 2021 AMI 47.9% of 2,588,613 meters; 2022 AMI 73.7% of 2,611,114 meters; 2023 AMI 93.1% of 2,630,114 meters; 2024 AMI 99.3% of 2,659,320 meters; 2025 AMI 99.8% of 2,682,315 meters | **MATCH** | AMI share from PUDL (EIA-861 Advanced Metering). The time-varying-rate half is F15b. |
| F15b | Almost no customers are on a time-varying rate | 2024: 26,560 of 2,655,130 customers enrolled (1.0%), residential 19,735 of 2,383,548 (0.83%); 2025: 27,039 of 2,681,231 customers enrolled (1.01%), residential 20,285 of 2,408,901 (0.84%) | **MATCH** | EIA-861 Dynamic Pricing: customers enrolled in time-of-use, real-time, variable-peak, critical-peak pricing or critical-peak rebate programs. Say 'about 1 in 100 customers', not 'almost none'. Programs reported for 2025: time-of-use (residential, commercial, industrial), variable-peak and critical-peak pricing (commercial, industrial). |

## Queries

### F01. Rolling 3-yr SAIDI ex-MED 130 (2022-24) -> 133 (2023-25)

```sql
SELECT ROUND(AVG(CASE WHEN year BETWEEN 2022 AND 2024 THEN saidi_ex_med END), 1) AS saidi_3yr_2022_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_3yr_2023_25
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA'
```

Result: 130.2 -> 133.0

### F02. SAIDI ex-MED 123.3 (2023) -> 144.4 (2025), +17%; SAIFI 1.165 -> 1.320, +13%; CAIDI 105.9 -> 109.4, +3%

```sql
SELECT a.saidi_ex_med AS saidi_2023, b.saidi_ex_med AS saidi_2025, ROUND(100*(b.saidi_ex_med/a.saidi_ex_med-1),1) AS saidi_pct,
       a.saifi_ex_med AS saifi_2023, b.saifi_ex_med AS saifi_2025, ROUND(100*(b.saifi_ex_med/a.saifi_ex_med-1),1) AS saifi_pct,
       a.caidi_ex_med AS caidi_2023, b.caidi_ex_med AS caidi_2025, ROUND(100*(b.caidi_ex_med/a.caidi_ex_med-1),1) AS caidi_pct
FROM mart.FCT_RELIABILITY a JOIN mart.FCT_RELIABILITY b ON a.utility_key = b.utility_key
WHERE a.utility_key = '19876|VA' AND a.year = 2023 AND b.year = 2025
```

Result: SAIDI 123.322 -> 144.4 (+17.1%); SAIFI 1.165 -> 1.32 (+13.3%); CAIDI 105.856 -> 109.394 (+3.3%)

### F03. The rise comes mostly from more interruptions, not longer ones

```sql
WITH p AS (SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA')
SELECT ROUND(100*LN(b.saifi_ex_med/a.saifi_ex_med)/LN(b.saidi_ex_med/a.saidi_ex_med)) AS pct_from_frequency,
       ROUND(100*LN(b.caidi_ex_med/a.caidi_ex_med)/LN(b.saidi_ex_med/a.saidi_ex_med)) AS pct_from_duration
FROM p a JOIN p b ON a.year = 2023 AND b.year = 2025
```

Result: 79% from frequency, 21% from duration (log decomposition, 2023->2025)

### F04. Storm county-days 464 (2024) -> 791 (2025) (decision D22; 465 -> 796 before Bedford city was folded into Bedford County)

```sql
SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year IN (2024, 2025) ORDER BY year
```

Result: 464 -> 791

### F05. r = 0.70 between storm county-days and SAIDI ex-MED, 2015-2024 (n = 10); fit predicts 145.3 for 2025 vs 144.4 actual

```sql
WITH j AS (SELECT * FROM mart.V_STORM_VS_SAIDI),
fit AS (SELECT REGR_SLOPE(saidi_ex_med, storm_county_days) AS slope, REGR_INTERCEPT(saidi_ex_med, storm_county_days) AS intercept,
               CORR(saidi_ex_med, storm_county_days) AS r, REGR_R2(saidi_ex_med, storm_county_days) AS r2, COUNT(*) AS n
        FROM j WHERE year BETWEEN 2015 AND 2024)
SELECT ROUND(r, 3) AS r, ROUND(r2, 3) AS r2, n, ROUND(slope, 4) AS slope, ROUND(intercept, 1) AS intercept,
       ROUND(intercept + slope * (SELECT storm_county_days FROM j WHERE year = 2025), 2) AS predicted_2025,
       intercept + slope * (SELECT storm_county_days FROM j WHERE year = 2025) AS predicted_raw,
       (SELECT saidi_ex_med FROM j WHERE year = 2025) AS actual_2025
FROM fit
```

Result: r = 0.697 (R2 = 0.486, n = 10); predicted 145.25 (145.2516) vs actual 144.4

### F06. 2025 all-events SAIDI 306.7 vs 144.4 ex-MED

```sql
SELECT saidi_all, saidi_ex_med, ROUND(100*(saidi_all - saidi_ex_med)/saidi_all) AS med_share_pct, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year = 2025
```

Result: 306.7 vs 144.4; major-event-day share 53%; customers 2,675,735

### F07. Dominion has the fourth-highest SAIDI of twelve peers over 2023-25

```sql
SELECT f.utility_key, d.utility_name, d.peer_group,
       ROUND(AVG(f.saidi_ex_med), 1) AS saidi_2023_25,
       RANK() OVER (ORDER BY AVG(f.saidi_ex_med) DESC) AS rank_highest
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL') AND f.year BETWEEN 2023 AND 2025
GROUP BY 1, 2, 3 ORDER BY saidi_2023_25 DESC
```

Result: Dominion rank 4 of 12 (133.0 min); top three: Duke Energy Carolinas, LLC 179.0; Duke Energy Progress - (NC) 143.8; Georgia Power Co 140.8

### F08. Peers: restoration is mid-pack; frequency is the gap (SAIFI 5yr, CAIDI 5yr, 2021-25)

```sql
WITH u AS (
  SELECT f.utility_key, d.utility_name, AVG(f.saifi_ex_med) AS saifi_5yr, AVG(f.caidi_ex_med) AS caidi_5yr
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL') AND f.year BETWEEN 2021 AND 2025 GROUP BY 1, 2)
SELECT utility_key, utility_name, ROUND(saifi_5yr, 3) AS saifi_5yr, ROUND(caidi_5yr, 1) AS caidi_5yr,
       RANK() OVER (ORDER BY saifi_5yr DESC) AS saifi_rank_highest, RANK() OVER (ORDER BY caidi_5yr DESC) AS caidi_rank_highest,
       ROUND(MEDIAN(saifi_5yr) OVER (), 3) AS median_saifi, ROUND(MEDIAN(caidi_5yr) OVER (), 1) AS median_caidi
FROM u ORDER BY saifi_5yr DESC
```

Result: Dominion SAIFI 5yr 1.211 (rank 4 highest of 12, median 0.964); CAIDI 5yr 110.4 (rank 6 of 12, median 105.0)

### F09. Since 2015, co-op SAIFI rose 37% against 14% for Dominion (index 137 vs 114)

```sql
WITH g AS (SELECT peer_group, year, saifi_ex_med FROM mart.V_GROUP_INDEX WHERE peer_group IN ('Virginia co-op','Dominion Energy Virginia'))
SELECT a.peer_group, ROUND(a.saifi_ex_med, 3) AS saifi_2015, ROUND(b.saifi_ex_med, 3) AS saifi_2025,
       ROUND(100 * b.saifi_ex_med / a.saifi_ex_med, 1) AS index_2025
FROM g a JOIN g b ON a.peer_group = b.peer_group AND a.year = 2015 AND b.year = 2025 ORDER BY 1
```

Result: Dominion Energy Virginia: 1.155 -> 1.32, index 114.3; Virginia co-op: 1.373 -> 1.887, index 137.4

### F10. DOM zone highest hour +26%, lowest hour +52% (2019 -> 2025)

```sql
SELECT a.peak_mw AS peak_2019, b.peak_mw AS peak_2025, ROUND(100*(b.peak_mw/a.peak_mw-1),1) AS peak_pct,
       a.floor_mw AS floor_2019, b.floor_mw AS floor_2025, ROUND(100*(b.floor_mw/a.floor_mw-1),1) AS floor_pct
FROM mart.DOM_LOAD_ANNUAL a JOIN mart.DOM_LOAD_ANNUAL b ON a.year = 2019 AND b.year = 2025
```

Result: peak 19,803 -> 24,957 MW (+26.0%); floor 7,167 -> 10,903 MW (+52.1%)

### F11. Night hours rose 41% and afternoon hours 27% (2019 -> 2025)

```sql
SELECT hour_no, avg_mw_2019, avg_mw_2025, growth_pct FROM mart.DOM_LOAD_PROFILE WHERE hour_no IN (1,2,3,4,5,13,14,15,16,17) ORDER BY hour_no
```

Result: HE01 +39.0%; HE02 +40.2%; HE03 +40.8%; HE04 +41.0%; HE05 +40.0%; HE13 +27.3%; HE14 +27.0%; HE15 +26.9%; HE16 +27.1%; HE17 +27.4%

### F12. The winter peak was at or above the summer peak in 2022, 2025 and 2026

```sql
SELECT year, winter_peak_mw, summer_peak_mw, CASE WHEN winter_peak_mw >= summer_peak_mw THEN 'winter' ELSE 'summer' END AS peak_season
FROM mart.DOM_LOAD_ANNUAL WHERE year BETWEEN 2019 AND 2026 ORDER BY year
```

Result: 2019 winter (19,803/19,478), 2020 summer (17,468/20,073), 2021 summer (17,985/20,493), 2022 winter (22,415/21,274), 2023 summer (19,635/22,050), 2024 summer (22,152/23,220), 2025 winter (24,957/23,905), 2026 winter (25,413/25,384)

### F13. 47 of the top 50 hours fall at the end of 2025 or later

```sql
SELECT 'ranked to 31 Dec 2025' AS reference, year, COUNT(*) AS hours_in_top50 FROM mart.DOM_TOP50_HOURS WHERE rank_end_2025 <= 50 GROUP BY 1, 2
UNION ALL
SELECT 'ranked to load date (30 Oct 2026)', year, COUNT(*) FROM mart.DOM_TOP50_HOURS WHERE rank_today <= 50 GROUP BY 1, 2 ORDER BY 1, 2
```

Result: ranked to 31 Dec 2025: 2024 = 3; ranked to 31 Dec 2025: 2025 = 47; ranked to load date (30 Oct 2026): 2025 = 4; ranked to load date (30 Oct 2026): 2026 = 46

### F14. Commercial sales rose 65% since 2013 on 8% more customers

```sql
WITH s AS (
  SELECT year, SUM(sales_mwh) AS sales_mwh,
         SUM(CASE WHEN service_type = 'bundled' THEN customers END) AS customers_bundled,
         SUM(customers) AS customers_all_service_types
  FROM stg.SALES WHERE utility_id = 19876 AND state = 'VA' AND customer_class = 'commercial' GROUP BY year)
SELECT a.sales_mwh AS mwh_2013, b.sales_mwh AS mwh_2025, ROUND(100*b.sales_mwh/a.sales_mwh, 1) AS sales_index_2025,
       a.customers_bundled AS cust_2013, b.customers_bundled AS cust_2025, ROUND(100*b.customers_bundled/a.customers_bundled, 1) AS cust_index_2025,
       ROUND(100*b.customers_all_service_types/a.customers_all_service_types, 1) AS cust_index_all_types
FROM s a JOIN s b ON a.year = 2013 AND b.year = 2025
```

Result: sales 39.08 -> 64.62 TWh (index 165.4); customers 251,209 -> 271,163 (index 107.9; all service types 108.0)

### F15. Most customers have a smart meter, but almost none are on a time-varying rate

```sql
SELECT year, ami_meters, total_meters, ROUND(100*ami_share, 1) AS ami_pct
FROM stg.AMI WHERE utility_id = 19876 AND state = 'VA' AND year >= 2019 ORDER BY year
```

Result: 2019 AMI 19.1% of 2,525,177 meters; 2020 AMI 27.6% of 2,557,904 meters; 2021 AMI 47.9% of 2,588,613 meters; 2022 AMI 73.7% of 2,611,114 meters; 2023 AMI 93.1% of 2,630,114 meters; 2024 AMI 99.3% of 2,659,320 meters; 2025 AMI 99.8% of 2,682,315 meters

### F15b. Almost no customers are on a time-varying rate

```sql
WITH dp AS (
  SELECT data_year, TRY_CAST(enrolled_res AS INT) AS enrolled_res, TRY_CAST(enrolled_com AS INT) AS enrolled_com,
         TRY_CAST(enrolled_total AS INT) AS enrolled_total
  FROM read_csv(['data/raw/eia861/csv/Dynamic_Pricing_2024_Dynamic_Pricing_States.csv',
                 'data/raw/eia861/csv/Dynamic_Pricing_2025_Dynamic_Pricing_States.csv'],
                skip = 3, header = false, all_varchar = true, names = ['data_year','utility_number','utility_name','short_form','state','ba_code','enrolled_res','enrolled_com','enrolled_ind','enrolled_trans','enrolled_total'])
  WHERE utility_number = '19876' AND state = 'VA'),
cu AS (  -- customers: bundled (part A) plus delivery-only (part C) rows
  SELECT data_year, SUM(TRY_CAST(res_cust AS INT)) AS res_customers, SUM(TRY_CAST(tot_cust AS INT)) AS customers
  FROM read_csv(['data/raw/eia861/csv/Sales_Ult_Cust_2024_States.csv',
                 'data/raw/eia861/csv/Sales_Ult_Cust_2025_States.csv'],
                skip = 5, header = false, all_varchar = true, strict_mode = false,  -- 3 header records (one spans 3 lines), multi-line footnote
                names = ['data_year','utility_number','utility_name','part','service_type','data_type','state','ownership','ba_code','res_rev','res_mwh','res_cust','com_rev','com_mwh','com_cust','ind_rev','ind_mwh','ind_cust','trans_rev','trans_mwh','trans_cust','tot_rev','tot_mwh','tot_cust'])
  WHERE utility_number = '19876' AND state = 'VA'
  GROUP BY 1)
SELECT dp.data_year AS year, dp.enrolled_total, cu.customers, ROUND(100.0 * dp.enrolled_total / cu.customers, 2) AS pct_enrolled,
       dp.enrolled_res, cu.res_customers, ROUND(100.0 * dp.enrolled_res / cu.res_customers, 2) AS pct_res_enrolled
FROM dp JOIN cu USING (data_year) ORDER BY 1
```

Result: 2024: 26,560 of 2,655,130 customers enrolled (1.0%), residential 19,735 of 2,383,548 (0.83%); 2025: 27,039 of 2,681,231 customers enrolled (1.01%), residential 20,285 of 2,408,901 (0.84%)

## Addendum: the 2025 values against the final EIA-861 2025 file

Final file: `data/raw/eia861/f8612025.zip` -> `Reliability_2025.xlsx`, sheet `Reliability_States` (980 rows including 3 header rows); repo file: `data/input/Reliability_2025_States.csv` (980 rows). Dominion reports under the "Other Standard" columns (its own major-event rule).

| Dominion VA, 2025 | Repo CSV | Final file | Same? |
|---|---:|---:|---|
| SAIDI all events | 306.700 | 306.7 | yes |
| SAIFI all events | 1.780 | 1.78 | yes |
| CAIDI all events | 172.303 | 172.30337 | yes |
| SAIDI ex-MED | 144.400 | 144.4 | yes |
| SAIFI ex-MED | 1.320 | 1.32 | yes |
| CAIDI ex-MED | 109.394 | 109.39394 | yes |
| Customers | 2,675,735 | 2675735 | yes |

**Result: MATCH.** The headline values (SAIDI ex-MED 144.4, SAIFI 1.320, CAIDI 109.4, all-events SAIDI 306.7, 2,675,735 customers) are the final 2025 values. Across the whole sheet 16 cells differ, all in other utilities' customer counts, which the final file holds as fractions and the repo CSV shows rounded to whole customers:

| Row | Utility | Name | State | Column | Repo CSV | Final file |
|---:|---|---|---|---|---:|---:|
| 24 | 562 | Amicalola Electric Member Corp | GA | Number of Customers | 56,981 | 56980.6 |
| 27 | 689 | Connexus Energy | MN | Number of Customers | 148,632 | 148632.3 |
| 99 | 3107 | Carteret-Craven El Member Corp | NC | Number of Customers | 43,239 | 43238.7 |
| 200 | 4975 | Deep East Texas Elec Coop Inc | TX | Number of Customers | 45,020 | 45019.8 |
| 211 | 5204 | Dixie Electric Coop - (AL) | AL | Number of Customers | 26,553 | 26553.1 |
| 253 | 6182 | Farmers Electric Coop, Inc - (TX) | TX | Number of Customers | 94,603 | 94603.3 |
| 303 | 7450 | Grady Electric Membership Corp | GA | Number of Customers | 20,382 | 20382.4 |
| 323 | 8000 | NineStar Connect | IN | Number of Customers | 19,471 | 19471.2 |
| 384 | 9668 | Jasper-Newton Elec Coop, Inc | TX | Number of Customers | 23,817 | 23816.6 |
| 737 | 16751 | Three Rivers Electric Coop | MO | Number of Customers | 24,580 | 24579.6 |
| 740 | 16865 | Sawnee Electric Membership Corporation | GA | Number of Customers | 203,530 | 203530.3 |
| 754 | 17252 | Singing River Elec Cooperative | AL | Number of Customers | 336 | 335.9 |
| 755 | 17252 | Singing River Elec Cooperative | MS | Number of Customers | 78,172 | 78172.2 |
| 768 | 17585 | Southeastern IL Elec Coop, Inc | IL | Number of Customers | 25,032 | 25031.9 |
| 826 | 18956 | Tri-County Elec Member Corp (GA) | GA | Number of Customers | 23,346 | 23345.9 |
| 837 | 19161 | Tri-County Electric Coop, Inc (FL) | FL | Number of Customers | 19,681 | 19681.4 |