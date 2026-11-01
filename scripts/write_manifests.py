"""Write MANIFEST.csv (file, rows, bytes, sha256, url, downloaded_at, note) for the smaller
source folders under data/raw/: census, hurdat2, degree_days, oe417, doe417, pjm, scc_reliability.
EAGLE-I and EIA-861/861M manifests are written by their own extract scripts.
Rows: data lines for text files (header excluded), blank for binary files.
Run with: python -I scripts/write_manifests.py
"""
import csv
import datetime as dt
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
URLS = {
    "census": {
        "cb_2024_us_county_500k.zip": "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip",
        "acsdt5y2024-b01003.dat": "https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01003.dat",
        "acsdt5y2024-b25001.dat": "https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b25001.dat",
        "co-est2025-alldata.csv": "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv",
    },
    "hurdat2": {"hurdat2-1851-2025-092326.txt": "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-092326.txt"},
    "oe417": {
        "eia_epm_table_b1_2024.html": "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_b_1",
        "eia_epm_table_b2_2023.html": "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_b_2",
    },
    "scc_reliability": {
        "rga_2025_RD916.pdf": "https://rga.lis.virginia.gov/Published/2025/RD916/PDF",
        "rga_2025_HD5.pdf": "https://rga.lis.virginia.gov/Published/2025/HD5/PDF",
    },
    "doe417": {**{f"{y}_Annual_Summary.xls": f"https://doe417.pnnl.gov/summaries/{y}_Annual_Summary.xls" for y in range(2014, 2024)},
               **{f"{y}_Annual_Summary.xlsx": f"https://doe417.pnnl.gov/summaries/{y}_Annual_Summary.xlsx" for y in (2024, 2025)}},
    "pjm": {"2026-load-report-tables.xlsx": "https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx"},
}
NOTES = {
    "doe417_events_2014_2025.csv": "derived: every event row of the 12 annual summaries in one long table (scripts/extract_doe417.py); workbooks unchanged",
    "va_counties_cb2024.geojson": "derived: Virginia features of cb_2024_us_county_500k (scripts/extract_census_va.py)",
    "va_county_census.csv": "derived: ACS 2020-2024 B01003/B25001 and PEP v2025 for the 133 Virginia counties and cities",
}


def rows_of(p: Path):
    if p.suffix.lower() in (".zip", ".pdf", ".xls", ".xlsx"):
        return ""
    if p.suffix.lower() == ".csv":  # records, not lines: quoted fields can hold line breaks
        with p.open(newline="", encoding="utf-8", errors="replace") as f:
            return max(sum(1 for _ in csv.reader(f)) - 1, 0)
    with p.open("rb") as f:
        n = sum(1 for _ in f)
    return max(n - 1, 0)


def main():
    for folder, urls in URLS.items():
        d = RAW / folder
        if folder == "degree_days":
            continue
        out = []
        for p in sorted(d.iterdir()):
            if p.name == "MANIFEST.csv" or p.is_dir():
                continue
            when = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            out.append({"file": p.name, "rows": rows_of(p), "bytes": p.stat().st_size,
                        "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "url": urls.get(p.name, ""),
                        "downloaded_at": when, "note": NOTES.get(p.name, "as downloaded")})
        write(d / "MANIFEST.csv", out)
    # degree days: one file per year and kind
    d = RAW / "degree_days"
    out = []
    for p in sorted(d.glob("cpc_StatesCONUS_*.txt")):
        _, _, kind, year = p.stem.split("_")
        url = f"https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/{year}/StatesCONUS.{kind}.txt"
        when = dt.datetime.fromtimestamp(p.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out.append({"file": p.name, "rows": rows_of(p), "bytes": p.stat().st_size,
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "url": url, "downloaded_at": when,
                    "note": f"CPC population-weighted daily {kind.lower()} degree days by state, {year} (wide: one column per day)"})
    write(d / "MANIFEST.csv", out)


def write(path, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "rows", "bytes", "sha256", "url", "downloaded_at", "note"])
        w.writeheader()
        w.writerows(rows)
    print(path.relative_to(ROOT).as_posix(), len(rows), "files")


if __name__ == "__main__":
    URLS["degree_days"] = {}
    main()
