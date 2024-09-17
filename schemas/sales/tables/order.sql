CREATE TABLE sales.order (
    id SERIAL PRIMARY KEY,
    customer_id INT,
    product_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    quantity INT,
    total_amount DECIMAL(10, 2),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES sales.customer(id),
    FOREIGN KEY (product_id) REFERENCES sales.product(id)
);