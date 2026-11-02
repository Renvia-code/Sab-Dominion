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
