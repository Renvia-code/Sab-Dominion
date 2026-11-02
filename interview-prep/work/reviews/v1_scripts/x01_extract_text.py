"""Extract all text from the frozen v2 deliverables (read-only on the snapshot).

Writes plain-text dumps to v1_scripts/../v1_text/ :
  deck_adopted_slides.txt, deck_adopted_notes.txt, deck_adopted_pdf.txt
  deck_public_slides.txt,  deck_public_notes.txt,  deck_public_pdf.txt
  brief_pdf.txt, brief_html.txt, qsheet_pdf.txt, qsheet_html.txt
"""
import sys, os, re, html
sys.stdout.reconfigure(encoding='utf-8')
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Emu

REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
SNAP = os.path.join(REPO, r"interview-prep\work\reviews\snapshot_v2_1035")
OUT = os.path.join(REPO, r"interview-prep\work\reviews\v1_text")
os.makedirs(OUT, exist_ok=True)


def shape_texts(shape, prefix=""):
    """Yield text from a shape, recursing into groups and tables; include alt text (descr)."""
    out = []
    try:
        descr = shape._element.xpath('./*[1]/p:cNvPr/@descr') if hasattr(shape, "_element") else []
    except Exception:
        descr = []
    if descr:
        out.append(f"{prefix}[ALT] {descr[0]}")
    if shape.shape_type == 6 and hasattr(shape, "shapes"):  # group
        for s in shape.shapes:
            out += shape_texts(s, prefix)
    if getattr(shape, "has_table", False) and shape.has_table:
        for r in shape.table.rows:
            out.append(prefix + "[TBL] " + " | ".join(c.text.replace("\n", " / ") for c in r.cells))
    if getattr(shape, "has_text_frame", False) and shape.has_text_frame:
        t = shape.text_frame.text
        if t.strip():
            out.append(prefix + t)
    if getattr(shape, "has_chart", False) and shape.has_chart:
        ch = shape.chart
        try:
            cats = list(ch.plots[0].categories)
        except Exception:
            cats = []
        out.append(prefix + f"[CHART] categories={cats}")
        for p in ch.plots:
            for s in p.series:
                try:
                    vals = list(s.values)
                except Exception:
                    vals = []
                out.append(prefix + f"[CHART] series={s.name!r} values={vals}")
        try:
            if ch.has_title:
                out.append(prefix + "[CHART TITLE] " + ch.chart_title.text_frame.text)
        except Exception:
            pass
    return out


def dump_pptx(path, tag):
    prs = Presentation(path)
    slides_lines, notes_lines = [], []
    for i, slide in enumerate(prs.slides, 1):
        slides_lines.append(f"\n===== SLIDE {i} =====")
        for shp in slide.shapes:
            slides_lines += shape_texts(shp)
        if slide.has_notes_slide:
            nt = slide.notes_slide.notes_text_frame.text if slide.notes_slide.notes_text_frame else ""
            notes_lines.append(f"\n===== NOTES {i} =====\n{nt}")
    open(os.path.join(OUT, f"{tag}_slides.txt"), "w", encoding="utf-8").write("\n".join(slides_lines))
    open(os.path.join(OUT, f"{tag}_notes.txt"), "w", encoding="utf-8").write("\n".join(notes_lines))
    print(tag, "slides:", len(prs.slides))


def dump_pdf(path, tag):
    doc = fitz.open(path)
    lines = []
    for i, page in enumerate(doc, 1):
        lines.append(f"\n===== PAGE {i} =====")
        lines.append(page.get_text("text"))
    open(os.path.join(OUT, f"{tag}_pdf.txt"), "w", encoding="utf-8").write("\n".join(lines))
    print(tag, "pages:", len(doc))


def dump_html(path, tag):
    raw = open(path, encoding="utf-8", errors="replace").read()
    # drop embedded data URIs, scripts and styles, keep alt/title/aria attributes
    raw2 = re.sub(r"data:[a-z/+]+;base64,[A-Za-z0-9+/=]+", "DATAURI", raw)
    raw2 = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", raw2)
    attrs = re.findall(r'(?:alt|title|aria-label)="([^"]*)"', raw2)
    # svg text nodes are kept by tag stripping
    txt = re.sub(r"(?s)<!--.*?-->", " ", raw2)
    txt = re.sub(r"<br\s*/?>", "\n", txt)
    txt = re.sub(r"</(p|div|li|tr|h[1-6]|section|table|td|th|text|tspan|figcaption)>", "\n", txt)
    txt = re.sub(r"<[^>]+>", " ", txt)
    txt = html.unescape(txt)
    txt = "\n".join(re.sub(r"[ \t]+", " ", l).strip() for l in txt.splitlines())
    txt = re.sub(r"\n{2,}", "\n", txt)
    txt += "\n\n===== ATTRIBUTES (alt/title/aria-label) =====\n" + "\n".join(html.unescape(a) for a in attrs if a.strip())
    open(os.path.join(OUT, f"{tag}_html.txt"), "w", encoding="utf-8").write(txt)
    print(tag, "html chars:", len(txt))


dump_pptx(os.path.join(SNAP, "Dominion_reliability_deck_v2.pptx"), "deck_adopted")
dump_pptx(os.path.join(SNAP, "Dominion_reliability_deck_v2_public.pptx"), "deck_public")
dump_pdf(os.path.join(SNAP, "Dominion_reliability_deck_v2_print_letter.pdf"), "deck_adopted")
dump_pdf(os.path.join(SNAP, "Dominion_reliability_deck_v2_public_print_letter.pdf"), "deck_public")
dump_pdf(os.path.join(SNAP, "Dominion_interview_brief_v2.pdf"), "brief")
dump_pdf(os.path.join(SNAP, "Dominion_question_sheet_v2.pdf"), "qsheet")
dump_html(os.path.join(SNAP, "Dominion_interview_brief_v2.html"), "brief")
dump_html(os.path.join(SNAP, "Dominion_question_sheet_v2.html"), "qsheet")
