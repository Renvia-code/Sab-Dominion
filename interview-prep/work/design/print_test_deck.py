"""Print test for the deck pipeline: chart PNGs -> PPTX (python-pptx) -> LibreOffice PDF ->
US Letter landscape imposition -> PNG proofs in colour and greyscale.

Uses real, already-verified repo figures (data/output/storm_vs_saidi.csv) so the test
shows real label lengths. Output: interview-prep/work/proofs/print_test/
Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\design\\print_test_deck.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ds  # noqa: E402
import pipeline  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR  # noqa: E402
from pptx.util import Inches, Pt  # noqa: E402

OUT = ds.WORK / "proofs" / "print_test"
OUT.mkdir(parents=True, exist_ok=True)


def rgb(h):
    h = h.lstrip("#")
    return RGBColor(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def load_series():
    rows = list(csv.DictReader(open(ds.REPO / "data" / "output" / "storm_vs_saidi.csv", encoding="utf-8")))
    return {int(r["year"]): r for r in rows}


def chart_bars(data, w_in, h_in):
    ds.use_style("deck")
    years = [y for y in range(2015, 2026)]
    vals = [float(data[y]["saidi_ex_med"]) for y in years]
    fig, ax = plt.subplots(figsize=(w_in, h_in))
    fig.subplots_adjust(left=0.09, right=0.98, top=0.93, bottom=0.13)
    ax.set_xlim(2014.4, 2025.6)
    ax.set_ylim(0, 170)
    ax.set_yticks([0, 50, 100, 150])
    ax.set_xticks([2015, 2017, 2019, 2021, 2023, 2025])
    for y, v in zip(years, vals):
        ds.rounded_bar(ax, y, v, 0.56, ds.SUBJECT if y in (2023, 2025) else ds.CONTEXT)
    for y in (2023, 2025):
        v = float(data[y]["saidi_ex_med"])
        ax.annotate(f"{v:.1f}", (y, v), xytext=(0, 6), textcoords="offset points", ha="center",
                    va="bottom", color=ds.INK, fontsize=ds.DECK["label_pt"], fontweight="semibold")
    ax.set_ylabel("Minutes per customer", labelpad=8)
    p = ds.save(fig, "test_bars", outdir=OUT,
                data_rows=[[y, v] for y, v in zip(years, vals)], header=["year", "saidi_ex_med"],
                caption="SAIDI ex-MED by year, Dominion Energy Virginia",
                source="EIA-861 (2025 final) and PUDL 2015-2024; data/output/storm_vs_saidi.csv")
    plt.close(fig)
    return p


def chart_lines(data, w_in, h_in):
    ds.use_style("deck")
    years = list(range(2015, 2026))
    saifi = [float(data[y]["saifi_ex_med"]) for y in years]
    saidi = [float(data[y]["saidi_ex_med"]) for y in years]
    caidi = [a / b for a, b in zip(saidi, saifi)]
    idx = lambda s: [v / s[0] * 100 for v in s]  # noqa: E731
    fig, ax = plt.subplots(figsize=(w_in, h_in))
    fig.subplots_adjust(left=0.11, right=0.80, top=0.93, bottom=0.13)
    ax.set_xlim(2014.6, 2025.4)
    ax.set_ylim(80, 130)
    ax.set_xticks([2015, 2019, 2023, 2025])
    ax.axhline(100, color=ds.BASELINE, linewidth=0.9, zorder=1)
    series = [("CAIDI", idx(caidi), ds.CONTEXT, "context"),
              ("SAIDI", idx(saidi), ds.DARK, "context"),
              ("SAIFI", idx(saifi), ds.SUBJECT, "subject")]
    for name, s, col, kind in series:
        ax.plot(years, s, color=col, linewidth=ds.line_width(kind), zorder=3 if kind == "subject" else 2)
        ax.plot(years[-1], s[-1], "o", color=col, markersize=ds.marker_size(), markeredgecolor="white",
                markeredgewidth=1.6, zorder=4)
        ds.end_label(ax, years[-1], s[-1], f"{name} {s[-1]:.0f}",
                     weight="semibold" if kind == "subject" else "normal")
    ax.set_ylabel("Index, 2015 = 100", labelpad=8)
    p = ds.save(fig, "test_lines", outdir=OUT,
                data_rows=[[y, a, b, c] for y, a, b, c in zip(years, idx(saifi), idx(saidi), idx(caidi))],
                header=["year", "saifi_idx", "saidi_idx", "caidi_idx"],
                caption="SAIFI, SAIDI, CAIDI ex-MED, 2015 = 100", source="EIA-861 and PUDL")
    plt.close(fig)
    return p


def add_text(slide, x, y, w, h, text, size, color=ds.INK, font=ds.FONT, bold=False, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.08):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    paras = text if isinstance(text, list) else [text]
    for i, t in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        r = p.add_run()
        r.text = t
        r.font.size = Pt(size)
        r.font.name = font
        r.font.bold = bold
        r.font.color.rgb = rgb(color)
    return tb


def build_pptx(bars_png, lines_png):
    prs = Presentation()
    prs.slide_width = Inches(ds.SLIDE_W_IN)
    prs.slide_height = Inches(ds.SLIDE_H_IN)
    blank = prs.slide_layouts[6]
    M = ds.DECK

    # Slide 1: title
    s = prs.slides.add_slide(blank)
    add_text(s, M["margin_l"], 2.2, 10.5, 1.6,
             "Dominion Energy Virginia reliability: what public data shows, and where I’d look first",
             36, font=ds.FONT_SEMIBOLD, line_spacing=1.04)
    add_text(s, M["margin_l"], 4.15, 10, 0.5, "Independent analysis of public data", 18, color=ds.INK_2)
    add_text(s, M["margin_l"], 6.35, 6, 0.4, "Print test · design system v0", M["source_pt"], color=ds.MUTED)
    s.notes_slide.notes_text_frame.text = "Test notes: talk track goes here."

    # Slide 2: content layout test (KPI column + two charts + so-what + source)
    s = prs.slides.add_slide(blank)
    add_text(s, M["margin_l"], M["margin_t"], 12.1, 1.0,
             "Outage minutes rose 17% from 2023 to 2025, and most of the rise came from more frequent interruptions",
             M["title_pt"], font=ds.FONT_SEMIBOLD, line_spacing=1.02)
    # KPI tiles
    kx, ky = M["margin_l"], 1.85
    for i, (val, lab) in enumerate([("144.4", "SAIDI ex-MED 2025, minutes"),
                                    ("1.32", "SAIFI ex-MED 2025, interruptions"),
                                    ("109.4", "CAIDI ex-MED 2025, minutes")]):
        y = ky + i * 1.38
        add_text(s, kx, y, 2.6, 0.75, val, M["kpi_pt"], font=ds.FONT_LIGHT, color=ds.SUBJECT if i == 1 else ds.INK,
                 line_spacing=0.9)
        add_text(s, kx, y + 0.82, 2.6, 0.4, lab, M["kpi_label_pt"], color=ds.INK_2)
    s.shapes.add_picture(str(bars_png), Inches(3.45), Inches(1.8), width=Inches(4.9), height=Inches(3.6))
    s.shapes.add_picture(str(lines_png), Inches(8.45), Inches(1.8), width=Inches(4.3), height=Inches(3.6))
    add_text(s, M["margin_l"], 5.72, 12.1, 0.6,
             "For Dominion: the first place to look is what drives interruption frequency on the worst circuits.",
             M["lead_pt"], color=ds.INK)
    add_text(s, M["margin_l"], 6.62, 10.6, 0.4,
             "Source: EIA-861 (2025 final) and PUDL 2015–2024, Dominion Energy Virginia, ex-MED. "
             "Table data/output/storm_vs_saidi.csv. Body 16 pt, labels 13.5 pt (12 and 10.1 pt printed).",
             M["source_pt"], color=ds.MUTED)
    add_text(s, 12.1, 6.62, 0.63, 0.4, "2", M["source_pt"], color=ds.MUTED, align=PP_ALIGN.RIGHT)
    s.notes_slide.notes_text_frame.text = "Test notes for slide 2."
    p = OUT / "print_test_deck.pptx"
    prs.save(str(p))
    return p


def main():
    data = load_series()
    bars = chart_bars(data, 4.9, 3.6)
    lines = chart_lines(data, 4.3, 3.6)
    pptx = build_pptx(bars, lines)
    pdf = pipeline.pptx_to_pdf(pptx, OUT)
    letter = pipeline.impose_letter_landscape(pdf, OUT / "print_test_deck_letter.pdf", scale=ds.PRINT_SCALE)
    print("fonts in slide PDF:", pipeline.pdf_fonts(pdf))
    print("min text size per page (printed pt):", pipeline.pdf_min_font_size(pdf, scale=ds.PRINT_SCALE))
    for grey in (False, True):
        for p in pipeline.pdf_to_pngs(letter, OUT, dpi=110, grey=grey):
            print("png:", p)


if __name__ == "__main__":
    main()
