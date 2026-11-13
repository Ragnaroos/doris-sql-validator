# float8：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 114 | 88 | 26 | 38 | 50 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/float8.yaml)；[首轮 Markdown](../../../validation/float8/validation.md) / [首轮 JSON](../../../validation/float8/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-float8-0011-6ab989be

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 11，源行 24–25，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float8send('2.2250738585072014E-308'::float8);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT8SEND(CAST('2.2250738585072014E-308' AS DOUBLE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT8SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0020-309c7b69

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 20，源行 37–38，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('34.5', 'float8');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('34.5', 'float8')
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

### pg-float8-0021-537262c3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 21，源行 39–39，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('xyz', 'float8');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('xyz', 'float8')
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

### pg-float8-0022-eb12c7c1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 22，源行 40–40，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('1e4000', 'float8');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('1e4000', 'float8')
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

### pg-float8-0034-b19cea1b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 34，源行 56–56，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '42'::float8 / 'Infinity'::float8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('42' AS DOUBLE) / CAST('Infinity' AS DOUBLE)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0036-2499e7b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 36，源行 58–58，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::float8 / '0'::float8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('nan' AS DOUBLE) / CAST('0' AS DOUBLE)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c46fdfbd4b447ef3fb87f13d68cb7001336c6ff0bd8a77afc8fb1dad5b570dbc",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['NaN']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0037-78ceabd8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 37，源行 59–59，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::numeric::float8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('nan' AS DECIMAL) AS DOUBLE)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c46fdfbd4b447ef3fb87f13d68cb7001336c6ff0bd8a77afc8fb1dad5b570dbc",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['NaN']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0058-93ee51d9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 58，源行 119–120，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sqrt(float8 '64') AS eight;
~~~

社区生成 SQL：


~~~sql
SELECT SQRT(CAST('64' AS DOUBLE)) AS eight
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=13168d628f126187e5ab8ed8760ef058a8c46888c8fbd173c2116f73f3bd787b",
    "doris_digest=c0f73b40a705e9a0988482af5579853a1221107a4ee9b3555cf4fd4fe470d839",
    "source_sample=[['8']]",
    "doris_sample=[['8.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0059-93ee51d9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 59，源行 122–122，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT |/ float8 '64' AS eight;
~~~

社区生成 SQL：


~~~sql
SELECT SQRT(CAST('64' AS DOUBLE)) AS eight
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=13168d628f126187e5ab8ed8760ef058a8c46888c8fbd173c2116f73f3bd787b",
    "doris_digest=c0f73b40a705e9a0988482af5579853a1221107a4ee9b3555cf4fd4fe470d839",
    "source_sample=[['8']]",
    "doris_sample=[['8.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0061-8c09f610

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 61，源行 128–129，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '144', float8 '0.5');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('144' AS DOUBLE), CAST('0.5' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e39f2590227da609d2c6bd9a7121025ae0dd23dfbb3765a6fa80f305932ed42d",
    "doris_digest=0150be0a17c5a59e3355c5a0887632f6b8604b0fa945fe6322276bd124e73043",
    "source_sample=[['12']]",
    "doris_sample=[['12.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0066-32a6f72c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 66，源行 134–134，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '1', float8 'NaN');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('NaN' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0067-47f22839

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 67，源行 135–135，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 'NaN', float8 '0');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('NaN' AS DOUBLE), CAST('0' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0068-ce75067e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 68，源行 136–136，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 'inf', float8 '0');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('0' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0069-45a0403b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 69，源行 137–137，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-inf', float8 '0');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('0' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0070-d81797b6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 70，源行 138–138，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '0', float8 'inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('0' AS DOUBLE), CAST('inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0072-4b7595fc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 72，源行 140–140，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '1', float8 'inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0073-5fa95364

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 73，源行 141–141，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '1', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0074-dcc2fab4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 74，源行 142–142，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-1', float8 'inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-1' AS DOUBLE), CAST('inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0075-3211ff12

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 75，源行 143–143，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-1', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-1' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0076-c3a3e121

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 76，源行 144–144，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '0.1', float8 'inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('0.1' AS DOUBLE), CAST('inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0077-97dc9f6a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 77，源行 145–145，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-0.1', float8 'inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-0.1' AS DOUBLE), CAST('inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0082-e2449205

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 82，源行 150–150，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '1.1', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('1.1' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0083-9c0182b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 83，源行 151–151，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-1.1', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-1.1' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0084-a3c7d189

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 84，源行 152–152，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 'inf', float8 '-2');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('-2' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0087-16088520

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 87，源行 155–155，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 'inf', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0089-f731dc20

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 89，源行 159–159，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-inf', float8 '-3');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('-3' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e39b10178c78f9bd1c5116e545832a80142cc3a9349f15817e98b89714cc4959",
    "doris_digest=349485c0cd6dc28f614ee25c330c9f86176af48276e28a0be4c64ac0bb54991c",
    "source_sample=[['-0']]",
    "doris_sample=[['-0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0094-e437580b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 94，源行 164–164，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT power(float8 '-inf', float8 '-inf');
~~~

社区生成 SQL：


~~~sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('-inf' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=04b6a59fbf68bdb99a609ce26f90526600cde3f4e715563e583741d378434735",
    "doris_digest=5dcdd7513229483c5ca11f2855a4b30137be52487c0b21491c3801d1cf31f037",
    "source_sample=[['0']]",
    "doris_sample=[['0.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0096-285130b3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 96，源行 171–172，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT exp('inf'::float8), exp('-inf'::float8), exp('nan'::float8);
~~~

社区生成 SQL：


~~~sql
SELECT EXP(CAST('inf' AS DOUBLE)), EXP(CAST('-inf' AS DOUBLE)), EXP(CAST('nan' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=0079759cc3d37d9d3c2762582b045fd02023179b49212064c5e6e020915bee2f",
    "doris_digest=13c0b26a2fc7e693fb8106c58be85ece14ef9820c578f252e3e066fea4e05c4d",
    "source_sample=[['Infinity', '0', 'NaN']]",
    "doris_sample=[['Infinity', '0.0', 'NaN']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0097-a14fc3c2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 97，源行 174–175，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ||/ float8 '27' AS three;
~~~

社区生成 SQL：


~~~sql
SELECT CBRT(CAST('27' AS DOUBLE)) AS three
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7e5acccc8c8fd7375f8700c06ef68c1dbf50eb98c0bb12527a571aade278a5a7",
    "doris_digest=3bb8608d7cea8e84f6ca133a32de72a928d916997d2a0d4933d1d60b03d47714",
    "source_sample=[['3']]",
    "doris_sample=[['3.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0103-c9b3ade2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 103，源行 190–190，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0 ^ 0 + 0 ^ 1 + 0 ^ 0.0 + 0 ^ 0.5;
~~~

社区生成 SQL：


~~~sql
SELECT POWER(0, 0) + POWER(0, 1) + POWER(0, 0.0) + POWER(0, 0.5)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a0a88ee57364f8f632469bb45e2fd5057419c8c1c1f6d52216176988ab0fbb90",
    "doris_digest=069ad5bfea6175ddb5c7be34b4c5ed1e9db905ab759a002e8b54040c721d3ed9",
    "source_sample=[['2']]",
    "doris_sample=[['2.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0109-ed5a37d8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 109，源行 202–205，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sinh(float8 '1');
~~~

社区生成 SQL：


~~~sql
SELECT SINH(CAST('1' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f04b554ccbad8f58777155532a548debcc5c83505d86c4bf6da486ff413e2864",
    "doris_digest=daec81e9ba8c12e3635054e58dbde10dd15d179f813b4b31f7027ddfc647417f",
    "source_sample=[['1.1752011936438']]",
    "doris_sample=[['1.175201193643801']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0110-b7f4cc0b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 110，源行 206–206，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT cosh(float8 '1');
~~~

社区生成 SQL：


~~~sql
SELECT COSH(CAST('1' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=fc94db70f17fc49365e6252d459a2ee7f8e2269747af824aec1f3d809bb62299",
    "doris_digest=ea01656affacedbcc687813797124e85d4651c8e92db3b1f2e0125b39e98011e",
    "source_sample=[['1.54308063481524']]",
    "doris_sample=[['1.543080634815244']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0111-e3136b56

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 111，源行 207–207，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT tanh(float8 '1');
~~~

社区生成 SQL：


~~~sql
SELECT TANH(CAST('1' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=b4b3474fc2a917121050b49df4b91829761d0d2144499b81a7b60c78ac5925d6",
    "doris_digest=0caf999f1495d10c1e571f1806c0f26b5c41c127bf0c20acd762ffa4ea18c5c0",
    "source_sample=[['0.761594155955765']]",
    "doris_sample=[['0.7615941559557649']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0112-793e70b9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 112，源行 208–208，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT asinh(float8 '1');
~~~

社区生成 SQL：


~~~sql
SELECT ASINH(CAST('1' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c8da209204cd24480716b5817432a10b321620efdfafd5972acd4ea710351714",
    "doris_digest=3698d4eecf6f470458b597a79778f910cbe97bbc64566fe89ceeb09b7461ba5a",
    "source_sample=[['0.881373587019543']]",
    "doris_sample=[['0.8813735870195429']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0113-0f62ba6b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 113，源行 209–209，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT acosh(float8 '2');
~~~

社区生成 SQL：


~~~sql
SELECT ACOSH(CAST('2' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=ebe7062137903ab28e40c64524670d54286cef90cd6758884effdfa796b3ba2d",
    "doris_digest=d4c2d0d48eae09a895f73d299bea6f5c94ec4a5da54622270c60818c8d4da2a0",
    "source_sample=[['1.31695789692482']]",
    "doris_sample=[['1.316957896924817']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0114-5dfbae93

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 114，源行 210–210，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT atanh(float8 '0.5');
~~~

社区生成 SQL：


~~~sql
SELECT ATANH(CAST('0.5' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=24eda159b9e5cee4937752630b436ab018d0974c42b745c1a227a5186832a82a",
    "doris_digest=9fbf0cf084db75dc92313415d693e1e235eddf36882cd2d8d90d922f5e34c9df",
    "source_sample=[['0.549306144334055']]",
    "doris_sample=[['0.5493061443340549']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0121-43d168cf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 121，源行 218–218，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT tanh(float8 'infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TANH(CAST('infinity' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0122-34c43150

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 122，源行 219–219，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT tanh(float8 '-infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TANH(CAST('-infinity' AS DOUBLE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=5576f4f12f153e3b83ed1c69c8673b0a35ba57c0755593621366a5f09cdb1ac1",
    "doris_digest=8d12c7f657983bc6800195025092c9ef8d9057e82351644c619a441657d13cff",
    "source_sample=[['-1']]",
    "doris_sample=[['-1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0133-1686bfe4

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 133，源行 236–244，同文回显第 1 次；历史成功 22 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       erf(x),
       erfc(x)
FROM (VALUES (float8 '-infinity'),
      (-28), (-6), (-3.4), (-2.1), (-1.1), (-0.45),
      (-1.2e-9), (-2.3e-13), (-1.2e-17), (0),
      (1.2e-17), (2.3e-13), (1.2e-9),
      (0.45), (1.1), (2.1), (3.4), (6), (28),
      (float8 'infinity'), (float8 'nan')) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, ERF(x), ERFC(x) FROM (SELECT CAST('-infinity' AS DOUBLE) AS x UNION ALL SELECT -28 UNION ALL SELECT -6 UNION ALL SELECT -3.4 UNION ALL SELECT -2.1 UNION ALL SELECT -1.1 UNION ALL SELECT -0.45 UNION ALL SELECT -1.2e-9 UNION ALL SELECT -2.3e-13 UNION ALL SELECT -1.2e-17 UNION ALL SELECT 0 UNION ALL SELECT 1.2e-17 UNION ALL SELECT 2.3e-13 UNION ALL SELECT 1.2e-9 UNION ALL SELECT 0.45 UNION ALL SELECT 1.1 UNION ALL SELECT 2.1 UNION ALL SELECT 3.4 UNION ALL SELECT 6 UNION ALL SELECT 28 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'ERF'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'ERF'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT x, ERF(x), ERFC(x) FROM (SELECT CAST('-infinity' AS DOUBLE) AS x UNION ALL SELECT -28 UNION ALL SELECT -6 UNION ALL SELECT -3.4 UNION ALL SELECT -2.1 UNION ALL SELECT -1.1 UNION ALL SELECT -0.45 UNION ALL SELECT -1.2e-9 UNION ALL SELECT -2.3e-13 UNION ALL SELECT -1.2e-17 UNION ALL SELECT 0 UNION ALL SELECT 1.2e-17 UNION ALL SELECT 2.3e-13 UNION ALL SELECT 1.2e-9 UNION ALL SELECT 0.45 UNION ALL SELECT 1.1 UNION ALL SELECT 2.1 UNION ALL SELECT 3.4 UNION ALL SELECT 6 UNION ALL SELECT 28 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t;
~~~

实际证据：[probe-01 JSON](../evidence/pg-float8-0133-1686bfe4/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-float8-0133-1686bfe4/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ERF'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ERF'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-float8-0136-1407357d

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 136，源行 252–256，同文回显第 1 次；历史成功 8 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       gamma(x),
       lgamma(x)
FROM (VALUES (0.5), (1), (2), (3), (4), (5),
             (float8 'infinity'), (float8 'nan')) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, GAMMA(x), LGAMMA(x) FROM (SELECT 0.5 AS x UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'GAMMA'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT x, GAMMA(x), LGAMMA(x) FROM (SELECT 0.5 AS x UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t;
~~~

实际证据：[probe-01 JSON](../evidence/pg-float8-0136-1407357d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-float8-0136-1407357d/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "float8",<br>      "Doris原生类型": "float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'GAMMA'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'GAMMA'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-float8-0138-64577def

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 138，源行 259–259，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lgamma(float8 '-infinity');
~~~

社区生成 SQL：


~~~sql
SELECT LGAMMA(CAST('-infinity' AS DOUBLE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'LGAMMA'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0140-ac1c1632

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 140，源行 261–261，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lgamma(float8 '-1000.5');
~~~

社区生成 SQL：


~~~sql
SELECT LGAMMA(CAST('-1000.5' AS DOUBLE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'LGAMMA'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0146-6496a2bb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 146，源行 267–267，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lgamma(float8 '1000');
~~~

社区生成 SQL：


~~~sql
SELECT LGAMMA(CAST('1000' AS DOUBLE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'LGAMMA'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0163-6ca27d28

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 163，源行 295–295，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '9223372036854773760'::float8::int8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('9223372036854773760' AS DOUBLE) AS BIGINT)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=73f893219df94c432194c89f00ff1229869f64d272b8921b514925cefda4ad7b",
    "doris_digest=6d66ab032776589c264dc241e54653bff564e9d3c5bd0cced72c2ab97602ffc3",
    "source_sample=[['9223372036854773760']]",
    "doris_sample=[['9223372036854773800']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0165-05c5bbe3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 165，源行 297–297，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '-9223372036854775808.5'::float8::int8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('-9223372036854775808.5' AS DOUBLE) AS BIGINT)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=d37f1303dc98b751907a0195235fec31b7c06857fb89850f6e1e73b547812f62",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['-9223372036854775808']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0167-04b2aa54

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 167，源行 300–306，同文回显第 1 次；历史成功 9 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       sind(x),
       sind(x) IN (-1,-0.5,0,0.5,1) AS sind_exact
FROM (VALUES (0), (30), (90), (150), (180),
      (210), (270), (330), (360)) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, SIND(x), SIND(x) IN (-1, -0.5, 0, 0.5, 1) AS sind_exact FROM (SELECT 0 AS x UNION ALL SELECT 30 UNION ALL SELECT 90 UNION ALL SELECT 150 UNION ALL SELECT 180 UNION ALL SELECT 210 UNION ALL SELECT 270 UNION ALL SELECT 330 UNION ALL SELECT 360) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'SIND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'SIND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0168-a8fd9aee

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 168，源行 308–312，同文回显第 1 次；历史成功 9 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       cosd(x),
       cosd(x) IN (-1,-0.5,0,0.5,1) AS cosd_exact
FROM (VALUES (0), (60), (90), (120), (180),
      (240), (270), (300), (360)) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, COSD(x), COSD(x) IN (-1, -0.5, 0, 0.5, 1) AS cosd_exact FROM (SELECT 0 AS x UNION ALL SELECT 60 UNION ALL SELECT 90 UNION ALL SELECT 120 UNION ALL SELECT 180 UNION ALL SELECT 240 UNION ALL SELECT 270 UNION ALL SELECT 300 UNION ALL SELECT 360) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'COSD'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'COSD'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0169-763c8507

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 169，源行 314–322，同文回显第 1 次；历史成功 9 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       tand(x),
       tand(x) IN ('-Infinity'::float8,-1,0,
                   1,'Infinity'::float8) AS tand_exact,
       cotd(x),
       cotd(x) IN ('-Infinity'::float8,-1,0,
                   1,'Infinity'::float8) AS cotd_exact
FROM (VALUES (0), (45), (90), (135), (180),
      (225), (270), (315), (360)) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, TAND(x), TAND(x) IN (CAST('-Infinity' AS DOUBLE), -1, 0, 1, CAST('Infinity' AS DOUBLE)) AS tand_exact, COTD(x), COTD(x) IN (CAST('-Infinity' AS DOUBLE), -1, 0, 1, CAST('Infinity' AS DOUBLE)) AS cotd_exact FROM (SELECT 0 AS x UNION ALL SELECT 45 UNION ALL SELECT 90 UNION ALL SELECT 135 UNION ALL SELECT 180 UNION ALL SELECT 225 UNION ALL SELECT 270 UNION ALL SELECT 315 UNION ALL SELECT 360) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TAND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TAND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0170-b46298bf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 170，源行 324–329，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       asind(x),
       asind(x) IN (-90,-30,0,30,90) AS asind_exact,
       acosd(x),
       acosd(x) IN (0,60,90,120,180) AS acosd_exact
FROM (VALUES (-1), (-0.5), (0), (0.5), (1)) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, ASIND(x), ASIND(x) IN (-90, -30, 0, 30, 90) AS asind_exact, ACOSD(x), ACOSD(x) IN (0, 60, 90, 120, 180) AS acosd_exact FROM (SELECT -1 AS x UNION ALL SELECT -0.5 UNION ALL SELECT 0 UNION ALL SELECT 0.5 UNION ALL SELECT 1) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'ASIND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'ASIND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float8-0171-b35da73e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)；原语句 171，源行 331–335，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT x,
       atand(x),
       atand(x) IN (-90,-45,0,45,90) AS atand_exact
FROM (VALUES ('-Infinity'::float8), (-1), (0), (1),
      ('Infinity'::float8)) AS t(x);
~~~

社区生成 SQL：


~~~sql
SELECT x, ATAND(x), ATAND(x) IN (-90, -45, 0, 45, 90) AS atand_exact FROM (SELECT CAST('-Infinity' AS DOUBLE) AS x UNION ALL SELECT -1 UNION ALL SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT CAST('Infinity' AS DOUBLE)) AS t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'ATAND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'ATAND'\")",
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
| pg-float8-0007-88440e0e / SELECT '10e400'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 7 | "10e400" is out of range for type double precision | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0008-cd413fb2 / SELECT '-10e400'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 8 | "-10e400" is out of range for type double precision | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0009-c9fe8398 / SELECT '10e-400'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 9 | "10e-400" is out of range for type double precision | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0010-7b8ae6f8 / SELECT '-10e-400'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 10 | "-10e-400" is out of range for type double precision | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0029-7bf74ce8 / SELECT 'N A N'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 29 | invalid input syntax for type double precision: "N A N" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0030-cb4f1143 / SELECT 'NaN x'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 30 | invalid input syntax for type double precision: "NaN x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0031-f4d72ba1 / SELECT ' INFINITY    x'::float8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 31 | invalid input syntax for type double precision: " INFINITY    x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0071-012234df / SELECT power(float8 '0', float8 '-inf'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 71 | zero raised to a negative power is undefined | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0092-86201c1e / SELECT power(float8 '-inf', float8 '3.5'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 92 | a negative number raised to a non-integer power yields a complex result | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0127-d9cb28b5 / SELECT acosh(float8 '-infinity'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 127 | input is out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0129-ff445481 / SELECT atanh(float8 'infinity'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 129 | input is out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0130-d6edd65a / SELECT atanh(float8 '-infinity'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 130 | input is out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0137-5cb14dc7 / SELECT gamma(float8 '-infinity'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 137 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0139-1db07e6d / SELECT gamma(float8 '-1000.5'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 139 | value out of range: underflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0141-3bc04443 / SELECT gamma(float8 '-1'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 141 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0142-de3bfeba / SELECT lgamma(float8 '-1'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 142 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0143-2cddd068 / SELECT gamma(float8 '0'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 143 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0144-bd18f753 / SELECT lgamma(float8 '0'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 144 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0145-08c21a50 / SELECT gamma(float8 '1000'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 145 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0147-8523fd1a / SELECT lgamma(float8 '1e308'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 147 | value out of range: overflow | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0156-dbb86232 / SELECT '32767.6'::float8::int2; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 156 | smallint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0158-df00ee2c / SELECT '-32768.6'::float8::int2; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 158 | smallint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0160-c5ba41f5 / SELECT '2147483647.6'::float8::int4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 160 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0162-902a328b / SELECT '-2147483648.6'::float8::int4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 162 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0164-7ca4124d / SELECT '9223372036854775807'::float8::int8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 164 | bigint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float8-0166-170d0b04 / SELECT '-9223372036854780000'::float8::int8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 166 | bigint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-float8-0024-c1a914ec | SELECT 'NaN'::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 24 |
| pg-float8-0025-6616e5ff | SELECT 'nan'::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 25 |
| pg-float8-0026-e24d20f0 | SELECT '   NAN  '::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 26 |
| pg-float8-0027-5327a329 | SELECT 'infinity'::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 27 |
| pg-float8-0028-dbdcc7e0 | SELECT '          -INFINiTY   '::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 28 |
| pg-float8-0032-2ed2fe36 | SELECT 'Infinity'::float8 + 100.0; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 32 |
| pg-float8-0033-fab0f874 | SELECT 'Infinity'::float8 / 'Infinity'::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 33 |
| pg-float8-0035-98f3140d | SELECT 'nan'::float8 / 'nan'::float8; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 35 |
| pg-float8-0062-1d0158b0 | SELECT power(float8 'NaN', float8 '0.5'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 62 |
| pg-float8-0063-3b58d3ae | SELECT power(float8 '144', float8 'NaN'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 63 |
| pg-float8-0064-29084e2c | SELECT power(float8 'NaN', float8 'NaN'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 64 |
| pg-float8-0065-3a2a1fed | SELECT power(float8 '-1', float8 'NaN'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 65 |
| pg-float8-0078-fcd3a905 | SELECT power(float8 '1.1', float8 'inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 78 |
| pg-float8-0079-3a0d29d4 | SELECT power(float8 '-1.1', float8 'inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 79 |
| pg-float8-0080-fa0c31da | SELECT power(float8 '0.1', float8 '-inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 80 |
| pg-float8-0081-db4c6e0a | SELECT power(float8 '-0.1', float8 '-inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 81 |
| pg-float8-0085-1d6f83d3 | SELECT power(float8 'inf', float8 '2'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 85 |
| pg-float8-0086-ad3650f5 | SELECT power(float8 'inf', float8 'inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 86 |
| pg-float8-0088-086db460 | SELECT power(float8 '-inf', float8 '-2') = '0'; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 88 |
| pg-float8-0090-dfe0b3d9 | SELECT power(float8 '-inf', float8 '2'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 90 |
| pg-float8-0091-101f01f3 | SELECT power(float8 '-inf', float8 '3'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 91 |
| pg-float8-0093-1b9189db | SELECT power(float8 '-inf', float8 'inf'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 93 |
| pg-float8-0115-e81acbb2 | SELECT sinh(float8 'infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 115 |
| pg-float8-0116-a5bc31de | SELECT sinh(float8 '-infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 116 |
| pg-float8-0117-fdb20380 | SELECT sinh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 117 |
| pg-float8-0118-1a8c506f | SELECT cosh(float8 'infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 118 |
| pg-float8-0119-ce38a8c0 | SELECT cosh(float8 '-infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 119 |
| pg-float8-0120-ff137ba2 | SELECT cosh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 120 |
| pg-float8-0123-7a12cdce | SELECT tanh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 123 |
| pg-float8-0124-6e06598a | SELECT asinh(float8 'infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 124 |
| pg-float8-0125-33896df8 | SELECT asinh(float8 '-infinity'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 125 |
| pg-float8-0126-53f0039a | SELECT asinh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 126 |
| pg-float8-0128-04142f37 | SELECT acosh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 128 |
| pg-float8-0131-91778068 | SELECT atanh(float8 'nan'); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 131 |
| pg-float8-0155-f8b09ed2 | SELECT '32767.4'::float8::int2; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 155 |
| pg-float8-0157-5d91cc84 | SELECT '-32768.4'::float8::int2; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 157 |
| pg-float8-0159-269e8ceb | SELECT '2147483647.4'::float8::int4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 159 |
| pg-float8-0161-1c93a18d | SELECT '-2147483648.4'::float8::int4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float8.out)，语句 161 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

