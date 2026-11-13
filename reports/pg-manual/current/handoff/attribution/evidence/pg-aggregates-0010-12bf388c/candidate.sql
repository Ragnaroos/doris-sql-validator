SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v;
