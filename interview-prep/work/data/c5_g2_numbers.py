"""Batch 5: numbers for the G2 revision after the V3 mock panel.
1. Peers (S3): is Dominion one of D10's twelve; medians with and without Dominion; Dominion's ranks.
2. S4: storm and calm levels (customer-hours per 1,000 customers) with intervals, ratio, robustness rows.
3. 6,108 against 6,530 storm county-days, reconciled, with one label each.
4. Storm county-days by year 2013-2025 after decision D22 (and before), for S2's 2022 against 2025.
5. The county map for the Dominion-only counties, beside the all-utilities map.
6. The 2025 storm-line arithmetic.
Reads the DuckDB mirror and the committed files in data/output/. Writes sections/c5_g2_numbers.md."""
import csv
import io
import re
import subprocess
import sys
from pathlib import Path

import duckdb
import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import storm_vs_calm_ratio as svc  # noqa: E402  (importing runs nothing)
from export_powerbi_csv import COUNTY_MAP_SQL, PEERS  # noqa: E402

OUT = Path(__file__).resolve().parent / "sections" / "c5_g2_numbers.md"
con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)
OFF_MAP = "('51600', '51683', '51660', '51520')"  # D20: Fairfax city, Manassas, Harrisonburg, Bristol
md = ["## C5 Numbers for the G2 revision (batch 5, after the V3 mock panel)", "",
      "Repo commits for this batch: c0b2ea2 (`storm_vs_calm.csv`), 7133aba (peer medians without Dominion; D10 wording), "
      "4fc9939 (`county_outage_map_dominion_only.csv`), d1bdff2 (docs/05 and README: 6,108 reconciled with 6,530). "
      "`scripts/check_output_metrics.py` asserts every number below that "
      "comes from a committed file.", ""]


def sql_block(q):
    return ["```sql", q.strip(), "```", ""]


def pct(a, b):
    return 100 * (a / b - 1)


# ---------- 1. Peers ----------
d10 = (ROOT / "docs" / "04_decisions.md").read_text(encoding="utf-8")
d10_line = re.search(r"### D10\. Peer set\s+\*\*Decision\.\*\* (.+)", d10).group(1)
PEER_CTE = f"""WITH u AS (
  SELECT f.utility_key, d.utility_name, d.peer_group,
         AVG(CASE WHEN f.year BETWEEN 2023 AND 2025 THEN f.saidi_ex_med END) AS saidi_2023_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.saifi_ex_med END) AS saifi_2021_25,
         AVG(CASE WHEN f.year BETWEEN 2021 AND 2025 THEN f.caidi_ex_med END) AS caidi_2021_25
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN ({PEERS})
  GROUP BY 1, 2, 3)"""
Q1_MED = PEER_CTE + """
SELECT COUNT(*) AS utilities, COUNT(CASE WHEN utility_key = '19876|VA' THEN 1 END) AS dominion_rows,
       MEDIAN(saidi_2023_25) AS saidi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saidi_2023_25 END) AS saidi_med_11,
       MEDIAN(saifi_2021_25) AS saifi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN saifi_2021_25 END) AS saifi_med_11,
       MEDIAN(caidi_2021_25) AS caidi_med_12, MEDIAN(CASE WHEN utility_key <> '19876|VA' THEN caidi_2021_25 END) AS caidi_med_11
FROM u"""
Q1_RANK = PEER_CTE + """
SELECT utility_key, utility_name, utility_key = '19876|VA' AS is_dominion,
       saidi_2023_25, saifi_2021_25, caidi_2021_25,
       RANK() OVER (ORDER BY saidi_2023_25 DESC) AS saidi_rank,  -- 1 = highest of the 12
       RANK() OVER (ORDER BY saifi_2021_25 DESC) AS saifi_rank,
       RANK() OVER (ORDER BY caidi_2021_25 DESC) AS caidi_rank
FROM u ORDER BY saifi_2021_25 DESC"""
med = con.execute(Q1_MED).df().iloc[0]
rk = con.execute(Q1_RANK).df()
dom = rk[rk.is_dominion].iloc[0]
assert int(med.utilities) == 12 and int(med.dominion_rows) == 1
md += ["### C5-1 Peers (S3): the twelve are Dominion and 11 peers", "",
       f"**Answer.** Yes, Dominion is one of the twelve. D10 names eleven utilities and then adds Dominion: \"{d10_line.split(' Appalachian')[0]}\" "
       "(docs/04; the clause \"so the twelve are Dominion and 11 peers\" was added in commit 7133aba to remove the ambiguity). "
       "The peer query returns 12 utilities, one of them Dominion. So the deck says **\"12 large utilities (Dominion and 11 peers)\"**.", "",
       f"**Medians without Dominion (the 11 peers), 2021-25 means of the annual ex-MED values:** SAIFI **{med.saifi_med_11:.3f}** "
       f"(with Dominion {med.saifi_med_12:.3f}), CAIDI **{med.caidi_med_11:.1f}** minutes (with Dominion {med.caidi_med_12:.1f}). "
       f"SAIDI 2023-25: **{med.saidi_med_11:.1f}** (with Dominion {med.saidi_med_12:.1f}).", "",
       f"**Ranks do not change.** A rank is Dominion's place among the twelve, so it does not depend on which median is drawn: SAIFI "
       f"{dom.saifi_2021_25:.3f} is **fourth-highest** of the 12 (three peers higher), CAIDI {dom.caidi_2021_25:.1f} is **sixth-highest** "
       f"(five peers higher), SAIDI 2023-25 {dom.saidi_2023_25:.1f} is fourth-highest. \"Fourth-highest SAIFI\" and \"6th CAIDI\" stand as "
       "long as they say \"of the 12\" (\"fourth among 11 peers\" would be wrong).", "",
       f"**Distance from the median.** Against the 11-peer medians Dominion is {pct(dom.saifi_2021_25, med.saifi_med_11):.0f}% above on SAIFI "
       f"(against the 12-utility median: {pct(dom.saifi_2021_25, med.saifi_med_12):.0f}%), {pct(dom.caidi_2021_25, med.caidi_med_11):.0f}% above "
       f"on CAIDI ({pct(dom.caidi_2021_25, med.caidi_med_12):.0f}%) and {pct(dom.saidi_2023_25, med.saidi_med_11):.0f}% above on SAIDI 2023-25 "
       f"({pct(dom.saidi_2023_25, med.saidi_med_12):.0f}%). It sits above both lines either way, so the quadrant is the same. The frequency gap "
       "reads larger and the restoration gap still modest: \"restoration mid-pack\" holds as a rank (6th of 12), but CAIDI is 11% above the "
       "11-peer median, so say \"mid-pack\", not \"at the median\".", "",
       f"**Line for S3:** \"Among 12 large utilities (Dominion and 11 peers), 2021-25: outages per customer {dom.saifi_2021_25:.2f}, "
       f"fourth-highest (peer median {med.saifi_med_11:.2f}); minutes per outage {dom.caidi_2021_25:.0f}, sixth-highest (peer median "
       f"{med.caidi_med_11:.1f}). Reporting methods differ, so the comparison is indicative.\"", "",
       "**Chart-ready:** `data/output/peer_reliability_5yr.csv` (12 rows; new columns `median_saidi_2023_25_excl_dominion`, "
       "`median_saifi_2021_25_excl_dominion`, `median_caidi_2021_25_excl_dominion`; the old median columns are unchanged).", "",
       "| Utility | SAIDI 2023-25 | Rank | SAIFI 2021-25 | Rank | CAIDI 2021-25 | Rank |",
       "|---|---:|---:|---:|---:|---:|---:|"]
for r in rk.itertuples():
    name = f"**{r.utility_name}**" if r.is_dominion else r.utility_name
    md.append(f"| {name} | {r.saidi_2023_25:.1f} | {r.saidi_rank} | {r.saifi_2021_25:.3f} | {r.saifi_rank} | {r.caidi_2021_25:.1f} | {r.caidi_rank} |")
md += [f"| Median of the 12 | {med.saidi_med_12:.1f} | | {med.saifi_med_12:.3f} | | {med.caidi_med_12:.1f} | |",
       f"| Median of the 11 peers | {med.saidi_med_11:.1f} | | {med.saifi_med_11:.3f} | | {med.caidi_med_11:.1f} | |", ""]
md += sql_block(Q1_MED) + sql_block(Q1_RANK)

# ---------- 2. S4 levels ----------
committed = list(csv.DictReader((ROOT / "data" / "output" / "storm_vs_calm.csv").open(encoding="utf-8")))
assert [[r[c] for c in svc.COLUMNS] for r in committed] == [[str(v) for v in row] for row in svc.storm_vs_calm_table(con)], \
    "storm_vs_calm.csv differs from a fresh run"


def _compare_raw(df, rng):
    """svc._compare without rounding: same groups, same single draw from rng, so the same resamples."""
    g = df.groupby(["day", "storm_day"]).customer_hours_per_1k.agg(["sum", "count"]).unstack(fill_value=0)
    s_sum, s_n = g[("sum", True)].to_numpy(), g[("count", True)].to_numpy()
    c_sum, c_n = g[("sum", False)].to_numpy(), g[("count", False)].to_numpy()
    idx = rng.integers(0, len(g), size=(svc.B, len(g)))
    b_storm, b_calm = s_sum[idx].sum(1) / s_n[idx].sum(1), c_sum[idx].sum(1) / c_n[idx].sum(1)
    storm, calm = s_sum.sum() / s_n.sum(), c_sum.sum() / c_n.sum()
    q = lambda a: list(np.percentile(a, [2.5, 97.5]))  # noqa: E731
    return [int(s_n.sum()), int(c_n.sum()), storm, *q(b_storm), calm, *q(b_calm), storm / calm, *q(b_storm / b_calm)]


orig, svc._compare = svc._compare, _compare_raw
raw = svc.storm_vs_calm_table(con)
svc._compare = orig
for row, c in zip(raw, committed):  # the unrounded values round to the committed ones
    assert all(round(float(v), 3) == float(c[k]) for v, k in zip(row[3:12], svc.COLUMNS[3:12])), row[0]
R = {row[0]: row for row in raw}


def lvl(v, lo, hi, d=1):
    return f"{v:.{d}f} ({lo:.{d}f} to {hi:.{d}f})"


a, nm, do = R["All complete county-days, 2015-2025"], R["Non-major days (proxy major event days removed)"], R["Dominion-only counties"]
years = [row for row in raw if row[0].isdigit()]
assert all(lvl(*row[9:12]) == c["ratio_label"] for row, c in zip(raw, committed))  # same text as ratio_label
md += ["### C5-2 S4: storm and calm levels, with the ratio and its robustness", "",
       f"**Answer.** On county-days with a NOAA line-risk storm report, outage customer-hours per 1,000 customers averaged "
       f"**{lvl(*a[3:6])}**; on calm county-days, **{lvl(*a[6:9], d=2)}** (95% intervals). Ratio **{lvl(*a[9:12])}** "
       f"(printed: \"11.9x (95% CI 7.9-16.9)\"), from {a[1]:,} storm and {a[2]:,} calm county-days, 2015-2025. "
       "The levels and the ratio come from the same 2,000 resamples of whole days, so the ratio interval is not the ratio of the "
       "level intervals.", "",
       f"**Robustness line:** non-major days only {lvl(*nm[9:12])}; the 31 Dominion-only counties on the map {lvl(*do[9:12])}; "
       f"every year from {min(years, key=lambda r: r[9])[9]:.1f} ({min(years, key=lambda r: r[9])[0]}) to "
       f"{max(years, key=lambda r: r[9])[9]:.1f} ({max(years, key=lambda r: r[9])[0]}), and every year's interval lies above 1 "
       f"(lowest lower bound {min(r[10] for r in years):.1f}, {min(years, key=lambda r: r[10])[0]}).", "",
       "**Slide text (one visual, the two levels):** \"Outage customer-hours per 1,000 customers per county-day: storm days "
       f"{a[3]:.0f}, calm days {a[6]:.0f} (about 12x; 95% CI {a[10]:.1f}-{a[11]:.1f}). Holds on non-major days ({nm[9]:.1f}x), in "
       f"Dominion-only counties ({do[9]:.1f}x) and in every year 2015-2025.\" Caveat line: \"EAGLE-I counts every utility's customers in a "
       "county; 99 of Dominion's 103 Virginia counties, complete days only. An association: storm reports partly follow damage.\"", "",
       "**Chart-ready:** `data/output/storm_vs_calm.csv` (19 rows: `subset`, both counts, `storm_ch_per_1k` and `calm_ch_per_1k` with "
       "`_ci_low`/`_ci_high`, `ratio` with its interval, `ratio_label`). The small table for the slide (one decimal, rounded once from the "
       "unrounded values):", "",
       "| Subset | Storm county-days | Storm days: customer-hours per 1,000 (95% CI) | Calm days (95% CI) | Ratio (95% CI) |",
       "|---|---:|---:|---:|---:|"]
for row in (a, nm, do):
    md.append(f"| {row[0]} | {row[1]:,} | {lvl(*row[3:6])} | {lvl(*row[6:9])} | {lvl(*row[9:12])} |")
md += ["", "Every year (the robustness line's \"every year\"):", "",
       "| Year | Storm county-days | Calm county-days | Storm level | Calm level | Ratio (95% CI) |", "|---:|---:|---:|---:|---:|---:|"]
for row in years:
    md.append(f"| {row[0]} | {row[1]:,} | {row[2]:,} | {row[3]:.1f} | {row[6]:.1f} | {lvl(*row[9:12])} |")
md += ["",
       "**Caveats.** 2025 rests on 74% of its county-days (26,899 complete of 36,135) because failed EAGLE-I runs cluster in late 2025 "
       "(docs/03 P20); it is the lowest year (5.9x) and its interval still lies above 1. The tropical subset (93 storm county-days) is too "
       "small to quote (1.5 to 116.8). Outages that run past midnight land on a \"calm\" next day, which pulls the ratio down.", "",
       "Query (the rows the bootstrap resamples; `scripts/storm_vs_calm_ratio.py`):", ""]
md += sql_block(svc.SQL)

# ---------- 3. 6,108 against 6,530 ----------
Q3 = f"""SELECT year,
       COUNT(CASE WHEN storm_day THEN 1 END)                                                          AS storm_103_counties,
       COUNT(CASE WHEN storm_day AND county_fips IN {OFF_MAP} THEN 1 END)                             AS in_4_off_map,
       COUNT(CASE WHEN storm_day AND county_fips NOT IN {OFF_MAP} AND failed_readings > 0 THEN 1 END) AS with_failed_reading,
       COUNT(CASE WHEN storm_day AND county_fips NOT IN {OFF_MAP} AND failed_readings = 0 THEN 1 END) AS complete_99_counties
FROM mart.FCT_COUNTY_DAY GROUP BY year ORDER BY year"""
Q3_INDEX = "SELECT SUM(storm_county_days) AS storm_index_2015_25 FROM mart.STORM_INDEX WHERE year BETWEEN 2015 AND 2025"
t3 = con.execute(Q3).df()
idx_total = int(con.execute(Q3_INDEX).fetchone()[0])
tot = t3[["storm_103_counties", "in_4_off_map", "with_failed_reading", "complete_99_counties"]].sum().astype(int)
assert tot.storm_103_counties == idx_total == 6530 and tot.complete_99_counties == 6108 == a[1]
assert tot.storm_103_counties - tot.in_4_off_map - tot.with_failed_reading == tot.complete_99_counties
failed_years = ", ".join(f"{int(r.year)} {int(r.with_failed_reading)}" for r in t3.itertuples() if r.with_failed_reading)
md += ["### C5-3 Storm county-days: 6,530 against 6,108", "",
       f"**Answer.** Both are right; they count different things. **6,530** is every storm county-day in Dominion's 103 Virginia counties, "
       f"2015-2025: the sum of the storm index (`storm_index.csv`, after D22) and of `storm_day` in the county-day table. **6,108** is the "
       f"part of it the storm-vs-calm comparison can use: {tot.in_4_off_map} fall in the four counties off the map (D20: Fairfax city, "
       f"Manassas, Harrisonburg, Bristol) and {tot.with_failed_reading} are days with at least one failed EAGLE-I reading ({failed_years}). "
       f"6,530 - {tot.in_4_off_map} - {tot.with_failed_reading} = 6,108.", "",
       "**Labels for B (use exactly):**", "",
       "- 6,530: \"storm county-days, 2015-2025, Dominion's 103 Virginia counties (NOAA)\". Long form: \"county-days with a NOAA line-risk "
       "storm report, 2015-2025, all 103 Virginia counties Dominion serves (Bedford city counted in Bedford County)\".",
       "- 6,108: \"storm county-days with complete outage readings, 2015-2025, 99 counties on the map (EAGLE-I)\". Long form: \"the "
       "storm county-days behind the 11.9x comparison: complete EAGLE-I readings, the 99 counties on the map\".", "",
       "Never put the two side by side without the label; the S4 slide uses only 6,108.", "",
       "| Year | Storm county-days, 103 counties | In the 4 counties off the map | With a failed EAGLE-I reading | Complete, 99 counties |",
       "|---:|---:|---:|---:|---:|"]
for r in t3.itertuples():
    md.append(f"| {r.year} | {int(r.storm_103_counties):,} | {int(r.in_4_off_map)} | {int(r.with_failed_reading)} | {int(r.complete_99_counties):,} |")
md += [f"| **2015-2025** | **{tot.storm_103_counties:,}** | **{tot.in_4_off_map}** | **{tot.with_failed_reading}** | **{tot.complete_99_counties:,}** |", ""]
md += sql_block(Q3) + sql_block(Q3_INDEX)

# ---------- 4. Storm county-days by year, after and before D22 ----------
Q4 = "SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year BETWEEN 2013 AND 2025 ORDER BY year"
t4 = con.execute(Q4).df()
pre = {int(r["year"]): int(r["storm_county_days"]) for r in csv.DictReader(io.StringIO(subprocess.run(
    ["git", "-C", str(ROOT), "show", "06631ad^:data/output/storm_index.csv"], capture_output=True, text=True, check=True).stdout))}
post = {int(r.year): int(r.storm_county_days) for r in t4.itertuples()}
committed_idx = {int(r["year"]): int(r["storm_county_days"]) for r in csv.DictReader((ROOT / "data" / "output" / "storm_index.csv").open(encoding="utf-8"))}
assert post == committed_idx and post[2022] == 718 and post[2025] == 791
md += ["### C5-4 Storm county-days by year, 2013-2025, after D22", "",
       f"**Answer.** Confirmed: **2022 = {post[2022]}** and **2025 = {post[2025]}** after D22 (V2's 718 is the post-D22 value). "
       f"2022 to 2025: +{post[2025] - post[2022]} ({pct(post[2025], post[2022]):+.1f}%). Before D22 the pair was {pre[2022]} and {pre[2025]}. "
       f"D22 lowered every year by 1 to 5, not only 2024 and 2025 (the 38 duplicate county-days of 2013-2025): any slide or note with "
       f"{pre[2022]}, {pre[2025]}, {pre[2024]} or {pre[2019]} carries pre-D22 values. 2025 is the second-highest year; 2019 ({post[2019]}) "
       "is the highest.", "",
       "**Chart-ready:** `data/output/storm_index.csv` (post-D22; also `storm_vs_saidi.csv`).", "",
       "| Year | " + " | ".join(str(y) for y in sorted(post)) + " |",
       "|---|" + "---:|" * len(post),
       "| After D22 | " + " | ".join(f"{post[y]:,}" for y in sorted(post)) + " |",
       "| Before D22 | " + " | ".join(f"{pre[y]:,}" for y in sorted(post)) + " |",
       "| Change | " + " | ".join(f"{post[y] - pre[y]}" for y in sorted(post)) + " |", ""]
assert sum(pre[y] - post[y] for y in post) == 38
md += sql_block(Q4)
md += ["Before-D22 values: `git show 06631ad^:data/output/storm_index.csv` (the file as first committed).", ""]

# ---------- 5. Dominion-only county map ----------
Q5_GROUPS = f"""WITH m AS (
{COUNTY_MAP_SQL}
),
y AS (
  SELECT c.year, m.dominion_only_county, SUM(c.customer_hours_non_med) AS customer_hours_non_med,
         SUM(c.customers_basis) AS customers_basis, COUNT(*) AS counties
  FROM mart.FCT_COUNTY_YEAR c JOIN m USING (county_fips)
  WHERE m.map_flag = 'ok' AND c.year BETWEEN 2015 AND 2024
  GROUP BY GROUPING SETS ((c.year, m.dominion_only_county), (c.year))
)
SELECT CASE WHEN dominion_only_county THEN 'Dominion-only counties'
            WHEN NOT dominion_only_county THEN 'Shared counties (Dominion and other utilities)'
            ELSE 'All counties on the map' END AS counties_group,
       MAX(counties) AS counties, MAX(customers_basis) AS customers_basis,
       AVG(60 * customer_hours_non_med / customers_basis) AS minutes_non_med_avg_2015_24  -- customer-weighted each year, then the mean
FROM y GROUP BY 1 ORDER BY 2"""
Q5_ALL103 = """SELECT AVG(60 * ch / basis) AS minutes_non_med_avg_2015_24
FROM (SELECT year, SUM(customer_hours_non_med) AS ch, SUM(customers_basis) AS basis
      FROM mart.FCT_COUNTY_YEAR WHERE year BETWEEN 2015 AND 2024 GROUP BY year)"""
Q5_COUNTIES = f"""SELECT * FROM (
{COUNTY_MAP_SQL}
) WHERE dominion_only_county ORDER BY minutes_non_med_avg_2015_24 DESC"""
g5 = con.execute(Q5_GROUPS).df()
all103 = con.execute(Q5_ALL103).fetchone()[0]
c5 = con.execute(Q5_COUNTIES).df()
ok5 = c5[c5.map_flag == "ok"]
allmap = list(csv.DictReader((ROOT / "data" / "output" / "county_outage_map.csv").open(encoding="utf-8")))
allok = [r for r in allmap if r["map_flag"] == "ok"]
amin = min(allok, key=lambda r: float(r["minutes_non_med_avg_2015_24"]))
amax = max(allok, key=lambda r: float(r["minutes_non_med_avg_2015_24"]))
big = ok5[ok5.customers_basis >= 20000]
G = {r.counties_group: r for r in g5.itertuples()}
gd, gs, ga = G["Dominion-only counties"], G["Shared counties (Dominion and other utilities)"], G["All counties on the map"]
md += ["### C5-5 The county map: Dominion-only counties, and the all-utilities version", "",
       f"**Answer.** Same A3 measure (outage minutes per customer a year on non-major days, 2015-2024 average). In the "
       f"**{int(gd.counties)} Dominion-only counties on the map** ({int(gd.customers_basis):,} customers), where EAGLE-I counts Dominion "
       f"customers alone: **{gd.minutes_non_med_avg_2015_24:.0f} minutes** (customer-weighted). The {int(gs.counties)} shared counties: "
       f"{gs.minutes_non_med_avg_2015_24:.0f}; all {int(ga.counties)} on the map: {ga.minutes_non_med_avg_2015_24:.0f}; all 103: "
       f"{all103:.0f} (A3's figure). By county: {ok5.iloc[-1].county_label} {ok5.iloc[-1].minutes_non_med_avg_2015_24:.1f} to "
       f"{ok5.iloc[0].county_label} {ok5.iloc[0].minutes_non_med_avg_2015_24:.1f}; among the {len(big)} with 20,000 or more customers, "
       f"{big.iloc[-1].county_label} {big.iloc[-1].minutes_non_med_avg_2015_24:.1f} to {big.iloc[0].county_label} "
       f"{big.iloc[0].minutes_non_med_avg_2015_24:.1f}.", "",
       "**Do not read the gap as Dominion against other utilities.** The Dominion-only counties are mostly cities and inner suburbs "
       "(Hampton Roads, Richmond, Arlington and Alexandria) plus a few small Tidewater counties, so the lower figure compares places, "
       "not utilities.", "",
       "**Chart-ready:**", "",
       f"- `data/output/county_outage_map_dominion_only.csv`: the 33 Dominion-only rows ({len(ok5)} with `map_flag = 'ok'`; Fairfax city "
       "and Harrisonburg city are Dominion-only but off the map, D20). Title: \"Outage minutes per customer a year, non-major days, "
       "2015-2024 average: the 31 counties Dominion serves alone (EAGLE-I counts Dominion customers there)\".",
       f"- `data/output/county_outage_map.csv`: all 103 (99 on the map). Title: \"Outage minutes per customer a year, non-major days, "
       f"2015-2024 average: **all utilities** in each of Dominion's Virginia counties (EAGLE-I); 99 of 103 shown\". Range on the map: "
       f"{amin['county_label']} {amin['minutes_non_med_avg_2015_24']} to {amax['county_label']} {amax['minutes_non_med_avg_2015_24']}; "
       "use one colour scale for both maps.",
       "- No \"start with these counties\" line on either (G2).", "",
       "| Counties | Number | Customers | Minutes a year, non-major days, 2015-2024 |", "|---|---:|---:|---:|"]
for r in (gd, gs, ga):
    md.append(f"| {r.counties_group} | {int(r.counties)} | {int(r.customers_basis):,} | {r.minutes_non_med_avg_2015_24:.1f} |")
md += [f"| All 103 Dominion counties (A3) | 103 | | {all103:.1f} |", "",
       "Dominion-only counties on the map, highest to lowest:", "",
       "| County | Customers | Minutes, non-major, avg 2015-24 | Storm days a year |", "|---|---:|---:|---:|"]
for r in ok5.itertuples():
    md.append(f"| {r.county_label} | {int(r.customers_basis):,} | {r.minutes_non_med_avg_2015_24:.1f} | {r.storm_days_avg_2015_24:.1f} |")
md += ["", "**Caveats.** Dominion-only means EIA-861's 2025 Service Territory lists no other utility in the county (D15); small "
       "counties have noisy rates (Charles City County, 2,516 customers). 2025 is not averaged (failed EAGLE-I runs, P20).", ""]
md += sql_block(Q5_GROUPS) + sql_block(Q5_ALL103) + sql_block(Q5_COUNTIES)

# ---------- 6. The 2025 storm line ----------
Q6 = """SELECT REGR_INTERCEPT(saidi_ex_med, storm_county_days) AS intercept,
       REGR_SLOPE(saidi_ex_med, storm_county_days)     AS slope,
       CORR(saidi_ex_med, storm_county_days)           AS r,
       COUNT(*) AS n, AVG(saidi_ex_med) AS mean_saidi
FROM mart.V_STORM_VS_SAIDI WHERE year BETWEEN 2015 AND 2024"""
Q6_2025 = "SELECT storm_county_days, saidi_ex_med FROM mart.V_STORM_VS_SAIDI WHERE year = 2025"
f6 = con.execute(Q6).df().iloc[0]
days25, saidi25 = con.execute(Q6_2025).fetchone()
days25, saidi25 = int(days25), float(saidi25)
pred_raw = f6.intercept + f6.slope * days25
pred_rounded_coef = 104.3 + 0.0518 * days25
saidi_by_year = {int(y): float(s) for y, s in con.execute("SELECT year, saidi_ex_med FROM mart.V_STORM_VS_SAIDI").fetchall()}
xs = np.array([pre[y] for y in range(2015, 2025)], float)
ys = np.array([saidi_by_year[y] for y in range(2015, 2025)])
b_pre, a_pre = np.polyfit(xs, ys, 1)
pred_pre = a_pre + b_pre * pre[2025]
assert round(pred_raw, 1) == round(pred_rounded_coef, 1) == 145.3 and int(days25) == 791
md += ["### C5-6 The 2025 storm line: 145.3 against 144.4", "",
       f"**Answer.** Confirmed. With the coefficients as printed, 104.3 + 0.0518 x 791 = 104.3 + {0.0518 * days25:.4f} = "
       f"**{pred_rounded_coef:.4f}**, which prints as 145.3. With the unrounded fit (2015-2024, n = {int(f6.n)}, after D22): "
       f"{f6.intercept:.4f} + {f6.slope:.6f} x 791 = **{pred_raw:.4f}**, also 145.3. Actual 2025 SAIDI ex-MED: {saidi25:.1f}, "
       f"so 2025 sits {pred_raw - saidi25:.2f} minutes ({100 * (pred_raw - saidi25) / pred_raw:.1f}%) below the line: \"2025 sits on the "
       f"storm line\" is fair. r = {f6.r:.4f} (prints 0.70). Weather-adjusted 2025 = {saidi25:.1f} - {pred_raw:.4f} + {f6.mean_saidi:.4f} "
       f"(the 2015-2024 mean) = {saidi25 - pred_raw + f6.mean_saidi:.4f}, which prints as 133.1 (not 133.2: it is just below the half).", "",
       f"Before D22 the fit was {a_pre:.4f} + {b_pre:.6f} x {pre[2025]} = {pred_pre:.4f} (also 145.3), so the slide figure did not move.", "",
       "**Chart-ready:** `data/output/saidi_weather_adjusted.csv` (`predicted_from_weather`, `fit_slope`, `fit_intercept`, `fit_mean`).", ""]
md += sql_block(Q6) + sql_block(Q6_2025)

OUT.write_text("\n".join(md).rstrip() + "\n", encoding="utf-8")
print(OUT)
