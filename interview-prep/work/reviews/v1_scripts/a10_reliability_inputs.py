"""Auditor's own read of the raw reliability inputs (PUDL 2013-2024 + EIA-861 2025 file).
Prints Dominion VA (19876) rows so the standard/MED columns can be chosen explicitly."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
p = pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)
print(p.shape); print(list(p.columns))
d = p[(p.utility_id_eia == 19876)].sort_values(["report_date", "state"])
print(d.T.to_string())
# 2025 file: three header rows
r = pd.read_csv(REPO + r"\data\input\Reliability_2025_States.csv", header=None, low_memory=False)
print(r.shape)
print(r.iloc[:3].T.to_string())
dom = r[(r[1].astype(str) == "19876")]
print(dom.T.to_string())
