# sqljson_queryfuncs：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 74 | 55 | 19 | 0 | 55 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/sqljson_queryfuncs.yaml)；[首轮 Markdown](../../../validation/sqljson_queryfuncs/validation.md) / [首轮 JSON](../../../validation/sqljson_queryfuncs/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-sqljson-queryfuncs-0025-2e24b896

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 25，源行 33–34，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(NULL::jsonb, '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST(NULL AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT JSON_VALUE(CAST(NULL AS JSONB), '$');
~~~

实际证据：[probe-01 JSON](../evidence/pg-sqljson-queryfuncs-0025-2e24b896/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-sqljson-queryfuncs-0025-2e24b896/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-sqljson-queryfuncs-0026-38745d07

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 26，源行 36–36，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb 'null', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('null' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0027-d66894eb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 27，源行 37–37，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb 'null', '$' RETURNING int);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('null' AS JSONB), '$' RETURNING INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0028-080a25b5

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 28，源行 39–39，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb 'true', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('true' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0029-8138825c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 29，源行 40–40，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb 'true', '$' RETURNING bool);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('true' AS JSONB), '$' RETURNING BOOLEAN)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0030-17c170f7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 30，源行 42–42，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '123', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0031-4f86e17d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 31，源行 43–43，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING int) + 234;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING INT) + 234
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0032-bd95d946

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 32，源行 44–44，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING STRING)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0033-dde545e7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 33，源行 45–46，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING bytea ERROR ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING VARBINARY ERROR ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0034-2188e922

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 34，源行 48–48，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1.23', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1.23' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0035-b84d7e2c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 35，源行 49–49，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1.23', '$' RETURNING int);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1.23' AS JSONB), '$' RETURNING INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0036-2b6a5ea9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 36，源行 50–50，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING numeric);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"1.23"' AS JSONB), '$' RETURNING DECIMAL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0038-d7147527

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 38，源行 53–53，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0039-0cd9e40c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 39，源行 54–54，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING STRING)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0040-7e2f34ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 40，源行 55–55，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(5));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(5))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0042-c2907fe7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 42，源行 57–57，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(2))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0043-6cb858d2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 43，源行 58–58，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(3) ERROR ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(3) ERROR ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0044-2033aaa6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 44，源行 59–59，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0045-90c16c7e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 45，源行 60–60，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0046-2b8a023d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 46，源行 61–61，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json ERROR ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSON ERROR ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0047-f792d638

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 47，源行 62–62，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb ERROR ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSONB ERROR ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0048-b4527b25

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 48，源行 63–63，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING json);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"\\"aaa\\""' AS JSONB), '$' RETURNING JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0049-96898d76

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 49，源行 64–64，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"\\"aaa\\""' AS JSONB), '$' RETURNING JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0050-50c3e3bd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 50，源行 65–65，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0052-f82b9920

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 52，源行 67–67，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int DEFAULT 111 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING INT DEFAULT 111 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0053-ee35c348

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 53，源行 68–68，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"123"', '$' RETURNING int) + 234;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"123"' AS JSONB), '$' RETURNING INT) + 234
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0054-557bf181

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 54，源行 70–70，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"2017-02-20"', '$' RETURNING date) + 9;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"2017-02-20"' AS JSONB), '$' RETURNING DATE) + 9
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 53)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 53)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0066-1f960c70

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 66，源行 87–87，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '[]', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('[]' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0068-b4bc6a7a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 68，源行 89–89，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '{}', '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0070-00d59bcd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 70，源行 92–92，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', '$.a');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), '$.a')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0072-1278b801

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 72，源行 94–94，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'strict $.a' DEFAULT 'error' ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'strict $.a' DEFAULT 'error' ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0073-bb4e0659

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 73，源行 95–95，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' ERROR ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0075-abc0de9c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 75，源行 97–97，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'strict $.*' DEFAULT 2 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'strict $.*' DEFAULT 2 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0076-b6c58a98

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 76，源行 98–98，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT 2 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT 2 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0077-800ba813

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 77，源行 99–99，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT '2' ON EMPTY)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0078-da6f3e1a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 78，源行 100–100，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' NULL ON EMPTY DEFAULT '2' ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' NULL ON EMPTY DEFAULT '2' ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0079-69f4f96a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 79，源行 101–101，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY DEFAULT '3' ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT '2' ON EMPTY DEFAULT '3' ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0082-fb1bee1a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 82，源行 105–105，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' DEFAULT '0' ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('[1,2]' AS JSONB), '$[*]' DEFAULT '0' ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 49)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0084-881a2588

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 84，源行 107–107，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('[" "]' AS JSONB), '$[*]' RETURNING INT DEFAULT 2 + 3 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0085-5ebde80a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 85，源行 108–108，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '["1"]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('["1"]' AS JSONB), '$[*]' RETURNING INT DEFAULT 2 + 3 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0089-29bd6f64

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 89，源行 115–115，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT NULL::numeric ON EMPTY);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING DECIMAL(4, 1) DEFAULT CAST(NULL AS DECIMAL) ON EMPTY)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0091-ada5e2dc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 91，源行 117–117，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT abs(NULL::numeric) ON EMPTY);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING DECIMAL(4, 1) DEFAULT ABS(CAST(NULL AS DECIMAL)) ON EMPTY)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0094-88ebeb21

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 94，源行 134–138，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x IS NULL AS is_null,
       json_value(x, '$.a' RETURNING int DEFAULT 42 ON EMPTY) AS jv
FROM (VALUES ('{}'), (NULL), ('{}')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT x IS NULL AS is_null, JSON_VALUE(x, '$.a' RETURNING INT DEFAULT 42 ON EMPTY) AS jv FROM (SELECT '{}' AS x UNION ALL SELECT NULL UNION ALL SELECT '{}') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0095-3198a481

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 95，源行 140–142，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x IS NULL AS is_null,
       json_value(x, 'strict $.a' RETURNING int DEFAULT 42 ON ERROR) AS jv
FROM (VALUES ('1'), (NULL), ('1')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT x IS NULL AS is_null, JSON_VALUE(x, 'strict $.a' RETURNING INT DEFAULT 42 ON ERROR) AS jv FROM (SELECT '1' AS x UNION ALL SELECT NULL UNION ALL SELECT '1') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 56)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 56)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0114-2e24b896

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 114，源行 181–183，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(NULL::jsonb, '$');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST(NULL AS JSONB), '$')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0293-69cc7045

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 293，源行 495–495，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '{"a": 123}', '$' || '.' || 'a');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('{"a": 123}' AS JSONB), CONCAT('$', '.', 'a'))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_VALUE'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0294-1411b7ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 294，源行 496–496，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '{"a": 123}', '$' || '.' || 'b' DEFAULT 'foo' ON EMPTY);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('{"a": 123}' AS JSONB), CONCAT('$', '.', 'b') DEFAULT 'foo' ON EMPTY)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 69)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0328-38effc65

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 328，源行 554–554，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '"x"', '$' RETURNING int DEFAULT 11 ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('"x"' AS JSONB), '$' RETURNING INT DEFAULT 11 ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0356-3b4096cf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 356，源行 590–590，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1::bit(3) ON ERROR);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(CAST('1234' AS JSONB), '$' RETURNING BIT(3) DEFAULT CAST(1 AS BIT(3)) ON ERROR)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0359-afd861ac

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 359，源行 594–596，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE('null', '$' RETURNING jsonb), JSON_VALUE('123', '$' RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE('null', '$' RETURNING JSONB), JSON_VALUE('123', '$' RETURNING JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0360-bf372197

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 360，源行 597–597，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), ('null'), ('2')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING JSONB) FROM (SELECT CAST('1' AS JSONB) AS x UNION ALL SELECT 'null' UNION ALL SELECT '2') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0361-85025945

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 361，源行 598–598，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING json) FROM (VALUES ('1'::json), ('null'), ('2')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING JSON) FROM (SELECT CAST('1' AS JSON) AS x UNION ALL SELECT 'null' UNION ALL SELECT '2') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0362-e7974a66

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 362，源行 599–600，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(x, '$.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('{}'), ('{"a": 2}')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(x, '$.a' RETURNING JSONB) FROM (SELECT CAST('{"a": 1}' AS JSONB) AS x UNION ALL SELECT '{}' UNION ALL SELECT '{"a": 2}') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 27)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0363-fab5929f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 363，源行 601–601，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(x, 'strict $.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('[]'), ('{"a": 2}')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(x, 'strict $.a' RETURNING JSONB) FROM (SELECT CAST('{"a": 1}' AS JSONB) AS x UNION ALL SELECT '[]' UNION ALL SELECT '{"a": 2}') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 34)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 34)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-queryfuncs-0364-20eac327

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)；原语句 364，源行 602–602，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), (NULL), ('2')) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_VALUE(x, '$' RETURNING JSONB) FROM (SELECT CAST('1' AS JSONB) AS x UNION ALL SELECT NULL UNION ALL SELECT '2') AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\\n\")",
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
| pg-sqljson-queryfuncs-0037-a5f418ce / SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING int ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 37 | invalid input syntax for type integer: "1.23" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0041-05967d19 / SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2) ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 41 | value too long for type character(2) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0051-9a2a57fa / SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 51 | invalid input syntax for type integer: "aaa" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0067-ff8839fa / SELECT JSON_VALUE(jsonb '[]', '$' ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 67 | JSON path expression in JSON_VALUE must return single scalar item | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0069-d1d29700 / SELECT JSON_VALUE(jsonb '{}', '$' ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 69 | JSON path expression in JSON_VALUE must return single scalar item | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0071-0a70fa3f / SELECT JSON_VALUE(jsonb '1', 'strict $.a' ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 71 | jsonpath member accessor can only be applied to an object | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0074-fa9f7b22 / SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 74 | no SQL/JSON item found for specified path | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0080-38413d71 / SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY DEFAULT '3' ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 80 | no SQL/JSON item found for specified path | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0081-d479382c / SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 81 | JSON path expression in JSON_VALUE must return single scalar item | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0083-4f6061d4 / SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 83 | invalid input syntax for type integer: " " | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0087-60a477e6 / SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT 99999.999 ON EMPTY); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 87 | numeric field overflow | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0088-ec1cd510 / SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING varchar(3) DEFAULT 'toolong'::varchar(10) ON EMPTY); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 88 | value too long for type character varying(3) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0090-2055fe2d / SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING bit(3) DEFAULT b'10101' ON EMPTY); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 90 | bit string length 5 does not match type bit(3) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0112-c017eeab / select json_value('{"a": 1.234}', '$.a' returning int error on error); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 112 | invalid input syntax for type integer: "1.234" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 40)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0113-71c80245 / select json_value('{"a": "1.234"}', '$.a' returning int error on error); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 113 | invalid input syntax for type integer: "1.234" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0319-10a7c60f / SELECT JSON_VALUE(jsonb '1', '$' EMPTY ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 319 | invalid ON ERROR behavior | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'EMPTY' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0354-e456510b / SELECT JSON_VALUE(jsonb '"111"', '$'  RETURNING bit(2) ERROR ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 354 | bit string length 3 does not match type bit(2) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0355-9a967b5b / SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1 ON ERROR); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 355 | cannot cast behavior expression of type integer to bit | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-queryfuncs-0357-fb7679a6 / SELECT JSON_VALUE(jsonb '"111"', '$.a'  RETURNING bit(3) DEFAULT '1111' ON EMPTY); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson_queryfuncs.out)，语句 357 | bit string length 4 does not match type bit(3) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 145 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 9 | 11–12 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_EXISTS(jsonb '1', 'strict $.a' [4mERROR[0m ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_EXISTS(jsonb '1', 'strict $.a' ERROR [4mON[0m ERROR); |
| 19 | 24–24 | error | Expecting ). Line 1, Col: 69.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' [4mPASSING[0m 1 AS x);<br><br>Invalid expression / Unexpected token. Line 1, Col: 71.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' PASSING [4m1[0m AS x); |
| 20 | 25–25 | error | Expecting ). Line 1, Col: 69.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' [4mPASSING[0m '1' AS x);<br><br>Invalid expression / Unexpected token. Line 1, Col: 73.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' PASSING [4m'1'[0m AS x); |
| 21 | 26–26 | error | Expecting ). Line 1, Col: 79.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' [4mPASSING[0m 0 AS x, 2 AS y);<br><br>Invalid expression / Unexpected token. Line 1, Col: 81.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' PASSING [4m0[0m AS x, 2 AS y); |
| 22 | 27–27 | error | Expecting ). Line 1, Col: 79.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' [4mPASSING[0m 0 AS x, 1 AS y);<br><br>Invalid expression / Unexpected token. Line 1, Col: 81.<br>  SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' PASSING [4m0[0m AS x, 1 AS y); |
| 24 | 31–31 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_EXISTS(jsonb '1', '$.a > 2' [4mERROR[0m ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_EXISTS(jsonb '1', '$.a > 2' ERROR [4mON[0m ERROR); |
| 86 | 109–109 | error | Invalid expression / Unexpected token. Line 1, Col: 65.<br>  SELECT JSON_VALUE(jsonb '["1"]', '$[*]' RETURNING int FORMAT [4mJSON[0m); |
| 93 | 122–132 | error | Invalid expression / Unexpected token. Line 5, Col: 28.<br>  SELECT<br>	x,<br>	JSON_VALUE(<br>		jsonb '{"a": 1, "b": 2}',<br>		'$.* ? (@ > $x)' PASSING [4mx[0m AS x<br>		RETURNING int<br>		DEFAULT -1 ON EMPTY<br>		DEFAULT -2 ON ERROR<br>	) y<br>FROM<br>	generate_series(0, 2) x |
| 97 | 148–150 | error | Expecting ). Line 2, Col: 34.<br>  SELECT x IS NULL AS is_null,<br>       json_query(x, '$.a' [4mDEFAULT[0m '"empty"' ON EMPTY) AS jq<br>FROM (VALUES ('{}'::jsonb), (NULL), ('{}'::jsonb)) v(x);<br><br>Invalid expression / Unexpected token. Line 2, Col: 44.<br>  SELECT x IS NULL AS is_null,<br>       json_query(x, '$.a' DEFAULT [4m'"empty"'[0m ON EMPTY) AS jq<br>FROM (VALUES ('{}'::jsonb), (NULL), ('{}'::jsonb)) v(x); |
| 98 | 152–154 | error | Expecting ). Line 2, Col: 39.<br>  SELECT x IS NULL AS is_null,<br>       json_exists(x, 'strict $.a' [4mTRUE[0m ON ERROR) AS je<br>FROM (VALUES ('1'::jsonb), (NULL), ('1'::jsonb)) v(x);<br><br>Invalid expression / Unexpected token. Line 2, Col: 42.<br>  SELECT x IS NULL AS is_null,<br>       json_exists(x, 'strict $.a' TRUE [4mON[0m ERROR) AS je<br>FROM (VALUES ('1'::jsonb), (NULL), ('1'::jsonb)) v(x); |
| 100 | 160–160 | error | Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a); |
| 101 | 161–161 | error | Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a RETURNING point); |
| 102 | 162–162 | error | Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a RETURNING point ERROR ON ERROR); |
| 103 | 164–165 | error | Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts); |
| 104 | 166–166 | error | Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamptz); |
| 105 | 167–167 | error | Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamp); |
| 106 | 168–168 | error | Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mdate[0m '2018-02-21 12:34:56 +10' AS ts RETURNING date); |
| 107 | 169–169 | error | Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtime[0m '2018-02-21 12:34:56 +10' AS ts RETURNING time); |
| 108 | 170–170 | error | Invalid expression / Unexpected token. Line 1, Col: 52.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimetz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timetz); |
| 109 | 171–171 | error | Invalid expression / Unexpected token. Line 1, Col: 55.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamp[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamp); |
| 110 | 173–174 | error | Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING json); |
| 111 | 175–175 | error | Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb); |
| 115 | 185–199 | error | Expecting ). Line 3, Col: 27.<br>  SELECT<br>	JSON_QUERY(js, '$') AS "unspec",<br>	JSON_QUERY(js, '$' [4mWITHOUT[0m WRAPPER) AS "without",<br>	JSON_QUERY(js, '$' WITH CONDITIONAL WRAPPER) AS "with cond",<br>	JSON_QUERY(js<br><br>Invalid expression / Unexpected token. Line 3, Col: 35.<br>  SELECT<br>	JSON_QUERY(js, '$') AS "unspec",<br>	JSON_QUERY(js, '$' WITHOUT [4mWRAPPER[0m) AS "without",<br>	JSON_QUERY(js, '$' WITH CONDITIONAL WRAPPER) AS "with cond",<br>	JSON_QUERY(js, '$' WI |
| 116 | 201–218 | error | Expecting ). Line 3, Col: 37.<br>  SELECT<br>	JSON_QUERY(js, 'strict $[*]') AS "unspec",<br>	JSON_QUERY(js, 'strict $[*]' [4mWITHOUT[0m WRAPPER) AS "without",<br>	JSON_QUERY(js, 'strict $[*]' WITH CONDITIONAL WRAPPER) AS "with cond",<br>	JSO<br><br>Invalid expression / Unexpected token. Line 3, Col: 45.<br>  SELECT<br>	JSON_QUERY(js, 'strict $[*]') AS "unspec",<br>	JSON_QUERY(js, 'strict $[*]' WITHOUT [4mWRAPPER[0m) AS "without",<br>	JSON_QUERY(js, 'strict $[*]' WITH CONDITIONAL WRAPPER) AS "with cond",<br>	JSON_QUERY( |
| 117 | 220–220 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text); |
| 118 | 221–221 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES); |
| 119 | 222–222 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES ON SCALAR STRING);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES ON SCALAR STRING); |
| 120 | 223–223 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES); |
| 121 | 224–224 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES ON SCALAR STRING);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES ON SCALAR STRING); |
| 122 | 225–225 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mOMIT[0m QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' OMIT [4mQUOTES[0m ERROR ON ERROR); |
| 123 | 226–226 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m json OMIT QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m json OMIT QUOTES ERROR ON ERROR); |
| 124 | 227–227 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m bytea FORMAT JSON OMIT QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m bytea FORMAT JSON OMIT QUOTES ERROR ON ERROR); |
| 125 | 229–230 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) ERROR ON ERROR); |
| 126 | 231–231 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3));<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3)); |
| 127 | 232–232 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) OMIT QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) OMIT QUOTES ERROR ON ERROR); |
| 128 | 233–233 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT 'bb' ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT 'bb' ON EMPTY); |
| 129 | 234–234 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT '"bb"'::jsonb ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT '"bb"'::jsonb ON EMPTY); |
| 130 | 236–238 | error | Expecting ). Line 1, Col: 39.<br>  SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m WRAPPER OMIT QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 39.<br>  SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m WRAPPER OMIT QUOTES); |
| 131 | 239–239 | error | Expecting ). Line 1, Col: 39.<br>  SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m CONDITIONAL WRAPPER OMIT QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 39.<br>  SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m CONDITIONAL WRAPPER OMIT QUOTES); |
| 132 | 240–241 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m CONDITIONAL WRAPPER KEEP QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m CONDITIONAL WRAPPER KEEP QUOTES); |
| 133 | 242–242 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m UNCONDITIONAL WRAPPER KEEP QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m UNCONDITIONAL WRAPPER KEEP QUOTES); |
| 134 | 243–243 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m WRAPPER KEEP QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m WRAPPER KEEP QUOTES); |
| 135 | 244–244 | error | Expecting ). Line 1, Col: 47.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITHOUT[0m WRAPPER OMIT QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 55.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' WITHOUT [4mWRAPPER[0m OMIT QUOTES); |
| 136 | 245–245 | error | Expecting ). Line 1, Col: 47.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITHOUT[0m WRAPPER KEEP QUOTES);<br><br>Invalid expression / Unexpected token. Line 1, Col: 55.<br>  SELECT JSON_QUERY(jsonb '["1"]', '$[*]' WITHOUT [4mWRAPPER[0m KEEP QUOTES); |
| 137 | 247–248 | error | Expecting ). Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] omit quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] omit quotes); |
| 138 | 249–249 | error | Expecting ). Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes); |
| 139 | 250–250 | error | Expecting ). Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 62.<br>  SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes error on error); |
| 140 | 251–251 | error | Expecting ). Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range omit quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range omit quotes); |
| 141 | 252–252 | error | Expecting ). Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range keep quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range keep quotes); |
| 142 | 253–253 | error | Expecting ). Line 1, Col: 61.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' 	[4mreturning[0m int4range keep quotes error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 61.<br>  SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' 	[4mreturning[0m int4range keep quotes error on error); |
| 145 | 256–256 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_char_domain OMIT QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_char_domain OMIT QUOTES ERROR ON ERROR); |
| 146 | 257–257 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_jsonb_domain OMIT QUOTES ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_jsonb_domain OMIT QUOTES ERROR ON ERROR); |
| 149 | 261–261 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mNULL[0m ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' NULL [4mON[0m EMPTY); |
| 150 | 262–262 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mON[0m EMPTY); |
| 151 | 263–263 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m ARRAY ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mARRAY[0m ON EMPTY); |
| 152 | 264–264 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m OBJECT ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mOBJECT[0m ON EMPTY); |
| 153 | 265–265 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY); |
| 154 | 266–266 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mDEFAULT[0m '"empty"' ON EMPTY);<br><br>Invalid expression / Unexpected token. Line 1, Col: 54.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' DEFAULT [4m'"empty"'[0m ON EMPTY); |
| 155 | 268–268 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY NULL ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY NULL ON ERROR); |
| 156 | 269–269 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY EMPTY ARRAY ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY EMPTY ARRAY ON ERROR); |
| 157 | 270–270 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY EMPTY OBJECT ON ERROR); |
| 158 | 271–271 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY ERROR ON ERROR); |
| 159 | 272–272 | error | Expecting ). Line 1, Col: 42.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m ERROR); |
| 160 | 272–274 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mERROR[0m ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' ERROR [4mON[0m ERROR); |
| 161 | 275–275 | error | Expecting ). Line 1, Col: 47.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mDEFAULT[0m '"empty"' ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' DEFAULT [4m'"empty"'[0m ON ERROR); |
| 162 | 277–277 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json); |
| 163 | 278–278 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json FORMAT JSON); |
| 164 | 279–279 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb); |
| 165 | 280–280 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb FORMAT JSON); |
| 166 | 281–281 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text); |
| 167 | 282–282 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m char(10));<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m char(10)); |
| 168 | 283–283 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text FORMAT JSON); |
| 169 | 284–284 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea); |
| 170 | 285–285 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea FORMAT JSON); |
| 171 | 287–287 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea EMPTY OBJECT ON ERROR); |
| 172 | 288–288 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea FORMAT JSON EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea FORMAT JSON EMPTY OBJECT ON ERROR); |
| 173 | 289–289 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m json EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m json EMPTY OBJECT ON ERROR); |
| 174 | 290–290 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m jsonb EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m jsonb EMPTY OBJECT ON ERROR); |
| 175 | 291–291 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR); |
| 176 | 292–292 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '"[3,4]"', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '"[3,4]"', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR); |
| 177 | 294–295 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 error on error); |
| 178 | 296–296 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int4 error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int4 error on error); |
| 179 | 297–297 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int8 error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int8 error on error); |
| 180 | 298–298 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m bool error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m bool error on error); |
| 181 | 299–299 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m numeric error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m numeric error on error); |
| 182 | 300–300 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m real error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m real error on error); |
| 183 | 301–301 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 error on error); |
| 184 | 302–303 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 omit quotes error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 omit quotes error on error); |
| 185 | 304–304 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 omit quotes error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 omit quotes error on error); |
| 186 | 306–307 | error | Expecting ). Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m anyarray EMPTY OBJECT ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 49.<br>  SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m anyarray EMPTY OBJECT ON ERROR); |
| 187 | 309–320 | error | Expecting ). Line 6, Col: 9.<br>  SELECT<br>	x, y,<br>	JSON_QUERY(<br>		jsonb '[1,2,3,4,5,null]',<br>		'$[*] ? (@ >= $x && @ <= $y)'<br>		[4mPASSING[0m x AS x, y AS y<br>		WITH CONDITIONAL WRAPPER<br>		EMPTY ARRAY ON EMPTY<br>	) list<br>FROM<br>	generate_series(0, 4<br><br>Invalid expression / Unexpected token. Line 6, Col: 11.<br>  SELECT<br>	x, y,<br>	JSON_QUERY(<br>		jsonb '[1,2,3,4,5,null]',<br>		'$[*] ? (@ >= $x && @ <= $y)'<br>		PASSING [4mx[0m AS x, y AS y<br>		WITH CONDITIONAL WRAPPER<br>		EMPTY ARRAY ON EMPTY<br>	) list<br>FROM<br>	generate_series(0, 4)  |
| 189 | 324–324 | error | Expecting ). Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc omit quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc omit quotes); |
| 190 | 325–325 | error | Expecting ). Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes); |
| 191 | 326–326 | error | Expecting ). Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes error on error);<br><br>Invalid expression / Unexpected token. Line 1, Col: 74.<br>  SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes error on error); |
| 195 | 333–333 | error | Expecting ). Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec);<br><br>Invalid expression / Unexpected token. Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec); |
| 196 | 334–334 | error | Expecting ). Line 1, Col: 138.<br>  ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 138.<br>  ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec ERROR ON ERROR); |
| 197 | 335–335 | error | Expecting ). Line 1, Col: 138.<br>  ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec);<br><br>Invalid expression / Unexpected token. Line 1, Col: 138.<br>  ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec); |
| 198 | 336–336 | error | Expecting ). Line 1, Col: 114.<br>  T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);<br><br>Expecting ). Line 1, Col: 114.<br>  T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);<br><br>Expecting ). Line 1, Col: 114.<br>  T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);<br><br>... and 1 more |
| 199 | 337–337 | error | Expecting ). Line 1, Col: 122.<br>   unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);<br><br>Expecting ). Line 1, Col: 122.<br>   unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);<br><br>Expecting ). Line 1, Col: 122.<br>   unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);<br><br>... and 1 more |
| 200 | 339–339 | error | Expecting ). Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath);<br><br>Invalid expression / Unexpected token. Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath); |
| 201 | 340–340 | error | Expecting ). Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 136.<br>  "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath ERROR ON ERROR); |
| 202 | 342–343 | error | Expecting ). Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"3"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"3"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER); |
| 203 | 344–344 | error | Expecting ). Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER ERROR ON ERROR); |
| 204 | 345–345 | error | Expecting ). Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER); |
| 205 | 346–346 | error | Expecting ). Line 1, Col: 111.<br>  LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[]));<br><br>Expecting ). Line 1, Col: 111.<br>  LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[]));<br><br>Invalid expression / Unexpected token. Line 1, Col: 111.<br>  LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[])); |
| 206 | 348–349 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.a' [4mRETURNING[0m sqljsonb_int_not_null);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.a' [4mRETURNING[0m sqljsonb_int_not_null); |
| 207 | 350–350 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null); |
| 208 | 351–351 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null ERROR ON EMPTY ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null ERROR ON EMPTY ERROR ON ERROR); |
| 209 | 353–354 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts);<br><br>Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts); |
| 210 | 355–355 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts RETURNING json);<br><br>Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING json); |
| 211 | 356–356 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb); |
| 271 | 459–459 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT ret_setint() ON ERROR) FROM test_jsonb_mutability;<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT ret_setint() ON ERROR) FROM test_jsonb_mutability; |
| 272 | 460–460 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT b + 1 ON ERROR) FROM test_jsonb_mutability;<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT b + 1 ON ERROR) FROM test_jsonb_mutability; |
| 273 | 461–461 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT sum(1) over() ON ERROR) FROM test_jsonb_mutability;<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT sum(1) over() ON ERROR) FROM test_jsonb_mutability; |
| 274 | 462–462 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT (SELECT 1) ON ERROR) FROM test_jsonb_mutability;<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT (SELECT 1) ON ERROR) FROM test_jsonb_mutability; |
| 282 | 472–476 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT '"1"')::jsonb ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT '"1"')::jsonb ON ERROR); |
| 283 | 477–478 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON_QUERY('"a"', '$.a' [4mRETURNING[0m queryfuncs_test_domain DEFAULT (select '"1"')::queryfuncs_test_domain ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 40.<br>  SELECT JSON_QUERY('"a"', '$.a' [4mRETURNING[0m queryfuncs_test_domain DEFAULT (select '"1"')::queryfuncs_test_domain ON ERROR); |
| 284 | 479–480 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT 1)::oid::int ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT 1)::oid::int ON ERROR); |
| 285 | 481–482 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::oid[]::int[] ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::oid[]::int[] ON ERROR); |
| 286 | 483–484 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::text COLLATE "C" ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::text COLLATE "C" ON ERROR); |
| 289 | 488–488 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m someparent DEFAULT (SELECT '(1)')::somechild::someparent ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m someparent DEFAULT (SELECT '(1)')::somechild::someparent ON ERROR); |
| 296 | 498–498 | error | Expecting ). Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'a' [4mWITH[0m WRAPPER);<br><br>Invalid expression / Unexpected token. Line 1, Col: 60.<br>  SELECT JSON_QUERY(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'a' [4mWITH[0m WRAPPER); |
| 297 | 499–499 | error | Expecting ). Line 1, Col: 76.<br>  SELECT JSON_QUERY(jsonb '{"a": 123}', ('$' \|\| '.' \|\| 'a' \|\| NULL)::date [4mWITH[0m WRAPPER);<br><br>Invalid expression / Unexpected token. Line 1, Col: 76.<br>  SELECT JSON_QUERY(jsonb '{"a": 123}', ('$' \|\| '.' \|\| 'a' \|\| NULL)::date [4mWITH[0m WRAPPER); |
| 300 | 505–505 | error | Expecting ). Line 1, Col: 29.<br>  SELECT JSON_QUERY(NULL [4mFORMAT[0m JSON, '$');<br><br>Invalid expression / Unexpected token. Line 1, Col: 34.<br>  SELECT JSON_QUERY(NULL FORMAT [4mJSON[0m, '$'); |
| 304 | 512–513 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb 'null', '$xyz' [4mPASSING[0m 1 AS xy);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb 'null', '$xyz' PASSING [4m1[0m AS xy); |
| 305 | 514–514 | error | Expecting ). Line 1, Col: 45.<br>  SELECT JSON_QUERY(jsonb 'null', '$xy' [4mPASSING[0m 1 AS xyz);<br><br>Invalid expression / Unexpected token. Line 1, Col: 47.<br>  SELECT JSON_QUERY(jsonb 'null', '$xy' PASSING [4m1[0m AS xyz); |
| 306 | 515–515 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb 'null', '$xyz' [4mPASSING[0m 1 AS xyz);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb 'null', '$xyz' PASSING [4m1[0m AS xyz); |
| 307 | 516–516 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb 'null', '$Xyz' [4mPASSING[0m 1 AS Xyz);<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb 'null', '$Xyz' PASSING [4m1[0m AS Xyz); |
| 308 | 517–517 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb 'null', '$Xyz' [4mPASSING[0m 1 AS "Xyz");<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb 'null', '$Xyz' PASSING [4m1[0m AS "Xyz"); |
| 309 | 518–518 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_QUERY(jsonb 'null', '$"Xyz"' [4mPASSING[0m 1 AS "Xyz");<br><br>Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_QUERY(jsonb 'null', '$"Xyz"' PASSING [4m1[0m AS "Xyz"); |
| 316 | 532–533 | error | Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mt[0m AS a) = t AS ok<br>  FROM test_passing_toast; |
| 318 | 536–537 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON_EXISTS(jsonb '1', '$' [4mDEFAULT[0m 1 ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_EXISTS(jsonb '1', '$' DEFAULT [4m1[0m ON ERROR); |
| 320 | 539–539 | error | Expecting ). Line 1, Col: 37.<br>  SELECT JSON_QUERY(jsonb '1', '$' [4mTRUE[0m ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 40.<br>  SELECT JSON_QUERY(jsonb '1', '$' TRUE [4mON[0m ERROR); |
| 323 | 545–545 | error | Expecting ). Line 1, Col: 38.<br>  SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (NULL::sqljsonb_int_not_null + 0) ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 38.<br>  SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (NULL::sqljsonb_int_not_null + 0) ON ERROR); |
| 325 | 547–547 | error | Expecting ). Line 1, Col: 38.<br>  SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (('a' \|\| (random() * 0)::int)::int + 0) ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 38.<br>  SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (('a' \|\| (random() * 0)::int)::int + 0) ON ERROR); |
| 329 | 555–555 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m int[] DEFAULT '{11}' ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m int[] DEFAULT '{11}' ON ERROR); |
| 331 | 557–557 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m queryfuncs_int[] DEFAULT '{11}' ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m queryfuncs_int[] DEFAULT '{11}' ON ERROR); |
| 333 | 560–560 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": "x"}', '$' [4mRETURNING[0m compcoalesce);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT JSON_QUERY(jsonb '{"a": "x"}', '$' [4mRETURNING[0m compcoalesce); |
| 334 | 561–561 | error | Expecting ). Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": 11}', '$' [4mRETURNING[0m compcoalesce);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": 11}', '$' [4mRETURNING[0m compcoalesce); |
| 335 | 562–562 | error | Expecting ). Line 1, Col: 59.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": "B"}', '$' [4mRETURNING[0m compcoalesce);<br><br>Invalid expression / Unexpected token. Line 1, Col: 59.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": "B"}', '$' [4mRETURNING[0m compcoalesce); |
| 336 | 563–563 | error | Expecting ). Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": 0}', '$' [4mRETURNING[0m compcoalesce);<br><br>Invalid expression / Unexpected token. Line 1, Col: 57.<br>  SELECT JSON_QUERY(jsonb '{"a": 1, "b": 0}', '$' [4mRETURNING[0m compcoalesce); |
| 341 | 571–571 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 ERROR ON ERROR); |
| 342 | 572–572 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 DEFAULT '1' ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 DEFAULT '1' ON ERROR); |
| 343 | 573–573 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk ERROR ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk ERROR ON ERROR); |
| 344 | 574–574 | error | Expecting ). Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk DEFAULT '1' ON ERROR);<br><br>Invalid expression / Unexpected token. Line 1, Col: 44.<br>  SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk DEFAULT '1' ON ERROR); |


