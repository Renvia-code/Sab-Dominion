"""List tables in the local DuckDB build (opened read-only)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import duckdb
DB = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\data\raw\duckdb\reliability_local.duckdb"
con = duckdb.connect(DB, read_only=True)
rows = con.execute("""
  select table_schema, table_name, table_type
  from information_schema.tables order by 1,2""").fetchall()
for s, t, ty in rows:
    try:
        n = con.execute(f'select count(*) from "{s}"."{t}"').fetchone()[0]
    except Exception as e:
        n = f"ERR {e}"[:60]
    cols = [c[0] for c in con.execute(f"select column_name from information_schema.columns where table_schema='{s}' and table_name='{t}' order by ordinal_position").fetchall()]
    print(f"{s}.{t} [{ty}] n={n} cols={cols[:25]}{'...' if len(cols)>25 else ''}")
