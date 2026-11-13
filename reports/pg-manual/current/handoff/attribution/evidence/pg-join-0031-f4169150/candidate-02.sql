WITH _dsv_t1(a,b,c) AS (SELECT * FROM J1_TBL), _dsv_t2(d,e) AS (SELECT * FROM J2_TBL) SELECT t1.a,t2.e FROM _dsv_t1 t1 CROSS JOIN _dsv_t2 t2 WHERE t1.a=t2.d;
