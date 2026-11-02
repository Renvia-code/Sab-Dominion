"""Write interview-prep/work/reviews/P4_titles.md: the template's on-screen text per page (from
p4_titles_raw.md, made by p4_titles.py), with the regex flags resolved and the review notes on top.
Usage: python -I make_p4_titles_md.py <p4_titles_raw.md> <out.md> <pbit>"""
import hashlib
import sys
from pathlib import Path

raw, out, pbit = (Path(a) for a in sys.argv[1:4])
sha = hashlib.sha256(pbit.read_bytes()).hexdigest()
body = raw.read_text(encoding="utf-8").split("\n", 1)[1]
body = (body.replace("| Visual | Text on screen | Behind it | Flags |", "| Visual | Text on screen | Behind it (table[measure or column]) | Check |")
        .replace("**causal?**", "ok: states association, not cause")
        .replace("**winter years?**", "ok: subtitle; the title names 2019, 2022, 2025"))

head = f"""# P4 titles: on-screen text of the Power BI template

**Template:** `deliverables/04_powerbi/Dominion_reliability_review.pbit`, SHA-256 `{sha[:16]}…`, built 1 Nov 11:10 by
`work/powerbi/b5/pbi_build.py --ship`. It was verified open in Desktop with `DataFolder` set to this repo's `data\\output\\`
(`work/powerbi/b6/shots_v3b/`, all 11 pages, no error window). The 11:04 build (`b6/shots_v3/`, the source of the deck's
Summary screenshot) differs from it only in the peer table's column header.

**Scope:** every page name, title, subtitle, text box, card label, reference-line label and axis title, page by page. Each
row names the table and measure or column behind it. Text that a measure returns is not on any card; numbers on cards and
in charts come from the fields listed. Static numbers in titles were checked against the CSV each visual reads (below).

## Rules applied, and what changed

| Rule (as the deck) | Result |
|---|---|
| No causal language | **Changed:** Summary header "Reliability performance and drivers" → "Reliability performance and weather"; sub-header "Customer outage trends, interruption drivers and weather exposure" → "Customer outage trends, interruptions and weather exposure". The other hits say "association, not cause" or "consistent with". |
| D's wording: winter peaks 2019, 2022, 2025 | Holds on Demand and seasons and Demand summary: "Winter set the year's peak in 2019, 2022 and 2025; 2026 is a near-tie so far" |
| D's wording: hours ending 1–5 a.m. | **Changed:** both hour-growth titles now read "Load growth 2019 to 2025: +39% to +41% in the hours ending 1 to 5 a.m., about +27% in the hours ending 1 to 5 p.m." The 24-hour profile title "…most at night" now ends "…most in the hours ending 1 to 5 a.m." |
| D's wording: storms "line up with" | No storm title claims more than association: "Years with more storm days had more outage minutes", subtitle "r = 0.70: association, not cause"; no "2025 sits where its weather predicts" |
| "All utilities" on every EAGLE-I view | Holds: the county chart title starts "All utilities:"; the county and event subtitles say "EAGLE-I, all utilities" / "EAGLE-I (all utilities)"; the Isaias subtitle and the Storms page note say "all utilities" |
| 464 / 791 after D22 | Holds: no title prints a storm count; storm visuals read `storm_vs_saidi.csv` (2024 = 464, 2025 = 791); the scatters stop at 2024 |
| 12 of 12 | Holds: Scorecard and Data notes, "Rebuilt values match the published ones (12 of 12)" (`reconciliation.csv`, 12 MATCH) |
| CAIDI is "minutes per interruption", never "minutes to restore" (O-33) | **Changed:** Summary card "Minutes to restore" → "Minutes per interruption"; Scorecard card "Minutes to restore (CAIDI)" → "Minutes per interruption (CAIDI)"; the Summary and What moved CAIDI titles "Minutes to restore each outage down 9% since 2019" → "Minutes per interruption down 9% since 2019", their axis "Minutes Per Outage" → "Minutes per interruption"; the Fair comparison scatter title "Restoration time is mid-pack. Outage frequency is the gap" → "Mid-pack on minutes per interruption; outage frequency is the gap", its axis "Minutes to restore each outage (CAIDI)" → "Minutes per interruption (CAIDI)"; the peer table's column "Minutes per Outage 2021 to 2025" → "Minutes per interruption 2021 to 2025". The `CAIDI ex MED` description now says it is a ratio (SAIDI / SAIFI), not a restoration time. Alt text follows the titles |
| US English and dates | Holds ("Oct 29", "Nov 1, 2026", "Oct 7, 2026"; color, gray) |

Also changed, for consistency: reference-line labels "2019 Level" and "2015 Level" → "2019 level" and "2015 level"; the
hour-growth charts' average line "Average line 1" → "Average of all hours" (its label is off on the canvas). The
hour-growth columns now take their colors from the hours the title names: hours ending 1 to 5 a.m. blue, 1 to 5 p.m. gold,
the rest gray (measure `Hour colour`; before, night hours 23 to 6 were blue, day gold and evening gray, which no title named).

**Static numbers checked against the data the visual reads** (`data/output/`):
- "co-op outage frequency rose 37% and Dominion's 14%": `v_group_index.csv` SAIFI ex-MED 2015 → 2025, Virginia co-op 1.373 → 1.887 (+37.4%), Dominion 1.155 → 1.320 (+14.3%).
- "Damaging wind was the largest storm type in 12 of 13 years": `storm_vs_saidi.csv`, wind days top in every year 2013–2025 except 2014 (winter).
- "Commercial sales grew 65% from 2013 to 2025; residential grew 4%, industrial fell 14%": `fct_sales_sector.csv` sales_mwh (bundled plus delivery-only), 39.08 → 64.62, 28.80 → 30.01, 6.39 → 5.50 TWh.
- "Commercial sales up 65% since 2013 on 8% more customers": `load_growth.csv` 2025 indices 165.4 and 107.9 (2013 = 100).
- "about 1% of customers are on a time-varying rate", "99.8% of meters": `programmes_2025.csv` (1; 0.998).
- "55 (Prince William County) to 633 (Pittsylvania County)", "the 35 counties with 20,000+ customers": `county_outage_map.csv`.
- "three tropical storms, two winter storms and five wind events", "33.5 hours": `outage_events_top10.csv`.
- "up 6% since 2019, most of it after 2023" (1.244 → 1.320; 2023 1.165), "down 9% since 2019" (120.5 → 109.4), "Fourth-highest outage minutes of twelve": `fct_reliability.csv` (fix plan F3, unchanged and verified).
- "All 31 data tests pass": `test_results.csv`, 31 PASS.

**Also changed in this build (orchestrator, D a810494):** LoadGrowth and Programmes2025 now read `load_growth.csv` and
`programmes_2025.csv` instead of the workbook, so every table reads `DataFolder` = `<clone>\\data\\output\\` and nothing else.
The two unused workbook columns (`Column9`, `Source`) left the LoadGrowth table.

**Committed files this changes** (859b52d): `powerbi/Dominion_reliability_review.pbit`, `powerbi/m/LoadGrowth.pq`,
`powerbi/m/Programmes2025.pq`, `powerbi/m/DataFolder.pq` (default now `C:\\path\\to\\dominion-reliability-review\\data\\output\\`),
`powerbi/measures.dax` (the `Hour colour` measure and the `CAIDI ex MED` description), `docs/06_powerbi_report.md`. Unchanged:
`powerbi/theme_dominion_review.json` and the other 16 `.pq` files.

## The text, page by page
"""
out.write_text(head + body, encoding="utf-8")
print(f"wrote {out} ({len((head + body).splitlines())} lines), template {sha[:16]}")
