-- =====================================================================
-- DOMINION RELIABILITY MART  |  11: context for the outage events of sql/09
-- Tropical cyclone tracks (NHC HURDAT2) and DOE-417 emergency reports, matched
-- to the EAGLE-I territory events. Run after 09.
-- =====================================================================
USE WAREHOUSE SNOWFLAKE_LEARNING_WH;

-- ---------- 0. File format and stage (Snowflake only) ----------
-- Upload data/raw/hurdat2/hurdat2_points.csv (scripts/extract_hurdat2.py) and
-- data/raw/doe417/doe417_events_2014_2025.csv (scripts/extract_doe417.py).
CREATE FILE FORMAT IF NOT EXISTS RELIABILITY.RAW.FF_CONTEXT_CSV
  TYPE = CSV
  SKIP_HEADER = 1
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  NULL_IF = ('')
  EMPTY_FIELD_AS_NULL = TRUE;

CREATE STAGE IF NOT EXISTS RELIABILITY.RAW.CONTEXT_STAGE FILE_FORMAT = RELIABILITY.RAW.FF_CONTEXT_CSV;

-- ---------- 1. Raw tables, all text ----------
CREATE OR REPLACE TABLE RELIABILITY.RAW.HURDAT2_POINTS (
  storm_id VARCHAR, storm_name VARCHAR, obs_date VARCHAR, obs_time VARCHAR, record_id VARCHAR,
  status VARCHAR, lat VARCHAR, lon VARCHAR, max_wind_kt VARCHAR, min_pressure_mb VARCHAR
);
COPY INTO RELIABILITY.RAW.HURDAT2_POINTS FROM @RELIABILITY.RAW.CONTEXT_STAGE/hurdat2_points.csv;

CREATE OR REPLACE TABLE RELIABILITY.RAW.DOE417_EVENTS (
  year VARCHAR, source_file VARCHAR, source_row VARCHAR, event_month VARCHAR, date_began VARCHAR,
  time_began VARCHAR, date_restored VARCHAR, time_restored VARCHAR, area_affected VARCHAR,
  nerc_region VARCHAR, alert_criteria VARCHAR, event_type VARCHAR, demand_loss_mw VARCHAR,
  customers_affected VARCHAR, date_began_raw VARCHAR, time_began_raw VARCHAR,
  date_restored_raw VARCHAR, time_restored_raw VARCHAR
);
COPY INTO RELIABILITY.RAW.DOE417_EVENTS FROM @RELIABILITY.RAW.CONTEXT_STAGE/doe417_events_2014_2025.csv;

-- ---------- 2. Staging ----------
-- Track points from 2014 on, with a timestamp and the great-circle distance in km
-- to Richmond (37.54 N, 77.44 W), the middle of Dominion's Virginia territory.
CREATE OR REPLACE VIEW RELIABILITY.STG.HURDAT2_POINTS AS
SELECT storm_id, storm_name, status,
       TRY_TO_TIMESTAMP_NTZ(obs_date || ' ' || obs_time, 'YYYYMMDD HH24MI')              AS obs_utc,
       TRY_TO_NUMBER(lat, 6, 1)                                                          AS lat,
       TRY_TO_NUMBER(lon, 6, 1)                                                          AS lon,
       TRY_TO_NUMBER(max_wind_kt)                                                        AS max_wind_kt,
       2 * 6371 * ASIN(SQRT(POWER(SIN(RADIANS(TRY_TO_NUMBER(lat, 6, 1) - 37.54) / 2), 2)
             + COS(RADIANS(37.54)) * COS(RADIANS(TRY_TO_NUMBER(lat, 6, 1)))
             * POWER(SIN(RADIANS(TRY_TO_NUMBER(lon, 6, 1) + 77.44) / 2), 2)))         AS km_from_richmond
FROM RELIABILITY.RAW.HURDAT2_POINTS
WHERE LEFT(obs_date, 4) >= '2014';

-- DOE-417 rows with numbers cast and the Virginia flags. There is no utility
-- column, so Dominion is matched by area, date and size (decision D19):
--   virginia_row: Area Affected still names Virginia after "West Virginia" (also
--     written "WestVirginia" in 2024-25) is removed;
--   dominion_area: a Virginia row that names no other state except North Carolina
--     (Dominion's other state). Rows that also name West Virginia, Kentucky,
--     Tennessee, Ohio and the rest are left out: Appalachian Power and other
--     utilities serve those combinations.
CREATE OR REPLACE VIEW RELIABILITY.STG.DOE417_EVENTS AS
SELECT TRY_TO_NUMBER(year)                       AS file_year,
       source_file, TRY_TO_NUMBER(source_row)    AS source_row,
       TRY_TO_DATE(date_began)                   AS date_began,
       time_began,
       TRY_TO_DATE(date_restored)                AS date_restored,
       area_affected, alert_criteria, event_type,
       TRY_TO_NUMBER(REPLACE(demand_loss_mw, ',', ''))     AS demand_loss_mw,
       TRY_TO_NUMBER(REPLACE(customers_affected, ',', '')) AS customers_affected,
       REPLACE(REPLACE(LOWER(area_affected), 'west virginia', ''), 'westvirginia', '') LIKE '%virginia%' AS virginia_row,
       REPLACE(REPLACE(LOWER(area_affected), 'west virginia', ''), 'westvirginia', '') LIKE '%virginia%'
         AND NOT REGEXP_LIKE(area_affected,
               '.*(West ?Virginia|Kentucky|Tennessee|Ohio|Indiana|Michigan|Georgia|Alabama|Mississippi|Maryland|District of Columbia|Pennsylvania|Delaware|New Jersey|New York|South Carolina|Florida|Louisiana|Arkansas|Texas).*', 'is')
                                                 AS dominion_area
FROM RELIABILITY.RAW.DOE417_EVENTS;

-- ---------- 3. Mart: one row per territory event with its context ----------
-- Storm type: Dominion county-days with NOAA line-risk reports on the event's
-- days (start day to end day, Eastern Standard Time), by type; the dominant type
-- has the most county-days. Tropical cyclone: any HURDAT2 track point within
-- 400 km of Richmond from 24 hours before the event starts to its peak.
-- DOE-417: dominion_area outage reports (customers affected above zero, or unknown
-- for a weather event; security reports with no customers out are not outages) that
-- began from one day before the start day to one day after the end day;
-- size_ratio = EAGLE-I peak / DOE-417 customers affected. EAGLE-I's peak is the
-- most customers out at one time, for every utility in the 103 counties; DOE-417
-- counts customers affected over the event, for the reporting utility.
CREATE OR REPLACE TABLE RELIABILITY.MART.FCT_EVENT_CONTEXT COPY GRANTS AS
WITH ev AS (
  SELECT e.*, CAST(e.end_utc - INTERVAL '5 HOUR' AS DATE) AS end_day
  FROM RELIABILITY.MART.FCT_OUTAGE_EVENT e
  WHERE e.scope = 'territory'
),
noaa AS (
  SELECT ev.event_key,
         SUM(CASE WHEN d.storm_wind     THEN 1 ELSE 0 END) AS wind_county_days,
         SUM(CASE WHEN d.storm_winter   THEN 1 ELSE 0 END) AS winter_county_days,
         SUM(CASE WHEN d.storm_tropical THEN 1 ELSE 0 END) AS tropical_county_days,
         COUNT(DISTINCT CASE WHEN d.storm_day THEN d.county_fips END) AS storm_counties,
         MAX(d.max_gust_kt)                                 AS max_gust_kt
  FROM ev
  JOIN RELIABILITY.MART.FCT_COUNTY_DAY d ON d.day BETWEEN ev.start_day AND ev.end_day
  GROUP BY ev.event_key
),
tc_hit AS (
  SELECT ev.event_key, h.storm_name, MIN(h.km_from_richmond) AS km
  FROM ev
  JOIN RELIABILITY.STG.HURDAT2_POINTS h
    ON h.obs_utc BETWEEN ev.start_utc - INTERVAL '24 HOUR' AND ev.peak_utc
   AND h.km_from_richmond <= 400
  GROUP BY ev.event_key, h.storm_name
),
tc AS (
  SELECT event_key,
         LISTAGG(storm_name, ', ') WITHIN GROUP (ORDER BY storm_name) AS tropical_cyclone,
         MIN(km)                                                     AS tc_min_km
  FROM tc_hit GROUP BY event_key
),
doe AS (
  SELECT ev.event_key,
         COUNT(*)                     AS doe417_reports,
         MAX(o.customers_affected)    AS doe417_customers_max,
         MIN(o.date_began)            AS doe417_first_date,
         LISTAGG(o.area_affected, ' | ') WITHIN GROUP (ORDER BY o.date_began, o.source_row) AS doe417_areas
  FROM ev
  JOIN RELIABILITY.STG.DOE417_EVENTS o
    ON o.dominion_area AND o.date_began BETWEEN ev.start_day - 1 AND ev.end_day + 1
   AND (o.customers_affected > 0 OR (o.customers_affected IS NULL AND LOWER(o.event_type) LIKE '%weather%'))
  GROUP BY ev.event_key
)
SELECT ev.event_key, ev.start_utc, ev.peak_utc, ev.end_utc, ev.start_day, ev.end_day, ev.year,
       ev.peak_customers_out, ev.peak_sustained_1h, ev.hours_above_threshold, ev.customer_hours, ev.background_customers_out,
       ev.hours_to_50pct, ev.hours_to_90pct, ev.hours_to_99pct, ev.starts_on_med_proxy_day,
       COALESCE(n.wind_county_days, 0)     AS wind_county_days,
       COALESCE(n.winter_county_days, 0)   AS winter_county_days,
       COALESCE(n.tropical_county_days, 0) AS tropical_county_days,
       COALESCE(n.storm_counties, 0)       AS storm_counties,
       n.max_gust_kt,
       CASE WHEN t.tropical_cyclone IS NOT NULL OR COALESCE(n.tropical_county_days, 0) > 0 THEN 'tropical'
            WHEN COALESCE(n.wind_county_days, 0) = 0 AND COALESCE(n.winter_county_days, 0) = 0 THEN 'no NOAA line-risk report'
            WHEN n.winter_county_days > n.wind_county_days THEN 'winter'
            ELSE 'wind' END                AS storm_type,
       t.tropical_cyclone, t.tc_min_km,
       COALESCE(d.doe417_reports, 0)       AS doe417_reports,
       d.doe417_customers_max, d.doe417_first_date, d.doe417_areas,
       ev.peak_customers_out / NULLIF(d.doe417_customers_max, 0) AS size_ratio
FROM ev
LEFT JOIN noaa n ON n.event_key = ev.event_key
LEFT JOIN tc   t ON t.event_key = ev.event_key
LEFT JOIN doe  d ON d.event_key = ev.event_key;

-- ---------- 4. Tests ----------
-- T25. HURDAT2 points parse and the 2014-2025 storms are all there (expected 1 row: value 0 in problems)
SELECT CASE WHEN COUNT(*) > 0 AND COUNT(obs_utc) = COUNT(*) AND COUNT(lat) = COUNT(*)
             AND COUNT(DISTINCT storm_id) BETWEEN 200 AND 400 THEN 0 ELSE 1 END AS problems
FROM RELIABILITY.STG.HURDAT2_POINTS;

-- T26. DOE-417: every row of the long file is staged, 3,702 rows, and 2024 and 2025 equal the
--      files' "Total Records" (622 and 426) (expected 1 row: value 0 in problems)
SELECT CASE WHEN COUNT(*) = 3702 AND SUM(CASE WHEN file_year = 2024 THEN 1 ELSE 0 END) = 622
             AND SUM(CASE WHEN file_year = 2025 THEN 1 ELSE 0 END) = 426 THEN 0 ELSE 1 END AS problems
FROM RELIABILITY.STG.DOE417_EVENTS;

-- T27. One context row per territory event (expected 1 row: value 0 in problems)
SELECT CASE WHEN (SELECT COUNT(*) FROM RELIABILITY.MART.FCT_EVENT_CONTEXT)
               = (SELECT COUNT(*) FROM RELIABILITY.MART.FCT_OUTAGE_EVENT WHERE scope = 'territory')
             AND (SELECT COUNT(DISTINCT event_key) FROM RELIABILITY.MART.FCT_EVENT_CONTEXT)
               = (SELECT COUNT(*) FROM RELIABILITY.MART.FCT_EVENT_CONTEXT) THEN 0 ELSE 1 END AS problems;

-- ---------- 5. Analysis ----------
-- Q16. The ten largest territory events with their context (A2)
SELECT event_key, start_day, peak_customers_out, ROUND(hours_above_threshold, 1) AS hours_above_10k,
       ROUND(hours_to_50pct, 1) AS h50, ROUND(hours_to_90pct, 1) AS h90, ROUND(hours_to_99pct, 1) AS h99,
       storm_type, tropical_cyclone, doe417_customers_max, ROUND(size_ratio, 2) AS size_ratio
FROM RELIABILITY.MART.FCT_EVENT_CONTEXT
ORDER BY peak_customers_out DESC LIMIT 10;

-- Q17. DOE-417 Dominion-area reports and whether an EAGLE-I territory event matches (D19)
SELECT o.date_began, o.area_affected, o.event_type, o.customers_affected,
       MAX(c.event_key) AS matched_event, MAX(c.peak_customers_out) AS eaglei_peak
FROM RELIABILITY.STG.DOE417_EVENTS o
LEFT JOIN RELIABILITY.MART.FCT_EVENT_CONTEXT c
  ON o.date_began BETWEEN c.start_day - 1 AND c.end_day + 1
WHERE o.dominion_area AND o.date_began >= '2014-11-01'
GROUP BY 1, 2, 3, 4 ORDER BY 1;
