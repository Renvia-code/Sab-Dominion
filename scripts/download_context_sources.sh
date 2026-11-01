#!/usr/bin/env bash
# Download the smaller sources added in November 2026 into their own folders under data/raw/.
# Each folder gets a MANIFEST.csv from scripts/write_manifests.py (EIA-861 and 861M manifests
# are written by scripts/extract_eia861.py). All are U.S. Government works unless noted.
set -euo pipefail
RAW="$(dirname "$0")/../data/raw"
UA="Mozilla/5.0"
get() { mkdir -p "$RAW/$1"; echo "fetching $2"; curl -fsSL -A "$UA" -o "$RAW/$1/$3" "$2"; }

# EIA-861 annual files (sector sales, dynamic pricing, meters, circuits): 2025 final and 2024
for y in 2025 2024; do get eia861 "https://www.eia.gov/electricity/data/eia861/zip/f861$y.zip" "f861$y.zip"; done

# EIA-861M utility-level monthly sales, one workbook per year (2013-2016 are .xls, some of them xlsx inside)
M="https://www.eia.gov/electricity/data/eia861m"
for y in 2013 2014 2015 2016; do get eia861m "$M/archive/xls/f826$y.xls" "f826$y.xls"; done
for y in 2017 2018 2019 2020; do get eia861m "$M/archive/xls/retail_sales_$y.xlsx" "retail_sales_$y.xlsx"; done
for y in 2021 2022 2023 2024 2025; do get eia861m "$M/archive/xls/sales_ult_cust_$y.xlsx" "sales_ult_cust_$y.xlsx"; done
get eia861m "$M/xls/sales_ult_cust_2026.xlsx" "sales_ult_cust_2026.xlsx"

# Census: county boundaries (cartographic, 1:500k, 2024), ACS 2020-2024 5-year tables, PEP vintage 2025
get census "https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip" "cb_2024_us_county_500k.zip"
get census "https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b01003.dat" "acsdt5y2024-b01003.dat"
get census "https://www2.census.gov/programs-surveys/acs/summary_file/2024/table-based-SF/data/5YRData/acsdt5y2024-b25001.dat" "acsdt5y2024-b25001.dat"
get census "https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv" "co-est2025-alldata.csv"

# NHC HURDAT2 Atlantic best tracks, 1851-2025 (file name changes with each revision: check the listing)
get hurdat2 "https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2025-092326.txt" "hurdat2-1851-2025-092326.txt"

# NOAA CPC population-weighted daily heating and cooling degree days by state
for y in 2018 2019 2020 2021 2022 2023 2024 2025 2026; do
  for k in Heating Cooling; do
    get degree_days "https://ftp.cpc.ncep.noaa.gov/htdocs/degree_days/weighted/daily_data/$y/StatesCONUS.$k.txt" "cpc_StatesCONUS_${k}_$y.txt"
  done
done

# OE-417 events: DOE's own page (www.oe.netl.doe.gov) did not resolve from this network on
# 01-11-2026 (IPv6-only); EIA republishes the events in Electric Power Monthly Appendix B.
get oe417 "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_b_1" "eia_epm_table_b1_2024.html"
get oe417 "https://www.eia.gov/electricity/monthly/epm_table_grapher.php?t=epmt_b_2" "eia_epm_table_b2_2023.html"

# DOE-417 electric emergency incident and disturbance reports, annual summaries (now hosted by
# PNNL): .xls for 2023 and earlier, .xlsx from 2024. No utility column; 2026 not posted yet.
for y in 2014 2015 2016 2017 2018 2019 2020 2021 2022 2023; do
  get doe417 "https://doe417.pnnl.gov/summaries/${y}_Annual_Summary.xls" "${y}_Annual_Summary.xls"
done
for y in 2024 2025; do get doe417 "https://doe417.pnnl.gov/summaries/${y}_Annual_Summary.xlsx" "${y}_Annual_Summary.xlsx"; done

# PJM 2026 Load Forecast Report tables (DOM zone peaks, energy, large-load adjustments)
get pjm "https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/2026-load-report-tables.xlsx" "2026-load-report-tables.xlsx"

# Virginia SCC reports to the General Assembly (reliability charts for Dominion and APCo)
get scc_reliability "https://rga.lis.virginia.gov/Published/2025/RD916/PDF" "rga_2025_RD916.pdf"
get scc_reliability "https://rga.lis.virginia.gov/Published/2025/HD5/PDF" "rga_2025_HD5.pdf"
echo "done; now run scripts/extract_eia861.py, scripts/extract_census_va.py and scripts/write_manifests.py"
