"""Scan the shipped Power BI deliverables for things that must not be there:
this machine's paths, tool names, the old Snowflake trial, the old author's path, stale wording
and the off-convention default blue. Usage: python -I scan_ship.py <file or folder> ..."""
import re
import sys
import zipfile
from pathlib import Path

BAD = re.compile(r"(users\\oni|users/oni|renvia|\\projects\\|claude|anthropic|agent|sakethbollina|vosrmgo|"
                 r"snowflake_learning|centres|comparision|#118dff)", re.I)


def text_of(name, raw):
    if raw[:2] == b"\xff\xfe" or (len(raw) > 1 and raw[1:2] == b"\x00"):
        return raw.decode("utf-16-le", "ignore")
    return raw.decode("utf-8", "ignore")


def scan_bytes(label, raw):
    hits = sorted({m.group(0) for m in BAD.finditer(text_of(label, raw))})
    if hits:
        print(f"HIT {label}: {hits}")
    return len(hits)


total = 0
for arg in sys.argv[1:]:
    p = Path(arg)
    files = [p] if p.is_file() else [q for q in p.rglob("*") if q.is_file()]
    for f in files:
        if f.suffix.lower() in (".pbit", ".pbix", ".zip"):
            with zipfile.ZipFile(f) as z:
                for n in z.namelist():
                    total += scan_bytes(f"{f.name}!{n}", z.read(n))
        elif f.suffix.lower() in (".csv", ".dax", ".pq", ".json", ".md", ".txt", ".html"):
            total += scan_bytes(str(f), f.read_bytes())
print("hits:", total)
