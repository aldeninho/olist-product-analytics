"""A/B-style test: does on-time vs late delivery change review scores?
Two-sample Welch t-test."""
import duckdb
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"))
df = con.execute("""
SELECT r.review_score,
       CASE WHEN DATE_DIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP),
                           o.order_delivered_customer_date) > 0
            THEN 'late' ELSE 'on_time' END AS grp
FROM orders o
JOIN reviews r ON r.order_id = o.order_id
WHERE o.order_status='delivered' AND o.order_delivered_customer_date IS NOT NULL
""").fetchdf()

on_time = df.loc[df.grp == "on_time", "review_score"]
late = df.loc[df.grp == "late", "review_score"]
t, p = stats.ttest_ind(on_time, late, equal_var=False)
print(f"on-time mean={on_time.mean():.3f} (n={len(on_time):,})")
print(f"late     mean={late.mean():.3f} (n={len(late):,})")
print(f"Welch t={t:.2f}, p-value={p:.2e}")
print("Conclusion: late delivery SIGNIFICANTLY lowers review scores." if p < 0.05 else "No significant difference.")
