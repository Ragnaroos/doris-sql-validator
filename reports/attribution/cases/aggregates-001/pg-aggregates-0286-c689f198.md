# pg-aggregates-0286-c689f198：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select array_agg(b order by a desc)
  from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 286；行 779–780；相同回显第 1 次。

阶段：aggregates-001-stage-17；数据库：dsv_wf_agg001_s17。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-17-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{2,1,3,4}"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT COLLECT_LIST(b ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END DESC, a DESC) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'COLLECT_LIST' which has 3 arity. Candidate functions are: [COLLECT_LIST(Expression, Expression), COLLECT_LIST(Expression)]")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.328426+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | array_agg | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[2, 1, 3, 4]]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = Can not found function 'COLLECT_LIST' which has 3 arity. Candidate functions are: [COLLECT_LIST(Expression, Expression), COLLECT_LIST(Expression)]")
```

### 尝试 1

时间：2026-11-20T02:20:20.487167+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_SORTBY(ARRAY_AGG(b), ARRAY_AGG(a)) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0286-c689f198', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ARRAY_SORTBY(ARRAY_AGG(b), ARRAY_AGG(a)) | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[4, 3, 1, 2]"]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [[2, 1, 3, 4]] | 1 |
| Doris多出 | ["[4, 3, 1, 2]"] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### 尝试 2

时间：2026-11-20T02:22:26.396978+00:00。改写依据：不同键降序排序候选，数组元素顺序保持为比较维度。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_REVERSE(ARRAY_SORTBY(ARRAY_AGG(b), ARRAY_AGG(a))) FROM (SELECT 1 AS a,4 AS b UNION ALL SELECT 2,3 UNION ALL SELECT 3,1 UNION ALL SELECT 4,2) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0286-c689f198', candidate_sql=上列候选文本)
```
**该候选 Doris**：未成功。


```text
(1105, "errCode = 2, detailMessage = Can not found function 'ARRAY_REVERSE'")
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=不同；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。重复稳定不证明排序键唯一。

### 尝试 3

时间：2026-11-20T02:28:55.952777+00:00。改写依据：仅当前有限整数键的降序反证候选；不适用于任意键、NULL 排序或整数取负溢出。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_SORTBY(ARRAY_AGG(b), ARRAY_AGG(-a)) FROM (SELECT 1 AS a,4 AS b UNION ALL SELECT 2,3 UNION ALL SELECT 3,1 UNION ALL SELECT 4,2) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0286-c689f198', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ARRAY_SORTBY(ARRAY_AGG(b), ARRAY_AGG(-a)) | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[2, 1, 3, 4]"]]
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

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-003：ARRAY_AGG 保留 NULL 并补偿空输入](../../aggregates-001-attribution-summary.md#task-003) | 普通非窗口、非 FILTER 的 ARRAY_AGG，含 DISTINCT；源语义要求保留 NULL 时不得使用丢 NULL 的 COLLECT_LIST；空输入返回 SQL NULL。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-003：NULL 与空输入修复后的复查

2026-11-23，使用 sqlglot-experiment 的 HEAD 089891f2521780e2c5b243005017af9db62f25a6 加既有 task-001/002 和本轮 task-003 未提交修改；完整身份、实际命令/SQL 和验收限制见[fix-003 任务报告](../../../fixes/tasks/aggregates-001/fix-003/task-003.md)。原首轮及前文独立候选事实不覆盖。

stage-17 聚合 b 而按 a 排序属于不同键研究，最终目标保留 COLLECT_LIST(b ORDER BY a DESC NULLS FIRST)。PG [2,1,3,4] 与原 .out 一致；Doris 报 1105：`collect_list doesn't support order by expression`，目标类型/值未比较。不能声称 task-004 的值自身排序直接覆盖本条。


## fix-011 后续类型核验（2026-11-24）

沿用原 aggregates-001-stage-17 YAML及其实际数据库 dsv_wf_agg001_s17；本轮未改源SQL/.out、数据、比较规则或SQLGlot代码。实际import为../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff指纹仍为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。任务仍为“已修改但未完成验收”，详细类型子项见 [task-003 / fix-011](../../../fixes/tasks/aggregates-001/fix-011/task-003.md)。前述首轮/前轮证据不覆盖。

本轮原.out规则的实际结果：**Doris 执行失败**。实时PG成功，文本化结果与原.out一致。目标没有完整成功结果；字段类型、行值和顺序不能判通过，具体独立问题保留。

实际由当前生成器产生的Doris SQL：

```sql
SELECT COLLECT_LIST(b ORDER BY a DESC NULLS FIRST) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v
```

实际错误（数据库执行错误以CLI记录为准；补证入口前置拒绝不冒充数据库执行）：

```text
(1105, "errCode = 2, detailMessage = collect_list doesn't support order by expression")
```

已取得字段：1: PG _int4 / Doris 未取得成功字段。目标无成功结果，不采样推断目标类型或值。 本原查询未另做完整双端重复，40条任务边界的重复稳定性不能冒充本条已重复。未commit/push，没有以人工CAST候选替换生成结果。

