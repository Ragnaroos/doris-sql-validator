# pg-aggregates-0005-11b43275：1.5000000000000000 与 1.5 的显示差异之外，PG AVG(INT) 为 NUMERIC，Doris 为 DOUBLE；数值相同

## 1. 结论与处理建议

- 具体原因：1.5000000000000000 与 1.5 的显示差异之外，PG AVG(INT) 为 NUMERIC，Doris 为 DOUBLE；数值相同不消除真实返回类型契约差异。
- 是否修改 SQLGlot：需类型感知方案，尚未形成独立可实施任务。
- 调查进度：调查未完成。
- 下一步：用明确输入类型、精度/Scale 和溢出边界验证 AVG 返回契约；不能统一转字符串制造匹配。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
SELECT avg(four) AS avg_1 FROM onek;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 5；行 23–23；相同回显第 1 次。

阶段：aggregates-001-stage-01；数据库：dsv_wf_agg001_s01。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-01-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-01-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["1.5000000000000000"]]
```

首轮结果：**行值或顺序不匹配**。返回记录值、重复次数或要求的顺序不同。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT AVG(four) AS avg_1 FROM onek
```

首轮具体差异（该报告反例有限，不据此推断全结果）：
首轮比较方式：忽略顺序，保留重复次数。
源端多出 1 行；Doris 多出 1 行（按重复次数）。

| 差异侧 | 实际行样本 / 字段差异 | 多出次数 |
| :--- | :--- | ---: |
| 历史 .out | ["1.5000000000000000"] | 1 |
| Doris | ["1.5"] | 1 |

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:47.617695+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | avg_1 | numeric | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[{"十进制数": "1.5000000000000000"}]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | avg_1 | double | 22 / 31 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1.5]]
```

初步候选与社区文本相同；仅保留原句控制重跑，不计独立改写。

没有独立候选实际执行记录；本条依据为控制重跑、代码与明确前提，不声称候选通过。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：

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
| 1 | numeric | double | 不同 | 不同 | 信息不足 |

独立候选：未执行，不把控制重跑当成候选对照。

PG 二进制补查时间：2026-11-20T02:24:23.386974+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | avg_1 | numeric | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[{"十进制数": "1.5000000000000000"}]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

1.5000000000000000 与 1.5 的显示差异之外，PG AVG(INT) 为 NUMERIC，Doris 为 DOUBLE；数值相同不消除真实返回类型契约差异。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- src/doris_sql_validator/recorded_output/parsers.py _parse_pg_regress；src/doris_sql_validator/comparison.py；src/doris_sql_validator/pg_probe.py canonical/declared_type/compare_probe。

- sqlglot/generators/doris.py TYPE_MAPPING / 继承 MySQL；缺省 NUMERIC 到 DECIMAL 的精度及聚合累计类型需要单独类型分析。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：用明确输入类型、精度/Scale 和溢出边界验证 AVG 返回契约；不能统一转字符串制造匹配。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
