"""v3 re-sourced facts: search the downloaded pages (untrusted data) for the cited quotes; short snippets only.
Also report whether the SEC 403 pages are block pages, and whether producer-saved copies exist (secondary only)."""
import sys, os, re, html, glob
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
BASE = REPO + r"\interview-prep\work\reviews\v1_sources"
def text(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    t = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    t = t.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\xa0", " ")
    return re.sub(r"\s+", " ", t)
def find(t, pats, label, w=120):
    print(f"\n=== {label} ({len(t)} chars)")
    for p in pats:
        i = t.lower().find(p.lower())
        print(f"  {'FOUND' if i >= 0 else 'NOT FOUND'} [{p}]" + (f" ...{t[max(0, i - w):i + len(p) + w]}..." if i >= 0 else ""))
for d in ["sec_8k_dominion_20260903", "sec_8k_nextera_20260903"]:
    t = text(os.path.join(BASE, d, "page.htm"))
    print(f"\n{d}: block page text: {t[:300]}")
find(text(os.path.join(BASE, "dominion_release_20260608", "page.html")),
     ["06/08/2026", "June 8, 2026", "RICHMOND, Va.", "Mainfeeder Hardening Program", "replaced more than 8,000 older utility poles",
      "hardened over 350 miles of power lines in Virginia", "reduced average annual outage time by 44% for customers in these areas"],
     "Dominion release (investors.dominionenergy.com)")
find(text(os.path.join(BASE, "dominion_tree_trimming_faq", "page.html")),
     ["cycles typically ranging from four to five years", "Nearly all of our neighborhood power lines are cleared on a four year cycle"],
     "Dominion tree-trimming FAQ")
saved = glob.glob(REPO + r"\interview-prep\work\research_raw\v1_followups\*")
print("\nproducer-saved files in work/research_raw/v1_followups:", [os.path.basename(s) + f" ({os.path.getsize(s)} B)" for s in saved])
