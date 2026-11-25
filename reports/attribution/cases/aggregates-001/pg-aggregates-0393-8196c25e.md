# pg-aggregates-0393-8196c25e：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写

## 1. 结论与处理建议

- 具体原因：涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写。
- 是否修改 SQLGlot：部分基础 task 可修；查询级算法待补证。
- 调查进度：调查未完成。
- 下一步：验证空输入、重复外行、标量多行错误、聚合属于内层/外层、SRF 展开时机后再形成独立任务。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select (select max(0) filter (where b1)) from bool_test;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 393；行 1070–1070；相同回显第 1 次。

阶段：aggregates-001-stage-31；数据库：dsv_wf_agg001_s31。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-31-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-31-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["0"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT (SELECT MAX(0) FILTER(WHERE b1)) FROM bool_test
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {')', ',', 'BULK', 'EXCEPT', 'FROM', 'GROUP', 'HAVING', 'INTERSECT', 'INTO', 'LIMIT', 'MINUS', 'ORDER', 'QUALIFY', 'UNION', 'WHERE'}(line 1, pos 28)\n")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:55.720977+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | max | int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {')', ',', 'BULK', 'EXCEPT', 'FROM', 'GROUP', 'HAVING', 'INTERSECT', 'INTO', 'LIMIT', 'MINUS', 'ORDER', 'QUALIFY', 'UNION', 'WHERE'}(line 1, pos 28)\n")
```

### 尝试 1

时间：2026-11-20T02:20:23.065778+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT (SELECT MAX(IF(b1, 0, NULL))) FROM bool_test
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-31-cases.yaml'), Path('reports/validation/aggregates-001-stage-31-validation.json'), 'pg-aggregates-0393-8196c25e', candidate_sql=上列候选文本)
```
**该候选 Doris**：未成功。


```text
(1105, "errCode = 2, detailMessage = access outer query's column in aggregate is not supported")
```

比较来源：PG 二进制读取与当前候选结果复算。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 不同 |
| 错误原因 | 一端成功一端失败 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=不同；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。重复稳定不证明排序键唯一。

### 尝试 2

时间：2026-11-20T02:30:51.678435+00:00。改写依据：按当前原文外层聚合归属构造对照，不将相关改写并入普通 FILTER PR。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT MAX(IF(b1,0,NULL)) FROM bool_test
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-31-cases.yaml'), Path('reports/validation/aggregates-001-stage-31-validation.json'), 'pg-aggregates-0393-8196c25e', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | MAX(IF(b1,0,NULL)) | tinyint | 4 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0]]
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
| 1 | int4 | tinyint | 一致 | 不同 | 不适用 |

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
| 1 | int4 | tinyint | 一致 | 不同 | 不适用 |

PG 二进制补查时间：2026-11-20T02:24:26.764765+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | max | int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[0]]
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

## 8. fix-005：FILTER 改写后的相关查询回归

2026-11-23，原 stage-31/YAML/SQL/.out 不变。用 sqlglot-experiment 的当前累积修改，经 SqlglotTranspiler 从原源文实际生成；最终 09:37:48–09:37:50 UTC 按原 YAML 调用 run --stdout：

```sql
SELECT (SELECT MAX(IF(b1, 0, NULL))) FROM bool_test
```

原 .out 为成功源证据；最终 run --stdout 目标报 `(1105, "errCode = 2, detailMessage = access outer query's column in aggregate is not supported")`。本轮没有重新执行实时 PG 或补查目标成功类型/值，不能验收完整查询。

此为本轮新增的受影响路径回归，不是把本条加入普通 FILTER 任务的已修复范围。表达式改写没有实施 PostgreSQL 相关聚合归属，也没有将其移到外层查询；沿用原研究事项，不冒称 Doris 永远无法模拟。

完整版本、API、168 组共享边界、AVG 独立浮点反例和单元测试见 [fix-005 任务报告](../../../fixes/tasks/aggregates-001/fix-005/task-005.md)。共享边界不算本条逐查询执行了 168 个专属变体；历史首轮和此前候选不覆盖。没有改比较器、源答案或数据，没有 commit/push。

