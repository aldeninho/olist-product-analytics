# Olist E-Commerce — Product Analytics Case Study

**One-line problem:** With ~99k real orders and near-zero repeat purchase, where is an e-commerce marketplace leaking revenue and customer satisfaction — and what should product fix first?

![Dashboard](charts/dashboard_screenshot.png)

## Key findings

**Finding 1 — Retention is the biggest lever, and it's broken.**
- Evidence: Only 3.1% of 96k customers ever buy twice (1.03 avg orders/customer); month-over-month customer churn is ~99.5%.
- Business implication: A repeat-purchase/loyalty program likely creates more revenue than acquisition spend at the top of the funnel.

**Finding 2 — Late delivery is strongly associated with low satisfaction.**
- Evidence: On-time orders average 4.29/5 reviews vs 2.27/5 for late orders; Welch two-sample t-test t ≈ 101, p < 0.001 (n = ~96k).
- Business implication: Fix delivery SLAs. *Limitation: this is an observational correlation — late delivery may proxy for problem regions/categories, not a pure causal effect.*

**Finding 3 — Revenue is concentrated geographically and by category.**
- Evidence: São Paulo alone generates R$6.0M of R$16.0M total revenue; bed/bath, health & beauty, and computers accessories are the top-3 categories.
- Business implication: Targeted marketing + logistics in high-revenue regions/categories yields the highest ROI.

## Tools
- SQL (DuckDB) · Python (pandas, scipy, seaborn, matplotlib) · Streamlit

## Methodology
1. Loaded the public **Olist** dataset (~100k real orders, 2016–2018, `github.com/olist/work-at-olist-data`) into DuckDB.
2. SQL: 8 analyses — order-status funnel, MAU engagement, monthly cohort retention, month-over-month churn, revenue/LTV, state & category segmentation, delivery performance, A/B-style group comparison.
3. Python: t-test on delivery vs review scores; publication-ready charts; Streamlit dashboard.

## Run it yourself
```bash
pip install -r requirements.txt
python scripts/build_db.py      # load CSVs into DuckDB
python scripts/run_sql.py       # run all SQL analyses -> results/
python scripts/make_charts.py   # charts -> charts/
python scripts/ab_test.py       # Welch t-test
streamlit run dashboard/app.py  # interactive dashboard
```

## Repository structure
```
data/      raw CSVs + olist.duckdb (excluded from git — see README)
sql/       01 funnel, 02 active users, 03 cohort retention, 04 churn,
           05 revenue/LTV, 06 segments, 07 delivery vs reviews, 08 A/B test
scripts/   build_db, run_sql, make_charts, ab_test
charts/    generated charts + dashboard screenshot
dashboard/ Streamlit app
results/   CSV outputs of each query
```
