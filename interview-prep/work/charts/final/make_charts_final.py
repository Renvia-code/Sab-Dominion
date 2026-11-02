"""Final charts (rulings O-34 to O-39, after V6).

  a3_load_profile_hour_ending   public deck A3 and brief p. 6: growth in average load by hour ending, 2019 -> 2025,
                                labeled with the values origin/main docs/05 prints (4am +41%, 4pm +27%). The same data
                                as charts/v2/a3_load_profile_public; only the framing changes to "hour ending", the
                                framing of the adopted A3 (EIA-930 hours are hour-ending; dom_load_profile.hour_no).

Run: .venv\\Scripts\\python.exe -I interview-prep\\work\\charts\\final\\make_charts_final.py
"""
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "design"))
import ds  # noqa: E402

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.transforms import offset_copy  # noqa: E402

LBL = ds.DECK["label_pt"]
DATA = ds.REPO / "data" / "output"


def text_at(ax, x, y, s, dx=0, dy=0, **kw):
    tr = offset_copy(ax.transData, fig=ax.figure, x=dx, y=dy, units="points")
    kw.setdefault("fontsize", LBL)
    kw.setdefault("color", ds.INK)
    return ax.text(x, y, s, transform=tr, **kw)


def a3_hour_ending():
    ds.use_style("deck")
    rows = list(csv.DictReader(open(DATA / "dom_load_profile.csv", encoding="utf-8")))
    hrs = [int(r["hour_no"]) for r in rows]
    g = [float(r["growth_pct"]) for r in rows]
    v4, v16 = g[hrs.index(4)], g[hrs.index(16)]
    assert round(v4) == 41 and round(v16) == 27, (v4, v16)      # origin/main docs/05: 4am +41%, 4pm +27%
    assert [round(x) for x in g[0:5]] == [39, 40, 41, 41, 40]       # hours ending 1-5 a.m.: 39-41%
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
    ax.set_xlabel("Hour ending, local time", labelpad=7)
    fig.text(0.1, 0.955, "Growth in average load by hour ending, 2019 → 2025", fontsize=LBL, fontweight="semibold",
             color=ds.INK, ha="left", va="center")
    p = ds.save(fig, "a3_load_profile_hour_ending",
                data_rows=[[r["hour_no"], r["avg_mw_2019"], r["avg_mw_2025"], r["growth_pct"]] for r in rows],
                header=["hour_ending", "avg_mw_2019", "avg_mw_2025", "growth_pct"],
                caption="Growth in average load by hour ending, 2019 to 2025, PJM DOM zone (EIA-930); labels as in "
                        "origin/main docs/05 (4am +41%, 4pm +27%)",
                source="EIA-930 via MART.DOM_LOAD_PROFILE (data/output/dom_load_profile.csv, hour_no = hour ending)",
                outdir=HERE)
    plt.close(fig)
    return p


if __name__ == "__main__":
    print(a3_hour_ending())
