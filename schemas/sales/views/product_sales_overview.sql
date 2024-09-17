CREATE VIEW sales.product_sales_overview AS
SELECT 
    p.id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS total_quantity_sold,
    SUM(o.total_amount) AS total_sales_amount,
    p.stock_quantity AS current_stock
FROM 
    @@sales.product@@ p
LEFT JOIN 
    @@sales.order@@ o ON p.product_id = o.product_id
GROUP BY 
    p.product_id, p.product_name, p.category, p.stock_quantity;