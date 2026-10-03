import streamlit as st
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _db import get_con

con = get_con()
st.set_page_config(page_title="Operations", layout="wide")
st.title("Operations — Delivery & Customer Satisfaction")

st.subheader("Average review score by delivery timeliness")
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

st.subheader("Late-delivery rate by state (top 10)")
late = con.execute("""
SELECT c.customer_state AS state,
       ROUND(100.0*AVG(CASE WHEN DATE_DIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP),
                          o.order_delivered_customer_date) > 0 THEN 1 ELSE 0 END),1) AS late_pct
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1 ORDER BY late_pct DESC LIMIT 10
""").fetchdf().set_index("state")
st.bar_chart(late)

st.subheader("Top 10 categories by revenue (item grain)")
cat = con.execute("""
SELECT COALESCE(t.product_category_name_english, pr.product_category_name, 'unknown') AS category,
       ROUND(SUM(oi.price + oi.freight_value),0) AS revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products pr ON pr.product_id = oi.product_id
LEFT JOIN category_translation t ON t.product_category_name = pr.product_category_name
GROUP BY 1 ORDER BY revenue DESC LIMIT 10
""").fetchdf().set_index("category")
st.bar_chart(cat)
