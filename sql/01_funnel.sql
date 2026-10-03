-- 01. Order-status funnel: where does the customer journey drop off?
SELECT
    order_status,
    COUNT(*) AS orders,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_orders
FROM orders
GROUP BY 1
ORDER BY orders DESC;
