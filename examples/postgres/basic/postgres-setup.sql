-- Run with psql connected to an administrative database.
-- This deliberately fails if dsv_demo already exists; it never drops data.
CREATE DATABASE dsv_demo;
\connect dsv_demo

CREATE TABLE validation_demo_items (
    id INTEGER NOT NULL,
    category VARCHAR(16) NOT NULL,
    amount INTEGER
);

INSERT INTO validation_demo_items (id, category, amount) VALUES
    (1, 'a', 10),
    (2, 'a', 20),
    (2, 'a', 20),
    (3, 'b', 0),
    (4, 'b', NULL);
