# pg-aggregates-0264-e3b16e8d：Doris 拒绝基表别名的列名列表 t1 x(x0,x1)

## 1. 结论与处理建议

- 具体原因：Doris 拒绝基表别名的列名列表 t1 x(x0,x1)。改成显式投影可执行，但当前数据为空且 JOIN USING 的输出类型与 PG 不同，未证明非空合并列语义。
- 是否修改 SQLGlot：需 Schema 感知的投影/USING 类型方案。
- 调查进度：调查未完成。
- 下一步：使用非空、重复、NULL 键最小数据证明别名投影及合并列类型；可复用 qualify，但不能删除列列表。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
select f1, count(*) from
t1 x(x0,x1) left join (t1 left join t2 using(f1)) on (x0 = 0)
group by f1;
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 264；行 668–671；相同回显第 1 次。

阶段：aggregates-001-stage-15；数据库：dsv_wf_agg001_s15。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-15-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-15-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 0，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT f1, COUNT(*) FROM t1 AS x(x0, x1) LEFT JOIN (t1 LEFT JOIN t2 USING (f1)) ON (x0 = 0) GROUP BY f1
```

Doris 首轮实际错误：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 28)\n\n== SQL ==\nSELECT f1, COUNT(*) FROM t1 AS x(x0, x1) LEFT JOIN (t1 LEFT JOIN t2 USING (f1)) ON (x0 = 0) GROUP BY f1\n----------------------------^^^\n')
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:54.076208+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int8 | 未取得 / 未取得 |
| 2 | count | int8 | 未取得 / 未取得 |

行数：0；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 28)\n\n== SQL ==\nSELECT f1, COUNT(*) FROM t1 AS x(x0, x1) LEFT JOIN (t1 LEFT JOIN t2 USING (f1)) ON (x0 = 0) GROUP BY f1\n----------------------------^^^\n')
```

### 尝试 1

时间：2026-11-20T02:36:36.294019+00:00。改写依据：基表列别名外提到投影，需要真实 Schema，不是简单删除列别名。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT f1, COUNT(*) FROM (SELECT f1 AS x0,f2 AS x1 FROM t1) x LEFT JOIN (t1 LEFT JOIN t2 USING (f1)) ON x0=0 GROUP BY f1
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-15-cases.yaml'), Path('reports/validation/aggregates-001-stage-15-validation.json'), 'pg-aggregates-0264-e3b16e8d', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int | 11 / 0 |
| 2 | COUNT(*) | bigint | 20 / 0 |

行数：0；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[]
```

比较来源：PG 二进制读取与当前候选结果复算。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 0, "Doris": 0} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int8 | int | 一致 | 不同 | 不适用 |
| 2 | int8 | bigint | 一致 | 一致 | 不适用 |

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
| 双端行数 | {"PostgreSQL": 0, "Doris": 0} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | int8 | int | 一致 | 不同 | 不适用 |
| 2 | int8 | bigint | 一致 | 一致 | 不适用 |

PG 二进制补查时间：2026-11-20T02:24:26.567621+00:00；原 SQL 不变。这是读取实际二进制数值，不修改比较容差。
**PG 二进制原文结果**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | f1 | int8 | 未取得 / 未取得 |
| 2 | count | int8 | 未取得 / 未取得 |

行数：0；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[]
```

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

Doris 拒绝基表别名的列名列表 t1 x(x0,x1)。改成显式投影可执行，但当前数据为空且 JOIN USING 的输出类型与 PG 不同，未证明非空合并列语义。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- src/doris_sql_validator/recorded_output/parsers.py _parse_pg_regress；src/doris_sql_validator/comparison.py；src/doris_sql_validator/pg_probe.py canonical/declared_type/compare_probe。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：使用非空、重复、NULL 键最小数据证明别名投影及合并列类型；可复用 qualify，但不能删除列列表。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
