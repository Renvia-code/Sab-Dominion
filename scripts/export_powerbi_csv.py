"""Export mart tables as CSV files in data/output/ so the Power BI report can Import them from a
folder (no Snowflake connection needed during the presentation; decision D13).

Source: the DuckDB mirror built from the source files by scripts/run_local_duckdb_sources.py
(data/raw/duckdb/reliability_local.duckdb), which passes the same tests (T1-T12, T13+) as the
Snowflake build. Column names are the mart's, lower case; the Power Query step upper-cases them.
Writes data/output/powerbi_exports_manifest.csv (file, rows, bytes, sha256, source, exported_at).

Run: .venv/Scripts/python.exe -I scripts/export_powerbi_csv.py [--only name1,name2]
"""
import argparse
import csv
import datetime as dt
import hashlib
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = ROOT / "data" / "output"
MANIFEST = OUT / "powerbi_exports_manifest.csv"

PEERS = ("'19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC',"
         "'1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL'")

# (file name, source object or description, query)
EXPORTS = [
    ("fct_reliability.csv", "MART.FCT_RELIABILITY",
     "SELECT * FROM mart.FCT_RELIABILITY ORDER BY utility_key, year"),
    ("dim_utility.csv", "MART.DIM_UTILITY",
     "SELECT * FROM mart.DIM_UTILITY ORDER BY utility_key"),
    ("v_group_index.csv", "MART.V_GROUP_INDEX",
     "SELECT * FROM mart.V_GROUP_INDEX ORDER BY peer_group, year"),
    ("saidi_weather_adjusted.csv", "MART.SAIDI_WEATHER_ADJUSTED",
     "SELECT * FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year"),
    ("dom_load_annual.csv", "MART.DOM_LOAD_ANNUAL (2018 starts 1 Jul; 2026 runs to the last EIA-930 file)",
     "SELECT * FROM mart.DOM_LOAD_ANNUAL ORDER BY year"),
    ("dom_top50_hours.csv", "MART.DOM_TOP50_HOURS (union of two top-50 rankings: rank_today, rank_end_2025)",
     "SELECT * FROM mart.DOM_TOP50_HOURS ORDER BY rank_today NULLS LAST, rank_end_2025"),
    ("dom_load_profile.csv", "MART.DOM_LOAD_PROFILE",
     "SELECT * FROM mart.DOM_LOAD_PROFILE ORDER BY hour_no"),
    ("peer_reliability_5yr.csv",
     "derived from MART.FCT_RELIABILITY and MART.DIM_UTILITY: the 12 large-utility peers (sql/03), "
     "SAIDI 2023-25 mean, SAIFI and CAIDI 2021-25 means of the annual ex-MED values, ranks (1 = highest)",
     f"""WITH u AS (
  SELECT f.utility_key, d.utility_name, d.peer_group,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_2023_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.caidi_ex_med END) AS caidi_2021_25,
         COUNT(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS years_2021_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ({PEERS})
  GROUP BY 1, 2, 3)
SELECT utility_key, utility_name, peer_group, utility_key = '19876|VA' AS is_dominion,
       ROUND(saidi_2023_25, 1) AS saidi_2023_25, ROUND(saifi_2021_25, 3) AS saifi_2021_25,
       ROUND(caidi_2021_25, 1) AS caidi_2021_25, years_2021_25,
       RANK() OVER (ORDER BY saidi_2023_25 DESC) AS saidi_rank_highest,
       RANK() OVER (ORDER BY saifi_2021_25 DESC) AS saifi_rank_highest,
       RANK() OVER (ORDER BY caidi_2021_25 DESC) AS caidi_rank_highest,
       ROUND(MEDIAN(saidi_2023_25) OVER (), 1) AS median_saidi_2023_25,
       ROUND(MEDIAN(saifi_2021_25) OVER (), 3) AS median_saifi_2021_25,
       ROUND(MEDIAN(caidi_2021_25) OVER (), 1) AS median_caidi_2021_25
FROM u ORDER BY saifi_2021_25 DESC"""),
    # ---- EAGLE-I county outages (sql/09) and event context (sql/11) ----
    ("dim_county.csv", "MART.DIM_COUNTY (133 Virginia counties and cities, Dominion-county rule and reason)",
     "SELECT * FROM mart.DIM_COUNTY ORDER BY county_fips"),
    ("fct_county_year.csv", "MART.FCT_COUNTY_YEAR (103 Dominion counties x 2015-2025)",
     "SELECT * FROM mart.FCT_COUNTY_YEAR ORDER BY county_fips, year"),
    ("county_outage_map.csv",
     "derived from MART.FCT_COUNTY_YEAR and FCT_COUNTY_DAY: one row per Dominion county for the map, 2015-2024 averages, map_flag",
     """WITH r AS (
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
FROM y GROUP BY county_fips, county_label, dominion_only_county, map_flag ORDER BY county_fips"""),
    ("fct_territory_day.csv", "MART.FCT_TERRITORY_DAY (103 Dominion counties together, one row per day, proxy major event days)",
     """SELECT day, year, customer_hours, customers_out_max, failed_readings, storm_counties,
       ROUND(alpha, 6) AS alpha, ROUND(beta, 6) AS beta, window_days,
       ROUND(med_threshold_customer_hours, 1) AS med_threshold_customer_hours, is_med_proxy
FROM mart.FCT_TERRITORY_DAY ORDER BY day"""),  # rounded: parallel float sums differ in the last bits
    ("fct_event_context.csv", "MART.FCT_EVENT_CONTEXT (every territory outage event with storm type, tropical cyclone and DOE-417 match)",
     "SELECT * FROM mart.FCT_EVENT_CONTEXT ORDER BY start_utc"),
    ("outage_events_top10.csv", "derived from MART.FCT_EVENT_CONTEXT: the ten largest events by the level held for one hour",
     """SELECT ROW_NUMBER() OVER (ORDER BY peak_sustained_1h DESC) AS rank, event_key, start_day,
       CAST(peak_utc - INTERVAL '5 HOUR' AS DATE) AS peak_day, storm_type, tropical_cyclone,
       peak_customers_out, peak_sustained_1h, ROUND(hours_above_threshold, 1) AS hours_above_10k,
       ROUND(customer_hours) AS customer_hours, ROUND(hours_to_50pct, 1) AS hours_to_50pct,
       ROUND(hours_to_90pct, 1) AS hours_to_90pct, ROUND(hours_to_99pct, 1) AS hours_to_99pct,
       doe417_customers_max, starts_on_med_proxy_day
FROM mart.FCT_EVENT_CONTEXT ORDER BY peak_sustained_1h DESC LIMIT 10"""),
    ("fct_restoration_curve.csv", "MART.FCT_RESTORATION_CURVE (hourly, 7 days from the peak, territory events peaking at 50,000+)",
     "SELECT * FROM mart.FCT_RESTORATION_CURVE ORDER BY event_key, hour_since_peak"),
    # ---- load and sales (sql/10); EIA-930 to the hour ending midnight 29 Oct 2026 ----
    ("dom_load_hour_month.csv", "MART.DOM_LOAD_HOUR_MONTH (year x month x hour, PJM DOM zone; to 29 Oct 2026)",
     "SELECT * FROM mart.DOM_LOAD_HOUR_MONTH ORDER BY year, month, hour_no"),
    ("dom_seasonal_peak.csv", "MART.DOM_SEASONAL_PEAK (year x season, date and hour of the peak)",
     "SELECT * FROM mart.DOM_SEASONAL_PEAK ORDER BY year, season"),
    ("dom_load_daily.csv", "MART.DOM_LOAD_DAILY (daily load with Virginia degree days; to 29 Oct 2026)",
     "SELECT * FROM mart.DOM_LOAD_DAILY ORDER BY data_date"),
    ("fct_sales_sector.csv", "MART.FCT_SALES_SECTOR (Dominion VA retail sales by class, 2013-2025)",
     "SELECT * FROM mart.FCT_SALES_SECTOR ORDER BY year, customer_class"),
]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated file stems to export")
    args = ap.parse_args()
    only = set(args.only.split(",")) if args.only else None
    con = duckdb.connect(str(DB), read_only=True)
    old = {}
    if MANIFEST.exists():
        with MANIFEST.open(newline="", encoding="utf-8") as f:
            old = {r["file"]: r for r in csv.DictReader(f)}
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for name, source, sql in EXPORTS:
        if only and Path(name).stem not in only:
            continue
        p = OUT / name
        df = con.execute(sql).df()
        df.to_csv(p, index=False, encoding="utf-8", lineterminator="\n")
        old[name] = {"file": name, "rows": len(df), "bytes": p.stat().st_size, "sha256": sha256(p),
                     "source": source, "exported_at": now}
        print(f"{name}: {len(df):,} rows, {p.stat().st_size:,} bytes")
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "rows", "bytes", "sha256", "source", "exported_at"], lineterminator="\n")
        w.writeheader()
        for k in sorted(old):
            w.writerow(old[k])


if __name__ == "__main__":
    main()
