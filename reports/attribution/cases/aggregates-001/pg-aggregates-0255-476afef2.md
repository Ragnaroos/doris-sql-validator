# pg-aggregates-0255-476afef2：avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失

## 1. 结论与处理建议

- 具体原因：avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失。
- 是否修改 SQLGlot：先处理类型和数据前提；Parser 缺口另行设计。
- 调查进度：前提阻断。
- 下一步：定义 avg_rec 的比较、分组和数组映射，核对当前 PG 与 .out 的差异后再验收。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select a, count(*) from t_having group by a having a = row(1.0)::avg_rec;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 255；行 650–650；相同回显第 1 次。

阶段：aggregates-001-stage-14；数据库：dsv_wf_agg001_s14。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-14-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-14-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["(1.0)", "2"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT a, COUNT(*) FROM t_having GROUP BY a HAVING a = CAST(ROW(1.0) AS avg_rec)
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 60)\n")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.037494+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | avg_rec | 未取得 / 未取得 |
| 2 | count | int8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["(1.0)", 2]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
Expected TYPE after CAST. Line 1, Col: 79.
  SELECT a, COUNT(*) FROM t_having GROUP BY a HAVING a = CAST(ROW(1.0) AS avg_rec)

Required keyword: 'to' missing for <class 'sqlglot.expressions.functions.Cast'>. Line 1, Col: 79.
  SELECT a, COUNT(*) FROM t_having GROUP BY a HAVING a = CAST(ROW(1.0) AS avg_rec)

Invalid expression / Unexpected token. Line 1, Col: 79.
  SELECT a, COUNT(*) FROM t_having GROUP BY a HAVING a = CAST(ROW(1.0) AS avg_rec)
```

初步候选与社区文本相同；仅保留原句控制重跑，不计独立改写。

没有独立候选实际执行记录；本条依据为控制重跑、代码与明确前提，不声称候选通过。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

独立候选：未执行，不把控制重跑当成候选对照。

PG 二进制补查时间：2026-11-20T02:24:26.547966+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | avg_rec | 未取得 / 未取得 |
| 2 | count | int8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[{"二进制十六进制": "00000001000006a40000000a00010000000000010001"}, 2]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- src/doris_sql_validator/recorded_output/parsers.py _parse_pg_regress；src/doris_sql_validator/comparison.py；src/doris_sql_validator/pg_probe.py canonical/declared_type/compare_probe。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：定义 avg_rec 的比较、分组和数组映射，核对当前 PG 与 .out 的差异后再验收。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
