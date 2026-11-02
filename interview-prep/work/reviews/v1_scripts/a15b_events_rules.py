"""Events again, with the documented rules implemented by the auditor:
P24: a county reading above twice the county's customer basis is NULL; P25/D17: hours to 90% = first reading
after the peak from which the next 13 readings (3 hours) all stay <= background + 10% of (peak - background);
background = median of the territory series over the 24 hours before the event start (auditor recomputed)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd, duckdb
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
dim = con.execute("select county_fips, customers_basis from mart.DIM_COUNTY where dominion_county").df()
dim["county_fips"] = dim.county_fips.astype(str).str.zfill(5)
print("Dominion counties (DIM_COUNTY):", len(dim))
con2 = duckdb.connect()
con2.register("dim", dim)
raw = con.execute("""select lpad(cast(cast(fips_code as bigint) as varchar),5,'0') fips, cast(run_start_time as timestamp) t,
                            try_cast(customers_out as double) out
                     from raw.EAGLEI_OUTAGES_VA""").df()
con2.register("raw", raw)
ts = con2.execute("""select t, sum(case when out > 2*customers_basis then null else out end) out,
                            sum(case when out > 2*customers_basis then 1 else 0 end) nulled
                     from raw join dim on raw.fips = dim.county_fips group by t order by t""").df().set_index("t")
print("readings nulled by the 2x rule:", int(ts.nulled.sum()))
s = ts.out.reindex(pd.date_range(ts.index.min(), ts.index.max(), freq="15min"))
held = s.rolling(4, min_periods=4).min()
nxt = s[::-1].rolling(13, min_periods=1).max()[::-1]   # max of this reading and the next 12
ev = con.execute("select event_key, start_utc, end_utc, background_customers_out from mart.FCT_EVENT_CONTEXT").df()
top = pd.read_csv(REPO + r"\data\output\outage_events_top10.csv")
print("#  peak(aud)  peak(file) held(aud) held(file)  bg(aud) bg(file) h90(aud) h90(file)")
for r in top.itertuples():
    e = ev[ev.event_key == r.event_key].iloc[0]
    st, en = pd.Timestamp(e.start_utc), pd.Timestamp(e.end_utc)
    w = s[(s.index >= st) & (s.index <= en)]; pk_t, pk = w.idxmax(), w.max()
    hmax = held[(held.index >= st) & (held.index <= en)].max()
    bg = s[(s.index >= st - pd.Timedelta(hours=24)) & (s.index < st)].median()
    thr = bg + 0.10 * (pk - bg)
    cand = nxt[(nxt.index >= pk_t) & (nxt <= thr)]
    h90 = (cand.index[0] - pk_t).total_seconds() / 3600 if len(cand) else np.nan
    print(f"{r.rank:<2} {pk:>9,.0f} {r.peak_customers_out:>10,.0f} {hmax:>9,.0f} {r.peak_sustained_1h:>10,.0f} {bg:>8,.0f} {e.background_customers_out:>8,.0f} {h90:>7.1f} {r.hours_to_90pct:>8.1f}")
