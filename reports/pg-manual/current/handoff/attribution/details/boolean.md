# boolean：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 45 | 33 | 12 | 27 | 6 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/boolean.yaml)；[首轮 Markdown](../../../validation/boolean/validation.md) / [首轮 JSON](../../../validation/boolean/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-boolean-0010-222849e6

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 10，源行 31–31，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bool 'y' AS true;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('y' AS BOOLEAN) AS `true`
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c1fc917cb0eae91bab50aa5654d09e17cec3656dd19d850587d575060c14665b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['t']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-008 保留合法 PostgreSQL 布尔文本前缀：PG 的 y/n/of 是合法输入；当前 Doris CAST 返回 NULL。基于 LOWER/TRIM 的合法前缀规范化候选取得相同 BOOLEAN 和行值。

代码位置：[sqlglot/generator.py:4281](../../../../../../../sqlglot/sqlglot/generator.py)（行 4281）；[sqlglot/generators/doris.py:57](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 57）。

第一次候选：


~~~sql
SELECT CAST(CASE WHEN LOWER(TRIM('y')) IN ('true', 't', 'tr', 'tru', 'yes', 'y', 'ye', 'on', '1') THEN 'true' WHEN LOWER(TRIM('y')) IN ('false', 'f', 'fa', 'fal', 'fals', 'no', 'n', 'off', 'of', '0') THEN 'false' ELSE 'y' END AS BOOLEAN) AS `true`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-boolean-0010-222849e6/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-boolean-0010-222849e6/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| boolean-case-space | [源 SQL](../evidence/boundaries/boolean-case-space/source.sql) / [候选](../evidence/boundaries/boolean-case-space/candidate.sql) | [probe](../evidence/boundaries/boolean-case-space/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| boolean-sql-null | [源 SQL](../evidence/boundaries/boolean-sql-null/source.sql) / [候选](../evidence/boundaries/boolean-sql-null/candidate.sql) | [probe](../evidence/boundaries/boolean-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

对明确文本→BOOLEAN 转换进行规范化，支持合法前缀、大小写和空白；不从返回值拼常量，不默认承担非法输入错误复刻。 限制：不能把接受前缀的规则应用到所有类型或把含糊的 o 当成合法值。

修复任务：[PG-DORIS-008](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-boolean-0013-41441aee

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 13，源行 37–37，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bool 'n' AS false;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('n' AS BOOLEAN) AS `false`
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['f']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-008 保留合法 PostgreSQL 布尔文本前缀：PG 的 y/n/of 是合法输入；当前 Doris CAST 返回 NULL。基于 LOWER/TRIM 的合法前缀规范化候选取得相同 BOOLEAN 和行值。

代码位置：[sqlglot/generator.py:4281](../../../../../../../sqlglot/sqlglot/generator.py)（行 4281）；[sqlglot/generators/doris.py:57](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 57）。

第一次候选：


~~~sql
SELECT CAST(CASE WHEN LOWER(TRIM('n')) IN ('true', 't', 'tr', 'tru', 'yes', 'y', 'ye', 'on', '1') THEN 'true' WHEN LOWER(TRIM('n')) IN ('false', 'f', 'fa', 'fal', 'fals', 'no', 'n', 'off', 'of', '0') THEN 'false' ELSE 'n' END AS BOOLEAN) AS `false`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-boolean-0013-41441aee/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-boolean-0013-41441aee/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| boolean-case-space | [源 SQL](../evidence/boundaries/boolean-case-space/source.sql) / [候选](../evidence/boundaries/boolean-case-space/candidate.sql) | [probe](../evidence/boundaries/boolean-case-space/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| boolean-sql-null | [源 SQL](../evidence/boundaries/boolean-sql-null/source.sql) / [候选](../evidence/boundaries/boolean-sql-null/candidate.sql) | [probe](../evidence/boundaries/boolean-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

对明确文本→BOOLEAN 转换进行规范化，支持合法前缀、大小写和空白；不从返回值拼常量，不默认承担非法输入错误复刻。 限制：不能把接受前缀的规则应用到所有类型或把含糊的 o 当成合法值。

修复任务：[PG-DORIS-008](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-boolean-0018-0e6e96f9

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 18，源行 47–47，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bool 'of' AS false;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('of' AS BOOLEAN) AS `false`
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['f']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-008 保留合法 PostgreSQL 布尔文本前缀：PG 的 y/n/of 是合法输入；当前 Doris CAST 返回 NULL。基于 LOWER/TRIM 的合法前缀规范化候选取得相同 BOOLEAN 和行值。

代码位置：[sqlglot/generator.py:4281](../../../../../../../sqlglot/sqlglot/generator.py)（行 4281）；[sqlglot/generators/doris.py:57](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 57）。

第一次候选：


~~~sql
SELECT CAST(CASE WHEN LOWER(TRIM('of')) IN ('true', 't', 'tr', 'tru', 'yes', 'y', 'ye', 'on', '1') THEN 'true' WHEN LOWER(TRIM('of')) IN ('false', 'f', 'fa', 'fal', 'fals', 'no', 'n', 'off', 'of', '0') THEN 'false' ELSE 'of' END AS BOOLEAN) AS `false`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-boolean-0018-0e6e96f9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-boolean-0018-0e6e96f9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| boolean-case-space | [源 SQL](../evidence/boundaries/boolean-case-space/source.sql) / [候选](../evidence/boundaries/boolean-case-space/candidate.sql) | [probe](../evidence/boundaries/boolean-case-space/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| boolean-sql-null | [源 SQL](../evidence/boundaries/boolean-sql-null/source.sql) / [候选](../evidence/boundaries/boolean-sql-null/candidate.sql) | [probe](../evidence/boundaries/boolean-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

对明确文本→BOOLEAN 转换进行规范化，支持合法前缀、大小写和空白；不从返回值拼常量，不默认承担非法输入错误复刻。 限制：不能把接受前缀的规则应用到所有类型或把含糊的 o 当成合法值。

修复任务：[PG-DORIS-008](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-boolean-0027-1e7243be

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 27，源行 65–66，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('true', 'bool');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('true', 'bool')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=FUNCTION_NOT_FOUND",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT PG_INPUT_IS_VALID('true', 'bool');
~~~

实际证据：[probe-01 JSON](../evidence/pg-boolean-0027-1e7243be/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-boolean-0027-1e7243be/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-boolean-0028-50f4807b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 28，源行 67–67，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('asdf', 'bool');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('asdf', 'bool')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=FUNCTION_NOT_FOUND",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT PG_INPUT_IS_VALID('asdf', 'bool');
~~~

实际证据：[probe-01 JSON](../evidence/pg-boolean-0028-50f4807b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-boolean-0028-50f4807b/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 不同 |
| 字段数量 | 未执行 | 未执行 |
| 显式别名 | 未执行 | 未执行 |
| 记录行数 | 未执行 | 未执行 |
| 记录值及重复次数 | 未执行 | 未执行 |
| 最终行顺序 | 未执行 | 未执行 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 未取得可用类型 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-boolean-0041-8fceef7a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)；原语句 41，源行 94–94，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT true::boolean::text AS true, false::boolean::text AS false;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST(TRUE AS BOOLEAN) AS STRING) AS `true`, CAST(CAST(FALSE AS BOOLEAN) AS STRING) AS `false`
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e26a2d12e831af8fea74c1032574d5cc1eac371e75a7e693c6b67d3f3dbf1c99",
    "doris_digest=0c201122eb164bc60949d10732db6e1e6bd44fe00942ba58683e8687ddbbbd72",
    "source_sample=[['true', 'false']]",
    "doris_sample=[['1', '0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-boolean-0007-e1b1ef89 / SELECT bool 'test' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 7 | invalid input syntax for type boolean: "test" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0009-38386ada / SELECT bool 'foo' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 9 | invalid input syntax for type boolean: "foo" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0012-81dee7f4 / SELECT bool 'yeah' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 12 | invalid input syntax for type boolean: "yeah" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0015-9a4316f3 / SELECT bool 'nay' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 15 | invalid input syntax for type boolean: "nay" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0019-75c89fd3 / SELECT bool 'o' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 19 | invalid input syntax for type boolean: "o" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0020-c50756c3 / SELECT bool 'on_' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 20 | invalid input syntax for type boolean: "on_" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0021-7dfc6ac1 / SELECT bool 'off_' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 21 | invalid input syntax for type boolean: "off_" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0023-f8e04b2d / SELECT bool '11' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 23 | invalid input syntax for type boolean: "11" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0025-2c6fc490 / SELECT bool '000' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 25 | invalid input syntax for type boolean: "000" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0026-2c8a99f3 / SELECT bool '' AS error; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 26 | invalid input syntax for type boolean: "" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0042-5862abf0 / SELECT '  tru e '::text::boolean AS invalid; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 42 | invalid input syntax for type boolean: "  tru e " | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-boolean-0043-f35e4f2d / SELECT ''::text::boolean AS invalid; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 43 | invalid input syntax for type boolean: "" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-boolean-0001-70d501bd | SELECT 1 AS one; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 1 |
| pg-boolean-0002-cd7e4191 | SELECT true AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 2 |
| pg-boolean-0003-c5856e9a | SELECT false AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 3 |
| pg-boolean-0004-3bf7e474 | SELECT bool 't' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 4 |
| pg-boolean-0005-97c5885a | SELECT bool '   f           ' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 5 |
| pg-boolean-0006-2b4f6271 | SELECT bool 'true' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 6 |
| pg-boolean-0008-7393cacc | SELECT bool 'false' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 8 |
| pg-boolean-0011-8724fe67 | SELECT bool 'yes' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 11 |
| pg-boolean-0014-820ec7d1 | SELECT bool 'no' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 14 |
| pg-boolean-0016-a26417ca | SELECT bool 'on' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 16 |
| pg-boolean-0017-bb8e4812 | SELECT bool 'off' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 17 |
| pg-boolean-0022-e5ab58c0 | SELECT bool '1' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 22 |
| pg-boolean-0024-107f4ce0 | SELECT bool '0' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 24 |
| pg-boolean-0030-926c4ad4 | SELECT bool 't' or bool 'f' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 30 |
| pg-boolean-0031-8355bac8 | SELECT bool 't' and bool 'f' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 31 |
| pg-boolean-0032-9502db2a | SELECT not bool 'f' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 32 |
| pg-boolean-0033-f3dc7c01 | SELECT bool 't' = bool 'f' AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 33 |
| pg-boolean-0034-beb69ffd | SELECT bool 't' <> bool 'f' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 34 |
| pg-boolean-0035-88080971 | SELECT bool 't' > bool 'f' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 35 |
| pg-boolean-0036-126950bd | SELECT bool 't' >= bool 'f' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 36 |
| pg-boolean-0037-1424908a | SELECT bool 'f' < bool 't' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 37 |
| pg-boolean-0038-de0b0e95 | SELECT bool 'f' <= bool 't' AS true; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 38 |
| pg-boolean-0039-06126331 | SELECT 'TrUe'::text::boolean AS true, 'fAlse'::text::boolean AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 39 |
| pg-boolean-0040-5c5709be | SELECT '    true   '::text::boolean AS true,<br>       '     FALSE'::text::boolean AS false; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 40 |
| pg-boolean-0092-bf6ced1a | SELECT 0::boolean; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 92 |
| pg-boolean-0093-b8e9145c | SELECT 1::boolean; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 93 |
| pg-boolean-0094-35e4dc2f | SELECT 2::boolean; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/boolean.out)，语句 94 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

