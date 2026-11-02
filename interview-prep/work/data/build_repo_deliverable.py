"""Build interview-prep/deliverables/05_repo/: a git bundle of interview-upgrade-2026-11 (full history, so it needs
no prerequisite commit), CHANGES.md (one line per commit, grouped by theme) and README.md (steps for the candidate's
own clone). Fails if a commit on the branch has no line in CHANGES, so a rebuild after new commits cannot skip one.
Every count is taken against the fixed base commit BASE (GitHub's main on 1 November 2026), never a moving branch.
Nothing is pushed.
Run: .venv/Scripts/python.exe -I interview-prep/work/data/build_repo_deliverable.py
     add --readme-only to rewrite README.md and CHANGES.md around the existing bundle (verified, tip checked) without
     creating it again."""
import argparse
import hashlib
import io
import json
import re
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "interview-prep" / "deliverables" / "05_repo"
BRANCH = "interview-upgrade-2026-11"
BASE, BASE_FULL = "ec8ecb6", "ec8ecb685c747fa1363e95355daade7cb6d3eed7"  # GitHub's main on 1 November 2026
BUNDLE = OUT / "dominion-reliability-review_interview-upgrade.bundle"
TEMPLATE = "powerbi/Dominion_reliability_review.pbit"
WORKBOOK_CSVS = {"load_growth.csv", "programmes_2025.csv"}  # written by scripts/export_workbook_tables.py


def git(*args):
    return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, check=True).stdout.strip()


def template_queries(rev):
    """The files each imported table of the committed template reads (DataFolder & "<file>"), and DataFolder's default."""
    pbit = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{TEMPLATE}"], capture_output=True, check=True).stdout
    return pbit_queries(pbit)


def pbit_queries(pbit_bytes):
    model = json.loads(zipfile.ZipFile(io.BytesIO(pbit_bytes)).read("DataModelSchema").decode("utf-16-le"))["model"]
    joined = lambda e: "\n".join(e) if isinstance(e, list) else (e or "")  # noqa: E731
    queries = {}
    for t in model["tables"]:
        for p in t.get("partitions", []):
            if p.get("source", {}).get("type") == "m":
                queries[t["name"]] = re.findall(r'DataFolder\s*&\s*"([^"]+)"', joined(p["source"].get("expression")))
    default = next((re.search(r'"([^"]*)"', joined(e["expression"])).group(1) for e in model.get("expressions", [])
                    if e["name"] == "DataFolder"), None)
    return queries, default


# (theme, short hash, what, why). Themes in display order; commits in time order within a theme.
LINES = [
    ("Sources", "124d01f", "Download and extract scripts for EAGLE-I, EIA-861 and 861M, Census, HURDAT2, CPC degree days, DOE-417, "
     "the PJM 2026 forecast tables and the SCC reports; files land in `data/raw/<source>/` with a MANIFEST.csv",
     "the county outage, storm-context and load-shape work needs public sources beyond the original three, fetched the same way every time and checked (EAGLE-I MD5s against figshare)"),
    ("Sources", "1b01faf", "HURDAT2 and degree-day extract scripts",
     "turn the downloaded text files into loadable CSVs without changing the originals"),
    ("Sources", "0a79adc", "`requirements.txt` names numpy; new `requirements-sources.txt` lists the extract scripts' packages",
     "a fresh environment can run every script; the checks and CI keep the short list"),
    ("Models (SQL)", "ce71834", "`sql/09`: EAGLE-I county outages, `DIM_COUNTY`, county-hour, county-day and territory-day facts, outage events, restoration curves",
     "county-level outage counts to set beside storm exposure, with Dominion counties defined by a stated rule (D15) and failed readings kept NULL (D16)"),
    ("Models (SQL)", "cfd14a0", "`sql/09`: restoration times that ignore one-reading drops, the peak held for an hour, `FCT_COUNTY_YEAR`",
     "a single collection drop ended restorations early and 45-minute spikes led the event ranking"),
    ("Models (SQL)", "656e15a", "`sql/10`: load by hour, month and year, seasonal peaks, degree days, retail sales by class",
     "the load-growth story needs hour-of-day, season, weather and customer-class views"),
    ("Models (SQL)", "606ac00", "`sql/11`: storm type, tropical cyclones and DOE-417 reports for each outage event (D19)",
     "context for the large events; DOE-417 has no utility column, so the match follows a written rule"),
    ("Analysis outputs", "7347e74", "`scripts/storm_vs_calm_ratio.py`: storm against calm county-days, 95% interval from resampling whole days",
     "the county-day comparison (11.9 times, 7.9 to 16.9) is the main new statistic and has to be reproducible from one command"),
    ("Analysis outputs", "c0b2ea2", "`data/output/storm_vs_calm.csv`: both levels with intervals, non-major days, Dominion-only counties, each year",
     "a reader compares the two levels, not only the ratio, and every quoted number comes from one asserted table"),
    ("Analysis outputs", "7133aba", "`peer_reliability_5yr.csv` adds the medians of the 11 peers without Dominion; D10 says the twelve include Dominion",
     "a reference median should not contain the utility being compared with it; ranks and quadrant are unchanged"),
    ("Analysis outputs", "4fc9939", "`data/output/county_outage_map_dominion_only.csv`: the 33 counties Dominion serves alone",
     "EAGLE-I counts every utility in a county; the Dominion-only counties are the clean check (159 minutes against 211 in shared counties, a comparison of places)"),
    ("Tests and checks", "bd9505f", "`scripts/run_local_duckdb_sources.py`: runs `sql/05`-`07` and `09` on in DuckDB and asserts each declared test",
     "the build and its tests run on a laptop without Snowflake"),
    ("Tests and checks", "cd71bae", "Runner: loaders for HURDAT2, DOE-417 and degree days; four more Snowflake-to-DuckDB translations",
     "`sql/10` and `sql/11` need them locally"),
    ("Tests and checks", "94dc884", "`sql/09`: T17 and T19 comments corrected (33 Dominion-only counties; 8 + 14 county-days)",
     "the comments stated counts from before the Bedford fold; tests and expected results unchanged"),
    ("Tests and checks", "94eb5e2", "`scripts/trend_tests.py`: 2015-2025 trend tests for SAIDI, SAIFI, CAIDI and weather-adjusted SAIDI, asserted in `check_output_metrics.py`",
     "say whether the long-run trends can be told apart from zero (none can: p 0.54 to 0.74)"),
    ("Tests and checks", "c49aeb1", "`scripts/run_local_duckdb.py`: the closing message points at `run_local_duckdb_sources.py` for T7-T31",
     "it said the NOAA and EIA-930 checks need the full Snowflake pipeline, but they run in DuckDB; message only, results unchanged"),
    ("D22 (Bedford city)", "06631ad", "`STORM_INDEX` counts Bedford city as Bedford County; re-exported storm files; README and docs",
     "NOAA zone 34 mapped to both codes, so 38 county-days were counted twice over 2013-2025 (2024 and 2025: 464 and 791, were 465 and 796); r 0.70 and the 145.3 prediction are unchanged"),
    ("Exports and Power BI", "c9c79c4", "`scripts/export_powerbi_csv.py`: mart tables to `data/output/` with a manifest (rows, bytes, SHA-256)",
     "the report imports from a folder instead of a live Snowflake connection (D13)"),
    ("Exports and Power BI", "7ae08d1", "`data/output/va_counties.topojson` for the shape map",
     "Power BI's shape map needs shared county borders keyed by `county_fips`"),
    ("Exports and Power BI", "ac4d9a2", "Exports for the county, event and load tables",
     "the new report pages import them; rounding keeps the files identical from one build to the next"),
    ("Exports and Power BI", "f444a31", "`test_results.csv` (T1-T31), `reconciliation.csv` (12 published figures), `storm_county_year.csv`",
     "the Data notes page shows that every test passes and every rebuilt figure matches its publisher"),
    ("Exports and Power BI", "859b52d", "Power BI template `powerbi/Dominion_reliability_review.pbit` with a `DataFolder` parameter, Power Query files, theme and documented measures",
     "the report opens offline from the committed CSV files"),
    ("Exports and Power BI", "a810494", "`scripts/export_workbook_tables.py`: the workbook's LoadGrowth and Programmes2025 tables as `load_growth.csv` and `programmes_2025.csv`",
     "every table the template imports can come from `data/output/`; each index is checked against its Excel formula before it is written"),
    ("Exports and Power BI", "7867129", "Template: LoadGrowth and Programmes2025 import the two new CSV files, `DataFolder` defaults to the clone's `data\\output\\`; CAIDI labelled minutes per interruption; docs/06",
     "the template needs only the `data/output/` folder, and the CAIDI label states its unit"),
    ("Docs", "cf2446e", "docs 01-04: sources S12-S20, new tables, data-quality notes P20-P34, decisions D15-D21",
     "every new source, anomaly and modelling choice is written down where a reviewer looks for it"),
    ("Docs", "0506bbe", "docs 05 and 08: EAGLE-I, event and load measures; worked examples 6 (Chesterfield) and 7 (Isaias)",
     "each new figure can be traced from source rows to the result"),
    ("Docs", "80095c4", "docs/07: refresh steps for `sql/09`-`11` and the first Snowflake run",
     "the yearly refresh can be repeated by someone else"),
    ("Docs", "ecb9e73", "docs 01 and 02: EIA-930 coverage as downloaded (values to the hour ending midnight 29 Oct 2026)",
     "one stated cut-off for every 2026 demand figure (D21)"),
    ("Docs", "69cc362", "README \"What's new (November 2026)\", docs/README, test numbering in docs/00",
     "the front door lists the additions, each worded as an association and tied to its table or script"),
    ("Docs", "d1bdff2", "docs/05 and README: 6,108 storm county-days reconciled with the storm index's 6,530",
     "two counts of storm days appear in the docs; both are now labelled (6,530 - 114 off the map - 308 failed readings = 6,108)"),
    ("Docs", "29b179f", "docs/06: ten of the twelve file under IEEE 1366, not \"half\"",
     "the old headline did not match the data (only Dominion and Alabama Power file \"Other\")"),
    ("Docs", "b0db94d", "docs/05: quadrant lines are the 11-peer medians; the `Method` measure covers 2014-2025",
     "matches the template"),
    ("Docs", "e0b3712", "README: the Power BI report is in the repository as a template",
     "the README still said no report file was included"),
    ("Docs", "2cbd7a8", "README: the template's `DataFolder` is `data/output/`",
     "since 7867129 the template no longer reads the workbook"),
    ("Docs", "506e969", "docs 07, 04 and 03: the 1 November Snowflake run of `sql/09`-`11` was a test in a separate trial account; "
     "the October report reads Snowflake, the template imports the CSV files; the yearly refresh exports them again first",
     "the docs must not suggest that the project's own Snowflake account holds the November tables, or that the template reads Snowflake"),
    ("Docs", "c17766a", "Comments: the `sql/09` header counts (three staging views, eight mart tables, T31) and the EAGLE-I sizes in "
     "`download_eaglei.sh` (11.6 GB of CSV, 1.66 GB zipped)",
     "the comments had the wrong counts and sizes; no code changes"),
]
REVIEW_FIRST = [
    "**README.md**, \"What's new (November 2026)\" and \"How to check the work\" (69cc362, d1bdff2, e0b3712): what a reader sees first.",
    "**D22** (06631ad): the only change to numbers published before, the storm county-days (464 and 791).",
    "**The storm comparison**: `scripts/storm_vs_calm_ratio.py`, `data/output/storm_vs_calm.csv` (7347e74, c0b2ea2), "
    "docs/05 \"Outages from EAGLE-I\" and decisions D15-D20 in docs/04.",
    "**`sql/09_eaglei_outages.sql`** (ce71834, cfd14a0): the model behind every county figure.",
    "**`data/output/reconciliation.csv` and `test_results.csv`** (f444a31): 12 of 12 published figures match; T1-T31 pass.",
    "**The peer comparison** (7133aba, 29b179f, b0db94d): Dominion and 11 peers; medians without Dominion; reporting methods.",
    "**The Power BI template** (859b52d) with docs/06.",
]


def check_existing_bundle():
    """--readme-only: the bundle on disk must verify, carry full history and point at the branch tip."""
    assert BUNDLE.exists(), f"no bundle at {BUNDLE}; run without --readme-only"
    verify = subprocess.run(["git", "-C", str(ROOT), "bundle", "verify", str(BUNDLE)], capture_output=True, text=True)
    assert verify.returncode == 0 and "complete history" in verify.stdout + verify.stderr, verify.stdout + verify.stderr
    heads = dict(reversed(line.split(" ", 1)) for line in git("bundle", "list-heads", str(BUNDLE)).splitlines())
    tip_full = git("rev-parse", BRANCH)
    assert heads.get(f"refs/heads/{BRANCH}") == tip_full, f"bundle head {heads} is not the branch tip {tip_full}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--readme-only", action="store_true",
                    help="keep the existing bundle (checked) and rewrite only README.md and CHANGES.md")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    assert git("rev-parse", BASE) == BASE_FULL, "the base commit is missing or ambiguous: run git fetch origin"
    subprocess.run(["git", "-C", str(ROOT), "merge-base", "--is-ancestor", BASE, BRANCH], check=True)
    commits = [line.split(" ", 1) for line in git("log", "--reverse", "--format=%h %s", f"{BASE}..{BRANCH}").splitlines()]
    full = {h: git("rev-parse", h) for h, _ in commits}
    mapped = {h for _, h, _, _ in LINES}
    missing = [f"{h} {s}" for h, s in commits if not any(full[h].startswith(m) for m in mapped)]
    extra = [m for m in mapped if not any(f.startswith(m) for f in full.values())]
    assert not missing and not extra, f"CHANGES lines out of step with the branch: missing {missing}, extra {extra}"
    tip, base = git("rev-parse", "--short", BRANCH), BASE
    base_subject = git("log", "-1", "--format=%s", BASE)
    moved = git("log", "--oneline", f"{BASE}..origin/main")
    # What the template at the tip reads: every file named in its queries must exist in data/output/ at the tip.
    queries, default_folder = template_queries(BRANCH)
    in_output = set(git("ls-tree", "--name-only", f"{BRANCH}:data/output").splitlines())
    reads_workbook = any(f.endswith(".xlsx") for fs in queries.values() for f in fs)
    csvs = sorted({f for fs in queries.values() for f in fs if f.endswith(".csv")})
    absent = [f for f in csvs if f not in in_output]
    assert not absent, f"the template reads files that are not in data/output/: {absent}"
    n_csv, n_tables = len(csvs), len(queries)
    assert not reads_workbook and all(len(fs) == 1 for fs in queries.values()), queries
    n_workbook = len(WORKBOOK_CSVS & set(csvs))
    assert n_workbook == len(WORKBOOK_CSVS), f"expected the template to read {sorted(WORKBOOK_CSVS)}"
    n_duckdb = n_csv - n_workbook
    pbi_section = rf"""Open `powerbi\Dominion_reliability_review.pbit` in Power BI Desktop. It asks for `DataFolder` when it opens: set it to
your clone's `data\output\` folder (the template suggests `{default_folder}`; the path must end with
`\`) and click Load. All {n_tables} tables import from the {n_csv} CSV files there; no other file and no Snowflake connection
is needed. Save the working copy as a `.pbix` (`*.pbix` is gitignored). To point it elsewhere later: Transform data >
Edit parameters > `DataFolder`, then Refresh."""
    n = len(commits)
    files = git("diff", "--shortstat", f"{BASE}...{BRANCH}").strip()
    # When the commits were made, as their author and committer dates show them (for step 8)
    stamps = sorted(set(git("log", "--format=%ad%n%cd", "--date=format:%Y-%m-%d %H:%M %z", f"{BASE}..{BRANCH}").splitlines()))
    days, zones = {s[:10] for s in stamps}, {s[-5:] for s in stamps}
    assert days == {"2026-11-01"} and len(zones) == 1, (days, zones)
    zone = next(iter(zones))
    t_first, t_last, tz = stamps[0][11:16], stamps[-1][11:16], f"{zone[:3]}:{zone[3:]}"

    if args.readme_only:
        check_existing_bundle()
    else:
        # the bundle: the whole branch, so it carries its own history (no prerequisite commit)
        git("bundle", "create", str(BUNDLE), BRANCH)
        verify = subprocess.run(["git", "-C", str(ROOT), "bundle", "verify", str(BUNDLE)], capture_output=True, text=True)
        assert verify.returncode == 0 and "complete history" in verify.stdout + verify.stderr, verify.stdout + verify.stderr
    sha = hashlib.sha256(BUNDLE.read_bytes()).hexdigest()
    size_mb = BUNDLE.stat().st_size / 1e6

    themes = []
    for t, *_ in LINES:
        if t not in themes:
            themes.append(t)
    ch = ["# Changes on `interview-upgrade-2026-11`", "",
          f"{n} commits on top of `{base}`, which was `main` on GitHub on 1 November 2026; the tip is `{tip}` "
          f"({files}). One line per commit: the hash, what changed, why. Nothing has been pushed.", "",
          "## What to review first", ""]
    ch += [f"{i}. {line}" for i, line in enumerate(REVIEW_FIRST, 1)] + [""]
    for t in themes:
        ch += [f"## {t}", ""]
        ch += [f"- `{h}` {what}. *Why:* {why}." for th, h, what, why in LINES if th == t] + [""]
    ch += [f"Each commit's full message (`git log {base}..{BRANCH}`) gives the detail and the numbers it checked."]
    (OUT / "CHANGES.md").write_text("\n".join(ch) + "\n", encoding="utf-8")

    rd = rf"""# The interview-upgrade branch, for your own clone

This folder holds the branch `{BRANCH}` of `dominion-reliability-review` as a git bundle. Nothing was pushed
from the machine that made it, and publishing it is optional (step 8).

| File | What |
|---|---|
| `{BUNDLE.name}` | git bundle of the whole branch ({size_mb:.1f} MB, SHA-256 `{sha}`). Tip `{tip}`, {n} commits on top of `{base}`, which was `main` on GitHub on 1 November 2026 |
| `CHANGES.md` | one line per commit (what and why), grouped by theme, and what to review first |

Not in the bundle: the raw downloads (`data/raw/`, gitignored), the local DuckDB mirror, credentials and local configuration.

The commands are for PowerShell on Windows (Power BI Desktop is Windows-only); the four download scripts run in Git Bash.
Replace `C:\path\to\` with your own paths. Every comparison below names the commit `{base}`, never your local `main`:
`git fetch` updates `origin/main` but never moves your local `main`, so on an older clone `main` can be behind `{base}`,
and `main..{BRANCH}` would then list more than {n} commits.

## 1. Fetch the branch into your clone

```powershell
# if you have no clone yet: git clone https://github.com/saketh1433/dominion-reliability-review.git
cd C:\path\to\dominion-reliability-review
git status --short                       # should print nothing (see below)
git fetch origin
Get-FileHash C:\path\to\{BUNDLE.name} -Algorithm SHA256      # expect {sha.upper()}
git bundle verify C:\path\to\{BUNDLE.name}                  # expect "complete history" and "is okay"
git fetch C:\path\to\{BUNDLE.name} {BRANCH}:{BRANCH}
git log --oneline -1 {base}              # {base} {base_subject}
git log --oneline {base}..origin/main    # prints nothing unless GitHub's main has moved since 1 November (then see step 8)
```

If `git status --short` lists files, commit them or set them aside with `git stash push -u` (bring them back later with
`git stash pop`): uncommitted changes can stop `git switch` in steps 2 and 8. The bundle carries the branch's full history,
so it fetches into any clone.

## 2. Review the diff

```powershell
git log --oneline {base}..{BRANCH}           # {n} commits
git diff --stat {base}...{BRANCH}            # {files}
git diff {base}...{BRANCH} -- README.md docs/
git switch {BRANCH}
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
template's data comes from it, not from Snowflake: `scripts\export_powerbi_csv.py` exported {n_duckdb} of the {n_csv} CSV
files the template imports from the mirror, and `scripts\export_workbook_tables.py` wrote the other {n_workbook} from the Excel
workbook. The CSV files are committed, so you do not need to export them again. Neither Power BI nor these checks connect to
Snowflake, and nothing on this branch has been built in your Snowflake account (step 7).

Several of T7-T31 pin facts of the source files (row counts, the last NOAA month, DOE-417 totals). If one fails after a fresh
download, a source file has changed since 1 November; `docs/03_data_quality.md` says what each test guards.

Optional, after `run_local_duckdb_sources.py`: `.venv\Scripts\python -I scripts\storm_vs_calm_ratio.py` prints the storm
comparison, 11.9 (7.9 to 16.9), from the mirror (it is in `data\output\storm_vs_calm.csv`, not on a report page).
`scripts\export_powerbi_csv.py` and `scripts\export_workbook_tables.py` rewrite their files in `data\output\`; with a Windows
checkout the CSV hashes differ from `powerbi_exports_manifest.csv` by line endings only (`data/README.md`).

## 6. Open the Power BI template

{pbi_section}

## 7. Snowflake (optional)

A Snowflake account that ran the October build (`sql/01` to `sql/08` as at `{base}`) holds the EIA-861, NOAA storm and
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
git merge --squash {BRANCH}
git commit
git push origin main
```

If `git merge --ff-only` refuses, your local `main` has commits that GitHub's does not: stop there. If `origin/main` has
moved past `{base}` (the last command in step 1 printed commits), rerun the three checks of step 5 after
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
county-days in 2024 and 2025); a Power BI template that imports {n_csv} CSV files
from data/output; README and docs updated.

How it was made: Prepared on November 1, 2026 with help, using an AI coding
assistant. I reviewed the changes and reran the checks before merging.
```

Edit the first paragraph as you like. Keep the second paragraph, and keep every sentence in it true: delete the last
sentence if you did not both review the changes and rerun the checks.

**Not recommended: pushing the {n} commits as they are**, to any branch or as a pull request. Each one shows author and
committer `.` with the preparing machine's email, which can link it to the preparer's GitHub account; times on 1 November
2026 between {t_first} and {t_last} {tz}; and a `Co-Authored-By: Claude` trailer
(`git log --format="%an <%ae> %ad" {base}..{BRANCH}` lists them). GitHub keeps a pull request's commits visible even
after a squash merge, so a pull request from this branch shows them too.
"""
    (OUT / "README.md").write_text(rd, encoding="utf-8")
    note = f"; origin/main has moved past {base}:\n{moved}" if moved else f"; origin/main is still {base}"
    print(f"bundle {BUNDLE.name} ({'kept, verified' if args.readme_only else 'created'}): {size_mb:.1f} MB, sha256 {sha}, "
          f"tip {tip}, {n} commits; template CSVs {n_duckdb} DuckDB + {n_workbook} workbook; "
          f"CHANGES.md and README.md written{note}")


if __name__ == "__main__":
    main()
