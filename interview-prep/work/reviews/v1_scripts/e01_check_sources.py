"""Search the downloaded sources (untrusted data) for the cited quotes; print short snippets only.
Paths are passed in by folder name under v1_sources; nothing is executed from those folders."""
import sys, os, re, json, html
sys.stdout.reconfigure(encoding='utf-8')
import fitz
BASE = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews\v1_sources"

def norm(t):
    t = html.unescape(t)
    t = t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-").replace("\xa0", " ")
    t = t.replace("\\u0026", "&").replace("\\n", " ").replace('\\"', '"')
    return re.sub(r"\s+", " ", t)

def html_text(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(style)[^>]*>.*?</\1>", " ", raw)
    return norm(re.sub(r"<[^>]+>", " ", raw))

def find(text, pats, label, width=110):
    print(f"\n=== {label} (chars {len(text)})")
    for p in pats:
        idx = [m.start() for m in re.finditer(re.escape(norm(p)), text, flags=re.I)]
        if idx:
            i = idx[0]; print(f"  FOUND x{len(idx)} [{p}] ...{text[max(0, i - width):i + len(p) + width]}...")
        else:
            print(f"  NOT FOUND [{p}]")

# 1 Annual report PDF
doc = fitz.open(os.path.join(BASE, "annual_report_2025", "ar2025.pdf"))
print("annual report pages:", len(doc))
pg = {i: norm(doc[i - 1].get_text("text")) for i in (7, 20, 28, 29)}
find(pg[20], ["133 minutes for the three-year average ending 2025", "previous three-year average of 130 minutes",
              "This increase is primarily due to increased storm activity."], "AR PDF p.20")
m = re.findall(r"(?:^| )(\d{1,3}) ?$", doc[19].get_text("text").strip()[-40:])
print("  PDF p.20 tail (printed folio?):", repr(doc[19].get_text("text").strip()[-60:]))
find(pg[7], ["11 data centers", "744 MW"], "AR PDF p.7")
find(pg[28] + " " + pg[29], ["50 basis points", "factors that may include reliability", "2025 Biennial Review"], "AR PDF p.28-29")
for i in (28, 29):
    print(f"  PDF p.{i} tail:", repr(doc[i - 1].get_text("text").strip()[-50:]))
# 2 Job posting (aggregator)
t = html_text(os.path.join(BASE, "jobright_posting", "posting.html"))
find(t, ["Associate Business Intelligence Analyst", "Business Intelligence Analyst", "Richmond", "Grid Resiliency",
         "Power BI, SQL, Excel, Snowflake, Power Apps, SharePoint", "reliability metrics", "Hybrid 3-2",
         "three days in the office, two days of teleworking", "Travel Up to 25%", "cannot transfer or sponsor a work visa",
         "job has closed", "closed"], "jobright posting")
# 3 Dominion grid resiliency page
t = html_text(os.path.join(BASE, "dominion_grid_resiliency", "page.html"))
find(t, ["Grid Resiliency and its programs are a part of", "Mainfeeder Hardening", "Voltage Island", "Voltage Optimization",
         "Intelligent Grid Devices", "Underground conversions are not within the scope", "As of November 30, 2023",
         "32% reduction in outage minutes", "at least 12 months", "at least 500 customers", "more than 2 minutes",
         "over the last 5 years"], "Dominion Grid Resiliency page")
# 4 NextEra release
t = html_text(os.path.join(BASE, "nextera_release", "page.html"))
find(t, ["May 18, 2026", "Hart-Scott-Rodino", "Section 203", "Nuclear Regulatory Commission", "Virginia State Corporation Commission",
         "North Carolina Utilities Commission", "Public Service Commission of South Carolina"], "NextEra release")
# 5 Fool transcript
t = html_text(os.path.join(BASE, "fool_q3_2026", "page.html"))
find(t, ["final order is due by January 11", "second half of 2027", "54 gigawatts", "shareholder", "December 8", "February 23"], "Fool Q3 2026 transcript")
# 6 WTVR
t = html_text(os.path.join(BASE, "wtvr_merger", "page.html"))
find(t, ["locally led, separately regulated and fully accountable to the State Corporation Commission", "1,000 new direct jobs"], "WTVR")
# 7 Crossref
for d in sorted(os.listdir(BASE)):
    if d.startswith("crossref_"):
        j = json.load(open(os.path.join(BASE, d, "meta.json"), encoding="utf-8"))["message"]
        au = ", ".join(a.get("family", "?") for a in j.get("author", []))
        yr = (j.get("published-print") or j.get("published-online") or j.get("issued"))["date-parts"][0]
        ab = norm(re.sub(r"<[^>]+>", " ", j.get("abstract", "")))
        print(f"\n{d}: {au} | {yr} | {j.get('container-title')} {j.get('volume')}({j.get('issue')}) {j.get('page')} | {j.get('title')}")
        if ab: print("   abstract:", ab[:600])
