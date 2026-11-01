"""Write the two workbook sheets the Power BI template imports, LoadGrowth and Programmes2025, as CSV files in
data/output/ (load_growth.csv, programmes_2025.csv), so the template reads every table from one folder.

Source: powerbi/Dominion_Reliability_PowerBI_Data.xlsx, the Excel tables of the same names. The workbook stays the
source; the CSV files are generated from it and never edited by hand. LoadGrowth's three index columns are Excel
formulas (the value over its 2013 value, x 100): the values Excel saved are written, after each is checked against
the same formula recomputed here, so a stale workbook stops the export. Column names are the sheet's headers, the
names the template's tables already use. Updates data/output/powerbi_exports_manifest.csv.

Run: .venv/Scripts/python.exe -I scripts/export_workbook_tables.py   (needs openpyxl, in requirements-sources.txt)
"""
import csv
import datetime as dt
import hashlib
import math
import re
from pathlib import Path

import openpyxl
from openpyxl.utils import range_boundaries

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK = ROOT / "powerbi" / "Dominion_Reliability_PowerBI_Data.xlsx"
OUT = ROOT / "data" / "output"
MANIFEST = OUT / "powerbi_exports_manifest.csv"
TABLES = [("LoadGrowth", "load_growth.csv"), ("Programmes2025", "programmes_2025.csv")]  # (Excel and model table, file)
INDEX_FORMULA = re.compile(r"^=([A-Z]+)(\d+)/\$([A-Z]+)\$(\d+)\*100$")              # e.g. =B3/$B$2*100


def table_rows(ws_values, ws_formulas, name):
    """Header and data rows of the Excel table `name`, formula cells checked against their recomputed value."""
    min_col, min_row, max_col, max_row = range_boundaries(ws_values.tables[name].ref)
    rows = []
    for r in range(min_row, max_row + 1):
        row = []
        for c in range(min_col, max_col + 1):
            value, formula = ws_values.cell(r, c).value, ws_formulas.cell(r, c).value
            if isinstance(formula, str) and formula.startswith("="):
                m = INDEX_FORMULA.match(formula)
                if not m:
                    raise ValueError(f"{name}!{ws_values.cell(r, c).coordinate}: unexpected formula {formula}")
                num = ws_values[f"{m.group(1)}{m.group(2)}"].value
                base = ws_values[f"{m.group(3)}{m.group(4)}"].value
                expected = num / base * 100
                if value is None or not math.isclose(value, expected, rel_tol=1e-12):
                    raise ValueError(f"{name}!{ws_values.cell(r, c).coordinate}: saved value {value} != {formula} = {expected}")
            row.append(value)
        rows.append(row)
    return rows


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    values = openpyxl.load_workbook(WORKBOOK, data_only=True)    # the values Excel saved
    formulas = openpyxl.load_workbook(WORKBOOK, data_only=False)  # the formulas behind them
    with MANIFEST.open(newline="", encoding="utf-8") as f:
        manifest = {r["file"]: r for r in csv.DictReader(f)}
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for name, file in TABLES:
        rows = table_rows(values[name], formulas[name], name)
        p = OUT / file
        with p.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f, lineterminator="\n").writerows(rows)  # None is written as an empty field
        manifest[file] = {"file": file, "rows": len(rows) - 1, "bytes": p.stat().st_size, "sha256": sha256(p),
                          "source": f"powerbi/{WORKBOOK.name}, Excel table {name} (scripts/export_workbook_tables.py)",
                          "exported_at": now}
        print(f"{file}: {len(rows) - 1} rows, columns {', '.join(rows[0])}")
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "rows", "bytes", "sha256", "source", "exported_at"], lineterminator="\n")
        w.writeheader()
        for k in sorted(manifest):
            w.writerow(manifest[k])


if __name__ == "__main__":
    main()
