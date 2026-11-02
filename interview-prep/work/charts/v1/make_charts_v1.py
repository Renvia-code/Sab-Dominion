"""v1 charts for S4 (storm county-days composite) and S5 (24-hour growth profile), from D's batch-2 tables.

Inputs (D, data/output/ unless noted; findings in work/data/findings.md A1-A4, E1):
  interview-prep/work/data/output/a1_storm_vs_calm.csv   A1 storm vs calm county-days (ratio, bootstrap CI)
  county_outage_map.csv + va_counties.geojson            A3 map table (map_flag = 'ok': 99 counties)
  dim_county.csv                                         independent-city flag (draw order)
  fct_restoration_curve.csv + outage_events_top10.csv    A2 Isaias curve, h50/h90
  dom_load_profile.csv                                   A4.1 hour-of-day growth 2019 -> 2025
  dom_seasonal_peak.csv                                  A4.2 winter vs summer peaks (2026 to 29 Oct, E1)
Each chart: PNG (300 dpi) + SVG + CSV snapshot + caption/source txt (ds.save), label QA by ds.check_layout.

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\charts\\v1\\make_charts_v1.py
"""
import csv
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "design"))
import ds  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import PathPatch, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402
from matplotlib.transforms import offset_copy  # noqa: E402

OUT = HERE
LBL = ds.DECK["label_pt"]  # 13.5
DATA = ds.REPO / "data" / "output"
WDATA = ds.WORK / "data" / "output"
PHI0 = math.radians(37.6)  # projection: x = lon * cos(37.6 deg), y = lat (equirectangular, fine at state scale)

# map classes: outage minutes per customer on non-major days, 2015-2024 average (D A3)
BREAKS = [150, 250, 350, 500]
CLASS_LABELS = ["under 150", "150–250", "250–350", "350–500", "500 or more"]


def text_at(ax, x, y, s, dx=0, dy=0, **kw):
    tr = offset_copy(ax.transData, fig=ax.figure, x=dx, y=dy, units="points")
    kw.setdefault("fontsize", LBL)
    kw.setdefault("color", ds.INK)
    return ax.text(x, y, s, transform=tr, **kw)


def read(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


# ---------------------------------------------------------------- A1 headline numbers
def a1():
    rows = {r["subset"]: r for r in read(WDATA / "a1_storm_vs_calm.csv")}
    allr = rows["All complete county-days, 2015-2025"]
    years = {int(k): float(v["ratio"]) for k, v in rows.items() if k.isdigit()}
    out = {
        "ratio": float(allr["ratio"]), "lo": float(allr["ci_low"]), "hi": float(allr["ci_high"]),
        "storm_days": int(allr["storm_county_days"]), "calm_days": int(allr["calm_county_days"]),
        "mean_storm": float(allr["mean_storm_ch_per_1k"]), "mean_calm": float(allr["mean_calm_ch_per_1k"]),
        "non_med": float(rows["Excluding proxy major event days"]["ratio"]),
        "dom_only": float(rows["Dominion-only counties"]["ratio"]),
        "year_min": min(years.values()), "year_max": max(years.values()), "years": years,
    }
    assert round(out["ratio"], 1) == 11.9 and round(out["lo"], 1) == 7.9 and round(out["hi"], 1) == 16.9
    assert out["storm_days"] == 6108 and all(v > 1 for v in years.values()) and len(years) == 11
    return out


# ---------------------------------------------------------------- geometry
def rings(geom):
    polys = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    for poly in polys:
        for ring in poly:
            yield [(lon * math.cos(PHI0), lat) for lon, lat in ring]


def ring_path(rs):
    verts, codes = [], []
    for r in rs:
        verts += r + [r[0]]
        codes += [MPath.MOVETO] + [MPath.LINETO] * (len(r) - 1) + [MPath.CLOSEPOLY]
    return MPath(verts, codes)


def centroid(rs):
    """Area-weighted centroid of the largest ring (good enough for a leader line)."""
    best = max(rs, key=lambda r: abs(_area(r)))
    a = _area(best)
    cx = sum((x0 + x1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(best, best[1:] + best[:1])) / (6 * a)
    cy = sum((y0 + y1) * (x0 * y1 - x1 * y0) for (x0, y0), (x1, y1) in zip(best, best[1:] + best[:1])) / (6 * a)
    return cx, cy


def _area(r):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(r, r[1:] + r[:1])) / 2


def klass(v):
    for i, b in enumerate(BREAKS):
        if v < b:
            return i
    return len(BREAKS)


# ---------------------------------------------------------------- S4 composite: county map + Isaias inset
def s4_composite():
    ds.use_style("deck")
    geo = json.load(open(DATA / "va_counties.geojson", encoding="utf-8"))
    cmap = {r["county_fips"]: r for r in read(DATA / "county_outage_map.csv")}
    city = {r["county_fips"]: r["is_independent_city"] == "True" for r in read(DATA / "dim_county.csv")}
    ok = {k: float(r["minutes_non_med_avg_2015_24"]) for k, r in cmap.items() if r["map_flag"] == "ok"}
    flagged = [r["county_label"] for r in cmap.values() if r["map_flag"] != "ok"]
    assert len(ok) == 99 and len(flagged) == 4 and len(cmap) == 103
    counts = [0] * 5
    for v in ok.values():
        counts[klass(v)] += 1

    fig = plt.figure(figsize=(8.3, 4.15))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_aspect("equal")
    ax.axis("off")
    feats = sorted(geo["features"], key=lambda f: city.get(f["properties"]["county_fips"], False))
    cents = {}
    xs, ys = [], []
    for f in feats:
        fips = f["properties"]["county_fips"]
        rs = list(rings(f["geometry"]))
        for r in rs:
            xs += [p[0] for p in r]
            ys += [p[1] for p in r]
        cents[fips] = centroid(rs)
        if fips in ok:
            fc, ec, lw = ds.SEQ5[klass(ok[fips])], ds.WHITE, 0.35
        elif fips in cmap:      # a Dominion county left off the map (unusable EAGLE-I data)
            fc, ec, lw = ds.WHITE, ds.MUTED, 0.5
        else:                   # not a Dominion county
            fc, ec, lw = ds.WHITE, ds.RULE, 0.5
        ax.add_patch(PathPatch(ring_path(rs), facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    ax.set_xlim(x0 - 0.02, x1 + 0.06)
    ax.set_ylim(y0 - 0.42, y1 + 0.32)
    fig.canvas.draw()

    # label the extremes among counties with 20,000+ customers (D A3), under the southern border
    big = {k: v for k, v in ok.items() if float(cmap[k]["customers_basis"]) >= 20000}
    hi_k = max(big, key=big.get)
    cx, cy = cents[hi_k]
    name = cmap[hi_k]["county_label"].replace(" County", "")
    ax.annotate(f"{name} {big[hi_k]:.0f}", xy=(cx, cy), xytext=(cx + 0.25, y0 - 0.3), textcoords="data",
                ha="left", va="center", fontsize=LBL, color=ds.INK, fontweight="semibold",
                arrowprops=dict(arrowstyle="-", color=ds.INK_2, linewidth=0.8, shrinkA=2, shrinkB=0,
                                relpos=(0.0, 0.5)), zorder=6)

    # legend, top right (over Maryland and the bay; no Virginia county there)
    lx = x1 - 1.36
    ly = y1 + 0.2
    text_at(ax, lx, ly, "Minutes per customer", ha="left", va="center", fontweight="semibold")
    sw = 0.13
    for i in range(5):
        yy = ly - 0.22 - i * 0.19
        ax.add_patch(Rectangle((lx, yy - 0.065), sw * 1.1, 0.13, facecolor=ds.SEQ5[i], edgecolor="none", zorder=4))
        text_at(ax, lx + sw * 1.1, yy, CLASS_LABELS[i], dx=5, ha="left", va="center", color=ds.INK_2)

    # inset: Isaias restoration curve, top left (over West Virginia and Kentucky)
    curve = [r for r in read(DATA / "fct_restoration_curve.csv") if r["event_key"].endswith("2020-08-04 07:45:00")]
    ev = [r for r in read(DATA / "outage_events_top10.csv") if r["tropical_cyclone"] == "ISAIAS"][0]
    h50, h90 = float(ev["hours_to_50pct"]), float(ev["hours_to_90pct"])
    hx = [float(r["hour_since_peak"]) for r in curve if float(r["hour_since_peak"]) <= 96]
    hy = [float(r["share_restored"]) * 100 for r in curve if float(r["hour_since_peak"]) <= 96]
    # inset axes placed in data coordinates of the map
    def fig_xy(x, y):
        return fig.transFigure.inverted().transform(ax.transData.transform((x, y)))
    (fx0, fy0), (fx1, fy1) = fig_xy(x0 + 0.62, y1 - 1.26), fig_xy(x0 + 2.55, y1 - 0.08)
    ia = fig.add_axes([fx0, fy0, fx1 - fx0, fy1 - fy0])
    ia.set_xlim(0, 96)
    ia.set_ylim(0, 100)
    ia.set_xticks([0, 24, 48, 72, 96])
    ia.set_yticks([0, 50, 100])
    ia.set_yticklabels(["0", "50", "100%"])
    ia.grid(axis="y", color=ds.GRID, linewidth=0.7)
    ia.plot(hx, hy, color=ds.SUBJECT, linewidth=ds.line_width("subject"), zorder=3)
    ia.scatter([h90], [90], s=46, color=ds.SUBJECT, edgecolors="white", linewidths=1.4, zorder=5)
    text_at(ia, h90, 90, f"90% after {h90:.1f} h", dx=7, dy=-4, ha="left", va="top", fontweight="semibold")
    ia.set_xlabel("Hours after the peak", labelpad=4)
    fig.canvas.draw()
    bb = ia.get_tightbbox(fig.canvas.get_renderer()).transformed(fig.transFigure.inverted())
    fig.text(bb.x0, fy1 + 0.035, "Isaias, Aug 2020: share restored", fontsize=LBL, fontweight="semibold",
             color=ds.INK, ha="left", va="bottom")

    rows = [[k, cmap[k]["county_label"], cmap[k]["customers_basis"], ok[k], CLASS_LABELS[klass(ok[k])]]
            for k in sorted(ok)]
    p = ds.save(fig, "s4_county_map_isaias",
                data_rows=rows + [["isaias_curve", "hour", h, round(v, 1), ""] for h, v in zip(hx, hy)],
                header=["county_fips", "county", "customers_basis", "minutes_non_med_avg_2015_24", "class"],
                caption="Outage minutes per customer on non-major days, 2015-2024 average, 99 Dominion counties "
                        "(all utilities, EAGLE-I); inset: Isaias 2020 share of excess outages restored by hour",
                source="EAGLE-I (ORNL/DOE) via D: data/output/county_outage_map.csv, va_counties.geojson, "
                       "fct_restoration_curve.csv, outage_events_top10.csv; findings.md A2, A3", outdir=OUT)
    plt.close(fig)
    big_lo = min(big, key=big.get)
    return p, {"counts": counts, "flagged": flagged, "h50": h50, "h90": h90,
               "hi": (cmap[hi_k]["county_label"], big[hi_k]), "lo": (cmap[big_lo]["county_label"], big[big_lo])}


# ---------------------------------------------------------------- S5 v1: 24-hour growth profile
def s5_profile():
    ds.use_style("deck")
    rows = read(DATA / "dom_load_profile.csv")
    hrs = [int(r["hour_no"]) for r in rows]
    g = [float(r["growth_pct"]) for r in rows]
    night = [v for h, v in zip(hrs, g) if 1 <= h <= 5]
    aft = [v for h, v in zip(hrs, g) if 13 <= h <= 17]
    assert (min(night), max(night)) == (39.0, 41.0), night
    assert (min(aft), max(aft)) == (26.9, 27.4), aft
    fig, ax = plt.subplots(figsize=(7.9, 4.15))
    fig.subplots_adjust(left=0.1, right=0.955, top=0.83, bottom=0.165)
    ax.set_xlim(0.3, 24.7)
    ax.set_ylim(0, 45)
    ax.set_yticks([0, 10, 20, 30, 40])
    ax.set_yticklabels(["0", "10", "20", "30", "40%"])
    ax.set_xticks([1, 6, 12, 18, 24])
    ax.set_xticklabels(["1 a.m.", "6 a.m.", "noon", "6 p.m.", "midnight"])
    fig.canvas.draw()
    for h, v in zip(hrs, g):
        ds.rounded_bar(ax, h, v, 0.72, ds.SUBJECT if 1 <= h <= 5 else ds.CONTEXT)

    # group brackets above the bars, labels above the plot area
    def bracket(h0, h1, top, text, bold):
        y = top + 1.6
        ax.plot([h0 - 0.36, h0 - 0.36, h1 + 0.36, h1 + 0.36], [y - 0.9, y, y, y - 0.9], color=ds.INK_2,
                linewidth=0.9, clip_on=False, solid_capstyle="butt")
        text_at(ax, (h0 + h1) / 2, y, text, dy=4, ha="center", va="bottom",
                fontweight="semibold" if bold else "normal", color=ds.INK if bold else ds.INK_2, clip_on=False)

    bracket(1, 5, max(night), f"1–5 a.m.: +{min(night):.0f}% to +{max(night):.0f}%", True)
    bracket(13, 17, max(aft), f"1–5 p.m.: about +{sum(aft) / len(aft):.0f}%", False)
    ax.set_xlabel("Hour ending, local time", labelpad=7)
    fig.text(0.1, 0.955, "Growth in average load by hour, 2019 → 2025", fontsize=LBL, fontweight="semibold",
             color=ds.INK, ha="left", va="center")
    p = ds.save(fig, "s5_hourly_growth_2019_2025",
                data_rows=[[r["hour_no"], r["avg_mw_2019"], r["avg_mw_2025"], r["growth_pct"]] for r in rows],
                header=["hour_ending", "avg_mw_2019", "avg_mw_2025", "growth_pct"],
                caption="Growth in average load by hour ending, 2019 to 2025, PJM DOM zone (EIA-930)",
                source="EIA-930 via D: data/output/dom_load_profile.csv (mart.DOM_LOAD_PROFILE); findings.md A4.1",
                outdir=OUT)
    plt.close(fig)
    return p, night, aft


# ---------------------------------------------------------------- brief: winter vs summer peaks, 2019-2026
def s5_peaks_v1():
    ds.use_style("deck")
    rows = read(DATA / "dom_seasonal_peak.csv")
    pk = {}
    for r in rows:
        pk.setdefault(int(r["year"]), {})[r["season"]] = float(r["peak_mw"])
    data = [(y, pk[y]["winter"], pk[y]["summer"]) for y in sorted(pk) if y >= 2019]
    winters = [y for y, w, s in data if w >= s]
    assert winters == [2019, 2022, 2025, 2026], winters
    assert pk[2026]["winter"] - pk[2026]["summer"] == 29
    fig, ax = plt.subplots(figsize=(7.9, 2.85))
    fig.subplots_adjust(left=0.085, right=0.985, top=0.85, bottom=0.135)
    ax.set_xlim(2018.4, 2026.6)
    ax.set_ylim(0, 29)
    ax.set_yticks([0, 10, 20])
    ax.set_xticks([d[0] for d in data])
    ax.set_xticklabels([str(d[0]) if d[0] < 2026 else "2026*" for d in data])
    fig.canvas.draw()
    w = 0.34
    for yr, wi, su in data:
        ds.rounded_bar(ax, yr - w / 2 - 0.02, wi / 1000, w, ds.SUBJECT)
        ds.rounded_bar(ax, yr + w / 2 + 0.02, su / 1000, w, ds.THIRD)
        top_w = wi >= su
        v = max(wi, su) / 1000
        # value of the higher bar only; W/S on a second line keeps the label narrow (greyscale-safe)
        text_at(ax, yr - w / 2 - 0.02 if top_w else yr + w / 2 + 0.02, v, ("W" if top_w else "S") + f"\n{v:.1f}",
                dy=4, ha="center", va="bottom", linespacing=1.0,
                fontweight="semibold" if top_w else "normal")
    ax.set_ylim(0, 33)
    ax.set_ylabel("Peak hour, GW", labelpad=6)
    for i, (c, t) in enumerate([(ds.SUBJECT, "W  winter peak (Dec–Feb)"), (ds.THIRD, "S  summer peak (Jun–Aug)")]):
        x0 = 0.01 + i * 0.36
        ax.add_patch(Rectangle((x0, 1.06), 0.022, 0.055, transform=ax.transAxes, color=c, clip_on=False))
        ax.text(x0 + 0.032, 1.088, t, transform=ax.transAxes, fontsize=LBL, color=ds.INK, va="center", ha="left")
    p = ds.save(fig, "s5_winter_summer_peaks_v1",
                data_rows=[[y, wi, su, "winter" if wi >= su else "summer"] for y, wi, su in data],
                header=["year", "winter_peak_mw", "summer_peak_mw", "higher"],
                caption="Highest hour in winter (Dec-Feb) vs summer (Jun-Aug), PJM DOM zone, 2019-2026; "
                        "*2026 to the hour ending midnight 29 Oct 2026 (winter = Jan-Feb only)",
                source="EIA-930 via D: data/output/dom_seasonal_peak.csv (mart.DOM_SEASONAL_PEAK); findings.md A4.2, E1",
                outdir=OUT)
    plt.close(fig)
    return p, data


# ---------------------------------------------------------------- A2: annual weather fit after D22 (snapshot for the deck table)
def a2_fit():
    rows = {int(r["year"]): r for r in read(DATA / "storm_vs_saidi.csv")}
    assert float(rows[2024]["storm_county_days"]) == 464 and float(rows[2025]["storm_county_days"]) == 791, \
        "expects the D22 re-export (Bedford city folded into Bedford County)"
    yrs = list(range(2015, 2025))
    x = [float(rows[y]["storm_county_days"]) for y in yrs]
    y_ = [float(rows[y]["saidi_ex_med"]) for y in yrs]
    mx, my = sum(x) / len(x), sum(y_) / len(y_)
    sxx = sum((u - mx) ** 2 for u in x)
    sxy = sum((u - mx) * (v - my) for u, v in zip(x, y_))
    syy = sum((v - my) ** 2 for v in y_)
    b = sxy / sxx
    a0 = my - b * mx
    r = sxy / math.sqrt(sxx * syy)
    out = []
    for yr in range(2015, 2026):
        cd, sd = float(rows[yr]["storm_county_days"]), float(rows[yr]["saidi_ex_med"])
        out.append([yr, int(cd), sd, round(a0 + b * cd, 2), round(sd - (a0 + b * cd), 2)])
    with open(OUT / "a2_weather_fit.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "storm_county_days", "saidi_ex_med", "fit", "difference"])
        w.writerows(out)
    (OUT / "a2_weather_fit.txt").write_text(
        f"fit 2015-2024: intercept {a0:.4f} slope {b:.6f} r {r:.4f} r2 {r * r:.4f}\n"
        "source: data/output/storm_vs_saidi.csv after D22 (re-exported 08:19); D findings.md B0 D22 table\n",
        encoding="utf-8")
    assert round(r, 2) == 0.70 and round(a0 + b * 791, 1) == 145.3
    return {"a": a0, "b": b, "r": r, "rows": out}


def main():
    f = a2_fit()
    print(f"A2 fit: {f['a']:.3f} + {f['b']:.5f} x; r {f['r']:.4f}; R2 {f['r'] ** 2:.4f}")
    s = a1()
    print(f"A1: {s['ratio']:.2f}x (CI {s['lo']:.2f}-{s['hi']:.2f}), storm {s['storm_days']}, non-MED {s['non_med']}, "
          f"Dominion-only {s['dom_only']}, by year {s['year_min']}-{s['year_max']}")
    _, m = s4_composite()
    print("S4 map:", m)
    _, night, aft = s5_profile()
    print("S5 profile: night", night, "afternoon", aft)
    _, peaks = s5_peaks_v1()
    print("S5 peaks:", peaks)


if __name__ == "__main__":
    main()
