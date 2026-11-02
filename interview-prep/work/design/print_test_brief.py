"""Print test for the brief pipeline: matplotlib SVG (text kept as text) inlined in HTML ->
headless Edge -> PDF (US Letter portrait, CSS @page margin boxes for page numbers) ->
PNG proofs in colour and greyscale.

Output: interview-prep/work/proofs/print_test/
Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\design\\print_test_brief.py
"""
import csv
import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ds  # noqa: E402
import pipeline  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = ds.WORK / "proofs" / "print_test"
OUT.mkdir(parents=True, exist_ok=True)


def svg_of(fig) -> str:
    buf = io.StringIO()
    fig.savefig(buf, format="svg")
    s = buf.getvalue()
    return s[s.index("<svg"):]


def chart_svg():
    ds.use_style("brief")
    rows = {int(r["year"]): r for r in csv.DictReader(open(ds.REPO / "data/output/storm_vs_saidi.csv", encoding="utf-8"))}
    years = list(range(2015, 2026))
    saifi = [float(rows[y]["saifi_ex_med"]) for y in years]
    fig, ax = plt.subplots(figsize=(6.9, 2.4))
    fig.subplots_adjust(left=0.07, right=0.88, top=0.92, bottom=0.14)
    ax.set_xlim(2014.6, 2025.4)
    ax.set_ylim(0.9, 1.4)
    ax.set_yticks([1.0, 1.1, 1.2, 1.3, 1.4])
    ax.set_xticks(years)
    ax.plot(years, saifi, color=ds.SUBJECT, linewidth=ds.line_width("subject", "brief"))
    for y in (2019, 2023, 2025):
        v = saifi[years.index(y)]
        ax.plot(y, v, "o", color=ds.SUBJECT, markersize=ds.marker_size("brief"), markeredgecolor="white",
                markeredgewidth=1.2, zorder=4)
        ax.annotate(f"{v:.3f}" if y == 2023 else f"{v:.2f}", (y, v), xytext=(0, 7), textcoords="offset points",
                    ha="center", fontsize=ds.BRIEF["label_pt"], color=ds.INK)
    ax.set_ylabel("Interruptions per customer", labelpad=6)
    s = svg_of(fig)
    plt.close(fig)
    return s


def ramp_svg():
    # Swatches of the sequential ramp with hex and print grey, so the greyscale proof shows the ordering
    w, h = 6.9 * 72, 0.75 * 72
    n = len(ds.SEQ)
    sw = w / n
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}pt" height="{h:.1f}pt">']
    for i, c in enumerate(ds.SEQ):
        x = i * sw
        parts.append(f'<rect x="{x + 1:.1f}" y="0" width="{sw - 2:.1f}" height="{h * 0.55:.1f}" rx="2" fill="{c}"/>')
        parts.append(f'<text x="{x + sw / 2:.1f}" y="{h * 0.82:.1f}" text-anchor="middle" '
                     f'font-family="Segoe UI" font-size="7.5" fill="#6B7280">{c}</text>')
    parts.append("</svg>")
    return "".join(parts)


def pipeline_svg():
    # Drawn diagram, not text: source -> RAW -> STG -> MART -> tests -> Power BI
    steps = [("Public sources", "EIA-861 · PUDL · NOAA · EIA-930"), ("RAW", "as published, all text"),
             ("STG", "typed, cleaned"), ("MART", "facts, dimensions, views"), ("Tests", "T1–T12"),
             ("Power BI", "Import, measures")]
    w, h = 6.9 * 72, 0.95 * 72
    n = len(steps)
    gap = 14
    bw = (w - gap * (n - 1)) / n
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.1f} {h:.1f}" width="{w:.1f}pt" height="{h:.1f}pt" role="img" '
             f'aria-label="Pipeline: public sources to RAW, STG, MART, tests, then Power BI">']
    for i, (t, sub) in enumerate(steps):
        x = i * (bw + gap)
        subj = t in ("MART",)
        parts.append(f'<rect x="{x:.1f}" y="6" width="{bw:.1f}" height="{h - 12:.1f}" rx="4" '
                     f'fill="{"#E8F0FB" if subj else "#FFFFFF"}" stroke="{"#0A66C2" if subj else "#B8BCC2"}" stroke-width="1"/>')
        parts.append(f'<text x="{x + 8:.1f}" y="{h / 2 - 2:.1f}" font-family="Segoe UI" font-weight="600" font-size="9.5" fill="#1F2A44">{t}</text>')
        parts.append(f'<text x="{x + 8:.1f}" y="{h / 2 + 11:.1f}" font-family="Segoe UI" font-size="7.5" fill="#374151">{sub}</text>')
        if i < n - 1:
            ax0 = x + bw + 2
            parts.append(f'<path d="M{ax0:.1f},{h / 2:.1f} L{ax0 + gap - 5:.1f},{h / 2:.1f}" stroke="#6B7280" stroke-width="1"/>')
            parts.append(f'<path d="M{ax0 + gap - 8:.1f},{h / 2 - 3:.1f} L{ax0 + gap - 4:.1f},{h / 2:.1f} L{ax0 + gap - 8:.1f},{h / 2 + 3:.1f}" '
                         f'fill="none" stroke="#6B7280" stroke-width="1"/>')
    parts.append("</svg>")
    return "".join(parts)


def html():
    css = (HERE / "brief.css").read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Print test: brief</title>
<style>{css}</style></head>
<body>
<section class="page">
  <div class="section-no">1 · The project on one page</div>
  <h1>Outage minutes rose because customers lost power more often, not because outages lasted longer</h1>
  <p class="lede">Print test of the brief’s type scale: lede 13&nbsp;pt Semilight, body 10.5&nbsp;pt, small 8.5&nbsp;pt,
  hero figures 40&nbsp;pt Light. Figures below are the repo’s verified 2023→2025 EIA-861 values.</p>
  <div class="figures">
    <div class="figure"><div class="value">+17%</div><div class="label">SAIDI ex-MED, 123.3 → 144.4 minutes per customer</div></div>
    <div class="figure is-subject"><div class="value subject">+13%</div><div class="label">SAIFI ex-MED, 1.165 → 1.320 interruptions per customer</div></div>
    <div class="figure"><div class="value">+3%</div><div class="label">CAIDI ex-MED, 105.9 → 109.4 minutes per interruption</div></div>
  </div>
  <h2>Body text at 10.5&nbsp;pt</h2>
  <p>Dominion reported that its rolling three-year average SAIDI rose from about 130 minutes (2022–2024) to 133 minutes
  (2023–2025), excluding major event days. These are overlapping rolling averages, not two separate periods. The public
  EIA-861 data shows the same direction and lets you split the change into frequency and duration: SAIDI&nbsp;=&nbsp;SAIFI&nbsp;×&nbsp;CAIDI,
  so ln(SAIDI ratio)&nbsp;=&nbsp;ln(SAIFI ratio)&nbsp;+&nbsp;ln(CAIDI ratio).</p>
  <figure>{chart_svg()}<figcaption>SAIFI ex-MED, Dominion Energy Virginia, 2015–2025. Labels on 2019, 2023 and 2025 only.
  Source: EIA-861 (2025 final), PUDL 2015–2024; data/output/storm_vs_saidi.csv.</figcaption></figure>
  <h2>Pipeline diagram (drawn, not written)</h2>
  <figure>{pipeline_svg()}</figure>
  <h2>Sequential ramp, light to dark (greyscale proof must read in order)</h2>
  <figure>{ramp_svg()}</figure>
  <table>
    <thead><tr><th>Measure</th><th class="r">2023</th><th class="r">2025</th><th class="r">Change</th><th>What it means</th></tr></thead>
    <tbody>
      <tr><td>SAIDI ex-MED</td><td class="r">123.3</td><td class="r">144.4</td><td class="r">+17%</td><td>outage minutes per customer per year</td></tr>
      <tr class="is-subject"><td>SAIFI ex-MED</td><td class="r">1.165</td><td class="r">1.320</td><td class="r">+13%</td><td>interruptions per customer per year</td></tr>
      <tr><td>CAIDI ex-MED</td><td class="r">105.9</td><td class="r">109.4</td><td class="r">+3%</td><td>minutes per interruption</td></tr>
    </tbody>
  </table>
  <p class="note">A placeholder the candidate fills in looks like this: <span class="placeholder">[you: start date]</span>.</p>
</section>
<section class="page">
  <h1>Second page: running footer and page counter</h1>
  <p class="small">Small text at 8.5&nbsp;pt for captions and source lines. Curly quotes “like this”, an ellipsis … and a
  non-breaking space in 26,000&nbsp;MW.</p>
</section>
</body></html>"""


def main():
    page = OUT / "print_test_brief.html"
    page.write_text(html(), encoding="utf-8")
    pdf = pipeline.html_to_pdf(page, OUT / "print_test_brief.pdf")
    print("fonts:", pipeline.pdf_fonts(pdf))
    print("min sizes:", pipeline.pdf_min_font_size(pdf))
    import pymupdf
    d = pymupdf.open(str(pdf))
    print("pages:", len(d), "size:", d[0].rect)
    for grey in (False, True):
        for p in pipeline.pdf_to_pngs(pdf, OUT, dpi=100, grey=grey):
            print("png:", p)


if __name__ == "__main__":
    main()
