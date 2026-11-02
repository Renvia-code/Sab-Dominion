"""Deck v3 (P1), the final candidate: deck v2 plus ruling O-33 from the V1 number audit.

v3 changes (work/reviews/V1_summary.md, V1_coverage.md):
  public S3 and A6   the medians origin/main prints (docs/05: median of the 12 including Dominion, 0.96 and 105) and
                     the workbook's method labels ("Mixed"); no "10 of 12" anywhere in the public deck
  adopted S6, A4     31 tests: 12 on the original build (6 reliability, 3 storm, 3 demand), 19 on the new tables
  both               CAIDI is "minutes per interruption", never "minutes to restore"; new S5 screenshots
                     (adopted: b6/s5_summary_v3.png; public: b6/orig_whatmoved_saifi.png, the frequency chart only)

One generator, two variants (rulings O-26):
  --variant adopted   the 1 Nov upgrade presented as part of the project (EAGLE-I, D22, T13-T31, 12 of 12, the
                      Import report). Main deck.
  --variant public    only what is on the candidate's origin/main today: NOAA scatter on S4 (465 -> 796), tests
                      T1-T12, decisions D1-D14, D13 for Power BI, the peer table on A6, no p-values. Every project
                      number must be findable on origin/main (work/v2/origin_main_corpus.py).

Main slides: S1 title, S2 130 -> 133 (storms and interruptions), S3 peers (Dominion and 11 peers), S4 storms,
S5 the Power BI report, S6 how it's built, S7 first 90 days, S8 close. Appendix: A1 definitions, A2 weather fit,
A3 load shape, A4 sources and tests, A5 limits, A6 events (adopted) or the peer table (public).
Drawing helpers come from build_deck_v1.py (imported; v1 itself is unchanged).

Run:  .venv\\Scripts\\python.exe -I interview-prep\\work\\deck\\build_deck_v3.py --variant adopted
      .venv\\Scripts\\python.exe -I interview-prep\\work\\deck\\build_deck_v3.py --variant public
Out:  interview-prep/deliverables/01_deck/Dominion_reliability_deck_v3[_public].pptx and _print_letter.pdf
      interview-prep/work/proofs/deck_v3[_public]/
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "design"))
sys.path.insert(0, str(HERE))
import ds  # noqa: E402
import pipeline  # noqa: E402
import build_deck_v1 as b  # noqa: E402  (drawing helpers only)

from pptx import Presentation  # noqa: E402
from pptx.util import Inches  # noqa: E402

L, CW, R, TOP, BOTTOM, BOTTOM_APX = b.L, b.CW, b.R, b.TOP, b.BOTTOM, b.BOTTOM_APX
REG, SEMI, LIGHT, SEMIL = b.REG, b.SEMI, b.LIGHT, b.SEMIL
CH0 = ds.WORK / "charts" / "v0"
CH1 = ds.WORK / "charts" / "v1"
CH2 = ds.WORK / "charts" / "v2"
CH3 = ds.WORK / "charts" / "v3"
DATA = ds.REPO / "data" / "output"
OUT = ds.REPO / "interview-prep" / "deliverables" / "01_deck"
SHOTS = ds.WORK / "powerbi" / "b6"
S5_SHOT = "s5_summary_v3.png"     # Summary page of the rebuilt template, CAIDI labeled minutes per interruption (O-33)
# Public S5 (ruling 4, O-33): the candidate's current report, What moved page, frequency chart only: the original's
# CAIDI chart says "minutes to restore" and the original is never modified
PUBLIC_SHOT = ds.WORK / "powerbi" / "b6" / "orig_whatmoved_saifi.png"
# Alt text for the adopted S5 screenshot, written from the labels read off s5_summary_v3.png
S5_ALT = ("Screenshot of the report's Summary page: a year slicer set to 2025; cards for customers served 2.68M, "
          "SAIDI 144.4, minutes per interruption 109.4, SAIFI 1.320 and major-event share 53%; line charts of SAIFI "
          "and CAIDI since 2013, actual and weather-adjusted SAIDI since 2015, and the storm-day scatter with its "
          "fitted line.")

ap = argparse.ArgumentParser()
ap.add_argument("--variant", choices=["adopted", "public"], default="adopted")
ap.add_argument("--shot", default=S5_SHOT, help="file in work/powerbi/b6/ for the adopted S5 screenshot")
ARGS = ap.parse_args()
VARIANT = ARGS.variant
ADOPT = VARIANT == "adopted"
DRANGE = "D1–D22" if ADOPT else "D1–D14"          # one constant per variant (orchestrator confirming)
STEM = "Dominion_reliability_deck_v3" + ("" if ADOPT else "_public")
PROOFS = ds.WORK / "proofs" / ("deck_v3" if ADOPT else "deck_v3_public")
DATE = "November 3, 2026"


def load_csv(p: Path):
    return list(csv.DictReader(open(p, encoding="utf-8")))


def origin_main_csv(path: str):
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show", f"origin/main:{path}"], capture_output=True,
                         check=True).stdout.decode("utf-8")
    return list(csv.DictReader(io.StringIO(raw)))


def origin_main_storm_index() -> dict[int, float]:
    """The public workbook's StormIndex sheet: year -> predicted_saidi_from_weather, the values the report shows.
    It fits the one-decimal SAIDI values, so three years differ by 0.1 from a refit on the CSV's three decimals."""
    import openpyxl
    raw = subprocess.run(["git", "-C", str(ds.REPO), "show",
                          "origin/main:powerbi/Dominion_Reliability_PowerBI_Data.xlsx"], capture_output=True,
                         check=True).stdout
    ws = openpyxl.load_workbook(io.BytesIO(raw), data_only=True, read_only=True)["StormIndex"]
    rows = list(ws.iter_rows(values_only=True))
    iy, ip = rows[0].index("year"), rows[0].index("predicted_saidi_from_weather")
    return {int(r[iy]): float(r[ip]) for r in rows[1:] if r[iy] is not None}


def ols(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    syy = sum((y - my) ** 2 for y in ys)
    b1 = sxy / sxx
    return my - b1 * mx, b1, sxy / math.sqrt(sxx * syy)


def why(slide, text):
    """The humble bottom line (G2: replaces 'For Dominion:')."""
    y = 5.84
    b.rect(slide, L, y + 0.06, 0.07, 0.27, ds.SUBJECT)
    b.tb(slide, L + 0.2, y, CW - 0.2, 0.66, [[("Why it matters: ", SEMI, ds.INK), (text, REG, ds.INK_2)]],
         ds.DECK["lead_pt"], ls=0.95, name="why")


def closing(slide, text):
    y = 5.84
    b.rect(slide, L, y + 0.06, 0.07, 0.27, ds.SUBJECT)
    b.tb(slide, L + 0.2, y, CW - 0.2, 0.66, [[(text, SEMI, ds.INK)]], ds.DECK["lead_pt"], ls=0.95, name="close")


def fit_picture(slide, png: Path, x, y, w, h, alt: str):
    """Picture scaled to fit inside w x h (aspect kept), top-left aligned."""
    from PIL import Image
    with Image.open(png) as im:
        wpx, hpx = im.size
    scale = min(w / wpx, h / hpx)
    pw, ph = wpx * scale, hpx * scale
    pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y), width=Inches(pw), height=Inches(ph))
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    b.rect(slide, x, y, pw, ph, None, line=ds.RULE)         # hairline frame round the screenshot
    return pw, ph


def main():
    PROOFS.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    events = load_csv(DATA / "outage_events_top10.csv")
    S3_PNG = CH2 / "s3_peer_quadrant_v2_adopted.png" if ADOPT else CH3 / "s3_peer_quadrant_v3_public.png"
    peers = load_csv(S3_PNG.with_suffix(".csv"))
    if ADOPT:   # D batch 5 (commit 7133aba): medians of the 11 peers, read, not recomputed
        pr0 = load_csv(DATA / "peer_reliability_5yr.csv")[0]
        med_saifi = float(pr0["median_saifi_2021_25_excl_dominion"])
        med_caidi = float(pr0["median_caidi_2021_25_excl_dominion"])
        assert (f"{med_saifi:.2f}", f"{med_caidi:.1f}") == ("0.93", "99.5"), (med_saifi, med_caidi)
    else:       # O-33: the medians origin/main prints (docs/05:87), the median of the 12 including Dominion
        xs = sorted(float(d["saifi_5yr_2021_25"]) for d in peers)
        ys = sorted(float(d["caidi_5yr_2021_25"]) for d in peers)
        med_saifi, med_caidi = (xs[5] + xs[6]) / 2, (ys[5] + ys[6]) / 2
        assert (f"{med_saifi:.2f}", f"{med_caidi:.0f}") == ("0.96", "105"), (med_saifi, med_caidi)
        assert {d["utility"] for d in peers if d["major_event_method"] == "Mixed"} == {"Georgia Power",
                                                                                      "Duke Energy Florida"}
    # public: the chart labels each line "median of the 12 (including Dominion)"; the column text is short for space
    med_lbl = ((f"peer median {med_saifi:.2f}", f"peer median {med_caidi:.1f}") if ADOPT else
               (f"median {med_saifi:.2f}", f"median {med_caidi:.0f}"))
    if ADOPT:
        fit = load_csv(CH1 / "a2_weather_fit.csv")                 # D22 storm county-days, 2015-2025
        ftxt = (CH1 / "a2_weather_fit.txt").read_text(encoding="utf-8").splitlines()[0].split()
        b0, b1_, r_fit = float(ftxt[3]), float(ftxt[5]), float(ftxt[7])
        svc = {r["subset"]: r for r in load_csv(DATA / "storm_vs_calm.csv")}      # D batch 5, commit c0b2ea2
        a1_all = svc["All complete county-days, 2015-2025"]
        assert a1_all["ratio_label"] == "11.9 (7.9 to 16.9)" and a1_all["storm_county_days"] == "6108"
    else:
        fit = [r for r in origin_main_csv("data/output/storm_vs_saidi.csv") if 2015 <= int(r["year"]) <= 2025]
        tr = [r for r in fit if int(r["year"]) <= 2024]
        b0, b1_, r_fit = ols([float(r["storm_county_days"]) for r in tr], [float(r["saidi_ex_med"]) for r in tr])
        assert (f"{b0:.1f}", f"{b1_:.4f}", f"{r_fit:.2f}", f"{r_fit ** 2:.2f}") == ("104.4", "0.0514", "0.70", "0.48")
        wb_pred = origin_main_storm_index()     # A2 prints these, so every value is the one the public report shows
        for r_ in fit:
            assert abs(wb_pred[int(r_["year"])] - (b0 + b1_ * float(r_["storm_county_days"]))) < 0.05, r_["year"]
    by_year = {int(r["year"]): r for r in fit}
    cd22, cd24, cd25 = (int(float(by_year[y]["storm_county_days"])) for y in (2022, 2024, 2025))
    assert (cd22, cd24, cd25) == ((718, 464, 791) if ADOPT else (723, 465, 796))
    pred25 = b0 + b1_ * cd25
    assert f"{pred25:.1f}" == "145.3"

    prs = Presentation()
    prs.slide_width = Inches(ds.SLIDE_W_IN)
    prs.slide_height = Inches(ds.SLIDE_H_IN)
    blank = prs.slide_layouts[6]
    cp = prs.core_properties
    now = dt.datetime.now().replace(microsecond=0)
    cp.author = "Saketh Bollina"
    cp.last_modified_by = "Saketh Bollina"
    cp.title = "Dominion Energy Virginia reliability: what public data shows"
    cp.subject = f"Interview presentation, {DATE}"
    cp.keywords = ""
    cp.comments = ""
    cp.category = ""
    cp.revision = 1
    cp.created = now
    cp.modified = now
    cp.last_printed = now

    def new():
        return prs.slides.add_slide(blank)

    rx = L + 7.9 + 0.33
    rw = R - rx

    # ------------------------------------------------------------------ S1 title
    s = new()
    b.rect(s, L, 1.62, 0.9, 0.09, ds.SUBJECT)
    b.tb(s, L, 1.95, CW, 2.3, [[("Dominion Energy Virginia reliability: what public data shows, and where "
                                 "I'd look first", SEMI, ds.INK)]], 40, ls=0.95, name="S1 title")
    b.tb(s, L, 4.3, 10.6, 0.45, [[("Independent analysis of public data", SEMIL, ds.INK_2)]], 22, name="S1 sub")
    b.tb(s, L, 5.15, 6.0, 0.42, [[("Saketh Bollina", SEMI, ds.INK)]], 22, name="S1 name")
    b.tb(s, L, 5.58, 6.0, 0.42, [[(DATE, REG, ds.INK_2)]], 20, name="S1 date")
    b.hline(s, L, 6.5, CW)
    foot = ("Data: EIA-861 · PUDL · NOAA Storm Events · EAGLE-I · EIA-930" if ADOPT
            else "Data: EIA-861 · PUDL · NOAA Storm Events · EIA-930")
    b.tb(s, L, 6.62, CW, 0.35, [[(foot, REG, ds.MUTED)]], ds.DECK["source_pt"], name="S1 foot")
    ctx = ("NOAA storm records, the Department of Energy's county outage records and EIA's hourly demand" if ADOPT
           else "NOAA storm records and EIA's hourly demand")
    b.notes(s, f"""Thank you for having me. I'm Saketh Bollina. To prepare, I rebuilt Dominion Energy Virginia's
    reported reliability numbers from EIA's public filings, then added {ctx} for context. Everything here is public;
    I had no Dominion internal data, and I'll say where public data stops. Three findings, then the Power BI report,
    how it's built, and what I'd do in the first 90 days.""")

    # ------------------------------------------------------------------ S2 130 -> 133: storms and interruptions
    s = new()
    b.title(s, "Outage minutes rose from 130 to 133; 2025 had more storms and more interruptions")
    lw = 4.95
    b.col(s, L, TOP - 0.04, lw, [
        ("130 → 133", LIGHT, 44, ds.INK, 0.0),
        ("Reported 3-year average outage minutes per customer, excluding major events", REG, 16, ds.INK_2, 0.08),
        ("Rebuilt from EIA-861: 130.2 → 133.0", SEMI, 16, ds.INK, 0.14),
        ("rule", 0.1),
        ("2025 (144.4) replaced 2022 (136.0) in the window.", REG, 16, ds.INK_2, 0.14),
        ("rule", 0.1),
        ("Dominion attributes the rise primarily to increased storm activity (2025 Annual Report, p. 10). 2025 "
         "sits on the storm line, with no clear trend once storms are counted (A2).", REG, 16, ds.INK_2, 0.0),
    ], BOTTOM, "S2 left")
    b.picture(s, CH2 / f"s2_change_2022_2025_{VARIANT}.png", R - 6.6, TOP - 0.06,
              f"Change from 2022 to 2025: storm county-days {cd22} to {cd25} (+10%); SAIFI 1.199 to 1.320 (+10%); "
              "CAIDI 113.5 to 109.4 minutes (-4%); SAIDI 136.0 to 144.4 minutes (+6%).")
    why(s, "a stormy year can move a 3-year average. With outage records, I'd ask whether non-storm "
           "interruptions are rising underneath.")
    b.source(s, "EIA-861 2025 final and PUDL (EIA-861) 2013–2024, Dominion Energy Virginia, excluding major event "
                "days; 3-year means of annual values. NOAA Storm Events (A2). Reported figures: Dominion Energy 2025 "
                "Annual Report, p. 10.", 2)
    b.notes(s, f"""Dominion's 2025 annual report gives SAIDI, excluding major events, of 133 minutes for the three
    years ending 2025, up from 130, and says: "This increase is primarily due to increased storm activity." SAIDI is
    average outage minutes per customer. I rebuilt it from EIA's filings. The public Virginia data reproduces both
    reported figures to the minute: 130.2 and 133.0, a rise of 2.8 minutes. A three-year average moves when a year
    leaves the window: 2025, at 144.4 minutes, replaced 2022, at 136.0. Between those two years storm county-days
    rose 10 percent, {cd25} against {cd22}, and interruptions per customer, SAIFI, rose 10 percent; minutes per
    interruption, CAIDI, fell 4 percent. The weather fit in A2 puts 2025 on the storm line, and once storms are
    counted there's no clear trend. Two cautions: 2025's SAIFI of 1.320 only edges 2018's 1.303, and 2025's SAIDI
    is still below 2018 and 2019. One year is not a trend.""")

    # ------------------------------------------------------------------ S3 Dominion and 11 peers
    s = new()
    b.title(s, "Among 12 large utilities, Dominion's interruption length is mid-pack; frequency is the gap")
    b.picture(s, S3_PNG, L, TOP - 0.03,
              "Scatter of Dominion Energy Virginia and 11 peers: SAIFI 2021-25 average across, CAIDI down. Dominion "
              "at 1.21 interruptions and 110 minutes; " +
              (f"medians of the 11 peers {med_saifi:.2f} and {med_caidi:.1f}." if ADOPT else
               f"medians of the 12 (including Dominion) {med_saifi:.2f} and {med_caidi:.0f}.") +
              " Every utility is labeled.")
    methods = ("Methods differ: Dominion uses its own (non-IEEE) major-event rule, most peers IEEE 1366, so ranks are "
               "indicative." if ADOPT else
               "Methods differ: Dominion reports under its own major-event rule; ranks are indicative.")
    b.col(s, rx, TOP + 0.02, rw, [
        ("rule", 0.08),
        ("1.21", LIGHT, 40, ds.INK, 0.0),
        (f"interruptions per customer a year: 4th highest of the 12 ({med_lbl[0]})", REG, 16, ds.INK_2, 0.22),
        ("rule", 0.08),
        ("110 min", LIGHT, 40, ds.INK, 0.0),
        (f"per interruption: mid-pack, 6th of the 12 ({med_lbl[1]})", REG, 16, ds.INK_2, 0.22),
        (methods, REG, 16, ds.INK_2, 0.0),
    ], BOTTOM, "S3 right")
    why(s, "if frequency is where Dominion differs, the next question is which causes drive interruptions, and "
           "that needs outage records.")
    b.source(s, "EIA-861 / PUDL 2021–2025, excluding major event days, means of annual values. Dominion and 11 "
                "peers: twelve large investor-owned utilities in PJM and the Southeast, selected by EIA ID before "
                "results were computed; " + ("medians exclude Dominion." if ADOPT else
                                             "medians include Dominion."), 3)
    caveat = ("Most of these peers use the IEEE 1366 method and Dominion reports under its own rule, so the ranking "
              "is indicative." if ADOPT else
              "Dominion reports under its own major-event rule, so the ranking is indicative.")
    against = (f"against a median of {med_saifi:.2f} for the eleven peers" if ADOPT else
               f"against a median of {med_saifi:.2f} for all twelve, Dominion included")
    b.notes(s, f"""Is that unusual? These are twelve large investor-owned utilities in PJM and the Southeast,
    Dominion and eleven peers, picked by EIA ID before I looked at any results. Across is interruptions per customer
    per year; up is minutes per interruption; both are 2021 to 2025 averages. Dominion is the blue dot. Its minutes
    per interruption, 110, are sixth of twelve: mid-pack. Its frequency, 1.21 interruptions a year, is fourth
    highest, {against}. One caveat I'd raise myself: utilities set aside major event days in different ways.
    {caveat} The gap to peers is how often customers lose power.""")

    # ------------------------------------------------------------------ S4 storms
    s = new()
    if ADOPT:
        fv = lambda row, k: float(row[k])  # noqa: E731
        ratio, lo, hi = fv(a1_all, "ratio"), fv(a1_all, "ratio_ci_low"), fv(a1_all, "ratio_ci_high")
        storm_lvl, calm_lvl = fv(a1_all, "storm_ch_per_1k"), fv(a1_all, "calm_ch_per_1k")
        nmed = fv(svc["Non-major days (proxy major event days removed)"], "ratio")
        donly = fv(svc["Dominion-only counties"], "ratio")
        yrs = [fv(svc[str(y)], "ratio") for y in range(2015, 2026)]
        assert all(fv(svc[str(y)], "ratio_ci_low") > 1 for y in range(2015, 2026))
        assert (f"{nmed:.1f}", f"{donly:.1f}", f"{min(yrs):.1f}", f"{max(yrs):.1f}") == ("9.9", "19.9", "5.9", "27.4")
        b.title(s, "County-days with storms had about 12 times the outage hours of calm days")
        b.picture(s, CH2 / "s4_storm_calm_levels.png", L, TOP - 0.03,
                  f"Two bars with 95% intervals: mean outage customer-hours per 1,000 customers per county-day, "
                  f"2015-2025. County-days with a NOAA storm report: {storm_lvl:.1f} (225.6 to 453.4); calm "
                  f"county-days: {calm_lvl:.1f} (23.1 to 33.2).")
        b.col(s, L + 7.4 + 0.33, TOP + 0.02, R - (L + 7.4 + 0.33), [
            ("rule", 0.08),
            (f"{ratio:.1f}×", LIGHT, 44, ds.INK, 0.0),
            (f"storm vs calm county-days (95% CI {lo:.1f}–{hi:.1f})", REG, 16, ds.INK_2, 0.2),
            ("rule", 0.08),
            (f"Holds on non-major days ({nmed:.1f}×), in Dominion-only counties ({donly:.1f}×) and in every year "
             "2015–2025.", REG, 16, ds.INK_2, 0.2),
            ("rule", 0.08),
            ("EAGLE-I counts every utility's customers in a county. An association: storm reports partly follow "
             "damage.", REG, 16, ds.INK_2, 0.0),
        ], BOTTOM, "S4 right")
        why(s, "reporting reliability next to storm exposure would keep a stormy year from being read as a trend.")
        b.source(s, "EAGLE-I (ORNL) and NOAA Storm Events, 2015–2025: 6,108 storm county-days with complete outage "
                    "readings, 99 counties on the map (EAGLE-I); complete days only (2025: 74% of county-days). 95% "
                    "intervals: 2,000 resamples of whole days.", 4)
        b.notes(s, f"""Weather is the obvious question, and the county-day data answers it more finely than annual
        totals. EAGLE-I, the Department of Energy's county outage record, gives the customers out every fifteen
        minutes in each county. On county-days with a NOAA storm report, outage customer-hours per thousand
        customers averaged about {storm_lvl:.0f}, against about {calm_lvl:.0f} on calm days: about twelve times,
        {ratio:.1f}, with a 95 percent interval of {lo:.1f} to {hi:.1f}, resampling whole days. It holds on non-major
        days, {nmed:.1f} times; in the counties Dominion serves alone, {donly:.1f}; and in every year from 2015 to
        2025, between {min(yrs):.1f} and {max(yrs):.1f} times. Two cautions: EAGLE-I counts every utility's
        customers in a county, so this is not Dominion's SAIDI; and storm reports partly follow damage, so it's an
        association, not a cause. The year-level fit and the largest events are in the appendix.""")
    else:
        b.title(s, "Years with more storm days had more outage minutes (r = 0.70 over ten years)")
        b.picture(s, CH0 / "s4_storm_days_vs_saidi.png", L, TOP - 0.03,
                  "Scatter: storm county-days against SAIDI ex-MED, 2015-2024, with a fitted line; r = 0.70. 2025 "
                  "(796 county-days, 144.4 minutes) sits on the line (145.3 from the fit).")
        b.col(s, rx, TOP + 0.02, rw, [
            ("rule", 0.08),
            (f"{cd24} → {cd25}", LIGHT, 40, ds.INK, 0.0),
            ("storm county-days in Dominion's Virginia counties, 2024 → 2025", REG, 16, ds.INK_2, 0.22),
            ("rule", 0.08),
            ("r = 0.70", LIGHT, 40, ds.INK, 0.0),
            ("over 2015–2024 (n = 10): an association, not a cause. The fit, made without 2025, gives 145.3; the "
             "actual was 144.4.", REG, 16, ds.INK_2, 0.0),
        ], BOTTOM, "S4 right")
        why(s, "reporting reliability next to storm exposure would keep a stormy year from being read as a trend.")
        b.source(s, "NOAA Storm Events 2015–2025, wind, winter and tropical event types, by county in Dominion's "
                    "Virginia service territory (EIA-861); EIA-861 SAIDI excluding major event days; least-squares "
                    "fit on 2015–2024.", 4)
        b.notes(s, f"""Weather is the obvious question. I counted storm county-days: each day a line-damaging storm,
        such as thunderstorm wind, an ice storm or a tropical storm, was recorded in a Virginia county Dominion
        serves, from NOAA's Storm Events data. 2025 had {cd25}, up from {cd24} in 2024. Over 2015 to 2024, years with
        more storm days had more outage minutes: the correlation is 0.70. That's ten points, so I treat it as a
        check, not a model. The fit, made without 2025, puts 2025 at 145.3 minutes; the actual was 144.4. So 2025
        looks like a stormy year more than a break in the trend, which is consistent with the annual report. What
        this can't say is which circuits or causes; that needs outage records.""")

    # ------------------------------------------------------------------ S5 the Power BI report (new)
    s = new()
    b.title(s, "The Power BI report: one page per question, on customer-weighted measures")
    shot = SHOTS / ARGS.shot
    sw_ = 6.95
    sh_ = sw_ * 1575 / 2790                     # the crops are 2790 x 1575 (16:9 canvas)
    if not ADOPT:
        # Public (rulings 4 and O-33): the candidate's current report as built, never the upgraded one; only the
        # What moved page's frequency chart (its CAIDI chart is titled "minutes to restore"). Its printed values are
        # screenshot content, not claims.
        ly = TOP + 0.5                           # two-line label; the frequency chart is 2.22:1, so it still fits
        b.tb(s, L, TOP - 0.08, sw_, 0.55, [[("My current report: ", SEMI, ds.INK),
                                           ("the What moved page, frequency chart (EIA-861, Import mode)", REG,
                                            ds.INK_2)]], 15, name="S5 label")
        if PUBLIC_SHOT.exists():
            fit_picture(s, PUBLIC_SHOT, L, ly, sw_, BOTTOM - ly,
                        "Screenshot of my current Power BI report, the What moved page's frequency chart: outages per "
                        "customer (SAIFI) by year since 2013, against its 2019 level.")
        else:
            b.rect(s, L, ly, sw_, BOTTOM - ly, ds.TINT, line=ds.RULE)
            b.PROBLEMS.append(f"PLACEHOLDER: public S5 screenshot {PUBLIC_SHOT} not found")
    elif shot.exists():
        fit_picture(s, shot, L, TOP - 0.03, sw_, sh_,
                    S5_ALT)
    else:
        b.rect(s, L, TOP - 0.03, sw_, sh_, ds.TINT, line=ds.RULE)
        b.tb(s, L + 0.3, TOP + 1.7, sw_ - 0.6, 0.6, [[("Report screenshot to come", SEMI, ds.MUTED)]], 20,
             align="center", name="S5 placeholder")
        b.PROBLEMS.append(f"PLACEHOLDER: S5 screenshot {shot.name} not found in {SHOTS}")
    px = L + sw_ + 0.3
    pw = R - px
    # star-schema thumbnail: the one relationship, FCT_RELIABILITY many-to-one DIM_UTILITY
    fy = TOP + 0.02
    fw, dw, bh = 2.32, 1.55, 0.7
    b.rect(s, px, fy, fw, bh, ds.SUBJECT_TINT, line=ds.RULE)
    b.col(s, px + 0.1, fy + 0.07, fw - 0.2, [("FCT_RELIABILITY", SEMI, 14, ds.INK, 0.0),
                                              ("utility × state × year", REG, 14, ds.INK_2, 0.0)], fy + bh,
          "S5 fact")
    aw_ = pw - fw - dw - 0.12
    b.arrow(s, px + fw + 0.06, fy + 0.12, w=aw_, h=0.24)
    b.tb(s, px + fw + 0.02, fy + 0.4, aw_ + 0.08, 0.3, [[("many:1", REG, ds.MUTED)]], 14, align="center",
         name="S5 many:1")
    b.rect(s, px + pw - dw, fy, dw, bh, "#FFFFFF", line=ds.RULE)
    b.col(s, px + pw - dw + 0.1, fy + 0.07, dw - 0.2, [("DIM_UTILITY", SEMI, 14, ds.INK, 0.0),
                                                        ("peer group", REG, 14, ds.INK_2, 0.0)], fy + bh, "S5 dim")
    if ADOPT:   # F22: the VAR form, exact text of deliverables/04_powerbi/measures.dax, laid out on lines
        about = ("18 tables through one DataFolder parameter (Import); 11 pages, ending on Data notes: 31 tests, "
                 "12 of 12 reconciled.")
        lead = "Customer-weighted measures; the cards follow the year slicer:"
        code = ["Selected SAIDI =", "VAR SelectedYear =", "    SELECTEDVALUE('Dashboard Year'[Year], 2025)",
                "RETURN", "    CALCULATE([SAIDI ex MED],", "        FCT_RELIABILITY[YEAR] = SelectedYear)"]
    else:       # origin/main powerbi/measures.dax
        about = "Import for presentation, DirectQuery during development (D13)."
        lead = "Customer-weighted measures; the 3-year figure averages the annual values:"
        code = ["SAIDI 3yr ending 2025 =", "CALCULATE(", "    AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]),",
                "        [SAIDI ex MED]),", "    FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025})"]
    for c_ in code:
        if b.text_w(c_, REG, 14) / 72 > pw - 0.3:
            b.PROBLEMS.append(f"S5 code line too wide: {c_!r}")
    yc = b.col(s, px, fy + bh + 0.12, pw, [(about, REG, 15, ds.INK_2, 0.1), ("rule", 0.08),
                                           (lead, SEMI, 15, ds.INK, 0.06)], BOTTOM, "S5 right")
    ch_ = len(code) * 14 * b.EM_LINE / 72 + 0.16
    b.rect(s, px, yc, pw, ch_, ds.TINT)
    b.col(s, px + 0.14, yc + 0.08, pw - 0.28, [(c_, REG, 14, ds.INK, 0.0) for c_ in code], BOTTOM, "S5 code")
    why(s, "Power BI reporting leads the role's duties, and the same model and measures could carry a "
           "program-tracking report.")
    b.source(s, ("Power BI Desktop, the project's report: Summary page, year 2025. Tables are the mart's CSV exports, "
                 "imported through a folder parameter; measures as in the project's measures.dax." if ADOPT else
                 "Power BI Desktop, the project's report (.pbix; not on GitHub, by design): What moved page, Import "
                 "mode. Measures as in the project's powerbi/measures.dax."), 5)
    if ADOPT:
        b.notes(s, """The role's first listed duty is Power BI, so here is the report. Each page answers one
        question: the scorecard, what moved, weather, the fair comparison, outages by county, storms, growth and
        demand, and it ends on a data notes page with the 31 tests and the twelve reconciled values. The model is a
        star: one fact table at utility, state and year, many-to-one to a utility dimension for names and peer
        groups. Measures are customer-weighted: SAIDI is total customer-minutes over total customers, and the KPI
        cards follow the year slicer through Selected SAIDI. The report imports eighteen tables from the mart's CSV
        exports through one folder parameter, so it opens with no network or running warehouse.""")
    else:
        b.notes(s, """The role's first listed duty is Power BI, so here is my current report. This is the frequency
        chart from its What moved page: how often the average customer loses power each year, against the 2019
        level. Each page answers one question: scorecards, what moved, weather, the peer comparison, growth,
        seasonal demand, and two executive summaries. The model is a star: one fact table at utility, state and year,
        many-to-one to a utility dimension for names and peer groups. Measures are customer-weighted: SAIDI is total
        customer-minutes over total customers, and the three-year figure averages the three annual values, as
        Dominion reports it. I built it in DirectQuery against Snowflake during development; decision D13 is Import
        for presentation, and this chart runs on imported data.""")

    # ------------------------------------------------------------------ S6 how it's built
    s = new()
    b.title(s, "Built with production habits: tested, documented, and reconciled to the reported numbers")
    y0, y1 = TOP + 0.02, 4.22
    aw, src_w, pbi_w = 0.3, 3.5, 1.75
    sf_x = L + src_w + aw + 0.04
    sf_w = R - pbi_w - aw - 0.04 - sf_x
    b.rect(s, L, y0, src_w, y1 - y0, "#FFFFFF", line=ds.RULE)
    srcs = [("EIA-861 reliability", "24,358 + 977 rows"), ("NOAA Storm Events", "831,288 rows")]
    if ADOPT:
        srcs += [("EAGLE-I county outages", "11,608,442 rows"), ("EIA-930 hourly demand", "6,094,320 rows")]
    else:
        srcs += [("EIA-930 hourly demand", "6,077,232 rows")]
    items = [("Public sources", SEMI, 16, ds.INK, 0.06)]
    for n_, c_ in srcs:
        items += [(n_, SEMI, 15, ds.INK, 0.0), (c_, REG, 14, ds.INK_2, 0.0 if ADOPT else 0.08)]
    b.col(s, L + 0.18, y0 + 0.12, src_w - 0.36, items, y1, "S6 sources")
    b.arrow(s, L + src_w + 0.02, (y0 + y1) / 2 - 0.13)
    b.rect(s, sf_x, y0, sf_w, y1 - y0, ds.TINT)
    b.tb(s, sf_x + 0.18, y0 + 0.1, 3.0, 0.32, [[("Snowflake", SEMI, ds.INK_2)]], 16, name="S6 snowflake")
    inner = [("RAW", "as published, all text"), ("STG", "typed and cleaned"), ("MART", "facts, dimensions, views")]
    iaw = 0.26
    bw = (sf_w - 0.36 - 2 * (iaw + 0.06)) / 3
    by0, by1 = y0 + 0.55, y1 - 0.18
    for k, (h_, d_) in enumerate(inner):
        bx = sf_x + 0.18 + k * (bw + iaw + 0.06)
        b.rect(s, bx, by0, bw, by1 - by0, "#FFFFFF", line=ds.RULE)
        b.col(s, bx + 0.14, by0 + 0.14, bw - 0.28, [(h_, SEMI, 18, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)],
              by1, f"S6 {h_}")
        if k < 2:
            b.arrow(s, bx + bw + 0.03, (by0 + by1) / 2 - 0.13, w=iaw)
    b.arrow(s, sf_x + sf_w + 0.02, (y0 + y1) / 2 - 0.13)
    ppx = R - pbi_w
    b.rect(s, ppx, y0, pbi_w, y1 - y0, ds.SUBJECT_TINT)
    pbi = ("Import model and report" if ADOPT else
           "Import for presentation; DirectQuery in development (D13)")
    b.col(s, ppx + 0.16, y0 + 0.14, pbi_w - 0.32, [("Power BI", SEMI, 18, ds.INK, 0.04), (pbi, REG, 16, ds.INK_2,
                                                                                         0.0)], y1, "S6 PBI")
    if ADOPT:
        badges = [("31 tests pass", "Original build: 12 (6 reliability, 3 storm, 3 demand). New tables: 19."),
                  ("Data dictionary", "every table and column; measures defined in docs/05"),
                  ("Decisions log", f"decisions logged ({DRANGE}); the peer set was chosen by EIA ID before results"),
                  ("Reconciled", "12 of 12 rebuilt values match the published figures: a check of definitions")]
    else:
        badges = [("12 tests pass", "keys, SAIDI = SAIFI × CAIDI, EIA's published 2025 values"),
                  ("Data dictionary", "every table and column; measures defined in docs/05"),
                  ("Decisions log", f"decisions logged ({DRANGE}); the peer set was chosen by EIA ID before results"),
                  ("Reconciled", "130.2 and 133.0 rebuilt against 130 and 133; 2025 matches EIA (test T4)")]
    gb = 0.22
    bw4 = (CW - 3 * gb) / 4
    gy0 = y1 + 0.1
    for k, (h_, d_) in enumerate(badges):
        bx = L + k * (bw4 + gb)
        b.rect(s, bx, gy0, bw4, 0.06, ds.SUBJECT if k == 3 else ds.CONTEXT)
        b.col(s, bx, gy0 + 0.14, bw4, [(h_, SEMI, 18, ds.INK, 0.03), (d_, REG, 16, ds.INK_2, 0.0)], BOTTOM,
              f"S6 badge {k + 1}")
    why(s, "the same habits would serve the team's reports: reconcile first, test every load, write each "
           "definition down.")
    b.source(s, (f"Project build: SQL scripts, tests T1–T31 (T1–T12 the original build, T13–T31 the new tables), data "
                 f"dictionary, decisions log {DRANGE}; row counts as loaded." if ADOPT else
                 f"Project build: SQL scripts, tests T1–T12, data dictionary and decisions log {DRANGE}; row counts "
                 f"as loaded."), 6)
    if ADOPT:
        b.notes(s, f"""Briefly, how it's built. Four public sources: EIA's reliability filings, NOAA Storm Events,
        the Department of Energy's EAGLE-I county outages, and EIA-930 hourly demand. They land in Snowflake as raw
        text exactly as published, a staging layer types and cleans them, and a mart of facts, dimensions and views
        feeds the Power BI report. Thirty-one tests pass: twelve on the original build, six of them on reliability,
        three on storms and three on demand, and nineteen on the new tables. The reliability tests check for duplicate
        keys, that SAIDI equals SAIFI times CAIDI, and that the 2025 values match what EIA published. A data dictionary covers every
        table and column, and the measures are defined in the metrics guide. Decisions are logged, {DRANGE}; the
        peer set was chosen by EIA ID before any results. The first check was reconciliation: twelve of twelve
        rebuilt values match the published figures, which confirms the definitions and filters. A local script,
        scripts/run_local_duckdb.py, rebuilds the core mart and runs its checks.""")
    else:
        b.notes(s, f"""Briefly, how it's built. Three public sources: EIA's reliability filings, NOAA Storm Events,
        and EIA-930 hourly demand. They land in Snowflake as raw text exactly as published, a staging layer types and
        cleans them, and a mart of facts, dimensions and views feeds Power BI. I built the report in DirectQuery and
        switch it to Import for presentation, decision D13. Twelve tests run after each load: no duplicate keys,
        SAIDI equals SAIFI times CAIDI, the 2025 values match what EIA published. All pass. A data dictionary covers
        every table and column, and the measures are defined in the metrics guide. Decisions are logged, {DRANGE};
        the peer set was chosen by EIA ID before any results. The first check was reconciliation: 130.2 and 133.0
        rebuilt against the reported 130 and 133, and test T4 matches Dominion's 2025 values to EIA's published
        306.7, 144.4 and 2,675,735 customers. A local script, scripts/run_local_duckdb.py, rebuilds the core mart and
        runs its checks.""")

    # ------------------------------------------------------------------ S7 first 90 days
    s = new()
    b.title(s, "With Dominion's outage, meter and circuit data: the questions I'd bring and what I'd build")
    gap = 0.28
    cw3 = (CW - 2 * gap) / 3
    cards = [
        ("Days 1–30", "Learn and reconcile",
         ["Learn how outages, meter events and circuits are recorded and reported.",
          "Rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filed figures."],
         "a reconciled baseline with written definitions"),
        ("Days 31–60", "Ask about frequency",
         ["By circuit and cause code, storm days apart from calm days; repeat interruptions (CEMIn).",
          "Outage times from meter last-gasp and restore messages (99.8% of meters are smart), checked against "
          "OMS."],
         "tested views and a data dictionary"),
        ("Days 61–90", "Build the tracking report",
         ["Track mainfeeder hardening against matched untreated feeders (same pre-period performance), "
          "weather-normalized, in support of the program's selection rule."],
         "a Power BI program-tracking report, refreshed on a schedule"),
    ]
    ytop, ybot = TOP + 0.02, BOTTOM - 0.04
    for i, (days, head, body, deliv) in enumerate(cards):
        x = L + i * (cw3 + gap)
        last = i == 2
        b.rect(s, x, ytop, cw3, ybot - ytop, ds.SUBJECT_TINT if last else ds.TINT)
        b.rect(s, x, ytop, cw3, 0.06, ds.SUBJECT)
        ix, iw = x + 0.2, cw3 - 0.4
        y = b.col(s, ix, ytop + 0.18, iw, [(days, SEMI, 16, ds.MUTED, 0.0), (head, SEMI, 22, ds.INK, 0.12)]
                  + [(t, REG, 16, ds.INK_2, 0.08) for t in body], ybot, f"S7 card {i + 1}")
        dh = b.need_h("Deliverable: " + deliv, SEMI, 16, iw)
        yd = ybot - 0.16 - dh
        if yd < y + 0.05:
            b.PROBLEMS.append(f"S7 card {i + 1}: deliverable collides ({yd:.2f} < {y:.2f})")
        b.hline(s, ix, yd - 0.1, iw, colour=ds.RULE)
        b.tb(s, ix, yd, iw, dh + 0.02, [[("Deliverable: ", SEMI, ds.INK), (deliv, SEMI if last else REG,
                                                                         ds.INK if last else ds.INK_2)]], 16,
             name=f"S7 deliverable {i + 1}")
    why(s, "these are questions to check first with the people who own each definition, not conclusions.")
    b.source(s, "A plan: Dominion data is named by type only, and none was used here. Smart meters: EIA-861 2025 "
                "(advanced meters as a share of all meters). Grid Resiliency: Dominion Energy website, read "
                "November 1, 2026.", 7)
    b.notes(s, """Public data narrows the question; Dominion's own data answers it. Here are the questions I'd
    bring in the first 90 days, and what I'd build. First month: learn how outages, meter events and circuits are
    recorded, then rebuild one year's SAIDI, SAIFI and CAIDI and reconcile them to the filed numbers. Second month:
    interruptions by circuit and cause code, storm days apart from calm days, and customers interrupted repeatedly.
    Meters mark when an outage starts and ends, which can be checked against the outage system's times. Third month:
    a Power BI report that tracks mainfeeder hardening against matched untreated feeders, weather-normalized, in
    support of the program's own selection rule. I'd check each of these first with the people who own the
    definitions.""")

    # ------------------------------------------------------------------ S8 close
    s = new()
    b.title(s, "Three takeaways: a stormier year, a frequency gap, and storms by county")
    g3 = 0.35
    w3 = (CW - 2 * g3) / 3
    take3 = ("Storm county-days carry far more outage hours, so report reliability beside storm exposure"
             if ADOPT else "Report reliability beside county storm exposure, so a stormy year isn't read as a trend")
    takeaways = [("1", "A stormier year",
                  "More storms and more interruptions in 2025; no clear trend once storms are counted"),
                 ("2", "Frequency is the peer gap",
                  "So causes are the question, and answering it needs outage records by cause code"),
                 ("3", "Storms by county", take3)]
    for k, (n_, h_, d_) in enumerate(takeaways):
        x = L + k * (w3 + g3)
        b.tb(s, x, TOP - 0.1, 0.5, 0.7, [[(n_, LIGHT, ds.SUBJECT)]], 40, ls=0.9, name="S8 numeral")
        b.col(s, x + 0.52, TOP, w3 - 0.52, [(h_, SEMI, 20, ds.INK, 0.04), (d_, REG, 16, ds.INK_2, 0.0)], 3.05,
              f"S8 take {k + 1}")
    b.hline(s, L, 3.12, CW, colour=ds.RULE)
    b.tb(s, L, 3.24, CW, 0.4, [[("I've built a tested Snowflake → Power BI pipeline on public reliability data.",
                                 SEMI, ds.INK)]], 20, ls=0.95, name="S8 fit")
    b.tb(s, L, 3.88, CW, 0.28, [[("How my experience maps", SEMI, ds.MUTED),
                                  ("   Mercury Insurance, Data Analyst", REG, ds.MUTED)]], ds.DECK["source_pt"],
         name="S8 strip label")
    maps = [("Snowflake pipeline, 20M+ rows", "this project's mart"),
            ("Root-cause analysis on joined data", "what I'd do with cause codes in the first 90 days"),   # V2 F11
            ("Metadata and business definitions", "the data dictionary")]
    for k, (a_, b_) in enumerate(maps):
        x = L + k * (w3 + g3)
        b.rect(s, x, 4.22, w3, 0.05, ds.CONTEXT)
        b.col(s, x, 4.34, w3, [(a_, SEMI, 16, ds.INK, 0.02), ("→ " + b_, REG, 16, ds.INK_2, 0.0)], BOTTOM,
              f"S8 map {k + 1}")
    closing(s, "Thank you. I'd like to do this work with your team.")
    b.source(s, "Takeaways: slides 2–4. Experience: Mercury Insurance, Data Analyst, 2026 to present.", 8)
    t3 = ("Three: storm county-days carry far more outage hours than calm ones, so I'd report reliability beside "
          "storm exposure by county." if ADOPT else
          "Three: I'd report reliability beside county-level storm exposure, so a stormy year isn't read as a "
          "trend.")
    b.notes(s, f"""Three takeaways. One: 2025 was a stormier year, with more storms and more interruptions, and once
    storms are counted there's no clear underlying trend. Two: frequency is where Dominion differs from its peers,
    so the useful question is what causes the interruptions, and that needs outage records by cause; the ranks are
    indicative. {t3} On fit: at Mercury Insurance I built a Snowflake pipeline across policy, claims and billing
    data, over 20 million rows, and led a root-cause analysis on joined data. I've built a tested Snowflake to Power
    BI pipeline on public reliability data, and I'd like to do this work with your team. Thank you; I'm happy to
    take questions.""")

    # ------------------------------------------------------------------ A1 definitions (+ MED share)
    s = new()
    b.title(s, "Definitions: SAIDI = SAIFI × CAIDI, and major event days are set aside by rule")
    bw_ = 3.35
    op = (CW - 3 * bw_) / 2
    defs = [("SAIDI", "outage minutes per customer per year"),
            ("SAIFI", "interruptions per customer per year: how often"),
            ("CAIDI", "minutes per interruption: how long")]
    for k, (h_, d_) in enumerate(defs):
        x = L + k * (bw_ + op)
        b.rect(s, x, TOP + 0.05, bw_, 1.2, ds.SUBJECT_TINT if k == 1 else ds.TINT)
        b.col(s, x + 0.2, TOP + 0.17, bw_ - 0.4, [(h_, SEMI, 24, ds.INK, 0.02), (d_, REG, 16, ds.INK_2, 0.0)],
              TOP + 1.25, f"A1 {h_}")
        if k < 2:
            b.tb(s, x + bw_, TOP + 0.28, op, 0.8, [[("=" if k == 0 else "×", LIGHT, ds.INK)]], 40, align="center",
                 name="A1 op")
    b.tb(s, L, TOP + 1.4, CW, 0.36, [[("Dominion 2025: ", SEMI, ds.INK),
                                      ("1.320 × 109.4 = 144.4 minutes (excluding major event days)", REG,
                                       ds.INK_2)]], 16, name="A1 example")
    b.col(s, L, TOP + 1.95, CW, [
        ("Major event days (MED): IEEE 1366's 2.5 beta method takes five years of daily SAIDI, drops zero days, and "
         "sets α and β as the mean and standard deviation of ln(daily SAIDI); a day above exp(α + 2.5β) is an MED.",
         REG, 16, ds.INK_2, 0.12),
        ("Dominion reports to EIA under a non-IEEE rule (“Other” in EIA-861); most peers in this deck use IEEE 1366."
         if ADOPT else "Dominion reports to EIA under its own major-event rule (“Other” in EIA-861); methods differ "
         "between utilities.", REG, 16, ds.INK_2, 0.12),
        ("With major event days, 2025 SAIDI was 306.7 minutes, against 144.4 without them: MEDs held 53%.", REG, 16,
         ds.INK_2, 0.12),
        ("Log split: ln(SAIDI ratio) = ln(SAIFI ratio) + ln(CAIDI ratio). From 2022, duration fell, so frequency "
         "accounts for more than all of the rise; from 2023, 79%.", REG, 16, ds.INK_2, 0.0),
    ], BOTTOM_APX, "A1 text")
    b.source(s, "IEEE Std 1366; EIA-861 reliability, Dominion Energy Virginia, 2022, 2023 and 2025.", "A1")
    b.notes(s, """Definitions for reference. SAIDI equals SAIFI times CAIDI, which is why a change in SAIDI splits
    exactly into a frequency part and a duration part using logs. The split depends on the base year: from 2022,
    minutes per interruption fell, so frequency explains more than the whole rise.""")

    # ------------------------------------------------------------------ A2 weather fit
    s = new()
    b.title(s, "The weather fit is a check on one year, not a forecast")
    if ADOPT:
        rows = [["Year", "Storm\ncounty-days", "SAIDI\nex‑MED", "From\nthe fit", "Difference"]]
        cols, al = [2.0, 1.55, 1.25, 1.25, 1.25], "lrrrr"
    else:
        rows = [["Year", "Storm\ncounty-days", "SAIDI\nex‑MED", "From\nthe fit"]]
        cols, al = [2.4, 1.75, 1.6, 1.55], "lrrr"
    for r_ in fit:
        yr = int(r_["year"])
        cd, sd = float(r_["storm_county_days"]), float(r_["saidi_ex_med"])
        fv = b0 + b1_ * cd if ADOPT else wb_pred[yr]
        row = [f"{yr}" + (" (not in fit)" if yr == 2025 else ""), f"{cd:,.0f}", f"{sd:.1f}", f"{fv:.1f}"]
        if ADOPT:
            row.append(f"{sd - fv:+.1f}".replace("-", "−"))
        rows.append(row)
    b.table(s, L, TOP + 0.02, 7.3, cols, rows, pt=16, row_h=0.355, highlight=len(rows) - 1, align=al)
    if ADOPT:
        t_fit = r_fit * math.sqrt(8 / (1 - r_fit ** 2))
        z = math.atanh(r_fit)
        ci_lo, ci_hi = math.tanh(z - 1.96 / math.sqrt(7)), math.tanh(z + 1.96 / math.sqrt(7))
        assert (f"{t_fit:.2f}", f"{ci_lo:.2f}", f"{ci_hi:.2f}") == ("2.75", "0.12", "0.92")
        fit_line = (f"Fit on 2015–2024 (n = 10): SAIDI = {b0:.1f} + {b1_:.4f} × storm county-days; "
                    f"r = {r_fit:.2f} (t = {t_fit:.2f}, p = 0.025; 95% CI {ci_lo:.2f} "
                    f"to {ci_hi:.2f}), R² {r_fit * r_fit:.2f}.")
        trend = ("Adjusted for storm days, the trend since 2015 is not distinguishable from zero: about +0.3 minutes "
                 "a year (95% range −1.4 to +2.1).")
    else:
        fit_line = (f"Fit on 2015–2024 (n = 10): SAIDI = {b0:.1f} + {b1_:.4f} × storm county-days; "
                    f"r = {r_fit:.2f}, R² {r_fit * r_fit:.2f}.")
        trend = "Adjusted for storm days, there is no clear trend since 2015."
    b.col(s, L + 7.75, TOP + 0.02, CW - 7.75, [
        ("rule", 0.1),
        (fit_line, REG, 16, ds.INK_2, 0.1 if ADOPT else 0.16),
        ("Why 2015: the change to automated outage recording that year shifts the level (decision D6).", REG, 16,
         ds.INK_2, 0.1 if ADOPT else 0.16),
        ("rule", 0.1),
        ((f"2025, left out of the fit: {pred25:.1f} from the fit (95% prediction interval 122.3–168.2), 144.4 "
          "actual." if ADOPT else f"2025 was left out: the fit gives {pred25:.1f}, the actual was 144.4."),
         REG, 16, ds.INK_2, 0.12 if ADOPT else 0.16),
        ("rule", 0.1),
        (trend, REG, 16, ds.INK_2, 0.0),
    ], BOTTOM_APX, "A2 right")
    b.source(s, "NOAA Storm Events and EIA-861, 2015–2025; ordinary least squares on ten annual points "
                "(exploratory)." + (" Storm county-days count Bedford city once (decision D22)." if ADOPT else ""),
             "A2")
    if ADOPT:
        b.notes(s, """Ten annual points, so the fit is a check, not a forecast. r is 0.70, but with ten points its 95
        percent interval runs from about 0.12 to 0.92, weak to very strong, so on its own this is thin evidence; the
        county-day comparison on slide 4 rests on 6,108 storm county-days with complete outage readings. The table's
        storm county-days count all 103 Virginia counties Dominion serves. The fit starts in 2015 because the change
        to automated outage recording that year shifts the level. 2025 was left out of the fit and lands within a
        minute of it; the 95 percent prediction interval for a single new year was about 122 to 168 minutes. After the storm-day adjustment, the trend since 2015 is about plus 0.3 minutes a year, with a
        range that includes zero.""")
    else:
        b.notes(s, """Ten annual points, so the fit is a check, not a forecast. It starts in 2015 because the change
        to automated outage recording that year shifts the level, decision D6. 2025 was left out of the fit and lands
        within a minute of it. Once storm days are allowed for, there is no clear trend since 2015.""")

    # ------------------------------------------------------------------ A3 load shape (was S5)
    s = new()
    b.title(s, "Overnight demand grew faster than afternoon demand; winter rivals summer for the peak")
    if ADOPT:
        b.picture(s, CH1 / "s5_hourly_growth_2019_2025.png", L, TOP - 0.03,
                  "Columns for the 24 hours of the day: growth in average load from 2019 to 2025, PJM Dominion zone. "
                  "Hours ending 1-5 a.m. are highlighted at +39% to +41%; hours ending 1-5 p.m. about +27%, the "
                  "lowest of the day.")
        tiles = [("+39–41%", "average load, hours ending 1–5 a.m., 2019 → 2025 (1–5 p.m.: about +27%)"),
                 ("Winter", "set the yearly peak in 2019, 2022 and 2025; 2026 so far: winter 25,413 vs summer 25,384 "
                            "MW, a tie")]
        src = ("EIA-930 hourly demand, PJM Dominion (DOM) zone, which is wider than Dominion's retail territory; 2019 "
               "and 2025 full years; 2026 to the hour ending midnight, Oct 29. Winter = Dec–Feb, summer = Jun–Aug.")
    else:
        b.picture(s, CH2 / "a3_load_profile_public.png", L, TOP - 0.03,
                  "Columns for the 24 hours of the day: growth in average load from 2019 to 2025, PJM Dominion zone. "
                  "4 a.m. +41%; 4 p.m. +27%.")
        tiles = [("+41%", "average load at 4 a.m., 2019 → 2025 (4 p.m.: +27%)"),
                 ("Winter", "set the yearly peak in 2019, 2022 and 2025")]
        src = ("EIA-930 hourly demand, PJM Dominion (DOM) zone, which is wider than Dominion's retail territory; 2019 "
               "and 2025 full years. Winter = Dec–Feb, summer = Jun–Aug.")
    items = []
    for big, small in tiles:
        items += [("rule", 0.08), (big, LIGHT, 40, ds.INK, 0.0), (small, REG, 16, ds.INK_2, 0.2)]
    items += [("Highest hour of the year +26%, lowest hour +52%.", REG, 16, ds.INK_2, 0.16),
              ("I'd add winter and overnight views to load and outage reports.", SEMI, 16, ds.INK, 0.0)]
    b.col(s, rx, TOP + 0.02, rw, items, BOTTOM_APX, "A3 right")
    b.source(s, src, "A3")
    if ADOPT:
        b.notes(s, """EIA's hourly demand for the PJM Dominion zone, which is wider than Dominion's retail territory.
        From 2019 to 2025 the hours ending 1 to 5 a.m. grew 39 to 41 percent, the hours ending 1 to 5 p.m. about 27.
        Holding Virginia's heating and cooling degree days and the weekday fixed, average load still rose about 33
        percent, against 32 unadjusted. Winter set the yearly peak in 2019, 2022 and 2025, and 2026 so far is a tie.
        The two winter events in A6 took about 100 hours to clear 90 percent of the outage, against 20 to 66 for
        the other eight: two events, so a pointer, not a finding. This data can't identify customers, so I don't
        attribute the growth to data centers.""")
    else:
        b.notes(s, """EIA's hourly demand for the PJM Dominion zone, which is wider than Dominion's retail territory.
        From 2019 to 2025 average load at 4 a.m. grew 41 percent, against 27 percent at 4 p.m. Winter set the yearly
        peak in 2019, 2022 and 2025. The highest hour of the year rose 26 percent and the lowest 52. This data can't
        identify customers, so I don't attribute the growth to data centers.""")

    # ------------------------------------------------------------------ A4 sources and tests
    s = new()
    b.title(s, "Every number traces to a public source; the tables behind them are tested after each load")
    rows = [["Source", "Publisher", "Years", "Grain", "Rows"],
            ["EIA-861 Reliability, 2025 final", "EIA", "2025", "utility × state × year", "977"],
            ["PUDL EIA-861 reliability", "Catalyst Cooperative", "2013–2024", "utility × state × year", "24,358"],
            ["EIA-861 Service Territory", "EIA", "2025", "utility × county", "11,803"],
            ["NOAA Storm Events", "NOAA NCEI", "2013–2025", "storm event", "831,288"]]
    if ADOPT:
        rows += [["EAGLE-I county outages", "ORNL for DOE", "Nov 2014–2025", "county × 15 minutes", "11,608,442"],
                 ["EIA-930 hourly demand", "EIA", "Jul 2018–Oct 2026", "region × hour", "6,094,320"],
                 ["HURDAT2 storm tracks", "NOAA NHC", "1851–2025", "storm × 6-hour fix", "55,524"],
                 ["DOE-417 disturbance reports", "DOE", "2014–2025", "reported event", "3,702"],
                 ["CPC degree days", "NOAA CPC", "2018–Oct 2026", "state × day", "309,504"]]
    else:
        rows += [["EIA-930 hourly demand", "EIA", "Jul 2018–Oct 2026", "region × hour", "6,077,232"]]
    rows += [["Dominion Energy 2025 Annual Report", "Dominion Energy", "2025", "document (130, 133)", "reference"]]
    rh = 0.33 if ADOPT else 0.42
    b.table(s, L, TOP + 0.02, CW, [3.9, 2.35, 2.05, 2.55, 1.283], rows, pt=15 if ADOPT else 16, row_h=rh,
            align="lllll")
    if ADOPT:
        tests = [("Tests T1–T31, all pass: ", SEMI, ds.INK),
                 ("T1–T6 on the reliability mart (no duplicate keys; SAIDI = SAIFI × CAIDI within 2%; Dominion 2025 "
                  "equals EIA's published 306.7, 144.4 and 2,675,735 customers); T7–T9 on NOAA storms; T10–T12 on "
                  "EIA-930 demand; T13–T31 on the new tables. ", REG, ds.INK_2),
                 ("Reconciled 12 of 12 ", SEMI, ds.INK),
                 ("against the annual report and the EIA-861 files.", REG, ds.INK_2)]
    else:
        tests = [("Tests after each load (T1–T12, all pass): ", SEMI, ds.INK),
                 ("no duplicate keys; SAIDI = SAIFI × CAIDI within 2%; Dominion 2025 equals EIA's published 306.7, "
                  "144.4 and 2,675,735 customers; every county mapped; full years; no duplicate hours.", REG,
                  ds.INK_2)]
    b.tb(s, L, TOP + 0.02 + rh * len(rows) + 0.18, CW, 1.0, [tests], 15 if ADOPT else 16, name="A4 tests")
    b.source(s, "Project documentation: sources register (publisher, vintage, license) and data-quality tests; all "
                "public data.", "A4")
    if ADOPT:
        b.notes(s, """Every source is public and every load is tested; the rows are as loaded. The twelve reconciled
        values: the two three-year SAIDI figures from the annual report, and from the EIA-861 files 2025 SAIDI,
        SAIFI, CAIDI and all-event SAIDI, 2025 customers, the same four measures for 2024, and 2025 commercial sales.
        It confirms definitions and filters; it is not an independent measurement.""")
    else:
        b.notes(s, """Every source is public and every load is tested. The rows are as loaded; the license and
        vintage of each file are in the project's sources register.""")

    # ------------------------------------------------------------------ A5 limits
    s = new()
    b.title(s, "What public data cannot show, and what would answer it")
    rows = [["Public data limit", "What would answer it (Dominion data, by type)"],
            ["One number per utility per year (EIA-861)", "Outage records by event, circuit and cause"],
            ["Storms counted by county, not by line", "Outage records with cause codes and circuit location"],
            ["Methods differ between utilities", "Dominion's daily SAIDI and its filing method"],
            ["The DOM zone is wider than the retail territory", "Meter interval data by circuit"],
            ["No customer identities: growth can't be attributed", "Customer class and large-load records"]]
    b.table(s, L, TOP + 0.02, CW, [5.6, 6.533], rows, pt=16, row_h=0.5, align="ll")
    b.source(s, "Project scope limits (decision D14) and the sources above.", "A5")
    b.notes(s, """These are the limits I'd name before anyone else does. Each one is answered by a kind of internal
    data, named by type only.""")

    # ------------------------------------------------------------------ A6 events + Isaias (adopted) / peer table
    s = new()
    if ADOPT:
        b.title(s, "The ten largest outage events since 2014: three tropical, two winter, five wind")
        rows = [["#", "Peak day", "Storm type", "Peak\ncustomers out", "Held\n1 h", "Hours to\nclear 90%"]]
        hi_row, kinds = None, []
        for i, e in enumerate(events, start=1):
            d = dt.date.fromisoformat(e["peak_day"])
            kind = e["storm_type"].capitalize() + (f" ({e['tropical_cyclone'].title()})" if e["tropical_cyclone"]
                                                   else "")
            kinds.append(e["storm_type"])
            rows.append([e["rank"], f"{d.strftime('%b')} {d.day}, {d.year}", kind,
                         f"{float(e['peak_customers_out']):,.0f}", f"{float(e['peak_sustained_1h']):,.0f}",
                         f"{float(e['hours_to_90pct']):.1f}"])
            if e["tropical_cyclone"] == "ISAIAS":
                hi_row = i
                assert float(e["peak_customers_out"]) == 351738 and float(e["peak_sustained_1h"]) == 343492
                assert e["hours_to_90pct"] == "33.5"
        assert (kinds.count("tropical"), kinds.count("winter"), kinds.count("wind")) == (3, 2, 5)
        tw = [0.42, 1.5, 2.05, 1.75, 1.25, 1.3]
        b.table(s, L, TOP - 0.02, sum(tw), tw, rows, pt=16, row_h=0.355, highlight=hi_row, align="rllrrr")
        b.picture(s, CH2 / "a6_isaias_curve.png", L + sum(tw) + 0.3, TOP - 0.02,
                  "Line: Isaias, August 2020, share of the outage cleared by hours after the peak, net of new "
                  "outages; 90% cleared 33.5 hours after the peak.")
        b.source(s, "EAGLE-I (ORNL), all utilities in Dominion's 103 counties, Nov 2014–2025; storm type from NOAA and "
                    "HURDAT2. Cleared = (peak − customers out) ÷ (peak − pre-event level): a net count, not a "
                    "utility's “% of affected customers restored”.", "A6")
        b.notes(s, """These are EAGLE-I events: every utility's customers in the counties Dominion serves, so not
        Dominion's own event records. Events are ranked by the highest count held for an hour; the peak is the
        highest fifteen-minute count. Hours to clear 90 percent run from the peak until 90 percent of the outage
        above the pre-event level has cleared. It's a net count, so it is not a utility's share of affected
        customers restored, which counts everyone affected and looks slower. Michael in 2018 is the largest,
        558,729 customers out at the peak. The two winter storms took about 100 hours to clear 90 percent. Across
        47 events with at least 50,000 customers out, after allowing for size, there's no evidence that clearing got
        faster: hours to clear 90 percent moved plus 4.6 percent a year, p = 0.07, not significant. Isaias,
        highlighted, is the largest event with a matching federal report: DOE-417 lists 508,000 customers affected
        in Virginia. The February 2025 event merges two storms.""")
    else:
        b.title(s, "The 12-utility comparison (Dominion and 11 peers), with each utility's reporting method")
        pr = sorted(peers, key=lambda d: -float(d["saifi_5yr_2021_25"]))
        rows = [["Utility", "Major-event method", "SAIFI 2021–25", "CAIDI 2021–25", "SAIDI 2023–25"]]
        hi_row = None
        for i, d in enumerate(pr, start=1):
            rows.append([d["utility"], d["major_event_method"], f"{float(d['saifi_5yr_2021_25']):.2f}",
                         f"{float(d['caidi_5yr_2021_25']):.0f}", f"{float(d['saidi_3yr_2023_25']):.0f}"])
            if d["utility"] == "Dominion Energy Virginia":
                hi_row = i
        b.table(s, L, TOP - 0.02, CW, [4.2, 2.6, 1.78, 1.78, 1.773], rows, pt=16, row_h=0.355, highlight=hi_row,
                align="llrrr")
        b.source(s, "EIA-861 / PUDL, excluding major event days; means of annual values; sorted by SAIFI. Peers chosen "
                    "by EIA ID before results (D10). Methods as labeled in the project's Power BI data; Mixed: “Other” "
                    "in 2013 only, IEEE 1366 for 2014–25.", "A6")
        b.notes(s, """The full table, sorted by frequency: Dominion is fourth of the twelve. Methods differ, so treat
        the ranks as indicative.""")

    # ------------------------------------------------------------------ write, render, proof
    print("runs with a newline turned into line breaks:", fix_line_breaks(prs))
    pptx = OUT / f"{STEM}.pptx"
    prs.save(pptx)
    print("saved", pptx)
    for p in b.PROBLEMS:
        print("  !", p)
    pdf = pipeline.pptx_to_pdf(pptx, PROOFS)
    letter = pipeline.impose_letter_landscape(pdf, OUT / f"{STEM}_print_letter.pdf", scale=ds.PRINT_SCALE)
    blank_pdf_metadata(letter)
    print("print pdf", letter)
    for grey in (False, True):
        pipeline.pdf_to_pngs(pdf, PROOFS, dpi=110, grey=grey)
    print("min printed sizes:", sorted({round(x[1], 2) for x in pipeline.pdf_min_font_size(letter)}))
    print("fonts:", pipeline.pdf_fonts(letter))
    print("notes words:", [len(sl.notes_slide.notes_text_frame.text.split()) for sl in prs.slides])


def fix_line_breaks(prs) -> int:
    """A newline inside a run's <a:t> (the two-line table headers) is not a line break in DrawingML: LibreOffice
    printed the first line left-aligned under a right-aligned column. Split such runs at the newline into runs
    joined by <a:br/>, each keeping the run's formatting."""
    import copy
    from pptx.oxml.ns import qn
    n = 0
    for slide in prs.slides:
        for r in list(slide._element.iter(qn("a:r"))):
            t = r.find(qn("a:t"))
            if t is None or not t.text or "\n" not in t.text:
                continue
            parts = t.text.split("\n")
            t.text = parts[0]
            rpr = r.find(qn("a:rPr"))
            anchor = r
            for part in parts[1:]:
                br = copy.deepcopy(r)            # same element type as needed below; rebuilt as <a:br>
                br.tag = qn("a:br")
                for child in list(br):
                    if child.tag != qn("a:rPr"):
                        br.remove(child)
                nxt = copy.deepcopy(r)
                nxt.find(qn("a:t")).text = part
                anchor.addnext(br)
                br.addnext(nxt)
                anchor = nxt
            n += 1
            assert rpr is None or r.find(qn("a:rPr")) is not None
    return n


def blank_pdf_metadata(pdf: Path):
    """Flag (e): no producing-tool names in the printed PDF's metadata."""
    import pymupdf
    doc = pymupdf.open(str(pdf))
    doc.set_metadata({"title": "Dominion Energy Virginia reliability", "author": "Saketh Bollina", "subject": "",
                      "keywords": "", "creator": "", "producer": ""})
    tmp = pdf.with_suffix(".tmp.pdf")
    doc.save(str(tmp), garbage=3, deflate=True)
    doc.close()
    tmp.replace(pdf)


if __name__ == "__main__":
    main()
