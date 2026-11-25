# pg-aggregates-0173-5bef76d3：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select max(unique2) from tenk1 order by 1;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 173；行 459–459；相同回显第 1 次。

阶段：aggregates-001-stage-09；数据库：dsv_wf_agg001_s09。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-09-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-09-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["9999"]]
```

首轮结果：**SQLGlot 转译失败**。SQLGlot 解析或生成失败。首轮证据维持原值；归因重跑不覆盖它。

首轮未生成可执行 Doris SQL；不伪造生成结果。

SQLGlot 原错误：

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:53.952677+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | max | int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[9999]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

没有可安全重放的已保存社区 SQL；转译先失败或原文安全阻断时不强行执行。

### 尝试 1

时间：2026-11-20T02:20:19.729893+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT MAX(unique2) FROM tenk1 ORDER BY 1 NULLS LAST
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-09-cases.yaml'), Path('reports/validation/aggregates-001-stage-09-validation.json'), 'pg-aggregates-0173-5bef76d3', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | MAX(unique2) | int | 11 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[9999]]
```

比较来源：PG 二进制读取与当前候选结果复算。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 本次顺序一致，排序键唯一性未证明 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int4 | int | 一致 | 一致 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=本次顺序一致，排序键唯一性未证明。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=本次顺序一致，排序键唯一性未证明。重复稳定不证明排序键唯一。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：
没有取得有效分维度比较；不记作通过。

最新候选的维度结果：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 本次顺序一致，排序键唯一性未证明 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int4 | int | 一致 | 一致 | 不适用 |

PG 二进制补查时间：2026-11-20T02:24:26.531093+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | max | int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[9999]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py NULL_ORDERING_SUPPORTED:127；sqlglot/generator.py ordered_sql。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-002：Doris 使用原生 NULLS FIRST/LAST 排序](../../aggregates-001-attribution-summary.md#task-002) | Doris 已实测支持的最终排序与位置/别名排序，保留源端默认 NULL 方向。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

### 位置排序显式 NULLS LAST

执行时间：2026-11-20T02:25:14.187576+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT x FROM (VALUES(NULL),(1),(2)) v(x) ORDER BY 1 ASC NULLS LAST
```

Doris 独立候选：

```sql
SELECT x FROM (SELECT CAST(NULL AS INT) x UNION ALL SELECT 1 UNION ALL SELECT 2) v ORDER BY 1 ASC NULLS LAST
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | x | int4 | 未取得 / 未取得 |

行数：3；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1], [2], [null]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | x | int | 11 / 0 |

行数：3；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1], [2], [null]]
```

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 3, "Doris": 3} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 本次顺序一致，排序键唯一性未证明 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int4 | int | 一致 | 一致 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=本次顺序一致，排序键唯一性未证明。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=本次顺序一致，排序键唯一性未证明。重复稳定不证明排序键唯一。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-002：排序修复后的实际复查

2026-11-23，SQLGlot checkout 为 sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，加原 task-001 与本轮 task-002 未提交修改；完整代码身份和命令见[fix-002 任务报告](../../../fixes/tasks/aggregates-001/fix-002/task-002.md)。本节是实际后续证据，前文首轮与独立候选事实不改写。

stage-09 原文经修改后 SQLGlot 实际生成 `SELECT MAX(unique2) FROM tenk1 ORDER BY 1 NULLS LAST`。原 CLI/.out 匹配；实时双端均为 1 列、1 行 `[[9999]]`，PG int4 / Doris int 声明映射一致，精度/Scale 不适用，无显式 Alias 要求。实时源文本与 .out 顺序一致，双端各增加一次执行结果一致。本条通过当前样本的排序、类型和行值检查；单行原例另以任务报告的多行 NULL 边界补证，不证明所有输入。
