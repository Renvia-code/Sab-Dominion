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
