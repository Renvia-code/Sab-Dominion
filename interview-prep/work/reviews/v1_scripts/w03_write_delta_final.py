"""Write V1_delta_final.csv: the ten C-F rows of the final pack (same columns as V1_delta_v3.csv).
Sources: v1_sources/ (download log appended by d20_fetch_final.sh); searches: e21, e22, e23; print check: x21;
frozen inputs: snapshot_final_audit/ (hashes in _sha256.txt)."""
import sys, csv
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
RV = r"C:\Users\oni\Desktop\PROJECTS\renvia-technologies\client-apps\dominion-reliability-review\interview-prep\work\reviews"
A = {}
def a(i, v, m, verdict, note=""): A[i] = (v, m, verdict, note)
a("C-F-01",
  "3.6 million electric ('homes and businesses in Virginia, North Carolina, and South Carolina') and 500,000 gas ('customers in South Carolina'): verbatim; 2.7M = EIA-861 Virginia 2,675,735 (C-S7-07, verified in V1)",
  "Cited page (R-042, the Oct 30 Q3 release on the Dominion newsroom) returned HTTP 403, a Cloudflare 'Just a moment... Enable JavaScript and cookies' page (v1_sources/final_dom_q3_2026_release); not worked around. The same company boilerplate is verbatim in the Dominion 2025 Annual Report PDF p.2 (the R-107 q4cdn URL; v1_sources/annual_report_2025), in Dominion's IR release dated 06/08/2026 (v1_sources/dominion_release_20260608) and in the NextEra release of 18 May 2026. Print: brief PDF p.2 (box line 1, Customers line), p.9 (A1); qsheet PDF p.2 item 19 (v1_scripts/e21, e22, x21)",
  "MATCH",
  "Scope is stated wherever a count is printed: brief p.2 '2.68M = Virginia in EIA-861 ... 2.8M = Dominion Energy Virginia incl. NC ... 3.6M = all three states'; A1 the same; qsheet 'about 3.6 million electric customers in Virginia and the Carolinas, about 2.7 million of them in Virginia' (2.7M = 2.68M rounded). The Oct 30 wording itself is R's quote only; the figures are unchanged from March (AR) to June 2026")
a("C-F-02",
  "'approximately 2.8 million residential, commercial, high load (including certain data centers), industrial and governmental customers in Virginia and North Carolina' (AR PDF p.19); 'Average electric distribution customer accounts (thousands) 2,809' for 2025, 2,782 for 2024 (AR PDF p.65)",
  "Dominion 2025 Annual Report PDF, the cited q4cdn URL (v1_sources/annual_report_2025/ar2025.pdf, opened 1 Nov), pp.19 and 65. Print: brief PDF p.2 Customers line and 'If a panelist says 2.8M', p.9 (A1) (x21)",
  "MATCH",
  "Scope clear: 2.8M is Dominion Energy Virginia including North Carolina, and the brief pairs it with the Virginia-only 2.68M every time. R-107's page locators are right")
a("C-F-03",
  "$1.28: verified (CFO on the call: 'Third-quarter operating earnings were $1.28 per share'); top half: verified (CFO: 'we now expect full year results to be in the top half of our original guidance range'); $3.45-$3.69: only in fool.com's own summary above the transcript (secondary), not in management's words; $1.06: in no source I could open",
  "Cited page (R-043, R-044: the Q3 release on the Dominion newsroom) returned HTTP 403, Cloudflare JavaScript challenge; not worked around (no other host, no repost). Q3 call transcript, fool.com, the R-095 URL (v1_sources/fool_q3_2026). Annual Report searched: its only '$1.06' is nuclear property insurance ($1.06 billion), and it gives no 2026 range. Print: brief PDF p.2 'Q3 2026 (Oct 30)' line (e21, e22, e23, x21)",
  "UNVERIFIABLE",
  "UNVERIFIABLE-BLOCKED: the prior-year $1.06 rests only on R's register quote of the blocked release, and the $3.45-$3.69 range has only a secondary source. The wording is hedged properly ('seen in the top half'). One browser look at the release closes it")
a("C-F-04",
  "Rebuttal due Nov 2, hearings from Nov 17, final order by Jan 11 [2027]: verbatim (CEO on the Q3 call: 'rebuttal testimony due November 2. Evidentiary hearings begin on November 17. And the final order is due by January 11th of next year.'). EC26-131: verbatim (Federal Register, 21 Oct 2026, p.2: 'Docket Numbers: EC26-131-000. Applicants: NextEra Energy, Inc., Dominion Energy, Inc.', a response to FERC's 09/23/2026 deficiency letter under Section 203). NRC, NC and SC pending: consistent with the approvals list (NextEra release) and the call ('Required federal approvals have all been filed and continue to progress'; SC hearings Dec 8; NC hearings Feb 23, 2027). PUR-2026-00112: not verified",
  "v1_sources/fool_q3_2026 (R-095); v1_sources/final_govinfo_fr_20261021/fr.pdf (R-093, HTTP 200); v1_sources/nextera_release (R-048). pv magazine (R-096) returned HTTP 403, a Cloudflare 'Sorry, you have been blocked' page; not worked around. No opened source contains the case number (e21 searched every v1_sources file). Print: brief PDF p.2 Merger and Pending lines; qsheet PDF p.2 item 19 'SCC hearings start November 17' (x21)",
  "UNVERIFIABLE",
  "UNVERIFIABLE-BLOCKED: the case number PUR-2026-00112 rests only on R's register quote of a secondary source (R could not open the SCC docket search either). Every date and EC26-131 match. The brief words the deadline two ways: p.2 'order by Jan 11' and Q23 (p.11) 'Virginia's order is due by mid-January 2027'. It is the same deadline; printing 'by January 11, 2027' in both would make them agree. The same box's 'shareholders approved Sep 3' is C-Q-10, still unverified (SEC 403)")
a("C-F-06",
  "Name: 'Coastal Virginia Offshore Wind (CVOW)' (AR PDF p.3). 2.6 GW: 'CVOW, a 2.6 GW generating project' (AR PDF p.4). About 85%: 'the project approximately 85% complete'. $11.65B: 'our current budget remains $11.65 billion including $123 million of unused contingency'. End-2027: 'We continue to expect project completion by the end of 2027', after 'we have utilized a portion of that contingency' (all three from management on the Q3 call)",
  "AR 2025 PDF pp.3-4 (the cited q4cdn URL); Q3 call transcript, fool.com (the R-061 URL). Print: brief PDF p.2 CVOW line (e21, e22, x21)",
  "MISMATCH",
  "Wording only; every number matches. 'done by end-2027' prints the company's expectation as a fact. The source says 'expect project completion by the end of 2027', and the date has already moved once: the AR (February 2026) said 'expected in early 2027'. Suggested print: 'completion expected by end-2027'. The pack prints no 'early 2027', so there is no date conflict inside it")
a("C-F-07",
  "28%: 'Data centers represent 28% and 26% of Virginia Power's electricity sales for the years ended December 31, 2025 and 2024' (AR PDF p.20). 54+ GW: 'over 54 gigawatts of data center capacity in various stages of contracting'. 12+ GW: 'over 12 gigawatts of capacity contracted under electric service agreements'. Growth: 'added over 6 gigawatts of contracts or 13% since the end of last year' (CFO on the Q3 call)",
  "AR 2025 PDF p.20 (R-112); Q3 call transcript (R-054, R-099). Print: brief PDF p.2 Data centers line; qsheet PDF p.2 item 19 (e21, x21)",
  "MATCH",
  "qsheet 'more than a quarter of Dominion Energy Virginia's sales' = 28% of Virginia Power's sales (the AR says Dominion Energy Virginia is made up of Virginia Power's regulated operations). 'the pipeline keeps growing' = +6 GW (13%) since end-2025. Periods are right: 2025 sales, and the pipeline as of the Oct 30 call")
a("C-F-08",
  "+$566M effective January 2026, +$210M effective January 2027, ROE 9.80% (AR PDF p.130: 'In November 2025, the Virginia Commission approved ...'). +$11.24 a month in 2026 'For a typical residential customer', and ROE 'from 9.7% to 9.8%' (Loudoun Now, published 2025-11-25). Up to 50 basis points 'based on factors that may include reliability' (AR PDF pp.28-29; C-Q-07, verified in V1)",
  "AR 2025 PDF p.130 and pp.28-29 (R-057, R-059); Loudoun Now article (R-058, HTTP 200; v1_sources/final_loudounnow_rates). Print: brief PDF p.2 Rates line (e21, x21)",
  "MATCH",
  "$11.24 comes from a local press report of the SCC final order (secondary; the order itself was not opened) and applies to a typical residential customer, so 'typical residential bill' would be exact. 'which the SCC can move' fits the source's 'may, at its discretion'")
a("C-F-09",
  "19: 'The Voltage Island Mitigation program should address 19 locations by the end of the program.' 1%: 'Our goal is to provide a system-wide average of 1% energy savings for our customers.'",
  "Dominion Grid Resiliency page, the R-114/R-038/R-039 URL (v1_sources/dominion_grid_resiliency, HTTP 200, opened 1 Nov). Print: brief PDF p.2 VIM and VO lines; brief PDF p.11 Q19 '(19 sites)' and '(goal: 1% energy savings)' (e21, x21)",
  "MATCH",
  "19 is the program's planned scope ('by the end of the program'), not sites finished. The print does not claim completion, but '19 sites planned' would be exact. The 1% is printed as a goal, as the source has it. Minor: 'so every customer can be restored' drops the source's condition 'in the event of a single transformer failure'")
a("C-F-10",
  "About 2,900 miles: 'Through its Strategic Underground Program, Dominion Energy has buried about 2,900 miles of outage-prone power lines in Virginia, including about 300 miles in the last year' (Dominion IR release dated 06/08/2026). About 4,000 and 2029: 'move approximately 4,000 miles of electric distribution lines underground' and 'is expected to be completed by 2029' (AR PDF p.23). Separate: 'Underground conversions are not within the scope of Grid Resiliency programs' (Grid Resiliency page, V1)",
  "v1_sources/dominion_release_20260608 (the R-013 URL, investors.dominionenergy.com, HTTP 200); AR 2025 PDF p.23 (R-034); v1_sources/dominion_grid_resiliency (R-035). Print: brief PDF p.2 SUP line (e21, x21)",
  "MATCH",
  "Mild wording: 'Due 2029' for the AR's 'expected to be completed by 2029'; 'expected by 2029' would be exact. No date conflict: the end-2025 figure of about 2,700 miles (R's note 6) is printed nowhere in the final pack")
a("C-F-12",
  "65°F and population-weighted: verbatim (CPC: '65°F is the base for both heating and cooling degree day computations'; 'population weighted State, Census Divisional and National data'). VA plus 12 other states plus DC: verbatim (SCC report RD916, 1 Dec 2025, pp.10-11). MAIFI, 5 min or less: IEEE PES Boston slides p.50 ('MAIFI: Momentary Average Interruption Frequency Index- Similar to SAIFI') and p.6 (sustained = 'any interruption that lasts more than five minutes'), and EIA-861 instructions p.9 ('sustained interruption (of over 5 minutes)'). EAGLE-I, 15-minute, ORNL, DOE: Crossref abstract of doi:10.1038/s41597-024-03095-5 ('created at Oak Ridge National Laboratory to map the population experiencing electricity outages every 15 minutes at the county level') and ORNL Constellation ('15-minute intervals'; sponsor DOE CESER). NRC 'four nuclear plants': not verified on the cited notice",
  "v1_sources/final_cpc_degree_days and final_cpc_ddayexp (R-119); final_va_rd916_2025 (R-080); final_ieee_pes_boston_1366 and final_eia861_instructions (R-130, R-074); final_crossref_10_1038_s41597-024-03095-5 and final_ornl_eaglei_2025 (R-129, R-016); all HTTP 200. The NRC notice (R-094, federalregister.gov) served a 'Request Access' page ('Your request has been flagged as potentially automated'; the site directs scripts to its API). I did not use the API. Print: brief PDF p.2 glossary (e21, e22, x21)",
  "UNVERIFIABLE",
  "UNVERIFIABLE-BLOCKED, for '4' only: that the NRC application covers four plants rests on R's register quote. Two opened sources support it indirectly: the AR's glossary names Dominion's four nuclear stations (Millstone, North Anna, Surry, V.C. Summer), and the NextEra release says NRC approval is required. The other four values match. MAIFI's 5-minute line is the IEEE default; utilities may set their own (EIA-861 line 14; slides p.6)")
IDS = "C-F-01 C-F-02 C-F-03 C-F-04 C-F-06 C-F-07 C-F-08 C-F-09 C-F-10 C-F-12".split()
assert list(A) == IDS, set(A) ^ set(IDS)
assert all(v[2] in {"MATCH", "ROUNDING", "MISMATCH", "UNVERIFIABLE"} for v in A.values())
with open(RV + r"\V1_delta_final.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["id", "checked_value", "method", "verdict", "note"])
    for i in A: w.writerow([i, *A[i]])
print("rows:", len(A), Counter(v[2] for v in A.values()))
