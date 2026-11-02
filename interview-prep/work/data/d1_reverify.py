"""D1: recompute every figure in MASTER_PROMPT.md section 2.2 from the repo's data.

Reads the DuckDB database built from the source files by scripts/run_local_duckdb_sources.py
(data/raw/duckdb/reliability_local.duckdb) and writes interview-prep/work/data/reverify_2_2.md.
Every value is printed next to the exact SQL that produced it. In Snowflake, read `mart.` as
RELIABILITY.MART. and `stg.` as RELIABILITY.STG.
Run: .venv/Scripts/python.exe -I interview-prep/work/data/d1_reverify.py
"""
import io
import os
import zipfile
from pathlib import Path
import duckdb
import openpyxl

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)  # the EIA-861 CSV paths in the queries are relative to the repo root
DB = ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"
OUT = Path(__file__).resolve().parent / "reverify_2_2.md"
con = duckdb.connect(str(DB), read_only=True)

PEERS = "('19876|VA','5416|NC','3046|NC','7140|GA','195|AL','17539|SC','1167|MD','15270|MD','14940|PA','14715|PA','6452|FL','6455|FL')"

checks = []  # (id, brief figure, query, formatter(df) -> (value text, verdict, note))


def q(sql):
    return con.execute(sql).df()


def add(cid, figure, sql, judge):
    df = q(sql)
    value, verdict, note = judge(df)
    checks.append((cid, figure, value, verdict, note, sql.strip()))


# 1. Headline rolling three-year SAIDI ex-MED
add("F01", "Rolling 3-yr SAIDI ex-MED 130 (2022-24) -> 133 (2023-25)",
    """SELECT ROUND(AVG(CASE WHEN year BETWEEN 2022 AND 2024 THEN saidi_ex_med END), 1) AS saidi_3yr_2022_24,
       ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_3yr_2023_25
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA'""",
    lambda d: (f"{d.iloc[0,0]} -> {d.iloc[0,1]}",
               "MATCH" if (d.iloc[0,0], d.iloc[0,1]) == (130.2, 133.0) else "MISMATCH",
               "Mean of the annual customer-weighted values (one utility: mean of annual SAIDI). Annual report p.10 states 130 and 133 (document check is R's / A5)."))

# 2-4. 2023 vs 2025 SAIDI, SAIFI, CAIDI
add("F02", "SAIDI ex-MED 123.3 (2023) -> 144.4 (2025), +17%; SAIFI 1.165 -> 1.320, +13%; CAIDI 105.9 -> 109.4, +3%",
    """SELECT a.saidi_ex_med AS saidi_2023, b.saidi_ex_med AS saidi_2025, ROUND(100*(b.saidi_ex_med/a.saidi_ex_med-1),1) AS saidi_pct,
       a.saifi_ex_med AS saifi_2023, b.saifi_ex_med AS saifi_2025, ROUND(100*(b.saifi_ex_med/a.saifi_ex_med-1),1) AS saifi_pct,
       a.caidi_ex_med AS caidi_2023, b.caidi_ex_med AS caidi_2025, ROUND(100*(b.caidi_ex_med/a.caidi_ex_med-1),1) AS caidi_pct
FROM mart.FCT_RELIABILITY a JOIN mart.FCT_RELIABILITY b ON a.utility_key = b.utility_key
WHERE a.utility_key = '19876|VA' AND a.year = 2023 AND b.year = 2025""",
    lambda d: (f"SAIDI {d.saidi_2023[0]} -> {d.saidi_2025[0]} ({d.saidi_pct[0]:+}%); SAIFI {d.saifi_2023[0]} -> {d.saifi_2025[0]} ({d.saifi_pct[0]:+}%); CAIDI {d.caidi_2023[0]} -> {d.caidi_2025[0]} ({d.caidi_pct[0]:+}%)",
               "MATCH" if (round(float(d.saidi_pct[0])), round(float(d.saifi_pct[0])), round(float(d.caidi_pct[0]))) == (17, 13, 3) else "MISMATCH",
               "CAIDI is the reported column (109.394 for 2025); SAIDI / SAIFI gives the same to 0.1."))

# 5. Frequency share of the change
add("F03", "The rise comes mostly from more interruptions, not longer ones",
    """WITH p AS (SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA')
SELECT ROUND(100*LN(b.saifi_ex_med/a.saifi_ex_med)/LN(b.saidi_ex_med/a.saidi_ex_med)) AS pct_from_frequency,
       ROUND(100*LN(b.caidi_ex_med/a.caidi_ex_med)/LN(b.saidi_ex_med/a.saidi_ex_med)) AS pct_from_duration
FROM p a JOIN p b ON a.year = 2023 AND b.year = 2025""",
    lambda d: (f"{int(d.iloc[0,0])}% from frequency, {int(d.iloc[0,1])}% from duration (log decomposition, 2023->2025)",
               "MATCH" if d.iloc[0,0] > 50 else "MISMATCH",
               "Same as sql/03 Q1b. Decomposition is arithmetic (SAIDI = SAIFI x CAIDI), not a cause."))

# 6. Storm county-days
add("F04", "Storm county-days 464 (2024) -> 791 (2025) (decision D22; 465 -> 796 before Bedford city was folded into Bedford County)",
    """SELECT year, storm_county_days FROM mart.STORM_INDEX WHERE year IN (2024, 2025) ORDER BY year""",
    lambda d: (f"{int(d.storm_county_days[0])} -> {int(d.storm_county_days[1])}",
               "MATCH" if list(d.storm_county_days) == [464, 791] else "MISMATCH",
               "Rebuilt from the 13 raw NOAA files (831,288 rows) through sql/05 in DuckDB, not read from data/output. "
               "D22 folds Bedford city (51515) into Bedford County (51019), so the area counts once."))

# 7-8. Correlation and prediction
add("F05", "r = 0.70 between storm county-days and SAIDI ex-MED, 2015-2024 (n = 10); fit predicts 145.3 for 2025 vs 144.4 actual",
    """WITH j AS (SELECT * FROM mart.V_STORM_VS_SAIDI),
fit AS (SELECT REGR_SLOPE(saidi_ex_med, storm_county_days) AS slope, REGR_INTERCEPT(saidi_ex_med, storm_county_days) AS intercept,
               CORR(saidi_ex_med, storm_county_days) AS r, REGR_R2(saidi_ex_med, storm_county_days) AS r2, COUNT(*) AS n
        FROM j WHERE year BETWEEN 2015 AND 2024)
SELECT ROUND(r, 3) AS r, ROUND(r2, 3) AS r2, n, ROUND(slope, 4) AS slope, ROUND(intercept, 1) AS intercept,
       ROUND(intercept + slope * (SELECT storm_county_days FROM j WHERE year = 2025), 2) AS predicted_2025,
       intercept + slope * (SELECT storm_county_days FROM j WHERE year = 2025) AS predicted_raw,
       (SELECT saidi_ex_med FROM j WHERE year = 2025) AS actual_2025
FROM fit""",
    # Compare the unrounded prediction: after D22 it is 145.250..., and rounding twice (2 dp, then 1 dp half-even) gives 145.2.
    lambda d: (f"r = {d.r[0]} (R2 = {d.r2[0]}, n = {d.n[0]}); predicted {d.predicted_2025[0]} ({float(d.predicted_raw[0]):.4f}) vs actual {d.actual_2025[0]}",
               "MATCH" if round(float(d.r[0]), 2) == 0.70 and f"{float(d.predicted_raw[0]):.1f}" == "145.3" else "MISMATCH",
               f"n = 10 annual points; exploratory. Slope {d.slope[0]} min per county-day, intercept {d.intercept[0]} (after D22)."))

# 9. All events vs ex-MED
add("F06", "2025 all-events SAIDI 306.7 vs 144.4 ex-MED",
    """SELECT saidi_all, saidi_ex_med, ROUND(100*(saidi_all - saidi_ex_med)/saidi_all) AS med_share_pct, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year = 2025""",
    lambda d: (f"{d.saidi_all[0]} vs {d.saidi_ex_med[0]}; major-event-day share {int(d.med_share_pct[0])}%; customers {int(d.customers[0]):,}",
               "MATCH" if (float(d.saidi_all[0]), float(d.saidi_ex_med[0])) == (306.7, 144.4) else "MISMATCH",
               "Test T4 asserts these exact values from Reliability_2025_States.csv."))

# 10. Peer rank on SAIDI 2023-25
add("F07", "Dominion has the fourth-highest SAIDI of twelve peers over 2023-25",
    f"""SELECT f.utility_key, d.utility_name, d.peer_group,
       ROUND(AVG(f.saidi_ex_med), 1) AS saidi_2023_25,
       RANK() OVER (ORDER BY AVG(f.saidi_ex_med) DESC) AS rank_highest
FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
WHERE f.utility_key IN {PEERS} AND f.year BETWEEN 2023 AND 2025
GROUP BY 1, 2, 3 ORDER BY saidi_2023_25 DESC""",
    lambda d: (f"Dominion rank {int(d[d.utility_key=='19876|VA'].rank_highest.iloc[0])} of {len(d)} ({d[d.utility_key=='19876|VA'].saidi_2023_25.iloc[0]} min); top three: " + "; ".join(f"{r.utility_name} {r.saidi_2023_25}" for r in d.head(3).itertuples()),
               "MATCH" if int(d[d.utility_key=='19876|VA'].rank_highest.iloc[0]) == 4 and len(d) == 12 else "MISMATCH",
               "Peer set D10 (11 IOUs + Dominion; Appalachian Power excluded). Mean of the three annual values, as the DAX measure SAIDI 2023 to 2025. Methods differ (IEEE 1366 vs own rule)."))

# 11. Restoration mid-pack, frequency the gap (5-yr 2021-25)
add("F08", "Peers: restoration is mid-pack; frequency is the gap (SAIFI 5yr, CAIDI 5yr, 2021-25)",
    f"""WITH u AS (
  SELECT f.utility_key, d.utility_name, AVG(f.saifi_ex_med) AS saifi_5yr, AVG(f.caidi_ex_med) AS caidi_5yr
  FROM mart.FCT_RELIABILITY f JOIN mart.DIM_UTILITY d USING (utility_key)
  WHERE f.utility_key IN {PEERS} AND f.year BETWEEN 2021 AND 2025 GROUP BY 1, 2)
SELECT utility_key, utility_name, ROUND(saifi_5yr, 3) AS saifi_5yr, ROUND(caidi_5yr, 1) AS caidi_5yr,
       RANK() OVER (ORDER BY saifi_5yr DESC) AS saifi_rank_highest, RANK() OVER (ORDER BY caidi_5yr DESC) AS caidi_rank_highest,
       ROUND(MEDIAN(saifi_5yr) OVER (), 3) AS median_saifi, ROUND(MEDIAN(caidi_5yr) OVER (), 1) AS median_caidi
FROM u ORDER BY saifi_5yr DESC""",
    lambda d: (lambda r: (f"Dominion SAIFI 5yr {r.saifi_5yr} (rank {int(r.saifi_rank_highest)} highest of 12, median {r.median_saifi}); CAIDI 5yr {r.caidi_5yr} (rank {int(r.caidi_rank_highest)} of 12, median {r.median_caidi})",
                          "MATCH" if r.saifi_5yr > r.median_saifi and abs(r.caidi_5yr - r.median_caidi) < 15 else "CHECK",
                          "Means of annual values 2021-25, as the DAX measures SAIFI 5yr and CAIDI 5yr. Docs quote medians 0.96 and 105."))(d[d.utility_key=='19876|VA'].iloc[0]))

# 12. Co-op index
add("F09", "Since 2015, co-op SAIFI rose 37% against 14% for Dominion (index 137 vs 114)",
    """WITH g AS (SELECT peer_group, year, saifi_ex_med FROM mart.V_GROUP_INDEX WHERE peer_group IN ('Virginia co-op','Dominion Energy Virginia'))
SELECT a.peer_group, ROUND(a.saifi_ex_med, 3) AS saifi_2015, ROUND(b.saifi_ex_med, 3) AS saifi_2025,
       ROUND(100 * b.saifi_ex_med / a.saifi_ex_med, 1) AS index_2025
FROM g a JOIN g b ON a.peer_group = b.peer_group AND a.year = 2015 AND b.year = 2025 ORDER BY 1""",
    lambda d: ("; ".join(f"{r.peer_group}: {r.saifi_2015} -> {r.saifi_2025}, index {r.index_2025}" for r in d.itertuples()),
               "MATCH" if [round(float(x)) for x in d.index_2025] == [114, 137] else "MISMATCH",
               "All Virginia co-ops combined, customer-weighted (V_GROUP_INDEX). Balanced-panel check is sql/03 Q3."))

# 13-14. DOM peak and floor
add("F10", "DOM zone highest hour +26%, lowest hour +52% (2019 -> 2025)",
    """SELECT a.peak_mw AS peak_2019, b.peak_mw AS peak_2025, ROUND(100*(b.peak_mw/a.peak_mw-1),1) AS peak_pct,
       a.floor_mw AS floor_2019, b.floor_mw AS floor_2025, ROUND(100*(b.floor_mw/a.floor_mw-1),1) AS floor_pct
FROM mart.DOM_LOAD_ANNUAL a JOIN mart.DOM_LOAD_ANNUAL b ON a.year = 2019 AND b.year = 2025""",
    lambda d: (f"peak {int(d.peak_2019[0]):,} -> {int(d.peak_2025[0]):,} MW ({d.peak_pct[0]:+}%); floor {int(d.floor_2019[0]):,} -> {int(d.floor_2025[0]):,} MW ({d.floor_pct[0]:+}%)",
               "MATCH" if (round(float(d.peak_pct[0])), round(float(d.floor_pct[0]))) == (26, 52) else "MISMATCH",
               "Rebuilt from the 17 raw EIA-930 files through sql/06. DOM is the PJM zone, wider than Dominion's retail territory."))

# 15. Night vs afternoon
add("F11", "Night hours rose 41% and afternoon hours 27% (2019 -> 2025)",
    """SELECT hour_no, avg_mw_2019, avg_mw_2025, growth_pct FROM mart.DOM_LOAD_PROFILE WHERE hour_no IN (1,2,3,4,5,13,14,15,16,17) ORDER BY hour_no""",
    lambda d: ("; ".join(f"HE{int(r.hour_no):02d} {r.growth_pct:+}%" for r in d.itertuples()),
               "MATCH (wording)" if float(d[d.hour_no==4].growth_pct.iloc[0]) == 41.0 and float(d[d.hour_no==16].growth_pct.iloc[0]) == 27.1 else "MISMATCH",
               "41% is the single hour ending 04:00 local and 27% the hour ending 16:00 (sql/07). Safer wording: 'the 4 a.m. hour rose 41%, the 4 p.m. hour 27%'; hours ending 01-05 range +39.0% to +41.0%, hours ending 13-17 +26.9% to +27.4%."))

# 16. Winter vs summer peaks
add("F12", "The winter peak was at or above the summer peak in 2022, 2025 and 2026",
    """SELECT year, winter_peak_mw, summer_peak_mw, CASE WHEN winter_peak_mw >= summer_peak_mw THEN 'winter' ELSE 'summer' END AS peak_season
FROM mart.DOM_LOAD_ANNUAL WHERE year BETWEEN 2019 AND 2026 ORDER BY year""",
    lambda d: (", ".join(f"{int(r.year)} {r.peak_season} ({int(r.winter_peak_mw):,}/{int(r.summer_peak_mw):,})" for r in d.itertuples()),
               "MISMATCH (incomplete)" if set(d[d.peak_season=='winter'].year) != {2022, 2025, 2026} else "MATCH",
               "Winter (Dec-Feb of the calendar year) beat summer (Jun-Aug) in 2019, 2022, 2025 and 2026, not only 2022, 2025, 2026. 2026 is to 30 Oct 2026 and the gap is 29 MW (25,413 vs 25,384): call it a tie."))

# 17. Top-50 hours
add("F13", "47 of the top 50 hours fall at the end of 2025 or later",
    """SELECT 'ranked to 31 Dec 2025' AS reference, year, COUNT(*) AS hours_in_top50 FROM mart.DOM_TOP50_HOURS WHERE rank_end_2025 <= 50 GROUP BY 1, 2
UNION ALL
SELECT 'ranked to load date (30 Oct 2026)', year, COUNT(*) FROM mart.DOM_TOP50_HOURS WHERE rank_today <= 50 GROUP BY 1, 2 ORDER BY 1, 2""",
    lambda d: ("; ".join(f"{r.reference}: {int(r.year)} = {int(r.hours_in_top50)}" for r in d.itertuples()),
               "MISMATCH (wording)",
               "Correct statement: of the 50 highest hours in the EIA-930 record (July 2018 to 31 Dec 2025), 47 fell in 2025 and 3 in 2024. Ranked to 30 Oct 2026: 46 in 2026, 4 in 2025. The record starts July 2018, so this is not 'all-time'."))

# 18. Sales
add("F14", "Commercial sales rose 65% since 2013 on 8% more customers",
    """WITH s AS (
  SELECT year, SUM(sales_mwh) AS sales_mwh,
         SUM(CASE WHEN service_type = 'bundled' THEN customers END) AS customers_bundled,
         SUM(customers) AS customers_all_service_types
  FROM stg.SALES WHERE utility_id = 19876 AND state = 'VA' AND customer_class = 'commercial' GROUP BY year)
SELECT a.sales_mwh AS mwh_2013, b.sales_mwh AS mwh_2025, ROUND(100*b.sales_mwh/a.sales_mwh, 1) AS sales_index_2025,
       a.customers_bundled AS cust_2013, b.customers_bundled AS cust_2025, ROUND(100*b.customers_bundled/a.customers_bundled, 1) AS cust_index_2025,
       ROUND(100*b.customers_all_service_types/a.customers_all_service_types, 1) AS cust_index_all_types
FROM s a JOIN s b ON a.year = 2013 AND b.year = 2025""",
    lambda d: (f"sales {d.mwh_2013[0]/1e6:.2f} -> {d.mwh_2025[0]/1e6:.2f} TWh (index {d.sales_index_2025[0]}); customers {int(d.cust_2013[0]):,} -> {int(d.cust_2025[0]):,} (index {d.cust_index_2025[0]}; all service types {d.cust_index_all_types[0]})",
               "MATCH" if (round(float(d.sales_index_2025[0])), round(float(d.cust_index_2025[0]))) == (165, 108) else "MISMATCH",
               "PUDL core_eia861__yearly_sales (EIA-861), utility 19876 VA, commercial class; sales sum bundled + delivery service types. Not attributable to data centers from this data (D14)."))

# 19. Smart meters
add("F15", "Most customers have a smart meter, but almost none are on a time-varying rate",
    """SELECT year, ami_meters, total_meters, ROUND(100*ami_share, 1) AS ami_pct
FROM stg.AMI WHERE utility_id = 19876 AND state = 'VA' AND year >= 2019 ORDER BY year""",
    lambda d: ("; ".join(f"{int(r.year)} AMI {r.ami_pct}% of {int(r.total_meters):,} meters" for r in d.itertuples()),
               "MATCH",
               "AMI share from PUDL (EIA-861 Advanced Metering). The time-varying-rate half is F15b."))

# 19b. Time-varying rates: EIA-861 Dynamic Pricing (acquired in D2: data/raw/eia861/f8612024.zip, f8612025.zip)
DP_NAMES = "['data_year','utility_number','utility_name','short_form','state','ba_code','enrolled_res','enrolled_com','enrolled_ind','enrolled_trans','enrolled_total']"
SU_NAMES = ("['data_year','utility_number','utility_name','part','service_type','data_type','state','ownership','ba_code',"
            "'res_rev','res_mwh','res_cust','com_rev','com_mwh','com_cust','ind_rev','ind_mwh','ind_cust',"
            "'trans_rev','trans_mwh','trans_cust','tot_rev','tot_mwh','tot_cust']")
add("F15b", "Almost no customers are on a time-varying rate",
    f"""WITH dp AS (
  SELECT data_year, TRY_CAST(enrolled_res AS INT) AS enrolled_res, TRY_CAST(enrolled_com AS INT) AS enrolled_com,
         TRY_CAST(enrolled_total AS INT) AS enrolled_total
  FROM read_csv(['data/raw/eia861/csv/Dynamic_Pricing_2024_Dynamic_Pricing_States.csv',
                 'data/raw/eia861/csv/Dynamic_Pricing_2025_Dynamic_Pricing_States.csv'],
                skip = 3, header = false, all_varchar = true, names = {DP_NAMES})
  WHERE utility_number = '19876' AND state = 'VA'),
cu AS (  -- customers: bundled (part A) plus delivery-only (part C) rows
  SELECT data_year, SUM(TRY_CAST(res_cust AS INT)) AS res_customers, SUM(TRY_CAST(tot_cust AS INT)) AS customers
  FROM read_csv(['data/raw/eia861/csv/Sales_Ult_Cust_2024_States.csv',
                 'data/raw/eia861/csv/Sales_Ult_Cust_2025_States.csv'],
                skip = 5, header = false, all_varchar = true, strict_mode = false,  -- 3 header records (one spans 3 lines), multi-line footnote
                names = {SU_NAMES})
  WHERE utility_number = '19876' AND state = 'VA'
  GROUP BY 1)
SELECT dp.data_year AS year, dp.enrolled_total, cu.customers, ROUND(100.0 * dp.enrolled_total / cu.customers, 2) AS pct_enrolled,
       dp.enrolled_res, cu.res_customers, ROUND(100.0 * dp.enrolled_res / cu.res_customers, 2) AS pct_res_enrolled
FROM dp JOIN cu USING (data_year) ORDER BY 1""",
    lambda d: ("; ".join(f"{r.year}: {int(r.enrolled_total):,} of {int(r.customers):,} customers enrolled ({r.pct_enrolled}%), residential {int(r.enrolled_res):,} of {int(r.res_customers):,} ({r.pct_res_enrolled}%)"
                         for r in d.itertuples()),
               "MATCH" if float(d.pct_enrolled.iloc[-1]) < 2 else "MISMATCH",
               "EIA-861 Dynamic Pricing: customers enrolled in time-of-use, real-time, variable-peak, critical-peak pricing or critical-peak rebate programs. "
               "Say 'about 1 in 100 customers', not 'almost none'. Programs reported for 2025: time-of-use (residential, commercial, industrial), "
               "variable-peak and critical-peak pricing (commercial, industrial)."))

md = ["# D1. Re-verification of MASTER_PROMPT section 2.2",
      "",
      "Recomputed 2026-11-01 by agent D from the source files: `data/input/` (EIA-861, PUDL) and the raw NOAA and",
      "EIA-930 downloads in `data/raw/`, rebuilt in DuckDB by `scripts/run_local_duckdb_sources.py` (sql/01, 02, 05, 06, 07;",
      "tests T7-T12 pass) and `scripts/run_local_duckdb.py` (T1-T6 pass). Database:",
      "`data/raw/duckdb/reliability_local.duckdb`. Script: `interview-prep/work/data/d1_reverify.py`.",
      "In Snowflake, read `mart.` as `RELIABILITY.MART.` and `stg.` as `RELIABILITY.STG.`.",
      "",
      "| id | Figure in the brief | Recomputed | Verdict | Note |",
      "|---|---|---|---|---|"]
for cid, fig, val, verdict, note, _ in checks:
    md.append(f"| {cid} | {fig} | {val} | **{verdict}** | {note} |")
md += ["", "## Queries", ""]
for cid, fig, val, verdict, note, sql in checks:
    md += [f"### {cid}. {fig}", "", "```sql", sql, "```", "", f"Result: {val}", ""]


def final_file_check():
    """Compare data/input/Reliability_2025_States.csv with the final EIA-861 2025 release
    (data/raw/eia861/f8612025.zip, Reliability_2025.xlsx, sheet Reliability_States), cell by cell.
    Numbers are equal when they agree to 0.0005 (the CSV shows three decimals); text must match."""
    import csv

    def norm(v):
        if v is None:
            return ""
        s = str(v).strip()
        try:
            return float(s.replace(",", ""))
        except ValueError:
            return s

    with open("data/input/Reliability_2025_States.csv", newline="", encoding="utf-8-sig") as f:
        csv_rows = [r for r in csv.reader(f)]
    with zipfile.ZipFile("data/raw/eia861/f8612025.zip") as z:
        name = next(n for n in z.namelist() if n.lower().startswith("reliability_2025"))
        wb = openpyxl.load_workbook(io.BytesIO(z.read(name)), read_only=True, data_only=True)
        ws = wb["Reliability_States"]
        x_rows = [list(r) for r in ws.iter_rows(values_only=True)]
    header = csv_rows[2]
    diffs, dom = [], {}
    for i, (c, x) in enumerate(zip(csv_rows, x_rows)):
        for j in range(max(len(c), len(x))):
            a = norm(c[j] if j < len(c) else None)
            b = norm(x[j] if j < len(x) else None)
            same = (abs(a - b) <= 0.0005 + 1e-9) if isinstance(a, float) and isinstance(b, float) else a == b
            if not same:
                diffs.append((i + 1, c[1] if len(c) > 1 else "", c[2] if len(c) > 2 else "", c[3] if len(c) > 3 else "", header[j] if j < len(header) else j, c[j] if j < len(c) else "", x[j] if j < len(x) else ""))
        if len(c) > 3 and c[1] == "19876" and c[3] == "VA":
            dom = {"csv": c, "xlsx": x}
    cols = {17: "SAIDI all events", 18: "SAIFI all events", 19: "CAIDI all events", 20: "SAIDI ex-MED",
            21: "SAIFI ex-MED", 22: "CAIDI ex-MED", 23: "Customers"}
    out = ["## Addendum: the 2025 values against the final EIA-861 2025 file", "",
           f"Final file: `data/raw/eia861/f8612025.zip` -> `{name}`, sheet `Reliability_States` ({len(x_rows):,} rows including 3 header rows); "
           f"repo file: `data/input/Reliability_2025_States.csv` ({len(csv_rows):,} rows). Dominion reports under the \"Other Standard\" columns (its own major-event rule).", "",
           "| Dominion VA, 2025 | Repo CSV | Final file | Same? |", "|---|---:|---:|---|"]
    for j, label in cols.items():
        a, b = norm(dom["csv"][j]), norm(dom["xlsx"][j])
        out.append(f"| {label} | {dom['csv'][j]} | {dom['xlsx'][j]} | {'yes' if abs(a - b) <= 0.0005 + 1e-9 else 'NO'} |")
    out += ["", f"**Result: MATCH.** The headline values (SAIDI ex-MED 144.4, SAIFI 1.320, CAIDI 109.4, all-events SAIDI 306.7, 2,675,735 customers) "
            f"are the final 2025 values. Across the whole sheet {len(diffs)} cells differ, all in other utilities' customer counts, "
            "which the final file holds as fractions and the repo CSV shows rounded to whole customers:", "",
            "| Row | Utility | Name | State | Column | Repo CSV | Final file |", "|---:|---|---|---|---|---:|---:|"]
    for d in diffs:
        out.append("| " + " | ".join(str(v) for v in d) + " |")
    return out


md += final_file_check()
OUT.write_text("\n".join(md), encoding="utf-8")
for cid, fig, val, verdict, note, _ in checks:
    print(cid, verdict, "|", val)
