SELECT ten, two, SUM(hundred) AS gsum, SUM(SUM(hundred)) OVER (PARTITION BY two ORDER BY ten NULLS LAST) AS wsum FROM tenk1 GROUP BY ten, two;
