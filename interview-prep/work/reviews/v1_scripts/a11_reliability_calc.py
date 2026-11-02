"""Auditor's independent reliability numbers from the raw inputs only
(data/input/pudl_reliability_2013_2024.csv + data/input/Reliability_2025_States.csv).
Standard rule (auditor's own): use the IEEE row when it has an ex-MED SAIDI, else the Other row;
any utility-year with BOTH filled is reported so the rule's effect is visible."""
import sys, math
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd
from scipy import stats
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"

def num(x):
    if pd.isna(x): return np.nan
    s = str(x).replace(",", "").strip()
    if s in (".", "", "nan"): return np.nan
    try: return float(s)
    except ValueError: return np.nan

# ---- PUDL 2013-2024
p = pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)
p["year"] = p.report_date.str[:4].astype(int)
p = p.rename(columns={"utility_id_eia": "uid", "saidi_wo_major_event_days_minutes": "saidi_ex",
    "saifi_wo_major_event_days_customers": "saifi_ex", "caidi_wo_major_event_days_minutes": "caidi_ex",
    "saidi_w_major_event_days_minutes": "saidi_all", "saifi_w_major_event_days_customers": "saifi_all",
    "caidi_w_major_event_days_minutes": "caidi_all"})
p["std"] = p.standard.map({"ieee_standard": "IEEE", "other_standard": "Other"})
p = p[["uid", "state", "year", "std", "customers", "saidi_ex", "saifi_ex", "caidi_ex", "saidi_all", "saifi_all", "caidi_all"]]
# ---- EIA-861 2025
r = pd.read_csv(REPO + r"\data\input\Reliability_2025_States.csv", header=None, skiprows=3, low_memory=False, dtype=str)
rows = []
for _, x in r.iterrows():
    uid = num(x[1])
    if np.isnan(uid): continue
    base = dict(uid=int(uid), state=str(x[3]).strip(), year=2025)
    rows.append({**base, "std": "IEEE", "customers": num(x[14]), "saidi_all": num(x[5]), "saifi_all": num(x[6]), "caidi_all": num(x[7]),
                 "saidi_ex": num(x[8]), "saifi_ex": num(x[9]), "caidi_ex": num(x[10])})
    rows.append({**base, "std": "Other", "customers": num(x[23]), "saidi_all": num(x[17]), "saifi_all": num(x[18]), "caidi_all": num(x[19]),
                 "saidi_ex": num(x[20]), "saifi_ex": num(x[21]), "caidi_ex": num(x[22])})
q = pd.DataFrame(rows)
allr = pd.concat([p, q], ignore_index=True)
allr = allr[allr.saidi_ex.notna() | allr.saifi_ex.notna() | allr.saidi_all.notna()]
both = allr.groupby(["uid", "state", "year"])["std"].nunique()
print("utility-state-years with BOTH standards filled:", int((both > 1).sum()))
dups = allr.groupby(["uid", "state", "year", "std"]).size()
print("duplicate utility-state-year-standard rows:", int((dups > 1).sum()))
allr["pref"] = allr["std"].map({"IEEE": 0, "Other": 1})
sel = allr.sort_values("pref").groupby(["uid", "state", "year"], as_index=False).first()

def U(uid, st): return sel[(sel.uid == uid) & (sel.state == st)].set_index("year").sort_index()

dom = U(19876, "VA")
print("\n== Dominion VA (19876), chosen rows")
print(dom[["std", "customers", "saidi_ex", "saifi_ex", "caidi_ex", "saidi_all", "saifi_all"]].to_string())
s = dom.saidi_ex; f = dom.saifi_ex; c = dom.caidi_ex
print("\n3-yr SAIDI ex-MED 2022-24 = %.3f ; 2023-25 = %.3f ; diff = %.3f" % (s.loc[2022:2024].mean(), s.loc[2023:2025].mean(), s.loc[2023:2025].mean() - s.loc[2022:2024].mean()))
print("(144.4-136.047)/3 = %.3f" % ((s[2025] - s[2022]) / 3))
nc = U(19876, "NC")
vanc = (dom.saidi_ex * dom.customers + nc.saidi_ex * nc.customers) / (dom.customers + nc.customers)
print("VA+NC customer-weighted 3-yr: 2022-24 = %.2f ; 2023-25 = %.2f" % (vanc.loc[2022:2024].mean(), vanc.loc[2023:2025].mean()))
print("NC rows:", nc[["std", "customers", "saidi_ex"]].loc[2022:2025].to_dict("index"))
for a, b in [(2022, 2025), (2023, 2025)]:
    cs_a, cs_b = s[a] / f[a], s[b] / f[b]
    print(f"\n{a}->{b}: SAIDI {s[a]:.3f}->{s[b]:.3f} ({(s[b]/s[a]-1)*100:+.2f}%), SAIFI {f[a]:.3f}->{f[b]:.3f} ({(f[b]/f[a]-1)*100:+.2f}%), "
          f"CAIDI(S/F) {cs_a:.2f}->{cs_b:.3f} ({(cs_b/cs_a-1)*100:+.2f}%), CAIDI reported {c[a]:.3f}->{c[b]:.3f} ({(c[b]/c[a]-1)*100:+.2f}%)")
    print(f"   log share from frequency = {math.log(f[b]/f[a]) / math.log(s[b]/s[a]) * 100:.1f}%")
print("\n2018 SAIFI %.3f, SAIDI 2018 %.3f, 2019 %.3f" % (f[2018], s[2018], s[2019]))
w = s.loc[2015:2025]; print("SAIDI 2015-25 min %.3f (%d) max %.3f (%d)" % (w.min(), w.idxmin(), w.max(), w.idxmax()))
print("SAIFI rank of 2025 in 2013-2025 (desc):", list(f.sort_values(ascending=False).round(3).items())[:3])
print("2025 all-events SAIDI %.1f; MED minutes %.1f; MED share %.2f%%; customers %d; 1.32*109.394=%.3f" % (
    dom.saidi_all[2025], dom.saidi_all[2025] - s[2025], (dom.saidi_all[2025] - s[2025]) / dom.saidi_all[2025] * 100, dom.customers[2025], 1.32 * 109.394))

# ---- trend tests, OLS on year 2015-2025 (n=11)
def ols(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    res = stats.linregress(x, y)
    tcrit = stats.t.ppf(0.975, len(x) - 2)
    return res.slope, res.slope - tcrit * res.stderr, res.slope + tcrit * res.stderr, res.pvalue, res.rvalue
yrs = list(range(2015, 2026))
for nm, ser in [("SAIFI", f), ("CAIDI(reported)", c), ("SAIDI", s)]:
    b, lo, hi, pv, _ = ols(yrs, ser.loc[2015:2025].values)
    print(f"trend {nm}: slope {b:+.4f}/yr CI [{lo:+.4f},{hi:+.4f}] p={pv:.3f}")

# ---- peers
peers = [(5416, "NC"), (7140, "GA"), (3046, "NC"), (19876, "VA"), (17539, "SC"), (6455, "FL"), (195, "AL"), (14940, "PA"), (1167, "MD"), (14715, "PA"), (15270, "MD"), (6452, "FL")]
out = []
for uid, st in peers:
    u = U(uid, st)
    w5 = u.loc[2021:2025]; w3 = u.loc[2023:2025]
    out.append(dict(uid=uid, st=st, n5=len(w5), saifi5=w5.saifi_ex.mean(), caidi5=w5.caidi_ex.mean(),
                    caidi5_from_means=w5.saidi_ex.mean() / w5.saifi_ex.mean(), saidi3=w3.saidi_ex.mean(),
                    saifi5_all=w5.saifi_all.mean(), saidi3_all=w3.saidi_all.mean(),
                    stds_2013=u.loc[2013, "std"] if 2013 in u.index else None,
                    ieee_all_2014_25=all(u.loc[2014:2025, "std"] == "IEEE") and len(u.loc[2014:2025]) == 12,
                    stds=",".join(sorted(set(u.loc[2014:2025, "std"])))))
P = pd.DataFrame(out)
for col in ["saifi5", "caidi5", "saidi3", "saifi5_all", "saidi3_all", "caidi5_from_means"]:
    P[col + "_rank"] = P[col].rank(ascending=False, method="min").astype(int)
print("\n== peers (2021-25 means of annual values; SAIDI 2023-25)")
print(P.round(3).to_string())
others = P[P.uid != 19876]
print("11-peer medians: SAIFI %.3f CAIDI %.2f CAIDI(from means) %.2f SAIDI3 %.2f SAIFI_all %.3f SAIDI3_all %.1f" % (
    others.saifi5.median(), others.caidi5.median(), others.caidi5_from_means.median(), others.saidi3.median(), others.saifi5_all.median(), others.saidi3_all.median()))
print("IEEE every year 2014-25:", int(P.ieee_all_2014_25.sum()), "of", len(P))
print("standard in 2013:", P[["uid", "st", "stds_2013"]].values.tolist())
