"""R batch 5: rule-free (all-events) peer ranks, medians without Dominion, and Dominion's EIA flags.

Read-only. Inputs: data/output/peer_reliability_5yr.csv (the 12-utility set, D10) and
data/output/fct_reliability.csv. Prints a plain-text report. Run with the repo's venv python -I.
Usage: r5b_all_events_rank.py <repo_root> <out_txt>
"""
import sys
from pathlib import Path

import pandas as pd

root = Path(sys.argv[1])
out = Path(sys.argv[2])
peers = pd.read_csv(root / "data/output/peer_reliability_5yr.csv")
fct = pd.read_csv(root / "data/output/fct_reliability.csv")
keys = peers["utility_key"].tolist()
names = dict(zip(peers["utility_key"], peers["utility_name"]))
dom = peers.loc[peers["is_dominion"], "utility_key"].iloc[0]

f = fct[fct["utility_key"].isin(keys)].copy()
lines = [f"peer set: {len(keys)} utilities; Dominion key {dom}"]

def window(col, y0, y1):
    w = f[(f["year"] >= y0) & (f["year"] <= y1)].groupby("utility_key")[col].agg(["mean", "count"])
    w["name"] = w.index.map(names)
    return w.sort_values("mean", ascending=False)

for col, y0, y1 in [("saifi_all", 2021, 2025), ("saifi_ex_med", 2021, 2025),
                    ("caidi_all", 2021, 2025), ("caidi_ex_med", 2021, 2025),
                    ("saidi_all", 2023, 2025), ("saidi_ex_med", 2023, 2025)]:
    w = window(col, y0, y1)
    w["rank_highest"] = range(1, len(w) + 1)
    others = w.drop(index=dom)
    lines.append(f"\n== {col} mean {y0}-{y1} (rank 1 = highest) ==")
    for k, r in w.iterrows():
        tag = "  <== Dominion" if k == dom else ""
        lines.append(f"{int(r['rank_highest']):>2}  {r['mean']:9.3f}  n={int(r['count'])}  {r['name']}{tag}")
    lines.append(f"median of all {len(w)}: {w['mean'].median():.3f}; median of the {len(others)} others "
                 f"(excluding Dominion): {others['mean'].median():.3f}")

d = fct[fct["utility_key"] == dom].sort_values("year")
lines.append("\n== Dominion VA by year: standard, auto_recorded, SAIFI ex-MED, SAIFI all ==")
for _, r in d.iterrows():
    lines.append(f"{int(r['year'])}  standard={r['standard']}  auto_recorded={r['auto_recorded']}  "
                 f"saifi_ex_med={r['saifi_ex_med']}  saifi_all={r['saifi_all']}  saidi_ex_med={r['saidi_ex_med']}")

std = f[f["year"] == 2025][["utility_key", "standard"]]
std["name"] = std["utility_key"].map(names)
lines.append("\n== 2025 reporting standard by peer ==")
for _, r in std.sort_values("name").iterrows():
    lines.append(f"{r['standard']:<12} {r['name']}")

out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("written", out)
