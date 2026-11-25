# pg-aggregates-0544-3a307492：REGR_COUNT 未映射，普通成对计数候选使查询可执行；其余 VAR_SAMP/SUM 返回类型及数值精度仍有差异，不把整条标为已修复

## 1. 结论与处理建议

- 具体原因：REGR_COUNT 未映射，普通成对计数候选使查询可执行；其余 VAR_SAMP/SUM 返回类型及数值精度仍有差异，不把整条标为已修复。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
SELECT variance(unique1::int4), sum(unique1::int8), regr_count(unique1::float8, unique1::float8)
FROM (SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1) u;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 544；行 1635–1639；相同回显第 1 次。

阶段：aggregates-001-stage-41；数据库：dsv_wf_agg001_s41。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-41-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-41-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["8333541.588539713493", "199980000", "40000"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT VAR_SAMP(CAST(unique1 AS INT)), SUM(CAST(unique1 AS BIGINT)), REGR_COUNT(CAST(unique1 AS DOUBLE), CAST(unique1 AS DOUBLE)) FROM (SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1) AS u
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_COUNT'")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:56.753617+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | variance | numeric | 未取得 / 未取得 |
| 2 | sum | numeric | 未取得 / 未取得 |
| 3 | regr_count | int8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[{"十进制数": "8333541.588539713493"}, {"十进制数": "199980000"}, 40000]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = Can not found function 'REGR_COUNT'")
```

### 尝试 1

时间：2026-11-20T02:20:27.013334+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT VAR_SAMP(CAST(unique1 AS INT)), SUM(CAST(unique1 AS BIGINT)), COUNT(IF(CAST(unique1 AS DOUBLE) IS NOT NULL AND CAST(unique1 AS DOUBLE) IS NOT NULL,1,NULL)) FROM (SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1) AS u
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-41-cases.yaml'), Path('reports/validation/aggregates-001-stage-41-validation.json'), 'pg-aggregates-0544-3a307492', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | VAR_SAMP(CAST(unique1 AS INT)) | double | 22 / 31 |
| 2 | SUM(CAST(unique1 AS BIGINT)) | bigint | 20 / 0 |
| 3 | COUNT(IF(CAST(unique1 AS DOUBLE) IS NOT NULL AND CAST(unique1 AS DOUBLE) IS NOT NULL,1,NULL)) | bigint | 20 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[8333541.588539696, 199980000, 40000]]
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
| 1 | numeric | double | 不同 | 不同 | 信息不足 |
| 2 | numeric | bigint | 不同 | 不同 | 信息不足 |
| 3 | int8 | bigint | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [{"十进制数": "8333541.588539713493"}, {"十进制数": "199980000"}, 40000] | 1 |
| Doris多出 | [8333541.588539696, 199980000, 40000] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

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
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | numeric | double | 不同 | 不同 | 信息不足 |
| 2 | numeric | bigint | 不同 | 不同 | 信息不足 |
| 3 | int8 | bigint | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [{"十进制数": "8333541.588539713493"}, {"十进制数": "199980000"}, 40000] | 1 |
| Doris多出 | [8333541.588539696, 199980000, 40000] | 1 |

PG 二进制补查时间：2026-11-20T02:24:27.081307+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | variance | numeric | 未取得 / 未取得 |
| 2 | sum | numeric | 未取得 / 未取得 |
| 3 | regr_count | int8 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[{"十进制数": "8333541.588539713493"}, {"十进制数": "199980000"}, 40000]]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

REGR_COUNT 未映射，普通成对计数候选使查询可执行；其余 VAR_SAMP/SUM 返回类型及数值精度仍有差异，不把整条标为已修复。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/expressions/aggregate.py RegrCount；sqlglot/generators/doris.py 无专门映射；Generator 默认保留函数名。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-009：REGR_COUNT 成对非 NULL 计数](../../aggregates-001-attribution-summary.md#task-009) | 普通 REGR_COUNT(y,x) 数值列参数；两者都非 NULL 的行数，空输入为 BIGINT 0。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-010 后续修复：REGR_COUNT 已解决，完整查询仍不同

2026-11-24，使用 ../sqlglot-experiment 的实际修改后生成器、原 stage-41 YAML/.out 和 dsv_wf_agg001_s41，只读重跑。HEAD 仍为 089891f2521780e2c5b243005017af9db62f25a6；最终累积未提交 diff SHA256 为 444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。完整范围/实际 SQL/类型与回归见 [fix-010 / task-009](../../../fixes/tasks/aggregates-001/fix-010/task-009.md)。保留前述首轮和独立候选历史。

实际由修改后 SQLGlot 生成，不是手写候选：

```sql
SELECT IF(COUNT(CAST(unique1 AS INT)) < 2, NULL, VAR_SAMP(CAST(unique1 AS INT))), SUM(CAST(unique1 AS BIGINT)), COUNT(IF(NOT CAST(unique1 AS DOUBLE) IS NULL AND NOT CAST(unique1 AS DOUBLE) IS NULL, 1, NULL)) FROM (SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1) AS u
```

双端成功、3列1行。PG 当前结果与原 .out 一致：NUMERIC 8333541.588539713493、NUMERIC 199980000、int8 40000；Doris 本轮为 DOUBLE 8333541.588539706、BIGINT 199980000、BIGINT 40000。双端重复一次结果稳定，无显式别名/最终排序。

第三列（task-009）值与有符号64位类型已对齐，找不到 REGR_COUNT 的错误消失；完整查询按原 .out 规则仍是“行值或顺序不匹配”，不伪称 MATCH。第一列方差值/类型与第二列SUM类型沿用现有聚合类型/精度研究；不因成对计数验收关闭。当前 task-009 完成约定验收，未 commit/push，未扩展修复其他问题。
