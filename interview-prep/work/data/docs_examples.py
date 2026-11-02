"""Numbers for the docs 05 and 08 worked examples (EAGLE-I county-day, A1 ratio, Isaias event, DOE-417 match,
proxy major event days, county map). Read-only queries on the DuckDB mirror; prints every result."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)


def show(title, sql):
    print(f"\n### {title}\n{sql}\n")
    print(con.execute(sql).df().to_string(index=False))


show("county 51041 basis", "SELECT county_fips, county_label, customers_basis, customers_basis_source, dominion_county, dominion_only_county "
     "FROM mart.DIM_COUNTY WHERE county_fips IN ('51041', '51143', '51153')")
show("county-day 51041 2025-07-18 and neighbours", """SELECT county_fips, day, customer_hours, customer_hours_per_1k, customers_out_max,
       failed_readings, storm_day, storm_wind, max_gust_kt
FROM mart.FCT_COUNTY_DAY WHERE county_fips = '51041' AND day BETWEEN DATE '2025-07-17' AND DATE '2025-07-19' ORDER BY day""")
show("15-min readings 51041 EST day 2025-07-18", """SELECT COUNT(*) AS slots, COUNT(customers_out) AS with_value,
       SUM(customers_out) AS sum_customers_out, SUM(customers_out) * 0.25 AS customer_hours, MAX(customers_out) AS max_out,
       MIN(ts_utc) AS first_utc, MAX(ts_utc) AS last_utc
FROM stg.EAGLEI_VA_15MIN
WHERE county_fips = '51041' AND CAST(ts_utc - INTERVAL 5 HOUR AS DATE) = DATE '2025-07-18'""")
show("A1 ratio in SQL", """WITH p AS (
  SELECT storm_day, customer_hours_per_1k FROM mart.FCT_COUNTY_DAY
  WHERE failed_readings = 0 AND county_fips NOT IN ('51600', '51683', '51660', '51520'))
SELECT SUM(CASE WHEN storm_day THEN 1 ELSE 0 END) AS storm_county_days,
       SUM(CASE WHEN NOT storm_day THEN 1 ELSE 0 END) AS calm_county_days,
       ROUND(AVG(CASE WHEN storm_day THEN customer_hours_per_1k END), 1) AS storm_mean,
       ROUND(AVG(CASE WHEN NOT storm_day THEN customer_hours_per_1k END), 2) AS calm_mean,
       ROUND(AVG(CASE WHEN storm_day THEN customer_hours_per_1k END)
           / AVG(CASE WHEN NOT storm_day THEN customer_hours_per_1k END), 1) AS ratio
FROM p""")
show("Isaias event", """SELECT event_key, start_utc, peak_utc, end_utc, peak_customers_out, peak_sustained_1h, hours_above_threshold,
       ROUND(customer_hours) AS customer_hours, background_customers_out, hours_to_50pct, hours_to_90pct, hours_to_99pct,
       starts_on_med_proxy_day, storm_type, tropical_cyclone, doe417_customers_max, size_ratio
FROM mart.FCT_EVENT_CONTEXT WHERE start_utc BETWEEN TIMESTAMP '2020-08-03' AND TIMESTAMP '2020-08-05'""")
show("Isaias restoration curve, selected hours", """SELECT hour_since_peak, customers_out, ROUND(share_restored, 3) AS share_restored
FROM mart.FCT_RESTORATION_CURVE WHERE event_key LIKE '%2020-08-04 07:45:00'
  AND hour_since_peak IN (0, 1, 6, 12, 24, 33, 34, 48, 72) ORDER BY hour_since_peak""")
show("DOE-417 rows Aug 2020", """SELECT * FROM stg.DOE417_EVENTS WHERE date_began BETWEEN DATE '2020-08-01' AND DATE '2020-08-10'""")
show("territory day 2020-08-04 and the 2020 threshold", """SELECT day, ROUND(customer_hours) AS customer_hours, customers_out_max,
       ROUND(alpha, 3) AS alpha, ROUND(beta, 3) AS beta, ROUND(med_threshold_customer_hours) AS threshold, is_med_proxy
FROM mart.FCT_TERRITORY_DAY WHERE day BETWEEN DATE '2020-08-03' AND DATE '2020-08-06' ORDER BY day""")
show("proxy MED days per year", """SELECT year(day) AS year, SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) AS med_days,
       ROUND(MAX(med_threshold_customer_hours)) AS threshold FROM mart.FCT_TERRITORY_DAY GROUP BY 1 ORDER BY 1""")
show("county map extremes", """SELECT county_fips, county_label, minutes_non_med_avg_2015_24, map_flag FROM read_csv_auto('data/output/county_outage_map.csv')
WHERE map_flag = 'ok' ORDER BY minutes_non_med_avg_2015_24 DESC LIMIT 2""")
show("county map min", """SELECT county_fips, county_label, minutes_non_med_avg_2015_24, map_flag FROM read_csv_auto('data/output/county_outage_map.csv')
WHERE map_flag = 'ok' ORDER BY minutes_non_med_avg_2015_24 ASC LIMIT 2""")
show("county-year Pittsylvania", """SELECT county_fips, year, ROUND(outage_minutes_per_customer_non_med, 1) AS min_non_med, events_non_med, storm_days, ROUND(failed_share, 3) AS failed_share
FROM mart.FCT_COUNTY_YEAR WHERE county_fips = '51143' ORDER BY year""")
