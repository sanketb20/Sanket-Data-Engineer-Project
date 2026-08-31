CREATE TABLE IF NOT EXISTS shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    shipment_date DATE,
    origin VARCHAR(100),
    destination VARCHAR(100),
    status VARCHAR(50),
    weight_kg NUMERIC(10, 2),
    shipping_cost NUMERIC(12, 2),
    carrier VARCHAR(100),
    delivery_date DATE,
    priority VARCHAR(30),
    warehouse_id VARCHAR(50),
    service_type VARCHAR(50)
);