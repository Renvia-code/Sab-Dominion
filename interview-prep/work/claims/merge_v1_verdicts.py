"""Write interview-prep/claims.csv: the v3 register (claims_v3.csv, from build_claims_v3.py) with the independent
verdicts merged in, so that checked_by is the reviewer who did not produce the number (MASTER_PROMPT spec).

- checked_by = V1 for every row V1 audited: its verdict and note from work/reviews/V1_delta_v3.csv where present,
  else from work/reviews/V1_number_audit.csv (the v2 audit).
- Rows V1 never saw, or whose source V1 could not open, are the orchestrator's (ORCH below: checked; others pending).
- The producer's own check (the builder's checked_by and result) moves to a new last column, producer_check.

Pipeline: build_claims_v3.py -> claims_v3.csv -> this script -> claims.csv. Rerun both after any claims change.
Usage: .venv\\Scripts\\python.exe -I interview-prep\\work\\claims\\merge_v1_verdicts.py
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
IP = Path(__file__).resolve().parents[2]
SRC = IP / "claims_final.csv"     # was claims_v3.csv; the final register (build_claims_final.py), per B's report
OUT = IP / "claims.csv"
DELTA = IP / "work" / "reviews" / "V1_delta_v3.csv"
AUDIT = IP / "work" / "reviews" / "V1_number_audit.csv"

# Checked by the orchestrator (orchestrator message, Nov 1): V1 could not open the 8-Ks (HTTP 403)
ORCH = {
    "C-Q-10": "MATCH (orchestrator, Nov 1): R-106, WWBT / 12 On Your Side, September 3, 2026, fetched with HTTP 200; "
              "it quotes Dominion: shareholders of Dominion Energy and NextEra Energy have approved the proposed "
              "merger. The 8-Ks (R-104, R-105) are secondary; their vote counts are not printed in the pack",
    "C-S5-14P": "MATCH (orchestrator, Nov 1): origin/main docs/06:37 prints '+6%'; the workbook Trend sheet has SAIFI "
                "1.244, 1.165 and 1.32; 1.32 / 1.244 = +6.1%",
    # Final build (O-34..O-40), checked by the orchestrator on Nov 1, 13:15-14:05, against the repo at c17766a
    "C-B-01": "MATCH (orchestrator, Nov 1, after the last batch): python-pptx whitespace word counts of S1-S8 notes at "
              "130 wpm, rounded per slide: adopted 28/73/48/67/65/77/60/59 s = 7:57; public 25/73/44/66/62/56/60/57 s "
              "= 7:23",
    "C-F-26": "MATCH (orchestrator, Nov 1): R-050 (WTVR, Oct 19) quotes the staff testimony, 'Staff concludes that the "
              "Merger as proposed in the Joint Petition should be denied by the Commission', with conditions under which "
              "it would not oppose; web-search results (VPM, Oct 19: 'SCC staff recommend axing Dominion-NextEra Energy "
              "merger as proposed'; 'unless both companies first commit to dozens of binding conditions') agree; the "
              "search pages were not opened",
    "C-F-27": "MATCH (orchestrator, Nov 1): recomputed from data/output/fct_reliability.csv: ex-MED SAIFI 2021-25 "
              "Appalachian Power (733|VA) 1.602 vs Dominion 1.211; ex-MED SAIDI 2023-25 342.2 vs 133.0",
    "C-F-28": "MATCH (orchestrator, Nov 1): scripts/run_local_duckdb_sources.py at c17766a: 'def translate' on line 46, "
              "its 'return sql' on line 79; it strips CREATE DATABASE/SCHEMA, USE WAREHOUSE/ROLE, FILE FORMAT, STAGE, "
              "COPY INTO, LIST, PUT, ALTER WAREHOUSE and the COPY GRANTS clause, and maps date-parsing formats",
    "C-F-05": "MATCH (orchestrator, Nov 1): recomputed from data/output (fct_reliability + dim_utility, the 12 = 4 "
              "Mid-Atlantic + 5 Southeast + 2 Florida + Dominion): FPL SAIFI-all 2021-25 0.766 vs Dominion 1.531; FPL "
              "ex-MED SAIFI 0.488, lowest of the 12",
    "C-F-11": "MATCH (orchestrator, Nov 1): standard column of fct_reliability, 2014-2025: IEEE 1366 every year for 10 "
              "of the 12; Dominion VA and Alabama Power file 'Other' every year 2013-2025",
    "C-F-14": "MATCH (orchestrator, Nov 1): workbook Trend and fct_reliability: SAIDI 149.9 -> 144.4 (-3.7%), SAIFI "
              "1.244 -> 1.320 (+6.1%), CAIDI 149.874/1.244 = 120.48 -> 144.4/1.32 = 109.39 (-9.2%)",
    "C-F-15": "MATCH (orchestrator, Nov 1): .pbit DataModelSchema: 18 tables with M partitions, 2 calculated "
              "(Dashboard Year, _Measures), 2 relationships",
    "C-F-16": "MATCH (orchestrator, Nov 1): run_local_duckdb_sources.py --quiet at c17766a: 'All 25 tests passed' "
              "(T7-T31; T1-T6 in run_local_duckdb.py = 31) in 22.7 s; the .pbit's 18 M queries read 18 CSVs, 2 from "
              "the workbook export (load_growth, programmes_2025) and 16 others; powerbi_exports_manifest.csv present",
    "C-F-17": "MATCH (orchestrator, Nov 1): docs/04_decisions.md:109 (D10): Appalachian Power 'held in a separate "
              "group ... because its SAIDI exceeds 300 minutes'",
    "C-F-18": "MATCH (orchestrator, Nov 1): docs/03_data_quality.md:32 (P20): '46% of August and 45% of October 2025 "
              "county readings are blank'; findings.md:1013",
    "C-F-19": "MATCH (orchestrator, Nov 1): docs/05:125 (tropical when a HURDAT2 track point lies within 400 km of "
              "Richmond); docs/08:170 (Isaias 59 km from Richmond)",
    "C-F-20": "MATCH (orchestrator, Nov 1): fct_reliability max_kv 46.0 from 2020 (34.5 in 2015-19); SAIDI ex-MED "
              "2020 140.989; fit 126.5 and residual +14.5 per C-S4-05 (V1 MATCH); trend_tests.py SAIDI p 0.58",
    "C-F-21": "MATCH (orchestrator, Nov 1): findings.md:1247-1257 proxy MED days 2,15,3,18,5,6,12,14,3,10,15 = 103; "
              "range 2-18 (docs/05:120)",
    "C-F-22": "MATCH (orchestrator, Nov 1): trend_tests.py rerun: n = 11, 9 df; SAIDI +0.64/yr, 95% CI -1.87 to "
              "+3.15, p 0.58",
    "C-F-23": "MATCH (orchestrator, Nov 1): brief A4 text: opener 63 words = 29 s, story 113 words = 52 s at 130 wpm; "
              "the opener follows sheet Q2 (V2-audited) and the resume's own '3 years'",
    "C-F-24": "MATCH (orchestrator, Nov 1): git log: origin/main author dates 2026-10-27 (f4f75df) to 2026-10-31 "
              "(ec8ecb6); branch commits dated 2026-11-01",
    "C-F-25": "MATCH (orchestrator, Nov 1): (136.047 + 123.322 + 131.3) / 3 = 130.22 and (123.322 + 131.3 + 144.4) / 3 "
              "= 133.01 from fct_reliability; ROWS BETWEEN 2 PRECEDING; run_local_duckdb.py prints 130.2 and 133.0",
    # V1's final audit (V1_delta_final.csv): 1 MISMATCH (wording) fixed in the last build; 3 UNVERIFIABLE because the
    # primary sites blocked V1 (Cloudflare 403 / bot check). The orchestrator confirmed them from web-search results that
    # quote the primary filings; those pages were NOT opened by the orchestrator, and the verdicts say so.
    "C-F-03": "MATCH (orchestrator, Nov 1, search evidence, pages not opened): search results quoting Dominion's Q3 8-K "
              "Ex. 99 (sec.gov d-ex99.htm) and Zacks/TradingView, GuruFocus, StockTitan: Q3 2026 operating EPS $1.28 vs "
              "$1.06; 'top half of the 2026 operating earnings guidance range of $3.45 to $3.69'. V1 confirmed $1.28 and "
              "'top half' in the call transcript it opened",
    "C-F-04": "MATCH (orchestrator, Nov 1, search evidence for the case number, pages not opened): VPM's Oct 19 story URL "
              "vpm.org/.../2026-10-19/scc-dominion-nextera-pur-2026-00112 and Clean Virginia's coverage tie PUR-2026-00112 to "
              "the NextEra-Dominion merger; V1 confirmed Nov 2, Nov 17 and Jan 11 on the Q3 call and EC26-131 in the "
              "Oct 21 Federal Register notice it opened",
    "C-F-06": "MATCH (orchestrator, Nov 1, after the wording fix to 'completion expected by end-2027'): V1's evidence, the "
              "Q3 call: 'We continue to expect project completion by the end of 2027'; 2.6 GW, about 85% and $11.65B "
              "matched by V1",
    "C-F-12": "MATCH (orchestrator, Nov 1): V1 matched 65F, 12 states + DC, MAIFI <= 5 min and EAGLE-I 15-minute readings; "
              "'four nuclear plants': V1 opened the annual report (four nuclear stations) and NextEra's release (NRC "
              "approval required); search results show the companies filed with the NRC on July 15 (SEC Form 425)",
}
FINAL = IP / "work" / "reviews" / "V1_delta_final.csv"   # V1's audit of the final build's web-sourced rows
PENDING_BY = "orchestrator (pending)"          # O-34..O-39 ruling E: every new number, until the orchestrator checks it
PENDING = "pending: orchestrator check (a row V1 never saw)"


def load(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def verdict(r, tag):
    v, note = r["verdict"].strip(), (r.get("note") or "").strip()
    return f"{v} ({tag})" + (f": {note}" if note else "")


def main():
    with open(SRC, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    delta, audit = load(DELTA), load(AUDIT)
    final = load(FINAL) if FINAL.exists() else {}
    header = list(rows[0].keys())
    assert "producer_check" not in header, "run on the builder's output, not on a merged file"
    header.append("producer_check")
    source = Counter()
    pending = []
    for d in rows:
        builder_pending = d["checked_by"] == PENDING_BY      # the builder marks new rows and rows whose numbers changed
        d["producer_check"] = f"B: {d['result']}" if builder_pending else f"{d['checked_by']}: {d['result']}"
        if d["id"] in ORCH:                                  # the orchestrator's own checks win over "pending"
            d["checked_by"], d["result"] = "orchestrator", ORCH[d["id"]]
            source["orchestrator (checked)"] += 1
        elif d["id"] in final:                               # V1's audit of the final build's new rows
            d["checked_by"], d["result"] = "V1", verdict(final[d["id"]], "V1 final delta")
            source["V1 final delta"] += 1
        elif builder_pending:
            d["checked_by"], d["result"] = PENDING_BY, PENDING
            pending.append(d["id"])
        elif d["id"] in delta:
            d["checked_by"], d["result"] = "V1", verdict(delta[d["id"]], "V1 v3 delta")
            source["V1 v3 delta"] += 1
        elif d["id"] in audit:
            d["checked_by"], d["result"] = "V1", verdict(audit[d["id"]], "V1 v2 audit")
            source["V1 v2 audit"] += 1
        else:
            d["checked_by"], d["result"] = PENDING_BY, PENDING
            pending.append(d["id"])
        assert d["checked_by"] not in (d["producer"], "B", "D", "R"), d["id"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header)
        w.writeheader()
        w.writerows(rows)
    ids = {d["id"] for d in rows}
    print(f"{OUT.name}: {len(rows)} rows; checked_by from {dict(source)}; pending orchestrator: {pending}")
    print("verdicts:", dict(Counter(d["result"].split(" (")[0] for d in rows)))
    print("not MATCH:", [(d["id"], d["result"][:70]) for d in rows if not d["result"].startswith("MATCH")])
    print("V1 rows not in the v3 register (retired before v3):", sorted((set(delta) | set(audit)) - ids))


if __name__ == "__main__":
    main()
