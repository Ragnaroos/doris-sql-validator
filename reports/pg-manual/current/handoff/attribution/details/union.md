# union：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 20 | 20 | 0 | 2 | 18 |


[YAML](../../../../../../cases/postgres/manual/current/union.yaml)；[首轮 Markdown](../../../validation/union/validation.md) / [首轮 JSON](../../../validation/union/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-union-0001-8842af4e

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 1，源行 1–7，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS two UNION SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS two UNION SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0001-8842af4e/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0001-8842af4e/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0002-46978a15

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 2，源行 9–9，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS one UNION SELECT 1 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS one UNION SELECT 1 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0002-46978a15/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0002-46978a15/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0005-4e651bba

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 5，源行 15–15，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0005-4e651bba/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0005-4e651bba/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0006-20935b45

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 6，源行 17–17，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS two UNION SELECT 2 UNION SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS two UNION SELECT 2 UNION SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0006-20935b45/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0006-20935b45/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0007-dee35ffd

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 7，源行 19–19，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0007-dee35ffd/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0007-dee35ffd/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0008-3b1c7020

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 8，源行 21–21，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS two UNION SELECT 2.2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS two UNION SELECT 2.2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0008-3b1c7020/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0008-3b1c7020/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(2,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(2,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0009-774cd2a0

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 9，源行 23–25，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS two UNION SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS two UNION SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0009-774cd2a0/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0009-774cd2a0/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0010-84c85402

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 10，源行 27–27，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS two UNION SELECT 2.2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS two UNION SELECT 2.2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0010-84c85402/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0010-84c85402/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0011-043dbbe9

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 11，源行 29–29，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1 AS one UNION SELECT 1.0::float8 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1 AS one UNION SELECT CAST(1.0 AS DOUBLE) ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0011-043dbbe9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0011-043dbbe9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: float8 → double，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0012-69bca50e

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 12，源行 31–31，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS two UNION ALL SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS two UNION ALL SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0012-69bca50e/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0012-69bca50e/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0013-6809b41b

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 13，源行 33–33，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.0::float8 AS two UNION ALL SELECT 1 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CAST(1.0 AS DOUBLE) AS two UNION ALL SELECT 1 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0013-6809b41b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0013-6809b41b/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: float8 → double，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0014-e4feb980

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 14，源行 35–35，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0014-e4feb980/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0014-e4feb980/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0015-0cb45014

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 15，源行 37–37，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1::float8 AS two UNION SELECT 2 UNION SELECT 2.0::float8 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CAST(1.1 AS DOUBLE) AS two UNION SELECT 2 UNION SELECT CAST(2.0 AS DOUBLE) ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0015-0cb45014/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0015-0cb45014/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: float8 → double，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "double",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0016-75c00d8c

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 16，源行 39–39，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0016-75c00d8c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0016-75c00d8c/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0017-86fb9d5a

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 17，源行 41–41，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1.1 AS two UNION (SELECT 2 UNION ALL SELECT 2) ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 1.1 AS two UNION (SELECT 2 UNION ALL SELECT 2) ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0017-86fb9d5a/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0017-86fb9d5a/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(4,1)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(4,1)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0027-021c0d72

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 27，源行 93–97，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT q2 FROM int8_tbl INTERSECT SELECT q1 FROM int8_tbl ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT q2 FROM int8_tbl INTERSECT SELECT q1 FROM int8_tbl ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0027-021c0d72/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0027-021c0d72/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0028-cb1f47b2

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 28，源行 99–99，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT q2 FROM int8_tbl INTERSECT ALL SELECT q1 FROM int8_tbl ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT q2 FROM int8_tbl INTERSECT ALL SELECT q1 FROM int8_tbl ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0028-cb1f47b2/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0028-cb1f47b2/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = INTERSECT and EXCEPT does not support ALL qualified')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-union-0029-6c7c44d0

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/union.out)；原语句 29，源行 101–101，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT q2 FROM int8_tbl EXCEPT SELECT q1 FROM int8_tbl ORDER BY 1;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT q2 FROM int8_tbl EXCEPT SELECT q1 FROM int8_tbl ORDER BY 1 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-union-0029-6c7c44d0/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-union-0029-6c7c44d0/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 集合查询别名尚未检查 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 本次顺序一致，排序键唯一性未证明 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "集合查询别名尚未检查",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。

本组没有负向查询。

## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-union-0003-ada5fa95 | SELECT 1 AS two UNION ALL SELECT 2; | [.out](../../../../../../cases/postgres/manual/current/assets/union.out)，语句 3 |
| pg-union-0004-f86b7384 | SELECT 1 AS two UNION ALL SELECT 1; | [.out](../../../../../../cases/postgres/manual/current/assets/union.out)，语句 4 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

