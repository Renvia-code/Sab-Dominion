# V1 coverage and consistency: numbers in the v2 deliverables vs claims.csv

Snapshot audited: `interview-prep/work/reviews/snapshot_v2_1035/` (both decks: PPTX slide text, alt text, tables and speaker notes, plus the print PDFs; the brief and the question sheet as HTML and PDF).
Text dumps: `v1_text/`. Every token with the claim rows it matched: `v1_work/coverage_tokens.csv`.
Scripts: `v1_scripts/x01_extract_text.py`, `x02_coverage.py` (numeric match at printed precision), `x03_coverage_strict.py` (the matching row must also name the document and share its wording), `x04_consistency.py`.

**Method.** I extracted 2,345 numeric tokens. I skipped:

- year labels from 2013 to 2027 (I checked each years-as-data row on its own);
- page and slide numbers, and line-start item numbers;
- letter-prefixed ids (Q, T, D, P, A, S);
- the document date.

The automatic pass left 36 tokens unmatched. Small integers can match an unrelated claim by accident, so I also read every deliverable in full and checked each data-bearing number by hand. The list below combines both passes.

## 1. Numbers with no claims.csv row

| # | Where | Printed | Checked by me | Severity |
|---|---|---|---|---|
| U1 | Brief Q3 | "EIA-861 lists 103 Dominion counties, **33** of them Dominion-only (D15)" | True. `mart.DIM_COUNTY` has 33 Dominion-only counties: 31 on the map and 2 off it (51600 Fairfax city, 51660 Harrisonburg). | Add a row |
| U2 | Brief Q7 | "Dominion trims on **4–5-year** cycles" | Register row R-076 (Dominion tree-trimming page) exists, but claims.csv has no row. I did not open the source. | Add a row and verify |
| U3 | Adopted deck S5, inside the Power BI screenshot (an image, so not extractable) | Chart titles "Outages per customer up **6%** since 2019" and "Minutes to restore each outage down **9%** since 2019"; point labels 1.24, 1.17, 120.5, 105.9, 122, 136, 133; "10 yr Avg" | All true: SAIFI 1.244 → 1.320 is +6.1%, CAIDI 120.48 → 109.39 is −9.2%, and the weather-adjusted values are 122.4, 135.7 and 133.1. C-S5-11 covers only the five cards. | Add a row (the panel sees these) |
| U4 | Brief A4 | r = **.42**, r = **.20**, r = **−.11 to −.19**, r = **−.19**; citation years **2015** (Ranehill), **2017** (Huang), **2018** (Powell) | Barrick 2010 (.42), Swider 2011 (.20, −.11, −.19) and all years are confirmed in Crossref/OpenAlex. Powell's −.19 rests only on the register quote, because no abstract could be retrieved. | Extend C-B-03's value list |
| U5 | Adopted deck S4 title; brief p2, p5, Q5 | "about **12** times", "The 12×" | Rounded from 11.944. C-S4-08 lists 11.9 but not 12. | Minor |
| U6 | Brief Q24 (spelled out in words) | "about an hour and fifty minutes each time", "almost two and a half hours in the year", "rose about three minutes" | Consistent: 109.4 min is 1 h 49 min, 144.4 min is 2 h 24 min, and the rise is 2.8 min. Not in the register. | Minor |
| U7 | Adopted deck A4 table | HURDAT2 grain "storm × **6**-hour fix" | Source property. Not checked against the data (HURDAT2 also carries landfall records off the 6-hour cycle). | Minor |
| U8 | Brief p2 | "about 7:40, leaving **two** minutes for interruptions" (implies a 10-minute slot) | No source for the slot length. | Minor |
| U9 | Brief A4 / A2 title | "**5–6** true STAR stories", "**30**-second" opener, "**8**-minute timer, **three** times", "The **25** hardest questions" | Advice or document structure, not data. | Ignore |
| U10 | Ignored identifiers and constants | "utility **19876**", IEEE "**1366**", "**2.5**β", "five years" (the MED method), "Days 1–30/31–60/61–90", "30–60-day deliverable", "30-day plan", chart axis ticks (brief p4: 0.6–1.4 and 60–140; p6: 0–40%), "24 hours", "2022–24" | Not data. | Ignore |

**Rows whose used_in field omits a place where the number appears.** These are documentation gaps; the numbers themselves are verified.

- C-Q-06 ($690M, 440) also appears in brief A1.
- C-Q-03 (71% → 90%) also appears in brief A1 and Q17.
- C-Q-08 (25%) also appears in brief A1.
- C-S8-01 (20M+) also appears in brief A1 and Q16, and in question-sheet items 1, 11 and 14.
- C-S5-04 (19,803 → 24,957; 7,167 → 10,903 MW) also appears in the brief p6 text.

## 2. Same number stated differently, or contradicted, across places

| # | Issue | Where | Evidence |
|---|---|---|---|
| I1 | **Test split mislabelled.** The decks say "31 tests pass: **12 on the reliability mart**, 19 on the new tables" and "T1–T12 on the reliability mart … T13–T31 on the county outage, storm and load tables". | Adopted deck S6 badge, S6 notes and A4 (C-S7-05A) | `test_results.csv` and docs/03: T1–T6 test the reliability mart (sql/04), T7–T9 test NOAA storms (sql/05), T10–T12 test EIA-930 demand (sql/06). So only 6 tests are on the reliability mart, and storm and load tests appear in both groups. The public deck's A4 describes T1–T12 correctly. |
| I2 | **CAIDI is called "minutes to restore".** The brief also says "CAIDI is a ratio, not restoration speed". | Adopted deck S5 card and alt text, and brief p7 ("minutes to restore 109.4"), against brief A1 and Q4 | Same value, 109.4, given two incompatible meanings. A panel engineer is likely to catch it. |
| I3 | **Talk timings fit only the adopted deck.** The brief's talk table is single-version. | Brief p2 | Adopted notes: 1,005 words, 7:44 ("about 7:40"). Public notes: 977 words, 7:31. Public slide 4 runs 0:57 against the printed 1:05, slide 5 runs 0:46 against 0:55, and slide 6 runs 1:12 against 1:05. |
| I4 | Brief Q3 says "33 Dominion-only"; brief p5 says "The 31 counties Dominion serves alone". | Brief | Both are true: 33 of the 103 counties, 31 of the 99 on the map. The text never says why they differ. |

No conflicting values were found for these quantities across the deck, brief, question sheet and claims.csv: 130/133, 130.2/133.0, 2.8, 718→791 / 723→796, 464/465, 1.21 and 0.93, 110/99.5/99.3, r 0.70, 145.3, 122.3–168.2 against "about 122–168", 11.9 (7.9–16.9), 332.8/27.9 against "about 333/28", 306.7/162.3/53%, 2.68M/2,675,735, 6,077,232/6,094,320, the T and D ranges, +41/+27/+26/+52%, 47 of 50, 65%/8%, 33%/32%, 25,413/25,384, 99.8%, 500/2/5/−32%/−44%, 1.849/1.887, 50 bp, and 38 months.

The two renderings of each document carry the same numbers. The extra tokens in the PPTX are alt text, and the HTML-versus-PDF differences come only from line breaks.

## 3. Adopted-only numbers in the public deck

**None found.** I scanned the public deck's slides, alt text, notes and print PDF for all of these: EAGLE-I, T13–T31, D15–D22, 718/791/464, degree days, "12 of 12", 6,094,320, "31 tests", 25,413/25,384, Oct 29, 11.9, 6,108, 332.8, HURDAT2, DOE-417, CPC, 99.5, 11,608,442, "18 tables", DataFolder, p = 0.025, the CI and prediction interval, +0.3, Isaias, 33.5, 39–41% and 33%.

The public deck uses the right variants throughout: 723→796, 465→796, 6,077,232, "12 tests", D1–D14, 4 a.m. +41% / 4 p.m. +27%, and no p-values.

## 4. Public-deck numbers that are not printed on origin/main

| # | Public deck | origin/main says | Status |
|---|---|---|---|
| P1 | S3 and alt text: "peer median **0.93**" and "peer median **99.3**" (11 peers, Dominion excluded) | docs/05: "Quadrant lines: medians of the twelve peers: SAIFI **0.96**, CAIDI **105**" (Dominion included) | Derivable from the origin/main workbook (the median of the 11 peers' values is 0.934 and 99.3), but the public repo prints different medians. Highest risk if a panelist opens GitHub. |
| P2 | A6: Georgia Power and Duke Energy Florida labelled "**IEEE 1366**"; "**10 of the 12** file IEEE 1366 every year 2014–25" | Workbook Peers sheet labels both "**Mixed**"; docs/06: "**Half the peers** use a different reporting method" | Derivable from the origin/main input files (true by my recount), but it contradicts origin/main's own docs and labels. The fix, commit 29b179f, exists only on the local branch. |
| P3 | A2 table: 2017 **125.9**, 2023 **124.4**, 2024 **128.2** "from the fit"; "R² **0.48**" | Workbook StormIndex predicted values are 125.94, 124.44 and 128.25, from a fit on SAIDI rounded to 1 dp. No R² is printed. | A refit on origin/main's `storm_vs_saidi.csv`, the source claims.csv cites, gives 126.0, 124.5 and 128.3. That is a 0.1 difference. R² 0.484 is derivable but not printed. |

Everything else in the public deck is printed on origin/main or read directly from it: 723→796 and 465→796 (`storm_vs_saidi.csv`), r 0.70 (docs/05), the 104.4 + 0.0514 fit (docs/02 and 08), 145.3 (workbook 145.26), 6,077,232 (docs/01 and 02), D1–D14 and D13 (docs/04), T1–T12 "within 2%" (docs/03), +41/+27/+26/+52% (docs/05), 79% (docs/05), 99.8% (workbook 0.998), the `{2023, 2024, 2025}` DAX (measures.dax), "Dominion and 11 peers" (D10), and 306.7, 144.4 and 2,675,735 (workbook Tests sheet).

## 5. Register hygiene (claims.csv)

- C-S3-02's result field says "chart script median 104.85 rounds to 105". That is the 12-utility median, and the slide does not show it: the rendered S3 chart draws its lines at 0.93 and 99.5. The note is stale.
- C-S5-07's value 7.9% counts bundled-only customers in 2025, while the sales figure counts bundled plus delivery-only. On a consistent basis the growth is +8.0%. The printed "8%" is right either way.
- C-S5-12 cites `deliverables/04_powerbi/measures.dax`. The measure is in the repo's `powerbi/measures.dax`.
- C-S4-20's "average 159 vs 211" is a customer-weighted mean. Simple means would be 225 vs 361. The text does not say which.
- The A6 event peaks depend on P24 cleaning, which sets to NULL any reading above twice a county's customers. Without it, Michael would be 565,365 and March 2018 would be 538,658. The cleaning is documented and the numbers reproduce with it.
