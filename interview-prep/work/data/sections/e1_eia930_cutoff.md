## E1 The EIA-930 cut-off for 2026 demand figures

**One cut-off for every 2026 figure: the last hour with data in the EIA-930 file downloaded on 1 November 2026, the hour ending midnight local time on 29 October 2026 (2026-10-30 04:00 UTC).** The file has rows for 30 October but no demand values yet (last row 2026-10-31 04:00 UTC). Every EIA-930 export in `data/output/` written by `scripts/export_powerbi_csv.py` comes from the rebuild with this cut-off. Write it as "to 29 Oct 2026" (I-03's "30 Oct" was the last row, not the last value).

The committed `data/output/dom_annual.csv` (the original snapshot, kept unchanged) stops a week earlier, at the hour ending midnight on 21 October 2026 (2026-10-22 04:00 UTC, shown as "22 Oct" in the repo): its 2026 row (7032 hours, 117.62 TWh, median 16160.0, average 16726.0) equals the rebuild cut at 21 October (7032 hours, 117.62 TWh, median 16160, average 16726). B should not use `dom_annual.csv` for 2026.

```sql
SELECT MAX(CASE WHEN demand_mw IS NOT NULL THEN utc_ts END)   AS last_valid_utc,
       MAX(CASE WHEN demand_mw IS NOT NULL THEN local_ts END) AS last_valid_local_hour_ending,
       MAX(utc_ts)                                            AS last_row_utc
FROM stg.EIA930_DOM_HOURLY
```

```sql
SELECT COUNT(*) AS hours, ROUND(SUM(demand_mw) / 1e6, 2) AS energy_twh, ROUND(MEDIAN(demand_mw)) AS median_mw,
       ROUND(AVG(demand_mw)) AS avg_mw, MAX(utc_ts) AS last_utc
FROM stg.EIA930_DOM_HOURLY
WHERE YEAR(data_date) = 2026 AND demand_mw IS NOT NULL AND data_date <= DATE '2026-10-21'  -- and '2026-10-29'
```

| 2026 figure | Committed snapshot (to 21 Oct) | Rebuild (to 29 Oct), use this |
|---|---:|---:|
| Hours reported | 7032 | 7224 |
| Energy, TWh | 117.62 | 120.49 |
| Median MW | 16,160 | 16,079 |
| Average MW | 16,726 | 16,679 |
| Summer peak MW (2026-07-03 00:00:00, hour ending 19) | 25,384 | 25,384 |
| Winter peak MW (2026-02-09 00:00:00, hour ending 8) | 25,413 | 25,413 |

The winter and summer peaks (25,413 vs 25,384 MW, a 29 MW tie) and the top-50 hours are the same under both cut-offs: no hour after 21 October comes near them. Only the 2026 totals, averages and medians differ.

| Export | Last timestamp in the data | Source |
|---|---|---|
| `dom_load_annual.csv` | 2026-10-30 04:00:00 | rebuild (sql/06), all years; 2026 row to the cut-off |
| `dom_top50_hours.csv` | 2026-09-04 20:00:00 | rebuild (sql/06); rank_today ranks every hour to the cut-off |
| `dom_load_profile.csv` | 2026-01-01 05:00:00 | rebuild (sql/07); uses 2019 and 2025 only |
| `dom_load_hour_month.csv` | 2026-10-01 | rebuild (sql/10); last month October 2026, partial |
| `dom_seasonal_peak.csv` | 2026-07-03 | rebuild (sql/10); 2026 winter = Jan-Feb only |
| `dom_load_daily.csv` | 2026-10-29 | rebuild (sql/10) |

Queries for the last timestamps:

```sql
SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL;  -- dom_load_annual.csv
SELECT MAX(utc_ts) FROM mart.DOM_TOP50_HOURS;  -- dom_top50_hours.csv
SELECT MAX(utc_ts) FROM stg.EIA930_DOM_HOURLY WHERE demand_mw IS NOT NULL AND YEAR(data_date) = 2025;  -- dom_load_profile.csv
SELECT MAX(make_date(year, month, 1)) FROM mart.DOM_LOAD_HOUR_MONTH WHERE hours_reported > 0;  -- dom_load_hour_month.csv
SELECT MAX(peak_date) FROM mart.DOM_SEASONAL_PEAK;  -- dom_seasonal_peak.csv
SELECT MAX(data_date) FROM mart.DOM_LOAD_DAILY WHERE hours_reported > 0;  -- dom_load_daily.csv
```
