"""Turn the NOAA CPC daily degree-day files (data/raw/degree_days/cpc_StatesCONUS_{Heating,Cooling}_YYYY.txt,
population-weighted, one row per state and one column per day) into one long CSV:
data/raw/degree_days/cpc_degree_days_long.csv (region, obs_date, kind, degree_days). Files unchanged.

Run: .venv/Scripts/python.exe -I scripts/extract_degree_days.py
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = ROOT / "data" / "raw" / "degree_days"


def main():
    rows = 0
    with (D / "cpc_degree_days_long.csv").open("w", newline="", encoding="utf-8") as out:
        w = csv.writer(out, lineterminator="\n")
        w.writerow(["region", "obs_date", "kind", "degree_days"])
        for p in sorted(D.glob("cpc_StatesCONUS_*_*.txt")):
            kind = "HDD" if "_Heating_" in p.name else "CDD"
            header = None
            for line in p.read_text(encoding="utf-8").splitlines():
                parts = line.strip().split("|")
                if parts[0] == "Region":
                    header = parts[1:]
                    continue
                if header is None or len(parts) != len(header) + 1:
                    continue
                for day, val in zip(header, parts[1:]):
                    w.writerow([parts[0], f"{day[:4]}-{day[4:6]}-{day[6:]}", kind, val])
                    rows += 1
    print("cpc_degree_days_long.csv", rows, "rows")


if __name__ == "__main__":
    main()
