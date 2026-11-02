# Data model inventory: `original_copy_readonly.pbix` (read-only, pbixray)

## Tables

AmiEventStudy, DIM_UTILITY, DOM_LOAD_ANNUAL, DOM_LOAD_PROFILE, DOM_TOP50_HOURS, Dashboard Year, FCT_RELIABILITY, Headline, LoadGrowth, Programmes2025, SAIDI_WEATHER_ADJUSTED, STORM_INDEX, Tests, V_GROUP_INDEX, V_STORM_VS_SAIDI, V_STORM_VS_SAIDI (2), V_TREND

Count: 17

## Table statistics

| TableName | ColumnName | Cardinality | Dictionary | HashIndex | DataSize | ModifiedTime | StructureModifiedTime |
|---|---|---|---|---|---|---|---|
| AmiEventStudy | Column1 | 8 | 259 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| AmiEventStudy | Column2 | 8 | 271 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| AmiEventStudy | Column3 | 8 | 275 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| AmiEventStudy | Column4 | 6 | 221 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| DIM_UTILITY | UTILITY_ID | 1210 | 0 | 32949 | 3568 | 2026-10-21 05:53:34 | 2026-10-21 05:49:47 |
| DIM_UTILITY | STATE | 51 | 837 | 0 | 1176 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| DIM_UTILITY | UTILITY_KEY | 1283 | 15870 | 0 | 2200 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| DIM_UTILITY | UTILITY_NAME | 1210 | 29142 | 0 | 2200 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| DIM_UTILITY | ENTITY_TYPE | 7 | 369 | 0 | 184 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| DIM_UTILITY | PEER_GROUP | 7 | 433 | 0 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| DIM_UTILITY | Display name | 1214 | 29164 | 0 | 2200 | 2026-10-22 18:23:17 | 2026-10-22 18:22:52 |
| DIM_UTILITY | Short name | 1214 | 29122 | 0 | 2200 | 2026-10-27 17:44:00 | 2026-10-27 17:43:36 |
| DIM_UTILITY | Quadrant name | 5 | 263 | 0 | 152 | 2026-10-27 18:05:31 | 2026-10-27 18:03:04 |
| DIM_UTILITY | Region | 7 | 347 | 0 | 160 | 2026-10-27 23:08:53 | 2026-10-27 23:08:44 |
| DOM_LOAD_ANNUAL | YEAR | 1 | 0 | 0 | 152 | 2026-10-26 22:25:41 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | WINTER_PEAK_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | SUMMER_PEAK_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | PEAK_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | FLOOR_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | MEDIAN_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | AVG_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | ENERGY_TWH | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | HOURS_REPORTED | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_ANNUAL | HOURS_MISSING | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_LOAD_PROFILE | HOUR_NO | 1 | 0 | 0 | 152 | 2026-10-27 01:55:13 | 2026-10-27 01:53:23 |
| DOM_LOAD_PROFILE | AVG_MW_2019 | 1 | 0 | 0 | 152 | 2026-10-27 01:53:23 | 2026-10-27 01:53:23 |
| DOM_LOAD_PROFILE | AVG_MW_2025 | 1 | 0 | 0 | 152 | 2026-10-27 01:53:23 | 2026-10-27 01:53:23 |
| DOM_LOAD_PROFILE | GROWTH_PCT | 1 | 0 | 0 | 152 | 2026-10-27 01:53:23 | 2026-10-27 01:53:23 |
| DOM_TOP50_HOURS | YEAR | 1 | 0 | 0 | 152 | 2026-10-26 22:25:57 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | DATA_DATE | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | HOUR_NO | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | UTC_TS | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | DEMAND_MW | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | RANK_TODAY | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| DOM_TOP50_HOURS | RANK_END_2025 | 1 | 0 | 0 | 152 | 2026-10-26 22:25:01 | 2026-10-26 22:25:01 |
| Dashboard Year | Year | 13 | 0 | 1133 | 152 | 2026-10-31 19:55:56 | 2026-10-31 19:55:56 |
| FCT_RELIABILITY | UTILITY_KEY | 1283 | 15870 | 0 | 21104 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | UTILITY_ID | 1210 | 0 | 32949 | 34880 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | STATE | 51 | 837 | 0 | 10176 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | YEAR | 13 | 144 | 0 | 6520 | 2026-10-27 07:40:55 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | STANDARD | 2 | 171 | 0 | 472 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | SOURCE | 2 | 227 | 0 | 1440 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | Customers Served | 11481 | 0 | 263117 | 52528 | 2026-10-21 06:21:03 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | SAIDI_ALL | 10685 | 0 | 262781 | 52528 | 2026-10-27 02:45:35 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | SAIFI_ALL | 3283 | 0 | 65645 | 24424 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CAIDI_ALL | 11317 | 0 | 262965 | 48680 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | SAIDI_EX_MED | 8963 | 0 | 134741 | 46744 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | SAIFI_EX_MED | 2655 | 0 | 65645 | 21448 | 2026-10-27 02:08:53 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CAIDI_EX_MED | 9857 | 0 | 262709 | 42496 | 2026-10-27 02:43:35 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | STORM_SAIDI | 7059 | 0 | 132405 | 35192 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | STORM_SAIFI | 1564 | 0 | 32885 | 16216 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CUST_MINUTES_ALL | 12897 | 103216 | 0 | 26336 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CUST_MINUTES_EX_MED | 11572 | 92616 | 0 | 23448 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CUST_INTERRUPTIONS_ALL | 11875 | 95040 | 0 | 24424 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | CUST_INTERRUPTIONS_EX_MED | 10558 | 84504 | 0 | 21448 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | MAX_KV | 92 | 776 | 0 | 5136 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | AUTO_RECORDED | 2 | 48 | 0 | 1016 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | MOMENTARY_DEF | 3 | 159 | 0 | 1288 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| FCT_RELIABILITY | INACTIVE_INCLUDED | 2 | 48 | 0 | 680 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| Headline | three_year_saidi_ending_2025 | 3 | 685 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | three_year_saidi_ending_2024 | 2 | 253 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | report_three_year_2025 | 2 | 249 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | report_three_year_2024 | 2 | 187 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | saifi_2025 | 2 | 243 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | saifi_2024 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | saifi_change_pct | 1 | 48 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | caidi_2025 | 2 | 201 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | caidi_2024 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | caidi_change_pct | 1 | 48 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | saidi_2025 | 2 | 245 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | storm_share_2025 | 2 | 247 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | storm_share_2024 | 1 | 48 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | customers_va_nc_thousand | 2 | 261 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | coop_corr_yoy | 2 | 323 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | dominion_saifi_change_2015_2025 | 1 | 48 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | coop_saifi_change_2015_2025 | 1 | 48 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | dominion_relative_to_coops_pct | 2 | 405 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | commercial_sales_index_2025 | 2 | 185 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | commercial_customers_index_2025 | 2 | 185 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | residential_sales_index_2025 | 2 | 185 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | heating_degree_days_2025 | 2 | 187 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | heating_degree_days_2024 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | cooling_degree_days_2025 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | cooling_degree_days_2024 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | data_centers_connected_2025 | 2 | 181 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | data_center_mw_connected_2025 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | data_center_gw_contracting | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | top50_peaks_since_2025 | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | expected_peak_growth_pct | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | mainfeeder_miles_hardened | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | winter_peak_mw | 2 | 211 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | summer_peak_mw | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | smart_meter_share | 2 | 209 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | time_varying_rate_share_pct | 2 | 233 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | demand_response_mw | 2 | 207 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | losses_pct | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Headline | tests_total | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | tests_passed | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | flagged_rows | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | storm_county_days_2025 | 2 | 249 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | predicted_2025_saidi_from_weather | 2 | 343 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Headline | corr_storm_days_vs_daytoday_saidi | 2 | 291 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | year | 13 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | commercial_twh | 13 | 0 | 1133 | 168 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | residential_twh | 13 | 0 | 1133 | 160 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | commercial_customers | 13 | 0 | 1133 | 176 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | residential_customers | 13 | 0 | 1133 | 184 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | commercial_sales_index | 13 | 144 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | commercial_customers_index | 13 | 144 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | residential_sales_index | 13 | 144 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | Column9 | 1 | 0 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| LoadGrowth | Source | 1 | 499 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Programmes2025 | utility | 6 | 315 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Programmes2025 | winter_peak_mw | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Programmes2025 | summer_peak_mw | 2 | 0 | 1133 | 152 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Programmes2025 | smart_meter_share | 6 | 0 | 1133 | 152 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Programmes2025 | time_varying_rate_share_pct | 6 | 0 | 1133 | 160 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Programmes2025 | demand_response_potential_mw | 6 | 0 | 1133 | 160 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| Programmes2025 | losses_pct | 6 | 0 | 1133 | 160 | 2026-10-22 19:23:10 | 2026-10-22 19:23:08 |
| SAIDI_WEATHER_ADJUSTED | YEAR | 1 | 0 | 0 | 152 | 2026-10-27 01:41:14 | 2026-10-27 01:38:33 |
| SAIDI_WEATHER_ADJUSTED | STORM_COUNTY_DAYS | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| SAIDI_WEATHER_ADJUSTED | SAIDI_EX_MED | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| SAIDI_WEATHER_ADJUSTED | PREDICTED_FROM_WEATHER | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| SAIDI_WEATHER_ADJUSTED | WEATHER_ADJUSTED_SAIDI | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| STORM_INDEX | YEAR | 13 | 0 | 1133 | 152 | 2026-10-21 05:53:34 | 2026-10-21 05:49:47 |
| STORM_INDEX | STORM_COUNTY_DAYS | 13 | 0 | 1133 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| STORM_INDEX | WIND_DAYS | 13 | 0 | 1133 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| STORM_INDEX | WINTER_DAYS | 13 | 0 | 1133 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| STORM_INDEX | TROPICAL_DAYS | 8 | 0 | 1133 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| STORM_INDEX | SEVERE_GUST_DAYS | 13 | 0 | 1133 | 160 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| Tests | test | 6 | 679 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Tests | rows_returned | 3 | 0 | 1133 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Tests | status | 2 | 159 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| Tests | note | 6 | 865 | 0 | 152 | 2026-10-22 19:23:08 | 2026-10-22 19:23:08 |
| V_GROUP_INDEX | PEER_GROUP | 7 | 433 | 0 | 184 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | YEAR | 13 | 0 | 1133 | 192 | 2026-10-27 07:47:11 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | UTILITIES | 21 | 0 | 1133 | 296 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | CUSTOMERS | 91 | 0 | 2157 | 512 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | SAIFI_EX_MED | 91 | 0 | 2157 | 512 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | SAIDI_EX_MED | 91 | 768 | 0 | 232 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_GROUP_INDEX | CAIDI_EX_MED | 91 | 768 | 0 | 232 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_STORM_VS_SAIDI | YEAR | 1 | 0 | 0 | 152 | 2026-10-22 06:58:38 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | STORM_COUNTY_DAYS | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | WIND_DAYS | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | WINTER_DAYS | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | TROPICAL_DAYS | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | SAIDI_EX_MED | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | SAIFI_EX_MED | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI | STORM_SAIDI | 1 | 0 | 0 | 152 | 2026-10-22 06:49:02 | 2026-10-22 06:49:02 |
| V_STORM_VS_SAIDI (2) | YEAR | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | STORM_COUNTY_DAYS | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | WIND_DAYS | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | WINTER_DAYS | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | TROPICAL_DAYS | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | SAIDI_EX_MED | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | SAIFI_EX_MED | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_STORM_VS_SAIDI (2) | STORM_SAIDI | 1 | 0 | 0 | 152 | 2026-10-27 01:38:33 | 2026-10-27 01:38:33 |
| V_TREND | UTILITY_KEY | 1283 | 15870 | 0 | 21104 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | UTILITY_NAME | 1210 | 29142 | 0 | 21104 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | PEER_GROUP | 7 | 433 | 0 | 384 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | YEAR | 13 | 144 | 0 | 2080 | 2026-10-21 05:53:34 | 2026-10-21 05:49:47 |
| V_TREND | STANDARD | 2 | 171 | 0 | 400 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIDI_EX_MED | 8963 | 0 | 134741 | 47000 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIFI_EX_MED | 2655 | 0 | 65645 | 21872 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | CAIDI_EX_MED | 9857 | 0 | 262709 | 43008 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIDI_ALL | 10685 | 0 | 262781 | 52528 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIFI_ALL | 3283 | 0 | 65645 | 24560 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | STORM_SAIDI | 7059 | 0 | 132405 | 34808 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | STORM_SAIFI | 1564 | 0 | 32885 | 16568 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | STORM_SHARE | 8399 | 0 | 134597 | 34800 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIDI_EX_MED_PY | 8067 | 0 | 133445 | 42048 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIFI_EX_MED_PY | 2521 | 0 | 65645 | 19384 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | CAIDI_EX_MED_PY | 8903 | 0 | 135645 | 38200 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIDI_YOY | 10214 | 81752 | 0 | 21096 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | FREQUENCY_SHARE_OF_CHANGE | 9281 | 74288 | 0 | 19176 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIDI_EX_MED_5YR | 10756 | 86088 | 0 | 23680 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |
| V_TREND | SAIFI_EX_MED_5YR | 6821 | 0 | 131765 | 43624 | 2026-10-21 05:49:47 | 2026-10-21 05:49:47 |


## Relationships

| FromTableName | FromColumnName | ToTableName | ToColumnName | IsActive | Cardinality | CrossFilteringBehavior | FromKeyCount | ToKeyCount | RelyOnReferentialIntegrity |
|---|---|---|---|---|---|---|---|---|---|
| FCT_RELIABILITY | UTILITY_KEY | DIM_UTILITY | UTILITY_KEY | 1 | M:1 | Single | 1286 | None | 0 |
| Headline | losses_pct | Programmes2025 | losses_pct | 1 | M:1 | Single | 4 | None | 0 |


## Measures (38)

| TableName | Name | Expression | DisplayFolder | Description |
|---|---|---|---|---|
| FCT_RELIABILITY | SAIDI ex MED | DIVIDE(SUM(FCT_RELIABILITY[CUST_MINUTES_EX_MED]), SUM(FCT_RELIABILITY[Customers Served])) | nan | nan |
| FCT_RELIABILITY | Outage Mins/Customer | CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025}) | nan | nan |
| FCT_RELIABILITY | Total Customers | SUM(FCT_RELIABILITY[Customers Served]) | nan | nan |
| FCT_RELIABILITY | Share of outage mins caused by major storms | DIVIDE(SUM(FCT_RELIABILITY[SAIDI_ALL]) - SUM(FCT_RELIABILITY[SAIDI_EX_MED]), SUM(FCT_RELIABILITY[SAIDI_ALL])) | nan | nan |
| FCT_RELIABILITY | SAIDI all events | DIVIDE(SUM(FCT_RELIABILITY[CUST_MINUTES_ALL]), [Total Customers]) | nan | nan |
| FCT_RELIABILITY | Storm SAIDI | [SAIDI all events] - [SAIDI ex MED] | nan | nan |
| V_GROUP_INDEX | SAIFI index 2015 | DIVIDE(SUM(V_GROUP_INDEX[SAIFI_EX_MED]), CALCULATE(SUM(V_GROUP_INDEX[SAIFI_EX_MED]), V_GROUP_INDEX[YEAR] = 2015)) * 100 | nan | nan |
| FCT_RELIABILITY | SAIDI 2015 to 2017 | CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2015, 2016, 2017}) | nan | nan |
| FCT_RELIABILITY | SAIDI 2023 to 2025 | CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025}) | nan | nan |
| FCT_RELIABILITY | SAIFI ex MED | DIVIDE(SUM(FCT_RELIABILITY[CUST_INTERRUPTIONS_EX_MED]), [Total Customers]) | nan | nan |
| FCT_RELIABILITY | CAIDI ex MED | DIVIDE([SAIDI ex MED], [SAIFI ex MED]) | nan | nan |
| FCT_RELIABILITY | SAIFI 5yr | CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIFI ex MED]), FCT_RELIABILITY[YEAR] IN {2021, 2022, 2023, 2024, 2025}) | nan | nan |
| FCT_RELIABILITY | CAIDI 5yr | CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [CAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2021, 2022, 2023, 2024, 2025}) | nan | nan |
| FCT_RELIABILITY | SAIDI change % | (DIVIDE([SAIDI 2023 to 2025], [SAIDI 2015 to 2017]) - 1) | nan | nan |
| FCT_RELIABILITY | Method | IF(DISTINCTCOUNT(FCT_RELIABILITY[STANDARD]) > 1, "Mixed", MAX(FCT_RELIABILITY[STANDARD])) | nan | nan |
| DIM_UTILITY | Bar colour | IF(SELECTEDVALUE(DIM_UTILITY[Display name]) = "Dominion Energy Virginia", "#0A66C2", "#B8BCC2") | nan | nan |
| Programmes2025 | Smart meter share % | SUM(Programmes2025[smart_meter_share]) * 100 | nan | nan |
| Programmes2025 | Time-varying rate % | SUM(Programmes2025[time_varying_rate_share_pct]) | nan | nan |
| DOM_LOAD_ANNUAL | Floor MW | SUM(DOM_LOAD_ANNUAL[FLOOR_MW]) | nan | nan |
| DOM_LOAD_ANNUAL | Peak MW | SUM(DOM_LOAD_ANNUAL[PEAK_MW]) | nan | nan |
| DOM_LOAD_ANNUAL | Winter peak MW | SUM(DOM_LOAD_ANNUAL[WINTER_PEAK_MW]) | nan | nan |
| DOM_LOAD_ANNUAL | Summer peak MW | SUM(DOM_LOAD_ANNUAL[SUMMER_PEAK_MW]) | nan | nan |
| DOM_LOAD_ANNUAL | Floor growth 2019 to 2025 | DIVIDE(CALCULATE([Floor MW], DOM_LOAD_ANNUAL[YEAR] = 2025), CALCULATE([Floor MW], DOM_LOAD_ANNUAL[YEAR] = 2019)) - 1 | nan | nan |
| DOM_LOAD_ANNUAL | Peak growth 2019 to 2025 | DIVIDE(CALCULATE([Peak MW], DOM_LOAD_ANNUAL[YEAR] = 2025), CALCULATE([Peak MW], DOM_LOAD_ANNUAL[YEAR] = 2019)) - 1 | nan | nan |
| DOM_TOP50_HOURS | Top 50 hours in 2025 | CALCULATE(COUNTROWS(DOM_TOP50_HOURS), DOM_TOP50_HOURS[RANK_END_2025] <= 50, DOM_TOP50_HOURS[YEAR] = 2025) | nan | nan |
| FCT_RELIABILITY | SAIFI label | IF(SELECTEDVALUE(FCT_RELIABILITY[YEAR]) IN {2019, 2023, 2025}, [SAIFI ex MED]) | nan | nan |
| FCT_RELIABILITY | CAIDI label | IF(SELECTEDVALUE(FCT_RELIABILITY[YEAR]) IN {2019, 2023, 2025}, [CAIDI ex MED]) | nan | nan |
| V_GROUP_INDEX | Index label | IF(SELECTEDVALUE(V_GROUP_INDEX[YEAR]) = 2025, [SAIFI index 2015]) | nan | nan |
| SAIDI_WEATHER_ADJUSTED | Adjusted label | IF(SELECTEDVALUE(SAIDI_WEATHER_ADJUSTED[YEAR]) IN {2015, 2019, 2025}, SUM(SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI])) | nan | nan |
| DIM_UTILITY | Row colour | IF(SELECTEDVALUE(DIM_UTILITY[Display name]) = "Dominion Energy Virginia", "#118DFF", "#FFFFFF") | nan | nan |
| LoadGrowth | Sales label | IF(SELECTEDVALUE(LoadGrowth[year]) = 2025, SUM(LoadGrowth[commercial_sales_index])) | nan | nan |
| DOM_LOAD_PROFILE | Hour colour |  VAR h = SELECTEDVALUE(DOM_LOAD_PROFILE[HOUR_NO]) RETURN SWITCH(TRUE(),     h <= 6 \|\| h >= 22, "#118DFF",     h >= 18,           "#B8BCC2",                        "#E8D166") | nan | nan |
| AmiEventStudy | Selected SAIDI |  VAR SelectedYear =     SELECTEDVALUE('Dashboard Year'[Year], 2025) RETURN     CALCULATE(         [SAIDI ex MED],         FCT_RELIABILITY[YEAR] = SelectedYear     )  | nan | nan |
| AmiEventStudy | Selected SAIFI |  VAR SelectedYear =     SELECTEDVALUE('Dashboard Year'[Year], 2025) RETURN     CALCULATE(         [SAIFI ex MED],         FCT_RELIABILITY[YEAR] = SelectedYear     )  | nan | nan |
| AmiEventStudy | Selected CAIDI |  VAR SelectedYear =     SELECTEDVALUE('Dashboard Year'[Year], 2025) RETURN     CALCULATE(         [CAIDI ex MED],         FCT_RELIABILITY[YEAR] = SelectedYear     )  | nan | nan |
| AmiEventStudy | Measure | nan | nan | nan |
| AmiEventStudy | Selected Customers |  VAR SelectedYear =     SELECTEDVALUE('Dashboard Year'[Year], 2025) RETURN     CALCULATE(         [Total Customers],         FCT_RELIABILITY[YEAR] = SelectedYear     )  | nan | nan |
| AmiEventStudy | Selected Major Event Share |  VAR SelectedYear =     SELECTEDVALUE('Dashboard Year'[Year], 2025) RETURN     CALCULATE(         DIVIDE(             [SAIDI all events] - [SAIDI ex MED],             [SAIDI all events]         ),         FCT_RELIABILITY[YEAR] = SelectedYear     )  | nan | nan |


## Calculated columns (4)

| TableName | ColumnName | Expression |
|---|---|---|
| DIM_UTILITY | Display name | SWITCH(DIM_UTILITY[UTILITY_KEY], "19876\|VA", "Dominion Energy Virginia", "17539\|SC", "Dominion Energy SC", "5416\|NC", "Duke Carolinas (NC)", "3046\|NC", "Duke Progress (NC)", "7140\|GA", "Georgia Power", "195\|AL", "Alabama Power", "6455\|FL", "Duke Energy Florida", "6452\|FL", "FPL", "1167\|MD",… |
| DIM_UTILITY | Short name |  SWITCH(DIM_UTILITY[Display name],     "Dominion Energy Virginia", "Dominion VA",     "Dominion Energy SC", "Dominion SC",     "Duke Carolinas (NC)", "Duke Carolinas",     "Duke Progress (NC)", "Duke Progress",     "Duke Energy Florida", "Duke FL",     "Georgia Power", "Georgia",     "Alabama Power"… |
| DIM_UTILITY | Quadrant name |  SWITCH(DIM_UTILITY[Display name],     "Dominion Energy Virginia", "Dominion VA",     "Duke Progress (NC)", "Duke Progress",     "Georgia Power", "Georgia",     "Duke Carolinas (NC)", "Duke Carolinas",     "") |
| DIM_UTILITY | Region | SWITCH(DIM_UTILITY[PEER_GROUP], "Southeast IOU peer", "Southeast", "Mid-Atlantic IOU peer", "Mid-Atlantic", "Florida IOU peer", "Florida", "Dominion Energy Virginia", "Virginia", DIM_UTILITY[PEER_GROUP]) |


## Power Query M (16)

### V_TREND

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    V_TREND_View = MART_Schema{[Name="V_TREND",Kind="View"]}[Data]
in
    V_TREND_View
```

### DIM_UTILITY

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    DIM_UTILITY_Table = MART_Schema{[Name="DIM_UTILITY",Kind="Table"]}[Data]
in
    DIM_UTILITY_Table
```

### FCT_RELIABILITY

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    FCT_RELIABILITY_Table = MART_Schema{[Name="FCT_RELIABILITY",Kind="Table"]}[Data],
    #"Renamed Columns" = Table.RenameColumns(FCT_RELIABILITY_Table,{{"CUSTOMERS", "Customers Served"}, {"SAIFI_EX_MED", "SAIFI_EX_MED"}, {"CAIDI_EX_MED", "CAIDI_EX_MED"}, {"SAIDI_ALL", "SAIDI_ALL"}})
in
    #"Renamed Columns"
```

### STORM_INDEX

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    STORM_INDEX_Table = MART_Schema{[Name="STORM_INDEX",Kind="Table"]}[Data]
in
    STORM_INDEX_Table
```

### V_GROUP_INDEX

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    V_GROUP_INDEX_View = MART_Schema{[Name="V_GROUP_INDEX",Kind="View"]}[Data]
in
    V_GROUP_INDEX_View
```

### V_STORM_VS_SAIDI

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    V_STORM_VS_SAIDI_View = MART_Schema{[Name="V_STORM_VS_SAIDI",Kind="View"]}[Data]
in
    V_STORM_VS_SAIDI_View
```

### LoadGrowth

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    LoadGrowth_Sheet = Source{[Item="LoadGrowth",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(LoadGrowth_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"year", Int64.Type}, {"commercial_twh", type number}, {"residential_twh", type number}, {"commercial_customers", Int64.Type}, {"residential_customers", Int64.Type}, {"commercial_sales_index", type number}, {"commercial_customers_index", type number}, {"residential_sales_index", type number}, {"Column9", type any}, {"Source", type text}})
in
    #"Changed Type"
```

### Programmes2025

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    Programmes2025_Sheet = Source{[Item="Programmes2025",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Programmes2025_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"utility", type text}, {"winter_peak_mw", Int64.Type}, {"summer_peak_mw", Int64.Type}, {"smart_meter_share", type number}, {"time_varying_rate_share_pct", type number}, {"demand_response_potential_mw", type number}, {"losses_pct", type number}})
in
    #"Changed Type"
```

### Headline

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    Headline_Sheet = Source{[Item="Headline",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Headline_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"three_year_saidi_ending_2025", type any}, {"three_year_saidi_ending_2024", type any}, {"report_three_year_2025", type any}, {"report_three_year_2024", type any}, {"saifi_2025", type any}, {"saifi_2024", type number}, {"saifi_change_pct", type number}, {"caidi_2025", type any}, {"caidi_2024", type number}, {"caidi_change_pct", type number}, {"saidi_2025", type any}, {"storm_share_2025", type any}, {"storm_share_2024", type number}, {"customers_va_nc_thousand", type any}, {"coop_corr_yoy", type any}, {"dominion_saifi_change_2015_2025", type number}, {"coop_saifi_change_2015_2025", type number}, {"dominion_relative_to_coops_pct", type any}, {"commercial_sales_index_2025", type any}, {"commercial_customers_index_2025", type any}, {"residential_sales_index_2025", type any}, {"heating_degree_days_2025", type any}, {"heating_degree_days_2024", Int64.Type}, {"cooling_degree_days_2025", Int64.Type}, {"cooling_degree_days_2024", Int64.Type}, {"data_centers_connected_2025", type any}, {"data_center_mw_connected_2025", Int64.Type}, {"data_center_gw_contracting", Int64.Type}, {"top50_peaks_since_2025", Int64.Type}, {"expected_peak_growth_pct", type number}, {"mainfeeder_miles_hardened", Int64.Type}, {"winter_peak_mw", type any}, {"summer_peak_mw", Int64.Type}, {"smart_meter_share", type any}, {"time_varying_rate_share_pct", type any}, {"demand_response_mw", type any}, {"losses_pct", type number}, {"tests_total", Int64.Type}, {"tests_passed", Int64.Type}, {"flagged_rows", Int64.Type}, {"storm_county_days_2025", type any}, {"predicted_2025_saidi_from_weather", type any}, {"corr_storm_days_vs_daytoday_saidi", type any}})
in
    #"Changed Type"
```

### AmiEventStudy

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    AmiEventStudy_Sheet = Source{[Item="AmiEventStudy",Kind="Sheet"]}[Data]
in
    AmiEventStudy_Sheet
```

### Tests

```powerquery
let
    Source = Excel.Workbook(File.Contents("C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx"), null, true),
    Tests_Sheet = Source{[Item="Tests",Kind="Sheet"]}[Data],
    #"Promoted Headers" = Table.PromoteHeaders(Tests_Sheet, [PromoteAllScalars=true]),
    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{"test", type text}, {"rows_returned", Int64.Type}, {"status", type text}, {"note", type text}})
in
    #"Changed Type"
```

### DOM_LOAD_ANNUAL

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    DOM_LOAD_ANNUAL_Table = MART_Schema{[Name="DOM_LOAD_ANNUAL",Kind="Table"]}[Data]
in
    DOM_LOAD_ANNUAL_Table
```

### DOM_TOP50_HOURS

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    DOM_TOP50_HOURS_Table = MART_Schema{[Name="DOM_TOP50_HOURS",Kind="Table"]}[Data]
in
    DOM_TOP50_HOURS_Table
```

### SAIDI_WEATHER_ADJUSTED

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    SAIDI_WEATHER_ADJUSTED_Table = MART_Schema{[Name="SAIDI_WEATHER_ADJUSTED",Kind="Table"]}[Data]
in
    SAIDI_WEATHER_ADJUSTED_Table
```

### V_STORM_VS_SAIDI (2)

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    V_STORM_VS_SAIDI_View = MART_Schema{[Name="V_STORM_VS_SAIDI",Kind="View"]}[Data]
in
    V_STORM_VS_SAIDI_View
```

### DOM_LOAD_PROFILE

```powerquery
let
    Source = Snowflake.Databases("vosrmgo-af46531.snowflakecomputing.com","SNOWFLAKE_LEARNING_WH",[Implementation="2.0"]),
    RELIABILITY_Database = Source{[Name="RELIABILITY",Kind="Database"]}[Data],
    MART_Schema = RELIABILITY_Database{[Name="MART",Kind="Schema"]}[Data],
    DOM_LOAD_PROFILE_Table = MART_Schema{[Name="DOM_LOAD_PROFILE",Kind="Table"]}[Data]
in
    DOM_LOAD_PROFILE_Table
```

## Columns (schema)

| TableName | ColumnName | PandasDataType |
|---|---|---|
| AmiEventStudy | Column1 | string |
| AmiEventStudy | Column2 | string |
| AmiEventStudy | Column3 | string |
| AmiEventStudy | Column4 | string |
| DIM_UTILITY | UTILITY_ID | Float64 |
| DIM_UTILITY | STATE | string |
| DIM_UTILITY | UTILITY_KEY | string |
| DIM_UTILITY | UTILITY_NAME | string |
| DIM_UTILITY | ENTITY_TYPE | string |
| DIM_UTILITY | PEER_GROUP | string |
| DIM_UTILITY | Display name | string |
| DIM_UTILITY | Short name | string |
| DIM_UTILITY | Quadrant name | string |
| DIM_UTILITY | Region | string |
| DOM_LOAD_ANNUAL | YEAR | Float64 |
| DOM_LOAD_ANNUAL | WINTER_PEAK_MW | Float64 |
| DOM_LOAD_ANNUAL | SUMMER_PEAK_MW | Float64 |
| DOM_LOAD_ANNUAL | PEAK_MW | Float64 |
| DOM_LOAD_ANNUAL | FLOOR_MW | Float64 |
| DOM_LOAD_ANNUAL | MEDIAN_MW | Float64 |
| DOM_LOAD_ANNUAL | AVG_MW | Float64 |
| DOM_LOAD_ANNUAL | ENERGY_TWH | Float64 |
| DOM_LOAD_ANNUAL | HOURS_REPORTED | Float64 |
| DOM_LOAD_ANNUAL | HOURS_MISSING | Float64 |
| DOM_LOAD_PROFILE | HOUR_NO | Float64 |
| DOM_LOAD_PROFILE | AVG_MW_2019 | Float64 |
| DOM_LOAD_PROFILE | AVG_MW_2025 | Float64 |
| DOM_LOAD_PROFILE | GROWTH_PCT | Float64 |
| DOM_TOP50_HOURS | YEAR | Float64 |
| DOM_TOP50_HOURS | DATA_DATE | datetime64[ns] |
| DOM_TOP50_HOURS | HOUR_NO | Float64 |
| DOM_TOP50_HOURS | UTC_TS | datetime64[ns] |
| DOM_TOP50_HOURS | DEMAND_MW | Float64 |
| DOM_TOP50_HOURS | RANK_TODAY | Float64 |
| DOM_TOP50_HOURS | RANK_END_2025 | Float64 |
| Dashboard Year | Year | Int64 |
| FCT_RELIABILITY | UTILITY_KEY | string |
| FCT_RELIABILITY | UTILITY_ID | Float64 |
| FCT_RELIABILITY | STATE | string |
| FCT_RELIABILITY | YEAR | Float64 |
| FCT_RELIABILITY | STANDARD | string |
| FCT_RELIABILITY | SOURCE | string |
| FCT_RELIABILITY | Customers Served | Float64 |
| FCT_RELIABILITY | SAIDI_ALL | Float64 |
| FCT_RELIABILITY | SAIFI_ALL | Float64 |
| FCT_RELIABILITY | CAIDI_ALL | Float64 |
| FCT_RELIABILITY | SAIDI_EX_MED | Float64 |
| FCT_RELIABILITY | SAIFI_EX_MED | Float64 |
| FCT_RELIABILITY | CAIDI_EX_MED | Float64 |
| FCT_RELIABILITY | STORM_SAIDI | Float64 |
| FCT_RELIABILITY | STORM_SAIFI | Float64 |
| FCT_RELIABILITY | CUST_MINUTES_ALL | Float64 |
| FCT_RELIABILITY | CUST_MINUTES_EX_MED | Float64 |
| FCT_RELIABILITY | CUST_INTERRUPTIONS_ALL | Float64 |
| FCT_RELIABILITY | CUST_INTERRUPTIONS_EX_MED | Float64 |
| FCT_RELIABILITY | MAX_KV | Float64 |
| FCT_RELIABILITY | AUTO_RECORDED | bool |
| FCT_RELIABILITY | MOMENTARY_DEF | string |
| FCT_RELIABILITY | INACTIVE_INCLUDED | bool |
| Headline | three_year_saidi_ending_2025 | string |
| Headline | three_year_saidi_ending_2024 | string |
| Headline | report_three_year_2025 | string |
| Headline | report_three_year_2024 | string |
| Headline | saifi_2025 | string |
| Headline | saifi_2024 | Float64 |
| Headline | saifi_change_pct | Float64 |
| Headline | caidi_2025 | string |
| Headline | caidi_2024 | Float64 |
| Headline | caidi_change_pct | Float64 |
| Headline | saidi_2025 | string |
| Headline | storm_share_2025 | string |
| Headline | storm_share_2024 | Float64 |
| Headline | customers_va_nc_thousand | string |
| Headline | coop_corr_yoy | string |
| Headline | dominion_saifi_change_2015_2025 | Float64 |
| Headline | coop_saifi_change_2015_2025 | Float64 |
| Headline | dominion_relative_to_coops_pct | string |
| Headline | commercial_sales_index_2025 | string |
| Headline | commercial_customers_index_2025 | string |
| Headline | residential_sales_index_2025 | string |
| Headline | heating_degree_days_2025 | string |
| Headline | heating_degree_days_2024 | Int64 |
| Headline | cooling_degree_days_2025 | Int64 |
| Headline | cooling_degree_days_2024 | Int64 |
| Headline | data_centers_connected_2025 | string |
| Headline | data_center_mw_connected_2025 | Int64 |
| Headline | data_center_gw_contracting | Int64 |
| Headline | top50_peaks_since_2025 | Int64 |
| Headline | expected_peak_growth_pct | Float64 |
| Headline | mainfeeder_miles_hardened | Int64 |
| Headline | winter_peak_mw | string |
| Headline | summer_peak_mw | Int64 |
| Headline | smart_meter_share | string |
| Headline | time_varying_rate_share_pct | string |
| Headline | demand_response_mw | string |
| Headline | losses_pct | Float64 |
| Headline | tests_total | Int64 |
| Headline | tests_passed | Int64 |
| Headline | flagged_rows | Int64 |
| Headline | storm_county_days_2025 | string |
| Headline | predicted_2025_saidi_from_weather | string |
| Headline | corr_storm_days_vs_daytoday_saidi | string |
| LoadGrowth | year | Int64 |
| LoadGrowth | commercial_twh | Float64 |
| LoadGrowth | residential_twh | Float64 |
| LoadGrowth | commercial_customers | Int64 |
| LoadGrowth | residential_customers | Int64 |
| LoadGrowth | commercial_sales_index | Float64 |
| LoadGrowth | commercial_customers_index | Float64 |
| LoadGrowth | residential_sales_index | Float64 |
| LoadGrowth | Column9 | string |
| LoadGrowth | Source | string |
| Programmes2025 | utility | string |
| Programmes2025 | winter_peak_mw | Int64 |
| Programmes2025 | summer_peak_mw | Int64 |
| Programmes2025 | smart_meter_share | Float64 |
| Programmes2025 | time_varying_rate_share_pct | Float64 |
| Programmes2025 | demand_response_potential_mw | Float64 |
| Programmes2025 | losses_pct | Float64 |
| SAIDI_WEATHER_ADJUSTED | YEAR | Float64 |
| SAIDI_WEATHER_ADJUSTED | STORM_COUNTY_DAYS | Float64 |
| SAIDI_WEATHER_ADJUSTED | SAIDI_EX_MED | Float64 |
| SAIDI_WEATHER_ADJUSTED | PREDICTED_FROM_WEATHER | Float64 |
| SAIDI_WEATHER_ADJUSTED | WEATHER_ADJUSTED_SAIDI | Float64 |
| STORM_INDEX | YEAR | Float64 |
| STORM_INDEX | STORM_COUNTY_DAYS | Float64 |
| STORM_INDEX | WIND_DAYS | Float64 |
| STORM_INDEX | WINTER_DAYS | Float64 |
| STORM_INDEX | TROPICAL_DAYS | Float64 |
| STORM_INDEX | SEVERE_GUST_DAYS | Float64 |
| Tests | test | string |
| Tests | rows_returned | Int64 |
| Tests | status | string |
| Tests | note | string |
| V_GROUP_INDEX | PEER_GROUP | string |
| V_GROUP_INDEX | YEAR | Float64 |
| V_GROUP_INDEX | UTILITIES | Float64 |
| V_GROUP_INDEX | CUSTOMERS | Float64 |
| V_GROUP_INDEX | SAIFI_EX_MED | Float64 |
| V_GROUP_INDEX | SAIDI_EX_MED | Float64 |
| V_GROUP_INDEX | CAIDI_EX_MED | Float64 |
| V_STORM_VS_SAIDI | YEAR | Float64 |
| V_STORM_VS_SAIDI | STORM_COUNTY_DAYS | Float64 |
| V_STORM_VS_SAIDI | WIND_DAYS | Float64 |
| V_STORM_VS_SAIDI | WINTER_DAYS | Float64 |
| V_STORM_VS_SAIDI | TROPICAL_DAYS | Float64 |
| V_STORM_VS_SAIDI | SAIDI_EX_MED | Float64 |
| V_STORM_VS_SAIDI | SAIFI_EX_MED | Float64 |
| V_STORM_VS_SAIDI | STORM_SAIDI | Float64 |
| V_STORM_VS_SAIDI (2) | YEAR | Float64 |
| V_STORM_VS_SAIDI (2) | STORM_COUNTY_DAYS | Float64 |
| V_STORM_VS_SAIDI (2) | WIND_DAYS | Float64 |
| V_STORM_VS_SAIDI (2) | WINTER_DAYS | Float64 |
| V_STORM_VS_SAIDI (2) | TROPICAL_DAYS | Float64 |
| V_STORM_VS_SAIDI (2) | SAIDI_EX_MED | Float64 |
| V_STORM_VS_SAIDI (2) | SAIFI_EX_MED | Float64 |
| V_STORM_VS_SAIDI (2) | STORM_SAIDI | Float64 |
| V_TREND | UTILITY_KEY | string |
| V_TREND | UTILITY_NAME | string |
| V_TREND | PEER_GROUP | string |
| V_TREND | YEAR | Float64 |
| V_TREND | STANDARD | string |
| V_TREND | SAIDI_EX_MED | Float64 |
| V_TREND | SAIFI_EX_MED | Float64 |
| V_TREND | CAIDI_EX_MED | Float64 |
| V_TREND | SAIDI_ALL | Float64 |
| V_TREND | SAIFI_ALL | Float64 |
| V_TREND | STORM_SAIDI | Float64 |
| V_TREND | STORM_SAIFI | Float64 |
| V_TREND | STORM_SHARE | Float64 |
| V_TREND | SAIDI_EX_MED_PY | Float64 |
| V_TREND | SAIFI_EX_MED_PY | Float64 |
| V_TREND | CAIDI_EX_MED_PY | Float64 |
| V_TREND | SAIDI_YOY | Float64 |
| V_TREND | FREQUENCY_SHARE_OF_CHANGE | Float64 |
| V_TREND | SAIDI_EX_MED_5YR | Float64 |
| V_TREND | SAIFI_EX_MED_5YR | Float64 |

