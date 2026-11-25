# pg-aggregates-0318-e95cf6b4：查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog

## 1. 结论与处理建议

- 具体原因：查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog。当前 PG 反解析文字还与历史 .out 不同。
- 是否修改 SQLGlot：不安排按固定输出伪造 catalog 的 SQLGlot 修复。
- 调查进度：原因已定位。
- 下一步：单列数据库专属观测；底层分位数/UDF/数组功能可独立提取正常成功复现，不能硬编码目录文本。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select pg_get_viewdef('agg_view1'::regclass);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 318；行 883–883；相同回显第 4 次。

阶段：aggregates-001-stage-21；数据库：dsv_wf_agg001_s21。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-21-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-21-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[[" SELECT aggfns(a, b, c ORDER BY (b + 1)) AS aggfns\n   FROM ( VALUES (1,3,'foo'::text), (0,NULL::integer,NULL::text), (2,2,'bar'::text), (3,1,'baz'::text)) v(a, b, c);"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT PG_GET_VIEWDEF(CAST('agg_view1' AS REGCLASS))
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'REGCLASS' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.891229+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | pg_get_viewdef | text | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[" SELECT aggfns(a, b, c ORDER BY (b + 1)) AS aggfns\n   FROM ( VALUES (1,3,'foo'::text), (0,NULL::integer,NULL::text), (2,2,'bar'::text), (3,1,'baz'::text)) v(a, b, c);"]]
```

历史参考与当前 PG：当前 PG 文本行值或显示与历史 .out 不同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

当前/历史反例：

```text
{"当前PG": [["SELECT aggfns(a, b, c ORDER BY (b + 1)) AS aggfns\n   FROM ( VALUES (1,3,'foo'::text), (0,NULL::integer,NULL::text), (2,2,'bar'::text), (3,1,'baz'::text)) v(a, b, c);"]], "历史out": [[" SELECT aggfns(a, b, c ORDER BY (b + 1)) AS aggfns\n   FROM ( VALUES (1,3,'foo'::text), (0,NULL::integer,NULL::text), (2,2,'bar'::text), (3,1,'baz'::text)) v(a, b, c);"]]}
```

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
Expected TYPE after CAST. Line 1, Col: 50.
  SELECT PG_GET_VIEWDEF(CAST('agg_view1' AS REGCLASS))

Required keyword: 'to' missing for <class 'sqlglot.expressions.functions.Cast'>. Line 1, Col: 50.
  SELECT PG_GET_VIEWDEF(CAST('agg_view1' AS REGCLASS))

Expecting ). Line 1, Col: 50.
  SELECT PG_GET_VIEWDEF(CAST('agg_view1' AS REGCLASS))

... and 1 more
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

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog。当前 PG 反解析文字还与历史 .out 不同。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- src/doris_sql_validator/recorded_output/parsers.py _parse_pg_regress；src/doris_sql_validator/comparison.py；src/doris_sql_validator/pg_probe.py canonical/declared_type/compare_probe。

- sqlglot/generator.py anonymous_sql / function_fallback_sql：未识别函数保留名称；不是执行源 UDF 定义或完整模拟 PG catalog。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：单列数据库专属观测；底层分位数/UDF/数组功能可独立提取正常成功复现，不能硬编码目录文本。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
