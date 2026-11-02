"""Strict coverage pass over v1_work/coverage_tokens.csv: a token counts as covered only if a covering claim row
(a) names the same document type in used_in (deck / brief / qsheet) and (b) either contains the token string verbatim
in exact_text/value, or shares a content word (>= 4 letters) with the token's context line."""
import sys, re, csv
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
WORK = REPO + r"\interview-prep\work\reviews\v1_work"
claims = {c["id"]: c for c in csv.DictReader(open(REPO + r"\interview-prep\work\reviews\snapshot_v2_1035\claims.csv", encoding="utf-8"))}
STOP = set("with that this from were have than they their there which what when into over about after before only also each every more most less year years data shows show public deck brief notes slide source minutes".split())
def words(s):
    return {w for w in re.findall(r"[a-z]{4,}", s.lower()) if w not in STOP}
rows = list(csv.DictReader(open(WORK + r"\coverage_tokens.csv", encoding="utf-8")))
weak = {}
for r in rows:
    if not r["covered_by"]:
        continue
    dtype = "deck" if r["doc"].startswith("deck") else ("brief" if r["doc"].startswith("brief") else "qsheet")
    tok = r["token"].replace("−", "-")
    ok = False
    for cid in r["covered_by"].split(";"):
        c = claims.get(cid)
        if not c or dtype not in c["used_in"].lower():
            continue
        blob = (c["exact_text"] + " " + c["value"]).replace("−", "-")
        if tok.strip("+-$%×M ") in blob or words(r["context"]) & words(c["exact_text"] + " " + c["unit"]):
            ok = True; break
    if not ok:
        key = (r["token"], r["context"][:90])
        weak.setdefault(key, [set(), r["covered_by"]])[0].add(r["doc"])
print("weakly covered (number matches a claim value, but no claim row ties it to this document and wording):", len(weak))
for (tok, ctx), (ds, cov) in sorted(weak.items(), key=lambda kv: (sorted(kv[1][0])[0], kv[0][1])):
    print(f"{tok:>9} | {','.join(sorted(d.replace('deck_', 'd_') for d in ds))[:40]:<40} | via {cov[:28]:<28} | {ctx}")
