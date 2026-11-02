"""Final round: reporting standard by peer and year (N-5 check), plus FPL vs Dominion all-events figures.

Read-only. Inputs: data/output/peer_reliability_5yr.csv and data/output/fct_reliability.csv.
Usage: python -I r_final_standards_check.py <repo_root>
"""
import sys
from pathlib import Path

import pandas as pd


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(sys.argv[1])
    peers = pd.read_csv(root / "data/output/peer_reliability_5yr.csv")
    fct = pd.read_csv(root / "data/output/fct_reliability.csv")
    names = dict(zip(peers["utility_key"], peers["utility_name"]))
    f = fct[fct["utility_key"].isin(names)].copy()
    f["name"] = f["utility_key"].map(names)

    piv = f[(f["year"] >= 2013) & (f["year"] <= 2025)].pivot_table(
        index="name", columns="year", values="standard", aggfunc="first")
    print("== standard by peer and year (I = IEEE 1366, O = Other, - = missing) ==")
    for name, row in piv.iterrows():
        cells = "".join("I" if v == "IEEE 1366" else "O" if v == "Other" else "-" for v in row.values)
        print(f"{cells}  {name}")
    print("years:", " ".join(str(c) for c in piv.columns))

    always_ieee = [n for n, r in piv.iterrows()
                   if all(r.get(y) == "IEEE 1366" for y in range(2014, 2026))]
    print(f"\npeers on IEEE 1366 in every year 2014-2025: {len(always_ieee)} of {len(piv)}")

    for col, y0, y1 in [("saifi_all", 2021, 2025), ("saifi_ex_med", 2021, 2025),
                        ("caidi_all", 2021, 2025), ("saidi_all", 2023, 2025), ("saidi_ex_med", 2023, 2025)]:
        w = f[(f["year"] >= y0) & (f["year"] <= y1)].groupby("name")[col].mean()
        fpl = w[[n for n in w.index if n.startswith("Florida Power")][0]]
        dom = w[[n for n in w.index if n.startswith("Virginia Electric")][0]]
        print(f"{col} {y0}-{y1}: FPL {fpl:.3f}  Dominion {dom:.3f}  ratio FPL/Dominion {fpl / dom:.2f}")


if __name__ == "__main__":
    main()
