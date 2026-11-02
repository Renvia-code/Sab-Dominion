"""Print regex hits (with context) from a saved HTML page's visible text.

Usage: python -I r_final_html_grep.py <html> <regex> [context_chars] [max_hits]
Read-only; prints to the console only (UTF-8).
"""
import html
import re
import sys


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    path, pattern = sys.argv[1], sys.argv[2]
    ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 250
    max_hits = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    raw = open(path, encoding="utf-8", errors="replace").read()
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    text = re.sub(r"\s+", " ", text)
    seen = 0
    last_end = -1
    for m in re.finditer(pattern, text, flags=re.I):
        if m.start() < last_end:
            continue
        lo, hi = max(0, m.start() - ctx), min(len(text), m.end() + ctx)
        print(f"...{text[lo:hi]}...\n")
        last_end = hi
        seen += 1
        if seen >= max_hits:
            break
    if not seen:
        print("(no hits)")


if __name__ == "__main__":
    main()
