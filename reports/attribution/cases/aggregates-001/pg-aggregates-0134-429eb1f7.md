# pg-aggregates-0134-429eb1f7：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写

## 1. 结论与处理建议

- 具体原因：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写。
- 是否修改 SQLGlot：部分基础 task 可修；查询级算法待补证。
- 调查进度：调查未完成。
- 下一步：验证空输入、重复外行、标量多行错误、聚合属于内层/外层、SRF 展开时机后再形成独立任务。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select s1, s2, sm
from generate_series(1, 3) s1,
     lateral (select s2, sum(s1 + s2) sm
              from generate_series(1, 3) s2 group by s2) ss
order by 1, 2;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 134；行 258–262；相同回显第 1 次。

阶段：aggregates-001-stage-03；数据库：dsv_wf_agg001_s03。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-03-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-03-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 9，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["1", "1", "2"], ["1", "2", "3"], ["1", "3", "4"]]
```

首轮结果：**SQLGlot 转译失败**。SQLGlot 解析或生成失败。首轮证据维持原值；归因重跑不覆盖它。

首轮未生成可执行 Doris SQL；不伪造生成结果。

SQLGlot 原错误：

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering

'NULLS LAST' translation not supported with positional ordering
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:53.640255+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | s1 | int4 | 未取得 / 未取得 |
| 2 | s2 | int4 | 未取得 / 未取得 |
| 3 | sm | int8 | 未取得 / 未取得 |

行数：9；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1, 1, 2], [1, 2, 3], [1, 3, 4]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

没有可安全重放的已保存社区 SQL；转译先失败或原文安全阻断时不强行执行。

### 尝试 1

时间：2026-11-20T02:20:19.013111+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT s1, s2, sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s1 FROM NUMBERS('number' = '3')) AS s1, LATERAL (SELECT s2, SUM(s1 + s2) AS sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s2 FROM NUMBERS('number' = '3')) AS s2 GROUP BY s2) AS ss ORDER BY 1 NULLS LAST, 2 NULLS LAST
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-03-cases.yaml'), Path('reports/validation/aggregates-001-stage-03-validation.json'), 'pg-aggregates-0134-429eb1f7', candidate_sql=上列候选文本)
```
**该候选 Doris**：未成功。


```text
(1105, "errCode = 2, detailMessage = \nmissing 'UNNEST' at '('(line 1, pos 110)\n")
```

比较来源：PG 二进制读取与当前候选结果复算。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=本次顺序一致，排序键唯一性未证明。Doris 候选 执行状态=不同；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。重复稳定不证明排序键唯一。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：
没有取得有效分维度比较；不记作通过。

最新候选的维度结果：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

PG 二进制补查时间：2026-11-20T02:24:26.425562+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | s1 | int4 | 未取得 / 未取得 |
| 2 | s2 | int4 | 未取得 / 未取得 |
| 3 | sm | int8 | 未取得 / 未取得 |

行数：9；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1, 1, 2], [1, 2, 3], [1, 3, 4]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py NULL_ORDERING_SUPPORTED:127；sqlglot/generator.py ordered_sql。

- sqlglot/parsers/postgres.py _build_generate_series/FUNCTIONS:146；sqlglot/generator.py explodinggenerateseries_sql:5821；sqlglot/generators/doris.py。

- sqlglot/generator.py anonymous_sql / function_fallback_sql：未识别函数保留名称；不是执行源 UDF 定义或完整模拟 PG catalog。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-002：Doris 使用原生 NULLS FIRST/LAST 排序](../../aggregates-001-attribution-summary.md#task-002) | Doris 已实测支持的最终排序与位置/别名排序，保留源端默认 NULL 方向。；本 Case 还需排除第 1 节列出的其他独立问题。 |
| [task-008：FROM 位置的常量整数 GENERATE_SERIES](../../aggregates-001-attribution-summary.md#task-008) | FROM 中非相关、整数常量起止与步长、源端 INT4 范围；别名和输出列，正/负步长与空区间。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：验证空输入、重复外行、标量多行错误、聚合属于内层/外层、SRF 展开时机后再形成独立任务。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-002：排序修复后的实际复查

2026-11-23，SQLGlot checkout 为 sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，加原 task-001 与本轮 task-002 未提交修改；完整代码身份和命令见[fix-002 任务报告](../../../fixes/tasks/aggregates-001/fix-002/task-002.md)。本节是实际后续证据，前文首轮与独立候选事实不改写。

stage-03 原文经当前修改后 SQLGlot 生成 `ORDER BY 1 NULLS LAST, 2 NULLS LAST`，严格转译成功，不再报位置排序不支持。原 .out 与实时 PG 均成功，9 行按顺序文本化一致；Doris 在 GENERATE_SERIES 参数处报 `mismatched input ',' expecting EQ(line 1, pos 40)`，目标类型/值/顺序未比较。普通非相关 FROM 序列基础关联 task-008，但本条 LATERAL/相关范围不能由该任务直接承诺；继续既有查询级研究，不伪造整条 MATCH。


## 9. fix-008：常量整数序列修复后的实际复测

时间 2026-11-23T10:47:14.875742+00:00；代码、环境、有限边界见 [fix-008 汇总](../../../fixes/aggregates-001-fix-008-summary.md)与[本条新生成 SQL/完整比较](../../../fixes/tasks/aggregates-001/fix-008/task-008.md#statement-134)。保留原源 SQL/.out、Case ID 和 aggregates-001-stage-03-cases.yaml 对应数据状态；首轮与前轮事实不覆盖。运行时从 ../sqlglot-experiment 导入（HEAD 089891f2521780e2c5b243005017af9db62f25a6，加报告记录的累积 diff），不是手写候选。

本轮 run --stdout 整条结论：**Doris 执行失败**。常量序列已转换；外层 LATERAL 相关聚合子查询仍被 Doris 拒绝，复用查询级重写研究。

实际新生成并执行的 Doris SQL：

```sql
SELECT s1, s2, sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s1 FROM NUMBERS('number' = '3')) AS s1, LATERAL (SELECT s2, SUM(s1 + s2) AS sm FROM (SELECT CAST(1 + number * 1 AS INT) AS s2 FROM NUMBERS('number' = '3')) AS s2 GROUP BY s2) AS ss ORDER BY 1 NULLS LAST, 2 NULLS LAST
```

当前 PG 原文执行成功；记录 `[[1,1,2],[1,2,3],[1,3,4],[2,1,3],[2,2,4],[2,3,5],[3,1,4],[3,2,5],[3,3,6]]`。Doris 无完整结果，实际错误：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'UNNEST' at '('(line 1, pos 110)\n")
```

至少一端没有成功结果，字段类型、值与顺序没有完整双端验收。

当前 PG 显示文本与原 .out 的值和重复次数相同；这不替代原生类型/顺序检查。

本轮 task-008 的非 NULL 常量 INT4 序列主路径已实测，NULL 参数仍未支持，任务整体尚未完成验收；本条的其他独立问题不混入序列补丁。未修改比较规则或数据，未 commit/push。


## 10. fix-009：task-008 NULL 参数完成验收

本轮继续原 task-008，不是开始 task-009。常量 INT4/NULL 序列规则已完成约定验收：123 条边界/上下文双端通过并复跑稳定，含NULL与零步长共存、列名/INT类型和空结果；详见[本轮汇总](../../../fixes/aggregates-001-fix-009-summary.md)与[任务报告](../../../fixes/tasks/aggregates-001/fix-009/task-008.md)。

本条仍按原阶段 YAML 运行，时间 2026-11-23T11:02:13.364770+00:00，框架整条结果为 **Doris 执行失败**。新生成 Doris SQL 与 fix-008 本条保存结果逐字相同；原序列参数不含NULL，本轮不重复复制该SQL。 原 SQL/.out、首轮统计、比较规则和数据不变。原聚合NULL输入不等于序列参数NULL；本条其他类型/统计/UDF/查询级等限制仍按前轮记录保留，序列task验收不把整条失败或类型差异改成完整匹配。本轮没有重新执行本条实时PG类型补证，不将沿用证据写成新实测。未 commit/push。


