## A6 What one minute of SAIDI means (arithmetic only)

**Finding.** For Dominion Energy Virginia in 2025, one minute of SAIDI is one minute for each of its 2,675,735 Virginia customers: **2,675,735 customer-minutes, about 44,596 customer-hours**. The rise in the three-year average behind the scorecard (130.2 -> 133.0) is about 7.5 million customer-minutes, or 124 thousand customer-hours, at 2025 customer numbers. **No dollar value is given:** R's claims register has no verified DOE ICE Calculator or LBNL value-of-reliability source (checked 1 Nov 2026), so the brief's optional order-of-magnitude estimate is skipped.

| Quantity | SAIDI (min, ex-MED) | Customer-minutes | Customer-hours |
|---|---|---:|---:|
| One minute of SAIDI, 2025 | 1 x customers | 2,675,735 customer-minutes | 44,596 customer-hours |
| Three-year average, 2022-24 -> 2023-25 | 130.2 -> 133.0 = +2.78 min | 7,450,138 customer-minutes | 124,169 customer-hours |
| 2024 -> 2025 | 131.3 -> 144.4 = +13.1 min | 35,052,128 customer-minutes | 584,202 customer-hours |
| All of 2025, ex-MED | 144.4 min x 2,675,735 | 386,376,134 customer-minutes | 6,439,602 customer-hours |

```sql
SELECT year, customers, saidi_ex_med, cust_minutes_ex_med
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2022 AND 2025 ORDER BY year
```

**Caveats.** Customer counts differ by year (2022-2024 customers are not 2025's), so the step rows use 2025 customers as an illustration; `cust_minutes_ex_med` is the exact 2025 total. SAIDI is ex-MED (Dominion files under its own major-event rule), so outages on major event days are not in these customer-minutes. Customer-minutes say nothing about who was affected: one customer out for 100 minutes and 100 customers out for one minute count the same.
