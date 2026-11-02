"""Layout test for the question sheet (B0): 22 Q&As at 8.5 pt on one US Letter sheet, two sides.

Answers are DUMMY text of realistic length (cue format: 45-62 words; STAR: four 12-16 word
lines), drawn from a domain word list so word lengths match the real sheet. Nothing here is
content for the candidate. Output: interview-prep/work/qsheet/qsheet_layout_test.{html,pdf} and
PNG proofs in interview-prep/work/proofs/qsheet_test/.

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\qsheet\\qsheet_layout_test.py
"""
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import pipeline  # noqa: E402

WORDS = ("reconciled the three-year SAIDI to the annual report so every number had a source and a test "
         "Snowflake marts with RAW STG MART layers and documented business definitions for each measure "
         "Power BI model with a disconnected year slicer and customer-weighted measures in DAX "
         "worked with operations and IT to agree requirements then validated the results with them "
         "frequency rose while restoration time stayed close to the peer median in public data "
         "storm county-days explain part of the swing but correlation is not cause with ten points").split()

GROUPS = [
    ("Opening", 3, "cue"),
    ("Behavioural (STAR)", 5, "star"),
    ("Technical BI: SQL, DAX, modelling, Power BI, Snowflake", 6, "cue"),
    ("Utility domain", 4, "cue"),
    ("Role and Dominion", 4, "cue"),
]
QUESTIONS = [
    "Tell me about yourself.", "Why Dominion Energy?", "Why this role?",
    "Tell me about a time you found an error in a report before it went out.",
    "Describe a time you had to explain a technical result to a non-technical audience.",
    "Tell me about a deadline you nearly missed and what you did.",
    "Give an example of working with a difficult stakeholder.",
    "Tell me about a root-cause analysis you led.",
    "Walk me through a SQL query with window functions you wrote recently.",
    "Explain filter context and CALCULATE in DAX.",
    "How do you design a star schema for a reporting model?",
    "A Power BI report is slow. Where do you start?",
    "Import or DirectQuery: how do you choose?",
    "How do you test data quality in a Snowflake pipeline?",
    "What are SAIDI, SAIFI and CAIDI?",
    "What is a major event day, and why exclude it?",
    "SAIFI is rising. How would you investigate?",
    "How would you measure whether undergrounding worked?",
    "How do you think about joining a company in a pending merger?",
    "Where do you see yourself in this team in a year?",
    "What would you do in your first 90 days?",
    "What questions do you have about our data and reporting?",
]


def dummy(n, rng):
    start = rng.randrange(0, len(WORDS) - n)
    return " ".join(WORDS[start:start + n])


def build_html(body_pt=8.5):
    rng = random.Random(7)
    css = (HERE / "qsheet.css").read_text(encoding="utf-8").replace("--body: 8.5pt", f"--body: {body_pt}pt")
    parts = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>Q-sheet layout test</title>"
             f"<style>{css}</style></head><body>",
             "<header class='sheet'><h1>Interview questions and answer cues (LAYOUT TEST, dummy answers)</h1>"
             "<span class='meta'>Dominion Energy · 3 Nov 2026</span></header>",
             "<p class='legend'>Each answer: claim → one proof from the resume → tie to Dominion. "
             "<span class='ph'>[you: …]</span> = only you can fill this in.</p><div class='cols'>"]
    qi = 0
    for name, n, kind in GROUPS:
        parts.append(f"<h2>{name}</h2>")
        for _ in range(n):
            q = QUESTIONS[qi]
            qi += 1
            parts.append(f"<div class='qa'><div class='q'><span class='n'>{qi}</span>{q}</div>")
            if kind == "star":
                parts.append("<ul class='star'>" + "".join(
                    f"<li><b>{k}</b>{dummy(rng.randint(12, 16), rng)}</li>" for k in "STAR") + "</ul>")
            else:
                parts.append(f"<p class='a'><b>{dummy(rng.randint(8, 11), rng)}.</b> "
                             f"{dummy(rng.randint(37, 51), rng)}. <span class='ph'>[you: detail]</span></p>")
            parts.append("</div>")
    parts.append("<div class='ask'><b>Five questions to ask the panel</b><ol>" +
                 "".join(f"<li>{dummy(rng.randint(14, 20), rng)}?</li>" for _ in range(5)) + "</ol></div>")
    parts.append(f"<p class='close'>Closing line: {dummy(24, rng)}.</p>")
    parts.append("</div></body></html>")
    return "".join(parts)


def main():
    out = HERE
    proofs = HERE.parent / "proofs" / "qsheet_test"
    for pt in (8.5, 9.0):
        html = out / f"qsheet_layout_test_{str(pt).replace('.', '_')}pt.html"
        html.write_text(build_html(pt), encoding="utf-8")
        pdf = pipeline.html_to_pdf(html, html.with_suffix(".pdf"))
        import pymupdf
        n = len(pymupdf.open(str(pdf)))
        print(f"{pt} pt -> {n} pages; min sizes {pipeline.pdf_min_font_size(pdf)}")
        for grey in (False, True):
            pipeline.pdf_to_pngs(pdf, proofs, dpi=100, grey=grey)


if __name__ == "__main__":
    main()
