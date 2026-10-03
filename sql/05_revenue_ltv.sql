-- 05. Revenue: AOV, revenue per customer (LTV proxy), repeat purchase rate
WITH customer_spend AS (
    SELECT c.customer_unique_id,
           COUNT(DISTINCT o.order_id) AS orders,
           SUM(p.payment_value) AS total_spend
    FROM orders o
    JOIN customers c ON c.customer_id = o.customer_id
    JOIN payments p ON p.order_id = o.order_id
    GROUP BY 1
)
SELECT
    COUNT(*) AS customers,
    ROUND(AVG(orders), 2) AS avg_orders_per_customer,
    ROUND(SUM(orders > 1) * 100.0 / COUNT(*), 1) AS repeat_customer_pct,
    ROUND(AVG(total_spend), 2) AS avg_revenue_per_customer,
    ROUND(AVG(total_spend / orders), 2) AS avg_order_value,
    (SELECT ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) FROM payments) AS overall_aov,
    ROUND(SUM(total_spend), 2) AS total_revenue
FROM customer_spend;
