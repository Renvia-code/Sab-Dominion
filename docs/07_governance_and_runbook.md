# 07. Governance and runbook

> **At a glance:** Quick read: this is a reproduction and security reference, not evidence that every optional deployment or scheduled task is running.

Access control, secrets handling, layering rules, refresh procedure and change control.

## Access model

| Principal | Role | Permitted | Not permitted |
|---|---|---|---|
| Build user | `ACCOUNTADMIN` on the project account | Create and replace all objects in `RELIABILITY` | |
| `POWERBI_SVC` | `BI_READER` | `SELECT` on all tables and views in `RELIABILITY.MART`, including objects created later (`FUTURE` grants). `USAGE` on the warehouse | Read `RAW` or `STG`. Write to any object. Access any other database |

The October report (`Dominion_Reliability.pbix`, kept outside the repository; see the last table) connects to Snowflake as `POWERBI_SVC` and can read only the mart. The template in `powerbi/` connects to no database: it imports the CSV files in `data/output/` (`docs/06_powerbi_report.md`). `sql/08_grants.sql` creates the role and user. Two points of note:

- `CREATE OR REPLACE` on a table or view drops its grants. Two measures are in place: `GRANT SELECT ON FUTURE TABLES/VIEWS` so that new and rebuilt objects are readable and `COPY GRANTS` on every `CREATE OR REPLACE` in MART so that existing objects retain their grants through a rebuild.
- Power BI's Snowflake connector with username and password authentication requires the user to be `TYPE = LEGACY_SERVICE`. The default user type fails authentication.

## Secrets

No password, key or token appears in the repository. `08_grants.sql` contains a placeholder. The service password is held in the Snowflake account and in the Power BI credential store on the build machine. In a shared environment the service user would use key-pair authentication with the private key in a secrets manager and scheduled rotation.

`.gitignore` excludes `*.pbix` (binary; embeds the connection), `*.env`, `*.key`, `*.p8` and the large raw downloads.

## Layering

| Layer | Reads from | Read by | Rebuild |
|---|---|---|---|
| `RAW` | stages | `STG` | Re-upload and `COPY INTO` |
| `STG` | `RAW` | `MART` | Immediate (views) |
| `MART` | `STG`, other `MART` objects | In Snowflake: the October report (`POWERBI_SVC`) and analysts. In the DuckDB mirror: `scripts/export_powerbi_csv.py`, which writes the CSV files the template imports | Seconds |

A change to a source file affects `RAW` only. A change to a definition affects one view in `STG` or one object in `MART` and consumers receive it on refresh. The tests verify that a change has not broken the layer contract.

## Refresh procedure

### Annual, October (EIA-861 final release)

1. Download the new `Reliability_YYYY.xlsx` and `Service_Territory_YYYY.xlsx`; save the named sheets as CSV into `data/input/` and `data/reference/`.
2. Run `scripts/extract_pudl.py` once PUDL has published the prior year's tables.
3. Upload to the stages. Run `sql/01`. The `RELIABILITY_2025` view and its `source` string are renamed for the new year.
4. Run `sql/02` and `sql/04`. All tests except T3 and T5 must return zero rows; T3's count must be explained.
5. Update the year windows in `powerbi/measures.dax` (`IN {...}` sets and the three-year measures).
6. Refresh the reports. The October report reads Snowflake and refreshes directly. The template imports CSV files, so first rebuild the DuckDB mirror and export them again (`python -I scripts/run_local_duckdb_sources.py`, then `python -I scripts/export_powerbi_csv.py`), then refresh it. Compare the scorecard with the new annual report. Record the load in `CHANGELOG.md`.

### Monthly (NOAA)

NOAA re-issues files with a new `_c` stamp when events are revised. Run `scripts/download_noaa.sh`, then `sql/05`. T8 indicates whether the latest year is complete.

### As required (EIA-930)

Run `scripts/download_eia930.sh`, then `sql/06` and `sql/07`. The file for the current half-year grows daily.

### Yearly (EAGLE-I, DOE-417, HURDAT2, degree days: sql/09 to 11)

1. `bash scripts/download_eaglei.sh`, then `python -I scripts/extract_eaglei_va.py`; `bash scripts/download_context_sources.sh`, then `extract_census_va.py`, `extract_doe417.py`, `extract_hurdat2.py` and `extract_degree_days.py`.
2. Create the two stages (the `CREATE ... IF NOT EXISTS` statements at the top of `sql/09` and `sql/10`), then upload uncompressed, because the COPY pattern in `sql/09` expects `.csv` names:
   `PUT 'file://<repo>/data/raw/eaglei/va/eaglei_outages_va_20*.csv' @RELIABILITY.RAW.EAGLEI_STAGE/va/ AUTO_COMPRESS = FALSE OVERWRITE = TRUE`;
   `MCC.csv`, `coverage_history.csv` and `data/raw/census/va_county_census.csv` to `@RELIABILITY.RAW.EAGLEI_STAGE`;
   `cpc_degree_days_long.csv`, `hurdat2_points.csv` and `doe417_events_2014_2025.csv` to `@RELIABILITY.RAW.CONTEXT_STAGE`.
3. Run `sql/09` (after `05`), `sql/10` (after `06`) and `sql/11` (after `09`). T13 to T31 are commented with their expected results. T21 compares the county-day panel with `STORM_INDEX`, so it fails until `STORM_INDEX` has been rebuilt with decision D22.
4. `python -I scripts/run_local_duckdb_sources.py` builds the same tables in DuckDB; `python -I scripts/export_powerbi_csv.py` writes the CSV files the report imports.

A test run on 1 November 2026 used a separate Snowflake trial account (X-Small warehouse, about one minute of build time): every load matched its file, T13 to T31 passed except T21 (that account's `STORM_INDEX` predated D22), and the new tables matched the DuckDB build on 25 row counts and totals. Any other account, including the project's own, gets the November tables only when steps 1 to 3 above are run in it.

### Example only: scheduling the tests in Snowflake

```sql
CREATE OR REPLACE TABLE RELIABILITY.MART.TEST_RESULTS (run_at TIMESTAMP_NTZ, test VARCHAR, rows_returned NUMBER, expected VARCHAR, status VARCHAR);

CREATE OR REPLACE TASK RELIABILITY.MART.RUN_TESTS
  WAREHOUSE = SNOWFLAKE_LEARNING_WH
  SCHEDULE = 'USING CRON 0 6 15 10 * America/New_York'   -- 15 October, after the EIA release
AS
INSERT INTO RELIABILITY.MART.TEST_RESULTS
SELECT CURRENT_TIMESTAMP, 'T1', COUNT(*), '0', IFF(COUNT(*) = 0, 'pass', 'flag')
FROM (SELECT utility_key, year FROM RELIABILITY.MART.FCT_RELIABILITY GROUP BY 1,2 HAVING COUNT(*) > 1)
UNION ALL
SELECT CURRENT_TIMESTAMP, 'T4', COUNT(*), '0', IFF(COUNT(*) = 0, 'pass', 'flag')
FROM RELIABILITY.MART.FCT_RELIABILITY
WHERE utility_key = '19876|VA' AND year = 2025 AND NOT (saidi_all = 306.7 AND saidi_ex_med = 144.4);
-- remaining tests follow the same pattern
```

If this example task is fully implemented and enabled, the Data notes page could read `TEST_RESULTS` in place of `data/output/test_results.csv`, which the template imports. The example above is not proof of a deployed scheduled task.

## Change control

- Each change to a SQL file is a commit whose message states the change and the test that verified it.
- `CHANGELOG.md` records each load: row counts and any test whose result changed.
- A definition change (a new event type in the storm index, a new peer) is recorded in `docs/04_decisions.md` with the alternative considered.
- Report screenshots are not committed. The PDF export of each presented version is retained outside the repository with its date.

## Limitations

1. Dominion's major-event rule differs from IEEE 1366. Peer comparisons are indicative.
2. EIA-861 identifies utilities, not customers. Attribution of load growth to data centres is an inference from the shape of the load.
3. The weather fit has ten observations. It is a check on one year, not a forecasting model.
4. EIA-930's DOM zone includes co-ops that take power through Dominion's transmission system. The zone load is slightly larger than Dominion's retail load.
5. The project does not measure the effect of the grid transformation programme. It reports what the public annual figure can and cannot show.

## Artefacts not in the repository

| Artefact | Location | Reason |
|---|---|---|
| `Dominion_Reliability.pbix` (Import and DirectQuery copies) | Build machine, with a dated PDF export per presented version | Binary; embeds connection details |
| NOAA and EIA-930 raw downloads | `data/raw/` locally, ignored by git | 560 MB; recreated by the scripts |
| Snowflake account | `RELIABILITY` database on the project account | Credentials |
