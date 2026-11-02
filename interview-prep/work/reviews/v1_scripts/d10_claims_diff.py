"""Diff v3 claims (frozen copy) against the v2 snapshot: added, removed, and changed fields per row."""
import sys, csv
sys.stdout.reconfigure(encoding='utf-8')
R = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
old = {r["id"]: r for r in csv.DictReader(open(R + r"\snapshot_v2_1035\claims.csv", encoding="utf-8"))}
new = {r["id"]: r for r in csv.DictReader(open(R + r"\snapshot_v3_audit\claims.csv", encoding="utf-8"))}
print("v2 rows", len(old), "| v3 rows", len(new))
added = [i for i in new if i not in old]; removed = [i for i in old if i not in new]
print("added:", added); print("removed:", removed)
announced = set("C-S3-01 C-S3-02 C-S4-08 C-S4-09 C-S5-04 C-S5-07 C-S6-02 C-S7-10 C-S8-01 C-Q-03 C-Q-06 C-Q-08 C-Q-10 C-S3-02P C-S3-04P C-S3-07 C-S3-09 C-S4-05P C-S4-20 C-S5-11 C-S5-12 C-S7-05A C-S6-06 C-B-03 C-B-01".split())
fields = ["exact_text", "value", "unit", "used_in", "source", "producer", "checked_by", "result", "variant"]
changed = {}
for i in new:
    if i in old:
        diffs = [f for f in fields if new[i][f] != old[i][f]]
        if diffs: changed[i] = diffs
key = {"exact_text", "value", "source", "used_in", "variant"}
print("changed rows:", len(changed))
print("changed in key fields but NOT announced:", [i for i, d in changed.items() if set(d) & key and i not in announced])
print("announced but no key-field change:", [i for i in announced if not (set(changed.get(i, [])) & key)])
mode = sys.argv[1] if len(sys.argv) > 1 else "brief"
for i in added + sorted(announced):
    r = new[i]
    print("=" * 100); print(i, "| ADDED" if i in added else "| changed: " + ",".join(changed.get(i, [])))
    for f in fields:
        if i in added or f in changed.get(i, []):
            if i not in added:
                print(f"  - {f} (v2): {old[i][f]}")
            print(f"  + {f}: {r[f]}")
