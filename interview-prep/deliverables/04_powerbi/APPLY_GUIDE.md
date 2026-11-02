# Power BI report: how to open and apply it

The extended Dominion reliability report ships as a Power BI template. It holds the report and the
model but no data. When you open it, it asks for one folder, your clone's `data\output\`, then
imports every table from the CSV files there: there is no Snowflake connection, gateway or sign-in.

**You need** a Windows laptop with Power BI Desktop (free from the Microsoft Store; Desktop runs
only on Windows).

**Use it only with the adopted extension.** The folder must be the branch's `data\output\` (EAGLE-I
counties and events, storm types, tests T1 to T31, the D22 storm counts), so fetch the branch into
your clone first (`05_repo/README.md`, step 1). If you present the public-repo-only version, use
your own report instead.

**Deadline:** if the template isn't open and checked by your decision time (11:15 on Monday in
START_HERE's plan), present the public version. Route B takes 2 to 3 hours; it is not for Monday.

## What is in this folder

| File | What it is |
|---|---|
| `Dominion_reliability_review.pbit` | The report (11 pages, 60 visuals) and the model (18 imported tables, 77 measures, 2 relationships). The branch has the same file at `powerbi\` |
| `measures.dax` | Every measure and calculated column, grouped by table, with its purpose above it. The same text is each measure's description in Desktop |
| `m/` | The Power Query (M) for each table, plus the `DataFolder` parameter |
| `theme_dominion_review.json` | The report theme: subject blue `#0A66C2`, context gray `#B8BCC2`, gold `#E8B117` for a third category, ink `#1F2A44` |
| `alt_text.csv` | The alt text on each visual |

## Route A: open the template (recommended, about 5 minutes)

1. **Update Power BI Desktop.** The template was built and tested in version 2.159 (October 2026),
   and it uses the newer report format, so older versions may refuse it.
2. **Have the branch checked out.** In your clone, `git switch interview-upgrade-2026-11`
   (`05_repo/README.md`, steps 1 and 2).
3. **Open the template.** Double-click `Dominion_reliability_review.pbit`. Desktop asks for
   **DataFolder**, and the box already holds the example
   `C:\path\to\dominion-reliability-review\data\output\`. Replace it with your clone's own
   `data\output\` folder; the path must end with a backslash. Then click **Load**.
4. **Wait for the load.** It takes about a minute. If a query fails, the path is the usual cause:
   use Transform data > Edit parameters > DataFolder, then Refresh.
5. **Save as a .pbix.** File > Save As > `Dominion_reliability_review.pbix` (`*.pbix` is gitignored).
6. **Check four things:**
   - **Scorecard:** 2025 shows 2.68M customers served, SAIDI 144.4, SAIFI 1.320 and CAIDI 109.4.
   - **Data notes:** "All 31 data tests pass" and "Rebuilt values match the published ones (12 of 12)".
   - **Fair comparison:** the dashed lines sit at the 11-peer medians, SAIFI 0.93 and CAIDI 99.5.
   - **Number format:** numbers follow your Windows regional format, so a US machine shows 2,675,735.

**Later data:** to refresh, rewrite the files in `data\output\` (same names; `05_repo/README.md`,
step 5) and click Home > Refresh. To use another folder, edit the DataFolder parameter.

## Route B: rebuild by hand in your own .pbix (fallback, 2 to 3 hours)

Use this only if the template will not open.

1. Home > Transform data > Manage parameters > New: `DataFolder`, type Text, current value = your folder, ending with `\`.
2. For each table in `m/`, open its query's Advanced Editor and replace the text with the file's text.
   Tables your file does not have: New source > Blank query, paste, rename to the file name.
3. Remove `Headline`, `V_TREND`, `STORM_INDEX`, `AmiEventStudy` and the second storm view. Their
   visuals move to the measures and tables in `measures.dax`.
4. Add the measures from `measures.dax` to the table named in each section. `_Measures` is a
   calculated table: `ROW("Measures", 0)`, with its column hidden.
5. View > Themes > Browse for themes > `theme_dominion_review.json`.
6. Make the report changes listed below by hand.

## What changed from the original report

**Data**
- Every table imports from `data\output\` through `DataFolder`. The original had six DirectQuery
  tables against Snowflake plus workbook sheets (D13: DirectQuery for development, Import for
  presentation). The two workbook tables now read their CSV exports, `load_growth.csv` and
  `programmes_2025.csv`.
- Storm figures come from `storm_vs_saidi.csv`, after D22 (Bedford city counted once). The
  workbook's `StormIndex` sheet predates D22 and is no longer read.
- Auto date/time is off.

**Measures**
- Charts use customer-weighted measures, not summed columns: sum the numerators, sum the
  denominators, divide once.
- Renamed: Storm share → Major-event-day share; Storm SAIDI → Major-event-day SAIDI.

**Titles**
- The two landing headers now match their pages: "Reliability performance and weather" and
  "Electricity demand and grid planning" (the original had them swapped).
- CAIDI is labeled "minutes per interruption" on every page, not "minutes to restore": it is SAIDI ÷
  SAIFI, a ratio, not a measured restoration time.
- The hour-growth columns are colored by the hours their title names: hours ending 1 to 5 a.m. blue,
  1 to 5 p.m. gold, the rest gray.
- Each title states a finding in plain words, with no causal claims from correlations. For example:
  - Weather: "Years with more storm days had more outage minutes", with "association, not cause" in the subtitle.
  - Growth: "consistent with large round-the-clock loads".

**Pages**
- Renamed and reordered (list below).
- New pages: Outages by county, Storms and Data notes.
- Demand and seasons gains the 24-hour profile and sales by customer class.
- Scorecard gains the reconciliation table.
- Dates read US-style (Oct 29, 2026).

**Summary page**
- The peer slicer is replaced by a page filter for Dominion Energy Virginia.

**Charts**
- The storm scatter shows the fit years 2015 to 2024 (n = 10), so its trend line is the fit behind
  the weather adjustment: 104.3 + 0.0518 × storm county-days, r = 0.70.
- The SAIFI trends use a continuous year axis, so the 2015 and 2020 counting-change lines show, as
  docs/06 intends.
- What moved stacks its two trends at full width.
- The peer quadrant's dashed lines are the medians of the 11 peers, excluding Dominion.
- The peer table's storm-rule column covers 2014 to 2025, the years compared, so ten of the twelve
  show IEEE 1366. Georgia Power and Duke Energy Florida filed "Other" in 2013 only.
- Explicit series colors; the axis title "Index, 2013 = 100".

**Accessibility**
- Every visual has alt text.

## The pages

Eight of the eleven pages are your own October pages, renamed and re-pointed to CSV with the
changes listed above. Three are new on November 1.

| # | Page | From | Question it answers |
|---|---|---|---|
| 1 | Summary | October | How did 2025 go, and how do storms relate to outage minutes? (Year slicer sets the cards) |
| 2 | Scorecard | October, plus the reconciliation table | 2025 in Dominion's own measures, with the reconciliation table (12 of 12) |
| 3 | What moved | October | Frequency (SAIFI) and minutes per interruption (CAIDI) since 2013 |
| 4 | Weather | October | Major-event days, the storm-day fit, the weather-adjusted trend, the co-op comparison |
| 5 | Fair comparison | October | Dominion against 11 large peer utilities, 2023 to 2025 and 2021 to 2025 |
| 6 | Outages by county | New | County outage minutes and the ten largest outage events (EAGLE-I, all utilities) |
| 7 | Storms | New | Storm types by year (NOAA) and the Isaias restoration curve (EAGLE-I, all utilities) |
| 8 | Growth | October | Sales and customer indices since 2013, load growth by hour of day, smart meters and time-varying rates |
| 9 | Demand and seasons | October, plus the 24-hour profile and sales by class | Winter vs summer peaks, the 24-hour demand profile, sales by customer class (TWh) |
| 10 | Demand summary | October | Demand on one page: seasonal peaks, growth by hour, three cards (lowest hour +52%, top-50 hours 47, peak hour +26%), sales index, smart meters |
| 11 | Data notes | New | Sources, method, the 31 data tests and the 12 reconciled figures |

## The model, in one honest line

The model has 18 imported tables, 2 calculated tables (`Dashboard Year` for the slicer and
`_Measures`) and 2 relationships. The core is a small star: `FCT_RELIABILITY` (utility × state ×
year) many-to-one to `DIM_UTILITY`, with customer-weighted measures. The other tables are pre-built
summaries for particular pages, so most stand alone; only the ten largest outage events join their
restoration curves. In production you would conform them to shared date and county dimensions. The
brief's Q11 has the spoken version.

## Reading notes

- **EAGLE-I figures are not Dominion's SAIDI.** On Outages by county and Storms, EAGLE-I counts
  every utility's customers in Dominion's 103 counties (D15). Read them as places, not as one
  utility's performance.
- **Hours to clear 90%** run from the peak until customers out stay at or below the pre-event level
  plus 10% of the peak's excess. This is a net count. It is not a utility's "% of affected customers
  restored".
- **The weather-adjusted series is a model estimate.** "No clear trend" rests on
  `scripts/trend_tests.py`: +0.34 minutes a year, 95% CI −1.41 to +2.08.
