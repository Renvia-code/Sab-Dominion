"""Extract text from the frozen final deliverables (snapshot_final_audit) into v1_text_final/, one file per
rendering, with page markers for the PDFs (same functions as x11)."""
import sys, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
import fitz
from pptx import Presentation
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
SNAP = REPO + r"\interview-prep\work\reviews\snapshot_final_audit"
OUT = REPO + r"\interview-prep\work\reviews\v1_text_final"
os.makedirs(OUT, exist_ok=True)

def dump_pdf(path, tag):
    doc = fitz.open(path)
    open(os.path.join(OUT, f"{tag}_pdf.txt"), "w", encoding="utf-8").write(
        "\n".join(f"\n===== PAGE {i} =====\n" + p.get_text("text") for i, p in enumerate(doc, 1)))
    print(tag, "pages", len(doc))

def dump_html(path, tag):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw2 = re.sub(r"data:[a-z/+]+;base64,[A-Za-z0-9+/=]+", "DATAURI", raw)
    raw2 = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw2)
    t = re.sub(r"(?s)<!--.*?-->", " ", raw2); t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"</(p|div|li|tr|h[1-6]|section|table|td|th|text|tspan|figcaption)>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\n{2,}", "\n", "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()))
    open(os.path.join(OUT, f"{tag}_html.txt"), "w", encoding="utf-8").write(t)
    print(tag, "html chars", len(t))

def dump_pptx(path, tag):
    prs = Presentation(path); out = []
    for i, slide in enumerate(prs.slides, 1):
        out.append(f"\n===== SLIDE {i} =====")
        for shp in slide.shapes:
            if getattr(shp, "has_text_frame", False) and shp.has_text_frame: out.append(shp.text_frame.text)
            if getattr(shp, "has_table", False) and shp.has_table:
                for r in shp.table.rows: out.append("[TBL] " + " | ".join(c.text for c in r.cells))
        if slide.has_notes_slide: out.append("[NOTES] " + slide.notes_slide.notes_text_frame.text)
    open(os.path.join(OUT, f"{tag}_pptx.txt"), "w", encoding="utf-8").write("\n".join(out))
    print(tag, "slides", len(prs.slides))

dump_pdf(SNAP + r"\Dominion_interview_brief.pdf", "brief")
dump_pdf(SNAP + r"\Dominion_question_sheet.pdf", "qsheet")
dump_pdf(SNAP + r"\Dominion_reliability_deck_adopted_print_letter.pdf", "deck_adopted")
dump_pdf(SNAP + r"\Dominion_reliability_deck_public_print_letter.pdf", "deck_public")
dump_html(SNAP + r"\Dominion_interview_brief.html", "brief")
dump_html(SNAP + r"\Dominion_question_sheet.html", "qsheet")
dump_pptx(SNAP + r"\Dominion_reliability_deck_adopted.pptx", "deck_adopted")
dump_pptx(SNAP + r"\Dominion_reliability_deck_public.pptx", "deck_public")
