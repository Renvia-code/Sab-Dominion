# Snowflake vs DuckDB after the sql/09-11 run (2026-11-01)

| Check | DuckDB | Snowflake | Same |
|---|---:|---:|---|
| DIM_COUNTY rows | 133 | 133 | yes |
| DIM_COUNTY customers_basis (Dominion) | 3462949 | 3462949 | yes |
| FCT_OUTAGE_COUNTY_HOUR rows | 3426064 | 3426064 | yes |
| FCT_OUTAGE_COUNTY_HOUR customer_hours | 320114763.50 | 320114763.50 | yes |
| FCT_TERRITORY_15MIN rows | 388315 | 388315 | yes |
| FCT_TERRITORY_15MIN customers_out | 1021286232 | 1021286232 | yes |
| FCT_COUNTY_DAY rows | 413854 | 413854 | yes |
| FCT_COUNTY_DAY customer_hours | 255053373.75 | 255053373.75 | yes |
| FCT_COUNTY_DAY storm days | 6530 | 6530 | yes |
| FCT_COUNTY_DAY complete county-days | 395397 | 395397 | yes |
| FCT_TERRITORY_DAY proxy MED days | 103 | 103 | yes |
| FCT_OUTAGE_EVENT territory events | 486 | 486 | yes |
| FCT_OUTAGE_EVENT county events | 41278 | 41278 | yes |
| FCT_OUTAGE_EVENT sum h90 (territory) | 6152 | 6152 | yes |
| FCT_OUTAGE_EVENT sum peak held 1 h (territory) | 11722280 | 11722280 | yes |
| FCT_RESTORATION_CURVE rows | 9237 | 9237 | yes |
| FCT_COUNTY_YEAR rows | 1133 | 1133 | yes |
| FCT_COUNTY_YEAR events_non_med | 37662 | 37662 | yes |
| DOM_LOAD_HOUR_MONTH rows | 2400 | 2400 | yes |
| DOM_SEASONAL_PEAK sum peak_mw | 380020 | 380020 | yes |
| DOM_LOAD_DAILY rows | 3044 | 3044 | yes |
| FCT_SALES_SECTOR sum sales_mwh | 1091868007 | 1091868007 | yes |
| FCT_EVENT_CONTEXT rows | 486 | 486 | yes |
| FCT_EVENT_CONTEXT with a tropical cyclone | 18 | 18 | yes |
| FCT_EVENT_CONTEXT DOE-417 reports matched | 11 | 11 | yes |

25 of 25 identical.