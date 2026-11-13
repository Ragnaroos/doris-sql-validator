# numerology：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 54 | 33 | 21 | 0 | 33 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/numerology.yaml)；[首轮 Markdown](../../../validation/numerology/validation.md) / [首轮 JSON](../../../validation/numerology/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-numerology-0001-bf1fea25

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 1，源行 1–11，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b100101;
~~~

社区生成 SQL：


~~~sql
SELECT b'100101'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(37 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0001-bf1fea25/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0001-bf1fea25/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0002-4393fd29

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 2，源行 12–12，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o273;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o273
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o273'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(187 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0002-4393fd29/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0002-4393fd29/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0003-bc278c1f

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 3，源行 13–13，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x42F;
~~~

社区生成 SQL：


~~~sql
SELECT x'42F'
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=4504d311cdf1ca90657c87995ff07ff7b97eb13af9b48f445f4239a4cfc7a8d9",
    "doris_digest=1fe3148e85ab94169115ffb4b91cdb059724100a55ae13f6c0e1a4e8c27bac84",
    "source_sample=[['1071']]",
    "doris_sample=[['\\\\x042f']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(1071 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0003-bc278c1f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0003-bc278c1f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → varbinary(2147483647)，逻辑=信息不足，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0004-5b3e7f7e

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 4，源行 15–16，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b1111111111111111111111111111111;
~~~

社区生成 SQL：


~~~sql
SELECT b'1111111111111111111111111111111'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483647 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0004-5b3e7f7e/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0004-5b3e7f7e/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0005-68d49865

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 5，源行 17–17，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b10000000000000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT b'10000000000000000000000000000000'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483648 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0005-68d49865/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0005-68d49865/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0006-2c1a7e8b

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 6，源行 18–18，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o17777777777;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o17777777777
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o17777777777'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483647 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0006-2c1a7e8b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0006-2c1a7e8b/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0007-113b58a4

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 7，源行 19–19，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o20000000000;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o20000000000
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o20000000000'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483648 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0007-113b58a4/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0007-113b58a4/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int8 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0008-e7bc3623

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 8，源行 20–20，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x7FFFFFFF;
~~~

社区生成 SQL：


~~~sql
SELECT x'7FFFFFFF'
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=55378dc37bd2695071aacf2b0512290c5303c1bcacd66d4b3976e7b875cd8ce2",
    "doris_digest=a1416606ba03ca3e3837d5b9b3e681b57506d4c54b62a0c76fa66d86a5c4fb30",
    "source_sample=[['2147483647']]",
    "doris_sample=[['\\\\x7fffffff']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483647 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0008-e7bc3623/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0008-e7bc3623/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → varbinary(2147483647)，逻辑=信息不足，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0009-69ae7cae

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 9，源行 21–21，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x80000000;
~~~

社区生成 SQL：


~~~sql
SELECT x'80000000'
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e9f0e5096a6ce796c6ca24722d24adc9f7ec0ffeff65774fb884bb2cb9492d87",
    "doris_digest=74222c0985651bf7cc093496b726955104697bfe9dbdacf8a77ea3b7e75faaac",
    "source_sample=[['2147483648']]",
    "doris_sample=[['\\\\x80000000']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(2147483648 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0009-69ae7cae/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0009-69ae7cae/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int8 → varbinary(2147483647)，逻辑=信息不足，声明=不同，精度/小数位=不适用 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0010-8616092f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 10，源行 23–23，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0b10000000000000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT -b'10000000000000000000000000000000'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0011-d12aadfa

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 11，源行 24–24，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0b10000000000000000000000000000001;
~~~

社区生成 SQL：


~~~sql
SELECT -b'10000000000000000000000000000001'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0012-8e6f36b0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 12，源行 25–25，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0o20000000000;
~~~

社区生成 SQL：


~~~sql
SELECT -0 AS o20000000000
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o20000000000'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0013-749586fe

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 13，源行 26–26，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0o20000000001;
~~~

社区生成 SQL：


~~~sql
SELECT -0 AS o20000000001
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o20000000001'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0014-997ce8ed

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 14，源行 27–27，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0x80000000;
~~~

社区生成 SQL：


~~~sql
SELECT -x'80000000'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=CAST_ERROR",
    "doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0015-19d5c006

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 15，源行 28–28，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0x80000001;
~~~

社区生成 SQL：


~~~sql
SELECT -x'80000001'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=CAST_ERROR",
    "doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0016-554fa98c

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 16，源行 30–31，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b111111111111111111111111111111111111111111111111111111111111111;
~~~

社区生成 SQL：


~~~sql
SELECT b'111111111111111111111111111111111111111111111111111111111111111'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775807 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0016-554fa98c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0016-554fa98c/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0017-73d4763f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 17，源行 32–32，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b1000000000000000000000000000000000000000000000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT b'1000000000000000000000000000000000000000000000000000000000000000'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775808 AS DECIMAL(38,0));
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0017-73d4763f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0017-73d4763f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: numeric → decimalv3(38,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(38,0)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0018-7a05d9a2

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 18，源行 33–33，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o777777777777777777777;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o777777777777777777777
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o777777777777777777777'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775807 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0018-7a05d9a2/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0018-7a05d9a2/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int8 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0019-335c2dae

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 19，源行 34–34，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o1000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o1000000000000000000000
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o1000000000000000000000'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775808 AS DECIMAL(38,0));
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0019-335c2dae/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0019-335c2dae/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: numeric → tinyint，逻辑=不同，声明=不同，精度/小数位=信息不足 | 1: numeric → decimalv3(38,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(38,0)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0020-885d9173

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 20，源行 35–35，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x7FFFFFFFFFFFFFFF;
~~~

社区生成 SQL：


~~~sql
SELECT x'7FFFFFFFFFFFFFFF'
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=bc8eb95e1e9db726225627c9c80b2cc5b4d2b7e9ac6b081a65633b073eab2136",
    "doris_digest=751d50a58f06a28db34150714b7e73e8a80dee6f9d7b054da14ea1a6b2782adb",
    "source_sample=[['9223372036854775807']]",
    "doris_sample=[['\\\\x7fffffffffffffff']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775807 AS BIGINT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0020-885d9173/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0020-885d9173/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int8 → varbinary(2147483647)，逻辑=信息不足，声明=不同，精度/小数位=不适用 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0021-65b661c9

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 21，源行 36–36，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x8000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT x'8000000000000000'
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=25607a9238080532e0e894cb82e0076a5217149224b6c25eca03371cb75c841f",
    "doris_digest=5438c33713b57cd34f791e35991d9405709cf1ce73b72d5b622288342e2115f7",
    "source_sample=[['9223372036854775808']]",
    "doris_sample=[['\\\\x8000000000000000']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(9223372036854775808 AS DECIMAL(38,0));
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0021-65b661c9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0021-65b661c9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: numeric → varbinary(2147483647)，逻辑=信息不足，声明=不同，精度/小数位=信息不足 | 1: numeric → decimalv3(38,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(38,0)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0022-72c6b526

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 22，源行 38–38，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0b1000000000000000000000000000000000000000000000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT -b'1000000000000000000000000000000000000000000000000000000000000000'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0023-529faf1e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 23，源行 39–39，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0b1000000000000000000000000000000000000000000000000000000000000001;
~~~

社区生成 SQL：


~~~sql
SELECT -b'1000000000000000000000000000000000000000000000000000000000000001'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0024-6a9c516b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 24，源行 40–40，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0o1000000000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT -0 AS o1000000000000000000000
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o1000000000000000000000'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0025-f8ec6ef6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 25，源行 41–41，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0o1000000000000000000001;
~~~

社区生成 SQL：


~~~sql
SELECT -0 AS o1000000000000000000001
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o1000000000000000000001'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0026-ffe92375

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 26，源行 42–42，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0x8000000000000000;
~~~

社区生成 SQL：


~~~sql
SELECT -x'8000000000000000'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=CAST_ERROR",
    "doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0027-c26c0457

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 27，源行 43–43，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -0x8000000000000001;
~~~

社区生成 SQL：


~~~sql
SELECT -x'8000000000000001'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=CAST_ERROR",
    "doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0047-b021aae2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 47，源行 69–70，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1_000_000;
~~~

社区生成 SQL：


~~~sql
SELECT 1 AS _000_000
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='_000_000'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0048-28a108ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 48，源行 71–71，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 1_2_3;
~~~

社区生成 SQL：


~~~sql
SELECT 1 AS _2_3
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='_2_3'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numerology-0049-9b45177b

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 49，源行 72–72，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0x1EEE_FFFF;
~~~

社区生成 SQL：


~~~sql
SELECT x'1EEE_FFFF'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(518979583 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0049-9b45177b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0049-9b45177b/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0050-0c169c9a

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 50，源行 73–73，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0o2_73;
~~~

社区生成 SQL：


~~~sql
SELECT 0 AS o2_73
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='o2_73'"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(187 AS INT);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numerology-0050-0c169c9a/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numerology-0050-0c169c9a/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 不同 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "不同",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0051-33408a72

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 51，源行 74–74，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0b_10_0101;
~~~

社区生成 SQL：


~~~sql
SELECT b'_10_0101'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=EXECUTION_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-007 正确区分 PG 非十进制整数与位串/字节串：0o273 被解析为数值 0 加别名，0x/0b 被当成十六进制/二进制串；18 条候选按进制转换并保留 int4/int8/numeric 范围。

代码位置：[sqlglot/tokenizer_core.py:1041](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1041）；[sqlglot/tokenizer_core.py:1051](../../../../../../../sqlglot/sqlglot/tokenizer_core.py)（行 1051）；[sqlglot/parser.py:5877](../../../../../../../sqlglot/sqlglot/parser.py)（行 5877）。

第一次候选：


~~~sql
SELECT CAST(37 AS INT);
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
TokenError: Error tokenizing 'SELECT b'_10_0101'
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| numeric-octal-zero | [源 SQL](../evidence/boundaries/numeric-octal-zero/source.sql) / [候选](../evidence/boundaries/numeric-octal-zero/candidate.sql) | 工具 Parser 拒绝，未取得完整双端证据，不算通过 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在 PG 方言保留数值字面量的来源和类型，识别 octal 与下划线；不能改坏 B'...'、X'...' 等真正的位串。 限制：超过 BIGINT 的 PG NUMERIC 与固定 DECIMAL(38,0) 只在明确范围内可比。pg-numerology-0051 还被诊断工具对旧生成 SQL 的 Tokenizer 检查阻断。

修复任务：[PG-DORIS-007](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-numerology-0054-8a209ea6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)；原语句 54，源行 78–78，同文回显第 1 次；历史成功 1 行。

- 首轮：字段数量/名称/已知类型不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT .000_005;
~~~

社区生成 SQL：


~~~sql
SELECT 0.000 AS _005
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "RESULT_SCHEMA_MISMATCH",
  "summary": "Canonical result schemas differ",
  "details": [
    "column[0] name: source='?column?', doris='_005'"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-numerology-0028-4f02026b / SELECT 123abc; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 28 | trailing junk after numeric literal at or near "123abc" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0029-c7e45ec9 / SELECT 0x0o; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 29 | trailing junk after numeric literal at or near "0x0o" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '0x0o' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0030-c1db4386 / SELECT 0.a; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 30 | trailing junk after numeric literal at or near "0.a" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0031-71d2199a / SELECT 0.0a; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 31 | trailing junk after numeric literal at or near "0.0a" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0032-71d2199a / SELECT .0a; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 32 | trailing junk after numeric literal at or near ".0a" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0033-33a201b2 / SELECT 0.0e1a; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 33 | trailing junk after numeric literal at or near "0.0e1a" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0034-0597a37e / SELECT 0.0e; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 34 | trailing junk after numeric literal at or near "0.0e" | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = Can not dereference field: 0e') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0035-97a6754a / SELECT 0.0e+a; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 35 | trailing junk after numeric literal at or near "0.0e+" | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = Can not dereference field: 0e') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0038-40292161 / SELECT 0b; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 38 | invalid binary integer at or near "0b" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '0b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0039-2cf24225 / SELECT 1b; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 39 | trailing junk after numeric literal at or near "1b" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0040-33157fdf / SELECT 0b0x; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 40 | trailing junk after numeric literal at or near "0b0x" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '0b0x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0041-4efe6eaa / SELECT 0o; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 41 | invalid octal integer at or near "0o" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0042-077be3a9 / SELECT 1o; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 42 | trailing junk after numeric literal at or near "1o" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0043-c31d8dd1 / SELECT 0o0x; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 43 | trailing junk after numeric literal at or near "0o0x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0044-a9ff2e9b / SELECT 0x; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 44 | invalid hexadecimal integer at or near "0x" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '0x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0045-c3b9b519 / SELECT 1x; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 45 | trailing junk after numeric literal at or near "1x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0046-cf0a0c41 / SELECT 0x0y; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 46 | trailing junk after numeric literal at or near "0x0y" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '0x0y' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0057-f1dc0d67 / SELECT _100; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 57 | column "_100" does not exist | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column '_100' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0058-3d65d0e3 / SELECT 100_; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 58 | trailing junk after numeric literal at or near "100_" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0059-d73d9e0e / SELECT 100__000; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 59 | trailing junk after numeric literal at or near "100__000" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numerology-0060-be24813a / SELECT _1_000.5; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/numerology.out)，语句 60 | syntax error at or near ".5" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input '.5' expecting {<EOF>, ';'}(line 1, pos 13)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 11 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 36 | 54–54 | error | Expected one read-only Query, got Command |
| 37 | 55–55 | error | Expected one read-only Query, got Command |
| 52 | 76–76 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m000_005; |
| 53 | 77–77 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m; |
| 55 | 79–79 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m5e0_1; |
| 56 | 81–88 | error | Expected one read-only Query, got Command |
| 61 | 96–96 | error | Invalid expression / Unexpected token. Line 1, Col: 14.<br>  SELECT 1_000_[4m.[0m5; |
| 62 | 97–97 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m_5; |
| 63 | 98–98 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m5_; |
| 64 | 99–99 | error | Invalid expression / Unexpected token. Line 1, Col: 13.<br>  SELECT 1_000[4m.[0m5e_1; |
| 65 | 101–101 | error | Expected one read-only Query, got Command |


