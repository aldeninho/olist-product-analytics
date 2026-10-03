-- 06. Segments: revenue & ARPU by state (top 10) and by product category (top 10)
-- 6a. By state
SELECT c.customer_state AS state,
       COUNT(DISTINCT c.customer_unique_id) AS customers,
       ROUND(SUM(p.payment_value), 0) AS revenue,
       ROUND(AVG(p.payment_value), 2) AS avg_payment_value
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN payments p ON p.order_id = o.order_id
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;

-- 6b. By category
SELECT COALESCE(t.product_category_name_english, pr.product_category_name, 'unknown') AS category,
       COUNT(DISTINCT o.order_id) AS orders,
       ROUND(SUM(p.payment_value), 0) AS revenue
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN products pr ON pr.product_id = oi.product_id
LEFT JOIN category_translation t ON t.product_category_name = pr.product_category_name
JOIN payments p ON p.order_id = o.order_id
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;
