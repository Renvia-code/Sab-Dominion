"""Two-page handout (one sheet, front and back): the plain-English leave-behind for the panel.

Owner request, 1 Nov 2026: the 14-page deck is too much to hand over and too technical; make a
2-page version in plain language. Public version only: every fact is one the public deck already
carries (variant 'public' or 'both' in interview-prep/claims.csv). No acronyms on page 1, no
model talk, nothing about how the pack was made (O-27).

  Page 1  What I found: the question, three findings, one chart, the next question.
  Page 2  What I built: the flow, a screenshot of the candidate's own report, three checks,
          one demand box, the GitHub link.

Chart data comes from origin/main:data/output/storm_vs_saidi.csv (the public repository), and the
build asserts it equals claims row C-S4-05P.

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\handout\\build_handout.py
Out:  interview-prep/deliverables/01_deck/Dominion_handout_2page.{html,pdf}
      interview-prep/work/charts/final/h1_storm_days_and_outage_minutes.{png,svg,csv,txt}
      interview-prep/work/proofs/handout/
"""
from __future__ import annotations

import base64
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
import ds  # noqa: E402
import pipeline  # noqa: E402

OUT = ds.REPO / "interview-prep" / "deliverables" / "01_deck"
PROOFS = ds.WORK / "proofs" / "handout"
CHART_DIR = ds.CHARTS / "final"
STEM = "Dominion_handout_2page"
CHART_STEM = "h1_storm_days_and_outage_minutes"
SHOT = ds.WORK / "powerbi" / "b6" / "orig_whatmoved_saifi.png"   # the public deck's S5 screenshot (C-S5-14P)
CLAIMS = ds.REPO / "interview-prep" / "claims.csv"
EDGE_MIN_PT = 21.6   # 0.30 in from every page edge
NB = "‑"         # non-breaking hyphen, keeps EIA-861 together


def eia(n: str) -> str:
    return f"EIA{NB}{n}"


# --------------------------------------------------------------------------------------
# data
# --------------------------------------------------------------------------------------
def public_storm_rows() -> dict[int, tuple[int, float]]:
    txt = subprocess.run(["git", "-C", str(ds.REPO), "show", "origin/main:data/output/storm_vs_saidi.csv"],
                         capture_output=True, text=True, check=True).stdout
    rows = {int(r["year"]): (int(r["storm_county_days"]), float(r["saidi_ex_med"]))
            for r in csv.DictReader(io.StringIO(txt))}
    return {y: rows[y] for y in range(2015, 2026)}


def assert_matches_claim(rows) -> None:
    """C-S4-05P lists storm county-days, SAIDI ex-MED and the fit for 2015-2025, three values a year."""
    claims = {r["id"]: r for r in csv.DictReader(open(CLAIMS, encoding="utf-8"))}
    vals = [float(v) for v in claims["C-S4-05P"]["value"].split(";")]
    triples = [vals[i:i + 3] for i in range(0, len(vals), 3)]
    assert len(triples) == 11, len(triples)
    for (y, (days, mins)), (c_days, c_mins, _fit) in zip(sorted(rows.items()), triples):
        assert days == c_days and round(mins, 1) == c_mins, (y, days, mins, c_days, c_mins)
    print("chart data = origin/main storm_vs_saidi.csv = claims C-S4-05P (2015-2025)")


# --------------------------------------------------------------------------------------
# chart: two aligned bar panels, storm days above, outage minutes below, 2025 in blue
# --------------------------------------------------------------------------------------
def make_chart(rows) -> Path:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ds.use_style("brief")
    years = sorted(rows)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(7.2, 2.85), sharex=True,
                                 gridspec_kw={"hspace": 0.7})
    fig.subplots_adjust(left=0.065, right=0.99, top=0.9, bottom=0.1)
    panels = [
        (a1, [rows[y][0] for y in years], (0, 900), [0, 300, 600, 900],
         "Storm days in Dominion's Virginia counties (NOAA)", lambda v: f"{v:,}"),
        (a2, [rows[y][1] for y in years], (0, 165), [0, 50, 100, 150],
         "Minutes without power per customer, major event days left out (" + eia("861") + ")",
         lambda v: f"{v:.1f}"),
    ]
    for ax, vals, ylim, ticks, title, fmt in panels:
        ax.set_xlim(years[0] - 0.6, years[-1] + 0.6)
        ax.set_ylim(*ylim)
        ax.set_yticks(ticks)
        ax.set_yticklabels([f"{t:,}" for t in ticks])
        ax.set_title(title, loc="left", fontsize=9, color=ds.INK, fontweight="semibold", pad=7)
        for y, v in zip(years, vals):
            ds.rounded_bar(ax, y, v, 0.62, ds.SUBJECT if y == 2025 else ds.CONTEXT, radius_pt=2.2)
            if y in (2024, 2025):
                ax.annotate(fmt(v), (y, v), xytext=(0, 3), textcoords="offset points", ha="center",
                            va="bottom", fontsize=8.5, color=ds.INK,
                            fontweight="semibold" if y == 2025 else "normal")
    a2.set_xticks(years)
    a2.set_xticklabels([str(y) for y in years])
    a1.tick_params(labelbottom=False)
    return ds.save(fig, CHART_STEM, outdir=CHART_DIR,
                   data_rows=[[y, rows[y][0], rows[y][1]] for y in years],
                   header=["year", "storm_county_days", "saidi_ex_med"],
                   caption="Handout p1: storm county-days and SAIDI ex-MED by year, 2015-2025, 2025 highlighted",
                   source="NOAA Storm Events + EIA-861; origin/main data/output/storm_vs_saidi.csv; claims C-S4-05P")


def inline_svg(path: Path) -> str:
    s = path.read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>\s*", "", s)
    s = re.sub(r"<!DOCTYPE[^>]*>\s*", "", s)
    s = re.sub(r'<svg([^>]*?)\swidth="[^"]*"\s+height="[^"]*"', r'<svg\1 width="100%"', s, count=1)
    return s


# --------------------------------------------------------------------------------------
# text (every number is on the public deck; the claims rows are named beside each)
# --------------------------------------------------------------------------------------
FINDINGS = [
    ("2025 was a stormy year, and outage time rose slightly.",            # C-S2-01, C-S4-01P
     "Dominion's reported three-year average went from 130 to 133 minutes without power per customer. "
     "The figure leaves out major event days, the few extreme days utilities set aside when they report. "
     "Storm days in its Virginia counties rose from 465 in 2024 to 796 in 2025."),
    ("Allowing for storms, there is no clear trend.",                     # C-S4-02/03 (wording), C-S4-05P
     "Stormier years had more outage minutes. Judging by 2015 to 2024, a year as stormy as 2025 would "
     "have about 145.3 minutes; the actual figure was 144.4. The two move together, which does not "
     "prove that storms caused every minute."),
    ("How often, more than how long, is where Dominion differs.",         # C-S3-11P, C-S3-02P
     "Against 11 other large utilities in the Mid-Atlantic and Southeast (2021 to 2025 averages), "
     "Dominion's customers lost power more often: 1.21 times a year, 4th highest of the 12, where the "
     "median is 0.96. Each outage lasted about as long as elsewhere: 110 minutes, against a median of "
     "105. Utilities measure slightly differently, so the ranks are a guide."),
]

CHECKS = [
    ("Tested.", "12 automatic tests run after each load: no duplicate records, the three reliability "    # C-S7-05
                "measures agree with each other, and 2025 matches the figures EIA published."),
    ("Reconciled.", "Rebuilt from the filings, the three-year averages come to 130.2 and 133.0, against "  # C-S2-02
                    "the 130 and 133 Dominion reports."),
    ("Documented.", "Every table, column and decision is written down, and the comparison group of "
                    "utilities was fixed before any results were run."),
]


def page1(svg: str) -> str:
    items = "\n".join(
        f'<li><span class="n">{i}</span><div><h3>{h}</h3><p>{b}</p></div></li>'
        for i, (h, b) in enumerate(FINDINGS, 1))
    return f"""
<section class="page">
  <header>
    <div class="kicker">Independent analysis of public data</div>
    <h1>How reliable is power in Dominion Energy Virginia's territory?</h1>
    <div class="byline">Saketh Bollina · November 3, 2026</div>
  </header>
  <p class="lead">I rebuilt Dominion Energy Virginia's reliability figures from public filings and storm
  records to answer one question: was 2025 a worse year for customers, and is service getting worse over
  time?</p>
  <h2>What I found</h2>
  <ol class="findings">{items}</ol>
  <figure class="chart">
    <figcaption><strong>Stormier years had more outage minutes.</strong> Dominion Energy Virginia,
    2015 to 2025, with 2025 highlighted.</figcaption>
    {svg}
  </figure>
  <p class="next"><strong>What I'd ask next, with Dominion's own outage records:</strong> which causes
  drive the extra interruptions, and are calm-day outages rising underneath the storms?</p>
  <footer>
    <span>Public data only: {eia("861")} (via PUDL) and NOAA Storm Events; no Dominion internal data.
    Storm days count each county separately. Reported three-year figures: Dominion Energy 2025 Annual
    Report, p. 10.</span>
    <span class="pg">1 / 2</span>
  </footer>
</section>"""


def page2(shot_b64: str) -> str:
    checks = "\n".join(f"<li><strong>{h}</strong> {b}</li>" for h, b in CHECKS)
    return f"""
<section class="page">
  <header class="h2page">
    <h1>What I built</h1>
    <p class="lead">A small, tested pipeline that turns public files into a Power BI report, built the
    way I would build one for a team.</p>
  </header>
  <div class="flow">
    <div class="box"><div class="bt">Public files</div><div class="bd">{eia("861")} reliability filings ·
      NOAA storm reports · {eia("930")} hourly demand</div></div>
    <div class="arrow">→</div>
    <div class="box"><div class="bt">Snowflake (SQL)</div><div class="bd">Loads each file as published,
      cleans it, and builds the tables the report reads</div></div>
    <div class="arrow">→</div>
    <div class="box sub"><div class="bt">Power BI</div><div class="bd">One page per question, on measures
      weighted by customers</div></div>
  </div>
  <figure class="shot">
    <img src="data:image/png;base64,{shot_b64}" alt="Power BI chart from the candidate's report: outages per
customer each year, 2013 to 2025, against the 2019 level; 1.24 in 2019, 1.17 in 2023, 1.32 in 2025.">
    <figcaption>From my report: how often the average customer lost power each year, 2013 to 2025
    ({eia("861")}).</figcaption>
  </figure>
  <h2>How I made sure the numbers are right</h2>
  <ul class="checks">{checks}</ul>
  <div class="demand">
    <h3>The report also covers demand</h3>
    <p>Average demand between 3 and 4 a.m. rose 41% from 2019 to 2025; between 3 and 4 p.m., 27%. Winter,
    not summer, set the year's peak in 2019, 2022 and 2025.</p>
    <p class="small">{eia("930")} hourly data for the PJM Dominion zone, which is wider than Dominion's own
    customers.</p>
  </div>
  <p class="link">Code, SQL and documentation: <strong>github.com/saketh1433/dominion-reliability-review</strong></p>
  <footer>
    <span>Public data only: {eia("861")} (via PUDL), NOAA Storm Events and {eia("930")}; no Dominion internal
    data.</span>
    <span class="pg">2 / 2</span>
  </footer>
</section>"""


CSS = f"""
@page {{ size: Letter; margin: 0.6in 0.65in 0.55in 0.65in; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: #fff; }}
body {{ font-family: "Segoe UI", sans-serif; font-size: 10.5pt; line-height: 1.42; color: {ds.INK}; }}
.page {{ height: 9.84in; display: flex; flex-direction: column; break-after: page; overflow: hidden; }}
.page:last-child {{ break-after: auto; }}
header {{ border-bottom: 1px solid {ds.RULE}; padding-bottom: 0.1in; margin-bottom: 0.13in; }}
.kicker {{ font-size: 8.5pt; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase;
          color: {ds.SUBJECT}; }}
h1 {{ font-size: 21pt; font-weight: 600; line-height: 1.18; margin: 0.03in 0 0.04in; }}
.byline {{ font-size: 10pt; color: {ds.MUTED}; }}
.lead {{ font-size: 11pt; font-weight: 350; margin: 0 0 0.12in; }}
.h2page .lead {{ margin: 0.02in 0 0; }}
h2 {{ font-size: 13pt; font-weight: 600; margin: 0.02in 0 0.07in; }}
h3 {{ font-size: 10.5pt; font-weight: 600; margin: 0 0 0.02in; }}
p {{ margin: 0; }}
strong {{ font-weight: 600; }}
.findings {{ list-style: none; margin: 0 0 0.14in; padding: 0; }}
.findings li {{ display: flex; gap: 0.14in; margin-bottom: 0.1in; }}
.findings .n {{ flex: 0 0 0.3in; height: 0.3in; border-radius: 50%; background: {ds.SUBJECT}; color: #fff;
               font-weight: 600; font-size: 11pt; display: flex; align-items: center; justify-content: center;
               margin-top: 0.01in; }}
figure {{ margin: 0; }}
.chart figcaption, .shot figcaption {{ font-size: 9.5pt; color: {ds.MUTED}; }}
.chart figcaption strong {{ color: {ds.INK}; font-size: 10.5pt; }}
.chart svg {{ display: block; height: auto; margin-top: 0.03in; }}
.next {{ background: {ds.TINT}; border-left: 3px solid {ds.SUBJECT}; padding: 0.08in 0.12in; margin-top: 0.1in; }}
footer {{ margin-top: auto; padding-top: 0.08in; border-top: 1px solid {ds.RULE}; display: flex; gap: 0.2in;
          justify-content: space-between; font-size: 8.5pt; color: {ds.MUTED}; line-height: 1.35; }}
footer .pg {{ white-space: nowrap; }}
.flow {{ display: flex; align-items: stretch; gap: 0.08in; margin: 0.06in 0 0.16in; }}
.flow .box {{ flex: 1; border: 1px solid {ds.RULE}; border-radius: 6px; padding: 0.08in 0.1in; background: #fff; }}
.flow .box.sub {{ border-color: {ds.SUBJECT}; background: {ds.SUBJECT_TINT}; }}
.flow .bt {{ font-weight: 600; font-size: 10.5pt; }}
.flow .bd {{ font-size: 9.5pt; color: {ds.INK2 if hasattr(ds, "INK2") else "#374151"}; line-height: 1.35; }}
.flow .arrow {{ align-self: center; font-size: 16pt; color: {ds.MUTED}; }}
.shot img {{ display: block; width: 100%; border: 1px solid {ds.RULE}; border-radius: 4px; }}
.shot figcaption {{ margin-top: 0.04in; }}
.shot {{ margin-bottom: 0.16in; }}
.checks {{ margin: 0 0 0.14in; padding-left: 0.2in; }}
.checks li {{ margin-bottom: 0.05in; }}
.demand {{ background: {ds.TINT}; border-left: 3px solid {ds.THIRD}; padding: 0.08in 0.12in; margin-bottom: 0.12in; }}
.demand .small {{ font-size: 8.5pt; color: {ds.MUTED}; margin-top: 0.03in; }}
.link {{ font-size: 10.5pt; }}
"""


def build_html(svg: str, shot_b64: str) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Dominion Energy Virginia reliability: two-page handout</title>
<style>{CSS}</style></head>
<body>{page1(svg)}{page2(shot_b64)}
</body></html>"""


# --------------------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------------------
BANNED = ["SAIDI", "SAIFI", "CAIDI", "ex-MED", "IEEE", "r =", "regression", "DAX", "DuckDB", "Claude",
          " AI ", "assistant", "generated", "salary", "$"]


def claim_numbers() -> set[str]:
    nums = set()
    for r in csv.DictReader(open(CLAIMS, encoding="utf-8")):
        if r["variant"] not in ("public", "both"):
            continue
        for v in re.split(r"[;\s]", r["value"] + " " + r["exact_text"]):
            v = v.strip().strip("()+%,'\"").replace(",", "")
            if re.fullmatch(r"-?\d+(\.\d+)?", v):
                nums.add(v)
    return nums


def scan(pdf: Path) -> None:
    import pymupdf
    doc = pymupdf.open(str(pdf))
    pages = [" ".join(pg.get_text().split()) for pg in doc]
    doc.close()
    for i, t in enumerate(pages, 1):
        hits = [b for b in BANNED if b in f" {t} "]
        assert not hits, f"page {i} prints {hits}"
    text = " ".join(pages)
    nums = sorted({n.replace(",", "") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)})
    known = claim_numbers()
    years = {str(y) for y in range(2013, 2027)}
    ticks = {"0", "50", "100", "150", "300", "600", "900"}
    other = [n for n in nums if n not in known and n not in years and n not in ticks]
    print("numbers printed:", nums)
    print("not a year, a tick or a public/both claims value:", other or "none")


def main():
    import pymupdf
    OUT.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    rows = public_storm_rows()
    assert rows[2024][0] == 465 and rows[2025][0] == 796 and rows[2025][1] == 144.4, rows
    assert_matches_claim(rows)
    make_chart(rows)
    svg = inline_svg(CHART_DIR / f"{CHART_STEM}.svg")
    shot_b64 = base64.b64encode(SHOT.read_bytes()).decode("ascii")
    html = OUT / f"{STEM}.html"
    html.write_text(build_html(svg, shot_b64), encoding="utf-8")
    pdf = pipeline.html_to_pdf(html, OUT / f"{STEM}.pdf")
    n = len(pymupdf.open(str(pdf)))
    print(f"pages: {n}")
    assert n == 2, f"expected 2 pages, got {n}"
    doc = pymupdf.open(str(pdf))
    doc.set_metadata({"title": "Dominion Energy Virginia reliability", "author": "Saketh Bollina", "subject": "",
                      "keywords": "", "creator": "", "producer": ""})
    tmp = pdf.with_suffix(".tmp.pdf")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf)
    print("min sizes:", pipeline.pdf_min_font_size(pdf))
    print("fonts:", pipeline.pdf_fonts(pdf))
    doc = pymupdf.open(str(pdf))
    edges = []
    for pg in doc:
        W, H = pg.rect.width, pg.rect.height
        edges += [min(w[0], w[1], W - w[2], H - w[3]) for w in pg.get_text("words")]
    doc.close()
    print(f"min distance from a page edge: {min(edges):.2f} pt ({min(edges) / 72:.3f} in)")
    assert min(edges) >= EDGE_MIN_PT, f"text closer than 0.30 in to a page edge: {min(edges):.2f} pt"
    scan(pdf)
    doc = pymupdf.open(str(pdf))            # the footer must print on both pages (overflow is hidden)
    for i, pg in enumerate(doc, 1):
        assert f"{i} / 2" in pg.get_text(), f"page {i}: footer missing (content overflows the page)"
    doc.close()
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=110, grey=grey)
    print("proofs:", PROOFS)


if __name__ == "__main__":
    main()
