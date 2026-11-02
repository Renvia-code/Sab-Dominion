# V1 independent number audit: summary

**Scope.** I audited `snapshot_v2_1035`: claims.csv (122 rows), both decks (PPTX text, alt text, notes and print PDFs), the brief and the question sheet (HTML and PDF).

**Outputs.**

- `V1_number_audit.csv`: one row per claim, in the order repo data, then external sources, then resume.
- `V1_coverage.md`
- Scripts in `v1_scripts/`, working files in `v1_work/`, downloaded sources in `v1_sources/` (each in its own folder; download log in `v1_sources/_download_log.txt`).

I edited, committed and uploaded nothing. The resume was read locally only.

## Verdicts

| Verdict | Count | Rows |
|---|---|---|
| MATCH | 117 | |
| ROUNDING | 2 | C-S4-05P (public A2: three fitted values 0.1 off a refit on the cited CSV; they equal origin/main's workbook), C-S5-07 (customers +8.0% on a consistent basis; claims value 7.9; printed "8%" holds) |
| MISMATCH | 1 | C-S7-05A: "12 on the reliability mart" should be 6. T7–T12 are storm and demand tests. The counts 31, 12 and 19 are right. |
| UNVERIFIABLE | 2 | C-S6-06 (−44%: StockTitan returned 403; marked BLOCKED, not worked around); C-Q-10 (the part "approved by shareholders in September" has no opened source; the other four parts match) |

## How the rows were checked

I recomputed the repo-data rows with my own code from `data/input`, the raw DuckDB tables (opened read-only) and `git show origin/main`:

- **Reliability.** SAIDI, SAIFI and CAIDI, the 3-year means, the VA+NC variant, log splits, trend p-values, peer ranks and medians, and IEEE filing years: all reproduce.
- **Storm index.** My own NOAA recount reproduces every year exactly, both with D22 (718/791, 464, 6,530) and without it (723/796).
- **Weather fit.** Reproduced exactly: r 0.6973, t 2.752, p 0.025, CI 0.121–0.922, PI 122.3–168.2, the full A2 table, and the adjusted trend +0.34 (−1.41 to +2.08).
- **EAGLE-I (adopted).**
  - My own storm flags agree with the producer's on 6,530 of 6,530.
  - My own bootstrap gives 11.9 (7.9–16.9), 9.9 and 19.9.
  - The map gives 55 and 633; the Dominion-only comparison gives 159 vs 211.
  - Customer-hours match the raw 15-minute rows.
  - All ten A6 events, 33.5 h and the 47-event +4.6%/yr (p = 0.074) reproduce, but only with the documented P24 and D17 rules applied.
- **Load, sales and AMI.** All match, including the exploratory 33% (with the stated squared-term spec).
- **Row counts, the template's 18 tables and 11 pages, and the screenshot cards:** all match.

**External sources.** Every opened quote was found verbatim: the annual report (pp. 7, 10, 18–19), the job posting, the Dominion Grid Resiliency page, the NextEra release, the Q3 transcript and WTVR. All 17 citations match Crossref, and the r-values match the OpenAlex abstracts.

**Resume.** All 11 rows match.

## Most serious problems, in order

1. **Public deck vs the public repo (P1, P2).** The public deck prints peer medians 0.93/99.3 and labels Georgia Power and Duke Energy Florida as IEEE 1366 ("10 of the 12"). origin/main itself prints medians 0.96/105 (docs/05), labels both utilities "Mixed" in the workbook, and says "half the peers use a different reporting method" (docs/06). The deck figures are derivable, but they contradict what a panelist would read on GitHub.
2. **Test label (C-S7-05A).** "12 on the reliability mart" is wrong in the adopted deck's S6 badge, S6 notes and A4.
3. **"Minutes to restore".** The adopted S5 card and brief p7 use this label for CAIDI, against the brief's own "CAIDI is a ratio, not restoration speed".
4. **Unverified external figures.** −44% (blocked) and "shareholders approved in September" (no source opened) are printed in the brief and question sheet.
5. **Numbers with no claims row.** "33 Dominion-only" (true), "4–5-year trim cycles" (register R-076, not opened), the screenshot's "+6% / −9% since 2019" (true), and the A4 r-values and three citation years (verified). There are also minor rounded or word forms.
6. **Brief talk times.** They fit the adopted notes only. The public notes run 7:31, and three slides differ by 7–9 s.
7. **Public A2 fitted values.** Three cells come from the origin/main workbook's 1-dp fit, not from the cited CSV (differences of 0.1).

No adopted-only number appears in the public deck.

## v3 delta (follow-up audit, 1 Nov 2026)

**Scope.** I audited only what changed in v3:

- the 5 added and 25 changed claims rows;
- C-S4-04P, whose result field changed without being announced (a non-key field only);
- coverage and consistency on the eight v3 files.

Frozen copies and their hashes are in `snapshot_v3_audit/`. At 11:58 IST the live files still matched them. I checked the public rows against origin/main at `ec8ecb6`.

The output is `V1_delta_v3.csv`. Scripts d10, e10, x11, x12, a20 and w02 are in `v1_scripts/`.

**Verdicts (31 rows).** 30 MATCH and 1 UNVERIFIABLE.

The UNVERIFIABLE row is C-Q-10: "approved by shareholders on September 3" (question-sheet item 19).
- Both SEC 8-K links (R-104, R-105) returned HTTP 403, "Undeclared Automated Tool".
- The row is marked BLOCKED, and I did not work around the block.
- The row's other parts still match.
- Opening the two EDGAR links in a browser would settle it.

**V1 problems now fixed.**

1. **Public deck vs origin/main (P1–P3).**
   - S3 prints "median of the 12 (including Dominion)" 0.96 and 105, and "Methods differ". origin/main's docs/05:87 prints the same 0.96 and 105.
   - A6 labels Georgia Power and Duke Energy Florida "Mixed".
   - The public slides, notes and PDF contain none of "10 of 12", "11-peer", "peer median", 99.3/99.5, "most peers" or "minutes to restore". The only 0.93 is Alabama Power's SAIFI in A6.
   - C-S4-05P now cites the workbook's fitted column, and A2's values equal it.
2. **Test split (C-S7-05A).** "12 (6 reliability, 3 storm, 3 demand)" agrees with test_results.csv.
3. **CAIDI label.** It is now "Minutes per interruption" on the S5 card, in the alt text and on brief p7.
4. **−44% (C-S6-06).** It appears verbatim in Dominion's own 8 June 2026 release.
5. **Numbers that had no claims row (U1–U6).** Each now has a row:
   - C-B-05: 33 Dominion-only counties, 31 on the map.
   - C-B-06.
   - C-B-07: 4–5-year trim cycles, verbatim on Dominion's FAQ.
   - C-S5-14: the adopted S5 screenshot.
   - C-B-03, extended.
   - C-S4-08, which now includes 12.
6. **Talk times.** The brief prints both variants, and my recount agrees: adopted 1,028 words (7:54), public 994 words (7:38).
7. **Register hygiene.** C-S3-02, C-S5-07, C-S4-20 and the used_in gaps are fixed.

**Coverage and consistency on v3.**

- 2,382 numeric tokens; 30 have no claims row. All 30 are one of these:
  - 2.5 (from 2.5β);
  - 24 ("24 hours", "2022–24");
  - the utility id 19876;
  - the brief's axis ticks 0.8, 80 and 40%.
- No adopted-only number appears in the public deck.
- I found no public-deck number that origin/main fails to support.

**Still open (all minor).**

1. **Public S5 screenshot.** The new screenshot prints "up 6% since 2019" and 1.24, 1.17 and 1.32, but no public row covers them; C-S5-14 is adopted-only.
   - origin/main supports these numbers. docs/06:37 says "outage frequency 2019 to 2025 (+6%)", and the workbook's Trend sheet has 1.244, 1.165 and 1.320.
   - A C-S5-14P row would close this.
2. **C-S5-12 line cite.** It cites measures.dax lines 400–402, but the measure is on lines 401–403, both here and at the cited commit 859b52d.
3. **C-S3-09 source.** The row (variant both) cites only D findings.md. Its public use is still supported: the reliability inputs are identical to origin/main's, and the workbook says "Mixed".
4. **Brief p4.** The body and chart still print the adopted "11-peer median 0.93 … 99.5" without a variant tag.
   - The p4 source note gives the public 0.96/105, and p2 points readers to it.
   - Even so, someone presenting the public deck reads different medians on p4 than on the slide.
5. **Powell's −.19 (C-B-03).** It still rests only on the register quote.

Nothing was edited, committed or uploaded. Outside `work/reviews/`, the only files written were temporary copies from `git show` in the session scratchpad.
