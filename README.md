# Olist E-Commerce — Product Analytics Case Study

## Business question
**How healthy is the Olist customer base, and where is revenue/retention leaking?**

## Dataset
Real, public data from **Olist** (Brazilian e-commerce marketplace, 2016–2018), ~100k orders,
mirrored at `github.com/olist/work-at-olist-data`. Loaded into DuckDB (`data/olist.duckdb`).

## Tech stack
- **SQL** (DuckDB) for analysis — `sql/01–08`
- **Python** (pandas, scipy, matplotlib, seaborn) — `scripts/`
- **Streamlit** dashboard — `dashboard/app.py`

## How to run
```bash
pip install -r requirements.txt
python scripts/build_db.py      # load CSVs into DuckDB
python scripts/run_sql.py       # run all SQL analyses -> results/
python scripts/make_charts.py   # charts -> charts/
python scripts/ab_test.py       # Welch t-test on delivery impact
streamlit run dashboard/app.py  # interactive dashboard
```

## Key findings
1. **Retention is near-zero**: ~99.5% of customers never buy again (avg 1.03 orders/customer, 3.1% repeat). Biggest business opportunity = repeat purchase programs.
2. **Late delivery destroys satisfaction**: on-time orders average **4.29/5** reviews vs **2.27/5** for late orders. Welch t-test: t ≈ 101, p << 0.001.
3. **Geographic concentration**: São Paulo alone contributes ~R$6M of R$16M revenue.
4. **Top categories**: bed/bath, health & beauty, computers accessories lead revenue.

## Recommendations
- Invest in delivery SLA; the late-delivery segment (~7% of orders) drags ratings sharply.
- Build a repeat-purchase/loyalty program — current retention is ~0.5% month over month.
- Expand logistics into RJ/MG where customer count is high but revenue per customer trails SP.

## Repo structure
```
data/      CSVs + olist.duckdb
sql/       01 funnel, 02 active users, 03 cohort retention, 04 churn,
           05 revenue/LTV, 06 segments, 07 delivery vs reviews, 08 A/B test
scripts/   build_db, run_sql, make_charts, ab_test
charts/    generated charts
dashboard/ Streamlit app
results/   CSV outputs of each query
```
