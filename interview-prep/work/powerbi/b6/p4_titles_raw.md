Template: `Dominion_reliability_review.pbit` (11 pages). Flags to review: 6.

### Page 1: Summary

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `ed0384` text box | Reliability performance and weather | static text |  |
| cardVisual `7f06e2` card label | Customers served | _Measures[Selected Customers] |  |
| cardVisual `85c7fe` card label | SAIDI (minutes) | _Measures[Selected SAIDI] |  |
| cardVisual `f37647` card label | Minutes per interruption | _Measures[Selected CAIDI] |  |
| cardVisual `f34f7f` card label | SAIFI (outages) | _Measures[Selected SAIFI] |  |
| cardVisual `60c7e3` card label | Major-event share | _Measures[Selected major-event-day share] |  |
| textbox `f98b3d` text box | Customer outage trends, interruptions and weather exposure | static text |  |
| textbox `f98b3d` text box | (EIA-861 and NOAA Storm Events) | ″ |  |
| lineChart `8cf55a` title | Outages per customer up 6% since 2019, most of it after 2023 | FCT_RELIABILITY[YEAR]; FCT_RELIABILITY[SAIFI ex MED] |  |
| lineChart `8cf55a` subtitle | SAIFI, excluding major event days. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `8cf55a` reference line | 2019 level | ″ |  |
| lineChart `8cf55a` reference line | 2015: Automated Outage Recording | ″ |  |
| lineChart `8cf55a` reference line | 2020: 46 kV lines added | ″ |  |
| lineChart `8cf55a` valueAxis title | Outages per Customer per Year | ″ |  |
| lineChart `5aedb8` title | Minutes per interruption down 9% since 2019 | FCT_RELIABILITY[YEAR]; FCT_RELIABILITY[CAIDI ex MED] |  |
| lineChart `5aedb8` subtitle | CAIDI, excluding major event days. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `5aedb8` reference line | 2019 level | ″ |  |
| lineChart `5aedb8` reference line | 2015: Automated Outage Recording | ″ |  |
| lineChart `5aedb8` reference line | 2020: 46 kV lines added | ″ |  |
| lineChart `5aedb8` valueAxis title | Minutes per interruption | ″ |  |
| lineChart `1bc8e4` title | Adjusted for storm days (a model estimate), SAIDI shows no clear trend since 2015 | SAIDI_WEATHER_ADJUSTED[YEAR]; SAIDI_WEATHER_ADJUSTED[Actual SAIDI]; SAIDI_WEATHER_ADJUSTED[Weather-adjusted SAIDI] |  |
| lineChart `1bc8e4` subtitle | SAIDI ex MED, actual vs weather-adjusted using the NOAA storm-day fit. Dominion Energy Virginia | ″ |  |
| lineChart `1bc8e4` reference line | 10 yr Avg | ″ |  |
| lineChart `1bc8e4` valueAxis title | Outage Mins per Customer | ″ |  |
| scatterChart `826577` title | Years with more storm days had more outage minutes | V_STORM_VS_SAIDI[YEAR]; V_STORM_VS_SAIDI[Storm county-days]; V_STORM_VS_SAIDI[SAIDI ex MED (weather table)] |  |
| scatterChart `826577` subtitle | 2015 to 2024 (n = 10). r = 0.70: association, not cause. The line is the fit used for the weather adjustment | ″ | **causal?** |
| scatterChart `826577` categoryAxis title | Storm county-days (NOAA) | ″ |  |
| scatterChart `826577` valueAxis title | Outage mins per customer | ″ |  |

### Page 2: Scorecard

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| cardVisual `2bddd3` card label | SAIDI (minutes) | FCT_RELIABILITY[SAIDI ex MED] |  |
| cardVisual `4815af` card label | Customers served | FCT_RELIABILITY[Total Customers] |  |
| cardVisual `3bc57c` card label | SAIFI (outages) | FCT_RELIABILITY[SAIFI ex MED] |  |
| cardVisual `7a8692` card label | Minutes per interruption (CAIDI) | FCT_RELIABILITY[CAIDI ex MED] |  |
| cardVisual `588c5e` card label | SAIDI incl. major event days | FCT_RELIABILITY[SAIDI all events] |  |
| cardVisual `268053` card label | Major-event-day share | FCT_RELIABILITY[Major-event-day share] |  |
| cardVisual `ca2695` card label | Lowest hour, 2019 to 2025 | DOM_LOAD_ANNUAL[Floor growth 2019 to 2025] |  |
| tableEx `47061a` title | Rebuilt values match the published ones (12 of 12) | Reconciliation[ROW_NO]; Reconciliation[METRIC]; Reconciliation[REBUILT]; Reconciliation[REPORTED]; Reconciliation[VERDICT] |  |
| tableEx `47061a` subtitle | Rebuilt from public files vs the published source (data/output/reconciliation.csv) | ″ |  |
| cardVisual `ea221b` card label | Peak hour, 2019 to 2025 | DOM_LOAD_ANNUAL[Peak growth 2019 to 2025] |  |
| cardVisual `1b4422` card label | Top-50 hours in 2025 | DOM_TOP50_HOURS[Top 50 hours in 2025] |  |

### Page 3: What moved

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| lineChart `eb9e34` title | Outages per customer up 6% since 2019, most of it after 2023 | FCT_RELIABILITY[YEAR]; FCT_RELIABILITY[SAIFI ex MED] |  |
| lineChart `eb9e34` subtitle | SAIFI, excluding major event days. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `eb9e34` reference line | 2019 level | ″ |  |
| lineChart `eb9e34` reference line | 2015: Automated Outage Recording | ″ |  |
| lineChart `eb9e34` reference line | 2020: 46 kV lines added | ″ |  |
| lineChart `eb9e34` valueAxis title | Outages per Customer per Year | ″ |  |
| lineChart `a56e85` title | Minutes per interruption down 9% since 2019 | FCT_RELIABILITY[YEAR]; FCT_RELIABILITY[CAIDI ex MED] |  |
| lineChart `a56e85` subtitle | CAIDI, excluding major event days. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `a56e85` reference line | 2019 level | ″ |  |
| lineChart `a56e85` reference line | 2015: Automated Outage Recording | ″ |  |
| lineChart `a56e85` reference line | 2020: 46 kV lines added | ″ |  |
| lineChart `a56e85` valueAxis title | Minutes per interruption | ″ |  |

### Page 4: Weather

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| columnChart `d2efd4` title | Major event days are about half of all-event outage minutes in 2025 | FCT_RELIABILITY[YEAR]; FCT_RELIABILITY[SAIDI ex MED]; FCT_RELIABILITY[Major-event-day SAIDI] |  |
| columnChart `d2efd4` subtitle | Minutes per customer: excluding major event days, and on major event days. Dominion Energy Virginia, EIA-861 | ″ |  |
| columnChart `d2efd4` valueAxis title | Outage Mins per Customer | ″ |  |
| scatterChart `cd3dca` title | Years with more storm days had more outage minutes | V_STORM_VS_SAIDI[YEAR]; V_STORM_VS_SAIDI[Storm county-days]; V_STORM_VS_SAIDI[SAIDI ex MED (weather table)] |  |
| scatterChart `cd3dca` subtitle | 2015 to 2024 (n = 10). r = 0.70: association, not cause. The line is the fit used for the weather adjustment | ″ | **causal?** |
| scatterChart `cd3dca` categoryAxis title | Storm county-days (NOAA) | ″ |  |
| scatterChart `cd3dca` valueAxis title | Outage mins per customer | ″ |  |
| lineChart `dcda2b` title | Since 2015, Virginia co-op outage frequency rose 37% and Dominion's 14% | V_GROUP_INDEX[YEAR]; V_GROUP_INDEX[PEER_GROUP]; V_GROUP_INDEX[SAIFI index 2015] |  |
| lineChart `dcda2b` subtitle | SAIFI ex MED, 2015 = 100. Dominion vs all Virginia co-ops. EIA-861 | ″ |  |
| lineChart `dcda2b` reference line | 2015 level | ″ |  |
| lineChart `0cdbc9` title | Adjusted for storm days (a model estimate), SAIDI shows no clear trend since 2015 | SAIDI_WEATHER_ADJUSTED[YEAR]; SAIDI_WEATHER_ADJUSTED[Actual SAIDI]; SAIDI_WEATHER_ADJUSTED[Weather-adjusted SAIDI] |  |
| lineChart `0cdbc9` subtitle | SAIDI ex MED, actual vs weather-adjusted using the NOAA storm-day fit. Dominion Energy Virginia | ″ |  |
| lineChart `0cdbc9` reference line | 10 yr Avg | ″ |  |
| lineChart `0cdbc9` valueAxis title | Outage Mins per Customer | ″ |  |

### Page 5: Fair comparison

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| clusteredBarChart `572942` title | Fourth-highest outage minutes of twelve large utilities, 2023 to 2025 | DIM_UTILITY[Display name]; FCT_RELIABILITY[SAIDI 2023 to 2025] |  |
| clusteredBarChart `572942` subtitle | SAIDI ex MED, 3-year average. Dominion excludes storms by its own rule, most peers by IEEE 1366, so gaps are indicative | ″ |  |
| clusteredBarChart `572942` valueAxis title | Yearly Outage mins per Customer | ″ |  |
| scatterChart `99301c` title | Mid-pack on minutes per interruption; outage frequency is the gap | DIM_UTILITY[Quadrant name]; DIM_UTILITY[Short name]; FCT_RELIABILITY[SAIFI 5yr]; FCT_RELIABILITY[CAIDI 5yr] |  |
| scatterChart `99301c` subtitle | 5-year averages 2021 to 2025, excluding major event days. Dashed lines: medians of the 11 peers (SAIFI 0.93, CAIDI 99.5) | ″ |  |
| scatterChart `99301c` reference line | Median of 11 peers | ″ |  |
| scatterChart `99301c` reference line | Median of 11 peers | ″ |  |
| scatterChart `99301c` categoryAxis title | Yearly Outages per Customer (SAIFI) | ″ |  |
| scatterChart `99301c` valueAxis title | Minutes per interruption (CAIDI) | ″ |  |

### Page 6: Outages by county

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `c27075` text box | Outages by county | static text |  |
| textbox `ca64ac` text box | EAGLE-I county outage records (ORNL), Dominion's 103 Virginia counties. EAGLE-I counts every utility's customers in a county; 4 counties are left off for unreliable data. | static text |  |
| clusteredBarChart `e4c89a` title | All utilities: non-major outage minutes ranged from 55 (Prince William County) to 633 (Pittsylvania County) a year | COUNTY_OUTAGE_MAP[COUNTY_LABEL]; COUNTY_OUTAGE_MAP[Non-major outage minutes, 20k+ counties] |  |
| clusteredBarChart `e4c89a` subtitle | EAGLE-I, all utilities (not Dominion's SAIDI). Top 15 of the 35 counties with 20,000+ customers; non-major-event days, 2015 to 2024 average | ″ |  |
| tableEx `f50bf6` title | The ten largest outage events: three tropical storms, two winter storms and five wind events | OUTAGE_EVENTS_TOP10[Event]; OUTAGE_EVENTS_TOP10[PEAK_CUSTOMERS_OUT]; OUTAGE_EVENTS_TOP10[PEAK_SUSTAINED_1H]; OUTAGE_EVENTS_TOP10[HOURS_TO_90PCT]; OUTAGE_EVENTS_TOP10[CUSTOMER_HOURS] |  |
| tableEx `f50bf6` subtitle | Territory events in Dominion's 103 counties, 2015 to 2025, by peak day; ranked by customers out held for an hour. EAGLE-I (all utilities) | ″ |  |

### Page 7: Storms

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `3c6be2` text box | Storms | static text |  |
| textbox `3afa5e` text box | NOAA Storm Events (storm county-days) and EAGLE-I outage records (all utilities). Associations, not causes. | static text | **causal?** |
| columnChart `d55f7c` title | Damaging wind was the largest storm type in 12 of 13 years | V_STORM_VS_SAIDI[YEAR]; V_STORM_VS_SAIDI[Wind days]; V_STORM_VS_SAIDI[Winter days]; V_STORM_VS_SAIDI[Tropical days] |  |
| columnChart `d55f7c` subtitle | NOAA storm county-days in Dominion's Virginia counties by type, 2013 to 2025 | ″ |  |
| lineChart `468c8a` title | Isaias, August 2020: 33.5 hours from the peak to clear 90% of the outage | RESTORATION_CURVE[HOUR_SINCE_PEAK]; RESTORATION_CURVE[Share restored] |  |
| lineChart `468c8a` subtitle | Share cleared by hour since the peak: (peak - customers out) / (peak - pre-event level), a net count. EAGLE-I, all utilities in Dominion's 103 counties; not a utility's '% of affected customers restored' | ″ |  |

### Page 8: Growth

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| lineChart `3e0ddc` title | Commercial sales up 65% since 2013 on 8% more customers, consistent with large round-the-clock loads | LoadGrowth[year]; LoadGrowth[Commercial sales index]; LoadGrowth[Commercial customers index]; LoadGrowth[Residential sales index] |  |
| lineChart `3e0ddc` subtitle | Retail sales and customer counts, 2013 = 100. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `3e0ddc` valueAxis title | Index, 2013 = 100 | ″ |  |
| clusteredColumnChart `7b0e71` title | Load growth 2019 to 2025: +39% to +41% in the hours ending 1 to 5 a.m., about +27% in the hours ending 1 to 5 p.m. | DOM_LOAD_PROFILE[HOUR_NO]; DOM_LOAD_PROFILE[Hour growth %] |  |
| clusteredColumnChart `7b0e71` subtitle | Change in average demand for each hour of the day (hour ending, local time), PJM DOM zone, EIA-930 | ″ |  |
| clusteredColumnChart `7b0e71` reference line | Average of all hours | ″ |  |
| clusteredColumnChart `7b0e71` categoryAxis title | Hour of Day | ″ |  |
| clusteredColumnChart `7b0e71` valueAxis title | Growth % | ″ |  |
| clusteredBarChart `1b2743` title | Dominion: smart meters are 99.8% of meters; about 1% of customers are on a time-varying rate | Programmes2025[utility]; Programmes2025[Smart meter share %]; Programmes2025[Time-varying rate %] |  |
| clusteredBarChart `1b2743` subtitle | Smart meters as a share of all meters, and the share of customers on a time-varying rate, 2025. EIA-861 | ″ |  |
| clusteredBarChart `1b2743` valueAxis title | Share % | ″ |  |

### Page 9: Demand and seasons

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `9a34b2` text box | Demand and seasons | static text |  |
| textbox `0d1671` text box | PJM DOM zone hourly demand (EIA-930; a zone, not Dominion's retail territory) and retail sales (EIA-861). 2026 runs through the hour ending midnight, Oct 29. | static text |  |
| clusteredColumnChart `e1c9d7` title | Winter set the year's peak in 2019, 2022 and 2025; 2026 is a near-tie so far | DOM_LOAD_ANNUAL[YEAR]; DOM_LOAD_ANNUAL[Winter peak MW]; DOM_LOAD_ANNUAL[Summer peak MW] |  |
| clusteredColumnChart `e1c9d7` subtitle | Highest hour in Dec to Feb vs Jun to Aug of each calendar year, PJM DOM zone, EIA-930. 2026 runs to Oct 29: summer complete, winter Jan to Feb only | ″ | **winter years?** |
| clusteredColumnChart `e1c9d7` valueAxis title | Peak Demand, MW | ″ |  |
| lineChart `0eee63` title | Average demand rose in every hour from 2019 to 2025, most in the hours ending 1 to 5 a.m. | DOM_LOAD_PROFILE[HOUR_NO]; DOM_LOAD_PROFILE[Average MW 2019]; DOM_LOAD_PROFILE[Average MW 2025] |  |
| lineChart `0eee63` subtitle | Average MW by hour of day (hour ending, local time), PJM DOM zone, EIA-930 | ″ |  |
| lineChart `130afd` title | Commercial sales grew 65% from 2013 to 2025; residential grew 4%, industrial fell 14% | FCT_SALES_SECTOR[YEAR]; FCT_SALES_SECTOR[CUSTOMER_CLASS]; FCT_SALES_SECTOR[Sales TWh] |  |
| lineChart `130afd` subtitle | Retail sales in TWh by customer class (bundled plus delivery-only), Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `130afd` valueAxis title | TWh | ″ |  |

### Page 10: Demand summary

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `0fb6bd` text box | Electricity demand and grid planning | static text |  |
| lineChart `f3f572` title | Commercial sales up 65% since 2013 on 8% more customers, consistent with large round-the-clock loads | LoadGrowth[year]; LoadGrowth[Commercial sales index]; LoadGrowth[Commercial customers index]; LoadGrowth[Residential sales index] |  |
| lineChart `f3f572` subtitle | Retail sales and customer counts, 2013 = 100. Dominion Energy Virginia, EIA-861 | ″ |  |
| lineChart `f3f572` valueAxis title | Index, 2013 = 100 | ″ |  |
| textbox `158cea` text box | Load growth, changing demand patterns and smart-meter adoption \| EIA-861 & EIA-930 | static text |  |
| clusteredBarChart `1d9205` title | Dominion: smart meters are 99.8% of meters; about 1% of customers are on a time-varying rate | Programmes2025[utility]; Programmes2025[Smart meter share %]; Programmes2025[Time-varying rate %] |  |
| clusteredBarChart `1d9205` subtitle | Smart meters as a share of all meters, and the share of customers on a time-varying rate, 2025. EIA-861 | ″ |  |
| clusteredBarChart `1d9205` valueAxis title | Share % | ″ |  |
| clusteredColumnChart `10a79b` title | Winter set the year's peak in 2019, 2022 and 2025; 2026 is a near-tie so far | DOM_LOAD_ANNUAL[YEAR]; DOM_LOAD_ANNUAL[Winter peak MW]; DOM_LOAD_ANNUAL[Summer peak MW] |  |
| clusteredColumnChart `10a79b` subtitle | Highest hour in Dec to Feb vs Jun to Aug of each calendar year, PJM DOM zone, EIA-930. 2026 runs to Oct 29: summer complete, winter Jan to Feb only | ″ | **winter years?** |
| clusteredColumnChart `10a79b` valueAxis title | Peak Demand, MW | ″ |  |
| cardVisual `e12a05` card label | Lowest hour, 2019 to 2025 | DOM_LOAD_ANNUAL[Floor growth 2019 to 2025] |  |
| cardVisual `18d3b9` card label | Top-50 hours in 2025 | DOM_TOP50_HOURS[Top 50 hours in 2025] |  |
| cardVisual `19360d` card label | Peak hour, 2019 to 2025 | DOM_LOAD_ANNUAL[Peak growth 2019 to 2025] |  |
| clusteredColumnChart `71ceb4` title | Load growth 2019 to 2025: +39% to +41% in the hours ending 1 to 5 a.m., about +27% in the hours ending 1 to 5 p.m. | DOM_LOAD_PROFILE[HOUR_NO]; DOM_LOAD_PROFILE[Hour growth %] |  |
| clusteredColumnChart `71ceb4` subtitle | Change in average demand for each hour of the day (hour ending, local time), PJM DOM zone, EIA-930 | ″ |  |
| clusteredColumnChart `71ceb4` reference line | Average of all hours | ″ |  |
| clusteredColumnChart `71ceb4` categoryAxis title | Hour of Day | ″ |  |
| clusteredColumnChart `71ceb4` valueAxis title | Growth % | ″ |  |

### Page 11: Data notes

| Visual | Text on screen | Behind it | Flags |
|---|---|---|---|
| textbox `3673ea` text box | Data notes | static text |  |
| textbox `7faf64` text box | Sources: EIA-861 (reliability, sales, customers; 2013-2024 via PUDL, 2025 final release of Oct 7, 2026); NOAA Storm Events (storm county-days); EIA-930 (PJM DOM zone hourly demand; 2026 runs through the hour ending midnight, Oct 29); EAGLE-I county outages 2015-2025 (ORNL, CC BY 4.0). | static text |  |
| textbox `7faf64` text box | Method: SAIDI, SAIFI and CAIDI exclude major event days unless stated; indices are customer-weighted (sum numerators, sum denominators, divide once). Correlations show association, not cause. The weather-adjusted series is a model estimate from a 2015-2024 fit. | ″ | **causal?** |
| textbox `7faf64` text box | Data snapshot: Nov 1, 2026, Import mode from the CSV files in the DataFolder parameter (no live connection). | ″ |  |
| tableEx `ddba76` title | All 31 data tests pass | Tests[TEST]; Tests[DESCRIPTION]; Tests[EXPECTED]; Tests[ROWS_RETURNED]; Tests[STATUS] |  |
| tableEx `ddba76` subtitle | Tests run on each build of the data (data/output/test_results.csv; definitions in docs/03_data_quality.md) | ″ |  |
| tableEx `ee5d97` title | Rebuilt values match the published ones (12 of 12) | Reconciliation[ROW_NO]; Reconciliation[METRIC]; Reconciliation[REBUILT]; Reconciliation[REPORTED]; Reconciliation[VERDICT] |  |
| tableEx `ee5d97` subtitle | Rebuilt from public files vs the published source (data/output/reconciliation.csv) | ″ |  |
