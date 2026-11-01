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
