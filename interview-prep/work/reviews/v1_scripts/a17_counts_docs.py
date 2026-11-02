"""Row counts, coverage dates, tests, reconciliation, docs text and the Power BI template (read-only)."""
import sys, os, gzip, json, zipfile, re, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd, duckdb
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
con = duckdb.connect(REPO + r"\data\raw\duckdb\reliability_local.duckdb", read_only=True)
def git(path):
    return subprocess.run(["git", "-C", REPO, "show", "origin/main:" + path], capture_output=True, text=True, encoding="utf-8").stdout
# NOAA raw files
tot = 0
for f in sorted(glob.glob(REPO + r"\data\raw\noaa\StormEvents_details*.csv.gz")):
    with gzip.open(f, "rt", encoding="utf-8", errors="replace") as fh:
        n = sum(1 for _ in fh) - 1
    tot += n
print("NOAA detail files rows (excl headers):", tot, "| files:", len(glob.glob(REPO + r"\data\raw\noaa\StormEvents_details*.csv.gz")))
print("PUDL reliability rows:", len(pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)))
r25 = pd.read_csv(REPO + r"\data\input\Reliability_2025_States.csv", header=None, skiprows=3, dtype=str)
print("EIA-861 2025 rows:", len(r25), "| with a utility number:", int(r25[1].notna().sum()))
print("Service territory reference rows:", len(pd.read_csv(REPO + r"\data\reference\Service_Territory_2025_Counties_States.csv", dtype=str)))
for q in ["select count(*), min(obs_date), max(obs_date) from raw.HURDAT2_POINTS",
          "select count(*), min(year), max(year) from raw.DOE417_EVENTS",
          "select count(*), min(obs_date), max(obs_date), count(distinct region) from raw.CPC_DEGREE_DAYS",
          "select count(*) from raw.EAGLEI_OUTAGES_VA", "select count(*) from raw.EIA930_SUBREGION",
          "select count(*) from raw.EIA861_SERVICE_TERRITORY_2025", "select count(*) from raw.PUDL_RELIABILITY", "select count(*) from raw.EIA861_RELIABILITY_2025",
          "select count(*) from raw.NOAA_STORM_EVENTS"]:
    print(q.split("from")[1].strip(), "->", con.execute(q).fetchone())
# tests and reconciliation
t = pd.read_csv(REPO + r"\data\output\test_results.csv")
print("\ntests:", len(t), t.status.value_counts().to_dict(), "| T13-T31 n =", int(t.test_no.between(13, 31).sum()), "| T1-T12 files:", t[t.test_no <= 12].sql_file.value_counts().to_dict())
print(t[t.test_no <= 12][["test", "sql_file", "description"]].to_string()[:1800])
rc = pd.read_csv(REPO + r"\data\output\reconciliation.csv")
print("reconciliation rows:", len(rc), rc.verdict.value_counts().to_dict())
# docs: local and origin/main
for path in ["docs/01_sources.md"]:
    loc = open(os.path.join(REPO, path), encoding="utf-8").read(); pub = git(path)
    for pat in ["831,288", "24,358", "977", "11,803", "11,608,442", "6,094,320", "6,077,232", "55,524", "3,702", "309,504"]:
        print(f"{path} {pat:>11}: local {pat in loc} | origin/main {pat in pub}")
    for line in pub.splitlines():
        if "6,077,232" in line or "EIA-930" in line and "rows" in line:
            print("  origin/main:", line[:300])
d03 = open(os.path.join(REPO, "docs/03_data_quality.md"), encoding="utf-8").read()
print("\ndocs/03 T2 line:", [l[:200] for l in d03.splitlines() if l.startswith("| T2 ")])
print("docs/03 T1-T12 rows:", [l.split("|")[1:3] for l in d03.splitlines() if re.match(r"\| T([1-9]|1[0-2]) \|", l)])
d04 = open(os.path.join(REPO, "docs/04_decisions.md"), encoding="utf-8").read()
i = d04.find("### D10"); print("\nlocal D10:", d04[i:i + 700].replace("\n", " "))
i = d04.find("### D6."); print("\nlocal D6:", d04[i:i + 500].replace("\n", " "))
# measures
md = open(os.path.join(REPO, "powerbi", "measures.dax"), encoding="utf-8").read()
print("\nlocal measures.dax has SELECTEDVALUE('Dashboard Year'[Year], 2025):", "SELECTEDVALUE('Dashboard Year'[Year], 2025)" in md)
pm = git("powerbi/measures.dax")
print("origin/main measures.dax has FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025}:", "FCT_RELIABILITY[YEAR] IN {2023, 2024, 2025}" in pm)
for nm, txt in [("local", md), ("origin", pm)]:
    for m in re.finditer(r"(?m)^(Selected SAIDI|SAIDI 3yr ending 2025)\s*=", txt):
        print(nm, "measure:", txt[m.start():m.start() + 260].replace("\n", " | "))
# pbit
z = zipfile.ZipFile(os.path.join(REPO, "powerbi", "Dominion_reliability_review.pbit"))
print("\npbit members:", z.namelist())
sch = json.loads(z.read("DataModelSchema").decode("utf-16-le").lstrip("\ufeff"))
tabs = sch["model"]["tables"]
names = [tb["name"] for tb in tabs]
print("tables in model:", len(names), names)
print("expressions/parameters:", [e.get("name") for e in sch["model"].get("expressions", [])])
lay = json.loads(z.read("Report/Layout").decode("utf-16-le").lstrip("\ufeff"))
print("pages:", len(lay["sections"]), [s.get("displayName") for s in lay["sections"]])
