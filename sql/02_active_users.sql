-- 02. Engagement: DAU / WAU / MAU of ordering customers
-- MAU: unique customers placing >=1 order per month
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month,
    COUNT(DISTINCT c.customer_unique_id) AS mau
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
GROUP BY 1
ORDER BY 1;
