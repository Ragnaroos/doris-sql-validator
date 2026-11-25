# pg-aggregates-0284-628b13e2：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select array_agg(a order by a)
  from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 284；行 775–776；相同回显第 1 次。

阶段：aggregates-001-stage-17；数据库：dsv_wf_agg001_s17。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-17-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{1,2,3,4}"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT COLLECT_LIST(a ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'COLLECT_LIST' which has 3 arity. Candidate functions are: [COLLECT_LIST(Expression, Expression), COLLECT_LIST(Expression)]")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.272716+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | array_agg | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[1, 2, 3, 4]]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = Can not found function 'COLLECT_LIST' which has 3 arity. Candidate functions are: [COLLECT_LIST(Expression, Expression), COLLECT_LIST(Expression)]")
```

### 尝试 1

时间：2026-11-20T02:20:20.251177+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_CONCAT(ARRAY_FILTER(x -> x IS NOT NULL, ARRAY_SORT(ARRAY_AGG(a))), ARRAY_FILTER(x -> x IS NULL, ARRAY_AGG(a))) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0284-628b13e2', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ARRAY_CONCAT(ARRAY_FILTER(x -&gt; x IS NOT NULL, ARRAY_SORT(ARRAY_AGG(a))), ARRAY_FILTER(x -&gt; x IS NULL, ARRAY_AGG(a))) | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[1, 2, 3, 4]"]]
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
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

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
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py TRANSFORMS exp.ArrayAgg:63；sqlglot/expressions/aggregate.py ArrayAgg:77。

- sqlglot/generators/doris.py exp.ArrayAgg；sqlglot/generator.py order_sql/ordered_sql。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-003：ARRAY_AGG 保留 NULL 并补偿空输入](../../aggregates-001-attribution-summary.md#task-003) | 普通非窗口、非 FILTER 的 ARRAY_AGG，含 DISTINCT；源语义要求保留 NULL 时不得使用丢 NULL 的 COLLECT_LIST；空输入返回 SQL NULL。；本 Case 还需排除第 1 节列出的其他独立问题。 |
| [task-004：ARRAY_AGG 按聚合值自身排序](../../aggregates-001-attribution-summary.md#task-004) | 单排序键与聚合值同一表达式；当前已实测的可比较整数、ASC/DESC、NULLS FIRST/LAST、DISTINCT。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-003：NULL 与空输入修复后的复查

2026-11-23，使用 sqlglot-experiment 的 HEAD 089891f2521780e2c5b243005017af9db62f25a6 加既有 task-001/002 和本轮 task-003 未提交修改；完整身份、实际命令/SQL 和验收限制见[fix-003 任务报告](../../../fixes/tasks/aggregates-001/fix-003/task-003.md)。原首轮及前文独立候选事实不覆盖。

stage-17 内部 ORDER BY a 不在本轮实施范围，最终仍是 COLLECT_LIST(a ORDER BY a NULLS LAST)。PG [1,2,3,4] 与原 .out 一致；Doris 报 1105：`collect_list doesn't support order by expression`，目标类型/值未比较。复用 task-004，不把该错误伪算为 task-003 的 NULL 逻辑已经完成全部查询验收。

## 9. fix-004：自值排序修复后的复查

2026-11-23 09:23:47–09:23:50 UTC，原 stage-17/SQL/.out 不变，修改后的 sqlglot-experiment 实际生成：

```sql
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SORT(COLLECT_LIST(a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(a)), 1, ARRAY_SIZE(ARRAY_AGG(a)) - ARRAY_SIZE(COLLECT_LIST(a)))), ARRAY()) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

两端成功，各 1 列/1 行，实时结构化数组均为 `[1,2,3,4]`；值、重复次数、数组内部顺序一致，每端额外执行一次稳定。没有显式 Alias 或最终 ORDER BY，默认列名不强比；结果行多重集合比较不改变数组元素顺序。实时 PG 显示 `{1,2,3,4}` 与原 .out 相同，Doris 用 JSON 数组文本显示，CLI 仍记“行值或顺序不匹配”。原生类型 `_int4` / `array<tinyint>` 的真实位宽差异保留，不能说完整 Case 已 MATCH。

本 task 的排序规则已完成约定整数边界验收，类型/显示仍为独立研究。完整身份、实际 API、68 组共享边界及未覆盖范围见 [fix-004 任务报告](../../../fixes/tasks/aggregates-001/fix-004/task-004.md)，共享边界不冒称本 Case 分别执行了 68 个专属变体。无提交/推送，前文历史不覆盖。


## fix-011 后续类型核验（2026-11-24）

沿用原 aggregates-001-stage-17 YAML及其实际数据库 dsv_wf_agg001_s17；本轮未改源SQL/.out、数据、比较规则或SQLGlot代码。实际import为../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff指纹仍为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。任务仍为“已修改但未完成验收”，详细类型子项见 [task-003 / fix-011](../../../fixes/tasks/aggregates-001/fix-011/task-003.md)。前述首轮/前轮证据不覆盖。

本轮原.out规则的实际结果：**行值或顺序不匹配**。实时PG成功，文本化结果与原.out一致。本条仍是INT32/TINYINT数组元素位宽差异；结构化值相同不等于类型相同。

实际由当前生成器产生的Doris SQL：

```sql
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SORT(COLLECT_LIST(a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(a)), 1, ARRAY_SIZE(ARRAY_AGG(a)) - ARRAY_SIZE(COLLECT_LIST(a)))), ARRAY()) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```


已取得字段：1: PG _int4 / Doris array<tinyint>。双端行数为1/1；结构化值/重复次数观察为“一致”；顺序观察为“无最终 ORDER BY，忽略结果行顺序但保留重复次数”。 本原查询未另做完整双端重复，40条任务边界的重复稳定性不能冒充本条已重复。未commit/push，没有以人工CAST候选替换生成结果。


