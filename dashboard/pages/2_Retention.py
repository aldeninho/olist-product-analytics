import streamlit as st
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from _db import get_con
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

con = get_con()
st.set_page_config(page_title="Retention", layout="wide")
st.title("Retention & Cohorts")

st.subheader("All-time repeat-purchase rate")
rep = con.execute("""
WITH cs AS (SELECT c.customer_unique_id, COUNT(DISTINCT o.order_id) AS orders
            FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY 1)
SELECT ROUND(100.0*SUM(orders>1)/COUNT(*),1) AS repeat_pct,
       COUNT(*) AS customers FROM cs
""").fetchdf().iloc[0]
st.metric("Repeat rate", f"{rep.repeat_pct}%", delta=f"{rep.customers:,} customers")

st.subheader("Cohort retention heatmap (% of cohort active N months later)")
sql3 = "\n".join(l for l in (pathlib.Path(__file__).resolve().parents[2]/"sql"/"03_cohort_retention.sql").read_text().splitlines() if not l.strip().startswith("--"))
ret = con.execute(sql3).fetchdf()
piv = ret.pivot_table(index="cohort_month", columns="months_since", values="retention_pct", aggfunc="mean")
fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(piv, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_title("Retention %")
st.pyplot(fig)

st.subheader("Month-over-month retention rate")
sql4 = "\n".join(l for l in (pathlib.Path(__file__).resolve().parents[2]/"sql"/"04_churn.sql").read_text().splitlines() if not l.strip().startswith("--"))
ch = con.execute(sql4).fetchdf()
st.line_chart(ch.set_index("base_month")[["retention_pct", "churn_pct"]])
