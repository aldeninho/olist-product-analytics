"""Generate all charts from the DuckDB database into charts/."""
from pathlib import Path
import duckdb
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"))
CH = ROOT / "charts"
CH.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid")

# 1. Order status funnel
df = con.execute(open(ROOT / "sql" / "01_funnel.sql").read().split("--")[1]).fetchdf() if False else None
df = con.execute("""
SELECT order_status, COUNT(*) AS orders FROM orders GROUP BY 1 ORDER BY orders DESC
""").fetchdf()
plt.figure(figsize=(9, 5))
sns.barplot(data=df, x="orders", y="order_status", color="steelblue")
plt.title("Orders by status (order journey funnel)")
plt.tight_layout(); plt.savefig(CH / "01_funnel.png", dpi=130); plt.close()

# 2. MAU over time
mau = con.execute("""
SELECT DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
       COUNT(DISTINCT c.customer_unique_id) AS mau,
       COUNT(DISTINCT o.order_id) AS orders
FROM orders o JOIN customers c ON c.customer_id = o.customer_id
GROUP BY 1 ORDER BY 1
""").fetchdf()
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(mau["month"], mau["mau"], marker="o", label="MAU")
ax1.set_ylabel("Active customers (MAU)")
ax2 = ax1.twinx()
ax2.plot(mau["month"], mau["orders"], marker="s", color="orange", label="Orders")
ax2.set_ylabel("Orders"); fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.9))
plt.title("Active customers & orders over time"); plt.tight_layout()
plt.savefig(CH / "02_mau_orders.png", dpi=130); plt.close()

# 3. Cohort retention heatmap
sql3 = "\n".join(l for l in open(ROOT / "sql" / "03_cohort_retention.sql").read().splitlines() if not l.strip().startswith("--"))
ret = con.execute(sql3).fetchdf()
piv = ret.pivot_table(index="cohort_month", columns="months_since", values="retention_pct", aggfunc="mean")
plt.figure(figsize=(9, 8))
sns.heatmap(piv, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={"label": "Retention %"})
plt.title("Cohort retention: % of customers still ordering N months later")
plt.tight_layout(); plt.savefig(CH / "03_cohort_heatmap.png", dpi=130); plt.close()

# 4. Monthly churn
sql4 = "\n".join(l for l in open(ROOT / "sql" / "04_churn.sql").read().splitlines() if not l.strip().startswith("--"))
ch = con.execute(sql4).fetchdf()
plt.figure(figsize=(10, 5))
sns.lineplot(data=ch, x="base_month", y="churn_pct", marker="o", color="firebrick")
plt.ylim(85, 100); plt.title("Monthly customer churn %"); plt.tight_layout()
plt.savefig(CH / "04_churn.png", dpi=130); plt.close()

# 5. Review score by delivery timeliness
sql7 = "\n".join(l for l in open(ROOT / "sql" / "07_delivery_reviews.sql").read().splitlines() if not l.strip().startswith("--"))
dl = con.execute(sql7).fetchdf()
plt.figure(figsize=(7, 5))
sns.barplot(data=dl, x="delivery", y="avg_review_score", color="seagreen")
plt.ylim(0, 5); plt.title("Average review score: late vs on-time delivery"); plt.tight_layout()
plt.savefig(CH / "05_delivery_review.png", dpi=130); plt.close()

# 6. Top categories by revenue
# Separate three metrics that are easy to conflate:
# - All-time repeat rate: % of customers with >= 2 orders ever (~3.1%)
# - Month-over-month retention: % of customers active in month m who buy again in m+1 (very low)
# - Long-term repeat behaviour: % of customers with no second purchase ever (~97%)
cat = con.execute("""
SELECT COALESCE(t.product_category_name_english, pr.product_category_name, 'unknown') AS category,
       SUM(oi.price + oi.freight_value) AS revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products pr ON pr.product_id = oi.product_id
LEFT JOIN category_translation t ON t.product_category_name = pr.product_category_name
GROUP BY 1 ORDER BY revenue DESC LIMIT 10
""").fetchdf()
plt.figure(figsize=(10, 6))
sns.barplot(data=cat, x="revenue", y="category", color="darkorange")
plt.title("Top 10 categories by revenue"); plt.tight_layout()
plt.savefig(CH / "06_top_categories.png", dpi=130); plt.close()

print("charts written to", CH)
