"""Extract text from a PDF (PyMuPDF) and print pages/lines matching a regex, with context.

Usage: python -I r_pdf_grep.py <file.pdf> <regex> [context_lines] [--pages]
  --pages  : print only page numbers + match counts
Writes nothing; reads the PDF only.
"""
import re
import sys

import fitz  # PyMuPDF


def main():
    # -I ignores PYTHONIOENCODING; the Windows console is cp1252, so force UTF-8 output.
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    path, pattern = sys.argv[1], sys.argv[2]
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 2
    pages_only = "--pages" in sys.argv
    rx = re.compile(pattern, re.I)
    doc = fitz.open(path)
    print(f"# {path}: {doc.page_count} pages")
    for i, page in enumerate(doc, start=1):
        lines = page.get_text("text").splitlines()
        hits = [j for j, ln in enumerate(lines) if rx.search(ln)]
        if not hits:
            continue
        if pages_only:
            print(f"p{i}: {len(hits)} hits")
            continue
        shown = set()
        for j in hits:
            lo, hi = max(0, j - ctx), min(len(lines), j + ctx + 1)
            if any(k in shown for k in range(lo, hi)):
                rng = [k for k in range(lo, hi) if k not in shown]
            else:
                rng = list(range(lo, hi))
                print(f"--- p{i} l{j}")
            for k in rng:
                shown.add(k)
                print(lines[k])


if __name__ == "__main__":
    main()
