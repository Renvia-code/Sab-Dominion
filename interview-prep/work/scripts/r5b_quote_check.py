"""Local-only check: does a markdown file reuse long word sequences from a PDF (paraphrase, never quote)?

Prints shared n-grams to stdout only; writes nothing. Usage: r5b_quote_check.py <pdf> <md> [n=6]
"""
import re
import sys

import pymupdf

pdf, md = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 6


def words(text):
    return re.findall(r"[a-z0-9%$+.]+", text.lower().replace("’", "'"))


src = words(" ".join(page.get_text() for page in pymupdf.open(pdf)))
doc = words(open(md, encoding="utf-8").read())
grams = {tuple(src[i:i + n]) for i in range(len(src) - n + 1)}
hits = sorted({" ".join(doc[i:i + n]) for i in range(len(doc) - n + 1) if tuple(doc[i:i + n]) in grams})
print(f"{len(hits)} shared {n}-word sequences")
for h in hits:
    print(" -", h)
