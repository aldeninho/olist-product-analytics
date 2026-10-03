-- 08. Observational group comparison: on-time vs late delivery -> review score
-- NOTE: observational analysis, not a randomized A/B test.
SELECT
    CASE WHEN DATE_DIFF('day', CAST(order_estimated_delivery_date AS TIMESTAMP), order_delivered_customer_date) > 0
         THEN 'late' ELSE 'on_time' END AS delivery_group,
    COUNT(*) AS n,
    ROUND(AVG(r.review_score), 3) AS mean_score,
    ROUND(MEDIAN(r.review_score), 1) AS median_score,
    ROUND(STDDEV(r.review_score), 3) AS std_score
FROM orders o
JOIN reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1;
