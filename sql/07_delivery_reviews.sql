-- 07. Delivery performance: late vs on-time delivery and its effect on review score
WITH delivery AS (
    SELECT o.order_id,
           r.review_score,
           DATE_DIFF('day', CAST(o.order_estimated_delivery_date AS TIMESTAMP), o.order_delivered_customer_date) AS days_early_vs_estimate
    FROM orders o
    JOIN reviews r ON r.order_id = o.order_id
    WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
)
SELECT
    CASE WHEN days_early_vs_estimate > 0 THEN 'late' ELSE 'on_time_or_early' END AS delivery,
    COUNT(*) AS orders,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM delivery
GROUP BY 1;
