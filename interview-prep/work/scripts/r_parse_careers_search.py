"""Parse Dominion careers (SuccessFactors RMK) search-result HTML files.

Usage: python -I r_parse_careers_search.py <file1.html> [<file2.html> ...]
Prints one line per job: title | location | date | href. Reads files only; executes nothing.
"""
import re
import sys
import html


def parse(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    # total results line, e.g. "Results 1 – 25 of 112"
    total = re.search(r"Results\s*<b>\s*([\d,]+)\s*</b>\s*&ndash;\s*<b>\s*([\d,]+)\s*</b>\s*of\s*<b>\s*([\d,]+)\s*</b>", text)
    if not total:
        total = re.search(r"of\s*<b>([\d,]+)</b>", text)
    rows = []
    # Each result row: <tr class="data-row"> ... </tr>
    for row in re.findall(r'<tr class="data-row[^"]*">(.*?)</tr>', text, flags=re.S):
        t = re.search(r'<a[^>]*class="jobTitle-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', row, flags=re.S)
        loc = re.search(r'<span class="jobLocation">(.*?)</span>', row, flags=re.S)
        date = re.search(r'<span class="jobDate">(.*?)</span>', row, flags=re.S)
        if t:
            rows.append((
                html.unescape(re.sub(r"\s+", " ", t.group(2)).strip()),
                html.unescape(re.sub(r"<[^>]+>", "", re.sub(r"\s+", " ", loc.group(1))).strip()) if loc else "",
                html.unescape(re.sub(r"\s+", " ", date.group(1)).strip()) if date else "",
                t.group(1),
            ))
    return total, rows


def main():
    for path in sys.argv[1:]:
        total, rows = parse(path)
        tot = total.group(0) if total else "(no total found)"
        print(f"=== {path} :: {re.sub('<[^>]+>', '', tot)} :: {len(rows)} rows parsed")
        seen = set()
        for r in rows:
            if r[3] in seen:
                continue
            seen.add(r[3])
            print(" | ".join(r))


if __name__ == "__main__":
    main()
