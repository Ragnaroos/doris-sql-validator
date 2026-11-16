-- Run with a MySQL-compatible client connected to Doris FE.
-- This deliberately fails if dsv_demo already exists; it never drops data.
CREATE DATABASE dsv_demo;
USE dsv_demo;

CREATE TABLE validation_demo_items (
    id INT NOT NULL,
    category VARCHAR(16) NOT NULL,
    amount INT NULL
)
DUPLICATE KEY(id)
DISTRIBUTED BY HASH(id) BUCKETS 1
PROPERTIES ("replication_num" = "1");

INSERT INTO validation_demo_items (id, category, amount) VALUES
    (1, 'a', 10),
    (2, 'a', 20),
    (2, 'a', 20),
    (3, 'b', 0),
    (4, 'b', NULL);
