# V4 print proof: the v3 print PDFs

**Scope.** The four files to be printed:
- both decks (adopted and public), as US Letter landscape print PDFs
- the question sheet
- the brief

The PPTX files are not printed.

**Method** (`work/reviews/v4_scripts/v4_proof.py`, PyMuPDF):
- **Size and type:** page count and size; the smallest text on each page in printed points; the embedded fonts.
- **Margins:** the nearest text to any page edge, measured over all words.
- **Images:** the smallest effective resolution of each placed raster image, in pixels per printed inch.
- **Proofs:**
  - Every page was rendered at 100 dpi in color and again in true grayscale (the PyMuPDF gray colorspace, what a mono printer gets).
  - I looked at every page in both renders, as contact sheets: decks 4 pages a sheet in color and 6 in grayscale; the sheet 2 a sheet; the brief 3 a sheet in color and 6 in grayscale.
  - Pages that needed a closer look were opened at full size.
  - The PNGs are in `work/reviews/v4_pages/<document>/`.

**Pass rules:**
- The sheet is 2 pages, printed as one double-sided sheet; the brief is at most 12 pages.
- Text is at least 9 pt (decks at least 10 pt as printed).
- All fonts are embedded.
- Text is at least 0.30 in from every edge, since many printers cannot print the outer 0.17–0.25 in.
- Images are at least 200 ppi.
- Nothing is clipped or overlapping.
- Every chart still reads in grayscale: the subject series is darker than its context, and gold never sits beside light gray as the only difference.

**Result: all four pass.**
- The sheet is 2 pages (one sheet) and the brief 12 pages.
- The decks' smallest text is 10.12 pt; the sheet's and the brief's is 9.0 pt.
- All fonts are embedded and no image is under 305 ppi.
- No page has clipped, overlapping or overflowing content, and every page reads in grayscale.

**Found and fixed on the way** (v2 dry run, 11:07; fixed in v3):
- The sheet's footer "Side 1 of 2" ended 0.135 in from the bottom edge, which many printers cannot print.
- The brief's running header and footer came within 0.208 in.
- Both now clear 0.30 in: the sheet 0.323 in, the brief 0.385 in. The builders now fail below 0.30 in.

**Noted, not defects:**
- On the talk's slide 2 and the brief's page 3, the gold storm-day bar prints at the same gray as the CAIDI and SAIDI bars. Each bar sits in its own labeled row with its value, so the design rule holds.
- The report screenshots (deck slide 5, brief page 7) carry small text by nature. They are sharp at 305–560 ppi, and the cards and titles are legible.

**Print settings** (as in START_HERE):
- US Letter, Actual size (100%).
- Decks double-sided, flipped on the short edge (the presenter's copy single-sided).
- The sheet as one double-sided sheet.

**Proofed files:** the v3 PDFs as listed below, modified 1 Nov.

## Summary

| Document | File (modified) | Pages | Page size | Smallest text | Fonts embedded | Nearest text to an edge | Smallest image resolution |
|---|---|---|---|---|---|---|---|
| Deck, adopted (print) | `deliverables/01_deck/Dominion_reliability_deck_v3_print_letter.pdf` (01 Nov 11:13:23) | 14 | 11.0 × 8.5 in | 10.12 pt | 4 of 4 | 0.95 in | 400 ppi |
| Deck, public (print) | `deliverables/01_deck/Dominion_reliability_deck_v3_public_print_letter.pdf` (01 Nov 11:13:30) | 14 | 11.0 × 8.5 in | 10.12 pt | 4 of 4 | 0.95 in | 305 ppi |
| Question sheet | `deliverables/02_question_sheet/Dominion_question_sheet_v3.pdf` (01 Nov 11:34:28) | 2 | 8.5 × 11.0 in | 9.0 pt | 2 of 2 | 0.323 in | no raster images |
| Brief | `deliverables/03_interview_brief/Dominion_interview_brief_v3.pdf` (01 Nov 11:34:47) | 12 | 8.5 × 11.0 in | 9.0 pt | 9 of 9 | 0.385 in | 560 ppi |

## Deck, adopted (print)

14 pages, Letter landscape. The talk's slides are imposed at the print scale, centered with wide top and bottom margins. Smallest text is 10.12 pt (the source lines). The nearest text is 0.95 in from an edge, and every chart image is 400 ppi. No defects.

| Page | Smallest text | Color | Grayscale |
|---|---|---|---|
| 1 | 10.12 pt | Title page: name and date only, data line. Clean | Clean |
| 2 | 10.12 pt | 130 → 133 with four labeled change bars (storm days gold, SAIFI blue, CAIDI and SAIDI gray). Nothing clipped | The gold storm bar prints as light as the gray bars. Each bar has its own labeled row, so the rule holds |
| 3 | 10.12 pt | Peer quadrant, 11-peer medians 0.93 and 99.5 labeled, Dominion in blue. Labels clear of the points | Dominion's dot is the darkest; median lines visible |
| 4 | 10.12 pt | Storm vs calm bars, 332.8 vs 27.9 with intervals; the 11.9× panel | Storm bar dark, calm bar light |
| 5 | 10.12 pt | Summary-page screenshot of the final template, 400 ppi (cards 2.68M, 144.4, 109.4, 1.320, 53%; 'Minutes per interruption'), with the model and DAX. Screenshot text is small but sharp | Screenshot lines and cards readable |
| 6 | 10.12 pt | Pipeline diagram; '31 tests pass: Original build 12 (6 reliability, 3 storm, 3 demand). New tables: 19' | Clean |
| 7 | 10.12 pt | Three 30/60/90 columns, equal heights, text inside the boxes | Clean; column tints print light |
| 8 | 10.12 pt | Three takeaways, experience map, thank-you line | Clean |
| 9 | 10.12 pt | A1: definition boxes and MED text | Clean |
| 10 | 10.12 pt | A2: table 2015–2025 with fit notes; 2025 row highlighted | The highlight prints light gray; table clean |
| 11 | 10.12 pt | A3: hour chart, hours ending 1–5 a.m. blue, brackets for 1–5 a.m. and 1–5 p.m. | Blue bars dark, the rest light |
| 12 | 10.12 pt | A4: sources table; test line T1–T6 / T7–T9 / T10–T12 / T13–T31 | Clean |
| 13 | 10.12 pt | A5: limits table | Clean |
| 14 | 10.12 pt | A6: ten largest events with the Isaias curve inset (400 ppi) | Curve and table clean |

## Deck, public (print)

14 pages, Letter landscape, the same layout as the adopted deck. Smallest text is 10.12 pt and the nearest text 0.95 in from an edge. Chart images are 400 ppi; the report screenshot on slide 5 is 305 ppi. No defects. The slide 3 chart was also checked at 200 dpi: the two 'median of the 12 (including Dominion)' labels sit clear of every point and label.

| Page | Smallest text | Color | Grayscale |
|---|---|---|---|
| 1 | 10.12 pt | Title page; data line without EAGLE-I | Clean |
| 2 | 10.12 pt | As adopted, with 723 → 796 | As adopted: the labeled rows carry the gold bar |
| 3 | 10.12 pt | Quadrant with the medians of the 12, including Dominion (0.96 and 105). 'Methods differ…; ranks are indicative' | Dominion's dot is the darkest; median lines visible |
| 4 | 10.12 pt | Storm scatter with the 2015–2024 fit and 2025 labeled; 465 → 796; r = 0.70 | The 2025 point is dark, the rest light |
| 5 | 10.12 pt | Frequency chart from the current report's What moved page (305 ppi), with the model and DAX | Line and labels readable |
| 6 | 10.12 pt | Pipeline; 12 tests; D1–D14; 'DirectQuery in development (D13)' | Clean |
| 7 | 10.12 pt | As adopted | Clean |
| 8 | 10.12 pt | As adopted; the storms-by-county line reworded | Clean |
| 9 | 10.12 pt | A1, with 'methods differ between utilities' | Clean |
| 10 | 10.12 pt | A2: public fit table (125.9, 124.4, 128.2), R² 0.48 | Clean |
| 11 | 10.12 pt | A3: hour chart, '4 a.m.: +41%', '4 p.m.: +27%' | Blue bars dark |
| 12 | 10.12 pt | A4: public sources, T1–T12 | Clean |
| 13 | 10.12 pt | A5: limits table | Clean |
| 14 | 10.12 pt | A6: 12-utility table with 'Mixed' and its footnote | The Dominion row prints light gray; clean |

## Question sheet

2 pages, US Letter portrait, printed double-sided as one sheet. 9.0 pt throughout. The nearest text is 0.323 in from an edge (v2: 0.135 in, the 'Side n of 2' footer, which some printers would clip; fixed in v3). No defects.

| Page | Smallest text | Color | Grayscale |
|---|---|---|---|
| 1 | 9.0 pt | Side 1: Q1–Q12 in two columns; [you: …] items highlighted; footer well inside the margin | Highlights print as light gray bands; all text black |
| 2 | 9.0 pt | Side 2: Q13–Q24, the five questions to ask and the closing line; some space left under Q18 | Clean |

## Brief

12 pages, US Letter portrait (limit 12). Smallest text is 9.0 pt (tags and appendix tables). The nearest text is 0.385 in from an edge (v2: 0.208 in, the running header and footer; fixed in v3). The screenshot on page 7 is 560 ppi. No defects.

| Page | Smallest text | Color | Grayscale |
|---|---|---|---|
| 1 | 9.0 pt | Cover and contents | Clean |
| 2 | 9.0 pt | Talk table with adopted · public times (7:54 / 7:38) and the two-sided lines | Clean |
| 3 | 9.0 pt | Finding 1: change bars and the split table; If-asked box | The gold storm bar is labeled in its own row |
| 4 | 9.0 pt | Finding 2: quadrant (11-peer medians) and the peer table; caveat box | Clean |
| 5 | 9.0 pt | Finding 3: EAGLE-I map with legend; the 31 mapped counties are labeled as such | The map ramp reads light to dark |
| 6 | 9.0 pt | Finding 4: hour chart; white space at the foot | Blue bars dark |
| 7 | 9.0 pt | Summary screenshot 5.0 in wide (560 ppi), caption, model and sources table | Readable |
| 8 | 9.0 pt | Role, the 90-day table, limits, logistics with [you: …] | Clean |
| 9 | 9.0 pt | A1 number table fills the page; nothing cut off | Clean |
| 10 | 9.0 pt | A2–A3 hard questions in two columns at 9 pt | Clean |
| 11 | 9.0 pt | A2–A3 continued; HR column | Clean |
| 12 | 9.0 pt | A4: delivery tables and the rehearsal outline | Clean |

