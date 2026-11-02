"""Extract all text from the frozen v3 deliverables (snapshot_v3_audit) into v1_text_v3/ (same layout as x01),
plus every embedded slide picture of the adopted deck's slide 5 (to view the screenshot the panel sees)."""
import sys, os, re, html, hashlib
sys.stdout.reconfigure(encoding='utf-8')
import fitz
from pptx import Presentation
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
SNAP = REPO + r"\interview-prep\work\reviews\snapshot_v3_audit"
OUT = REPO + r"\interview-prep\work\reviews\v1_text_v3"
os.makedirs(OUT, exist_ok=True)

def shape_texts(shape):
    out = []
    try:
        descr = shape._element.xpath('./*[1]/p:cNvPr/@descr')
    except Exception:
        descr = []
    if descr: out.append(f"[ALT] {descr[0]}")
    if shape.shape_type == 6 and hasattr(shape, "shapes"):
        for s in shape.shapes: out += shape_texts(s)
    if getattr(shape, "has_table", False) and shape.has_table:
        for r in shape.table.rows:
            out.append("[TBL] " + " | ".join(c.text.replace("\n", " / ") for c in r.cells))
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame and shape.text_frame.text.strip():
        out.append(shape.text_frame.text)
    return out

def dump_pptx(path, tag):
    prs = Presentation(path); sl, nt = [], []
    for i, slide in enumerate(prs.slides, 1):
        sl.append(f"\n===== SLIDE {i} =====")
        for shp in slide.shapes:
            sl += shape_texts(shp)
            if tag == "deck_adopted" and i == 5 and shp.shape_type == 13:
                blob = shp.image.blob
                fn = os.path.join(OUT, f"adopted_s5_picture_{hashlib.sha256(blob).hexdigest()[:12]}.{shp.image.ext}")
                open(fn, "wb").write(blob); print("saved", fn, len(blob))
        if slide.has_notes_slide:
            nt.append(f"\n===== NOTES {i} =====\n{slide.notes_slide.notes_text_frame.text}")
    open(os.path.join(OUT, f"{tag}_slides.txt"), "w", encoding="utf-8").write("\n".join(sl))
    open(os.path.join(OUT, f"{tag}_notes.txt"), "w", encoding="utf-8").write("\n".join(nt))
    print(tag, "slides", len(prs.slides))

def dump_pdf(path, tag):
    doc = fitz.open(path)
    open(os.path.join(OUT, f"{tag}_pdf.txt"), "w", encoding="utf-8").write(
        "\n".join(f"\n===== PAGE {i} =====\n" + p.get_text("text") for i, p in enumerate(doc, 1)))
    print(tag, "pages", len(doc))

def dump_html(path, tag):
    raw = open(path, encoding="utf-8", errors="replace").read()
    raw2 = re.sub(r"data:[a-z/+]+;base64,[A-Za-z0-9+/=]+", "DATAURI", raw)
    raw2 = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw2)
    attrs = re.findall(r'(?:alt|title|aria-label)="([^"]*)"', raw2)
    t = re.sub(r"(?s)<!--.*?-->", " ", raw2); t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"</(p|div|li|tr|h[1-6]|section|table|td|th|text|tspan|figcaption)>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    t = re.sub(r"\n{2,}", "\n", "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in t.splitlines()))
    t += "\n\n===== ATTRIBUTES (alt/title/aria-label) =====\n" + "\n".join(html.unescape(a) for a in attrs if a.strip())
    open(os.path.join(OUT, f"{tag}_html.txt"), "w", encoding="utf-8").write(t)
    print(tag, "html chars", len(t))

dump_pptx(SNAP + r"\Dominion_reliability_deck_v3.pptx", "deck_adopted")
dump_pptx(SNAP + r"\Dominion_reliability_deck_v3_public.pptx", "deck_public")
dump_pdf(SNAP + r"\Dominion_reliability_deck_v3_print_letter.pdf", "deck_adopted")
dump_pdf(SNAP + r"\Dominion_reliability_deck_v3_public_print_letter.pdf", "deck_public")
dump_pdf(SNAP + r"\Dominion_interview_brief_v3.pdf", "brief")
dump_pdf(SNAP + r"\Dominion_question_sheet_v3.pdf", "qsheet")
dump_html(SNAP + r"\Dominion_interview_brief_v3.html", "brief")
dump_html(SNAP + r"\Dominion_question_sheet_v3.html", "qsheet")
