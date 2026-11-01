"""Save the EIA-861 and EIA-861M sheets the new SQL reads as CSV, and write both manifests.

Downloads (scripts/download_eia861.sh) sit in data/raw/eia861/ (annual zips f861YYYY.zip) and
data/raw/eia861m/ (monthly utility-level workbooks, one per year). Snowflake and DuckDB both load
CSV, so this script writes:

  data/raw/eia861/csv/<Workbook>_<Sheet>.csv   the named sheets, every row as published
                                               (header rows included, as Reliability_2025_States.csv)
  data/raw/eia861m/csv/sales_ult_cust_monthly.csv
                                               every utility-state-month row of the yearly 861M
                                               workbooks, one row per sector (long form)

Values are written as they appear in the workbook (whole numbers without a decimal point).
Run with: python -I scripts/extract_eia861.py
"""
import csv
import datetime as dt
import hashlib
import io
import zipfile
from pathlib import Path

import openpyxl
import xlrd

ROOT = Path(__file__).resolve().parent.parent
A = ROOT / "data" / "raw" / "eia861"
M = ROOT / "data" / "raw" / "eia861m"
URL_A = "https://www.eia.gov/electricity/data/eia861/zip/{}"
URL_M = "https://www.eia.gov/electricity/data/eia861m/{}"
SHEETS = {  # workbook stem -> sheet
    "Sales_Ult_Cust": "States",
    "Dynamic_Pricing": "Dynamic Pricing_States",
    "Advanced_Meters": "states",
    "Distribution_Systems": "Distribution_Systems_States",
}
SECTORS = ["residential", "commercial", "industrial", "transportation", "total"]


def cell(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def digest(path: Path):
    s = hashlib.sha256(path.read_bytes()).hexdigest()
    return s


def when(path: Path):
    return dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def xlsx_rows(data: bytes, sheet: str):
    wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
    for row in wb[sheet].iter_rows(values_only=True):
        yield [cell(v) for v in row]


def xls_rows(path: Path, sheet_index=0):
    book = xlrd.open_workbook(str(path))
    sh = book.sheet_by_index(sheet_index)
    for r in range(sh.nrows):
        yield [cell(v) if not isinstance(v, str) else v for v in sh.row_values(r)]


def annual():
    out = A / "csv"
    out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for z in sorted(A.glob("f861*.zip")):
        year = z.stem[-4:]
        manifest.append({"file": z.name, "rows": "", "bytes": z.stat().st_size, "sha256": digest(z),
                         "url": URL_A.format(z.name), "downloaded_at": when(z), "note": f"EIA-861 {year} annual files (zip as published)"})
        with zipfile.ZipFile(z) as zz:
            for stem, sheet in SHEETS.items():
                name = f"{stem}_{year}.xlsx"
                if name not in zz.namelist():
                    continue
                rows = list(xlsx_rows(zz.read(name), sheet))
                target = out / f"{stem}_{year}_{sheet.replace(' ', '_')}.csv"
                with target.open("w", newline="", encoding="utf-8") as f:
                    csv.writer(f).writerows(rows)
                manifest.append({"file": f"csv/{target.name}", "rows": len(rows), "bytes": target.stat().st_size,
                                 "sha256": digest(target), "url": URL_A.format(z.name), "downloaded_at": when(z),
                                 "note": f"sheet '{sheet}' of {name}, all rows including the header rows"})
    write_manifest(A / "MANIFEST.csv", manifest)
    return manifest


def monthly():
    out = M / "csv"
    out.mkdir(parents=True, exist_ok=True)
    long_rows, manifest = [], []
    files = sorted(M.glob("f826*.xls")) + sorted(M.glob("retail_sales_*.xlsx")) + sorted(M.glob("sales_ult_cust_*.xlsx"))
    for p in files:
        is_zip = p.read_bytes()[:2] == b"PK"  # some '.xls' files are xlsx inside
        if p.suffix == ".xls" and not is_zip:
            rows = list(xls_rows(p))
            sub = "archive/xls/" + p.name
        else:
            wb = openpyxl.load_workbook(io.BytesIO(p.read_bytes()), read_only=True, data_only=True)
            rows = [[cell(v) for v in r] for r in wb[wb.sheetnames[0]].iter_rows(values_only=True)]
            sub = ("xls/" if p.name.endswith("2026.xlsx") else "archive/xls/") + p.name
        header = [h.strip().lower() for h in rows[2]]
        has_owner = "ownership" in header
        first = 7 if has_owner else 6  # first sector column
        n = 0
        for r in rows[3:]:
            if not r or not r[0] or not str(r[0]).strip().isdigit():
                continue  # footnotes
            ident = {"year": r[0], "month": r[1], "utility_number": r[2], "utility_name": r[3], "state": r[4],
                     "ownership": r[5] if has_owner else "", "data_status": r[first - 1]}
            for i, sector in enumerate(SECTORS):
                c = first + 3 * i
                long_rows.append({**ident, "sector": sector, "revenue_thousand_usd": r[c], "sales_mwh": r[c + 1],
                                  "customers": r[c + 2], "source_file": p.name})
            n += 1
        manifest.append({"file": p.name, "rows": n, "bytes": p.stat().st_size, "sha256": digest(p),
                         "url": URL_M.format(sub), "downloaded_at": when(p),
                         "note": f"EIA-861M utility-level monthly sales, sheet '{'Retail Sales - States' if p.suffix == '.xls' else 'Sales Ultimate Cust. -States'}'; rows = utility-state-months"})
    target = out / "sales_ult_cust_monthly.csv"
    cols = ["year", "month", "utility_number", "utility_name", "state", "ownership", "data_status", "sector",
            "revenue_thousand_usd", "sales_mwh", "customers", "source_file"]
    with target.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(long_rows)
    manifest.append({"file": f"csv/{target.name}", "rows": len(long_rows), "bytes": target.stat().st_size,
                     "sha256": digest(target), "url": "", "downloaded_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "note": f"long form of the {len(files)} workbooks above: one row per utility-state-month-sector"})
    write_manifest(M / "MANIFEST.csv", manifest)
    return manifest


def write_manifest(path: Path, rows):
    cols = ["file", "rows", "bytes", "sha256", "url", "downloaded_at", "note"]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    for m in annual() + monthly():
        print(f"{m['file']}: {m['rows']} rows, {m['bytes']:,} bytes")
