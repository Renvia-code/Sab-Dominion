"""v3 charts (ruling O-33 from V1): the public deck says nothing GitHub main contradicts.

  s3_peer_quadrant_v3_public   S3 (public): the twelve utilities with the medians origin/main prints in
                               docs/05_metrics_and_measures.md:87, "medians of the twelve peers: SAIFI 0.96, CAIDI 105",
                               i.e. the median of the 12 including Dominion; method labels exactly as the public
                               workbook's Peers sheet ("Mixed" for Georgia Power and Duke Energy Florida).

The adopted S3 chart is unchanged (charts/v2/s3_peer_quadrant_v2_adopted: medians of the 11 peers, 0.93 and 99.5).
Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\charts\\v3\\make_charts_v3.py
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "design"))
sys.path.insert(0, str(HERE.parents[0] / "v0"))
sys.path.insert(0, str(HERE.parents[0] / "v1"))
sys.path.insert(0, str(HERE.parents[0] / "v2"))
import ds  # noqa: E402
import make_charts_v2 as m2  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = HERE
DOCS05 = "docs/05_metrics_and_measures.md"


def docs05_medians() -> tuple[str, str]:
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show", f"origin/main:{DOCS05}"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    line = [ln for ln in raw.splitlines() if "Quadrant lines" in ln]
    assert len(line) == 1 and "medians of the twelve peers: SAIFI 0.96, CAIDI 105" in line[0], line
    return "0.96", "105"


def peers_public_v3():
    """The public workbook's Peers sheet as it stands on origin/main: values and method labels unchanged."""
    import make_charts_v0 as m0
    wb = {d["utility"]: d for d in m0.peers()}
    assert len(wb) == 12 and set(wb) == set(m2.KEY2NAME.values())
    for u in ("Georgia Power", "Duke Energy Florida"):
        assert wb[u]["standard"] == "Mixed", (u, wb[u]["standard"])
    pp = [{"utility": u, "standard": d["standard"], "saifi_5yr": d["saifi_5yr"], "caidi_5yr": d["caidi_5yr"],
           "saidi_2023_25": d["saidi_2023_25"]} for u, d in wb.items()]
    xs = sorted(d["saifi_5yr"] for d in pp)
    ys = sorted(d["caidi_5yr"] for d in pp)
    med_x, med_y = (xs[5] + xs[6]) / 2, (ys[5] + ys[6]) / 2           # median of the 12, Dominion included
    sx, sy = docs05_medians()
    assert (f"{med_x:.2f}", f"{med_y:.0f}") == (sx, sy), (med_x, med_y)
    dom = [d for d in pp if d["utility"] == "Dominion Energy Virginia"][0]
    assert sum(d["saifi_5yr"] > dom["saifi_5yr"] for d in pp) == 3                # 4th-highest of the 12
    assert sum(d["caidi_5yr"] > dom["caidi_5yr"] for d in pp) == 5                # 6th of the 12
    return pp, med_x, med_y


def s3_quadrant_public_v3():
    ds.use_style("deck")
    pp, med_x, med_y = peers_public_v3()
    lbl = m2.LBL
    fig, ax = plt.subplots(figsize=(7.9, 4.15))
    fig.subplots_adjust(left=0.115, right=0.975, top=0.97, bottom=0.165)
    ax.set_xlim(0.4, 1.4)
    ax.set_ylim(60, 150)
    ax.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4])
    ax.set_yticks([60, 80, 100, 120, 140])
    ax.grid(axis="both", color=ds.GRID, linewidth=0.7)
    ax.axvline(med_x, color=ds.MUTED, linewidth=1.0, zorder=1)
    ax.axhline(med_y, color=ds.MUTED, linewidth=1.0, zorder=1)
    # labels kept clear of the dots: the SAIFI median at the foot of its line, the CAIDI median above its line, left
    m2.text_at(ax, med_x, 62, f"median of the 12\n(including Dominion): {med_x:.2f}", dx=-5, va="bottom",
               ha="right", color=ds.MUTED, linespacing=1.05)
    m2.text_at(ax, 0.41, med_y, f"median of the 12\n(including Dominion): {med_y:.0f} min", dy=4, va="bottom",
               ha="left", color=ds.MUTED, linespacing=1.05)
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
        "PECO": ("PECO", 10, 0, "left", "center", False),     # beside its dot, under the CAIDI median line
    }
    for d in pp:
        if d["utility"] in lab:
            t, dx, dy, ha, va, bold = lab[d["utility"]]
            tt = m2.text_at(ax, d["saifi_5yr"], d["caidi_5yr"], t, dx=dx, dy=dy, ha=ha, va=va,
                            fontweight="semibold" if bold else "normal", color=ds.INK if bold else ds.INK_2,
                            linespacing=1.05, zorder=6)
            tt.set_bbox(dict(boxstyle="square,pad=0.12", facecolor="white", edgecolor="none"))
    gp = [d for d in pp if d["utility"] in ("Duke Progress (NC)", "Georgia Power")]
    gx = sum(d["saifi_5yr"] for d in gp) / 2
    gy = sum(d["caidi_5yr"] for d in gp) / 2
    ax.annotate("Duke Progress (NC),\nGeorgia Power", xy=(gx + 0.004, gy - 1.2), xytext=(1.392, 92),
                textcoords="data", ha="right", va="center", fontsize=lbl, color=ds.INK_2, linespacing=1.05,
                arrowprops=dict(arrowstyle="-", color=ds.MUTED, linewidth=0.8, shrinkA=3, shrinkB=4,
                                relpos=(0.75, 1.0)))
    ax.set_xlabel("Interruptions per customer per year (SAIFI), 2021–25 average", labelpad=7)
    ax.set_ylabel("Minutes per interruption (CAIDI)", labelpad=7)
    p = ds.save(fig, "s3_peer_quadrant_v3_public",
                data_rows=[[d["utility"], d["standard"], d["saifi_5yr"], d["caidi_5yr"], d["saidi_2023_25"]]
                           for d in pp],
                header=["utility", "major_event_method", "saifi_5yr_2021_25", "caidi_5yr_2021_25",
                        "saidi_3yr_2023_25"],
                caption="Dominion Energy Virginia and 11 peers: SAIFI vs CAIDI, 2021-2025 averages, ex-MED; "
                        f"medians of the 12 including Dominion {med_x:.3f} and {med_y:.2f} (origin/main docs/05: "
                        "0.96 and 105)",
                source="origin/main powerbi/Dominion_Reliability_PowerBI_Data.xlsx sheet Peers; medians as printed "
                       f"in origin/main {DOCS05}", outdir=OUT)
    plt.close(fig)
    return p, med_x, med_y


def main():
    print(s3_quadrant_public_v3())


if __name__ == "__main__":
    main()
