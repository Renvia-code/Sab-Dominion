"""Update fields of existing rows in research/claims_register.csv from a JSON file, safely quoted.

Usage: python -I r_update_claim.py <updates.json>
updates.json: {"R-028": {"quote_or_locator": "...", "confidence": "..."}, ...}
Refuses unknown ids or unknown fields. Prints each change (old length -> new length).
"""
import csv
import json
import sys
from pathlib import Path

REG = Path(__file__).resolve().parents[2] / "research" / "claims_register.csv"


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    updates = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    rows = list(csv.reader(REG.open(encoding="utf-8")))
    head, body = rows[0], rows[1:]
    idx = {r[0]: r for r in body}
    for cid, fields in updates.items():
        if cid not in idx:
            sys.exit(f"unknown id {cid}")
        for f, v in fields.items():
            if f not in head or f == "id":
                sys.exit(f"bad field {f}")
            k = head.index(f)
            print(f"{cid}.{f}: {len(idx[cid][k])} -> {len(v)} chars")
            idx[cid][k] = v
    with REG.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(head)
        w.writerows(body)
    print(f"rows {len(body)}")


if __name__ == "__main__":
    main()
