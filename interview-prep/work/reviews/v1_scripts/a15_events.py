"""Outage events (adopted A6): auditor's own territory 15-minute series from raw EAGLE-I rows for Dominion's
103 counties (EIA-861 2025 territory, mapped via Census names in a12), peaks, 1-hour held peaks, hours to clear 90%,
the 47-event trend regression, DOE-417 Isaias row."""
import sys, math
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd, duckdb
import statsmodels.api as sm
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
terr = con.execute("select county from raw.EIA861_SERVICE_TERRITORY_2025 where try_cast(utility_number as int)=19876 and state='VA'").df()
cen = con.execute("select county_fips, namelsad from raw.CENSUS_VA_COUNTY").df()
cen["key"] = cen.namelsad.str.lower().str.replace(" county", "", regex=False).str.strip()
fips = set()
for n in terr.county:
    k = n.strip().lower(); hit = cen[cen.key == k]
    if len(hit) == 1: fips.add(str(hit.county_fips.iloc[0]).zfill(5))
print("Dominion counties mapped via Census:", len(fips))
fl = ",".join(f"'{f}'" for f in sorted(fips))
ts = con.execute(f"""select cast(run_start_time as timestamp) t, sum(try_cast(customers_out as double)) out, count(*) n
                     from raw.EAGLEI_OUTAGES_VA where lpad(cast(cast(fips_code as bigint) as varchar),5,'0') in ({fl})
                     group by 1 order by 1""").df().set_index("t")
print("territory series rows:", len(ts), ts.index.min(), ts.index.max())
ev = con.execute("""select event_key, start_utc, peak_utc, end_utc, peak_customers_out, peak_sustained_1h, background_customers_out,
                           hours_to_90pct from mart.FCT_EVENT_CONTEXT""").df()
top = pd.read_csv(REPO + r"\data\output\outage_events_top10.csv")
# full 15-minute grid so missing runs show as gaps (not zero)
grid = pd.date_range(ts.index.min(), ts.index.max(), freq="15min")
s = ts.out.reindex(grid)
held = s.rolling(4, min_periods=4).min()
print("\n#  event_key                               peak(aud)  peak(file)  held1h(aud) held1h(file)  h90(aud) h90(file)")
for r in top.itertuples():
    e = ev[ev.event_key == r.event_key].iloc[0]
    w = s[(s.index >= pd.Timestamp(e.start_utc)) & (s.index <= pd.Timestamp(e.end_utc))]
    hw = held[(held.index >= pd.Timestamp(e.start_utc)) & (held.index <= pd.Timestamp(e.end_utc))]
    pk_t = w.idxmax(); pk = w.max(); bg = e.background_customers_out
    after = s[s.index >= pk_t]
    share = (pk - after) / (pk - bg)
    hit = share[share >= 0.9]
    h90 = (hit.index[0] - pk_t).total_seconds() / 3600 if len(hit) else float("nan")
    print(f"{r.rank:<2} {r.event_key:<40} {pk:>9,.0f} {r.peak_customers_out:>11,.0f} {hw.max():>11,.0f} {r.peak_sustained_1h:>12,.0f} {h90:>8.1f} {r.hours_to_90pct:>8.1f}  peak {(pk_t - pd.Timedelta(hours=5)).date()} {r.storm_type}")
# Is the top 10 the top 10 by held-1h among all territory events? (auditor: distinct EST days of the held series)
hd = held.groupby((held.index - pd.Timedelta(hours=5)).date).max().sort_values(ascending=False)
print("\nTop 14 EST days by 1-hour held territory outage (auditor series):")
print(hd.head(14).round(0).to_string())
# the 47-event regression
oe = con.execute("""select event_key, start_day, year, peak_customers_out, peak_sustained_1h, hours_to_90pct
                    from mart.FCT_OUTAGE_EVENT where scope='territory'""").df()
big = oe[(oe.peak_sustained_1h >= 50000) & oe.hours_to_90pct.notna() & (oe.hours_to_90pct > 0)].copy()
print("\nterritory events with >= 50,000 held 1 h:", len(big), "| all scopes territory events:", len(oe))
for size in ["peak_sustained_1h", "peak_customers_out"]:
    X = sm.add_constant(pd.DataFrame({"year": big.year.astype(float), "lsize": np.log(big[size].astype(float))}))
    m = sm.OLS(np.log(big.hours_to_90pct.astype(float)), X).fit()
    print(f"ln(h90) ~ year + ln({size}): year coef {m.params.year:+.4f} -> {100*(math.exp(m.params.year)-1):+.2f}%/yr, p={m.pvalues.year:.3f}, n={int(m.nobs)}")
X = sm.add_constant(big.year.astype(float)); m = sm.OLS(np.log(big.hours_to_90pct.astype(float)), X).fit()
print(f"ln(h90) ~ year (no size): {100*(math.exp(m.params.iloc[1])-1):+.2f}%/yr p={m.pvalues.iloc[1]:.3f}")
# winter vs other hours to 90
print("hours_to_90 winter:", top[top.storm_type == "winter"].hours_to_90pct.tolist(), "| others min/max:",
      top[top.storm_type != "winter"].hours_to_90pct.min(), top[top.storm_type != "winter"].hours_to_90pct.max())
print("storm types:", top.storm_type.value_counts().to_dict(), "| Michael customer-hours (M):", round(top.customer_hours.iloc[0] / 1e6, 1))
# DOE-417: Virginia rows in Aug 2020
d = con.execute("""select year, date_began, area_affected, event_type, customers_affected, demand_loss_mw from raw.DOE417_EVENTS
                   where (date_began like '%2020-08%' or date_began like '8/%/2020%' or date_began like '08/%/2020%')""").df()
print("\nDOE-417 Aug 2020 rows:", len(d)); print(d[d.area_affected.str.contains("Virginia", case=False, na=False)].to_string()[:1500])
