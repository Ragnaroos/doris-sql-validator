# pg-aggregates-0298-261e1b98：原脚本自定义聚合/函数在 Doris 未定义

## 1. 结论与处理建议

- 具体原因：原脚本自定义聚合/函数在 Doris 未定义。按已审阅的转移函数、初始状态、STRICT、DISTINCT/VARIADIC 语义构造的候选仅适用于这些定义，不能把任意同名 UDF 写成社区核心通用规则。同时 SQLGlot 不识别 ORDER BY USING ~<~。
- 是否修改 SQLGlot：仅关联基础 task；UDF 定义迁移另行处理。
- 调查进度：原因已定位。
- 下一步：把 UDF/聚合定义迁移当外部准备或单独扩展；BALK 的 NULL 常量候选失败，不能声称已等价。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select aggfns(distinct a,a,c order by c using ~<~)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_series(1,2) i;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 298；行 817–819；相同回显第 1 次。

阶段：aggregates-001-stage-17；数据库：dsv_wf_agg001_s17。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-17-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-17-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{\"(2,2,bar)\",\"(3,3,baz)\",\"(1,1,foo)\",\"(0,0,)\"}"]]
```

首轮结果：**SQLGlot 转译失败**。源 SQL 解析失败。首轮证据维持原值；归因重跑不覆盖它。

首轮未生成可执行 Doris SQL；不伪造生成结果。

SQLGlot 原错误：

```text
ParseError: Expecting ). Line 1, Col: 45.
  select aggfns(distinct a,a,c order by c using ~<~)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_se

Invalid expression / Unexpected token. Line 1, Col: 45.
  select aggfns(distinct a,a,c order by c using ~<~)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_se
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.664519+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。

标准只读工具先被 SQLGlot Parser 阻断，不是 PG 执行错误。对明确审阅过的只读原文，额外用 psycopg 直连原阶段，在只读事务和 10 秒超时内执行原 SQL，未替换文本。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | aggfns | _aggtype | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["{\"(2,2,bar)\",\"(3,3,baz)\",\"(1,1,foo)\",\"(0,0,)\"}"]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

没有可安全重放的已保存社区 SQL；转译先失败或原文安全阻断时不强行执行。

初次候选构造/解析的实际阻断（不等于 Doris 已拒绝所有模拟）：

```text
Expecting ). Line 1, Col: 45.
  select aggfns(distinct a,a,c order by c using ~<~)
  from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),
       generate_se
```

没有独立候选实际执行记录；本条依据为控制重跑、代码与明确前提，不声称候选通过。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：
没有取得有效分维度比较；不记作通过。

独立候选：未执行，不把控制重跑当成候选对照。

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

原脚本自定义聚合/函数在 Doris 未定义。按已审阅的转移函数、初始状态、STRICT、DISTINCT/VARIADIC 语义构造的候选仅适用于这些定义，不能把任意同名 UDF 写成社区核心通用规则。同时 SQLGlot 不识别 ORDER BY USING ~<~。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/parser.py _parse_ordered:5877（ORDER BY USING 缺口）。

- sqlglot/generator.py anonymous_sql / function_fallback_sql：未识别函数保留名称；不是执行源 UDF 定义或完整模拟 PG catalog。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：把 UDF/聚合定义迁移当外部准备或单独扩展；BALK 的 NULL 常量候选失败，不能声称已等价。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
