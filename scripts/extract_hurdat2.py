"""Turn NHC HURDAT2 (data/raw/hurdat2/hurdat2-1851-2025-*.txt) into one CSV of track points:
data/raw/hurdat2/hurdat2_points.csv. The text file is left unchanged.

HURDAT2 interleaves a header line per storm ("AL092020, ISAIAS, 36,") with that many data lines
("20200804, 1200,  , TS, 37.7N,  76.8W,  60,  993, ..."). Each data line becomes one row with the
storm id and name; latitude and longitude become signed decimals (S and W negative); -999 wind or
pressure becomes empty. Wind radii columns are dropped.

Run: .venv/Scripts/python.exe -I scripts/extract_hurdat2.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "raw" / "hurdat2"
COLS = ["storm_id", "storm_name", "obs_date", "obs_time", "record_id", "status", "lat", "lon", "max_wind_kt", "min_pressure_mb"]


def coord(s):
    s = s.strip()
    v = float(s[:-1])
    return -v if s[-1] in "SW" else v


def num(s):
    s = s.strip()
    return "" if s in ("", "-999") else int(s)


def main():
    src = sorted(D.glob("hurdat2-1851-*.txt"))[-1]
    out, storm_id, name, left = [], None, None, 0
    with src.open(encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.rstrip("\n").split(",")]
            if left == 0:
                storm_id, name, left = parts[0], parts[1], int(parts[2])
                continue
            out.append({"storm_id": storm_id, "storm_name": name, "obs_date": parts[0], "obs_time": parts[1],
                        "record_id": parts[2], "status": parts[3], "lat": coord(parts[4]), "lon": coord(parts[5]),
                        "max_wind_kt": num(parts[6]), "min_pressure_mb": num(parts[7])})
            left -= 1
    dest = D / "hurdat2_points.csv"
    with dest.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator="\n")
        w.writeheader()
        w.writerows(out)
    print(src.name, "->", dest.relative_to(ROOT).as_posix(), len(out), "points,", len({r["storm_id"] for r in out}), "storms")


if __name__ == "__main__":
    main()
