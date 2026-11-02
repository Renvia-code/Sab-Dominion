"""EIA-930 DOM zone load, sales and AMI: auditor's own queries on raw tables / input CSVs."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd, duckdb
import statsmodels.formula.api as smf
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
print("EIA930 raw rows:", con.execute("select count(*) from raw.EIA930_SUBREGION").fetchone()[0])
print(con.execute("select * from raw.EIA930_SUBREGION where sub_region='DOM' limit 2").df().to_string())
d = con.execute("""select try_strptime(utc_time_end, '%m/%d/%Y %I:%M:%S %p') utc, try_strptime(local_time_end, '%m/%d/%Y %I:%M:%S %p') loc,
                          try_cast(demand_mw as double) mw,
                          balancing_authority ba, sub_region sr
                   from raw.EIA930_SUBREGION where sub_region='DOM'""").df()
print("DOM rows:", len(d), "| BAs:", d.ba.unique()[:5], "| null mw:", int(d.mw.isna().sum()), "| >60000:", int((d.mw > 60000).sum()))
d = d[(d.ba == "PJM")].dropna(subset=["utc"]).sort_values("utc").drop_duplicates("utc")
d.loc[d.mw > 60000, "mw"] = np.nan
print("DOM hours (deduped on UTC):", len(d), d.utc.min(), d.utc.max(), "| last non-null:", d.loc[d.mw.notna(), "utc"].max(), "local", d.loc[d.mw.notna(), "loc"].max())
d["he"] = d["loc"].dt.hour.replace(0, 24)   # hour ending 1..24 (midnight = 24 of the previous day)
d["ldate"] = (d["loc"] - pd.Timedelta(minutes=1)).dt.date
d["lyear"] = (d["loc"] - pd.Timedelta(minutes=1)).dt.year
d["lmonth"] = (d["loc"] - pd.Timedelta(minutes=1)).dt.month
prof = d[d.lyear.isin([2019, 2025])].groupby(["he", "lyear"]).mw.mean().unstack()
prof["growth"] = (prof[2025] / prof[2019] - 1) * 100
print("\ngrowth by hour ending (local):"); print(prof.round(1).T.to_string())
print("HE1-5 range: %.1f-%.1f ; HE13-17 range: %.1f-%.1f ; min hour %d (%.1f)" % (prof.growth.loc[1:5].min(), prof.growth.loc[1:5].max(),
      prof.growth.loc[13:17].min(), prof.growth.loc[13:17].max(), prof.growth.idxmin(), prof.growth.min()))
ann = d.groupby("lyear").mw.agg(["max", "min", "mean", "count"])
print("\nannual:"); print(ann.round(0).to_string())
print("max 2019->2025 %+.1f%% ; min %+.1f%% ; mean %+.1f%%" % ((ann.loc[2025, "max"] / ann.loc[2019, "max"] - 1) * 100, (ann.loc[2025, "min"] / ann.loc[2019, "min"] - 1) * 100, (ann.loc[2025, "mean"] / ann.loc[2019, "mean"] - 1) * 100))
d["season"] = np.where(d.lmonth.isin([12, 1, 2]), "winter", np.where(d.lmonth.isin([6, 7, 8]), "summer", None))
sp = d.dropna(subset=["season"]).groupby(["lyear", "season"]).mw.max().unstack()
sp["winter_sets_peak"] = sp.winter > sp.summer
print("\nseasonal peaks (calendar-year Dec+Jan+Feb winter):"); print(sp.to_string())
c26 = d[(d["loc"] <= "2026-10-30 00:00")]
print("2026 to HE24 29 Oct: winter %.0f summer %.0f" % (c26[(c26.lyear == 2026) & (c26.season == "winter")].mw.max(), c26[(c26.lyear == 2026) & (c26.season == "summer")].mw.max()))
t50 = d[(d.utc >= "2018-07-01") & (d.lyear <= 2025)].nlargest(50, "mw")
print("top 50 hours Jul 2018-Dec 2025 by year:", t50.lyear.value_counts().to_dict(), "| 50th:", t50.mw.min(), "| 51st:", d[(d.lyear <= 2025)].nlargest(51, "mw").mw.iloc[-1])
# degree-day normalisation (exploratory): daily mean MW ~ year + weekday + HDD + CDD (Virginia daily degree days)
dd = con.execute("select region, obs_date, kind, degree_days from raw.CPC_DEGREE_DAYS limit 3").df(); print("\nCPC sample:", dd.to_string())
dd = con.execute("""select cast(obs_date as date) dt, kind, try_cast(degree_days as double) v from raw.CPC_DEGREE_DAYS
                    where region = 'VA'""").df()
print("CPC Virginia rows:", len(dd), dd.kind.unique())
if len(dd):
    w = dd.pivot_table(index="dt", columns="kind", values="v", aggfunc="mean")
    w.columns = [c.lower() for c in w.columns]
    day = d.groupby("ldate").agg(mw=("mw", "mean"), n=("mw", "count")).reset_index()
    day = day[day.n >= 20]; day["ldate"] = pd.to_datetime(day.ldate)
    day = day.merge(w, left_on="ldate", right_index=True)
    day["yr"] = day.ldate.dt.year.astype(str); day["wd"] = day.ldate.dt.dayofweek.astype(str)
    hc = [c for c in w.columns if "heat" in c or c.startswith("h")][0]; cc = [c for c in w.columns if "cool" in c or c.startswith("c")][0]
    sub = day[day.ldate.dt.year.between(2019, 2025)]
    for spec in [f"mw ~ C(yr) + C(wd) + {hc} + {cc}", f"mw ~ C(yr) + C(wd) + {hc} + {cc} + I({hc}**2) + I({cc}**2)"]:
        m = smf.ols(spec, data=sub).fit()
        def norm(y):
            t = sub.copy(); t["yr"] = str(y); return m.predict(t).mean()
        n19, n25 = norm(2019), norm(2025)
        print("[%s] n=%d R2=%.3f degree-day normalised mean MW: 2019 %.0f 2025 %.0f -> %+.1f%% (actual daily-mean %+.1f%%)" % (spec, len(sub), m.rsquared, n19, n25, (n25 / n19 - 1) * 100,
              (sub[sub.ldate.dt.year == 2025].mw.mean() / sub[sub.ldate.dt.year == 2019].mw.mean() - 1) * 100))
# sales and AMI
s = pd.read_csv(REPO + r"\data\input\pudl_sales.csv", low_memory=False)
s["year"] = s.report_date.str[:4].astype(int)
c = s[(s.utility_id_eia == 19876) & (s.state == "VA") & (s.customer_class == "commercial")]
g = c.groupby("year").agg(mwh=("sales_mwh", "sum"), cust=("customers", "sum"))
print("\ncommercial sales (all service types):"); print(g.loc[[2013, 2024] + ([2025] if 2025 in g.index else [])].to_string())
if 2025 in g.index:
    print("2013->2025 sales %+.1f%% (%.2f -> %.2f TWh); customers %+.1f%%" % ((g.mwh[2025] / g.mwh[2013] - 1) * 100, g.mwh[2013] / 1e6, g.mwh[2025] / 1e6, (g.cust[2025] / g.cust[2013] - 1) * 100))
print("service types 2025:", c[c.year == 2025][["service_type", "sales_mwh", "customers"]].to_dict("records"))
a = pd.read_csv(REPO + r"\data\input\pudl_ami.csv", low_memory=False)
a["year"] = a.report_date.str[:4].astype(int)
x = a[(a.utility_id_eia == 19876) & (a.state == "VA") & (a.year == 2025)]
num = lambda col: pd.to_numeric(x[col], errors="coerce").fillna(0).sum()
ami, amr, non = num("advanced_metering_infrastructure"), num("automated_meter_reading"), num("non_amr_ami")
print("AMI 2025: ami %d amr %d non %d total %d share %.2f%%" % (ami, amr, non, ami + amr + non, 100 * ami / (ami + amr + non)))
