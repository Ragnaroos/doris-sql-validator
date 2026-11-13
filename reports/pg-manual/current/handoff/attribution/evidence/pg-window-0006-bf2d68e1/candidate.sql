SELECT depname, empno, salary, SUM(salary) OVER (PARTITION BY depname) FROM empsalary;
