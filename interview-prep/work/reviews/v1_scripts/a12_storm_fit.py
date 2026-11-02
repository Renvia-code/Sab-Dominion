"""Auditor's own storm county-day count from raw NOAA rows + the weather fit.
County list: EIA-861 2025 service territory (19876, VA) matched to FIPS through the Census county table
(not the producer's NOAA-name lookup). NOAA zone events are spread to counties with NOAA's zone-county file.
Line-risk types as documented in sql/05. D22 = Bedford city 51515 folded into Bedford County 51019."""
import sys, io, math, subprocess
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd, duckdb
from scipy import stats
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)

terr = con.execute("select county from raw.EIA861_SERVICE_TERRITORY_2025 where try_cast(utility_number as int)=19876 and state='VA'").df()
cen = con.execute("select county_fips, name, namelsad from raw.CENSUS_VA_COUNTY").df()
cen["key"] = cen.namelsad.str.lower().str.replace(" county", "", regex=False).str.strip()
def ckey(n):
    n = n.strip().lower()
    if n.endswith(" city") and n not in ("james city", "charles city"):
        return n  # "alexandria city"
    return n
m = {}
miss = []
for n in terr.county:
    k = ckey(n)
    hit = cen[cen.key == k]
    if len(hit) == 0 and k == "bedford city":
        m[n] = "51515"; continue
    if len(hit) != 1:
        miss.append((n, len(hit))); continue
    m[n] = str(hit.county_fips.iloc[0]).zfill(5)
print("EIA territory rows:", len(terr), "mapped:", len(m), "unmapped:", miss)
dom_fips = set(m.values())
print("distinct FIPS:", len(dom_fips), "| incl 51515:", "51515" in dom_fips, "| after D22 fold:", len({('51019' if f == '51515' else f) for f in dom_fips}))

ev = con.execute("""select year, begin_yearmonth, begin_day, event_type, cz_type, cz_fips, cz_name, state
                    from raw.NOAA_STORM_EVENTS where state='VIRGINIA'""").df()
print("NOAA raw rows total:", con.execute("select count(*) from raw.NOAA_STORM_EVENTS").fetchone()[0], "| VA rows:", len(ev))
risk = {**{t: "wind" for t in ['Thunderstorm Wind', 'High Wind', 'Strong Wind', 'Tornado']},
        **{t: "winter" for t in ['Ice Storm', 'Winter Storm', 'Heavy Snow', 'Blizzard', 'Sleet']},
        **{t: "tropical" for t in ['Hurricane', 'Hurricane (Typhoon)', 'Tropical Storm', 'Tropical Depression']}}
ev["risk"] = ev.event_type.map(risk)
ev = ev[ev.risk.notna()].copy()
zc = con.execute("select zone, fips, county_name from raw.NOAA_ZONE_COUNTY where state='VA' and fips<>'9999'").df()
zc["zone_i"] = pd.to_numeric(zc.zone, errors="coerce"); zc["fips5"] = zc.fips.astype(str).str.zfill(5)
zmap = zc.groupby("zone_i").fips5.apply(set).to_dict()
nmap = zc.assign(k=zc.county_name.str.upper().str.replace("CITY OF ", "", regex=False)).groupby("k").fips5.apply(set).to_dict()
recs, unm = [], 0
for x in ev.itertuples():
    if x.cz_type == "C":
        fl = {"51" + str(int(float(x.cz_fips))).zfill(3)}
    else:
        z = pd.to_numeric(x.cz_fips, errors="coerce")
        fl = zmap.get(z) or nmap.get(str(x.cz_name).upper(), set())
        if not fl: unm += 1
    d = f"{int(x.begin_yearmonth)}{int(x.begin_day):02d}"
    for fp in fl:
        recs.append((int(x.year), fp, d, x.risk))
print("line-risk VA events:", len(ev), "| zone events unmapped:", unm)
R = pd.DataFrame(recs, columns=["year", "fips", "date", "risk"])
R = R[R.fips.isin(dom_fips)]
def count(df, fold):
    d = df.copy()
    if fold: d["fips"] = d.fips.replace("51515", "51019")
    g = d.groupby(["year", "fips", "date"]).risk.apply(set).reset_index()
    out = g.groupby("year").agg(n=("date", "size"), wind=("risk", lambda s: sum("wind" in v for v in s)),
                                winter=("risk", lambda s: sum("winter" in v for v in s)), tropical=("risk", lambda s: sum("tropical" in v for v in s)))
    return out
A = count(R, True); B = count(R, False)
tab = A.join(B, rsuffix="_noD22")
print(tab.to_string())
print("county-days removed by D22, 2013-2025:", int((B.n - A.n).sum()))
print("total 2015-2025 storm county-days (D22):", int(A.n.loc[2015:2025].sum()))
# save the auditor's storm county-day list (D22 fold) for the EAGLE-I checks
import os
WORK = REPO + r"\interview-prep\work\reviews\v1_work"; os.makedirs(WORK, exist_ok=True)
sv = R.copy(); sv["fips"] = sv.fips.replace("51515", "51019")
sv = sv.groupby(["year", "fips", "date"]).risk.apply(lambda s: "|".join(sorted(set(s)))).reset_index()
sv.to_csv(WORK + r"\auditor_storm_county_days.csv", index=False)
print("saved", len(sv), "storm county-days")

# ---------------- the fit (auditor's own OLS)
rel = pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)
rel = rel[(rel.utility_id_eia == 19876) & (rel.state == "VA") & (rel.standard == "other_standard")]
saidi = {int(d[:4]): v for d, v in zip(rel.report_date, rel.saidi_wo_major_event_days_minutes)}
saidi[2025] = 144.4  # EIA-861 2025 final, Other standard (verified in a11)
def fit_report(storm, label):
    yrs = list(range(2015, 2025))
    x = np.array([storm[y] for y in yrs], float); y = np.array([saidi[y] for y in yrs], float)
    n = len(x); lr = stats.linregress(x, y); r = lr.rvalue
    t = r * math.sqrt((n - 2) / (1 - r * r)); p = 2 * stats.t.sf(abs(t), n - 2)
    z = math.atanh(r); se = 1 / math.sqrt(n - 3); lo, hi = math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)
    x0 = storm[2025]; yhat = lr.intercept + lr.slope * x0
    resid = y - (lr.intercept + lr.slope * x); s2 = (resid ** 2).sum() / (n - 2); sxx = ((x - x.mean()) ** 2).sum()
    tc = stats.t.ppf(0.975, n - 2)
    pi = tc * math.sqrt(s2 * (1 + 1 / n + (x0 - x.mean()) ** 2 / sxx)); ci = tc * math.sqrt(s2 * (1 / n + (x0 - x.mean()) ** 2 / sxx))
    print(f"\n== fit [{label}] 2015-2024: SAIDI = {lr.intercept:.4f} + {lr.slope:.6f} x ; r={r:.4f} R2={r*r:.4f} t={t:.3f} p={p:.4f} "
          f"Fisher95%=[{lo:.3f},{hi:.3f}]")
    print(f"   2025 x={x0}: fit {yhat:.2f} actual 144.4 diff {144.4-yhat:+.2f}; PI [{yhat-pi:.1f},{yhat+pi:.1f}] CI-line [{yhat-ci:.1f},{yhat+ci:.1f}]")
    rows = []
    for yy in range(2015, 2026):
        fv = lr.intercept + lr.slope * storm[yy]; rows.append((yy, storm[yy], round(saidi[yy], 1), round(fv, 1), round(saidi[yy] - fv, 1)))
    print("   table:", rows)
    mean_s = y.mean()
    adj = [saidi[yy] - (lr.intercept + lr.slope * storm[yy]) + mean_s for yy in range(2015, 2026)]
    adj_r = [round(a, 1) for a in adj]
    for nm, ser in [("unrounded", adj), ("rounded 1dp", adj_r)]:
        lt = stats.linregress(range(2015, 2026), ser); tc9 = stats.t.ppf(0.975, 9)
        print(f"   weather-adjusted trend ({nm}): {lt.slope:+.3f}/yr CI [{lt.slope-tc9*lt.stderr:+.2f},{lt.slope+tc9*lt.stderr:+.2f}] p={lt.pvalue:.3f}")
fit_report({int(y): int(v) for y, v in A.n.items()}, "auditor storm count, D22")
fit_report({int(y): int(v) for y, v in B.n.items()}, "auditor storm count, no D22")
# public: origin/main storm_vs_saidi.csv, read through git (read-only)
txt = subprocess.run(["git", "-C", REPO, "show", "origin/main:data/output/storm_vs_saidi.csv"], capture_output=True, text=True).stdout
pub = pd.read_csv(io.StringIO(txt))
print("\norigin/main storm_vs_saidi.csv:\n", pub.to_string())
fit_report(dict(zip(pub.year.astype(int), pub.storm_county_days.astype(int))), "origin/main storm counts")
