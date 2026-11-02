"""Coverage: every number printed in the deliverables vs the numbers in claims.csv (exact_text + value).
A token is covered when some claim number rounds to it at the token's printed precision (sign ignored).
Ignored: years 2013-2027 (period labels and dates; years-as-data rows are checked row by row), page/slide markers,
question/decision/test/appendix ids (letter-prefixed), line-start item numbers, the document date.
Writes v1_work/coverage_tokens.csv (every token) and prints the uncovered ones grouped by value."""
import sys, os, re, csv
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
TXT = REPO + r"\interview-prep\work\reviews\v1_text"
WORK = REPO + r"\interview-prep\work\reviews\v1_work"
NUM = re.compile(r"(?<![\w.\-/])(?:[−\-+])?\$?(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?(?:\s?(?:%|×|M\b|GW\b|MW\b|TWh\b))?")
TIME = re.compile(r"(?<![\w:])\d{1,2}:\d{2}(?![\w:])")

def tokens(text):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("=====") or re.fullmatch(r"\d+ / \d+", s) or re.fullmatch(r"Side \d of \d", s):
            continue
        for m in TIME.finditer(line):
            out.append((m.group(0), line))
        line2 = TIME.sub(" ", line)
        for m in NUM.finditer(line2):
            tok = m.group(0).strip()
            if not re.search(r"\d", tok):
                continue
            # line-start item numbers ("13 How do...", "2 130 → 133", "1 Title")
            if m.start() == len(line2) - len(line2.lstrip()) and re.fullmatch(r"\d{1,2}", tok) and int(tok) <= 25:
                rest = line2[m.end():].lstrip()
                if not rest or rest[0].isupper() or rest[0].isdigit() or rest[0] in "|":
                    continue
            out.append((tok, line))
    return out

def parse(tok):
    t = tok.replace("−", "-").replace("$", "").replace(",", "").replace("+", "")
    t = re.sub(r"\s?(%|×|M|GW|MW|TWh)$", "", t).strip()
    try:
        v = abs(float(t))
    except ValueError:
        return None, 0
    dp = len(t.split(".")[1]) if "." in t else 0
    return v, dp

claims = list(csv.DictReader(open(REPO + r"\interview-prep\work\reviews\snapshot_v2_1035\claims.csv", encoding="utf-8")))
cnums, ctimes = [], set()
for c in claims:
    blob = c["exact_text"] + " ; " + c["value"].replace(";", " ; ")
    for t in TIME.findall(blob): ctimes.add(t)
    for tok, _ in tokens(blob.replace(";", " ")):
        v, _ = parse(tok)
        if v is not None: cnums.append((v, c["id"]))
def covered(tok):
    if TIME.fullmatch(tok):
        return [c for c in ctimes if c.lstrip("0") == tok.lstrip("0") or c == tok][:1]
    v, dp = parse(tok)
    if v is None: return ["unparsed"]
    tol = 0.5 * 10 ** (-dp) + 1e-9
    return sorted({cid for cv, cid in cnums if abs(cv - v) <= tol})

docs = {"deck_adopted_slides": "deck_adopted_slides.txt", "deck_adopted_notes": "deck_adopted_notes.txt", "deck_adopted_pdf": "deck_adopted_pdf.txt",
        "deck_public_slides": "deck_public_slides.txt", "deck_public_notes": "deck_public_notes.txt", "deck_public_pdf": "deck_public_pdf.txt",
        "brief_pdf": "brief_pdf.txt", "brief_html": "brief_html.txt", "qsheet_pdf": "qsheet_pdf.txt", "qsheet_html": "qsheet_html.txt"}
rows = []
for name, fn in docs.items():
    text = open(os.path.join(TXT, fn), encoding="utf-8").read()
    if name.endswith("_html"):
        text = text.split("===== ATTRIBUTES")[0] + "\n" + text.split("===== ATTRIBUTES")[-1] if "===== ATTRIBUTES" in text else text
    for tok, line in tokens(text):
        v, dp = parse(tok) if not TIME.fullmatch(tok) else (None, 0)
        if v is not None and dp == 0 and 2013 <= v <= 2027 and re.fullmatch(r"\d{4}", tok.strip("+−-")):
            continue  # year label
        if name.startswith("deck") and re.fullmatch(r"\d{1,2}", tok) and line.strip() == tok:
            continue  # slide number line
        cov = covered(tok)
        rows.append(dict(doc=name, token=tok, value=v, covered_by=";".join(cov[:6]), context=re.sub(r"\s+", " ", line.strip())[:160]))
with open(os.path.join(WORK, "coverage_tokens.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
unc = [r for r in rows if not r["covered_by"]]
print("tokens:", len(rows), "| uncovered:", len(unc))
seen = {}
for r in unc:
    key = (r["token"], r["context"][:70])
    seen.setdefault(key, set()).add(r["doc"])
for (tok, ctx), ds in sorted(seen.items(), key=lambda kv: (sorted(kv[1])[0], kv[0][0])):
    print(f"{tok:>10} | {','.join(sorted(d.replace('deck_', 'd_').replace('_slides', '_s').replace('_notes', '_n') for d in ds))} | {ctx}")
