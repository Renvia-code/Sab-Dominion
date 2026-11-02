"""Final-pack audit, follow-ups: management wording in the Q3 transcript (vs the site's own summary), any second
source for $1.06, the AR's 3.6M context and nuclear fleet, and cross-document consistency of dates and counts."""
import sys, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
import fitz
RV = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
B = RV + r"\v1_sources"
def norm(t):
    t = html.unescape(t)
    for a, b in [("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u2013", "-"), ("\u2014", "-"), ("\xa0", " ")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)
def html_text(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return norm(re.sub(r"<[^>]+>", " ", raw))
def all_hits(t, pat, w=140, n=6):
    out = [t[max(0, m.start() - w):m.end() + w] for m in re.finditer(pat, t)]
    print(f"\n[{pat}] x{len(out)}"); [print("   ...", o, "...") for o in out[:n]]
# 1 transcript: where the summary ('TAKEAWAYS') ends and the call begins; management's own words
t = html_text(os.path.join(B, "fool_q3_2026", "page.html"))
for k in ["TAKEAWAYS", "SUMMARY", "RISKS", "Full Conference Call Transcript", "Operator"]:
    print(f"position of {k!r}:", t.find(k))
all_hits(t, r"1\.28")
all_hits(t, r"1\.06|\$1\.06|106")
all_hits(t, r"11\.65")
all_hits(t, r"end of 2027")
all_hits(t, r"federal approvals")
all_hits(t, r"top half")
# 2 annual report: '1.06' anywhere, p.2 context of 3.6 million, the nuclear fleet
ar = {i: norm(p.get_text("text")) for i, p in enumerate(fitz.open(os.path.join(B, "annual_report_2025", "ar2025.pdf")), 1)}
print("\nAR pages with '$1.06':", [i for i, x in ar.items() if "$1.06" in x])
all_hits(ar[2], r"3\.6 million", n=2)
for i in (4, 15, 16):
    all_hits(ar[i], r"(?i)nuclear (power )?(stations|facilities|units|fleet)", n=4)
all_hits(" ".join(ar[i] for i in range(14, 19)), r"(?i)(Millstone|North Anna|Surry|V\.C\. Summer)[^.]{0,200}", w=60, n=8)
# 3 the final pack: dates and counts that could disagree across documents
TX = RV + r"\v1_text_final"
docs = {f: open(os.path.join(TX, f), encoding="utf-8").read() for f in os.listdir(TX) if f.endswith(".txt")}
for pat in [r"early 2027", r"end-2027|end of 2027", r"mid-January", r"Jan(uary)?\.? 11", r"2,700|2,900|2,500", r"(?i)underground", r"4,000",
            r"Sep(tember)?\.? 3", r"H2 2027|second half of 2027", r"3\.6 ?M|3\.6 million", r"2\.8 ?M|2\.8 million", r"2\.7 ?M|2\.7 million", r"2\.68 ?M",
            r"(?i)quarter of", r"28%", r"19 (sites|locations)", r"1% energy", r"(?i)four nuclear|4 nuclear", r"65 ?°F"]:
    hits = {f: len(re.findall(pat, x)) for f, x in docs.items() if re.search(pat, x)}
    print(f"\npack [{pat}]:", hits or "none")
    for f, x in docs.items():
        if f.endswith("_pdf.txt"):
            for m in list(re.finditer(pat, x))[:4]:
                print(f"   {f}: ...{re.sub(chr(10), ' ', x[max(0, m.start() - 90):m.end() + 90])}...")
