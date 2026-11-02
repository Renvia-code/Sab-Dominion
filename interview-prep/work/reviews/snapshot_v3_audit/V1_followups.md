# V1 follow-ups: three facts checked against primary sources (R → B)

*Agent R · 2026-11-01 11:16 · for B, relayed by the orchestrator. This answers the three facts that
`work/reviews/V1_number_audit.csv` left unverified (C-Q-10 and C-S6-06 marked UNVERIFIABLE, plus the trim-cycle
line). All sources were opened on 1 Nov 2026. Register rows: `research/claims_register.csv`.*

## Verdicts

None of the three is cut. All three are verified on primary sources.

| # | Item | Verdict | Wording to print | Register |
|---|---|---|---|---|
| 1 | C-Q-10 "approved by shareholders in September" (sheet item 19) | **Verified, keep** | As now, or more exactly: "approved by both companies' shareholders on September 3" | R-104, R-105 |
| 2 | C-S6-06 "−44%" (brief, hard 25 Q8) | **Verified on Dominion's own release, keep** | "−44% average annual outage time for customers in hardened areas (Dominion, June 2026)". If space allows, add "company-reported; no baseline stated". | R-013 (now cites the primary source) |
| 3 | "4–5-year trim cycles" (brief, hard 25 Q7) | **Verified, keep** | "Dominion trims on cycles of about four to five years; nearly all neighborhood lines on four" | R-076 (re-opened) |

No change to `hard25_print.md` is needed: the Q7 and Q8 text is supported as written. I didn't edit it, because the
brief builder parses that file.

## 1. Shareholder approval (C-Q-10)

Both companies held special meetings on **3 September 2026**, and both approved. Found through EDGAR (8-Ks listing
Item 5.07, filed 3 Sep 2026).

**Dominion Energy (Form 8-K, accession 0001193125-26-381919)**
- URL: https://www.sec.gov/Archives/edgar/data/715957/000119312526381919/d323818d8k.htm
- The meeting: "On September 3, 2026, Dominion Energy, Inc. (Dominion Energy) held a special meeting of shareholders".
- The result: "As reflected below, all proposals presented for voting at the Special Meeting were approved."
- The vote on "The proposal to approve the Merger Agreement and the first plan of merger":
  - For: 671,317,253
  - Against: 8,566,156
  - Abstained: 2,185,104
  - Broker non-votes: none

**NextEra Energy (Form 8-K, accession 0000753308-26-000071)**
- URL: https://www.sec.gov/Archives/edgar/data/753308/000075330826000071/nee-20260903.htm
- The meeting: "NextEra Energy, Inc. (NEE) held a special meeting of shareholders (2026 Special Meeting) on September 3, 2026".
- The result: "At the 2026 Special Meeting, NEE's shareholders approved three management proposals."
- The vote on Proposal 1, issuing NEE shares to Dominion shareholders under the merger agreement dated 15 May 2026:
  - For: 1,612,635,616 (99.47% of votes cast)
  - Against: 8,545,037
  - Abstentions: 3,850,294

**For `claims.csv`:** C-Q-10's source column should cite R-104 and R-105 and drop "D8 not opened". Every other part
of C-Q-10 already matched in V1.

## 2. The −44% (C-S6-06): source and what it measures

**Primary source:** Dominion Energy release, dated 06/08/2026, "RICHMOND, Va.--(BUSINESS WIRE)--", on Dominion's
investor site:
https://investors.dominionenergy.com/news/press-release-details/2026/Dominion-Energy-prepares-year-round-for-hurricane-season-and-encourages-customers-to-prepare-as-well/default.aspx
(saved: `work/research_raw/v1_followups/dom_hurricane_2026.html`). The StockTitan repost that V1 couldn't open is no
longer the source.

> "Through its Mainfeeder Hardening Program, the company has replaced more than 8,000 older utility poles and hardened
> over 350 miles of power lines in Virginia. The program has reduced average annual outage time by 44% for customers
> in these areas."

**What it measures:**
- the average yearly time without power (a SAIDI-style average)
- for customers served by the hardened mainfeeders in Virginia, the areas where the 8,000+ poles and 350+ miles of
  work were done

**What the release doesn't state:**
- the baseline years or the measurement window
- whether major-event days are excluded
- any comparison group of unhardened feeders
- how many feeders are included

It is a **company-reported** result. It is a different measure from the FAQ figure already in the pack: −32% outage
minutes on feeders hardened for 12 months or more, as of 30 Nov 2023 (C-S6-02, R-036). Print them side by side with
their dates, never as one trend.

**Lead, not used:** search snippets mention a 2025 Dominion release giving −30% for hardened mainfeeders. I didn't open
it, so don't use it.

## 3. Trim cycles

**Source:** Dominion Energy, "Virginia/North Carolina Tree Trimming and Powerlines FAQ",
https://www.dominionenergy.com/safety/electric-safety/tree-trimming-and-powerlines/va-tree-trimming-and-powerlines

> Under "How do Dominion Energy and its contractors decide how much to trim?": "Our maintenance trimming is done on
> cycles typically ranging from four to five years"
>
> Under "How often do you trim?": "Nearly all of our neighborhood power lines are cleared on a four year cycle."

**For `claims.csv`:** no row carries this line yet. If the brief or sheet prints it, add a row citing R-076 with the
two quotes above.
