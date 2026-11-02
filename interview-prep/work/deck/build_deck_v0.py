"""Safety-net v0 deck (P1): 8 main slides + 6 appendix slides, 16:9, Segoe UI, speaker notes on
every main slide. Built from the storyline v0 (work/storyline_v0.md), D's re-verified figures
(work/data/reverify_2_2.md F01-F15, work/data/findings.md) and R's verified facts (research/for_B.md).

Every text box is measured with the real Segoe UI metrics before it is written (fit check), and the
deck is then rendered (LibreOffice -> PDF -> PNG) and looked at.

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\deck\\build_deck_v0.py
Out:  interview-prep/deliverables/01_deck/Dominion_reliability_deck_v0.pptx
      interview-prep/deliverables/01_deck/Dominion_reliability_deck_v0_print_letter.pdf
      interview-prep/work/proofs/deck_v0/ (slide-size PDF, PNG proofs colour + greyscale)
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402
import pipeline  # noqa: E402

from lxml import etree  # noqa: E402
from PIL import ImageFont  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE  # noqa: E402
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN  # noqa: E402
from pptx.oxml.ns import qn  # noqa: E402
from pptx.util import Emu, Inches, Pt  # noqa: E402

CH = ds.WORK / "charts" / "v0"
OUT = ds.REPO / "interview-prep" / "deliverables" / "01_deck"
PROOFS = ds.WORK / "proofs" / "deck_v0"
STEM = "Dominion_reliability_deck_v0"

REG, SEMI, LIGHT, SEMIL = ds.FONT, ds.FONT_SEMIBOLD, ds.FONT_LIGHT, ds.FONT_SEMILIGHT
FONTFILES = {REG: "C:/Windows/Fonts/segoeui.ttf", SEMI: "C:/Windows/Fonts/seguisb.ttf",
             LIGHT: "C:/Windows/Fonts/segoeuil.ttf", SEMIL: "C:/Windows/Fonts/segoeuisl.ttf"}
EM_LINE = 1.33           # Segoe UI single-spaced line height, in em (win ascent + descent)
L, CW = 0.6, 13.333 - 1.2
R = L + CW
TOP = 1.58               # content zone top
BOTTOM = 5.72            # content zone bottom on main slides (the "For Dominion" line sits below)
BOTTOM_APX = 6.38        # appendix slides have no "For Dominion" line
PROBLEMS: list[str] = []

# ----------------------------------------------------------------------------- measuring
_fonts: dict = {}


def text_w(text: str, font: str, pt: float) -> float:
    """Advance width in points, from the real font file."""
    key = (font, pt)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(FONTFILES[font], int(round(pt * 20)))
    return _fonts[key].getlength(text) / 20.0


def n_lines(text: str, font: str, pt: float, width_in: float) -> int:
    width = width_in * 72 - 1.0
    total = 0
    for para in text.split("\n"):
        cur, n = "", 1
        for w in para.split(" "):
            t = f"{cur} {w}".strip()
            if not cur or text_w(t, font, pt) <= width:
                cur = t
            else:
                n, cur = n + 1, w
        total += n
    return total


def need_h(text, font, pt, width_in, ls=1.0) -> float:
    return n_lines(text, font, pt, width_in) * pt * EM_LINE * ls / 72


# ----------------------------------------------------------------------------- drawing
def rgb(h: str) -> RGBColor:
    return RGBColor.from_string(h.lstrip("#").upper())


def tb(slide, x, y, w, h, paras, size, *, anchor="top", align="left", ls=1.0, space_after=0.0,
       name="", check=True):
    """Text box with zero insets. paras: list of str or list of (text, font, colour) runs."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    total = 0.0
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
        p.line_spacing = ls
        if space_after and i < len(paras) - 1:
            p.space_after = Pt(space_after)
        runs = [(para, REG, ds.INK)] if isinstance(para, str) else para
        for text, font, colour in runs:
            r = p.add_run()
            r.text = text
            r.font.name = font
            r.font.size = Pt(size)
            r.font.color.rgb = rgb(colour)
        full = "".join(t for t, _, _ in runs)
        fonts = [f for _, f, _ in runs]
        mfont = SEMI if SEMI in fonts else fonts[0]
        total += need_h(full, mfont, size, w, ls) + (space_after / 72 if i < len(paras) - 1 else 0)
    if check and total > h + 0.02:
        PROBLEMS.append(f"OVERFLOW {name or str(paras[0])[:40]!r}: needs {total:.2f} in, box {h:.2f} in")
    return box, total


def _plain(shape):
    """Drop the theme style reference (it carries a shadow in LibreOffice and PowerPoint)."""
    st = shape._element.find(qn("p:style"))
    if st is not None:
        shape._element.remove(st)
    shape.shadow.inherit = False


def rect(slide, x, y, w, h, fill, line=None, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    _plain(s)
    if fill:
        s.fill.solid()
        s.fill.fore_color.rgb = rgb(fill)
    else:
        s.fill.background()
    if line:
        s.line.color.rgb = rgb(line)
        s.line.width = Pt(0.9)
    else:
        s.line.fill.background()
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.text_frame.text = ""
    return s


def hline(slide, x, y, w, colour=ds.RULE, width_pt=0.9):
    """A hairline rule drawn as a thin filled rectangle (no line style, no shadow)."""
    return rect(slide, x, y, w, width_pt / 72.0, colour)


def arrow(slide, x, y, w=0.26, h=0.26, colour=ds.MUTED):
    s = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    _plain(s)
    s.fill.solid()
    s.fill.fore_color.rgb = rgb(colour)
    s.line.fill.background()
    return s


def picture(slide, png: Path, x, y, alt: str):
    from PIL import Image
    with Image.open(png) as im:
        wpx, hpx = im.size
        dpi = im.info.get("dpi", (300, 300))[0] or 300
    w_in, h_in = wpx / dpi, hpx / dpi
    pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y), width=Inches(w_in), height=Inches(h_in))
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    return pic, w_in, h_in


def col(slide, x, y, w, items, bottom, name):
    """Stack text items top-down, each sized to its measured height.
    item: ('rule', gap_after) | (text, font, pt, colour, gap_after) | (runs, None, pt, None, gap_after)."""
    for it in items:
        if it[0] == "rule":
            hline(slide, x, y, w)
            y += it[1]
            continue
        text, font, pt, colour, gap = it
        paras = [text if font is None else [(text, font, colour)]]
        if font is None:
            paras = [text]
            plain = "".join(t for t, _, _ in text)
            fonts = [f for _, f, _ in text]
            h = need_h(plain, SEMI if SEMI in fonts else fonts[0], pt, w)
        else:
            h = need_h(text, font, pt, w, 0.95 if pt >= 30 else 1.0)
        tb(slide, x, y, w, h + 0.02, paras, pt, ls=0.95 if pt >= 30 else 1.0, name=f"{name}:{str(text)[:24]}")
        y += h + gap
    if y > bottom + 0.02:
        PROBLEMS.append(f"COLUMN {name}: ends at {y:.2f} in, limit {bottom:.2f} in")
    return y


def title(slide, text):
    _, h = tb(slide, L, 0.42, CW, 1.0, [[(text, SEMI, ds.INK)]], ds.DECK["title_pt"], ls=0.92, name="title")
    words = len(text.split())
    if words > 16:
        PROBLEMS.append(f"TITLE has {words} words: {text[:50]!r}")


def means(slide, text):
    y = 5.84
    rect(slide, L, y + 0.06, 0.07, 0.27, ds.SUBJECT)
    tb(slide, L + 0.2, y, CW - 0.2, 0.66,
       [[("For Dominion: ", SEMI, ds.INK), (text, REG, ds.INK_2)]], ds.DECK["lead_pt"], ls=0.95, name="means")


def source(slide, text, num):
    tb(slide, L, 6.56, CW - 0.75, 0.52, [[("Source: ", SEMI, ds.MUTED), (text, REG, ds.MUTED)]],
       ds.DECK["source_pt"], ls=0.95, name="source")
    tb(slide, R - 0.6, 6.56, 0.6, 0.3, [[(str(num), REG, ds.MUTED)]], ds.DECK["source_pt"], align="right",
       name="num")


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = " ".join(text.split())


def table(slide, x, y, w, col_w, rows, pt=16, header_fill=None, row_h=0.32, highlight=None, align=None,
          bold_rows=()):
    """Plain table: no style, hairline rules, header in semibold ink, optional tinted row."""
    nr, nc = len(rows), len(rows[0])
    gf = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    t = gf.table
    tblPr = t._tbl.tblPr
    sid = tblPr.find(qn("a:tableStyleId"))
    if sid is None:
        sid = etree.SubElement(tblPr, qn("a:tableStyleId"))
    sid.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"  # No Style, No Grid
    t.first_row = False
    t.horz_banding = False
    for j, cw in enumerate(col_w):
        t.columns[j].width = Inches(cw)
    for i in range(nr):
        t.rows[i].height = Inches(row_h)
        for j in range(nc):
            cell = t.cell(i, j)
            cell.margin_left = Inches(0.08)
            cell.margin_right = Inches(0.08)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            fill = ds.SUBJECT_TINT if (highlight is not None and i == highlight) else "#FFFFFF"
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(fill)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if (align and align[j] == "r") else PP_ALIGN.LEFT
            r = p.add_run()
            r.text = str(rows[i][j])
            head = i == 0
            r.font.name = SEMI if (head or i in bold_rows or (highlight is not None and i == highlight)) else REG
            r.font.size = Pt(pt)
            r.font.color.rgb = rgb(ds.INK if head or i == highlight else ds.INK_2)
            # hairline bottom rule (heavier under the header)
            tcPr = cell._tc.get_or_add_tcPr()
            ln = etree.Element(qn("a:lnB"), w=str(int((1.1 if head else 0.6) * 12700)), cap="flat", cmpd="sng",
                               algn="ctr")
            sf = etree.SubElement(ln, qn("a:solidFill"))
            etree.SubElement(sf, qn("a:srgbClr"), val=(ds.INK if head else ds.RULE).lstrip("#"))
            tcPr.insert(0, ln)
            # width check for single-line cells
            lines = n_lines(str(rows[i][j]), SEMI if head else REG, pt, col_w[j] - 0.16)
            if lines > 1 and not head and pt * EM_LINE * lines / 72 + 0.04 > row_h:
                PROBLEMS.append(f"TABLE cell wraps to {lines} lines: {str(rows[i][j])[:40]!r}")
    return gf


# ----------------------------------------------------------------------------- data
def load_csv(p: Path):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def main():
    PROOFS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    peers = load_csv(CH / "s3_peer_quadrant.csv")
    storm = load_csv(CH / "s4_storm_days_vs_saidi.csv")
    stack = load_csv(CH / "a3_exmed_vs_med.csv")

    prs = Presentation()
    prs.slide_width = Inches(ds.SLIDE_W_IN)
    prs.slide_height = Inches(ds.SLIDE_H_IN)
    blank = prs.slide_layouts[6]
    cp = prs.core_properties
    cp.author = "Saketh Bollina"
    cp.last_modified_by = "Saketh Bollina"
    cp.title = "Dominion Energy Virginia reliability: what public data shows"
    cp.subject = "Interview presentation, 3 November 2026"
    cp.keywords = ""
    cp.comments = ""
    cp.category = ""
    cp.revision = 1

    def new():
        return prs.slides.add_slide(blank)

    rx = L + 7.9 + 0.33        # right column x when a 7.9 in chart sits on the left
    rw = R - rx

    # ------------------------------------------------------------------ S1 title
    s = new()
    rect(s, L, 1.62, 0.9, 0.09, ds.SUBJECT)
    tb(s, L, 1.95, CW, 2.3, [[("Dominion Energy Virginia reliability: what public data shows, and where "
                                 "I'd look first", SEMI, ds.INK)]], 40, ls=0.95, name="S1 title")
    tb(s, L, 4.3, 10.6, 0.45, [[("Independent analysis of public data", SEMIL, ds.INK_2)]], 22, name="S1 sub")
    tb(s, L, 5.15, 6.0, 0.42, [[("Saketh Bollina", SEMI, ds.INK)]], 22, name="S1 name")
    tb(s, L, 5.58, 6.0, 0.42, [[("3 November 2026", REG, ds.INK_2)]], 20, name="S1 date")
    hline(s, L, 6.5, CW)
    tb(s, L, 6.62, CW, 0.35, [[("Data: EIA-861 · PUDL · NOAA Storm Events · EIA-930", REG, ds.MUTED)]],
       ds.DECK["source_pt"], name="S1 foot")
    notes(s, """Thank you for having me. I'm Saketh Bollina. To prepare, I tried to understand Dominion Energy
    Virginia's reliability the way an analyst on your team would, so I rebuilt the reported reliability numbers from
    public data: EIA's annual reliability filings, NOAA's storm records and EIA's hourly demand data. Everything
    here is public. I had no Dominion internal data, and I'll point out where public data stops. In the next ten
    minutes: first the answer, what happened to outage minutes and where the change came from; then how Dominion
    compares with twelve peer utilities; then weather; then how demand is changing shape. Last, what I would do
    with Dominion's own data in the first 90 days, and how I built this. I've kept the numbers few, and each one
    has its source on the slide. Please stop me at any point.""")

    # ------------------------------------------------------------------ S2 answer first
    s = new()
    title(s, "Outage minutes rose from 130 to 133 because interruptions became more frequent, not longer")
    lw = 4.95
    col(s, L, TOP - 0.04, lw, [
        ("130 → 133", LIGHT, 44, ds.INK, 0.0),
        ("Reported 3-year average outage minutes per customer, ex-major events (2022–24 → 2023–25)",
         REG, 16, ds.INK_2, 0.16),
        ("rule", 0.1),
        ("130.2 → 133.0", LIGHT, 30, ds.INK, 0.0),
        ("The same figures rebuilt from public EIA-861 data: they reconcile", REG, 16, ds.INK_2, 0.16),
        ("rule", 0.1),
        ("136.0 → 144.4", LIGHT, 30, ds.INK, 0.0),
        ("The average moved because 2025 replaced 2022 in the 3-year window", REG, 16, ds.INK_2, 0.0),
    ], BOTTOM, "S2 left")
    picture(s, CH / "s2_lock_2022_2025_saifi.png", R - 6.6, TOP - 0.06,
            "Two panels. Top: change from 2022 to 2025, SAIDI 136.0 to 144.4 minutes (+6%), SAIFI 1.199 to 1.320 "
            "(+10%), CAIDI 113.5 to 109.4 minutes (-4%). Bottom: SAIFI by year 2013-2025; 2025 (1.320) is the "
            "highest, ahead of 2018 (1.303).")
    means(s, "the first question is what is making interruptions more frequent, before how to restore faster.")
    source(s, "EIA-861 2025 final and PUDL (EIA-861) 2013–2024, Dominion Energy Virginia, excluding major event "
              "days; 3-year means of annual values. Reported figures: Dominion Energy 2025 Annual Report, p. 10.", 2)
    notes(s, """Dominion's 2025 annual report gives SAIDI, excluding major events, of 133 minutes for the three years
    ending 2025, up from 130, and attributes the increase primarily to storm activity. SAIDI is average outage
    minutes per customer. I rebuilt it from EIA's public filings and got 130.2 and 133.0, so the public data
    reconciles. A three-year average only moves when a year leaves the window: here 2025, at 144.4 minutes, replaced
    2022, at 136.0. Between those two years SAIFI, how often customers lose power, rose 10 percent, and CAIDI, how
    long each interruption lasts, fell 4 percent. So the rise is more frequent interruptions, not longer ones. And
    2025's SAIFI, 1.32, is the highest in EIA's 2013 to 2025 record. Two cautions I'd volunteer: 2025's SAIDI is
    still below 2018 and 2019, and over eleven years none of these trends is statistically significant, so one year
    is not a trend. Measured from 2023 instead, about four-fifths of the change is still frequency.""")

    # ------------------------------------------------------------------ S3 peers
    s = new()
    title(s, "Among 12 peer utilities, Dominion restores at a mid-pack pace; frequency is the gap")
    picture(s, CH / "s3_peer_quadrant.png", L, TOP - 0.03,
            "Scatter of 12 utilities: SAIFI 2021-25 average across, CAIDI down. Dominion Energy Virginia at 1.21 "
            "interruptions and 110 minutes, beside Duke Progress and Georgia Power; peer medians 0.96 and 105.")
    col(s, rx, TOP + 0.02, rw, [
        ("rule", 0.08),
        ("1.21", LIGHT, 40, ds.INK, 0.0),
        ("interruptions per customer a year: 4th highest of 12 (peer median 0.96)", REG, 16, ds.INK_2, 0.22),
        ("rule", 0.08),
        ("110 min", LIGHT, 40, ds.INK, 0.0),
        ("per interruption: 6th of 12 (peer median 105)", REG, 16, ds.INK_2, 0.22),
        ("Methods differ: Dominion uses its own major-event rule, most peers IEEE 1366, so ranks are indicative.",
         REG, 16, ds.MUTED, 0.0),
    ], BOTTOM, "S3 right")
    means(s, "preventing interruptions is where the gap to peers is; restoration speed is already near the middle.")
    source(s, "EIA-861 / PUDL 2021–2025, excluding major event days, means of annual values; 12 large "
              "investor-owned utilities in PJM and the Southeast, chosen by EIA ID before results.", 3)
    notes(s, """To see whether that's unusual, I compared Dominion with twelve large investor-owned utilities in PJM
    and the Southeast, picked by EIA ID before I looked at any results. Across is interruptions per customer per
    year; up is minutes per interruption; both are 2021 to 2025 averages. Dominion is the blue dot. On restoration
    time it's mid-pack: 110 minutes against a peer median of 105, sixth of twelve. On frequency it's 1.21
    interruptions a year, fourth highest of twelve, against a median of 0.96. Its nearest neighbours are Duke
    Energy Progress and Georgia Power. One caveat I'd raise myself: utilities set aside major event days in
    different ways. Most of these peers use the IEEE 1366 method and Dominion reports under its own rule, so I'd
    treat the ranking as indicative, not exact. The pattern matches the previous slide: the gap to peers is how
    often customers lose power, not how fast it comes back.""")

    # ------------------------------------------------------------------ S4 weather
    s = new()
    title(s, "Years with more storm days had more outage minutes (r = 0.70 over ten years)")
    picture(s, CH / "s4_storm_days_vs_saidi.png", L, TOP - 0.03,
            "Scatter: storm county-days against SAIDI ex-MED, 2015-2024, with a fitted line; r = 0.70. 2025 "
            "(796 county-days, 144.4 minutes) sits on the line (145.3 from the fit).")
    col(s, rx, TOP + 0.02, rw, [
        ("rule", 0.08),
        ("465 → 796", LIGHT, 40, ds.INK, 0.0),
        ("storm county-days in Dominion's Virginia counties, 2024 → 2025", REG, 16, ds.INK_2, 0.22),
        ("rule", 0.08),
        ("r = 0.70", LIGHT, 40, ds.INK, 0.0),
        ("over 2015–2024 (n = 10): an association, not a cause", REG, 16, ds.INK_2, 0.22),
        ("Dominion attributes the rise primarily to increased storm activity (2025 Annual Report, p. 10).",
         REG, 16, ds.MUTED, 0.0),
    ], BOTTOM, "S4 right")
    means(s, "report reliability next to weather exposure, so that a stormy year is not mistaken for a trend.")
    source(s, "NOAA Storm Events 2015–2025, wind, winter and tropical event types, by county in Dominion's Virginia "
              "service territory (EIA-861); EIA-861 SAIDI excluding major event days; least-squares fit on "
              "2015–2024.", 4)
    notes(s, """Weather is the obvious question. I counted storm county-days: each day a line-damaging storm, such as
    thunderstorm wind, an ice storm or a tropical storm, was recorded in a Virginia county Dominion serves, from
    NOAA's Storm Events data. 2025 had 796, up from 465 in 2024. Over 2015 to 2024, years with more storm days had
    more outage minutes: the correlation is 0.70. That's ten points, so I treat it as a check, not a model. The fit,
    made without 2025, puts 2025 at 145 minutes; the actual was 144. So 2025 looks like a stormy year more than a
    break in the trend, which is consistent with the annual report: Dominion attributes the rise primarily to
    increased storm activity. Adjusted for storm days, there's no clear trend since 2015. What this can't do is say
    which circuits, which causes, or whether hardened lines held up; that needs outage records. For reporting, I'd
    show reliability next to weather exposure.""")

    # ------------------------------------------------------------------ S5 demand shape
    s = new()
    title(s, "Overnight demand grew faster than afternoon demand, and winter rivals summer for the yearly peak")
    picture(s, CH / "s5_winter_summer_peaks.png", L, TOP - 0.03,
            "Paired columns 2019-2026: highest winter hour against highest summer hour, PJM Dominion zone. "
            "Winter is higher in 2019, 2022, 2025 and, so far, 2026 (25,413 vs 25,384 MW, a near-tie).")
    col(s, rx, TOP + 0.02, rw, [
        ("rule", 0.08),
        ("+39–41%", LIGHT, 40, ds.INK, 0.0),
        ("average load in the hours ending 1–5 a.m., 2019 → 2025", REG, 16, ds.INK_2, 0.2),
        ("rule", 0.08),
        ("about +27%", LIGHT, 40, ds.INK, 0.0),
        ("in the hours ending 1–5 p.m., same years", REG, 16, ds.INK_2, 0.2),
        ("rule", 0.1),
        ("Lowest hour of the year +52%, highest +26%. 2026 so far: 25,413 MW winter vs 25,384 MW summer.",
         REG, 16, ds.MUTED, 0.0),
    ], BOTTOM, "S5 right")
    means(s, "less overnight slack and winter peaks: plans and reports built around summer afternoons need "
             "updating.")
    source(s, "EIA-930 hourly demand, PJM Dominion (DOM) zone, which is wider than Dominion's retail territory; "
              "July 2018–October 2026 (2026 year to date). Winter = Dec–Feb, summer = Jun–Aug.", 5)
    notes(s, """Reliability is one side; load is the other. This is EIA's hourly demand for the PJM Dominion zone,
    which is wider than Dominion's retail territory. Two changes stand out. First, the yearly peak: winter set the
    year's highest hour in 2019, 2022 and 2025, and 2026 is a near-tie so far, 25,413 against 25,384 megawatts.
    Second, the daily shape: from 2019 to 2025, average load in the hours ending 1 to 5 a.m. rose 39 to 41 percent,
    against about 27 percent in the hours ending 1 to 5 p.m. The lowest hour of the year rose 52 percent, the
    highest 26. Growth around the clock is consistent with large constant loads, but this data can't identify
    customers, so I don't attribute it to data centers. For planning and reporting, it means less overnight slack,
    and winter readiness matters as much as summer.""")

    # ------------------------------------------------------------------ S6 first 90 days
    s = new()
    title(s, "With Dominion's outage, meter and circuit data, I would start where public data stops")
    gap = 0.28
    cw3 = (CW - 2 * gap) / 3
    cards = [
        ("Days 1–30", "Reconcile",
         ["Learn how outages, meter events and circuits are recorded and reported.",
          "Rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filed figures."],
         "a reconciled baseline with written definitions"),
        ("Days 31–60", "Diagnose",
         ["Interruptions by circuit and cause code, vegetation included; repeat interruptions (CEMI).",
          "Restoration timed from meter “last gasp” (99.8% of meters are smart)."],
         "tested views and a data dictionary"),
        ("Days 61–90", "Prioritise and track",
         ["Rank feeders by customer-minutes; track Grid Resiliency work such as mainfeeder hardening against "
          "similar untreated feeders and weather."],
         "a Power BI programme-tracking report, refreshed on a schedule"),
    ]
    ytop, ybot = TOP + 0.02, BOTTOM - 0.04
    for i, (days, head, body, deliv) in enumerate(cards):
        x = L + i * (cw3 + gap)
        last = i == 2
        rect(s, x, ytop, cw3, ybot - ytop, ds.SUBJECT_TINT if last else ds.TINT)
        rect(s, x, ytop, cw3, 0.06, ds.SUBJECT)
        ix, iw = x + 0.2, cw3 - 0.4
        y = col(s, ix, ytop + 0.2, iw, [
            (days, SEMI, 16, ds.MUTED, 0.0),
            (head, SEMI, 22, ds.INK, 0.14),
        ] + [(b, REG, 16, ds.INK_2, 0.1) for b in body], ybot, f"S6 card {i + 1}")
        dh = need_h("Deliverable: " + deliv, SEMI, 16, iw)
        yd = ybot - 0.18 - dh
        if yd < y + 0.05:
            PROBLEMS.append(f"S6 card {i + 1}: deliverable collides ({yd:.2f} < {y:.2f})")
        hline(s, ix, yd - 0.1, iw, colour=ds.RULE)
        tb(s, ix, yd, iw, dh + 0.02, [[("Deliverable: ", SEMI, ds.INK), (deliv, SEMI if last else REG,
                                                                         ds.INK if last else ds.INK_2)]], 16,
           name=f"S6 deliverable {i + 1}")
    means(s, "each step turns a system-level trend into a circuit-level view the programme team can act on.")
    source(s, "A plan: Dominion data is named by type only, and none was used here. Smart meters: EIA-861 2025 "
              "(AMI share of meters). Grid Resiliency: Dominion Energy website, read 1 November 2026.", 6)
    notes(s, """Public data narrows the question; Dominion's own data answers it. Here is how I'd spend the first 90
    days, practically. First month, reconcile: learn how outages, meter events and circuits are recorded and how
    reliability is reported, then rebuild one year's SAIDI, SAIFI and CAIDI from source records and reconcile them
    to the filed numbers, the way I reconciled the public data to 133. Second month, diagnose: interruptions by
    circuit and cause code, vegetation included, and customers interrupted repeatedly. EIA's 2025 data shows 99.8
    percent of Dominion's meters are smart meters, so restoration can be timed from last-gasp and restore signals.
    Third month, prioritise and track. Mainfeeder hardening already selects feeders on five years of outage
    history, and Dominion reports a 32 percent cut in outage minutes on feeders hardened for at least a year, as of
    November 2023. I'd build the Power BI report that tracks treated feeders against similar untreated feeders and
    weather, refreshed on a schedule.""")

    # ------------------------------------------------------------------ S7 how it's built
    s = new()
    title(s, "Built like governed production reporting: tested, documented, and reconciled to the reported numbers")
    y0, y1 = TOP + 0.02, 4.05
    aw = 0.3
    src_w = 3.3
    pbi_w = 1.75
    sf_x = L + src_w + aw + 0.04
    sf_w = R - pbi_w - aw - 0.04 - sf_x
    # sources
    rect(s, L, y0, src_w, y1 - y0, "#FFFFFF", line=ds.RULE)
    col(s, L + 0.18, y0 + 0.14, src_w - 0.36, [
        ("Public sources", SEMI, 18, ds.INK, 0.06),
        ("EIA-861 reliability", SEMI, 16, ds.INK, 0.0), ("24,358 + 977 rows", REG, 16, ds.INK_2, 0.05),
        ("NOAA Storm Events", SEMI, 16, ds.INK, 0.0), ("831,288 rows", REG, 16, ds.INK_2, 0.05),
        ("EIA-930 hourly demand", SEMI, 16, ds.INK, 0.0), ("6,077,232 rows", REG, 16, ds.INK_2, 0.0),
    ], y1, "S7 sources")
    arrow(s, L + src_w + 0.02, (y0 + y1) / 2 - 0.13)
    # Snowflake group
    rect(s, sf_x, y0, sf_w, y1 - y0, ds.TINT)
    tb(s, sf_x + 0.18, y0 + 0.1, 3.0, 0.32, [[("Snowflake", SEMI, ds.INK_2)]], 16, name="S7 snowflake")
    inner = [("RAW", "as published, all text"), ("STG", "typed and cleaned"), ("MART", "facts, dimensions, views")]
    iaw = 0.26
    bw = (sf_w - 0.36 - 2 * (iaw + 0.06)) / 3
    by0, by1 = y0 + 0.55, y1 - 0.18
    for k, (h_, d_) in enumerate(inner):
        bx = sf_x + 0.18 + k * (bw + iaw + 0.06)
        rect(s, bx, by0, bw, by1 - by0, "#FFFFFF", line=ds.RULE)
        col(s, bx + 0.14, by0 + 0.14, bw - 0.28, [(h_, SEMI, 18, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)],
            by1, f"S7 {h_}")
        if k < 2:
            arrow(s, bx + bw + 0.03, (by0 + by1) / 2 - 0.13, w=iaw)
    arrow(s, sf_x + sf_w + 0.02, (y0 + y1) / 2 - 0.13)
    px = R - pbi_w
    rect(s, px, y0, pbi_w, y1 - y0, ds.SUBJECT_TINT)
    col(s, px + 0.16, y0 + 0.14, pbi_w - 0.32, [("Power BI", SEMI, 18, ds.INK, 0.04),
                                                ("Import model and report", REG, 16, ds.INK_2, 0.0)], y1, "S7 PBI")
    # governance badges
    badges = [("12 tests pass", "keys, SAIDI = SAIFI × CAIDI, EIA's published 2025 values"),
              ("Data dictionary", "a business definition for every column and measure"),
              ("Decisions log", "14 decisions, such as storm types and peers, made before results"),
              ("Reconciled", "rebuilt 130.2 and 133.0 vs 130 and 133 reported")]
    gb = 0.22
    bw4 = (CW - 3 * gb) / 4
    gy0, gy1 = 4.2, BOTTOM
    for k, (h_, d_) in enumerate(badges):
        bx = L + k * (bw4 + gb)
        rect(s, bx, gy0, bw4, 0.06, ds.SUBJECT if k == 3 else ds.CONTEXT)
        col(s, bx, gy0 + 0.16, bw4, [(h_, SEMI, 18, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)], gy1,
            f"S7 badge {k + 1}")
    means(s, "reconcile first, test every load, document every decision: the same discipline for Dominion's "
             "reporting.")
    source(s, "Project build: SQL scripts, tests T1–T12, data dictionary and decisions log D1–D14; row counts as "
              "loaded.", 7)
    notes(s, """Briefly, how it's built, because it's the same discipline I'd bring. Three public sources: EIA's
    reliability filings, through PUDL plus the 2025 final file; NOAA Storm Events, about 831,000 storm records; and
    EIA-930 hourly demand, about six million rows. They land in Snowflake as raw text exactly as published, a
    staging layer types and cleans them, and a mart of facts, dimensions and views feeds Power BI in Import mode.
    Twelve tests run after each load: no duplicate keys, SAIDI equals SAIFI times CAIDI, the 2025 values match what
    EIA published, every county maps, full years, no duplicate hours. All pass. A data dictionary gives each measure
    a business definition, and a decisions log records fourteen choices, such as which storm types count and which
    peers to use, made before seeing results. The first check was reconciliation: 130.2 and 133.0 against the
    reported 130 and 133. Every chart comes from a script and a saved data snapshot.""")

    # ------------------------------------------------------------------ S8 close
    s = new()
    title(s, "Three takeaways: frequency first, reliability net of weather, plan for a new load shape")
    g3 = 0.35
    w3 = (CW - 2 * g3) / 3
    takeaways = [("1", "Look at frequency first",
                  "Interruptions per customer +10% (2022→2025), the 2013–2025 high; 4th of 12 peers"),
                 ("2", "Net out the weather",
                  "Storm days track outage minutes (r = 0.70, ten years): an association, not a cause"),
                 ("3", "Plan for a new load shape",
                  "Hours ending 1–5 a.m. +39–41% (2019→2025); winter set the peak in 2019, 2022 and 2025")]
    for k, (n_, h_, d_) in enumerate(takeaways):
        x = L + k * (w3 + g3)
        tb(s, x, TOP - 0.1, 0.5, 0.7, [[(n_, LIGHT, ds.SUBJECT)]], 40, ls=0.9, name="S8 numeral")
        col(s, x + 0.52, TOP, w3 - 0.52, [(h_, SEMI, 20, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)], 2.95,
            f"S8 take {k + 1}")
    hline(s, L, 3.02, CW, colour=ds.RULE)
    tb(s, L, 3.14, CW, 0.72, [[("I build governed Snowflake → Power BI reporting, and I've already started "
                                "learning your reliability data.", SEMI, ds.INK)]], 20, ls=0.95, name="S8 fit")
    tb(s, L, 4.05, CW, 0.28, [[("How my experience maps", SEMI, ds.MUTED),
                                ("   Mercury Insurance, Data Analyst", REG, ds.MUTED)]], ds.DECK["source_pt"],
       name="S8 strip label")
    maps = [("Snowflake pipeline, 20M+ rows", "this mart"),
            ("Root-cause analysis on joined data", "SAIFI by cause"),
            ("Validation and reconciliation", "reconciled 133.0"),
            ("Metadata and business definitions", "data dictionary"),
            ("Requirements with operations and IT", "programme teams")]
    g5 = 0.2
    w5 = (CW - 4 * g5) / 5
    for k, (a_, b_) in enumerate(maps):
        x = L + k * (w5 + g5)
        rect(s, x, 4.38, w5, 0.05, ds.CONTEXT)
        col(s, x, 4.5, w5, [(a_, SEMI, 16, ds.INK, 0.02), ("→ " + b_, REG, 16, ds.INK_2, 0.0)], BOTTOM,
            f"S8 map {k + 1}")
    means(s, "I would like to do this with your data.")
    source(s, "Numbers from slides 2–5. Experience: Mercury Insurance, Data Analyst, 2026 to present.", 8)
    notes(s, """Three takeaways. One: look at frequency first. Interruptions per customer rose 10 percent from 2022
    to 2025 to the highest level in EIA's 2013 to 2025 record, and Dominion is fourth highest of twelve peers, while
    restoration time is mid-pack. Two: read reliability net of weather. Storm days line up with outage minutes, r of 0.70, but that's an
    association over ten years, not a cause. Three: plan for a new load shape. The small hours grew 39 to 41
    percent, and winter set the yearly peak in 2019, 2022 and 2025. On fit: at Mercury Insurance I built a
    Snowflake pipeline across policy, claims and billing data, over 20 million rows, led a root-cause analysis, and
    owned validation and reconciliation for a pilot. This project applies the same habits to your data. I build
    governed Snowflake to Power BI reporting, and I've already started learning your reliability data. I would
    like to do this with your data. Thank you; I'm happy to take questions.""")

    # ------------------------------------------------------------------ A1 definitions
    s = new()
    title(s, "Definitions: SAIDI = SAIFI × CAIDI, and major event days are set aside by rule")
    bw_ = 3.35
    op = (CW - 3 * bw_) / 2
    defs = [("SAIDI", "outage minutes per customer per year"),
            ("SAIFI", "interruptions per customer per year: how often"),
            ("CAIDI", "minutes per interruption: how long")]
    for k, (h_, d_) in enumerate(defs):
        x = L + k * (bw_ + op)
        rect(s, x, TOP + 0.05, bw_, 1.45, ds.SUBJECT_TINT if k == 1 else ds.TINT)
        col(s, x + 0.2, TOP + 0.2, bw_ - 0.4, [(h_, SEMI, 26, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)],
            TOP + 1.5, f"A1 {h_}")
        if k < 2:
            tb(s, x + bw_, TOP + 0.38, op, 0.8, [[("=" if k == 0 else "×", LIGHT, ds.INK)]], 40, align="center",
               name="A1 op")
    tb(s, L, TOP + 1.65, CW, 0.36, [[("Dominion 2025: ", SEMI, ds.INK),
                                      ("1.320 × 109.4 = 144.4 minutes (excluding major event days)", REG,
                                       ds.INK_2)]], 16, name="A1 example")
    col(s, L, TOP + 2.25, CW, [
        ("Major event days (MED) are set aside so that one extreme storm does not swamp the trend. IEEE 1366 marks "
         "a day as a major event day when its SAIDI exceeds a threshold set from the previous five years of daily "
         "SAIDI (the “2.5 beta” method).", REG, 16, ds.INK_2, 0.14),
        ("Dominion reports to EIA under its own major-event rule; most peers in this deck use IEEE 1366. Headline "
         "figures here exclude major event days; all-event figures are on A3.", REG, 16, ds.INK_2, 0.14),
        ("Log split: ln(SAIDI ratio) = ln(SAIFI ratio) + ln(CAIDI ratio). Share from frequency = ln(SAIFI ratio) ÷ "
         "ln(SAIDI ratio): 2023→2025, 0.125 ÷ 0.158 = 79%.", REG, 16, ds.INK_2, 0.0),
    ], BOTTOM_APX, "A1 text")
    source(s, "IEEE Std 1366 (reliability indices); EIA-861 reliability, Dominion Energy Virginia 2023 and 2025.",
           "A1")
    notes(s, """Definitions for reference. SAIDI equals SAIFI times CAIDI, which is why the change in SAIDI can be
    split exactly into a frequency part and a duration part using logs.""")

    # ------------------------------------------------------------------ A2 weather fit table
    s = new()
    title(s, "The weather fit is a check on one year, not a forecast")
    b0, b1 = 104.37, 0.0514
    rows = [["Year", "Storm\ncounty-days", "SAIDI\nex‑MED", "From\nthe fit", "Difference"]]
    for r_ in storm:
        yr = int(r_["year"])
        cd = float(r_["storm_county_days"])
        sd = float(r_["saidi_ex_med"])
        fit = b0 + b1 * cd
        rows.append([f"{yr}" + (" (not in fit)" if yr == 2025 else ""), f"{cd:,.0f}", f"{sd:.1f}", f"{fit:.1f}",
                     f"{sd - fit:+.1f}".replace("-", "−")])
    table(s, L, TOP + 0.02, 7.3, [2.0, 1.55, 1.25, 1.25, 1.25], rows, pt=16, row_h=0.355, highlight=len(rows) - 1,
          align="lrrrr")
    col(s, L + 7.75, TOP + 0.02, CW - 7.75, [
        ("rule", 0.1),
        ("Fit on 2015–2024 (n = 10): SAIDI = 104.4 + 0.0514 × storm county-days; r = 0.70, R² 0.48.", REG, 16,
         ds.INK_2, 0.2),
        ("rule", 0.1),
        ("2025 was left out: the fit gives 145.3, the actual was 144.4.", REG, 16, ds.INK_2, 0.2),
        ("rule", 0.1),
        ("Adjusted for storm days, no clear trend since 2015: about +0.3 minutes a year (95% range −1.4 to +2.1).",
         REG, 16, ds.INK_2, 0.0),
    ], BOTTOM_APX, "A2 right")
    source(s, "NOAA Storm Events and EIA-861, 2015–2025; ordinary least squares on ten annual points (exploratory).",
           "A2")
    notes(s, """Ten annual points, so the fit is a check, not a forecast. The 2025 value was left out of the fit and
    lands within a minute of it. After the storm-day adjustment, the trend since 2015 is about plus 0.3 minutes a
    year, with a range that includes zero.""")

    # ------------------------------------------------------------------ A3 ex-MED vs MED
    s = new()
    title(s, "Major event days were about half of all-event outage minutes in 2025")
    picture(s, CH / "a3_exmed_vs_med.png", L, TOP - 0.03,
            "Stacked columns 2013-2025: SAIDI excluding major event days (blue) and major-event-day minutes (grey). "
            "2025: 144.4 plus 162.3 = 306.7 minutes.")
    mshare = 162.3 / 306.7 * 100
    col(s, rx, TOP + 0.02, rw, [
        ("rule", 0.08),
        (f"{mshare:.0f}%", LIGHT, 40, ds.INK, 0.0),
        ("of 2025's all-event outage minutes fell on major event days (162.3 of 306.7)", REG, 16, ds.INK_2, 0.22),
        ("rule", 0.08),
        ("Major-event minutes swing most: 285 in 2022, 41 in 2024.", REG, 16, ds.INK_2, 0.2),
        ("Major-event minutes are EIA's all-events SAIDI minus ex-MED SAIDI, not a storm attribution.", REG, 16,
         ds.MUTED, 0.0),
    ], BOTTOM_APX, "A3 right")
    source(s, "EIA-861 / PUDL 2013–2025, Dominion Energy Virginia: SAIDI with and without major event days.", "A3")
    notes(s, """All-event SAIDI in 2025 was 306.7 minutes; 144.4 of them were on ordinary days. The headline numbers in
    this deck use the ordinary-day series, which is the one Dominion reports.""")

    # ------------------------------------------------------------------ A4 sources
    s = new()
    title(s, "Every number traces to a public source and a tested query")
    rows = [["Source", "Publisher", "Years", "Grain", "Rows"],
            ["EIA-861 Reliability, 2025 final", "EIA", "2025", "utility × state × year", "977"],
            ["PUDL EIA-861 reliability", "Catalyst Cooperative", "2013–2024", "utility × state × year", "24,358"],
            ["EIA-861 Service Territory", "EIA", "2025", "utility × county", "11,803"],
            ["NOAA Storm Events", "NOAA NCEI", "2013–2025", "storm event", "831,288"],
            ["EIA-930 hourly demand", "EIA", "Jul 2018–Oct 2026", "region × hour", "6,077,232"],
            ["Dominion Energy 2025 Annual Report", "Dominion Energy", "2025", "document (130, 133)", "reference"]]
    table(s, L, TOP + 0.02, CW, [3.9, 2.35, 2.05, 2.55, 1.283], rows, pt=16, row_h=0.42, align="lllll")
    tb(s, L, TOP + 0.02 + 0.42 * 7 + 0.25, CW, 0.7,
       [[("Tests after each load (T1–T12, all pass): ", SEMI, ds.INK),
         ("no duplicate keys; SAIDI = SAIFI × CAIDI within 2%; Dominion 2025 equals EIA's published 306.7, 144.4 and "
          "2,675,735 customers; every county mapped; full years; no duplicate hours.", REG, ds.INK_2)]], 16,
       name="A4 tests")
    source(s, "Project documentation: sources register (publisher, vintage, licence) and data-quality tests; all "
              "public data.", "A4")
    notes(s, """Every source is public and every load is tested. The rows are as loaded; the licence and vintage of
    each file are in the project's sources register.""")

    # ------------------------------------------------------------------ A5 limits
    s = new()
    title(s, "What public data cannot show, and what would answer it")
    rows = [["Public data limit", "What would answer it (Dominion data, by type)"],
            ["One number per utility per year (EIA-861)", "Outage records by event, circuit and cause"],
            ["Storms counted by county, not by line", "Outage records with cause codes and circuit location"],
            ["Methods differ between utilities", "Dominion's daily SAIDI and its filing method"],
            ["The DOM zone is wider than the retail territory", "Meter interval data by circuit"],
            ["No customer identities: growth can't be attributed", "Customer class and large-load records"]]
    table(s, L, TOP + 0.02, CW, [5.6, 6.533], rows, pt=16, row_h=0.5, align="ll")
    source(s, "Project scope limits (decision D14) and the sources above.", "A5")
    notes(s, """These are the limits I'd name before anyone else does. Each one is answered by a kind of internal data,
    named by type only.""")

    # ------------------------------------------------------------------ A6 peer table
    s = new()
    title(s, "The twelve-peer comparison, with each utility's reporting method")
    pr = sorted(peers, key=lambda d: -float(d["saifi_5yr_2021_25"]))
    rows = [["Utility", "Major-event method", "SAIFI 2021–25", "CAIDI 2021–25", "SAIDI 2023–25"]]
    hi = None
    for i, d in enumerate(pr, start=1):
        rows.append([d["utility"], d["major_event_method"], f"{float(d['saifi_5yr_2021_25']):.2f}",
                     f"{float(d['caidi_5yr_2021_25']):.0f}", f"{float(d['saidi_3yr_2023_25']):.0f}"])
        if d["utility"] == "Dominion Energy Virginia":
            hi = i
    table(s, L, TOP - 0.02, CW, [4.2, 2.6, 1.78, 1.78, 1.773], rows, pt=16, row_h=0.355, highlight=hi,
          align="llrrr")
    source(s, "EIA-861 / PUDL, excluding major event days; means of annual values; peers chosen by EIA ID before "
              "results. Sorted by SAIFI.", "A6")
    notes(s, """The full peer table. Sorted by frequency: Dominion is fourth. Methods differ, so treat the ranks as
    indicative.""")

    # ------------------------------------------------------------------ write, render, proof
    pptx = OUT / f"{STEM}.pptx"
    prs.save(pptx)
    print("saved", pptx)
    for p in PROBLEMS:
        print("  !", p)
    pdf = pipeline.pptx_to_pdf(pptx, PROOFS)
    letter = pipeline.impose_letter_landscape(pdf, OUT / f"{STEM}_print_letter.pdf", scale=ds.PRINT_SCALE)
    print("print pdf", letter)
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=110, grey=grey)
    print("min printed sizes:", pipeline.pdf_min_font_size(letter)[:16])
    print("fonts:", pipeline.pdf_fonts(letter))


if __name__ == "__main__":
    main()
