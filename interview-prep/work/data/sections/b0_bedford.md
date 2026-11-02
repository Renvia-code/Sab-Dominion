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
