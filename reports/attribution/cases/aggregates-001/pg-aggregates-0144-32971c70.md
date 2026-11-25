# pg-aggregates-0144-32971c70：PG booland_statefunc/boolor_statefunc 是 STRICT 内部状态函数；普通 AND/OR 的三值逻辑不能替代

## 1. 结论与处理建议

- 具体原因：PG booland_statefunc/boolor_statefunc 是 STRICT 内部状态函数；普通 AND/OR 的三值逻辑不能替代。显式任一 NULL→NULL 的 CASE 候选当前已对齐，但不是 EVERY 聚合任务。
- 是否修改 SQLGlot：可研究专门状态函数支持，不并入 EVERY。
- 调查进度：原因已定位。
- 下一步：若确实要支持 PG 内部函数，先确认公共 AST 与签名范围；保存 NULL 严格性反例。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
SELECT
  -- boolean or transitions
  -- null because strict
  boolor_statefunc(NULL, NULL)  IS NULL AS "t",
  boolor_statefunc(TRUE, NULL)  IS NULL AS "t",
  boolor_statefunc(FALSE, NULL) IS NULL AS "t",
  boolor_statefunc(NULL, TRUE)  IS NULL AS "t",
  boolor_statefunc(NULL, FALSE) IS NULL AS "t",
  -- actual computations
  boolor_statefunc(TRUE, TRUE) AS "t",
  boolor_statefunc(TRUE, FALSE) AS "t",
  boolor_statefunc(FALSE, TRUE) AS "t",
  NOT boolor_statefunc(FALSE, FALSE) AS "t";
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 144；行 349–361；相同回显第 1 次。

阶段：aggregates-001-stage-05；数据库：dsv_wf_agg001_s05。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-05-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-05-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["t", "t", "t", "t", "t", "t", "t", "t", "t"]]
```

首轮结果：**Doris 执行失败**。源端成功，但生成的 Doris SQL 执行报错；具体错误见 doris_error。首轮证据维持原值；归因重跑不覆盖它。

社区实际生成的 Doris SQL：

```sql
SELECT BOOLOR_STATEFUNC(NULL, NULL) /* boolean or transitions */ /* null because strict */ IS NULL AS `t`, BOOLOR_STATEFUNC(TRUE, NULL) IS NULL AS `t`, BOOLOR_STATEFUNC(FALSE, NULL) IS NULL AS `t`, BOOLOR_STATEFUNC(NULL, TRUE) IS NULL AS `t`, BOOLOR_STATEFUNC(NULL, FALSE) IS NULL AS `t`, BOOLOR_STATEFUNC(TRUE, TRUE) AS `t` /* actual computations */, BOOLOR_STATEFUNC(TRUE, FALSE) AS `t`, BOOLOR_STATEFUNC(FALSE, TRUE) AS `t`, NOT BOOLOR_STATEFUNC(FALSE, FALSE) AS `t`
```

Doris 首轮实际错误：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'BOOLOR_STATEFUNC'")
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:53.770952+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | t | bool | 未取得 / 未取得 |
| 2 | t | bool | 未取得 / 未取得 |
| 3 | t | bool | 未取得 / 未取得 |
| 4 | t | bool | 未取得 / 未取得 |
| 5 | t | bool | 未取得 / 未取得 |
| 6 | t | bool | 未取得 / 未取得 |
| 7 | t | bool | 未取得 / 未取得 |
| 8 | t | bool | 未取得 / 未取得 |
| 9 | t | bool | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[true, true, true, true, true, true, true, true, true]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

原社区生成 SQL 控制重跑（不是独立候选）：
**社区 Doris 控制**：未成功。


```text
(1105, "errCode = 2, detailMessage = Can not found function 'BOOLOR_STATEFUNC'")
```

### 尝试 1

时间：2026-11-20T02:20:19.519475+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT (NULL OR NULL) /* boolean or transitions */ /* null because strict */ IS NULL AS `t`, (TRUE OR NULL) IS NULL AS `t`, (FALSE OR NULL) IS NULL AS `t`, (NULL OR TRUE) IS NULL AS `t`, (NULL OR FALSE) IS NULL AS `t`, (TRUE OR TRUE) AS `t` /* actual computations */, (TRUE OR FALSE) AS `t`, (FALSE OR TRUE) AS `t`, NOT (FALSE OR FALSE) AS `t`
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-05-cases.yaml'), Path('reports/validation/aggregates-001-stage-05-validation.json'), 'pg-aggregates-0144-32971c70', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | t | boolean | 1 / 0 |
| 2 | t | boolean | 1 / 0 |
| 3 | t | boolean | 1 / 0 |
| 4 | t | boolean | 1 / 0 |
| 5 | t | boolean | 1 / 0 |
| 6 | t | boolean | 1 / 0 |
| 7 | t | boolean | 1 / 0 |
| 8 | t | boolean | 1 / 0 |
| 9 | t | boolean | 1 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1, 0, 1, 0, 1, 1, 1, 1, 1]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | bool | boolean | 一致 | 一致 | 不适用 |
| 2 | bool | boolean | 一致 | 一致 | 不适用 |
| 3 | bool | boolean | 一致 | 一致 | 不适用 |
| 4 | bool | boolean | 一致 | 一致 | 不适用 |
| 5 | bool | boolean | 一致 | 一致 | 不适用 |
| 6 | bool | boolean | 一致 | 一致 | 不适用 |
| 7 | bool | boolean | 一致 | 一致 | 不适用 |
| 8 | bool | boolean | 一致 | 一致 | 不适用 |
| 9 | bool | boolean | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [true, true, true, true, true, true, true, true, true] | 1 |
| Doris多出 | [1, 0, 1, 0, 1, 1, 1, 1, 1] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### 尝试 2

时间：2026-11-20T02:22:25.547408+00:00。改写依据：按 ROW/严格 NULL 传播定义补充候选；记录结果，不将用户内部函数映射视为通用规则。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT (NULL OR NULL) /* boolean or transitions */ /* null because strict */ IS NULL AS `t`, (TRUE OR NULL) IS NULL AS `t`, (FALSE OR NULL) IS NULL AS `t`, (NULL OR TRUE) IS NULL AS `t`, (NULL OR FALSE) IS NULL AS `t`, (TRUE OR TRUE) AS `t` /* actual computations */, (TRUE OR FALSE) AS `t`, (FALSE OR TRUE) AS `t`, NOT (FALSE OR FALSE) AS `t`
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-05-cases.yaml'), Path('reports/validation/aggregates-001-stage-05-validation.json'), 'pg-aggregates-0144-32971c70', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | t | boolean | 1 / 0 |
| 2 | t | boolean | 1 / 0 |
| 3 | t | boolean | 1 / 0 |
| 4 | t | boolean | 1 / 0 |
| 5 | t | boolean | 1 / 0 |
| 6 | t | boolean | 1 / 0 |
| 7 | t | boolean | 1 / 0 |
| 8 | t | boolean | 1 / 0 |
| 9 | t | boolean | 1 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1, 0, 1, 0, 1, 1, 1, 1, 1]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

| 比较维度 | 实际观察 |
| :--- | :--- |
| 执行状态 | 一致 |
| 字段数量 | 一致 |
| 显式别名 | 一致 |
| 记录行数 | 一致 |
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | bool | boolean | 一致 | 一致 | 不适用 |
| 2 | bool | boolean | 一致 | 一致 | 不适用 |
| 3 | bool | boolean | 一致 | 一致 | 不适用 |
| 4 | bool | boolean | 一致 | 一致 | 不适用 |
| 5 | bool | boolean | 一致 | 一致 | 不适用 |
| 6 | bool | boolean | 一致 | 一致 | 不适用 |
| 7 | bool | boolean | 一致 | 一致 | 不适用 |
| 8 | bool | boolean | 一致 | 一致 | 不适用 |
| 9 | bool | boolean | 一致 | 一致 | 不适用 |

| 实际差异侧 | 行值反例 | 多出次数 |
| :--- | :--- | ---: |
| PostgreSQL多出 | [true, true, true, true, true, true, true, true, true] | 1 |
| Doris多出 | [1, 0, 1, 0, 1, 1, 1, 1, 1] | 1 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=不同；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

### 尝试 3

时间：2026-11-20T02:28:55.870069+00:00。改写依据：内部状态函数仅按本例严格 NULL 定义展开；不是通用 UDF 自动转换。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT CASE WHEN NULL IS NULL OR NULL IS NULL THEN NULL ELSE (NULL OR NULL) END IS NULL AS `t`, CASE WHEN TRUE IS NULL OR NULL IS NULL THEN NULL ELSE (TRUE OR NULL) END IS NULL AS `t`, CASE WHEN FALSE IS NULL OR NULL IS NULL THEN NULL ELSE (FALSE OR NULL) END IS NULL AS `t`, CASE WHEN NULL IS NULL OR TRUE IS NULL THEN NULL ELSE (NULL OR TRUE) END IS NULL AS `t`, CASE WHEN NULL IS NULL OR FALSE IS NULL THEN NULL ELSE (NULL OR FALSE) END IS NULL AS `t`, CASE WHEN TRUE IS NULL OR TRUE IS NULL THEN NULL ELSE (TRUE OR TRUE) END AS `t` /* actual computations */, CASE WHEN TRUE IS NULL OR FALSE IS NULL THEN NULL ELSE (TRUE OR FALSE) END AS `t`, CASE WHEN FALSE IS NULL OR TRUE IS NULL THEN NULL ELSE (FALSE OR TRUE) END AS `t`, NOT CASE WHEN FALSE IS NULL OR FALSE IS NULL THEN NULL ELSE (FALSE OR FALSE) END AS `t`
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-05-cases.yaml'), Path('reports/validation/aggregates-001-stage-05-validation.json'), 'pg-aggregates-0144-32971c70', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | t | boolean | 1 / 0 |
| 2 | t | boolean | 1 / 0 |
| 3 | t | boolean | 1 / 0 |
| 4 | t | boolean | 1 / 0 |
| 5 | t | boolean | 1 / 0 |
| 6 | t | boolean | 1 / 0 |
| 7 | t | boolean | 1 / 0 |
| 8 | t | boolean | 1 / 0 |
| 9 | t | boolean | 1 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[1, 1, 1, 1, 1, 1, 1, 1, 1]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

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
| 1 | bool | boolean | 一致 | 一致 | 不适用 |
| 2 | bool | boolean | 一致 | 一致 | 不适用 |
| 3 | bool | boolean | 一致 | 一致 | 不适用 |
| 4 | bool | boolean | 一致 | 一致 | 不适用 |
| 5 | bool | boolean | 一致 | 一致 | 不适用 |
| 6 | bool | boolean | 一致 | 一致 | 不适用 |
| 7 | bool | boolean | 一致 | 一致 | 不适用 |
| 8 | bool | boolean | 一致 | 一致 | 不适用 |
| 9 | bool | boolean | 一致 | 一致 | 不适用 |

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
| 双端行数 | {"PostgreSQL": 1, "Doris": 1} |
| 记录值及重复次数 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |

| 位置 | PG 原生类型 | Doris 原生类型 | 逻辑类型 | 声明比较 | 精度/Scale |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | bool | boolean | 一致 | 一致 | 不适用 |
| 2 | bool | boolean | 一致 | 一致 | 不适用 |
| 3 | bool | boolean | 一致 | 一致 | 不适用 |
| 4 | bool | boolean | 一致 | 一致 | 不适用 |
| 5 | bool | boolean | 一致 | 一致 | 不适用 |
| 6 | bool | boolean | 一致 | 一致 | 不适用 |
| 7 | bool | boolean | 一致 | 一致 | 不适用 |
| 8 | bool | boolean | 一致 | 一致 | 不适用 |
| 9 | bool | boolean | 一致 | 一致 | 不适用 |

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

PG booland_statefunc/boolor_statefunc 是 STRICT 内部状态函数；普通 AND/OR 的三值逻辑不能替代。显式任一 NULL→NULL 的 CASE 候选当前已对齐，但不是 EVERY 聚合任务。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generator.py anonymous_sql / function_fallback_sql：未识别函数保留名称；不是执行源 UDF 定义或完整模拟 PG catalog。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

未形成可立即实施的 SQLGlot task；归入汇总的[待补证与讨论事项](../../aggregates-001-attribution-summary.md#pending)。不要把临时候选照抄成通用规则。

本条下一步：若确实要支持 PG 内部函数，先确认公共 AST 与签名范围；保存 NULL 严格性反例。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

没有为本条额外执行独立边界变体；共享规则的边界见对应 task 的代表 Case，不能把它们计为本条逐查询边界已通过。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。
