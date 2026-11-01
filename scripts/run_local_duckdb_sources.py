"""Run the NOAA (05), EIA-930 (06, 07) and new-source SQL (09 onward) in a local DuckDB database.

Companion to scripts/run_local_duckdb.py, which covers 01 to 04 and tests T1 to T6 and is
left unchanged. This runner needs the raw downloads in data/raw/ (see data/raw/README.md and
the scripts/download_*.sh files). It rebuilds the reliability mart (01, 02) because 05 and 07
join to it, runs 05, 06 and 07 and asserts tests T7 to T12, then runs every sql/NN_*.sql file
from 09 onward and asserts the tests they declare (T13 onward).

Snowflake-only statements (warehouses, file formats, stages, COPY INTO, LIST, PUT) are skipped:
the raw tables are filled here from the local files instead. The database is written to
data/raw/duckdb/reliability_local.duckdb (gitignored) so analysis queries can reuse it.

Run with: python -I scripts/run_local_duckdb_sources.py [--skip-legacy] [--only 09,10]
"""
import argparse
import re
import sys
import time
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
SQL = ROOT / "sql"
INPUT = ROOT / "data" / "input"
REF = ROOT / "data" / "reference"
RAW = ROOT / "data" / "raw"
DB = RAW / "duckdb" / "reliability_local.duckdb"


def strip_comments(sql: str) -> str:
    """Remove -- comments (whole-line and trailing), leaving text inside single quotes alone."""
    out = []
    for line in sql.splitlines():
        in_str, cut = False, None
        for i, ch in enumerate(line):
            if ch == "'":
                in_str = not in_str
            elif not in_str and line.startswith("--", i):
                cut = i
                break
        out.append(line if cut is None else line[:cut])
    return "\n".join(out)


def translate(sql: str) -> str:
    """Snowflake dialect -> DuckDB, for the constructs used in this repository."""
    sql = strip_comments(sql)
    sql = re.sub(r"CREATE DATABASE.*?;|CREATE SCHEMA.*?;|USE WAREHOUSE.*?;|USE ROLE.*?;", "", sql, flags=re.S)
    sql = re.sub(r"CREATE OR REPLACE FILE FORMAT.*?;|CREATE FILE FORMAT.*?;", "", sql, flags=re.S)
    sql = re.sub(r"CREATE (OR REPLACE )?STAGE.*?;", "", sql, flags=re.S)
    sql = re.sub(r"COPY INTO.*?;|LIST @.*?;|PUT file.*?;|ALTER WAREHOUSE.*?;", "", sql, flags=re.S)
    sql = sql.replace(" COPY GRANTS AS", " AS").replace(" COPY GRANTS", "")
    sql = sql.replace("RELIABILITY.RAW.", "raw.").replace("RELIABILITY.STG.", "stg.").replace("RELIABILITY.MART.", "mart.")
    # Date and timestamp parsing with a format
    fmt = {"'MM/DD/YYYY'": "'%m/%d/%Y'", "'MM/DD/YYYY HH12:MI:SS AM'": "'%m/%d/%Y %I:%M:%S %p'",
           "'YYYYMMDD HH24MI'": "'%Y%m%d %H%M'"}
    def _date(m):
        return f"CAST(TRY_STRPTIME({m.group(1)}, {fmt[m.group(2)]}) AS DATE)"
    def _ts(m):
        return f"TRY_STRPTIME({m.group(1)}, {fmt[m.group(2)]})"
    sql = re.sub(r"TRY_TO_DATE\(([^(),]+),\s*('MM/DD/YYYY')\)", _date, sql)
    sql = re.sub(r"TRY_TO_TIMESTAMP_NTZ\(([^(),]+),\s*('MM/DD/YYYY HH12:MI:SS AM'|'YYYYMMDD HH24MI')\)", _ts, sql)
    # REGEXP_LIKE matches the whole string in Snowflake, as regexp_full_match does in DuckDB
    sql = sql.replace("REGEXP_LIKE(", "regexp_full_match(")
    sql = sql.replace("DAYOFWEEKISO(", "isodow(")  # 1 = Monday ... 7 = Sunday in both
    # LISTAGG(x, 'sep') WITHIN GROUP (ORDER BY y) -> listagg(x, 'sep' ORDER BY y)
    sql = re.sub(r"LISTAGG\(([^(),]+),\s*('[^']*')\)\s*WITHIN GROUP\s*\(ORDER BY ([^()]+)\)", r"listagg(\1, \2 ORDER BY \3)", sql)
    # TRY_TO_NUMBER(x, p, s) -> TRY_CAST(x AS DECIMAL(p,s)); TRY_TO_NUMBER(x) -> TRY_CAST(x AS BIGINT)
    sql = re.sub(r"TRY_TO_NUMBER\(([^()]*(?:\([^()]*\))?[^()]*),\s*(\d+),\s*(\d+)\)", r"TRY_CAST(\1 AS DECIMAL(\2,\3))", sql)
    sql = re.sub(r"TRY_TO_NUMBER\(([^()]*(?:\([^()]*\))?[^()]*)\)", r"TRY_CAST(\1 AS BIGINT)", sql)
    sql = re.sub(r"TRY_TO_DATE\(([^()]*)\)", r"TRY_CAST(\1 AS DATE)", sql)
    sql = re.sub(r"TRY_TO_BOOLEAN\(([^()]*)\)", r"TRY_CAST(\1 AS BOOLEAN)", sql)
    sql = sql.replace("NULL::VARCHAR", "CAST(NULL AS VARCHAR)").replace("NULL::BOOLEAN", "CAST(NULL AS BOOLEAN)")
    sql = sql.replace("TIMESTAMP_NTZ", "TIMESTAMP")
    # TIME_SLICE(x, n, 'MINUTE') -> time_bucket(INTERVAL 'n minutes', x); DATE_FROM_PARTS -> make_date
    sql = re.sub(r"TIME_SLICE\(((?:[^()]|\([^()]*\))*?),\s*(\d+),\s*'MINUTE'\)", r"time_bucket(INTERVAL '\2 minutes', \1)", sql)
    sql = sql.replace("DATE_FROM_PARTS(", "make_date(")
    return sql


# ---- raw loaders for the sources added from sql/09 on: Snowflake fills these with COPY INTO
def _csv(path):
    return path.as_posix()


def load_eaglei_outages(con):
    for f in sorted((RAW / "eaglei" / "va").glob("eaglei_outages_va_*.csv")):
        cols = [r[0] for r in con.execute(f"DESCRIBE SELECT * FROM read_csv('{_csv(f)}', header=true, all_varchar=true)").fetchall()]
        sel = ", ".join([f'"{c}"' for c in cols[:5]] + ([f'"{cols[5]}"'] if len(cols) > 5 else ["NULL"]))
        con.execute(f"INSERT INTO raw.EAGLEI_OUTAGES_VA SELECT {sel}, '{f.name}' FROM read_csv('{_csv(f)}', header=true, all_varchar=true, nullstr=[''])")


def _positional(con, table, path):
    con.execute(f"INSERT INTO raw.{table} SELECT * FROM read_csv('{_csv(path)}', header=true, all_varchar=true, nullstr=[''])")


LOADERS = {
    "EAGLEI_OUTAGES_VA": load_eaglei_outages,
    "EAGLEI_MCC": lambda con: _positional(con, "EAGLEI_MCC", RAW / "eaglei" / "MCC.csv"),
    "EAGLEI_COVERAGE_HISTORY": lambda con: _positional(con, "EAGLEI_COVERAGE_HISTORY", RAW / "eaglei" / "coverage_history.csv"),
    "CENSUS_VA_COUNTY": lambda con: _positional(con, "CENSUS_VA_COUNTY", RAW / "census" / "va_county_census.csv"),
    "HURDAT2_POINTS": lambda con: _positional(con, "HURDAT2_POINTS", RAW / "hurdat2" / "hurdat2_points.csv"),
    "DOE417_EVENTS": lambda con: _positional(con, "DOE417_EVENTS", RAW / "doe417" / "doe417_events_2014_2025.csv"),
    "CPC_DEGREE_DAYS": lambda con: _positional(con, "CPC_DEGREE_DAYS", RAW / "degree_days" / "cpc_degree_days_long.csv"),
}


def statements(sql: str):
    """Split translated SQL on semicolons; keep the test or query label written above each one."""
    out = []
    for block in sql.split(";"):
        stmt = block.strip()
        if stmt:
            out.append(stmt)
    return out


def labelled(path: Path):
    """Yield (label, statement) for a SQL file. The label is the T<n> or Q<n> named in the
    comment directly above the statement, else None."""
    text = path.read_text(encoding="utf-8")
    # Split on semicolons in code only: comments may contain semicolons.
    blocks, cur = [], []
    for line in text.splitlines():
        cur.append(line)
        if ";" in strip_comments(line):
            blocks.append("\n".join(cur))
            cur = []
    if cur:
        blocks.append("\n".join(cur))
    for raw in blocks:
        m = re.findall(r"(?m)^\s*--\s*(T\d+|Q\d+[a-z]?)\b", raw)
        label = m[-1] if m else None
        stmt = translate(raw + ";").strip().rstrip(";").strip()
        copy = re.search(r"(?m)^\s*COPY INTO RELIABILITY\.RAW\.(\w+)", strip_comments(raw))
        if copy:
            yield "LOAD", copy.group(1)
        elif stmt:
            yield label, stmt


def expected_from_comment(path: Path):
    """Read 'expected N rows' / 'expected value V' markers written as
    '-- T13. ... (expected 0 rows)' or '(expected 1 row: 202512)'."""
    exp = {}
    lines = path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"\s*--\s*(T\d+)\.", line)
        if not m:
            continue
        text = line
        j = i + 1
        while j < len(lines) and lines[j].lstrip().startswith("--"):  # comment continues
            text += " " + lines[j].lstrip("- ")
            j += 1
        e = re.search(r"\(expected ([^)]*)\)", text)
        if e:
            exp[m.group(1)] = e.group(1)
    return exp


def load_reliability(con):
    sql01 = translate((SQL / "01_raw_staging.sql").read_text(encoding="utf-8"))
    for s in statements(sql01):
        if s.upper().startswith("CREATE OR REPLACE TABLE"):
            con.execute(s)
    con.execute(f"INSERT INTO raw.EIA861_RELIABILITY_2025 SELECT * FROM read_csv('{(INPUT / 'Reliability_2025_States.csv').as_posix()}', skip=3, header=false, all_varchar=true, nullstr=['.',''])")
    for tbl, f in [("PUDL_RELIABILITY", "pudl_reliability_2013_2024.csv"), ("PUDL_AMI", "pudl_ami.csv"), ("PUDL_SALES", "pudl_sales.csv")]:
        con.execute(f"INSERT INTO raw.{tbl} SELECT * FROM read_csv('{(INPUT / f).as_posix()}', header=true, all_varchar=true, nullstr=['','<NA>','NULL'])")
    for s in statements(sql01):
        if s.upper().startswith("CREATE OR REPLACE VIEW"):
            con.execute(s)
    for s in statements(translate((SQL / "02_mart.sql").read_text(encoding="utf-8"))):
        con.execute(s)
    n = con.execute("SELECT COUNT(*) FROM mart.FCT_RELIABILITY").fetchone()[0]
    print(f"01-02 reliability mart rebuilt: FCT_RELIABILITY {n:,} rows (expected 13,095)")
    if n != 13095:
        raise RuntimeError("FCT_RELIABILITY row count changed")


def load_noaa_and_eia930(con):
    noaa = sorted((RAW / "noaa").glob("StormEvents_details-ftp_v1.0_d20*_c*.csv.gz"))
    eia = sorted((RAW / "eia930").glob("EIA930_SUBREGION_20*_*.csv"))
    if len(noaa) != 13 or len(eia) < 17:
        raise RuntimeError(f"raw files missing: {len(noaa)} NOAA (need 13), {len(eia)} EIA-930 (need 17)")
    files = "[" + ",".join(f"'{p.as_posix()}'" for p in noaa) + "]"
    con.execute(f"INSERT INTO raw.NOAA_STORM_EVENTS SELECT * FROM read_csv({files}, header=true, all_varchar=true, nullstr=[''], quote='\"', escape='\"', max_line_size=10000000)")
    con.execute(f"INSERT INTO raw.NOAA_ZONE_COUNTY SELECT * FROM read_csv('{(REF / 'zone_county_correlation.csv').as_posix()}', header=true, all_varchar=true, nullstr=[''])")
    con.execute(f"INSERT INTO raw.EIA861_SERVICE_TERRITORY_2025 SELECT * FROM read_csv('{(REF / 'Service_Territory_2025_Counties_States.csv').as_posix()}', header=true, all_varchar=true, nullstr=[''])")
    files = "[" + ",".join(f"'{p.as_posix()}'" for p in eia) + "]"
    con.execute(f"INSERT INTO raw.EIA930_SUBREGION SELECT * FROM read_csv({files}, header=true, all_varchar=true, nullstr=[''])")
    counts = {t: con.execute(f"SELECT COUNT(*) FROM raw.{t}").fetchone()[0]
              for t in ["NOAA_STORM_EVENTS", "NOAA_ZONE_COUNTY", "EIA861_SERVICE_TERRITORY_2025", "EIA930_SUBREGION"]}
    print("raw rows:", {k: f"{v:,}" for k, v in counts.items()},
          "(expected 831,288 / 7,087 / 11,803 / 6,094,320 with the 2026 H2 file to 30 Oct 2026)")
    if counts["NOAA_STORM_EVENTS"] != 831288 or counts["NOAA_ZONE_COUNTY"] != 7087 or counts["EIA861_SERVICE_TERRITORY_2025"] != 11803:
        raise RuntimeError("raw row counts differ from docs/01_sources.md")


def run_file(con, path: Path, test_expect: dict, results: dict, quiet_queries=False):
    """Execute a SQL file. Raw CREATE TABLE statements for tables that the runner loads
    itself are skipped when the table already holds rows."""
    print(f"\n==== {path.name} ====")
    for label, stmt in labelled(path):
        if label == "LOAD":
            if stmt in LOADERS:
                t0 = time.time()
                LOADERS[stmt](con)
                n = con.execute(f"SELECT COUNT(*) FROM raw.{stmt}").fetchone()[0]
                print(f"loaded raw.{stmt}: {n:,} rows  [{time.time()-t0:.1f}s]")
            continue
        head = stmt.lstrip().upper()
        if head.startswith("CREATE OR REPLACE TABLE RAW.") or head.startswith("CREATE TABLE IF NOT EXISTS RAW."):
            name = re.match(r"CREATE (?:OR REPLACE )?TABLE (?:IF NOT EXISTS )?(raw\.\w+)", stmt, flags=re.I).group(1)
            if name.split(".")[1].upper() in LOADERS:
                con.execute(stmt)  # new-source raw table: recreate empty, the LOAD step refills it
                continue
            exists = con.execute(
                "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='raw' AND lower(table_name)=lower(?)",
                [name.split(".")[1]]).fetchone()[0]
            if exists:
                continue
        t0 = time.time()
        try:
            res = con.execute(stmt)
        except Exception as exc:
            print(f"FAILED in {path.name} ({label}): {exc}\n{stmt[:800]}", file=sys.stderr)
            raise
        if head.startswith(("SELECT", "WITH")):
            df = res.df()
            if label and label.startswith("T"):
                results[label] = df
                exp = test_expect.get(label)
                print(f"{label}: {len(df)} rows (expected {exp})  [{time.time()-t0:.1f}s]")
                if len(df) and len(df) <= 12:
                    print(df.to_string(index=False))
            elif not quiet_queries:
                print(f"\n{label or 'query'}  [{time.time()-t0:.1f}s]")
                print(df.head(40).to_string(index=False))


def check_tests(results: dict, expected: dict):
    """expected: label -> ('rows', n) or ('value', column, value)."""
    bad = {}
    for label, rule in expected.items():
        if label not in results:
            bad[label] = "missing"
            continue
        df = results[label]
        if rule[0] == "rows":
            ok = len(df) == rule[1]
        else:
            ok = len(df) == 1 and str(df.iloc[0][rule[1]]) == str(rule[2])
        print(f"{label}: {'PASS' if ok else 'FAIL'} ({rule})")
        if not ok:
            bad[label] = rule
    return bad


def parse_expect(text: str):
    """'0 rows' -> ('rows', 0); '1 row: 202512' -> ('value_first', '202512'); '2 rows ...' -> ('rows', 2);
    'value 0 in <col>' -> ('value', col, 0)."""
    m = re.search(r"value (\S+) in (\w+)", text)
    if m:
        return ("value", m.group(2), m.group(1))
    m = re.match(r"\s*(\d+) rows?", text)
    if m:
        return ("rows", int(m.group(1)))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-legacy", action="store_true", help="reuse the existing database; run only 09 onward")
    ap.add_argument("--only", default="", help="comma list of file numbers from 09 onward to run, e.g. 09,10")
    ap.add_argument("--quiet", action="store_true", help="print tests only, not analysis queries")
    args = ap.parse_args()
    DB.parent.mkdir(parents=True, exist_ok=True)
    results, expected = {}, {}

    if not args.skip_legacy:
        if DB.exists():
            DB.unlink()
        con = duckdb.connect(str(DB))
        con.execute("SET preserve_insertion_order=false")
        con.execute("CREATE SCHEMA raw; CREATE SCHEMA stg; CREATE SCHEMA mart;")
        load_reliability(con)
        # Create the raw tables of 05 and 06 from their own DDL, then fill them from local files.
        for f in ("05_noaa_storms.sql", "06_eia930_demand.sql"):
            for label, stmt in labelled(SQL / f):
                if stmt.upper().startswith("CREATE OR REPLACE TABLE RAW."):
                    con.execute(stmt)
        load_noaa_and_eia930(con)
        for f in ("05_noaa_storms.sql", "06_eia930_demand.sql", "07_weather_adjusted_and_profile.sql"):
            run_file(con, SQL / f, {}, results, quiet_queries=args.quiet)
        expected.update({"T7": ("rows", 0), "T8": ("value", "last_month", "202512"), "T9": ("value", "unmapped_zone_rows", "0"),
                         "T10": ("rows", 2), "T11": ("rows", 0), "T12": ("rows", 0)})
    else:
        con = duckdb.connect(str(DB))

    only = {s.strip() for s in args.only.split(",") if s.strip()}
    new_files = sorted(p for p in SQL.glob("[0-9][0-9]_*.sql") if int(p.name[:2]) >= 9 and p.name[:2] != "08")
    for path in new_files:
        if only and path.name[:2] not in only:
            continue
        exp = {k: parse_expect(v) for k, v in expected_from_comment(path).items()}
        run_file(con, path, exp, results, quiet_queries=args.quiet)
        expected.update({k: v for k, v in exp.items() if v})

    print("\n==== TESTS ====")
    bad = check_tests(results, expected)
    con.close()
    if bad:
        raise SystemExit(f"Tests failed: {bad}")
    print(f"All {len(expected)} tests passed. Database: {DB.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
