# Domain primer: utility reliability for the Dominion panel (R3)

*Agent R · 2026-11-01 08:55 · for B's appendix A1, the brief's domain-primer page (P3 p. 8) and the candidate's own
study.*

- **Source ids** in brackets point to §8 and to `claims_register.csv` (R-xxx). [I] marks R's inference.
- **IEEE Std 1366-2022 itself is paywalled and was not opened.** The definitions come from two places:
  - EIA's form instructions, which require the IEEE 1366-2003/2012 method
  - IEEE PES training slides (2019)

  The core definitions are the same in every edition we could see.

---

## A1. One-liners to say without notes (for B's appendix)

| Term | Say it like this | Source |
|---|---|---|
| **Sustained interruption** | An outage longer than five minutes. Shorter ones are "momentary" and are left out of SAIFI and SAIDI. | [IEEE-S p6; EIA-I p9] |
| **SAIFI** | How often the average customer loses power in a year: customers interrupted ÷ customers served. | [EIA-I p9; IEEE-S p10] |
| **SAIDI** | How many minutes the average customer is without power in a year: customer-minutes interrupted ÷ customers served. | [EIA-I p9; IEEE-S p10] |
| **CAIDI** | How long an interrupted customer waits for power back, on average: SAIDI ÷ SAIFI. "Be careful with this one. The numbers can be deceiving." | [IEEE-S p10, p41] |
| **The identity** | SAIDI = SAIFI × CAIDI. So a rise in SAIDI is either more interruptions or longer ones; the deck's S2 finds it was frequency. Dominion VA 2025: 1.320 × 109.4 ≈ 144.4. | [IEEE-S p41; F06] |
| **MAIFI** | Like SAIFI, but for momentary interruptions (breaker or recloser blinks). MAIFI_E counts events and leaves out momentaries that were part of a sustained outage. | [IEEE-S p50] |
| **CEMIn** | The percent of customers who had *n* or more sustained interruptions. It shows who the average hides. | [IEEE-S p47–48] |
| **CELID** | The percent of customers whose interruptions lasted *S* hours or more. | [IEEE-S p48] |
| **Major event day (MED)** | A day whose SAIDI is far above normal: above T_MED = e^(α + 2.5β). α and β are the mean and standard deviation of ln(daily SAIDI) over the previous five years. | [IEEE-S pp75, 82, 86; R-070] |
| **Why report ex-MED** | A few extreme storm days would swamp the year-to-year trend. Ex-MED shows everyday performance; storm days are judged separately, as storm response. | [IEEE-S pp72–75; I] |
| **What ex-MED hides** | In 2025, major-event days were about half (53%) of Dominion Virginia's all-event SAIDI: 306.7 against 144.4 ex-MED. | [F06; LOCK A3] |
| **Customer** | A metered service point with an active bill account at a location (IEEE's definition, used by EIA). | [EIA-I p9] |
| **AMI** | Meters that record usage at least hourly and send it to the utility at least daily. At Dominion VA, 99.8% of meters are AMI (2025). | [EIA-I p17; F15] |

Two cautions to keep handy:
- One SAIDI minute at Dominion VA is about 2.7 million customer-minutes (2,675,735 customers) [C-S6-05].
- Comparing utilities is hard: the SCC says so itself, so the deck's peer slide is "indicative" [R-021].

---

## 1. The indices, with a worked check

- **Basis.** Every index is built from two counts per interruption: customers interrupted (CI) and customer minutes
  interrupted (CMI). "CI and CMI provide the basis for calculating the indices" [IEEE-S p13].
  - SAIFI = ΣCI ÷ customers served
  - SAIDI = ΣCMI ÷ customers served
  - CAIDI = ΣCMI ÷ ΣCI
- **EIA's wording**, the one the deck's data use [EIA-I p9]:
  - SAIFI "indicates how often the average customer experiences a sustained interruption (of over 5 minutes) over
    a predefined period of time".
  - SAIDI "indicates the total duration of interruption for the average customer over a predefined period of
    time".
- **The slides' worked exercise** [IEEE-S pp40–41]: SAIDI 159 min, SAIFI 2.02, so CAIDI = 159 ÷ 2.02 ≈ 79 min.
  - Dominion VA 2025 checks the same way: 144.4 ÷ 1.320 = 109.4 [F06].
- **Why CAIDI misleads** [I]: it can *fall* when SAIFI rises, if the extra interruptions are short ones. Read it
  together with SAIFI, never alone. The slide's own warning is "The numbers can be deceiving" [IEEE-S p10].
- **Momentary interruptions don't count** in SAIFI or SAIDI. Each recloser operation is a separate momentary
  interruption [IEEE-S pp6, 25]. "Some companies and/or jurisdictions may use one minute or some other interval"
  as the momentary cut-off [IEEE-S p6].
- **Averages deceive.**
  - The slides' example: a utility with SAIDI 90 and SAIFI 1.5, where half the customers are on a network that
    hasn't had an interruption in ten years. The other half are worse off than the average says [IEEE-S p47].
  - CEMIn and CELID exist "to give a view of the relative number of customers with reliability below some
    threshold" [IEEE-S p48].
  - Dominion's own mainfeeder screen works the same way: it looks for groups of at least 500 customers whose
    SAIDI is more than 2 minutes worse than everyone else's [R-037].

## 2. Major event days and the 2.5-beta method

**How it works** [IEEE-S pp72–88; R-070]
1. Compute SAIDI for every day of the previous five years.
2. Take the natural log of each day's value. Daily SAIDI is heavily skewed, but "Ln (SAIDI) is a reasonable bell
   curve ('log-normal distribution')" [p74].
3. α = mean of ln(daily SAIDI); β = its standard deviation [p82].
4. T_MED = e^(α + 2.5β). It is "basically, two and a half standard deviations on an average" [p80].
5. Any day in the *next* year with SAIDI above T_MED is a major event day. "This TMED is used to evaluate the next
   year"; "For 2019, Calculate TMED using 2014 – 2018 data" [p86].

**Other definitions exist.** "Definitions vary by utility, regulator, and/or others." Examples: named storms,
declarations of emergency, the worst x% of days, and exclusions set by regulators [IEEE-S p72].
- **Virginia's SCC** charts SAIFI and SAIDI that "omit the impacts of major weather-related events such as
  hurricanes and derechos" [RD916 fn 13; R-020].
- **EIA** asks utilities that use IEEE 1366 to report with and without MEDs (Part B), and others to report
  their own method (Part C) [EIA-I pp9–10].

**Why it matters for the deck**
- The ex-MED series shows the everyday grid.
- The MED days are the storm story:
  - Dominion VA, 2025: MED days were 53% of all-event SAIDI [F06].
  - US, 2024: major events were 80% of hours without power (Hurricanes Beryl, Helene, Milton) [EIA-TIE].
- **How ex-MED SAIDI can still rise "because of storms"** [I]:
  - Storm days that stay below T_MED remain in the ex-MED figure. The deck's S4 storm effect holds on non-major
    days (9.9×) [LOCK S4].
  - The threshold is set from the five prior years, so after a run of stormy years T_MED rises and fewer days
    qualify as MEDs.

## 3. EIA-861 versus the Virginia SCC report

| | EIA-861, Schedule 3 (the deck's source) | SCC Annual Reliability and Tree Trimming Report |
|---|---|---|
| Who reports | Distribution utilities nationwide, by state | Each of Virginia's three investor-owned utilities: Dominion, APCo and ODP [RD916 p11 fn 12; R-019] |
| Method | IEEE 1366-2003 or 2012, with and without MEDs (Part B), or "another method" (Part C) [EIA-I p9] | SAIFI and SAIDI that omit major weather-related events [R-020] |
| Extra cuts | Lines for SAIDI and SAIFI excluding events "initiated by a loss of supply from the high-voltage system", and whether the utility has an OMS "that detects loss of load or customer outages" [EIA-I p9] | Tree-trimming measures sit alongside the indices (the report's name) [R-019] |
| Detail | Annual, utility by state; public | Annual filings on the SCC docket site, which returns 403 to us. Five-year charts appear in the SCC's report to the General Assembly [RD916 p12] |
| Comparisons | National and peer series possible | The SCC cautions that utility-to-utility comparisons are difficult [R-021] |

**The rule behind the SCC report: not found.**
- It is not in the 20VAC5 chapters we searched.
- RD916's footnote to the report names only the three utilities and cites no rule.
- The SCC's own site is blocked to us (403), and we did not work around it.
- **History [I]:**
  - In 1990, answering 1989 House Joint Resolution 155, the SCC set tree-trimming guidelines [HD21 p5].
  - It told each utility to state its "capability to track previously specified data in order to respond to
    Commission data requests on an annual basis beginning with the calendar year 1990" [HD21 pp25–27].
  - That is probably the root of the annual tree-trimming reporting. It is not confirmed.
- **Dominion's own published number** (2025 Annual Report p. 10): three-year SAIDI ex-major events of 133 min, up
  from 130 [R-028]. D's check shows these match Virginia-only data: 130.22 and 133.01. Adding North Carolina would
  print 129.

## 4. How utilities analyse reliability

1. **Split the change.** Frequency or duration? SAIDI = SAIFI × CAIDI. The deck's S2 finding is that 2022→2025 was
   frequency, up 10%, while CAIDI fell 4% [F01].
2. **Cause codes.** "Utilities categorize interruptions depending on if they are attributed to major events such as
   hurricanes or other storms, interference from vegetation near power lines, or atypical utility operations"
   [EIA-TIE]. Cause by feeder and device is the first internal data to ask for. Public data has none.
3. **Worst-performing circuits.**
   - Dominion picks mainfeeders through "a data-driven process that identifies circuits that have experienced an
     above-average number of outages over the last 5 years" [R-037]. Its GT booklet calls them "worst performing
     mainfeeders" [R-027].
   - It reports a 32% cut in outage minutes on feeders hardened for at least 12 months (as of Nov 2023) [R-036].
   - A stronger test would compare against similar unhardened feeders and the same weather, and allow for
     regression to the mean, because the feeders were chosen *for* bad history [I].
4. **Customers the average hides.** CEMIn and CELID; repeat-outage customers [IEEE-S pp47–48].
5. **Vegetation cycles.**
   - Dominion Virginia: "maintenance trimming is done on cycles typically ranging from four to five years";
     "nearly all of our neighborhood power lines are cleared on a four year cycle" [DOM-VEG].
   - Dead ash trees are being removed under an SCC-approved mitigation plan [DOM-VEG].
   - Wind, precipitation and lightning go with more interruptions [LARSEN].
6. **Storm restoration.**
   - Restoration curves show the percent restored against hours since the peak. In the deck's Isaias inset, 90% of
     customers were restored in 33.5 h [LOCK S4]. Restoration has not clearly got faster over time (p = 0.07; notes
     only).
   - Dominion's February 2025 wind event cut power to more than 240,000 customers; over 90% were restored in two days
     [R-031].
7. **Estimated restoration times (ETR).** No source on how accurate these are was opened in this run. Ask the
   panel how the team measures it rather than asserting a method.
8. **Meters and outage systems.**
   - AMI meters time each customer's outage, through last-gasp and restore messages [I].
   - EIA-861 asks whether a utility's OMS detects loss of load [EIA-I p9].
   - Dominion is putting in a new OMS and a remote-sensing analytics programme under GT Phase IIIB [R-060].
   - Better detection can raise recorded SAIFI without the grid getting worse. Check this before reading a trend
     [I; hard question H21].

## 5. Grid vocabulary the panel will use

- **Feeder / mainfeeder** [I]: a distribution circuit leaving a substation, and its main trunk line. Dominion's
  Mainfeeder Hardening rebuilds, relocates, converts or undergrounds "targeted mainlines to stronger standards"
  [R-035].
- **Grid Resiliency programmes:**
  - Mainfeeder Hardening
  - Voltage Island Mitigation: a second transformer where a substation has only one, at 19 locations [R-038]
  - Voltage Optimization: smart-meter voltage readings; goal of 1% energy savings [R-039]
  - Intelligent Grid Devices: fault location, isolation and restoration (FLISR) [R-035]
  - The Strategic Underground Program is **separate** [R-035].
- **Undergrounding.**
  - SUP: about 2,700 miles buried 2014–2025, out of about 4,000 authorised; completion expected 2029
    [R-032, R-034].
  - In the literature, more underground line miles go with fewer minutes of interruption [LARSEN].

## 6. PJM, the DOM zone and data-centre load

- **PJM** "is the regional transmission organization that manages the electric grid and wholesale electricity
  market in Virginia and across 12 other states and the District of Columbia" and "must maintain reliability of the
  transmission grid" [RD916 pp10–11].
- **The DOM zone** is the Dominion transmission zone in PJM's planning tables [R-026].
  - The deck's hourly load (EIA-930) covers the zone. The zone is larger than Dominion's retail territory and
    includes other utilities' load [findings caveat; LOCK S5].
- **Data-centre load** (Dominion's own statements):
  - over 54 GW in contracting stages; over 12 GW under service agreements [R-054]
  - 11 data centres (744 MW) connected in 2025 [R-040]
  - all 10 of the DOM zone's 2026 summer peak days [R-055]
  - a new GS-5 class for loads of 25 MW or more from 1 Jan 2027 [R-056]
- **The deck's S5 pattern** (overnight load growing faster; winter peaks) is consistent with large round-the-clock
  loads. It is **not** attributed to them [D14].

## 7. What the research says (weather, outages, trends)

**Larsen, LaCommare, Eto and Sweeney (2016), *Energy* 117, 29–46** [LARSEN]
- Data: 13 years of utility-reported reliability.
- Interruption frequency correlates with above-average wind speeds, precipitation, lightning strikes and customers
  per line mile.
- Minutes of interruption correlate with wind, precipitation, cooling degree-days and underground line miles.
- "We find a significant time trend of increasing annual average number of minutes of power interruptions over
  time—especially when interruptions associated with extreme weather are included."
- Strength: peer-reviewed, a large panel; correlational.

**Do et al. (2023), *Nature Communications* 14** [DO]
- Data: county outages for 2018–2020.
- About 520 million customer-hours without power a year across 2,447 counties.
- "62.1% of 8+ hour outages co-occur with extreme weather/climate events, particularly heavy precipitation,
  anomalous heat, and tropical cyclones."

**Brelsford et al. (2024), *Scientific Data* 11** [BRELSFORD]
- The EAGLE-I county data behind the deck's S4: 15-minute county outage estimates, 2014–2022.
- Coverage reached 92% of customers by 2022 and "increases through time".
- A Data Quality Index covers 2018–2022.
- [I] Rising coverage can make raw outage counts look higher in later years, so year-to-year comparisons need
  care. S4's storm-versus-calm comparison holds in every year, and four counties are left off for unreliable data
  [LOCK S4].

**EIA, Today in Energy (2024 data)** [EIA-TIE]
- US customers averaged 11 hours of interruptions in 2024, "nearly twice as many as the annual average experienced
  in the decade before".
- Interruptions not triggered by major events "routinely average about two hours per year".
- [I] Context only, since methods differ: Dominion VA's 2025 ex-MED SAIDI of 144.4 min (about 2.4 h) is a little
  above that routine national level. The deck's peer comparison (S3) is the careful version.

## 8. Sources (all opened and read 2026-11-01)

| Id | Source | URL or DOI | Locator |
|---|---|---|---|
| IEEE-S | J. Teixeira (National Grid), "IEEE 1366 – Reliability Indices", IEEE Boston Section, 19 Feb 2019 (training slides) | https://site.ieee.org/boston-pes/files/2019/03/IEEE-1366-Reliability-Indices-2-2019.pdf | pp3, 6, 10, 13, 25, 40–41, 47–50, 72–88 |
| EIA-I | EIA, Form EIA-861 Instructions (OMB 1905-0129, exp. 07/31/2029) | https://www.eia.gov/survey/form/eia_861/instructions.pdf | p9 Schedule 3 Parts B–C; p17 AMI definition |
| EIA-TIE | EIA, Today in Energy, "Hurricanes in 2024 led to the most hours without power in the United States in 10 years" | https://www.eia.gov/todayinenergy/detail.php?id=66744 | article text |
| RD916 | Virginia SCC, Annual Report on Grid Modernization, Reliability, and Integration of Renewables (RD916, 1 Dec 2025) | https://rga.lis.virginia.gov/Published/2025/RD916/PDF | pp10–12, fn 12–14 |
| HD21 | Virginia SCC, Report on Tree Trimming Guidelines for Utility Line Clearance (House Document 21, 1990) | https://rga.lis.virginia.gov/Published/1990/HD21/PDF | pp5, 25–27 |
| DOM-VEG | Dominion Energy, "VA Tree Trimming and Powerlines" | https://www.dominionenergy.com/safety/electric-safety/tree-trimming-and-powerlines/va-tree-trimming-and-powerlines | FAQ text |
| LARSEN | Larsen, LaCommare, Eto, Sweeney, *Energy* 117 (2016) 29–46 | doi:10.1016/j.energy.2016.10.063 (abstract read in the eScholarship preprint: https://escholarship.org/uc/item/2rv3v46z) | abstract |
| DO | Do et al., *Nature Communications* 14 (2023) | doi:10.1038/s41467-023-38084-6 | abstract |
| BRELSFORD | Brelsford et al., *Scientific Data* 11 (2024) | doi:10.1038/s41597-024-03095-5 | abstract |
| F01, F06, F15; LOCK; C-S6-05; D14 | D's findings, the storyline lock, the claims file, the decision log | `work/data/findings.md`, `work/storyline_LOCK_G1.md`, `claims.csv`, `docs/04` | as cited |

**Gaps:**
- The IEEE 1366-2022 standard text (paywalled).
- The SCC's rule for the Annual Reliability and Tree Trimming Report. Not found; the SCC site returns 403 and was
  not worked around.
- Any source on ETR accuracy.
- LBNL's value-of-service work (Sullivan et al., 2015), not opened. Not needed for the deck.
