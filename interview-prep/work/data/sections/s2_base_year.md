## S2 base-year check

Question: does "the rise comes mostly from more frequent interruptions" hold whichever base year is used?
Source: EIA-861 via `mart.FCT_RELIABILITY` (Dominion Energy Virginia, utility 19876, VA, ex-MED, Dominion's own
major-event rule). 2025 values equal the EIA-861 2025 final file (released 7 Oct 2026).

### S2.1 SAIDI, SAIFI and CAIDI ex-MED, 2013 to 2025

```sql
SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med, customers
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2013 AND 2025 ORDER BY year
```

| Year | SAIDI (min) | SAIFI | CAIDI (min) | Customers |
|---:|---:|---:|---:|---:|
| 2013 | 106.0 | 1.052 | 100.8 | 2,358,445 |
| 2014 | 112.0 | 1.154 | 97.1 | 2,381,774 |
| 2015 | 119.6 | 1.155 | 103.6 | 2,420,939 |
| 2016 | 138.2 | 1.275 | 108.4 | 2,432,641 |
| 2017 | 117.4 | 1.100 | 106.7 | 2,456,901 |
| 2018 | 149.6 | 1.303 | 114.8 | 2,482,946 |
| 2019 | 149.9 | 1.244 | 120.5 | 2,507,580 |
| 2020 | 141.0 | 1.260 | 111.9 | 2,535,825 |
| 2021 | 133.6 | 1.162 | 115.0 | 2,567,152 |
| 2022 | 136.0 | 1.199 | 113.5 | 2,589,282 |
| 2023 | 123.3 | 1.165 | 105.9 | 2,612,104 |
| 2024 | 131.3 | 1.210 | 108.5 | 2,635,267 |
| 2025 | 144.4 | 1.320 | 109.4 | 2,675,735 |

SAIFI 2025 = 1.320 is the highest value in 2013-2025 (next: 2018, 1.303). CAIDI 2025 = 109.4 is below every year 2018-2022 (111.9 to 120.5) and above 2015-2017 and 2023-2024.

### S2.2 Log decomposition of the SAIDI change, every base year to 2025

ln(SAIDI2/SAIDI1) = ln(SAIFI2/SAIFI1) + ln(CAIDI2/CAIDI1). The share from frequency is ln(SAIFI ratio) / ln(SAIDI ratio);
it is only meaningful when SAIDI moved by more than about 2% (sql/02, V_TREND rule) and in the same direction as SAIFI.

```sql
WITH p AS (SELECT year, saidi_ex_med, saifi_ex_med, caidi_ex_med FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA')
SELECT a.year AS base_year, b.year AS end_year,
       ROUND(100 * (b.saidi_ex_med / a.saidi_ex_med - 1), 1) AS saidi_pct,
       ROUND(100 * (b.saifi_ex_med / a.saifi_ex_med - 1), 1) AS saifi_pct,
       ROUND(100 * (b.caidi_ex_med / a.caidi_ex_med - 1), 1) AS caidi_pct,
       ROUND(LN(b.saidi_ex_med / a.saidi_ex_med), 4) AS ln_saidi,
       ROUND(LN(b.saifi_ex_med / a.saifi_ex_med), 4) AS ln_saifi,
       ROUND(LN(b.caidi_ex_med / a.caidi_ex_med), 4) AS ln_caidi,
       ROUND(100 * LN(b.saifi_ex_med / a.saifi_ex_med) / LN(b.saidi_ex_med / a.saidi_ex_med)) AS pct_of_change_from_frequency
FROM p a JOIN p b ON b.year = 2025 AND a.year BETWEEN 2015 AND 2024
ORDER BY a.year
```

| Base year | SAIDI change | SAIFI change | CAIDI change | Share of ln change from frequency | Reading |
|---:|---:|---:|---:|---:|---|
| 2015 | +20.7% | +14.3% | +5.6% | 71% | mostly frequency |
| 2016 | +4.5% | +3.5% | +0.9% | 79% | mostly frequency |
| 2017 | +23.0% | +20.0% | +2.5% | 88% | mostly frequency |
| 2018 | -3.5% | +1.3% | -4.7% | n/m | SAIDI fell; frequency up, duration down more |
| 2019 | -3.7% | +6.1% | -9.2% | n/m | SAIDI fell; frequency up, duration down more |
| 2020 | +2.4% | +4.8% | -2.2% | 195% | frequency explains all of it; duration fell |
| 2021 | +8.1% | +13.6% | -4.9% | 164% | frequency explains all of it; duration fell |
| 2022 | +6.1% | +10.1% | -3.6% | 161% | frequency explains all of it; duration fell |
| 2023 | +17.1% | +13.3% | +3.3% | 79% | mostly frequency |
| 2024 | +10.0% | +9.1% | +0.8% | 91% | mostly frequency |

Pairs the brief needs:
- **2023 -> 2025** (the pair in the README): SAIDI +17.1%, SAIFI +13.3%, CAIDI +3.3%; 79% of the log change from frequency.
- **2022 -> 2025** (the pair that moves the 3-year average from 130.2 to 133.0, because (2023-25) - (2022-24) = (2025 - 2022)/3 = 2.78 min): SAIDI +6.1%, SAIFI +10.1%, CAIDI -3.6%. Frequency more than explains the rise; average restoration time fell.

### S2.3 Long run: 2015-17 mean vs 2023-25 mean, and OLS slopes 2015-2025 (n = 11)

```sql
SELECT
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saifi_ex_med END), 3) AS saifi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saifi_ex_med END), 3) AS saifi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN caidi_ex_med END), 1) AS caidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN caidi_ex_med END), 1) AS caidi_2023_25,
  ROUND(AVG(CASE WHEN year BETWEEN 2015 AND 2017 THEN saidi_ex_med END), 1) AS saidi_2015_17,
  ROUND(AVG(CASE WHEN year BETWEEN 2023 AND 2025 THEN saidi_ex_med END), 1) AS saidi_2023_25,
  REGR_SLOPE(saifi_ex_med, year) AS saifi_slope, REGR_SLOPE(caidi_ex_med, year) AS caidi_slope, REGR_SLOPE(saidi_ex_med, year) AS saidi_slope
FROM mart.FCT_RELIABILITY WHERE utility_key = '19876|VA' AND year BETWEEN 2015 AND 2025
```

Slope standard errors and p-values: `scipy.stats.linregress` on the same 11 rows (two-sided, t with 9 df).

| Measure | 2015-17 mean | 2023-25 mean | Change | OLS slope per year | 95% CI | p |
|---|---:|---:|---:|---:|---|---:|
| SAIFI | 1.177 | 1.232 | +4.7% | 0.0043 | -0.0111 to 0.0196 | 0.54 |
| CAIDI (min) | 106.2 | 107.9 | +1.6% | 0.17 | -0.94 to 1.28 | 0.74 |
| SAIDI (min) | 125.1 | 133.0 | +6.3% | 0.64 | -1.87 to 3.15 | 0.58 |

Period-mean decomposition: ln SAIFI ratio 0.0457, ln CAIDI ratio 0.0159, so 74% of the 2015-17 -> 2023-25 rise in SAIDI is frequency (period means of the annual values; SAIDI of the means is not exactly SAIFI x CAIDI of the means, the gap is under 0.2%).

### S2.4 Answer

- **Yes for every base year in which SAIDI rose.** Against 2015, 2016, 2017, 2020, 2021, 2022, 2023 and 2024, SAIFI rose by more than CAIDI, or CAIDI fell. For 2022 -> 2025 (the pair behind 130.2 -> 133.0) frequency more than explains the rise: SAIFI +10.1%, CAIDI -3.6%.
- **Against 2018 and 2019 SAIDI is lower in 2025** (149.6 and 149.9 then, 144.4 now): frequency is still higher in 2025, duration is lower. So the safe wording is about the recent rise, not "reliability is worse than ever".
- **2025 frequency is a record for the series:** SAIFI 1.320 is the highest of 2013-2025. Restoration time (CAIDI 109) is mid-range: higher than 2015-17 and 2023-24, lower than 2018-22.
- **Long run, neither trend is statistically clear on 11 points** (SAIFI slope p = 0.54, CAIDI slope p = 0.74; both 95% intervals include zero). The 2015-17 -> 2023-25 rise in SAIDI (+6.3%) is 74% frequency, so the direction agrees with the short-run pairs; present the long run as direction, not proof.
- **Defensible sentence:** "Measured from 2022 or from 2023, most of the increase in outage minutes came from more interruptions per customer; average restoration time changed little (3.6% shorter than in 2022, 3.3% longer than in 2023). In 2025 interruptions per customer were the highest in EIA's 2013-2025 record."

## Q10 check: trend in the weather-adjusted SAIDI (sql/07)

```sql
SELECT year, weather_adjusted_saidi FROM mart.SAIDI_WEATHER_ADJUSTED ORDER BY year
-- sql/07 Q10: SELECT ROUND(REGR_SLOPE(weather_adjusted_saidi, year), 2) FROM RELIABILITY.MART.SAIDI_WEATHER_ADJUSTED
```

- Slope **+0.34 minutes per year** over 2015-2025 (n = 11; SQL REGR_SLOPE and scipy agree: +0.338).
- Standard error 0.772; **95% CI -1.41 to +2.08 min/yr; p = 0.67**; R2 = 0.021.
- The adjusted series comes from a fit on the same 2015-2024 years (intercept 104.3, slope 0.0518 min per storm county-day, after decision D22), so it is model-based and its uncertainty is understated by this CI.
- **Wording to defend:** "After the exploratory weather adjustment, there is no clear trend since 2015: about +0.3 minutes a year, with a 95% range from roughly -1.4 to +2.1." B's "no clear trend since 2015" is right; avoid "flat" or "has not moved" (the README's older wording) because the interval is wide.
