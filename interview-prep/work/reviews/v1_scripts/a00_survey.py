"""Survey: shape, columns and a few rows of each committed table (read-only)."""
import sys, os, glob
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
names = sys.argv[1:]
files = [os.path.join(REPO, "data", n) for n in names] if names else sorted(glob.glob(os.path.join(REPO, "data", "*", "*.csv")))
for f in files:
    try:
        df = pd.read_csv(f, low_memory=False)
    except Exception as e:
        print(f, "ERR", e); continue
    print("=" * 110)
    print(os.path.relpath(f, REPO), df.shape)
    print(list(df.columns))
    n = 30 if len(df) <= 30 else 4
    print(df.head(n).to_string())
