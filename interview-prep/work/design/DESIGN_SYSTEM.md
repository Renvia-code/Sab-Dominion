# Design system v0: the interview pack (deck, question sheet, brief)

Scope: the visual rules every deliverable in `interview-prep/deliverables/` follows. Light and
print-first; colour meanings from `docs/00_conventions.md`; charts per the `dataviz` method. Code:
`ds.py` (Python tokens and chart helpers), `brief.css` (print CSS), `pipeline.py` (PPTX→PDF, HTML→PDF,
PDF→PNG). Computed colour facts: `palette_computed.json` (from `palette_tools.py`).

## 1. Colour (palette instance)

| Role | Hex | Use | Contrast on white | Grey in a mono print (L*) |
|---|---|---|---:|---:|
| Subject | `#0A66C2` | Dominion, or the series the title is about | 5.69 | 43.5 |
| Context | `#B8BCC2` | peers, other years, other series (fills and thin lines) | 1.91 | 76.1 |
| Second context | `#6B7280` | **text and reference lines only** (medians, rules, ticks) | 4.83 | 47.9 |
| Third category (print) | `#D5A20B` | the conventions gold `#E8B117` snapped into the dataviz light band (L 0.74) for printed marks | 2.33 | 69.5 |
| Third category (Power BI) | `#E8B117` | kept in the Power BI theme to match `docs/00` | 1.96 | 75.2 |
| Dark accent | `#1F2A44` | ink, headings, a call-out mark | 14.26 | 17.3 |

Chrome (never data): ink `#1F2A44`, ink-2 `#374151` (10.3:1), muted `#6B7280` (4.8:1), rule
`#D1D5DB`, grid `#E5E7EB`, panel tint `#F3F6FA`, subject tint `#E8F0FB` (highlighted table row).

**Sequential ramp** (one hue, the subject's OKLCH hue 254.7°, lightness strictly falling, so it
also prints as an ordered grey ramp): `#EAF3FE #C9E0FE #AACAF4 #86B1E8 #6298DC #3C7ECF #0A66C2
#00519F #013C78`. Five classes for maps and heatmaps: `#C9E0FE #86B1E8 #3C7ECF #00519F #013C78`
(grey L* 88 / 71 / 52 / 35 / 25). Counties out of scope: white with a `#D1D5DB` outline.

**Deviation from `docs/00_conventions.md` (accepted by the orchestrator, 2026-11-01 07:40):** printed
marks in the deck, brief and question sheet use `#D5A20B` for the third category instead of the
conventions' `#E8B117`. Same hue and chroma, lightness 0.79 → 0.74, so it clears the dataviz light
band and prints darker. Meaning unchanged (third category, e.g. summer). The Power BI theme keeps
`#E8B117`, so the report still matches the conventions. Nothing in the repo changes.

**Validator results** (`dataviz/scripts/validate_palette.js`, white surface):
- Subject + third (`#0A66C2,#E8B117`): CVD ΔE 36.8, normal-vision ΔE 42.1 (pass); `#E8B117` FAILS the
  lightness band (L 0.79 > 0.77) and is 1.96:1 → print marks use `#D5A20B`, and every gold mark
  carries a direct label (relief rule).
- Full conventions set, all pairs: `#6B7280` vs `#0A66C2` normal-vision ΔE 14.5 (below the 15 floor),
  and in greyscale they print at nearly the same grey (L* 47.9 vs 43.5). Hence the rule that
  `#6B7280` is never a data colour beside the subject.
- Grey context colours fail the chroma floor **by design**: they carry no identity (emphasis form:
  one subject hue, the rest grey, every non-subject series named by a direct label).

**Greyscale rules (the pack must survive a mono printer):**
1. Subject vs context is the core pair: L* 43.5 vs 76.1, distinct.
2. Gold and light grey print the same (L* 75 vs 76): never let them be the only difference. A chart
   with gold has no grey-filled series, or labels every mark.
3. Subject and dark accent differ by L* 26 plus line weight; name both with direct labels.
4. Meaning is never carried by colour alone: direct labels, legends for ≥ 2 series, and position.

## 2. Type: one family, Segoe UI

Static files on every Windows 10/11 PC (`segoeui*.ttf`, `seguisb.ttf`, `segoeuisl.ttf`,
`segoeuil.ttf`), so the PPTX renders on the candidate's laptop exactly as here; LibreOffice and Edge
embed it (checked: PDFs carry SegoeUI, SegoeUI-Semibold, SegoeUI-Semilight, SegoeUI-Light).
Weights: Light 300 (hero numbers), Semilight 350 (lede), Regular 400 (body), Semibold 600 (titles,
emphasis). No second family, no serif, no display face. Proportional figures for big numbers;
tabular figures in table columns.

| Element | Deck (slide pt → printed pt at 0.75) | Brief (pt) | Question sheet (pt) |
|---|---|---|---|
| Action title / h1 | 28 Semibold → 21 | 24 Semibold | — |
| Body | ≥ 16 → 12 | 10.5 / 15 leading | 8.5 / 10.5 leading |
| "What it means" line | 18 → 13.5 | — | — |
| Chart labels | ≥ 13.5 → 10.1 | ≥ 8.5 | — |
| Source line | 13.5 → 10.1, muted | 8.5, muted | — |
| Hero / KPI number | 54 Light → 40.5 | 40 Light | — |
| Section h2 | — | 13.5 Semibold | group 9.5 Semibold |

## 3. Layout

**Deck:** 16:9 (13.333 × 7.5 in). Margins 0.6 in left/right, 0.48 top, 0.42 bottom. Zones: title
(top, up to 2 lines), content (1.75–6.1 in), "what it means" line, source line at 6.62 in, slide
number right. No accent line under titles. Each main slide: one chart or diagram, vary the layout
(full-width chart; chart + KPI column; diagram; table).
**Print PDF:** each slide placed as vectors at 0.75 scale (10.0 × 5.625 in) centred on US Letter
landscape (0.5 in side margins), by `pipeline.impose_letter_landscape`.
**Brief:** US Letter portrait, margins 0.7/0.75/0.75/0.75 in, 12-column grid, one idea per page
(`.page` breaks), footer via CSS `@page` margin boxes (title left, "n / N" right; Edge supports them).
**Question sheet:** US Letter portrait, two columns, 0.5 in margins, both sides.

## 4. Chart rules (dataviz method, applied)

- Form first: emphasis (one subject series in blue, the rest grey) is the default; stat tiles for
  single numbers; sequential blue ramp for maps and heatmaps; no dual axes, no pies, no rainbow.
- Marks: bars capped in thickness with a rounded data-end and square baseline (`ds.rounded_bar`);
  lines 2.6 pt subject / 1.6 pt context on a slide; markers ≥ 9 pt with a white ring; gridlines
  hairline solid `#E5E7EB`; baseline `#B8BCC2`; no chart borders.
- Labels: selective (end, extreme, the point the title names); text in ink, never in the series
  colour; legend for ≥ 2 series or direct labels for each.
- Every chart is written by a script in `work/charts/` with `<stem>.png` (300 dpi), `<stem>.svg`
  (text kept as text), `<stem>.csv` (data snapshot) and `<stem>.txt` (caption and source line):
  `ds.save()`. Every number on a chart goes into `interview-prep/claims.csv`.
- Print has no hover layer: the table view is the appendix table or the brief's "know every number".

## 5. Print test (2026-11-01 07:2x): results, looked at

Files: `work/proofs/print_test/` (`print_test_deck_letter_p0{1,2}{,_grey}.png`,
`print_test_brief_p0{1,2,3}{,_grey}.png`).
- PPTX → LibreOffice → PDF → Letter imposition: works; fonts embedded (Segoe UI Regular, Semibold,
  Light); smallest printed text 10.1 pt. Greyscale: subject bars dark grey vs context light grey,
  lines distinguishable with labels.
- HTML → Edge → PDF: works; `@page` margin boxes print the footer and "n / N"; Light/Semilight/
  Semibold all resolve; inline matplotlib SVG keeps Segoe UI text; sequential ramp prints in order.
- Lessons carried into the build: (1) KPI labels must fit one line or the tile grows (the test tile
  collided with the line below); (2) diagram labels must be measured and ≥ 8.5 pt (test boxes
  overflowed at 7.5 pt); (3) keep tokens like EIA‑861 together (non-breaking hyphen or nowrap);
  (4) CSS `content` escapes eat the following space (write separators as " · ").

## 6. Question-sheet layout test (2026-11-01 07:3x): result

`work/qsheet/qsheet_layout_test.py` with `qsheet.css`: 22 Q&As of realistic length (cue answers 45–62
words, STAR four lines of 12–16 words), five questions to ask and a closing line, two columns on US
Letter. **Both 8.5 pt and 9.0 pt fit on two sides**; at 9.0 pt about 40% of side 2's right column is
free. Use 9.0 pt for v1 (more legible) and keep 8.5 pt as the fallback if R5's answers run long.
Proofs: `work/proofs/qsheet_test/`.

## 7. QA built into the build (batch 2)

- `ds.check_layout(fig)` (called by `ds.save`): text-on-text overlaps, text on a scatter marker, text
  outside the figure. Every v0 chart passes.
- Deck builder: every text box is measured with the real Segoe UI files (PIL) before it is written;
  overflowing boxes and stacked columns that pass their limit are listed, then the deck is rendered and
  looked at. Autoshapes have their theme style removed (it added shadows in LibreOffice); rules are thin
  filled rectangles, not connectors.
- Claims checker (`work/claims/build_claims.py`): every number in slide text, notes and the brief must
  be covered by a claims row; every row's exact text must appear verbatim.
