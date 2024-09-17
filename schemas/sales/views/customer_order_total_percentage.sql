CREATE OR REPLACE VIEW sales.customer_order_total_percentage AS
SELECT 
    order.id,
    customer_name,
    order.total_amount,
    total_spent,
    100 * order.total_amount / total_spent AS order_total_percentage
FROM @@sales.customer_order_summary@@
JOIN @@sales.order@@
    ON customer_order_summary.order_id = order.id;