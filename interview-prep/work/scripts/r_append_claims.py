"""Append rows to research/claims_register.csv from a small JSON-lines file, safely quoted.

Usage: python -I r_append_claims.py <rows.jsonl>
Each line: {"id":..., "claim":..., "value":..., "url_or_doi":..., "accessed":..., "quote_or_locator":...,
            "confidence":..., "used_in":...}
Refuses duplicate ids. Prints the new row count.
"""
import csv
import json
import sys
from pathlib import Path

REG = Path(__file__).resolve().parents[2] / "research" / "claims_register.csv"
COLS = ["id", "claim", "value", "url_or_doi", "accessed", "quote_or_locator", "confidence", "used_in"]


def main():
    existing = list(csv.reader(REG.open(encoding="utf-8")))
    ids = {r[0] for r in existing[1:]}
    new = []
    for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj["id"] in ids:
            sys.exit(f"duplicate id {obj['id']}")
        ids.add(obj["id"])
        new.append([str(obj.get(c, "")) for c in COLS])
    with REG.open("a", encoding="utf-8", newline="") as fh:
        csv.writer(fh, quoting=csv.QUOTE_MINIMAL, lineterminator="\n").writerows(new)
    print(f"appended {len(new)}; total rows {len(existing) - 1 + len(new)}")


if __name__ == "__main__":
    main()
