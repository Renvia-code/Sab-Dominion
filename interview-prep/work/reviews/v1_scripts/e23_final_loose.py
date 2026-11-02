"""Final-pack audit, loose ends: the AR's '$1.06' context and any 2026 guidance range; the Loudoun Now date line;
the RD916 sentence across its page break; the transcript's own words on the guidance range."""
import sys, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
import fitz
B = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews\v1_sources"
def norm(t):
    t = html.unescape(t)
    for a, b in [("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u2013", "-"), ("\u2014", "-"), ("\xa0", " ")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
def hits(t, pat, w=160, n=4, label=""):
    out = [t[max(0, m.start() - w):m.end() + w] for m in re.finditer(pat, t)]
    print(f"\n{label} [{pat}] x{len(out)}"); [print("   ...", o, "...") for o in out[:n]]
ar = {i: norm(p.get_text("text")) for i, p in enumerate(fitz.open(os.path.join(B, "annual_report_2025", "ar2025.pdf")), 1)}
hits(ar[157], r"\$1\.06", label="AR p.157")
hits(" ".join(ar.values()), r"3\.45|3\.69", label="AR all pages")
raw = open(os.path.join(B, "final_loudounnow_rates", "page.html"), encoding="utf-8", errors="replace").read()
m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', raw) or re.search(r'article:published_time"\s+content="([^"]+)"', raw)
print("\nLoudoun Now datePublished:", m.group(1) if m else None)
lt = norm(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)))
hits(lt, r"final order|Nov\. \d+|November \d+, 2025", n=3, label="Loudoun Now")
rd = {i: norm(p.get_text("text")) for i, p in enumerate(fitz.open(os.path.join(B, "final_va_rd916_2025", "rd916.pdf")), 1)}
hits(rd[10], r"12 other states", w=200, label="RD916 p.10")
print("RD916 p.11 head:", rd[11][:260])
print("RD916 p.1 head:", rd[1][:300])
t = norm(re.sub(r"<[^>]+>", " ", re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", open(os.path.join(B, "fool_q3_2026", "page.html"), encoding="utf-8", errors="replace").read())))
i = t.find("Full Conference Call Transcript")
call = t[i:]
hits(call, r"guidance range|3\.45|3\.69", n=6, label="call transcript only (after the site's summary)")
