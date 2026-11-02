"""Assemble interview-prep/work/data/findings.md from the generated section files.

Each analysis script writes one file in sections/ (with the exact query behind every number);
this script puts them in a fixed order under one header. Re-run after any section changes.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = ["c6_r_numbers.md", "c5_g2_numbers.md", "s2_base_year.md", "b0_bedford.md", "d22_recheck.md", "c3_quick_checks.md", "a1_county_day.md", "a2_events.md", "a3_county_map.md",
         "a4_load.md", "e1_eia930_cutoff.md", "a5_reconciliation.md", "a6_optional.md"]
HEADER = """# Findings (Agent D)

Each section: one-paragraph finding, the chart-ready table (file in `data/output/`), caveats, and
the exact query. Queries run against the DuckDB mirror built from the source files
(`scripts/run_local_duckdb_sources.py`); in Snowflake read `mart.` as `RELIABILITY.MART.` and
`stg.` as `RELIABILITY.STG.`. Public data only: nothing here is Dominion internal data.
"""


def main():
    parts = [HEADER]
    for name in ORDER:
        p = HERE / "sections" / name
        if p.exists():
            parts.append(p.read_text(encoding="utf-8").strip() + "\n")
    out = HERE / "findings.md"
    out.write_text("\n".join(parts), encoding="utf-8")
    print(out, "sections:", sum(1 for n in ORDER if (HERE / "sections" / n).exists()))


if __name__ == "__main__":
    main()
