"""EAGLE-I county-day checks (adopted rows). Auditor's own storm flags (a12 output), own per-1k normalisation,
own whole-day bootstrap (seed 20261101, 2,000 resamples); spot-check of customer-hours against raw 15-min rows."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd, duckdb
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
cd = con.execute("select county_fips, day, year, dominion_only_county, customers_basis, customer_hours, readings, failed_readings, storm_day from mart.FCT_COUNTY_DAY").df()
cd["day"] = pd.to_datetime(cd.day)
med = con.execute("select day, is_med_proxy from mart.FCT_TERRITORY_DAY").df(); med["day"] = pd.to_datetime(med.day)
cmap = pd.read_csv(REPO + r"\data\output\county_outage_map.csv", dtype={"county_fips": str})
print("county_outage_map columns:", list(cmap.columns)); print(cmap.head(3).to_string())
flagcol = [c for c in cmap.columns if "flag" in c.lower()][0]
onmap = set(cmap.loc[cmap[flagcol] == "ok", "county_fips"].astype(str).str.zfill(5))
print("map counties ok:", len(onmap), "| all counties:", cd.county_fips.nunique())
st = pd.read_csv(REPO + r"\interview-prep\work\reviews\v1_work\auditor_storm_county_days.csv", dtype={"fips": str, "date": str})
st["day"] = pd.to_datetime(st.date, format="%Y%m%d"); st = st[(st.year >= 2015) & (st.year <= 2025)]
mine = set(zip(st.fips, st.day))
cd["county_fips"] = cd.county_fips.astype(str).str.zfill(5)
cd["storm_mine"] = [(f, d) in mine for f, d in zip(cd.county_fips, cd.day)]
print("storm flags: producer", int(cd.storm_day.sum()), "| auditor", int(cd.storm_mine.sum()), "| disagree", int((cd.storm_day != cd.storm_mine).sum()))
cd = cd.merge(med, on="day", how="left")
cd["ch1k"] = cd.customer_hours / cd.customers_basis * 1000
cd["onmap"] = cd.county_fips.isin(onmap)
S = cd[cd.storm_mine]
print("storm county-days 2015-25 all 103:", len(S), "| off map:", int((~S.onmap).sum()), "| on map failed:", int((S.onmap & (S.failed_readings > 0)).sum()),
      "| on map complete:", int((S.onmap & (S.failed_readings == 0)).sum()), "| failed in 2025:", int((S.onmap & (S.failed_readings > 0) & (S.year == 2025)).sum()))
m25 = cd[(cd.year == 2025) & cd.onmap]
print("2025 complete share of on-map county-days: %.1f%%" % (100 * (m25.failed_readings == 0).mean()))
P = cd[cd.onmap & (cd.failed_readings == 0)].copy()
rng = np.random.default_rng(20261101); B = 2000
def ratio(df, label):
    g = df.groupby(["day", "storm_mine"]).ch1k.agg(["sum", "count"]).unstack(fill_value=0)
    ssum, scnt = g[("sum", True)].values, g[("count", True)].values
    csum, ccnt = g[("sum", False)].values, g[("count", False)].values
    s, c = ssum.sum() / scnt.sum(), csum.sum() / ccnt.sum()
    idx = rng.integers(0, len(g), size=(B, len(g)))
    bs = ssum[idx].sum(1) / scnt[idx].sum(1); bc = csum[idx].sum(1) / ccnt[idx].sum(1); br = bs / bc
    q = lambda a: np.percentile(a, [2.5, 97.5])
    print(f"{label:<34} storm n={int(scnt.sum()):>5} {s:8.3f} {q(bs).round(1)}  calm n={int(ccnt.sum()):>6} {c:7.3f} {q(bc).round(1)}  ratio {s/c:6.3f} {q(br).round(1)}")
    return s / c, q(br)
ratio(P, "all complete, 2015-2025")
ratio(P[~P.is_med_proxy.astype(bool)], "non-major days")
ratio(P[P.dominion_only_county.astype(bool)], "Dominion-only counties")
yr = {}
for y in range(2015, 2026):
    yr[y] = ratio(P[P.year == y], f"year {y}")
print("min/max yearly ratio:", min((v[0], k) for k, v in yr.items()), max((v[0], k) for k, v in yr.items()),
      "| every yearly CI low > 1:", all(v[1][0] > 1 for v in yr.values()))
# ---- county map: outage minutes per customer a year, non-major days, 2015-2024 mean of annual values
W = cd[(cd.year <= 2024) & (~cd.is_med_proxy.astype(bool))]
cy = W.groupby(["county_fips", "year"]).agg(ch=("customer_hours", "sum"), basis=("customers_basis", "first")).reset_index()
cy["mpc"] = cy.ch * 60 / cy.basis
cm = cy.groupby("county_fips").agg(mpc=("mpc", "mean"), basis=("basis", "first")).reset_index()
cm = cm[cm.county_fips.isin(onmap)]
big = cm[cm.basis >= 20000]
dimc = con.execute("select county_fips, county_label, dominion_only_county from mart.DIM_COUNTY").df(); dimc["county_fips"] = dimc.county_fips.astype(str).str.zfill(5)
cm = cm.merge(dimc, on="county_fips")
big = cm[cm.basis >= 20000]
print("\ncounties on map:", len(cm), "| >=20,000 customers:", len(big))
print("min:", big.nsmallest(1, "mpc")[["county_label", "mpc", "basis"]].values.tolist(), "max:", big.nlargest(1, "mpc")[["county_label", "mpc", "basis"]].values.tolist())
print("overall min/max (any size):", cm.nsmallest(1, "mpc")[["county_label", "mpc"]].values.tolist(), cm.nlargest(1, "mpc")[["county_label", "mpc"]].values.tolist())
for flag, nm in [(True, "Dominion-only"), (False, "shared")]:
    g = cm[cm.dominion_only_county.astype(bool) == flag]
    print(f"{nm}: n={len(g)} simple mean {g.mpc.mean():.1f} | customer-weighted {np.average(g.mpc, weights=g.basis):.1f}")
print("Dominion-only counties among all 103:", int(dimc.dominion_only_county.sum()), "| off-map Dominion-only:", sorted(set(dimc[dimc.dominion_only_county.astype(bool)].county_fips) - onmap))
cmp = cm.merge(cmap.assign(county_fips=cmap.county_fips.astype(str).str.zfill(5)), on="county_fips", suffixes=("", "_out"))
valcol = [c for c in cmap.columns if "non_med" in c or "minutes" in c]
print("map file value columns:", valcol)
if valcol:
    print("max |auditor - file| on", valcol[0], ":", float((cmp.mpc - cmp[valcol[0]]).abs().max()))
# ---- spot check customer-hours against raw 15-minute rows (EST day = UTC - 5 h)
samp = cd[(cd.failed_readings == 0) & (cd.customer_hours > 0)].sample(25, random_state=7)
isa = cd[(cd.day == "2020-08-04") & (cd.county_fips.isin(["51087", "51760", "51153", "51059"]))]
samp = pd.concat([samp, isa])
raw = con.execute("""select lpad(cast(fips_code as varchar),5,'0') fips, cast(run_start_time - interval 5 hour as date) d,
                     sum(customers_out)*0.25 ch, count(*) n from raw.EAGLEI_OUTAGES_VA
                     where cast(run_start_time - interval 5 hour as date) in (select unnest(?::date[]))
                     group by 1,2""", [list(samp.day.dt.date.unique())]).df()
raw["d"] = pd.to_datetime(raw.d)
chk = samp.merge(raw, left_on=["county_fips", "day"], right_on=["fips", "d"], how="left")
chk["diff"] = chk.customer_hours - chk.ch
print("\nspot check (n=%d): max |mart - raw| customer-hours = %.2f; raw rows/day range %s" % (len(chk), chk["diff"].abs().max(), (chk.n.min(), chk.n.max())))
print(chk[["county_fips", "day", "customer_hours", "ch", "n"]].tail(6).to_string())
