#!/usr/bin/env bash
# Download the external sources cited by claims.csv, each into its own new, empty folder.
# Read-only on the web: plain GETs with a browser user agent; no workaround for blocks.
set -u
BASE="C:/Users/oni/Desktop/PROJECTS/renvia-technologies/client-apps/dominion-reliability-review/interview-prep/work/reviews/v1_sources"
mkdir -p "$BASE"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

get() {  # name url outfile
  local d="$BASE/$1"; mkdir -p "$d"
  local code
  code=$(curl -sSL -A "$UA" --max-time 120 -o "$d/$3" -w "%{http_code} %{content_type} %{size_download}" "$2" 2>&1)
  echo "$1 | $code | $2" | tee -a "$BASE/_download_log.txt"
}

: > "$BASE/_download_log.txt"
get annual_report_2025 "https://s2.q4cdn.com/510812146/files/doc_downloads/2026/03/17/Dominion-Energy-2025-Annual-Report.pdf" ar2025.pdf
get jobright_posting "https://jobright.ai/jobs/info/6aa3a1d5c5a856ac7e33a91a" posting.html
get dominion_grid_resiliency "https://www.dominionenergy.com/about/delivering-energy/electric-projects/energy-grid-transformation/grid-resiliency-projects" page.html
get stocktitan_hurricane "https://www.stocktitan.net/news/D/dominion-energy-prepares-year-round-for-hurricane-season-and-o7ahitzchhvw.html" page.html
get nextera_release "https://newsroom.nexteraenergy.com/2026-05-18-NextEra-Energy-and-Dominion-Energy-to-Combine,-Creating-the-Worlds-Largest-Regulated-Electric-Utility-Business-and-North-Americas-Premier-Energy-Infrastructure-Platform-Benefiting-Customers" page.html
get fool_q3_2026 "https://www.fool.com/earnings/call-transcripts/2026/10/30/dominion-energy-d-q3-2026-earnings-call-transcript/" page.html
get wtvr_merger "https://www.wtvr.com/news/local-news/dominion-nextera-merger-update-oct-19-2026" page.html
get virginiabusiness_scc "https://virginiabusiness.com/spanberger-wont-call-special-session-to-extend-dominion-nextera-merger-deadline/" page.html
for doi in 10.1037/apl0000994 10.1348/096317902320369712 10.1080/23808985.1999.11678963 10.1177/009102600203100310; do
  n=$(echo "$doi" | tr '/.' '__')
  get "crossref_$n" "https://api.crossref.org/works/$doi" meta.json
done
echo DONE
