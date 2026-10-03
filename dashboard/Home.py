import streamlit as st

st.set_page_config(page_title="Olist Product Analytics", layout="wide")

st.title("Olist — Customer & Product Analytics")
st.subheader("Retention, funnel, and revenue dynamics on ~100k real orders")

st.markdown("""
This dashboard summarizes a full product-analytics case study. Navigate the pages on the left:

- **1 · Executive** — headline KPIs, revenue & active-customer trends, top segments
- **2 · Retention** — cohort heatmap, month-over-month retention, repeat-purchase rate
- **3 · Operations** — delivery performance, review scores, category economics

**Data grain:** `orders` = 1 row/order · `order_items` = 1 row/item · `payments` = 1 row/payment · `customers` = 1 row/customer. Category revenue is computed at item grain to avoid join fan-out.
""")

st.info("Run: `streamlit run dashboard/Home.py` from the repo root.")
