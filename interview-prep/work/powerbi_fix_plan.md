# Power BI fix plan (P4): exact list, method and feasibility

Written 2026-11-01 07:25–07:45 by B. Evidence: a read-only decode of the report layer
(`work/powerbi/pbix_inventory.md`, script `decode_pbix.py`), the data model
(`work/powerbi/pbix_model_inventory.md`, `decode_model.py`, pbixray 0.15.5), and a copy of the file
opened in Power BI Desktop 2.159.883.0 (Store) on this PC with screenshots
(`work/powerbi/feasibility/*.png`). The original `Dominion Dashboards.pbix` was never modified
(sha256 f2a747a5…6d15, same before and after); all work used copies in `work/powerbi/`.

## 0. Verdict

1. **The file opens offline, but half of it cannot render.** The model is composite: 6 tables are
   **DirectQuery** to the candidate's old Snowflake trial (`vosrmgo-af46531`, warehouse
   `SNOWFLAKE_LEARNING_WH`): `DOM_LOAD_ANNUAL`, `DOM_TOP50_HOURS`, `DOM_LOAD_PROFILE`,
   `SAIDI_WEATHER_ADJUSTED`, `V_STORM_VS_SAIDI`, `V_STORM_VS_SAIDI (2)` (partition Mode = 1). Opened
   here, every visual on them spun for 2.5 minutes and never drew: the Seasonal chart, the hour-of-day
   chart, the weather scatter and adjusted line, and the three DOM cards on Scorecards
   (`feasibility/pbi_page_*.png`). The Import tables (`FCT_RELIABILITY`, `DIM_UTILITY`,
   `V_GROUP_INDEX`, `STORM_INDEX`, `V_TREND`, the five Excel tables) render from cache. This is a
   **new must-fix, ahead of everything in inputs part C**: in the interview, those pages would show
   spinners or errors. Fix F1 makes every table Import from local files.
2. Every issue in inputs part C is confirmed in the file, plus five more found in the decode
   (F3 rows 7–9, F7, F12): two titles the data does not support as worded (winter-peak years, "night
   +41%"), a "same storms" claim, measures that differ from the repo's `measures.dax`, and
   off-convention colours.
3. **Feasibility of an edited copy: positive.** Desktop opens copies, the dialogs and page tabs can be
   driven by UI Automation and MSAA scoped to our own process (`pbi_uia.ps1`, `msaa_click.ps1`), and
   this build has **TMDL view** and PBIR. Recommended route for B5: Desktop "Save as → Power BI project
   (.pbip)" on a copy (driven by UIA), then text edits to the TMDL model and PBIR report, reopen,
   Refresh, screenshot every page, save as .pbix. The apply guide stays the guaranteed path.

## 1. Current state (decoded)

**Pages (8, 1920×1080):** Scorecards `61745dccdb7948ee4977` · What Moved `2414a423c3820b09c17c` ·
Weather `241c63d8c7e81067e9cc` · Peer Comparision `39dca24cb135da967227` · Growth
`4348e5cd66c9b48126f0` · Seasonal `e8d8451399dc68c3ece6` · Executive Dashboard-1
`e6f27ff89680632d5471` (the landing page) · Executive Dashboard-2 `ca36f3cced18c2313453`.

**Model:** 17 tables, 38 measures, 4 calculated columns, 16 M queries, 2 relationships
(`FCT_RELIABILITY[UTILITY_KEY]` → `DIM_UTILITY` M:1; auto-detected `Headline[losses_pct]` →
`Programmes2025[losses_pct]` M:1). `Dashboard Year` is a calculated table (2013–2025).
`FCT_RELIABILITY` renames `CUSTOMERS` to `Customers Served` in M, so the repo's `measures.dax`
(`FCT_RELIABILITY[CUSTOMERS]`) does not match the file; the updated `measures.dax` must use
`Customers Served`.

| Table | Source | Mode | Used by visuals |
|---|---|---|---|
| FCT_RELIABILITY, DIM_UTILITY | old Snowflake trial | Import | yes |
| V_GROUP_INDEX | old Snowflake trial | Import | yes (co-op index) |
| V_TREND, STORM_INDEX | old Snowflake trial | Import | **no** |
| V_STORM_VS_SAIDI | old Snowflake trial | **DirectQuery** | yes (2 scatters) |
| V_STORM_VS_SAIDI (2) | old Snowflake trial | **DirectQuery** | **no** |
| SAIDI_WEATHER_ADJUSTED | old Snowflake trial | **DirectQuery** | yes (2 lines) |
| DOM_LOAD_ANNUAL, DOM_TOP50_HOURS, DOM_LOAD_PROFILE | old Snowflake trial | **DirectQuery** | yes |
| LoadGrowth, Programmes2025, Tests, AmiEventStudy, Headline | `C:\Users\SakethBollina\Downloads\Dominion_Reliability_PowerBI_Data.xlsx` | Import | LoadGrowth, Programmes2025 yes; Tests **no**; AmiEventStudy holds measures only; Headline **no** |

## 2. The fix list

Priority: **P0** must be done before the interview · **P1** should · **P2** new content.
"Where" uses page and visual ids from §1 and `pbix_inventory.md`.

### P0

**F1. Make every table Import from local files, with a folder parameter.**
- Add two text parameters (Home → Transform data → Manage parameters → New): `DataFolder`
  (the repo's `data\output\` folder on the laptop) and `WorkbookPath` (the repo's
  `powerbi\Dominion_Reliability_PowerBI_Data.xlsx`).
- Re-point each query's `Source` step (M per table delivered as `04_powerbi/m/<table>.pq`):
  - Excel tables → `Excel.Workbook(File.Contents(WorkbookPath), null, true)`.
  - Snowflake tables → `Csv.Document(File.Contents(DataFolder & "<file>.csv"), [Delimiter=",",
    Encoding=65001, QuoteStyle=QuoteStyle.Csv])`, promote headers, upper-case the column names
    (`Table.TransformColumnNames(_, Text.Upper)`) so every visual binding keeps its field name,
    then type the columns; `FCT_RELIABILITY` keeps its rename to `Customers Served`.
- When Power Query warns that the DirectQuery tables cannot use a file source, choose
  **Switch all tables to Import mode**. Then Close & Apply.
- Needs from D: CSV exports of the mart tables (hand-off list in §5).
- Check: disconnect Wi-Fi, Home → Refresh succeeds; every page draws.
- Note for the interview (decision D13 already says it): DirectQuery for development, Import for
  presentation; the Snowflake source is kept as an alternative M script for the live demo story.

**F2. Swap the two executive page headers.** Executive Dashboard-1 textbox `ed03849209beb1288bb0`
"Electricity Demand & Grid Planning" → "Reliability performance and drivers". Executive
Dashboard-2 textbox `0fb6bdf75ea43a197450` "Reliability Performance & Drivers" → "Electricity
demand and grid planning". Subtitles stay.

**F3. Titles: replace the overclaiming and unverified wording** (every copy of each visual).

| # | Visual id(s) | Current title | New title (verified wording) | Basis |
|---|---|---|---|---|
| 1 | Growth `3e0ddca78b79485a3fea`, ED-2 `f3f57290918057748a49` | Commercial sales up 65% since 2013 on 8% more customers. That gap is data centres | Commercial sales up 65% since 2013 on 8% more customers, consistent with large round-the-clock loads | part C; D14; F14 |
| 2 | Weather `0cdbc9919c3afef37960`, ED-1 `1bc8e4107099744b0737` | Remove the weather and the underlying number has not moved since 2015 | Adjusted for storm days (a model estimate), SAIDI shows no clear trend since 2015 | part C said "roughly flat"; the adjusted series runs 122 to 149 (2015–2025, recomputed by B from the D6 fit), so "no clear trend" is the defensible wording; D to confirm with sql/07 Q10 |
| 3 | Weather `cd3dca34756db97f5ed6`, ED-1 `826577f03738cae22210` | More storm days, more outage minutes. 2025 sits where its weather predicts | More storm days, more outage minutes (r = 0.70, 10 years) | part C; F05 |
| 4 | Weather `d2efd4d136e889ee2b0e` | Major storms are half of all outage minutes in 2025, and the whole of the bad years | Major-event days are about half of all-event SAIDI in 2025 | part C; F06 |
| 5 | Scorecards card `268053916982bec30f81` (field label) | Storm Share (measure "Share of outage mins caused by major storms") | Major-event-day share | part C; F7 |
| 6 | Weather `dcda2b950535cd9fed73` | Same storms, different outcome: co-op outage frequency up 37% since 2015, Dominion up 14% | Since 2015, Virginia co-op outage frequency rose 37% and Dominion's 14% | "same storms" is not shown by the data; F09 |
| 7 | Seasonal `e1c9d78e2ce3b1f88809`, ED-2 `10a79b0633cd9c8e9009` | Winter peak now matches summer: higher in 2022, 2025 and 2026 | Winter set the year's peak in 2019, 2022 and 2025; 2026 is a near-tie so far | F12 (2019 was missing; 2026 gap 29 MW) |
| 8 | Growth `7b0e71f981e225998e87`, ED-2 `71ceb4a586c3d3d3acb9` | Load growth 2019 to 2025 by hour of day: night +41%, afternoon +27% | Load growth 2019 to 2025 by hour of day: 4 a.m. +41%, 4 p.m. +27% | F11 (single hours) |
| 9 | Growth `1b2743b4ff761d5db85f`, ED-2 `1d92052046d0a3c7b466` | The meters are installed. Almost nobody is on a rate that uses them | Nearly every customer has a smart meter; few are on a time-varying rate | F15 partial: keep only if D verifies the time-varying share from EIA-861 Dynamic Pricing; otherwise "Smart meters reached 99.8% of meters by 2025" |

Unchanged and verified: "Outages per customer up 6% since 2019, most of it after 2023" (1.244 →
1.320; 2023 was 1.165), "Minutes to restore each outage down 9% since 2019" (120.5 → 109.4),
"Fourth-highest outage minutes of twelve large utilities, 2023 to 2025" (F07), "Restoration time is
mid-pack. Outage frequency is the gap" (F08).

**F4. Remove the peer slicer from the landing page.** Delete slicer `56198e8c521b4d60a663`
(`DIM_UTILITY[PEER_GROUP]`) on Executive Dashboard-1 and add a page-level filter
`DIM_UTILITY[PEER_GROUP] = "Dominion Energy Virginia"` (as Scorecards already has). Peer filtering
stays on the Fair comparison page. Keep the Year slicer `d841e406606cb6877656`.

**F5. Wrong axis title.** Value-axis title "Index, 2023 = 100" → "Index, 2013 = 100" on
`3e0ddca78b79485a3fea` and `f3f57290918057748a49` (the subtitle already says 2013 = 100).

**F6. Replace raw-column sums with measures** (10 visuals, 18 fields; each works today only because
of page filters).

| Visual | Field now | Replace with |
|---|---|---|
| Scorecards card `4815afead0c6a4a7ca4b` | Sum of FCT_RELIABILITY[Customers Served] | `[Total Customers]` |
| What Moved `eb9e34101c7ddbafa3ba` | Sum of SAIFI_EX_MED | `[SAIFI ex MED]` |
| Weather `0cdbc9919c3afef37960`, ED-1 `1bc8e4107099744b0737` | Sum of SAIDI_WEATHER_ADJUSTED[SAIDI_EX_MED], [WEATHER_ADJUSTED_SAIDI] | `[Actual SAIDI]`, `[Weather-adjusted SAIDI]` (new, `SELECTEDVALUE`) |
| Weather `cd3dca34756db97f5ed6`, ED-1 `826577f03738cae22210` | Sum of V_STORM_VS_SAIDI[STORM_COUNTY_DAYS], [SAIDI_EX_MED] | `[Storm county-days]`, `[SAIDI ex MED (weather table)]` (new, `SELECTEDVALUE`) |
| Growth `3e0ddca78b79485a3fea`, ED-2 `f3f57290918057748a49` | Sum of three LoadGrowth index columns | `[Commercial sales index]`, `[Commercial customers index]`, `[Residential sales index]` (new) |
| Growth `7b0e71f981e225998e87`, ED-2 `71ceb4a586c3d3d3acb9` | Sum of DOM_LOAD_PROFILE[GROWTH_PCT] | `[Hour growth %]` (new, `SELECTEDVALUE`) |

**F7. Measures that disagree with the repo or aggregate wrongly** (fix in the file and in the
updated `powerbi/measures.dax`):
- "Share of outage mins caused by major storms" sums SAIDI ratios across rows → replace with
  `Major-event-day share = DIVIDE([SAIDI all events] - [SAIDI ex MED], [SAIDI all events])`
  (customer-weighted; keep a `Storm share` alias only if a visual still needs the old name).
- `Floor MW`, `Peak MW`, `Winter peak MW`, `Summer peak MW` use `SUM` → `MIN`/`MAX` (annual extrema,
  as in the repo).
- `Smart meter share %`, `Time-varying rate %` use `SUM` → `SELECTEDVALUE` (a share cannot be summed).
- `SAIFI index 2015` → the repo's `HASONEVALUE` + `REMOVEFILTERS` version.
- `Method` returns "Mixed" → the repo's version ("Changed", "Own rule", "IEEE").
- `Outage Mins/Customer` duplicates `SAIDI 2023 to 2025` → delete after re-pointing its visuals (none
  found in the decode).
- `Row colour` `#118DFF` → `#E8F0FB`; `Hour colour` (`#118DFF`, `#E8D166`, night from 22:00) →
  conventions (`#0A66C2` night 23:00–06:00, `#B8BCC2` evening, `#E8B117` day).
- Every measure gets a Description (TMDL `///` comment), shown in the field-list tooltip.

### P1

**F8. Clean the model.** Delete tables `Headline`, `V_STORM_VS_SAIDI (2)`, `V_TREND`,
`STORM_INDEX`; delete the empty measure `Measure`; delete the relationship `Headline[losses_pct]` →
`Programmes2025[losses_pct]` (goes with Headline); File → Options → Current file → Data load →
untick "Autodetect new relationships after data is loaded".

**F9. Home for the year-slicer measures.** Create `_Measures` (Home → Enter data, one column, load),
move the five `Selected …` measures there (Model view → measure → Properties → Home table), then
delete `AmiEventStudy` (headers never promoted, `Column1–4`, used by no visual).

**F10. Page names and order** (docs/00 tab names; new pages from P2):
1 Summary (was Executive Dashboard-1, landing) · 2 Scorecard (Scorecards) · 3 What moved ·
4 Weather · 5 Fair comparison (Peer Comparision) · 6 Outages by county (new) · 7 Storms (new) ·
8 Growth · 9 Demand and seasons (Seasonal, expanded) · 10 Demand summary (Executive Dashboard-2) ·
11 Data notes (new).

**F11. Data notes page.** The `Tests` table (T1–T6 from the workbook, plus T7–T12 and T13+ from D),
the `Reconciliation` sheet (metric, rebuilt, annual report, page: 133.0 vs 133, 130.2 vs 130, …),
a text box with method notes and sources, and "Data snapshot: 1 Nov 2026, Import" (decision D13).

**F12. Formats, typos, theme, alt text.**
- "Peer Comparision" → "Fair comparison"; "data centres" → "data centers" everywhere.
- SAIDI cards show 144.40 → one decimal (144.4); keep 2.68M.
- Theme JSON (`04_powerbi/theme_dominion_review.json`): data colours in conventions order
  (`#0A66C2`, `#B8BCC2`, `#6B7280`, `#E8B117`, `#1F2A44`), Segoe UI, title 14 pt Semibold
  `#1F2A44`, subtitle 10 pt `#6B7280`, no visual borders or shadows, white page.
- Alt text on every visual: 44 today (43 after F4), none has any (text per visual delivered in the
  guide: title + what it shows + the key number).
- Year slicer default 2025 stays; peer slicer only on Fair comparison.

### P2 (new data, built after D's tables land)

| Page | Visuals | Tables (D4) | Notes |
|---|---|---|---|
| Outages by county | shape map of Virginia counties (outage customer-hours or non-major events per 10k customers, 5-class blue ramp); table of the ten largest events; restoration curve (percent of peak restored by hours since peak) with an event slicer | `DIM_COUNTY`, county-day or county-year outage fact, `FCT_OUTAGE_EVENT`, `FCT_RESTORATION_CURVE`, VA county TopoJSON | Shape map works offline with a custom TopoJSON (enable it in Options → Preview features if this build still lists it there). Subtitle states the county rule and that EAGLE-I counts every utility in a county. |
| Storms | shape map of storm county-days; column timeline of storm county-days by year and type (wind, winter, tropical) | `FCT_COUNTY_DAY`, `STORM_INDEX` (or `storm_vs_saidi.csv`) | Association only. |
| Demand and seasons | matrix heatmap hour × month (average MW, conditional background in the sequential blue ramp); winter vs summer peaks by year; residential / commercial / industrial sales and customers | `DOM_LOAD_HOURLY` aggregate, `DOM_LOAD_ANNUAL`, `FCT_SALES_SECTOR` | DOM zone ≠ retail territory, said in the subtitle. |

## 3. Method

**Guaranteed path (always delivered, `deliverables/04_powerbi/`):** `APPLY_GUIDE.md` in three timed
stages (Stage 1 P0 ≈ 30 min: F1–F6; Stage 2 P1 ≈ 25 min: F7–F12; Stage 3 P2 ≈ 30 min: new pages),
the updated `measures.dax` (with purpose comments), a TMDL script the candidate pastes into **TMDL
view → Apply** to create or replace every measure at once (faster and safer than 38 manual edits),
the theme JSON, the M script per table, the data files, and the alt-text list.

**Optional edited copy (B5, after P1–P3 v1):**
1. Copy the original; open it in Desktop; click through the security prompt with MSAA (scoped to
   that window).
2. File → Save as → Power BI project (.pbip), driven by UI Automation; check the folder has
   `*.SemanticModel/definition/*.tmdl` and `*.Report/definition/pages/...`.
3. Text edits: partitions → Import with `Csv.Document(File.Contents(DataFolder & …))`, parameters in
   `expressions.tmdl`, measures from the updated `measures.dax`, deletions (F8, F9); report JSON for
   F2–F6, F10, F12 (titles are `visualContainerObjects.title[0].properties.text`, axis titles
   `objects.valueAxis[0].properties.titleText`, alt text `visualContainerObjects.general[0].properties.altText`,
   page names `page.json displayName`, slicer removal = delete its `visuals/<id>` folder).
4. Reopen the .pbip, Home → Refresh (UIA), screenshot every page, fix, repeat; then File → Save as
   .pbix. Never claim it works without the screenshots; if a step fails twice, ship the guide only and
   mark the copy "not delivered".
5. Never touch the original file; close only the Power BI process this run started.

## 4. Verification checklist (for the copy and for the guide's end state)

- [ ] Wi-Fi off: Refresh succeeds; all 11 pages draw (screenshot each).
- [ ] Every title in F3 matches the table; no "data centres", no "Comparision".
- [ ] Landing page has no peer slicer; changing the year slicer changes only the cards.
- [ ] No visual uses "Sum of" a ratio column (Format pane → field wells show measures).
- [ ] Data notes shows the tests and the reconciliation (133.0 vs 133; 130.2 vs 130).
- [ ] Alt text present (Selection pane spot-check of 5 visuals).

## 5. Hand-offs

**To D** (CSV in `data/output/`, snake_case file names, column names as in the mart so the M can
upper-case them): `fct_reliability.csv`, `dim_utility.csv`, `v_group_index.csv`,
`saidi_weather_adjusted.csv`, `dom_load_annual.csv` (all columns, including `peak_mw` and
`hours_missing`; the committed `dom_annual.csv` lacks `peak_mw`), `dom_top50_hours.csv`,
`dom_load_profile.csv`, and the new D4 tables (county, events, restoration curve, county-day, hourly
or hour × month load, sector sales) plus a Virginia county TopoJSON. `V_STORM_VS_SAIDI` can load
from the committed `storm_vs_saidi.csv`. Please also confirm sql/07 Q10 (slope of the
weather-adjusted series) for F3 row 2, and whether the time-varying-rate share is verified (F3 row 9).

**To the orchestrator:** this plan changes nothing in the repo yet. B5 will deliver an updated
`powerbi/measures.dax` (D commits), and the theme and M files live in `deliverables/04_powerbi/`.
