# Data files

The original data files are stored separately from the supporting files and the results of my analysis making it easier to trace a number in the dashboard back to where it came from.

## What's in each folder?

| Folder | What it's for |
| --- | --- |
| [`input/`](input/) | Four EIA/PUDL extracts covering reliability, customer meters and electricity sales. The historical reliability file covers 2013–2024; the separate EIA file provides 2025. |
| [`reference/`](reference/) | Information used to interpret the data: Dominion's Virginia service counties, NOAA's weather-zone-to-county lookup, and selected figures from Dominion investor presentations. |
| [`output/`](output/) | Exported summaries (annual storm exposure, storms alongside SAIDI, annual demand for the PJM DOM subregion), the mart tables the Power BI report imports, and simplified Virginia county boundaries for the map. |

## How I used the files

**Reliability:** I put the 2013–2024 history and 2025 EIA records into a consistent annual dataset. I used this to check Dominion's reported SAIDI, SAIFI and CAIDI trends.

**Weather:** NOAA records are filed by event, but several reports may describe weather affecting the same county on the same day. I matched the events to Dominion's Virginia service area using the files in `reference/`, then counted each county-date once, with Bedford city counted as part of Bedford County (decision D22). The result is [`storm_index.csv`](output/storm_index.csv). I matched these yearly totals with reported outage minutes in [`storm_vs_saidi.csv`](output/storm_vs_saidi.csv) for an exploratory regression.

**Electricity demand:** I filtered EIA-930 hourly records to the PJM DOM subregion, checked unusual readings, and summarized demand by year in [`dom_annual.csv`](output/dom_annual.csv). The DOM subregion is broader than Dominion's Virginia retail service area.

**Meters and sales:** The PUDL files in `input/` helped me compare smart-meter adoption, electricity use and customer growth. Those analyses don't have separate CSV exports in `output/`.

## Where are the full NOAA and hourly demand files?

They are too large to keep in this repository. The download scripts in [`scripts/`](../scripts/) retrieve them into a local `data/raw/` folder, which Git ignores. **So `raw/` won't appear in the GitHub folder listing.** The smaller files needed to reproduce the core reliability analysis are included here.

I didn't manually change numbers to make the charts. The cleaning and calculations are defined in [`sql/`](../sql/). For exact sources and file counts, see [Sources](../docs/01_sources.md); for worked examples showing how a source row becomes a result, see [Transformations](../docs/08_transformations.md).

**Output format note:** `data/output/dom_annual.csv` is a compact saved snapshot, not an exact export of every column in `MART.DOM_LOAD_ANNUAL`. Its year column is named `yr` (rather than `year`), and it does not include `peak_mw` or `hours_missing`. Use the SQL mart definition for the full set of fields, or `dom_load_annual.csv` below.

**Power BI exports:** [`scripts/export_powerbi_csv.py`](../scripts/export_powerbi_csv.py) writes the mart tables the report uses as CSV, so the report can refresh from a folder without a Snowflake connection: `fct_reliability.csv`, `dim_utility.csv`, `v_group_index.csv`, `saidi_weather_adjusted.csv`, `dom_load_annual.csv` (every column), `dom_top50_hours.csv`, `dom_load_profile.csv` and `peer_reliability_5yr.csv` (the twelve large-utility peers: SAIDI 2023–25, SAIFI and CAIDI 2021–25, with ranks). Since decision D22 it also rewrites `storm_index.csv` and `storm_vs_saidi.csv` in their original columns and number format. The same script writes the November 2026 tables (`dim_county`, `fct_county_year`, `county_outage_map`, `fct_territory_day`, `fct_event_context`, `outage_events_top10`, `fct_restoration_curve`, `dom_load_hour_month`, `dom_seasonal_peak`, `dom_load_daily`, `fct_sales_sector`; definitions in `docs/02_data_dictionary.md`). EIA-930 figures run to the hour ending midnight on 29 October 2026 (decision D21). Column names are the mart's. They are exported from the local DuckDB build of the same SQL (`scripts/run_local_duckdb_sources.py`, which runs the tests), and [`powerbi_exports_manifest.csv`](output/powerbi_exports_manifest.csv) records the rows, bytes and SHA-256 of each file as written (LF line endings, as stored in Git; a Windows checkout with `core.autocrlf` converts them to CRLF and changes the hash, not the data). [`va_counties.geojson`](output/va_counties.geojson) holds the 133 Virginia counties and independent cities (Census cartographic boundaries 2024, simplified) for charts, and [`va_counties.topojson`](output/va_counties.topojson) the same counties for the Power BI shape map (object `counties`, key `county_fips`; shared borders simplified once so neighbours still meet).
