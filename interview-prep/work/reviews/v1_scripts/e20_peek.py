"""Peek at small or blocked downloads (untrusted data): title and the first visible text, to classify blocks."""
import sys, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
BASE = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews\v1_sources"
for d in sys.argv[1:]:
    p = os.path.join(BASE, d, "page.html")
    raw = open(p, encoding="utf-8", errors="replace").read()
    title = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    body = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    t = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body))).strip()
    print(f"\n=== {d}: {len(raw)} bytes | title: {title.group(1).strip()[:120] if title else None}")
    print("   text:", t[:420])
