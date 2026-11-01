"""Keep the Virginia rows of the EAGLE-I county outage files and write the manifest.

Input: the zips that scripts/download_eaglei.sh saved in data/raw/eaglei/downloads/ (DOE EAGLE-I
Aviary, https://eagle-i.doe.gov/aviary), plus the figshare record snapshot saved beside them
(doi:10.6084/m9.figshare.24237376, version 4). Each yearly CSV is streamed out of its zip once:
its MD5 is compared with the MD5 figshare publishes for the same file, its SHA-256, bytes and
rows are recorded, and the rows for Virginia (state "Virginia", county FIPS 51xxx) are written
unchanged to data/raw/eaglei/va/eaglei_outages_va_<year>.csv. The full national files are not
kept (13.6 GB); the zips are.

Then DuckDB types the Virginia rows into one Parquet file, eaglei_va_2014_2025.parquet:
fips_code (text, 5 digits), county, state, customers_out (integer; the 2023 file calls it "sum";
blank in the source = NULL, a failed collection run), run_start_time (timestamp, UTC as
published), total_customers (integer, only in the 2024 file), source_file.

Output: data/raw/eaglei/MANIFEST.csv with file, rows, bytes, sha256, url, downloaded_at and the
MD5 check. Run with: python -I scripts/extract_eaglei_va.py
"""
import csv
import datetime as dt
import hashlib
import json
import re
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "data" / "raw" / "eaglei"
DL = BASE / "downloads"
VA = BASE / "va"
PARQUET = BASE / "eaglei_va_2014_2025.parquet"
URL = "https://eagle-i.doe.gov/api/aviary/download?file={}"
VA_LINE = re.compile(rb"(?m)^[^\n]*,Virginia,[^\n]*\n")


def sha256_md5(path: Path):
    s, m = hashlib.sha256(), hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            s.update(chunk)
            m.update(chunk)
    return s.hexdigest(), m.hexdigest()


def stream_year(zpath: str):
    """Stream one yearly CSV out of its zip: hashes, row count, Virginia rows."""
    zpath = Path(zpath)
    csvname = zpath.stem + ".csv"
    out_path = VA / csvname.replace("eaglei_outages_", "eaglei_outages_va_")
    md5, sha = hashlib.md5(), hashlib.sha256()
    nbytes = newlines = va_rows = odd_rows = 0
    carry, header = b"", None
    with zipfile.ZipFile(zpath) as z, z.open(csvname) as f, out_path.open("wb") as out:
        while True:
            chunk = f.read(1 << 24)
            if not chunk:
                break
            md5.update(chunk)
            sha.update(chunk)
            nbytes += len(chunk)
            newlines += chunk.count(b"\n")
            data = carry + chunk
            cut = data.rfind(b"\n") + 1
            block, carry = data[:cut], data[cut:]
            if header is None and block:
                header, block = block.split(b"\n", 1)
                header += b"\n"
                out.write(header)
            for m in VA_LINE.finditer(block):
                line = m.group(0)
                fields = line.rstrip(b"\r\n").split(b",")
                if b'"' in line or len(fields) < 5:
                    odd_rows += 1
                if len(fields) >= 3 and fields[2] == b"Virginia" and fields[0].startswith(b"51") and len(fields[0]) == 5:
                    out.write(line)
                    va_rows += 1
                elif len(fields) >= 3 and fields[2] == b"Virginia":
                    odd_rows += 1
        if carry:  # last line without a newline
            newlines += 1
            fields = carry.rstrip(b"\r").split(b",")
            if len(fields) >= 3 and fields[2] == b"Virginia" and fields[0].startswith(b"51"):
                out.write(carry + b"\n")
                va_rows += 1
    return {"zip": zpath.name, "csv": csvname, "csv_bytes": nbytes, "csv_rows": newlines - 1,
            "csv_md5": md5.hexdigest(), "csv_sha256": sha.hexdigest(), "header": header.decode().strip(),
            "va_file": out_path.name, "va_rows": va_rows, "odd_rows": odd_rows}


def extract_small(zpath: Path):
    """MCC.csv and coverage_history.csv: write the CSV out of its zip unchanged."""
    csvname = zpath.stem + ".csv"
    with zipfile.ZipFile(zpath) as z:
        data = z.read(csvname)
    (BASE / csvname).write_bytes(data)
    rows = data.count(b"\n") - 1 + (0 if data.endswith(b"\n") else 1)
    return {"zip": zpath.name, "csv": csvname, "csv_bytes": len(data), "csv_rows": rows,
            "csv_md5": hashlib.md5(data).hexdigest(), "csv_sha256": hashlib.sha256(data).hexdigest()}


def main():
    VA.mkdir(parents=True, exist_ok=True)
    fig = json.loads(sorted(DL.glob("figshare_24237376_*.json"))[-1].read_text(encoding="utf-8"))
    published = {f["name"]: (f.get("computed_md5") or f.get("supplied_md5"), f["size"]) for f in fig["files"]}
    zips = sorted(DL.glob("*.zip"))
    good = []
    for z in zips:
        try:
            with zipfile.ZipFile(z) as zz:
                if zz.testzip() is None:
                    good.append(z)
        except zipfile.BadZipFile:
            print(f"skip (incomplete) {z.name}", file=sys.stderr)
    years = [z for z in good if z.stem.startswith("eaglei_outages_")]
    small = [z for z in good if z.stem in ("MCC", "coverage_history")]
    with ProcessPoolExecutor(max_workers=6) as ex:
        results = list(ex.map(stream_year, [str(z) for z in years]))
    results += [extract_small(z) for z in small]

    rows = []
    for r in sorted(results, key=lambda x: x["csv"]):
        zpath = DL / r["zip"]
        zsha, zmd5 = sha256_md5(zpath)
        when = dt.datetime.fromtimestamp(zpath.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        url = URL.format(r["csv"])
        pub_md5, pub_size = published.get(r["csv"], (None, None))
        rows.append({"file": f"downloads/{r['zip']}", "rows": "", "bytes": zpath.stat().st_size, "sha256": zsha,
                     "url": url, "downloaded_at": when, "md5": zmd5, "md5_published": "", "md5_match": "",
                     "note": f"zip as served by the DOE EAGLE-I Aviary; holds {r['csv']} and DOI citation text files"})
        kept = "kept" if r["csv"] in ("MCC.csv", "coverage_history.csv") else "not kept (streamed from the zip)"
        rows.append({"file": r["csv"], "rows": r["csv_rows"], "bytes": r["csv_bytes"], "sha256": r["csv_sha256"],
                     "url": url, "downloaded_at": when, "md5": r["csv_md5"], "md5_published": pub_md5 or "",
                     "md5_match": (r["csv_md5"] == pub_md5) if pub_md5 else "",
                     "note": f"national file, {kept}; figshare size {pub_size}" + (f"; header: {r['header']}" if "header" in r else "")})
        if "va_file" in r:
            vpath = VA / r["va_file"]
            vsha, vmd5 = sha256_md5(vpath)
            rows.append({"file": f"va/{r['va_file']}", "rows": r["va_rows"], "bytes": vpath.stat().st_size, "sha256": vsha,
                         "url": "", "downloaded_at": when, "md5": vmd5, "md5_published": "", "md5_match": "",
                         "note": f"Virginia rows of {r['csv']} (state = Virginia, FIPS 51xxx), bytes unchanged; rows needing review: {r['odd_rows']}"})

    # Typed Parquet of all Virginia rows
    import duckdb
    con = duckdb.connect()
    files = sorted(VA.glob("eaglei_outages_va_*.csv"))
    flist = "[" + ",".join(f"'{p.as_posix()}'" for p in files) + "]"
    con.execute(f"""
        COPY (
          SELECT LPAD(CAST(fips_code AS VARCHAR), 5, '0')         AS fips_code,
                 county, state,
                 -- the 2023 file names this column "sum"; a blank value marks a failed
                 -- collection run and stays NULL (not zero)
                 TRY_CAST(COALESCE(NULLIF(customers_out, ''), NULLIF("sum", '')) AS INTEGER) AS customers_out,
                 CAST(run_start_time AS TIMESTAMP)                 AS run_start_time,
                 TRY_CAST(total_customers AS INTEGER)              AS total_customers,
                 regexp_extract(filename, 'eaglei_outages_va_[0-9]{{4}}\\.csv') AS source_file
          FROM read_csv({flist}, union_by_name = true, filename = true, all_varchar = true)
          ORDER BY fips_code, run_start_time
        ) TO '{PARQUET.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)""")
    n = con.execute(f"SELECT COUNT(*) FROM read_parquet('{PARQUET.as_posix()}')").fetchone()[0]
    psha, pmd5 = sha256_md5(PARQUET)
    rows.append({"file": PARQUET.name, "rows": n, "bytes": PARQUET.stat().st_size, "sha256": psha, "url": "",
                 "downloaded_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "md5": pmd5,
                 "md5_published": "", "md5_match": "", "note": f"typed union of {len(files)} files in va/ (DuckDB {duckdb.__version__})"})
    for snap in sorted(DL.glob("*.json")):
        ssha, smd5 = sha256_md5(snap)
        src = "https://eagle-i.doe.gov/api/aviary/files" if snap.name.startswith("aviary") else "https://api.figshare.com/v2/articles/24237376"
        rows.append({"file": f"downloads/{snap.name}", "rows": "", "bytes": snap.stat().st_size, "sha256": ssha, "url": src,
                     "downloaded_at": dt.datetime.fromtimestamp(snap.stat().st_mtime, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     "md5": smd5, "md5_published": "", "md5_match": "", "note": "file list snapshot (names, sizes, MD5s, column notes)"})

    cols = ["file", "rows", "bytes", "sha256", "url", "downloaded_at", "md5", "md5_published", "md5_match", "note"]
    with (BASE / "MANIFEST.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    bad = [r for r in rows if r["md5_match"] is False]
    print(f"{len(years)} yearly files, {len(small)} supplementary; Virginia rows in Parquet: {n:,}")
    for r in rows:
        if r["file"].endswith(".csv") and not r["file"].startswith("va/"):
            print(f"  {r['file']}: {r['rows']:,} rows, md5 match = {r['md5_match']}")
    if bad:
        raise SystemExit(f"MD5 mismatch: {[r['file'] for r in bad]}")


if __name__ == "__main__":
    main()
