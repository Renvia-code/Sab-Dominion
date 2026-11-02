"""A6 (arithmetic only): what one minute of SAIDI means for Dominion Energy Virginia in customer-minutes and
customer-hours. No dollar value: R's claims register holds no verified DOE ICE Calculator or LBNL value-of-
reliability figure (checked 2026-11-01), so none is given. Writes sections/a6_optional.md."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "sections" / "a6_optional.md"
con = duckdb.connect(str(ROOT / "data" / "raw" / "duckdb" / "reliability_local.duckdb"), read_only=True)

Q = """SELECT year, customers, saidi_ex_med, cust_minutes_ex_med
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2022 AND 2025 ORDER BY year"""
d = con.execute(Q).df().set_index("year")
c25 = int(d.loc[2025, "customers"])
s = d.saidi_ex_med.astype(float)
avg_22_24, avg_23_25 = s.loc[2022:2024].mean(), s.loc[2023:2025].mean()
step3 = avg_23_25 - avg_22_24
step1 = s.loc[2025] - s.loc[2024]
cm25 = float(d.loc[2025, "cust_minutes_ex_med"])

rows = [
    ("One minute of SAIDI, 2025", "1 x customers", f"{c25:,} customer-minutes", f"{c25 / 60:,.0f} customer-hours"),
    ("Three-year average, 2022-24 -> 2023-25", f"{avg_22_24:.1f} -> {avg_23_25:.1f} = +{step3:.2f} min",
     f"{step3 * c25:,.0f} customer-minutes", f"{step3 * c25 / 60:,.0f} customer-hours"),
    ("2024 -> 2025", f"{s.loc[2024]:.1f} -> {s.loc[2025]:.1f} = +{step1:.1f} min",
     f"{step1 * c25:,.0f} customer-minutes", f"{step1 * c25 / 60:,.0f} customer-hours"),
    ("All of 2025, ex-MED", f"{s.loc[2025]:.1f} min x {c25:,}", f"{cm25:,.0f} customer-minutes", f"{cm25 / 60:,.0f} customer-hours"),
]
md = ["## A6 What one minute of SAIDI means (arithmetic only)", "",
      f"**Finding.** For Dominion Energy Virginia in 2025, one minute of SAIDI is one minute for each of its {c25:,} Virginia customers: "
      f"**{c25:,} customer-minutes, about {c25 / 60:,.0f} customer-hours**. The rise in the three-year average behind the scorecard "
      f"(130.2 -> 133.0) is about {step3 * c25 / 1e6:.1f} million customer-minutes, or {step3 * c25 / 60 / 1000:,.0f} thousand customer-hours, "
      "at 2025 customer numbers. **No dollar value is given:** R's claims register has no verified DOE ICE Calculator or LBNL "
      "value-of-reliability source (checked 1 Nov 2026), so the brief's optional order-of-magnitude estimate is skipped.", "",
      "| Quantity | SAIDI (min, ex-MED) | Customer-minutes | Customer-hours |", "|---|---|---:|---:|"]
md += [f"| {a} | {b} | {c} | {e} |" for a, b, c, e in rows]
md += ["", "```sql", Q, "```", "",
       "**Caveats.** Customer counts differ by year (2022-2024 customers are not 2025's), so the step rows use 2025 customers as an "
       "illustration; `cust_minutes_ex_med` is the exact 2025 total. SAIDI is ex-MED (Dominion files under its own major-event rule), so outages on major event days "
       "are not in these customer-minutes. Customer-minutes say nothing about who was affected: one customer out for "
       "100 minutes and 100 customers out for one minute count the same.", ""]
OUT.write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
