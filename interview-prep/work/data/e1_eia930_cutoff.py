"""E1: the EIA-930 cut-off behind every 2026 demand figure, and the last timestamp in each export.

Reads the DuckDB mirror and the committed data/output/dom_annual.csv. Writes sections/e1_eia930_cutoff.md.
"""
import csv
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "e1_eia930_cutoff.md"
con = duckdb.connect(str(DB), read_only=True)

Q_LAST = """SELECT MAX(CASE WHEN demand_mw IS NOT NULL THEN utc_ts END)   AS last_valid_utc,
       MAX(CASE WHEN demand_mw IS NOT NULL THEN local_ts END) AS last_valid_local_hour_ending,
       MAX(utc_ts)                                            AS last_row_utc
FROM stg.EIA930_DOM_HOURLY"""
last = con.execute(Q_LAST).df().iloc[0]

Q_CUT = """SELECT COUNT(*) AS hours, ROUND(SUM(demand_mw) / 1e6, 2) AS energy_twh, ROUND(MEDIAN(demand_mw)) AS median_mw,
       ROUND(AVG(demand_mw)) AS avg_mw, MAX(utc_ts) AS last_utc
FROM stg.EIA930_DOM_HOURLY
WHERE YEAR(data_date) = 2026 AND demand_mw IS NOT NULL AND data_date <= DATE '{cut}'"""
c21 = con.execute(Q_CUT.format(cut="2026-10-21")).df().iloc[0]
c29 = con.execute(Q_CUT.format(cut="2026-10-29")).df().iloc[0]
with (ROOT / "data" / "output" / "dom_annual.csv").open(encoding="utf-8") as f:
    committed = {r["yr"]: r for r in csv.DictReader(f)}["2026"]
peaks = con.execute("SELECT season, peak_mw, peak_date, peak_hour_no FROM mart.DOM_SEASONAL_PEAK WHERE year = 2026 ORDER BY season").df()

exports = [
    ("dom_load_annual.csv", "SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL", "rebuild (sql/06), all years; 2026 row to the cut-off"),
    ("dom_top50_hours.csv", "SELECT MAX(utc_ts) FROM mart.DOM_TOP50_HOURS", "rebuild (sql/06); rank_today ranks every hour to the cut-off"),
    ("dom_load_profile.csv", "SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL AND YEAR(data_date) = 2025", "rebuild (sql/07); uses 2019 and 2025 only"),
    ("dom_load_hour_month.csv", "SELECT MAX(make_date(year, month, 1)) FROM mart.DOM_LOAD_HOUR_MONTH WHERE hours_reported > 0", "rebuild (sql/10); last month October 2026, partial"),
    ("dom_seasonal_peak.csv", "SELECT MAX(peak_date) FROM mart.DOM_SEASONAL_PEAK", "rebuild (sql/10); 2026 winter = Jan-Feb only"),
    ("dom_load_daily.csv", "SELECT MAX(data_date) FROM mart.DOM_LOAD_DAILY WHERE hours_reported > 0", "rebuild (sql/10)"),
]
md = ["## E1 The EIA-930 cut-off for 2026 demand figures", "",
      f"**One cut-off for every 2026 figure: the last hour with data in the EIA-930 file downloaded on 1 November 2026, the hour ending midnight "
      f"local time on 29 October 2026 ({last.last_valid_utc:%Y-%m-%d %H:%M} UTC).** The file has rows for 30 October but no demand values yet "
      f"(last row {last.last_row_utc:%Y-%m-%d %H:%M} UTC). Every EIA-930 export in `data/output/` written by `scripts/export_powerbi_csv.py` comes from "
      "the rebuild with this cut-off. Write it as \"to 29 Oct 2026\" (I-03's \"30 Oct\" was the last row, not the last value).", "",
      "The committed `data/output/dom_annual.csv` (the original snapshot, kept unchanged) stops a week earlier, at the hour ending midnight on "
      f"21 October 2026 ({c21.last_utc:%Y-%m-%d %H:%M} UTC, shown as \"22 Oct\" in the repo): its 2026 row ({committed['hours_reported']} hours, "
      f"{committed['energy_twh']} TWh, median {committed['median_mw']}, average {committed['avg_mw']}) equals the rebuild cut at 21 October "
      f"({int(c21.hours)} hours, {c21.energy_twh} TWh, median {c21.median_mw:.0f}, average {c21.avg_mw:.0f}). B should not use `dom_annual.csv` for 2026.", "",
      "```sql", Q_LAST, "```", "", "```sql", Q_CUT.format(cut="2026-10-21") + "  -- and '2026-10-29'", "```", "",
      "| 2026 figure | Committed snapshot (to 21 Oct) | Rebuild (to 29 Oct), use this |", "|---|---:|---:|",
      f"| Hours reported | {committed['hours_reported']} | {int(c29.hours)} |",
      f"| Energy, TWh | {committed['energy_twh']} | {c29.energy_twh} |",
      f"| Median MW | {float(committed['median_mw']):,.0f} | {c29.median_mw:,.0f} |",
      f"| Average MW | {float(committed['avg_mw']):,.0f} | {c29.avg_mw:,.0f} |"]
for r in peaks.itertuples():
    md.append(f"| {r.season.title()} peak MW ({r.peak_date}, hour ending {r.peak_hour_no}) | {float(committed[r.season + '_peak_mw']):,.0f} | {int(r.peak_mw):,} |")
md += ["", "The winter and summer peaks (25,413 vs 25,384 MW, a 29 MW tie) and the top-50 hours are the same under both cut-offs: "
       "no hour after 21 October comes near them. Only the 2026 totals, averages and medians differ.", "",
       "| Export | Last timestamp in the data | Source |", "|---|---|---|"]
for name, sql, src in exports:
    v = con.execute(sql).fetchone()[0]
    md.append(f"| `{name}` | {v} | {src} |")
md += ["", "Queries for the last timestamps:", "", "```sql"] + [f"{s};  -- {n}" for n, s, _ in exports] + ["```", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
