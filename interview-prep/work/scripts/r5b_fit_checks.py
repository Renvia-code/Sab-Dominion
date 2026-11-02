"""R batch 5: re-derive the weather-fit numbers the hard-25 answers quote.

Read-only on data/output/storm_vs_saidi.csv (post-D22). Fit SAIDI ex-MED on storm county-days, 2015-2024,
then the 95% prediction interval for 2025, the SD of the annual values, and the 2.8-minute step.
Usage: r5b_fit_checks.py <repo_root> <out_txt>
"""
import math
import sys
from pathlib import Path

import pandas as pd
from scipy import stats

root, out = Path(sys.argv[1]), Path(sys.argv[2])
d = pd.read_csv(root / "data/output/storm_vs_saidi.csv")
cols = list(d.columns)
ycol = "saidi_ex_med" if "saidi_ex_med" in cols else [c for c in cols if "saidi" in c.lower()][0]
xcol = [c for c in cols if "storm" in c.lower() and "day" in c.lower()][0]
fit = d[(d["year"] >= 2015) & (d["year"] <= 2024)]
x, y = fit[xcol].astype(float), fit[ycol].astype(float)
n = len(fit)
lr = stats.linregress(x, y)
resid = y - (lr.intercept + lr.slope * x)
s = math.sqrt((resid ** 2).sum() / (n - 2))
x0 = float(d.loc[d["year"] == 2025, xcol].iloc[0])
y25 = float(d.loc[d["year"] == 2025, ycol].iloc[0])
pred = lr.intercept + lr.slope * x0
sxx = ((x - x.mean()) ** 2).sum()
tcrit = stats.t.ppf(0.975, n - 2)
half = tcrit * s * math.sqrt(1 + 1 / n + (x0 - x.mean()) ** 2 / sxx)
y22 = float(d.loc[d["year"] == 2022, ycol].iloc[0])
lines = [
    f"columns used: x={xcol}, y={ycol}; n={n} (2015-2024)",
    f"fit: SAIDI = {lr.intercept:.2f} + {lr.slope:.4f} x storm county-days; r={lr.rvalue:.4f}; p={lr.pvalue:.4f}",
    f"residual SD={s:.2f}; t(0.975,{n-2})={tcrit:.3f}",
    f"2025: storm county-days={x0:.0f}; predicted={pred:.2f}; actual={y25:.2f}; "
    f"95% PI {pred-half:.1f} to {pred+half:.1f} (+/-{half:.1f})",
    f"SD of annual SAIDI ex-MED 2015-2024={y.std(ddof=1):.2f}; min={y.min():.1f}; max={y.max():.1f}",
    f"3-yr average step: (2025-2022)/3 = ({y25:.3f}-{y22:.3f})/3 = {(y25-y22)/3:.2f}",
]
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("written", out)
