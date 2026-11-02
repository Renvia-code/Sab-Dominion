# Prior chat notes (as received, 2026-11-01)

The owner pasted these from an earlier chat with another assistant. **They are leads, not facts.**
Every figure must be re-verified against a primary source before it reaches a deliverable. The last
part of the paste (how to open the .pbix against the owner's old Snowflake trial) is left out: this
workspace now uses its own Snowflake account (see `CLAUDE.md` and `_setup/README.md`).

---

## A. Dominion Energy research summary (prior chat)

Dominion Energy (NYSE: D): research summary

The big picture: Dominion is a regulated utility growing fast on Virginia data-center demand. Its biggest open question is the pending $66.8B acquisition by NextEra Energy, which regulators have not yet approved. This is not investment advice.

What it is
- Richmond, VA utility holding company. It provides regulated electricity to 3.6 million homes and businesses in Virginia, North Carolina and South Carolina, and regulated gas to 500,000 customers in South Carolina.
- Three segments: Dominion Energy Virginia, Dominion Energy South Carolina, and Contracted Energy. Contracted Energy includes the Millstone nuclear plant and solar assets.
- At the end of 2025 it had about 30.7 GW of generating capacity.
- CEO and chair is Robert (Bob) Blue; CFO is Steven Ridge.

Latest results (Q3 2026, reported Oct 30)
- Operating earnings were $1.28 per share, up from $1.06 a year earlier.
- Management expects to land in the top half of its 2026 guidance range of $3.45 to $3.69 per share. It reaffirmed its credit, dividend and long-term growth guidance.
- Long-term growth target is 5–7% annual operating EPS growth through 2030, leaning toward the upper half from 2028 on.
- The annual dividend is $2.67 per share, or 66.75 cents per quarter.

The NextEra merger
- Terms: Each Dominion share converts into 0.8138 NextEra shares. Dominion holders also keep the current dividend through closing and get a one-time $360 million cash payment shared across all shares. Dominion holders would own about 25.5% of the combined company.
- Customer pitch: $2.25B in shareholder-funded bill credits across Virginia, North Carolina and South Carolina, with no merger costs passed to customers.
- Status: Shareholders of both companies approved the deal in early September. Close is expected in the second half of 2027. It still needs FERC, NRC, antitrust, and Virginia, North Carolina and South Carolina approvals.
- Political friction in Virginia: Gov. Spanberger formally intervened in the SCC case, which was unprecedented for a Virginia governor. Lt. Gov. Hashmi pushed for a longer review. Two Republican legislators called for a special session on the deal. The SCC chair previously worked as a senior NextEra attorney, which adds scrutiny.
- Stock: the stock jumped about 9% on announcement. Ahead of Q3 earnings it traded around $62, below its 200-day average and down roughly 10% since the prior report. The implied deal value is well above that, which points to market doubt about closing or timing (the prior assistant's inference, not a sourced fact).

Growth driver: data centers
- Dominion has more than 53 GW of data-center capacity in various stages of contracting, about 12 GW of it under signed service agreements.
- Nine of its ten highest-ever peak-demand days occurred in 2026.
- The five-year capital plan for 2026–2030 is $64.7B, up from $50.1B. About 64% of it is eligible for rider recovery, and over 90% of the increase is in Virginia. Equity issuance of about $8.8B through 2030 is required.
- Regulators approved a smaller base-rate increase than requested last November: about $11.24 a month for the average household in 2026 and $2.36 more in 2027. They also created a new large-user rate class (25 MW and up) from 2027.
- New data-center contracts run 14 years with minimum-demand charges and collateral of $1.5M per MW. Recently the SCC also told Dominion to shift more future transmission costs onto data centers. Affordability is becoming a political issue.

Coastal Virginia Offshore Wind (CVOW)
- It is a 176-turbine, 2.6 GW project. It was 81% complete at the Q2 call, with 31 turbines installed.
- The final turbine is now expected by year-end 2027, a six-month slip, and cost is up about 2% to $11.65B. Management called the delay largely earnings-neutral because of how recovery works.
- Stonepeak holds a 50% noncontrolling interest in the commercial project, per the 10-K.
- Federal political risk remains. An earlier stop-work order on offshore wind did not end the project.

Balance sheet and analyst view
- FFO-to-debt was 15.3% at year-end 2025 against a ~15% target.
- S&P rates it BBB+ with a positive outlook. Fitch has the same rating on Rating Watch Positive after the merger announcement.
- Analyst consensus is "Hold" with a price target near $70.

Key risks: merger rejection or heavy conditions; affordability backlash over data-center costs; CVOW execution and the large capital and equity needs; concentration of growth in Virginia.

Caveats given at the time: stock figures from secondary sources and a few weeks old; the Q3 call transcript was not pulled; some aggregator pages looked unreliable.

Sources named at the time: Q3 2026 results (8-K); Q2 2026 call highlights (Nasdaq); NextEra merger announcement; shareholder vote (WHSV); Spanberger intervention (Virginia Mercury); merger approval timeline (NextEra 425 filing); data-center demand (WTVR, Oct 27); Q4 2025 capital plan summary (Fintool); 2025 10-K; Virginia rate case (Cardinal News); pre-Q3 stock and CVOW delay (Earnings Whispers); analyst consensus (StockAnalysis).

---

## B. The dashboard the owner pictured (internal reference only)

The owner asked for Midjourney prompts for "a creative high end analytical dashboard" covering:
1. reliability: number of outages, customers affected, how fast outages are restored, frequency of outages;
2. hourly demand at county level over history;
3. summer and seasonal peaks, hourly usage over the years, residential vs commercial customer split;
4. storms, because Virginia is storm prone.

The four concepts produced (Midjourney V8.2, `--raw`, low stylize):
1. **Grid command centre (dark):** KPI cards SAIFI, SAIDI, CAIDI, Customers Out, Active Outages; a Virginia county choropleth of outage density; restoration-time curve; outage frequency bars; multi-year hourly demand line; residential vs commercial donut.
2. **Demand analytics (light, Swiss editorial):** calendar heatmap of hourly load across years; county selector; ridgeline of summer vs winter load by hour; annotated peaks; small multiples per county.
3. **Storm and outage response:** Virginia coast and Chesapeake map with storm track, wind bands and lightning; live outage counter; percent-restored curve over hours; crew panel; storm timeline by year; outages per storm.
4. **Load patterns and customer mix (ultrawide):** stacked area of hourly load by residential, commercial and industrial over ten years; polar chart of hourly usage by season; annual summer peak bars with records highlighted; reliability sparklines; customer count tiles.

Reliability terms as explained then: SAIFI is how often the average customer loses power per year; SAIDI is total outage minutes per customer per year; CAIDI is the average restoration time per interruption (SAIDI / SAIFI).

---

## C. Review of `Dominion Dashboards.pbix` (prior chat; confirmed present in the file on 2026-11-01)

Must fix:
1. Landing page titles are swapped. Executive Dashboard-1 opens with "Electricity Demand & Grid Planning" but shows reliability charts. Executive Dashboard-2 says "Reliability Performance & Drivers" but shows demand charts.
2. Titles claim more than the data shows (the repo's own docs/06 says to change these):

| Current | Safer |
|---|---|
| "…That gap is data centres" | "…consistent with large round-the-clock loads" |
| "Remove the weather and the underlying number has not moved since 2015" | "Weather-adjusted SAIDI (model estimate) is roughly flat since 2015" |
| "2025 sits where its weather predicts" | "More storm days, more outage minutes (r = 0.70, 10 years)" |
| "Major storms are half of all outage minutes… and the whole of the bad years" | "Major-event days are about half of all-event SAIDI in 2025" |
| Card: "Share of outage mins caused by major storms" | "Major-event-day share of SAIDI" |

3. Wrong axis label: the Growth chart's subtitle and data use 2013 = 100, but the axis says "Index, 2023 = 100".
4. The peer-group slicer on Executive Dashboard-1 can make the page contradict itself (pick "Dominion Energy SC": cards and SAIFI/CAIDI change, weather charts stay Dominion VA, titles still say "Dominion Energy Virginia… up 6%"). Remove it from that page or lock it to Dominion VA; keep it on the Peer page.
5. It may not refresh on another computer: 5 tables point to `C:\Users\SakethBollina\Downloads\…xlsx`, 11 come from Snowflake. Test offline. Replace the hardcoded path with a folder-path parameter.

Clean-up:
- Delete unused tables: Headline, V_STORM_VS_SAIDI (2), V_TREND, STORM_INDEX; delete the empty measure `Measure`.
- Delete the auto-created relationship Headline[losses_pct] → Programmes2025[losses_pct]; turn off auto-detect relationships. Headline imported 4 rows including note text instead of 1.
- AmiEventStudy: header row not promoted (Column1–4), data not shown anywhere, only holds the "Selected" measures. Build a small page from it or move the measures to a `_Measures` table.
- 11 visuals sum raw columns (for example SAIFI on What Moved); works only because of page filters. Use measures such as [SAIFI ex MED].
- Add a Data Quality page: the Tests table is loaded but unused; docs describe a Data Notes page and a reconciliation table that are not in the file.
- Polish: "Peer Comparision" typo; "data centres" → "data centers"; alt text on 0 visuals; Seasonal page has one chart.

Likely panel questions about the file:
- "Why Snowflake plus an Excel file?" One line: warehouse data in Snowflake, small reference tables in Excel.
- "How do the KPI cards follow the year slicer?" A disconnected Dashboard Year table read with SELECTEDVALUE, defaulting to 2025.
- "What happens if I pick another utility in that slicer?" Fix #4 first.
- "How does your three-year SAIDI match the annual report?" Average of annual customer-weighted values: 130.2 and 133.0.
- "Walk me through your model." Fact table, utility dimension, year-keyed side tables.

Suggested addition: a distribution-level page, a county outage map with restoration curves from EAGLE-I.
