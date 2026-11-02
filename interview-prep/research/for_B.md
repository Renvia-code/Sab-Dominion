# For B: verified facts for the storyline (R → B)

**Agent R · 2026-11-01 07:58.** Each item carries its claims-register id (`research/claims_register.csv`). Quote
from here; ask R before adding anything not listed.

---

## 1. C-S2-01 confirmed: the 130 → 133 headline (R-028)

- **Document:** *Dominion Energy 2025 Annual Report* (the annual report wraps the Form 10-K).
  - Company copy: `https://s2.q4cdn.com/510812146/files/doc_downloads/2026/03/17/Dominion-Energy-2025-Annual-Report.pdf`
  - SEC copy (Form ARS), per the repo's `docs/01_sources.md`: `https://www.sec.gov/Archives/edgar/data/715957/000119312526115192/dei-ars-12312025.pdf`.
    Not opened by R.
- **Page:** **printed page 10** (PDF page 20), in the Dominion Energy Virginia segment description. Your "2025 Annual
  Report p. 10" is correct.
- **Exact wording:** "SAIDI performance results, excluding major events, were 133 minutes for the three-year average
  ending 2025, up from the previous three-year average of 130 minutes. **This increase is primarily due to increased
  storm activity.**"
- **Why the last sentence matters:**
  - Dominion itself attributes the rise mainly to storms. The deck's finding (more interruptions, not longer ones)
    and the weather slide are *consistent with* Dominion's own explanation; that helps.
  - Use it as "Dominion attributes the increase primarily to increased storm activity (2025 Annual Report, p. 10)".
  - The candidate's analysis adds the *how*: the rise shows up in frequency (SAIFI), not duration (CAIDI).
  - Don't claim the analysis "proves" the storm explanation.
- **Scope (updated 08:47 with D's quick check; know it, don't lead with it):**
  - The paragraph describes Virginia Power's electric operations, whose rates are set by the Virginia *and North
    Carolina* Commissions. The report does not say which territory the SAIDI covers.
  - D's check (`work/data/findings.md`, quick checks):
    - Virginia alone gives 130.22 and 133.01, which print as 130 and 133.
    - Virginia plus North Carolina gives 129.49 and 132.50, which print as 129 and 133.
    - So the reported figures are consistent with Virginia only. That fits; it does not prove it.
  - If asked: "The public Virginia data reproduces both reported figures to the minute; adding North Carolina
    would print 129, so the report's figures are consistent with Virginia only."
- **Same document, South Carolina (DESC):** 84 minutes ending 2025, up from 83 (printed p. 15; R-029). Context
  only.

## 2. Grid Resiliency programme facts for slide 6 (R-030 to R-039)

**What "Grid Resiliency" covers** (Dominion's Grid Resiliency page,
`https://www.dominionenergy.com/about/delivering-energy/electric-projects/energy-grid-transformation/grid-resiliency-projects`,
read 1 Nov 2026):
- "Grid Resiliency and its programs are a part of Dominion Energy's Grid Transformation Plan."
- **Mainfeeder Hardening (MFH):** rebuilding, relocating, converting or undergrounding targeted mainlines to stronger
  standards.
- **Voltage Island Mitigation:** adds a second transformer where a substation has only one; "should address 19
  locations"; such outages "can be upwards for 24 hours long".
- **Voltage Optimization:** uses smart-meter voltage readings; goal "a system-wide average of 1% energy savings".
- **Intelligent Grid Devices (FLISR):** fault location, isolation and restoration; more data and control for
  operators.
- **Not Grid Resiliency:** "Underground conversions are not within the scope of Grid Resiliency programs." The
  Strategic Underground Program (SUP) is a separate programme. **Don't put SUP under the team's name on a slide.**

**How Dominion selects and measures MFH work** (same page, R-036, R-037). This is the analytics hook:
- **Selection:**
  - "a data-driven process that identifies circuits that have experienced an above-average number of outages over
    the last 5 years"
  - feeders where "at least 500 customers … experienced an average SAIDI … significantly worse (more than 2
    minutes) than the rest of our customers"
- **Measurement:** "As of November 30, 2023, over 250 miles on 44 different feeders have been completed … After
  analyzing feeders that have been completed for at least 12 months, an average of **32% reduction in outage
  minutes** was found on circuits that had been hardened."

**Programme totals, by date (all company-reported; pick ONE per slide and date it):**

| Item | End-2025 (2025 Annual Report, letter) | June 2026 (Dominion release, 8 Jun 2026, via repost) |
|---|---|---|
| SUP miles underground | "roughly 2,700 miles … from 2014 to 2025" (PDF p. 8; R-032) | "about 2,900 miles … including about 300 miles in the last year" (R-012) |
| SUP outage effect | "fallen from 11 hours to just two minutes" (R-032) | "from eight hours to just two minutes" (R-012). ⚠ the starting figure differs between documents |
| MFH miles | "nearly 400 miles of distribution feeders" (PDF p. 5; R-033) | "over 350 miles"; "more than 8,000 older utility poles" (R-013) |
| MFH effect | n/a | "reduced average annual outage time by 44% for customers in these areas" (R-013) |

**SUP legal and cost frame** (2025 Annual Report printed p. 13; R-034):
- about **4,000 miles** authorised by Virginia legislation
- an annual investment cap of about **$387 million**
- expected completion **2029**
- **eight phases approved**: about 2,500 miles and $1.4 billion, recovered through Riders U and DIST
- **phase nine requested**: about 300 miles and $240 million

**Reliability context, same report:** 99.98% power availability excluding major storms in 2025, Virginia and
Carolinas (R-030). The February 2025 wind event cut power to more than 240,000 customers; more than 90% were
restored in two days (R-031).

**New, primary (2025 Annual Report printed p. 120), added 08:30:** GT Plan **Phase IIIB** (2024–2026; filed Mar
2025, approved Sep 2025):
- mainfeeder hardening on 20 more feeders in 2025–2026
- "continued implementation of a new outage management system"
- one new project, "a remote sensing, image management and analytical program"
- $278 million capital

It is the cleanest public evidence that this team's data world now includes an OMS and remote-sensing analytics.
Good for slide 6 ("data I'd ask for first: OMS events, AMI, remote-sensing condition data") without implying inside
knowledge.

**Why reliability matters financially** (printed pp. 18–19): from the 2025 Biennial Review on, the SCC "may, at its
discretion, increase or decrease Virginia Power's authorized ROE by up to 50 basis points based on factors that may
include reliability, generating plant performance, customer service and operating efficiency". One line for the
close or the "why this role" answer.

## 3. Suggested use on slide 6 (B decides)

1. **"Where I'd start" reads naturally as an extension of Dominion's own method:**
   - rank feeders by customer-minutes and by frequency; Dominion already screens on 5-year outage history and
     SAIDI
   - measure MFH outcomes against comparable unhardened feeders and weather, not only before and after. This
     builds on Dominion's published 32% before/after measure; never present it as a criticism
   - add CEMI-style counts (customers with repeated interruptions) and AMI last-gasp restoration timing
2. **One dated proof line** if a number is needed: "Dominion reports mainfeeder hardening cut outage minutes 32% on
   feeders hardened ≥12 months (as of Nov 2023)", or the 2026 release's 44%, labelled with its date. Not both.
3. **Avoid:**
   - "Grid Resiliency runs SUP"
   - "SUP cut outages from 11 hours to 2 minutes" without the "for customers with buried lines" qualifier and the
     source date

## 4. Landed since, and still to come

- **Landed (batch 2):**
  - `dominion_on_a_page.md` (for P3 p. 7) and `dominion_dossier.md` (08:20)
  - `top40.md` and `question_bank.csv` (08:45) for B3, built by rule:
    - 24 ★ sheet picks
    - five questions to ask
    - 32 hard project questions with answer frames (the brief's seven are marked ●)
- **Landed (batch 3, 08:57):**
  - `domain_primer.md`: the **A1 one-liners table is at the top**. Ex-MED's 53% share and the SAIDI = SAIFI × CAIDI
    check are included.
  - `interview_science.md`: the **delivery-page table is at the top**: tip → study → strength → rule.
    - Reappraisal is **mixed and small**: word it as a small edge.
    - Power posing is out.
    - Answer-first, "I don't know", pacing and the follow-up note have **no verified study**; keep them as advice
      without a citation.
- **Landed (batch 4, 09:13–09:14):**
  - `freshness.md` (V5): no headline number changed.
  - V5 lines added to `dominion_on_a_page.md`.
  - `morning_prompt_2nov.md`: the block for START_HERE.
- **Landed (batch 5, 09:41), for the brief's appendix:**
  - **`hard25_print.md` (09:44): print this one.** It's a compressed copy of the full file below, about 2,000 words
    (roughly 2.3 pages at 10.5 pt in two columns). With "know every number" and the two delivery pages, the appendix
    exceeds the 4-page cap, and the orchestrator decides.
  - **`hard25_answers.md`: the 25 hardest questions with answers, the full study version.**
    - V3's 25 merged with the brief's seven (all kept, marked ●).
    - Each answer is Claim → Proof → Limit, with a locator: C-…, R-…, docs D/P/T ids, or a resume role and bullet,
      paraphrased.
    - Answers that depend on the upgrade carry "(adopted variant)" plus a "Public-only:" line.
    - Ten new numbers (N-1 to N-11) need `claims.csv` rows before print, after D confirms them. They are listed at the
      end of the file.
  - **`delivery_and_rehearsal.md`: two one-page sections.**
    - Page A: the delivery table, plus a panel block for three interviewers.
    - Page B: the Monday plan with times; Step 1 is the adopt-or-not decision.
    - Four new verified sources (R-100 to R-103).
    - The printed text never says how the pack was made. US spelling throughout; align with the brief's spelling as
      you prefer.
  - **Flag for you or D:** docs/06's Fair comparison headline says "Half the peers use a different reporting method".
    EIA-861 shows 10 of 12 on IEEE 1366 every year from 2014 to 2025; Dominion VA and Alabama Power report "Other"
    (N-5). If that headline is in the .pbix or the P4 guide, it needs fixing.
