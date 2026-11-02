"""Read origin/main's Power BI workbook through `git show` (read-only) and print every sheet briefly,
plus the Peers sheet and any sheet with a storm/fit column in full."""
import sys, io, subprocess
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 60)
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
blob = subprocess.run(["git", "-C", REPO, "show", "origin/main:powerbi/Dominion_Reliability_PowerBI_Data.xlsx"], capture_output=True).stdout
xl = pd.ExcelFile(io.BytesIO(blob), engine="openpyxl")
print("sheets:", xl.sheet_names)
full = set(a.lower() for a in sys.argv[1:])
for sh in xl.sheet_names:
    df = xl.parse(sh, header=None)
    print("=" * 100); print(sh, df.shape)
    if sh.lower() in full:
        print(df.to_string())
    else:
        print(df.head(6).to_string())
