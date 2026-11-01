"""Turn the DOE-417 annual summaries (data/raw/doe417/{YYYY}_Annual_Summary.xls|xlsx, PNNL host)
into one long CSV: data/raw/doe417/doe417_events_2014_2025.csv. The workbooks are left unchanged.

The layouts differ by year (2014: 9 columns, month section rows; 2015-2023: 11 columns with NERC
Region; 2024-2025: 10 columns, 4 title rows). Header names are mapped to one set of columns. Title,
month and footnote rows are skipped. An event row is any row after the header with an Area Affected (the 2023 file
has 32 August rows whose begin date is blank as published; they are kept with an empty
date_began). Dates and times are normalised (ISO date, 24-hour HH:MM) and the original cell
text is kept beside each. Demand loss and customers stay as published text ("Unknown", "1,300");
the SQL casts them. There is no utility column in any year.

Run: .venv/Scripts/python.exe -I scripts/extract_doe417.py
"""
import csv
import datetime as dt
import re
import warnings
from pathlib import Path

import openpyxl
import xlrd

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "raw" / "doe417"
OUT = D / "doe417_events_2014_2025.csv"

HEADER_MAP = {
    "month": "event_month", "event month": "event_month",
    "date event began": "date_began", "date began": "date_began",
    "time event began": "time_began", "time began": "time_began",
    "date of restoration": "date_restored", "date restored": "date_restored",
    "time of restoration": "time_restored", "time restored": "time_restored",
    "area affected": "area_affected", "nerc region": "nerc_region",
    "alert criteria": "alert_criteria", "event type": "event_type",
    "demand loss (mw)": "demand_loss_mw",
    "number of customers affected": "customers_affected", "customers affected": "customers_affected",
}
COLS = ["year", "source_file", "source_row", "event_month", "date_began", "time_began", "date_restored",
        "time_restored", "area_affected", "nerc_region", "alert_criteria", "event_type", "demand_loss_mw",
        "customers_affected", "date_began_raw", "time_began_raw", "date_restored_raw", "time_restored_raw"]
DATE_RE = re.compile(r"^\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$")


def as_text(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def parse_date(v, datemode):
    if isinstance(v, (int, float)) and not isinstance(v, bool) and 20000 < v < 60000:
        return xlrd.xldate_as_datetime(v, datemode).date().isoformat()
    if isinstance(v, dt.datetime):
        return v.date().isoformat()
    m = DATE_RE.match(as_text(v))
    if m:
        mo, da, yr = map(int, m.groups())
        try:
            return dt.date(yr, mo, da).isoformat()
        except ValueError:
            return ""
    return ""


def parse_time(v):
    if isinstance(v, (int, float)) and not isinstance(v, bool) and 0 <= v < 1:
        minutes = int(round(v * 24 * 60)) % (24 * 60)
        return f"{minutes // 60:02d}:{minutes % 60:02d}"
    if isinstance(v, dt.time):
        return f"{v.hour:02d}:{v.minute:02d}"
    s = as_text(v).lower().replace(".", "").replace(" ", "")
    for fmt in ("%I:%M%p", "%H:%M", "%I:%M:%S%p", "%H:%M:%S"):
        try:
            t = dt.datetime.strptime(s, fmt)
            return f"{t.hour:02d}:{t.minute:02d}"
        except ValueError:
            pass
    return ""


def rows_of(path: Path):
    """Yield (row_number_1_based, list_of_values, datemode)."""
    if path.suffix.lower() == ".xls":
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            with open(Path("nul") if Path("nul").exists() else "/dev/null", "w") as log:
                wb = xlrd.open_workbook(str(path), logfile=log)
        sh = wb.sheet_by_index(0)
        for r in range(sh.nrows):
            yield r + 1, sh.row_values(r), wb.datemode
    else:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        for i, r in enumerate(ws.iter_rows(values_only=True), start=1):
            yield i, list(r), 0


def main():
    out, per_year = [], {}
    for path in sorted(D.glob("*_Annual_Summary.xls*")):
        year = int(path.name[:4])
        header = None
        n = 0
        for rn, vals, datemode in rows_of(path):
            texts = [as_text(v).lower() for v in vals]
            if header is None:
                if "area affected" in texts:
                    header = {i: HEADER_MAP[t] for i, t in enumerate(texts) if t in HEADER_MAP}
                continue
            rec = {header[i]: vals[i] for i in header if i < len(vals)}
            if not as_text(rec.get("area_affected")):
                continue  # month section, footnote or end-of-report row
            d_began = parse_date(rec.get("date_began"), datemode)  # blank for 32 August rows of 2023 as published
            row = {"year": year, "source_file": path.name, "source_row": rn,
                   "date_began": d_began, "time_began": parse_time(rec.get("time_began")),
                   "date_restored": parse_date(rec.get("date_restored"), datemode),
                   "time_restored": parse_time(rec.get("time_restored")),
                   "date_began_raw": as_text(rec.get("date_began")), "time_began_raw": as_text(rec.get("time_began")),
                   "date_restored_raw": as_text(rec.get("date_restored")), "time_restored_raw": as_text(rec.get("time_restored"))}
            for k in ("event_month", "area_affected", "nerc_region", "alert_criteria", "event_type",
                      "demand_loss_mw", "customers_affected"):
                row[k] = as_text(rec.get(k))
            out.append(row)
            n += 1
        per_year[year] = n
        if header is None:
            raise SystemExit(f"no header row found in {path.name}")
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    for y, n in per_year.items():
        print(y, n)
    print(OUT.relative_to(ROOT).as_posix(), len(out), "events")


if __name__ == "__main__":
    main()
