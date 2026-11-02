"""Append the handout to used_in of the claims rows it prints, and add a row for its chart.

Idempotent: a row that already names the handout is left alone. Rows must be variant public or
both (the handout is public-only); the script stops otherwise.
"""
import csv
import sys
from pathlib import Path

CLAIMS = Path(__file__).resolve().parents[2] / "claims.csv"
TAG = "handout"
USES = {
    "C-S2-01": "handout p1 finding 1 ('130 to 133')",
    "C-S2-02": "handout p2 Reconciled ('130.2 and 133.0', '130 and 133')",
    "C-S4-01P": "handout p1 finding 1 ('465 in 2024 to 796 in 2025') and chart labels",
    "C-S4-03": "handout p1 finding 2 ('about 145.3 minutes; the actual figure was 144.4')",
    "C-S4-06": "handout p1 finding 2 heading ('there is no clear trend')",
    "C-S4-05P": "handout p1 chart (2015-2025 storm days and minutes; labels 465, 796, 131.3, 144.4)",
    "C-S3-11P": "handout p1 finding 3 ('1.21 times a year, 4th highest of the 12, where the median is 0.96')",
    "C-S3-02P": "handout p1 finding 3 ('110 minutes, against a median of 105')",
    "C-S7-05": "handout p2 Tested ('12 automatic tests')",
    "C-S5-01P": "handout p2 demand box ('between 3 and 4 a.m. rose 41%'; '3 and 4 p.m., 27%' = hours ending 4 a.m. and 4 p.m.)",
    "C-S5-02": "handout p2 demand box ('set the year's peak in 2019, 2022 and 2025')",
    "C-S5-14P": "handout p2 screenshot (same image as the public deck S5)",
}

sys.stdout.reconfigure(encoding="utf-8")
with open(CLAIMS, encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    rows = list(reader)
by_id = {r["id"]: r for r in rows}
missing = [k for k in USES if k not in by_id]
assert not missing, f"rows not found: {missing}"
bad = [(k, by_id[k]["variant"]) for k in USES if by_id[k]["variant"] not in ("public", "both")]
assert not bad, f"not public/both: {bad}"
changed = 0
for k, use in USES.items():
    r = by_id[k]
    if TAG in r["used_in"]:
        continue
    r["used_in"] = f"{r['used_in']}; {use}"
    changed += 1
new_id = "C-H-01"
if new_id not in by_id:
    rows.append({
        "id": new_id,
        "exact_text": "[chart] handout p1: storm days and minutes without power per customer, 2015-2025, 2025 highlighted",
        "value": "per row (as C-S4-05P)",
        "unit": "county-days; minutes (SAIDI ex-MED)",
        "used_in": "handout p1 chart",
        "source": "origin/main data/output/storm_vs_saidi.csv; snapshot work/charts/final/h1_storm_days_and_outage_minutes.csv; "
                  "build_handout.py asserts it equals C-S4-05P",
        "producer": "orchestrator",
        "checked_by": "orchestrator (build assert)",
        "result": "MATCH (build assert against C-S4-05P and origin/main)",
        "variant": "public",
        "producer_check": "assert in work/handout/build_handout.py",
    })
    changed += 1
with open(CLAIMS, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
print(f"rows changed or added: {changed}; total rows: {len(rows)}")
