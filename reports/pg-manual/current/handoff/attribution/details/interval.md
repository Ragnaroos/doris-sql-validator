# interval：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 20 | 11 | 9 | 0 | 11 |


[YAML](../../../../../../cases/postgres/manual/current/interval.yaml)；[首轮 Markdown](../../../validation/interval/validation.md) / [首轮 JSON](../../../validation/interval/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-interval-0003-8fdfc48d

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 3，源行 8–9，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '01:00' AS "One hour";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '01:00' AS `One hour`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 24)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 24)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT INTERVAL '01:00' AS `One hour`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-interval-0003-8fdfc48d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-interval-0003-8fdfc48d/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "interval",<br>      "Doris原生类型": "interval",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 24)\\n\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 24)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-interval-0004-c90dd650

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 4，源行 10–10，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '+02:00' AS "Two hours";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '+02:00' AS `Two hours`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 25)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0005-52af31c8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 5，源行 11–11，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '-08:00' AS "Eight hours";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '-08:00' AS `Eight hours`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 25)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0006-8bbc181a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 6，源行 12–12，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '-1 +02:03' AS "22 hours ago...";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '-1 +02:03' AS `22 hours ago...`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 28)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 28)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0007-f1af5ce0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 7，源行 13–13，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '-1 days +02:03' AS "22 hours ago...";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '-1' DAY AS `22 hours ago...`
~~~

Doris 原错误：


~~~text
(1105, 'NullPointerException, msg: Cannot invoke "org.apache.doris.analysis.Expr.treeToThrift()" because "expr" is null')
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
    "doris_error_message=(1105, 'NullPointerException, msg: Cannot invoke \"org.apache.doris.analysis.Expr.treeToThrift()\" because \"expr\" is null')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0008-a5e251de

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 8，源行 14–14，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '1.5 weeks' AS "Ten days twelve hours";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '1.5' WEEK AS `Ten days twelve hours`
~~~

Doris 原错误：


~~~text
(1105, 'NullPointerException, msg: Cannot invoke "org.apache.doris.analysis.Expr.treeToThrift()" because "expr" is null')
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
    "doris_error_message=(1105, 'NullPointerException, msg: Cannot invoke \"org.apache.doris.analysis.Expr.treeToThrift()\" because \"expr\" is null')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0009-3add4f85

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 9，源行 15–15，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '1.5 months' AS "One month 15 days";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '1.5' MONTH AS `One month 15 days`
~~~

Doris 原错误：


~~~text
(1105, 'NullPointerException, msg: Cannot invoke "org.apache.doris.analysis.Expr.treeToThrift()" because "expr" is null')
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
    "doris_error_message=(1105, 'NullPointerException, msg: Cannot invoke \"org.apache.doris.analysis.Expr.treeToThrift()\" because \"expr\" is null')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0010-1d0b98d6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 10，源行 16–16，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '10 years -11 month -12 days +13:14' AS "9 years...";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '10 years -11 month -12 days +13:14' AS `9 years...`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 53)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 53)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0011-c3689488

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 11，源行 17–17，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL 'infinity' AS "eternity";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL 'infinity' AS `eternity`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 27)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 27)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0012-5f6e40d5

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 12，源行 18–18，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT INTERVAL '-infinity' AS "beginning of time";
~~~

社区生成 SQL：


~~~sql
SELECT INTERVAL '-infinity' AS `beginning of time`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 28)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at 'AS'(line 1, pos 28)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-interval-0043-c75b564b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/interval.out)；原语句 43，源行 76–77，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT -('-2147483647 months'::interval);
~~~

社区生成 SQL：


~~~sql
SELECT -(CAST('-2147483647 months' AS INTERVAL))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 38)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 38)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-interval-0042-9b4eb8dd / SELECT -('-2147483648 months'::interval); / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 42 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 38)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0044-52cb668e / SELECT -('-2147483648 days'::interval); / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 44 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 36)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0046-b7094563 / SELECT -('-9223372036854775808 us'::interval); / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 46 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0055-ea0dbdc1 / select extract(epoch from '256 microseconds'::interval * (2^55)::float8); / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 55 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 49)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0074-9e931758 / SELECT '3000000 months'::interval * 1000; / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 74 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0075-5310bd27 / SELECT '3000000 months'::interval / 0.001; / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 75 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0076-42ea5d08 / SELECT '3000000 days'::interval * 1000; / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 76 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0077-02688b9c / SELECT '3000000 days'::interval / 0.001; / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 77 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-interval-0078-a0dd407c / SELECT '1 month 2146410 days'::interval * 1000.5002; / [.out](../../../../../../cases/postgres/manual/current/assets/interval.out)，语句 78 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 38)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

