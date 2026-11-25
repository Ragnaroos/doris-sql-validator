# task-008 / fix-009：补齐常量 INT4 序列的 NULL 参数

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`be0918f1a48384e1f842d8705afc05824fc3eb36`。将fix-008的常量序列与fix-009的NULL补齐作为同一规则保存，不按两轮机械拆分；投影/LATERAL等排除范围不变。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与范围

**已修复并完成约定验收。** 继续 [task-008](../../../../attribution/aggregates-001-attribution-summary.md#task-008)，补齐 [fix-008](../fix-008/task-008.md) 未完成的常量 NULL 参数处理，不创建新 task。fix-009 是本轮编号，**不是 task-009**；REGR_COUNT 本轮没有实施。

仅限 FROM 中非相关的常量 INT4/NULL 输入，含括号和 INT CAST；任一起点、终点或步长为 NULL 返回零行，保留输出列、别名、INT 类型。NULL 与零步长共存也返回零行；全部非 NULL 而步长为零仍明确 UnsupportedError，不将源端负向改成成功结果。本轮授权不包括 commit/push、Issue/PR、框架修改、建表装数、Session 政策或其他任务。

不扩展动态参数、列引用、NULLIF 等函数表达式、直接 LATERAL/投影 SRF、WITH ORDINALITY、BIGINT/Decimal/时间序列。大范围资源行为未纳入性能验收。共同代码、版本和输入见[本轮汇总](../../../aggregates-001-fix-009-summary.md)。旧报告与首轮事实保留。

## 2. 修复依据与实现

修改前本轮复现 `SELECT * FROM generate_series(NULL,3)` 及 `generate_series(NULL::INT,3,0)`：PG 成功返回零行，SQLGlot RAISE 模式报不支持。与源端负向不同，这是成功源查询的转换缺口。

| 代码 / 测试入口 | 实际修改与边界 |
| :--- | :--- |
| generators/doris.py / table_sql | 保留整数 NUMBERS 路径；INT CAST 可安全剥离作常量检查；非整数字面量必须是常量叶节点、非函数，且按 PG 的 COALESCE(arg,1) 类型规则可归到 INT；BIGINT、FLOAT、字符串、Boolean、参数或列等拒绝 |
| 同文件 / INTEGER_SERIES_LENGTH | SQL CASE 在执行时检查三个参数 IS NULL，计算展开长度；任一 NULL 长度为零。差值提升 BIGINT，NULLIF(step,0) 避免无效分母 |
| 同文件 / NULL 运行时关系 | 一行种子关系 + LATERAL VIEW EXPLODE_NUMBERS(length)，不是 OUTER 版本，长度零不补一条 NULL 行；显式投影一列并 CAST AS INT，内部辅助列不泄漏 |
| tests/dialects/test_doris.py | 新增 test_integer_generate_series_nulls、test_integer_generate_series_nullable_scope；更新旧 NULL 排除断言，补非 NULL INT CAST 的原路径和零步长排除 |

COALESCE 只用于 **Schema 无关的常量类型准入检查**，不放进目标 SQL 代替原参数，不把 NULL 当 1 执行；不在 Python 用 isinstance(arg, exp.Null) 分支返回预制空关系。实际原参数保留在生成 SQL，NULL 语义由运行时 CASE 实现。默认 parse_one → sql('doris') 已受益，不要求用户先 annotate_types，也未给验证框架注入 Schema。

共享长度模板如下，仅表达规则；逐条实际生成 SQL 位于第 3 节可展开区域：

```sql
CASE
  WHEN start IS NULL OR stop IS NULL OR step IS NULL THEN 0
  WHEN (step > 0 AND start <= stop) OR (step < 0 AND start >= stop)
    THEN (CAST(stop AS BIGINT) - CAST(start AS BIGINT)) DIV NULLIF(step, 0) + 1
  ELSE 0
END
```

[PostgreSQL 18 文档](https://www.postgresql.org/docs/18/functions-srf.html)规定 NULL 输入返回零行；[Doris EXPLODE_NUMBERS](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/table-functions/explode-numbers/)说明非 OUTER 展开的零长度行为。当前实例另行实测，不能只凭文档宣称版本可用。源 SQL 的直接 LATERAL 支持仍排除；生成器为自身非相关派生关系使用 Doris LATERAL VIEW，并不等于支持任意源 LATERAL。

实际最小复现及生成结果：

```sql
SELECT * FROM generate_series(NULL,3)
```

```sql
SELECT * FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series
```

双端成功、零行；源字段 generate_series: int4，目标同名 int；目标精度11、Scale0，源整数精度不适用，不比较驱动的显示宽度。返回的是带一列 INT 的空结果，而不是一条 NULL 记录。

## 3. 实际边界执行与结果

执行时间 2026-11-23T11:00:58.156357+00:00；解释器 ../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-experiment:src，import=../sqlglot-experiment/sqlglot/__init__.py，版本 30.25.1.dev355。通过 parse_one(source, read='postgres').sql('doris', unsupported_level=RAISE) 生成，再调用 execute_query/compare_probe；源目标均为 dsv_wf_agg001_s01，10秒超时、10000行上限。所有目标 SQL 来自本轮生成器，不用独立手写候选替代验收。

123 条变体全部成功；执行状态、字段数量/名称、已取得的逻辑类型与类型声明、行数、值及重复次数、需要的最终顺序全部一致。每端另重跑一次，状态/字段/完整有限结果均稳定。无最终 ORDER BY 按多重集合保留重复次数；集合查询的列名额外从真实元数据核对，未将工具的“集合别名尚未检查”当通过。没有放宽浮点或文本比较规则。

| 分组 | 条数 | 范围 / 结果 |
| :--- | ---: | :--- |
| 新组合网格 | 32 | start/end 各取1、3、CAST(NULL AS INT)，step取1、-1、0、CAST(NULL AS INT)，排除4条全部非NULL且步长0的负向；24条含NULL、8条普通整数对照，全部通过 |
| 新 NULL 边界 | 11 | 默认步长、裸NULL、多NULL、全参数的typed NULL、NULL与零步长、INT4极值；全部通过 |
| 新上下文 | 15 | COUNT/SUM空输入、限定/带引号/星号/number列名、LEFT/RIGHT JOIN、重复UNION ALL、CTE、标量子查询、窗口、非NULL INT CAST及空CROSS JOIN；全部通过 |
| 前轮整数/上下文回归 | 65 | 原45条小整数网格、6条默认/INT边界和14条上下文，含1001行；全部通过，详见前轮定义 |

新增58条中，48条使用 NULL 运行时路径，10条为非NULL对照；前轮65条继续 NUMBERS 路径。最大实际结果1001行，比较取得的是完整结果；下表样本最多5行，不用截断样本作比较。

| 变体 | 完整源 SELECT | 实际目标路径 | 源/目标行数 | 原生类型声明 | Doris实际记录（最多5行） |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `SELECT x AS value FROM generate_series(1,1,1) g(x) ORDER BY x` | NUMBERS | 1 / 1 | int4→int | `[[1]]` |
| 2 | `SELECT x AS value FROM generate_series(1,1,-1) g(x) ORDER BY x` | NUMBERS | 1 / 1 | int4→int | `[[1]]` |
| 3 | `SELECT x AS value FROM generate_series(1,1,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 4 | `SELECT x AS value FROM generate_series(1,3,1) g(x) ORDER BY x` | NUMBERS | 3 / 3 | int4→int | `[[1],[2],[3]]` |
| 5 | `SELECT x AS value FROM generate_series(1,3,-1) g(x) ORDER BY x` | NUMBERS | 0 / 0 | int4→int | `[]` |
| 6 | `SELECT x AS value FROM generate_series(1,3,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 7 | `SELECT x AS value FROM generate_series(1,CAST(NULL AS INT),1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 8 | `SELECT x AS value FROM generate_series(1,CAST(NULL AS INT),-1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 9 | `SELECT x AS value FROM generate_series(1,CAST(NULL AS INT),0) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 10 | `SELECT x AS value FROM generate_series(1,CAST(NULL AS INT),CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 11 | `SELECT x AS value FROM generate_series(3,1,1) g(x) ORDER BY x` | NUMBERS | 0 / 0 | int4→int | `[]` |
| 12 | `SELECT x AS value FROM generate_series(3,1,-1) g(x) ORDER BY x` | NUMBERS | 3 / 3 | int4→int | `[[1],[2],[3]]` |
| 13 | `SELECT x AS value FROM generate_series(3,1,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 14 | `SELECT x AS value FROM generate_series(3,3,1) g(x) ORDER BY x` | NUMBERS | 1 / 1 | int4→int | `[[3]]` |
| 15 | `SELECT x AS value FROM generate_series(3,3,-1) g(x) ORDER BY x` | NUMBERS | 1 / 1 | int4→int | `[[3]]` |
| 16 | `SELECT x AS value FROM generate_series(3,3,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 17 | `SELECT x AS value FROM generate_series(3,CAST(NULL AS INT),1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 18 | `SELECT x AS value FROM generate_series(3,CAST(NULL AS INT),-1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 19 | `SELECT x AS value FROM generate_series(3,CAST(NULL AS INT),0) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 20 | `SELECT x AS value FROM generate_series(3,CAST(NULL AS INT),CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 21 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),1,1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 22 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),1,-1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 23 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),1,0) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 24 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),1,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 25 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),3,1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 26 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),3,-1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 27 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),3,0) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 28 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),3,CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 29 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),CAST(NULL AS INT),1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 30 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),CAST(NULL AS INT),-1) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 31 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),CAST(NULL AS INT),0) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 32 | `SELECT x AS value FROM generate_series(CAST(NULL AS INT),CAST(NULL AS INT),CAST(NULL AS INT)) g(x) ORDER BY x` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 33 | `SELECT * FROM generate_series(NULL,3)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 34 | `SELECT * FROM generate_series(1,NULL)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 35 | `SELECT * FROM generate_series(1,3,NULL)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 36 | `SELECT * FROM generate_series(NULL,NULL,1)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 37 | `SELECT * FROM generate_series(CAST(NULL AS INT),NULL,NULL)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 38 | `SELECT * FROM generate_series(NULL,2147483647,1)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 39 | `SELECT * FROM generate_series(-2147483648,NULL,1)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 40 | `SELECT * FROM generate_series(-2147483648,2147483647,NULL)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 41 | `SELECT * FROM generate_series(NULL,-2147483648,-1)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 42 | `SELECT * FROM generate_series(2147483647,NULL,-2147483648)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 43 | `SELECT * FROM generate_series(NULL,3,0)` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 44 | `SELECT COUNT(*) AS n FROM generate_series(NULL,3)` | 运行时 NULL 路径 | 1 / 1 | int8→bigint | `[[0]]` |
| 45 | `SELECT SUM(x) AS s, COUNT(x) AS n FROM generate_series(1,3,NULL) g(x)` | 运行时 NULL 路径 | 1 / 1 | int8→bigint；int8→bigint | `[[null,0]]` |
| 46 | `SELECT g, g.g FROM generate_series(NULL,3) AS g` | 运行时 NULL 路径 | 0 / 0 | int4→int；int4→int | `[]` |
| 47 | `SELECT "S"."V" AS "Value" FROM generate_series(NULL,3) "S"("V") ORDER BY "Value"` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 48 | `SELECT g.* FROM generate_series(NULL,3) g` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 49 | `SELECT a,b FROM generate_series(1,3) a LEFT JOIN generate_series(NULL,3) b ON a=b ORDER BY a` | 运行时 NULL 路径 | 3 / 3 | int4→int；int4→int | `[[1,null],[2,null],[3,null]]` |
| 50 | `SELECT a,b FROM generate_series(NULL,3) a RIGHT JOIN generate_series(1,3) b ON a=b ORDER BY b` | 运行时 NULL 路径 | 3 / 3 | int4→int；int4→int | `[[null,1],[null,2],[null,3]]` |
| 51 | `SELECT x AS v FROM generate_series(NULL,3) g(x) UNION ALL SELECT x AS v FROM generate_series(1,2) g(x) UNION ALL SELECT x AS v FROM generate_series(1,2) g(x)` | 运行时 NULL 路径 | 4 / 4 | int4→int | `[[1],[2],[1],[2]]` |
| 52 | `WITH c AS (SELECT x FROM generate_series(NULL,3) g(x)) SELECT COUNT(*) AS n FROM c` | 运行时 NULL 路径 | 1 / 1 | int8→bigint | `[[0]]` |
| 53 | `SELECT (SELECT COUNT(*) FROM generate_series(NULL,3)) AS n` | 运行时 NULL 路径 | 1 / 1 | int8→bigint | `[[0]]` |
| 54 | `SELECT g AS v, ROW_NUMBER() OVER (ORDER BY g) AS rn FROM generate_series(NULL,3) g ORDER BY v` | 运行时 NULL 路径 | 0 / 0 | int4→int；int8→bigint | `[]` |
| 55 | `SELECT number FROM generate_series(NULL,3) g(number) ORDER BY number` | 运行时 NULL 路径 | 0 / 0 | int4→int | `[]` |
| 56 | `SELECT x AS v FROM generate_series(CAST(1 AS INT),CAST(3 AS INT)) g(x) ORDER BY x` | NUMBERS | 3 / 3 | int4→int | `[[1],[2],[3]]` |
| 57 | `SELECT g AS v FROM generate_series(CAST(3 AS INT),CAST(1 AS INT),CAST(-1 AS INT)) g ORDER BY g` | NUMBERS | 3 / 3 | int4→int | `[[1],[2],[3]]` |
| 58 | `SELECT COUNT(*) AS n FROM generate_series(NULL,3) g CROSS JOIN generate_series(1,3) b` | 运行时 NULL 路径 | 1 / 1 | int8→bigint | `[[0]]` |

上表所有变体的字段名称、类型声明、值/重复次数与要求顺序均通过，不以空行数掩盖字段类型差异。NULL步长与零步长不同；前者属于成功源，后者仅在其他参数NULL时有成功源结果。排序稳定不证明任意排序键唯一；本次有序序列和JOIN使用对应序列键。

<details>
<summary>新增58条变体的实际生成 Doris SQL（编号对应上表）</summary>

以下分隔注释用于阅读，实际均经只读检查后逐条执行，不作为多语句脚本运行。

```sql
-- 变体 1，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '1')) AS g ORDER BY x NULLS LAST

-- 变体 2，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + number * -1 AS INT) AS x FROM NUMBERS('number' = '1')) AS g ORDER BY x NULLS LAST

-- 变体 3，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR 1 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 1 <= 1) OR (CAST(NULL AS INT) < 0 AND 1 >= 1) THEN (CAST(1 AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 4，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '3')) AS g ORDER BY x NULLS LAST

-- 变体 5，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + number * -1 AS INT) AS x FROM NUMBERS('number' = '0')) AS g ORDER BY x NULLS LAST

-- 变体 6，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR 3 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 1 <= 3) OR (CAST(NULL AS INT) < 0 AND 1 >= 3) THEN (CAST(3 AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 7，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR CAST(NULL AS INT) IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND 1 <= CAST(NULL AS INT)) OR (1 < 0 AND 1 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 8，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * -1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR CAST(NULL AS INT) IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND 1 <= CAST(NULL AS INT)) OR ((-1) < 0 AND 1 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 9，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * 0 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR CAST(NULL AS INT) IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND 1 <= CAST(NULL AS INT)) OR (0 < 0 AND 1 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 10，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(1 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 1 <= CAST(NULL AS INT)) OR (CAST(NULL AS INT) < 0 AND 1 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 11，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + number * 1 AS INT) AS x FROM NUMBERS('number' = '0')) AS g ORDER BY x NULLS LAST

-- 变体 12，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + number * -1 AS INT) AS x FROM NUMBERS('number' = '3')) AS g ORDER BY x NULLS LAST

-- 变体 13，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR 1 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 3 <= 1) OR (CAST(NULL AS INT) < 0 AND 3 >= 1) THEN (CAST(1 AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 14，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + number * 1 AS INT) AS x FROM NUMBERS('number' = '1')) AS g ORDER BY x NULLS LAST

-- 变体 15，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + number * -1 AS INT) AS x FROM NUMBERS('number' = '1')) AS g ORDER BY x NULLS LAST

-- 变体 16，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR 3 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 3 <= 3) OR (CAST(NULL AS INT) < 0 AND 3 >= 3) THEN (CAST(3 AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 17，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR CAST(NULL AS INT) IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND 3 <= CAST(NULL AS INT)) OR (1 < 0 AND 3 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 18，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * -1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR CAST(NULL AS INT) IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND 3 <= CAST(NULL AS INT)) OR ((-1) < 0 AND 3 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 19，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * 0 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR CAST(NULL AS INT) IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND 3 <= CAST(NULL AS INT)) OR (0 < 0 AND 3 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 20，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(3 + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 3 IS NULL OR CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND 3 <= CAST(NULL AS INT)) OR (CAST(NULL AS INT) < 0 AND 3 >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(3 AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 21，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 1 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND CAST(NULL AS INT) <= 1) OR (1 < 0 AND CAST(NULL AS INT) >= 1) THEN (CAST(1 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 22，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * -1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 1 IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND CAST(NULL AS INT) <= 1) OR ((-1) < 0 AND CAST(NULL AS INT) >= 1) THEN (CAST(1 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 23，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 0 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 1 IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND CAST(NULL AS INT) <= 1) OR (0 < 0 AND CAST(NULL AS INT) >= 1) THEN (CAST(1 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 24，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 1 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND CAST(NULL AS INT) <= 1) OR (CAST(NULL AS INT) < 0 AND CAST(NULL AS INT) >= 1) THEN (CAST(1 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 25，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND CAST(NULL AS INT) <= 3) OR (1 < 0 AND CAST(NULL AS INT) >= 3) THEN (CAST(3 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 26，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * -1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 3 IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND CAST(NULL AS INT) <= 3) OR ((-1) < 0 AND CAST(NULL AS INT) >= 3) THEN (CAST(3 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 27，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 0 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 3 IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND CAST(NULL AS INT) <= 3) OR (0 < 0 AND CAST(NULL AS INT) >= 3) THEN (CAST(3 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 28，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR 3 IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND CAST(NULL AS INT) <= 3) OR (CAST(NULL AS INT) < 0 AND CAST(NULL AS INT) >= 3) THEN (CAST(3 AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 29，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND CAST(NULL AS INT) <= CAST(NULL AS INT)) OR (1 < 0 AND CAST(NULL AS INT) >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 30，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * -1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND CAST(NULL AS INT) <= CAST(NULL AS INT)) OR ((-1) < 0 AND CAST(NULL AS INT) >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 31，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * 0 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND CAST(NULL AS INT) <= CAST(NULL AS INT)) OR (0 < 0 AND CAST(NULL AS INT) >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 32，对应上表源 SQL；以下为实际生成结果。
SELECT x AS `value` FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * CAST(NULL AS INT) AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL OR CAST(NULL AS INT) IS NULL THEN 0 WHEN (CAST(NULL AS INT) > 0 AND CAST(NULL AS INT) <= CAST(NULL AS INT)) OR (CAST(NULL AS INT) < 0 AND CAST(NULL AS INT) >= CAST(NULL AS INT)) THEN (CAST(CAST(NULL AS INT) AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(CAST(NULL AS INT), 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY x NULLS LAST

-- 变体 33，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 34，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(1 + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR NULL IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND 1 <= NULL) OR (1 < 0 AND 1 >= NULL) THEN (CAST(NULL AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 35，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(1 + _numbers.number * NULL AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR 3 IS NULL OR NULL IS NULL THEN 0 WHEN (NULL > 0 AND 1 <= 3) OR (NULL < 0 AND 1 >= 3) THEN (CAST(3 AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(NULL, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 36，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR NULL IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= NULL) OR (1 < 0 AND NULL >= NULL) THEN (CAST(NULL AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 37，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(CAST(NULL AS INT) + _numbers.number * NULL AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN CAST(NULL AS INT) IS NULL OR NULL IS NULL OR NULL IS NULL THEN 0 WHEN (NULL > 0 AND CAST(NULL AS INT) <= NULL) OR (NULL < 0 AND CAST(NULL AS INT) >= NULL) THEN (CAST(NULL AS BIGINT) - CAST(CAST(NULL AS INT) AS BIGINT)) DIV NULLIF(NULL, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 38，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 2147483647 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 2147483647) OR (1 < 0 AND NULL >= 2147483647) THEN (CAST(2147483647 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 39，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(-2147483648 + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN (-2147483648) IS NULL OR NULL IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND (-2147483648) <= NULL) OR (1 < 0 AND (-2147483648) >= NULL) THEN (CAST(NULL AS BIGINT) - CAST(-2147483648 AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 40，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(-2147483648 + _numbers.number * NULL AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN (-2147483648) IS NULL OR 2147483647 IS NULL OR NULL IS NULL THEN 0 WHEN (NULL > 0 AND (-2147483648) <= 2147483647) OR (NULL < 0 AND (-2147483648) >= 2147483647) THEN (CAST(2147483647 AS BIGINT) - CAST(-2147483648 AS BIGINT)) DIV NULLIF(NULL, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 41，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(NULL + _numbers.number * -1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR (-2147483648) IS NULL OR (-1) IS NULL THEN 0 WHEN ((-1) > 0 AND NULL <= (-2147483648)) OR ((-1) < 0 AND NULL >= (-2147483648)) THEN (CAST(-2147483648 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(-1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 42，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(2147483647 + _numbers.number * -2147483648 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 2147483647 IS NULL OR NULL IS NULL OR (-2147483648) IS NULL THEN 0 WHEN ((-2147483648) > 0 AND 2147483647 <= NULL) OR ((-2147483648) < 0 AND 2147483647 >= NULL) THEN (CAST(NULL AS BIGINT) - CAST(2147483647 AS BIGINT)) DIV NULLIF(-2147483648, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 43，对应上表源 SQL；以下为实际生成结果。
SELECT * FROM (SELECT CAST(NULL + _numbers.number * 0 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 0 IS NULL THEN 0 WHEN (0 > 0 AND NULL <= 3) OR (0 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(0, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 44，对应上表源 SQL；以下为实际生成结果。
SELECT COUNT(*) AS n FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series

-- 变体 45，对应上表源 SQL；以下为实际生成结果。
SELECT SUM(x) AS s, COUNT(x) AS n FROM (SELECT CAST(1 + _numbers.number * NULL AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN 1 IS NULL OR 3 IS NULL OR NULL IS NULL THEN 0 WHEN (NULL > 0 AND 1 <= 3) OR (NULL < 0 AND 1 >= 3) THEN (CAST(3 AS BIGINT) - CAST(1 AS BIGINT)) DIV NULLIF(NULL, 0) + 1 ELSE 0 END) _numbers AS number) AS g

-- 变体 46，对应上表源 SQL；以下为实际生成结果。
SELECT g, g.g FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS g FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g

-- 变体 47，对应上表源 SQL；以下为实际生成结果。
SELECT `S`.`V` AS `Value` FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS `V` FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS `S` ORDER BY `Value` NULLS LAST

-- 变体 48，对应上表源 SQL；以下为实际生成结果。
SELECT g.* FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS g FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g

-- 变体 49，对应上表源 SQL；以下为实际生成结果。
SELECT a, b FROM (SELECT CAST(1 + number * 1 AS INT) AS a FROM NUMBERS('number' = '3')) AS a LEFT JOIN (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS b FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS b ON a = b ORDER BY a NULLS LAST

-- 变体 50，对应上表源 SQL；以下为实际生成结果。
SELECT a, b FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS a FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS a RIGHT JOIN (SELECT CAST(1 + number * 1 AS INT) AS b FROM NUMBERS('number' = '3')) AS b ON a = b ORDER BY b NULLS LAST

-- 变体 51，对应上表源 SQL；以下为实际生成结果。
SELECT x AS v FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g UNION ALL SELECT x AS v FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '2')) AS g UNION ALL SELECT x AS v FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '2')) AS g

-- 变体 52，对应上表源 SQL；以下为实际生成结果。
WITH c AS (SELECT x FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS x FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g) SELECT COUNT(*) AS n FROM c

-- 变体 53，对应上表源 SQL；以下为实际生成结果。
SELECT (SELECT COUNT(*) FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS generate_series FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS generate_series) AS n

-- 变体 54，对应上表源 SQL；以下为实际生成结果。
SELECT g AS v, ROW_NUMBER() OVER (ORDER BY g NULLS LAST) AS rn FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS g FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY v NULLS LAST

-- 变体 55，对应上表源 SQL；以下为实际生成结果。
SELECT number FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS number FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g ORDER BY number NULLS LAST

-- 变体 56，对应上表源 SQL；以下为实际生成结果。
SELECT x AS v FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '3')) AS g ORDER BY x NULLS LAST

-- 变体 57，对应上表源 SQL；以下为实际生成结果。
SELECT g AS v FROM (SELECT CAST(3 + number * -1 AS INT) AS g FROM NUMBERS('number' = '3')) AS g ORDER BY g NULLS LAST

-- 变体 58，对应上表源 SQL；以下为实际生成结果。
SELECT COUNT(*) AS n FROM (SELECT CAST(NULL + _numbers.number * 1 AS INT) AS g FROM (SELECT 1 AS seed) AS _series LATERAL VIEW EXPLODE_NUMBERS(CASE WHEN NULL IS NULL OR 3 IS NULL OR 1 IS NULL THEN 0 WHEN (1 > 0 AND NULL <= 3) OR (1 < 0 AND NULL >= 3) THEN (CAST(3 AS BIGINT) - CAST(NULL AS BIGINT)) DIV NULLIF(1, 0) + 1 ELSE 0 END) _numbers AS number) AS g CROSS JOIN (SELECT CAST(1 + number * 1 AS INT) AS b FROM NUMBERS('number' = '3')) AS b
```

</details>

## 4. 非 NULL 零步长与不支持范围

两条直接相关负向控制实测：

| 源 SELECT | 源结果 | 修改后转译 / 目标执行 |
| :--- | :--- | :--- |
| `SELECT * FROM generate_series(1,3,0)` | SQLSTATE 22023：step size cannot equal zero | UnsupportedError: Doris GENERATE_SERIES requires constant INT-compatible table arguments without LATERAL or WITH ORDINALITY; zero step on non-NULL inputs is unsupported；目标未执行 |
| `SELECT * FROM generate_series(CAST(1 AS INT),3,CAST(0 AS INT))` | SQLSTATE 22023：step size cannot equal zero | UnsupportedError: Doris GENERATE_SERIES requires constant INT-compatible table arguments without LATERAL or WITH ORDINALITY; zero step on non-NULL inputs is unsupported；目标未执行 |

不要求复制 PG 错误全文，不把负向拒绝算成功匹配。BIGINT/Decimal typed NULL、浮点、超出INT4、字符串、Boolean、未绑定参数、NULLIF及相关列仍有 UnsupportedError 单测。NULL+零步长的成功源已在组合与边界实际验证，不再误拒绝。

## 5. 原 Case 与既有匹配回归

于 2026-11-23T11:02:13.364770+00:00 按原16阶段 YAML，通过一个 Python 进程内逐阶段 CliRunner 调用 run --path <阶段YAML> --stdout --id ...，没有保存新的验证JSON。130条唯一原查询结果与fix-008一致：80匹配、28 Doris执行失败、17行值/顺序不同、1转译失败、4源端负向；80个匹配Case ID全部保持，新增/丢失匹配均为0。既有72条也包含在80中，未另增分母。

32条task-008关联原查询的 .out 仍全部记录源成功：8匹配、3值差异、20 Doris失败、1转译失败。31条可生成SQL与fix-008报告逐字相同；0136仍是 ARRAY子查询 UnsupportedError。这32条的序列参数都没有NULL，故本轮补齐NULL不会使它们新增MATCH。首轮 .out/SQL/YAML/JSON和比较器保持；原聚合NULL参数不是序列表函数NULL参数，二者不混淆。

当前32条的框架观察如下，原SQL/实际生成SQL/类型限制沿链接保留。本轮没有重新执行每条实时PG或重新声称32条原生类型全部一致；类型补证来自本轮123条边界及前轮已有证据。原 .out 与实时PG的7条统计冲突不静默替换，仍见fix-008。

| 原 Case | 本轮 run 结果 | 实际差异 / 错误 |
| :--- | :--- | :--- |
| [pg-aggregates-0051-6f50d445](../../../../attribution/cases/aggregates-001/pg-aggregates-0051-6f50d445.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0052-57717b1c](../../../../attribution/cases/aggregates-001/pg-aggregates-0052-57717b1c.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0053-80bc631f](../../../../attribution/cases/aggregates-001/pg-aggregates-0053-80bc631f.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0054-9d43ca75](../../../../attribution/cases/aggregates-001/pg-aggregates-0054-9d43ca75.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0055-a2bc4e59](../../../../attribution/cases/aggregates-001/pg-aggregates-0055-a2bc4e59.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0056-ed925b77](../../../../attribution/cases/aggregates-001/pg-aggregates-0056-ed925b77.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0057-54488b60](../../../../attribution/cases/aggregates-001/pg-aggregates-0057-54488b60.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0058-774c37d9](../../../../attribution/cases/aggregates-001/pg-aggregates-0058-774c37d9.md) | 匹配 | 原 .out 匹配，未据此增加原生类型结论 |
| [pg-aggregates-0059-6e8dac37](../../../../attribution/cases/aggregates-001/pg-aggregates-0059-6e8dac37.md) | 行值或顺序不匹配 | 值/显示差异：{"row_order":"忽略顺序，保留重复次数","source_only":[{"row":["NaN"],"extra_count":1}],"doris_only":[{"row":[""],"extra_count":1}],"source_extra_rows":1,"doris_extra_rows":1,"omitted_distinct_rows":0} |
| [pg-aggregates-0060-10dc4c9b](../../../../attribution/cases/aggregates-001/pg-aggregates-0060-10dc4c9b.md) | 行值或顺序不匹配 | 值/显示差异：{"row_order":"忽略顺序，保留重复次数","source_only":[{"row":["NaN"],"extra_count":1}],"doris_only":[{"row":[""],"extra_count":1}],"source_extra_rows":1,"doris_extra_rows":1,"omitted_distinct_rows":0} |
| [pg-aggregates-0085-b2d1da4b](../../../../attribution/cases/aggregates-001/pg-aggregates-0085-b2d1da4b.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0086-94d0e96a](../../../../attribution/cases/aggregates-001/pg-aggregates-0086-94d0e96a.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0087-c50d900b](../../../../attribution/cases/aggregates-001/pg-aggregates-0087-c50d900b.md) | 行值或顺序不匹配 | 值/显示差异：{"row_order":"忽略顺序，保留重复次数","source_only":[{"row":[""],"extra_count":1}],"doris_only":[{"row":["0.0"],"extra_count":1}],"source_extra_rows":1,"doris_extra_rows":1,"omitted_distinct_rows":0} |
| [pg-aggregates-0093-d3a22e61](../../../../attribution/cases/aggregates-001/pg-aggregates-0093-d3a22e61.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0094-75ff7206](../../../../attribution/cases/aggregates-001/pg-aggregates-0094-75ff7206.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0095-5046511e](../../../../attribution/cases/aggregates-001/pg-aggregates-0095-5046511e.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0098-b1e5567b](../../../../attribution/cases/aggregates-001/pg-aggregates-0098-b1e5567b.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0099-bed0f6ec](../../../../attribution/cases/aggregates-001/pg-aggregates-0099-bed0f6ec.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0100-3b815f6a](../../../../attribution/cases/aggregates-001/pg-aggregates-0100-3b815f6a.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0101-7fc3b3aa](../../../../attribution/cases/aggregates-001/pg-aggregates-0101-7fc3b3aa.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'REGR_R2'") |
| [pg-aggregates-0134-429eb1f7](../../../../attribution/cases/aggregates-001/pg-aggregates-0134-429eb1f7.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nmissing 'UNNEST' at '('(line 1, pos 110)\n") |
| [pg-aggregates-0136-4243166e](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md) | SQLGlot 转译失败 | UnsupportedError: Doris does not support ARRAY subquery constructors |
| [pg-aggregates-0276-0f1f5154](../../../../attribution/cases/aggregates-001/pg-aggregates-0276-0f1f5154.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 53)\n\n== SQL ==\nSELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)\n-----------------------------------------------------^^^\n") |
| [pg-aggregates-0293-3e365a0a](../../../../attribution/cases/aggregates-001/pg-aggregates-0293-3e365a0a.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'AGGFSTR'") |
| [pg-aggregates-0294-5412623b](../../../../attribution/cases/aggregates-001/pg-aggregates-0294-5412623b.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'") |
| [pg-aggregates-0295-bf759c5f](../../../../attribution/cases/aggregates-001/pg-aggregates-0295-bf759c5f.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'AGGFSTR'") |
| [pg-aggregates-0296-a77bafc5](../../../../attribution/cases/aggregates-001/pg-aggregates-0296-a77bafc5.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'") |
| [pg-aggregates-0299-d52780a5](../../../../attribution/cases/aggregates-001/pg-aggregates-0299-d52780a5.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = Can not found function 'AGGFNS'") |
| [pg-aggregates-0398-73d63cba](../../../../attribution/cases/aggregates-001/pg-aggregates-0398-73d63cba.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 42)\n") |
| [pg-aggregates-0413-6ccabd9a](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 97)\n") |
| [pg-aggregates-0427-1ad928b9](../../../../attribution/cases/aggregates-001/pg-aggregates-0427-1ad928b9.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 30)\n") |
| [pg-aggregates-0428-5c5a2a90](../../../../attribution/cases/aggregates-001/pg-aggregates-0428-5c5a2a90.md) | Doris 执行失败 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 36)\n") |

## 6. 单元测试与验收

先补测试时，新NULL方法产生8个UnsupportedError失败，复现前轮缺口；实现后通过。INT/BIGINT等边界和不修改源AST、目标round-trip均纳入单测；无源AST的手工类型注入。未安装或升级依赖。

| 实际命令，工作目录 ../sqlglot-experiment | 结果 |
| :--- | :--- |
| .venv/bin/python -m unittest tests.dialects.test_doris.TestDoris.test_integer_generate_series_nulls tests.dialects.test_doris.TestDoris.test_integer_generate_series_nullable_scope tests.dialects.test_doris.TestDoris.test_integer_generate_series tests.dialects.test_doris.TestDoris.test_integer_generate_series_exclusions | 4个方法通过 |
| PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql | 154个方法通过 |
| 同PATH/解释器：python -m unittest discover -s tests/dialects | 1077个方法通过，含上述154，不相加 |
| 同PATH/解释器：python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens | 233个方法通过 |
| Ruff check / format --check，六个累积修改文件；git diff --check | 通过 |

未运行完整make check、C扩展、mypy或DuckDB executor/optimizer全套。没有将未运行写通过。对全INT4大范围保留NUMBERS静态路径，前轮4294967296行仅生成测试，本轮也未执行；NULL边界即使另一端是INT4极值也先得到零长度，不分配大数组。运行时EXPLODE路径不作为动态长度/任意大序列的支持承诺。

本轮补齐NULL，并重新验证既有主路径、别名/字段、INT类型、空区间和关联匹配查询，**task-008 转为已修复并完成约定验收**。原Case的统计返回类型、NaN/CORR、缺少REGR_R2、自定义聚合、LATERAL、派生表别名、ARRAY子查询和WITHIN GROUP仍按既有研究/任务处理，不混入序列实现。

全批仍未完成：task-001/003未全验收，task-009未处理，研究/前提/导入遗漏与全43阶段最终回归仍保留。下一独立任务建议 task-009（REGR_COUNT），本轮没有开始。未提交、未推送，不创建社区Issue/PR。

