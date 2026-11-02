#!/usr/bin/env bash
# Final-pack audit: fetch the primary pages the ten C-F rows cite that V1 has not already opened today.
# Same command as the original brief: curl -sSL -A "Mozilla/5.0" -o <file> <url>, one new folder per source.
# The log is APPENDED (never truncated). No retries with other agents, no mirrors: a block is recorded and left.
BASE="C:/Users/oni/Desktop/PROJECTS/renvia-technologies/client-apps/dominion-reliability-review/interview-prep/work/reviews/v1_sources"
UA="Mozilla/5.0"
get() {
  d="$BASE/$1"; mkdir -p "$d"
  code=$(curl -sSL -A "$UA" --max-time 120 -o "$d/$3" -w "%{http_code} %{content_type} %{size_download}" "$2" 2>&1)
  echo "$1 | $code | $2" | tee -a "$BASE/_download_log.txt"
}
get final_dom_q3_2026_release "https://news.dominionenergy.com/press-releases/press-releases/2026/Dominion-Energy-Announces-Third-Quarter-2026-Results/default.aspx" page.html
get final_pvmag_coalition "https://pv-magazine-usa.com/2026/10/27/solar-industry-coalition-opposes-67-billion-dominion-nextera-merger-as-proposed/" page.html
get final_govinfo_fr_20261021 "https://www.govinfo.gov/content/pkg/FR-2026-10-21/pdf/2026-21490.pdf" fr.pdf
get final_fedreg_nrc_20260827 "https://www.federalregister.gov/documents/2026/08/27/2026-17529/nextera-energy-inc-dominion-energy-inc-virginia-electric-and-power-company-dominion-energy-nuclear" page.html
get final_loudounnow_rates "https://www.loudounnow.com/news/scc-approves-new-data-center-rate-class-for-dominion/article_02d5fa0c-1ed8-4771-b57d-c24765739854.html" page.html
get final_cpc_degree_days "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/degree_days/" page.html
get final_cpc_ddayexp "https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/cdus/degree_days/ddayexp.shtml" page.html
get final_va_rd916_2025 "https://rga.lis.virginia.gov/Published/2025/RD916/PDF" rd916.pdf
get final_eia861_instructions "https://www.eia.gov/survey/form/eia_861/instructions.pdf" instructions.pdf
get final_ieee_pes_boston_1366 "https://site.ieee.org/boston-pes/files/2019/03/IEEE-1366-Reliability-Indices-2-2019.pdf" slides.pdf
get final_crossref_10_1038_s41597-024-03095-5 "https://api.crossref.org/works/10.1038/s41597-024-03095-5" meta.json
get final_ornl_eaglei_2025 "https://doi.ccs.ornl.gov/dataset/c09fce3f-5faa-54ef-878a-cb0af6851cb6" page.html
