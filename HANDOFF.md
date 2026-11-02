# Hand-off: the Dominion reliability project, the November 1 extension and the interview pack

This repository is your `dominion-reliability-review` (GitHub `main` at `ec8ecb6`, 1 November 2026)
plus everything prepared on November 1–2 for the Dominion interview:

| Part | Where | What |
|---|---|---|
| Your project | the whole history up to `ec8ecb6` | unchanged |
| The extension | 36 commits after `ec8ecb6` (they were branch `interview-upgrade-2026-11`) | EAGLE-I county outages, storm types, outage events, load and sales, the storm-vs-calm comparison, trend tests, D22, 31 tests, a DuckDB build, the Power BI template |
| The interview pack | `interview-prep/` | decks, the 2-page handout, the question sheet, the brief, START_HERE, the ledgers, every chart and build script |
| Raw data | **not in git**: `Sab-Dominion_data_raw.zip` on Drive | 339 MB zip, 129 files, 1.35 GB unzipped |

The commits after `ec8ecb6` were made on the preparer's machine with an AI coding assistant; each
carries a `Co-Authored-By: Claude` trailer. You did not write them. Review before you present them
as yours (`interview-prep/deliverables/START_HERE.md`, section 2).

## 1. Set up (Windows, PowerShell, Python 3.12)

Clone into a **new** folder; leave your old copy alone.

```powershell
cd C:\path\to\a\new\folder
git clone https://github.com/Renvia-code/Sab-Dominion.git
cd Sab-Dominion
```

Download `Sab-Dominion_data_raw.zip` from the Drive link, then, from the repository folder:

```powershell
Get-FileHash C:\path\to\Sab-Dominion_data_raw.zip -Algorithm SHA256
#   expect 196E1E92AF5C1CAAD6ADC60F9B8C90FD7E3C679482FCD39F22E7324122D0B9EC
tar -xf C:\path\to\Sab-Dominion_data_raw.zip      # creates data\raw\... (paths in the zip start with data/raw/)
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-sources.txt
```

The zip leaves out three things the build doesn't read or rebuilds itself: `data/raw/duckdb/`
(built in step 2), `data/raw/eaglei/downloads/` (the 14 national EAGLE-I zips, 1.6 GB; `eaglei/va/`
and the parquet were extracted from them and MD5-checked against figshare) and `data/raw/_downloads/`
(the original copy of `noaa/`). `bash scripts/download_eaglei.sh` fetches the national zips if you
ever need them. `data/raw/README.md` describes every folder, and each folder's `MANIFEST.csv` gives
row counts and SHA-256 per file.

## 2. Rebuild and check

```powershell
.venv\Scripts\python -I scripts\run_local_duckdb.py            # T1-T6; "rolling SAIDI averages = 130.2 and 133.0"
.venv\Scripts\python -I scripts\check_output_metrics.py        # ends "All committed-output checks passed."
.venv\Scripts\python -I scripts\trend_tests.py                 # SAIFI p 0.54, CAIDI 0.74, SAIDI 0.58, weather-adjusted 0.67
.venv\Scripts\python -I scripts\run_local_duckdb_sources.py    # full build from data\raw (about 25 s), asserts T7-T31
.venv\Scripts\python -I scripts\storm_vs_calm_ratio.py         # slide 4: 11.9 (7.9 to 16.9)
```

The full build writes `data\raw\duckdb\reliability_local.duckdb` (0.9 GB): the same SQL as the
Snowflake build (`sql/01` to `sql/11`), run locally. Query it with DuckDB for anything else.

**Power BI:** open `powerbi\Dominion_reliability_review.pbit`. When it asks for `DataFolder`,
**replace** the example path with this clone's `data\output\` folder (ending in `\`) and click Load.
Details: `interview-prep/deliverables/04_powerbi/APPLY_GUIDE.md`.

## 3. Slide 4 ("about 12 times the outage hours"): where each number comes from

Adopted deck, slide 4. Every figure is a row of **`data/output/storm_vs_calm.csv`**, written by
**`scripts/storm_vs_calm_ratio.py`** from the county-day panel that **`sql/09_eaglei_outages.sql`**
builds.

| On the slide | Value | Row and columns of `storm_vs_calm.csv` |
|---|---|---|
| Storm county-days | 6,108 | "All complete county-days, 2015-2025": `storm_county_days` |
| Calm county-days | 373,851 | same row: `calm_county_days` |
| Storm bar, with its 95% interval | 332.8 (225.6 to 453.4) | `storm_ch_per_1k`, `storm_ci_low`, `storm_ci_high` |
| Calm bar, with its 95% interval | 27.9 (23.1 to 33.2) | `calm_ch_per_1k`, `calm_ci_low`, `calm_ci_high` |
| The ratio | 11.9× (7.9 to 16.9) | `ratio`, `ratio_ci_low`, `ratio_ci_high` |
| Holds on non-major days | 9.9× | "Non-major days (proxy major event days removed)" |
| Holds in Dominion-only counties | 19.9× | "Dominion-only counties" (the 31 on the map served only by Dominion) |
| Holds in every year 2015 to 2025 | 5.9× to 27.4× | the eleven year rows |

**Method, in four lines:**
- **The unit** is a county-day: one of Dominion's Virginia counties on one day.
- **"Storm" county-days** have a NOAA Storm Events report of a line-risk type (wind, winter or tropical) in that county that day. **"Calm"** are all the others.
- **Outage customer-hours** are summed from EAGLE-I's 15-minute customers-out counts and put per 1,000 customers. Only days with complete readings count, in 99 of the 103 counties; the four left off the map are decision D20. In 2025, 74% of county-days are complete.
- **The 95% intervals** come from 2,000 resamples of whole days.

**What it is not:**
- **EAGLE-I counts every utility's customers in a county**, co-ops included, not only Dominion's (decision D15). That is why the Dominion-only counties are shown separately.
- **It is an association.** Storm reports partly follow damage, so storm days can't be credited with all the extra hours.

**Read more:**
- `docs/04_decisions.md`: D15 (all utilities), D16 (blank readings), D17 (outage events), D18 (proxy major event days), D20 (counties off the map)
- `docs/08_transformations.md`: worked examples
- `docs/03_data_quality.md`: tests T13 to T31
- `interview-prep/work/data/findings.md`: sections C5-2 and C5-3
- `interview-prep/claims.csv`: rows C-S4-08 to C-S4-10

## 4. Where everything else is

| Looking for | File |
|---|---|
| What to do before the interview | `interview-prep/deliverables/START_HERE.md` |
| The decks (adopted and public) and the 2-page handout | `interview-prep/deliverables/01_deck/` |
| Question sheet; interview brief | `interview-prep/deliverables/02_question_sheet/`, `03_interview_brief/` |
| Project decisions D1 to D22 | `docs/04_decisions.md` |
| Pack decisions O-01 to O-42 and the run log | `interview-prep/MASTER_LEDGER.md` |
| Every number in the pack, with its source and check | `interview-prep/claims.csv` |
| Each commit after `ec8ecb6`, what and why | `interview-prep/deliverables/05_repo/CHANGES.md` |
| The data dictionary and measures | `docs/02_data_dictionary.md`, `docs/05_metrics_and_measures.md`, `powerbi/measures.dax` |

## 5. Putting it on your own GitHub

Don't push these commits to your repository as they are: they carry the preparer's name and email.
If you adopt the work, squash it into one commit of your own, with an honest note on how it was
made. The commands and a message template are in `interview-prep/deliverables/05_repo/README.md`,
step 8. The comparison base there is `ec8ecb6`, which is in this history too.
