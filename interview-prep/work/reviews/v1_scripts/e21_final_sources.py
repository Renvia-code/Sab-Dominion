"""Final-pack audit: search the opened sources (untrusted data) for each value the ten C-F rows print.
Short snippets only. A pattern is also tried with all whitespace removed (the AR text layer splits words)."""
import sys, os, re, json, html, glob
sys.stdout.reconfigure(encoding='utf-8')
import fitz
B = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews\v1_sources"

def norm(t):
    t = html.unescape(t)
    for a, b in [("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'), ("\u2013", "-"), ("\u2014", "-"), ("\xa0", " "), ("\u00ad", ""), ("\u2010", "-"), ("\u2011", "-")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t)

def html_text(p):
    raw = open(p, encoding="utf-8", errors="replace").read()
    raw = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw)
    return norm(re.sub(r"<[^>]+>", " ", raw))

def pdf_pages(p):
    return {i: norm(pg.get_text("text")) for i, pg in enumerate(fitz.open(p), 1)}

def find(text, pats, label, w=120):
    print(f"\n=== {label} (chars {len(text)})")
    flat = re.sub(r"\s+", "", text).lower()
    for p in pats:
        i = text.lower().find(norm(p).lower())
        if i >= 0:
            print(f"  FOUND [{p}] ...{text[max(0, i - w):i + len(p) + w]}...")
            continue
        j = flat.find(re.sub(r"\s+", "", norm(p)).lower())
        print(f"  {'FOUND (despaced)' if j >= 0 else 'NOT FOUND'} [{p}]" + (f" ...{flat[max(0, j - 90):j + len(p) + 90]}..." if j >= 0 else ""))

def pages_with(pages, pat):
    return [i for i, t in pages.items() if pat.lower() in t.lower() or re.sub(r"\s+", "", pat).lower() in re.sub(r"\s+", "", t).lower()]

# A. Annual report 2025 (V1 download of the cited q4cdn URL)
ar = pdf_pages(os.path.join(B, "annual_report_2025", "ar2025.pdf"))
print("AR pages:", len(ar))
for pat in ["3.6 million", "500,000", "2.8 million", "Coastal Virginia Offshore Wind", "2.6 GW", "Data centers represent", "4,000 miles",
            "customer accounts", "$566 million", "9.80%", "50 basis points", "Millstone", "V.C. Summer", "North Anna"]:
    print(f"  pages with [{pat}]:", pages_with(ar, pat)[:12])
find(ar[3], ["Coastal Virginia Offshore Wind (CVOW)"], "AR PDF p.3")
find(ar[4], ["2.6 GW", "660,000 homes", "expected in early 2027", "176 monopile"], "AR PDF p.4")
find(ar[19], ["approximately 2.8 million", "customers in Virginia and North Carolina"], "AR PDF p.19")
find(ar[20], ["Data centers represent 28% and 26% of Virginia Power's electricity sales", "years ended December 31, 2025 and 2024", "PJM DOM Zone"], "AR PDF p.20")
find(ar[23], ["approximately 4,000 miles", "completed by 2029", "$387 million", "eight phases"], "AR PDF p.23")
find(ar[65], ["Average electric distribution customer accounts (thousands)", "2,809", "2,782"], "AR PDF p.65")
find(ar[130], ["$566 million effective January 2026", "$210 million effective January 2027", "ROE of 9.80%", "November 2025"], "AR PDF p.130")
# B. Q3 2026 call transcript (V1 download, third party)
t = html_text(os.path.join(B, "fool_q3_2026", "page.html"))
find(t, ["rebuttal testimony due November 2", "Evidentiary hearings begin on November 17", "final order is due by January 11", "January 11, 2027",
         "approximately 85% complete", "$11.65 billion", "end of 2027", "54 gigawatts", "12 gigawatts", "6 gigawatts", "13%",
         "$1.28", "$1.06", "3.45", "3.69", "top half", "PUR-", "case number", "nuclear"], "Q3 2026 call transcript (fool.com)")
# C. NextEra release (V1 download)
find(html_text(os.path.join(B, "nextera_release", "page.html")), ["Nuclear Regulatory Commission", "nuclear", "3.6 million", "500,000"], "NextEra release 18 May 2026")
# D. Grid Resiliency page (V1 download)
find(html_text(os.path.join(B, "dominion_grid_resiliency", "page.html")),
     ["should address 19 locations by the end of the program", "19 locations", "Our goal is to provide a system-wide average of 1% energy savings",
      "Voltage islands are when we have a substation with only a single-transformer", "adding a second transformer"], "Dominion Grid Resiliency page")
# E. Dominion release 8 June 2026 (V1 download)
find(html_text(os.path.join(B, "dominion_release_20260608", "page.html")),
     ["buried about 2,900 miles of outage-prone power lines in Virginia", "about 300 miles in the last year", "Strategic Underground",
      "3.6 million homes and businesses", "500,000 customers in South Carolina", "06/08/2026"], "Dominion IR release 8 June 2026")
# F. Federal Register 21 Oct 2026 (govinfo PDF)
fr = pdf_pages(os.path.join(B, "final_govinfo_fr_20261021", "fr.pdf"))
frt = " ".join(fr.values())
find(frt, ["EC26-131", "NextEra Energy", "deficiency letter", "Section 203", "Filed Date: 10/15/26", "20261015-5185"], "Federal Register 2026-10-21 (govinfo)")
print("  FR pages:", len(fr), "| EC26-131 on pages:", pages_with(fr, "EC26-131"))
# G. Loudoun Now
find(html_text(os.path.join(B, "final_loudounnow_rates", "page.html")),
     ["$11.24", "$2.36", "9.7% to 9.8%", "1,000 kilowatt", "typical", "residential", "base rate", "$566 million", "$210 million"], "Loudoun Now")
# H. CPC
find(html_text(os.path.join(B, "final_cpc_degree_days", "page.html")), ["Degree Days", "population", "2010 Census", "weighted"], "CPC degree days index")
find(html_text(os.path.join(B, "final_cpc_ddayexp", "page.html")), ["65", "65°F", "65 F", "base", "population", "weighted", "heating degree", "cooling degree"], "CPC ddayexp")
# I. Virginia report RD916 (2025)
rd = pdf_pages(os.path.join(B, "final_va_rd916_2025", "rd916.pdf"))
find(" ".join(rd.values()), ["12 other states and the District of Columbia", "regional transmission organization", "maintain reliability of the transmission grid"], "VA RD916 (2025)")
print("  RD916 pages:", len(rd), "| '12 other states' on pages:", pages_with(rd, "12 other states"))
# J. EIA-861 instructions
ei = pdf_pages(os.path.join(B, "final_eia861_instructions", "instructions.pdf"))
find(" ".join(ei.values()), ["Momentary outages are not included in determining SAIDI and SAIFI", "momentary", "five minutes", "5 minutes"], "EIA-861 instructions")
print("  EIA pages:", len(ei), "| 'Momentary outages are not included' on pages:", pages_with(ei, "Momentary outages are not included"),
      "| 'five minutes' on:", pages_with(ei, "five minutes"), "| '5 minutes' on:", pages_with(ei, "5 minutes"))
# K. IEEE PES Boston slides
ie = pdf_pages(os.path.join(B, "final_ieee_pes_boston_1366", "slides.pdf"))
find(" ".join(ie.values()), ["MAIFI", "Momentary Average Interruption Frequency Index", "Similar to SAIFI", "more than five minutes", "five minutes", "CEMI"], "IEEE PES Boston slides")
print("  slides:", len(ie), "| MAIFI on:", pages_with(ie, "MAIFI"), "| 'five minutes' on:", pages_with(ie, "five minutes"), "| 'momentary' on:", pages_with(ie, "momentary"))
for i in pages_with(ie, "five minutes")[:3] + pages_with(ie, "MAIFI")[:3]:
    print(f"  slide p.{i}: {ie[i][:400]}")
# L. Crossref record of the EAGLE-I data paper
j = json.load(open(os.path.join(B, "final_crossref_10_1038_s41597-024-03095-5", "meta.json"), encoding="utf-8"))["message"]
ab = norm(re.sub(r"<[^>]+>", " ", j.get("abstract", "")))
print("\nCrossref:", j.get("title"), j.get("container-title"), (j.get("issued") or {}).get("date-parts"))
find(ab, ["Environment for Analysis of Geo-Located Energy Information", "Oak Ridge National Laboratory", "every 15 minutes", "county level"], "Crossref abstract")
# M. ORNL Constellation
find(html_text(os.path.join(B, "final_ornl_eaglei_2025", "page.html")),
     ["15-minute intervals", "15 minute", "Release Date", "February 19, 2026", "Office of Cybersecurity, Energy Security, and Emergency Response", "CESER", "public outage maps"], "ORNL Constellation EAGLE-I 2025")
# N. Any opened source with the SCC case number
hits = []
for f in glob.glob(os.path.join(B, "*", "*")):
    if f.lower().endswith((".html", ".htm")):
        if "PUR-2026-00112" in open(f, encoding="utf-8", errors="replace").read(): hits.append(f)
    elif f.lower().endswith(".pdf"):
        if any("PUR-2026-00112" in pg.get_text("text") for pg in fitz.open(f)): hits.append(f)
print("\nopened sources containing PUR-2026-00112:", [os.path.relpath(h, B) for h in hits])
