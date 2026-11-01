"""Export mart tables as CSV files in data/output/ so the Power BI report can Import them from a
folder (no Snowflake connection needed during the presentation; decision D13).

Source: the DuckDB mirror built from the source files by scripts/run_local_duckdb_sources.py
(data/raw/duckdb/reliability_local.duckdb), which passes the same tests (T1-T12, T13+) as the
Snowflake build. Column names are the mart's, lower case; the Power Query step upper-cases them.
Writes data/output/powerbi_exports_manifest.csv (file, rows, bytes, sha256, source, exported_at).
For the report's Data notes page it also writes reconciliation.csv (rebuilt figures against the
values their publishers print) and test_results.csv (tests T1 onward, run read-only on the same
database), and storm_vs_calm.csv (scripts/storm_vs_calm_ratio.py: storm against calm county-days,
with bootstrap intervals).

Run: .venv/Scripts/python.exe -I scripts/export_powerbi_csv.py [--only name1,name2]
"""
import argparse
import csv
import datetime as dt
import hashlib
import re
import sys
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
    # the two original weather summaries, same columns and number format as first committed (decision D22 re-export)
    ("storm_index.csv", "MART.STORM_INDEX (Bedford city folded into Bedford County, D22)",
     """SELECT year, CAST(storm_county_days AS INTEGER) AS storm_county_days, CAST(wind_days AS INTEGER) AS wind_days,
       CAST(winter_days AS INTEGER) AS winter_days, CAST(tropical_days AS INTEGER) AS tropical_days,
       CAST(severe_gust_days AS INTEGER) AS severe_gust_days
FROM mart.STORM_INDEX ORDER BY year"""),
    ("storm_vs_saidi.csv", "MART.V_STORM_VS_SAIDI (D22)",
     """SELECT year, CAST(storm_county_days AS INTEGER) AS storm_county_days, CAST(wind_days AS INTEGER) AS wind_days,
       CAST(winter_days AS INTEGER) AS winter_days, CAST(tropical_days AS INTEGER) AS tropical_days,
       CAST(severe_gust_days AS INTEGER) AS severe_gust_days,
       printf('%.3f', saidi_ex_med) AS saidi_ex_med, printf('%.3f', saifi_ex_med) AS saifi_ex_med,
       printf('%.3f', storm_saidi) AS storm_saidi
FROM mart.V_STORM_VS_SAIDI ORDER BY year"""),
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
    # ---- storms by county (county-day panel, sql/09): NOAA storm county-days per county and year ----
    ("storm_county_year.csv",
     "derived from MART.FCT_COUNTY_DAY: NOAA storm county-days by county, year and type, 103 Dominion counties, 2015-2025 (D22 fold)",
     """SELECT county_fips, year,
       CAST(SUM(CASE WHEN storm_day THEN 1 ELSE 0 END) AS INTEGER)      AS storm_days,
       CAST(SUM(CASE WHEN storm_wind THEN 1 ELSE 0 END) AS INTEGER)     AS wind_days,
       CAST(SUM(CASE WHEN storm_winter THEN 1 ELSE 0 END) AS INTEGER)   AS winter_days,
       CAST(SUM(CASE WHEN storm_tropical THEN 1 ELSE 0 END) AS INTEGER) AS tropical_days,
       CAST(MAX(max_gust_kt) AS INTEGER)                                AS max_gust_kt
FROM mart.FCT_COUNTY_DAY GROUP BY county_fips, year ORDER BY county_fips, year"""),
    # ---- Data notes: rebuilt figures against the values their publishers print ----
    # Reported values are typed from the cited documents; decimals = the precision the publisher prints.
    ("reconciliation.csv",
     "derived from MART.FCT_RELIABILITY and FCT_SALES_SECTOR against published values (annual report, EIA-861 2024 and 2025 final files)",
     """WITH f AS (SELECT * FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA'),
rebuilt AS (
  SELECT 1 AS row_no, '3-year SAIDI ex-MED, 2022-2024 (minutes)' AS metric, AVG(CASE WHEN year BETWEEN 2022 AND 2024 THEN saidi_ex_med END) AS rebuilt FROM f
  UNION ALL SELECT 2, '3-year SAIDI ex-MED, 2023-2025 (minutes)', AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END) FROM f
  UNION ALL SELECT 3, 'SAIDI ex-MED 2025 (minutes)', MAX(CASE WHEN year = 2025 THEN saidi_ex_med END) FROM f
  UNION ALL SELECT 4, 'SAIFI ex-MED 2025', MAX(CASE WHEN year = 2025 THEN saifi_ex_med END) FROM f
  UNION ALL SELECT 5, 'CAIDI ex-MED 2025 (minutes)', MAX(CASE WHEN year = 2025 THEN caidi_ex_med END) FROM f
  UNION ALL SELECT 6, 'SAIDI all events 2025 (minutes)', MAX(CASE WHEN year = 2025 THEN saidi_all END) FROM f
  UNION ALL SELECT 7, 'Customers 2025 (Virginia)', MAX(CASE WHEN year = 2025 THEN customers END) FROM f
  UNION ALL SELECT 8, 'SAIDI ex-MED 2024 (minutes)', MAX(CASE WHEN year = 2024 THEN saidi_ex_med END) FROM f
  UNION ALL SELECT 9, 'SAIFI ex-MED 2024', MAX(CASE WHEN year = 2024 THEN saifi_ex_med END) FROM f
  UNION ALL SELECT 10, 'CAIDI ex-MED 2024 (minutes)', MAX(CASE WHEN year = 2024 THEN caidi_ex_med END) FROM f
  UNION ALL SELECT 11, 'SAIDI all events 2024 (minutes)', MAX(CASE WHEN year = 2024 THEN saidi_all END) FROM f
  UNION ALL SELECT 12, 'Commercial sales 2025 (MWh, bundled + delivery-only)',
                   (SELECT SUM(sales_mwh) FROM mart.FCT_SALES_SECTOR WHERE year = 2025 AND customer_class = 'commercial')
),
reported(row_no, reported, decimals, reported_source) AS (VALUES
  (1, 130, 0, 'Dominion Energy 2025 Annual Report, printed p. 10: "the previous three-year average of 130 minutes"'),
  (2, 133, 0, 'Dominion Energy 2025 Annual Report, printed p. 10: "133 minutes for the three-year average ending 2025"'),
  (3, 144.4, 3, 'EIA-861 2025 final (f8612025.zip, Reliability_2025.xlsx, Other standard)'),
  (4, 1.32, 3, 'EIA-861 2025 final (f8612025.zip, Reliability_2025.xlsx, Other standard)'),
  (5, 109.394, 3, 'EIA-861 2025 final (f8612025.zip, Reliability_2025.xlsx, Other standard)'),
  (6, 306.7, 3, 'EIA-861 2025 final (f8612025.zip, Reliability_2025.xlsx, Other standard)'),
  (7, 2675735, 0, 'EIA-861 2025 final (f8612025.zip, Reliability_2025.xlsx)'),
  (8, 131.3, 3, 'EIA-861 2024 (f8612024.zip, Reliability_2024.xlsx); the mart reads 2024 from PUDL'),
  (9, 1.21, 3, 'EIA-861 2024 (f8612024.zip, Reliability_2024.xlsx); the mart reads 2024 from PUDL'),
  (10, 108.512, 3, 'EIA-861 2024 (f8612024.zip, Reliability_2024.xlsx); the mart reads 2024 from PUDL'),
  (11, 172.1, 3, 'EIA-861 2024 (f8612024.zip, Reliability_2024.xlsx); the mart reads 2024 from PUDL'),
  (12, 64620793, 0, 'EIA-861 2025 final: 60,088,202 bundled + 4,532,591 delivery-only MWh (test T29)')
)
SELECT r.row_no, r.metric, ROUND(r.rebuilt, 3) AS rebuilt, p.reported, ROUND(r.rebuilt - p.reported, 3) AS difference,
       p.decimals AS reported_decimals, p.reported_source,
       CASE WHEN ROUND(r.rebuilt, p.decimals) = p.reported THEN 'MATCH' ELSE 'DIFFERS' END AS verdict
FROM rebuilt r JOIN reported p USING (row_no) ORDER BY r.row_no"""),
]

# ---- Data notes: results of tests T1-T31, run on the same DuckDB build ----
# Expected results of T1-T12 as the two runners assert them (run_local_duckdb.py: T1-T6;
# run_local_duckdb_sources.py: T7-T12); from T13 on they are read from each test's comment.
EXPECTED_FIXED = {
    "T1": ("rows", 0), "T2": ("rows", 0), "T3": ("rows", 4), "T4": ("rows", 0), "T5": ("rows", 13), "T6": ("rows", 0),
    "T7": ("rows", 0), "T8": ("value", "last_month", "202512"), "T9": ("value", "unmapped_zone_rows", "0"),
    "T10": ("rows", 2), "T11": ("rows", 0), "T12": ("rows", 0),
}
TEST_FILES = ["04_tests.sql", "05_noaa_storms.sql", "06_eia930_demand.sql"]


def describe(path: Path, label: str) -> str:
    """The test's comment: the line '-- Tn. ...' plus indented continuation lines, without '(expected ...)'."""
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(rf"\s*--\s*{label}\.\s*(.*)", line)
        if not m:
            continue
        text = m.group(1)
        for nxt in lines[i + 1:]:
            c = re.match(r"\s*--\s{2,}(\S.*)", nxt)
            if not c:
                break
            text += " " + c.group(1)
        text = re.split(r"\s*\(expected", text)[0]
        return re.sub(r"\s+", " ", text).strip().rstrip(".")
    return ""


def test_results(con):
    """Run every T-labelled SELECT in sql/04, 05, 06 and 09 onward (read-only) and return one row per test."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import run_local_duckdb_sources as runner  # helpers only: importing it runs nothing

    files = [ROOT / "sql" / f for f in TEST_FILES]
    files += sorted(p for p in (ROOT / "sql").glob("[0-9][0-9]_*.sql") if int(p.name[:2]) >= 9)
    out = []
    for path in files:
        from_comment = {k: runner.parse_expect(v) for k, v in runner.expected_from_comment(path).items()}
        for label, stmt in runner.labelled(path):
            if not label or not label.startswith("T") or not stmt.lstrip().upper().startswith(("SELECT", "WITH")):
                continue
            rule = EXPECTED_FIXED.get(label) or from_comment.get(label)
            df = con.execute(stmt).df()
            if rule[0] == "rows":
                expected, observed, ok = f"{rule[1]} rows", "", len(df) == rule[1]
            else:
                observed = str(df.iloc[0][rule[1]]) if len(df) == 1 else ""
                expected, ok = f"{rule[1]} = {rule[2]}", len(df) == 1 and observed == str(rule[2])
            out.append({"test": label, "test_no": int(label[1:]), "sql_file": path.name, "description": describe(path, label),
                        "expected": expected, "rows_returned": len(df), "observed_value": observed,
                        "status": "PASS" if ok else "FAIL"})
    out.sort(key=lambda r: r["test_no"])
    return out


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
    if not only or "test_results" in only:
        rows = test_results(con)
        p = OUT / "test_results.csv"
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)
        old["test_results.csv"] = {"file": "test_results.csv", "rows": len(rows), "bytes": p.stat().st_size, "sha256": sha256(p),
                                   "source": f"tests {rows[0]['test']}-{rows[-1]['test']} run on this DuckDB build (sql/04, 05, 06, 09 onward)",
                                   "exported_at": now}
        print(f"test_results.csv: {len(rows)} tests, {sum(r['status'] == 'PASS' for r in rows)} PASS")
    if not only or "storm_vs_calm" in only:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import storm_vs_calm_ratio as svc  # importing it runs nothing
        rows = svc.storm_vs_calm_table(con)
        p = OUT / "storm_vs_calm.csv"
        with p.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(svc.COLUMNS)
            w.writerows(rows)
        old["storm_vs_calm.csv"] = {"file": "storm_vs_calm.csv", "rows": len(rows), "bytes": p.stat().st_size, "sha256": sha256(p),
                                    "source": "scripts/storm_vs_calm_ratio.py on MART.FCT_COUNTY_DAY and FCT_TERRITORY_DAY: outage customer-hours "
                                              f"per 1,000 customers, storm vs calm county-days, 95% day-cluster bootstrap ({svc.B:,} resamples, seed {svc.SEED})",
                                    "exported_at": now}
        print(f"storm_vs_calm.csv: {len(rows)} rows; all county-days {rows[0][-1]}")
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "rows", "bytes", "sha256", "source", "exported_at"], lineterminator="\n")
        w.writeheader()
        for k in sorted(old):
            w.writerow(old[k])


if __name__ == "__main__":
    main()
