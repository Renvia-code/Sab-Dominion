"""Print the claims_register rows that claims.csv cites (read-only)."""
import sys, csv
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
ids = sys.argv[1:] or ["R-002","R-003","R-004","R-006","R-008","R-009","R-010","R-013","R-028","R-035","R-036","R-037","R-040","R-048","R-049","R-052","R-053","R-054","R-059","R-081","R-082","R-088","R-091"]
with open(REPO + r"\interview-prep\research\claims_register.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
by = {r["id"]: r for r in rows}
print("register rows:", len(rows))
for i in ids:
    r = by.get(i)
    if not r:
        print(i, "NOT FOUND"); continue
    print("=" * 100)
    for k, v in r.items():
        print(f"{k}: {v}")
