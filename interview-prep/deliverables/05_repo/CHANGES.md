# Changes on `interview-upgrade-2026-11`

36 commits on top of `ec8ecb6`, which was `main` on GitHub on 1 November 2026; the tip is `c17766a` (88 files changed, 40414 insertions(+), 293 deletions(-)). One line per commit: the hash, what changed, why. Nothing has been pushed.

## What to review first

1. **README.md**, "What's new (November 2026)" and "How to check the work" (69cc362, d1bdff2, e0b3712): what a reader sees first.
2. **D22** (06631ad): the only change to numbers published before, the storm county-days (464 and 791).
3. **The storm comparison**: `scripts/storm_vs_calm_ratio.py`, `data/output/storm_vs_calm.csv` (7347e74, c0b2ea2), docs/05 "Outages from EAGLE-I" and decisions D15-D20 in docs/04.
4. **`sql/09_eaglei_outages.sql`** (ce71834, cfd14a0): the model behind every county figure.
5. **`data/output/reconciliation.csv` and `test_results.csv`** (f444a31): 12 of 12 published figures match; T1-T31 pass.
6. **The peer comparison** (7133aba, 29b179f, b0db94d): Dominion and 11 peers; medians without Dominion; reporting methods.
7. **The Power BI template** (859b52d) with docs/06.

## Sources

- `124d01f` Download and extract scripts for EAGLE-I, EIA-861 and 861M, Census, HURDAT2, CPC degree days, DOE-417, the PJM 2026 forecast tables and the SCC reports; files land in `data/raw/<source>/` with a MANIFEST.csv. *Why:* the county outage, storm-context and load-shape work needs public sources beyond the original three, fetched the same way every time and checked (EAGLE-I MD5s against figshare).
- `1b01faf` HURDAT2 and degree-day extract scripts. *Why:* turn the downloaded text files into loadable CSVs without changing the originals.
- `0a79adc` `requirements.txt` names numpy; new `requirements-sources.txt` lists the extract scripts' packages. *Why:* a fresh environment can run every script; the checks and CI keep the short list.

## Models (SQL)

- `ce71834` `sql/09`: EAGLE-I county outages, `DIM_COUNTY`, county-hour, county-day and territory-day facts, outage events, restoration curves. *Why:* county-level outage counts to set beside storm exposure, with Dominion counties defined by a stated rule (D15) and failed readings kept NULL (D16).
- `cfd14a0` `sql/09`: restoration times that ignore one-reading drops, the peak held for an hour, `FCT_COUNTY_YEAR`. *Why:* a single collection drop ended restorations early and 45-minute spikes led the event ranking.
- `656e15a` `sql/10`: load by hour, month and year, seasonal peaks, degree days, retail sales by class. *Why:* the load-growth story needs hour-of-day, season, weather and customer-class views.
- `606ac00` `sql/11`: storm type, tropical cyclones and DOE-417 reports for each outage event (D19). *Why:* context for the large events; DOE-417 has no utility column, so the match follows a written rule.

## Analysis outputs

- `7347e74` `scripts/storm_vs_calm_ratio.py`: storm against calm county-days, 95% interval from resampling whole days. *Why:* the county-day comparison (11.9 times, 7.9 to 16.9) is the main new statistic and has to be reproducible from one command.
- `c0b2ea2` `data/output/storm_vs_calm.csv`: both levels with intervals, non-major days, Dominion-only counties, each year. *Why:* a reader compares the two levels, not only the ratio, and every quoted number comes from one asserted table.
- `7133aba` `peer_reliability_5yr.csv` adds the medians of the 11 peers without Dominion; D10 says the twelve include Dominion. *Why:* a reference median should not contain the utility being compared with it; ranks and quadrant are unchanged.
- `4fc9939` `data/output/county_outage_map_dominion_only.csv`: the 33 counties Dominion serves alone. *Why:* EAGLE-I counts every utility in a county; the Dominion-only counties are the clean check (159 minutes against 211 in shared counties, a comparison of places).

## Tests and checks

- `bd9505f` `scripts/run_local_duckdb_sources.py`: runs `sql/05`-`07` and `09` on in DuckDB and asserts each declared test. *Why:* the build and its tests run on a laptop without Snowflake.
- `cd71bae` Runner: loaders for HURDAT2, DOE-417 and degree days; four more Snowflake-to-DuckDB translations. *Why:* `sql/10` and `sql/11` need them locally.
- `94dc884` `sql/09`: T17 and T19 comments corrected (33 Dominion-only counties; 8 + 14 county-days). *Why:* the comments stated counts from before the Bedford fold; tests and expected results unchanged.
- `94eb5e2` `scripts/trend_tests.py`: 2015-2025 trend tests for SAIDI, SAIFI, CAIDI and weather-adjusted SAIDI, asserted in `check_output_metrics.py`. *Why:* say whether the long-run trends can be told apart from zero (none can: p 0.54 to 0.74).
- `c49aeb1` `scripts/run_local_duckdb.py`: the closing message points at `run_local_duckdb_sources.py` for T7-T31. *Why:* it said the NOAA and EIA-930 checks need the full Snowflake pipeline, but they run in DuckDB; message only, results unchanged.

## D22 (Bedford city)

- `06631ad` `STORM_INDEX` counts Bedford city as Bedford County; re-exported storm files; README and docs. *Why:* NOAA zone 34 mapped to both codes, so 38 county-days were counted twice over 2013-2025 (2024 and 2025: 464 and 791, were 465 and 796); r 0.70 and the 145.3 prediction are unchanged.

## Exports and Power BI

- `c9c79c4` `scripts/export_powerbi_csv.py`: mart tables to `data/output/` with a manifest (rows, bytes, SHA-256). *Why:* the report imports from a folder instead of a live Snowflake connection (D13).
- `7ae08d1` `data/output/va_counties.topojson` for the shape map. *Why:* Power BI's shape map needs shared county borders keyed by `county_fips`.
- `ac4d9a2` Exports for the county, event and load tables. *Why:* the new report pages import them; rounding keeps the files identical from one build to the next.
- `f444a31` `test_results.csv` (T1-T31), `reconciliation.csv` (12 published figures), `storm_county_year.csv`. *Why:* the Data notes page shows that every test passes and every rebuilt figure matches its publisher.
- `859b52d` Power BI template `powerbi/Dominion_reliability_review.pbit` with a `DataFolder` parameter, Power Query files, theme and documented measures. *Why:* the report opens offline from the committed CSV files.
- `a810494` `scripts/export_workbook_tables.py`: the workbook's LoadGrowth and Programmes2025 tables as `load_growth.csv` and `programmes_2025.csv`. *Why:* every table the template imports can come from `data/output/`; each index is checked against its Excel formula before it is written.
- `7867129` Template: LoadGrowth and Programmes2025 import the two new CSV files, `DataFolder` defaults to the clone's `data\output\`; CAIDI labelled minutes per interruption; docs/06. *Why:* the template needs only the `data/output/` folder, and the CAIDI label states its unit.

## Docs

- `cf2446e` docs 01-04: sources S12-S20, new tables, data-quality notes P20-P34, decisions D15-D21. *Why:* every new source, anomaly and modelling choice is written down where a reviewer looks for it.
- `0506bbe` docs 05 and 08: EAGLE-I, event and load measures; worked examples 6 (Chesterfield) and 7 (Isaias). *Why:* each new figure can be traced from source rows to the result.
- `80095c4` docs/07: refresh steps for `sql/09`-`11` and the first Snowflake run. *Why:* the yearly refresh can be repeated by someone else.
- `ecb9e73` docs 01 and 02: EIA-930 coverage as downloaded (values to the hour ending midnight 29 Oct 2026). *Why:* one stated cut-off for every 2026 demand figure (D21).
- `69cc362` README "What's new (November 2026)", docs/README, test numbering in docs/00. *Why:* the front door lists the additions, each worded as an association and tied to its table or script.
- `d1bdff2` docs/05 and README: 6,108 storm county-days reconciled with the storm index's 6,530. *Why:* two counts of storm days appear in the docs; both are now labelled (6,530 - 114 off the map - 308 failed readings = 6,108).
- `29b179f` docs/06: ten of the twelve file under IEEE 1366, not "half". *Why:* the old headline did not match the data (only Dominion and Alabama Power file "Other").
- `b0db94d` docs/05: quadrant lines are the 11-peer medians; the `Method` measure covers 2014-2025. *Why:* matches the template.
- `e0b3712` README: the Power BI report is in the repository as a template. *Why:* the README still said no report file was included.
- `2cbd7a8` README: the template's `DataFolder` is `data/output/`. *Why:* since 7867129 the template no longer reads the workbook.
- `506e969` docs 07, 04 and 03: the 1 November Snowflake run of `sql/09`-`11` was a test in a separate trial account; the October report reads Snowflake, the template imports the CSV files; the yearly refresh exports them again first. *Why:* the docs must not suggest that the project's own Snowflake account holds the November tables, or that the template reads Snowflake.
- `c17766a` Comments: the `sql/09` header counts (three staging views, eight mart tables, T31) and the EAGLE-I sizes in `download_eaglei.sh` (11.6 GB of CSV, 1.66 GB zipped). *Why:* the comments had the wrong counts and sizes; no code changes.

Each commit's full message (`git log ec8ecb6..interview-upgrade-2026-11`) gives the detail and the numbers it checked.
