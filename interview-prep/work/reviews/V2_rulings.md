# V2 rulings (orchestrator, 2026-11-01 09:15)

Source: `work/reviews/V2_truth_audit.md`, which ran on `snapshot_v1_0855`. B applies every fix below
in v2. D does the repo items. The ruling numbers match V2's findings F1–F17. Pronouns for the candidate:
they/them.

## The ownership framework (F1–F6, F9, F16)

The 1 Nov upgrade is on the local branch `interview-upgrade-2026-11` only: the EAGLE-I county work,
degree days, T13–T31, D22, the new exports and the all-Import report. The candidate's public GitHub
repo doesn't have it. The pack therefore ships in **two variants**, and the candidate chooses on Monday
(START_HERE, step 1):

1. **Adopted (main variant, the default).** The candidate first reviews the branch (a CHANGES list per
   commit), reruns the checks on their own laptop from a git bundle, and publishes it from their own
   GitHub account. The deck, brief and sheet may then present the upgrade as part of the project.
   START_HERE says plainly that this variant is only for an adopted upgrade.
2. **Public-repo-only (fallback).** Only what is on the candidate's public `main` today:
   - S4 = the NOAA scatter (r = 0.70, n = 10), with the public numbers 465 → 796
   - S7 = tests T1–T12
   - A6 = the peer table
   - no EAGLE-I, degree-day, T13+ or D22 material
   - S5 without the degree-day line

   Everything else is identical to v2. B builds it from the same generator with a switch, if that takes
   ≤ 45 min. Otherwise the fallback is v0 plus every wording fix below, rebuilt and proofed.

## Fixes for both variants

**Wording**

| V2 | Fix |
|---|---|
| F7 (Q13) | No discovery story. Use the candidate's own documented decision **D13** (DirectQuery for development, Import for presentation) as the true example. In the adopted variant, describe the folder-parameter Import as how the report works now, never as "I found…". |
| F8 (Q7) | Use the candidate's own catch, **P18** (the group-index denominator, corrected 27 Oct, commit 1635a8e), as the example. Drop "summed ratio columns → measures" as their story. |
| F9 (N7) | Delete "Every chart comes from a script and a saved data snapshot." For reproducibility, cite `scripts/run_local_duckdb.py` and the tests. |
| F10 (Q24, S8, N8) | Replace "I build governed Snowflake → Power BI reporting" with resume-true wording. For example: "I build governed Snowflake pipelines and BI reporting" (Snowflake at Mercury; Tableau dashboards in the job bullets; Power BI in this project). Never Power BI "at work". |
| F11 (S8 strip) | "Root-cause analysis on joined data → what I'd do with cause codes in the first 90 days". It's future and conditional, because the project has no cause codes. |
| F12 (Q11) | Within a year, SAIDI = customer-minutes ÷ customers. The 3-year figure is the mean of the three annual values, as the reported 130 and 133 are (they reconcile). Delete "never an average of ratios". |
| F13 (S7, B p.8) | "Decisions logged (D1–D14); the peer set was chosen by EIA ID before results." Never "14 decisions made before results". |
| F14 (N1) | "I rebuilt the reported reliability numbers from EIA-861." NOAA, EIA-930 and DOE are context, not the rebuild. |
| F15 (S12 title) | "Every number traces to a public source; the tables behind them are tested after each load." |
| F16 (S7, N7, B p.8) | Adopted: "Power BI (Import)" is true once they apply the P4 guide Monday. Public-only: "Power BI (Import for presentation; DirectQuery used in development, D13)". |
| F17 (S7, N7, B p.8) | "A data dictionary for every table and column; measures defined in docs/05." |

**Numbers**

| V2 | Fix |
|---|---|
| F4 | **12 of 12** everywhere, in the adopted variant. In public-only, cite only what the public docs say: 130.2/133.0 vs 130/133. |
| F5 | Adopted: 464 → 791 (the D22 note in the brief's "know every number"). Public-only: 465 → 796. |
| F6 | Adopted: D commits a trend-test script so the p-values exist in the repo; cite that script. Public-only: drop the p-values and keep "no clear trend" in plain words. |

**Logistics:** add `[you: commute or relocation plan for a hybrid 3-2 schedule in Richmond]` to the hybrid answer (R5).

**Voice:** across the 1 Nov material, prefer "the county-day data shows…" to "I went below…". The
candidate owns the analysis by adopting it, not through invented personal moments.

## AI-use honesty (START_HERE only, never in the printed pack)

START_HERE gets a short private note for the candidate. Panels in 2026 often ask whether AI tools were
used, and the answer must be true. Suggested line, for the candidate to adapt: "Yes. I used AI assistants
to help gather public data, write and test SQL and draft materials. I reviewed and reran everything,
and I can walk you through any step." The printed deck, sheet and brief still never mention how they
were made (brief §1).

## Repo items (D, then the orchestrator)

- D: commit `scripts/trend_tests.py` (OLS slope, CI, p for SAIDI, SAIFI and CAIDI ex-MED 2015–2025,
  plus the weather-adjusted slope) and document it in docs/03 or 05. The output must reproduce the
  values the pack prints.
- Orchestrator, at the end: commit B's repo-bound Power BI files (theme, M, measures, docs/06; the
  `.pbit` only if verified to open).
- D, at the very end: a git bundle of the branch plus `CHANGES.md` (one line per commit: what and why)
  into `interview-prep/deliverables/05_repo/`, with the fetch steps for START_HERE. Nothing is pushed
  from this machine.
