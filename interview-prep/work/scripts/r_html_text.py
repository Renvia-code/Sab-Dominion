"""Convert a downloaded HTML page to plain text lines and print the lines matching a regex.

Usage: python -I r_html_text.py <page.html> [regex] [--min N] [--all] [--max M]
  regex  : case-insensitive pattern; lines matching it are printed (default: all lines)
  --min N: drop lines shorter than N characters (default 30)
  --all  : print all lines (ignore regex)
  --max M: print at most M lines (default 200)
Reads the file only; never executes anything from it.
"""
import html
import re
import sys


def to_lines(raw):
    raw = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<br\s*/?>|</p>|</li>|</h\d>|</tr>|</div>|</section>|</article>", "\n", raw, flags=re.I)
    raw = re.sub(r"</t[dh]>", " | ", raw, flags=re.I)
    raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    out = []
    for ln in raw.splitlines():
        ln = re.sub(r"\s+", " ", ln).strip()
        if ln:
            out.append(ln)
    return out


def main():
    args = sys.argv[1:]
    path = args[0]
    minlen, maxn, show_all, pattern = 30, 200, False, None
    i = 1
    while i < len(args):
        a = args[i]
        if a == "--min":
            minlen = int(args[i + 1]); i += 2; continue
        if a == "--max":
            maxn = int(args[i + 1]); i += 2; continue
        if a == "--all":
            show_all = True; i += 1; continue
        pattern = a; i += 1
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = [ln for ln in to_lines(fh.read()) if len(ln) >= minlen]
    rx = re.compile(pattern, re.I) if pattern and not show_all else None
    shown = 0
    for ln in lines:
        if rx is None or rx.search(ln):
            print("-", ln[:900])
            shown += 1
            if shown >= maxn:
                break
    print(f"# {shown} lines shown of {len(lines)}")


if __name__ == "__main__":
    main()
