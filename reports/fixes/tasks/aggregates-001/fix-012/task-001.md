# task-001：保留 PostgreSQL 数组构造的有限源元素类型（fix-012）

## 1. 结论与范围

状态：**已修改但未完成验收**。这轮有实际代码修改，不是再次只补查类型：整数和标量子查询整数默认保留 INT/BIGINT，全 unknown/NULL 与纯字符串保留 TEXT；显式受支持类型及矩形嵌套数组也保留共同元素类型。

上一轮18条边界中，7条默认元素类型差异全部修正，另外原0010的 text[] / ARRAY<VARCHAR(5)> 改为 text[] / ARRAY<TEXT>。18条当前值全部一致，其中16条本次取得的全部字段类型/约束可对齐；另1条独立 id 位宽不同、1条Decimal结果约束未验收。不能据此把整个 task 或完整 aggregates.sql 标为完成。

本轮仅继续 [task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，前轮为 [fix-011](../fix-011/task-001.md)。不修 task-003、通用 VALUES/CASE/SUM 类型、数组索引、时间精度、UDF、WITHIN GROUP、VARIADIC 或验证器。共同身份与回归统计见[本轮汇总](../../../aggregates-001-fix-012-summary.md)。

## 2. 修改依据与实际实现

修复前小整数 ARRAY(1,NULL,2) 被 Doris 推成 ARRAY<TINYINT>，全 NULL 为 ARRAY<NULL_TYPE>，纯字符串可能为 ARRAY<VARCHAR(n)>；PG分别是 int4[]、text[]、text[]。前轮独立 CAST 对照已证明部分目标类型可表达，但统一 INT 会把2147483648变成NULL，不能采用。

| 实际文件/函数 | 本轮职责 | 边界 |
| :--- | :--- | :--- |
| [expressions/array.py](../../../../../../sqlglot-experiment/sqlglot/expressions/array.py) / Array.element_type | 在公共 AST 保存可确定的源元素类型；可 dump/load | 不把类型当额外数组元素 |
| [parsers/postgres.py](../../../../../../sqlglot-experiment/sqlglot/parsers/postgres.py) / _array_element_type、_parse_bracket | 按源语句的有限共同类型规则标注数组 | 整数字面量按32/64位范围；字符串/NULL的unknown只在无已知类型时默认TEXT；支持同类有限数值、BOOL、TEXT显式CAST、嵌套及单列标量子查询；未知列/参数/Decimal不猜 |
| [generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py) / array_sql | 对有 element_type 的数组生成整体 CAST；清除副本中的提示以避免递归，copy=False 不改源 AST | 默认转译就受益，不传Schema、不向验证器注入改写；无可信提示仍保留原路径 |
| [generator.py](../../../../../../sqlglot-experiment/sqlglot/generator.py) / array_sql | 公共默认 ARRAY 生成只取 expressions | 初次测试发现Hive/Spark的通用函数回退把DataType当额外元素；此方法修正新增字段的跨方言泄漏，不修改其他源方言的类型选择 |
| tests/dialects/test_doris.py、test_postgres.py | 更新实际输出；增加类型边界、未知类型拒绝猜测、非PG不加提示、AST序列化/往返与不变性测试 | 无表名、Case答案或固定NULL返回值特判 |

NULL只参与类型分析，输出中仍由SQL运行时计算NULL；没有在Python返回固定查询答案。为识别unknown叶子的类型使用既有 annotate_types 的 COALESCE 类型路径；不以通用推断的DOUBLE结果替代PG NUMERIC。全部源字段未知时不拿另一个参数的INT猜列类型。

[PG官方共同类型规则](https://www.postgresql.org/docs/18/typeconv-union-case.html)是范围依据；本实现只是其可证明的有限子集，不是完整PG类型解析器。混合unknown字符串与非TEXT已知类型保留未实现，因为PG输入函数不普遍等于Doris CAST（例如布尔拼写/数字格式）。

实际例子：

~~~sql
-- 源
SELECT ARRAY[1,NULL,2] AS xs;
-- 修复前
SELECT ARRAY(1, NULL, 2) AS xs;
-- 修复后默认生成
SELECT CAST(ARRAY(1, NULL, 2) AS ARRAY<INT>) AS xs;

-- 源 ARRAY[2147483648,1,NULL]：选择 BIGINT，而不是 INT
SELECT CAST(ARRAY(2147483648, 1, NULL) AS ARRAY<BIGINT>) AS xs;
-- 源 ARRAY[NULL]：保留源默认 TEXT，不折叠为NULL答案
SELECT CAST(ARRAY(NULL) AS ARRAY<STRING>) AS xs;
~~~

这些xs示例的生成形状与实际边界相同；下表保留实测的原别名 value 及完整实际SQL，不用示例替换原查询。

## 3. 实际执行与原14条查询

从工作流根目录使用 ../doris-sql-validator/.venv/bin/python，PYTHONDONTWRITEBYTECODE=1、PYTHONPATH=../sqlglot-experiment:src，加载原项目 .env。先用 SqlglotTranspiler.transpile_case 从固定Case生成SQL，再 pg_probe.execute_query / compare_probe；37条边界使用 parse_one(..., read='postgres').sql('doris', unsupported_level=RAISE) 同一默认链路生成，双端各执行两次。每次10秒、10000行上限，不写数据库。

14条原查询当前PG均成功，另用 PostgreSQL TEXT 投影只读包装与 RecordedOutputProvider 读取的原.out逐条比较多重集合，14条均相同；该包装不用于证明原生类型/排序，不替换原基线。

| Case / stage | 原 .out 比较结果 | `` PG → Doris 已取得原生类型 `` | 实际观察/报错 |
| :--- | :--- | :--- | :--- |
| [0010](../../../../attribution/cases/aggregates-001/pg-aggregates-0010-12bf388c.md) / 01 | 行值或顺序不匹配 | `` _text → array<text> `` | 元素由 VARCHAR(5) 改为 TEXT；结构化数组一致，原 .out 显示仍不同。 |
| [0136](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md) / 03 | SQLGlot 转译失败 | `` _int8 → 无 `` | ARRAY(SELECT…) 未纳入本轮。 |
| [0306](../../../../attribution/cases/aggregates-001/pg-aggregates-0306-e70870c4.md) / 17 | 匹配 | `` text / numeric → varchar(65533) / bigint `` | 内部数组已为 INT；外层 SUM NUMERIC/BIGINT 与文本类型余项保留。 |
| [0410](../../../../attribution/cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md) / 31 | Doris 执行失败 | `` _int4 → 无 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 76)\n") |
| [0411](../../../../attribution/cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md) / 31 | Doris 执行失败 | `` _float8 → 无 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 66)\n") |
| [0412](../../../../attribution/cases/aggregates-001/pg-aggregates-0412-cbdaef84.md) / 31 | Doris 执行失败 | `` _int4 → 无 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 89)\n") |
| [0413](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) / 31 | Doris 执行失败 | `` _float8 → 无 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 97)\n") |
| [0415](../../../../attribution/cases/aggregates-001/pg-aggregates-0415-16b30942.md) / 31 | Doris 执行失败 | `` _text → 无 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 60)\n") |
| [0434](../../../../attribution/cases/aggregates-001/pg-aggregates-0434-5da33736.md) / 33 | Doris 执行失败 | `` int8 → 无 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 26)\n") |
| [0437](../../../../attribution/cases/aggregates-001/pg-aggregates-0437-d68f01c2.md) / 33 | Doris 执行失败 | `` numeric → 无 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") |
| [0438](../../../../attribution/cases/aggregates-001/pg-aggregates-0438-998adec3.md) / 33 | Doris 执行失败 | `` regtype → 无 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 37)\n") |
| [0534](../../../../attribution/cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) / 40 | Doris 执行失败 | `` _float4 / _float4 → 无 `` | (1105, "errCode = 2, detailMessage = Can not found function 'RWAGG'") |
| [0551](../../../../attribution/cases/aggregates-001/pg-aggregates-0551-f476de2c.md) / 42 | 匹配 | `` text / int4 / int8 → varchar(65533) / tinyint / bigint `` | 内部字符串数组已为 TEXT；外层 CASE int4/tinyint 余项保留。 |
| [0552](../../../../attribution/cases/aggregates-001/pg-aggregates-0552-7ea82af2.md) / 42 | 匹配 | `` text / int4 / int8 → varchar(65533) / tinyint / bigint `` | 内部字符串数组已为 TEXT；外层 CASE int4/tinyint 余项保留。 |

合计与fix-011相同：3条.out匹配、1条显示差异、9条Doris执行失败、1条SQLGlot拒绝。0010结构化元素值与TEXT类型已对齐，但PG .out的 {hello,world} 与Doris JSON数组显示仍不同，不放宽原比较器。0306、0551、0552的其他字段类型差异不能记为数组构造修复失败，也不能伪造整条类型通过。

VARIADIC三条的上表错误来自 run 的真实Doris执行；额外 pg_probe 在目标Parser前置检查即拒绝，未再连接目标执行，不能将工具错误充当另一份数据库错误。其他10条非空目标有实际生成SQL，0136是真实转译拒绝。

### 原查询与本轮实际生成 SQL

### Case 0010 / stage-01

PostgreSQL 原 SQL：

~~~sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
~~~

本轮默认转译实际生成：

~~~sql
SELECT ANY_VALUE(v) FROM (SELECT CAST(ARRAY('hello', 'world') AS ARRAY<STRING>) AS v) AS v
~~~

### Case 0136 / stage-03

PostgreSQL 原 SQL：

~~~sql
select array(select sum(x+y) s
            from generate_series(1,3) y group by y order by s)
  from generate_series(1,3) x;
~~~

本轮实际转译拒绝：Doris does not support ARRAY subquery constructors

### Case 0306 / stage-17

PostgreSQL 原 SQL：

~~~sql
select
    string_agg(distinct 'a', ','),
    sum((
        select sum(1)
        from (values(1)) b(id)
        where a.id = b.id
)) from unnest(array[1]) a(id);
~~~

本轮默认转译实际生成：

~~~sql
SELECT GROUP_CONCAT(DISTINCT 'a', ','), SUM((SELECT SUM(1) FROM (SELECT 1 AS id) AS b WHERE a.id = b.id)) FROM UNNEST(CAST(ARRAY(1) AS ARRAY<INT>)) AS a(id)
~~~

### Case 0410 / stage-31

PostgreSQL 原 SQL：

~~~sql
select percentile_disc(array[0,0.1,0.25,0.5,0.75,0.9,1]) within group (order by thousand)
from tenk1;
~~~

本轮默认转译实际生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(0, 0.1, 0.25, 0.5, 0.75, 0.9, 1)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0411 / stage-31

PostgreSQL 原 SQL：

~~~sql
select percentile_cont(array[0,0.25,0.5,0.75,1]) within group (order by thousand)
from tenk1;
~~~

本轮默认转译实际生成：

~~~sql
SELECT PERCENTILE_CONT(ARRAY(0, 0.25, 0.5, 0.75, 1)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0412 / stage-31

PostgreSQL 原 SQL：

~~~sql
select percentile_disc(array[[null,1,0.5],[0.75,0.25,null]]) within group (order by thousand)
from tenk1;
~~~

本轮默认转译实际生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(ARRAY(NULL, 1, 0.5), ARRAY(0.75, 0.25, NULL))) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0413 / stage-31

PostgreSQL 原 SQL：

~~~sql
select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x)
from generate_series(1,6) x;
~~~

本轮默认转译实际生成：

~~~sql
SELECT PERCENTILE_CONT(ARRAY(0, 1, 0.25, 0.75, 0.5, 1, 0.3, 0.32, 0.35, 0.38, 0.4)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '6')) AS x
~~~

### Case 0415 / stage-31

PostgreSQL 原 SQL：

~~~sql
select percentile_disc(array[0.25,0.5,0.75]) within group (order by x)
from unnest('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}'::text[]) u(x);
~~~

本轮默认转译实际生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(0.25, 0.5, 0.75)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM UNNEST(CAST('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}' AS ARRAY<STRING>)) AS u(x)
~~~

### Case 0434 / stage-33

PostgreSQL 原 SQL：

~~~sql
select least_agg(variadic array[q1,q2]) from int8_tbl;
~~~

本轮实际转译拒绝：Expecting ). Line 1, Col: 31.
  SELECT LEAST_AGG(VARIADIC [4mARRAY[0m(q1, q2)) FROM int8_tbl

Invalid expression / Unexpected token. Line 1, Col: 32.
  SELECT LEAST_AGG(VARIADIC ARRAY[4m([0mq1, q2)) FROM int8_tbl

### Case 0437 / stage-33

PostgreSQL 原 SQL：

~~~sql
select cleast_agg(variadic array[4.5,f1]) from int4_tbl;
~~~

本轮实际转译拒绝：Expecting ). Line 1, Col: 32.
  SELECT CLEAST_AGG(VARIADIC [4mARRAY[0m(4.5, f1)) FROM int4_tbl

Invalid expression / Unexpected token. Line 1, Col: 33.
  SELECT CLEAST_AGG(VARIADIC ARRAY[4m([0m4.5, f1)) FROM int4_tbl

### Case 0438 / stage-33

PostgreSQL 原 SQL：

~~~sql
select pg_typeof(cleast_agg(variadic array[4.5,f1])) from int4_tbl;
~~~

本轮实际转译拒绝：Expecting ). Line 1, Col: 42.
  SELECT PG_TYPEOF(CLEAST_AGG(VARIADIC [4mARRAY[0m(4.5, f1))) FROM int4_tbl

Expecting ). Line 1, Col: 42.
  SELECT PG_TYPEOF(CLEAST_AGG(VARIADIC [4mARRAY[0m(4.5, f1))) FROM int4_tbl

Invalid expression / Unexpected token. Line 1, Col: 43.
  SELECT PG_TYPEOF(CLEAST_AGG(VARIADIC ARRAY[4m([0m4.5, f1))) FROM int4_tbl

### Case 0534 / stage-40

PostgreSQL 原 SQL：

~~~sql
SELECT eatarray(rwagg(ARRAY[1.0::real])), eatarray(rwagg(ARRAY[1.0::real]));
~~~

本轮默认转译实际生成：

~~~sql
SELECT EATARRAY(RWAGG(CAST(ARRAY(CAST(1.0 AS FLOAT)) AS ARRAY<FLOAT>))), EATARRAY(RWAGG(CAST(ARRAY(CAST(1.0 AS FLOAT)) AS ARRAY<FLOAT>)))
~~~

### Case 0551 / stage-42

PostgreSQL 原 SQL：

~~~sql
select v||'a', case v||'a' when 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
~~~

本轮默认转译实际生成：

~~~sql
SELECT CONCAT(v, 'a'), CASE CONCAT(v, 'a') WHEN 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(CAST(ARRAY('a', 'b') AS ARRAY<STRING>)) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST
~~~

### Case 0552 / stage-42

PostgreSQL 原 SQL：

~~~sql
select v||'a', case when v||'a' = 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
~~~

本轮默认转译实际生成：

~~~sql
SELECT CONCAT(v, 'a'), CASE WHEN CONCAT(v, 'a') = 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(CAST(ARRAY('a', 'b') AS ARRAY<STRING>)) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST
~~~

## 4. 37条边界与未通过项

前18条为前轮原边界（仅空格不影响表达式），后19条扩展整数极值、混合已知数值类型、标量unknown、显式外层CAST和保留的反例。37条双端成功、每端额外重跑一次均稳定；35条按现有结构化值/重复次数比较一致，2条不同（25、36），没有把它们隐藏为通过。

前18条的7条真实默认类型差异为编号1、2、5、10、11、12、17；本轮全已对齐。前轮Unicode/空字符串/NULL数组本就可能被Doris推为TEXT，不能把该样本原本正确也算新增修复。编号14有唯一id=1/2/3并保持最终顺序；其余无最终ORDER BY，按多重集合保留重复次数。数组内部元素顺序始终保留，没有任意排序。

| 编号 | 完整源 SQL | 实际生成 Doris SQL | `` PG → Doris 原生类型 `` | 本次结论与限制 |
| ---: | :--- | :--- | :--- | :--- |
| 1 | `` SELECT ARRAY[1,2] AS value `` | `` SELECT CAST(ARRAY(1, 2) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 2 | `` SELECT ARRAY[1,NULL,2,1] AS value `` | `` SELECT CAST(ARRAY(1, NULL, 2, 1) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 3 | `` SELECT ARRAY[NULL::INT] AS value `` | `` SELECT CAST(ARRAY(CAST(NULL AS INT)) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 4 | `` SELECT ARRAY[]::INT[] AS value `` | `` SELECT CAST(ARRAY() AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 5 | `` SELECT ARRAY[[1,2],[3,4]] AS value `` | `` SELECT CAST(ARRAY(CAST(ARRAY(1, 2) AS ARRAY<INT>), CAST(ARRAY(3, 4) AS ARRAY<INT>)) AS ARRAY<ARRAY<INT>>) AS `value` `` | `` _int4 → array<array<int>> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 6 | `` SELECT ARRAY[1::BIGINT,NULL::BIGINT] AS value `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST(NULL AS BIGINT)) AS ARRAY<BIGINT>) AS `value` `` | `` _int8 → array<bigint> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 7 | `` SELECT ARRAY[1.25::DECIMAL(10,2),NULL::DECIMAL(10,2)] AS value `` | `` SELECT ARRAY(CAST(1.25 AS DECIMAL(10, 2)), CAST(NULL AS DECIMAL(10, 2))) AS `value` `` | `` _numeric → array<decimalv3(10,2)> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 8 | `` SELECT ARRAY['hello','','世界',NULL] AS value `` | `` SELECT CAST(ARRAY('hello', '', '世界', NULL) AS ARRAY<STRING>) AS `value` `` | `` _text → array<text> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 9 | `` SELECT ARRAY[x,NULL::INT] AS value FROM (VALUES(1::INT),(NULL::INT),(1::INT)) t(x) `` | `` SELECT ARRAY(x, CAST(NULL AS INT)) AS `value` FROM (SELECT CAST(1 AS INT) AS x UNION ALL SELECT CAST(NULL AS INT) UNION ALL SELECT CAST(1 AS INT)) AS t `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 10 | `` SELECT ARRAY[(SELECT 1)] AS value `` | `` SELECT CAST(ARRAY((SELECT 1)) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 11 | `` SELECT ARRAY[(SELECT 1),(SELECT 2)] AS value `` | `` SELECT CAST(ARRAY((SELECT 1), (SELECT 2)) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 12 | `` SELECT ARRAY[(SELECT 1 WHERE FALSE)] AS value `` | `` SELECT CAST(ARRAY((SELECT 1 WHERE FALSE)) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 13 | `` SELECT NULL::INT[] AS value `` | `` SELECT CAST(NULL AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 14 | `` SELECT id AS id,ARRAY[x,NULL::INT] AS value FROM (VALUES(1,1::INT),(2,NULL::INT),(3,1::INT)) t(id,x) ORDER BY id NULLS FIRST `` | `` SELECT id AS id, ARRAY(x, CAST(NULL AS INT)) AS `value` FROM (SELECT 1 AS id, CAST(1 AS INT) AS x UNION ALL SELECT 2, CAST(NULL AS INT) UNION ALL SELECT 3, CAST(1 AS INT)) AS t ORDER BY id `` | `` int4 / _int4 → tinyint / array<int> `` | 数组元素 INT 已对齐；独立 id 仍 int4 / tinyint，不属数组构造。 |
| 15 | `` SELECT ARRAY[(-9223372036854775807-1)::BIGINT,9223372036854775807::BIGINT] AS value `` | `` SELECT CAST(ARRAY(CAST((-9223372036854775807 - 1) AS BIGINT), CAST(9223372036854775807 AS BIGINT)) AS ARRAY<BIGINT>) AS `value` `` | `` _int8 → array<bigint> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 16 | `` SELECT ARRAY[-99999999.99::DECIMAL(10,2),99999999.99::DECIMAL(10,2),NULL::DECIMAL(10,2)] AS value `` | `` SELECT ARRAY(-CAST(99999999.99 AS DECIMAL(10, 2)), CAST(99999999.99 AS DECIMAL(10, 2)), CAST(NULL AS DECIMAL(10, 2))) AS `value` `` | `` _numeric → array<decimalv3(13,2)> `` | 值相同；源 numeric 无结果精度声明，目标 DECIMAL(13,2)，约束未验收。 |
| 17 | `` SELECT ARRAY[NULL] AS value `` | `` SELECT CAST(ARRAY(NULL) AS ARRAY<STRING>) AS `value` `` | `` _text → array<text> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 18 | `` SELECT ARRAY[1.0::REAL,NULL::REAL] AS value `` | `` SELECT CAST(ARRAY(CAST(1.0 AS FLOAT), CAST(NULL AS FLOAT)) AS ARRAY<FLOAT>) AS `value` `` | `` _float4 → array<float> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 19 | `` SELECT ARRAY[-2147483648,2147483647,NULL] AS value `` | `` SELECT CAST(ARRAY(-2147483648, 2147483647, NULL) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 20 | `` SELECT ARRAY[2147483648,1,NULL] AS value `` | `` SELECT CAST(ARRAY(2147483648, 1, NULL) AS ARRAY<BIGINT>) AS `value` `` | `` _int8 → array<bigint> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 21 | `` SELECT ARRAY[-9223372036854775808,9223372036854775807] AS value `` | `` SELECT CAST(ARRAY(-9223372036854775808, 9223372036854775807) AS ARRAY<BIGINT>) AS `value` `` | `` _int8 → array<bigint> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 22 | `` SELECT ARRAY[NULL,NULL] AS value `` | `` SELECT CAST(ARRAY(NULL, NULL) AS ARRAY<STRING>) AS `value` `` | `` _text → array<text> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 23 | `` SELECT ARRAY[(SELECT NULL)] AS value `` | `` SELECT CAST(ARRAY((SELECT NULL)) AS ARRAY<STRING>) AS `value` `` | `` _text → array<text> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 24 | `` SELECT ARRAY[(SELECT 'hello')] AS value `` | `` SELECT CAST(ARRAY((SELECT 'hello')) AS ARRAY<STRING>) AS `value` `` | `` _text → array<text> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 25 | `` SELECT ARRAY[TRUE,FALSE,NULL] AS value `` | `` SELECT CAST(ARRAY(TRUE, FALSE, NULL) AS ARRAY<BOOLEAN>) AS `value` `` | `` _bool → array<boolean> `` | BOOL/BOOLEAN 类型对齐；协议数组显示 true/false 与 1/0 不同，工具仍报值不同。 |
| 26 | `` SELECT ARRAY[1::SMALLINT,2::INT,NULL] AS value `` | `` SELECT CAST(ARRAY(CAST(1 AS SMALLINT), CAST(2 AS INT), NULL) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 27 | `` SELECT ARRAY[1::REAL,2,NULL] AS value `` | `` SELECT CAST(ARRAY(CAST(1 AS FLOAT), 2, NULL) AS ARRAY<FLOAT>) AS `value` `` | `` _float4 → array<float> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 28 | `` SELECT ARRAY[1::DOUBLE PRECISION,2::REAL,NULL] AS value `` | `` SELECT CAST(ARRAY(CAST(1 AS DOUBLE), CAST(2 AS FLOAT), NULL) AS ARRAY<DOUBLE>) AS `value` `` | `` _float8 → array<double> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 29 | `` SELECT ARRAY[[1],[2147483648]] AS value `` | `` SELECT CAST(ARRAY(CAST(ARRAY(1) AS ARRAY<INT>), CAST(ARRAY(2147483648) AS ARRAY<BIGINT>)) AS ARRAY<ARRAY<BIGINT>>) AS `value` `` | `` _int8 → array<array<bigint>> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 30 | `` SELECT ARRAY[1.25,2] AS value `` | `` SELECT ARRAY(1.25, 2) AS `value` `` | `` _numeric → array<decimalv3(3,2)> `` | 值相同；源无约束 NUMERIC / 目标 DECIMAL(3,2)，不强转 DOUBLE，精度域未验收。 |
| 31 | `` SELECT ARRAY[9223372036854775808] AS value `` | `` SELECT ARRAY(9223372036854775808) AS `value` `` | `` _numeric → array<largeint> `` | 值相同；源 NUMERIC / 目标 LARGEINT 仍不同，未猜成 BIGINT。 |
| 32 | `` SELECT ARRAY['1','2',NULL]::INT[] AS value `` | `` SELECT CAST(CAST(ARRAY('1', '2', NULL) AS ARRAY<STRING>) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 33 | `` SELECT ARRAY[NULL]::INT[] AS value `` | `` SELECT CAST(CAST(ARRAY(NULL) AS ARRAY<STRING>) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 34 | `` SELECT ARRAY[NULL::INT,NULL] AS value `` | `` SELECT CAST(ARRAY(CAST(NULL AS INT), NULL) AS ARRAY<INT>) AS `value` `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 35 | `` SELECT ARRAY[NULL]::BIGINT[] AS value `` | `` SELECT CAST(CAST(ARRAY(NULL) AS ARRAY<STRING>) AS ARRAY<BIGINT>) AS `value` `` | `` _int8 → array<bigint> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |
| 36 | `` SELECT ARRAY['1',2] AS value `` | `` SELECT ARRAY('1', 2) AS `value` `` | `` _int4 → array<text> `` | 真实差异：PG [1,2] / Doris ["1","2"]；字符串输入转换尚未实现。 |
| 37 | `` SELECT ARRAY[x,NULL] AS value FROM (VALUES(1::INT),(NULL::INT)) t(x) `` | `` SELECT ARRAY(x, NULL) AS `value` FROM (SELECT CAST(1 AS INT) AS x UNION ALL SELECT CAST(NULL AS INT)) AS t `` | `` _int4 → array<int> `` | 本次类型可映射、状态/字段/值/重复次数对齐 |

类型解释：PG _int4、_int8、_text、_float4、_float8、_bool 分别按元素OID映射INT、BIGINT、TEXT、FLOAT、DOUBLE、BOOLEAN；PG数组OID本身不编码维数，嵌套维数结合本次实际矩形数据和Doris ARRAY<ARRAY<...>>核对。工具仅做顶层名称比较时仍会显示“类型声明不同”，本报告据已取得OID/目标原生声明补充递归别名判断，没有修改工具或把未知类型当一致。

编号7源字段给出precision10/scale2，目标子类型DECIMALV3(10,2)，当前约束可核对；编号16和30源结果没有可用精度约束，不能拿输入子CAST当结果声明。编号31即使值同样是9223372036854775808，NUMERIC与LARGEINT仍不同。

BIGINT两端极值另以Python原生repr核对：PG为 `[[[-9223372036854775808, 9223372036854775807]]]`，Doris数组文本为 `[-9223372036854775808, 9223372036854775807]`；逐位相同，不使用JavaScript数值序列化后的舍入结果作证据。编号25原生PG为 `[True, False, None]`，目标协议为 `[1, 0, null]` 且类型为BOOLEAN；本轮仅保留该已有表示差异，不据类型相同篡改值比较。

另只读补查两种PG失败的类型组合：ARRAY[ARRAY[NULL],ARRAY[1]] 为42846，ARRAY[(SELECT '1'),2] 为42804；不替非法源输入安排Doris错误复刻，不将它们算入上述37条成功边界。

## 5. 单元测试、回归与提交边界

共同测试命令见[本轮汇总](../../../aggregates-001-fix-012-summary.md)：PG/Doris/MySQL158方法、全部方言1081方法、core四模块199方法、另四模块79方法均通过。158包含在1081中，不相加。ruff与git diff --check通过；缺duckdb/mypy，未运行完整optimizer测试、mypy及make check/C扩展。

初次定向测试158方法有6个失败：1个新测试错把既有PG标量子查询ARRAY输出当保持方括号；5个跨方言测试发现element_type泄漏为额外INT参数。前者改为断言真实类型和既有输出，后者增加公共Array生成方法修正；没有直接改旧跨方言期望来掩盖回归，最终旧测试保持通过。

142条固定原Case跨19阶段 run --stdout，全量Case ID与结果逐条对比fix-011，**0条结果改变，原82个匹配全部保持**。未跑全部313条/43阶段，未宣布全批验收。原.sql/.out、YAML、首轮JSON、准备材料不修改。

本轮代码边界是“PG ARRAY构造保留有限源共同元素类型”及其必要公共AST/生成支持和测试；与此前task-003等累积修改在同文件共存，不应按整份当前diff混合提交。HEAD仍089891f2521780e2c5b243005017af9db62f25a6，当前累积diff指纹309f2694a0a1ed3760b346c4dbd4d1b02da43c9b55830163c0f036b738b8e675，包含原任务已有修改，不是本轮独立补丁。未commit/push，未创建Issue/PR。

## 6. 验收与下一步

| 原task-001验收子项 | 本轮状态 | 下一步 |
| :--- | :--- | :--- |
| 有限裸整数/单列标量子查询默认元素类型 | 本轮约定样本通过：INT32/INT64边界、NULL、嵌套与标量空结果 | 保留本轮回归；这不是所有表达式的PG求型实现 |
| 全unknown/NULL及纯字符串默认TEXT | 本轮类型/当前值通过，0010原.out显示不同仍保留 | 不为抹平显示差异把数组改成字符串 |
| 显式已知INT/BIGINT/REAL等及当前Decimal(10,2) | 当前有限样本保持 | 非有限Float、任意CAST输入函数/错误语义不宣称全域覆盖 |
| 混合unknown字符串与非TEXT已知类型 | 未实现；编号36是真实元素值/类型差异 | 继续原task-001，明确源输入转换规则和成功边界后实施，不能只给一个'1'样本硬编码CAST |
| Decimal及超INT64的NUMERIC共同类型/结果约束 | 未验收；编号16/30/31保留 | 继续原task的类型子项；区分源结果有无typmod及Doris可表示域，不猜为DOUBLE/INT |
| 未知列/参数、一般函数及复杂表达式 | 本轮不猜类型，仍沿原生成路径 | 需要可信类型传播/Schema条件；不悄悄强制框架输入Schema，不扩大到task-003的VALUES传播 |

因此 task-001 继续保持“已修改但未完成验收”，不是“全部已修复”。下一轮应沿原task继续混合输入转换及Decimal/NUMERIC范围研究；另有task-003未关闭，但本轮未实施。整份输入仍未完成。

