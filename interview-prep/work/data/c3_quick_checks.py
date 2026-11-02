"""Batch 3 quick checks for the orchestrator (after D22):
1. Reconciliation scope: 3-year SAIDI ex-MED for Virginia only vs Virginia + North Carolina (utility 19876).
2. Weather-fit arithmetic from the unrounded r: t over n = 10 and the 95% Fisher-z interval for r.
3. The peer-set rule, quoted exactly from docs/04 D10, with the members as the mart assigns them.
Reads the DuckDB mirror. Writes sections/c3_quick_checks.md."""
import math
import re
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import duckdb
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "sections" / "c3_quick_checks.md"
con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)
md = ["## Quick checks for the orchestrator (batch 3, after D22)", ""]

# ---------- 1. Reconciliation scope ----------
Q1_YEARS = """SELECT year,
       SUM(CASE WHEN state = 'VA' THEN customers END)                                   AS customers_va,
       SUM(CASE WHEN state = 'NC' THEN customers END)                                   AS customers_nc,
       SUM(CASE WHEN state = 'VA' THEN cust_minutes_ex_med END)
         / SUM(CASE WHEN state = 'VA' THEN customers END)                               AS saidi_va,
       SUM(CASE WHEN state = 'NC' THEN cust_minutes_ex_med END)
         / SUM(CASE WHEN state = 'NC' THEN customers END)                               AS saidi_nc,
       SUM(cust_minutes_ex_med) / SUM(customers)                                        AS saidi_va_nc,
       SUM(cust_minutes_ex_med) AS cust_minutes, SUM(customers) AS customers,
       STRING_AGG(DISTINCT standard, ', ')                                              AS standards
FROM mart.FCT_RELIABILITY
WHERE utility_id = 19876 AND state IN ('VA', 'NC') AND year BETWEEN 2022 AND 2025
GROUP BY year ORDER BY year"""
Q1 = """WITH y AS (
""" + "\n".join("  " + l for l in Q1_YEARS.splitlines()) + """
)
SELECT p.period,
       AVG(y.saidi_va)    AS saidi_va_3yr,      -- mean of the annual customer-weighted values (the scorecard's method)
       AVG(y.saidi_va_nc) AS saidi_va_nc_3yr,
       SUM(y.cust_minutes) / SUM(y.customers) AS saidi_va_nc_pooled  -- sensitivity: three years pooled
FROM y JOIN (SELECT '2022-24' AS period, 2022 AS y0 UNION ALL SELECT '2023-25', 2023) p
  ON y.year BETWEEN p.y0 AND p.y0 + 2
GROUP BY p.period ORDER BY p.period"""
yrs = con.execute(Q1_YEARS).df()
res = con.execute(Q1).df().set_index("period")
va1, va2 = res.loc["2022-24", "saidi_va_3yr"], res.loc["2023-25", "saidi_va_3yr"]
vn1, vn2 = res.loc["2022-24", "saidi_va_nc_3yr"], res.loc["2023-25", "saidi_va_nc_3yr"]
pl1, pl2 = res.loc["2022-24", "saidi_va_nc_pooled"], res.loc["2023-25", "saidi_va_nc_pooled"]
nc_share = yrs.customers_nc.sum() / yrs.customers.sum()

def half_up(x):
    return int(Decimal(str(x)).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


md += ["### Q-1 Reconciliation scope: Virginia only vs Virginia + North Carolina", "",
       f"**Answer.** Virginia only gives **{va1:.2f} and {va2:.2f}**, which print as {half_up(va1)} and {half_up(va2)}: both of the annual "
       f"report's figures. Virginia + North Carolina, customer-weighted each year and then averaged over the three years (the scorecard's "
       f"method), gives **{vn1:.3f} and {vn2:.3f}**, which print as **{half_up(vn1)}** and {half_up(vn2)} ({vn2:.3f} is just above the half); "
       f"pooling the three years instead gives {pl1:.2f} and {pl2:.2f} ({half_up(pl1)} and {half_up(pl2)}). So only the Virginia-only rebuild "
       f"reproduces both printed numbers: with North Carolina the 2022-24 average prints as {half_up(vn1)}, not 130. North Carolina is "
       f"{100 * nc_share:.1f}% of the customers and had lower SAIDI in 2022 and 2024. The rise is about three minutes either way "
       f"({va2 - va1:+.2f} Virginia, {vn2 - vn1:+.2f} with North Carolina).", "",
       "**Defensible line:** \"Rebuilt from EIA-861, Virginia's rows reproduce both of Dominion's figures, 130 and 133. Adding North "
       f"Carolina gives {vn1:.1f} and {vn2:.1f}, so the printed figures fit Virginia; either way the rise is about three minutes. The report "
       "doesn't state its scope, so I'd confirm it with the reliability team.\"", "",
       "**Caveat.** Dominion computes these from its own outage records, not from its EIA-861 filing, so a half-minute gap could also come "
       "from different customer counts or data vintages: this is consistency with a Virginia-only scope, not proof. R's note in "
       "`research/for_B.md` (\"inference: probably system-wide\") is not supported by this arithmetic.", "",
       "| Year | Customers VA | Customers NC | SAIDI VA | SAIDI NC | SAIDI VA + NC | Standard |", "|---:|---:|---:|---:|---:|---:|---|"]
md += [f"| {int(r.year)} | {int(r.customers_va):,} | {int(r.customers_nc):,} | {r.saidi_va:.3f} | {r.saidi_nc:.3f} | {r.saidi_va_nc:.3f} | {r.standards} |"
       for r in yrs.itertuples()]
md += ["", "| Three-year average | Virginia only | VA + NC (mean of annual values) | VA + NC (pooled) | Annual report |", "|---|---:|---:|---:|---:|",
       f"| 2022-24 | {va1:.2f} | {vn1:.2f} | {pl1:.2f} | 130 |",
       f"| 2023-25 | {va2:.2f} | {vn2:.2f} | {pl2:.2f} | 133 |", "",
       "```sql", Q1, "```", "",
       "Both states file under EIA's \"Other\" standard (Dominion's own major-event rule) in every year shown, so the two states' ex-MED "
       "values are on the same basis. `cust_minutes_ex_med` = SAIDI x customers per state (`02_mart.sql`), so the VA + NC value is the "
       "customer-weighted SAIDI of the two states together.", ""]

# ---------- 2. Weather-fit arithmetic ----------
Q2 = """SELECT CORR(saidi_ex_med, storm_county_days) AS r, COUNT(*) AS n
FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024"""
r, n = con.execute(Q2).fetchone()
r, n = float(r), int(n)


def t_and_ci(rv, nv):
    t = rv * math.sqrt((nv - 2) / (1 - rv * rv))
    p = 2 * stats.t.sf(abs(t), nv - 2)
    z, se, zc = math.atanh(rv), 1 / math.sqrt(nv - 3), stats.norm.ppf(0.975)
    return t, p, math.tanh(z - zc * se), math.tanh(z + zc * se)


t, p, lo, hi = t_and_ci(r, n)
t70, p70, lo70, hi70 = t_and_ci(0.70, n)
lr = con.execute("SELECT saidi_ex_med, storm_county_days FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024").df()
lin = stats.linregress(lr.storm_county_days, lr.saidi_ex_med)
md += ["### Q-2 Weather-fit arithmetic from the unrounded r (after D22)", "",
       f"**Answer.** r = **{r:.4f}** (n = {n}, 2015-2024). t = r x sqrt((n - 2) / (1 - r^2)) = **{t:.3f}** on {n - 2} df, two-sided "
       f"p = **{p:.4f}**. 95% interval for r by Fisher z (z = atanh r, SE = 1 / sqrt(n - 3), z +/- 1.96 SE, back with tanh): "
       f"**{lo:.3f} to {hi:.3f}**, i.e. {lo:.2f} to {hi:.2f}. R's t = 2.77 and 0.13 to 0.92 are right for r = 0.70 exactly "
       f"(t {t70:.3f}, interval {lo70:.3f} to {hi70:.3f}); from the unrounded r they become t = {t:.2f} and {lo:.2f} to {hi:.2f}.", "",
       f"Cross-check: `scipy.stats.linregress` on the same ten rows gives slope t = {lin.slope / lin.stderr:.3f} and p = {lin.pvalue:.4f}, "
       "the same test as t for r.", "",
       "```sql", Q2, "```", "",
       f"Defensible wording: \"r = 0.70 on ten years (t = {t:.2f}, p = {p:.3f}); the 95% interval runs from about {lo:.2f} to {hi:.2f}, so the "
       "data are consistent with anything from a weak to a very strong association. That is why the slide leads with the county-day "
       "comparison.\"", ""]

# ---------- 3. Peer rule ----------
d04 = (ROOT / "docs" / "04_decisions.md").read_text(encoding="utf-8")
sec = d04[d04.index("### D10. Peer set"):]
sec = sec[:sec.index("---")]
decision = re.search(r"\*\*Decision\.\*\* (.+)", sec).group(1).strip()
first_sentence = decision.split(". ")[0] + "."
Q3 = """SELECT peer_group, utility_key, utility_name FROM mart.DIM_UTILITY
WHERE peer_group IN ('Dominion Energy Virginia', 'Southeast IOU peer', 'Mid-Atlantic IOU peer', 'Florida IOU peer', 'Appalachian Power (VA)')
ORDER BY peer_group, utility_name"""
peers = con.execute(Q3).df()
n_peer = int((peers.peer_group != "Appalachian Power (VA)").sum())
md += ["### Q-3 The peer-set rule (docs/04 D10), quoted exactly", "",
       f"> {first_sentence}", "",
       "The rest of the decision, also verbatim:", "",
       f"> {decision[len(first_sentence):].strip()}", "",
       f"`DIM_UTILITY` assigns exactly these by EIA ID: {n_peer} utility-states including Dominion VA, plus Appalachian Power (VA) in its own group.", "",
       "| Peer group | Utility key | Utility |", "|---|---|---|"]
md += [f"| {r.peer_group} | {r.utility_key} | {r.utility_name} |" for r in peers.itertuples()]
md += ["", "```sql", Q3, "```", ""]

OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
