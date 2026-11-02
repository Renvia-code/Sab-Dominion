"""Final-pack audit: is each row's printed text in the final PDFs exactly (after joining PDF line breaks), and on
which pages? Also checks the quoted fragments named in each row's used_in field, and the HTML twin."""
import sys, os, re, csv
sys.stdout.reconfigure(encoding='utf-8')
RV = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
TX = RV + r"\v1_text_final"
def pages(name):
    raw = open(os.path.join(TX, name), encoding="utf-8").read()
    parts = re.split(r"===== PAGE (\d+) =====", raw)
    return {int(parts[i]): flat(parts[i + 1]) for i in range(1, len(parts), 2)}
def flat(t):
    t = re.sub(r"(\w)-\n(\w)", r"\1-\2", t)          # 'population-\nweighted' -> 'population-weighted'
    t = re.sub(r"\s+", " ", t.replace("\u00a0", " "))
    return t.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")
def norm(s):
    return re.sub(r"\s+", " ", s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2019", "'")).strip()
docs = {"brief_pdf": pages("brief_pdf.txt"), "qsheet_pdf": pages("qsheet_pdf.txt"),
        "deck_adopted_pdf": pages("deck_adopted_pdf.txt"), "deck_public_pdf": pages("deck_public_pdf.txt")}
html = {k: flat(open(os.path.join(TX, k + ".txt"), encoding="utf-8").read()) for k in ["brief_html", "qsheet_html"]}
IDS = "C-F-01 C-F-02 C-F-03 C-F-04 C-F-06 C-F-07 C-F-08 C-F-09 C-F-10 C-F-12".split()
rows = {r["id"]: r for r in csv.DictReader(open(RV + r"\snapshot_final_audit\claims.csv", encoding="utf-8")) if r["id"] in IDS}
def where(s):
    s = norm(s); out = []
    for d, pg in docs.items():
        for p, t in pg.items():
            if s.lower() in t.lower(): out.append(f"{d} p.{p}")
    return out
for i in IDS:
    r = rows[i]
    print(f"\n{i}: exact_text in PDFs -> {where(r['exact_text']) or 'NOT FOUND'} | in HTML -> {[k for k, t in html.items() if norm(r['exact_text']).lower() in t.lower()]}")
    for frag in re.findall(r"'([^']{4,})'", r["used_in"]):
        print(f"   used_in fragment '{frag[:90]}': {where(frag) or 'NOT FOUND'}")
