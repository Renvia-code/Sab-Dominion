"""Print regex hits (with context) from a saved PDF, page-numbered (1-based PDF pages).

Usage: python -I r_final_pdf_grep.py <pdf> <regex> [context_chars]
Read-only; prints to the console only.
"""
import re
import sys

from pypdf import PdfReader


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    pdf, pattern = sys.argv[1], sys.argv[2]
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 250
    rx = re.compile(pattern, re.I)
    reader = PdfReader(pdf)
    for i, page in enumerate(reader.pages, start=1):
        text = re.sub(r"\s+", " ", page.extract_text() or "")
        for m in rx.finditer(text):
            lo, hi = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
            print(f"[p{i}] ...{text[lo:hi]}...\n")


if __name__ == "__main__":
    main()
