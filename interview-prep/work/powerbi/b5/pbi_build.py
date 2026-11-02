"""B5: build the edited Power BI template (.pbit) from the exported copy.

Input   b5/pbit_src/      File > Export > Power BI template of a COPY of the original .pbix
Output  b5/build/         the edited package tree
        b5/out/Dominion_reliability_review_verify.pbit   DataFolder = this repo's data/output/ (read, never written)
        deliverables/04_powerbi/Dominion_reliability_review.pbit (with --ship) DataFolder = placeholder clone path

Every table imports from the repo's data/output/ CSV files through one text parameter, DataFolder (F1);
since 1 Nov 10:44 (D, a810494) no table reads the workbook. The report edits
are F2-F12 of work/powerbi_fix_plan.md, with the orchestrator's rulings. Run with the repo .venv:
  .venv/Scripts/python.exe -I interview-prep/work/powerbi/b5/pbi_build.py [--ship]
"""
import copy
import csv
import hashlib
import itertools
import json
import re
import shutil
import sys
import uuid
import zipfile
from pathlib import Path

B5 = Path(__file__).resolve().parent
IP = B5.parents[2]                      # interview-prep/
REPO = IP.parent
SRC = B5 / "pbit_src"
BUILD = B5 / "build"
OUT = B5 / "out"
DELIV = IP / "deliverables" / "04_powerbi"
DATA_DIR = REPO / "data" / "output"     # read only: the template's DataFolder is <clone>\data\output\
SHIP_DEFAULT = "C:\\path\\to\\dominion-reliability-review\\data\\output\\"
NAME = "Dominion_reliability_review"

SUBJECT, CONTEXT, GREY, GOLD, INK = "#0A66C2", "#B8BCC2", "#6B7280", "#E8B117", "#1F2A44"


_UID_SEQ = itertools.count()
_HEX_SEQ = itertools.count()
_NS = uuid.UUID("6f1c2a52-6d1e-4b6e-9d0a-2b7c3e4f5a60")


def uid():
    """Deterministic lineage tag (same build -> same tags), so a rebuild reproduces the verified bytes."""
    return str(uuid.uuid5(_NS, f"uid/{next(_UID_SEQ)}"))


def hexid():
    """Deterministic 20-hex-digit name for new pages, visuals and filters."""
    return hashlib.sha1(f"hex/{next(_HEX_SEQ)}".encode()).hexdigest()[:20]


def lit(s):
    """PBIR string literal: single quotes, inner quotes doubled."""
    return "'" + str(s).replace("'", "''") + "'"


def L(value):
    return {"expr": {"Literal": {"Value": value}}}


# ---------------------------------------------------------------------------------------------
# 1. Data snapshot (copied, never edited; the repo's data/ stays untouched)
# ---------------------------------------------------------------------------------------------
CSV_FROM_REPO = [
    "fct_reliability.csv", "dim_utility.csv", "v_group_index.csv", "saidi_weather_adjusted.csv",
    "dom_load_annual.csv", "dom_top50_hours.csv", "dom_load_profile.csv", "storm_vs_saidi.csv",
    "county_outage_map.csv", "outage_events_top10.csv", "fct_restoration_curve.csv",
    "dom_load_hour_month.csv", "dom_seasonal_peak.csv", "fct_sales_sector.csv",
    "test_results.csv", "reconciliation.csv", "load_growth.csv", "programmes_2025.csv",
]


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def build_tests_csv(dst):
    """T1-T31 from docs/03_data_quality.md, status from the latest local test logs."""
    doc = (REPO / "docs" / "03_data_quality.md").read_text(encoding="utf-8")
    rows = []
    for line in doc.splitlines():
        m = re.match(r"^\| (T\d+) \| (\d+) \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", line)
        if m:
            rows.append(dict(test=m.group(1), test_no=int(m.group(1)[1:]), sql_file=m.group(2),
                             check=m.group(3).replace("`", ""), expected=m.group(4).replace("`", ""),
                             result=m.group(5).replace("`", "")))
    logs = IP / "work" / "data" / "logs"
    passed = set()
    for log in ["d4_run_local_duckdb.log", "d4_run_sources_full.log", "d22_run_sources_full.log"]:
        p = logs / log
        if p.exists():
            for t in re.findall(r"^(T\d+): PASS", p.read_text(encoding="utf-8", errors="replace"), re.M):
                passed.add(t)
    for r in rows:
        r["status"] = "pass" if r["test"] in passed else "not run"
    rows.sort(key=lambda r: int(r["test"][1:]))
    with dst.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["test", "test_no", "sql_file", "check", "expected", "result", "status"])
        w.writeheader()
        w.writerows(rows)
    return len(rows), sum(r["status"] == "pass" for r in rows)


def stage_data():
    """Check the files the template reads in the repo's data/output/ and count tests and matches.
    Nothing is copied or written: DataFolder points at <clone>\\data\\output\\ itself."""
    missing = [name for name in CSV_FROM_REPO if not (DATA_DIR / name).is_file()]
    assert not missing, f"missing in {DATA_DIR}: {missing}"
    with (DATA_DIR / "test_results.csv").open(encoding="utf-8") as f:
        tests = list(csv.DictReader(f))
    STATS["tests"] = (sum(r["status"].upper() == "PASS" for r in tests), len(tests))
    with (DATA_DIR / "reconciliation.csv").open(encoding="utf-8") as f:
        recs = list(csv.DictReader(f))
    STATS["rec"] = (sum(r["verdict"].upper().startswith("MATCH") for r in recs), len(recs))
    print(f"reading {len(CSV_FROM_REPO)} CSV files from {DATA_DIR} (tests: {STATS['tests'][0]}/{STATS['tests'][1]} pass)")


# ---------------------------------------------------------------------------------------------
# 2. Model (DataModelSchema, TMSL JSON)
# ---------------------------------------------------------------------------------------------
M_TYPES = {"string": "type text", "double": "type number", "int64": "Int64.Type",
           "dateTime": "type datetime", "boolean": "type logical"}

# Existing Snowflake tables: same model columns, new CSV source. (file, {CSV upper name: model name})
CSV_FOR_EXISTING = {
    "DIM_UTILITY": ("dim_utility.csv", {}),
    "FCT_RELIABILITY": ("fct_reliability.csv", {"CUSTOMERS": "Customers Served"}),
    "V_GROUP_INDEX": ("v_group_index.csv", {}),
    "V_STORM_VS_SAIDI": ("storm_vs_saidi.csv", {}),
    "SAIDI_WEATHER_ADJUSTED": ("saidi_weather_adjusted.csv", {}),
    "DOM_LOAD_ANNUAL": ("dom_load_annual.csv", {}),
    "DOM_TOP50_HOURS": ("dom_top50_hours.csv", {}),
    "DOM_LOAD_PROFILE": ("dom_load_profile.csv", {}),
}
EXTRA_COLUMNS = {"V_STORM_VS_SAIDI": [("SEVERE_GUST_DAYS", "double")]}

# New tables (P2 pages, Data notes). (file, [(column, type)])
NEW_TABLES = {
    "COUNTY_OUTAGE_MAP": ("county_outage_map.csv", [
        ("COUNTY_FIPS", "string"), ("COUNTY_LABEL", "string"), ("DOMINION_ONLY_COUNTY", "boolean"),
        ("CUSTOMERS_BASIS", "int64"), ("MAP_FLAG", "string"), ("READINGS_2015_24", "double"),
        ("MINUTES_NON_MED_AVG_2015_24", "double"), ("EVENTS_PER_10K_AVG_2015_24", "double"),
        ("EVENTS_PER_10K_2015_19", "double"), ("EVENTS_PER_10K_2020_24", "double"),
        ("STORM_DAYS_AVG_2015_24", "double")]),
    "OUTAGE_EVENTS_TOP10": ("outage_events_top10.csv", [
        ("RANK", "int64"), ("EVENT_KEY", "string"), ("START_DAY", "dateTime"), ("PEAK_DAY", "dateTime"),
        ("STORM_TYPE", "string"), ("TROPICAL_CYCLONE", "string"), ("PEAK_CUSTOMERS_OUT", "double"),
        ("PEAK_SUSTAINED_1H", "double"), ("HOURS_ABOVE_10K", "double"), ("CUSTOMER_HOURS", "double"),
        ("HOURS_TO_50PCT", "double"), ("HOURS_TO_90PCT", "double"), ("HOURS_TO_99PCT", "double"),
        ("DOE417_CUSTOMERS_MAX", "double"), ("STARTS_ON_MED_PROXY_DAY", "boolean")]),
    "RESTORATION_CURVE": ("fct_restoration_curve.csv", [
        ("EVENT_KEY", "string"), ("PEAK_UTC", "dateTime"), ("PEAK_CUSTOMERS_OUT", "double"),
        ("BACKGROUND_CUSTOMERS_OUT", "double"), ("HOUR_SINCE_PEAK", "double"), ("CUSTOMERS_OUT", "double"),
        ("SHARE_RESTORED", "double")]),
    "DOM_LOAD_HOUR_MONTH": ("dom_load_hour_month.csv", [
        ("YEAR", "int64"), ("MONTH", "int64"), ("HOUR_NO", "int64"), ("AVG_MW", "double"),
        ("MAX_MW", "double"), ("HOURS_REPORTED", "int64")]),
    "DOM_SEASONAL_PEAK": ("dom_seasonal_peak.csv", [
        ("YEAR", "int64"), ("SEASON", "string"), ("PEAK_MW", "double"), ("PEAK_DATE", "dateTime"),
        ("PEAK_HOUR_NO", "int64"), ("HOURS_REPORTED", "int64")]),
    "FCT_SALES_SECTOR": ("fct_sales_sector.csv", [
        ("YEAR", "int64"), ("CUSTOMER_CLASS", "string"), ("SALES_MWH", "double"), ("CUSTOMERS", "double"),
        ("REVENUE_USD", "double"), ("MWH_PER_CUSTOMER", "double"), ("DELIVERY_ONLY_MWH", "double")]),
    "Tests": ("test_results.csv", [
        ("TEST", "string"), ("TEST_NO", "int64"), ("SQL_FILE", "string"), ("DESCRIPTION", "string"),
        ("EXPECTED", "string"), ("ROWS_RETURNED", "int64"), ("OBSERVED_VALUE", "string"), ("STATUS", "string")]),
    "Reconciliation": ("reconciliation.csv", [
        ("ROW_NO", "int64"), ("METRIC", "string"), ("REBUILT", "double"), ("REPORTED", "double"),
        ("DIFFERENCE", "double"), ("REPORTED_DECIMALS", "int64"), ("REPORTED_SOURCE", "string"), ("VERDICT", "string")]),
}
DELETE_TABLES = ["Headline", "V_STORM_VS_SAIDI (2)", "V_TREND", "STORM_INDEX", "AmiEventStudy", "Tests"]
# Former workbook sheets, now CSV exports in data/output/ (D, a810494). Model column names stay lower case.
EXCEL_CSV = {"LoadGrowth": "load_growth.csv", "Programmes2025": "programmes_2025.csv"}
EXCEL_DROP_COLUMNS = {"LoadGrowth": ["Column9", "Source"]}   # empty and note columns of the old sheet

NEW_CALC_COLUMNS = {
    "OUTAGE_EVENTS_TOP10": [(
        "Event", "string",
        'FORMAT(OUTAGE_EVENTS_TOP10[PEAK_DAY], "mmm d, yyyy") & " " & '
        'IF(ISBLANK(OUTAGE_EVENTS_TOP10[TROPICAL_CYCLONE]), OUTAGE_EVENTS_TOP10[STORM_TYPE], '
        '"tropical (" & UPPER(LEFT(OUTAGE_EVENTS_TOP10[TROPICAL_CYCLONE], 1)) & '
        'LOWER(MID(OUTAGE_EVENTS_TOP10[TROPICAL_CYCLONE], 2, 40)) & ")")')],
}
DISPLAY_NAME_EXPR = (
    'SWITCH(DIM_UTILITY[UTILITY_KEY], "19876|VA", "Dominion Energy Virginia", "17539|SC", "Dominion Energy SC", '
    '"5416|NC", "Duke Carolinas (NC)", "3046|NC", "Duke Progress (NC)", "7140|GA", "Georgia Power", '
    '"195|AL", "Alabama Power", "6455|FL", "Duke Energy Florida", "6452|FL", "FPL", "1167|MD", "BGE", '
    '"15270|MD", "Pepco (MD)", "14940|PA", "PECO", "14715|PA", "PPL Electric", '
    '"733|VA", "Appalachian Power (VA)", DIM_UTILITY[UTILITY_NAME])')

# Measures: (table, name, expression, formatString or None, description, hidden)
MEASURES = [
    # FCT_RELIABILITY: core indices (sum numerators, sum denominators, divide once)
    ("FCT_RELIABILITY", "Total Customers", "SUM(FCT_RELIABILITY[Customers Served])", None,
     "Customers served in the rows in context. Denominator of every index.", False),
    ("FCT_RELIABILITY", "SAIDI ex MED", "DIVIDE(SUM(FCT_RELIABILITY[CUST_MINUTES_EX_MED]), [Total Customers])", "0.0",
     "Outage minutes per customer excluding major event days, customer-weighted: summed customer-minutes over summed customers.", False),
    ("FCT_RELIABILITY", "SAIFI ex MED", "DIVIDE(SUM(FCT_RELIABILITY[CUST_INTERRUPTIONS_EX_MED]), [Total Customers])", "0.000",
     "Sustained interruptions per customer excluding major event days, customer-weighted.", False),
    ("FCT_RELIABILITY", "CAIDI ex MED", "DIVIDE([SAIDI ex MED], [SAIFI ex MED])", "0.0",
     "Minutes per interruption excluding major event days: a ratio of the two indices (SAIDI / SAIFI), not a restoration time. SAIDI = SAIFI x CAIDI.", False),
    ("FCT_RELIABILITY", "SAIDI all events", "DIVIDE(SUM(FCT_RELIABILITY[CUST_MINUTES_ALL]), [Total Customers])", "0.0",
     "Outage minutes per customer including major event days.", False),
    ("FCT_RELIABILITY", "Major-event-day SAIDI", "[SAIDI all events] - [SAIDI ex MED]", "0.0",
     "Minutes per customer on major event days: the EIA reporting difference, not a measure of NOAA storm damage.", False),
    ("FCT_RELIABILITY", "Major-event-day share", "DIVIDE([Major-event-day SAIDI], [SAIDI all events])", "0%",
     "Share of all-event outage minutes that fell on major event days, customer-weighted (replaces the old sum of row ratios).", False),
    ("FCT_RELIABILITY", "Storm SAIDI", "[Major-event-day SAIDI]", "0.0",
     "Legacy alias of Major-event-day SAIDI, kept so older visuals do not break.", True),
    ("FCT_RELIABILITY", "Storm share", "[Major-event-day share]", "0%",
     "Legacy alias of Major-event-day share, kept so older visuals do not break.", True),
    ("FCT_RELIABILITY", "SAIDI 3yr ending 2025",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025})", "0.0",
     "Mean of the 2023-2025 annual SAIDI ex MED values (Dominion's 3-year definition). Annual report: 133.", False),
    ("FCT_RELIABILITY", "SAIDI 3yr ending 2024",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2022, 2023, 2024})", "0.0",
     "Mean of the 2022-2024 annual SAIDI ex MED values. Annual report: 130.", False),
    ("FCT_RELIABILITY", "SAIDI 2015 to 2017",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2015, 2016, 2017})", "0.0",
     "Peer table: mean annual SAIDI ex MED 2015-2017.", False),
    ("FCT_RELIABILITY", "SAIDI 2023 to 2025",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025})", "0.0",
     "Peer bars and table: mean annual SAIDI ex MED 2023-2025.", False),
    ("FCT_RELIABILITY", "SAIDI change %", "DIVIDE([SAIDI 2023 to 2025], [SAIDI 2015 to 2017]) - 1", "0.0%",
     "Change in mean SAIDI ex MED from 2015-2017 to 2023-2025.", False),
    ("FCT_RELIABILITY", "SAIFI 5yr",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [SAIFI ex MED]), FCT_RELIABILITY[YEAR] IN {2021, 2022, 2023, 2024, 2025})", "0.000",
     "Mean annual SAIFI ex MED 2021-2025 (peer scatter x-axis).", False),
    ("FCT_RELIABILITY", "CAIDI 5yr",
     "CALCULATE(AVERAGEX(VALUES(FCT_RELIABILITY[YEAR]), [CAIDI ex MED]), FCT_RELIABILITY[YEAR] IN {2021, 2022, 2023, 2024, 2025})", "0.0",
     "Mean annual CAIDI ex MED 2021-2025 (peer scatter y-axis).", False),
    ("FCT_RELIABILITY", "SAIFI 5yr quadrant", "IF([SAIFI 5yr] > {MED_SAIFI} && [CAIDI 5yr] > {MED_CAIDI}, [SAIFI 5yr])", "0.000",
     "SAIFI 5yr shown only above both medians of the 11 peers, Dominion excluded (top-right quadrant).", False),
    ("FCT_RELIABILITY", "CAIDI 5yr quadrant", "IF([SAIFI 5yr] > {MED_SAIFI} && [CAIDI 5yr] > {MED_CAIDI}, [CAIDI 5yr])", "0.0",
     "CAIDI 5yr shown only above both medians of the 11 peers, Dominion excluded (top-right quadrant).", False),
    ("FCT_RELIABILITY", "SAIDI change 2019 to 2023",
     "DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2023), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2019)) - 1", "0.0%",
     "SAIDI ex MED change 2019 to 2023.", False),
    ("FCT_RELIABILITY", "Frequency share 2019 to 2023",
     "DIVIDE(LN(DIVIDE(CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2023), CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2019))), "
     "LN(DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2023), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2019))))", "0%",
     "Share of the 2019-2023 SAIDI change from frequency: ln(SAIFI ratio) / ln(SAIDI ratio).", False),
    ("FCT_RELIABILITY", "SAIDI change 2023 to 2025",
     "DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2023)) - 1", "0.0%",
     "SAIDI ex MED change 2023 to 2025.", False),
    ("FCT_RELIABILITY", "Frequency share 2023 to 2025",
     "DIVIDE(LN(DIVIDE(CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2023))), "
     "LN(DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2023))))", "0%",
     "Share of the 2023-2025 SAIDI change from frequency.", False),
    ("FCT_RELIABILITY", "SAIDI change 2022 to 2025",
     "DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2022)) - 1", "0.0%",
     "SAIDI ex MED change 2022 to 2025: the year the 3-year window dropped and the year it added.", False),
    ("FCT_RELIABILITY", "Frequency share 2022 to 2025",
     "DIVIDE(LN(DIVIDE(CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2022))), "
     "LN(DIVIDE(CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = 2022))))", "0%",
     "Share of the 2022-2025 SAIDI change from frequency (above 100% because CAIDI fell).", False),
    ("FCT_RELIABILITY", "SAIFI change 2019 to 2025",
     "DIVIDE(CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = 2019)) - 1", "0.0%",
     "SAIFI ex MED change 2019 to 2025 (title: up 6%).", False),
    ("FCT_RELIABILITY", "CAIDI change 2019 to 2025",
     "DIVIDE(CALCULATE([CAIDI ex MED], FCT_RELIABILITY[YEAR] = 2025), CALCULATE([CAIDI ex MED], FCT_RELIABILITY[YEAR] = 2019)) - 1", "0.0%",
     "CAIDI ex MED change 2019 to 2025 (title: down 9%).", False),
    ("FCT_RELIABILITY", "Method",
     'VAR s = CALCULATE(IF(DISTINCTCOUNT(FCT_RELIABILITY[STANDARD]) > 1, "Changed", MAX(FCT_RELIABILITY[STANDARD])), '
     'FCT_RELIABILITY[YEAR] >= 2014)\n'
     'RETURN IF(s = "Other", "Own rule", s)', None,
     "How the utility excluded major events in 2014-2025, the years compared: IEEE 1366, or its own rule (EIA's "
     "\"Other\"). Ten of the twelve filed IEEE 1366 every year; Dominion and Alabama Power filed \"Other\". Georgia "
     "Power and Duke Energy Florida filed \"Other\" in 2013 only.", False),
    ("FCT_RELIABILITY", "SAIFI label", "IF(SELECTEDVALUE(FCT_RELIABILITY[YEAR]) IN {2019, 2023, 2025}, [SAIFI ex MED])", "0.00",
     "Point label: SAIFI shown only for 2019, 2023 and 2025.", False),
    ("FCT_RELIABILITY", "CAIDI label", "IF(SELECTEDVALUE(FCT_RELIABILITY[YEAR]) IN {2019, 2023, 2025}, [CAIDI ex MED])", "0.0",
     "Point label: CAIDI shown only for 2019, 2023 and 2025.", False),
    ("FCT_RELIABILITY", "Change colour",
     'IF([SAIDI change %] > 0, "#B23B3B", IF([SAIDI change %] < 0, "#2E7D32", "#333333"))', None,
     "Font color for the change column: increase red, decrease green.", False),
    # DIM_UTILITY
    ("DIM_UTILITY", "Bar colour",
     f'IF(SELECTEDVALUE(DIM_UTILITY[Display name]) = "Dominion Energy Virginia", "{SUBJECT}", "{CONTEXT}")', None,
     "Bar color: Dominion in the subject blue, peers in gray.", False),
    ("DIM_UTILITY", "Row colour",
     'IF(SELECTEDVALUE(DIM_UTILITY[Display name]) = "Dominion Energy Virginia", "#E8F0FB", "#FFFFFF")', None,
     "Table row background: Dominion's row lightly tinted.", False),
    # V_GROUP_INDEX
    ("V_GROUP_INDEX", "SAIFI index 2015",
     "VAR CurrentValue = SELECTEDVALUE(V_GROUP_INDEX[SAIFI_EX_MED])\n"
     "VAR Base2015 = CALCULATE(MAX(V_GROUP_INDEX[SAIFI_EX_MED]), REMOVEFILTERS(V_GROUP_INDEX[YEAR]), V_GROUP_INDEX[YEAR] = 2015)\n"
     "RETURN IF(HASONEVALUE(V_GROUP_INDEX[YEAR]) && HASONEVALUE(V_GROUP_INDEX[PEER_GROUP]), DIVIDE(CurrentValue, Base2015) * 100)",
     "0", "SAIFI ex MED indexed to 2015 = 100, for one year and one group; blank otherwise (never sums ratios).", False),
    ("V_GROUP_INDEX", "Index label", "IF(SELECTEDVALUE(V_GROUP_INDEX[YEAR]) = 2025, [SAIFI index 2015])", "0",
     "Point label: index shown only for 2025.", False),
    # V_STORM_VS_SAIDI
    ("V_STORM_VS_SAIDI", "Storm county-days", "SELECTEDVALUE(V_STORM_VS_SAIDI[STORM_COUNTY_DAYS])", "#,0",
     "NOAA storm county-days in Dominion's Virginia counties for one year (blank across years).", False),
    ("V_STORM_VS_SAIDI", "SAIDI ex MED (weather table)", "SELECTEDVALUE(V_STORM_VS_SAIDI[SAIDI_EX_MED])", "0.0",
     "SAIDI ex MED for one year, from the weather table (scatter y-axis).", False),
    ("V_STORM_VS_SAIDI", "Wind days", "SUM(V_STORM_VS_SAIDI[WIND_DAYS])", "#,0",
     "Storm county-days with a damaging-wind report (additive across years).", False),
    ("V_STORM_VS_SAIDI", "Winter days", "SUM(V_STORM_VS_SAIDI[WINTER_DAYS])", "#,0",
     "Storm county-days with a winter-storm report (additive across years).", False),
    ("V_STORM_VS_SAIDI", "Tropical days", "SUM(V_STORM_VS_SAIDI[TROPICAL_DAYS])", "#,0",
     "Storm county-days with a tropical report (additive across years).", False),
    ("V_STORM_VS_SAIDI", "Dot colour", f'IF(SELECTEDVALUE(V_STORM_VS_SAIDI[YEAR]) = 2025, "{SUBJECT}", "{CONTEXT}")', None,
     "Scatter dot color: 2025 in the subject blue.", False),
    # SAIDI_WEATHER_ADJUSTED
    ("SAIDI_WEATHER_ADJUSTED", "Actual SAIDI", "SELECTEDVALUE(SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED])", "0.0",
     "Reported SAIDI ex MED for one year.", False),
    ("SAIDI_WEATHER_ADJUSTED", "Weather-adjusted SAIDI", "SELECTEDVALUE(SAIDI_WEATHER_ADJUSTED[WEATHER_ADJUSTED_SAIDI])", "0.0",
     "SAIDI ex MED minus the storm-day prediction plus the 2015-2024 mean: a model estimate, not an observed value.", False),
    ("SAIDI_WEATHER_ADJUSTED", "Weather-predicted 2025",
     "CALCULATE(SUM(SAIDI_WEATHER_ADJUSTED[PREDICTED_FROM_WEATHER]), SAIDI_WEATHER_ADJUSTED[YEAR] = 2025)", "0.0",
     "2025 SAIDI predicted from 2025 storm days by the 2015-2024 fit (2025 was not in the fit).", False),
    ("SAIDI_WEATHER_ADJUSTED", "Actual 2025",
     "CALCULATE(SUM(SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED]), SAIDI_WEATHER_ADJUSTED[YEAR] = 2025)", "0.0",
     "Reported 2025 SAIDI ex MED.", False),
    ("SAIDI_WEATHER_ADJUSTED", "Adjusted label",
     "IF(SELECTEDVALUE(SAIDI_WEATHER_ADJUSTED[YEAR]) IN {2015, 2019, 2025}, [Weather-adjusted SAIDI])", "0.0",
     "Point label: adjusted value shown only for 2015, 2019 and 2025.", False),
    # DOM_LOAD_ANNUAL, DOM_TOP50_HOURS, DOM_LOAD_PROFILE (EIA-930, PJM DOM zone)
    ("DOM_LOAD_ANNUAL", "Floor MW", "MIN(DOM_LOAD_ANNUAL[FLOOR_MW])", "#,0",
     "Lowest hourly demand in the year (an extreme, never summed).", False),
    ("DOM_LOAD_ANNUAL", "Peak MW", "MAX(DOM_LOAD_ANNUAL[PEAK_MW])", "#,0",
     "Highest hourly demand in the year.", False),
    ("DOM_LOAD_ANNUAL", "Winter peak MW", "MAX(DOM_LOAD_ANNUAL[WINTER_PEAK_MW])", "#,0",
     "Highest hour in Dec, Jan and Feb of the same calendar year.", False),
    ("DOM_LOAD_ANNUAL", "Summer peak MW", "MAX(DOM_LOAD_ANNUAL[SUMMER_PEAK_MW])", "#,0",
     "Highest hour in Jun, Jul and Aug.", False),
    ("DOM_LOAD_ANNUAL", "Floor growth 2019 to 2025",
     "DIVIDE(CALCULATE([Floor MW], DOM_LOAD_ANNUAL[YEAR] = 2025), CALCULATE([Floor MW], DOM_LOAD_ANNUAL[YEAR] = 2019)) - 1", "0%",
     "Change in the year's lowest hour, 2019 to 2025.", False),
    ("DOM_LOAD_ANNUAL", "Peak growth 2019 to 2025",
     "DIVIDE(CALCULATE([Peak MW], DOM_LOAD_ANNUAL[YEAR] = 2025), CALCULATE([Peak MW], DOM_LOAD_ANNUAL[YEAR] = 2019)) - 1", "0%",
     "Change in the year's highest hour, 2019 to 2025.", False),
    ("DOM_TOP50_HOURS", "Top 50 hours in 2025",
     "CALCULATE(COUNTROWS(DOM_TOP50_HOURS), DOM_TOP50_HOURS[RANK_END_2025] <= 50, DOM_TOP50_HOURS[YEAR] = 2025)", "0",
     "Of the 50 highest hours on record to Dec 31, 2025, the number that fell in 2025.", False),
    ("DOM_LOAD_PROFILE", "Hour growth %", "SELECTEDVALUE(DOM_LOAD_PROFILE[GROWTH_PCT])", '0.0"%"',
     "Change in average demand for one hour of the day, 2019 to 2025 (percent).", False),
    ("DOM_LOAD_PROFILE", "Average MW 2019", "SELECTEDVALUE(DOM_LOAD_PROFILE[AVG_MW_2019])", "#,0",
     "Average demand in one hour of the day, 2019.", False),
    ("DOM_LOAD_PROFILE", "Average MW 2025", "SELECTEDVALUE(DOM_LOAD_PROFILE[AVG_MW_2025])", "#,0",
     "Average demand in one hour of the day, 2025.", False),
    ("DOM_LOAD_PROFILE", "Hour colour",
     "VAR h = SELECTEDVALUE(DOM_LOAD_PROFILE[HOUR_NO])\nRETURN SWITCH(TRUE(), h >= 1 && h <= 5, \"" + SUBJECT + "\", "
     "h >= 13 && h <= 17, \"" + GOLD + "\", \"" + CONTEXT + "\")", None,
     "Column color by the hours the title names: hours ending 1-5 a.m. blue, 1-5 p.m. gold, the rest gray.", False),
    # Workbook tables
    ("Programmes2025", "Smart meter share %", "SELECTEDVALUE(Programmes2025[smart_meter_share]) * 100", "0.0",
     "Smart meters as a percent of all meters, one utility (a share is never summed).", False),
    ("Programmes2025", "Time-varying rate %", "SELECTEDVALUE(Programmes2025[time_varying_rate_share_pct])", "0.0",
     "Percent of customers on a time-varying rate, one utility.", False),
    ("LoadGrowth", "Commercial sales index", "SELECTEDVALUE(LoadGrowth[commercial_sales_index])", "0",
     "Commercial sales, 2013 = 100, one year.", False),
    ("LoadGrowth", "Commercial customers index", "SELECTEDVALUE(LoadGrowth[commercial_customers_index])", "0",
     "Commercial customers, 2013 = 100, one year.", False),
    ("LoadGrowth", "Residential sales index", "SELECTEDVALUE(LoadGrowth[residential_sales_index])", "0",
     "Residential sales, 2013 = 100, one year.", False),
    ("LoadGrowth", "Sales label", "IF(SELECTEDVALUE(LoadGrowth[year]) = 2025, [Commercial sales index])", "0",
     "Point label: commercial index shown only for 2025.", False),
    # New tables
    ("COUNTY_OUTAGE_MAP", "Non-major outage minutes",
     'CALCULATE(AVERAGE(COUNTY_OUTAGE_MAP[MINUTES_NON_MED_AVG_2015_24]), COUNTY_OUTAGE_MAP[MAP_FLAG] = "ok")', "0",
     "Outage minutes per customer a year on days that are not major event days, 2015-2024 average (EAGLE-I, all utilities "
     "in the county). Blank for the 4 counties flagged for unreliable data.", False),
    ("COUNTY_OUTAGE_MAP", "Non-major outage minutes, 20k+ counties",
     'CALCULATE([Non-major outage minutes], COUNTY_OUTAGE_MAP[CUSTOMERS_BASIS] >= 20000)', "0",
     "Non-major outage minutes for counties with 20,000 or more customers (the comparison rule in the county analysis).", False),
    ("COUNTY_OUTAGE_MAP", "Outage events per 10k customers",
     'CALCULATE(AVERAGE(COUNTY_OUTAGE_MAP[EVENTS_PER_10K_AVG_2015_24]), COUNTY_OUTAGE_MAP[MAP_FLAG] = "ok")', "0.0",
     "Non-major outage events per 10,000 customers a year, 2015-2024 average. Blank for flagged counties.", False),
    ("OUTAGE_EVENTS_TOP10", "Peak customers out", "MAX(OUTAGE_EVENTS_TOP10[PEAK_CUSTOMERS_OUT])", "#,0",
     "Highest count of customers out in any 15-minute EAGLE-I reading of the event (all utilities in the 103 counties).", False),
    ("OUTAGE_EVENTS_TOP10", "Peak customers out (held 1 h)", "MAX(OUTAGE_EVENTS_TOP10[PEAK_SUSTAINED_1H])", "#,0",
     "Highest count of customers out that held for at least one hour (the ranking rule for the ten events).", False),
    ("OUTAGE_EVENTS_TOP10", "Hours to clear 90%", "MAX(OUTAGE_EVENTS_TOP10[HOURS_TO_90PCT])", "0.0",
     "Hours from the peak until customers out stayed at or below the pre-event level plus 10% of the peak's excess "
     "over it (a net count, all utilities). Not a utility's '% of affected customers restored'.", False),
    ("RESTORATION_CURVE", "Share restored", "AVERAGE(RESTORATION_CURVE[SHARE_RESTORED])", "0%",
     "Share of the outage cleared by each hour since the peak: (peak - customers out) / (peak - pre-event level); "
     "0 at the peak, 1 back to the pre-event level. A net count, all utilities.", False),
    ("DOM_LOAD_HOUR_MONTH", "Average MW", "AVERAGE(DOM_LOAD_HOUR_MONTH[AVG_MW])", "#,0",
     "Average hourly demand in the cells in context (hour x month x year).", False),
    ("DOM_SEASONAL_PEAK", "Seasonal peak MW", "MAX(DOM_SEASONAL_PEAK[PEAK_MW])", "#,0",
     "Highest hour of the season.", False),
    ("FCT_SALES_SECTOR", "Sales TWh", "DIVIDE(SUM(FCT_SALES_SECTOR[SALES_MWH]), 1000000)", "0.0",
     "Retail sales in TWh (bundled plus delivery-only), EIA-861.", False),
    # _Measures: year-slicer cards on the Summary page
    ("_Measures", "Selected SAIDI",
     "VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)\nRETURN CALCULATE([SAIDI ex MED], FCT_RELIABILITY[YEAR] = SelectedYear)", "0.0",
     "SAIDI ex MED for the year chosen in the Year slicer (2025 if none).", False),
    ("_Measures", "Selected SAIFI",
     "VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)\nRETURN CALCULATE([SAIFI ex MED], FCT_RELIABILITY[YEAR] = SelectedYear)", "0.000",
     "SAIFI ex MED for the year chosen in the Year slicer.", False),
    ("_Measures", "Selected CAIDI",
     "VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)\nRETURN CALCULATE([CAIDI ex MED], FCT_RELIABILITY[YEAR] = SelectedYear)", "0.0",
     "CAIDI ex MED for the year chosen in the Year slicer.", False),
    ("_Measures", "Selected Customers",
     "VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)\nRETURN CALCULATE([Total Customers], FCT_RELIABILITY[YEAR] = SelectedYear)", None,
     "Customers served in the year chosen in the Year slicer.", False),
    ("_Measures", "Selected major-event-day share",
     "VAR SelectedYear = SELECTEDVALUE('Dashboard Year'[Year], 2025)\nRETURN CALCULATE([Major-event-day share], FCT_RELIABILITY[YEAR] = SelectedYear)", "0%",
     "Major-event-day share of all-event minutes in the year chosen in the Year slicer.", False),
]

MEASURE_RENAMES = {
    ("FCT_RELIABILITY", "Share of outage mins caused by major storms"): ("FCT_RELIABILITY", "Major-event-day share"),
    ("FCT_RELIABILITY", "Storm SAIDI"): ("FCT_RELIABILITY", "Major-event-day SAIDI"),
    ("AmiEventStudy", "Selected SAIDI"): ("_Measures", "Selected SAIDI"),
    ("AmiEventStudy", "Selected SAIFI"): ("_Measures", "Selected SAIFI"),
    ("AmiEventStudy", "Selected CAIDI"): ("_Measures", "Selected CAIDI"),
    ("AmiEventStudy", "Selected Customers"): ("_Measures", "Selected Customers"),
    ("AmiEventStudy", "Selected Major Event Share"): ("_Measures", "Selected major-event-day share"),
}
AGG_TO_MEASURE = {
    ("FCT_RELIABILITY", "Customers Served"): ("FCT_RELIABILITY", "Total Customers"),
    ("FCT_RELIABILITY", "SAIFI_EX_MED"): ("FCT_RELIABILITY", "SAIFI ex MED"),
    ("SAIDI_WEATHER_ADJUSTED", "SAIDI_EX_MED"): ("SAIDI_WEATHER_ADJUSTED", "Actual SAIDI"),
    ("SAIDI_WEATHER_ADJUSTED", "WEATHER_ADJUSTED_SAIDI"): ("SAIDI_WEATHER_ADJUSTED", "Weather-adjusted SAIDI"),
    ("V_STORM_VS_SAIDI", "STORM_COUNTY_DAYS"): ("V_STORM_VS_SAIDI", "Storm county-days"),
    ("V_STORM_VS_SAIDI", "SAIDI_EX_MED"): ("V_STORM_VS_SAIDI", "SAIDI ex MED (weather table)"),
    ("LoadGrowth", "commercial_sales_index"): ("LoadGrowth", "Commercial sales index"),
    ("LoadGrowth", "commercial_customers_index"): ("LoadGrowth", "Commercial customers index"),
    ("LoadGrowth", "residential_sales_index"): ("LoadGrowth", "Residential sales index"),
    ("DOM_LOAD_PROFILE", "GROWTH_PCT"): ("DOM_LOAD_PROFILE", "Hour growth %"),
}


def m_csv(file, cols, renames=None, upper=True):
    """Power Query M for one CSV: promote headers, upper-case names (unless upper=False), rename, select,
    blank->null, type."""
    names = ", ".join(json.dumps(c) for c, _ in cols)
    types = ", ".join("{" + json.dumps(c) + ", " + M_TYPES[t] + "}" for c, t in cols)
    lines = [
        "let",
        f'    Source = Csv.Document(File.Contents(DataFolder & "{file}"), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),',
        "    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),",
    ]
    prev = "Promoted"
    if upper:
        lines.append("    UpperNames = Table.TransformColumnNames(Promoted, Text.Upper),")
        prev = "UpperNames"
    if renames:
        pairs = ", ".join("{" + json.dumps(a) + ", " + json.dumps(b) + "}" for a, b in renames.items())
        lines.append(f"    Renamed = Table.RenameColumns(UpperNames, {{{pairs}}}),")
        prev = "Renamed"
    lines += [
        f"    Selected = Table.SelectColumns({prev}, {{{names}}}),",
        '    Blanks = Table.ReplaceValue(Selected, "", null, Replacer.ReplaceValue, Table.ColumnNames(Selected)),',
        f'    Typed = Table.TransformColumnTypes(Blanks, {{{types}}}, "en-US")',
        "in",
        "    Typed",
    ]
    return lines


def new_column(name, dtype):
    is_num = dtype in ("double", "int64")
    key_like = any(k in name for k in ("YEAR", "MONTH", "HOUR", "RANK", "FIPS", "_ID"))
    return {"name": name, "dataType": dtype, "sourceColumn": name, "lineageTag": uid(),
            "summarizeBy": "sum" if is_num and not key_like else "none",
            **({"formatString": "0"} if dtype == "int64" else {}),
            "annotations": [{"name": "SummarizationSetBy", "value": "Automatic"}]}


def build_model(data_folder):
    raw = (SRC / "DataModelSchema").read_bytes()
    db = json.loads(raw.decode("utf-16-le").lstrip("\ufeff"))
    model = db["model"]
    tables = {t["name"]: t for t in model["tables"]}
    old_lineage = {name: t.get("lineageTag") for name, t in tables.items()}
    old_measure_tags = {(t["name"], m["name"]): m.get("lineageTag") for t in model["tables"] for m in t.get("measures", [])}

    # existing Snowflake tables -> CSV import
    for tname, (file, renames) in CSV_FOR_EXISTING.items():
        t = tables[tname]
        for c in t["columns"]:
            c.pop("sourceProviderType", None)
        for cname, dtype in EXTRA_COLUMNS.get(tname, []):
            t["columns"].append(new_column(cname, dtype))
        data_cols = [(c["sourceColumn"], c["dataType"]) for c in t["columns"] if c.get("type") not in ("calculated", "calculatedTableColumn")]
        t["partitions"] = [{"name": tname, "mode": "import", "source": {"type": "m", "expression": m_csv(file, data_cols, renames)}}]
        t["annotations"] = [{"name": "PBI_ResultType", "value": "Table"}]
    # former workbook sheets -> their CSV exports in data/output/ (same lower-case column names)
    for tname, file in EXCEL_CSV.items():
        t = tables[tname]
        drop = EXCEL_DROP_COLUMNS.get(tname, [])
        t["columns"] = [c for c in t["columns"] if c["name"] not in drop]
        for c in t["columns"]:
            c.pop("sourceProviderType", None)
        cols = [(c["sourceColumn"], c["dataType"]) for c in t["columns"] if c.get("type") not in ("calculated", "calculatedTableColumn")]
        with (DATA_DIR / file).open(encoding="utf-8") as f:
            header = next(csv.reader(f))
        assert [c for c, _ in cols] == header, (tname, cols, header)
        t["partitions"] = [{"name": tname, "mode": "import", "source": {"type": "m", "expression": m_csv(file, cols, upper=False)}}]
        t["annotations"] = [{"name": "PBI_ResultType", "value": "Table"}]
    # Display name: add Appalachian Power (VA), as in the repo
    for c in tables["DIM_UTILITY"]["columns"]:
        if c["name"] == "Display name":
            c["expression"] = DISPLAY_NAME_EXPR
    # delete tables
    for tname in DELETE_TABLES:
        tables.pop(tname, None)
    # new tables
    for tname, (file, cols) in NEW_TABLES.items():
        t = {"name": tname, "lineageTag": old_lineage.get(tname) or uid(),
             "columns": [new_column(c, d) for c, d in cols],
             "partitions": [{"name": tname, "mode": "import", "source": {"type": "m", "expression": m_csv(file, cols)}}],
             "annotations": [{"name": "PBI_ResultType", "value": "Table"}]}
        for cname, dtype, expr in NEW_CALC_COLUMNS.get(tname, []):
            t["columns"].append({"type": "calculated", "name": cname, "dataType": dtype, "isDataTypeInferred": True,
                                 "expression": expr, "lineageTag": uid(), "summarizeBy": "none",
                                 "annotations": [{"name": "SummarizationSetBy", "value": "Automatic"}]})
        tables[tname] = t
    for c in tables["Tests"]["columns"]:
        if c["name"] == "TEST":
            c["sortByColumn"] = "TEST_NO"
        if c["name"] == "TEST_NO":
            c["isHidden"] = True
    for c in tables["Reconciliation"]["columns"]:
        if c["dataType"] == "double":
            c["formatString"] = "#,0.###"
        if c["name"] == "ROW_NO":
            c["summarizeBy"] = "none"
    for c in tables["OUTAGE_EVENTS_TOP10"]["columns"]:
        if c["name"] in ("PEAK_CUSTOMERS_OUT", "PEAK_SUSTAINED_1H", "CUSTOMER_HOURS", "DOE417_CUSTOMERS_MAX"):
            c["formatString"] = "#,0"
        if c["name"].startswith("HOURS_"):
            c["formatString"] = "0.0"
    # _Measures: calculated one-row table with a hidden column
    tables["_Measures"] = {
        "name": "_Measures", "lineageTag": uid(),
        "columns": [{"type": "calculatedTableColumn", "name": "Measures", "dataType": "int64", "isNameInferred": True,
                     "isDataTypeInferred": True, "isHidden": True, "sourceColumn": "[Measures]", "lineageTag": uid(),
                     "summarizeBy": "none", "annotations": [{"name": "SummarizationSetBy", "value": "Automatic"}]}],
        "partitions": [{"name": "_Measures", "mode": "import", "source": {"type": "calculated", "expression": 'ROW("Measures", 0)'}}],
    }
    # measures: replace all with the spec (keep lineage tags where the name survives)
    for t in tables.values():
        t["measures"] = []
    used_tags = set()
    med_saifi, med_caidi = peer_medians()
    for (tname, mname, expr, fmt, desc, hidden) in MEASURES:
        expr = expr.replace("{MED_SAIFI}", f"{med_saifi:g}").replace("{MED_CAIDI}", f"{med_caidi:g}")
        tag = old_measure_tags.get((tname, mname))
        if not tag or tag in used_tags:
            tag = uid()
        used_tags.add(tag)
        m = {"name": mname, "expression": expr.split("\n") if "\n" in expr else expr, "lineageTag": tag, "description": desc}
        if fmt:
            m["formatString"] = fmt
        if hidden:
            m["isHidden"] = True
        tables[tname]["measures"].append(m)
    for t in tables.values():
        if not t["measures"]:
            del t["measures"]
    # order: data tables first, then helpers
    order = ["FCT_RELIABILITY", "DIM_UTILITY", "V_GROUP_INDEX", "V_STORM_VS_SAIDI", "SAIDI_WEATHER_ADJUSTED",
             "COUNTY_OUTAGE_MAP", "OUTAGE_EVENTS_TOP10", "RESTORATION_CURVE", "LoadGrowth", "Programmes2025",
             "DOM_LOAD_ANNUAL", "DOM_TOP50_HOURS", "DOM_LOAD_PROFILE", "DOM_LOAD_HOUR_MONTH", "DOM_SEASONAL_PEAK",
             "FCT_SALES_SECTOR", "Tests", "Reconciliation", "Dashboard Year", "_Measures"]
    assert set(order) == set(tables), set(order) ^ set(tables)
    model["tables"] = [tables[n] for n in order]
    # relationships: keep FCT->DIM; drop Headline; add curve -> top-10 events
    model["relationships"] = [r for r in model["relationships"] if r["fromTable"] in tables and r["toTable"] in tables]
    model["relationships"].append({"name": uid(), "fromTable": "RESTORATION_CURVE", "fromColumn": "EVENT_KEY",
                                   "toTable": "OUTAGE_EVENTS_TOP10", "toColumn": "EVENT_KEY"})
    # parameter
    m_value = '"' + data_folder.replace('"', '""') + '" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]'
    model["expressions"] = [{"name": "DataFolder", "kind": "m", "expression": m_value, "lineageTag": uid(),
                             "description": "The repo's data\\output\\ folder, which holds every CSV file the report reads; must end with a backslash.",
                             "annotations": [{"name": "PBI_NavigationStepName", "value": "Navigation"},
                                             {"name": "PBI_ResultType", "value": "Text"}]}]
    # model annotations: query order, auto date/time off; drop generated Q&A metadata
    ann = {a["name"]: a for a in model.get("annotations", [])}
    query_order = ["DataFolder"] + [n for n in order if n not in ("Dashboard Year", "_Measures")]
    ann["PBI_QueryOrder"] = {"name": "PBI_QueryOrder", "value": json.dumps(query_order)}
    ann["__PBI_TimeIntelligenceEnabled"] = {"name": "__PBI_TimeIntelligenceEnabled", "value": "0"}
    model["annotations"] = list(ann.values())
    model["cultures"] = [{"name": c["name"]} for c in model.get("cultures", [])]
    return db


def prune_diagram(raw_bytes, keep):
    d = json.loads(raw_bytes.decode("utf-16-le").lstrip("\ufeff"))
    for dg in d.get("diagrams", []):
        dg["nodes"] = [n for n in dg.get("nodes", []) if n.get("nodeIndex") in keep]
    return json.dumps(d, ensure_ascii=False).encode("utf-16-le")


# ---------------------------------------------------------------------------------------------
# 3. Report (PBIR)
# ---------------------------------------------------------------------------------------------
P2 = "--no-p2" not in sys.argv
PAGES = {  # id: new display name, in the new order (F10); new pages get generated ids
    "e6f27ff89680632d5471": "Summary",
    "61745dccdb7948ee4977": "Scorecard",
    "2414a423c3820b09c17c": "What moved",
    "241c63d8c7e81067e9cc": "Weather",
    "39dca24cb135da967227": "Fair comparison",
    **({"NEW_COUNTY": "Outages by county", "NEW_STORMS": "Storms"} if P2 else {}),
    "4348e5cd66c9b48126f0": "Growth",
    "e8d8451399dc68c3ece6": "Demand and seasons",
    "ca36f3cced18c2313453": "Demand summary",
    "NEW_NOTES": "Data notes",
}
STATS = {}
NUMS = {}


def data_numbers():
    """Numbers used in titles, recomputed from the staged data so titles match the data."""
    out = {}
    with (DATA_DIR / "v_group_index.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    def saifi(group, year):
        return float(next(r["saifi_ex_med"] for r in rows if r["peer_group"] == group and int(r["year"]) == year))
    groups = sorted({r["peer_group"] for r in rows})
    out["groups"] = groups
    out["dom_2015_2025"] = saifi("Dominion Energy Virginia", 2025) / saifi("Dominion Energy Virginia", 2015) - 1
    out["coop_2015_2025"] = saifi("Virginia co-op", 2025) / saifi("Virginia co-op", 2015) - 1
    with (DATA_DIR / "dom_load_profile.csv").open(encoding="utf-8") as f:
        prof = {int(r["hour_no"]): float(r["growth_pct"]) for r in csv.DictReader(f)}
    out["night"] = (min(prof[h] for h in range(1, 6)), max(prof[h] for h in range(1, 6)))
    out["afternoon"] = (min(prof[h] for h in range(13, 18)), max(prof[h] for h in range(13, 18)))
    out["all_hours_up"] = min(prof.values()) > 0
    out["max_hour"] = max(prof, key=prof.get)
    # county map (map_flag = ok)
    with (DATA_DIR / "county_outage_map.csv").open(encoding="utf-8") as f:
        cm = [r for r in csv.DictReader(f) if r["map_flag"] == "ok"]
    out["county_n"] = len(cm)
    cm = [r for r in cm if float(r["customers_basis"]) >= 20000]   # D's A3 rule: counties with 20,000+ customers
    hi = max(cm, key=lambda r: float(r["minutes_non_med_avg_2015_24"]))
    lo = min(cm, key=lambda r: float(r["minutes_non_med_avg_2015_24"]))
    out["county_n20k"] = len(cm)
    out["county_hi"] = (hi["county_label"], round(float(hi["minutes_non_med_avg_2015_24"])))
    out["county_lo"] = (lo["county_label"], round(float(lo["minutes_non_med_avg_2015_24"])))
    # ten largest events
    with (DATA_DIR / "outage_events_top10.csv").open(encoding="utf-8") as f:
        ev = list(csv.DictReader(f))
    out["ev_types"] = {t: sum(r["storm_type"] == t for r in ev) for t in sorted({r["storm_type"] for r in ev})}
    with (DATA_DIR / "fct_restoration_curve.csv").open(encoding="utf-8") as f:
        yrs = {r["event_key"].split("|")[-1][:4] for r in csv.DictReader(f)}
    out["ev_years"] = (min(yrs), max(yrs))   # the universe of territory events the ten are drawn from
    isaias = [r for r in ev if r["tropical_cyclone"].upper() == "ISAIAS"]
    assert len(isaias) == 1, isaias
    out["isaias_key"] = isaias[0]["event_key"]
    out["isaias_h90"] = float(isaias[0]["hours_to_90pct"])
    # storm types by year
    with (DATA_DIR / "storm_vs_saidi.csv").open(encoding="utf-8") as f:
        st = list(csv.DictReader(f))
    out["wind_top_years"] = sum(float(r["wind_days"]) >= max(float(r["winter_days"]), float(r["tropical_days"])) for r in st)
    out["storm_years"] = (min(r["year"] for r in st), max(r["year"] for r in st), len(st))
    # sales by sector 2013 -> 2025
    with (DATA_DIR / "fct_sales_sector.csv").open(encoding="utf-8") as f:
        ss = list(csv.DictReader(f))
    def sales(cls, yr):
        return sum(float(r["sales_mwh"]) for r in ss if r["customer_class"] == cls and int(r["year"]) == yr)
    out["sector_growth"] = {c: sales(c, 2025) / sales(c, 2013) - 1 for c in ("commercial", "residential", "industrial")}
    return out


def textbox(name, x, y, w, h, z, paragraphs):
    """paragraphs: list of (text, size_pt, colour, bold)."""
    paras = []
    for text, size, colour, bold in paragraphs:
        style = {"fontSize": f"{size}pt", "color": colour}
        if bold:
            style["fontWeight"] = "bold"
        paras.append({"textRuns": [{"value": text, "textStyle": style}]})
    return {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json",
            "name": name, "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
            "visual": {"visualType": "textbox", "objects": {"general": [{"properties": {"paragraphs": paras}}]},
                       "drillFilterOtherVisuals": True}}


def proj_col(entity, prop, display=None):
    p = {"field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
         "queryRef": f"{entity}.{prop}", "nativeQueryRef": display or prop}
    if display:
        p["displayName"] = display
    return p


def proj_measure(entity, prop, display=None):
    p = {"field": {"Measure": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
         "queryRef": f"{entity}.{prop}", "nativeQueryRef": display or prop}
    if display:
        p["displayName"] = display
    return p


def chart(name, vtype, x, y, w, h, z, roles, title, subtitle=None, objects=None, sort=None, filters=None):
    v = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.14.0/schema.json",
         "name": name, "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
         "visual": {"visualType": vtype, "query": {"queryState": {r: {"projections": p} for r, p in roles.items()}},
                    "visualContainerObjects": {"title": [{"properties": {"show": L("true"), "text": L(lit(title))}}]},
                    "drillFilterOtherVisuals": True}}
    if subtitle:
        v["visual"]["visualContainerObjects"]["subTitle"] = [{"properties": {"show": L("true"), "text": L(lit(subtitle))}}]
    if objects:
        v["visual"]["objects"] = objects
    if sort:
        v["visual"]["query"]["sortDefinition"] = {"sort": sort}
    if filters:
        v["filterConfig"] = {"filters": filters}
    return v


def straight(markers=True):
    """Straight segments between points (docs/06: smoothed lines imply values between observations)."""
    return [{"properties": {"lineChartType": L("'linear'"), "showMarker": L("true" if markers else "false")}}]


def categorical_filter(entity, prop, values, alias="t"):
    return {"name": hexid(), "field": {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
            "type": "Categorical",
            "filter": {"Version": 2, "From": [{"Name": alias, "Entity": entity, "Type": 0}],
                       "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": prop}}],
                                                       "Values": [[{"Literal": {"Value": v}}] for v in values]}}}]}}


def peer_medians():
    """SAIFI and CAIDI 2021-2025 medians of the 11 peers, Dominion excluded (the committed peer table)."""
    with (REPO / "data" / "output" / "peer_reliability_5yr.csv").open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    saifi = {r["median_saifi_2021_25_excl_dominion"] for r in rows}
    caidi = {r["median_caidi_2021_25_excl_dominion"] for r in rows}
    assert len(rows) == 12 and len(saifi) == 1 and len(caidi) == 1, (len(rows), saifi, caidi)
    return float(saifi.pop()), float(caidi.pop())


def storm_fit(first=2015, last=2024):
    """OLS of SAIDI ex MED on storm county-days over the fit years, from the staged storm_vs_saidi.csv."""
    with (DATA_DIR / "storm_vs_saidi.csv").open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if first <= int(r["year"]) <= last]
    xs = [float(r["storm_county_days"]) for r in rows]
    ys = [float(r["saidi_ex_med"]) for r in rows]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    b = sxy / sxx
    return my - b * mx, b, sxy / (sxx * syy) ** 0.5, n


def rewrite_fields(node, qref_map):
    """Aggregation over a mapped column -> measure; renamed measures -> new table/name."""
    if isinstance(node, dict):
        if set(node) == {"Aggregation"}:
            agg = node["Aggregation"]
            col = agg.get("Expression", {}).get("Column")
            if col and agg.get("Function") == 0:
                ent = col.get("Expression", {}).get("SourceRef", {}).get("Entity")
                key = (ent, col.get("Property"))
                if key in AGG_TO_MEASURE:
                    e2, m2 = AGG_TO_MEASURE[key]
                    qref_map[f"Sum({ent}.{col['Property']})"] = f"{e2}.{m2}"
                    return {"Measure": {"Expression": {"SourceRef": {"Entity": e2}}, "Property": m2}}
        if set(node) == {"Measure"}:
            m = node["Measure"]
            ent = m.get("Expression", {}).get("SourceRef", {}).get("Entity")
            key = (ent, m.get("Property"))
            if key in MEASURE_RENAMES:
                e2, m2 = MEASURE_RENAMES[key]
                return {"Measure": {"Expression": {"SourceRef": {"Entity": e2}}, "Property": m2}}
        return {k: rewrite_fields(v, qref_map) for k, v in node.items()}
    if isinstance(node, list):
        return [rewrite_fields(v, qref_map) for v in node]
    return node


def replace_strings(node, mapping):
    if isinstance(node, dict):
        return {k: replace_strings(v, mapping) for k, v in node.items()}
    if isinstance(node, list):
        return [replace_strings(v, mapping) for v in node]
    if isinstance(node, str) and node in mapping:
        return mapping[node]
    return node


def recolour(node):
    """Off-convention default blue -> subject blue (literal colours and text styles)."""
    if isinstance(node, dict):
        return {k: recolour(v) for k, v in node.items()}
    if isinstance(node, list):
        return [recolour(v) for v in node]
    if isinstance(node, str) and node.lower() in ("'#118dff'", "#118dff"):
        return node.replace(node.strip("'"), SUBJECT)
    return node


def fix_projections(v, qref_map):
    qs = v.get("visual", {}).get("query", {}).get("queryState", {})
    for role in qs.values():
        for p in role.get("projections", []):
            f = p["field"]
            if "Measure" in f:
                ent = f["Measure"]["Expression"]["SourceRef"]["Entity"]
                new_ref = f"{ent}.{f['Measure']['Property']}"
                if p.get("queryRef") != new_ref:
                    qref_map[p["queryRef"]] = new_ref
                    p["queryRef"] = new_ref
                p["nativeQueryRef"] = p.get("displayName") or f["Measure"]["Property"]


def set_vco_text(v, key, text):
    vco = v["visual"].setdefault("visualContainerObjects", {})
    arr = vco.setdefault(key, [{"properties": {}}])
    arr[0].setdefault("properties", {})["text"] = L(lit(text))


def set_alt(v, text):
    vco = v["visual"].setdefault("visualContainerObjects", {})
    gen = vco.setdefault("general", [{"properties": {}}])
    gen[0].setdefault("properties", {})["altText"] = L(lit(text[:250]))


def get_vco_text(v, key):
    try:
        val = v["visual"]["visualContainerObjects"][key][0]["properties"]["text"]["expr"]["Literal"]["Value"]
        return val[1:-1].replace("''", "'")
    except (KeyError, IndexError, TypeError):
        return None


def set_display_name(v, measure_prop, display):
    for role in v["visual"]["query"]["queryState"].values():
        for p in role.get("projections", []):
            f = p["field"]
            prop = f.get("Measure", {}).get("Property") or f.get("Column", {}).get("Property")
            if prop == measure_prop:
                p["displayName"] = display
                p["nativeQueryRef"] = display


def build_report(tree, nums):
    pages_dir = tree / "Report" / "definition" / "pages"
    visuals = {}
    for vj in pages_dir.glob("*/visuals/*/visual.json"):
        visuals[vj.parent.name] = (vj, json.loads(vj.read_text(encoding="utf-8")))
    log = []

    # F4: remove the peer slicer from the landing page; page filter instead
    shutil.rmtree(pages_dir / "e6f27ff89680632d5471" / "visuals" / "56198e8c521b4d60a663")
    visuals.pop("56198e8c521b4d60a663")
    log.append("F4 removed slicer 56198e8c521b4d60a663")

    # F6 + renames: fields, query refs, selectors
    for vid, (path, v) in visuals.items():
        qmap = {}
        v2 = rewrite_fields(v, qmap)
        fix_projections(v2, qmap)
        if qmap:
            v2 = replace_strings(v2, qmap)
            log.append(f"F6/renames {vid}: {qmap}")
        visuals[vid] = (path, recolour(v2))

    # F2: header swap (and neutral ink instead of the default blue)
    # (P4 titles review, 1 Nov: "drivers" reads as cause, so the reliability header says "weather")
    for vid, text in {"ed03849209beb1288bb0": "Reliability performance and weather",
                      "0fb6bdf75ea43a197450": "Electricity demand and grid planning"}.items():
        v = visuals[vid][1]
        run = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
        log.append(f"F2 {vid}: '{run['value']}' -> '{text}'")
        run["value"] = text
        run.setdefault("textStyle", {})["color"] = INK
    # Summary sub-header: no "drivers"; the NOAA product is Storm Events
    paras = visuals["f98b3d720c82504c0056"][1]["visual"]["objects"]["general"][0]["properties"]["paragraphs"]
    for para, (old, new) in zip(paras, (("Customer outage trends, interruption drivers and weather exposure",
                                         "Customer outage trends, interruptions and weather exposure"),
                                        ("(EIA-861 & NOAA Storm Data)", "(EIA-861 and NOAA Storm Events)"))):
        assert para["textRuns"][0]["value"] == old, para
        para["textRuns"][0]["value"] = new
    # reference-line labels: one capitalization; name the average line on the hour-growth charts
    for vid, pairs in {"eb9e34101c7ddbafa3ba": [("'2019 Level'", "'2019 level'")],
                       "8cf55a203d9c93e66b58": [("'2019 Level'", "'2019 level'")],
                       "dcda2b950535cd9fed73": [("'2015 Level'", "'2015 level'")],
                       "7b0e71f981e225998e87": [("'Average line 1'", "'Average of all hours'")],
                       "71ceb4a586c3d3d3acb9": [("'Average line 1'", "'Average of all hours'")],
                       # V1/O-33: CAIDI is "minutes per interruption" (a ratio), never "minutes to restore"
                       "5aedb895e782649461c9": [("'Minutes Per Outage'", "'Minutes per interruption'")],
                       "a56e85d260bd5432b881": [("'Minutes Per Outage'", "'Minutes per interruption'")],
                       "99301c6283764dcfd28f": [("'Minutes to restore each outage (CAIDI)'",
                                                 "'Minutes per interruption (CAIDI)'")]}.items():
        if vid not in visuals:
            continue
        path, v = visuals[vid]
        s = json.dumps(v)
        for old, new in pairs:
            assert old in s, (vid, old)
            s = s.replace(old, new)
        visuals[vid] = (path, json.loads(s))

    # F3: titles and subtitles
    dom = round(nums["dom_2015_2025"] * 100)
    coop = round(nums["coop_2015_2025"] * 100)
    n_lo, n_hi = nums["night"]
    a_lo, a_hi = nums["afternoon"]
    assert 38.95 <= n_lo and n_hi <= 41.05 and 26.85 <= a_lo and a_hi <= 27.45, nums
    titles = {
        ("3e0ddca78b79485a3fea", "f3f57290918057748a49"): (
            "Commercial sales up 65% since 2013 on 8% more customers, consistent with large round-the-clock loads", None),
        ("0cdbc9919c3afef37960", "1bc8e4107099744b0737"): (
            "Adjusted for storm days (a model estimate), SAIDI shows no clear trend since 2015", None),
        ("cd3dca34756db97f5ed6", "826577f03738cae22210"): (
            "Years with more storm days had more outage minutes",
            "2015 to 2024 (n = 10). r = 0.70: association, not cause. The line is the fit used for the weather adjustment"),
        ("d2efd4d136e889ee2b0e",): (
            "Major event days are about half of all-event outage minutes in 2025",
            "Minutes per customer: excluding major event days, and on major event days. Dominion Energy Virginia, EIA-861"),
        ("dcda2b950535cd9fed73",): (
            f"Since 2015, Virginia co-op outage frequency rose {coop}% and Dominion's {dom}%", None),
        ("e1c9d78e2ce3b1f88809", "10a79b0633cd9c8e9009"): (
            "Winter set the year's peak in 2019, 2022 and 2025; 2026 is a near-tie so far",
            "Highest hour in Dec to Feb vs Jun to Aug of each calendar year, PJM DOM zone, EIA-930. 2026 runs to Oct 29: summer complete, winter Jan to Feb only"),
        ("7b0e71f981e225998e87", "71ceb4a586c3d3d3acb9"): (
            "Load growth 2019 to 2025: +39% to +41% in the hours ending 1 to 5 a.m., about +27% in the hours ending 1 to 5 p.m.",
            "Change in average demand for each hour of the day (hour ending, local time), PJM DOM zone, EIA-930"),
        ("5aedb895e782649461c9", "a56e85d260bd5432b881"): (
            "Minutes per interruption down 9% since 2019", None),
        ("99301c6283764dcfd28f",): (
            "Mid-pack on minutes per interruption; outage frequency is the gap", None),
        ("1b2743b4ff761d5db85f", "1d92052046d0a3c7b466"): (
            "Dominion: smart meters are 99.8% of meters; about 1% of customers are on a time-varying rate",
            "Smart meters as a share of all meters, and the share of customers on a time-varying rate, 2025. EIA-861"),
    }
    for vids, (title, sub) in titles.items():
        for vid in vids:
            v = visuals[vid][1]
            log.append(f"F3 {vid}: '{get_vco_text(v, 'title')}' -> '{title}'")
            set_vco_text(v, "title", title)
            if sub:
                set_vco_text(v, "subTitle", sub)

    # card labels (F3 row 5 and plain-language labels)
    # labels sized to the card widths (about 0.1 characters per pixel before truncation)
    labels = {
        "268053916982bec30f81": ("Major-event-day share", "Major-event-day share"),
        "60c7e3f0b4bead9c30cb": ("Selected major-event-day share", "Major-event share"),
        "7f06e22e345306270702": ("Selected Customers", "Customers served"),
        "85c7fe070bb08b249a19": ("Selected SAIDI", "SAIDI (minutes)"),
        "f34f7fc4d6b95e25b282": ("Selected SAIFI", "SAIFI (outages)"),
        "f37647b5550328452389": ("Selected CAIDI", "Minutes per interruption"),
        "2bddd35670236987c7c1": ("SAIDI ex MED", "SAIDI (minutes)"),
        "4815afead0c6a4a7ca4b": ("Total Customers", "Customers served"),
        "3bc57cca3f71ef9d7cc3": ("SAIFI ex MED", "SAIFI (outages)"),
        "7a8692e79a615d758900": ("CAIDI ex MED", "Minutes per interruption (CAIDI)"),
        "abfe0d2588105da0a784": ("CAIDI 5yr", "Minutes per interruption 2021 to 2025"),   # peer table column
        "588c5e9877c5c13562f4": ("SAIDI all events", "SAIDI incl. major event days"),
        "ca269581fd1be8142455": ("Floor growth 2019 to 2025", "Lowest hour, 2019 to 2025"),
        "ea221bd41bd7ea9c1c49": ("Peak growth 2019 to 2025", "Peak hour, 2019 to 2025"),
        "e12a05449550ed1cb6e0": ("Floor growth 2019 to 2025", "Lowest hour, 2019 to 2025"),
        "19360d26904890819773": ("Peak growth 2019 to 2025", "Peak hour, 2019 to 2025"),
        "1b4422116d6104d407dd": ("Top 50 hours in 2025", "Top-50 hours in 2025"),
        "18d3b980d88222e2273d": ("Top 50 hours in 2025", "Top-50 hours in 2025"),
    }
    for vid, (prop, display) in labels.items():
        v = visuals[vid][1]
        set_display_name(v, prop, display)
        qmap = {}
        fix_projections(v, qmap)

    # F5: axis title; explicit series colours (no theme-slot colours)
    for vid in ("3e0ddca78b79485a3fea", "f3f57290918057748a49"):
        v = visuals[vid][1]
        v["visual"]["objects"]["valueAxis"][0]["properties"]["titleText"] = L(lit("Index, 2013 = 100"))
        v["visual"]["objects"]["dataPoint"] = [
            {"properties": {"fill": {"solid": {"color": L(lit(col))}}}, "selector": {"metadata": f"LoadGrowth.{m}"}}
            for m, col in (("Commercial sales index", SUBJECT), ("Commercial customers index", GREY),
                           ("Residential sales index", CONTEXT))]
        log.append(f"F5 {vid}: axis title -> Index, 2013 = 100")
    # smart meter bars: one decimal so 99.8 is not shown as 100
    for vid in ("1b2743b4ff761d5db85f", "1d92052046d0a3c7b466"):
        v = visuals[vid][1]
        v["visual"]["objects"]["labels"][0]["properties"]["labelPrecision"] = L("1L")
        for dp in v["visual"]["objects"].get("dataPoint", []):
            if dp.get("selector", {}).get("metadata") == "Programmes2025.Smart meter share %":
                dp["properties"]["fill"] = {"solid": {"color": L(lit(CONTEXT))}}
            if dp.get("selector", {}).get("metadata") == "Programmes2025.Time-varying rate %":
                dp["properties"]["fill"] = {"solid": {"color": L(lit(SUBJECT))}}
    # major-event-day columns: plain series names
    v = visuals["d2efd4d136e889ee2b0e"][1]
    set_display_name(v, "Major-event-day SAIDI", "On major event days")
    set_display_name(v, "SAIDI ex MED", "Excluding major event days")
    fix_projections(v, {})
    for vid in ("0cdbc9919c3afef37960", "1bc8e4107099744b0737"):
        v = visuals[vid][1]
        set_display_name(v, "Weather-adjusted SAIDI", "Weather-adjusted (model)")
        set_display_name(v, "Actual SAIDI", "Actual")
        fix_projections(v, {})
    for vid in ("1b2743b4ff761d5db85f", "1d92052046d0a3c7b466"):
        v = visuals[vid][1]
        set_display_name(v, "Smart meter share %", "Smart meters, % of meters")
        set_display_name(v, "Time-varying rate %", "Time-varying rate, % of customers")
        fix_projections(v, {})

    # Storm scatter: show only the fit years 2015-2024, so Power BI's trend line is the published fit
    # (104.3 + 0.0518 x storm county-days, r = 0.70), not a fit over every year on the axis
    a, b, r, n = storm_fit()
    assert (round(a, 1), round(b, 4), round(r, 2), n) == (104.3, 0.0518, 0.70, 10), (a, b, r, n)
    for vid in ("cd3dca34756db97f5ed6", "826577f03738cae22210"):
        v = visuals[vid][1]
        filters = v.setdefault("filterConfig", {}).setdefault("filters", [])
        new = categorical_filter("V_STORM_VS_SAIDI", "YEAR", [f"{y}D" for y in range(2015, 2025)], alias="s")
        for i, f in enumerate(filters):
            if f.get("field", {}).get("Column", {}).get("Property") == "YEAR":
                new["name"] = f["name"]
                filters[i] = new
                break
        else:
            filters.append(new)
        log.append(f"scatter {vid}: visual filter YEAR 2015-2024; trend line = {a:.1f} + {b:.4f} x days, r = {r:.3f}")
    # SAIFI trends: continuous year axis, so the 2015 and 2020 counting-change lines show (docs/06 rule)
    for vid in ("eb9e34101c7ddbafa3ba", "8cf55a203d9c93e66b58"):
        v = visuals[vid][1]
        v["visual"]["objects"]["categoryAxis"][0]["properties"]["axisType"] = L("'Scalar'")
        log.append(f"axis {vid}: Categorical -> Scalar (2015 and 2020 lines now drawn)")
    # CAIDI trends: the 2015 line carries the same label as on the SAIFI chart
    for vid in ("a56e85d260bd5432b881", "5aedb895e782649461c9"):
        for line in visuals[vid][1]["visual"]["objects"].get("xAxisReferenceLine", []):
            props = line["properties"]
            if props.get("value", {}).get("expr", {}).get("Literal", {}).get("Value") == "2015D":
                props["displayName"] = L("'2015: Automated Outage Recording'")
                props["dataLabelText"] = L("'Name'")
                log.append(f"label {vid}: 2015 line named as on the SAIFI chart")
    # Peer quadrant: dashed lines at the medians of the 11 peers (Dominion excluded), as the deck states,
    # instead of Power BI's median over all twelve points
    med_saifi, med_caidi = peer_medians()
    v = visuals["99301c6283764dcfd28f"][1]
    objs = v["visual"]["objects"]
    for line in objs.get("referenceLine", []):
        line["properties"]["show"] = L("false")
    grey = {"lineColor": {"solid": {"color": L(lit(GREY))}}, "width": L("1D"), "dataLabelShow": L("false")}
    objs["xAxisReferenceLine"] = [{"properties": {"show": L("true"), "displayName": L(lit("Median of 11 peers")),
                                                  "value": L(f"{med_saifi:g}D"), **grey}, "selector": {"id": "1"}}]
    objs["y1AxisReferenceLine"] = [{"properties": {"show": L("true"), "displayName": L(lit("Median of 11 peers")),
                                                   "value": L(f"{med_caidi:g}D"), **grey}, "selector": {"id": "1"}}]
    set_vco_text(v, "subTitle", "5-year averages 2021 to 2025, excluding major event days. "
                                f"Dashed lines: medians of the 11 peers (SAIFI {med_saifi:.2f}, CAIDI {med_caidi:g})")
    log.append(f"peer quadrant: median lines over 11 peers, SAIFI {med_saifi:g}, CAIDI {med_caidi:g}")
    # What moved: the two trends stacked at full width (they sat half-width on a diagonal)
    for vid, y in (("eb9e34101c7ddbafa3ba", 8), ("a56e85d260bd5432b881", 548)):
        visuals[vid][1]["position"].update({"x": 11, "y": y, "width": 1898, "height": 520})
        log.append(f"layout {vid}: x 11, y {y}, 1898 x 520")

    # write visuals back
    for vid, (path, v) in visuals.items():
        path.write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")

    # pages: F4 page filter, F10 names and order, new pages
    page_ids = {}
    for pid, display in PAGES.items():
        if pid.startswith("NEW_"):
            page_ids[pid] = hexid()
        else:
            page_ids[pid] = pid
    what_moved = json.loads((pages_dir / "2414a423c3820b09c17c" / "page.json").read_text(encoding="utf-8"))
    for pid, display in PAGES.items():
        real = page_ids[pid]
        pdir = pages_dir / real
        if pid.startswith("NEW_"):
            (pdir / "visuals").mkdir(parents=True, exist_ok=True)
            page = {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
                    "name": real, "displayName": display, "displayOption": "FitToPage", "height": 1080, "width": 1920}
        else:
            page = json.loads((pdir / "page.json").read_text(encoding="utf-8"))
            log.append(f"F10 page {real}: '{page.get('displayName')}' -> '{display}'")
            page["displayName"] = display
        if pid == "e6f27ff89680632d5471":
            fc = copy.deepcopy(what_moved["filterConfig"])
            fc["filters"][0]["name"] = hexid()
            page["filterConfig"] = fc
            log.append("F4 Summary page filter: DIM_UTILITY[PEER_GROUP] = Dominion Energy Virginia")
        (pdir / "page.json").write_text(json.dumps(page, ensure_ascii=False), encoding="utf-8")
    new_visuals = new_pages(pages_dir, page_ids)
    order = [page_ids[p] for p in PAGES]
    pj = json.loads((pages_dir / "pages.json").read_text(encoding="utf-8"))
    pj["pageOrder"] = order
    pj["activePageName"] = page_ids["e6f27ff89680632d5471"]
    pj["landingPageName"] = page_ids["e6f27ff89680632d5471"]
    (pages_dir / "pages.json").write_text(json.dumps(pj, ensure_ascii=False), encoding="utf-8")

    # F12: alt text on every visual (after all edits)
    alt_rows = []
    for vj in sorted(pages_dir.glob("*/visuals/*/visual.json")):
        v = json.loads(vj.read_text(encoding="utf-8"))
        page = json.loads((vj.parents[2] / "page.json").read_text(encoding="utf-8"))["displayName"]
        alt = alt_text(v, page)
        set_alt(v, alt)
        vj.write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        alt_rows.append((page, v["name"], v["visual"]["visualType"], alt))
    return log, alt_rows, page_ids, new_visuals


def alt_text(v, page):
    vt = v["visual"]["visualType"]
    title = get_vco_text(v, "title")
    sub = get_vco_text(v, "subTitle")
    if vt == "textbox":
        paras = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"]
        return "Text: " + " ".join("".join(r.get("value", "") for r in p.get("textRuns", [])) for p in paras)
    if vt == "slicer":
        return "Year slicer, default 2025. It sets the year shown on the cards on this page."
    if vt == "cardVisual":
        labels = [p.get("displayName") or p.get("nativeQueryRef") for r in v["visual"]["query"]["queryState"].values() for p in r["projections"]]
        ctx = "for the year chosen in the Year slicer" if page == "Summary" else ("for 2025" if page == "Scorecard" else "")
        return f"Card: {labels[0]} {ctx}".strip() + "."
    kind = {"lineChart": "Line chart", "scatterChart": "Scatter chart", "columnChart": "Column chart",
            "clusteredColumnChart": "Column chart", "clusteredBarChart": "Bar chart", "tableEx": "Table",
            "barChart": "Bar chart"}.get(vt, vt)
    parts = [f"{kind}: {title}" if title else kind]
    if sub:
        parts.append(sub)
    return ". ".join(parts) + "."


def new_pages(pages_dir, page_ids):
    """Data notes page (F11) and the P2 pages from D's tables."""
    made = []
    # ---- Data notes
    pid = page_ids["NEW_NOTES"]
    vdir = pages_dir / pid / "visuals"
    head = textbox(hexid(), 15, 10, 1200, 66, 0, [("Data notes", 28, INK, False)])
    body = textbox(hexid(), 15, 80, 1890, 150, 1000, [
        ("Sources: EIA-861 (reliability, sales, customers; 2013-2024 via PUDL, 2025 final release of Oct 7, 2026); "
         "NOAA Storm Events (storm county-days); EIA-930 (PJM DOM zone hourly demand; 2026 runs through the hour ending midnight, Oct 29)"
         + ("; EAGLE-I county outages 2015-2025 (ORNL, CC BY 4.0)." if P2 else "."), 11, INK, False),
        ("Method: SAIDI, SAIFI and CAIDI exclude major event days unless stated; indices are customer-weighted "
         "(sum numerators, sum denominators, divide once). Correlations show association, not cause. "
         "The weather-adjusted series is a model estimate from a 2015-2024 fit.", 11, INK, False),
        ("Data snapshot: Nov 1, 2026, Import mode from the CSV files in the DataFolder parameter (no live connection).", 11, GREY, False),
    ])
    tests = chart(hexid(), "tableEx", 15, 245, 1180, 820, 2000, {"Values": [
        proj_col("Tests", "TEST", "Test"), proj_col("Tests", "DESCRIPTION", "Check"),
        proj_col("Tests", "EXPECTED", "Expected"), proj_col("Tests", "ROWS_RETURNED", "Rows returned"),
        proj_col("Tests", "STATUS", "Status")]},
        (f"All {STATS['tests'][1]} data tests pass" if STATS["tests"][0] == STATS["tests"][1]
         else f"{STATS['tests'][0]} of {STATS['tests'][1]} data tests pass"),
        "Tests run on each build of the data (data/output/test_results.csv; definitions in docs/03_data_quality.md)",
        sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Tests"}}, "Property": "TEST"}}, "direction": "Ascending"}])
    rec = chart(hexid(), "tableEx", 1215, 245, 690, 820, 3000, {"Values": [
        proj_col("Reconciliation", "ROW_NO", "#"),
        proj_col("Reconciliation", "METRIC", "Metric"), proj_col("Reconciliation", "REBUILT", "Rebuilt"),
        proj_col("Reconciliation", "REPORTED", "Published"), proj_col("Reconciliation", "VERDICT", "Verdict")]},
        f"Rebuilt values match the published ones ({STATS['rec'][0]} of {STATS['rec'][1]})",
        "Rebuilt from public files vs the published source (data/output/reconciliation.csv)",
        sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "Reconciliation"}}, "Property": "ROW_NO"}}, "direction": "Ascending"}])
    for v in (head, body, tests, rec):
        (vdir / v["name"]).mkdir(parents=True, exist_ok=True)
        (vdir / v["name"] / "visual.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        made.append(("Data notes", v["name"]))
    # Scorecard: the reconciliation beside the 2025 cards, as docs/06 describes the page
    # (Reconciliation has no relationships, so the page's YEAR and PEER_GROUP filters leave it whole)
    rec2 = copy.deepcopy(rec)
    rec2["name"] = hexid()
    rec2["position"].update({"x": 330, "y": 200, "width": 780, "height": 560})
    made += write_visuals(pages_dir, "61745dccdb7948ee4977", "Scorecard", [rec2])
    if P2:
        made += p2_pages(pages_dir, page_ids)
    return made


def write_visuals(pages_dir, pid, page_name, visuals):
    vdir = pages_dir / pid / "visuals"
    out = []
    for v in visuals:
        (vdir / v["name"]).mkdir(parents=True, exist_ok=True)
        (vdir / v["name"] / "visual.json").write_text(json.dumps(v, ensure_ascii=False), encoding="utf-8")
        out.append((page_name, v["name"]))
    return out


def series_colours(entity, pairs):
    return [{"properties": {"fill": {"solid": {"color": L(lit(col))}}}, "selector": {"metadata": f"{entity}.{m}"}}
            for m, col in pairs]


def p2_pages(pages_dir, page_ids):
    n = NUMS
    made = []
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}
    labels_on = {"labels": [{"properties": {"show": L("true")}}]}

    # ---- Outages by county
    pid = page_ids["NEW_COUNTY"]
    head = textbox(hexid(), 15, 10, 1500, 66, 0, [("Outages by county", 28, INK, False)])
    sub = textbox(hexid(), 15, 75, 1890, 45, 1000, [(
        "EAGLE-I county outage records (ORNL), Dominion's 103 Virginia counties. EAGLE-I counts every utility's customers "
        f"in a county; {103 - n['county_n']} counties are left off for unreliable data.", 12, GREY, False)])
    lo_name, lo_val = n["county_lo"]
    hi_name, hi_val = n["county_hi"]
    top = {"name": hexid(), "field": {"Column": {"Expression": {"SourceRef": {"Entity": "COUNTY_OUTAGE_MAP"}}, "Property": "COUNTY_LABEL"}},
           "type": "TopN",
           "filter": {"Version": 2,
                      "From": [{"Name": "subquery", "Expression": {"Subquery": {"Query": {
                          "Version": 2, "From": [{"Name": "c", "Entity": "COUNTY_OUTAGE_MAP", "Type": 0}],
                          "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": "COUNTY_LABEL"}, "Name": "field"}],
                          "OrderBy": [{"Direction": 2, "Expression": {"Measure": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": "Non-major outage minutes, 20k+ counties"}}}],
                          "Top": 15}}}, "Type": 2},
                               {"Name": "c", "Entity": "COUNTY_OUTAGE_MAP", "Type": 0}],
                      "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "c"}}, "Property": "COUNTY_LABEL"}}],
                                                      "Table": {"SourceRef": {"Source": "subquery"}}}}}]}}
    county = chart(hexid(), "clusteredBarChart", 15, 130, 930, 935, 2000,
                   {"Category": [proj_col("COUNTY_OUTAGE_MAP", "COUNTY_LABEL", "County")],
                    "Y": [proj_measure("COUNTY_OUTAGE_MAP", "Non-major outage minutes, 20k+ counties", "Minutes a year")]},
                   f"All utilities: non-major outage minutes ranged from {lo_val} ({lo_name}) to {hi_val} ({hi_name}) a year",
                   f"EAGLE-I, all utilities (not Dominion's SAIDI). Top 15 of the {n['county_n20k']} counties with 20,000+ customers; "
                   "non-major-event days, 2015 to 2024 average",
                   objects={**labels_on, "dataPoint": [{"properties": {"fill": {"solid": {"color": L(lit(SUBJECT))}}}}]},
                   sort=[{"field": {"Measure": {"Expression": {"SourceRef": {"Entity": "COUNTY_OUTAGE_MAP"}}, "Property": "Non-major outage minutes, 20k+ counties"}},
                          "direction": "Descending"}],
                   filters=[top])
    t = n["ev_types"]
    parts = []
    for key, word in (("tropical", "tropical storms"), ("winter", "winter storms"), ("wind", "wind events")):
        if t.get(key):
            parts.append(f"{words.get(t[key], t[key])} {word}")
    events_title = "The ten largest outage events: " + (", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0])
    events = chart(hexid(), "tableEx", 975, 130, 930, 600, 3000, {"Values": [
        proj_col("OUTAGE_EVENTS_TOP10", "Event", "Event"),
        proj_col("OUTAGE_EVENTS_TOP10", "PEAK_CUSTOMERS_OUT", "Peak customers out"),
        proj_col("OUTAGE_EVENTS_TOP10", "PEAK_SUSTAINED_1H", "Held 1 h"),
        proj_col("OUTAGE_EVENTS_TOP10", "HOURS_TO_90PCT", "Hours to clear 90%"),
        proj_col("OUTAGE_EVENTS_TOP10", "CUSTOMER_HOURS", "Customer-hours")]},
        events_title,
        f"Territory events in Dominion's 103 counties, {n['ev_years'][0]} to {n['ev_years'][1]}, by peak day; ranked by customers out held for an hour. EAGLE-I (all utilities)",
        sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "OUTAGE_EVENTS_TOP10"}}, "Property": "PEAK_SUSTAINED_1H"}}, "direction": "Descending"}])
    made += write_visuals(pages_dir, pid, "Outages by county", [head, sub, county, events])

    # ---- Storms
    pid = page_ids["NEW_STORMS"]
    head = textbox(hexid(), 15, 10, 1500, 66, 0, [("Storms", 28, INK, False)])
    sub = textbox(hexid(), 15, 75, 1890, 45, 1000, [(
        "NOAA Storm Events (storm county-days) and EAGLE-I outage records (all utilities). Associations, not causes.", 12, GREY, False)])
    y0, y1, ny = n["storm_years"]
    stack = chart(hexid(), "columnChart", 15, 130, 1890, 450, 2000,
                  {"Category": [proj_col("V_STORM_VS_SAIDI", "YEAR", "Year")],
                   "Y": [proj_measure("V_STORM_VS_SAIDI", "Wind days", "Wind"),
                         proj_measure("V_STORM_VS_SAIDI", "Winter days", "Winter"),
                         proj_measure("V_STORM_VS_SAIDI", "Tropical days", "Tropical")]},
                  f"Damaging wind was the largest storm type in {n['wind_top_years']} of {ny} years",
                  f"NOAA storm county-days in Dominion's Virginia counties by type, {y0} to {y1}",
                  objects={**labels_on, "categoryAxis": [{"properties": {"axisType": L("'Categorical'")}}],
                           "dataPoint": series_colours("V_STORM_VS_SAIDI", (("Wind days", SUBJECT), ("Winter days", GREY), ("Tropical days", GOLD)))},
                  sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "V_STORM_VS_SAIDI"}}, "Property": "YEAR"}}, "direction": "Ascending"}])
    h90 = n["isaias_h90"]
    curve = chart(hexid(), "lineChart", 15, 610, 1890, 455, 3000,
                  {"Category": [proj_col("RESTORATION_CURVE", "HOUR_SINCE_PEAK", "Hours since the peak")],
                   "Y": [proj_measure("RESTORATION_CURVE", "Share restored", "Share of the outage cleared")]},
                  f"Isaias, August 2020: {h90:g} hours from the peak to clear 90% of the outage",
                  "Share cleared by hour since the peak: (peak - customers out) / (peak - pre-event level), a net count. "
                  "EAGLE-I, all utilities in Dominion's 103 counties; not a utility's '% of affected customers restored'",
                  objects={"dataPoint": [{"properties": {"fill": {"solid": {"color": L(lit(SUBJECT))}}}}],
                           "lineStyles": straight(markers=False)},
                  filters=[categorical_filter("RESTORATION_CURVE", "EVENT_KEY", [lit(n["isaias_key"])], alias="r")])
    made += write_visuals(pages_dir, pid, "Storms", [head, sub, stack, curve])

    # ---- Demand and seasons: two more visuals beside the seasonal peaks
    pid = "e8d8451399dc68c3ece6"
    g = n["sector_growth"]
    prof = chart(hexid(), "lineChart", 1100, 135, 800, 500, 2000,
                 {"Category": [proj_col("DOM_LOAD_PROFILE", "HOUR_NO", "Hour of day")],
                  "Y": [proj_measure("DOM_LOAD_PROFILE", "Average MW 2019", "2019"),
                        proj_measure("DOM_LOAD_PROFILE", "Average MW 2025", "2025")]},
                 "Average demand rose in every hour from 2019 to 2025, most in the hours ending 1 to 5 a.m."
                 if n["all_hours_up"] and 1 <= n["max_hour"] <= 5
                 else "Average demand by hour of day, 2019 and 2025",
                 "Average MW by hour of day (hour ending, local time), PJM DOM zone, EIA-930",
                 objects={"dataPoint": series_colours("DOM_LOAD_PROFILE", (("Average MW 2019", CONTEXT), ("Average MW 2025", SUBJECT))),
                          "categoryAxis": [{"properties": {"axisType": L("'Categorical'")}}],
                          "lineStyles": straight(markers=True)},
                 sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "DOM_LOAD_PROFILE"}}, "Property": "HOUR_NO"}}, "direction": "Ascending"}])
    sales = chart(hexid(), "lineChart", 81, 660, 1819, 400, 3000,
                  {"Category": [proj_col("FCT_SALES_SECTOR", "YEAR", "Year")],
                   "Series": [proj_col("FCT_SALES_SECTOR", "CUSTOMER_CLASS", "Class")],
                   "Y": [proj_measure("FCT_SALES_SECTOR", "Sales TWh", "Sales, TWh")]},
                  f"Commercial sales grew {round(g['commercial'] * 100)}% from 2013 to 2025; residential "
                  + (f"grew {round(g['residential'] * 100)}%" if g["residential"] >= 0 else f"fell {round(-g['residential'] * 100)}%")
                  + ", industrial "
                  + (f"grew {round(g['industrial'] * 100)}%" if g["industrial"] >= 0 else f"fell {round(-g['industrial'] * 100)}%"),
                  "Retail sales in TWh by customer class (bundled plus delivery-only), Dominion Energy Virginia, EIA-861",
                  objects={"categoryAxis": [{"properties": {"axisType": L("'Categorical'")}}],
                           "valueAxis": [{"properties": {"showAxisTitle": L("true"), "titleText": L(lit("TWh"))}}],
                           "lineStyles": straight(markers=True)},
                  sort=[{"field": {"Column": {"Expression": {"SourceRef": {"Entity": "FCT_SALES_SECTOR"}}, "Property": "YEAR"}}, "direction": "Ascending"}])
    head = textbox(hexid(), 15, 10, 1500, 66, 0, [("Demand and seasons", 28, INK, False)])
    sub = textbox(hexid(), 15, 75, 1890, 45, 1000, [(
        "PJM DOM zone hourly demand (EIA-930; a zone, not Dominion's retail territory) and retail sales (EIA-861). "
        "2026 runs through the hour ending midnight, Oct 29.", 12, GREY, False)])
    made += write_visuals(pages_dir, pid, "Demand and seasons", [head, sub, prof, sales])
    return made


# ---------------------------------------------------------------------------------------------
# 4. Theme (F12)
# ---------------------------------------------------------------------------------------------
THEME_FILE = "DominionReview_theme.json"


def theme():
    return {
        "name": "Dominion reliability review",
        "dataColors": [SUBJECT, CONTEXT, GREY, GOLD, INK, "#7FB2E5", "#D9DCE1", "#9CA3AF", "#F3D27A", "#3B4A6B", "#BFD7F2", "#E5E7EB"],
        "foreground": INK, "background": "#FFFFFF",
        "tableAccent": SUBJECT, "good": "#2E7D32", "bad": "#B23B3B", "neutral": GREY,
        "textClasses": {
            "callout": {"fontFace": "Segoe UI Semibold", "fontSize": 28, "color": INK},
            "title": {"fontFace": "Segoe UI Semibold", "fontSize": 14, "color": INK},
            "header": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": INK},
            "label": {"fontFace": "Segoe UI", "fontSize": 10, "color": INK},
        },
        "visualStyles": {
            "*": {"*": {
                "title": [{"fontFamily": "Segoe UI Semibold", "fontSize": 14, "fontColor": {"solid": {"color": INK}}}],
                "subTitle": [{"fontFamily": "Segoe UI", "fontSize": 10, "fontColor": {"solid": {"color": GREY}}}],
                "border": [{"show": False}],
                "dropShadow": [{"show": False}],
            }},
            "page": {"*": {"background": [{"color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}]}},
        },
    }


def apply_theme(tree):
    res = tree / "Report" / "StaticResources" / "RegisteredResources"
    res.mkdir(parents=True, exist_ok=True)
    (res / THEME_FILE).write_text(json.dumps(theme(), indent=2), encoding="utf-8")
    rj_path = tree / "Report" / "definition" / "report.json"
    rj = json.loads(rj_path.read_text(encoding="utf-8"))
    base = rj["themeCollection"]["baseTheme"]
    rj["themeCollection"]["customTheme"] = {"name": THEME_FILE, "reportVersionAtImport": base.get("reportVersionAtImport"),
                                            "type": "RegisteredResources"}
    pk = [p for p in rj.get("resourcePackages", []) if p.get("name") != "RegisteredResources"]
    pk.append({"name": "RegisteredResources", "type": "RegisteredResources",
               "items": [{"name": THEME_FILE, "path": THEME_FILE, "type": "CustomTheme"}]})
    rj["resourcePackages"] = pk
    rj_path.write_text(json.dumps(rj, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------------------------
# 5. Package
# ---------------------------------------------------------------------------------------------
def package(tree, db, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    ct = (tree / "[Content_Types].xml").read_text(encoding="utf-8-sig")
    ct = ct.replace('<Override PartName="/SecurityBindings" ContentType="" />', "")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "\ufeff" + ct)
        for p in sorted(tree.rglob("*")):
            if p.is_dir():
                continue
            rel = p.relative_to(tree).as_posix()
            if rel in ("[Content_Types].xml", "SecurityBindings", "DataModelSchema.pretty.json"):
                continue
            if rel == "DataModelSchema":
                z.writestr(rel, json.dumps(db, ensure_ascii=False).encode("utf-16-le"))
            else:
                z.write(p, rel)
    print("wrote", dest, dest.stat().st_size, "bytes")


def write_docs(db, alt_rows):
    """measures.dax with the purpose of each measure, M per query, theme, alt-text list."""
    model = db["model"]
    lines = [
        "// =====================================================================",
        "// Dominion reliability review: DAX measures and calculated columns, by table.",
        "// Matches the model in Dominion_reliability_review.pbit. Each measure has its purpose above it",
        "// (the same text is the measure's Description, shown when you hover over it in the Data pane).",
        "// Aggregation rule: sum numerators, sum denominators, divide once; ratios and extremes are never summed.",
        "// =====================================================================",
    ]
    for t in model["tables"]:
        calc = [c for c in t.get("columns", []) if c.get("type") == "calculated"]
        ms = t.get("measures", [])
        if not calc and not ms:
            continue
        lines += ["", "// ---------------------------------------------------------------------", f"// {t['name']}",
                  "// ---------------------------------------------------------------------"]
        for c in calc:
            expr = c["expression"] if isinstance(c["expression"], str) else "\n".join(c["expression"])
            lines += ["", "// Calculated column", f"{c['name']} =", expr.strip()]
        for m in ms:
            expr = m["expression"] if isinstance(m["expression"], str) else "\n".join(m["expression"])
            lines += ["", f"// {m.get('description', '')}" + (" (hidden)" if m.get("isHidden") else "")]
            if m.get("formatString"):
                lines.append(f"// Format: {m['formatString']}")
            lines.append(f"{m['name']} =" + ("\n" if "\n" in expr else " ") + expr)
    (DELIV / "measures.dax").write_text("\n".join(lines) + "\n", encoding="utf-8")
    mdir = DELIV / "m"
    if mdir.exists():
        shutil.rmtree(mdir)
    mdir.mkdir(parents=True)
    for e in model.get("expressions", []):
        (mdir / f"{e['name']}.pq").write_text(
            "// Parameter: the repo's data\\output\\ folder. In the template it is asked for when the file opens.\n"
            + '"' + SHIP_DEFAULT + '" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]\n',
            encoding="utf-8")
    for t in model["tables"]:
        p = t["partitions"][0]
        if p["source"]["type"] != "m":
            continue
        expr = p["source"]["expression"]
        text = "\n".join(expr) if isinstance(expr, list) else expr
        (mdir / f"{t['name']}.pq").write_text(f"// Query {t['name']} (Import)\n{text}\n", encoding="utf-8")
    (DELIV / "theme_dominion_review.json").write_text(json.dumps(theme(), indent=2), encoding="utf-8")
    with (DELIV / "alt_text.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["page", "visual_id", "visual_type", "alt_text"])
        w.writerows(alt_rows)
    print("docs written:", "measures.dax,", len(list(mdir.glob('*.pq'))), "M files, theme, alt_text.csv")


def main():
    ship = "--ship" in sys.argv
    stage_data()
    nums = data_numbers()
    NUMS.update(nums)
    print("numbers:", {k: v for k, v in nums.items() if k != "groups"})
    if BUILD.exists():
        shutil.rmtree(BUILD)
    shutil.copytree(SRC, BUILD)
    (BUILD / "DataModelSchema.pretty.json").unlink(missing_ok=True)
    log, alt_rows, page_ids, new_visuals = build_report(BUILD, nums)
    apply_theme(BUILD)
    keep = set()
    verify_folder = str(DATA_DIR) + "\\"
    db = build_model(verify_folder)
    keep = {t["name"] for t in db["model"]["tables"]}
    (BUILD / "DiagramLayout").write_bytes(prune_diagram((SRC / "DiagramLayout").read_bytes(), keep))
    (B5 / "build_log.txt").write_text("\n".join(log), encoding="utf-8")
    with (B5 / "alt_text.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["page", "visual_id", "visual_type", "alt_text"])
        w.writerows(alt_rows)
    (B5 / "page_ids.json").write_text(json.dumps(page_ids, indent=1), encoding="utf-8")
    package(BUILD, db, OUT / f"{NAME}_verify.pbit")
    if ship:
        # the shipped model is the verified one with only the parameter's default changed
        db_ship = copy.deepcopy(db)
        for e in db_ship["model"]["expressions"]:
            if e["name"] == "DataFolder":
                old = '"' + verify_folder.replace('"', '""') + '"'
                assert e["expression"].startswith(old), e["expression"][:80]
                e["expression"] = '"' + SHIP_DEFAULT + '"' + e["expression"][len(old):]
        package(BUILD, db_ship, DELIV / f"{NAME}.pbit")
        write_docs(db_ship, alt_rows)
    print(f"{len(log)} logged edits; {len(alt_rows)} visuals with alt text; pages {list(PAGES.values())}")


if __name__ == "__main__":
    main()
