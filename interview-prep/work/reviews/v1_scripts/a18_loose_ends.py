"""Loose ends: exact trend p-values, co-op SAIFI dilution (P18), speaker-note timings, interview date,
origin/main texts, Power BI page order, chart snapshot CSVs."""
import sys, os, re, json, zipfile, subprocess, glob
sys.stdout.reconfigure(encoding='utf-8')
import numpy as np, pandas as pd
from scipy import stats
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
def git(path):
    return subprocess.run(["git", "-C", REPO, "show", "origin/main:" + path], capture_output=True, text=True, encoding="utf-8").stdout
# 1 exact p-values
p = pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)
d = p[(p.utility_id_eia == 19876) & (p.state == "VA") & (p.standard == "other_standard")].copy(); d["y"] = d.report_date.str[:4].astype(int)
d = d.set_index("y").sort_index()
ser = {"SAIFI": list(d.saifi_wo_major_event_days_customers.loc[2015:2024]) + [1.32],
       "CAIDI": list(d.caidi_wo_major_event_days_minutes.loc[2015:2024]) + [109.394],
       "SAIDI": list(d.saidi_wo_major_event_days_minutes.loc[2015:2024]) + [144.4]}
for k, v in ser.items():
    lr = stats.linregress(range(2015, 2026), v); print(f"{k} trend p = {lr.pvalue:.5f} slope {lr.slope:+.5f}")
# 2 co-op SAIFI 2025 with and without the no-SAIFI co-op in the denominator
du = pd.read_csv(REPO + r"\data\output\dim_utility.csv")
print("peer groups:", du.peer_group.value_counts().head(12).to_dict())
coop_grp = [g for g in du.peer_group.dropna().unique() if "co-op" in g.lower() or "coop" in g.lower() or "cooperative" in g.lower()]
print("co-op groups:", coop_grp)
r = pd.read_csv(REPO + r"\data\input\Reliability_2025_States.csv", header=None, skiprows=3, dtype=str)
def num(x):
    try: return float(str(x).replace(",", ""))
    except ValueError: return np.nan
rows = []
for _, x in r.iterrows():
    uid = num(x[1])
    if np.isnan(uid): continue
    ieee = (num(x[9]), num(x[8]), num(x[14])); oth = (num(x[21]), num(x[20]), num(x[23]))
    saifi, saidi, cust = ieee if not np.isnan(ieee[1]) else oth
    rows.append(dict(uid=int(uid), state=str(x[3]).strip(), saifi=saifi, saidi=saidi, cust=cust))
R25 = pd.DataFrame(rows)
for g in coop_grp:
    mem = du[du.peer_group == g][["utility_id", "state", "utility_name"]]
    m = mem.merge(R25, left_on=["utility_id", "state"], right_on=["uid", "state"], how="left")
    print(m[["utility_name", "state", "saifi", "saidi", "cust"]].to_string())
    has = m[m.saifi.notna() & m.cust.notna()]
    allc = m[m.saidi.notna() & m.cust.notna()]
    print(f"{g}: SAIFI matched denominators {np.average(has.saifi, weights=has.cust):.3f} | diluted (customers of SAIDI filers) {(has.saifi * has.cust).sum() / allc.cust.sum():.3f} | missing-SAIFI customers {allc.cust.sum() - has.cust.sum():,.0f}")
# 3 speaker-note timings
for tag in ["deck_adopted", "deck_public"]:
    t = open(REPO + rf"\interview-prep\work\reviews\v1_text\{tag}_notes.txt", encoding="utf-8").read()
    parts = re.split(r"===== NOTES (\d+) =====", t)
    wc = {int(parts[i]): len(parts[i + 1].split()) for i in range(1, len(parts), 2)}
    s8 = [wc[i] for i in range(1, 9)]
    secs = [round(w / 130 * 60) for w in s8]
    print(f"{tag} words slides 1-8: {s8} total {sum(s8)} -> {sum(s8)/130:.2f} min; per-slide seconds {secs}")
# 4 interview date
mp = open(REPO + r"\interview-prep\MASTER_PROMPT.md", encoding="utf-8").read()
print("MASTER_PROMPT date lines:", [l.strip()[:160] for l in mp.splitlines() if re.search(r"(?i)(nov(ember)?\.? ?3|3 nov|2026-11-03|tuesday)", l)][:4])
# 5 origin/main texts
d02, d03, d05, d08 = git("docs/02_data_dictionary.md"), git("docs/03_data_quality.md"), git("docs/05_metrics_and_measures.md"), git("docs/08_transformations.md")
for nm, txt in [("docs/02", d02), ("docs/05", d05), ("docs/08", d08), ("docs/03", d03)]:
    for pat in [r"r\s*=\s*0\.70", r"0\.70", r"R.?2\s*=?\s*0\.4\d", r"0\.48", r"within 2%", r"79%", r"0\.96", r"\b105\b", r"6,077,232"]:
        hits = [l.strip()[:200] for l in txt.splitlines() if re.search(pat, l)]
        if hits: print(f"origin/main {nm} [{pat}]: {hits[:2]}")
print("origin/main docs/03 T rows:", [l[:140] for l in d03.splitlines() if re.match(r"\| T\d+ \|", l)])
# 6 Power BI page order
z = zipfile.ZipFile(REPO + r"\powerbi\Dominion_reliability_review.pbit")
pj = [n for n in z.namelist() if n.endswith("pages/pages.json")]
if pj:
    order = json.loads(z.read(pj[0]).decode("utf-8-sig")).get("pageOrder", [])
    names = {n.split("/")[3]: json.loads(z.read(n).decode("utf-8-sig")).get("displayName") for n in z.namelist() if n.endswith("/page.json")}
    print("page order:", [names.get(o) for o in order])
# 7 chart snapshots
for f in glob.glob(REPO + r"\interview-prep\work\charts\v1\s5_*.csv"):
    print(os.path.basename(f)); print(pd.read_csv(f).round(1).head(30).to_string()[:1500])
