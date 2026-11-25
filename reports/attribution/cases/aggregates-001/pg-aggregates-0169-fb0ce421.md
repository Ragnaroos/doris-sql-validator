# pg-aggregates-0169-fb0ce421：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写

## 1. 结论与处理建议

- 具体原因：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写。
- 是否修改 SQLGlot：部分基础 task 可修；查询级算法待补证。
- 调查进度：调查未完成。
- 下一步：验证空输入、重复外行、标量多行错误、聚合属于内层/外层、SRF 展开时机后再形成独立任务。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select f1, (select min(unique1) from tenk1 where unique1 > f1) AS gt
  from int4_tbl;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 169；行 450–451；相同回显第 1 次。

阶段：aggregates-001-stage-09；数据库：dsv_wf_agg001_s09。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-09-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-09-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 5，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["0", "1"], ["123456", ""], ["-123456", "0"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT f1, (SELECT MIN(unique1) FROM tenk1 WHERE unique1 > f1) AS gt FROM int4_tbl
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = scalar subquery's correlatedPredicates's operator must be EQ")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:53.820636+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int4 | 未取得 / 未取得 |
| 2 | gt | int4 | 未取得 / 未取得 |

行数：5；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0, 1], [123456, null], [-123456, 0]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = scalar subquery's correlatedPredicates's operator must be EQ")
```

### 尝试 1

时间：2026-11-20T02:29:49.012132+00:00。改写依据：当前 f1 数据下的非等值关联候选，不证明可消除重复外行。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT o.f1, MIN(i.unique1) AS gt FROM int4_tbl o LEFT JOIN tenk1 i ON i.unique1>o.f1 GROUP BY o.f1
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-09-cases.yaml'), Path('reports/validation/aggregates-001-stage-09-validation.json'), 'pg-aggregates-0169-fb0ce421', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int | 11 / 0 |
| 2 | gt | int | 11 / 0 |

行数：5；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[123456, null], [0, 1], [-123456, 0]]
```
工具在内存比较了有限范围完整结果；这里另有 2 行未展示。样本不是完整比较的替代。

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 5, "Doris": 5} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int4 | int | 一致 | 一致 | 不适用 |
| 2 | int4 | int | 一致 | 一致 | 不适用 |

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
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 5, "Doris": 5} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int4 | int | 一致 | 一致 | 不适用 |
| 2 | int4 | int | 一致 | 一致 | 不适用 |

PG 二进制补查时间：2026-11-20T02:24:26.518651+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int4 | 未取得 / 未取得 |
| 2 | gt | int4 | 未取得 / 未取得 |

行数：5；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0, 1], [123456, null], [-123456, 0]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generator.py anonymous_sql / function_fallback_sql：未识别函数保留名称；不是执行源 UDF 定义或完整模拟 PG catalog。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：验证空输入、重复外行、标量多行错误、聚合属于内层/外层、SRF 展开时机后再形成独立任务。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
