-- 08. Experimentation case: does delivery delay cause lower review scores?
-- (two-sample t-test in Python; this SQL sets up the groups)
SELECT
    CASE WHEN DATE_DIFF('day', CAST(order_estimated_delivery_date AS TIMESTAMP), order_delivered_customer_date) > 0
         THEN 'late' ELSE 'on_time' END AS group_delivery,
    COUNT(*) AS n,
    ROUND(AVG(r.review_score), 3) AS mean_score,
    ROUND(STDDEV(r.review_score), 3) AS std_score
FROM orders o
JOIN reviews r ON r.order_id = o.order_id
WHERE o.order_status = 'delivered' AND o.order_delivered_customer_date IS NOT NULL
GROUP BY 1;
