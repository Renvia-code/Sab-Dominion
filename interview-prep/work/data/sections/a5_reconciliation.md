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
