"""Validate the small annual summaries committed with this project.

This checks arithmetic and that the saved CSVs agree with each other.
It does not rebuild the NOAA or EIA-930 raw-data pipelines.
"""
import csv
import sys
from math import isclose, sqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "output"


def rows(filename):
    with (OUT / filename).open(newline="", encoding="utf-8") as stream:
        records = list(csv.DictReader(stream))
    assert records, f"{filename} contains no rows"
    return records


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("PASS:", message)


storm = {int(r["year"]): r for r in rows("storm_index.csv")}
paired = {int(r["year"]): r for r in rows("storm_vs_saidi.csv")}
check(set(storm) == set(paired) == set(range(2013, 2026)), "2013-2025 complete and matching")
for year in storm:
    for col in ("storm_county_days", "wind_days", "winter_days", "tropical_days", "severe_gust_days"):
        check(storm[year][col] == paired[year][col], f"{year} {col} matches the annual index")
# Decision D22 (docs/04): Bedford city folded into Bedford County, so each zone-34 storm counts once.
# Before D22 these were 465 and 796.
check(int(storm[2024]["storm_county_days"]) == 464, "2024 storm county-days = 464 (D22)")
check(int(storm[2025]["storm_county_days"]) == 791, "2025 storm county-days = 791 (D22)")

training = [paired[y] for y in range(2015, 2025)]
x = [float(r["storm_county_days"]) for r in training]
y = [float(r["saidi_ex_med"]) for r in training]
mx, my = sum(x) / len(x), sum(y) / len(y)
ssx = sum((v - mx) ** 2 for v in x)
ssy = sum((v - my) ** 2 for v in y)
cross = sum((a - mx) * (b - my) for a, b in zip(x, y))
slope = cross / ssx
intercept = my - slope * mx
r = cross / sqrt(ssx * ssy)
pred_2025 = intercept + slope * float(paired[2025]["storm_county_days"])
actual_2025 = float(paired[2025]["saidi_ex_med"])
adjusted_2025 = actual_2025 - pred_2025 + my
check(0.69 < r < 0.71, f"2015-2024 Pearson correlation = {r:.3f}")
check(0.050 < slope < 0.053, f"2015-2024 regression slope = {slope:.4f}")
check(isclose(pred_2025, 145.3, abs_tol=0.15), f"2025 holdout prediction = {pred_2025:.2f} minutes")
check(isclose(actual_2025, 144.4, abs_tol=0.001), "2025 actual SAIDI ex-MED = 144.4")
check(isclose(adjusted_2025, 133.1, abs_tol=0.2), f"exploratory adjusted SAIDI = {adjusted_2025:.2f}")
print("NOTE: regression checks confirm calculations, not weather causality.")

load = {int(r["yr"]): r for r in rows("dom_annual.csv")}
check(2019 in load and 2025 in load, "DOM annual demand has 2019 and 2025")
check(float(load[2019]["floor_mw"]) == 7167, "2019 minimum hourly demand = 7167 MW")
check(float(load[2025]["floor_mw"]) == 10903, "2025 minimum hourly demand = 10903 MW")
peak19 = max(float(load[2019]["winter_peak_mw"]), float(load[2019]["summer_peak_mw"]))
peak25 = max(float(load[2025]["winter_peak_mw"]), float(load[2025]["summer_peak_mw"]))
check(peak19 == 19803 and peak25 == 24957, "DOM annual peaks match source output")
check(isclose((peak25 / peak19 - 1) * 100, 26, abs_tol=0.1), "peak-hour demand growth rounds to 26%")
check(isclose((10903 / 7167 - 1) * 100, 52, abs_tol=0.2), "minimum-hour demand growth rounds to 52%")

# Data notes tables written by scripts/export_powerbi_csv.py
tests = rows("test_results.csv")
check([r["test"] for r in tests] == [f"T{n}" for n in range(1, len(tests) + 1)] and len(tests) == 31, "test_results.csv lists T1-T31 in order")
check(all(r["status"] == "PASS" for r in tests), "every test in test_results.csv passed")
recon = rows("reconciliation.csv")
check(len(recon) == 12 and all(r["verdict"] == "MATCH" for r in recon), "reconciliation.csv: 12 rows, all MATCH")
check(round(float(recon[0]["rebuilt"]), 1) == 130.2 and round(float(recon[1]["rebuilt"]), 1) == 133.0,
      "reconciliation 3-year SAIDI = 130.2 and 133.0 (reported 130 and 133)")
by_year = {}
for r in rows("storm_county_year.csv"):
    by_year[int(r["year"])] = by_year.get(int(r["year"]), 0) + int(r["storm_days"])
check(set(by_year) == set(range(2015, 2026)) and all(by_year[y] == int(storm[y]["storm_county_days"]) for y in by_year),
      "storm_county_year.csv adds up to storm_index.csv for every year 2015-2025")
peers = rows("peer_reliability_5yr.csv")
dom = [r for r in peers if r["is_dominion"] == "True"]
check(len(peers) == 12 and len(dom) == 1, "peer_reliability_5yr.csv: twelve utilities, Dominion and 11 peers (D10)")
dom = dom[0]
check((dom["saidi_rank_highest"], dom["saifi_rank_highest"], dom["caidi_rank_highest"]) == ("4", "4", "6"),
      "Dominion among the twelve: fourth-highest SAIDI 2023-25 and SAIFI 2021-25, sixth-highest CAIDI 2021-25")
check(tuple(dom[c] for c in ("median_saifi_2021_25", "median_caidi_2021_25", "median_saifi_2021_25_excl_dominion",
                             "median_caidi_2021_25_excl_dominion")) == ("0.964", "105.0", "0.934", "99.5"),
      "medians 2021-25: SAIFI 0.964 and CAIDI 105.0 for the twelve, 0.934 and 99.5 for the 11 peers alone")
check(all(float(dom[m]) < float(dom[v]) for v, m in (("saifi_2021_25", "median_saifi_2021_25"), ("caidi_2021_25", "median_caidi_2021_25"),
                                                      ("saifi_2021_25", "median_saifi_2021_25_excl_dominion"),
                                                      ("caidi_2021_25", "median_caidi_2021_25_excl_dominion"))),
      "Dominion's SAIFI and CAIDI are above the median with or without Dominion (same quadrant)")
svc = rows("storm_vs_calm.csv")
by_subset = {r["subset"]: r for r in svc}
first = svc[0]
check(len(svc) == 19 and first["subset"] == "All complete county-days, 2015-2025" and first["ratio_label"] == "11.9 (7.9 to 16.9)"
      and (int(first["storm_county_days"]), int(first["calm_county_days"])) == (6108, 373851),
      "storm vs calm county-days 2015-2025: 11.9 times (7.9 to 16.9), 6,108 storm and 373,851 calm county-days")
check(round(float(first["storm_ch_per_1k"]), 1) == 332.8 and round(float(first["calm_ch_per_1k"]), 2) == 27.86,
      "storm 332.8 and calm 27.86 customer-hours per 1,000 customers")
check(by_subset["Non-major days (proxy major event days removed)"]["ratio_label"] == "9.9 (8.6 to 11.3)",
      "storm vs calm on non-major days: 9.9 (8.6 to 11.3)")
check(by_subset["Dominion-only counties"]["ratio_label"] == "19.9 (11.2 to 32.5)", "storm vs calm, Dominion-only counties: 19.9 (11.2 to 32.5)")
years = [r for r in svc if r["subset"].isdigit()]
check([int(r["subset"]) for r in years] == list(range(2015, 2026)) and all(float(r["ratio_ci_low"]) > 1 for r in years),
      "storm vs calm, every year 2015-2025: the interval lies above 1")
check(sum(int(r["storm_county_days"]) for r in years) == 6108 and sum(int(r["calm_county_days"]) for r in years) == 373851,
      "storm vs calm: the yearly rows add up to the all-years row")

# Trend tests, 2015-2025 (scripts/trend_tests.py; docs/05 "Trend tests"): the values the documents quote
sys.path.insert(0, str(Path(__file__).resolve().parent))
import trend_tests  # noqa: E402  (standard library only; importing runs nothing)

trends = {label: r for label, _unit, r in trend_tests.trend_table()}
check(round(trends["SAIFI ex-MED"]["p"], 2) == 0.54, "SAIFI ex-MED trend 2015-2025: p = 0.54")
check(round(trends["CAIDI ex-MED"]["p"], 2) == 0.74, "CAIDI ex-MED trend 2015-2025: p = 0.74")
check(round(trends["SAIDI ex-MED"]["p"], 2) == 0.58, "SAIDI ex-MED trend 2015-2025: p = 0.58")
adj = trends["Weather-adjusted SAIDI (sql/07 Q10)"]
check((round(adj["slope"], 2), round(adj["lo"], 2), round(adj["hi"], 2), round(adj["p"], 2)) == (0.34, -1.41, 2.08, 0.67),
      "weather-adjusted SAIDI trend: +0.34 min/yr, 95% CI -1.41 to +2.08, p = 0.67 (D22)")
print("All committed-output checks passed.")
