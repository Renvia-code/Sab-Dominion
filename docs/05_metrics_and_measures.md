# 05. Metrics and measures

> **At a glance:** Quick read: SAIDI is outage minutes per customer, SAIFI is interruptions per customer, and CAIDI is average minutes per customer-interruption. SAIDI = SAIFI x CAIDI. The recent increase is more frequency-driven.

Definitions of the reliability indices and the calculation behind each figure on the report. DAX for all measures is in `powerbi/measures.dax`.

## Reliability indices

Each index is derived from two annual totals reported by the utility, customer-interruptions and customer-minutes of interruption, divided by customers served.

| Index | Name used on the report | Formula | Unit | Measures |
|---|---|---|---|---|
| SAIFI | Outages per customer | customer-interruptions / customers | interruptions per customer per year | Frequency of interruption |
| SAIDI | Outage minutes per customer | customer-minutes / customers | minutes per customer per year | Total interruption time per customer |
| CAIDI | Minutes to restore each outage | SAIDI / SAIFI | minutes per interruption | Average duration of an interruption |

SAIDI = SAIFI x CAIDI by definition (test T2 checks the identity in the data). A change in SAIDI therefore decomposes into a frequency component and a duration component:

ln(SAIDI2 / SAIDI1) = ln(SAIFI2 / SAIFI1) + ln(CAIDI2 / CAIDI1)

The share of a SAIDI change attributable to frequency is ln(SAIFI ratio) / ln(SAIDI ratio). This is `V_TREND.frequency_share_of_change` and the `Frequency share` measures.

## Major event days

Each index is reported in two forms:

- All events.
- Excluding major event days (ex-MED): days classified as major events are removed. Regulatory reporting and the annual report use this form.

IEEE Standard 1366 defines a major event day statistically (a day whose SAIDI exceeds a threshold derived from the previous five years, the 2.5 beta method). Dominion, Alabama Power and some other utilities apply their own definition and file under EIA's "Other" standard. The report shows the method beside each peer figure.

**Major-event-day exclusion share** = (SAIDI all - SAIDI ex-MED) / SAIDI all. The existing SQL/DAX field names `storm_share` and `storm_saidi` are legacy labels: this difference is **not** an independent NOAA attribution of storm-caused outage minutes. For Dominion in 2025: (306.7 - 144.4) / 306.7 = 53%.

## Aggregation rule

Ratios are not averaged. Numerators and denominators are summed separately and divided once.

| Not used | Used |
|---|---|
| `AVERAGE(saidi_ex_med)` across utilities | `SUM(cust_minutes_ex_med) / SUM(customers)` |
| `AVERAGE(saidi_ex_med)` across years for one utility | `AVERAGEX(VALUES(year), [SAIDI ex MED])`: the customer-weighted value for each year, then the mean of the years |

## Report figures

### Scorecard

| Card | Value | Measure | Calculation |
|---|---|---|---|
| Outage minutes per customer, 3-year average 2023 to 2025 | 133.0 | `SAIDI 3yr ending 2025` | Customer-weighted SAIDI ex-MED for each of 2023, 2024, 2025, then the mean. Annual report page 10: 133 |
| 3-year average 2022 to 2024 | 130.2 | `SAIDI 3yr ending 2024` | Same for 2022 to 2024. Report: 130 |
| Customers served, 2025 | 2,675,735 | `Total Customers` filtered to 2025 | EIA `oth_customers`. Virginia only. The annual report's 2,809k includes North Carolina |
| Outages per customer, 2025 | 1.32 | `SAIFI ex MED` | 2025 row |
| Minutes to restore each outage, 2025 | 109.4 | `CAIDI ex MED` | SAIDI / SAIFI |
| Including major storms, 2025 | 306.7 | `SAIDI all events` | 2025 row |
| Storm share, 2025 | 53% | `Storm share` | (306.7 - 144.4) / 306.7 |

### What moved

| Figure | Value | Calculation |
|---|---|---|
| SAIFI 2019 -> 2025 | 1.24 -> 1.32, about +6% | `SAIFI change 2019 to 2025` |
| CAIDI 2019 -> 2025 | 120.5 -> 109.4, -9% | `CAIDI change 2019 to 2025` |
| SAIDI 2019 -> 2023 | -17.7%, 34% of it from frequency, 66% from duration | `SAIDI change 2019 to 2023`, `Frequency share 2019 to 2023` |
| SAIDI 2023 -> 2025 | +17.1%, 79% from frequency | same pair for 2023 to 2025 |
| Dashed lines at 2015 and 2020 | | 2015: outages recorded automatically from this year. 2020: lines up to 46 kV included from this year. Both are changes in what is counted |

### Weather

| Figure | Value | Calculation |
|---|---|---|
| Storm county-days, 2025 | 791 | `STORM_INDEX` (D22). Second-highest in the record; 2019 was 848 |
| Correlation, storm days vs SAIDI ex-MED, 2015 to 2024 | 0.70 | `CORR()` in `05_noaa_storms.sql` Q6b. With SAIFI: 0.41. With major-storm minutes: 0.47 |
| Predicted from weather, 2025 | 145.3 | `REGR_INTERCEPT + REGR_SLOPE x 791`, fitted 2015 to 2024 |
| Actual 2025 | 144.4 | EIA |
| Weather-adjusted SAIDI | 2015: 122, 2019: 136, 2025: 133 | actual - predicted + mean(2015 to 2024) |
| Ten-year average line | 134 | mean of actual SAIDI ex-MED, 2015 to 2024 |
| Co-op index 2025 | 137 | all Virginia co-ops, customer-weighted SAIFI ex-MED, / 2015 value x 100 |
| Dominion index 2025 | 114 | same for Dominion VA |

### Fair comparison

| Figure | Calculation |
|---|---|
| Minutes 2015 to 17, Minutes 2023 to 25 | `SAIDI 2015 to 2017`, `SAIDI 2023 to 2025`: three-year customer-weighted averages per utility |
| Change | Minutes 2023 to 25 / Minutes 2015 to 17 - 1 |
| Outages per customer 2021 to 25, Minutes per outage 2021 to 25 | `SAIFI 5yr`, `CAIDI 5yr`: five-year averages |
| Quadrant lines | medians of the twelve peers: SAIFI 0.96, CAIDI 105 |
| Major-storm rule | `IEEE 1366`, `Own rule` (EIA "Other"), `Changed` (filed under both across years) |

### Growth

| Figure | Value | Calculation |
|---|---|---|
| Base load, 2019 to 2025 | +52% | min hour of 2025 (10,903 MW) / min hour of 2019 (7,167) - 1 |
| Peak load, 2019 to 2025 | +26% | max hour 24,957 / 19,803 - 1 |
| Top-50 load hours in 2025 | 47 | `DOM_TOP50_HOURS` where `rank_end_2025 <= 50` and year = 2025 |
| Growth by hour of day | 4am +41%, 4pm +27% | `DOM_LOAD_PROFILE`: mean MW in that hour, 2025 / 2019 - 1 |
| Winter and summer peaks | 2025: 24,957 (23 Jan, 8am) vs 23,905 | `DOM_LOAD_ANNUAL` |
| Commercial sales index 2025 | 165 (2013 = 100) | `STG.SALES`, Dominion VA, commercial class, `sales_mwh` / 2013 value |
| Commercial customers index | 108 | same with `customers` |
| Smart meters installed | 100% | `STG.AMI`, `ami_share` |
| On a time-varying rate | about 1% | EIA-861 Dynamic Pricing, time-based rate customers / customers |
| Data centre contracted capacity | 16.5 GW (Jul 2023) to 53.8 GW (Jul 2026) | `data/reference/dominion_ir_series.csv`, from the earnings decks. Stages: SELOA (engineering), CLOA (construction), ESA (service agreement) |
| Data centre sales, 2025 | 27.8 million MWh, 20% CAGR since 2016 | 4Q 2025 deck, slide 22. 27.8 TWh / 8,760 h = 3,170 MW average load |
| Weather-normal sales growth, 2025 | total 4.5%, commercial 8.1%, residential 2.3% (DEV and DESC combined); DEV 5.4% | 4Q 2025 deck, slides 7 and 30 |
| Reliability in the rate review | authorised ROE 9.80%, performance adjustment of plus or minus 0.50% on criteria including reliability. 25 bps of DEV earned ROE = $0.027 EPS (deck sensitivity) | 4Q 2025 deck, slides 42 and 48 |

### Outages from EAGLE-I (added November 2026; sql/09 and 11)

EAGLE-I counts customers out in a county from **every utility that serves it**, so these figures describe all utilities in Dominion's 103 Virginia counties, not Dominion's customers alone, and each chart says so (D15). The 33 Dominion-only counties are the check. A failed EAGLE-I run is NULL, not zero, and a 15-minute slot with no row means nobody out (D16). Days run midnight to midnight Eastern Standard Time. None of these figures is Dominion's SAIDI.

| Figure | Value | Calculation |
|---|---|---|
| Customer-hours | Chesterfield County, 18 Jul 2025: 13,513 | sum of `customers_out` x 0.25 over the day's 15-minute readings (`FCT_COUNTY_DAY.customer_hours`; worked example 6 in `08`) |
| Customer-hours per 1,000 customers | Chesterfield, 18 Jul 2025: 87.2 | customer-hours / `DIM_COUNTY.customers_basis` x 1,000 (basis 155,017; D15) |
| Storm vs calm county-days, 2015 to 2025 | **11.9 times** (95% interval 7.9 to 16.9) | mean customer-hours per 1,000 customers on county-days with a NOAA line-risk storm report (6,108 county-days, mean 332.8, interval 225.6 to 453.4) / on county-days without one (373,851, mean 27.86, interval 23.09 to 33.22). Complete county-days only, the 99 mapped counties (D20). Intervals: 2,000 bootstrap resamples of whole days, because one storm hits many counties at once; the two levels and the ratio come from the same resamples. Checks: non-major days only (proxy major event days, D18, removed) 9.9 (8.6 to 11.3); the 31 Dominion-only counties in the panel 19.9 (11.2 to 32.5); each year from 5.9 (2025) to 27.4 (2020), every interval above 1. 2025 rests on 74% of its county-days, because failed EAGLE-I runs cluster in late 2025 (P20). `scripts/storm_vs_calm_ratio.py`, every row in `data/output/storm_vs_calm.csv`. An association, not the storm's causal effect: NOAA reports are partly triggered by damage, and outages that run past midnight land on a "calm" next day, which pulls the ratio down |
| Outage minutes per customer by county, non-major days, 2015 to 2024 | 195 across the 103 counties; 55 (Prince William) to 633 (Pittsylvania) among counties with 20,000 or more customers | 60 x customer-hours on days that are not proxy major event days / `customers_basis`, for each year, then the mean of the ten years (`FCT_COUNTY_YEAR.outage_minutes_per_customer_non_med`; map: `data/output/county_outage_map.csv`, `map_flag = 'ok'`) |
| Non-major county outage events per 10,000 customers | 9.5 a year (2015 to 2019), 10.0 (2020 to 2024) | `SUM(events_non_med) / SUM(customers_basis) x 10,000` over the 103 counties. County events scale with county size (D17), so compare a county with itself over time |
| Proxy major event days | 2 to 18 a year, 2015 to 2025 | IEEE 1366 2.5 beta method on daily customer-hours in the 103 counties (D18): the 2020 threshold is exp(9.8256 + 2.5 x 1.2389) = 409,595 customer-hours, from 2015 to 2019 (worked example 7 in `08`). An approximation of, not Dominion's own, major event days |
| Territory event | 486, Feb 2015 to Dec 2025 | 10,000 or more customers out in the 103 counties, gaps up to 3 hours merged (D17) |
| Event peak, and peak held one hour | Isaias, 4 Aug 2020: 351,738 and 343,492 | `peak_customers_out`: the highest 15-minute count. `peak_sustained_1h`: the highest count held for four consecutive readings; events are ranked on it, so a 45-minute spike does not outrank a multi-day storm (D17) |
| Hours to 50%, 90% and 99% restored | Isaias: 8.25, 33.5 and 72.75 | hours from the peak until the count falls below peak - share x (peak - background) and stays below for the next 3 hours; background = median of the 24 hours before the event (2,316 for Isaias) |
| Restoration curve | Isaias: 60.5% restored 12 hours after the peak, 89.9% after 33 | `FCT_RESTORATION_CURVE.share_restored` = (peak - hourly maximum) / (peak - background), hours 0 to 167, events peaking at 50,000 or more |
| Storm type, tropical cyclone | Isaias: tropical, ISAIAS | `FCT_EVENT_CONTEXT`: `tropical` when a HURDAT2 track point lies within 400 km of Richmond from 24 hours before the event starts to its peak, or NOAA has a tropical county-day on the event's days; otherwise `winter` or `wind`, whichever has more NOAA county-days, or `no NOAA line-risk report` |
| DOE-417 customers affected, size ratio | Isaias: 508,000; 0.69 | matched report (D19); `size_ratio` = EAGLE-I peak / DOE-417 customers affected. Shown, not filtered on: the two count different things |

### Load shape and sales (added November 2026; sql/07 and 10)

| Figure | Value | Calculation |
|---|---|---|
| Growth by hour of day, 2019 to 2025 | hours ending 1 to 5 a.m. +39.0% to +41.0%; 1 to 5 p.m. +26.9% to +27.4% | `DOM_LOAD_PROFILE.growth_pct`: mean MW in that hour ending, 2025 / 2019 - 1 (PJM DOM zone, EIA-930) |
| Winter and summer peaks by year | 2026 to 29 Oct: winter 25,413 MW (9 Feb), summer 25,384 MW (3 Jul) | `DOM_SEASONAL_PEAK`: highest hour in December, January and February of the same calendar year (winter) and in June, July and August (summer), as in `DOM_LOAD_ANNUAL`; 2026 runs to the hour ending midnight 29 Oct (D21) |
| Average load by month and hour | | `DOM_LOAD_HOUR_MONTH.avg_mw` (heatmap); `hours_reported` shows the hours behind each cell |
| Daily load with degree days | | `DOM_LOAD_DAILY`: daily average, maximum and minimum MW beside Virginia's population-weighted HDD and CDD (NOAA CPC) |
| Commercial sales per commercial customer | 156 MWh (2013) to 238 MWh (2025) | `FCT_SALES_SECTOR.mwh_per_customer`: bundled plus delivery-only MWh / customers, Dominion Virginia (EIA-861). T29 checks the 2025 commercial total |

The DOM zone is larger than Dominion's retail territory, and hourly load by customer class or county is not public, so none of these figures says which customers drove the growth (D14).

## Measure naming

Measures use the metric name (`SAIDI ex MED`, `CAIDI 5yr`). Plain-language names are used in visual titles. Columns keep their Snowflake names, so each card can be traced to a column in `docs/02_data_dictionary.md`.

Formatting measures (`Bar colour`, `Dot colour`, `Row colour`, `SAIFI label`, `CAIDI label`, `Index label`, `Adjusted label`, `Hour colour`, `Change colour`) return colour strings or conditional labels and are listed at the end of `powerbi/measures.dax`.

## Trend tests, 2015 to 2025

`scripts/trend_tests.py` fits an ordinary least-squares line against the year to each annual series for Dominion Virginia, 2015 to 2025 (eleven points, read from `data/output/fct_reliability.csv` and `saidi_weather_adjusted.csv`), and reports the slope, its 95% confidence interval and the two-sided p-value (t test, 9 degrees of freedom). `scripts/check_output_metrics.py` asserts the values below.

| Series | Slope per year | 95% CI | p |
|---|---:|---|---:|
| SAIDI ex-MED (minutes) | +0.64 | -1.87 to +3.15 | 0.58 |
| SAIFI ex-MED (interruptions per customer) | +0.0043 | -0.0111 to +0.0196 | 0.54 |
| CAIDI ex-MED (minutes) | +0.17 | -0.94 to +1.28 | 0.74 |
| Weather-adjusted SAIDI (minutes; `07` Q10) | +0.34 | -1.41 to +2.08 | 0.67 |

Every interval includes zero: on eleven points none of these long-run trends is statistically clear, so the long run is described as a direction, not a finding. The weather-adjusted series comes from a fit on 2015 to 2024 (D6), so its interval understates the uncertainty; before decision D22 its upper bound was +2.09.

## Weather-model interpretation

The regression was fitted on only ten annual observations (2015-2024); the correlation shows association, not causation. The unusually small 2025 prediction error should not be presented as evidence of consistent forecasting accuracy. Annual NOAA storm county-days and ex-MED SAIDI also differ in which event days they cover. Weather-adjusted SAIDI is a model-based comparison, not an audited reliability measure.

## Interpreting year-to-year attribution

When annual SAIDI barely changes, dividing the logarithmic SAIFI change by the tiny logarithmic SAIDI change gives an unstable percentage. In `V_TREND`, the frequency-share calculation is now left blank when the absolute logarithmic SAIDI change is below 0.02 (approximately a 2% annual change). The longer 2023-to-2025 comparison remains available and is interpretable. Suppressing a ratio is not suppressing the actual SAIDI/SAIFI/CAIDI values.
