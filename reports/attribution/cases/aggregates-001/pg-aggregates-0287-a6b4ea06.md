# pg-aggregates-0287-a6b4ea06：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select array_agg(distinct a)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 287；行 782–783；相同回显第 1 次。

阶段：aggregates-001-stage-17；数据库：dsv_wf_agg001_s17。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-17-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{1,2,3,NULL}"]]
```

首轮结果：**行值或顺序不匹配**。返回记录值、重复次数或要求的顺序不同。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT COLLECT_LIST(DISTINCT a) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v
```

首轮具体差异（该报告反例有限，不据此推断全结果）：
首轮比较方式：忽略顺序，保留重复次数。
源端多出 1 行；Doris 多出 1 行（按重复次数）。

| 差异侧 | 实际行样本 / 字段差异 | 多出次数 |
| :--- | :--- | ---: |
| 历史 .out | ["{1,2,3,NULL}"] | 1 |
| Doris | ["[1, 2, 3]"] | 1 |

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.352838+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | array_agg | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[1, 2, 3, null]]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | COLLECT_LIST(DISTINCT a) | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[1, 2, 3]"]]
```

### 尝试 1

时间：2026-11-20T02:20:20.588736+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ARRAY_AGG(DISTINCT a) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-17-cases.yaml'), Path('reports/validation/aggregates-001-stage-17-validation.json'), 'pg-aggregates-0287-a6b4ea06', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ARRAY_AGG(DISTINCT a) | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[1, 2, 3, null]"]]
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
| PostgreSQL多出 | [[1, 2, 3, null]] | 1 |
| Doris多出 | ["[1, 2, 3]"] | 1 |

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

### ARRAY_AGG DISTINCT 保留 NULL

执行时间：2026-11-20T02:25:14.275625+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT ARRAY_AGG(DISTINCT x) AS a FROM (VALUES(1),(NULL),(1),(2)) v(x)
```

Doris 独立候选：

```sql
SELECT ARRAY_AGG(DISTINCT x) AS a FROM (SELECT 1 x UNION ALL SELECT NULL UNION ALL SELECT 1 UNION ALL SELECT 2) v
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[1, 2, null]]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[1, null, 2]"]]
```

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [[1, 2, null]] | 1 |
| Doris多出 | ["[1, null, 2]"] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### ARRAY_AGG 空输入

执行时间：2026-11-20T02:25:14.362200+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT ARRAY_AGG(x) AS a FROM (VALUES(1)) v(x) WHERE FALSE
```

Doris 独立候选：

```sql
SELECT ARRAY_AGG(x) AS a FROM (SELECT 1 x) v WHERE FALSE
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[null]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[]"]]
```

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [null] | 1 |
| Doris多出 | ["[]"] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### ARRAY_AGG 空输入补偿

执行时间：2026-11-20T02:28:56.103091+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT ARRAY_AGG(x) AS a FROM (VALUES(1)) v(x) WHERE FALSE
```

Doris 独立候选：

```sql
SELECT CASE WHEN COUNT(*)=0 THEN NULL ELSE ARRAY_AGG(x) END AS a FROM (SELECT 1 x) v WHERE FALSE
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[null]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | array&lt;tinyint&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[null]]
```

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _int4 | array&lt;tinyint&gt; | 一致 | 不同 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### ARRAY_AGG 全 NULL 保留次数

执行时间：2026-11-20T02:28:56.185452+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT ARRAY_AGG(x) AS a FROM (VALUES(NULL::int),(NULL)) v(x)
```

Doris 独立候选：

```sql
SELECT CASE WHEN COUNT(*)=0 THEN NULL ELSE ARRAY_AGG(x) END AS a FROM (SELECT CAST(NULL AS INT) x UNION ALL SELECT NULL) v
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[null, null]]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | array&lt;int&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[null, null]"]]
```

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | _int4 | array&lt;int&gt; | 一致 | 不同 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-003：NULL 与空输入修复后的复查

2026-11-23，使用 sqlglot-experiment 的 HEAD 089891f2521780e2c5b243005017af9db62f25a6 加既有 task-001/002 和本轮 task-003 未提交修改；完整身份、实际命令/SQL 和验收限制见[fix-003 任务报告](../../../fixes/tasks/aggregates-001/fix-003/task-003.md)。原首轮及前文独立候选事实不覆盖。

stage-17 已实际生成 NULLIF(ARRAY_AGG(DISTINCT a), ARRAY())，完整 SQL 见任务报告。原 CLI 仍为行值/顺序不匹配：.out 是 {1,2,3,NULL}，Doris 是 [1, 2, 3, null]。实时 PG 和目标均成功，各 1 列/1 行，结构化元素 [1,2,3,NULL] 及重复执行一致，NULL 不再丢失；PG 文本与 .out 一致。类型 _int4 / array<tinyint> 是真实元素位宽差异，无显式 Alias。另一个 DISTINCT 边界实际为 PG [1,2,NULL] / Doris [1,NULL,2]，原查询不保证聚合内顺序，不调整比较规则制造通过。22 组边界、类型限制、布尔和 TIMESTAMP 独立补证都写在同一任务报告；本任务暂不关闭。


## fix-011 后续类型核验（2026-11-24）

沿用原 aggregates-001-stage-17 YAML及其实际数据库 dsv_wf_agg001_s17；本轮未改源SQL/.out、数据、比较规则或SQLGlot代码。实际import为../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff指纹仍为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。任务仍为“已修改但未完成验收”，详细类型子项见 [task-003 / fix-011](../../../fixes/tasks/aggregates-001/fix-011/task-003.md)。前述首轮/前轮证据不覆盖。

本轮原.out规则的实际结果：**行值或顺序不匹配**。实时PG成功，文本化结果与原.out一致。本条仍是INT32/TINYINT数组元素位宽差异；结构化值相同不等于类型相同。

实际由当前生成器产生的Doris SQL：

```sql
SELECT NULLIF(ARRAY_AGG(DISTINCT a), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v
```


已取得字段：1: PG _int4 / Doris array<tinyint>。双端行数为1/1；结构化值/重复次数观察为“一致”；顺序观察为“无最终 ORDER BY，忽略结果行顺序但保留重复次数”。 本原查询未另做完整双端重复，40条任务边界的重复稳定性不能冒充本条已重复。未commit/push，没有以人工CAST候选替换生成结果。

