-- 04. Month-over-month customer churn (distinct from all-time repeat rate)
-- Of customers active in month m, what share does NOT purchase again in m+1?
WITH monthly AS (
    SELECT DISTINCT c.customer_unique_id,
           DATE_TRUNC('month', o.order_purchase_timestamp) AS month
    FROM orders o JOIN customers c ON c.customer_id = o.customer_id
),
comeback AS (
    SELECT m1.month AS base_month,
           CASE WHEN m2.customer_unique_id IS NOT NULL THEN 1 ELSE 0 END AS retained
    FROM monthly m1
    LEFT JOIN monthly m2
      ON m2.customer_unique_id = m1.customer_unique_id
     AND m2.month = m1.month + INTERVAL '1 month'
)
SELECT base_month,
       COUNT(*) AS active_base_month,
       SUM(retained) AS retained_next_month,
       ROUND(100.0 * SUM(retained) / COUNT(*), 1) AS retention_pct,
       ROUND(100.0 * (1 - SUM(retained) * 1.0 / COUNT(*)), 1) AS churn_pct
FROM comeback
GROUP BY 1
ORDER BY 1;
