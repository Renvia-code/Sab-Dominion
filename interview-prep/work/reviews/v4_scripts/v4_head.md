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
