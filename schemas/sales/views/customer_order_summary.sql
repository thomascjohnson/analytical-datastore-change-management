CREATE VIEW sales.customer_order_summary AS
SELECT 
    c.id,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    MAX(o.order_date) AS last_order_date
FROM 
    @@sales.customer@@ c
LEFT JOIN 
    @@sales.order@@ o ON c.customer_id = o.id
GROUP BY 
    c.id, c.first_name, c.last_name, c.email
ORDER BY total_orders DESC;