-- 03. Cohort retention: % of customers who return each month after first purchase
WITH first_purchase AS (
    SELECT c.customer_unique_id,
           DATE_TRUNC('month', MIN(o.order_purchase_timestamp)) AS cohort_month
    FROM orders o JOIN customers c ON c.customer_id = o.customer_id
    GROUP BY 1
),
activity AS (
    SELECT DISTINCT c.customer_unique_id,
           DATE_TRUNC('month', o.order_purchase_timestamp) AS active_month
    FROM orders o JOIN customers c ON c.customer_id = o.customer_id
),
cohorts AS (
    SELECT f.cohort_month,
           COUNT(DISTINCT f.customer_unique_id) AS cohort_size,
           a.active_month,
           COUNT(DISTINCT a.customer_unique_id) AS active,
           (EXTRACT(YEAR FROM a.active_month) - EXTRACT(YEAR FROM f.cohort_month)) * 12
             + (EXTRACT(MONTH FROM a.active_month) - EXTRACT(MONTH FROM f.cohort_month)) AS months_since
    FROM first_purchase f
    JOIN activity a ON a.customer_unique_id = f.customer_unique_id
    GROUP BY 1, 3
)
SELECT cohort_month, cohort_size, months_since, active,
       ROUND(100.0 * active / cohort_size, 1) AS retention_pct
FROM cohorts
WHERE months_since BETWEEN 0 AND 5
ORDER BY 1, 3;
