"""Trend tests for Dominion Energy Virginia's reliability, 2015-2025.

For SAIDI, SAIFI and CAIDI excluding major event days, and for the weather-adjusted SAIDI of
sql/07 (query Q10), this fits an ordinary least-squares line against the year and prints the
slope per year, its 95% confidence interval and the two-sided p-value (t test on n - 2 = 9
degrees of freedom), the same statistics as scipy.stats.linregress.

Reads only committed files: data/output/fct_reliability.csv (utility_key 19876|VA) and
data/output/saidi_weather_adjusted.csv. Standard library only (the t distribution is computed
here), so it runs from a fresh clone. Eleven annual points describe a direction; they cannot
establish a trend, and the weather-adjusted series is itself model-based, so its interval is
too narrow. Documented in docs/05 (Trend tests); scripts/check_output_metrics.py asserts the
values quoted there.

Run: python -I scripts/trend_tests.py
"""
import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "output"
YEARS = list(range(2015, 2026))


def _betacf(a, b, x):
    """Continued fraction for the incomplete beta function (modified Lentz)."""
    tiny, qab, qap, qam = 1e-300, a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    d = 1.0 / (d if abs(d) > tiny else tiny)
    h = d
    for m in range(1, 300):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = 1.0 / (d if abs(d) > tiny else tiny)
        c = 1.0 + aa / c
        c = c if abs(c) > tiny else tiny
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return h


def betainc(a, b, x):
    """Regularised incomplete beta function I_x(a, b)."""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    front = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b) + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return front * _betacf(a, b, x) / a
    return 1.0 - front * _betacf(b, a, 1.0 - x) / b


def t_two_sided_p(t, df):
    """P(|T| >= |t|) for Student's t with df degrees of freedom."""
    return betainc(df / 2.0, 0.5, df / (df + t * t))


def t_critical(df, level=0.95):
    """The t value with two-sided tail probability 1 - level, by bisection."""
    lo, hi = 0.0, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if t_two_sided_p(mid, df) > 1.0 - level:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def ols_trend(xs, ys):
    """Slope of y on x, its standard error, 95% interval and two-sided p (as scipy.stats.linregress)."""
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    slope = sxy / sxx
    intercept = my - slope * mx
    sse = sum((y - intercept - slope * x) ** 2 for x, y in zip(xs, ys))
    se = math.sqrt(sse / (n - 2) / sxx)
    tc = t_critical(n - 2)
    return {"n": n, "slope": slope, "se": se, "lo": slope - tc * se, "hi": slope + tc * se,
            "p": t_two_sided_p(slope / se, n - 2)}


def _read(name):
    with (OUT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def trend_table():
    """One row per series: (series, unit, result of ols_trend over 2015-2025)."""
    rel = {int(r["year"]): r for r in _read("fct_reliability.csv") if r["utility_key"] == "19876|VA"}
    adj = {int(r["year"]): float(r["weather_adjusted_saidi"]) for r in _read("saidi_weather_adjusted.csv")}
    if not all(y in rel for y in YEARS) or sorted(adj) != YEARS:
        raise SystemExit("2015-2025 rows missing from the committed outputs")
    rows = []
    for col, label, unit in (("saidi_ex_med", "SAIDI ex-MED", "minutes"),
                             ("saifi_ex_med", "SAIFI ex-MED", "interruptions per customer"),
                             ("caidi_ex_med", "CAIDI ex-MED", "minutes")):
        rows.append((label, unit, ols_trend(YEARS, [float(rel[y][col]) for y in YEARS])))
    rows.append(("Weather-adjusted SAIDI (sql/07 Q10)", "minutes", ols_trend(YEARS, [adj[y] for y in YEARS])))
    return rows


def main():
    print("Dominion Energy Virginia, 2015-2025 (n = 11): OLS slope per year, 95% CI, two-sided p (t, 9 df)")
    print(f"{'Series':<38}{'Slope/yr':>10}{'95% CI':>22}{'p':>7}")
    for label, unit, r in trend_table():
        dp = 4 if label.startswith("SAIFI") else 2
        ci = f"{r['lo']:+.{dp}f} to {r['hi']:+.{dp}f}"
        print(f"{label:<38}{r['slope']:>+10.{dp}f}{ci:>22}{r['p']:>7.2f}")
    print("Eleven points describe a direction, not a proven trend; the weather-adjusted series is model-based.")


if __name__ == "__main__":
    main()
