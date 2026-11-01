#!/usr/bin/env bash
# Download the EAGLE-I county outage files (ORNL, 15-minute customers out by county,
# Nov 2014 to Dec 2025) and the two supplementary files into data/raw/eaglei/downloads/.
#
# Source: DOE CESER's EAGLE-I "Aviary" public download page, https://eagle-i.doe.gov/aviary .
# The page serves each CSV inside a zip together with the DOI citation text files. The same
# CSVs are on figshare (doi:10.6084/m9.figshare.24237376, version 4, 25 Feb 2026), whose
# API publishes an MD5 per file; scripts/extract_eaglei_va.py checks every CSV against it.
# figshare's own download links sit behind a bot challenge, which is why this script uses
# the DOE page. Files are large (13.6 GB of CSV, about 1.4 GB zipped), so the extract
# script keeps only the Virginia rows.
set -euo pipefail
BASE="https://eagle-i.doe.gov/api/aviary"
OUT="$(dirname "$0")/../data/raw/eaglei/downloads"
mkdir -p "$OUT" && cd "$OUT"

# Snapshot of the file list as published today (names, sizes, last update, column notes)
curl -fsSL -A "Mozilla/5.0" -o "aviary_files_$(date +%F).json" "$BASE/files"
curl -fsSL -A "Mozilla/5.0" -o "figshare_24237376_$(date +%F).json" "https://api.figshare.com/v2/articles/24237376"

fetch() {
  local csv="$1" zip="${1%.csv}.zip"
  if [ -s "$zip" ] && unzip -tq "$zip" >/dev/null 2>&1; then echo "have $zip"; return 0; fi
  for attempt in 1 2 3; do
    echo "fetching $csv (attempt $attempt)"
    if curl -fsSL -A "Mozilla/5.0" -o "$zip.part" "$BASE/download?file=$csv"; then
      mv -f "$zip.part" "$zip"; echo "done $zip"; return 0
    fi
    sleep 10
  done
  echo "FAILED $csv" >&2; return 1
}

# Largest years first; at most four downloads at a time.
FILES="eaglei_outages_2024.csv eaglei_outages_2025.csv eaglei_outages_2023.csv eaglei_outages_2022.csv
eaglei_outages_2020.csv eaglei_outages_2021.csv eaglei_outages_2019.csv eaglei_outages_2018.csv
eaglei_outages_2017.csv eaglei_outages_2016.csv eaglei_outages_2015.csv eaglei_outages_2014.csv
MCC.csv coverage_history.csv"
for f in $FILES; do
  while [ "$(jobs -rp | wc -l)" -ge 4 ]; do sleep 2; done
  fetch "$f" &
done
wait
echo "---"
ls -l
echo "expected: 14 zips (12 years, MCC, coverage history); then run scripts/extract_eaglei_va.py"
