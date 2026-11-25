# task-001：Doris 值列表数组构造修复与验收

## 1. 结论与范围

**状态：已修改但未完成验收。** 已实现数组构造，单元测试及 18 个固定输入的实际值比较通过；字段类型的统一契约尚未完整验证，不能以“当前值相同”关闭类型验收。完整查询中仍存在其他转换缺口及 UDF 前提问题。

任务入口：[原 task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)；共同版本、目录、diff 指纹及回归汇总见[本批汇总](../../../aggregates-001-fix-001-summary.md)。本轮只建议一个独立修复范围：Doris 值列表 ARRAY 输出及其必要的 Parser round-trip。没有新增共享 AST 类型、Schema 强制输入或框架自定义转换。

纳入：普通值、NULL、空数组、嵌套数组、运行时元素和显式元素 CAST。数组中的标量子查询仍是一个元素，因此保留该路径；排除从查询多行构造数组的 `ARRAY(SELECT ...)`，不混为标量子查询元素。

排除：PG 文本数组 CAST、数组下界、UNNEST 算法、ARRAY_AGG、WITHIN GROUP、GENERATE_SERIES、NULL 排序以及 UDF/用户定义类型。关联列表的 Case 0136 实际属于排除项；原列表不改写，执行及统计单独说明。

## 2. 修改依据与实现

拉取最新 main 后、修改前，在 `ErrorLevel.RAISE` 下复现代表查询：

```sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
```

原生成器继承 MySQL 的数组方法，严格生成报 `Arrays are not supported by MySQL`。检查全部 14 条关联 SQL，均仍被该数组错误拒绝；Case 0551/0552 还包含位置 NULL 排序错误。不是社区新版已经覆盖而重复打补丁。

新增测试后、实现前，两个新测试方法失败；实现及补齐依赖后，最终回归通过。修改后实际输出：

```sql
SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v
```

| 文件 / 方法 | 实际改动 | 必要性及边界 |
| :--- | :--- | :--- |
| [generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py)：DorisGenerator.array_sql | 复用 self.func("ARRAY", *expression.expressions)；遇到未标记为值构造的单个 Query 元素时调用 unsupported | 不再继承 MySQL 的拒绝；逐个生成元素，CAST 与运行时 NULL 不被手工折叠。严格模式拒绝排除范围的数组查询构造 |
| [parsers/doris.py](../../../../../../sqlglot-experiment/sqlglot/parsers/doris.py)：DorisParser.FUNCTIONS["ARRAY"] | 使用现有 exp.Array，并设置 value_constructor=True | Doris ARRAY(...) 的参数是值。单个标量子查询往返解析后仍应是一个值，不能误判成 PG ARRAY(SELECT ...) |
| [test_doris.py](../../../../../../sqlglot-experiment/tests/dialects/test_doris.py)：test_array_constructor / test_array_query_constructor | 两个参数化测试方法，13 个 PG 正向输入；3 个其他方言输入；MySQL 严格拒绝回归；3 个被排除的数组查询构造 | 验证严格生成、Doris Parser/Generator round-trip、NULL/空/嵌套/CAST/标量子查询；不改变 MySQL 原有行为 |

没有对特定表、列、字面量答案特判，没有过滤 NULL、丢弃重复元素或在 Generator 内执行常量求值。没有新增“所有元素自动转 INT”之类未经类型契约确认的规则。

`self.unsupported` 遵循 SQLGlot 原有错误策略；本轮验证使用 **ErrorLevel.RAISE 枚举**。默认 WARN 只表示发出告警，不是该排除语法已取得可执行等价输出。

## 3. 实际调用与比较范围

数据库补证时间：2026-11-20T04:19:40.670049+00:00 至 2026-11-20T04:26:16.269469+00:00（UTC；最初复现与单元测试早于此窗口）。

实际 CLI 由同一修改后导入环境中的 `typer.testing.CliRunner().invoke(app, args)` 调用。传入真实 run 命令，不是读取旧报告重新计数；标准输出 JSON 仅在内存使用，未保存或覆盖首轮文件：

```bash
# 工作目录：doris-sql-validator-workflow；已加载既有连接环境变量
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../sqlglot-experiment:src \
  ../doris-sql-validator/.venv/bin/python -m doris_sql_validator.cli run \
  --path reports/data-preparation/aggregates-001-stage-01-cases.yaml \
  --id pg-aggregates-0010-12bf388c --stdout
```

这是同一 CLI 参数的单条复跑方式；本轮实际将每个阶段关联 ID 放入同一次 CliRunner 调用。stage-01/03/17/31/33/40/42 分别运行 1/1/1/5/3/1/2 条，共 14 条。CLI 退出 1 表示其中有差异，不等于命令未产生有效结果。

另用以下现有 API 补齐 CLI 简写记录省略的维度，所有目标 SQL 由修改后 SQLGlot 从对应源 SQL 生成，不使用人工 Doris 候选：

```python
tr = SqlglotTranspiler().transpile_case(case, source_dialect="postgres")
source = execute_query("postgres", case.sql, stage_database)
target = execute_query("doris", tr.target_sql, stage_database)
checks = compare_probe(source, target, case.sql)
```

- 补证每条 10 秒超时、最多 10000 行；源/目标均无截断。只读 PG UDF 先阅读了准备 SQL 中函数体，未执行有外部副作用的函数或重建数据。
- .out 是主参考。14 条实时 PG 结果另用 SELECT 包装，将每个输出列 CAST AS TEXT，与对应 .out 的文本行多重集合核对，14 条均一致。包装形如 `SELECT c0::TEXT FROM (<原查询>) AS checked(c0)`；只核对源基线的显示值/重复次数，不据包装查询证明原查询顺序，也不替换 .out。
- 额外比较使用源 OID 对应类型及 Doris EXPLAIN VERBOSE 原生类型；Doris 的协议 STRING 不能冒充数组类型。结构化数组逐元素保留顺序和 NULL，结果行无最终 ORDER BY 时按多重集合，保留重复次数。
- 原查询中的三个 VARIADIC 目标被补证工具的 Doris Parser 前置检查拒绝；CLI 则已真正提交 Doris 并取得下文语法错误。两种事实分开记录，未把前置检查错误冒充数据库执行。
- 没有更改验证框架、原 YAML/.out、阶段数据或比较规则；没有把 .out 缺失类型自动计为类型通过。

### 3.1 完整查询结果汇总

| 结果（原 .out 规则） | 数量 | 说明 |
| :--- | ---: | :--- |
| 匹配 | 1 | 0306；实时补证仍有 SUM 返回类型差异 |
| 行值或顺序不匹配 | 1 | 0010 的数组显示格式；非元素差异 |
| Doris 执行失败 | 9 | WITHIN GROUP × 5、VARIADIC × 3、缺少 RWAGG × 1 |
| SQLGlot 转译失败 | 3 | task-002 位置排序 × 2，排除的 ARRAY 子查询构造 × 1 |
| 合计 | 14 | 13 条值列表相关 + 1 条排除控制 |

范围内 13 条中，11 条完成严格生成，2 条因其他规则仍无法完成生成。不能把 11 条“生成成功”误当成 11 条“查询语义匹配”。

### 3.2 原查询逐条执行事实

下面的“源记录”来自本轮实际 PG，不是 AI 推测。Decimal 使用带“十进制数”的表示以避免转为 Float；数组对照保留嵌套形状和重复元素。没有成功目标结果时，字段类型/行值/顺序均记为未比较。

#### pg-aggregates-0010-12bf388c

材料：[pg-aggregates-0010-12bf388c](../../../../attribution/cases/aggregates-001/pg-aggregates-0010-12bf388c.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-01-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-01-validation.json)。数据库 `dsv_wf_agg001_s01`。

源 SQL：

```sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
```

修改后实际生成 SQL：

```sql
SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v
```

原 .out 规则结果：**行值或顺序不匹配**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

- 字段数量：一致；显式别名：未发现需检查的显式别名。
- 第 1 列：PG `_text`；Doris `array<varchar(5)>`；逻辑类型一致，声明不同，精度/小数位不适用。
- 行数：1/1；结构化值及重复次数：一致。源记录 `[[["hello","world"]]]`；Doris 驱动记录 `[["[\"hello\", \"world\"]"]]`。
- 最终顺序：无最终 ORDER BY，忽略结果行顺序但保留重复次数；本原查询未另作重复执行，不宣称全部输入稳定。

结论：数组构造已可执行；.out 的 PG 数组显示与 Doris 显示不同。实时元素/NULL/行数相同，但 _text / array<varchar(5)> 仍不是完整类型等价证明。

#### pg-aggregates-0136-4243166e

材料：[pg-aggregates-0136-4243166e](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-03-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-03-validation.json)。数据库 `dsv_wf_agg001_s03`。

源 SQL：

```sql
select array(select sum(x+y) s
            from generate_series(1,3) y group by y order by s)
  from generate_series(1,3) x;
```

修改后严格生成错误（未向 Doris 执行）：

```text
Doris does not support ARRAY subquery constructors
```

原 .out 规则结果：**SQLGlot 转译失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

源记录：`[[[2,3,4]],[[3,4,5]],[[4,5,6]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：这条是 ARRAY(SELECT ...)，与原 task-001 的排除范围一致。原归因关联列表含有它，但本轮不修改归因，只保留排除控制；不得将其计入 13 条值列表转换缺口。

#### pg-aggregates-0306-e70870c4

材料：[pg-aggregates-0306-e70870c4](../../../../attribution/cases/aggregates-001/pg-aggregates-0306-e70870c4.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-17-validation.json)。数据库 `dsv_wf_agg001_s17`。

源 SQL：

```sql
select
    string_agg(distinct 'a', ','),
    sum((
        select sum(1)
        from (values(1)) b(id)
        where a.id = b.id
)) from unnest(array[1]) a(id);
```

修改后实际生成 SQL：

```sql
SELECT GROUP_CONCAT(DISTINCT 'a', ','), SUM((SELECT SUM(1) FROM (SELECT 1 AS id) AS b WHERE a.id = b.id)) FROM UNNEST(ARRAY(1)) AS a(id)
```

原 .out 规则结果：**匹配**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

- 字段数量：一致；显式别名：未发现需检查的显式别名。
- 第 1 列：PG `text`；Doris `varchar(65533)`；逻辑类型一致，声明不同，精度/小数位不适用。
- 第 2 列：PG `numeric`；Doris `bigint`；逻辑类型不同，声明不同，精度/小数位信息不足。
- 行数：1/1；结构化值及重复次数：一致。源记录 `[["a",{"十进制数":"1"}]]`；Doris 驱动记录 `[["a",1]]`。
- 最终顺序：无最终 ORDER BY，忽略结果行顺序但保留重复次数；本原查询未另作重复执行，不宣称全部输入稳定。

结论：ARRAY(1) 已可执行。原 .out 显示匹配；实时第二列为 PG numeric、Doris bigint，属于 SUM 返回类型的剩余差异，不把整条查询标为完全语义一致。

#### pg-aggregates-0410-f6f52dc3

材料：[pg-aggregates-0410-f6f52dc3](../../../../attribution/cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-31-validation.json)。数据库 `dsv_wf_agg001_s31`。

源 SQL：

```sql
select percentile_disc(array[0,0.1,0.25,0.5,0.75,0.9,1]) within group (order by thousand)
from tenk1;
```

修改后实际生成 SQL：

```sql
SELECT PERCENTILE_DISC(ARRAY(0, 0.1, 0.25, 0.5, 0.75, 0.9, 1)) WITHIN GROUP (ORDER BY CASE WHEN thousand IS NULL THEN 1 ELSE 0 END, thousand) FROM tenk1
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
missing 'BY' at '('(line 1, pos 76)
")
```

源记录：`[[[0,99,249,499,749,899,999]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：值列表数组已生成；整条查询仍被 WITHIN GROUP 调用语法阻断。本轮未实现百分位数组算法或有序集合改写。

#### pg-aggregates-0411-b38c2a1f

材料：[pg-aggregates-0411-b38c2a1f](../../../../attribution/cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-31-validation.json)。数据库 `dsv_wf_agg001_s31`。

源 SQL：

```sql
select percentile_cont(array[0,0.25,0.5,0.75,1]) within group (order by thousand)
from tenk1;
```

修改后实际生成 SQL：

```sql
SELECT PERCENTILE_CONT(ARRAY(0, 0.25, 0.5, 0.75, 1)) WITHIN GROUP (ORDER BY CASE WHEN thousand IS NULL THEN 1 ELSE 0 END, thousand) FROM tenk1
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
missing 'BY' at '('(line 1, pos 66)
")
```

源记录：`[[[0,249.75,499.5,749.25,999]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：值列表数组已生成；WITHIN GROUP 仍失败。PERCENTILE_CONT 的数组参数/返回类型没有在本轮验收。

#### pg-aggregates-0412-cbdaef84

材料：[pg-aggregates-0412-cbdaef84](../../../../attribution/cases/aggregates-001/pg-aggregates-0412-cbdaef84.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-31-validation.json)。数据库 `dsv_wf_agg001_s31`。

源 SQL：

```sql
select percentile_disc(array[[null,1,0.5],[0.75,0.25,null]]) within group (order by thousand)
from tenk1;
```

修改后实际生成 SQL：

```sql
SELECT PERCENTILE_DISC(ARRAY(ARRAY(NULL, 1, 0.5), ARRAY(0.75, 0.25, NULL))) WITHIN GROUP (ORDER BY CASE WHEN thousand IS NULL THEN 1 ELSE 0 END, thousand) FROM tenk1
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
missing 'BY' at '('(line 1, pos 89)
")
```

源记录：`[[[[null,999,499],[749,249,null]]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：嵌套值列表与 NULL 保留；WITHIN GROUP 仍失败。不能据构造文本正确声称百分位嵌套返回形状已修复。

#### pg-aggregates-0413-6ccabd9a

材料：[pg-aggregates-0413-6ccabd9a](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-31-validation.json)。数据库 `dsv_wf_agg001_s31`。

源 SQL：

```sql
select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x)
from generate_series(1,6) x;
```

修改后实际生成 SQL：

```sql
SELECT PERCENTILE_CONT(ARRAY(0, 1, 0.25, 0.75, 0.5, 1, 0.3, 0.32, 0.35, 0.38, 0.4)) WITHIN GROUP (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x) FROM GENERATE_SERIES(1, 6) AS x
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
missing 'BY' at '('(line 1, pos 97)
")
```

源记录：`[[[1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：数组已生成；当前首先失败在 WITHIN GROUP。GENERATE_SERIES 的 FROM 规则另属 task-008，本轮没有处理。

#### pg-aggregates-0415-16b30942

材料：[pg-aggregates-0415-16b30942](../../../../attribution/cases/aggregates-001/pg-aggregates-0415-16b30942.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-31-validation.json)。数据库 `dsv_wf_agg001_s31`。

源 SQL：

```sql
select percentile_disc(array[0.25,0.5,0.75]) within group (order by x)
from unnest('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}'::text[]) u(x);
```

修改后实际生成 SQL：

```sql
SELECT PERCENTILE_DISC(ARRAY(0.25, 0.5, 0.75)) WITHIN GROUP (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x) FROM UNNEST(CAST('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}' AS ARRAY<STRING>)) AS u(x)
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
missing 'BY' at '('(line 1, pos 60)
")
```

源记录：`[[["fred","jill","jim"]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：概率数组已生成；WITHIN GROUP 仍失败。源 SQL 同时含 PG 文本数组 CAST，明确不属于 task-001。

#### pg-aggregates-0434-5da33736

材料：[pg-aggregates-0434-5da33736](../../../../attribution/cases/aggregates-001/pg-aggregates-0434-5da33736.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-33-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-33-validation.json)。数据库 `dsv_wf_agg001_s33`。

源 SQL：

```sql
select least_agg(variadic array[q1,q2]) from int8_tbl;
```

修改后实际生成 SQL：

```sql
SELECT LEAST_AGG(VARIADIC ARRAY(q1, q2)) FROM int8_tbl
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
mismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 26)
")
```

额外补证前置检查：Doris Parser 拒绝 VARIADIC 后的 ARRAY 参数；未在该 API 路径执行，不覆盖 CLI 已执行的错误事实。

源记录：`[[-4567890123456789]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：ARRAY(q1,q2) 已生成；PG VARIADIC 语法和 LEAST_AGG 自定义聚合没有被迁移，不能靠数组构造修复解决整条查询。

#### pg-aggregates-0437-d68f01c2

材料：[pg-aggregates-0437-d68f01c2](../../../../attribution/cases/aggregates-001/pg-aggregates-0437-d68f01c2.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-33-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-33-validation.json)。数据库 `dsv_wf_agg001_s33`。

源 SQL：

```sql
select cleast_agg(variadic array[4.5,f1]) from int4_tbl;
```

修改后实际生成 SQL：

```sql
SELECT CLEAST_AGG(VARIADIC ARRAY(4.5, f1)) FROM int4_tbl
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
mismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 27)
")
```

额外补证前置检查：Doris Parser 拒绝 VARIADIC 后的 ARRAY 参数；未在该 API 路径执行，不覆盖 CLI 已执行的错误事实。

源记录：`[[{"十进制数":"-2147483647"}]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：ARRAY(4.5,f1) 已生成；VARIADIC 与 CLEAST_AGG UDF 是剩余问题，未改写或安装。

#### pg-aggregates-0438-998adec3

材料：[pg-aggregates-0438-998adec3](../../../../attribution/cases/aggregates-001/pg-aggregates-0438-998adec3.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-33-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-33-validation.json)。数据库 `dsv_wf_agg001_s33`。

源 SQL：

```sql
select pg_typeof(cleast_agg(variadic array[4.5,f1])) from int4_tbl;
```

修改后实际生成 SQL：

```sql
SELECT PG_TYPEOF(CLEAST_AGG(VARIADIC ARRAY(4.5, f1))) FROM int4_tbl
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = 
mismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 37)
")
```

额外补证前置检查：Doris Parser 拒绝 VARIADIC 后的 ARRAY 参数；未在该 API 路径执行，不覆盖 CLI 已执行的错误事实。

源记录：`[["numeric"]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：ARRAY(4.5,f1) 已生成；VARIADIC、CLEAST_AGG 以及 PG_TYPEOF 的 PG 专有类型观测均不在本任务范围。

#### pg-aggregates-0534-1b68ef98

材料：[pg-aggregates-0534-1b68ef98](../../../../attribution/cases/aggregates-001/pg-aggregates-0534-1b68ef98.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-40-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-40-validation.json)。数据库 `dsv_wf_agg001_s40`。

源 SQL：

```sql
SELECT eatarray(rwagg(ARRAY[1.0::real])), eatarray(rwagg(ARRAY[1.0::real]));
```

修改后实际生成 SQL：

```sql
SELECT EATARRAY(RWAGG(ARRAY(CAST(1.0 AS FLOAT)))), EATARRAY(RWAGG(ARRAY(CAST(1.0 AS FLOAT))))
```

原 .out 规则结果：**Doris 执行失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

Doris 实际错误：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'RWAGG'")
```

源记录：`[[[2,1,1,1],[2,1,1,1]]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：ARRAY(CAST(1.0 AS FLOAT)) 已生成，显式 REAL → FLOAT 转换保留；Doris 缺少本批 PG 自定义聚合 RWAGG，未安装/替代。

#### pg-aggregates-0551-f476de2c

材料：[pg-aggregates-0551-f476de2c](../../../../attribution/cases/aggregates-001/pg-aggregates-0551-f476de2c.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-42-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-42-validation.json)。数据库 `dsv_wf_agg001_s42`。

源 SQL：

```sql
select v||'a', case v||'a' when 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
```

修改后严格生成错误（未向 Doris 执行）：

```text
'NULLS LAST' translation not supported with positional ordering
```

原 .out 规则结果：**SQLGlot 转译失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

源记录：`[["aa",1,1],["ba",0,1]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：数组不再触发 MySQL unsupported，但严格生成仍被 ORDER BY 1 的 NULLS LAST 拒绝；属于未选定的 task-002。没有使用手改排序绕过验收。

#### pg-aggregates-0552-7ea82af2

材料：[pg-aggregates-0552-7ea82af2](../../../../attribution/cases/aggregates-001/pg-aggregates-0552-7ea82af2.md)；[阶段 YAML](../../../../data-preparation/aggregates-001-stage-42-cases.yaml)、[首轮 JSON](../../../../validation/aggregates-001-stage-42-validation.json)。数据库 `dsv_wf_agg001_s42`。

源 SQL：

```sql
select v||'a', case when v||'a' = 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
```

修改后严格生成错误（未向 Doris 执行）：

```text
'NULLS LAST' translation not supported with positional ordering
```

原 .out 规则结果：**SQLGlot 转译失败**。实时 PG 成功；文本化后的行值/重复次数与本条 .out 一致。

源记录：`[["aa",1,1],["ba",0,1]]`。目标未得到成功结果，字段/别名、类型/精度、行数/值/重复次数及最终顺序未比较。

结论：同上，位置排序规则仍属 task-002；源 CASE 表达式与另一条不同，仍保留独立 Case。

## 4. 单元测试、边界及既有匹配回归

### 4.1 最终单元测试与检查

工作目录均为 `sqlglot-experiment`，解释器 `.venv/bin/python`（Python 3.12.15）。测试数字为 unittest 方法数，参数化的多个输入不再额外算成多个测试方法。

| 实际命令 | 最终结果 | 范围 |
| :--- | :--- | :--- |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_doris tests.dialects.test_mysql tests.dialects.test_postgres` | 133 个通过，0 失败 | 目标/源/继承方言；包含新方法 |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest discover -s tests/dialects -t .` | 1045 个通过，0 失败；最终一次 4.377 秒 | 全部方言 |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.test_parser tests.test_generator tests.test_expressions tests.test_transpile tests.test_build tests.test_tokens tests.test_schema tests.test_dialect_imports` | 230 个通过，0 失败；23.742 秒 | 相关核心 |
| `.venv/bin/ruff check sqlglot/generators/doris.py sqlglot/parsers/doris.py tests/dialects/test_doris.py` | 通过 | 三个改动文件 |
| `.venv/bin/ruff format --check sqlglot/generators/doris.py sqlglot/parsers/doris.py tests/dialects/test_doris.py` | 通过 | 未对其他文件格式化 |
| `git diff --check` | 通过 | 无空白错误 |

1045 已包含定向的 133，不将二者相加宣称独立覆盖数。全根测试集、C 扩展、完整 mypy、make check 未运行。首次新测试在实现前失败，确认不是空测试；中途全方言运行的依赖缺失和日期简化失败，补齐 pytz/python-dateutil 与 PATH 后重新通过，详见汇总。

### 4.2 数据库边界：实际源 SQL 与生成 SQL

18 个样例均在 `dsv_wf_agg001_s01`；无外部基表依赖。全部双端成功、字段数量和显式别名一致、行数和值/重复次数一致。这里的“一致”逐维度记录，不包含未证明的类型契约。数组内元素顺序始终比较；没有最终 ORDER BY 的结果行只比较多重集合。

| 样例 | PostgreSQL SQL | 修改后实际生成的 Doris SQL |
| :--- | :--- | :--- |
| 普通整数 | `SELECT ARRAY[1, 2] AS value` | `SELECT ARRAY(1, 2) AS `value`` |
| 元素 NULL 与重复 | `SELECT ARRAY[1, NULL, 2, 1] AS value` | `SELECT ARRAY(1, NULL, 2, 1) AS `value`` |
| 显式 INT 的全 NULL | `SELECT ARRAY[NULL::INT] AS value` | `SELECT ARRAY(CAST(NULL AS INT)) AS `value`` |
| 显式 INT 空数组 | `SELECT ARRAY[]::INT[] AS value` | `SELECT CAST(ARRAY() AS ARRAY<INT>) AS `value`` |
| 矩形嵌套 | `SELECT ARRAY[[1, 2], [3, 4]] AS value` | `SELECT ARRAY(ARRAY(1, 2), ARRAY(3, 4)) AS `value`` |
| 显式 BIGINT | `SELECT ARRAY[1::BIGINT, NULL::BIGINT] AS value` | `SELECT ARRAY(CAST(1 AS BIGINT), CAST(NULL AS BIGINT)) AS `value`` |
| 显式 Decimal | `SELECT ARRAY[1.25::DECIMAL(10,2), NULL::DECIMAL(10,2)] AS value` | `SELECT ARRAY(CAST(1.25 AS DECIMAL(10, 2)), CAST(NULL AS DECIMAL(10, 2))) AS `value`` |
| 空字符串/Unicode/NULL | `SELECT ARRAY['hello', '', '世界', NULL] AS value` | `SELECT ARRAY('hello', '', '世界', NULL) AS `value`` |
| 运行时 NULL 与重复行 | `SELECT ARRAY[x, NULL::INT] AS value FROM (VALUES (1::INT), (NULL::INT), (1::INT)) AS t(x)` | `SELECT ARRAY(x, CAST(NULL AS INT)) AS `value` FROM (SELECT CAST(1 AS INT) AS x UNION ALL SELECT CAST(NULL AS INT) UNION ALL SELECT CAST(1 AS INT)) AS t` |
| 单个标量子查询元素 | `SELECT ARRAY[(SELECT 1)] AS value` | `SELECT ARRAY((SELECT 1)) AS `value`` |
| 两个标量子查询元素 | `SELECT ARRAY[(SELECT 1), (SELECT 2)] AS value` | `SELECT ARRAY((SELECT 1), (SELECT 2)) AS `value`` |
| 标量子查询无行 | `SELECT ARRAY[(SELECT 1 WHERE FALSE)] AS value` | `SELECT ARRAY((SELECT 1 WHERE FALSE)) AS `value`` |
| 整数组为 SQL NULL | `SELECT NULL::INT[] AS value` | `SELECT CAST(NULL AS ARRAY<INT>) AS `value`` |
| 稳定 id 最终排序 | `SELECT id AS id, ARRAY[x, NULL::INT] AS value FROM (VALUES (1, 1::INT), (2, NULL::INT), (3, 1::INT)) AS t(id, x) ORDER BY id NULLS FIRST` | `SELECT id AS id, ARRAY(x, CAST(NULL AS INT)) AS `value` FROM (SELECT 1 AS id, CAST(1 AS INT) AS x UNION ALL SELECT 2, CAST(NULL AS INT) UNION ALL SELECT 3, CAST(1 AS INT)) AS t ORDER BY id` |
| BIGINT 两端边界 | `SELECT ARRAY[(-9223372036854775807-1)::BIGINT, 9223372036854775807::BIGINT] AS value` | `SELECT ARRAY(CAST((-9223372036854775807 - 1) AS BIGINT), CAST(9223372036854775807 AS BIGINT)) AS `value`` |
| Decimal 正负边界 | `SELECT ARRAY[-99999999.99::DECIMAL(10,2), 99999999.99::DECIMAL(10,2), NULL::DECIMAL(10,2)] AS value` | `SELECT ARRAY(-CAST(99999999.99 AS DECIMAL(10, 2)), CAST(99999999.99 AS DECIMAL(10, 2)), CAST(NULL AS DECIMAL(10, 2))) AS `value`` |
| 未显式类型的全 NULL | `SELECT ARRAY[NULL] AS value` | `SELECT ARRAY(NULL) AS `value`` |
| 显式 REAL | `SELECT ARRAY[1.0::REAL, NULL::REAL] AS value` | `SELECT ARRAY(CAST(1.0 AS FLOAT), CAST(NULL AS FLOAT)) AS `value`` |

| 样例 | 源实际行值 | 目标实际原生类型 | 类型与结果限制 |
| :--- | :--- | :--- | :--- |
| 普通整数 | `[[[1,2]]]` | array<tinyint> | 源 _int4；Doris 子类型 tinyint，声明宽度不同 |
| 元素 NULL 与重复 | `[[[1,null,2,1]]]` | array<tinyint> | 保留元素 NULL、元素重复和元素顺序；整数宽度仍不同 |
| 显式 INT 的全 NULL | `[[[null]]]` | array<int> | 源 _int4 / 目标 array<int> 属同一 INT32 元素映射；工具未递归映射数组声明 |
| 显式 INT 空数组 | `[[[]]]` | array<int> | 空数组 []，不是 SQL NULL；INT32 元素 CAST 保留 |
| 矩形嵌套 | `[[[[1,2],[3,4]]]]` | array<array<tinyint>> | 实际二维形状相同；PG OID _int4 不编码维数，Doris 嵌套 tinyint，不声明全域同义 |
| 显式 BIGINT | `[[[1,null]]]` | array<bigint> | 源 _int8 / 目标 array<bigint>；显式 INT64 元素映射保留 |
| 显式 Decimal | `[[[{"十进制数":"1.25"},null]]]` | array<decimalv3(10,2)> | CAST(10,2) 保留，Doris 实际 (10,2)；PG 数组元数据不返回元素 typmod，精度契约仍信息不足 |
| 空字符串/Unicode/NULL | `[[["hello","","世界",null]]]` | array<text> | 源 _text；空字符串与 SQL NULL 未混淆；仅当前字符串输入 |
| 运行时 NULL 与重复行 | `[[[1,null]],[[null,null]],[[1,null]]]` | array<int> | 三行含两条完全相同记录，未丢重复；NULL 列在运行时进入数组 |
| 单个标量子查询元素 | `[[[1]]]` | array<tinyint> | [1]，不是展开成多行；整数宽度不同 |
| 两个标量子查询元素 | `[[[1,2]]]` | array<tinyint> | [1,2]，两个参数各为一个值；整数宽度不同 |
| 标量子查询无行 | `[[[null]]]` | array<tinyint> | [NULL]，不是空数组；整数宽度不同 |
| 整数组为 SQL NULL | `[[null]]` | array<int> | SQL NULL，不是 [] 或 [NULL]；INT32 CAST 保留 |
| 稳定 id 最终排序 | `[[1,[1,null]],[2,[null,null]],[3,[1,null]]]` | tinyint；array<int> | id=1/2/3 唯一，实际顺序相同；id 列 PG int4 / Doris tinyint，数组子类型为 int |
| BIGINT 两端边界 | `[[[-9223372036854776000,9223372036854776000]]]` | array<bigint> | 两端值均为 -9223372036854775808 和 9223372036854775807；INT64 CAST 保留 |
| Decimal 正负边界 | `[[[{"十进制数":"-99999999.99"},{"十进制数":"99999999.99"},null]]]` | array<decimalv3(13,2)> | Doris ARRAY 实际 decimalv3(13,2)，虽元素 CAST 写 (10,2)；值无损，源数组精度元数据不足，未关闭类型验收 |
| 未显式类型的全 NULL | `[[[null]]]` | array<null_type> | 源 _text / 目标 array<null_type>；值 [NULL] 相同，不代表元素类型相同 |
| 显式 REAL | `[[[1,null]]]` | array<float> | 源 _float4 / 目标 array<float>；当前 1.0 值精确相同，没有靠额外浮点容差通过 |

类型说明：现有 compare_probe 对原生类型声明做字符串/少量别名比较，不递归把 PG `_int4` 等同于 Doris `array<int>`；因此它对所有这些数组声明报告不同。上表只对明确已取得的元素别名映射说明一致，**不修改比较器、不把全部声明差异都算误报**。真实的整数宽度、NULL 元素默认类型不同单独保留；PG 的数组 OID 也无法证明维数或 Decimal 元素精度。不能用 ARRAY 这个粗粒度逻辑类型掩盖这些差异。

重复执行：元素 NULL/重复、显式空数组、运行时 NULL/重复行、稳定 id 排序、空标量子查询五个样例各增加一次双端执行，记录值/重复次数均与首遍及对端一致。只有稳定 id 样例要求最终结果行顺序，其固定输入 id=1/2/3 唯一，首遍与重复遍均按 1/2/3 返回。其他样例的结果行顺序不作为保证；数组内部元素顺序没有忽略。

严格负向边界仅检查三种被排除的数组子查询构造：`ARRAY(SELECT 1)`、`ARRAY((SELECT 1))`、`ARRAY(SELECT 1 UNION ALL SELECT 2)`；均按本任务排除契约抛 UnsupportedError，**不是说这些 PG SQL 非法**。未安排重现其他源端负向错误，不将两端失败算成成功匹配。

### 4.3 原先匹配的查询

从各原首轮 JSON 中选择全部 62 条“匹配”记录，按各自 YAML/阶段运行同一 CLI `run --stdout --id ...`。以下各次退出均为 0，仍按原 .out 显示规则，不强制增加 Schema 或换答案。

| 阶段 | 查询数 | 本轮结果 |
| :--- | ---: | :--- |
| [aggregates-001-stage-01](../../../../data-preparation/aggregates-001-stage-01-cases.yaml) | 21 | 21 条匹配 |
| [aggregates-001-stage-03](../../../../data-preparation/aggregates-001-stage-03-cases.yaml) | 6 | 6 条匹配 |
| [aggregates-001-stage-06](../../../../data-preparation/aggregates-001-stage-06-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-07](../../../../data-preparation/aggregates-001-stage-07-cases.yaml) | 5 | 5 条匹配 |
| [aggregates-001-stage-08](../../../../data-preparation/aggregates-001-stage-08-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-09](../../../../data-preparation/aggregates-001-stage-09-cases.yaml) | 7 | 7 条匹配 |
| [aggregates-001-stage-10](../../../../data-preparation/aggregates-001-stage-10-cases.yaml) | 2 | 2 条匹配 |
| [aggregates-001-stage-11](../../../../data-preparation/aggregates-001-stage-11-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-15](../../../../data-preparation/aggregates-001-stage-15-cases.yaml) | 3 | 3 条匹配 |
| [aggregates-001-stage-25](../../../../data-preparation/aggregates-001-stage-25-cases.yaml) | 6 | 6 条匹配 |
| [aggregates-001-stage-30](../../../../data-preparation/aggregates-001-stage-30-cases.yaml) | 2 | 2 条匹配 |
| [aggregates-001-stage-31](../../../../data-preparation/aggregates-001-stage-31-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-32](../../../../data-preparation/aggregates-001-stage-32-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-42](../../../../data-preparation/aggregates-001-stage-42-cases.yaml) | 1 | 1 条匹配 |
| [aggregates-001-stage-43](../../../../data-preparation/aggregates-001-stage-43-cases.yaml) | 4 | 4 条匹配 |

合计 62 条；未发现这部分新增回归。该范围不是全部 313 条，不能据此宣布全工作负载无回归。保留关联查询自身的剩余失败，不将这 62 条与修复关联 14 条混成可比较的提升百分比。

## 5. 验收与下一步

| 约定维度 | 结论 | 依据 / 限制 |
| :--- | :--- | :--- |
| 不再继承 MySQL 拒绝值列表数组 | 通过 | 最新 main 复现失败；Doris Generator 独立输出，原关联 13 条中 11 条完整生成，2 条仅剩其他生成错误 |
| 普通/NULL/空/嵌套、运行时值、显式 CAST 的结构与当前值 | 已测范围通过 | 单元测试及 18 个固定数据库样例；未使用手写 Doris 候选 |
| 类型一致性 | 未完成 | 显式 INT/BIGINT/REAL 映射有证据；裸整数/全 NULL 子类型不同，Decimal 源端数组精度信息不足，负值样例目标精度扩展 |
| 行数、值、重复次数与必要顺序 | 已测范围通过 | 边界全结果及五项重复；稳定唯一 id 排序另测。不是所有原关联查询都成功执行 |
| 原 YAML/.out 验证 | 完成重跑，不能全判通过 | 14 条中 1 匹配、1 显示差异、9 Doris 错误、3 转译失败；逐条事实保留 |
| 既有匹配回归 | 通过 | 原先 62 条仍匹配 |
| 相关源/目标/继承方言及核心单测 | 通过 | 1045 方言 + 230 核心，定向 133 包含在方言中 |
| 所有输入/全部 Doris 版本完全等价 | 未证明 | 不是有限测试能证明的目标，排除范围也未实现 |

建议后续先对隐式整数/NULL 子类型与 Decimal 元素精度建立明确契约，再决定是否需要增加独立的类型推断/显式 CAST 规则；本轮没有擅自扩展为全类型自动转换。不可把其他 task 或 UDF 迁移塞入本补丁以提高 Case 匹配率。

建议 PR 单一目标仍为 Doris 值列表数组构造与必要 round-trip，无前置实现依赖；当前尚需解决上述类型验收保留项、复核 Doris 最早支持版本、按社区贡献规范人工审查并补适用完整检查。试验代码没有提交，不代表已准备好合并。**本轮没有 commit、push、创建 Issue 或社区 PR，也没有推进其他 task。**

