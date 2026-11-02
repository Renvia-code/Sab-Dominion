"""Safety-net v0 charts for the deck (and the v0 brief), from committed repo data only.

Inputs (all re-verified by D in work/data/reverify_2_2.md):
  data/output/storm_vs_saidi.csv          (F02, F04, F05, F06: annual SAIDI/SAIFI, storm county-days)
  data/output/dom_annual.csv              (F10, F12: DOM zone winter/summer peaks)
  powerbi/Dominion_Reliability_PowerBI_Data.xlsx, sheet Peers   (F07, F08: 12-peer 5-yr averages)
Each chart: PNG (300 dpi) + SVG + CSV snapshot + caption/source txt, sized for its slide placement
(deck) so label sizes are real slide points (>= 13.5 pt = 10.1 pt printed).

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\charts\\v0\\make_charts_v0.py
"""
import csv
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "design"))
import ds  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.transforms import offset_copy  # noqa: E402

OUT = HERE
LBL = ds.DECK["label_pt"]  # 13.5


def annual():
    rows = list(csv.DictReader(open(ds.REPO / "data/output/storm_vs_saidi.csv", encoding="utf-8")))
    return {int(r["year"]): {k: float(v) for k, v in r.items() if k != "year"} for r in rows}


def peers():
    import openpyxl
    wb = openpyxl.load_workbook(ds.REPO / "powerbi/Dominion_Reliability_PowerBI_Data.xlsx", read_only=True, data_only=True)
    rows = list(wb["Peers"].iter_rows(values_only=True))
    hdr = rows[0]
    out = []
    for r in rows[1:]:
        d = dict(zip(hdr, r))
        if d["utility"] and d["utility"] != "Appalachian Power (VA)":  # held out by decision D10
            out.append(d)
    return out


def text_at(ax, x, y, s, dx=0, dy=0, **kw):
    tr = offset_copy(ax.transData, fig=ax.figure, x=dx, y=dy, units="points")
    kw.setdefault("fontsize", LBL)
    kw.setdefault("color", ds.INK)
    return ax.text(x, y, s, transform=tr, **kw)


# ---------------------------------------------------------------- S2: % change 2023 -> 2025
def s2_change(a):
    ds.use_style("deck")
    y0, y1 = 2023, 2025
    saidi = (a[y0]["saidi_ex_med"], a[y1]["saidi_ex_med"])
    saifi = (a[y0]["saifi_ex_med"], a[y1]["saifi_ex_med"])
    caidi = (saidi[0] / saifi[0], saidi[1] / saifi[1])
    rows = [("SAIDI", "outage minutes per customer", saidi, ds.DARK),
            ("SAIFI", "interruptions per customer (how often)", saifi, ds.SUBJECT),
            ("CAIDI", "minutes per interruption (how long)", caidi, ds.CONTEXT)]
    pct = [(r[2][1] / r[2][0] - 1) * 100 for r in rows]
    fig, ax = plt.subplots(figsize=(6.6, 3.55))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.97, bottom=0.03)
    ax.set_xlim(-1, 30)
    ax.set_ylim(-0.6, 2.75)
    ax.axis("off")
    ax.figure.canvas.draw()
    for i, ((name, desc, (v0, v1), col), p) in enumerate(zip(rows, pct)):
        y = 2 - i
        ds.rounded_bar(ax, y, p, 0.36, col, horizontal=True)
        # labels: name + values above the bar, % at the tip
        fmt = "{:.3f}" if name == "SAIFI" else "{:.1f}"
        text_at(ax, 0, y + 0.24, f"{name}", va="bottom", ha="left", fontweight="semibold")
        text_at(ax, 0, y + 0.24, f"{desc}:  {fmt.format(v0)} → {fmt.format(v1)}", dx=48, va="bottom",
                ha="left", color=ds.INK_2)
        text_at(ax, p, y, f"+{p:.0f}%", dx=8, va="center", ha="left", fontweight="semibold", fontsize=LBL + 2)
    ax.plot([0, 0], [-0.35, 2.45], color=ds.BASELINE, linewidth=0.9)
    p = ds.save(fig, "s2_change_2023_2025",
                data_rows=[[r[0], round(r[2][0], 3), round(r[2][1], 3), round(x, 1)] for r, x in zip(rows, pct)],
                header=["measure", "value_2023", "value_2025", "change_pct"],
                caption="Change 2023 to 2025, Dominion Energy Virginia, excluding major event days",
                source="EIA-861 2025 final and PUDL; data/output/storm_vs_saidi.csv; D reverify F02", outdir=OUT)
    plt.close(fig)
    return p, pct


# ---------------------------------------------------------------- S2 (locked G1a): 2022 -> 2025 + SAIFI high
def s2_lock(a):
    """Two panels, one figure: (A) the change between the two years that move the 3-year average
    (2025 replaced 2022), split into SAIFI and CAIDI; (B) SAIFI by year, 2025 the 2013-2025 high."""
    ds.use_style("deck")
    y0, y1 = 2022, 2025
    saidi = (a[y0]["saidi_ex_med"], a[y1]["saidi_ex_med"])
    saifi = (a[y0]["saifi_ex_med"], a[y1]["saifi_ex_med"])
    caidi = (saidi[0] / saifi[0], saidi[1] / saifi[1])
    rows = [("SAIDI", "minutes per customer", saidi, ds.DARK, "{:.1f}"),
            ("SAIFI", "interruptions per customer", saifi, ds.SUBJECT, "{:.3f}"),
            ("CAIDI", "minutes per interruption", caidi, ds.CONTEXT, "{:.1f}")]
    pct = [(r[2][1] / r[2][0] - 1) * 100 for r in rows]
    fig = plt.figure(figsize=(6.6, 4.25))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.3, 1.0], hspace=0.42, left=0.11, right=0.97, top=0.93,
                          bottom=0.085)
    axA = fig.add_subplot(gs[0])
    axB = fig.add_subplot(gs[1])
    # panel A: % change, bars from a zero line
    axA.set_xlim(-14, 16)
    axA.set_ylim(-0.32, 3.5)
    axA.axis("off")
    fig.canvas.draw()
    for i, ((name, desc, (v0, v1), colr, fmt), p) in enumerate(zip(rows, pct)):
        y = (2 - i) * 1.3
        ds.rounded_bar(axA, y, p, 0.34, colr, horizontal=True)
        text_at(axA, -14, y + 0.3, name, va="bottom", ha="left", fontweight="semibold")
        text_at(axA, -14, y + 0.3, f"{desc}:  {fmt.format(v0)} → {fmt.format(v1)}", dx=50, va="bottom",
                ha="left", color=ds.INK_2)
        sign = "+" if p >= 0 else "−"
        text_at(axA, p, y, f"{sign}{abs(p):.0f}%", dx=7 if p >= 0 else -7, va="center",
                ha="left" if p >= 0 else "right", fontweight="semibold", fontsize=LBL + 1.5)
    for y in (0, 1.3, 2.6):  # zero line only where the bars are, so it never crosses a label
        axA.plot([0, 0], [y - 0.24, y + 0.24], color=ds.BASELINE, linewidth=0.9)
    fig.text(0.11, 0.965, "2022 → 2025, the two years that move the 3-year average", fontsize=LBL,
             fontweight="semibold", color=ds.INK, va="center", ha="left")
    # panel B: SAIFI by year
    yrs = list(range(2013, 2026))
    sv = [a[y]["saifi_ex_med"] for y in yrs]
    axB.set_xlim(2012.5, 2026.0)
    axB.set_ylim(1.0, 1.36)
    axB.set_yticks([1.0, 1.1, 1.2, 1.3])
    axB.set_xticks([2013, 2016, 2019, 2022, 2025])
    axB.plot(yrs, sv, color=ds.CONTEXT, linewidth=ds.line_width("context"), zorder=2)
    axB.scatter(yrs[:-1], sv[:-1], s=36, color=ds.CONTEXT, edgecolors="white", linewidths=1.2, zorder=3)
    axB.scatter([2025], [sv[-1]], s=110, color=ds.SUBJECT, edgecolors="white", linewidths=1.8, zorder=5)
    text_at(axB, 2025, sv[-1], f"{sv[-1]:.3f}", dx=-10, dy=2, ha="right", va="bottom", fontweight="semibold")
    text_at(axB, 2018, a[2018]["saifi_ex_med"], f"{a[2018]['saifi_ex_med']:.3f}", dy=8, ha="center",
            va="bottom", color=ds.INK_2)
    axB.set_ylabel("SAIFI", labelpad=6)
    fig.text(0.11, 0.455, "SAIFI by year: 2025 is the highest of 2013–2025", fontsize=LBL, fontweight="semibold",
             color=ds.INK, va="center", ha="left")
    assert max(sv) == sv[-1], "2025 must be the series high"
    p = ds.save(fig, "s2_lock_2022_2025_saifi",
                data_rows=[[r[0], round(r[2][0], 3), round(r[2][1], 3), round(x, 1)] for r, x in zip(rows, pct)]
                + [["SAIFI", y, v, ""] for y, v in zip(yrs, sv)],
                header=["measure", "value_2022_or_year", "value_2025_or_saifi", "change_pct"],
                caption="2022 to 2025 change in SAIDI, SAIFI, CAIDI ex-MED, and SAIFI 2013-2025; Dominion Energy Virginia",
                source="EIA-861 2025 final and PUDL; data/output/storm_vs_saidi.csv; D findings.md S2.1-S2.2", outdir=OUT)
    plt.close(fig)
    return p, pct


# ---------------------------------------------------------------- S3: peer quadrant
def s3_quadrant(pp):
    ds.use_style("deck")
    fig, ax = plt.subplots(figsize=(7.9, 4.15))
    fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.165)
    xs = [d["saifi_5yr"] for d in pp]
    ys = [d["caidi_5yr"] for d in pp]
    med_x = sorted(xs)[5:7]
    med_x = sum(med_x) / 2
    med_y = sorted(ys)[5:7]
    med_y = sum(med_y) / 2
    ax.set_xlim(0.4, 1.4)
    ax.set_ylim(60, 150)
    ax.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4])
    ax.set_yticks([60, 80, 100, 120, 140])
    ax.grid(axis="both", color=ds.GRID, linewidth=0.7)
    ax.axvline(med_x, color=ds.MUTED, linewidth=1.0, zorder=1)
    ax.axhline(med_y, color=ds.MUTED, linewidth=1.0, zorder=1)
    text_at(ax, med_x, 148, f"peer median {med_x:.2f}", dx=-5, va="top", ha="right", color=ds.MUTED)
    text_at(ax, 0.41, med_y, f"peer median {med_y:.0f} min", dy=4, va="bottom", ha="left", color=ds.MUTED)
    for d in pp:
        dom = d["utility"] == "Dominion Energy Virginia"
        ax.scatter(d["saifi_5yr"], d["caidi_5yr"], s=130 if dom else 80,
                   color=ds.SUBJECT if dom else ds.CONTEXT, edgecolors="white", linewidths=1.8,
                   zorder=5 if dom else 3)
    lab = {
        "Dominion Energy Virginia": ("Dominion\nEnergy Virginia", -12, 5, "right", "center", True),
        "Duke Carolinas (NC)": ("Duke Carolinas", -10, 0, "right", "center", False),
        "Duke Progress (NC)": ("Duke Progress", 0, 0, None, None, False),
        "Georgia Power": ("Georgia Power", 0, 0, None, None, False),
        "PPL Electric": ("PPL", 10, 0, "left", "center", False),
        "FPL": ("FPL", 10, 0, "left", "center", False),
        "Alabama Power": ("Alabama Power", 10, 0, "left", "center", False),
        "Dominion Energy SC": ("Dominion SC", 10, 0, "left", "center", False),
    }
    for d in pp:
        if d["utility"] in lab:
            t, dx, dy, ha, va, bold = lab[d["utility"]]
            if ha is None:
                continue
            tt = text_at(ax, d["saifi_5yr"], d["caidi_5yr"], t, dx=dx, dy=dy, ha=ha, va=va,
                         fontweight="semibold" if bold else "normal", color=ds.INK if bold else ds.INK_2,
                         linespacing=1.05, zorder=6)
            # labels interrupt the median rules they cross
            tt.set_bbox(dict(boxstyle="square,pad=0.12", facecolor="white", edgecolor="none"))
    # the two peers sitting on Dominion: one label below the cluster, with a leader
    gp = [d for d in pp if d["utility"] in ("Duke Progress (NC)", "Georgia Power")]
    gx = sum(d["saifi_5yr"] for d in gp) / 2
    gy = sum(d["caidi_5yr"] for d in gp) / 2
    ax.annotate("Duke Progress (NC),\nGeorgia Power", xy=(gx + 0.004, gy - 1.2), xytext=(1.392, 93),
                textcoords="data", ha="right", va="center", fontsize=LBL, color=ds.INK_2, linespacing=1.05,
                arrowprops=dict(arrowstyle="-", color=ds.MUTED, linewidth=0.8, shrinkA=3, shrinkB=4,
                                relpos=(0.75, 1.0)))
    ax.set_xlabel("Interruptions per customer per year (SAIFI), 2021–25 average", labelpad=7)
    ax.set_ylabel("Minutes per interruption (CAIDI)", labelpad=7)
    p = ds.save(fig, "s3_peer_quadrant",
                data_rows=[[d["utility"], d["standard"], d["saifi_5yr"], d["caidi_5yr"], d["saidi_2023_25"]] for d in pp],
                header=["utility", "major_event_method", "saifi_5yr_2021_25", "caidi_5yr_2021_25", "saidi_3yr_2023_25"],
                caption="12 peer utilities: SAIFI vs CAIDI, 2021-2025 averages, excluding major event days",
                source="EIA-861 / PUDL; powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers; D reverify F07-F08",
                outdir=OUT)
    plt.close(fig)
    return p, med_x, med_y


# ---------------------------------------------------------------- S4: storm days vs SAIDI
def s4_storms(a):
    ds.use_style("deck")
    yrs = list(range(2015, 2025))
    x = [a[y]["storm_county_days"] for y in yrs]
    y_ = [a[y]["saidi_ex_med"] for y in yrs]
    mx, my = sum(x) / len(x), sum(y_) / len(y_)
    sxx = sum((u - mx) ** 2 for u in x)
    sxy = sum((u - mx) * (v - my) for u, v in zip(x, y_))
    syy = sum((v - my) ** 2 for v in y_)
    b = sxy / sxx
    a0 = my - b * mx
    r = sxy / math.sqrt(sxx * syy)
    pred25 = a0 + b * a[2025]["storm_county_days"]
    fig, ax = plt.subplots(figsize=(7.9, 4.15))
    fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.165)
    ax.set_xlim(350, 900)
    ax.set_ylim(100, 160)
    ax.set_yticks([100, 120, 140, 160])
    ax.grid(axis="both", color=ds.GRID, linewidth=0.7)
    xx = [380, 880]
    ax.plot(xx, [a0 + b * u for u in xx], color=ds.MUTED, linewidth=1.2, zorder=2)
    ax.scatter(x, y_, s=80, color=ds.CONTEXT, edgecolors="white", linewidths=1.8, zorder=3)
    for yr, u, v in zip(yrs, x, y_):
        if yr in (2017, 2019, 2023, 2024):
            text_at(ax, u, v, str(yr), dx=0, dy=-12 if yr != 2019 else 10, ha="center",
                    va="top" if yr != 2019 else "bottom", color=ds.INK_2)
    x25, y25 = a[2025]["storm_county_days"], a[2025]["saidi_ex_med"]
    ax.scatter([x25], [y25], s=140, color=ds.SUBJECT, edgecolors="white", linewidths=2, zorder=5)
    text_at(ax, x25, y25, "2025", dx=9, dy=-3, ha="left", va="top", fontweight="semibold")
    text_at(ax, 893, 101.5, f"Fit 2015–2024: r = {r:.2f}, n = 10 years, R² {r * r:.2f}", ha="right",
            va="bottom", color=ds.INK_2)
    text_at(ax, 893, 101.5, f"2025 (not in the fit): {y25:.1f} actual, {pred25:.1f} from the fit", dy=19,
            ha="right", va="bottom", fontweight="semibold")
    ax.set_xlabel("Storm county-days in Dominion's Virginia counties (NOAA)", labelpad=7)
    ax.set_ylabel("SAIDI ex-MED, minutes per customer", labelpad=7)
    p = ds.save(fig, "s4_storm_days_vs_saidi",
                data_rows=[[yy, a[yy]["storm_county_days"], a[yy]["saidi_ex_med"]] for yy in range(2015, 2026)],
                header=["year", "storm_county_days", "saidi_ex_med"],
                caption=f"Storm county-days vs SAIDI ex-MED, 2015-2024 fit (r={r:.3f}); 2025 out of sample",
                source="NOAA Storm Events + EIA-861; data/output/storm_vs_saidi.csv; D reverify F04-F05", outdir=OUT)
    plt.close(fig)
    return p, r, b, a0, pred25


# ---------------------------------------------------------------- S5: winter vs summer peaks
def s5_peaks():
    ds.use_style("deck")
    rows = list(csv.DictReader(open(ds.REPO / "data/output/dom_annual.csv", encoding="utf-8")))
    data = [(int(r["yr"]), float(r["winter_peak_mw"]), float(r["summer_peak_mw"])) for r in rows if int(r["yr"]) >= 2019]
    fig, ax = plt.subplots(figsize=(7.9, 4.0))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.9, bottom=0.12)
    ax.set_xlim(2018.4, 2026.6)
    ax.set_ylim(0, 28)
    ax.set_yticks([0, 5, 10, 15, 20, 25])
    ax.set_xticks([d[0] for d in data])
    ax.set_xticklabels([str(d[0]) if d[0] < 2026 else "2026 YTD" for d in data])
    ax.figure.canvas.draw()
    w = 0.34
    for yr, wi, su in data:
        ds.rounded_bar(ax, yr - w / 2 - 0.02, wi / 1000, w, ds.SUBJECT)
        ds.rounded_bar(ax, yr + w / 2 + 0.02, su / 1000, w, ds.THIRD)
        top_is_winter = wi >= su
        v = max(wi, su) / 1000
        lab = ("W " if top_is_winter else "S ") + f"{v:.1f}"
        xpos = yr - w / 2 - 0.02 if top_is_winter else yr + w / 2 + 0.02
        text_at(ax, xpos, v, lab, dy=5, ha="center", va="bottom",
                fontweight="semibold" if top_is_winter else "normal", fontsize=LBL - 1 if False else LBL)
    ax.set_ylabel("Peak hour, GW", labelpad=6)
    # legend (two series): swatch + text in ink
    from matplotlib.patches import Rectangle
    for i, (col, t) in enumerate([(ds.SUBJECT, "W  winter peak (Dec–Feb)"), (ds.THIRD, "S  summer peak (Jun–Aug)")]):
        x0 = 0.01 + i * 0.36
        ax.add_patch(Rectangle((x0, 1.045), 0.022, 0.045, transform=ax.transAxes, color=col, clip_on=False))
        ax.text(x0 + 0.032, 1.068, t, transform=ax.transAxes, fontsize=LBL, color=ds.INK, va="center", ha="left")
    p = ds.save(fig, "s5_winter_summer_peaks",
                data_rows=[[yr, wi, su, "winter" if wi >= su else "summer"] for yr, wi, su in data],
                header=["year", "winter_peak_mw", "summer_peak_mw", "higher"],
                caption="Highest hour in winter (Dec-Feb) vs summer (Jun-Aug), PJM DOM zone; 2026 year to date "
                        "(EIA-930 files to 22 Oct 2026 per docs/01; D's F12 says 'to 30 Oct', the load date)",
                source="EIA-930; data/output/dom_annual.csv (mart.DOM_LOAD_ANNUAL); D reverify F12", outdir=OUT)
    plt.close(fig)
    return p, data


# ---------------------------------------------------------------- A3: ex-MED vs major-event-day minutes
def a3_stack(a):
    ds.use_style("deck")
    yrs = list(range(2013, 2026))
    ex = [a[y]["saidi_ex_med"] for y in yrs]
    med = [a[y]["storm_saidi"] for y in yrs]
    fig, ax = plt.subplots(figsize=(7.9, 4.0))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.9, bottom=0.12)
    ax.set_xlim(2012.4, 2026.75)
    ax.set_ylim(0, 450)
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.set_xticks([2013, 2015, 2017, 2019, 2021, 2023, 2025])
    ax.figure.canvas.draw()
    from matplotlib.patches import Rectangle, FancyBboxPatch
    w = 0.56
    gap = 1.6  # visual gap between segments, in data units of minutes (about 2 px)
    for yr, e, m in zip(yrs, ex, med):
        ax.add_patch(Rectangle((yr - w / 2, 0), w, e - gap / 2, color=ds.SUBJECT, linewidth=0, zorder=3))
        # top segment with rounded data end
        bar_bottom = e + gap / 2
        ax.add_patch(Rectangle((yr - w / 2, bar_bottom), w, max(0, m - gap / 2 - 4), color=ds.CONTEXT, linewidth=0, zorder=3))
        ax.add_patch(FancyBboxPatch((yr - w / 2, bar_bottom), w, m - gap / 2, boxstyle="round,pad=0,rounding_size=0.08",
                                    mutation_aspect=40, color=ds.CONTEXT, linewidth=0, zorder=3))
    e25, m25 = ex[-1], med[-1]
    text_at(ax, 2025, e25 + m25, f"{e25 + m25:.1f} all events", dy=5, ha="right", va="bottom", dx=14, fontweight="semibold")
    text_at(ax, 2025 + w / 2, e25 + m25 / 2, f"{m25:.1f}\nMED", dx=6, ha="left", va="center", linespacing=1.05)
    text_at(ax, 2025 + w / 2, e25 / 2, f"{e25:.1f}\nex-MED", dx=6, ha="left", va="center", linespacing=1.05,
            fontweight="semibold")
    ax.set_ylabel("Minutes per customer", labelpad=6)
    for i, (col, t) in enumerate([(ds.SUBJECT, "Excluding major event days (ex-MED)"), (ds.CONTEXT, "Major event days (MED)")]):
        x0 = 0.01 + i * 0.5
        ax.add_patch(Rectangle((x0, 1.045), 0.022, 0.045, transform=ax.transAxes, color=col, clip_on=False))
        ax.text(x0 + 0.032, 1.068, t, transform=ax.transAxes, fontsize=LBL, color=ds.INK, va="center", ha="left")
    p = ds.save(fig, "a3_exmed_vs_med",
                data_rows=[[y, e, m, round(e + m, 1), round(m / (e + m), 3)] for y, e, m in zip(yrs, ex, med)],
                header=["year", "saidi_ex_med", "major_event_day_minutes", "saidi_all", "med_share"],
                caption="SAIDI ex-MED and major-event-day minutes, Dominion Energy Virginia, 2013-2025",
                source="EIA-861 / PUDL; data/output/storm_vs_saidi.csv (storm_saidi = all events minus ex-MED); D reverify F06",
                outdir=OUT)
    plt.close(fig)
    return p


def main():
    a = annual()
    pp = peers()
    _, pct = s2_change(a)
    _, pct_lock = s2_lock(a)
    print("S2 lock pct 2022->2025:", [round(x, 1) for x in pct_lock])
    _, mx, my = s3_quadrant(pp)
    _, r, b, a0, pred = s4_storms(a)
    _, peaks = s5_peaks()
    a3_stack(a)
    print("S2 pct:", [round(x, 1) for x in pct])
    print(f"S3 medians: SAIFI {mx:.3f}  CAIDI {my:.2f}")
    print(f"S4 fit: r={r:.3f} r2={r*r:.3f} slope={b:.4f} intercept={a0:.2f} pred2025={pred:.2f}")
    print("S5:", peaks)


if __name__ == "__main__":
    main()
