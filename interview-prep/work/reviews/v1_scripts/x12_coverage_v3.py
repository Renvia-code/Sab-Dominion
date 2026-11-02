"""Coverage on v3: same tokenizer and matching rule as x02 (with the en-dash fix), v3 texts against v3 claims.
Prints (1) uncovered tokens, (2) tokens uncovered now that were covered or absent in v2 (new gaps),
(3) adopted-only and stale-public markers in the v3 public deck."""
import sys, os, re, csv, collections
sys.stdout.reconfigure(encoding='utf-8')
RV = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
NUM = re.compile(r"(?<![\w.\-/])(?:[−\-+])?\$?(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?(?:\s?(?:%|×|M\b|GW\b|MW\b|TWh\b))?")
TIME = re.compile(r"(?<![\w:])\d{1,2}:\d{2}(?![\w:])")
def tokens(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("=====") or re.fullmatch(r"\d+ / \d+", s) or re.fullmatch(r"Side \d of \d", s):
            continue
        for m in TIME.finditer(line): out.append((m.group(0), line))
        l2 = TIME.sub(" ", line)
        for m in NUM.finditer(l2):
            tok = m.group(0).strip()
            if not re.search(r"\d", tok): continue
            if m.start() == len(l2) - len(l2.lstrip()) and re.fullmatch(r"\d{1,2}", tok) and int(tok) <= 25:
                rest = l2[m.end():].lstrip()
                if not rest or rest[0].isupper() or rest[0].isdigit() or rest[0] in "|": continue
            out.append((tok, line))
    return out
def parse(tok):
    t = re.sub(r"\s?(%|×|M|GW|MW|TWh)$", "", tok.replace("−", "-").replace("$", "").replace(",", "").replace("+", "")).strip()
    try: v = abs(float(t))
    except ValueError: return None, 0
    return v, (len(t.split(".")[1]) if "." in t else 0)
def load_claims(path):
    cn, ct = [], set()
    for c in csv.DictReader(open(path, encoding="utf-8")):
        blob = c["exact_text"] + " ; " + c["value"].replace(";", " ; ")
        ct.update(TIME.findall(blob))
        for tok, _ in tokens(blob.replace(";", " ")):
            v, _ = parse(tok)
            if v is not None: cn.append((v, c["id"]))
    return cn, ct
def covered(tok, cn, ct):
    if TIME.fullmatch(tok): return [c for c in ct if c.lstrip("0") == tok.lstrip("0")][:1]
    v, dp = parse(tok)
    if v is None: return ["unparsed"]
    return sorted({cid for cv, cid in cn if abs(cv - v) <= 0.5 * 10 ** (-dp) + 1e-9})
DOCS = ["deck_adopted_slides", "deck_adopted_notes", "deck_adopted_pdf", "deck_public_slides", "deck_public_notes", "deck_public_pdf",
        "brief_pdf", "brief_html", "qsheet_pdf", "qsheet_html"]
def run(txtdir, claims):
    cn, ct = load_claims(claims); rows = []
    for name in DOCS:
        text = open(os.path.join(txtdir, name.replace("_slides", "_slides").rsplit("_", 1)[0] + "_" + name.rsplit("_", 1)[1] + ".txt"), encoding="utf-8").read()
        for tok, line in tokens(text):
            v, dp = parse(tok) if not TIME.fullmatch(tok) else (None, 0)
            if v is not None and dp == 0 and 2013 <= v <= 2027 and re.fullmatch(r"\d{4}", tok.strip("+−-")): continue
            if name.startswith("deck") and re.fullmatch(r"\d{1,2}", tok) and line.strip() == tok: continue
            rows.append((name, tok, ";".join(covered(tok, cn, ct)[:6]), re.sub(r"\s+", " ", line.strip())[:150]))
    return rows
v3 = run(RV + r"\v1_text_v3", RV + r"\snapshot_v3_audit\claims.csv")
v2 = run(RV + r"\v1_text", RV + r"\snapshot_v2_1035\claims.csv")
with open(RV + r"\v1_work\coverage_tokens_v3.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["doc", "token", "covered_by", "context"]); w.writerows(v3)
unc3 = collections.OrderedDict(); unc2 = set()
for d, t, c, x in v2:
    if not c: unc2.add((t, x[:70]))
for d, t, c, x in v3:
    if not c: unc3.setdefault((t, x[:70]), set()).add(d)
print("v3 tokens:", len(v3), "| uncovered:", sum(1 for r in v3 if not r[2]), "| distinct uncovered:", len(unc3))
for (t, x), ds in unc3.items():
    print(f"{'NEW ' if (t, x) not in unc2 else '    '}{t:>9} | {','.join(sorted(ds))[:45]:<45} | {x}")
v2ctx = {(t, x[:90]) for d, t, c, x in v2}
print("\nTokens whose (token, context) is new in v3 (any coverage), deduplicated:")
seen = set()
for d, t, c, x in v3:
    k = (t, x[:90])
    if k not in v2ctx and k not in seen:
        seen.add(k); print(f"  {t:>9} | {d:<20} | via {c[:30]:<30} | {x[:120]}")
pub = "\n".join(open(RV + rf"\v1_text_v3\{f}.txt", encoding="utf-8").read() for f in ["deck_public_slides", "deck_public_notes", "deck_public_pdf"])
markers = ["EAGLE", "T13", "T31", "D15", "D16", "D17", "D18", "D19", "D20", "D21", "D22", "718", "791", "464", "degree", "12 of 12", "6,094,320",
           "31 tests", "25,413", "Oct 29", "October 29", "11.9", "6,108", "332.8", "HURDAT", "DOE-417", "CPC", "11,608,442", "18 tables", "DataFolder",
           "0.025", "122.3", "168.2", "+0.3", "Isaias", "33.5", "39–41", "33%", "Dominion-only", "10 of 12", "10 of the 12", "every year 2014", "0.93",
           "99.3", "99.5", "11-peer", "11 peers'", "peer median", "medians exclude", "most peers", "IEEE 1366 every", "minutes to restore", "Minutes to restore"]
print("\npublic v3 deck markers:", {m: pub.count(m) for m in markers if m in pub} or "none")
