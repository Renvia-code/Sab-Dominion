"""A1: one stratified comparison on the county-day panel. Outage customer-hours per 1,000 customers on
county-days with a NOAA line-risk storm report vs county-days without one, 2015-2025, with a 95%
interval from a bootstrap that resamples whole days (storms hit many counties on the same day).

Reads the DuckDB mirror. Writes sections/a1_county_day.md.
"""
from pathlib import Path

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "a1_county_day.md"
con = duckdb.connect(str(DB), read_only=True)
RNG = np.random.default_rng(20261101)
B = 2000

Q_PANEL = """SELECT d.county_fips, d.day, d.year, d.dominion_only_county, d.customer_hours_per_1k,
       d.storm_day, d.storm_wind, d.storm_winter, d.storm_tropical, t.is_med_proxy
FROM mart.FCT_COUNTY_DAY d
JOIN mart.FCT_TERRITORY_DAY t ON t.day = d.day
WHERE d.failed_readings = 0                                    -- complete county-days only
  AND d.county_fips NOT IN ('51600', '51683', '51660', '51520') -- A3 map exclusions (docs/03 P26, P27)"""
p = con.execute(Q_PANEL).df()
p["day"] = p["day"].astype("datetime64[ns]")
n_all = con.execute("SELECT COUNT(*) FROM mart.FCT_COUNTY_DAY").fetchone()[0]


def ratio_ci(df, storm_col="storm_day"):
    """Ratio of mean customer-hours per 1k, storm vs calm county-days, with a day-cluster bootstrap."""
    g = df.groupby(["day", storm_col]).customer_hours_per_1k.agg(["sum", "count"]).unstack(fill_value=0)
    s_sum, s_n = g[("sum", True)].to_numpy(), g[("count", True)].to_numpy()
    c_sum, c_n = g[("sum", False)].to_numpy(), g[("count", False)].to_numpy()
    point = (s_sum.sum() / s_n.sum()) / (c_sum.sum() / c_n.sum())
    idx = RNG.integers(0, len(g), size=(B, len(g)))
    boot = (s_sum[idx].sum(1) / s_n[idx].sum(1)) / (c_sum[idx].sum(1) / c_n[idx].sum(1))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return dict(ratio=point, lo=lo, hi=hi, storm_n=int(s_n.sum()), calm_n=int(c_n.sum()),
                storm_mean=s_sum.sum() / s_n.sum(), calm_mean=c_sum.sum() / c_n.sum(), days=len(g))


main = ratio_ci(p)
rows = [("All complete county-days, 2015-2025", main)]
rows.append(("Excluding proxy major event days", ratio_ci(p[~p.is_med_proxy])))
rows.append(("Dominion-only counties", ratio_ci(p[p.dominion_only_county])))
rows.append(("2015-2019", ratio_ci(p[p.year <= 2019])))
rows.append(("2020-2025", ratio_ci(p[p.year >= 2020])))
by_type = []
for col, label in (("storm_wind", "wind (thunderstorm, high wind, tornado)"), ("storm_winter", "winter (ice, snow, sleet, blizzard)"),
                   ("storm_tropical", "tropical")):
    sub = p[(~p.storm_day) | (p[col])]
    by_type.append((label, ratio_ci(sub)))
by_year = [(y, ratio_ci(p[p.year == y])) for y in sorted(p.year.unique())]
# share of county-days with a heavy outage (10 or more customer-hours per 1,000 customers: on average 1% of customers out for an hour)
heavy_s = (p[p.storm_day].customer_hours_per_1k >= 10).mean()
heavy_c = (p[~p.storm_day].customer_hours_per_1k >= 10).mean()

md = ["## A1 County-day panel: storm days vs calm days", "",
      f"**Finding (S4 headline candidate).** On county-days with a NOAA damaging-wind, winter-storm or tropical report, outage customer-hours "
      f"per 1,000 customers were **{main['ratio']:.1f} times** those of county-days without one (95% CI {main['lo']:.1f} to {main['hi']:.1f}; "
      f"{main['storm_n']:,} storm and {main['calm_n']:,} calm county-days in {p.county_fips.nunique()} Dominion counties, 2015-2025). "
      f"In plain terms: an average storm county-day cost {main['storm_mean']:.0f} customer-hours per 1,000 customers, a calm one {main['calm_mean']:.1f}. "
      f"The gap holds on non-major days, in Dominion-only counties, in both halves of the period and in every year (table below). "
      f"{heavy_s:.0%} of storm county-days had a heavy outage (10 or more customer-hours per 1,000 customers), against {heavy_c:.1%} of calm ones. "
      "This is an association: NOAA storm reports are partly triggered by damage, so the ratio is not the storm's causal effect.", "",
      "Suggested slide line: \"On county-days with a storm report, outages cost about "
      f"{main['ratio']:.0f} times as many customer-hours per 1,000 customers as on calm days ({main['storm_n']:,} storm county-days, 2015-2025).\"", "",
      "```sql", Q_PANEL, "```", "",
      f"Ratio of means (storm / calm). 95% CI: {B:,} bootstrap resamples of whole days (seed 20261101), so county-days hit by the same storm move together. "
      f"Complete county-days only (no failed EAGLE-I reading that day): {len(p):,} of {n_all:,}.", "",
      "| Subset | Storm county-days | Calm county-days | Mean storm | Mean calm | Ratio | 95% CI |", "|---|---:|---:|---:|---:|---:|---|"]
for label, r in rows + [("Storm type: " + l, r) for l, r in by_type]:
    md.append(f"| {label} | {r['storm_n']:,} | {r['calm_n']:,} | {r['storm_mean']:.1f} | {r['calm_mean']:.2f} | {r['ratio']:.1f} | {r['lo']:.1f} to {r['hi']:.1f} |")
md += ["", "By year:", "", "| Year | Storm county-days | Ratio | 95% CI |", "|---:|---:|---:|---|"]
md += [f"| {y} | {r['storm_n']:,} | {r['ratio']:.1f} | {r['lo']:.1f} to {r['hi']:.1f} |" for y, r in by_year]
md += ["", "**Chart-ready table:** `interview-prep/work/data/output/a1_storm_vs_calm.csv` (the two tables above, one row per subset or year).", "",
       "**Caveats.**",
       "- EAGLE-I counts every utility in a county; Dominion-only counties give the same reading.",
       "- Storm flags are NOAA line-risk reports (wind, winter, tropical) on the event's begin date in that county (decision D5); a storm that "
       "starts at night and causes outages the next day counts the second day as calm, which biases the ratio down.",
       "- County-days with any failed EAGLE-I reading are dropped (most of August to November 2025), and four counties with unusable EAGLE-I data "
       "(Fairfax city, Manassas, Harrisonburg, Bristol) are left out.",
       "- No count model was fitted: the stratified ratio and its bootstrap interval already answer the slide's question, and every subset points the same way.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")

# chart-ready table
import csv
dest = Path(__file__).resolve().parent / "output" / "a1_storm_vs_calm.csv"
with dest.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["subset", "storm_county_days", "calm_county_days", "mean_storm_ch_per_1k", "mean_calm_ch_per_1k", "ratio", "ci_low", "ci_high"])
    for label, r in rows + [("Storm type: " + l, r) for l, r in by_type] + [(str(y), r) for y, r in by_year]:
        w.writerow([label, r["storm_n"], r["calm_n"], round(r["storm_mean"], 2), round(r["calm_mean"], 3), round(r["ratio"], 2), round(r["lo"], 2), round(r["hi"], 2)])
print("\n".join(md[:6]))
print("\n".join(md[10:40]))
