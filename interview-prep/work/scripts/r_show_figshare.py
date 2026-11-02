"""Summarise a figshare article JSON (downloaded from api.figshare.com/v2/articles/<id>).

Usage: python -I r_show_figshare.py <article.json>
Prints title, DOI, version, dates, description (plain text) and each file's name, size and download URL.
"""
import html
import json
import re
import sys


def main():
    with open(sys.argv[1], encoding="utf-8") as fh:
        art = json.load(fh)
    print("TITLE:", art.get("title"))
    print("DOI:", art.get("doi"), "| version:", art.get("version"))
    print("published:", art.get("published_date"), "| modified:", art.get("modified_date"), "| created:", art.get("created_date"))
    lic = art.get("license") or {}
    print("LICENSE:", lic.get("name"), lic.get("url"))
    desc = html.unescape(re.sub(r"<[^>]+>", " ", art.get("description") or ""))
    print("DESCRIPTION:", re.sub(r"\s+", " ", desc).strip()[:3000])
    print("FILES:")
    total = 0
    for f in art.get("files", []):
        total += f.get("size", 0)
        print(f"  {f.get('name')} | {f.get('size'):,} bytes | md5 {f.get('computed_md5') or f.get('supplied_md5')} | {f.get('download_url')}")
    print(f"TOTAL: {total:,} bytes in {len(art.get('files', []))} files")
    for ref in art.get("references", []) or []:
        print("REF:", ref)


if __name__ == "__main__":
    main()
