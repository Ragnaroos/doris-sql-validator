# task-003：ARRAY_AGG 保留 NULL 与空输入补偿

## 1. 结论与范围

**已修改但未完成验收。** 普通 PostgreSQL ARRAY_AGG 的 NULL/空输入规则已实现并实际运行；原代表查询的数组元素类型仍不同，嵌套声明/精度和部分完整行值比较不能标为全部通过。

入口：[task-003](../../../../attribution/aggregates-001-attribution-summary.md#task-003)；本轮为 fix-003，仅修这一项，代码身份、权限和共同回归见[汇总](../../../aggregates-001-fix-003-summary.md)。没有 commit/push，没有修改验证框架或数据。

纳入普通非窗口、非 FILTER、没有聚合内部 ORDER BY 的 ARRAY_AGG，含 DISTINCT、空输入、运行时 NULL 和重复元素。排序、整行复合值、数组维度、类型推断、时间精度和返回文本格式不顺带修改。关联 10 条不等于本轮能让 10 条全通过；仍逐条运行和保留剩余错误。

## 2. 为什么不能只改函数名

修复前在当前 checkout 实际运行：

```sql
SELECT ARRAY_AGG(a) AS value
FROM (VALUES (CAST(1 AS INT)), (CAST(NULL AS INT)), (CAST(2 AS INT))) v(a);
```

旧生成 SQL 为：

```sql
SELECT COLLECT_LIST(a) AS `value` FROM (SELECT CAST(1 AS INT) AS a UNION ALL SELECT CAST(NULL AS INT) UNION ALL SELECT CAST(2 AS INT)) AS v
```

PG 为 `[1,NULL,2]`，Doris 为 `[1,2]`。全 NULL 两行时，PG `[NULL,NULL]`、旧目标 `[]`；没有任何输入行时，PG SQL NULL、旧目标 `[]`。

[Doris COLLECT_LIST](https://doris.apache.org/docs/3.x/sql-manual/sql-functions/aggregate-functions/collect-list/) 说明会过滤 NULL；[PostgreSQL 聚合文档](https://www.postgresql.org/docs/18/functions-aggregate.html) 说明 ARRAY_AGG 无输入行返回 NULL。实际数据库还确认，Doris ARRAY_AGG 保留 NULL，但空输入仍为 []，所以改名不够。

本轮对照验证 `NULLIF(ARRAY_AGG(a), ARRAY())`：空输入变 SQL NULL，全 NULL 两行仍为 `[NULL,NULL]`，普通输入和重复元素不删除。使用聚合结果和空数组比较，不额外添加 COUNT(*)，避免为此新引入一个可能有不同相关归属的聚合；不宣称所有相关查询已支持。

## 3. 实际代码和测试

| 文件 / 方法 | 改动和原因 |
| :--- | :--- |
| [expressions/aggregate.py](../../../../../../sqlglot-experiment/sqlglot/expressions/aggregate.py)：ArrayAgg | 新增可选 null_on_empty 语义字段，记录明确的“无输入行应返回 SQL NULL”要求；字段说明不把 NULL 元素和空输入混淆 |
| [parsers/postgres.py](../../../../../../sqlglot-experiment/sqlglot/parsers/postgres.py)：FUNCTIONS[ARRAY_AGG] | 设置 null_on_empty=True；不靠目标 Generator 猜输入方言，不要求 Schema |
| [generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py)：arrayagg_sql / TRANSFORMS | 去除继承的 ArrayAgg 简单映射，使专用方法生效。普通保留 NULL 的聚合用 ARRAY_AGG；PG 明确空输入要求时外包 NULLIF；nulls_excluded=True 继续 COLLECT_LIST |
| 同生成方法的排除检查 | 遇内部 Order、最近作用域内 Window/Filter/WithinGroup，保留旧 COLLECT_LIST 生成路径，不声称本轮已修这些能力；检查到 Select 就停止向外找祖先 |
| [test_doris.py](../../../../../../sqlglot-experiment/tests/dialects/test_doris.py) | 2 个新方法：普通/DISTINCT、CAST、分组/多聚合、HAVING、标量子查询、严格生成/往返、原生 Doris 与 Hive/Spark 保持，排除上下文不变 |
| [test_postgres.py](../../../../../../sqlglot-experiment/tests/dialects/test_postgres.py) | 新方法核对 PG AST 标志、PG 原样生成和 PG→MySQL 既有输出不变 |

最终生成通过 self.func 组合原生函数；空 ARRAY() 不借用 task-001 的 array_sql，因此普通列聚合没有新增对数组字面量修复的实现依赖。重新用 Doris Parser 读取生成 SQL 时，原生 ARRAY_AGG 没有 PG 标志，不重复套 NULLIF，也不改变其原生空数组结果。没有把所有元素强制 CAST INT 或在框架里改 SQL。

```sql
-- PostgreSQL
SELECT ARRAY_AGG(a) FROM t;
SELECT ARRAY_AGG(DISTINCT a) FROM t;

-- 最终修改后的 SQLGlot 实际生成
SELECT NULLIF(ARRAY_AGG(a), ARRAY()) FROM t;
SELECT NULLIF(ARRAY_AGG(DISTINCT a), ARRAY()) FROM t;
```

本轮新增语义字段当前由 PG Parser 设置、Doris Generator 消费；不宣称其他来源/目标的空输入兼容也都已实现。原 task-001/002 代码未撤回或合并提交。

## 4. 原查询执行

使用固定 stage-17 的 9 条和 stage-30 的 1 条。通过 CliRunner 真正调用 `run --path <对应 YAML> --stdout --id <id> ...`，每阶段一次；再用 SqlglotTranspiler.transpile_case 生成目标，pg_probe.execute_query / compare_probe 补证。不是把旧报告重新统计，也不是执行手写候选冒充修复验证。

全部 10 条实时 PG 成功；另执行 `SELECT CAST(c0 AS TEXT) FROM (<原文>) checked(c0)`，与各自原 .out 对应文本行一致。原查询都没有最终 ORDER BY，这项包装核对不证明数组顺序在所有计划中固定。时间为 2026-11-23 08:58:22–08:58:23 UTC；最终实现另于 09:03:43–09:03:47 UTC 重跑原 CLI 范围。

### 4.1 原文和最终实际生成 SQL

```sql
-- 0276：stage-17
select array_agg(distinct val)
from (select null as val from generate_series(1, 2));
-- 目标
SELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM GENERATE_SERIES(1, 2));

-- 0283：stage-17，不同排序键
select array_agg(a order by b) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 目标
SELECT COLLECT_LIST(a ORDER BY b NULLS LAST) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- 0284：stage-17
select array_agg(a order by a) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 目标
SELECT COLLECT_LIST(a ORDER BY a NULLS LAST) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- 0285：stage-17
select array_agg(a order by a desc) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 目标
SELECT COLLECT_LIST(a ORDER BY a DESC NULLS FIRST) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- 0286：stage-17，不同排序键
select array_agg(b order by a desc) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 目标
SELECT COLLECT_LIST(b ORDER BY a DESC NULLS FIRST) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- 0287：stage-17
select array_agg(distinct a) from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 目标
SELECT NULLIF(ARRAY_AGG(DISTINCT a), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- 0288：stage-17
select array_agg(distinct a order by a) from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 目标
SELECT COLLECT_LIST(DISTINCT a ORDER BY a NULLS LAST) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- 0289：stage-17
select array_agg(distinct a order by a desc) from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 目标
SELECT COLLECT_LIST(DISTINCT a ORDER BY a DESC NULLS FIRST) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- 0290：stage-17
select array_agg(distinct a order by a desc nulls last) from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 目标
SELECT COLLECT_LIST(DISTINCT a ORDER BY a DESC) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- 0371：stage-30，整行聚合和数组维度
select array_dims(array_agg(s)) from (select * from pagg_test) s;
-- 目标
SELECT ARRAY_DIMS(NULLIF(ARRAY_AGG(s), ARRAY())) FROM (SELECT * FROM pagg_test) AS s;
```

上面为阅读并列展示，实际每条单独只读执行；原文位置/大小写/换行以原 YAML 和各 Case 第 2 节为准，没有改写原文件。

| 原 Case | 本轮完整结果及具体剩余问题 |
| :--- | :--- |
| [0276](../../../../attribution/cases/aggregates-001/pg-aggregates-0276-0f1f5154.md) | PG `[NULL]`，Doris 报 1105：`mismatched input ',' expecting EQ(line 1, pos 95)`；序列转换仍缺。目标字段/类型/值未比较 |
| [0283](../../../../attribution/cases/aggregates-001/pg-aggregates-0283-9ca01715.md) | PG `[3,4,2,1]`，Doris 报 1105：`collect_list doesn't support order by expression`；不同键排序研究，目标字段/类型/值未比较 |
| [0284](../../../../attribution/cases/aggregates-001/pg-aggregates-0284-628b13e2.md) | PG `[1,2,3,4]`，同上错误；task-004 |
| [0285](../../../../attribution/cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md) | PG `[4,3,2,1]`，同上错误；task-004 |
| [0286](../../../../attribution/cases/aggregates-001/pg-aggregates-0286-c689f198.md) | PG `[2,1,3,4]`，同上错误；不同键排序研究 |
| [0287](../../../../attribution/cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md) | 两端成功，各 1 列/1 行，实时结构化元素 `[1,2,3,NULL]` 一致，各重复一次仍一致；原 .out `{1,2,3,NULL}` 与 Doris `[1, 2, 3, null]` 文本不同。PG _int4 / Doris array<tinyint>：逻辑均数组但元素宽度真正不同；无显式 Alias。未验证所有 DISTINCT 输入的数组顺序 |
| [0288](../../../../attribution/cases/aggregates-001/pg-aggregates-0288-1528b423.md) | PG `[1,2,3,NULL]`，内部排序错误；task-004 |
| [0289](../../../../attribution/cases/aggregates-001/pg-aggregates-0289-64071a98.md) | PG `[NULL,3,2,1]`，内部排序错误；task-004 |
| [0290](../../../../attribution/cases/aggregates-001/pg-aggregates-0290-2bc98abf.md) | PG `[3,2,1,NULL]`，内部排序错误；task-004 |
| [0371](../../../../attribution/cases/aggregates-001/pg-aggregates-0371-e4fde69d.md) | PG `[1:5000]`，Doris 报 1105：`Unknown column 's' in 'table list' in PROJECT clause(line 1, pos 35)`；整行引用和 ARRAY_DIMS 未修，目标类型/值未比较 |

## 5. 22 组固定边界

下表是实际执行的完整 PG SELECT，目标均由本轮 SQLGlot 生成，不人工维护另一份目标答案。普通目标聚合统一生成 `NULLIF(ARRAY_AGG(a), ARRAY())`，DISTINCT 仍放在 ARRAY_AGG 内，源 CAST 和查询结构保留；完整生成示例见第 2/3 节。两端均成功、字段数量和显式别名一致，每组两端各重复一次，端内值/重复次数均稳定。结果行无最终 ORDER BY 时按多重集合比较，**数组内部元素顺序仍保留**。

| 名称 | 完整源 SQL | 实际结果 / 限制 |
| :--- | :--- | :--- |
| int-mixed | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1 AS INT)),(CAST(NULL AS INT)),(CAST(2 AS INT)),(CAST(1 AS INT))) v(a)` | 两端 `[1,NULL,2,1]`，保留 NULL 和重复元素 |
| int-all-null | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(NULL AS INT)),(CAST(NULL AS INT))) v(a)` | `[NULL,NULL]`，不变为空数组或 SQL NULL |
| int-empty | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE` | 两端 1 行 SQL NULL |
| distinct-mixed | `SELECT ARRAY_AGG(DISTINCT a) AS xs FROM (VALUES (CAST(1 AS INT)),(CAST(NULL AS INT)),(CAST(1 AS INT)),(CAST(2 AS INT))) v(a)` | PG `[1,2,NULL]` / Doris `[1,NULL,2]`，当前比较不同；NULL 只保留一次，但未指定元素顺序 |
| distinct-all-null | `SELECT ARRAY_AGG(DISTINCT a) AS xs FROM (VALUES (CAST(NULL AS INT)),(CAST(NULL AS INT))) v(a)` | `[NULL]` |
| distinct-empty | `SELECT ARRAY_AGG(DISTINCT a) AS xs FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE` | 1 行 SQL NULL |
| bigint-boundary | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(9223372036854775807 AS BIGINT)),(CAST(NULL AS BIGINT)),(CAST(-9223372036854775808 AS BIGINT))) v(a)` | 极值/NULL 的完整元素和顺序一致，无浮点化 |
| decimal | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1.20 AS DECIMAL(10,2))),(CAST(NULL AS DECIMAL(10,2))),(CAST(-3.45 AS DECIMAL(10,2)))) v(a)` | 数值 1.20/NULL/-3.45 一致，用 Decimal，不用 Float 容差 |
| decimal-empty | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1.20 AS DECIMAL(10,2)))) v(a) WHERE FALSE` | 1 行 SQL NULL，目标仍为 decimal 数组类型 |
| string-unicode | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST('汉字' AS TEXT)),(CAST('' AS TEXT)),(CAST(NULL AS TEXT)),(CAST('a\|b' AS TEXT))) v(a)` | 汉字、空串、NULL 和含竖线字符串均保留；表格中反斜杠仅转义竖线，实际 SQL 为 `'a|b'` |
| bool | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(TRUE AS BOOLEAN)),(CAST(NULL AS BOOLEAN)),(CAST(FALSE AS BOOLEAN))) v(a)` | PG true/NULL/false，Doris 数组文本为 1/NULL/0；当前归一化仍记不同，后续元素对照见第 6 节 |
| float | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1.5 AS DOUBLE PRECISION)),(CAST(NULL AS DOUBLE PRECISION)),(CAST(-2.5 AS DOUBLE PRECISION))) v(a)` | 元素精确一致，没有放宽容差 |
| date | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST('2024-02-29' AS DATE)),(CAST(NULL AS DATE)),(CAST('2024-03-01' AS DATE))) v(a)` | 闰日、NULL、跨月值一致 |
| timestamp | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST('2024-02-29 12:34:56.123456' AS TIMESTAMP)),(CAST(NULL AS TIMESTAMP))) v(a)` | PG 保留 .123456，目标 DATETIME(0) 丢失；真实差异保留 |
| grouped | `SELECT g, ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1 AS INT),CAST(NULL AS INT)),(CAST(1 AS INT),CAST(NULL AS INT)),(CAST(2 AS INT),CAST(3 AS INT)),(CAST(2 AS INT),CAST(NULL AS INT))) v(g,a) GROUP BY g ORDER BY g` | `(1,[NULL,NULL]),(2,[3,NULL])`，两组和最终顺序一致 |
| grouped-empty | `SELECT g, ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1 AS INT),CAST(1 AS INT))) v(g,a) WHERE FALSE GROUP BY g ORDER BY g` | 两端 0 行，不凭空补出分组 |
| left-join | `SELECT l.id, ARRAY_AGG(r.a) AS xs FROM (VALUES (CAST(1 AS INT)),(CAST(2 AS INT))) l(id) LEFT JOIN (VALUES (CAST(1 AS INT),CAST(9 AS INT))) r(id,a) ON l.id=r.id GROUP BY l.id ORDER BY l.id` | `(1,[9]),(2,[NULL])`，未匹配连接行不是空输入，最终顺序一致 |
| scalar-empty | `SELECT (SELECT ARRAY_AGG(a) FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE) AS xs` | 1 行 SQL NULL |
| scalar-mixed | `SELECT (SELECT ARRAY_AGG(a) FROM (VALUES (CAST(1 AS INT)),(CAST(NULL AS INT))) v(a)) AS xs` | `[1,NULL]` |
| having-empty | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE HAVING ARRAY_AGG(a) IS NULL` | HAVING 保留 1 行 SQL NULL |
| having-all-null | `SELECT ARRAY_AGG(a) AS xs FROM (VALUES (CAST(NULL AS INT))) v(a) HAVING ARRAY_AGG(a) IS NULL` | 非空 [NULL] 不满足 SQL NULL，返回 0 行 |
| multiple | `SELECT ARRAY_AGG(a) AS xs, ARRAY_AGG(DISTINCT a) AS ys, COUNT(*) AS n FROM (VALUES (CAST(1 AS INT)),(CAST(NULL AS INT)),(CAST(1 AS INT))) v(a)` | 本次两端 `[1,1,NULL] / [1,NULL] / 3` 一致；没有据此承诺未排序聚合的全计划顺序 |

完整行值 19 组一致，3 组不同（distinct-mixed、bool、timestamp），不把其中的 NULL 子维度正确冒充完整通过。带最终 ORDER BY 的分组/连接查询，当前值、重复次数和顺序一致，键为明确分组值/id；重复稳定本身不证明任意输入唯一。

### 类型证据不能只看工具的一句“不同”

工具当前对 `_int4` / `array<int>` 没有递归统一别名，因此把这类受控 INT 边界也列为声明不同；两端原生声明可以人工识别为相同的 32 位元素类型。相反，原 0287 的 `_int4` / `array<tinyint>` 真正是位宽差异，不能忽略。相同原则适用于 `_int8`/array<bigint>、_float8/array<double>、_bool/array<boolean> 和 _date/array<datev2>。

Decimal 两个边界目标计划为 array<decimalv3(10,2)>，源为 _numeric，驱动没有给出数组元素 Precision/Scale；即使源参数 CAST 写明 10,2 且当前 Decimal 值相同，也不宣称已取得完整返回类型约束证明。工具顶层把数组精度列作“不适用”不代表嵌套精度已经验收。timestamp 目标 array<datetimev2(0)> 的值损失是真实问题，不是仅声明名称不同。

另实测 Doris 原生 `SELECT ARRAY_AGG(a) AS xs FROM (SELECT CAST(1 AS INT) a) v WHERE FALSE`，重新解析/生成后仍返回 []；`SELECT COLLECT_LIST(a) AS xs FROM (SELECT CAST(NULL AS INT) a) v` 也仍返回 []，不错误套 PG 的空输入规则。

## 6. 差异补证与后续归因

### 布尔数组：表示差异对照

原边界在完整数组比较中仍不同。另做下列**独立诊断对照**，不是 SQLGlot 修复验收，也没有用它替换原查询：

```sql
-- PG
SELECT CAST(xs[1] AS BOOLEAN) AS b1, CAST(xs[2] AS BOOLEAN) AS b2,
       CAST(xs[3] AS BOOLEAN) AS b3
FROM (SELECT ARRAY_AGG(a) AS xs FROM
      (VALUES (CAST(TRUE AS BOOLEAN)),(CAST(NULL AS BOOLEAN)),(CAST(FALSE AS BOOLEAN))) v(a)) s;
-- Doris 原生对照
SELECT CAST(xs[1] AS BOOLEAN) AS b1, CAST(xs[2] AS BOOLEAN) AS b2,
       CAST(xs[3] AS BOOLEAN) AS b3
FROM (SELECT NULLIF(ARRAY_AGG(a), ARRAY()) AS xs FROM
      (SELECT CAST(TRUE AS BOOLEAN) a UNION ALL SELECT CAST(NULL AS BOOLEAN)
       UNION ALL SELECT CAST(FALSE AS BOOLEAN)) v) s;
```

两端 3 列，声明 bool/boolean 一致；PG true/NULL/false，Doris 协议 1/NULL/0，经已有标量布尔比较后值一致。这支持“该样本是嵌套表示未正确归一化”，不是所有数组数字都可当成布尔。未修改 Comparator。核对时还看到当前 PG 下标 `[1]` 会生成 Doris `[0]`，因此本控制明确使用原生 Doris 1-based 下标；该生成变体没有执行或验收，索引转换需独立调查。

### TIMESTAMP：聚合之外也丢微秒

```sql
-- 源
SELECT CAST('2024-02-29 12:34:56.123456' AS TIMESTAMP) AS ts;
-- 当前 SQLGlot 实际生成
SELECT CAST('2024-02-29 12:34:56.123456' AS DATETIME) AS ts;
-- 独立 Doris 对照，不是本轮补丁输出
SELECT CAST('2024-02-29 12:34:56.123456' AS DATETIME(6)) AS ts;
```

源值为 `2024-02-29T12:34:56.123456`；当前输出计划 datetimev2(0)，返回 `2024-02-29T12:34:56`；DATETIME(6) 对照计划 datetimev2(6)，值与源一致，字段数/别名一致但源精度元数据仍不完整。证明是独立 CAST 类型转换问题，不是本轮 NULL 聚合实现导致；尚未确定所有精度/值域的安全补丁，不混入 task-003。

初次控制使用 DATETIMEV2(6) 名称，被 SQLGlot Doris Parser 的前置只读检查拒绝，**没有提交 Doris**；随后改用上面的 DATETIME(6) 实际执行成功。两个阶段不混为 Doris 数据库错误。

## 7. 测试、最终回归与验收状态

工作目录 sqlglot-experiment，执行命令：

```bash
PATH="$PWD/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.dialects.test_doris tests.dialects.test_mysql tests.dialects.test_postgres
PATH="$PWD/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests/dialects -t .
PATH="$PWD/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens
PATH="$PWD/.venv/bin:$PATH" SKIP_INTEGRATION=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest
```

结果为定向 140、方言 1063、列出的核心 233 个方法通过，存在包含关系不累加。最终根集 1546 个条目中 1544 通过、2 个因缺 duckdb 无法导入（test_executor/test_optimizer），没有把根集写成通过，也不擅自装依赖。mypy/C 扩展/make check 未运行。Ruff check、format --check 和 diff --check 通过。新增方法在修改前运行确有 21 个断言失败。

最终实现用相同 22 个边界重跑并重复执行，结论保持；CLI 另实际运行 75 条：10 条本任务关联、首轮 62 条及 fix-002 新匹配 3 条，按 16 个实际 stage 执行，结果 65 MATCH/9 Doris 错误/1 行值或顺序差异。65 条已有 MATCH 没有退化；不是全批 313 条验收。所有事实只写进现有 Markdown，没有覆盖首轮 JSON 或生成执行附件。

NULL/空输入规则有正向、NULL、空输入、DISTINCT、分组、连接和子查询证据；仍不把任务关闭：0287 真实元素位宽差异、嵌套类型/精度验收和原比较规则下的差异要明确去向。窗口/FILTER/内部排序/整行类型没有声称已修，未指定聚合内顺序不制造保证。先继续本任务的类型/证据核对，再决定是否转为独立类型任务；可另行授权处理 task-004，但不能用它掩盖 task-003 未验收项。整份输入未完成。
