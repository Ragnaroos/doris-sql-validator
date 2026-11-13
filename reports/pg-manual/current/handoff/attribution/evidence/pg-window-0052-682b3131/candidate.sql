SELECT SUM(unique1) OVER (ORDER BY four NULLS LAST range BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10;
