# pg-aggregates-0030-549b8efa：PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值

## 1. 结论与处理建议

- 具体原因：PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值。NUMERIC 输入还存在返回 DOUBLE 的独立类型问题。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 30；行 63–63；相同回显第 1 次。

阶段：aggregates-001-stage-01；数据库：dsv_wf_agg001_s01。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-01-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-01-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["0", ""]]
```

首轮结果：**行值或顺序不匹配**。返回记录值、重复次数或要求的顺序不同。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), STDDEV_SAMP(CAST(4.0 AS DOUBLE))
```

首轮具体差异（该报告反例有限，不据此推断全结果）：
首轮比较方式：忽略顺序，保留重复次数。
源端多出 1 行；Doris 多出 1 行（按重复次数）。

| 差异侧 | 实际行样本 / 字段差异 | 多出次数 |
| :--- | :--- | ---: |
| 历史 .out | ["0", ""] | 1 |
| Doris | ["0.0", "0.0"] | 1 |

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:48.351405+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | stddev_pop | float8 | 未取得 / 未取得 |
| 2 | stddev_samp | float8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0.0, null]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | STDDEV_POP(CAST(3.0 AS DOUBLE)) | double | 22 / 31 |
| 2 | STDDEV_SAMP(CAST(4.0 AS DOUBLE)) | double | 22 / 31 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0.0, 0.0]]
```

### 尝试 1

时间：2026-11-20T02:22:27.126635+00:00。改写依据：按有效样本数补采样统计 NULL 行为；原生返回类型和 NUMERIC 契约仍单列。文本与社区相同，仅为控制重跑。


```sql
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), STDDEV_SAMP(CAST(4.0 AS DOUBLE))
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-01-cases.yaml'), Path('reports/validation/aggregates-001-stage-01-validation.json'), 'pg-aggregates-0030-549b8efa', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | STDDEV_POP(CAST(3.0 AS DOUBLE)) | double | 22 / 31 |
| 2 | STDDEV_SAMP(CAST(4.0 AS DOUBLE)) | double | 22 / 31 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0.0, 0.0]]
```

比较来源：PG 二进制读取与当前候选结果复算。

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
| 1 | float8 | double | 一致 | 一致 | 不适用 |
| 2 | float8 | double | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [0.0, null] | 1 |
| Doris多出 | [0.0, 0.0] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### 尝试 2

时间：2026-11-20T02:36:36.627018+00:00。改写依据：STDDEV_SAMP 的单样本 NULL 补偿，保留类型差异。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), CASE WHEN COUNT(CAST(4.0 AS DOUBLE)) < 2 THEN NULL ELSE STDDEV_SAMP(CAST(4.0 AS DOUBLE)) END
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-01-cases.yaml'), Path('reports/validation/aggregates-001-stage-01-validation.json'), 'pg-aggregates-0030-549b8efa', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | STDDEV_POP(CAST(3.0 AS DOUBLE)) | double | 22 / 31 |
| 2 | CASE WHEN COUNT(CAST(4.0 AS DOUBLE)) &lt; 2 THEN NULL ELSE STDDEV_SAMP(CAST(4.0 AS DOUBLE)) END | double | 22 / 31 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0.0, null]]
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
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | float8 | double | 一致 | 一致 | 不适用 |
| 2 | float8 | double | 一致 | 一致 | 不适用 |

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
| 1 | float8 | double | 一致 | 一致 | 不适用 |
| 2 | float8 | double | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [0.0, null] | 1 |
| Doris多出 | [0.0, 0.0] | 1 |

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
| 1 | float8 | double | 一致 | 一致 | 不适用 |
| 2 | float8 | double | 一致 | 一致 | 不适用 |

PG 二进制补查时间：2026-11-20T02:24:23.477269+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | stddev_pop | float8 | 未取得 / 未取得 |
| 2 | stddev_samp | float8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0.0, null]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值。NUMERIC 输入还存在返回 DOUBLE 的独立类型问题。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/mysql.py 统计聚合映射；sqlglot/generators/doris.py；sqlglot/expressions/aggregate.py。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-007：样本统计聚合在有效样本不足时返回 NULL](../../aggregates-001-attribution-summary.md#task-007) | 源语义为样本方差/标准差/协方差的普通聚合；有效样本数小于 2 时的 NULL 契约；协方差按成对非 NULL 计数。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-007 后续修复与验收（2026-11-23）

task-007 的有限输入小样本 NULL 规则已修复并完成约定验收；**本 Case 按原 .out 仍不匹配，不能改写为完整 MATCH**。见[任务报告](../../../fixes/tasks/aggregates-001/fix-007/task-007.md)与[本轮汇总](../../../fixes/aggregates-001-fix-007-summary.md)。第 1–7 节保留首轮归因事实。

在原 stage-01 / dsv_wf_agg001_s01，从本 Case 原 PostgreSQL SQL 经修改后的 SQLGlot 实际生成：

```sql
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), IF(COUNT(CAST(4.0 AS DOUBLE)) < 2, NULL, STDDEV_SAMP(CAST(4.0 AS DOUBLE)))
```

| 检查项 | 本轮实测 |
| :--- | :--- |
| 双端执行与字段 | 均成功，均一行两列；原文无显式 Alias，不要求默认字段名相同 |
| 实时行值 | 两端均为 [0.0,NULL]；样本列修复前是目标 0，现为正确 NULL |
| 原生类型 | 源两列 float8 / 目标两列 double，FLOAT64 逻辑类型及声明一致；浮点精度/Scale 不适用 |
| 原 .out 与框架结论 | 原参考 ["0",""]，当前目标显示 ["0.0",""]；标准 run --stdout 仍判行值或顺序不匹配。剩余显示差异位于总体聚合列，不是 NULL 补偿失效 |
| 源参考核对 | 当前 PG 另转文本为 ["0",""]，与原 .out 一致；没有换基线 |
| 重复与顺序 | 两端各重跑一次结果稳定；无最终 ORDER BY，不要求额外行顺序 |
| 边界与原匹配回归 | 共享任务实测 108 条小样本 NULL 全通过；225 条边界整体含 30 条原生多样本尾差，不冒称全通过。99 条原查询回归中此前 72 条匹配保持 |

PG Parser 为样本统计节点标记小样本 NULL 语义，Doris 补 COUNT 条件；一元 COUNT 与样本聚合使用相同参数，DISTINCT 场景同步去重计数。本条不是手写候选验收。

代码位于 ../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6 加本地修改；最终累积 diff SHA256：073be5b32f6e6208a2a92cd72d980003879511b1d3097fd254356b34ecc04792。原 SQL/.out、YAML、首轮 JSON、数据和比较器未改，未提交/推送。这里只关闭有限输入的小样本 NULL 规则，显示差异、多样本浮点、NaN/Infinity、窗口及 FILTER 等排除范围仍不作完整等价结论。

