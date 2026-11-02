# The interview-upgrade branch, for your own clone

This folder holds the branch `interview-upgrade-2026-11` of `dominion-reliability-review` as a git bundle. Nothing was pushed
from the machine that made it, and publishing it is optional (step 8).

| File | What |
|---|---|
| `dominion-reliability-review_interview-upgrade.bundle` | git bundle of the whole branch (8.5 MB, SHA-256 `5521017494d3b83a445ee4a7afef2d8269a34333572231d0c56b977043fedbc2`). Tip `c17766a`, 36 commits on top of `ec8ecb6`, which was `main` on GitHub on 1 November 2026 |
| `CHANGES.md` | one line per commit (what and why), grouped by theme, and what to review first |

Not in the bundle: the raw downloads (`data/raw/`, gitignored), the local DuckDB mirror, credentials and local configuration.

The commands are for PowerShell on Windows (Power BI Desktop is Windows-only); the four download scripts run in Git Bash.
Replace `C:\path\to\` with your own paths. Every comparison below names the commit `ec8ecb6`, never your local `main`:
`git fetch` updates `origin/main` but never moves your local `main`, so on an older clone `main` can be behind `ec8ecb6`,
and `main..interview-upgrade-2026-11` would then list more than 36 commits.

## 1. Fetch the branch into your clone

```powershell
# if you have no clone yet: git clone https://github.com/saketh1433/dominion-reliability-review.git
cd C:\path\to\dominion-reliability-review
git status --short                       # should print nothing (see below)
git fetch origin
Get-FileHash C:\path\to\dominion-reliability-review_interview-upgrade.bundle -Algorithm SHA256      # expect 5521017494D3B83A445EE4A7AFEF2D8269A34333572231D0C56B977043FEDBC2
git bundle verify C:\path\to\dominion-reliability-review_interview-upgrade.bundle                  # expect "complete history" and "is okay"
git fetch C:\path\to\dominion-reliability-review_interview-upgrade.bundle interview-upgrade-2026-11:interview-upgrade-2026-11
git log --oneline -1 ec8ecb6              # ec8ecb6 Update NOTICE.md to clarify data sources
git log --oneline ec8ecb6..origin/main    # prints nothing unless GitHub's main has moved since 1 November (then see step 8)
```

If `git status --short` lists files, commit them or set them aside with `git stash push -u` (bring them back later with
`git stash pop`): uncommitted changes can stop `git switch` in steps 2 and 8. The bundle carries the branch's full history,
so it fetches into any clone.

## 2. Review the diff

```powershell
git log --oneline ec8ecb6..interview-upgrade-2026-11           # 36 commits
git diff --stat ec8ecb6...interview-upgrade-2026-11            # 88 files changed, 40414 insertions(+), 293 deletions(-)
git diff ec8ecb6...interview-upgrade-2026-11 -- README.md docs/
git switch interview-upgrade-2026-11
```

`CHANGES.md` lists what to review first.

## 3. Python environment (Python 3.12)

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install -r requirements-sources.txt
```

Tested with Python 3.12 (`requirements-sources.txt` lists the package versions); `py -0` lists the versions you have.
`requirements.txt` alone (duckdb, pandas, numpy) is enough for the three checks at the top of step 5; the repository's
GitHub workflow runs two of them on Python 3.11.

## 4. Re-download the raw sources (optional: about 3 GB, about half an hour)

Only the DuckDB build in step 5, the storm comparison and the export scripts need the raw files. The three checks at the
top of step 5 and the Power BI template (step 6) run from committed files.

On the machine that made the bundle (1 November), the EAGLE-I zips, 1.7 GB of the downloads, took about 14 minutes to
download and 3 minutes to extract. All of `data\raw\` comes to about 3 GB, and step 5's DuckDB file adds 0.9 GB. Allow about
half an hour on a similar connection, longer on a slow one, and 4 GB of free disk.

In Git Bash, from the repository folder (`curl` and `unzip` come with Git for Windows):

```bash
bash scripts/download_noaa.sh
bash scripts/download_eia930.sh
bash scripts/download_eaglei.sh              # about 1.7 GB of zips from DOE's EAGLE-I download page
bash scripts/download_context_sources.sh     # EIA-861 and 861M, Census, HURDAT2, CPC degree days, DOE-417, PJM, SCC
```

Then, in PowerShell:

```powershell
.venv\Scripts\python -I scripts\extract_eaglei_va.py     # Virginia rows, MD5 check against figshare, Parquet
.venv\Scripts\python -I scripts\extract_eia861.py
.venv\Scripts\python -I scripts\extract_census_va.py
.venv\Scripts\python -I scripts\extract_hurdat2.py
.venv\Scripts\python -I scripts\extract_degree_days.py
.venv\Scripts\python -I scripts\extract_doe417.py
.venv\Scripts\python -I scripts\write_manifests.py
```

- Do not run `extract_pudl.py`: it rewrites the committed `data\input\pudl_*.csv` and is only for a PUDL refresh.
- `extract_census_va.py` also rewrites `data\output\va_counties.geojson` and `.topojson`. If `git status` then shows them
  changed, the difference is library formatting: `git restore data/output/va_counties.geojson data/output/va_counties.topojson`.
- Sources move on. EIA-930's current half-year file grows every day, so a new download runs past the hour ending midnight on
  29 October 2026, the cut-off of every committed 2026 demand figure (decision D21); 2019-2025 figures do not change. NOAA
  re-issues files when it revises events. Keep the committed `data\output\` files unless you mean to move the cut-off.

## 5. Rerun the checks

Three checks need no download and take about a second in all:

```powershell
.venv\Scripts\python -I scripts\run_local_duckdb.py            # T1-T6 on the committed EIA inputs; "rolling SAIDI averages = 130.2 and 133.0"
.venv\Scripts\python -I scripts\check_output_metrics.py        # every committed output in data\output\; ends "All committed-output checks passed."
.venv\Scripts\python -I scripts\trend_tests.py                 # 2015-2025 trend tests; SAIFI p 0.54, CAIDI 0.74, SAIDI 0.58, adjusted 0.67
```

After step 4, the full local build (about 25 seconds):

```powershell
.venv\Scripts\python -I scripts\run_local_duckdb_sources.py    # builds data\raw\duckdb\reliability_local.duckdb (0.9 GB) and asserts T7-T31
```

That file is the DuckDB mirror: the same SQL files as the Snowflake build (`sql/01` to `sql/11`), run on your laptop. The
template's data comes from it, not from Snowflake: `scripts\export_powerbi_csv.py` exported 16 of the 18 CSV
files the template imports from the mirror, and `scripts\export_workbook_tables.py` wrote the other 2 from the Excel
workbook. The CSV files are committed, so you do not need to export them again. Neither Power BI nor these checks connect to
Snowflake, and nothing on this branch has been built in your Snowflake account (step 7).

Several of T7-T31 pin facts of the source files (row counts, the last NOAA month, DOE-417 totals). If one fails after a fresh
download, a source file has changed since 1 November; `docs/03_data_quality.md` says what each test guards.

Optional, after `run_local_duckdb_sources.py`: `.venv\Scripts\python -I scripts\storm_vs_calm_ratio.py` prints the storm
comparison, 11.9 (7.9 to 16.9), from the mirror (it is in `data\output\storm_vs_calm.csv`, not on a report page).
`scripts\export_powerbi_csv.py` and `scripts\export_workbook_tables.py` rewrite their files in `data\output\`; with a Windows
checkout the CSV hashes differ from `powerbi_exports_manifest.csv` by line endings only (`data/README.md`).

## 6. Open the Power BI template

Open `powerbi\Dominion_reliability_review.pbit` in Power BI Desktop. It asks for `DataFolder` when it opens: set it to
your clone's `data\output\` folder (the template suggests `C:\path\to\dominion-reliability-review\data\output\`; the path must end with
`\`) and click Load. All 18 tables import from the 18 CSV files there; no other file and no Snowflake connection
is needed. Save the working copy as a `.pbix` (`*.pbix` is gitignored). To point it elsewhere later: Transform data >
Edit parameters > `DataFolder`, then Refresh.

## 7. Snowflake (optional)

A Snowflake account that ran the October build (`sql/01` to `sql/08` as at `ec8ecb6`) holds the EIA-861, NOAA storm and
EIA-930 tables. The new tables (EAGLE-I county outages, outage events and restoration, load and sales, event context) reach
it only through this step; until then they exist in the DuckDB mirror and in the CSV files of step 5. The template does not
need Snowflake and still imports the CSV files afterwards.

To build the new tables in your own account, follow docs/07, "Yearly (EAGLE-I, DOE-417, HURDAT2, degree days: sql/09 to
11)": create the two stages, `PUT` the extracted files uncompressed, then run `sql/09` (after `05`), `sql/10` (after `06`)
and `sql/11` (after `09`). Tests T13-T31 are declared in those files. If your account still holds a `STORM_INDEX` built
before decision D22, re-run that statement in `sql/05` and `SAIDI_WEATHER_ADJUSTED` in `sql/07` first, or T21 fails.

## 8. Publish (optional)

Publishing is optional, and comes only after the Power BI test in step 6 has passed. Not publishing is fine: the adopted
deck's slide 6 shows what was added on 1 November.

**Recommended: one commit of your own on `main`, after review.**

```powershell
git status --short                                # should print nothing (see step 1)
git switch main
git merge --ff-only origin/main
git merge --squash interview-upgrade-2026-11
git commit
git push origin main
```

If `git merge --ff-only` refuses, your local `main` has commits that GitHub's does not: stop there. If `origin/main` has
moved past `ec8ecb6` (the last command in step 1 printed commits), rerun the three checks of step 5 after
`git merge --squash` and before `git commit`. If the squash stops with conflicts, `git reset --merge` puts `main` back as it
was.

`git commit` opens an editor for the message. A template:

```text
Add county outage, storm-context and load-shape analyses (November 2026)

What: six more public sources (EAGLE-I county outages, EIA-861 sales and 861M,
Census counties, HURDAT2, DOE-417, CPC degree days) with download and extract
scripts; sql/09 to 11 (county outages, outage events and restoration, load and
sales, event context) with tests T13-T31; a DuckDB build that runs the SQL and
its tests on a laptop; the storm-vs-calm comparison and the 2015-2025 trend
tests; Bedford city counted once in the storm index (D22: 464 and 791 storm
county-days in 2024 and 2025); a Power BI template that imports 18 CSV files
from data/output; README and docs updated.

How it was made: Prepared on November 1, 2026 with help, using an AI coding
assistant. I reviewed the changes and reran the checks before merging.
```

Edit the first paragraph as you like. Keep the second paragraph, and keep every sentence in it true: delete the last
sentence if you did not both review the changes and rerun the checks.

**Not recommended: pushing the 36 commits as they are**, to any branch or as a pull request. Each one shows author and
committer `.` with the preparing machine's email, which can link it to the preparer's GitHub account; times on 1 November
2026 between 07:47 and 12:51 +05:30; and a `Co-Authored-By: Claude` trailer
(`git log --format="%an <%ae> %ad" ec8ecb6..interview-upgrade-2026-11` lists them). GitHub keeps a pull request's commits visible even
after a squash merge, so a pull request from this branch shows them too.
