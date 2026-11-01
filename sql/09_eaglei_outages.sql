-- =====================================================================
-- DOMINION RELIABILITY MART  |  09: EAGLE-I county outages (ORNL), Virginia
-- Adds four raw tables, two staging views, seven mart tables, tests T13 to
-- T24 and four analysis queries. Run after 05 (it reuses STG.NOAA_VA_EVENTS
-- and STG.DOMINION_VA_COUNTIES).
--
-- EAGLE-I records, every 15 minutes, how many customers each county's
-- utilities show as out on their public outage maps. It counts EVERY
-- utility's customers in a county (Dominion, co-ops, municipals, APCo), so
-- the county outage figures here are not Dominion-only. DIM_COUNTY carries
-- the rule used to pick Dominion counties and the reason, row by row.
-- Times are UTC as published. Days are Eastern Standard Time (UTC-5) all
-- year, the convention NOAA Storm Events uses, so outage days and storm days
-- line up.
-- =====================================================================

USE WAREHOUSE SNOWFLAKE_LEARNING_WH;

-- ---------- 0. File format and stage (Snowflake only) ----------
CREATE FILE FORMAT IF NOT EXISTS RELIABILITY.RAW.FF_EAGLEI_CSV
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('')
  EMPTY_FIELD_AS_NULL = TRUE
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;   -- 2024 has a sixth column, total_customers

CREATE STAGE IF NOT EXISTS RELIABILITY.RAW.EAGLEI_STAGE FILE_FORMAT = RELIABILITY.RAW.FF_EAGLEI_CSV;
-- Upload data/raw/eaglei/va/eaglei_outages_va_2014.csv ... _2025.csv (12 files),
-- data/raw/eaglei/MCC.csv, data/raw/eaglei/coverage_history.csv and
-- data/raw/census/va_county_census.csv:
--   PUT file://data/raw/eaglei/va/*.csv @RELIABILITY.RAW.EAGLEI_STAGE/va/;

-- ---------- 1. Raw tables, all text ----------
-- One row per county per 15-minute run, Virginia only (scripts/extract_eaglei_va.py
-- keeps the Virginia rows of the national files unchanged). The 2023 file names the
-- count column "sum"; loading by position puts it in customers_out.
CREATE OR REPLACE TABLE RELIABILITY.RAW.EAGLEI_OUTAGES_VA (
  fips_code VARCHAR, county VARCHAR, state VARCHAR, customers_out VARCHAR,
  run_start_time VARCHAR, total_customers VARCHAR, source_file VARCHAR
);

-- EAGLE-I modelled customers per county (all utilities), 2022 basis
CREATE OR REPLACE TABLE RELIABILITY.RAW.EAGLEI_MCC (county_fips VARCHAR, customers VARCHAR);

-- Share of each state's customers that EAGLE-I collected, 2018 to 2022
CREATE OR REPLACE TABLE RELIABILITY.RAW.EAGLEI_COVERAGE_HISTORY (
  year VARCHAR, state VARCHAR, total_customers VARCHAR, min_covered VARCHAR,
  max_covered VARCHAR, min_pct_covered VARCHAR, max_pct_covered VARCHAR
);

-- Census: Virginia counties and independent cities (scripts/extract_census_va.py)
CREATE OR REPLACE TABLE RELIABILITY.RAW.CENSUS_VA_COUNTY (
  county_fips VARCHAR, name VARCHAR, namelsad VARCHAR, aland_sq_mi VARCHAR,
  acs5_2024_population VARCHAR, acs5_2024_housing_units VARCHAR,
  pep_population_2020 VARCHAR, pep_population_2025 VARCHAR
);

COPY INTO RELIABILITY.RAW.EAGLEI_OUTAGES_VA FROM (
  SELECT $1, $2, $3, $4, $5, $6, METADATA$FILENAME FROM @RELIABILITY.RAW.EAGLEI_STAGE/va/
) PATTERN = '.*eaglei_outages_va_20[0-9]{2}\.csv';
COPY INTO RELIABILITY.RAW.EAGLEI_MCC FROM @RELIABILITY.RAW.EAGLEI_STAGE/MCC.csv;
COPY INTO RELIABILITY.RAW.EAGLEI_COVERAGE_HISTORY FROM @RELIABILITY.RAW.EAGLEI_STAGE/coverage_history.csv;
COPY INTO RELIABILITY.RAW.CENSUS_VA_COUNTY FROM @RELIABILITY.RAW.EAGLEI_STAGE/va_county_census.csv;

-- Check: expected 11,608,442 / 3,234 / 280 / 133
SELECT 'eaglei_va' AS t, COUNT(*) AS n FROM RELIABILITY.RAW.EAGLEI_OUTAGES_VA
UNION ALL SELECT 'mcc', COUNT(*) FROM RELIABILITY.RAW.EAGLEI_MCC
UNION ALL SELECT 'coverage', COUNT(*) FROM RELIABILITY.RAW.EAGLEI_COVERAGE_HISTORY
UNION ALL SELECT 'census', COUNT(*) FROM RELIABILITY.RAW.CENSUS_VA_COUNTY;

-- ---------- 2. Staging ----------
-- Customers per county, the denominator for every county rate (decision D15).
-- EAGLE-I's modelled county customers (MCC.csv, 2022) add up to 3.96 million for
-- Virginia, which matches EIA's count of the state's customers, so they are the
-- basis. MCC gives 1 to 16 customers for Buena Vista, Waynesboro and Lexington
-- and has no row for Norton, so where MCC is missing or below half the county's
-- housing units, ACS housing units are used instead. (The 2024 outage file also
-- carries a total_customers column, but it adds up to 4.9 million for Virginia,
-- 142,597 for Fairfax city, so it is not used.)
CREATE OR REPLACE VIEW RELIABILITY.STG.VA_COUNTY_CUSTOMERS AS
SELECT c.county_fips,
       TRY_TO_NUMBER(m.customers)                 AS eaglei_modelled_customers,
       TRY_TO_NUMBER(c.acs5_2024_housing_units)   AS housing_units,
       CASE WHEN TRY_TO_NUMBER(m.customers) IS NULL
              OR TRY_TO_NUMBER(m.customers) < 0.5 * TRY_TO_NUMBER(c.acs5_2024_housing_units)
            THEN TRY_TO_NUMBER(c.acs5_2024_housing_units)
            ELSE TRY_TO_NUMBER(m.customers) END  AS customers_basis,
       CASE WHEN TRY_TO_NUMBER(m.customers) IS NULL
              OR TRY_TO_NUMBER(m.customers) < 0.5 * TRY_TO_NUMBER(c.acs5_2024_housing_units)
            THEN 'ACS housing units (EAGLE-I modelled count missing or below half of housing units)'
            ELSE 'EAGLE-I modelled customers (MCC.csv, 2022)' END AS customers_basis_source
FROM RELIABILITY.RAW.CENSUS_VA_COUNTY c
LEFT JOIN RELIABILITY.RAW.EAGLEI_MCC m ON LPAD(m.county_fips, 5, '0') = c.county_fips;

-- One row per county per 15-minute slot. A handful of runs start off the
-- quarter hour (1,010 rows): they are placed in their 15-minute slot and, where
-- two readings share a slot, the higher is kept, which is EAGLE-I's own rule for
-- grouping readings into a time frame. A blank count in the source marks a
-- failed collection run: it stays NULL, never zero (decision D16). A county with
-- no row at a slot had no customers out, or was not collected; EAGLE-I does
-- not distinguish the two. A reading of more than twice the county's customers
-- cannot be true: customers_out is set to NULL and the published value kept in
-- customers_out_reported, as decision D7 does for EIA-930 (test T19 lists them).
CREATE OR REPLACE VIEW RELIABILITY.STG.EAGLEI_VA_15MIN AS
SELECT s.county_fips, s.county_name, s.ts_utc, s.customers_out_reported,
       CASE WHEN s.customers_out_reported > 2 * b.customers_basis THEN NULL
            ELSE s.customers_out_reported END                     AS customers_out,
       s.customers_out_reported IS NULL                           AS failed_run,
       s.source_rows, s.valued_rows, s.total_customers, s.source_file
FROM (
SELECT county_fips,
       MIN(county)                    AS county_name,
       ts_slot                        AS ts_utc,
       MAX(customers_out)             AS customers_out_reported,
       COUNT(*)                       AS source_rows,
       COUNT(customers_out)           AS valued_rows,
       MAX(total_customers)           AS total_customers,
       MIN(source_file)               AS source_file
FROM (
  SELECT LPAD(fips_code, 5, '0')                                   AS county_fips,
         county,
         TIME_SLICE(TRY_CAST(run_start_time AS TIMESTAMP), 15, 'MINUTE') AS ts_slot,
         TRY_CAST(customers_out AS INTEGER)                        AS customers_out,
         TRY_CAST(total_customers AS INTEGER)                      AS total_customers,
         source_file
  FROM RELIABILITY.RAW.EAGLEI_OUTAGES_VA
  WHERE state = 'Virginia'
) r
GROUP BY county_fips, ts_slot
) s
LEFT JOIN RELIABILITY.STG.VA_COUNTY_CUSTOMERS b ON b.county_fips = s.county_fips;

-- Every utility EIA lists in each Virginia county, with the county's FIPS code.
-- Same name rule as STG.DOMINION_VA_COUNTIES ("Alexandria City" = "City of Alexandria").
CREATE OR REPLACE VIEW RELIABILITY.STG.EIA861_VA_COUNTY_UTILITY AS
WITH eia AS (
  SELECT DISTINCT TRY_TO_NUMBER(utility_number) AS utility_id, utility_name, county,
         CASE WHEN county LIKE '% City' THEN 'City of ' || LEFT(county, LENGTH(county) - 5) ELSE county END AS noaa_name
  FROM RELIABILITY.RAW.EIA861_SERVICE_TERRITORY_2025
  WHERE state = 'VA'
),
lookup AS (
  SELECT DISTINCT county_name, LPAD(fips, 5, '0') AS county_fips
  FROM RELIABILITY.RAW.NOAA_ZONE_COUNTY
  WHERE state = 'VA' AND fips <> '9999'
)
SELECT e.utility_id, e.utility_name, e.county AS eia_county,
       -- Bedford city (51515) became part of Bedford County (51019) in 2013
       CASE WHEN MIN(l.county_fips) = '51515' THEN '51019' ELSE MIN(l.county_fips) END AS county_fips
FROM eia e
LEFT JOIN lookup l ON LOWER(l.county_name) IN (LOWER(e.county), LOWER(e.noaa_name))
GROUP BY e.utility_id, e.utility_name, e.county;

-- ---------- 3. Mart ----------
-- DIM_COUNTY: the 133 Virginia counties and independent cities, with the
-- Dominion-county rule as columns.
--   dominion_county: EIA-861 2025 Service Territory lists Dominion Energy Virginia
--     (utility 19876) in the county. 103 counties and cities (EIA's 104 names
--     less Bedford city, now part of Bedford County). Same set as the NOAA storm index.
--   dominion_only_county: Dominion is the only utility EIA lists there, so EAGLE-I's
--     count there is (almost) all Dominion customers. Used as a robustness check.
CREATE OR REPLACE TABLE RELIABILITY.MART.DIM_COUNTY COPY GRANTS AS
WITH u AS (
  SELECT county_fips,
         COUNT(DISTINCT utility_id)                                     AS utilities_listed,
         MAX(CASE WHEN utility_id = 19876 THEN 1 ELSE 0 END)            AS has_dominion
  FROM RELIABILITY.STG.EIA861_VA_COUNTY_UTILITY
  WHERE county_fips IS NOT NULL
  GROUP BY county_fips
),
-- The 2024 outage file's total_customers column, kept for reference only (see STG.VA_COUNTY_CUSTOMERS)
tc AS (
  SELECT county_fips, MAX(total_customers) AS customers_2024
  FROM RELIABILITY.STG.EAGLEI_VA_15MIN WHERE total_customers IS NOT NULL
  GROUP BY county_fips
)
SELECT c.county_fips,
       c.name                                                          AS county_name,
       c.namelsad                                                      AS county_label,
       c.namelsad LIKE '% city'                                        AS is_independent_city,
       TRY_CAST(c.aland_sq_mi AS DOUBLE)                               AS land_sq_mi,
       TRY_TO_NUMBER(c.acs5_2024_population)                           AS population_acs5_2024,
       TRY_TO_NUMBER(c.acs5_2024_housing_units)                        AS housing_units_acs5_2024,
       TRY_TO_NUMBER(c.pep_population_2025)                            AS population_2025,
       b.eaglei_modelled_customers,
       t.customers_2024                                                AS eaglei_file_customers_2024,
       b.customers_basis,
       b.customers_basis_source,
       COALESCE(u.utilities_listed, 0)                                 AS utilities_listed,
       COALESCE(u.has_dominion, 0) = 1                                 AS dominion_county,
       COALESCE(u.has_dominion, 0) = 1 AND u.utilities_listed = 1      AS dominion_only_county,
       CASE WHEN COALESCE(u.has_dominion, 0) = 1
            THEN 'Dominion county: EIA-861 2025 Service Territory lists Dominion Energy Virginia (utility 19876) here'
            ELSE 'Not a Dominion county: EIA-861 2025 Service Territory does not list utility 19876 here' END AS dominion_county_rule,
       CASE WHEN COALESCE(u.has_dominion, 0) = 1 AND u.utilities_listed = 1
              THEN 'Only Dominion is listed, so EAGLE-I outage counts here are Dominion customers'
            WHEN COALESCE(u.has_dominion, 0) = 1
              THEN 'Shared with ' || (u.utilities_listed - 1) || ' other utilit' || CASE WHEN u.utilities_listed = 2 THEN 'y' ELSE 'ies' END || ', whose customers EAGLE-I also counts'
            ELSE 'EAGLE-I counts here are other utilities'' customers' END AS dominion_county_reason
FROM RELIABILITY.RAW.CENSUS_VA_COUNTY c
LEFT JOIN u   ON u.county_fips = c.county_fips
LEFT JOIN RELIABILITY.STG.VA_COUNTY_CUSTOMERS b ON b.county_fips = c.county_fips
LEFT JOIN tc  t ON t.county_fips = c.county_fips;

-- Hourly county outages, all Virginia counties. customer_hours: each 15-minute
-- reading stands for a quarter hour, so customers out x 0.25.
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_OUTAGE_COUNTY_HOUR COPY GRANTS AS
SELECT county_fips,
       DATE_TRUNC('HOUR', ts_utc)                AS hour_utc,
       MAX(customers_out)                        AS customers_out_max,
       SUM(customers_out) * 0.25                 AS customer_hours,
       COUNT(customers_out)                      AS readings,
       COUNT(*) - COUNT(customers_out)           AS failed_readings
FROM RELIABILITY.STG.EAGLEI_VA_15MIN
GROUP BY 1, 2;

-- Territory series: all utilities' customers out in the 103 Dominion counties,
-- every 15 minutes. NULL when every county's reading at that slot failed.
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_TERRITORY_15MIN COPY GRANTS AS
SELECT s.ts_utc,
       SUM(s.customers_out)                      AS customers_out,
       COUNT(s.customers_out)                    AS counties_with_value,
       COUNT(*) - COUNT(s.customers_out)         AS counties_failed
FROM RELIABILITY.STG.EAGLEI_VA_15MIN s
JOIN RELIABILITY.MART.DIM_COUNTY c ON c.county_fips = s.county_fips AND c.dominion_county
GROUP BY s.ts_utc;

-- County-day panel for the 103 Dominion counties, every day 2015 to 2025
-- (Eastern Standard Time), with NOAA storm flags from the same events the
-- storm index counts (line-risk types, begin date, decision D5).
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_COUNTY_DAY COPY GRANTS AS
WITH days AS (
  SELECT DISTINCT CAST(ts_utc - INTERVAL '5 HOUR' AS DATE) AS day
  FROM RELIABILITY.STG.EAGLEI_VA_15MIN
  WHERE ts_utc >= '2015-01-01 05:00:00' AND ts_utc < '2026-01-01 05:00:00'
),
counties AS (
  SELECT county_fips, customers_basis, dominion_only_county FROM RELIABILITY.MART.DIM_COUNTY WHERE dominion_county
),
outage AS (
  SELECT county_fips, CAST(ts_utc - INTERVAL '5 HOUR' AS DATE) AS day,
         SUM(customers_out) * 0.25           AS customer_hours,
         MAX(customers_out)                  AS customers_out_max,
         COUNT(customers_out)                AS readings,
         COUNT(*) - COUNT(customers_out)     AS failed_readings
  FROM RELIABILITY.STG.EAGLEI_VA_15MIN
  GROUP BY 1, 2
),
storm AS (
  SELECT CASE WHEN county_id_fips = '51515' THEN '51019' ELSE county_id_fips END AS county_fips,
         DATE_FROM_PARTS(CAST(FLOOR(begin_yearmonth / 100) AS INTEGER), CAST(MOD(begin_yearmonth, 100) AS INTEGER),
                         CAST(begin_day AS INTEGER))                     AS day,
         COUNT(*)                                                        AS storm_events,
         MAX(CASE WHEN line_risk = 'wind'     THEN 1 ELSE 0 END)         AS storm_wind,
         MAX(CASE WHEN line_risk = 'winter'   THEN 1 ELSE 0 END)         AS storm_winter,
         MAX(CASE WHEN line_risk = 'tropical' THEN 1 ELSE 0 END)         AS storm_tropical,
         MAX(CASE WHEN event_type = 'Thunderstorm Wind' THEN magnitude END) AS max_gust_kt
  FROM RELIABILITY.STG.NOAA_VA_EVENTS
  WHERE line_risk <> 'other' AND county_id_fips IS NOT NULL
  GROUP BY 1, 2
)
SELECT c.county_fips,
       d.day,
       YEAR(d.day)                                         AS year,
       MONTH(d.day)                                        AS month,
       c.dominion_only_county,
       c.customers_basis,
       COALESCE(o.customer_hours, 0)                       AS customer_hours,
       COALESCE(o.customers_out_max, 0)                    AS customers_out_max,
       COALESCE(o.readings, 0)                             AS readings,
       COALESCE(o.failed_readings, 0)                      AS failed_readings,
       1000 * COALESCE(o.customer_hours, 0) / NULLIF(c.customers_basis, 0) AS customer_hours_per_1k,
       COALESCE(s.storm_events, 0) > 0                     AS storm_day,
       COALESCE(s.storm_events, 0)                         AS storm_events,
       COALESCE(s.storm_wind, 0) = 1                       AS storm_wind,
       COALESCE(s.storm_winter, 0) = 1                     AS storm_winter,
       COALESCE(s.storm_tropical, 0) = 1                   AS storm_tropical,
       s.max_gust_kt
FROM counties c
CROSS JOIN days d
LEFT JOIN outage o ON o.county_fips = c.county_fips AND o.day = d.day
LEFT JOIN storm  s ON s.county_fips = c.county_fips AND s.day = d.day;

-- Territory day with a major-event-day proxy. IEEE 1366's 2.5 beta method applied
-- to EAGLE-I customer-hours in the 103 Dominion counties: a day is a proxy major
-- event day when its customer-hours exceed exp(alpha + 2.5 beta), where alpha and
-- beta are the mean and standard deviation of ln(daily customer-hours) over the
-- previous five years (2015 uses its own year; 2016 to 2019 use the years
-- available from 2015). Dominion's own major-event days are not public; this is a
-- stand-in built the IEEE way (decision D18).
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_TERRITORY_DAY COPY GRANTS AS
WITH d AS (
  SELECT day, year, SUM(customer_hours) AS customer_hours, SUM(failed_readings) AS failed_readings,
         SUM(CASE WHEN storm_day THEN 1 ELSE 0 END) AS storm_counties
  FROM RELIABILITY.MART.FCT_COUNTY_DAY
  GROUP BY 1, 2
),
peak AS (
  SELECT CAST(ts_utc - INTERVAL '5 HOUR' AS DATE) AS day, MAX(customers_out) AS customers_out_max
  FROM RELIABILITY.MART.FCT_TERRITORY_15MIN GROUP BY 1
),
thr AS (
  SELECT y.year,
         AVG(LN(h.customer_hours))         AS alpha,
         STDDEV_SAMP(LN(h.customer_hours)) AS beta,
         COUNT(*)                          AS window_days
  FROM (SELECT DISTINCT year FROM d) y
  JOIN d h ON h.customer_hours > 0
          AND ((y.year = 2015 AND h.year = 2015)
            OR (y.year > 2015 AND h.year BETWEEN GREATEST(2015, y.year - 5) AND y.year - 1))
  GROUP BY y.year
)
SELECT d.day, d.year, d.customer_hours, p.customers_out_max, d.failed_readings, d.storm_counties,
       t.alpha, t.beta, t.window_days,
       EXP(t.alpha + 2.5 * t.beta)                     AS med_threshold_customer_hours,
       d.customer_hours > EXP(t.alpha + 2.5 * t.beta)  AS is_med_proxy
FROM d
JOIN thr t ON t.year = d.year
LEFT JOIN peak p ON p.day = d.day;

-- Outage events, two scopes, thresholds stated (decision D17):
--   territory: the 103 Dominion counties together, 10,000 or more customers out
--     (about 0.3% of the 3.44 million customers EAGLE-I models there);
--   county: one county, 1% or more of its customers out (and at least 10).
-- Readings above the threshold no more than 3 hours apart (territory) or 1 hour
-- apart (county) belong to the same event. Restoration is measured from the peak,
-- above the background level (median of the 24 hours before the event starts):
-- hours_to_90pct is the first reading after the peak at or below
-- background + 10% of (peak - background). Searched for 14 days after the peak.
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_OUTAGE_EVENT COPY GRANTS AS
WITH terr AS (
  SELECT ts_utc, customers_out FROM RELIABILITY.MART.FCT_TERRITORY_15MIN WHERE customers_out IS NOT NULL
),
t_above AS (
  SELECT ts_utc, customers_out,
         CASE WHEN DATEDIFF('minute', LAG(ts_utc) OVER (ORDER BY ts_utc), ts_utc) <= 180 THEN 0 ELSE 1 END AS new_event
  FROM terr WHERE customers_out >= 10000
),
t_ev AS (
  SELECT ts_utc, customers_out, SUM(new_event) OVER (ORDER BY ts_utc ROWS UNBOUNDED PRECEDING) AS seq FROM t_above
),
t_sum AS (
  SELECT seq, MIN(ts_utc) AS start_utc, MAX(ts_utc) AS end_utc, MAX(customers_out) AS peak_customers_out,
         MAX_BY(ts_utc, customers_out) AS peak_utc, COUNT(*) AS readings_above
  FROM t_ev GROUP BY seq
),
t_base AS (
  SELECT e.seq, MEDIAN(t.customers_out) AS background
  FROM t_sum e JOIN terr t ON t.ts_utc >= e.start_utc - INTERVAL '24 HOUR' AND t.ts_utc < e.start_utc
  GROUP BY e.seq
),
t_ch AS (
  SELECT e.seq, SUM(t.customers_out) * 0.25 AS customer_hours
  FROM t_sum e JOIN terr t ON t.ts_utc BETWEEN e.start_utc AND e.end_utc
  GROUP BY e.seq
),
t_rest AS (
  SELECT e.seq,
         MIN(CASE WHEN t.customers_out <= b.background + 0.50 * (e.peak_customers_out - b.background) THEN t.ts_utc END) AS ts_50,
         MIN(CASE WHEN t.customers_out <= b.background + 0.10 * (e.peak_customers_out - b.background) THEN t.ts_utc END) AS ts_90,
         MIN(CASE WHEN t.customers_out <= b.background + 0.01 * (e.peak_customers_out - b.background) THEN t.ts_utc END) AS ts_99
  FROM t_sum e
  JOIN t_base b ON b.seq = e.seq
  JOIN terr t ON t.ts_utc > e.peak_utc AND t.ts_utc <= e.peak_utc + INTERVAL '14 DAY'
  GROUP BY e.seq
),
territory AS (
  SELECT 'territory' AS scope, 'DOM103' AS area_code, e.seq,
         e.start_utc, e.peak_utc, e.end_utc, e.peak_customers_out, e.readings_above,
         c.customer_hours, b.background AS background_customers_out,
         DATEDIFF('minute', e.peak_utc, r.ts_50) / 60.0 AS hours_to_50pct,
         DATEDIFF('minute', e.peak_utc, r.ts_90) / 60.0 AS hours_to_90pct,
         DATEDIFF('minute', e.peak_utc, r.ts_99) / 60.0 AS hours_to_99pct
  FROM t_sum e
  LEFT JOIN t_base b ON b.seq = e.seq
  LEFT JOIN t_ch   c ON c.seq = e.seq
  LEFT JOIN t_rest r ON r.seq = e.seq
),
cty AS (
  SELECT s.county_fips, s.ts_utc, s.customers_out
  FROM RELIABILITY.STG.EAGLEI_VA_15MIN s
  JOIN RELIABILITY.MART.DIM_COUNTY d ON d.county_fips = s.county_fips AND d.dominion_county
  WHERE s.customers_out >= GREATEST(10, 0.01 * d.customers_basis)
),
c_flag AS (
  SELECT county_fips, ts_utc, customers_out,
         CASE WHEN DATEDIFF('minute', LAG(ts_utc) OVER (PARTITION BY county_fips ORDER BY ts_utc), ts_utc) <= 60 THEN 0 ELSE 1 END AS new_event
  FROM cty
),
c_ev AS (
  SELECT county_fips, ts_utc, customers_out,
         SUM(new_event) OVER (PARTITION BY county_fips ORDER BY ts_utc ROWS UNBOUNDED PRECEDING) AS seq
  FROM c_flag
),
county AS (
  SELECT 'county' AS scope, county_fips AS area_code, seq,
         MIN(ts_utc) AS start_utc, MAX_BY(ts_utc, customers_out) AS peak_utc, MAX(ts_utc) AS end_utc,
         MAX(customers_out) AS peak_customers_out, COUNT(*) AS readings_above,
         SUM(customers_out) * 0.25 AS customer_hours, CAST(NULL AS DOUBLE) AS background_customers_out,
         CAST(NULL AS DOUBLE) AS hours_to_50pct, CAST(NULL AS DOUBLE) AS hours_to_90pct, CAST(NULL AS DOUBLE) AS hours_to_99pct
  FROM c_ev GROUP BY county_fips, seq
),
both_scopes AS (
  SELECT * FROM territory
  UNION ALL
  SELECT * FROM county
)
SELECT b.scope || '|' || b.area_code || '|' || CAST(b.start_utc AS VARCHAR)  AS event_key,
       b.scope, b.area_code, b.start_utc, b.peak_utc, b.end_utc,
       CAST(b.start_utc - INTERVAL '5 HOUR' AS DATE)                         AS start_day,
       YEAR(b.start_utc - INTERVAL '5 HOUR')                                 AS year,
       b.peak_customers_out, b.readings_above,
       DATEDIFF('minute', b.start_utc, b.end_utc) / 60.0 + 0.25               AS hours_above_threshold,
       b.customer_hours, b.background_customers_out,
       b.hours_to_50pct, b.hours_to_90pct, b.hours_to_99pct,
       COALESCE(m.is_med_proxy, FALSE)                                       AS starts_on_med_proxy_day
FROM both_scopes b
LEFT JOIN RELIABILITY.MART.FCT_TERRITORY_DAY m ON m.day = CAST(b.start_utc - INTERVAL '5 HOUR' AS DATE);

-- Restoration curves for territory events that peaked at 50,000 or more customers
-- out: the highest reading in each hour after the peak, for 7 days, as a share of
-- the event's excess over its background (0 = at peak, 1 = back to background).
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_RESTORATION_CURVE COPY GRANTS AS
SELECT e.event_key, e.peak_utc, e.peak_customers_out, e.background_customers_out,
       FLOOR(DATEDIFF('minute', e.peak_utc, t.ts_utc) / 60)                                AS hour_since_peak,
       MAX(t.customers_out)                                                                AS customers_out,
       LEAST(1, GREATEST(0, (e.peak_customers_out - MAX(t.customers_out))
                            / NULLIF(e.peak_customers_out - e.background_customers_out, 0))) AS share_restored
FROM RELIABILITY.MART.FCT_OUTAGE_EVENT e
JOIN RELIABILITY.MART.FCT_TERRITORY_15MIN t
  ON t.ts_utc >= e.peak_utc AND t.ts_utc < e.peak_utc + INTERVAL '7 DAY' AND t.customers_out IS NOT NULL
WHERE e.scope = 'territory' AND e.peak_customers_out >= 50000
GROUP BY e.event_key, e.peak_utc, e.peak_customers_out, e.background_customers_out,
         FLOOR(DATEDIFF('minute', e.peak_utc, t.ts_utc) / 60);

-- ---------- 4. Tests ----------
-- T13. Raw row count equals the sum of the Virginia rows written by the extract script (expected 0 rows)
SELECT COUNT(*) AS n FROM RELIABILITY.RAW.EAGLEI_OUTAGES_VA HAVING COUNT(*) <> 11608442;

-- T14. No Virginia row has a county code outside 51001-51840 or a timestamp that does not parse (expected 0 rows)
SELECT fips_code, run_start_time FROM RELIABILITY.RAW.EAGLEI_OUTAGES_VA
WHERE fips_code NOT LIKE '51___' OR TRY_CAST(run_start_time AS TIMESTAMP) IS NULL;

-- T15. One row per county per 15-minute slot after staging (expected 0 rows)
SELECT county_fips, ts_utc FROM RELIABILITY.STG.EAGLEI_VA_15MIN GROUP BY 1, 2 HAVING COUNT(*) > 1;

-- T16. Every EAGLE-I county code is a Census county or city (expected 0 rows)
SELECT DISTINCT s.county_fips FROM RELIABILITY.STG.EAGLEI_VA_15MIN s
LEFT JOIN RELIABILITY.MART.DIM_COUNTY d ON d.county_fips = s.county_fips WHERE d.county_fips IS NULL;

-- T17. Dominion counties: 103 (EIA's 104 names less Bedford city) of 133, 34 Dominion-only (expected 1 row: value 0 in problems)
SELECT CASE WHEN COUNT(*) = 133 AND SUM(CASE WHEN dominion_county THEN 1 ELSE 0 END) = 103
             AND SUM(CASE WHEN dominion_only_county THEN 1 ELSE 0 END) BETWEEN 30 AND 40 THEN 0 ELSE 1 END AS problems
FROM RELIABILITY.MART.DIM_COUNTY;

-- T18. Every Virginia utility-county in EIA-861 Service Territory resolves to a FIPS code (expected 0 rows)
SELECT * FROM RELIABILITY.STG.EIA861_VA_COUNTY_UTILITY WHERE county_fips IS NULL;

-- T19. County-days with readings above twice the county's customers, which staging sets
--      to NULL: Fairfax city on 2-4 March 2018 (up to 136,046 out in a city of 12,701
--      customers) and 2019-2020, and 18 other county-days (expected 22 rows)
SELECT s.county_fips, CAST(s.ts_utc AS DATE) AS utc_day, COUNT(*) AS readings,
       MAX(s.customers_out_reported) AS max_reported, MAX(d.customers_basis) AS customers_basis
FROM RELIABILITY.STG.EAGLEI_VA_15MIN s JOIN RELIABILITY.MART.DIM_COUNTY d ON d.county_fips = s.county_fips
WHERE s.customers_out_reported < 0 OR s.customers_out_reported > 2 * d.customers_basis
GROUP BY 1, 2;

-- T20. The county-day panel is complete: 103 counties x 4,018 days (expected 1 row: value 0 in problems)
SELECT CASE WHEN COUNT(*) = 103 * 4018 AND COUNT(DISTINCT day) = 4018 THEN 0 ELSE 1 END AS problems
FROM RELIABILITY.MART.FCT_COUNTY_DAY;

-- T21. The panel's storm days add up to the storm index, year by year, once Bedford
--      city's duplicate county-days are removed (expected 0 rows)
WITH panel AS (SELECT year, SUM(CASE WHEN storm_day THEN 1 ELSE 0 END) AS storm_county_days FROM RELIABILITY.MART.FCT_COUNTY_DAY GROUP BY year),
idx AS (
  SELECT year, COUNT(*) AS storm_county_days FROM (
    SELECT DISTINCT year, CASE WHEN county_id_fips = '51515' THEN '51019' ELSE county_id_fips END AS f, begin_yearmonth, begin_day
    FROM RELIABILITY.STG.NOAA_VA_EVENTS
    WHERE line_risk <> 'other' AND county_id_fips IN (SELECT county_id_fips FROM RELIABILITY.STG.DOMINION_VA_COUNTIES)
  ) x GROUP BY year
)
SELECT p.year, p.storm_county_days, i.storm_county_days AS index_days
FROM panel p JOIN idx i USING (year) WHERE p.storm_county_days <> i.storm_county_days;

-- T22. Hourly customer-hours add up to the 15-minute total (expected 0 rows)
SELECT 'mismatch' AS t FROM (SELECT SUM(customer_hours) AS a FROM RELIABILITY.MART.FCT_OUTAGE_COUNTY_HOUR) h,
     (SELECT SUM(customers_out) * 0.25 AS b FROM RELIABILITY.STG.EAGLEI_VA_15MIN) s
WHERE ABS(h.a - s.b) > 1;

-- T23. Restoration curves are bounded and start at the peak (expected 0 rows)
SELECT event_key FROM RELIABILITY.MART.FCT_RESTORATION_CURVE
WHERE share_restored < 0 OR share_restored > 1 OR (hour_since_peak = 0 AND share_restored > 0.5);

-- T24. Every full year 2015 to 2025 has between 1 and 20 proxy major event days (expected 0 rows)
SELECT year, SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) AS med_days FROM RELIABILITY.MART.FCT_TERRITORY_DAY
WHERE year BETWEEN 2015 AND 2025 GROUP BY year
HAVING SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) NOT BETWEEN 1 AND 20;

-- ---------- 5. Analysis ----------
-- Q12. Readings, failed runs and zero rows by year (data quality, docs/03 P20 to P23)
SELECT YEAR(ts_utc) AS year, COUNT(*) AS county_slots, SUM(valued_rows) AS valued,
       COUNT(*) - COUNT(customers_out) AS failed_slots,
       SUM(CASE WHEN customers_out = 0 THEN 1 ELSE 0 END) AS zero_rows,
       COUNT(DISTINCT county_fips) AS counties
FROM RELIABILITY.STG.EAGLEI_VA_15MIN GROUP BY 1 ORDER BY 1;

-- Q13. The ten largest territory events (A2)
SELECT event_key, start_utc, peak_utc, peak_customers_out, ROUND(hours_above_threshold, 1) AS hours_above_10k,
       ROUND(customer_hours) AS customer_hours, ROUND(background_customers_out) AS background,
       ROUND(hours_to_50pct, 1) AS h50, ROUND(hours_to_90pct, 1) AS h90, ROUND(hours_to_99pct, 1) AS h99
FROM RELIABILITY.MART.FCT_OUTAGE_EVENT WHERE scope = 'territory'
ORDER BY peak_customers_out DESC LIMIT 10;

-- Q14. Proxy major event days and customer-hours by year, against EIA SAIDI (A5)
WITH y AS (
  SELECT year, COUNT(*) AS days, SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) AS med_days,
         SUM(customer_hours) AS ch_all, SUM(CASE WHEN NOT is_med_proxy THEN customer_hours ELSE 0 END) AS ch_ex_med
  FROM RELIABILITY.MART.FCT_TERRITORY_DAY GROUP BY year
),
basis AS (SELECT SUM(customers_basis) AS customers FROM RELIABILITY.MART.DIM_COUNTY WHERE dominion_county)
SELECT y.year, y.med_days, ROUND(60 * y.ch_all / b.customers, 1) AS eaglei_minutes_per_customer_all,
       ROUND(60 * y.ch_ex_med / b.customers, 1) AS eaglei_minutes_per_customer_ex_med,
       f.saidi_all, f.saidi_ex_med
FROM y CROSS JOIN basis b
LEFT JOIN RELIABILITY.MART.FCT_RELIABILITY f ON f.utility_key = '19876|VA' AND f.year = y.year
WHERE y.year BETWEEN 2015 AND 2025 ORDER BY y.year;

-- Q15. County outage events on non-major days per county per year (A3)
SELECT area_code AS county_fips, year, COUNT(*) AS events
FROM RELIABILITY.MART.FCT_OUTAGE_EVENT
WHERE scope = 'county' AND NOT starts_on_med_proxy_day AND year BETWEEN 2015 AND 2025
GROUP BY 1, 2 ORDER BY 1, 2;
