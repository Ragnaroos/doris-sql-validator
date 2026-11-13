# date：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 64 | 47 | 17 | 11 | 36 |


[YAML](../../../../../../cases/postgres/manual/current/date.yaml)；[首轮 Markdown](../../../validation/date/validation.md) / [首轮 JSON](../../../validation/date/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-date-0024-afe42f36

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 24，源行 39–39，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT date 'January 8, 1999';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('January 8, 1999' AS DATE)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=dbaccd18db6b22c277be2d0b68b8455d0d7cb5e65db345f4bc3db65d05b46f0b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['1999-01-08']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-014 保留合法 PostgreSQL 日期字面量格式：January 8, 1999 在 PG 为成功 DATE，普通 Doris CAST 返回 NULL；指定格式 STR_TO_DATE 的候选和闰年正常变体成功。

代码位置：[sqlglot/generator.py:4281](../../../../../../../sqlglot/sqlglot/generator.py)（行 4281）；[sqlglot/generators/doris.py:57](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 57）。

第一次候选：


~~~sql
SELECT CAST(STR_TO_DATE('January 8, 1999','%M %e, %Y') AS DATE);
~~~

实际证据：[probe-01 JSON](../evidence/pg-date-0024-afe42f36/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-date-0024-afe42f36/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 | 1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "date",<br>      "Doris原生类型": "date",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "date",<br>      "Doris原生类型": "datev2",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| date-month-name-leap | [源 SQL](../evidence/boundaries/date-month-name-leap/source.sql) / [候选](../evidence/boundaries/date-month-name-leap/candidate.sql) | [probe](../evidence/boundaries/date-month-name-leap/probe/probe-evidence.json)：值与重复次数=一致；1: date → datev2，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

对可无歧义识别的字面量格式转换，或显式保留支持限制；不能硬编码当前日期答案。 限制：只验证了列明格式；不宣称任意 PG 日期字符串、BC/Infinity 或全域日期可支持。

修复任务：[PG-DORIS-014](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-date-0178-8dc03b96

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 178，源行 248–252，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '0101-12-31 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('0101-12-31 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0179-9c4321eb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 179，源行 252–253，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '0100-12-31 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('0100-12-31 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0180-ef5fd48d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 180，源行 253–254，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '0001-12-31 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('0001-12-31 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0181-9dbfd03a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 181，源行 254–255，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '0001-01-01');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('0001-01-01' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0182-987cf591

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 182，源行 255–256，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '0001-01-01 AD');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('0001-01-01 AD' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0183-5bacb2df

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 183，源行 256–257，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(CENTURY FROM DATE '1900-12-31');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(CENTURY FROM CAST('1900-12-31' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'CENTURY' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0188-3d4e9947

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 188，源行 261–265，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '0001-12-31 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('0001-12-31 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0189-2763751d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 189，源行 265–266，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '0001-01-01 AD');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('0001-01-01 AD' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0190-8f9ed83e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 190，源行 266–267，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '1000-12-31');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('1000-12-31' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0191-2739ae8d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 191，源行 267–268，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '1001-01-01');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('1001-01-01' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0192-238ee4a9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 192，源行 268–269，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '2000-12-31');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('2000-12-31' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0193-b3ea1942

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 193，源行 269–270，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLENNIUM FROM DATE '2001-01-01');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLENNIUM FROM CAST('2001-01-01' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLENNIUM' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0195-4a798da9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 195，源行 272–276，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '1994-12-25');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('1994-12-25' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0196-6b3c74f1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 196，源行 276–277，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '0010-01-01');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('0010-01-01' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0197-a461c8c8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 197，源行 277–278，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '0009-12-31');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('0009-12-31' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0198-95bb9db9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 198，源行 278–279，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '0001-01-01 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('0001-01-01 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0199-f43f8cb8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 199，源行 279–280，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '0002-12-31 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('0002-12-31 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0200-142cae8e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 200，源行 280–281，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DECADE FROM DATE '0011-01-01 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DECADE FROM CAST('0011-01-01 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'DECADE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0210-9da76665

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 210，源行 294–294，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(YEAR          FROM DATE '2020-08-11 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(YEAR FROM CAST('2020-08-11 BC' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=0fc048957c7782f22db3477a4a2d7246b1d26f65745a374fd54c0c019fdf489a",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['-2020']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0214-b53a6379

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 214，源行 298–298，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(ISOYEAR       FROM DATE '2020-08-11');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(ISOYEAR FROM CAST('2020-08-11' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0215-648cd8c2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 215，源行 299–299，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(ISOYEAR       FROM DATE '2020-08-11 BC');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(ISOYEAR FROM CAST('2020-08-11 BC' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0217-85e60c38

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 217，源行 301–301，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(WEEK          FROM DATE '2020-08-11');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(WEEK FROM CAST('2020-08-11' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=cb5afa16ba9f67aaba12e4ca8dcfb4d8e87e9e636fc4e0ba0b7c5316ca157d4c",
    "doris_digest=5eea3a047f78a488dec5773a35fee4238d60c95f88b26db094910c424295b60a",
    "source_sample=[['33']]",
    "doris_sample=[['32']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0218-5c369326

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 218，源行 302–302，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DOW           FROM DATE '2020-08-11');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DOW FROM CAST('2020-08-11' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a0a88ee57364f8f632469bb45e2fd5057419c8c1c1f6d52216176988ab0fbb90",
    "doris_digest=7e5acccc8c8fd7375f8700c06ef68c1dbf50eb98c0bb12527a571aade278a5a7",
    "source_sample=[['2']]",
    "doris_sample=[['3']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0219-e68d10f7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 219，源行 303–303，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(DOW           FROM DATE '2020-08-16');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(DOW FROM CAST('2020-08-16' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "source_sample=[['0']]",
    "doris_sample=[['1']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0220-e3a4d73e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 220，源行 304–304，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(ISODOW        FROM DATE '2020-08-11');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(ISODOW FROM CAST('2020-08-11' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ISODOW' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'ISODOW' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0221-a242da04

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 221，源行 305–305，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(ISODOW        FROM DATE '2020-08-16');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(ISODOW FROM CAST('2020-08-16' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ISODOW' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'ISODOW' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0227-cc63d9cf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 227，源行 311–311，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(JULIAN        FROM DATE '2020-08-11');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(JULIAN FROM CAST('2020-08-11' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'JULIAN' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'JULIAN' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0242-87859433

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 242，源行 332–332，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'infinity'::date = '+infinity'::date as t;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('infinity' AS DATE) = CAST('+infinity' AS DATE) AS t
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0252-62c6927e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 252，源行 346–350，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(EPOCH FROM DATE 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=ead584c5e0013c95b9b50108ed341725c4182d31f3c06b97822307814ecc755d",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['Infinity']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0253-05b6a631

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 253，源行 350–351，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(EPOCH FROM DATE '-infinity');
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('-infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=3cf63f9d0a88280835de6dbef8a5c7773c491c05c21e78e783187a703665e627",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['-Infinity']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0254-ea07e92b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 254，源行 351–353，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(YEAR       FROM DATE 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(YEAR FROM CAST('infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=ead584c5e0013c95b9b50108ed341725c4182d31f3c06b97822307814ecc755d",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['Infinity']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0258-446bd4d5

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 258，源行 356–357，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(JULIAN     FROM DATE 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(JULIAN FROM CAST('infinity' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'JULIAN' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'JULIAN' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0259-9eeb088a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 259，源行 357–358，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(ISOYEAR    FROM DATE 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(ISOYEAR FROM CAST('infinity' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'ISOYEAR' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0260-62c6927e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 260，源行 358–359，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(EPOCH      FROM DATE 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=ead584c5e0013c95b9b50108ed341725c4182d31f3c06b97822307814ecc755d",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['Infinity']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-date-0264-d086f520

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/date.out)；原语句 264，源行 368–368，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select make_time(8, 20, 0.0);
~~~

社区生成 SQL：


~~~sql
SELECT MAKETIME(8, 20, 0.0)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=fe3525e0046e6912219e4d03550030eff7980d6d8a8d186d7c6e933d68892814",
    "doris_digest=cc57fcfe68275d2b36d05c7f4893d91d03a433da26bdf151f58e21b4d6f4c413",
    "source_sample=[['08:20:00']]",
    "doris_sample=[['8:20:00']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-date-0029-de69b5bd / SELECT date '18/1/1999'; / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 29 | date/time field value out of range: "18/1/1999" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0202-210faa28 / SELECT EXTRACT(MICROSECONDS  FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 202 | unit "microseconds" not supported for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'MICROSECONDS' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0203-571dfa63 / SELECT EXTRACT(MILLISECONDS  FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 203 | unit "milliseconds" not supported for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLISECONDS' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0204-bfb90ebf / SELECT EXTRACT(SECOND        FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 204 | unit "second" not supported for type date | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0205-5cd1b273 / SELECT EXTRACT(MINUTE        FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 205 | unit "minute" not supported for type date | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0206-38fe6873 / SELECT EXTRACT(HOUR          FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 206 | unit "hour" not supported for type date | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0223-631f0364 / SELECT EXTRACT(TIMEZONE      FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 223 | unit "timezone" not supported for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'TIMEZONE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0224-b6de1465 / SELECT EXTRACT(TIMEZONE_M    FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 224 | unit "timezone_m" not supported for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'TIMEZONE_M' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0225-25f0d41a / SELECT EXTRACT(TIMEZONE_H    FROM DATE '2020-08-11'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 225 | unit "timezone_h" not supported for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'TIMEZONE_H' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0261-d0afe236 / SELECT EXTRACT(MICROSEC  FROM DATE 'infinity'); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 261 | unit "microsec" not recognized for type date | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'MICROSEC' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0265-583926f3 / select make_date(0, 7, 15); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 265 | date field value out of range: 0-07-15 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'MAKE_DATE'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0266-add0cea0 / select make_date(2013, 2, 30); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 266 | date field value out of range: 2013-02-30 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'MAKE_DATE'") | 默认不纳入主修复范围，未安排独立改写 | MAKE_DATE 已另建正常输入变体并实测 PG，不借用本条负向答案 |
| pg-date-0267-76b09c1a / select make_date(2013, 13, 1); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 267 | date field value out of range: 2013-13-01 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'MAKE_DATE'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0268-9b35cd38 / select make_date(2013, 11, -1); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 268 | date field value out of range: 2013-11--1 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'MAKE_DATE'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0269-cc3d9623 / SELECT make_date(-2147483648, 1, 1); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 269 | date field value out of range: -2147483648-01-01 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'MAKE_DATE'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0270-a3077f5e / select make_time(10, 55, 100.1); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 270 | time field value out of range: 10:55:100.1 | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-date-0271-572e5fea / select make_time(24, 0, 2.1); / [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 271 | time field value out of range: 24:00:2.1 | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-date-0025-04632bf5 | SELECT date '1999-01-08'; | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 25 |
| pg-date-0026-2243e99c | SELECT date '1999-01-18'; | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 26 |
| pg-date-0031-8961f61b | SELECT date '19990108'; | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 31 |
| pg-date-0032-27b150a2 | SELECT date '990108'; | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 32 |
| pg-date-0177-7a208832 | SELECT EXTRACT(EPOCH FROM DATE        '1970-01-01'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 177 |
| pg-date-0207-6c53bfb0 | SELECT EXTRACT(DAY           FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 207 |
| pg-date-0208-6b0c7844 | SELECT EXTRACT(MONTH         FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 208 |
| pg-date-0209-e953d696 | SELECT EXTRACT(YEAR          FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 209 |
| pg-date-0216-372a952d | SELECT EXTRACT(QUARTER       FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 216 |
| pg-date-0222-0da07efd | SELECT EXTRACT(DOY           FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 222 |
| pg-date-0226-1b61b66e | SELECT EXTRACT(EPOCH         FROM DATE '2020-08-11'); | [.out](../../../../../../cases/postgres/manual/current/assets/date.out)，语句 226 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

