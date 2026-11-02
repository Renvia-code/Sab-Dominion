"""Spot-check mart.FCT_COUNTY_DAY customer-hours against raw EAGLE-I 15-minute rows (EST day = UTC - 5 h)."""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd, duckdb
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
print(con.execute("select any_value(typeof(run_start_time)), any_value(typeof(fips_code)), any_value(typeof(customers_out)), min(run_start_time), max(run_start_time) from raw.EAGLEI_OUTAGES_VA").fetchall())
cd = con.execute("select county_fips, day, customer_hours, failed_readings from mart.FCT_COUNTY_DAY").df()
cd["county_fips"] = cd.county_fips.astype(str).str.zfill(5); cd["day"] = pd.to_datetime(cd.day)
samp = pd.concat([cd[(cd.failed_readings == 0) & (cd.customer_hours > 0)].sample(25, random_state=7),
                  cd[(cd.day == "2020-08-04") & cd.county_fips.isin(["51087", "51760", "51153", "51059"])]])
days = sorted(set(samp.day.dt.strftime("%Y-%m-%d")))
q = f"""select lpad(cast(cast(fips_code as bigint) as varchar),5,'0') fips,
               cast(cast(run_start_time as timestamp) - interval 5 hour as date) d,
               sum(try_cast(customers_out as double))*0.25 ch, count(*) n
        from raw.EAGLEI_OUTAGES_VA
        where cast(cast(run_start_time as timestamp) - interval 5 hour as date) in ({",".join("DATE '" + d + "'" for d in days)})
        group by 1,2"""
raw = con.execute(q).df(); raw["d"] = pd.to_datetime(raw.d)
chk = samp.merge(raw, left_on=["county_fips", "day"], right_on=["fips", "d"], how="left")
chk["diff"] = (chk.customer_hours - chk.ch).abs()
print("spot check n=%d, max |mart - raw| = %.3f, rows/day %s-%s" % (len(chk), chk["diff"].max(), chk.n.min(), chk.n.max()))
print(chk[["county_fips", "day", "customer_hours", "ch", "n"]].tail(5).to_string())
