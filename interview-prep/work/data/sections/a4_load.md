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
