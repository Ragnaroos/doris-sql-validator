# task-008 / fix-008：FROM 常量整数 GENERATE_SERIES

## 1. 结论与范围

**状态：已修改但未完成全部验收。** 非 NULL 的常量 INT4 起点、终点与非零步长主路径已实现、实际执行和验证；原验收还要求 NULL 参数行为，目前仍明确报 UnsupportedError，故不关闭 task-008。没有将源端负向的零步长强行转为成功结果。

指定任务模式，仅处理[原任务](../../../../attribution/aggregates-001-attribution-summary.md#task-008)。没有修改其他 task 的实现、验证框架、原 SQL/.out/YAML/首轮 JSON、数据或 Session 政策。未 commit/push，未创建 Issue/PR。共同版本、输入和回归见[本轮汇总](../../../aggregates-001-fix-008-summary.md)。保留前七轮修改；本轮代码仅改 generators/doris.py 与 test_doris.py。

不支持投影位置 SRF、相关/直接 LATERAL 表函数、WITH ORDINALITY、动态表达式、时间/Decimal/BIGINT 序列；不把一次独立候选的成功视为这些能力可用。原 32 条有关联但不全属于可完整解决的查询：LATERAL、数组子查询、UDF、统计类型/算法与 WITHIN GROUP 各自保留。

## 2. 修改依据与实现

修复前 PG `SELECT SUM(NULL::INT4) FROM GENERATE_SERIES(1,3)` 生成的 `FROM GENERATE_SERIES(1, 3)` 在 Doris 报 `mismatched input ',' expecting EQ`，见原 0051 Case；本轮不靠手写候选验收。

| 文件 / 入口 | 本轮行为 |
| :--- | :--- |
| sqlglot/generators/doris.py / table_sql | 仅 ExplodingGenerateSeries 表节点、参数为括号可剥离的整数字面量、均在 INT4 范围、非零步长时转换；保留原 UPDATE/DELETE 等上下文的别名输出规则 |
| 同文件 / explodinggenerateseries_sql | 未被安全表转换覆盖的调用明确报告不支持；RAISE 模式不会静默当作已正确转译 |
| tests/dialects/test_doris.py | 两个测试方法覆盖生成、别名、空区间、INT 边界、大范围只生成、不修改输入 AST、目标重新解析、排除范围 |

使用 Python 整数计算包含终点的长度 `max(0, (end - start) // step + 1)`，没有浮点除法、固定答案或 1000 行硬上限。生成一列关系：

```sql
SELECT CAST(start + number * step AS INT) AS output_column
FROM NUMBERS('number' = 'computed_count')
```

上段是规则示意，实际 SQL 见逐条。NUMBERS 的 number 为 BIGINT，中间乘加在足够宽的整数中计算，最终 CAST AS INT 恢复 PG INT4。别名规则：未命名时输出 generate_series；`AS g` 同时使输出列名为 g；`AS g(x)` 使用 x；引用限定名与大小写/引号保留。原 Table 的 JOIN 等属性复制，不原地改源 AST。

[PG 18 序列文档](https://www.postgresql.org/docs/18/functions-srf.html)规定默认步长 1、正负方向、NULL 输入与零步长行为；[Doris NUMBERS 文档](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/table-valued-functions/numbers/)给出从 0 开始的单列关系。本轮数据库另实查 NUMBERS('number'='0') 返回零行；`number=CAST(... AS STRING)` 不被当前 Doris 语法接受，不能把运行时长度直接放进参数。

## 3. 原查询实际执行

执行入口为修改后 SQLGlot parse_one(read='postgres').sql('doris', unsupported_level=RAISE)，并调用既有 execute_query / compare_probe；框架 run --stdout 按实际阶段批量复跑。时间 2026-11-23T10:47:14.875742+00:00，解释器为 ../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-experiment:src，import=../sqlglot-experiment/sqlglot/__init__.py。每条源与目标使用原 YAML 对应库。超时 10 秒、完整结果上限 10000 行；32 条当前 PG 原文全部成功，目标有转译失败时不执行目标。

原 .out 仍为基线。另用 `SELECT CAST(c0 AS TEXT), ... FROM (<原查询>) checked(c0,...)` 核对当前 PG 显示文本；它只补充证据、不替换原查询或历史答案。0085/0086/0093/0094/0095/0099/0100 共七条与 .out 已不同，下列分别列出。统计函数的当前浮点结果不据此写成历史结果正确或序列错误。

32 条整条结果：8 匹配、3 行值/顺序不同、20 Doris 执行失败、1 转译失败。八个 .out NULL 匹配中只有 0051/0054/0058 的当前原生类型声明也一致；其他五条继续保留类型契约差异。.out 本身没有原生类型，匹配不能代替补证。

<a id="statement-51"></a>

### 原语句 51：pg-aggregates-0051-6f50d445

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0051-6f50d445.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select sum(null::int4) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT SUM(CAST(NULL AS INT)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；sum: int8；记录 `[[null]]` |
| 实时 Doris | 成功；SUM(CAST(NULL AS INT)): bigint；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | int8 → bigint: 一致，精度/Scale 不适用 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 显示结果匹配；实时补证的 INT64/FLOAT64 类型也一致，不等于任意聚合输入都同义。

<a id="statement-52"></a>

### 原语句 52：pg-aggregates-0052-57717b1c

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0052-57717b1c.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select sum(null::int8) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT SUM(CAST(NULL AS BIGINT)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；sum: numeric；记录 `[[null]]` |
| 实时 Doris | 成功；SUM(CAST(NULL AS BIGINT)): bigint；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → bigint: 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 的 NULL 显示结果匹配；实时补证仍存在 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 声明差异，不能称完整类型验收通过。

<a id="statement-53"></a>

### 原语句 53：pg-aggregates-0053-80bc631f

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0053-80bc631f.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select sum(null::numeric) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT SUM(CAST(NULL AS DECIMAL)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；sum: numeric；记录 `[[null]]` |
| 实时 Doris | 成功；SUM(CAST(NULL AS DECIMAL)): decimalv3(38,9)；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → decimalv3(38,9): 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 的 NULL 显示结果匹配；实时补证仍存在 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 声明差异，不能称完整类型验收通过。

<a id="statement-54"></a>

### 原语句 54：pg-aggregates-0054-9d43ca75

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0054-9d43ca75.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select sum(null::float8) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT SUM(CAST(NULL AS DOUBLE)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；sum: float8；记录 `[[null]]` |
| 实时 Doris | 成功；SUM(CAST(NULL AS DOUBLE)): double；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | float8 → double: 一致，精度/Scale 不适用 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 显示结果匹配；实时补证的 INT64/FLOAT64 类型也一致，不等于任意聚合输入都同义。

<a id="statement-55"></a>

### 原语句 55：pg-aggregates-0055-a2bc4e59

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0055-a2bc4e59.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select avg(null::int4) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AVG(CAST(NULL AS INT)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；avg: numeric；记录 `[[null]]` |
| 实时 Doris | 成功；AVG(CAST(NULL AS INT)): double；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → double: 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 的 NULL 显示结果匹配；实时补证仍存在 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 声明差异，不能称完整类型验收通过。

<a id="statement-56"></a>

### 原语句 56：pg-aggregates-0056-ed925b77

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0056-ed925b77.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select avg(null::int8) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AVG(CAST(NULL AS BIGINT)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；avg: numeric；记录 `[[null]]` |
| 实时 Doris | 成功；AVG(CAST(NULL AS BIGINT)): double；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → double: 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 的 NULL 显示结果匹配；实时补证仍存在 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 声明差异，不能称完整类型验收通过。

<a id="statement-57"></a>

### 原语句 57：pg-aggregates-0057-54488b60

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0057-54488b60.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select avg(null::numeric) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AVG(CAST(NULL AS DECIMAL)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；avg: numeric；记录 `[[null]]` |
| 实时 Doris | 成功；AVG(CAST(NULL AS DECIMAL)): decimalv3(38,9)；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → decimalv3(38,9): 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 的 NULL 显示结果匹配；实时补证仍存在 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 声明差异，不能称完整类型验收通过。

<a id="statement-58"></a>

### 原语句 58：pg-aggregates-0058-774c37d9

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0058-774c37d9.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select avg(null::float8) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AVG(CAST(NULL AS DOUBLE)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **匹配** |
| 实时源端 | 成功；avg: float8；记录 `[[null]]` |
| 实时 Doris | 成功；AVG(CAST(NULL AS DOUBLE)): double；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | float8 → double: 一致，精度/Scale 不适用 |
| 行数 / 值及重复次数 | 一致 / 一致 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

.out 显示结果匹配；实时补证的 INT64/FLOAT64 类型也一致，不等于任意聚合输入都同义。

<a id="statement-59"></a>

### 原语句 59：pg-aggregates-0059-6e8dac37

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0059-6e8dac37.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select sum('NaN'::numeric) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT SUM(CAST('NaN' AS DECIMAL)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["NaN"]]` / **行值或顺序不匹配** |
| 实时源端 | 成功；sum: numeric；记录 `[[{"十进制数":"NaN"}]]` |
| 实时 Doris | 成功；SUM(CAST('NaN' AS DECIMAL)): decimalv3(38,9)；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → decimalv3(38,9): 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 不同 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

NaN NUMERIC 在 Doris CAST/聚合后为 NULL；不是序列产生的值或行数错误。保留非有限数/类型契约研究。

<a id="statement-60"></a>

### 原语句 60：pg-aggregates-0060-10dc4c9b

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0060-10dc4c9b.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
select avg('NaN'::numeric) from generate_series(1,3);
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AVG(CAST('NaN' AS DECIMAL)) FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '3')) AS generate_series
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["NaN"]]` / **行值或顺序不匹配** |
| 实时源端 | 成功；avg: numeric；记录 `[[{"十进制数":"NaN"}]]` |
| 实时 Doris | 成功；AVG(CAST('NaN' AS DECIMAL)): decimalv3(38,9)；记录 `[[null]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | numeric → decimalv3(38,9): 不同，精度/Scale 信息不足 |
| 行数 / 值及重复次数 | 一致 / 不同 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

NaN NUMERIC 在 Doris CAST/聚合后为 NULL；不是序列产生的值或行数错误。保留非有限数/类型契约研究。

<a id="statement-85"></a>

### 原语句 85：pg-aggregates-0085-b2d1da4b

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0085-b2d1da4b.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(0.09, g), regr_r2(0.09, g)
  FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(0.09, g), REGR_R2(0.09, g) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["","1"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[-0.564611496222153,0.318786141666219]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["-0.564611496222153","0.318786141666219"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-86"></a>

### 原语句 86：pg-aggregates-0086-94d0e96a

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0086-94d0e96a.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(g, 0.09), regr_r2(g, 0.09), regr_slope(g, 0.09), regr_intercept(g, 0.09)
  FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(g, 0.09), REGR_R2(g, 0.09), REGR_SLOPE(g, 0.09), REGR_INTERCEPT(g, 0.09) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["","","",""]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；regr_slope: float8；regr_intercept: float8；记录 `[[-0.564611496222153,0.318786141666219,-277565795438313000,24980921589448200]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["-0.564611496222153","0.318786141666219","-2.77565795438313e+17","2.49809215894482e+16"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-87"></a>

### 原语句 87：pg-aggregates-0087-c50d900b

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0087-c50d900b.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(1.3 + g * 1e-16, 1.3 + g * 1e-16)
  FROM generate_series(1, 3) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(1.3 + g * 1e-16, 1.3 + g * 1e-16) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '3')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[[""]]` / **行值或顺序不匹配** |
| 实时源端 | 成功；corr: float8；记录 `[[null]]` |
| 实时 Doris | 成功；CORR(1.3 + g * 1e-16, 1.3 + g * 1e-16): double；记录 `[[0]]` |
| 字段数量 / 显式别名 | 一致 / 未发现需检查的显式别名 |
| 类型声明 | float8 → double: 一致，精度/Scale 不适用 |
| 行数 / 值及重复次数 | 一致 / 不同 |
| 最终顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

CORR 对近常数输入返回 PG NULL / Doris 0.0；保留数值算法研究。

<a id="statement-93"></a>

### 原语句 93：pg-aggregates-0093-d3a22e61

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0093-d3a22e61.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(1e-100 + g * 1e-105, 1e-100 + g * 1e-105),
       regr_r2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105)
  FROM generate_series(1, 3) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(1e-100 + g * 1e-105, 1e-100 + g * 1e-105), REGR_R2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '3')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["1","1"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"inf"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["Infinity","NaN"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-94"></a>

### 原语句 94：pg-aggregates-0094-75ff7206

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0094-75ff7206.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(1e-100 + g * 1e-105, 1e-100 + g * 1e-105),
       regr_r2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105)
  FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(1e-100 + g * 1e-105, 1e-100 + g * 1e-105), REGR_R2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["1","1"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"inf"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["Infinity","NaN"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-95"></a>

### 原语句 95：pg-aggregates-0095-5046511e

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0095-5046511e.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(1e100 + g * 1e95, 1e100 + g * 1e95),
       regr_r2(1e100 + g * 1e95, 1e100 + g * 1e95)
  FROM generate_series(1, 2) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(1e100 + g * 1e95, 1e100 + g * 1e95), REGR_R2(1e100 + g * 1e95, 1e100 + g * 1e95) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '2')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["1","1"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[0,{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["0","NaN"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-98"></a>

### 原语句 98：pg-aggregates-0098-b1e5567b

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0098-b1e5567b.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(g, 'NaN'), regr_r2(g, 'NaN') FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(g, 'NaN'), REGR_R2(g, 'NaN') FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["NaN","NaN"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"nan"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-99"></a>

### 原语句 99：pg-aggregates-0099-bed0f6ec

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0099-bed0f6ec.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr(0.1, 'NaN'), regr_r2(0.1, 'NaN') FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR(0.1, 'NaN'), REGR_R2(0.1, 'NaN') FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["","1"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"nan"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["NaN","NaN"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-100"></a>

### 原语句 100：pg-aggregates-0100-3b815f6a

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0100-3b815f6a.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr('NaN', 0.1), regr_r2('NaN', 0.1) FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR('NaN', 0.1), REGR_R2('NaN', 0.1) FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["",""]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"nan"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 不同；当前显示文本 `[["NaN","NaN"]]`，不替换原 .out |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-101"></a>

### 原语句 101：pg-aggregates-0101-7fc3b3aa

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0101-7fc3b3aa.md)；阶段 [aggregates-001-stage-01-cases.yaml](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)。原源 SQL：

```sql
SELECT corr('NaN', 'NaN'), regr_r2('NaN', 'NaN') FROM generate_series(1, 30) g;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT CORR('NaN', 'NaN'), REGR_R2('NaN', 'NaN') FROM (SELECT CAST(1 + number * 1 AS INT) AS g FROM NUMBERS('number' = '30')) AS g
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["NaN","NaN"]]` / **Doris 执行失败** |
| 实时源端 | 成功；corr: float8；regr_r2: float8；记录 `[[{"特殊浮点数":"nan"},{"特殊浮点数":"nan"}]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'")
```

Doris 缺少 REGR_R2；未据函数缺失认定不可模拟。保留回归统计研究；其中实时 PG 与 .out 的冲突另列。

<a id="statement-134"></a>

### 原语句 134：pg-aggregates-0134-429eb1f7

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0134-429eb1f7.md)；阶段 [aggregates-001-stage-03-cases.yaml](../../../../data-preparation/aggregates-001-stage-03-cases.yaml)。原源 SQL：

```sql
select s1, s2, sm
from generate_series(1, 3) s1,
     lateral (select s2, sum(s1 + s2) sm
              from generate_series(1, 3) s2 group by s2) ss
order by 1, 2;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT s1, s2, sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s1 FROM NUMBERS('number' = '3')) AS s1, LATERAL (SELECT s2, SUM(s1 + s2) AS sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s2 FROM NUMBERS('number' = '3')) AS s2 GROUP BY s2) AS ss ORDER BY 1 NULLS LAST, 2 NULLS LAST
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["1","1","2"],["1","2","3"],["1","3","4"],["2","1","3"],["2","2","4"],["2","3","5"],["3","1","4"],["3","2","5"],["3","3","6"]]` / **Doris 执行失败** |
| 实时源端 | 成功；s1: int4；s2: int4；sm: int8；记录 `[[1,1,2],[1,2,3],[1,3,4],[2,1,3],[2,2,4],[2,3,5],[3,1,4],[3,2,5],[3,3,6]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'UNNEST' at '('(line 1, pos 110)\n")
```

常量序列已转换；外层 LATERAL 相关聚合子查询仍被 Doris 拒绝，复用查询级重写研究。

<a id="statement-136"></a>

### 原语句 136：pg-aggregates-0136-4243166e

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md)；阶段 [aggregates-001-stage-03-cases.yaml](../../../../data-preparation/aggregates-001-stage-03-cases.yaml)。原源 SQL：

```sql
select array(select sum(x+y) s
            from generate_series(1,3) y group by y order by s)
  from generate_series(1,3) x;
```

本轮转译错误（目标未执行）：

```text
UnsupportedError: Doris does not support ARRAY subquery constructors
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{2,3,4}"],["{3,4,5}"],["{4,5,6}"]]` / **SQLGlot 转译失败** |
| 实时源端 | 成功；array: _int8；记录 `[[[2,3,4]],[[3,4,5]],[[4,5,6]]]` |
| 实时 Doris | 未执行，转译失败 |
| 字段数量 / 显式别名 | 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

ARRAY 子查询构造属于 task-001 排除范围；未执行目标 SQL，序列主路径不代表整个相关子查询可用。

<a id="statement-276"></a>

### 原语句 276：pg-aggregates-0276-0f1f5154

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0276-0f1f5154.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select array_agg(distinct val)
from (select null as val from generate_series(1, 2));
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{NULL}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；array_agg: _text；记录 `[[[null]]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 53)\n\n== SQL ==\nSELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)\n-----------------------------------------------------^^^\n")
```

序列已转换；原 PG 允许的无别名派生表仍被 Doris 拒绝。错误自动分类为类型转换失败并不准确，以原文为准；关联派生表/查询级兼容研究，不属于序列行数算法。

<a id="statement-293"></a>

### 原语句 293：pg-aggregates-0293-3e365a0a

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0293-3e365a0a.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select aggfstr(distinct a,b,c)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,3) i;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AGGFSTR(DISTINCT a, b, c) FROM (SELECT 1 AS a, 3 AS b, 'foo' AS c UNION ALL SELECT 0, NULL, NULL UNION ALL SELECT 2, 2, 'bar' UNION ALL SELECT 3, 1, 'baz') AS v, (SELECT CAST(1 + number * 1 AS INT) AS i FROM NUMBERS('number' = '3')) AS i
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{\"(1,3,foo)\",\"(2,2,bar)\",\"(3,1,baz)\"}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；aggfstr: _aggtype；记录 `[["{\"(1,3,foo)\",\"(2,2,bar)\",\"(3,1,baz)\"}"]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'AGGFSTR'")
```

AGGFSTR/AGGFNS 为原脚本自定义聚合，Doris 未定义；不按名字硬编码社区规则。

<a id="statement-294"></a>

### 原语句 294：pg-aggregates-0294-5412623b

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0294-5412623b.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select aggfns(distinct a,b,c)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,3) i;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AGGFNS(DISTINCT a, b, c) FROM (SELECT 1 AS a, 3 AS b, 'foo' AS c UNION ALL SELECT 0, NULL, NULL UNION ALL SELECT 2, 2, 'bar' UNION ALL SELECT 3, 1, 'baz') AS v, (SELECT CAST(1 + number * 1 AS INT) AS i FROM NUMBERS('number' = '3')) AS i
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{\"(0,,)\",\"(1,3,foo)\",\"(2,2,bar)\",\"(3,1,baz)\"}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；aggfns: _aggtype；记录 `[["{\"(0,,)\",\"(1,3,foo)\",\"(2,2,bar)\",\"(3,1,baz)\"}"]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'")
```

AGGFSTR/AGGFNS 为原脚本自定义聚合，Doris 未定义；不按名字硬编码社区规则。

<a id="statement-295"></a>

### 原语句 295：pg-aggregates-0295-bf759c5f

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0295-bf759c5f.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select aggfstr(distinct a,b,c order by b)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,3) i;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AGGFSTR(DISTINCT a, b, c ORDER BY b NULLS LAST) FROM (SELECT 1 AS a, 3 AS b, 'foo' AS c UNION ALL SELECT 0, NULL, NULL UNION ALL SELECT 2, 2, 'bar' UNION ALL SELECT 3, 1, 'baz') AS v, (SELECT CAST(1 + number * 1 AS INT) AS i FROM NUMBERS('number' = '3')) AS i
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{\"(3,1,baz)\",\"(2,2,bar)\",\"(1,3,foo)\"}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；aggfstr: _aggtype；记录 `[["{\"(3,1,baz)\",\"(2,2,bar)\",\"(1,3,foo)\"}"]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'AGGFSTR'")
```

AGGFSTR/AGGFNS 为原脚本自定义聚合，Doris 未定义；不按名字硬编码社区规则。

<a id="statement-296"></a>

### 原语句 296：pg-aggregates-0296-a77bafc5

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0296-a77bafc5.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select aggfns(distinct a,b,c order by b)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,3) i;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AGGFNS(DISTINCT a, b, c ORDER BY b NULLS LAST) FROM (SELECT 1 AS a, 3 AS b, 'foo' AS c UNION ALL SELECT 0, NULL, NULL UNION ALL SELECT 2, 2, 'bar' UNION ALL SELECT 3, 1, 'baz') AS v, (SELECT CAST(1 + number * 1 AS INT) AS i FROM NUMBERS('number' = '3')) AS i
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{\"(3,1,baz)\",\"(2,2,bar)\",\"(1,3,foo)\",\"(0,,)\"}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；aggfns: _aggtype；记录 `[["{\"(3,1,baz)\",\"(2,2,bar)\",\"(1,3,foo)\",\"(0,,)\"}"]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'")
```

AGGFSTR/AGGFNS 为原脚本自定义聚合，Doris 未定义；不按名字硬编码社区规则。

<a id="statement-299"></a>

### 原语句 299：pg-aggregates-0299-d52780a5

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0299-d52780a5.md)；阶段 [aggregates-001-stage-17-cases.yaml](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)。原源 SQL：

```sql
select aggfns(distinct a,a,c order by a)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,2) i;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT AGGFNS(DISTINCT a, a, c ORDER BY a NULLS LAST) FROM (SELECT 1 AS a, 3 AS b, 'foo' AS c UNION ALL SELECT 0, NULL, NULL UNION ALL SELECT 2, 2, 'bar' UNION ALL SELECT 3, 1, 'baz') AS v, (SELECT CAST(1 + number * 1 AS INT) AS i FROM NUMBERS('number' = '2')) AS i
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{\"(0,0,)\",\"(1,1,foo)\",\"(2,2,bar)\",\"(3,3,baz)\"}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；aggfns: _aggtype；记录 `[["{\"(0,0,)\",\"(1,1,foo)\",\"(2,2,bar)\",\"(3,3,baz)\"}"]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'")
```

AGGFSTR/AGGFNS 为原脚本自定义聚合，Doris 未定义；不按名字硬编码社区规则。

<a id="statement-398"></a>

### 原语句 398：pg-aggregates-0398-73d63cba

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0398-73d63cba.md)；阶段 [aggregates-001-stage-31-cases.yaml](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)。原源 SQL：

```sql
select p, percentile_cont(p) within group (order by x::float8)
from generate_series(1,5) x,
     (values (0::float8),(0.1),(0.25),(0.4),(0.5),(0.6),(0.75),(0.9),(1)) v(p)
group by p order by p;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT p, PERCENTILE_CONT(p) WITHIN GROUP (ORDER BY CAST(x AS DOUBLE) NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '5')) AS x, (SELECT CAST(0 AS DOUBLE) AS p UNION ALL SELECT 0.1 UNION ALL SELECT 0.25 UNION ALL SELECT 0.4 UNION ALL SELECT 0.5 UNION ALL SELECT 0.6 UNION ALL SELECT 0.75 UNION ALL SELECT 0.9 UNION ALL SELECT 1) AS v GROUP BY p ORDER BY p NULLS LAST
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["0","1"],["0.1","1.4"],["0.25","2"],["0.4","2.6"],["0.5","3"],["0.6","3.4"],["0.75","4"],["0.9","4.6"],["1","5"]]` / **Doris 执行失败** |
| 实时源端 | 成功；p: float8；percentile_cont: float8；记录 `[[0,1],[0.1,1.4],[0.25,2],[0.4,2.6],[0.5,3],[0.6,3.4],[0.75,4],[0.9,4.6],[1,5]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 42)\n")
```

WITHIN GROUP 仍原样生成，被 Doris 解析器拒绝；保留有序/假想集合聚合研究。

<a id="statement-413"></a>

### 原语句 413：pg-aggregates-0413-6ccabd9a

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md)；阶段 [aggregates-001-stage-31-cases.yaml](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)。原源 SQL：

```sql
select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x)
from generate_series(1,6) x;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT PERCENTILE_CONT(ARRAY(0, 1, 0.25, 0.75, 0.5, 1, 0.3, 0.32, 0.35, 0.38, 0.4)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '6')) AS x
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["{1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3}"]]` / **Doris 执行失败** |
| 实时源端 | 成功；percentile_cont: _float8；记录 `[[[1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3]]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 97)\n")
```

WITHIN GROUP 仍原样生成，被 Doris 解析器拒绝；保留有序/假想集合聚合研究。

<a id="statement-427"></a>

### 原语句 427：pg-aggregates-0427-1ad928b9

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0427-1ad928b9.md)；阶段 [aggregates-001-stage-31-cases.yaml](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)。原源 SQL：

```sql
select rank('3') within group (order by x) from generate_series(1,5) x;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT RANK('3') WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '5')) AS x
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["3"]]` / **Doris 执行失败** |
| 实时源端 | 成功；rank: int8；记录 `[[3]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 30)\n")
```

WITHIN GROUP 仍原样生成，被 Doris 解析器拒绝；保留有序/假想集合聚合研究。

<a id="statement-428"></a>

### 原语句 428：pg-aggregates-0428-5c5a2a90

原 [Case 归因](../../../../attribution/cases/aggregates-001/pg-aggregates-0428-5c5a2a90.md)；阶段 [aggregates-001-stage-31-cases.yaml](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)。原源 SQL：

```sql
select percent_rank(0) within group (order by x) from generate_series(1,0) x;
```

本轮实际生成并执行的 Doris SQL：

```sql
SELECT PERCENT_RANK(0) WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '0')) AS x
```

| 维度 | 实际观察 |
| :--- | :--- |
| 原 .out / 框架整条结果 | `[["0"]]` / **Doris 执行失败** |
| 实时源端 | 成功；percent_rank: float8；记录 `[[0]]` |
| 实时 Doris | 失败；无完整字段/结果；错误见下文 |
| 字段数量 / 显式别名 | 未比较 / 未比较 |
| 类型声明 | 无完整双端结果，未比较 |
| 行数 / 值及重复次数 | 未比较 / 未比较 |
| 最终顺序 | 未比较 |
| 当前 PG 文本与原 .out | 值和重复次数相同（不代替类型及顺序验证） |

Doris 实际错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 36)\n")
```

WITHIN GROUP 仍原样生成，被 Doris 解析器拒绝；保留有序/假想集合聚合研究。

## 4. 有限边界与限制

65 条变体全部由修改后 SQLGlot 生成，再在双端执行，并分别重跑一次。65/65 状态、字段数、已取得的类型声明、行数、值及重复次数一致；带最终 ORDER BY 的结果本次顺序一致。序列是 INT4/INT，标量 COUNT 与窗口编号为 INT8/BIGINT；没有放宽比较器。普通 SELECT 显式 Alias 由工具核查；工具提示 UNION ALL“集合查询别名尚未检查”；本轮另读双端真实返回元数据，列名均为 v、类型 INT4/INT，补证通过，不冒称工具自动完成该项。无 ORDER BY 的查询以多重集合为准，不要求偶然扫描顺序。

| 组 | 条数 | 可复现输入 / 目的 |
| :--- | ---: | :--- |
| 小整数笛卡尔积 | 45 | start/end 分别取 -3,0,3；step 取 -3,-2,1,2,3；统一 SELECT x AS value FROM generate_series(...) g(x) ORDER BY x。覆盖升降、方向错误、单点、越过终点 |
| 默认步长及 INT4 边界 | 6 | (1,3,默认)、(-2147483648,-2147483646,1)、(2147483645,2147483647,1)、(2147483647,2147483645,-1)、(-2147483648,2147483647,2147483647)、(2147483647,-2147483648,-2147483648) |
| 别名与上下文 | 14 | SELECT *；g/g.g/g.*；带引号 S(V)；CROSS JOIN；LEFT JOIN 无匹配；UNION ALL 重复值；CTE/WHERE；GROUP BY/HAVING；空序列标量 COUNT；限定 generate_series.generate_series；窗口 ROW_NUMBER；列别名 number；1..1001 的 1001 条记录 |

有序查询的具体模板为 ORDER BY x 或实际唯一关系键；本次稳定不证明任意排序键都唯一。INT4 全范围长度 4294967296 只做生成单元测试，未执行；不声称大范围性能/资源验收。没有引入 1000 上限；上限属于探针安全策略而非转换语义。

### NULL 与零步长：当前未覆盖

| 源调用 | PG 原文实测 | 修改后转译 |
| :--- | :--- | :--- |
| generate_series(NULL,3) | 成功，零行 | UnsupportedError，目标未执行 |
| generate_series(1,NULL) | 成功，零行 | UnsupportedError，目标未执行 |
| generate_series(1,3,NULL) | 成功，零行 | UnsupportedError，目标未执行 |
| generate_series(NULL::INT,3,0) | 成功，零行，NULL 输入不能误当普通零步长错误 | UnsupportedError，目标未执行 |
| generate_series(1,3,0) | SQLSTATE 22023，step size cannot equal zero | UnsupportedError，默认不复制源端负向错误 |

当前明确诊断为 `Doris GENERATE_SERIES requires a table reference with constant INT arguments and a nonzero step, without LATERAL or WITH ORDINALITY`。NULL 是成功源查询的缺口，不把它归为负向或已通过。仓库要求 NULL 语义在查询时处理，不能靠识别字面量 NULL 然后返回预制空关系完成验收。当前 NUMBERS 主路径依赖静态长度，需另设计可安全处理 NULL 的运行时路径；[Doris EXPLODE_NUMBERS](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/table-functions/explode-numbers/)可作为后续调查方向，本轮未执行/实现，且它的 INT 长度与较大范围另需核对，不认定 Doris 无法实现。

## 5. 测试与相关回归

先补测试，未实现时两个方法出现 19 个失败断言；最终修改后通过。未安装依赖或改测试答案制造通过。

| 命令，工作目录 ../sqlglot-experiment | 实际结果 |
| :--- | :--- |
| .venv/bin/python -m unittest tests.dialects.test_doris.TestDoris.test_integer_generate_series tests.dialects.test_doris.TestDoris.test_integer_generate_series_exclusions | 两个新增方法通过 |
| PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql | 152 个方法通过 |
| 同 PATH/解释器，python -m unittest discover -s tests/dialects | 1075 个方法通过，包含上面 152，不相加 |
| 同 PATH/解释器，python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens | 233 个方法通过 |
| Ruff check / format --check，六个累积修改文件；git diff --check | 通过 |

没有运行完整 make check、C 扩展、mypy、DuckDB executor/optimizer 全套；不代表其他数据库实际执行验证。原前七轮语义补丁保持，未修改其代码或比较规则。

run --stdout 的 130 条唯一原查询为前轮 99 与本任务 32 的并集，0276 重合一次，覆盖原 16 阶段。80 匹配、28 Doris 执行失败、17 行值/顺序不同、1 转译失败、4 源端负向；原 72 个匹配全部保持。全量 313/43 阶段未重跑，原导入遗漏未改。

## 6. 验收与下一步

非 NULL 常量 INT4 序列主路径已实测；NULL 相关验收未完成，所以 task-008 当前维持“已修改但未完成验收”，不以八条新增 MATCH 替代任务验收。零步长未错误变成成功；源负向默认排除，不承担错误全文复刻。NEXT：先为同一 task-008 补充运行时 NULL 路径及范围/资源反例，再决定是否关闭；不另起一个重复的 NULL task。task-009 是独立下一能力，本轮没有实施。

原 Case 新暴露的独立问题保留到已有类型、非有限数、回归统计、查询级重写、有序集合/UDF 研究；不把所有失败归为序列、也不混进本轮实现。0276 的派生表别名问题需独立核对作用域/命名碰撞后决定通用规则，不能仅因报错文本建同名 task。本轮未发现这 130 条中的既有匹配回归；这不证明全输入无回归。

