# bit：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 66 | 57 | 9 | 0 | 57 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/bit.yaml)；[首轮 Markdown](../../../validation/bit/validation.md) / [首轮 JSON](../../../validation/bit/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-bit-0024-89958cf4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 24，源行 61–62，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT SUBSTRING('01010101'::bit(8) FROM 2 FOR 2147483646) AS "1010101";
~~~

社区生成 SQL：


~~~sql
SELECT SUBSTRING(CAST('01010101' AS BIT(8)), 2, 2147483646) AS `1010101`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0025-6b3902a8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 25，源行 63–63，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR 2147483646) AS "01010101";
~~~

社区生成 SQL：


~~~sql
SELECT SUBSTRING(CAST('01010101' AS BIT(8)), -10, 2147483646) AS `01010101`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0047-301a8e99

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 47，源行 123–124，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1010' IN B'0000101');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1010', b'0000101')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0048-caf7f5b8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 48，源行 124–125，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1010' IN B'00001010');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1010', b'00001010')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0049-595c054b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 49，源行 125–126，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1010' IN B'00000101');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1010', b'00000101')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0050-bb4bcf7c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 50，源行 126–127，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1010' IN B'000001010');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1010', b'000001010')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0051-3a142de9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 51，源行 127–129，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'' IN B'00001010');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'', b'00001010')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0052-00592fea

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 52，源行 129–130，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'0' IN B'');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'0', b'')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''0'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0053-42e1d4df

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 53，源行 130–131，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'' IN B'');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'', b'')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0054-1ecd298b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 54，源行 131–132，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'101101' IN B'001011011011011000');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'101101', b'001011011011011000')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''101101'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''101101'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0055-2846a24a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 55，源行 132–133，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'10110110' IN B'001011011011010');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'10110110', b'001011011011010')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''10110110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''10110110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0056-fcfbadfd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 56，源行 133–134，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1011011011011' IN B'001011011011011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1011011011011', b'001011011011011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0057-93be16f6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 57，源行 134–135，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'1011011011011' IN B'00001011011011011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'1011011011011', b'00001011011011011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0058-30959611

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 58，源行 135–137，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'11101011' IN B'11101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'11101011', b'11101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0059-58faa847

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 59，源行 137–138，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'11101011' IN B'011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'11101011', b'011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0060-92ceb8e3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 60，源行 138–139，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'11101011' IN B'00011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'11101011', b'00011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0061-97441cec

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 61，源行 139–140，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'11101011' IN B'0000011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'11101011', b'0000011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0062-d1d81002

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 62，源行 140–142，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0063-70bb2d0f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 63，源行 142–143，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0064-cb7ca512

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 64，源行 143–144，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'000111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'000111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0065-064bcc08

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 65，源行 144–145，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'00000111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'00000111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0066-6b7cee3e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 66，源行 145–147，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'11101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'11101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0067-0f374bcc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 67，源行 147–148，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0068-d261399c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 68，源行 148–149，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'00011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'00011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0069-dba0b492

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 69，源行 149–150，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0000011101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0000011101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0070-d1d81002

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 70，源行 150–152，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0071-70bb2d0f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 71，源行 152–153，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0072-cb7ca512

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 72，源行 153–154，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'000111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'000111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0073-064bcc08

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 73，源行 154–155，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'00000111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'00000111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0074-d546974c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 74，源行 155–157，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'000001110101111101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'000001110101111101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0075-7a835daf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 75，源行 157–158，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0000001110101111101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0000001110101111101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0076-14193951

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 76，源行 158–159，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'000000001110101111101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'000000001110101111101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0077-dfb6069c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 77，源行 159–160，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'00000000001110101111101011');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'00000000001110101111101011')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0078-217a86de

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 78，源行 160–162，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0079-09b22e90

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 79，源行 162–163，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'00000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'00000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0080-552fd82c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 80，源行 163–164，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'0000000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'0000000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0081-ac8b2e03

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 81，源行 164–165，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'111010110' IN B'000000000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'111010110', b'000000000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0082-21fef106

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 82，源行 165–167，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'000000000011101011111010110' IN B'000000000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'000000000011101011111010110', b'000000000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0083-8313870d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 83，源行 167–168，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'00000000011101011111010110' IN B'000000000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'00000000011101011111010110', b'000000000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''00000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''00000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0084-e9975bc6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 84，源行 168–169，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT POSITION(B'0000000000011101011111010110' IN B'000000000011101011111010110');
~~~

社区生成 SQL：


~~~sql
SELECT LOCATE(b'0000000000011101011111010110', b'000000000011101011111010110')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''0000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0107-124a125e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 107，源行 212–213，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT get_bit(B'0101011000100', 10);
~~~

社区生成 SQL：


~~~sql
SELECT GETBIT(b'0101011000100', 10)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''0101011000100'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0108-73e11c02

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 108，源行 214–214，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT set_bit(B'0101011000100100', 15, 1);
~~~

社区生成 SQL：


~~~sql
SELECT SET_BIT(b'0101011000100100', 15, 1)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0110-6542d715

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 110，源行 215–218，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT overlay(B'0101011100' placing '001' from 2 for 3);
~~~

社区生成 SQL：


~~~sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 2 FOR 3)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0111-0e365504

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 111，源行 219–219，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT overlay(B'0101011100' placing '101' from 6);
~~~

社区生成 SQL：


~~~sql
SELECT OVERLAY(b'0101011100' PLACING '101' FROM 6)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0112-f46cc6df

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 112，源行 220–220，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT overlay(B'0101011100' placing '001' from 11);
~~~

社区生成 SQL：


~~~sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 11)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0113-3453faf6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 113，源行 221–221，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT overlay(B'0101011100' placing '001' from 20);
~~~

社区生成 SQL：


~~~sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 20)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0114-941c9a67

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 114，源行 223–224，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(B'0101011100'::bit(10));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(b'0101011100' AS BIT(10)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'0101011100''(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'CAST(b'0101011100''(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0115-f2a0ef80

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 115，源行 225–225，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(B'1111111111'::bit(10));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(b'1111111111' AS BIT(10)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'1111111111''(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'CAST(b'1111111111''(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0116-3c6fed87

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 116，源行 226–226，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(repeat('0', 100)::bit(100));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(REPEAT('0', 100) AS BIT(100)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0117-2b92a352

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 117，源行 227–227，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(repeat('1', 100)::bit(100));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(REPEAT('1', 100) AS BIT(100)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0118-fc3fdefd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 118，源行 228–228，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(repeat('01', 500)::bit(1000));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(REPEAT('01', 500) AS BIT(1000)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0119-949253dd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 119，源行 229–229，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT bit_count(repeat('10101', 200)::bit(1000));
~~~

社区生成 SQL：


~~~sql
SELECT BIT_COUNT(CAST(REPEAT('10101', 200) AS BIT(1000)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0123-64e8d6bc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 123，源行 242–243，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('01010001', 'bit(10)');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('01010001', 'bit(10)')
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0125-086339bb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 125，源行 245–245，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('01010Z01', 'bit(8)');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('01010Z01', 'bit(8)')
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0127-81e3a323

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 127，源行 247–247，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('x01010Z01', 'bit(32)');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('x01010Z01', 'bit(32)')
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0129-b5856278

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 129，源行 250–250，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('01010Z01', 'varbit');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('01010Z01', 'varbit')
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-bit-0131-d7060d25

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)；原语句 131，源行 252–252，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('x01010Z01', 'varbit');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('x01010Z01', 'varbit')
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

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-bit-0015-ababd899 / SELECT b' 0'; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 15 | " " is not a valid binary digit | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0016-61bca181 / SELECT b'0 '; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 16 | " " is not a valid binary digit | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0017-d071168a / SELECT x' 0'; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 17 | " " is not a valid hexadecimal digit | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0018-8fbe6087 / SELECT x'0 '; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 18 | " " is not a valid hexadecimal digit | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0026-af154103 / SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR -2147483646) AS "error"; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 26 | negative substring length not allowed | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0044-e16f06ff / select B'001' & B'10'; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 44 | cannot AND bit strings of different sizes | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '&' expecting {<EOF>, ';'}(line 1, pos 14)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0045-1ef7e230 / select B'0111' \| B'011'; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 45 | cannot OR bit strings of different sizes | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '\|' expecting {<EOF>, ';'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0046-479ef11f / select B'0010' # B'011101'; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 46 | cannot XOR bit strings of different sizes | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '^' expecting {<EOF>, ';'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-bit-0109-73f2b61f / SELECT set_bit(B'0101011000100100', 16, 1); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/bit.out)，语句 109 | bit index 16 out of valid range (0..15) | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 1 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 122 | 240–240 | error | Expected one read-only Query, got Alias |


