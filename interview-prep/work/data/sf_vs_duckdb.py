"""Compare the Snowflake build of sql/09-11 with the DuckDB mirror: row counts and key sums per new MART table.
Runs one read-only query on each engine. On 2026-11-01 the Snowflake side went through `snow sql -c dominion`
(RENV, ACCOUNTADMIN) because no Snowflake MCP tool was loaded in that session; the repo CLAUDE.md reserves that
connection for builds, so run this query through the MCP tool (role MCP_READER) next time instead of re-running
this script as is. Writes logs/sf_vs_duckdb_2026-11-01.md."""
import json
import subprocess
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "logs" / "sf_vs_duckdb_2026-11-01.md"

CHECKS = [
    ("DIM_COUNTY rows", "SELECT COUNT(*) FROM {m}.DIM_COUNTY"),
    ("DIM_COUNTY customers_basis (Dominion)", "SELECT SUM(customers_basis) FROM {m}.DIM_COUNTY WHERE dominion_county"),
    ("FCT_OUTAGE_COUNTY_HOUR rows", "SELECT COUNT(*) FROM {m}.FCT_OUTAGE_COUNTY_HOUR"),
    ("FCT_OUTAGE_COUNTY_HOUR customer_hours", "SELECT ROUND(SUM(customer_hours), 2) FROM {m}.FCT_OUTAGE_COUNTY_HOUR"),
    ("FCT_TERRITORY_15MIN rows", "SELECT COUNT(*) FROM {m}.FCT_TERRITORY_15MIN"),
    ("FCT_TERRITORY_15MIN customers_out", "SELECT SUM(customers_out) FROM {m}.FCT_TERRITORY_15MIN"),
    ("FCT_COUNTY_DAY rows", "SELECT COUNT(*) FROM {m}.FCT_COUNTY_DAY"),
    ("FCT_COUNTY_DAY customer_hours", "SELECT ROUND(SUM(customer_hours), 2) FROM {m}.FCT_COUNTY_DAY"),
    ("FCT_COUNTY_DAY storm days", "SELECT SUM(CASE WHEN storm_day THEN 1 ELSE 0 END) FROM {m}.FCT_COUNTY_DAY"),
    ("FCT_COUNTY_DAY complete county-days", "SELECT SUM(CASE WHEN failed_readings = 0 THEN 1 ELSE 0 END) FROM {m}.FCT_COUNTY_DAY"),
    ("FCT_TERRITORY_DAY proxy MED days", "SELECT SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) FROM {m}.FCT_TERRITORY_DAY"),
    ("FCT_OUTAGE_EVENT territory events", "SELECT COUNT(*) FROM {m}.FCT_OUTAGE_EVENT WHERE scope = 'territory'"),
    ("FCT_OUTAGE_EVENT county events", "SELECT COUNT(*) FROM {m}.FCT_OUTAGE_EVENT WHERE scope = 'county'"),
    ("FCT_OUTAGE_EVENT sum h90 (territory)", "SELECT ROUND(SUM(hours_to_90pct), 2) FROM {m}.FCT_OUTAGE_EVENT WHERE scope = 'territory'"),
    ("FCT_OUTAGE_EVENT sum peak held 1 h (territory)", "SELECT SUM(peak_sustained_1h) FROM {m}.FCT_OUTAGE_EVENT WHERE scope = 'territory'"),
    ("FCT_RESTORATION_CURVE rows", "SELECT COUNT(*) FROM {m}.FCT_RESTORATION_CURVE"),
    ("FCT_COUNTY_YEAR rows", "SELECT COUNT(*) FROM {m}.FCT_COUNTY_YEAR"),
    ("FCT_COUNTY_YEAR events_non_med", "SELECT SUM(events_non_med) FROM {m}.FCT_COUNTY_YEAR"),
    ("DOM_LOAD_HOUR_MONTH rows", "SELECT COUNT(*) FROM {m}.DOM_LOAD_HOUR_MONTH"),
    ("DOM_SEASONAL_PEAK sum peak_mw", "SELECT SUM(peak_mw) FROM {m}.DOM_SEASONAL_PEAK"),
    ("DOM_LOAD_DAILY rows", "SELECT COUNT(*) FROM {m}.DOM_LOAD_DAILY"),
    ("FCT_SALES_SECTOR sum sales_mwh", "SELECT SUM(sales_mwh) FROM {m}.FCT_SALES_SECTOR"),
    ("FCT_EVENT_CONTEXT rows", "SELECT COUNT(*) FROM {m}.FCT_EVENT_CONTEXT"),
    ("FCT_EVENT_CONTEXT with a tropical cyclone", "SELECT COUNT(tropical_cyclone) FROM {m}.FCT_EVENT_CONTEXT"),
    ("FCT_EVENT_CONTEXT DOE-417 reports matched", "SELECT SUM(doe417_reports) FROM {m}.FCT_EVENT_CONTEXT"),
]


def union(m):
    return "\nUNION ALL ".join(f"SELECT {i} AS k, CAST(({sql.format(m=m)}) AS VARCHAR) AS v" for i, (_, sql) in enumerate(CHECKS)) + "\nORDER BY k"


def norm(v):
    try:
        f = float(v)
        return f"{f:.2f}" if f != int(f) else str(int(f))
    except (TypeError, ValueError):
        return str(v)


con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)
duck = {int(k): norm(v) for k, v in con.execute(union("mart")).fetchall()}
res = subprocess.run(["snow", "sql", "-c", "dominion", "-q", union("RELIABILITY.MART"), "--format", "json"],
                     capture_output=True, text=True, encoding="utf-8", cwd=ROOT)
rows = json.loads(res.stdout)
sf = {int(r["K"]): norm(r["V"]) for r in rows}
md = ["# Snowflake vs DuckDB after the sql/09-11 run (2026-11-01)", "", "| Check | DuckDB | Snowflake | Same |", "|---|---:|---:|---|"]
same = 0
for i, (label, _) in enumerate(CHECKS):
    ok = duck.get(i) == sf.get(i)
    same += ok
    md.append(f"| {label} | {duck.get(i)} | {sf.get(i)} | {'yes' if ok else 'NO'} |")
md += ["", f"{same} of {len(CHECKS)} identical."]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
