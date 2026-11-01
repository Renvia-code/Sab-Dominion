# 06. Power BI report

> **At a glance:** One page per question. Start with frequency against minutes per interruption. Read weather as context, then the county and storm pages (all utilities), and hourly demand as a separate growth story. The Data notes page shows the tests and the reconciliation.

**Files**
- Report: `powerbi/Dominion_reliability_review.pbit`. It is a template: the report and the model, no data.
- Working copy: the `.pbix` saved from it is not committed (`*.pbix` is in `.gitignore`).
- `powerbi/measures.dax`: every measure, with its purpose. The same text is each measure's description in Desktop.
- `powerbi/m/`: the query behind each table.
- `powerbi/theme_dominion_review.json`: the theme.

**Data source.** Opening the template asks for one text parameter, `DataFolder`: this repository's `data\output\` folder, for example `C:\path\to\dominion-reliability-review\data\output\` (it must end with a backslash). Every table is imported from the CSV files there, so the report opens with no network connection or running warehouse. The report was developed in DirectQuery against Snowflake (D13).

**Model**
- 18 imported tables, plus a disconnected year table (`'Dashboard Year'`) and a measures table.
- 77 measures and 5 calculated columns.
- Two relationships:
  - `FCT_RELIABILITY[UTILITY_KEY]` many-to-one `DIM_UTILITY[UTILITY_KEY]`
  - `RESTORATION_CURVE[EVENT_KEY]` many-to-one `OUTAGE_EVENTS_TOP10[EVENT_KEY]`
- All other tables are keyed by year, hour or county and have no relationships.
- Auto date/time is off.

## Design rules

| Rule | Reason |
|---|---|
| The title states the finding; the subtitle states the unit and source | The titles summarize the report on their own |
| `#0A66C2` for the subject of the chart (Dominion, or the series the title refers to); `#B8BCC2` for context; `#E8B117` only where a third category is required (the hours ending 1 to 5 p.m. on the hour-growth charts, summer) | Consistent color meaning across pages |
| Straight lines between points, with markers on annual series | Smoothed lines imply values between the observations |
| Counting changes (2015, 2020) are dashed vertical lines on each reliability trend, on a continuous year axis | Separates changes in measurement from changes in performance |
| A reference line where an anchor is needed (2019 level, 2015 = 100, ten-year average, peer medians) | Makes non-zero axes readable |
| Data labels on the points the title refers to | Reduces clutter |
| All figures come from measures, not dragged columns. Aggregation is customer-weighted: sum the numerators, sum the denominators, divide once | No "Sum of" headers and no averaged ratios |
| Correlations are titled as associations; model estimates are labeled as such | A correlation is not a cause, and the weather-adjusted series is a model comparison (D14) |
| Every EAGLE-I chart says "all utilities" | EAGLE-I counts every utility's customers in a county (D15) |
| Alt text on every visual | Screen readers and the exported PDF |

## Pages

### 1. Summary
- Header and a year slicer (default 2025).
- Five cards for the selected year: customers served, SAIDI, minutes per interruption (CAIDI), SAIFI, major-event share.
- SAIFI and CAIDI trends.
- Actual and weather-adjusted SAIDI.
- The storm scatter.
- Page filter: `PEER_GROUP` = Dominion Energy Virginia.

### 2. Scorecard
2025 in Dominion's own measures.
- Cards: SAIDI ex MED 144.4, customers served 2.68M, SAIFI 1.320, CAIDI 109.4, SAIDI with major event days 306.7, and the major-event-day share 53%.
- Load cards: lowest hour +52% and peak hour +26% (2019 to 2025), and 47 of the top 50 hours in 2025.
- The reconciliation table: twelve rebuilt figures against the published ones (`data/output/reconciliation.csv`, 12 of 12 match).
- Page filters: `PEER_GROUP` = Dominion Energy Virginia and `YEAR` = 2025.

### 3. What moved
SAIFI ex MED and CAIDI ex MED, 2013 to 2025, stacked at full width, each with the 2015 and 2020 lines and the 2019 level.
- Frequency: up 6% since 2019, most of it after 2023.
- Minutes per interruption (CAIDI): down 9% since 2019. CAIDI is SAIDI ÷ SAIFI, a ratio, not a measured restoration time.

### 4. Weather
- Stacked columns: minutes on ordinary days and on major event days.
- Scatter of storm county-days against SAIDI ex MED for 2015 to 2024 (n = 10). Its trend line is the fit behind the weather adjustment: 104.3 + 0.0518 × storm county-days, r = 0.70, an association.
- The weather-adjusted SAIDI line, a model estimate. Its trend is +0.34 minutes a year, 95% CI −1.41 to +2.08 (`scripts/trend_tests.py`).
- The co-op SAIFI index.

### 5. Fair comparison
Twelve large utilities: Dominion and 11 peers, chosen by EIA ID before results were computed (D10).

Fourth of twelve on outage minutes. Minutes per interruption are mid-range; frequency is the gap. Ten of the twelve use IEEE 1366; Dominion and Alabama Power use their own rule.

- **Bar chart:** three-year SAIDI, 2023 to 2025.
- **Quadrant scatter:** five-year SAIFI against CAIDI.
  - The dashed lines are the medians of the 11 peers, Dominion excluded: SAIFI 0.934 and CAIDI 99.5.
  - `peer_reliability_5yr.csv` also holds the medians of all twelve. Dominion falls in the same quadrant with either set.
- **Table:** region, storm rule, two period averages, change and five-year CAIDI.
  - The storm rule (measure `Method`) covers 2014 to 2025, the years compared.
  - Georgia Power and Duke Energy Florida filed "Other" in 2013 only, so they show as IEEE 1366.

### 6. Outages by county
EAGLE-I, all utilities in Dominion's 103 counties; four counties are left off for unreliable data.
- Non-major outage minutes for the 15 highest of the 35 counties with 20,000 or more customers.
- The ten largest territory events, 2015 to 2025, with:
  - peak customers out, and the peak held for one hour (the ranking rule)
  - hours to clear 90% of the outage
  - customer-hours

These figures describe places, not one utility, and none of them is Dominion's SAIDI.

### 7. Storms
- NOAA storm county-days by type, 2013 to 2025.
- The Isaias restoration curve (August 2020). The share of the outage cleared each hour after the peak is (peak − customers out) ÷ (peak − pre-event level). It is a net count across all utilities, not a utility's "% of affected customers restored".

### 8. Growth
- Sales and customer indices since 2013 (2013 = 100).
- Load growth by hour of day, 2019 to 2025.
- Smart meters as a share of meters, and the share of customers on a time-varying rate.

### 9. Demand and seasons
- Winter and summer peaks by year. 2026 runs to the hour ending midnight, October 29.
- Average demand by hour of day, 2019 and 2025.
- Retail sales by customer class (TWh).

### 10. Demand summary
One page on demand: smart meters, the sales index, seasonal peaks, three cards and load growth by hour of day.
- The cards: lowest hour +52%, top-50 hours in 2025: 47, peak hour +26%.

### 11. Data notes
- Sources and method.
- The 31 data tests (T1 to T31, `data/output/test_results.csv`).
- The twelve rebuilt figures against the published ones (`data/output/reconciliation.csv`, 12 of 12 match).

## Model objects

| Object | Source file in `DataFolder` | Pages |
|---|---|---|
| `FCT_RELIABILITY`, `DIM_UTILITY` | `fct_reliability.csv`, `dim_utility.csv` | 1 to 5 |
| `V_GROUP_INDEX` | `v_group_index.csv` | 4 |
| `V_STORM_VS_SAIDI` | `storm_vs_saidi.csv` (after D22) | 1, 4, 7 |
| `SAIDI_WEATHER_ADJUSTED` | `saidi_weather_adjusted.csv` | 1, 4 |
| `COUNTY_OUTAGE_MAP`, `OUTAGE_EVENTS_TOP10`, `RESTORATION_CURVE` | `county_outage_map.csv`, `outage_events_top10.csv`, `fct_restoration_curve.csv` | 6, 7 |
| `DOM_LOAD_ANNUAL`, `DOM_TOP50_HOURS`, `DOM_LOAD_PROFILE`, `DOM_LOAD_HOUR_MONTH`, `DOM_SEASONAL_PEAK` | the `dom_*.csv` files of the same names | 8 to 10 |
| `FCT_SALES_SECTOR` | `fct_sales_sector.csv` | 9 |
| `LoadGrowth`, `Programmes2025` | `load_growth.csv`, `programmes_2025.csv` (the workbook's two sheets, exported by `scripts/export_workbook_tables.py`) | 8, 10 |
| `Tests`, `Reconciliation` | `test_results.csv`, `reconciliation.csv` | 11 |

The report reads no workbook sheet. The workbook's `StormIndex` sheet predates D22.

## Refresh

1. Replace the files in the folder, keeping the same names.
2. Click Home > Refresh.

To use another folder, go to Transform data > Edit parameters > `DataFolder`. The path must end with a backslash.

The CSV files come from `scripts/export_powerbi_csv.py`, which exports the local DuckDB build of the same SQL that builds `RELIABILITY.MART` in Snowflake (`data/README.md`), and from `scripts/export_workbook_tables.py` for the two workbook tables.

## Export

File > Export > PDF produces the static copy. Pages are 16:9 (1920 × 1080).
