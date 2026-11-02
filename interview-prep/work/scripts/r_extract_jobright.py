"""Extract job-posting text from a downloaded Jobright page (Next.js).

Usage: python -I r_extract_jobright.py <page.html>
Looks for the __NEXT_DATA__ JSON blob and prints string fields that look like posting text
(title, company, location, dates, summary, responsibilities, qualifications, original URL).
Drops any field whose key mentions salary/pay/compensation. Reads the file only.
"""
import json
import re
import sys

SKIP = re.compile(r"salary|pay|compens|wage", re.I)
KEEP = re.compile(r"title|company|location|date|time|summary|respons|qualif|requir|skill|"
                  r"desc|core|prefer|benefit|url|link|apply|origin|source|level|type|work|"
                  r"education|visa|sponsor|status|closed|expire|publish", re.I)


def walk(obj, path, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            walk(v, f"{path}.{k}", out)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]", out)
    elif isinstance(obj, (str, int, float, bool)) and obj not in ("", None):
        key = path.rsplit(".", 1)[-1]
        if SKIP.search(path):
            return
        if KEEP.search(key) or (isinstance(obj, str) and len(obj) > 60):
            out.append((path, obj))


def main():
    path = sys.argv[1]
    with open(path, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', text, flags=re.S)
    if not m:
        print("no __NEXT_DATA__ found; falling back to JSON-LD")
        for blob in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S):
            print(blob[:6000])
        return
    data = json.loads(m.group(1))
    out = []
    walk(data, "$", out)
    seen = set()
    for p, v in out:
        if isinstance(v, str):
            v = re.sub(r"\s+", " ", v).strip()
        sig = (p.rsplit(".", 1)[-1], str(v)[:200])
        if sig in seen:
            continue
        seen.add(sig)
        print(f"{p} :: {v}")


if __name__ == "__main__":
    main()
