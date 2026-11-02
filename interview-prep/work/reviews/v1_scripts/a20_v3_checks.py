"""v3 row checks: note word counts and timings, the measures.dax line cite, the Dominion-only county file,
the 46 kV marker year, the 12-utility medians, origin/main texts, and the one changed row not announced."""
import sys, re, csv, io, subprocess
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd, numpy as np
REPO = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review"
RV = REPO + r"\interview-prep\work\reviews"
def git(path):
    return subprocess.run(["git", "-C", REPO, "show", "origin/main:" + path], capture_output=True, text=True, encoding="utf-8").stdout
# 1 timings from the v3 PPTX notes (whitespace word counts, 130 wpm, per-slide seconds rounded half-up)
for tag in ["deck_adopted", "deck_public"]:
    t = open(RV + rf"\v1_text_v3\{tag}_notes.txt", encoding="utf-8").read()
    parts = re.split(r"===== NOTES (\d+) =====", t)
    wc = [len(parts[i + 1].split()) for i in range(1, len(parts), 2)][:8]
    secs = [int(w * 60 / 130 + 0.5) for w in wc]
    fmt = lambda s: f"{s // 60}:{s % 60:02d}"
    print(f"{tag}: words {wc} = {sum(wc)}; per slide {[fmt(s) for s in secs]}; sum {fmt(sum(secs))}; exact {sum(wc) / 130:.2f} min")
# 2 measures.dax lines 400-402
md = open(REPO + r"\powerbi\measures.dax", encoding="utf-8").read().splitlines()
print("measures.dax 399-403:", [l.strip() for l in md[398:403]])
# 3 Dominion-only county file
d = pd.read_csv(REPO + r"\data\output\county_outage_map_dominion_only.csv", dtype=str)
print("dominion_only file rows:", len(d), "| map_flag counts:", d.map_flag.value_counts().to_dict() if "map_flag" in d else list(d.columns))
if "map_flag" in d: print("off map:", d[d.map_flag != "ok"][["county_fips", "county_label", "map_flag"]].values.tolist())
# 4 highest distribution voltage, 19876 VA, by year (the '2020: 46 kV lines added' marker)
p = pd.read_csv(REPO + r"\data\input\pudl_reliability_2013_2024.csv", low_memory=False)
v = p[(p.utility_id_eia == 19876) & (p.state == "VA") & (p.standard == "other_standard")]
print("highest_distribution_voltage_kv by year:", dict(zip(v.report_date.str[:4], v.highest_distribution_voltage_kv)), "| 2025 file: 46.0")
for nm, txt in [("origin/main docs/03", git("docs/03_data_quality.md")), ("origin/main docs/05", git("docs/05_metrics_and_measures.md")), ("local docs/03", open(REPO + r"\docs\03_data_quality.md", encoding="utf-8").read())]:
    hits = [f"{i + 1}: {l.strip()[:220]}" for i, l in enumerate(txt.splitlines()) if re.search(r"46 ?kV", l)]
    print(nm, "46 kV lines:", hits[:3])
# 5 12-utility medians from raw inputs (incl. Dominion) and from the origin/main workbook
d05 = git("docs/05_metrics_and_measures.md").splitlines()
print("origin/main docs/05 line 87:", d05[86].strip() if len(d05) > 86 else None)
d06 = git("docs/06_powerbi_report.md")
print("origin/main docs/06 lines with 6%:", [l.strip()[:200] for l in d06.splitlines() if "6%" in l or "up 6" in l][:3])
blob = subprocess.run(["git", "-C", REPO, "show", "origin/main:powerbi/Dominion_Reliability_PowerBI_Data.xlsx"], capture_output=True).stdout
pe = pd.read_excel(io.BytesIO(blob), sheet_name="Peers")
pe = pe[pe.utility != "Appalachian Power (VA)"]
print("origin/main workbook, 12 utilities: median saifi_5yr %.4f, median caidi_5yr %.2f, n=%d" % (pe.saifi_5yr.median(), pe.caidi_5yr.median(), len(pe)))
print("origin/main workbook standards:", dict(zip(pe.utility, pe.standard)))
tr = pd.read_excel(io.BytesIO(blob), sheet_name="Trend")
print("origin/main workbook Trend SAIFI 2019, 2023, 2025:", tr.set_index("year").loc[[2019, 2023, 2025], "saifi_ex_med"].tolist())
own = {"5416": (1.253, 139.25), "7140": (1.243, 114.17), "3046": (1.228, 113.86), "19876": (1.211, 110.44), "17539": (1.140, 72.05), "6455": (0.994, 87.16),
       "195": (0.934, 125.33), "14940": (0.742, 98.63), "1167": (0.710, 99.47), "14715": (0.689, 136.66), "15270": (0.569, 90.06), "6452": (0.488, 96.04)}
print("own (a11) 12-utility medians: SAIFI %.4f CAIDI %.3f" % (np.median([v[0] for v in own.values()]), np.median([v[1] for v in own.values()])))
# 6 the changed row that was not announced
old = {r["id"]: r for r in csv.DictReader(open(RV + r"\snapshot_v2_1035\claims.csv", encoding="utf-8"))}
new = {r["id"]: r for r in csv.DictReader(open(RV + r"\snapshot_v3_audit\claims.csv", encoding="utf-8"))}
ann = set("C-S3-01 C-S3-02 C-S4-08 C-S4-09 C-S5-04 C-S5-07 C-S6-02 C-S7-10 C-S8-01 C-Q-03 C-Q-06 C-Q-08 C-Q-10 C-S3-02P C-S3-04P C-S3-07 C-S3-09 C-S4-05P C-S4-20 C-S5-11 C-S5-12 C-S7-05A C-S6-06 C-B-03 C-B-01".split())
for i in new:
    if i in old and i not in ann:
        ch = [f for f in new[i] if new[i][f] != old[i][f]]
        if ch:
            print("unannounced change:", i, ch); [print(f"   - {f}: {old[i][f]}\n   + {f}: {new[i][f]}") for f in ch]
