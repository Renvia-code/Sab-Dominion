# How to read the project

The [main README](../README.md) is the business summary. This folder holds the supporting evidence for anyone who wants to check the numbers or understand the choices.

**Start with three documents:**

1. [Metrics and measures](05_metrics_and_measures.md): what SAIDI, SAIFI, CAIDI, weather exposure and demand numbers actually mean.
2. [Transformations](08_transformations.md): seven worked examples tracing source data to calculations, including an EAGLE-I county-day and the Isaias outage event.
3. [Decisions](04_decisions.md): why the methods were chosen and where the findings are limited.

**For technical questions:** [Sources](01_sources.md) identifies datasets and attribution; [Data quality](03_data_quality.md) documents known anomalies and the 31 checks (T1 to T31; results in `data/output/test_results.csv`, published figures compared in `data/output/reconciliation.csv`); [Data dictionary](02_data_dictionary.md) lists the actual tables and fields; [Power BI guide](06_powerbi_report.md) maps findings to pages. [Conventions](00_conventions.md) and [Runbook](07_governance_and_runbook.md) are reference notes.

The `sql/` folder contains the executable calculations. These documents are explanatory records, not a substitute for the code or proof that any optional Snowflake automation has been deployed.

**Core conclusion:** The increase in reported outage minutes from 2023 to 2025 was more associated with interruption frequency than interruption duration. NOAA storm exposure was positively correlated with SAIDI in a small exploratory model, and county by county, outage customer-hours on storm county-days were about 12 times those on calm days (EAGLE-I, all utilities in Dominion's counties). The public data does not establish the cause of outages or which feeder should be upgraded.
