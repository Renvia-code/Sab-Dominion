"""Find UK spellings and day-month dates in the Power BI deliverables (O-30: US English).
Usage: python -I scan_us_english.py <file or folder> ..."""
import re
import sys
import zipfile
from pathlib import Path

UK = re.compile(r"\b(programmes?|colou?rs?\b(?<=colours)|colour|centres?|analys(e|ed|es|ing)|prioritis\w*|licence|"
                r"modell(ed|ing)|labell(ed|ing)|organis\w*|behaviour|catalogue|favour\w*|neighbour\w*|"
                r"cancell(ed|ing)|summaris\w*|recognis\w*|normalis\w*|optimis\w*|minimis\w*|maximis\w*|"
                r"utilis\w*|emphasis(e|ed|es)|standardis\w*|categoris\w*|realis\w*|travell\w*|"
                r"\d{1,2} (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*( \d{4})?)\b")


def text_of(raw):
    if raw[:2] == b"\xff\xfe" or (len(raw) > 1 and raw[1:2] == b"\x00"):
        return raw.decode("utf-16-le", "ignore")
    return raw.decode("utf-8", "ignore")


def scan(label, text):
    hits = []
    for m in UK.finditer(text):
        s = max(0, m.start() - 50)
        hits.append(f"  {m.group(0)!r}: ...{text[s:m.end() + 30]!r}")
    if hits:
        print(f"== {label}: {len(hits)}")
        for h in hits[:40]:
            print(h)
    return len(hits)


total = 0
for arg in sys.argv[1:]:
    p = Path(arg)
    files = [p] if p.is_file() else [q for q in p.rglob("*") if q.is_file()]
    for f in files:
        if f.suffix.lower() == ".pbit":
            with zipfile.ZipFile(f) as z:
                for n in z.namelist():
                    if n.startswith("Report/definition") or n == "DataModelSchema":
                        total += scan(f"{f.name}!{n}", text_of(z.read(n)))
        elif f.suffix.lower() in (".dax", ".pq", ".json", ".md", ".csv") and f.parent.name != "data":
            total += scan(str(f), f.read_text(encoding="utf-8", errors="ignore"))
print("hits:", total)
