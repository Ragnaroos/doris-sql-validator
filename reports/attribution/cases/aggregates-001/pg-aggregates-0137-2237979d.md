# pg-aggregates-0137-2237979d：历史 .out 成功，但当前 PG 18.1 原文执行失败

## 1. 结论与处理建议

- 具体原因：历史 .out 成功，但当前 PG 18.1 原文执行失败。当前 PG 的分组/相关列规则拒绝原文；先恢复能够重现历史成功的源版本和对象语义。
- 是否修改 SQLGlot：不能据本次执行确认通用补丁。
- 调查进度：前提阻断。
- 下一步：查明原 PostgreSQL 分支/版本和内部状态或分组语义；历史 .out 不改写。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select two + four as g, (select f1 from int4_tbl where f1 = (two + four))
from tenk1 t1
group by two + four order by 1;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 137；行 272–276；相同回显第 1 次。

阶段：aggregates-001-stage-03；数据库：dsv_wf_agg001_s03。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-03-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-03-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 3，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["0", "0"], ["2", ""], ["4", ""]]
```

首轮结果：**SQLGlot 转译失败**。SQLGlot 解析或生成失败。首轮证据维持原值；归因重跑不覆盖它。

首轮未生成可执行 Doris SQL；不伪造生成结果。

SQLGlot 原错误：

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:53.661303+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：未成功。


```text
subquery uses ungrouped column "t1.two" from outer query
LINE 1: ...+ four as g, (select f1 from int4_tbl where f1 = (two + four...
                                                             ^
```

历史参考与当前 PG：本轮源执行失败或工具阻断，保留历史成功基线。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

没有可安全重放的已保存社区 SQL；转译先失败或原文安全阻断时不强行执行。

### 尝试 1

时间：2026-11-20T02:20:19.164503+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT two + four AS g, (SELECT f1 FROM int4_tbl WHERE f1 = (two + four)) FROM tenk1 AS t1 GROUP BY two + four ORDER BY 1 NULLS LAST
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-03-cases.yaml'), Path('reports/validation/aggregates-001-stage-03-validation.json'), 'pg-aggregates-0137-2237979d', candidate_sql=上列候选文本)
```
**该候选 Doris**：未成功。


```text
(1105, "errCode = 2, detailMessage = four, two not in aggregate's output")
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 错误原因 | 两端均失败，但是否同因仍需阅读错误原文 |

重复执行观察：PG 执行状态=一致；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。Doris 候选 执行状态=一致；记录行数=未取得；记录值及重复次数=未取得；最终行顺序=未取得。重复稳定不证明排序键唯一。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：
没有取得有效分维度比较；不记作通过。

最新候选的维度结果：

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 错误原因 | 两端均失败，但是否同因仍需阅读错误原文 |

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

历史 .out 成功，但当前 PG 18.1 原文执行失败。当前 PG 的分组/相关列规则拒绝原文；先恢复能够重现历史成功的源版本和对象语义。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py NULL_ORDERING_SUPPORTED:127；sqlglot/generator.py ordered_sql。

- src/doris_sql_validator/recorded_output/parsers.py _parse_pg_regress；src/doris_sql_validator/comparison.py；src/doris_sql_validator/pg_probe.py canonical/declared_type/compare_probe。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-002：Doris 使用原生 NULLS FIRST/LAST 排序](../../aggregates-001-attribution-summary.md#task-002) | Doris 已实测支持的最终排序与位置/别名排序，保留源端默认 NULL 方向。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：查明原 PostgreSQL 分支/版本和内部状态或分组语义；历史 .out 不改写。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。

## 8. fix-002：排序修复后的实际复查

2026-11-23，SQLGlot checkout 为 sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，加原 task-001 与本轮 task-002 未提交修改；完整代码身份和命令见[fix-002 任务报告](../../../fixes/tasks/aggregates-001/fix-002/task-002.md)。本节是实际后续证据，前文首轮与独立候选事实不改写。

stage-03 原文严格转译成功，实际目标末尾为 `GROUP BY two + four ORDER BY 1 NULLS LAST`。Doris 报 `four, two not in aggregate's output`。本次 PG 18.1 原文也报 SQLSTATE 42803：`subquery uses ungrouped column "t1.two" from outer query`，与原 .out 成功及前文历史补证存在冲突。保留旧事实和当前错误，先核对源输出版本/执行条件；不替换 .out，不改记为源端负向，不据两端失败判成功等价，字段/类型/值/顺序未比较。
