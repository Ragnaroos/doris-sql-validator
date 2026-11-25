# pg-aggregates-0010-12bf388c：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 t


## fix-013 后续混合数组输入修复（2026-11-24）

沿用本条stage-01原YAML、数据库及.out。当前实验HEAD仍089891f2521780e2c5b243005017af9db62f25a6，累积diff SHA256为b3737ff1ad9a7fafc5c43675efb645a334ccc5795b32c6285de5045f00a1ad55。本轮task-001新增整数/Boolean unknown文本输入转换和显式数组CAST上下文；本条原.out结论仍为**行值或顺序不匹配**，与fix-012相同。

当前PG成功，TEXT投影与原.out多重集合相同；字段原生类型为PG `_text` / Doris `array<text>`。投影不替代类型/顺序验收，本条不借用97条变体的双端重复结论。

本轮实际生成SQL（取自run/当前Transpiler）：

~~~sql
SELECT ANY_VALUE(v) FROM (SELECT CAST(ARRAY('hello', 'world') AS ARRAY<STRING>) AS v) AS v
~~~

当前14条关联原查询与142条同范围回归的逐ID结果均未变化。97条边界中旧ARRAY['1',2]真值反例已修正；Boolean显示、Float/NUMERIC、未知类型和本查询其他独立余项仍按原规则保留。详见 [task-001 / fix-013](../../../fixes/tasks/aggregates-001/fix-013/task-001.md)。任务仍已修改但未完成验收；未改源SQL/.out、数据、比较器或task-003，无commit/push。首轮/前轮事实保留。

## 1. 结论与处理建议

- 具体原因：锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。
- 是否修改 SQLGlot：需修改，但不承诺本条全部匹配。
- 调查进度：原因已定位。
- 下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

“原因已定位”只说明当前差异的原因有证据；不是整条查询或所有输入已证明同义。候选由 Agent 提供，执行事实来自只读工具；本轮没有修改 SQLGlot。

## 2. 源查询与首轮问题



```sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
```

原文件：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql；原语句编号 10；行 30–30；相同回显第 1 次。

阶段：aggregates-001-stage-01；数据库：dsv_wf_agg001_s01。材料：[Case YAML](../../../data-preparation/aggregates-001-stage-01-cases.yaml)、[首轮 validation JSON](../../../validation/aggregates-001-stage-01-validation.json)、[共同环境与准备材料](../../aggregates-001-attribution-summary.md#inputs)。

源 .out：../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.out；已按源原文和出现次数读取成功结果。历史参考行数 1，显示文本样本（空字符串无法单独证明 SQL NULL）：

```text
[["{hello,world}"]]
```

首轮结果：**SQLGlot 转译失败**。SQLGlot 解析或生成失败。首轮证据维持原值；归因重跑不覆盖它。

首轮未生成可执行 Doris SQL；不伪造生成结果。

SQLGlot 原错误：

```text
UnsupportedError: Arrays are not supported by MySQL
```

## 3. 独立候选与实际执行

本次调查开始：2026-11-20T02:16:47.865256+00:00。使用锁定 SQLGlot feb0e08aba28a29590596bb3f5761fbaeb0e98b9；UTC、10 秒只读查询超时；共同版本/会话见汇总。没有重装或改变阶段数据。
**本轮原文 PostgreSQL**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | any_value | _text | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[["hello", "world"]]]
```

历史参考与当前 PG：当前 PG 文本行值及重复次数与 .out 相同。此核对是文本多重集合（保留重复次数），不证明最终顺序或字段类型；历史 .out 仍是首轮基线。

没有可安全重放的已保存社区 SQL；转译先失败或原文安全阻断时不强行执行。

### 尝试 1

时间：2026-11-20T02:20:12.973459+00:00。改写依据：根据源表达式语义构造的独立候选；非社区补丁，规则须分别验证。文本不同于已保存社区输出；仍须独立验收。


```sql
SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v
```

实际执行入口：probe_postgres_case。

内存调用：

```text
probe_postgres_case(Path('reports/data-preparation/aggregates-001-stage-01-cases.yaml'), Path('reports/validation/aggregates-001-stage-01-validation.json'), 'pg-aggregates-0010-12bf388c', candidate_sql=上列候选文本)
```
**该候选 Doris**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | ANY_VALUE(v) | array&lt;varchar(5)&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[\"hello\", \"world\"]"]]
```

比较来源：probe-pg-case 的实时 PG 证据（未额外放宽容差）。

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
| 1 | _text | array&lt;varchar(5)&gt; | 一致 | 不同 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

## 4. 分维度比较

社区输出与实时源端（有 PG 二进制证据时优先它，避免 extra_float_digits=0 的显示舍入）：
没有取得有效分维度比较；不记作通过。

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
| 1 | _text | array&lt;varchar(5)&gt; | 一致 | 不同 | 不适用 |

类型比较限制：现有工具对 _int4 与 ARRAY<INT> 等嵌套声明未递归归一化，声明“不同”有时包含别名问题；TINYINT 与 INT、NUMERIC 与 DOUBLE 则是真实差异，不能一并忽略。未知类型/精度不算通过。无最终 ORDER BY 时仅对结果行用多重集合，数组元素本身不随意重排；有 ORDER BY 仍需确认并列键约束。

## 5. 代码依据与具体归因

锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收。

分析基线：feb0e08aba28a29590596bb3f5761fbaeb0e98b9，未重新检查远端最新 main。以下为实际 checkout 的路径/函数定位：

- sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py array_sql:654。

首轮自动分类只是观察结果。例如 ONLY 被误作表名时，“Doris 环境问题”并不表示缺少真实源表。实际错误与生成文本优先于自动标签。

## 6. 修复方案与验收要求

共同实现计划、PR 范围、依赖和单元测试集中在汇总；本条不复制通用方案。

| task | 本条适用范围与剩余条件 |
| :--- | :--- |
| [task-001：Doris 数组字面量生成](../../aggregates-001-attribution-summary.md#task-001) | ARRAY[...] 的标量、NULL、空数组与嵌套字面量；按 AST 类型保留元素 CAST。；本 Case 还需排除第 1 节列出的其他独立问题。 |

本条下一步：按关联 task 的最小复现及边界验收；保留本 Case 的其他独立差异。

单个 task 的最小复现通过，不代表整条 Case 已匹配；不更改源 SQL/.out、阶段数据或比较规则来制造通过。

## 7. 已测边界与限制

### 数组构造 NULL 与嵌套

执行时间：2026-11-20T02:25:14.085517+00:00。新变体，不借用历史 .out。

PostgreSQL：

```sql
SELECT ARRAY[1,NULL,2] AS a, ARRAY[ARRAY[1,2],ARRAY[3,4]] AS b
```

Doris 独立候选：

```sql
SELECT ARRAY(1,CAST(NULL AS INT),2) AS a, ARRAY(ARRAY(1,2),ARRAY(3,4)) AS b
```

实际调用：probe_postgres_case(..., candidate_sql=上列目标文本, source_variant_sql=上列源文本)，与 CLI 的 --source-variant-sql 相同，只返回内存事实。
**源变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | _int4 | 未取得 / 未取得 |
| 2 | b | _int4 | 未取得 / 未取得 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[[[1, null, 2], [[1, 2], [3, 4]]]]
```
**目标变体**：成功。

| 字段位置 | 名称 | 实际原生类型 | 精度 / Scale |
| :--- | :--- | :--- | :--- |
| 1 | a | array&lt;int&gt; | 255 / 0 |
| 2 | b | array&lt;array&lt;tinyint&gt;&gt; | 255 / 0 |

行数：1；样本（最多 3 行，SQL NULL 写为 null；十进制数保留标签）：

```text
[["[1, null, 2]", "[[1, 2], [3, 4]]"]]
```

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
| 1 | _int4 | array&lt;int&gt; | 一致 | 不同 | 不适用 |
| 2 | _int4 | array&lt;array&lt;tinyint&gt;&gt; | 一致 | 不同 | 不适用 |

重复执行观察：PG 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。Doris 候选 执行状态=一致；记录行数=一致；记录值及重复次数=一致；最终行顺序=无最终 ORDER BY，忽略结果行顺序但保留重复次数。重复稳定不证明排序键唯一。

本报告仅覆盖这里明确执行的原文与变体；不证明全部输入同义，不证明全部字段元数据、排序唯一性、复杂类型域或资源行为已验收。需要后续修复时，由人选 task 调用修复 Skill，本轮未自动进入修复。


## fix-011 后续类型核验（2026-11-24）

沿用原 aggregates-001-stage-01 YAML及其实际数据库 dsv_wf_agg001_s01；本轮未改源SQL/.out、数据、比较规则或SQLGlot代码。实际import为../sqlglot-experiment，HEAD 089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff指纹仍为444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18。任务仍为“已修改但未完成验收”，详细类型子项见 [task-001 / fix-011](../../../fixes/tasks/aggregates-001/fix-011/task-001.md)。前述首轮/前轮证据不覆盖。

本轮原.out规则的实际结果：**行值或顺序不匹配**。实时PG成功，文本化结果与原.out一致。元素值相同，但PG text[] / Doris ARRAY<VARCHAR(5)>仍有真实声明差异；.out数组显示差异另列。

实际由当前生成器产生的Doris SQL：

```sql
SELECT ANY_VALUE(v) FROM (SELECT ARRAY('hello', 'world') AS v) AS v
```


已取得字段：1: PG _text / Doris array<varchar(5)>。双端行数为1/1；结构化值/重复次数观察为“一致”；顺序观察为“无最终 ORDER BY，忽略结果行顺序但保留重复次数”。 本原查询未另做完整双端重复，40条任务边界的重复稳定性不能冒充本条已重复。未commit/push，没有以人工CAST候选替换生成结果。

## fix-012 后续源元素类型修复（2026-11-24）

沿用stage-01原YAML、数据库和.out。默认转译使用../sqlglot-experiment的本轮修改；HEAD仍089891f2521780e2c5b243005017af9db62f25a6，累积未提交diff SHA256为309f2694a0a1ed3760b346c4dbd4d1b02da43c9b55830163c0f036b738b8e675。本条原先的PG text[] / Doris ARRAY<VARCHAR(5)>类型差异已修正为ARRAY<TEXT>；结构化元素值一致，但原.out数组显示差异仍保留，不冒称MATCH。

本轮run --stdout实际结果：**行值或顺序不匹配**。当前PG成功，TEXT投影与原.out多重集合相同；包装不作为类型/最终排序验收。已取得PG原生类型：`_text`；目标补证：`array<text>`。

实际从原Case生成的Doris SQL：

~~~sql
SELECT ANY_VALUE(v) FROM (SELECT CAST(ARRAY('hello', 'world') AS ARRAY<STRING>) AS v) AS v
~~~

同任务37条边界双端重跑，7条旧默认类型反例已修正；本条原查询不借用边界的重复执行结论。细节见 [task-001 / fix-012](../../../fixes/tasks/aggregates-001/fix-012/task-001.md)。task-001仍未完成全部类型验收；本轮未修改数据、比较器、源SQL/.out或task-003，未commit/push。首轮及之前证据保留。



## fix-014：有限浮点输入修复后的原查询复查（2026-11-24）

本条仍用stage-01原YAML、阶段库和.out；原比较结果为**行值或顺序不匹配**，与fix-013相同。当前源查询成功，另以完整字段TEXT投影核对原.out多重集合一致；投影不替代原生类型/必要顺序验收。当前已取得类型为PG _text / Doris array<text>。其他独立执行/类型/显示余项不关闭。

本轮继续task-001的十进制unknown浮点输入，41条变体原生元素核验通过，但原比较器仍有15显示不同和1驱动解码失败；变体证据不能冒充本原查询的完整边界/重复验收。原142条固定回归逐ID不变，task-001仍未完成验收；新发现的已知REAL元素CAST差异及下一轮方案写在[原归因task条目](../../aggregates-001-attribution-summary.md#task-001)，详细实际生成SQL/错误、回归及限制见[fix-014任务报告](../../../fixes/tasks/aggregates-001/fix-014/task-001.md)。

代码HEAD仍089891f2521780e2c5b243005017af9db62f25a6，累积diff SHA256为32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73。未改源SQL/.out、数据、比较器或其他任务；未commit/push。首轮/前轮事实保留。

