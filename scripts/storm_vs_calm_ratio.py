"""Storm vs calm county-days: how many times as many outage customer-hours per 1,000 customers a county has on a
day with a NOAA line-risk storm report as on a day without one, 2015-2025, with a 95% interval.

EAGLE-I counts customers out from every utility in a county, so this describes all utilities in Dominion's
counties, not Dominion alone. Complete county-days only (no failed EAGLE-I readings); the four counties left off
the map (decision D20) are excluded. The interval comes from a bootstrap that resamples whole days, because one
storm hits many counties on the same day. An association, not a causal effect: NOAA storm reports are partly
triggered by damage.

Reads the DuckDB mirror built by scripts/run_local_duckdb_sources.py. Documented in docs/05 (Outages from EAGLE-I)
and docs/08 (worked example 6).
Run with: python -I scripts/storm_vs_calm_ratio.py
"""
from pathlib import Path

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
B = 2000                                  # bootstrap resamples
RNG = np.random.default_rng(20261101)     # fixed seed: the interval is reproducible

SQL = """SELECT d.day, d.storm_day, d.customer_hours_per_1k
FROM mart.FCT_COUNTY_DAY d
WHERE d.failed_readings = 0                                    -- complete county-days only
  AND d.county_fips NOT IN ('51600', '51683', '51660', '51520') -- D20: off the map"""


def main():
    con = duckdb.connect(str(DB), read_only=True)
    p = con.execute(SQL).df()
    g = p.groupby(["day", "storm_day"]).customer_hours_per_1k.agg(["sum", "count"]).unstack(fill_value=0)
    s_sum, s_n = g[("sum", True)].to_numpy(), g[("count", True)].to_numpy()
    c_sum, c_n = g[("sum", False)].to_numpy(), g[("count", False)].to_numpy()
    storm_mean, calm_mean = s_sum.sum() / s_n.sum(), c_sum.sum() / c_n.sum()
    ratio = storm_mean / calm_mean
    idx = RNG.integers(0, len(g), size=(B, len(g)))
    boot = (s_sum[idx].sum(1) / s_n[idx].sum(1)) / (c_sum[idx].sum(1) / c_n[idx].sum(1))
    lo, hi = np.percentile(boot, [2.5, 97.5])
    print(f"storm county-days {int(s_n.sum()):,}; calm county-days {int(c_n.sum()):,}; days {len(g):,}")
    print(f"mean customer-hours per 1,000 customers: storm {storm_mean:.1f}, calm {calm_mean:.2f}")
    print(f"ratio {ratio:.1f} (95% interval {lo:.1f} to {hi:.1f}; {B:,} resamples of whole days)")


if __name__ == "__main__":
    main()
