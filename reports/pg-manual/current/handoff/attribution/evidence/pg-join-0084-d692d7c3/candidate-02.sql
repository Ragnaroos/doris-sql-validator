SELECT COALESCE(s2.name,s3.name) AS name,s2.s2_n,s2.s2_2,s3.s3_n,s3.s3_2 FROM (SELECT name,n AS s2_n,2 AS s2_2 FROM t2) s2 FULL JOIN (SELECT name,n AS s3_n,3 AS s3_2 FROM t3) s3 ON s2.name=s3.name;
