import duckdb
import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"), read_only=True)

st.set_page_config(page_title="Olist Product Analytics", layout="wide")
st.title("Olist E-Commerce — Product Analytics Dashboard")

kpi = con.execute("""
SELECT COUNT(DISTINCT o.order_id) AS orders,
       COUNT(DISTINCT c.customer_unique_id) AS customers,
       ROUND(SUM(p.payment_value),0) AS revenue,
       ROUND(AVG(p.payment_value),2) AS aov
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN payments p ON p.order_id = o.order_id
""").fetchdf().iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders", f"{kpi.orders:,}")
c2.metric("Customers", f"{kpi.customers:,}")
c3.metric("Revenue", f"R$ {kpi.revenue:,.0f}")
c4.metric("Avg payment", f"R$ {kpi.aov:,.2f}")

st.subheader("MAU & orders over time")
mau = con.execute("""
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
       COUNT(DISTINCT c.customer_unique_id) AS mau,
       COUNT(DISTINCT o.order_id) AS orders
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY 1 ORDER BY 1
""").fetchdf().set_index("month")
st.line_chart(mau)

st.subheader("Top states by revenue")
states = con.execute("""
SELECT c.customer_state AS state, ROUND(SUM(p.payment_value),0) AS revenue
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
JOIN payments p ON p.order_id = o.order_id
GROUP BY 1 ORDER BY revenue DESC LIMIT 10
""").fetchdf().set_index("state")
st.bar_chart(states)

st.subheader("Top categories")
cat = con.execute("""
SELECT COALESCE(t.product_category_name_english, pr.product_category_name, 'unknown') AS category,
       ROUND(SUM(p.payment_value),0) AS revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products pr ON pr.product_id = oi.product_id
LEFT JOIN category_translation t ON t.product_category_name = pr.product_category_name
JOIN payments p ON p.order_id = o.order_id
GROUP BY 1 ORDER BY revenue DESC LIMIT 10
""").fetchdf().set_index("category")
st.bar_chart(cat)

st.subheader("Review score by delivery performance")
dl = con.execute("""
SELECT CASE WHEN DATE_DIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP),
                           o.order_delivered_customer_date) > 0
            THEN 'late' ELSE 'on_time_or_early' END AS delivery,
       ROUND(AVG(r.review_score),2) AS avg_review
FROM orders o JOIN reviews r ON r.order_id = o.order_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1
""").fetchdf().set_index("delivery")
st.bar_chart(dl)

st.subheader("Raw cohort retention (first 50 rows)")
sql3 = "\n".join(l for l in (ROOT / "sql" / "03_cohort_retention.sql").read_text().splitlines() if not l.strip().startswith("--"))
st.dataframe(con.execute(sql3).fetchdf().head(50))
