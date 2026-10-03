import streamlit as st
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _db import get_con

con = get_con()
st.set_page_config(page_title="Executive", layout="wide")
st.title("Executive Overview")

kpi = con.execute("""
SELECT COUNT(DISTINCT o.order_id) AS orders,
       COUNT(DISTINCT c.customer_unique_id) AS customers,
       ROUND(SUM(p.payment_value),0) AS revenue,
       ROUND(SUM(p.payment_value)/COUNT(DISTINCT o.order_id),2) AS aov
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN payments p ON p.order_id = o.order_id
""").fetchdf().iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Orders", f"{kpi.orders:,}")
c2.metric("Customers", f"{kpi.customers:,}")
c3.metric("Revenue", f"R$ {kpi.revenue:,.0f}")
c4.metric("AOV (per order)", f"R$ {kpi.aov:,.2f}")

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
