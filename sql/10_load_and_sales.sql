-- =====================================================================
-- DOMINION RELIABILITY MART  |  10: load shape, seasonal peaks, degree days
-- and retail sales by sector. Run after 06 (EIA-930) and 02 (sales).
-- The PJM DOM zone (EIA-930) is larger than Dominion's Virginia retail
-- territory; hourly load by county is not public (decision D14 still holds:
-- nothing here attributes growth to data centers).
-- =====================================================================
USE WAREHOUSE SNOWFLAKE_LEARNING_WH;

-- ---------- 0. File format and stage (Snowflake only) ----------
-- Upload data/raw/degree_days/cpc_degree_days_long.csv (scripts/extract_degree_days.py)
-- into CONTEXT_STAGE (created in sql/11; create it here if 10 runs first).
CREATE FILE FORMAT IF NOT EXISTS RELIABILITY.RAW.FF_CONTEXT_CSV
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('')
  EMPTY_FIELD_AS_NULL = TRUE;

CREATE STAGE IF NOT EXISTS RELIABILITY.RAW.CONTEXT_STAGE FILE_FORMAT = RELIABILITY.RAW.FF_CONTEXT_CSV;

-- ---------- 1. Raw table, all text ----------
-- NOAA CPC population-weighted daily heating and cooling degree days by state
CREATE OR REPLACE TABLE RELIABILITY.RAW.CPC_DEGREE_DAYS (
  region VARCHAR, obs_date VARCHAR, kind VARCHAR, degree_days VARCHAR
);
COPY INTO RELIABILITY.RAW.CPC_DEGREE_DAYS FROM @RELIABILITY.RAW.CONTEXT_STAGE/cpc_degree_days_long.csv;

-- ---------- 2. Staging ----------
-- Virginia, one row per day: heating and cooling degree days (base 65 F)
CREATE OR REPLACE VIEW RELIABILITY.STG.VA_DEGREE_DAYS AS
SELECT TRY_TO_DATE(obs_date) AS obs_date,
       MAX(CASE WHEN kind = 'HDD' THEN TRY_TO_NUMBER(degree_days) END) AS hdd,
       MAX(CASE WHEN kind = 'CDD' THEN TRY_TO_NUMBER(degree_days) END) AS cdd
FROM RELIABILITY.RAW.CPC_DEGREE_DAYS
WHERE region = 'VA'
GROUP BY 1;

-- ---------- 3. Mart ----------
-- Hour x month x year: average and highest hourly demand, PJM DOM zone.
-- hour_no is EIA-930's hour number (1 = the hour ending 1 a.m., local time).
CREATE OR REPLACE TABLE RELIABILITY.MART.DOM_LOAD_HOUR_MONTH COPY GRANTS AS
SELECT YEAR(data_date)            AS year,
       MONTH(data_date)           AS month,
       hour_no,
       ROUND(AVG(demand_mw))      AS avg_mw,
       MAX(demand_mw)             AS max_mw,
       COUNT(demand_mw)           AS hours_reported
FROM RELIABILITY.STG.EIA930_DOM_HOURLY
WHERE hour_no BETWEEN 1 AND 24
GROUP BY 1, 2, 3;

-- Seasonal peaks with the date and hour they happened. Winter = Dec, Jan, Feb of
-- the same calendar year and summer = Jun, Jul, Aug, as in DOM_LOAD_ANNUAL (sql/06).
CREATE OR REPLACE TABLE RELIABILITY.MART.DOM_SEASONAL_PEAK COPY GRANTS AS
WITH s AS (
  SELECT YEAR(data_date) AS year,
         CASE WHEN MONTH(data_date) IN (12, 1, 2) THEN 'winter'
              WHEN MONTH(data_date) IN (6, 7, 8)  THEN 'summer' END AS season,
         data_date, hour_no, demand_mw
  FROM RELIABILITY.STG.EIA930_DOM_HOURLY
  WHERE demand_mw IS NOT NULL
)
SELECT year, season,
       MAX(demand_mw)                   AS peak_mw,
       MAX_BY(data_date, demand_mw)     AS peak_date,
       MAX_BY(hour_no, demand_mw)       AS peak_hour_no,
       COUNT(*)                         AS hours_reported
FROM s
WHERE season IS NOT NULL
GROUP BY 1, 2;

-- Daily load with Virginia degree days, for the weather-normalised trend (A4).
CREATE OR REPLACE TABLE RELIABILITY.MART.DOM_LOAD_DAILY COPY GRANTS AS
SELECT h.data_date,
       YEAR(h.data_date)                AS year,
       MONTH(h.data_date)               AS month,
       DAYOFWEEKISO(h.data_date)        AS iso_weekday,
       ROUND(AVG(h.demand_mw))          AS avg_mw,
       MAX(h.demand_mw)                 AS max_mw,
       MIN(h.demand_mw)                 AS min_mw,
       COUNT(h.demand_mw)               AS hours_reported,
       MAX(d.hdd)                       AS hdd,
       MAX(d.cdd)                       AS cdd
FROM RELIABILITY.STG.EIA930_DOM_HOURLY h
LEFT JOIN RELIABILITY.STG.VA_DEGREE_DAYS d ON d.obs_date = h.data_date
GROUP BY 1, 2, 3, 4;

-- Dominion Energy Virginia retail sales by sector (EIA-861 via PUDL to 2024,
-- EIA-861 2025 final), bundled and delivery-only service summed.
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_SALES_SECTOR COPY GRANTS AS
SELECT year, customer_class,
       SUM(sales_mwh)                                  AS sales_mwh,
       SUM(customers)                                  AS customers,
       SUM(revenue_usd)                                AS revenue_usd,
       ROUND(SUM(sales_mwh) / NULLIF(SUM(customers), 0), 1) AS mwh_per_customer,
       SUM(CASE WHEN service_type = 'delivery' THEN sales_mwh ELSE 0 END) AS delivery_only_mwh
FROM RELIABILITY.STG.SALES
WHERE utility_id = 19876 AND state = 'VA'
GROUP BY 1, 2;

-- ---------- 4. Tests ----------
-- T28. Every month from July 2018 to October 2026 has all 24 hours in the hour x month table (expected 0 rows)
WITH m AS (SELECT year, month, COUNT(DISTINCT hour_no) AS hours FROM RELIABILITY.MART.DOM_LOAD_HOUR_MONTH GROUP BY 1, 2)
SELECT * FROM m WHERE hours <> 24
UNION ALL
SELECT 0, 0, COUNT(*) FROM m HAVING COUNT(*) <> 100;

-- T29. Commercial sales 2025 = 60,088,202 bundled + 4,532,591 delivery-only MWh, the EIA-861 2025 file (expected 0 rows)
SELECT * FROM RELIABILITY.MART.FCT_SALES_SECTOR
WHERE year = 2025 AND customer_class = 'commercial' AND sales_mwh <> 60088202 + 4532591;

-- T30. Virginia degree days: one HDD and one CDD per day from 2018-01-01, none negative (expected 1 row: value 0 in problems)
SELECT CASE WHEN COUNT(*) = COUNT(hdd) AND COUNT(*) = COUNT(cdd) AND MIN(hdd) >= 0 AND MIN(cdd) >= 0
             AND MIN(obs_date) = '2018-01-01' AND COUNT(*) = DATEDIFF('day', MIN(obs_date), MAX(obs_date)) + 1
            THEN 0 ELSE 1 END AS problems
FROM RELIABILITY.STG.VA_DEGREE_DAYS;

-- ---------- 5. Analysis ----------
-- Q18. Sector split, 2013 and 2025 (A4)
SELECT customer_class, year, sales_mwh, customers, mwh_per_customer
FROM RELIABILITY.MART.FCT_SALES_SECTOR
WHERE year IN (2013, 2019, 2025) AND customer_class IN ('residential', 'commercial', 'industrial')
ORDER BY customer_class, year;

-- Q19. Seasonal peaks by year, with the date and hour (A4)
SELECT year, season, peak_mw, peak_date, peak_hour_no FROM RELIABILITY.MART.DOM_SEASONAL_PEAK ORDER BY year, season;
