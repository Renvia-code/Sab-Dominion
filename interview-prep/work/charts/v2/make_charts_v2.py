"""v2 charts (storyline G2 revision, 09:30): the deck's two variants and the brief.

  s2_change_2022_2025_{adopted,public}  S2: the 2022 -> 2025 change bars, storm county-days included
                                        (adopted: D22 values 718 -> 791; public: origin/main 723 -> 796).
                                        SAIFI is the darkest mark in greyscale (V3 P5).
  s3_peer_quadrant_v2                   S3: Dominion and 11 peers, medians of the 11 (V3 P6), every dot labelled
  s4_storm_calm_levels                  S4 (adopted): storm vs calm county-day levels, ratio and CI (D's A1)
  a3_load_profile_public                A3 (public): hour-of-day growth labelled with the values on origin/main
                                        docs/05 (4 a.m. +41%, 4 p.m. +27%)
  a6_isaias_curve                       A6 (adopted): the Isaias restoration curve on its own

Inputs: data/output/ (D), interview-prep/work/data/output/a1_storm_vs_calm.csv (D's A1), the workbook's Peers
sheet (D F07/F08), and origin/main:data/output/storm_vs_saidi.csv for the public variant.
Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\charts\\v2\\make_charts_v2.py
"""
import csv
import io
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "design"))
sys.path.insert(0, str(HERE.parents[0] / "v0"))
sys.path.insert(0, str(HERE.parents[0] / "v1"))
import ds  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.transforms import offset_copy  # noqa: E402

OUT = HERE
LBL = ds.DECK["label_pt"]  # 13.5
DATA = ds.REPO / "data" / "output"
WDATA = ds.WORK / "data" / "output"


def text_at(ax, x, y, s, dx=0, dy=0, **kw):
    tr = offset_copy(ax.transData, fig=ax.figure, x=dx, y=dy, units="points")
    kw.setdefault("fontsize", LBL)
    kw.setdefault("color", ds.INK)
    return ax.text(x, y, s, transform=tr, **kw)


def read(p):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def origin_main_csv(path: str):
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show", f"origin/main:{path}"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw)))


def annual(variant: str):
    rows = read(DATA / "storm_vs_saidi.csv") if variant == "adopted" else origin_main_csv(
        "data/output/storm_vs_saidi.csv")
    return {int(r["year"]): {k: float(v) for k, v in r.items() if k != "year"} for r in rows}


# ---------------------------------------------------------------- S2: the 2022 -> 2025 change, storms included
def s2_change(variant: str):
    ds.use_style("deck")
    a = annual(variant)
    y0, y1 = 2022, 2025
    saidi = (a[y0]["saidi_ex_med"], a[y1]["saidi_ex_med"])
    saifi = (a[y0]["saifi_ex_med"], a[y1]["saifi_ex_med"])
    caidi = (saidi[0] / saifi[0], saidi[1] / saifi[1])
    storm = (a[y0]["storm_county_days"], a[y1]["storm_county_days"])
    assert storm == ((718.0, 791.0) if variant == "adopted" else (723.0, 796.0)), storm
    rows = [("Storm county-days", "NOAA, Dominion's counties", storm, ds.THIRD, "{:,.0f}"),
            ("SAIFI", "interruptions per customer", saifi, ds.SUBJECT, "{:.3f}"),
            ("CAIDI", "minutes per interruption", caidi, ds.CONTEXT, "{:.1f}"),
            ("SAIDI", "outage minutes per customer", saidi, ds.CONTEXT, "{:.1f}")]
    pct = [(r[2][1] / r[2][0] - 1) * 100 for r in rows]
    fig, ax = plt.subplots(figsize=(6.6, 4.05))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.03)
    ax.set_xlim(-14, 16)
    ax.set_ylim(-0.45, 4.55)
    ax.axis("off")
    fig.canvas.draw()
    ys = [3.95, 2.55, 1.4, 0.25]
    for (name, desc, (v0, v1), colr, fmt), p, y in zip(rows, pct, ys):
        ds.rounded_bar(ax, y, p, 0.34, colr, horizontal=True)
        text_at(ax, -14, y + 0.3, name, va="bottom", ha="left", fontweight="semibold")
        w = 50 if name != "Storm county-days" else 128
        text_at(ax, -14, y + 0.3, f"{desc}:  {fmt.format(v0)} → {fmt.format(v1)}", dx=w, va="bottom", ha="left",
                color=ds.INK_2)
        sign = "+" if p >= 0 else "−"
        text_at(ax, p, y, f"{sign}{abs(p):.0f}%", dx=7 if p >= 0 else -7, va="center",
                ha="left" if p >= 0 else "right", fontweight="semibold", fontsize=LBL + 1.5)
        ax.plot([0, 0], [y - 0.24, y + 0.24], color=ds.BASELINE, linewidth=0.9)
    ax.plot([-14, 16], [3.3, 3.3], color=ds.RULE, linewidth=0.8)
    fig.text(0.02, 0.965, "2022 → 2025, the two years that move the 3-year average", fontsize=LBL,
             fontweight="semibold", color=ds.INK, va="center", ha="left")
    stem = f"s2_change_2022_2025_{variant}"
    p = ds.save(fig, stem,
                data_rows=[[r[0], round(r[2][0], 3), round(r[2][1], 3), round(x, 1)] for r, x in zip(rows, pct)],
                header=["measure", "value_2022", "value_2025", "change_pct"],
                caption="2022 to 2025: storm county-days, SAIFI, CAIDI and SAIDI ex-MED, Dominion Energy Virginia",
                source=("data/output/storm_vs_saidi.csv (D22)" if variant == "adopted"
                        else "origin/main:data/output/storm_vs_saidi.csv"), outdir=OUT)
    plt.close(fig)
    return p, [round(x, 1) for x in pct]


# ---------------------------------------------------------------- S3: Dominion and 11 peers
KEY2NAME = {"19876|VA": "Dominion Energy Virginia", "5416|NC": "Duke Carolinas (NC)", "3046|NC": "Duke Progress (NC)",
            "7140|GA": "Georgia Power", "195|AL": "Alabama Power", "17539|SC": "Dominion Energy SC",
            "1167|MD": "BGE", "15270|MD": "Pepco (MD)", "14940|PA": "PECO", "14715|PA": "PPL Electric",
            "6452|FL": "FPL", "6455|FL": "Duke Energy Florida"}


def peers_for(variant: str):
    """adopted: D's peer_reliability_5yr.csv (batch 5: medians of the 11 peers 0.934 and 99.5, read, not computed).
    public: the workbook's Peers sheet on origin/main; the 11-peer medians are its 6th values (0.934, 99.3)."""
    import make_charts_v0 as m0
    wb = {d["utility"]: d for d in m0.peers()}
    assert len(wb) == 12 and set(wb) == set(KEY2NAME.values())
    # D batch 6 (findings C6, N-5): Georgia Power and Duke Energy Florida filed "Other" in 2013 only and IEEE 1366
    # every year 2014-25; the workbook's "Mixed" covers 2013-25. 10 of the 12 file IEEE 1366 every year 2014-25.
    for u in ("Georgia Power", "Duke Energy Florida"):
        assert wb[u]["standard"] == "Mixed", (u, wb[u]["standard"])
        wb[u] = dict(wb[u], standard="IEEE 1366")
    assert sum(d["standard"] == "IEEE 1366" for d in wb.values()) == 10
    assert {u for u, d in wb.items() if d["standard"] != "IEEE 1366"} == {"Dominion Energy Virginia", "Alabama Power"}
    if variant == "adopted":
        rows = read(DATA / "peer_reliability_5yr.csv")
        assert len(rows) == 12
        pp = [{"utility": KEY2NAME[r["utility_key"]], "standard": wb[KEY2NAME[r["utility_key"]]]["standard"],
               "saifi_5yr": float(r["saifi_2021_25"]), "caidi_5yr": float(r["caidi_2021_25"]),
               "saidi_2023_25": float(r["saidi_2023_25"])} for r in rows]
        med_x = float(rows[0]["median_saifi_2021_25_excl_dominion"])
        med_y = float(rows[0]["median_caidi_2021_25_excl_dominion"])
        assert (med_x, med_y) == (0.934, 99.5), (med_x, med_y)
    else:
        pp = [{"utility": u, "standard": d["standard"], "saifi_5yr": d["saifi_5yr"], "caidi_5yr": d["caidi_5yr"],
               "saidi_2023_25": d["saidi_2023_25"]} for u, d in wb.items()]
        p11 = [d for d in pp if d["utility"] != "Dominion Energy Virginia"]
        med_x = sorted(d["saifi_5yr"] for d in p11)[5]
        med_y = sorted(d["caidi_5yr"] for d in p11)[5]
        assert (med_x, med_y) == (0.934, 99.3), (med_x, med_y)
    dom = [d for d in pp if d["utility"] == "Dominion Energy Virginia"][0]
    assert sum(d["saifi_5yr"] > dom["saifi_5yr"] for d in pp) == 3                # 4th-highest of the 12
    assert sum(d["caidi_5yr"] > dom["caidi_5yr"] for d in pp) == 5                # 6th of the 12
    return pp, med_x, med_y


def s3_quadrant(variant: str):
    ds.use_style("deck")
    pp, med_x, med_y = peers_for(variant)
    fig, ax = plt.subplots(figsize=(7.9, 4.15))
    fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.165)
    ax.set_xlim(0.4, 1.4)
    ax.set_ylim(60, 150)
    ax.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4])
    ax.set_yticks([60, 80, 100, 120, 140])
    ax.grid(axis="both", color=ds.GRID, linewidth=0.7)
    ax.axvline(med_x, color=ds.MUTED, linewidth=1.0, zorder=1)
    ax.axhline(med_y, color=ds.MUTED, linewidth=1.0, zorder=1)
    text_at(ax, med_x, 148, f"median of the 11 peers: {med_x:.2f}", dx=-5, va="top", ha="right", color=ds.MUTED)
    text_at(ax, 0.41, med_y, f"peer median {med_y:.1f} min", dy=4, va="bottom", ha="left", color=ds.MUTED)
    for d in pp:
        dom = d["utility"] == "Dominion Energy Virginia"
        ax.scatter(d["saifi_5yr"], d["caidi_5yr"], s=130 if dom else 80,
                   color=ds.SUBJECT if dom else "#8A9099", edgecolors="white", linewidths=1.8,
                   zorder=5 if dom else 3)
    lab = {
        "Dominion Energy Virginia": ("Dominion\nEnergy Virginia", -12, 6, "right", "center", True),
        "Duke Carolinas (NC)": ("Duke Carolinas", -10, 0, "right", "center", False),
        "PPL Electric": ("PPL", 10, 0, "left", "center", False),
        "FPL": ("FPL", 10, 0, "left", "center", False),
        "Alabama Power": ("Alabama Power", 10, 0, "left", "center", False),
        "Dominion Energy SC": ("Dominion SC", 10, 0, "left", "center", False),
        "Duke Energy Florida": ("Duke Florida", -10, 0, "right", "center", False),
        "Pepco (MD)": ("Pepco", -10, 0, "right", "center", False),
        "BGE": ("BGE", 0, -9, "center", "top", False),
        "PECO": ("PECO", 9, 8, "left", "bottom", False),
    }
    for d in pp:
        if d["utility"] in lab:
            t, dx, dy, ha, va, bold = lab[d["utility"]]
            tt = text_at(ax, d["saifi_5yr"], d["caidi_5yr"], t, dx=dx, dy=dy, ha=ha, va=va,
                         fontweight="semibold" if bold else "normal", color=ds.INK if bold else ds.INK_2,
                         linespacing=1.05, zorder=6)
            tt.set_bbox(dict(boxstyle="square,pad=0.12", facecolor="white", edgecolor="none"))
    gp = [d for d in pp if d["utility"] in ("Duke Progress (NC)", "Georgia Power")]
    gx = sum(d["saifi_5yr"] for d in gp) / 2
    gy = sum(d["caidi_5yr"] for d in gp) / 2
    ax.annotate("Duke Progress (NC),\nGeorgia Power", xy=(gx + 0.004, gy - 1.2), xytext=(1.392, 92),
                textcoords="data", ha="right", va="center", fontsize=LBL, color=ds.INK_2, linespacing=1.05,
                arrowprops=dict(arrowstyle="-", color=ds.MUTED, linewidth=0.8, shrinkA=3, shrinkB=4,
                                relpos=(0.75, 1.0)))
    ax.set_xlabel("Interruptions per customer per year (SAIFI), 2021–25 average", labelpad=7)
    ax.set_ylabel("Minutes per interruption (CAIDI)", labelpad=7)
    p = ds.save(fig, f"s3_peer_quadrant_v2_{variant}",
                data_rows=[[d["utility"], d["standard"], d["saifi_5yr"], d["caidi_5yr"], d["saidi_2023_25"]]
                           for d in pp],
                header=["utility", "major_event_method", "saifi_5yr_2021_25", "caidi_5yr_2021_25",
                        "saidi_3yr_2023_25"],
                caption="Dominion Energy Virginia and 11 peers: SAIFI vs CAIDI, 2021-2025 averages, ex-MED; "
                        f"medians of the 11 peers {med_x:.3f} and {med_y:.1f}",
                source=("data/output/peer_reliability_5yr.csv (D batch 5, commit 7133aba); method from the "
                        "workbook Peers sheet" if variant == "adopted" else
                        "origin/main powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers"),
                outdir=OUT)
    plt.close(fig)
    return p, med_x, med_y


# ---------------------------------------------------------------- S4 (adopted): storm vs calm levels
def s4_levels():
    """D's batch-5 table (data/output/storm_vs_calm.csv, commit c0b2ea2), read, not recomputed."""
    ds.use_style("deck")
    rows = {r["subset"]: r for r in read(DATA / "storm_vs_calm.csv")}
    al = rows["All complete county-days, 2015-2025"]
    g = {k: float(al[k]) for k in ("storm_ch_per_1k", "storm_ci_low", "storm_ci_high", "calm_ch_per_1k",
                                   "calm_ci_low", "calm_ci_high", "ratio", "ratio_ci_low", "ratio_ci_high")}
    assert [f"{g[k]:.1f}" for k in g] == ["332.8", "225.6", "453.4", "27.9", "23.1", "33.2", "11.9", "7.9", "16.9"]
    assert al["ratio_label"] == "11.9 (7.9 to 16.9)" and int(al["storm_county_days"]) == 6108
    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    fig.subplots_adjust(left=0.03, right=0.97, top=0.86, bottom=0.05)
    ax.set_xlim(0, 540)
    ax.set_ylim(-0.2, 2.55)
    ax.axis("off")
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    bars = [(1.75, "County-days with a NOAA storm report", f"{int(al['storm_county_days']):,}", "storm", ds.SUBJECT),
            (0.45, "Calm county-days", f"{int(al['calm_county_days']):,}", "calm", ds.CONTEXT)]
    for y, name, n, k, colr in bars:
        v, lo, hi = g[f"{k}_ch_per_1k"], g[f"{k}_ci_low"], g[f"{k}_ci_high"]
        ds.rounded_bar(ax, y, v, 0.42, colr, horizontal=True)
        ax.plot([lo, hi], [y, y], color=ds.INK, linewidth=1.3, zorder=4, solid_capstyle="butt")
        for xx in (lo, hi):
            ax.plot([xx, xx], [y - 0.1, y + 0.1], color=ds.INK, linewidth=1.3, zorder=4)
        t1 = text_at(ax, 0, y + 0.3, name, va="bottom", ha="left", fontweight="semibold")
        wpt = t1.get_window_extent(renderer=rend).width * 72 / fig.dpi
        text_at(ax, 0, y + 0.3, f"{n} county-days", dx=wpt + 10, va="bottom", ha="left", color=ds.INK_2)
        text_at(ax, 0, y - 0.3, f"95% interval {lo:.1f} to {hi:.1f}", va="top", ha="left", color=ds.INK_2)
        text_at(ax, hi, y, f"{v:.1f}", dx=8, va="center", ha="left", fontweight="semibold", fontsize=LBL + 1.5)
    ax.plot([0, 0], [0.15, 2.05], color=ds.BASELINE, linewidth=0.9)
    fig.text(0.03, 0.955, "Outage customer-hours per 1,000 customers, mean per county-day, 2015–2025",
             fontsize=LBL, fontweight="semibold", color=ds.INK, va="center", ha="left")
    p = ds.save(fig, "s4_storm_calm_levels",
                data_rows=[[k, al[f"{k}_county_days"], g[f"{k}_ch_per_1k"], g[f"{k}_ci_low"], g[f"{k}_ci_high"]]
                           for k in ("storm", "calm")] + [["ratio", "", g["ratio"], g["ratio_ci_low"],
                                                           g["ratio_ci_high"]]],
                header=["subset", "county_days", "customer_hours_per_1k", "ci_low", "ci_high"],
                caption="Storm-report vs calm county-days: mean outage customer-hours per 1,000 customers, "
                        "2015-2025, with 95% intervals (EAGLE-I, all utilities, 99 counties)",
                source="data/output/storm_vs_calm.csv row 1 (D batch 5, commit c0b2ea2; 2,000 resamples of whole "
                       "days)", outdir=OUT)
    plt.close(fig)
    return p, g


# ---------------------------------------------------------------- A3 (public): load profile, origin/main labels
def a3_profile_public():
    ds.use_style("deck")
    rows = read(DATA / "dom_load_profile.csv")
    hrs = [int(r["hour_no"]) for r in rows]
    g = [float(r["growth_pct"]) for r in rows]
    v4, v16 = g[hrs.index(4)], g[hrs.index(16)]
    assert round(v4) == 41 and round(v16) == 27, (v4, v16)      # origin/main docs/05: 4am +41%, 4pm +27%
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
    text_at(ax, 4, v4, "4 a.m.: +41%", dy=6, ha="center", va="bottom", fontweight="semibold", clip_on=False)
    text_at(ax, 16, v16, "4 p.m.: +27%", dy=6, ha="center", va="bottom", color=ds.INK_2, clip_on=False)
    ax.set_xlabel("Hour of the day, local time", labelpad=7)
    fig.text(0.1, 0.955, "Growth in average load by hour, 2019 → 2025", fontsize=LBL, fontweight="semibold",
             color=ds.INK, ha="left", va="center")
    p = ds.save(fig, "a3_load_profile_public",
                data_rows=[[r["hour_no"], r["avg_mw_2019"], r["avg_mw_2025"], r["growth_pct"]] for r in rows],
                header=["hour", "avg_mw_2019", "avg_mw_2025", "growth_pct"],
                caption="Growth in average load by hour, 2019 to 2025, PJM DOM zone (EIA-930); labels as in "
                        "origin/main docs/05",
                source="EIA-930 via MART.DOM_LOAD_PROFILE (sql/07 on origin/main); docs/05 'Growth by hour of day'",
                outdir=OUT)
    plt.close(fig)
    return p, (v4, v16)


# ---------------------------------------------------------------- A6 (adopted): the Isaias curve
def a6_isaias():
    ds.use_style("deck")
    curve = [r for r in read(DATA / "fct_restoration_curve.csv") if r["event_key"].endswith("2020-08-04 07:45:00")]
    ev = [r for r in read(DATA / "outage_events_top10.csv") if r["tropical_cyclone"] == "ISAIAS"][0]
    h90 = float(ev["hours_to_90pct"])
    assert f"{h90:.1f}" == "33.5" and float(ev["peak_customers_out"]) == 351738
    hx = [float(r["hour_since_peak"]) for r in curve if float(r["hour_since_peak"]) <= 96]
    hy = [float(r["share_restored"]) * 100 for r in curve if float(r["hour_since_peak"]) <= 96]
    fig, ax = plt.subplots(figsize=(3.4, 3.4))
    fig.subplots_adjust(left=0.2, right=0.95, top=0.72, bottom=0.2)
    ax.set_xlim(0, 96)
    ax.set_ylim(0, 100)
    ax.set_xticks([0, 24, 48, 72, 96])
    ax.set_yticks([0, 50, 100])
    ax.set_yticklabels(["0", "50", "100%"])
    ax.grid(axis="y", color=ds.GRID, linewidth=0.7)
    ax.plot(hx, hy, color=ds.SUBJECT, linewidth=ds.line_width("subject"), zorder=3)
    ax.scatter([h90], [90], s=46, color=ds.SUBJECT, edgecolors="white", linewidths=1.4, zorder=5)
    text_at(ax, h90, 90, f"90% cleared\nat {h90:.1f} h", dx=7, dy=-4, ha="left", va="top", fontweight="semibold",
            linespacing=1.05)
    ax.set_xlabel("Hours after the peak", labelpad=5)
    # P4's final wording (orchestrator, after 09:35): "33.5 hours from the peak to clear 90% of the outage"
    for yy, s_ in ((0.945, "Isaias, August 2020:"), (0.87, f"{h90:.1f} hours from the peak to"),
                   (0.795, "clear 90% of the outage")):
        fig.text(0.04, yy, s_, fontsize=LBL, fontweight="semibold", color=ds.INK, ha="left", va="center")
    p = ds.save(fig, "a6_isaias_curve", data_rows=[[h, round(v, 1)] for h, v in zip(hx, hy)],
                header=["hour_since_peak", "share_cleared_pct"],
                caption="Isaias 2020: share of the outage cleared, (peak - customers out) / (peak - pre-event "
                        "level), by hours after the peak (EAGLE-I, all utilities in Dominion's 103 counties)",
                source="data/output/fct_restoration_curve.csv, outage_events_top10.csv (D findings A2; sql/09)",
                outdir=OUT)
    plt.close(fig)
    return p, h90


# ---------------------------------------------------------------- brief: county map, all utilities (G2: labeled)
def b_county_map():
    """The A3 map on its own for the brief, labeled 'all utilities' (G2; D batch 5 C5-5). No Isaias inset (it is on
    A6 and in Power BI), no 'start with these counties' line. Extremes among counties with 20,000+ customers are the
    P4 wording: 55 (Prince William County) to 633 (Pittsylvania County)."""
    import json
    import make_charts_v1 as m1
    from matplotlib.patches import PathPatch, Rectangle
    ds.use_style("deck")
    geo = json.load(open(DATA / "va_counties.geojson", encoding="utf-8"))
    cmap = {r["county_fips"]: r for r in read(DATA / "county_outage_map.csv")}
    city = {r["county_fips"]: r["is_independent_city"] == "True" for r in read(DATA / "dim_county.csv")}
    ok = {k: float(r["minutes_non_med_avg_2015_24"]) for k, r in cmap.items() if r["map_flag"] == "ok"}
    assert len(ok) == 99 and len(cmap) == 103
    big = {k: v for k, v in ok.items() if float(cmap[k]["customers_basis"]) >= 20000}
    hi_k, lo_k = max(big, key=big.get), min(big, key=big.get)
    assert (cmap[hi_k]["county_label"], f"{big[hi_k]:.0f}") == ("Pittsylvania County", "633")
    assert (cmap[lo_k]["county_label"], f"{big[lo_k]:.0f}") == ("Prince William County", "55")
    fig = plt.figure(figsize=(7.4, 3.75))
    ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_aspect("equal")
    ax.axis("off")
    feats = sorted(geo["features"], key=lambda f: city.get(f["properties"]["county_fips"], False))
    cents, xs, ys = {}, [], []
    for f in feats:
        fips = f["properties"]["county_fips"]
        rs = list(m1.rings(f["geometry"]))
        for r in rs:
            xs += [p[0] for p in r]
            ys += [p[1] for p in r]
        cents[fips] = m1.centroid(rs)
        if fips in ok:
            fc, ec, lw = ds.SEQ5[m1.klass(ok[fips])], ds.WHITE, 0.35
        elif fips in cmap:
            fc, ec, lw = ds.WHITE, ds.MUTED, 0.5
        else:
            fc, ec, lw = ds.WHITE, ds.RULE, 0.5
        ax.add_patch(PathPatch(m1.ring_path(rs), facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    ax.set_xlim(x0 - 0.02, x1 + 0.06)
    ax.set_ylim(y0 - 0.42, y1 + 0.42)
    fig.canvas.draw()
    # leader end: the point nearest the centroid that lies inside the county and outside every other feature
    # (Prince William's centroid falls in Manassas city, which is off the map)
    from matplotlib.path import Path as MPath2
    paths = {f["properties"]["county_fips"]: [MPath2(r) for r in m1.rings(f["geometry"])] for f in feats}

    def inside_point(k):
        cx, cy = cents[k]
        cand = [(cx + i * 0.02, cy + j * 0.02) for i in range(-15, 16) for j in range(-15, 16)]
        cand.sort(key=lambda p: (p[0] - cx) ** 2 + (p[1] - cy) ** 2)
        for p in cand:
            if any(pp.contains_point(p) for pp in paths[k]) and not any(
                    pp.contains_point(p) for o, ps in paths.items() if o != k for pp in ps):
                return p
        return cx, cy

    for k in (hi_k, lo_k):
        cents[k] = inside_point(k)
    for k, xt, yt, ha, rp in ((hi_k, cents[hi_k][0] + 0.25, y0 - 0.3, "left", (0.0, 0.5)),
                              (lo_k, cents[lo_k][0] - 0.2, y1 + 0.27, "right", (1.0, 0.5))):
        cx, cy = cents[k]
        name = cmap[k]["county_label"]
        ax.annotate(f"{name} {big[k]:.0f}", xy=(cx, cy), xytext=(xt, yt), textcoords="data", ha=ha, va="center",
                    fontsize=LBL, color=ds.INK, fontweight="semibold",
                    arrowprops=dict(arrowstyle="-", color=ds.INK_2, linewidth=0.8, shrinkA=2, shrinkB=0,
                                    relpos=rp), zorder=6)
    lx, ly = x0 + 0.05, y1 - 0.15
    text_at(ax, lx, ly, "All utilities in each county (EAGLE-I)", ha="left", va="center", fontweight="semibold")
    text_at(ax, lx, ly - 0.26, "Outage minutes per customer a year,", ha="left", va="center", color=ds.INK_2)
    text_at(ax, lx, ly - 0.48, "non-major days, 2015–2024 average", ha="left", va="center", color=ds.INK_2)
    sw = 0.13
    for i in range(5):
        yy = ly - 0.8 - i * 0.19
        ax.add_patch(Rectangle((lx, yy - 0.065), sw * 1.1, 0.13, facecolor=ds.SEQ5[i], edgecolor="none", zorder=4))
        text_at(ax, lx + sw * 1.1, yy, m1.CLASS_LABELS[i], dx=5, ha="left", va="center", color=ds.INK_2)
    p = ds.save(fig, "b_county_map_all_utilities",
                data_rows=[[k, cmap[k]["county_label"], cmap[k]["customers_basis"], ok[k]] for k in sorted(ok)],
                header=["county_fips", "county", "customers_basis", "minutes_non_med_avg_2015_24"],
                caption="All utilities in each of Dominion's Virginia counties (EAGLE-I): outage minutes per customer "
                        "a year, non-major days, 2015-2024 average; 99 of 103 shown",
                source="data/output/county_outage_map.csv (map_flag = 'ok'), va_counties.geojson (D findings A3, C5-5)",
                outdir=OUT)
    plt.close(fig)
    return p


def main():
    b_county_map()
    print("brief map: done")
    for v in ("adopted", "public"):
        _, pct = s2_change(v)
        print(f"S2 {v}: change % {pct}")
    for v in ("adopted", "public"):
        _, mx, my = s3_quadrant(v)
        print(f"S3 {v}: medians of the 11 peers {mx:.3f}, {my:.1f}")
    _, lv = s4_levels()
    print("S4 levels:", lv)
    _, pr = a3_profile_public()
    print("A3 public profile 4 a.m., 4 p.m.:", pr)
    _, h90 = a6_isaias()
    print("A6 Isaias h90:", h90)


if __name__ == "__main__":
    main()
