"""(1) numbers that differ between the two renderings of one deliverable (HTML vs PDF; PPTX vs PDF);
(2) adopted-only markers in the public deck (slides, notes, PDF)."""
import sys, re, csv, collections
sys.stdout.reconfigure(encoding='utf-8')
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
WORK = REPO + r"\interview-prep\work\reviews\v1_work"
TXT = REPO + r"\interview-prep\work\reviews\v1_text"
rows = list(csv.DictReader(open(WORK + r"\coverage_tokens.csv", encoding="utf-8")))
def bag(*docs):
    return collections.Counter(r["token"].replace(" ", "") for r in rows if r["doc"] in docs)
for a, b in [(("brief_pdf",), ("brief_html",)), (("qsheet_pdf",), ("qsheet_html",)),
             (("deck_adopted_pdf",), ("deck_adopted_slides",)), (("deck_public_pdf",), ("deck_public_slides",))]:
    A, B = bag(*a), bag(*b)
    onlyA = {k: v for k, v in (A - B).items()}; onlyB = {k: v for k, v in (B - A).items()}
    print(f"{a[0]} vs {b[0]}: only in first {dict(sorted(onlyA.items()))} | only in second {dict(sorted(onlyB.items()))}")
markers = ["EAGLE-I", "EAGLE", "T13", "T31", "D15", "D16", "D17", "D18", "D19", "D20", "D21", "D22", "718", "791", "464", "degree",
           "12 of 12", "6,094,320", "31 tests", "25,413", "25,384", "Oct 29", "October 29", "11.9", "6,108", "332.8", "HURDAT", "DOE-417",
           "CPC", "99.5", "11,608,442", "18 tables", "11 pages", "DataFolder", "folder parameter", "0.025", "0.12", "122.3", "168.2", "+0.3",
           "-1.4", "−1.4", "2.75", "Bedford", "Isaias", "33.5", "county outage", "39–41", "+39", "33%", "Dominion-only"]
for fn in ["deck_public_slides.txt", "deck_public_notes.txt", "deck_public_pdf.txt"]:
    t = open(f"{TXT}\\{fn}", encoding="utf-8").read()
    hits = {m: t.count(m) for m in markers if m in t}
    print(fn, "adopted-only markers found:", hits or "none")
    for m in hits:
        i = t.find(m); print("   ", m, "->", re.sub(r"\s+", " ", t[max(0, i - 90):i + 90]))
