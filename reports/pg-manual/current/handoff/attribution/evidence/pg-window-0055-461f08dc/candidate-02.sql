SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 2 following), unique1, four FROM tenk1 WHERE unique1 < 10;
