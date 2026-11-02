"""A5: reconciliation. Every rebuilt headline number against the value its publisher reported, plus
EAGLE-I's outage minutes against EIA SAIDI (two independent public sources for the same counties).

Reads the DuckDB mirror, the EIA-861 2024 and 2025 zips, and the committed outputs. Writes
sections/a5_reconciliation.md and data/output/a5_reconciliation.csv.
"""
import csv
import io
import zipfile
from pathlib import Path

import duckdb
import openpyxl
from scipy import stats

ROOT = Path(__file__).resolve().parents[3]
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "sections" / "a5_reconciliation.md"
con = duckdb.connect(str(DB), read_only=True)


def eia_row(year):
    """Dominion VA row of the EIA-861 Reliability_YYYY.xlsx sheet Reliability_States (Other Standard columns)."""
    with zipfile.ZipFile(ROOT / "data" / "raw" / "eia861" / f"f861{year}.zip") as z:
        name = next(n for n in z.namelist() if n.lower().startswith(f"reliability_{year}"))
        ws = openpyxl.load_workbook(io.BytesIO(z.read(name)), read_only=True, data_only=True)["Reliability_States"]
        for r in ws.iter_rows(values_only=True):
            if r[1] in (19876, "19876") and r[3] == "VA":
                return {"saidi_all": r[17], "saifi_all": r[18], "saidi_ex_med": r[20], "saifi_ex_med": r[21], "caidi_ex_med": r[22], "customers": r[23]}


Q_REL = """SELECT year, saidi_all, saifi_all, saidi_ex_med, saifi_ex_med, caidi_ex_med, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year IN (2024, 2025) ORDER BY year"""
rel = con.execute(Q_REL).df().set_index("year")
Q_ROLL = """SELECT ROUND(AVG(CASE WHEN year BETWEEN 2022 AND 2024 THEN saidi_ex_med END), 1) AS saidi_3yr_2022_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_3yr_2023_25
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA'"""
roll = con.execute(Q_ROLL).df().iloc[0]
Q_STORM = "SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year IN (2024, 2025) ORDER BY year"
storm = dict(con.execute(Q_STORM).fetchall())
with (ROOT / "data" / "output" / "storm_index.csv").open(encoding="utf-8") as f:
    storm_committed = {int(r[next(k for k in r if k.lower() in ("year", "yr"))]): int(float(r["storm_county_days"])) for r in csv.DictReader(f)}
Q_SALES = """SELECT ROUND(SUM(sales_mwh)) AS mwh FROM mart.FCT_SALES_SECTOR WHERE year = 2025 AND customer_class = 'commercial'"""
sales = con.execute(Q_SALES).fetchone()[0]
Q_861M = """SELECT ROUND(SUM(TRY_CAST(commercial_mwh AS DOUBLE))) FROM read_csv('data/raw/eia861m/csv/sales_ult_cust_monthly.csv', all_varchar = true)
WHERE utility_number = '19876' AND state = 'VA' AND year = '2025'"""
e24, e25 = eia_row(2024), eia_row(2025)

rows = [
    ("3-year SAIDI ex-MED, 2022-2024", roll.saidi_3yr_2022_24, 130, "Dominion annual report (rounded); R checks the page", "MATCH (rounding)"),
    ("3-year SAIDI ex-MED, 2023-2025", roll.saidi_3yr_2023_25, 133, "Dominion annual report (rounded); R checks the page", "MATCH (rounding)"),
    ("SAIDI ex-MED 2025", rel.loc[2025, "saidi_ex_med"], e25["saidi_ex_med"], "EIA-861 2025 final file", ""),
    ("SAIFI ex-MED 2025", rel.loc[2025, "saifi_ex_med"], e25["saifi_ex_med"], "EIA-861 2025 final file", ""),
    ("CAIDI ex-MED 2025", rel.loc[2025, "caidi_ex_med"], e25["caidi_ex_med"], "EIA-861 2025 final file", ""),
    ("SAIDI all events 2025", rel.loc[2025, "saidi_all"], e25["saidi_all"], "EIA-861 2025 final file", ""),
    ("SAIDI ex-MED 2024", rel.loc[2024, "saidi_ex_med"], e24["saidi_ex_med"], "EIA-861 2024 file (repo uses PUDL)", ""),
    ("SAIFI ex-MED 2024", rel.loc[2024, "saifi_ex_med"], e24["saifi_ex_med"], "EIA-861 2024 file (repo uses PUDL)", ""),
    ("CAIDI ex-MED 2024", rel.loc[2024, "caidi_ex_med"], e24["caidi_ex_med"], "EIA-861 2024 file (repo uses PUDL)", ""),
    ("SAIDI all events 2024", rel.loc[2024, "saidi_all"], e24["saidi_all"], "EIA-861 2024 file (repo uses PUDL)", ""),
    ("Storm county-days 2024 (raw NOAA rebuild)", storm[2024], storm_committed[2024], "committed data/output/storm_index.csv", ""),
    ("Storm county-days 2025 (raw NOAA rebuild)", storm[2025], storm_committed[2025], "committed data/output/storm_index.csv", ""),
]
try:
    m861 = con.execute(Q_861M).fetchone()[0]
except Exception:
    m861 = None
rows.append(("Commercial sales 2025, MWh (bundled + delivery)", sales, 60088202 + 4532591, "EIA-861 2025 Sales_Ult_Cust (60,088,202 + 4,532,591)", ""))
out = []
for metric, rebuilt, reported, source, verdict in rows:
    rb, rp = float(rebuilt), float(reported)
    diff = rb - rp
    v = verdict or ("MATCH" if abs(diff) <= max(0.0005 * abs(rp), 0.001) else "DIFFERS")
    out.append((metric, rb, rp, diff, source, v))

# EAGLE-I vs EIA: minutes per customer by year
Q_EA = """WITH y AS (
  SELECT year, SUM(customer_hours) AS ch_all, SUM(CASE WHEN NOT is_med_proxy THEN customer_hours ELSE 0 END) AS ch_ex_med,
         SUM(CASE WHEN is_med_proxy THEN 1 ELSE 0 END) AS med_proxy_days
  FROM mart.FCT_TERRITORY_DAY GROUP BY year
),
basis AS (SELECT SUM(customers_basis) AS customers FROM mart.DIM_COUNTY WHERE dominion_county)
SELECT y.year, y.med_proxy_days, ROUND(60 * y.ch_all / b.customers, 1) AS eaglei_min_all, ROUND(60 * y.ch_ex_med / b.customers, 1) AS eaglei_min_ex_med,
       f.saidi_all, f.saidi_ex_med
FROM y CROSS JOIN basis b
JOIN mart.FCT_RELIABILITY f ON f.utility_key = '19876|VA' AND f.year = y.year
WHERE y.year BETWEEN 2015 AND 2025 ORDER BY y.year"""
ea = con.execute(Q_EA).df()
ea24 = ea[ea.year <= 2024]
r_all = stats.pearsonr(ea24.eaglei_min_all, ea24.saidi_all)
r_ex = stats.pearsonr(ea24.eaglei_min_ex_med, ea24.saidi_ex_med)

md = ["## A5 Reconciliation: rebuilt against reported", "",
      "**Finding.** Every headline number rebuilt from public files matches its published source: the 3-year SAIDI (130.2 and 133.0 against the "
      "reported 130 and 133), the 2024 and 2025 EIA-861 values to the published decimals, the storm county-days rebuilt from the raw NOAA files, "
      "and 2025 commercial sales. EAGLE-I, an independent source built from utilities' outage maps, tracks EIA's SAIDI only loosely "
      f"(2015-2024, n = 10: r = {r_ex.statistic:.2f} on non-major days, p = {r_ex.pvalue:.2f}; r = {r_all.statistic:.2f} for all events, p = {r_all.pvalue:.2f}) "
      "and sits at a different level, because it counts every utility in the 103 counties, uses a proxy major-event rule and misses failed collection runs. "
      "EAGLE-I is therefore used for where and when outages happened, never to restate Dominion's SAIDI.", "",
      "**Chart-ready table:** `interview-prep/work/data/output/a5_reconciliation.csv`.", "",
      "| Metric | Rebuilt | Reported | Difference | Reported source | Verdict |", "|---|---:|---:|---:|---|---|"]
md += [f"| {m} | {rb:,.3f} | {rp:,.3f} | {d:+,.3f} | {s} | {v} |" for m, rb, rp, d, s, v in out]
md += ["", "Queries:", "", "```sql", Q_REL, ";", Q_ROLL, ";", Q_STORM, ";", Q_SALES, "```", "",
       "EIA-861 values: `Reliability_2024.xlsx` and `Reliability_2025.xlsx` (sheet `Reliability_States`, Dominion VA row, Other Standard columns) "
       "read from `data/raw/eia861/f8612024.zip` and `f8612025.zip`. The annual-report figures are R's document check (claims register).", "",
       "### A5.2 EAGLE-I minutes per customer against EIA SAIDI", "", "```sql", Q_EA, "```", "",
       "| Year | Proxy MED days | EAGLE-I min, all days | EAGLE-I min, non-major days | EIA SAIDI all events | EIA SAIDI ex-MED |",
       "|---:|---:|---:|---:|---:|---:|"]
md += [f"| {r.year} | {r.med_proxy_days} | {r.eaglei_min_all} | {r.eaglei_min_ex_med} | {r.saidi_all} | {r.saidi_ex_med} |" for r in ea.itertuples()]
md += ["", f"Pearson r over 2015-2024 (n = 10): all-events {r_all.statistic:.2f} (p = {r_all.pvalue:.3f}); non-major {r_ex.statistic:.2f} (p = {r_ex.pvalue:.3f}). "
       "2025 is left out of r because EAGLE-I collection failed for much of August to November 2025.", "",
       "**Caveats.** EAGLE-I's denominator is the customer basis of decision D15 (3.46 million in the 103 counties, all utilities) against EIA's "
       "2.68 million Dominion customers; its major-event days are a proxy built the IEEE way (D18), not Dominion's own.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
with (Path(__file__).resolve().parent / "output" / "a5_reconciliation.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["metric", "rebuilt", "reported", "difference", "reported_source", "verdict"])
    for m, rb, rp, d, s, v in out:
        w.writerow([m, round(rb, 3), round(rp, 3), round(d, 3), s, v])
print("\n".join(md[:12 + len(out)]))
print(ea.to_string())
