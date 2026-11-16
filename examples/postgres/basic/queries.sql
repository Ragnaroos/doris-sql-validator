SELECT 1 AS value;

SELECT id, amount
FROM validation_demo_items
WHERE id <= 3
ORDER BY id, amount;

SELECT amount
FROM validation_demo_items
WHERE category = 'a';

SELECT category, COUNT(*) AS row_count, COUNT(amount) AS non_null_count
FROM validation_demo_items
GROUP BY category
ORDER BY category;
