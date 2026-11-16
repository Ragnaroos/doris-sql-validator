# sqljson：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 87 | 56 | 31 | 1 | 55 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/sqljson.yaml)；[首轮 Markdown](../../../validation/sqljson/validation.md) / [首轮 JSON](../../../validation/sqljson/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-sqljson-0002-346f0009

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 2，源行 3–3，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON(NULL);
~~~

社区生成 SQL：


~~~sql
SELECT JSON(NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0003-a9569d2c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 3，源行 4–4，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON('{ "a" : 1 } ');
~~~

社区生成 SQL：


~~~sql
SELECT JSON('{ "a" : 1 } ')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0007-7e3bd2d6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 7，源行 8–8，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_typeof(JSON('{ "a" : 1 } '));
~~~

社区生成 SQL：


~~~sql
SELECT PG_TYPEOF(JSON('{ "a" : 1 } '))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0008-08261502

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 8，源行 10–10，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON('   1   '::json);
~~~

社区生成 SQL：


~~~sql
SELECT JSON(CAST('   1   ' AS JSON))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0009-9360d8e4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 9，源行 11–11，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON('   1   '::jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON(CAST('   1   ' AS JSONB))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0012-15c90301

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 12，源行 15–15，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON('{"a": 1, "a": 2}');
~~~

社区生成 SQL：


~~~sql
SELECT JSON('{"a": 1, "a": 2}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0022-d7d54d91

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 22，源行 27–27，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_typeof(JSON('123'));
~~~

社区生成 SQL：


~~~sql
SELECT PG_TYPEOF(JSON('123'))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0051-e3442d62

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 51，源行 67–67，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING json);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `json`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0052-39a48994

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 52，源行 68–68，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING json FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `json` FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0053-8e6196dd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 53，源行 69–69，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `jsonb`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0054-93e19cf4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 54，源行 70–70，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING jsonb FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `jsonb` FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0055-bf277f7e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 55，源行 71–71，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `text`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0056-27679350

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 56，源行 72–72，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING text FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING `text` FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0059-1e1245ec

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 59，源行 75–75，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING bytea);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING bytea)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0060-b4f9dd0f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 60，源行 76–76，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0061-488b91cc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 61，源行 77–77，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF8);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON ENCODING UTF8)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0066-195f92ad

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 66，源行 83–83，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSON) FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0068-134f492c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 68，源行 85–85，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSONB) FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0071-d2f3c48a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 71，源行 89–89，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': 2 + 3);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', 2 + 3)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7bad8f95c7775344ea131e18454dab2e15ddca50a5ebd01417f67f08432c9c70",
    "doris_digest=61c0deaa4390b7fcbf8607b763e6b192cfff5d4caff4544f4cc71bca59dbffc6",
    "source_sample=[['{\"a\" : 5}']]",
    "doris_sample=[['{\"a\":5}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0072-d2f3c48a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 72，源行 90–90，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a' VALUE 2 + 3);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', 2 + 3)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7bad8f95c7775344ea131e18454dab2e15ddca50a5ebd01417f67f08432c9c70",
    "doris_digest=61c0deaa4390b7fcbf8607b763e6b192cfff5d4caff4544f4cc71bca59dbffc6",
    "source_sample=[['{\"a\" : 5}']]",
    "doris_sample=[['{\"a\":5}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0074-47c9e80c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 74，源行 93–93，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(('a' || 2) VALUE 1);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT((CONCAT('a', 2)), 1)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=1c98c96aff5f7588e95e247713a2928ea24de9c9ddea01724a0527c825128451",
    "doris_digest=cd13966f4c832cbd06902ff505f33d957767147e1de942ea884f08ce1c2ee4a4",
    "source_sample=[['{\"a2\" : 1}']]",
    "doris_sample=[['{\"a2\":1}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0075-671952eb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 75，源行 94–96，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': 2::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', CAST(2 AS STRING))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=0399782f6d55f802e4d1f75f6f0c3368f42c465f9d2badc7259ba6137127104b",
    "doris_digest=5b4f54211cdc333c4b0f534431cbf0e89f3ce70bed3e50221bc6a6bf2aea12ad",
    "source_sample=[['{\"a\" : \"2\"}']]",
    "doris_sample=[['{\"a\":\"2\"}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0076-671952eb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 76，源行 97–97，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a' VALUE 2::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', CAST(2 AS STRING))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=0399782f6d55f802e4d1f75f6f0c3368f42c465f9d2badc7259ba6137127104b",
    "doris_digest=5b4f54211cdc333c4b0f534431cbf0e89f3ce70bed3e50221bc6a6bf2aea12ad",
    "source_sample=[['{\"a\" : \"2\"}']]",
    "doris_sample=[['{\"a\":\"2\"}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0077-ebc7ac8a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 77，源行 98–99，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(1::text: 2);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT(CAST(1 AS STRING), 2)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=01c18f7e676fc8964b290929a179022dac6849f358d3b8ecd2dd37482f1d4cdb",
    "doris_digest=ff6615340188f41c5dc208e03ee0d3e57bf2f3da1062ca86b2ce0ec388357753",
    "source_sample=[['{\"1\" : 2}']]",
    "doris_sample=[['{\"1\":2}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0078-72a2205c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 78，源行 100–100，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT((1::text) VALUE 2);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT((CAST(1 AS STRING)), 2)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=01c18f7e676fc8964b290929a179022dac6849f358d3b8ecd2dd37482f1d4cdb",
    "doris_digest=ff6615340188f41c5dc208e03ee0d3e57bf2f3da1062ca86b2ce0ec388357753",
    "source_sample=[['{\"1\" : 2}']]",
    "doris_sample=[['{\"1\":2}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0081-b9d917c8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 81，源行 106–111，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(
	'a': '123',
	1.23: 123,
	'c': json '[ 1,true,{ } ]',
	'd': jsonb '{ "x" : 123.45 }'
);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '123', 1.23, 123, 'c', '[ 1,true,{ } ]', 'd', CAST('{ "x" : 123.45 }' AS JSONB))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7f2ce4c66b385d622164d1e98e2a3a8101ee4ac250e1b09126051a2d9525901b",
    "doris_digest=2404651bd4eab81bbd93036a8735754272bb8b8f6b8cbf8214a113aafbce0c66",
    "source_sample=[['{\"a\": \"123\", \"c\": [1, true, {}], \"d\": {\"x\": 123.45}, \"1.23\": 123}']]",
    "doris_sample=[['{\"a\":\"123\",\"1.23\":123,\"c\":\"[ 1,true,{ } ]\",\"d\":{\"x\":123.45}}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0082-793614ae

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 82，源行 113–119，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(
	'a': '123',
	1.23: 123,
	'c': json '[ 1,true,{ } ]',
	'd': jsonb '{ "x" : 123.45 }'
	RETURNING jsonb
);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '123', 1.23, 123, 'c', '[ 1,true,{ } ]', 'd', CAST('{ "x" : 123.45 }' AS JSONB) RETURNING `jsonb`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 104)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 104)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0083-aaaaf0cc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 83，源行 121–129，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa'));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '123', 'b', JSON_OBJECT('a', 111, 'b', 'aaa'))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=23d34396e9bba821e067e7ab3f869f7c561703d4fe66657d7618fc3b405d3723",
    "doris_digest=ccc9c66d0bbf4b6e4e59210993584123e5b86c8d74acb2b199a361ae4ecc5e3d",
    "source_sample=[['{\"a\" : \"123\", \"b\" : {\"a\" : 111, \"b\" : \"aaa\"}}']]",
    "doris_sample=[['{\"a\":\"123\",\"b\":{\"a\":111,\"b\":\"aaa\"}}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0084-fe2afc9b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 84，源行 130–130，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa' RETURNING jsonb));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '123', 'b', JSON_OBJECT('a', 111, 'b', 'aaa' RETURNING `jsonb`))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 69)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0085-cf7e7536

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 85，源行 132–132，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING `text`))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0086-c06829ab

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 86，源行 133–133，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text) FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING `text`) FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0087-390d22a4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 87，源行 134–134，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea));
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING bytea))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0088-00c725f2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 88，源行 135–135，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea) FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING bytea) FORMAT JSON)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0089-ccef3b65

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 89，源行 137–137，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=30bd1dc64ee814c4b11b5ce4e1910cac23b7c717a9d3152f1dcb7c385abdc339",
    "doris_digest=6029d3d87ea3d8b2b13ee7943c98a00a9b7d1287203fd8adfe4dc50498205a3b",
    "source_sample=[['{\"a\" : \"1\", \"b\" : null, \"c\" : 2}']]",
    "doris_sample=[['{\"a\":\"1\",\"b\":null,\"c\":2}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0090-4100b949

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 90，源行 138–138，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 NULL ON NULL);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2 NULL ON NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 47)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0091-d5dec91a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 91，源行 139–139，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 ABSENT ON NULL);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2 ABSENT ON NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 47)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0099-58eb4d86

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 99，源行 150–150，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITHOUT UNIQUE KEYS)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0101-593d412a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 101，源行 152–152，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITHOUT UNIQUE KEYS RETURNING `jsonb`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0102-fd2215ab

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 102，源行 153–153，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, 4: NULL, '5': 'a' ABSENT ON NULL WITH UNIQUE RETURNING jsonb);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '3', 1, 4, NULL, '5', 'a' ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 62)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 62)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0103-9cacb58a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 103，源行 155–156，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CASE 'x' WHEN JSON_OBJECT('a': 'b' RETURNING text) THEN 1 ELSE 0 END;
~~~

社区生成 SQL：


~~~sql
SELECT CASE 'x' WHEN JSON_OBJECT('a', 'b' RETURNING `text`) THEN 1 ELSE 0 END
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0163-abd3e937

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 163，源行 287–290，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT	JSON_OBJECTAGG('key': 1) IS NULL,
		JSON_OBJECTAGG('key': 1 RETURNING jsonb) IS NULL
WHERE FALSE;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECTAGG('key', 1) IS NULL, JSON_OBJECTAGG('key', 1 RETURNING `jsonb`) IS NULL WHERE FALSE
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 65)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 65)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0167-73cfdf71

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 167，源行 304–312，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
	JSON_OBJECTAGG(k: v),
	JSON_OBJECTAGG(k: v NULL ON NULL),
	JSON_OBJECTAGG(k: v ABSENT ON NULL),
	JSON_OBJECTAGG(k: v RETURNING jsonb),
	JSON_OBJECTAGG(k: v NULL ON NULL RETURNING jsonb),
	JSON_OBJECTAGG(k: v ABSENT ON NULL RETURNING jsonb)
FROM
	(VALUES (1, 1), (1, NULL), (2, NULL), (3, 3)) foo(k, v);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECTAGG(k, v), JSON_OBJECTAGG(k, v NULL ON NULL), JSON_OBJECTAGG(k, v ABSENT ON NULL), JSON_OBJECTAGG(k, v RETURNING `jsonb`), JSON_OBJECTAGG(k, v NULL ON NULL RETURNING `jsonb`), JSON_OBJECTAGG(k, v ABSENT ON NULL RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, NULL UNION ALL SELECT 3, 3) AS foo
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 49)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0170-c919f1c8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 170，源行 320–321，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS)
FROM (VALUES (1, 1), (0, NULL), (3, NULL), (2, 2), (4, NULL)) foo(k, v);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 0, NULL UNION ALL SELECT 3, NULL UNION ALL SELECT 2, 2 UNION ALL SELECT 4, NULL) AS foo
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0173-d56175c2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 173，源行 329–330，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb)
FROM (VALUES (1, 1), (0, NULL),(4, null), (5, null),(6, null),(2, 2)) foo(k, v);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 0, NULL UNION ALL SELECT 4, NULL UNION ALL SELECT 5, NULL UNION ALL SELECT 6, NULL UNION ALL SELECT 2, 2) AS foo
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0178-9008fe3b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 178，源行 346–347，同文回显第 1 次；历史成功 2 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k)
FROM (VALUES (1,1), (2,2)) a(k,v);
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v WITH UNIQUE KEYS) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 2, 2) AS a
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0181-cd2e0593

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 181，源行 356–358，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL)
OVER (ORDER BY k)
FROM (VALUES (1,1), (1,null), (2,2)) a(k,v);
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v ABSENT ON NULL) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS a
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0182-0b849be1

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 182，源行 360–362，同文回显第 1 次；历史成功 3 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL)
OVER (ORDER BY k RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM (VALUES (1,1), (1,null), (2,2)) a(k,v);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function J_S_O_N_OBJECT_AGG
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L127)（行 127）；[sqlglot/generator.py:3317](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generator.py#L3317)（行 3317）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v ABSENT ON NULL) OVER (ORDER BY k NULLS LAST RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS a;
~~~

实际证据：[probe-01 JSON](../evidence/pg-sqljson-0182-0b849be1/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-sqljson-0182-0b849be1/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\\n\")"
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

### pg-sqljson-0271-ef876352

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 271，源行 554–555，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT NULL IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0272-4206dfb2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 272，源行 556–556，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL IS NOT JSON;
~~~

社区生成 SQL：


~~~sql
SELECT NOT NULL IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 19)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 19)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0273-41ef498e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 273，源行 557–557，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL::json IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS JSON) IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 29)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 29)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0274-b22967f6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 274，源行 558–558，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL::jsonb IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS JSONB) IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 30)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 30)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0275-e37eaee8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 275，源行 559–559，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL::text IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS STRING) IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 31)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 31)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0276-3725ca72

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 276，源行 560–560，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NULL::bytea IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS VARBINARY) IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 34)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 34)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0300-c4b3e4db

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 300，源行 616–616，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '' IS JSON;
~~~

社区生成 SQL：


~~~sql
SELECT '' IS JSON
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 13)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'IS JSON'(line 1, pos 13)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-sqljson-0326-0f327300

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)；原语句 326，源行 726–726，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT JSON_OBJECT('a': JSON_OBJECTAGG('b': 1 RETURNING text) FORMAT JSON);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_OBJECT('a', JSON_OBJECTAGG('b', 1 RETURNING `text`) FORMAT JSON)
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

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-sqljson-0001-77f7d4f6 / SELECT JSON(); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 1 | syntax error at or near ")" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSON'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0011-44407adb / SELECT JSON(123); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 11 | cannot cast type integer to json | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSON'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0057-4e7cbe3a / SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING UTF8); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 57 | cannot set JSON encoding for non-bytea output types | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0058-85507464 / SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING INVALID_ENCODING); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 58 | unrecognized JSON encoding: invalid_encoding | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0062-93593d80 / SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF16); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 62 | unsupported JSON encoding | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0063-4b63a422 / SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF32); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 63 | unsupported JSON encoding | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0064-0d7459f4 / SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 64 | cannot use non-string types with explicit FORMAT JSON clause | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0065-9043d551 / SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON ENCODING UTF8); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 65 | JSON ENCODING clause is only allowed for bytea input type | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0067-59f72b1a / SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON ENCODING UTF8); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 67 | JSON ENCODING clause is only allowed for bytea input type | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0069-df18a825 / SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON ENCODING UTF8); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 69 | JSON ENCODING clause is only allowed for bytea input type | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0070-3ed43f9d / SELECT JSON_OBJECT(NULL: 1); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 70 | null value not allowed for object key | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = json_object key can't be NULL: json_object(NULL, 1)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0080-13b666a6 / SELECT JSON_OBJECT(ARRAY[1,2,3]: 'aaa'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 80 | key value must be scalar, not array, composite, or json | SQLGlot 解析/生成失败；UnsupportedError: Arrays are not supported by MySQL | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0092-3790e5f7 / SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, repeat('x', 1000): 1, 2: repeat('a', 100) WITH UNIQUE); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 92 | duplicate JSON object key value: "2" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 86)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0093-acbaa7d0 / SELECT JSON_OBJECT(1: 1, '1': NULL WITH UNIQUE); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 93 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0094-f73d48c0 / SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 94 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0095-8c86e00c / SELECT JSON_OBJECT(1: 1, '1': NULL NULL ON NULL WITH UNIQUE RETURNING jsonb); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 95 | duplicate JSON object key value | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0096-1dd063a7 / SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE RETURNING jsonb); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 96 | duplicate JSON object key value | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0097-0e919246 / SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 NULL ON NULL WITH UNIQUE); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 97 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0098-89651d9e / SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 98 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0100-4b5d20e7 / SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE RETURNING jsonb); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 100 | duplicate JSON object key value | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0164-af03a290 / SELECT JSON_OBJECTAGG(NULL: 1); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 164 | null value not allowed for object key | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSON_OBJECTAGG'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0165-a1180034 / SELECT JSON_OBJECTAGG(NULL: 1 RETURNING jsonb); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 165 | field name must not be null | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0168-c9ed413f / SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS)<br>FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 168 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0169-37cd8fa3 / SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS)<br>FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 169 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0171-2e6e989c / SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS RETURNING jsonb)<br>FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 171 | duplicate JSON object key value | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0172-dcca672d / SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb)<br>FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 172 | duplicate JSON object key value | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0179-042a7503 / SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k)<br>FROM (VALUES (1,1), (1,2), (2,2)) a(k,v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 179 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0180-cd2e0593 / SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL WITH UNIQUE KEYS)<br>   OVER (ORDER BY k)<br>FROM (VALUES (1,1), (1,null), (2,2)) a(k,v); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 180 | duplicate JSON object key value: "1" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0277-a43252a0 / SELECT NULL::int IS JSON; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 277 | cannot use type integer in IS JSON predicate | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 28)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0301-fa18fe76 / SELECT bytea '\x00' IS JSON; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 301 | invalid byte sequence for encoding "UTF8": 0x00 | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 37)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-sqljson-0312-4933fc10 / SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING varchar(2))); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 312 | value too long for type character varying(2) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-sqljson-0050-90a4ab71 | SELECT JSON_OBJECT(); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/sqljson.out)，语句 50 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 55 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 4 | 5–5 | error | Expecting ). Line 1, Col: 33.<br>  SELECT JSON('{ "a" : 1 } ' [4mFORMAT[0m JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 38.<br>  SELECT JSON('{ "a" : 1 } ' FORMAT [4mJSON[0m); |
| 5 | 6–6 | error | Expecting ). Line 1, Col: 33.<br>  SELECT JSON('{ "a" : 1 } ' [4mFORMAT[0m JSON ENCODING UTF8);<br><br>Invalid expression / Unexpected token. Line 1, Col: 38.<br>  SELECT JSON('{ "a" : 1 } ' FORMAT [4mJSON[0m ENCODING UTF8); |
| 6 | 7–7 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON('{ "a" : 1 } '::bytea [4mFORMAT[0m JSON ENCODING UTF8);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON('{ "a" : 1 } '::bytea FORMAT [4mJSON[0m ENCODING UTF8); |
| 10 | 12–12 | error | Expecting ). Line 1, Col: 32.<br>  SELECT JSON('   1   '::json [4mWITH[0m UNIQUE KEYS);<br><br>Invalid expression / Unexpected token. Line 1, Col: 32.<br>  SELECT JSON('   1   '::json [4mWITH[0m UNIQUE KEYS); |
| 13 | 16–16 | error | Expecting ). Line 1, Col: 35.<br>  SELECT JSON('{"a": 1, "a": 2}' [4mWITH[0m UNIQUE KEYS);<br><br>Invalid expression / Unexpected token. Line 1, Col: 35.<br>  SELECT JSON('{"a": 1, "a": 2}' [4mWITH[0m UNIQUE KEYS); |
| 14 | 17–17 | error | Expecting ). Line 1, Col: 38.<br>  SELECT JSON('{"a": 1, "a": 2}' [4mWITHOUT[0m UNIQUE KEYS);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT JSON('{"a": 1, "a": 2}' WITHOUT [4mUNIQUE[0m KEYS); |
| 43 | 53–53 | error | Expecting ). Line 1, Col: 32.<br>  SELECT JSON_SERIALIZE('1' [4mFORMAT[0m JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 37.<br>  SELECT JSON_SERIALIZE('1' FORMAT [4mJSON[0m); |
| 44 | 54–54 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m bytea);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m bytea); |
| 45 | 55–55 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar); |
| 47 | 58–59 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m jsonb); |
| 73 | 91–92 | error | Required keyword: 'this' missing for <class 'sqlglot.expressions.core.DPipe'>. Line 1, Col: 28.<br>  SELECT JSON_OBJECT('a' \|\| 2[4m:[0m 1);<br><br>Invalid expression / Unexpected token. Line 1, Col: 28.<br>  SELECT JSON_OBJECT('a' \|\| 2[4m:[0m 1); |
| 79 | 101–103 | error | Invalid expression / Unexpected token. Line 1, Col: 30.<br>  SELECT JSON_OBJECT(json '[1]'[4m:[0m 123); |
| 116 | 180–180 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m json);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m json); |
| 117 | 181–181 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m json FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m json FORMAT JSON); |
| 118 | 182–182 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m jsonb); |
| 119 | 183–183 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m jsonb FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m jsonb FORMAT JSON); |
| 120 | 184–184 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text); |
| 121 | 185–185 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON); |
| 122 | 186–186 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING UTF8);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING UTF8); |
| 123 | 187–187 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING INVALID_ENCODING);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING INVALID_ENCODING); |
| 124 | 188–188 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea); |
| 125 | 189–189 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON); |
| 126 | 190–190 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF8);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF8); |
| 127 | 191–191 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF16);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF16); |
| 128 | 192–192 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF32);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF32); |
| 130 | 196–196 | error | Expecting ). Line 1, Col: 38.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' [4mNULL[0m   ON NULL);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' NULL   [4mON[0m NULL); |
| 131 | 197–197 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' [4mABSENT[0m ON NULL);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' ABSENT [4mON[0m NULL); |
| 132 | 198–198 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON_ARRAY(NULL, NULL, 'b' [4mABSENT[0m ON NULL);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY(NULL, NULL, 'b' ABSENT [4mON[0m NULL); |
| 133 | 199–199 | error | Expecting ). Line 1, Col: 38.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' [4mNULL[0m   ON NULL RETURNING jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' NULL   [4mON[0m NULL RETURNING jsonb); |
| 134 | 200–200 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' [4mABSENT[0m ON NULL RETURNING jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY('a',  NULL, 'b' ABSENT [4mON[0m NULL RETURNING jsonb); |
| 135 | 201–201 | error | Expecting ). Line 1, Col: 40.<br>  SELECT JSON_ARRAY(NULL, NULL, 'b' [4mABSENT[0m ON NULL RETURNING jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 43.<br>  SELECT JSON_ARRAY(NULL, NULL, 'b' ABSENT [4mON[0m NULL RETURNING jsonb); |
| 136 | 203–203 | error | Expecting ). Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text));<br><br>Expecting ). Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text));<br><br>Invalid expression / Unexpected token. Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text)); |
| 137 | 204–204 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text));<br><br>Expecting ). Line 1, Col: 51.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text));<br><br>Invalid expression / Unexpected token. Line 1, Col: 56.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' FORMAT [4mJSON[0m RETURNING text)); |
| 138 | 205–205 | error | Expecting ). Line 1, Col: 51.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text) FORMAT JSON);<br><br>Expecting ). Line 1, Col: 51.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text) FORMAT JSON);<br><br>Invalid expression / Unexpected token. Line 1, Col: 56.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' FORMAT [4mJSON[0m RETURNING text) FORMAT JSON); |
| 141 | 210–210 | error | Expecting ). Line 1, Col: 117.<br>  SON_ARRAY(SELECT i FROM (VALUES (NULL::int[]), ('{1,2}'), (NULL), (NULL), ('{3,4}'), (NULL)) foo(i) [4mRETURNING[0m jsonb);<br><br>Invalid expression / Unexpected token. Line 1, Col: 117.<br>  SON_ARRAY(SELECT i FROM (VALUES (NULL::int[]), ('{1,2}'), (NULL), (NULL), ('{3,4}'), (NULL)) foo(i) [4mRETURNING[0m jsonb); |
| 143 | 214–214 | error | values does not support CTE. Line 1, Col: 53.<br>  SELECT JSON_ARRAY(WITH x AS (SELECT 1) VALUES (TRUE)[4m)[0m; |
| 146 | 220–225 | error | Expecting ). Line 4, Col: 13.<br>  LL), (4)) t1(a)<br>WHERE JSON_ARRAY(<br>    SELECT b FROM (VALUES (1), (2), (3)) t2(b) WHERE b = t1.a<br>    [4mRETURNING[0m jsonb<br>) = '[]'::jsonb;<br><br>Invalid expression / Unexpected token. Line 4, Col: 13.<br>  LL), (4)) t1(a)<br>WHERE JSON_ARRAY(<br>    SELECT b FROM (VALUES (1), (2), (3)) t2(b) WHERE b = t1.a<br>    [4mRETURNING[0m jsonb<br>) = '[]'::jsonb; |
| 147 | 227–229 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(1));<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(1)); |
| 148 | 230–230 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(1));<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(1)); |
| 149 | 231–232 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(3));<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(3)); |
| 150 | 233–233 | error | Expecting ). Line 1, Col: 48.<br>  SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(2));<br><br>Invalid expression / Unexpected token. Line 1, Col: 48.<br>  SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(2)); |
| 154 | 240–243 | error | Expecting ). Line 2, Col: 27.<br>  SELECT	JSON_ARRAYAGG(i) IS NULL,<br>		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) IS NULL<br>FROM generate_series(1, 0) i;<br><br>Invalid expression / Unexpected token. Line 2, Col: 27.<br>  SELECT	JSON_ARRAYAGG(i) IS NULL,<br>		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) IS NULL<br>FROM generate_series(1, 0) i; |
| 155 | 245–247 | error | Expecting ). Line 2, Col: 27.<br>  SELECT	JSON_ARRAYAGG(i),<br>		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb)<br>FROM generate_series(1, 5) i;<br><br>Invalid expression / Unexpected token. Line 2, Col: 27.<br>  SELECT	JSON_ARRAYAGG(i),<br>		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb)<br>FROM generate_series(1, 5) i; |
| 158 | 255–256 | error | Expecting ). Line 1, Col: 50.<br>  SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON)<br>FROM generate_series(1, 5) i;<br><br>Expecting ). Line 1, Col: 50.<br>  SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON)<br>FROM generate_series(1, 5) i;<br><br>Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON)<br>FROM generate_series(1, 5) i; |
| 159 | 258–260 | error | Expecting ). Line 2, Col: 30.<br>  SELECT	JSON_ARRAYAGG(NULL),<br>		JSON_ARRAYAGG(NULL [4mRETURNING[0m jsonb)<br>FROM generate_series(1, 5);<br><br>Invalid expression / Unexpected token. Line 2, Col: 30.<br>  SELECT	JSON_ARRAYAGG(NULL),<br>		JSON_ARRAYAGG(NULL [4mRETURNING[0m jsonb)<br>FROM generate_series(1, 5); |
| 160 | 262–264 | error | Expecting ). Line 1, Col: 30.<br>  SELECT	JSON_ARRAYAGG(NULL [4mNULL[0m ON NULL),<br>		JSON_ARRAYAGG(NULL NULL ON NULL RETURNING jsonb)<br>FROM generate_series(1, 5);<br><br>Invalid expression / Unexpected token. Line 1, Col: 33.<br>  SELECT	JSON_ARRAYAGG(NULL NULL [4mON[0m NULL),<br>		JSON_ARRAYAGG(NULL NULL ON NULL RETURNING jsonb)<br>FROM generate_series(1, 5); |
| 161 | 266–279 | error | Expecting ). Line 3, Col: 28.<br>  SELECT<br>	JSON_ARRAYAGG(bar) as no_options,<br>	JSON_ARRAYAGG(bar [4mRETURNING[0m jsonb) as returning_jsonb,<br>	JSON_ARRAYAGG(bar ABSENT ON NULL) as absent_on_null,<br>	JSON_ARRAYAGG(bar<br><br>Invalid expression / Unexpected token. Line 3, Col: 28.<br>  SELECT<br>	JSON_ARRAYAGG(bar) as no_options,<br>	JSON_ARRAYAGG(bar [4mRETURNING[0m jsonb) as returning_jsonb,<br>	JSON_ARRAYAGG(bar ABSENT ON NULL) as absent_on_null,<br>	JSON_ARRAYAGG(bar |
| 292 | 594–595 | error | Expecting ). Line 1, Col: 41.<br>  SELECT JSON('{"a":1}'::sqljson_mystr [4mWITH[0m UNIQUE KEYS);<br><br>Invalid expression / Unexpected token. Line 1, Col: 41.<br>  SELECT JSON('{"a":1}'::sqljson_mystr [4mWITH[0m UNIQUE KEYS); |
| 311 | 703–704 | error | Expecting ). Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar(2));<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar(2)); |
| 313 | 706–706 | error | Expecting ). Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2)));<br><br>Expecting ). Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2)));<br><br>Invalid expression / Unexpected token. Line 1, Col: 54.<br>  SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2))); |
| 314 | 707–707 | error | Expecting ). Line 1, Col: 47.<br>  SELECT JSON_ARRAYAGG(('111' \|\| i)::bytea [4mFORMAT[0m JSON NULL ON NULL RETURNING varchar(2)) FROM generate_series(1,1) i;<br><br>Invalid expression / Unexpected token. Line 1, Col: 52.<br>  SELECT JSON_ARRAYAGG(('111' \|\| i)::bytea FORMAT [4mJSON[0m NULL ON NULL RETURNING varchar(2)) FROM generate_series(1,1) i; |
| 317 | 712–712 | error | Expecting ). Line 1, Col: 37.<br>  SELECT JSON_SERIALIZE('123' [4mRETURNING[0m sqljson_char2);<br><br>Invalid expression / Unexpected token. Line 1, Col: 37.<br>  SELECT JSON_SERIALIZE('123' [4mRETURNING[0m sqljson_char2); |
| 318 | 713–713 | error | Expecting ). Line 1, Col: 36.<br>  SELECT JSON_SERIALIZE('12' [4mRETURNING[0m sqljson_char2);<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT JSON_SERIALIZE('12' [4mRETURNING[0m sqljson_char2); |
| 329 | 741–749 | error | Expecting ). Line 2, Col: 37.<br>  SELECT i % 2 AS g,<br>	JSON_ARRAYAGG(i ORDER BY i [4mRETURNING[0m jsonb) AS ja,<br>	JSON_ARRAYAGG(i ORDER BY i RETURNING text) AS ja_text,<br>	JSON_ARRAYAGG(i ORDER BY i N<br><br>Invalid expression / Unexpected token. Line 2, Col: 37.<br>  SELECT i % 2 AS g,<br>	JSON_ARRAYAGG(i ORDER BY i [4mRETURNING[0m jsonb) AS ja,<br>	JSON_ARRAYAGG(i ORDER BY i RETURNING text) AS ja_text,<br>	JSON_ARRAYAGG(i ORDER BY i N |
| 331 | 757–759 | error | Expecting ). Line 1, Col: 27.<br>  SELECT JSON_ARRAYAGG(i [4mNULL[0m ON NULL RETURNING jsonb) OVER (ORDER BY i DESC) AS ja,<br>	row_number() OVER (ORDER BY i) AS rn<br>FROM g<br><br>Invalid expression / Unexpected token. Line 1, Col: 30.<br>  SELECT JSON_ARRAYAGG(i NULL [4mON[0m NULL RETURNING jsonb) OVER (ORDER BY i DESC) AS ja,<br>	row_number() OVER (ORDER BY i) AS rn<br>FROM gene |


