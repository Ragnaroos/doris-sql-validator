CREATE TABLE J1_TBL (
  i integer,
  j integer,
  t text
);

CREATE TABLE J2_TBL (
  i integer,
  k integer
);

INSERT INTO J1_TBL VALUES (1, 4, 'one');

INSERT INTO J1_TBL VALUES (2, 3, 'two');

INSERT INTO J1_TBL VALUES (3, 2, 'three');

INSERT INTO J1_TBL VALUES (4, 1, 'four');

INSERT INTO J1_TBL VALUES (5, 0, 'five');

INSERT INTO J1_TBL VALUES (6, 6, 'six');

INSERT INTO J1_TBL VALUES (7, 7, 'seven');

INSERT INTO J1_TBL VALUES (8, 8, 'eight');

INSERT INTO J1_TBL VALUES (0, NULL, 'zero');

INSERT INTO J1_TBL VALUES (NULL, NULL, 'null');

INSERT INTO J1_TBL VALUES (NULL, 0, 'zero');

INSERT INTO J2_TBL VALUES (1, -1);

INSERT INTO J2_TBL VALUES (2, 2);

INSERT INTO J2_TBL VALUES (3, -3);

INSERT INTO J2_TBL VALUES (2, 4);

INSERT INTO J2_TBL VALUES (5, -5);

INSERT INTO J2_TBL VALUES (5, -5);

INSERT INTO J2_TBL VALUES (0, NULL);

INSERT INTO J2_TBL VALUES (NULL, NULL);

INSERT INTO J2_TBL VALUES (NULL, 0);

CREATE TABLE t1 (name TEXT, n INTEGER);

CREATE TABLE t2 (name TEXT, n INTEGER);

CREATE TABLE t3 (name TEXT, n INTEGER);

INSERT INTO t1 VALUES ( 'bb', 11 );

INSERT INTO t2 VALUES ( 'bb', 12 );

INSERT INTO t2 VALUES ( 'cc', 22 );

INSERT INTO t2 VALUES ( 'ee', 42 );

INSERT INTO t3 VALUES ( 'bb', 13 );

INSERT INTO t3 VALUES ( 'cc', 23 );

INSERT INTO t3 VALUES ( 'dd', 33 );

create table x (x1 int, x2 int);

insert into x values (1,11);

insert into x values (2,22);

insert into x values (3,null);

insert into x values (4,44);

insert into x values (5,null);

create table y (y1 int, y2 int);

insert into y values (1,111);

insert into y values (2,222);

insert into y values (3,333);

insert into y values (4,null);

CREATE TABLE empsalary (
    depname varchar,
    empno bigint,
    salary int,
    enroll_date date
);

INSERT INTO empsalary VALUES
('develop', 10, 5200, '2007-08-01'),
('sales', 1, 5000, '2006-10-01'),
('personnel', 5, 3500, '2007-12-10'),
('sales', 4, 4800, '2007-08-08'),
('personnel', 2, 3900, '2006-12-23'),
('develop', 7, 4200, '2008-01-01'),
('develop', 9, 4500, '2008-01-01'),
('sales', 3, 4800, '2007-08-01'),
('develop', 8, 6000, '2006-10-01'),
('develop', 11, 5200, '2007-08-15');

CREATE TABLE SUBSELECT_TBL (
  f1 integer,
  f2 integer,
  f3 float
);

INSERT INTO SUBSELECT_TBL VALUES (1, 2, 3);

INSERT INTO SUBSELECT_TBL VALUES (2, 3, 4);

INSERT INTO SUBSELECT_TBL VALUES (3, 4, 5);

INSERT INTO SUBSELECT_TBL VALUES (1, 1, 1);

INSERT INTO SUBSELECT_TBL VALUES (2, 2, 2);

INSERT INTO SUBSELECT_TBL VALUES (3, 3, 3);

INSERT INTO SUBSELECT_TBL VALUES (6, 7, 8);

INSERT INTO SUBSELECT_TBL VALUES (8, 9, NULL);

CREATE TABLE foo (id integer);

CREATE TABLE bar (id1 integer, id2 integer);

INSERT INTO foo VALUES (1);

INSERT INTO bar VALUES (1, 1);

INSERT INTO bar VALUES (2, 2);

INSERT INTO bar VALUES (3, 1);

CREATE TABLE department (
	id INTEGER PRIMARY KEY,  -- department ID
	parent_department INTEGER REFERENCES department, -- upper department ID
	name TEXT -- department name
);

INSERT INTO department VALUES (0, NULL, 'ROOT');

INSERT INTO department VALUES (1, 0, 'A');

INSERT INTO department VALUES (2, 1, 'B');

INSERT INTO department VALUES (3, 2, 'C');

INSERT INTO department VALUES (4, 2, 'D');

INSERT INTO department VALUES (5, 0, 'E');

INSERT INTO department VALUES (6, 4, 'F');

INSERT INTO department VALUES (7, 5, 'G');

CREATE TABLE INT2_TBL(f1 int2);

INSERT INTO INT2_TBL(f1) VALUES
  ('0   '),
  ('  1234 '),
  ('    -1234'),
  ('32767'),  -- largest and smallest values
  ('-32767');

CREATE TABLE INT4_TBL(f1 int4);

INSERT INTO INT4_TBL(f1) VALUES
  ('   0  '),
  ('123456     '),
  ('    -123456'),
  ('2147483647'),  -- largest and smallest values
  ('-2147483647');

CREATE TABLE INT8_TBL(q1 int8, q2 int8);

INSERT INTO INT8_TBL VALUES
  ('  123   ','  456'),
  ('123   ','4567890123456789'),
  ('4567890123456789','123'),
  (+4567890123456789,'4567890123456789'),
  ('+4567890123456789','-4567890123456789');

CREATE TABLE TEXT_TBL (f1 text);

INSERT INTO TEXT_TBL VALUES
  ('doh!'),
  ('hi de ho neighbor');

CREATE TABLE onek (
	unique1		int4,
	unique2		int4,
	two			int4,
	four		int4,
	ten			int4,
	twenty		int4,
	hundred		int4,
	thousand	int4,
	twothousand	int4,
	fivethous	int4,
	tenthous	int4,
	odd			int4,
	even		int4,
	stringu1	name,
	stringu2	name,
	string4		name
);

CREATE TABLE tenk1 (
	unique1		int4,
	unique2		int4,
	two			int4,
	four		int4,
	ten			int4,
	twenty		int4,
	hundred		int4,
	thousand	int4,
	twothousand	int4,
	fivethous	int4,
	tenthous	int4,
	odd			int4,
	even		int4,
	stringu1	name,
	stringu2	name,
	string4		name
);

CREATE TABLE aggtest (
	a 			int2,
	b			float4
);

create view gstest1(a,b,v)
  as values (1,1,10),(1,1,11),(1,2,12),(1,2,13),(1,3,14),
            (2,3,15),
            (3,3,16),(3,4,17),
            (4,1,18),(4,1,19);

create table gstest_empty (a integer, b integer, v integer);
