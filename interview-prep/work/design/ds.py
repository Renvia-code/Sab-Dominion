"""Design system for the interview pack: one module shared by every chart, deck and print script.

Colour meanings come from docs/00_conventions.md. Values were checked with
palette_tools.py (OKLCH, contrast on white, greyscale level) and the dataviz
validator (see palette.md in this folder). One type family: Segoe UI.

Import from a script in interview-prep/work/...:
    import sys; sys.path.insert(0, r"<repo>/interview-prep/work/design"); import ds
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

try:  # python -I ignores PYTHONIOENCODING; keep console output safe for arrows and dashes
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

REPO = Path(__file__).resolve().parents[3]
WORK = REPO / "interview-prep" / "work"
CHARTS = WORK / "charts"

# --------------------------------------------------------------------------------------
# Colour (hex). Data colours carry meaning; chrome colours never carry data.
# --------------------------------------------------------------------------------------
SUBJECT = "#0A66C2"        # Dominion, or the series the title is about (conventions)
CONTEXT = "#B8BCC2"        # peers, other years, other series (conventions)
CONTEXT_2 = "#6B7280"      # conventions "second context": text, reference lines, medians only.
                           # Never a data fill beside SUBJECT: same grey level in a greyscale print
THIRD_PBI = "#E8B117"      # conventions third category (Power BI theme keeps this value)
THIRD = "#D5A20B"          # the same gold snapped into the dataviz light band for printed marks
DARK = "#1F2A44"           # dark accent: headings, ink, call-out marks

INK = "#1F2A44"            # primary text (14.3:1 on white)
INK_2 = "#374151"          # secondary text (10.3:1)
MUTED = "#6B7280"          # axis ticks, source lines, captions (4.8:1)
RULE = "#D1D5DB"           # dividers, table rules
GRID = "#E5E7EB"           # chart gridlines (hairline, solid)
BASELINE = "#B8BCC2"       # chart baseline / zero line
TINT = "#F3F6FA"           # panel background (prints as near-white)
SUBJECT_TINT = "#E8F0FB"   # highlighted table row (conventions Row colour)
WHITE = "#FFFFFF"

# One-hue sequential ramp from the subject blue (OKLCH hue 254.7), light -> dark.
# Lightness falls monotonically, so it also reads as an ordered grey ramp in greyscale.
SEQ = ["#EAF3FE", "#C9E0FE", "#AACAF4", "#86B1E8", "#6298DC",
       "#3C7ECF", "#0A66C2", "#00519F", "#013C78"]
# Five-class choropleth / heatmap classes (greyscale L* 88, 71, 52, 35, 25)
SEQ5 = [SEQ[1], SEQ[3], SEQ[5], SEQ[7], SEQ[8]]
NO_DATA = "#FFFFFF"        # counties outside scope: white with a RULE outline (+ hatch where needed)

# --------------------------------------------------------------------------------------
# Type: one family, Segoe UI (static files on every Windows 10/11 machine; LibreOffice,
# Edge and PowerPoint all resolve it). Weights in use: Light 300, Semilight 350,
# Regular 400, Semibold 600.
# --------------------------------------------------------------------------------------
FONT = "Segoe UI"
FONT_LIGHT = "Segoe UI Light"         # PPTX family names for weights
FONT_SEMILIGHT = "Segoe UI Semilight"
FONT_SEMIBOLD = "Segoe UI Semibold"

# --------------------------------------------------------------------------------------
# Deck geometry (16:9 slide, printed on US Letter landscape at 0.75 scale:
# 10.0 x 5.625 in, centred, 0.5 in side margins). All sizes below are SLIDE points.
# Printed size = slide size x 0.75.
# --------------------------------------------------------------------------------------
SLIDE_W_IN, SLIDE_H_IN = 13.333, 7.5
PRINT_SCALE = 0.75
DECK = {
    "margin_l": 0.6, "margin_r": 0.6, "margin_t": 0.48, "margin_b": 0.42,
    "title_pt": 28,          # action title, Semibold, sentence case (21 pt printed)
    "body_pt": 16,           # minimum body (12 pt printed)
    "lead_pt": 18,           # "what it means" line
    "label_pt": 13.5,        # minimum chart label at placement size (10.1 pt printed)
    "source_pt": 13.5,       # source line (10.1 pt printed)
    "kpi_pt": 54,            # stat-tile value, Light
    "kpi_label_pt": 15,
}

# --------------------------------------------------------------------------------------
# Brief and question-sheet geometry (US Letter portrait). Sizes in print points.
# --------------------------------------------------------------------------------------
BRIEF = {"body_pt": 10.5, "small_pt": 8.5, "label_pt": 8.5, "h1_pt": 24, "h2_pt": 13.5}
QSHEET = {"body_pt": 8.5, "question_pt": 8.5, "group_pt": 9.5}


# --------------------------------------------------------------------------------------
# matplotlib style
# --------------------------------------------------------------------------------------
def use_style(medium: str = "deck"):
    """Apply the chart style. medium='deck' sizes text for a slide; 'brief' for the PDF."""
    import matplotlib as mpl

    label = DECK["label_pt"] if medium == "deck" else BRIEF["label_pt"]
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": [FONT, "DejaVu Sans"],
        "font.size": label,
        "font.weight": "normal",
        "text.color": INK,
        "axes.labelcolor": MUTED,
        "axes.labelsize": label,
        "axes.titlesize": label,
        "axes.edgecolor": BASELINE,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.bottom": True,
        "axes.grid": True,
        "axes.grid.axis": "y",
        "axes.axisbelow": True,
        "grid.color": GRID,
        "grid.linewidth": 0.7,
        "grid.linestyle": "-",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelsize": label,
        "ytick.labelsize": label,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "xtick.major.pad": 6,
        "ytick.major.pad": 6,
        "legend.frameon": False,
        "legend.fontsize": label,
        "figure.facecolor": WHITE,
        "axes.facecolor": WHITE,
        "savefig.facecolor": WHITE,
        "svg.fonttype": "none",        # keep text as text in SVG (Edge renders Segoe UI)
        "pdf.fonttype": 42,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
    })
    return label


def line_width(kind: str = "subject", medium: str = "deck") -> float:
    """Line widths in points: subject 2.6 / context 1.6 on a slide (about 2 / 1.2 printed)."""
    base = {"subject": 2.6, "context": 1.6, "ref": 1.0}[kind]
    return base if medium == "deck" else base * 0.6


def marker_size(medium: str = "deck") -> float:
    """Marker diameter in points (>= 8 px on screen); ringed with a white edge."""
    return 9.0 if medium == "deck" else 5.5


def rounded_bar(ax, x, height, width, color, radius_pt=3.0, horizontal=False, zorder=3):
    """A bar with a rounded data-end and a square baseline (dataviz mark spec).

    Call after the axis limits are final: the radius is converted from points to data
    units using the current transform.
    """
    from matplotlib.patches import FancyBboxPatch, Rectangle

    fig = ax.figure
    fig.canvas.draw_idle()
    bbox = ax.get_window_extent()
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    px_per_pt = fig.dpi / 72.0
    dx_per_pt = (x1 - x0) / (bbox.width / px_per_pt)
    dy_per_pt = (y1 - y0) / (bbox.height / px_per_pt)
    if not horizontal:
        r_x = radius_pt * dx_per_pt
        r_y = radius_pt * dy_per_pt
        r_y = min(r_y, abs(height) / 2) if height else 0
        left = x - width / 2
        body = FancyBboxPatch((left, 0), width, height,
                              boxstyle=f"round,pad=0,rounding_size={r_x}",
                              mutation_aspect=(r_y / r_x) if r_x else 1,
                              linewidth=0, facecolor=color, zorder=zorder)
        ax.add_patch(body)
        sq_h = max(0.0, height - r_y) if height >= 0 else min(0.0, height + r_y)
        ax.add_patch(Rectangle((left, 0), width, sq_h, linewidth=0, facecolor=color, zorder=zorder))
    else:
        r_x = radius_pt * dx_per_pt
        r_y = radius_pt * dy_per_pt
        r_x = min(r_x, abs(height) / 2) if height else 0
        bottom = x - width / 2
        body = FancyBboxPatch((0, bottom), height, width,
                              boxstyle=f"round,pad=0,rounding_size={r_y}",
                              mutation_aspect=1,
                              linewidth=0, facecolor=color, zorder=zorder)
        # rounding_size is in x units after aspect; approximate with min of both radii
        body.set_boxstyle(f"round,pad=0,rounding_size={min(r_x, r_y) if r_y else r_x}")
        ax.add_patch(body)
        sq_w = max(0.0, height - r_x)
        ax.add_patch(Rectangle((0, bottom), sq_w, width, linewidth=0, facecolor=color, zorder=zorder))


def end_label(ax, x, y, text, color=INK, dx_pt=8, weight="normal", size=None, va="center"):
    """Direct label placed to the right of a line end; text wears ink, never the series colour."""
    from matplotlib.transforms import offset_copy

    tr = offset_copy(ax.transData, fig=ax.figure, x=dx_pt, y=0, units="points")
    return ax.text(x, y, text, transform=tr, color=color, ha="left", va=va,
                   fontweight=weight, fontsize=size)


def check_layout(fig, stem: str = "") -> list[str]:
    """Label QA: report text-on-text overlaps, text on a scatter marker, and text outside the
    figure. Printed as warnings by save(); an empty list means no collisions were found."""
    from matplotlib.text import Text

    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    W, H = fig.bbox.width, fig.bbox.height
    texts = []
    for ax in fig.axes:
        cands = list(ax.texts)
        if ax.axison:
            cands += [ax.xaxis.label, ax.yaxis.label]
            cands += list(ax.get_xticklabels()) + list(ax.get_yticklabels())
        for t in cands:
            if not t.get_visible() or not t.get_text().strip():
                continue
            bb = Text.get_window_extent(t, r)  # text only (an Annotation's own extent adds its arrow)
            if bb.width > 0:
                texts.append((t.get_text().replace("\n", " ")[:32], bb))
    for t in fig.texts:
        if t.get_text().strip():
            texts.append((t.get_text()[:32], t.get_window_extent(r)))
    probs = []
    for i, (n1, b1) in enumerate(texts):
        if b1.x0 < -1 or b1.y0 < -1 or b1.x1 > W + 1 or b1.y1 > H + 1:
            probs.append(f"outside figure: {n1!r}")
        for n2, b2 in texts[i + 1:]:
            if b1.overlaps(b2):
                probs.append(f"text overlap: {n1!r} x {n2!r}")
    px = fig.dpi / 72.0
    for ax in fig.axes:
        for coll in ax.collections:
            offs = coll.get_offsets()
            sizes = coll.get_sizes()
            if offs is None or len(offs) == 0 or len(sizes) == 0:
                continue
            pts = coll.get_offset_transform().transform(offs)
            for k, (xp, yp) in enumerate(pts):
                rad = (sizes[k] if len(sizes) > k else sizes[0]) ** 0.5 / 2 * px
                for n, bb in texts:
                    cx, cy = min(max(xp, bb.x0), bb.x1), min(max(yp, bb.y0), bb.y1)
                    if (cx - xp) ** 2 + (cy - yp) ** 2 < rad ** 2:
                        probs.append(f"text on marker: {n!r} at ({offs[k][0]:.4g}, {offs[k][1]:.4g})")
    for p in probs:
        print(f"  [{stem}] {p}")
    return probs


def save(fig, stem: str, data_rows=None, header=None, caption: str = "", source: str = "",
         outdir: Path | None = None, dpi: int = 300):
    """Write <stem>.png (300 dpi), <stem>.svg, <stem>.csv (data snapshot) and <stem>.txt
    (caption + source line) so every chart can be reproduced and audited."""
    outdir = outdir or CHARTS
    outdir.mkdir(parents=True, exist_ok=True)
    check_layout(fig, stem)
    fig.savefig(outdir / f"{stem}.png", dpi=dpi)
    fig.savefig(outdir / f"{stem}.svg")
    if data_rows is not None:
        with open(outdir / f"{stem}.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if header:
                w.writerow(header)
            w.writerows(data_rows)
    (outdir / f"{stem}.txt").write_text(f"caption: {caption}\nsource: {source}\n", encoding="utf-8")
    return outdir / f"{stem}.png"


def fmt_int(v) -> str:
    return f"{int(round(v)):,}"


def pct(a, b, digits=0) -> str:
    """Signed percent change from a to b, e.g. '+17%'."""
    v = (b / a - 1) * 100
    return f"{v:+.{digits}f}%"
