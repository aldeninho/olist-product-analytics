"""Observational group comparison: does delivery timeliness differ with review scores?
Outputs: sample sizes, means, median, Welch t-test, 95% CI for mean difference, Cohen's d."""
import duckdb
import numpy as np
from pathlib import Path
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
con = duckdb.connect(str(ROOT / "data" / "olist.duckdb"), read_only=True)
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

n1, n2 = len(on_time), len(late)
m1, m2 = on_time.mean(), late.mean()
s1, s2 = on_time.std(ddof=1), late.std(ddof=1)
t, p = stats.ttest_ind(on_time, late, equal_var=False)
d = (m1 - m2) / np.sqrt((s1**2 + s2**2) / 2)                      # Cohen's d
se = np.sqrt(s1**2 / n1 + s2**2 / n2)                               # SE of diff
mean_diff = m1 - m2
ci = (mean_diff - 1.96 * se, mean_diff + 1.96 * se)

print(f"on-time: n={n1:,}  mean={m1:.3f}  median={on_time.median():.0f}  sd={s1:.3f}")
print(f"late:    n={n2:,}  mean={m2:.3f}  median={late.median():.0f}  sd={s2:.3f}")
print(f"mean difference (on-time - late): {mean_diff:.3f} points")
print(f"95% CI for difference: [{ci[0]:.3f}, {ci[1]:.3f}]")
print(f"Cohen's d: {d:.3f}  (|d| > 0.8 = large effect)")
print(f"Welch t={t:.2f}, p={p:.2e}")
print("Note: observational, not randomized; late delivery may proxy for problem segments.")
