# pg-aggregates-0276-0f1f5154：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select array_agg(distinct val)
from (select null as val from generate_series(1, 2));
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 276；行 740–742；相同回显第 1 次。

阶段：aggregates-001-stage-17；数据库：dsv_wf_agg001_s17。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-17-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{NULL}"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT COLLECT_LIST(DISTINCT val) FROM (SELECT NULL AS val FROM GENERATE_SERIES(1, 2))
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 81)\n")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.208072+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | array_agg | _text | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[null]]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 81)\n")
```

### 尝试 1

时间：2026-11-20T02:20:20.021714+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_AGG(DISTINCT val) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS _series)
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0276-0f1f5154', candidate_sql=上列候选文本)
```
**该候选 Doris**：未成功。


```text
(1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 36)\n\n== SQL ==\nSELECT ARRAY_AGG(DISTINCT val) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS _series)\n------------------------------------^^^\n")
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=不同；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。重复稳定不证明排序键唯一。

### 尝试 2

时间：2026-11-20T02:22:26.286494+00:00。改写依据：修正初步候选缺派生表 Alias；保留 NULL，不靠删除行造通过。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_AGG(DISTINCT val) FROM (SELECT CAST(NULL AS INT) AS val FROM NUMBERS("number"="2")) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0276-0f1f5154', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ARRAY_AGG(DISTINCT val) | array&lt;int&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[null]"]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _text | array&lt;int&gt; | 一致 | 不同 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

最新候选的维度结果：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _text | array&lt;int&gt; | 一致 | 不同 | 不适用 |

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py TRANSFORMS exp.ArrayAgg:63；sqlglot/expressions/aggregate.py ArrayAgg:77。

- sqlglot/parsers/postgres.py _build_generate_series/FUNCTIONS:146；sqlglot/generator.py explodinggenerateseries_sql:5821；sqlglot/generators/doris.py。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-003：ARRAY_AGG 保留 NULL 并补偿空输入](../../aggregates-001-attribution-summary.md#task-003) | 普通非窗口、非 FILTER 的 ARRAY_AGG，含 DISTINCT；源语义要求保留 NULL 时不得使用丢 NULL 的 COLLECT_LIST；空输入返回 SQL NULL。；本 Case 还需排除第 1 节列出的其他独立问题。 |
| [task-008：FROM 位置的常量整数 GENERATE_SERIES](../../aggregates-001-attribution-summary.md#task-008) | FROM 中非相关、整数常量起止与步长、源端 INT4 范围；别名和输出列，正/负步长与空区间。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-003：NULL 与空输入修复后的复查

2026-11-23，使用 sqlglot-experiment 的 HEAD 089891f2521780e2c5b243005017af9db62f25a6 加既有 task-001/002 和本轮 task-003 未提交修改；完整身份、实际命令/SQL 和验收限制见[fix-003 任务报告](../../../fixes/tasks/aggregates-001/fix-003/task-003.md)。原首轮及前文独立候选事实不覆盖。

stage-17 实际生成 `SELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM GENERATE_SERIES(1, 2))`。PG 原文成功返回 [NULL]，文本化与原 .out 一致；Doris 仍报 1105：`mismatched input ',' expecting EQ(line 1, pos 95)`，目标字段/类型/值未比较。NULL 规则已修改，但还需 task-008 的序列能力，不改写为 MATCH。


## 9. fix-008：常量整数序列修复后的实际复测

时间 2026-11-23T10:47:14.875742+00:00；代码、环境、有限边界见 [fix-008 汇总](../../../fixes/aggregates-001-fix-008-summary.md)与[本条新生成 SQL/完整比较](../../../fixes/tasks/aggregates-001/fix-008/task-008.md#statement-276)。保留原源 SQL/.out、Case ID 和 aggregates-001-stage-17-cases.yaml 对应数据状态；首轮与前轮事实不覆盖。运行时从 ../sqlglot-experiment 导入（HEAD 089891f2521780e2c5b243005017af9db62f25a6，加报告记录的累积 diff），不是手写候选。

本轮 run --stdout 整条结论：**Doris 执行失败**。序列已转换；原 PG 允许的无别名派生表仍被 Doris 拒绝。错误自动分类为类型转换失败并不准确，以原文为准；关联派生表/查询级兼容研究，不属于序列行数算法。

实际新生成并执行的 Doris SQL：

```sql
SELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)
```

当前 PG 原文执行成功；记录 `[[[null]]]`。Doris 无完整结果，实际错误：

```text
(1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 53)\n\n== SQL ==\nSELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)\n-----------------------------------------------------^^^\n")
```

至少一端没有成功结果，字段类型、值与顺序没有完整双端验收。

当前 PG 显示文本与原 .out 的值和重复次数相同；这不替代原生类型/顺序检查。

本轮 task-008 的非 NULL 常量 INT4 序列主路径已实测，NULL 参数仍未支持，任务整体尚未完成验收；本条的其他独立问题不混入序列补丁。未修改比较规则或数据，未 commit/push。


## 10. fix-009：task-008 NULL 参数完成验收

本轮继续原 task-008，不是开始 task-009。常量 INT4/NULL 序列规则已完成约定验收：123 条边界/上下文双端通过并复跑稳定，含NULL与零步长共存、列名/INT类型和空结果；详见[本轮汇总](../../../fixes/aggregates-001-fix-009-summary.md)与[任务报告](../../../fixes/tasks/aggregates-001/fix-009/task-008.md)。

本条仍按原阶段 YAML 运行，时间 2026-11-23T11:02:13.364770+00:00，框架整条结果为 **Doris 执行失败**。新生成 Doris SQL 与 fix-008 本条保存结果逐字相同；原序列参数不含NULL，本轮不重复复制该SQL。 原 SQL/.out、首轮统计、比较规则和数据不变。原聚合NULL输入不等于序列参数NULL；本条其他类型/统计/UDF/查询级等限制仍按前轮记录保留，序列task验收不把整条失败或类型差异改成完整匹配。本轮没有重新执行本条实时PG类型补证，不将沿用证据写成新实测。未 commit/push。


## fix-011 后续类型核验（2026-11-24）

沿用原 aggregates-001-stage-17 YAML及其实际数据库 dsv_wf_agg001_s17；本轮未改源SQL/.out、数据、比较规则或SQLGlot代码。实际import为../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff指纹仍为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。任务仍为“已修改但未完成验收”，详细类型子项见 [task-003 / fix-011](../../../fixes/tasks/aggregates-001/fix-011/task-003.md)。前述首轮/前轮证据不覆盖。

本轮原.out规则的实际结果：**Doris 执行失败**。实时PG成功，文本化结果与原.out一致。当前首先因无别名派生表失败，不能继续用早期的序列函数错误解释；目标类型/值未比较。

实际由当前生成器产生的Doris SQL：

```sql
SELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)
```

实际错误（数据库执行错误以CLI记录为准；补证入口前置拒绝不冒充数据库执行）：

```text
(1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 53)\n\n== SQL ==\nSELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)\n-----------------------------------------------------^^^\n")
```

已取得字段：1: PG _text / Doris 未取得成功字段。目标无成功结果，不采样推断目标类型或值。 本原查询未另做完整双端重复，40条任务边界的重复稳定性不能冒充本条已重复。未commit/push，没有以人工CAST候选替换生成结果。



