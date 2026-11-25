# task-002：Doris 原生 NULLS FIRST/LAST 排序

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`64d2701093f675f7b757510d5fdbfb04fa53c3ec`。保存原NULL排序规则及其测试；原约定验收结论不变。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 验收结论与范围

**状态：已修复并完成本次约定验收。** 在当前 Doris 4.1.3-rc02 环境，保留 PostgreSQL 的默认和显式 NULL 排序，支持位置、别名和多键排序。6 条关联原查询均完成严格转译；其中 3 条仍因其他能力/前提失败，不将它们标为完全匹配。

入口：[task-002 原范围](../../../../attribution/aggregates-001-attribution-summary.md#task-002)；共同版本、diff、授权与回归范围见[fix-002 汇总](../../../aggregates-001-fix-002-summary.md)。本次只修 task-002，没有 commit/push。本任务是已有 task 的首次正式修复轮次，不新建 task-id，不覆盖 fix-001 的历史证据。

排除自定义 ORDER BY USING、不同 Collation、聚合内部排序算法、序列展开、相关子查询以及表达式返回类型补偿。能力标志也影响已有窗口生成路径，因此增加了窗口单元测试和实际数据库回归，但不宣称所有窗口/所有版本都已验证。

## 2. 修改原因与代码

当前 checkout 089891f 上仍能复现：

```sql
-- PostgreSQL 源 SQL
select max(unique2) from tenk1 order by 1;
```

修改前使用 `unsupported_level=ErrorLevel.RAISE`，实际错误为：

```text
'NULLS LAST' translation not supported with positional ordering
```

原因：DorisGenerator 继承 MySQLGenerator 的 `NULL_ORDERING_SUPPORTED = None`，公共 `Generator.ordered_sql` 尝试用额外 CASE 排序键模拟 NULL 顺序；位置序号无法这样模拟，于是严格拒绝。Doris 的实测版本支持原生 NULLS FIRST/LAST，不应沿用该限制。

| 文件 / 位置 | 本轮改动 | 边界 |
| :--- | :--- | :--- |
| [generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py)：DorisGenerator | 增加 `NULL_ORDERING_SUPPORTED = True` | 复用公共 ordered_sql；不改变 MySQL，不手写查询级改写 |
| [test_doris.py](../../../../../../sqlglot-experiment/tests/dialects/test_doris.py)：test_null_ordering | 13 个 PG→Doris 转译变体、Doris 往返、MySQL CASE 模拟及严格位置排序拒绝检查 | 覆盖位置/别名、多键、默认/显式方向及 ROW_NUMBER / SUM ROWS / SUM RANGE |
| 同测试文件 test_doris | 4 条 LAG/LEAD 的 PG 转译预期保留 NULLS LAST；另检查原生 Doris 无显式 NULL 子句的 identity | 不再用丢失源默认排序的旧预期；原生 Doris 默认行为不改 |

修改后的最小实际输出：

```sql
SELECT MAX(unique2) FROM tenk1 ORDER BY 1 NULLS LAST
```

原有 task-001 数组修改完整保留，不算成本轮排序实现。未修改公共 Generator、Parser、AST、验证框架、原 SQL/.out 或数据。

## 3. 原查询真实执行

工作目录为 doris-sql-validator-workflow，使用 `../doris-sql-validator/.venv/bin/python`，设置 `PYTHONPATH=../sqlglot-experiment:src` 并在进程内加载既有 .env。以 `typer.testing.CliRunner().invoke(app, ['run', '--path', <实际阶段 YAML>, '--stdout', '--id', ...])` 实际调用 CLI，每个 stage 一次，不保存执行 JSON。退出 1 表示含差异，不能替代逐条结果。

实际分组：stage-03 为 0134/0137，stage-09 为 0173/0179，stage-42 为 0551/0552。另用 `SqlglotTranspiler.transpile_case` 重新生成 Doris SQL，再经 `pg_probe.execute_query` 和 `compare_probe` 补证；没有用手写候选代替生成结果。双端成功的 3 条各增加一次执行，值/顺序均保持一致。

### 3.1 Case 0134：排序通过，序列/LATERAL 仍失败

[原 Case](../../../../attribution/cases/aggregates-001/pg-aggregates-0134-429eb1f7.md)，stage-03。原 SQL：

```sql
select s1, s2, sm
from generate_series(1, 3) s1,
     lateral (select s2, sum(s1 + s2) sm
              from generate_series(1, 3) s2 group by s2) ss
order by 1, 2;
```

修改后实际生成：

```sql
SELECT s1, s2, sm FROM GENERATE_SERIES(1, 3) AS s1, LATERAL (SELECT s2, SUM(s1 + s2) AS sm FROM GENERATE_SERIES(1, 3) AS s2 GROUP BY s2) AS ss ORDER BY 1 NULLS LAST, 2 NULLS LAST
```

修改前两个位置排序报错，修改后严格生成成功。PG 成功返回 9 行，按顺序文本化与原 .out 一致；Doris 实际报 `(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 40)\n")`。目标没有成功结果，字段/类型/行值/顺序未比较。该错误在 GENERATE_SERIES 参数处，不是 NULL 排序被拒绝；后续 LATERAL 也仍需独立验证，不承诺 task-008 能完整解决。

### 3.2 Case 0137：源端执行前提冲突，不能证明整条等价

[原 Case](../../../../attribution/cases/aggregates-001/pg-aggregates-0137-2237979d.md)，stage-03。原 SQL：

```sql
select two + four as g, (select f1 from int4_tbl where f1 = (two + four))
from tenk1 t1
group by two + four order by 1;
```

修改后实际生成：

```sql
SELECT two + four AS g, (SELECT f1 FROM int4_tbl WHERE f1 = (two + four)) FROM tenk1 AS t1 GROUP BY two + four ORDER BY 1 NULLS LAST
```

修改前位置排序报错，修改后生成成功。原 .out 记录成功；本轮 PG 18.1 原文却失败，SQLSTATE `42803`，错误 `subquery uses ungrouped column "t1.two" from outer query`。Doris 报 `(1105, "errCode = 2, detailMessage = four, two not in aggregate's output")`。两端均失败不算成功匹配，字段/类型/结果未比较。

这与原归因报告记录的成功补证冲突，本轮保留双方事实，不覆盖原输出、不无声更换基线，也不将此条改成默认排除的源端负向。需先核对源文件/.out 对应版本和历史执行条件。不能从当前 PG 报错认定历史源 SQL 非法，也不能用它验收相关子查询能力。

### 3.3 Case 0173：完整当前样本匹配

[原 Case](../../../../attribution/cases/aggregates-001/pg-aggregates-0173-5bef76d3.md)，stage-09。源 SQL 和生成 SQL见第 2 节。

PG/Doris 均成功，均为 1 列、1 行 `[[9999]]`，值及重复次数、最终顺序与各端重复执行均一致。实时 PG 文本按顺序与原 .out 一致；PG int4 / Doris int 按既有映射一致，精度/Scale 不适用。未出现需严格比较的显式 Alias。单行结果不存在行间排序歧义，但不据此替代多行 NULL 边界。

### 3.4 Case 0179：别名已保留，投影序列仍失败

[原 Case](../../../../attribution/cases/aggregates-001/pg-aggregates-0179-8eb5c0b1.md)，stage-09。原 SQL：

```sql
select max(unique2), generate_series(1,3) as g from tenk1 order by g desc;
```

修改后实际生成：

```sql
SELECT MAX(unique2), UNNEST(GENERATE_SERIES(1, 3)) AS g FROM tenk1 ORDER BY g DESC NULLS FIRST
```

修改前严格生成可完成，但排序别名被展开成 `CASE WHEN UNNEST(GENERATE_SERIES(1, 3)) IS NULL THEN 1 ELSE 0 END DESC, UNNEST(GENERATE_SERIES(1, 3)) DESC`；现在使用原生子句并保留别名。PG 成功返回 `[[9999,3],[9999,2],[9999,1]]`，按顺序文本化与原 .out 一致。Doris 报 `(1105, "errCode = 2, detailMessage = Can not found function 'GENERATE_SERIES'")`；字段/类型/行值/顺序未比较。投影位置 SRF 是 task-008 明确排除的查询级研究事项。

### 3.5 Case 0551 / 0552：原 .out 匹配，类型声明仍有其他差异

均在 stage-42，原查询分别为：

```sql
-- pg-aggregates-0551-f476de2c
select v||'a', case v||'a' when 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;

-- pg-aggregates-0552-7ea82af2
select v||'a', case when v||'a' = 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
```

修改后分别生成：

```sql
SELECT CONCAT(v, 'a'), CASE CONCAT(v, 'a') WHEN 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(ARRAY('a', 'b')) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST

SELECT CONCAT(v, 'a'), CASE WHEN CONCAT(v, 'a') = 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(ARRAY('a', 'b')) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST
```

两条在 fix-001 后仍报位置排序不支持；现在双端均成功，各为 3 列、2 行 `[["aa",1,1],["ba",0,1]]`，按原 .out 匹配。实时 PG 与 .out 的文本行顺序一致，补证行值、重复次数、最终顺序及两端各一次重复均一致。本样本第一列 aa/ba 唯一，顺序没有并列歧义；不据重复稳定证明所有数据唯一。

每条类型均为 PG `text,int4,int8` / Doris `varchar(65533),tinyint,bigint`：逻辑类型一致，前两列声明不同，第三列声明一致；精度/Scale 不适用，没有需检查的显式 Alias。不能把 `.out` 的 MATCH 当作完整类型通过；这些声明差异不是 task-002 改动引入，原归因候选已经记录。

## 4. 边界与回归

### 4.1 19 组实际边界

完整源查询由以下共同 CTE 加下表的 PG 后缀组成，执行时各自是单条 SELECT，不创建表或文件。目标用 `parse_one(source_sql, read="postgres").sql("doris", unsupported_level=ErrorLevel.RAISE)` 实际生成。下表给目标末尾规则，共同 CTE 保持相同；不是手写目标执行。

```sql
WITH t AS (
  SELECT CAST(NULL AS INT) AS a, CAST(1 AS INT) AS id
  UNION ALL SELECT CAST(2 AS INT), CAST(2 AS INT)
  UNION ALL SELECT CAST(-1 AS INT), CAST(3 AS INT)
  UNION ALL SELECT CAST(2 AS INT), CAST(4 AS INT)
  UNION ALL SELECT CAST(NULL AS INT), CAST(5 AS INT)
  UNION ALL SELECT CAST(0 AS INT), CAST(6 AS INT)
)
```

| 编号 | 完整 PG 查询的后缀 | 实际生成的 Doris 后缀 / 差异 | 实测观察 |
| :--- | :--- | :--- | :--- |
| order-1 | `SELECT a FROM t ORDER BY a` | `SELECT a FROM t ORDER BY a NULLS LAST` | 值序列 -1,0,2,2,NULL,NULL |
| order-2 | `SELECT a FROM t ORDER BY a DESC` | `SELECT a FROM t ORDER BY a DESC NULLS FIRST` | NULL,NULL,2,2,0,-1 |
| order-3 | `SELECT a FROM t ORDER BY a ASC NULLS FIRST` | `SELECT a FROM t ORDER BY a ASC` | NULL,NULL,-1,0,2,2 |
| order-4 | `SELECT a FROM t ORDER BY a ASC NULLS LAST` | 同源后缀 | -1,0,2,2,NULL,NULL |
| order-5 | `SELECT a FROM t ORDER BY a DESC NULLS FIRST` | 同源后缀 | NULL,NULL,2,2,0,-1 |
| order-6 | `SELECT a FROM t ORDER BY a DESC NULLS LAST` | `SELECT a FROM t ORDER BY a DESC` | 2,2,0,-1,NULL,NULL |
| order-7 | `SELECT a FROM t ORDER BY 1` | `SELECT a FROM t ORDER BY 1 NULLS LAST` | 同 order-1，保留 2 和 NULL 的重复次数 |
| order-8 | `SELECT a FROM t ORDER BY 1 DESC` | `SELECT a FROM t ORDER BY 1 DESC NULLS FIRST` | 同 order-2 |
| alias | `SELECT a + CAST(1 AS INT) AS b, id FROM t ORDER BY b, id` | `SELECT a + CAST(1 AS INT) AS b, id FROM t ORDER BY b NULLS LAST, id NULLS LAST` | 6 行依次为 (0,3),(1,6),(3,2),(3,4),(NULL,1),(NULL,5)；b 为 PG int4 / Doris bigint，声明不同 |
| multiple-keys | `SELECT a, id FROM t ORDER BY 1 DESC NULLS LAST, 2 DESC` | `SELECT a, id FROM t ORDER BY 1 DESC, 2 DESC NULLS FIRST` | (2,4),(2,2),(0,6),(-1,3),(NULL,5),(NULL,1) |
| empty | `SELECT a FROM t WHERE FALSE ORDER BY 1` | 同源并增加 `NULLS LAST` | 两端 0 行，字段类型仍取得 int4/int |
| all-null | `SELECT a FROM t WHERE a IS NULL ORDER BY 1 DESC` | 同源并增加 `NULLS FIRST` | 两端各 2 行 SQL NULL，不丢行 |
| distinct | `SELECT DISTINCT a FROM t ORDER BY 1` | 同源并增加 `NULLS LAST` | -1,0,2,NULL，共 4 行 |
| grouped | `SELECT a, COUNT(*) AS n FROM t GROUP BY a ORDER BY 1` | 同源并增加 `NULLS LAST` | (-1,1),(0,1),(2,2),(NULL,2) |
| window-row-number | `SELECT a, id, ROW_NUMBER() OVER (ORDER BY a, id) AS rn FROM t ORDER BY id` | 窗口为 `ORDER BY a NULLS LAST, id NULLS LAST`；最终 `ORDER BY id NULLS LAST` | 按 id 的 rn 为 5,3,1,4,6,2 |
| window-rows | `SELECT a, id, SUM(a) OVER (ORDER BY a, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS s FROM t ORDER BY id` | 窗口 a/id 和最终 id 均保留 `NULLS LAST`，ROWS 范围不变 | 按 id 的 s 为 3,1,-1,3,3,-1 |
| window-range | `SELECT a, id, SUM(a) OVER (ORDER BY a RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS s FROM t ORDER BY id` | 窗口 a 和最终 id 增加 `NULLS LAST`，RANGE 范围不变 | 按 id 的 s 为 3,3,-1,3,3,-1，并列 2 共享累计范围 |
| window-lag | `SELECT a, id, LAG(a) OVER (ORDER BY a, id) AS prev FROM t ORDER BY id` | `LAG(a, 1, NULL)`；窗口 a/id 和最终 id 增加 `NULLS LAST` | 按 id 的 prev 为 2,0,NULL,2,NULL,-1 |
| window-lead | `SELECT a, id, LEAD(a) OVER (ORDER BY a DESC, id) AS next FROM t ORDER BY id` | `LEAD(a, 1, NULL) AS` 后用反引号引用 next；窗口 `a DESC NULLS FIRST, id NULLS LAST`；最终 `id NULLS LAST` | 按 id 的 next 为 NULL,2,NULL,0,2,-1 |

19 组双端均成功，各追加一次双端执行，行值/重复次数、顺序及重复结果一致，没有浮点容差或 Decimal 近似。字段数量均一致，识别到的显式别名一致。除 alias 的 int4/bigint 算术声明差异外，其他 18 组输出按现有映射声明一致：INT 对应 int4/int，COUNT、ROW_NUMBER 和 SUM(INT) 对应 int8/bigint。当前边界均无 Decimal/时间精度比较，不能据此声称这些类型也已验收。

对只输出 a 的并列行，完整输出相同，交换位置不可观测；多列样例使用唯一 id 作最终顺序或并列键。重复执行稳定仅是补证，不代替唯一性分析。没有测试 Collation、自定义运算符、聚合内部排序、不同版本或所有输入域。

### 4.2 测试及既有成功查询

命令工作目录为 sqlglot-experiment，单元测试解释器为该目录 .venv/bin/python。详细命令、环境修正和未运行检查见本轮汇总：定向 137、全部方言 1060（包含定向）、核心 199 个测试通过，Ruff/check/format 通过，mypy 因未安装没有运行。新增排序测试在修复前确实失败，修复后通过，不是仅调整测试让错误行为通过。

另对原首轮 62 条 MATCH 按原 YAML 分 15 个 stage 实际执行 CLI `run --stdout`：stage-01/03/06/07/08/09/10/11/15/25/30/31/32/42/43，数量依次 21/6/1/5/1/7/2/1/3/6/2/1/1/1/4，合计 62 条全部保持 MATCH。没有把原 .out 无法证明的类型标为通过，也没有重跑全部 313 条。

## 5. 验收与下一步

本任务的排序行为、必要边界及已测既有回归通过；原查询的非排序差异分别保留，不因它们继续失败而扩大排序修改，也不伪造完全等价。任务验收仅针对当前 Doris 实测版本和明确范围；最早支持版本、完整根测试集、C 扩展、mypy/make check 未覆盖，发布前需按目标范围补查。

建议下一项独立实现 [task-003](../../../../attribution/aggregates-001-attribution-summary.md#task-003)：ARRAY_AGG 的 NULL 与空输入规则，它有明确现存缺口且是 task-004 的前置能力。task-001 的类型验收仍未完成；0134/0179 的序列和查询级能力、0137 的源证据冲突也不会随 task-003 自动解决。没有擅自开始下一任务或创建下一轮空白报告。
