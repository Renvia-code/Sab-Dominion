"""Storm vs calm county-days: how many times as many outage customer-hours per 1,000 customers a county has on a
day with a NOAA line-risk storm report as on a day without one, 2015-2025, with 95% intervals.

EAGLE-I counts customers out from every utility in a county, so this describes all utilities in Dominion's
counties, not Dominion alone (the Dominion-only row is the check). Complete county-days only (no failed EAGLE-I
reading); the four counties left off the map (decision D20) are excluded. The intervals come from a bootstrap
that resamples whole days, because one storm hits many counties on the same day; the levels and the ratio use the
same resamples. An association, not a causal effect: NOAA storm reports are partly triggered by damage.

storm_vs_calm_table() returns one row per subset: all county-days, non-major days (proxy major event days, D18,
removed), Dominion-only counties, 2015-2019, 2020-2025, each storm type against all calm days, and each year.
scripts/export_powerbi_csv.py writes it to data/output/storm_vs_calm.csv. Documented in docs/05 (Outages from
EAGLE-I) and docs/08 (worked example 6).
Run with: python -I scripts/storm_vs_calm_ratio.py
"""
from pathlib import Path

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
B = 2000          # bootstrap resamples
SEED = 20261101   # fixed: the intervals are reproducible

SQL = """SELECT d.day, d.year, d.storm_day, d.storm_wind, d.storm_winter, d.storm_tropical, d.dominion_only_county,
       d.customer_hours_per_1k, t.is_med_proxy
FROM mart.FCT_COUNTY_DAY d
JOIN mart.FCT_TERRITORY_DAY t ON t.day = d.day
WHERE d.failed_readings = 0                                    -- complete county-days only
  AND d.county_fips NOT IN ('51600', '51683', '51660', '51520') -- D20: off the map
ORDER BY d.day, d.county_fips                                  -- fixed order: sums are bit-identical run to run"""

COLUMNS = ["subset", "storm_county_days", "calm_county_days",
           "storm_ch_per_1k", "storm_ci_low", "storm_ci_high",
           "calm_ch_per_1k", "calm_ci_low", "calm_ci_high",
           "ratio", "ratio_ci_low", "ratio_ci_high", "ratio_label"]


def _compare(df, rng):
    """Mean customer-hours per 1,000 customers on storm and calm county-days, their ratio, and day-cluster
    bootstrap intervals for all three from one set of resamples."""
    g = df.groupby(["day", "storm_day"]).customer_hours_per_1k.agg(["sum", "count"]).unstack(fill_value=0)
    s_sum, s_n = g[("sum", True)].to_numpy(), g[("count", True)].to_numpy()
    c_sum, c_n = g[("sum", False)].to_numpy(), g[("count", False)].to_numpy()
    storm, calm = s_sum.sum() / s_n.sum(), c_sum.sum() / c_n.sum()
    idx = rng.integers(0, len(g), size=(B, len(g)))
    b_storm = s_sum[idx].sum(1) / s_n[idx].sum(1)
    b_calm = c_sum[idx].sum(1) / c_n[idx].sum(1)
    pct = lambda a: np.percentile(a, [2.5, 97.5])  # noqa: E731
    (sl, sh), (cl, ch), (rl, rh) = pct(b_storm), pct(b_calm), pct(b_storm / b_calm)
    # Rounded once from the unrounded values, as Python floats (the csv module writes a numpy float64 as its repr);
    # ratio_label is the text to print (one decimal, no double rounding).
    r3 = lambda v: round(float(v), 3)  # noqa: E731
    return [int(s_n.sum()), int(c_n.sum()), r3(storm), r3(sl), r3(sh), r3(calm), r3(cl), r3(ch),
            r3(storm / calm), r3(rl), r3(rh), f"{storm / calm:.1f} ({rl:.1f} to {rh:.1f})"]


def storm_vs_calm_table(con):
    """Rows in a fixed order (the bootstrap draws depend on it): all, non-major days, Dominion-only counties,
    two periods, three storm types, then each year."""
    rng = np.random.default_rng(SEED)
    p = con.execute(SQL).df()
    subsets = [("All complete county-days, 2015-2025", p),
               ("Non-major days (proxy major event days removed)", p[~p.is_med_proxy]),
               ("Dominion-only counties", p[p.dominion_only_county]),
               ("2015-2019", p[p.year <= 2019]),
               ("2020-2025", p[p.year >= 2020])]
    for col, label in (("storm_wind", "wind"), ("storm_winter", "winter"), ("storm_tropical", "tropical")):
        subsets.append((f"Storm type: {label} (against all calm county-days)", p[(~p.storm_day) | (p[col])]))
    subsets += [(str(y), p[p.year == y]) for y in sorted(p.year.unique())]
    return [[label] + _compare(df, rng) for label, df in subsets]


def main():
    con = duckdb.connect(str(DB), read_only=True)
    rows = storm_vs_calm_table(con)
    print("Outage customer-hours per 1,000 customers, storm vs calm county-days (95% intervals, "
          f"{B:,} resamples of whole days)")
    for r in rows:
        print(f"{r[0]:<58} storm {r[3]:>9.3f} ({r[4]:.3f} to {r[5]:.3f})  calm {r[6]:>7.3f} ({r[7]:.3f} to {r[8]:.3f})  "
              f"ratio {r[12]}  n = {r[1]:,} / {r[2]:,}")


if __name__ == "__main__":
    main()
