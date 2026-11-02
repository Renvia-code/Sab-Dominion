"""Exact text shared by the final deck, brief, sheet and claims builders (rulings O-34 to O-39, after V6).

One definition each, so the slide, its notes, the brief and the sheet cannot drift apart.
"""

# C.1 the model line (orchestrator checked the .pbit: 18 imported tables, 2 calculated tables (Dashboard Year,
# _Measures), 2 relationships: FCT_RELIABILITY -> DIM_UTILITY and RESTORATION_CURVE -> OUTAGE_EVENTS_TOP10).
MODEL_LINE = ("The core is a small star: one fact table at utility × state × year, many-to-one to a utility dimension, "
              "with customer-weighted measures. The other tables are pre-built summaries for particular pages, so "
              "most stand alone; only the ten largest outage events join their restoration curves. A year table "
              "drives the slicer. In production I'd conform them to shared date and county dimensions.")

# The candidate's own report (public route), as origin/main docs/06 describes its model: one relationship,
# FCT_RELIABILITY many-to-one DIM_UTILITY; "all other tables are keyed by year or hour and have no relationships".
MODEL_LINE_PUBLIC = ("The core is a small star: one fact table at utility × state × year, many-to-one to a utility "
                     "dimension, with customer-weighted measures. The other tables are pre-built summaries for "
                     "particular pages, keyed by year or hour, so they stand alone. In production I'd conform them to "
                     "shared date and county dimensions.")

# C.2 the authorship sentence: it ends the ADOPTED slide 6 speaker notes and is printed nowhere (correction 1 to C.3)
AUTHORSHIP = ("The October build is mine: the pipeline, the first 12 tests and the report. On November 1 it was "
              "extended with help, using an AI coding assistant: the county outage analysis, 19 more tests and this "
              "template. I reviewed those changes and reran the checks myself. [you: say the last sentence only if "
              "you did both before the interview]")

# C.3 Q18, as corrected: the rule, and the pointer that replaces the sentence in print
Q18_RULE = ("The November changes were made in the extension, not found by you. Say 'the extension counts Bedford city "
            "once; the October build counted it twice', never 'I noticed…'.")
Q18_WHO = ("Use the authorship sentence in START_HERE §8; it also ends slide 6's speaker notes. Say only the parts "
           "that are true.")

# How the same SQL runs locally (orchestrator's final batch, item 8: brief p. 7 and Q15, after the DuckDB sentence).
# scripts/run_local_duckdb_sources.py: translate() is lines 46-79; it removes CREATE DATABASE/SCHEMA, USE WAREHOUSE/ROLE,
# file formats, stages, COPY INTO, LIST, PUT, ALTER WAREHOUSE and the COPY GRANTS clause, and rewrites date parsing
# (TRY_TO_DATE / TRY_TO_TIMESTAMP_NTZ formats) and a few functions (REGEXP_LIKE, DAYOFWEEKISO, LISTAGG, TRY_TO_NUMBER,
# TIME_SLICE, DATE_FROM_PARTS).
RUNNER = ("The runner, scripts/run_local_duckdb_sources.py, drops the Snowflake-only statements (warehouses, stages, "
          "COPY INTO, grants) and translates date parsing and a few functions (translate(), lines 46–79).")

# The adopted data path in one sentence (brief p. 7 and Q15 match slide 6; scripts/export_powerbi_csv.py: "Source: the
# DuckDB mirror built from the source files by scripts/run_local_duckdb_sources.py")
BUILD_UP = ("The same SQL also runs in DuckDB, a local mirror that builds everything, the November tables included, "
            f"and runs all 31 tests in about 22 seconds. {RUNNER} The template imports 18 CSV files exported from that mirror "
            "(16) and the workbook (2), with a manifest of row counts and checksums, so it opens offline. The new "
            "tables reach Snowflake only through one optional step (README step 7).")

# The sheet's model line (item 10): variant-neutral, so "most stand alone" (adopted: 16 of 18; public: all of them)
MODEL_LINE_SHEET = ("The core is a small star: one fact table at utility × state × year, many-to-one to a utility "
                    "dimension, with customer-weighted measures. The other tables are pre-built summaries for particular "
                    "pages, and most stand alone. In production I'd conform them to shared date and county dimensions.")

# Brief A4's three named pieces (B.3). The opener is the sheet's item 2 from the resume, with "a pilot" for the resume's
# "AI pilot" (no "AI" in the brief); the story uses only sourced project facts; the route keeps every slide.
OPENER = ("I'm a business intelligence analyst with three years building dashboards, reporting and data pipelines. At "
          "Mercury Insurance I built a Snowflake pipeline across policy, claims and billing data, over 20 million rows, "
          "and owned the evaluation methodology for a pilot. Before that: Tableau board reporting at The Life "
          "Initiative, forecasting and dashboards at Cofoods, and an MS in Business Analytics at Boston University.")
STORY = ("To prepare, I rebuilt Dominion Energy Virginia's reported reliability numbers from public EIA filings: 130.2 "
         "and 133.0 against the reported 130 and 133. The SQL runs in three layers, raw, staged and mart, with tests "
         "after each load, and a Power BI report sits on customer-weighted measures. Three findings: 2025 had more "
         "storms and more interruptions, and once storms are counted there's no clear trend; against eleven peers, "
         "Dominion's gap is how often customers lose power, not how long; and overnight demand grew faster than "
         "afternoon demand. Public data stops at the county: with your outage records I'd start with interruptions by "
         "circuit and cause, then build the report that tracks mainfeeder hardening.")
ROUTE = ("S1 in full. S2: the reported 130 → 133 and Dominion's reason, the rebuilt 130.2 and 133.0, 2025 replacing "
         "2022, SAIFI +10% and CAIDI −4%. S3: frequency 4th highest of the 12, length mid-pack, methods differ. S4: the result and "
         "its caution. S5: the first two sentences of the model line. S6: the first two sentences and, adopted, the "
         "closing ones. S7: the three months, one line each, without the program lines. S8 in full. Leave the appendix "
         "for questions.")

# Provenance legend on the adopted slide 6 (dates, not a how-made line)
PROV_ORIGINAL = "Original build, Oct 27–31, 2026"
PROV_ADDED = "Added Nov 1, 2026"
