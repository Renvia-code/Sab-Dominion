# 02. Data dictionary

> **At a glance:** Quick read: RAW preserves imported records, STG standardizes them, and MART holds calculated metrics ready for analysis. For Dominion Virginia, the utility key is 19876|VA.

Database `RELIABILITY`, three schemas.

| Schema | Rule | Who writes | Who reads |
|---|---|---|---|
| `RAW` | Every column `VARCHAR`. One table per source file, loaded by `COPY INTO`. Not modified after load. | load scripts | `STG` |
| `STG` | Views. Typing (`TRY_TO_NUMBER`, `TRY_TO_DATE`), separator removal, unpivot, de-duplication. No business logic. | `01`, `05`, `06` | `MART` |
| `MART` | Tables and views with the business logic: keys, peer groups, additive numerators, indexes, fits. | `02`, `05`, `06`, `07` | Power BI (`BI_READER`), analysts |

Grain is stated for each object. A utility is identified by `utility_key = utility_id || '|' || state`. EIA reports one row per utility per state, so a utility operating in two states is two reporting units.

## RAW

### `RAW.EIA861_RELIABILITY_2025` (977 rows, one per utility-state, 2025)
Sheet `Reliability_States` of EIA's `Reliability_2025.xlsx`. The sheet has two blocks side by side: utilities that report under IEEE 1366 fill the `ieee_*` columns, utilities with their own major-event rule fill the `oth_*` columns.

| Column | Meaning |
|---|---|
| `data_year`, `utility_number`, `utility_name`, `state`, `ownership` | Identity. `ownership` is EIA's entity type (Investor Owned, Cooperative, Municipal, ...) |
| `ieee_saidi_all`, `ieee_saifi_all`, `ieee_caidi_all` | All events, IEEE 1366 filers |
| `ieee_saidi_ex_med`, `ieee_saifi_ex_med`, `ieee_caidi_ex_med` | Excluding major event days (IEEE 1366 2.5 beta method) |
| `ieee_saidi_los`, `ieee_saifi_los`, `ieee_caidi_los` | Excluding loss-of-supply events |
| `ieee_customers`, `ieee_max_kv`, `ieee_auto_recorded` | Customers served, highest distribution voltage, whether outages are logged automatically (OMS) |
| `oth_saidi_all` ... `oth_caidi_ex_med` | Same six metrics for utilities using their own storm rule |
| `oth_customers`, `oth_inactive_included`, `oth_momentary_def`, `oth_max_kv`, `oth_auto_recorded` | Same, plus the definition of a momentary interruption the utility applies |

Blanks are ".", numbers carry thousands separators. Three header rows.

### `RAW.PUDL_RELIABILITY` (24,358 rows, utility-state-year-standard, 2013 to 2024)
PUDL's cleaned long form of the same sheet across years. `standard` is `ieee_standard` or `other_standard`; both rows exist even when one is empty. `saidi_w_med` = with major event days (all events), `saidi_wo_med` = without. `data_maturity` is PUDL's flag (`final`, `provisional`).

### `RAW.PUDL_AMI` (127,720 rows, utility-state-year-customer class)
Meter counts: `advanced_metering_infrastructure` (smart meters), `automated_meter_reading` (one-way AMR), `non_amr_ami` (standard meters), `energy_served_ami_mwh`, `direct_load_control_customers`, `daily_digital_access_customers`, `home_area_network`.

### `RAW.PUDL_SALES` (198,770 rows, utility-state-year-class-service type)
`sales_mwh`, `customers`, `sales_revenue` by `customer_class` (residential, commercial, industrial, transportation, total) and `service_type` (bundled, delivery, energy).

### `RAW.NOAA_STORM_EVENTS` (831,288 rows, one per event, 2013 to 2025)
51 columns as published. Used: `state`, `year`, `event_type`, `cz_type` (`C` county, `Z` forecast zone), `cz_fips`, `cz_name`, `begin_yearmonth`, `begin_day`, `magnitude` (wind in knots for Thunderstorm Wind), `episode_id`, `event_id`.

### `RAW.NOAA_ZONE_COUNTY` (7,087 rows, zone-county)
NWS lookup: `state`, `zone`, `county_name`, `fips`. A forecast zone can span several counties.

### `RAW.EIA861_SERVICE_TERRITORY_2025` (11,803 rows, utility-state-county)
Which counties each utility serves. `utility_number`, `state`, `county`.

### `RAW.EIA930_SUBREGION` (6,077,232 rows, BA-subregion-hour, July 2018 to October 2026)
`balancing_authority`, `sub_region`, `data_date`, `hour_number` (1 to 24, hour ending), `demand_mw`, `local_time_end`, `utc_time_end`.

## STG

| View | Grain | What it does |
|---|---|---|
| `STG.RELIABILITY_2025` | utility-state-year (2025) | Unpivots the IEEE and Other blocks into one shape with a `standard` column. Types every metric as `NUMBER(12,3)`. |
| `STG.RELIABILITY_HIST` | utility-state-year (2013 to 2024) | Types PUDL, maps `ieee_standard` -> `IEEE 1366`, `other_standard` -> `Other`. Drops rows with no SAIDI at all. |
| `STG.RELIABILITY` | utility-state-year | Union of the two. Seven small utilities filed both standards in 2021: keep the IEEE row (`QUALIFY ROW_NUMBER() ... = 1`) so customers are not double counted. |
| `STG.AMI` | utility-state-year | Sums meter counts across classes, computes `ami_share`. |
| `STG.SALES` | utility-state-year-class-service type | Typed sales, customers, revenue. |
| `STG.DOMINION_VA_COUNTIES` | county | The 104 Virginia counties and cities Dominion serves, as 5-digit FIPS. EIA writes "Alexandria City", NOAA writes "City of Alexandria", both spellings are tried. |
| `STG.NOAA_VA_EVENTS` | event x county | Virginia events with a county FIPS: county events directly, zone events through the zone lookup, then a second pass on county name for zones renumbered since the lookup was built. Adds `line_risk` (wind, winter, tropical, other). |
| `STG.EIA930_DOM_HOURLY` | hour (72,864) | PJM / DOM only. `utc_ts` for the hour, `demand_mw_reported` as filed, `demand_mw` with values above 60,000 set to NULL. |

Common typed columns in `STG.RELIABILITY`:

| Column | Type | Unit | Meaning |
|---|---|---|---|
| `year` | NUMBER | | Data year |
| `utility_id`, `state`, `utility_name`, `entity_type` | | | Identity |
| `standard` | VARCHAR | | `IEEE 1366` or `Other` |
| `saidi_all`, `saidi_ex_med` | NUMBER(12,3) | minutes per customer per year | System Average Interruption Duration Index, all events / excluding major event days |
| `saifi_all`, `saifi_ex_med` | NUMBER(12,3) | interruptions per customer per year | System Average Interruption Frequency Index |
| `caidi_all`, `caidi_ex_med` | NUMBER(12,3) | minutes per interruption | Customer Average Interruption Duration Index = SAIDI / SAIFI |
| `saidi_all_minus_los` | NUMBER(12,3) | minutes | All events less loss-of-supply, IEEE filers only |
| `customers` | NUMBER | count | Customers served, the denominator of every ratio |
| `max_kv` | NUMBER(6,1) | kV | Highest distribution voltage included |
| `auto_recorded` | BOOLEAN | | Outages recorded automatically |
| `momentary_def` | VARCHAR | | Utility's definition of momentary (Other filers) |
| `inactive_included` | BOOLEAN | | Inactive accounts counted in customers |
| `source` | VARCHAR | | `EIA-861 final 2025` or `PUDL (EIA-861) 2013-2024` |

## MART

### `MART.DIM_UTILITY` (one row per utility_key)
`utility_id`, `state`, `utility_key`, `utility_name` (latest filed), `entity_type`, `peer_group`. Peer groups are assigned by ID rather than by name and are listed in `docs/04_decisions.md` D10:

| peer_group | Members |
|---|---|
| Dominion Energy Virginia | 19876-VA |
| Virginia co-op | every Virginia utility with entity type Cooperative |
| Appalachian Power (VA) | 733-VA, kept separate because its mountain terrain makes it an outlier |
| Southeast IOU peer | Duke Carolinas 5416-NC, Duke Progress 3046-NC, Georgia Power 7140-GA, Alabama Power 195-AL, Dominion SC 17539-SC |
| Mid-Atlantic IOU peer | BGE 1167-MD, Pepco 15270-MD, PECO 14940-PA, PPL 14715-PA |
| Florida IOU peer | FPL 6452-FL, Duke Energy Florida 6455-FL |
| Other | all remaining reporting units (about 950) |

### `MART.FCT_RELIABILITY` (13,095 rows, utility_key x year, 2013 to 2025)
All columns of `STG.RELIABILITY` plus the additive numerators used for aggregation:

| Column | Formula | Purpose |
|---|---|---|
| `storm_saidi`, `storm_saifi` | all - ex_med | Minutes and interruptions attributable to major event days |
| `cust_minutes_all`, `cust_minutes_ex_med` | SAIDI x customers | Total customer-minutes. Summed across utilities or years and divided by summed customers. |
| `cust_interruptions_all`, `cust_interruptions_ex_med` | SAIFI x customers | Total customer-interruptions, aggregated the same way |

### `MART.V_TREND` (view, utility_key x year)
Adds prior-year values (`*_py`), `saidi_yoy`, `storm_share`, five-year rolling averages and `frequency_share_of_change` = ln(SAIFI ratio) / ln(SAIDI ratio), the share of a SAIDI change attributable to frequency. Arguments to `LN` are guarded with `NULLIF` because Snowflake raises an error on `LN(0)` and some utilities report zero.

### `MART.V_GROUP_INDEX` (view, peer_group x year)
Customer-weighted SAIFI, SAIDI, CAIDI for each peer group: `SUM(cust_interruptions_ex_med) / SUM(customers of utilities that reported it)`. Used for the co-op benchmark. See `docs/03` P18 on the denominator.

### `MART.V_VA_COOP_PANEL` (view, created in `03_analysis.sql`)
Balanced panel of Virginia co-ops with at least 10,000 customers that filed in every year 2015 to 2025 (seven utilities). Used in Q3 as a robustness check. The report uses the all-co-op group from `V_GROUP_INDEX`.

### `MART.STORM_INDEX` (13 rows, year)
| Column | Meaning |
|---|---|
| `storm_county_days` | Count of (county, date) pairs in Dominion's Virginia counties with at least one wind, winter or tropical event. Multiple reports in one county on one day count once. |
| `wind_days`, `winter_days`, `tropical_days` | Same, by event family |
| `severe_gust_days` | County-days with a Thunderstorm Wind gust of 60 knots or more |

### `MART.V_STORM_VS_SAIDI` (view, year)
`STORM_INDEX` joined to Dominion's rows in `FCT_RELIABILITY`: adds `saidi_ex_med`, `saifi_ex_med`, `storm_saidi`. Source for the scatter chart and the weather fit.

### `MART.SAIDI_WEATHER_ADJUSTED` (11 rows, year 2015 to 2025)
| Column | Meaning |
|---|---|
| `predicted_from_weather` | intercept + slope x storm_county_days, fitted on 2015 to 2024 (intercept 104.4, slope 0.0514 minutes per county-day) |
| `weather_adjusted_saidi` | actual - predicted + mean(2015 to 2024). The year's SAIDI at average weather exposure |

### `MART.DOM_LOAD_ANNUAL` (9 rows, year 2018 to 2026)
`winter_peak_mw` (Dec, Jan, Feb of the calendar year), `summer_peak_mw` (Jun to Aug), `peak_mw`, `floor_mw` (lowest hour), `median_mw`, `avg_mw`, `energy_twh`, `hours_reported`, `hours_missing`. 2018 is July onward and 2026 is year to date.

### `MART.DOM_TOP50_HOURS` (96 rows)
The fifty highest-demand hours ranked at two reference dates: `rank_end_2025` (record to 31 December 2025, comparable with the annual report) and `rank_today`. A row is included if it is in either top fifty.

### `MART.DOM_LOAD_PROFILE` (24 rows, hour of day)
`avg_mw_2019`, `avg_mw_2025`, `growth_pct` for each hour ending 1 to 24.

### Added in November 2026 (sql/09 to 11; sources S12 to S20 in `01_sources.md`)

RAW tables, all VARCHAR as before: `EAGLEI_OUTAGES_VA` (11,608,442 rows, county x 15 minutes, with `source_file`), `EAGLEI_MCC`, `EAGLEI_COVERAGE_HISTORY`, `CENSUS_VA_COUNTY` (133), `HURDAT2_POINTS` (55,524), `DOE417_EVENTS` (3,702), `CPC_DEGREE_DAYS` (309,504). Staging views: `VA_COUNTY_CUSTOMERS` (customer basis, D15), `EAGLEI_VA_15MIN` (one row per county and slot; `customers_out` NULL for failed runs and impossible readings, `customers_out_reported` as published, D16), `EIA861_VA_COUNTY_UTILITY`, `HURDAT2_POINTS` (with `km_from_richmond`), `DOE417_EVENTS` (with `virginia_row`, `dominion_area`, D19), `VA_DEGREE_DAYS`.

| Table | Grain, rows | Key columns |
|---|---|---|
| `MART.DIM_COUNTY` | county, 133 | `county_fips`, `county_label`, `customers_basis` and `customers_basis_source`, `dominion_county`, `dominion_only_county`, `dominion_county_rule`, `dominion_county_reason` |
| `MART.FCT_OUTAGE_COUNTY_HOUR` | county x hour, all Virginia | `customers_out_max`, `customer_hours` (sum of 15-minute counts x 0.25), `readings`, `failed_readings` |
| `MART.FCT_TERRITORY_15MIN` | 15 minutes, Nov 2014 to 2025 | `customers_out` in the 103 Dominion counties, `counties_with_value`, `counties_failed` |
| `MART.FCT_COUNTY_DAY` | county x day (EST), 103 x 4,018 | `customer_hours`, `customer_hours_per_1k`, `customers_out_max`, `failed_readings`, NOAA flags `storm_day`, `storm_wind`, `storm_winter`, `storm_tropical`, `max_gust_kt` |
| `MART.FCT_TERRITORY_DAY` | day, 4,018 | `customer_hours`, `customers_out_max`, `alpha`, `beta`, `med_threshold_customer_hours`, `is_med_proxy` (D18) |
| `MART.FCT_COUNTY_YEAR` | county x year, 103 x 11 | `outage_minutes_per_customer` (all days and `_non_med`), `events`, `events_non_med`, `events_non_med_per_10k_customers`, `storm_days`, `failed_share` |
| `MART.FCT_OUTAGE_EVENT` | event, 486 territory + 41,278 county | `scope`, `start_utc`, `peak_utc`, `end_utc`, `peak_customers_out`, `peak_sustained_1h`, `hours_above_threshold`, `customer_hours`, `background_customers_out`, `hours_to_50pct`, `hours_to_90pct`, `hours_to_99pct`, `starts_on_med_proxy_day` (D17) |
| `MART.FCT_RESTORATION_CURVE` | territory event x hour since peak (0 to 167), events peaking at 50,000+ | `customers_out` (hourly max), `share_restored` (0 at the peak, 1 back to background) |
| `MART.FCT_EVENT_CONTEXT` | territory event, 486 | the event columns plus `storm_type`, county-days by storm type, `tropical_cyclone` (HURDAT2 within 400 km of Richmond), `doe417_customers_max`, `size_ratio` |
| `MART.DOM_LOAD_HOUR_MONTH` | year x month x hour, 2,400 | `avg_mw`, `max_mw`, `hours_reported` (to 29 Oct 2026, D21) |
| `MART.DOM_SEASONAL_PEAK` | year x season, 18 | `peak_mw`, `peak_date`, `peak_hour_no` |
| `MART.DOM_LOAD_DAILY` | day, 3,044 | `avg_mw`, `max_mw`, `min_mw`, `hours_reported`, `hdd`, `cdd` (Virginia, population-weighted) |
| `MART.FCT_SALES_SECTOR` | year x class, 52 | `sales_mwh` (bundled + delivery), `customers`, `revenue_usd`, `mwh_per_customer`, `delivery_only_mwh` |

The CSV copies of these tables for the Power BI Import are listed in `data/README.md`.

## Naming conventions

- Tables and views upper case, columns lower case snake case, as Snowflake displays them.
- `V_` prefix for views in MART, none in STG (everything in STG is a view).
- `_ex_med` = excluding major event days, `_all` = all events. `adjusted` refers only to the weather fit.
- `customers` is a count of customers. `saidi_*` is minutes per customer.
