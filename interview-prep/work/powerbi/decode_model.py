"""Read-only inventory of the data model inside a .pbix (tables, columns, measures, relationships,
Power Query M), using pbixray. Writes markdown; never modifies the .pbix.

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\powerbi\\decode_model.py <file.pbix> <out.md>
"""
import sys
from pathlib import Path

import pandas as pd
from pbixray import PBIXRay


def md_table(df: pd.DataFrame, cols=None, maxw=160) -> str:
    if df is None or len(df) == 0:
        return "(none)\n"
    if cols:
        df = df[[c for c in cols if c in df.columns]]
    out = ["| " + " | ".join(map(str, df.columns)) + " |", "|" + "---|" * len(df.columns)]
    for _, r in df.iterrows():
        cells = []
        for v in r.values:
            s = str(v).replace("\n", " ").replace("|", "\\|")
            cells.append(s if len(s) <= maxw else s[:maxw] + "…")
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out) + "\n"


def main(pbix, out_md):
    m = PBIXRay(pbix)
    parts = [f"# Data model inventory: `{Path(pbix).name}` (read-only, pbixray)", ""]
    parts += ["## Tables", "", ", ".join(map(str, m.tables)), "", f"Count: {len(m.tables)}", ""]
    try:
        stats = m.statistics
        parts += ["## Table statistics", "", md_table(stats), ""]
    except Exception as e:  # noqa: BLE001
        parts += [f"(statistics unavailable: {e})", ""]
    parts += ["## Relationships", "", md_table(m.relationships), ""]
    dax = m.dax_measures
    parts += [f"## Measures ({len(dax)})", "", md_table(dax, maxw=400), ""]
    try:
        cc = m.dax_columns
        parts += [f"## Calculated columns ({len(cc)})", "", md_table(cc, maxw=300), ""]
    except Exception as e:  # noqa: BLE001
        parts += [f"(calculated columns unavailable: {e})", ""]
    pq = m.power_query
    parts += [f"## Power Query M ({len(pq)})", ""]
    for _, r in pq.iterrows():
        parts += [f"### {r.get('TableName')}", "", "```powerquery", str(r.get('Expression')), "```", ""]
    try:
        sch = m.schema
        parts += ["## Columns (schema)", "", md_table(sch, maxw=80), ""]
    except Exception as e:  # noqa: BLE001
        parts += [f"(schema unavailable: {e})", ""]
    Path(out_md).write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out_md}: {len(m.tables)} tables, {len(dax)} measures, {len(pq)} M queries, "
          f"{len(m.relationships)} relationships")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
