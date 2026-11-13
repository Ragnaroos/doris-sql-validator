# float4：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 46 | 37 | 9 | 11 | 26 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/float4.yaml)；[首轮 Markdown](../../../validation/float4/validation.md) / [首轮 JSON](../../../validation/float4/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-float4-0027-9d7f4076

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 27，源行 39–40，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('34.5', 'float4');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('34.5', 'float4')
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

### pg-float4-0028-1a832cc8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 28，源行 41–41，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('xyz', 'float4');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('xyz', 'float4')
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

### pg-float4-0029-f6cc5990

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 29，源行 42–42，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('1e400', 'float4');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('1e400', 'float4')
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

### pg-float4-0041-0785fb35

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 41，源行 58–58，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '42'::float4 / 'Infinity'::float4;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('42' AS FLOAT) / CAST('Infinity' AS FLOAT)
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

### pg-float4-0043-b1829e7e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 43，源行 60–60，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::float4 / '0'::float4;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('nan' AS FLOAT) / CAST('0' AS FLOAT)
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

### pg-float4-0044-48facef7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 44，源行 61–61，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::numeric::float4;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('nan' AS DECIMAL) AS FLOAT)
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

### pg-float4-0067-27fcec9b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 67，源行 110–110，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '-2147483648.5'::float4::int4;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('-2147483648.5' AS FLOAT) AS INT)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=2de1cd545afd58bfc3d93d9d3517eb5a2c8c25f69332785628c74ab646e72928",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['-2147483648']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0069-908a1692

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 69，源行 112–112，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '9223369837831520256'::float4::int8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('9223369837831520256' AS FLOAT) AS BIGINT)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=193ec0d6f61fcd24e79c23779c14f0f2ba3841a7c57bca791d2b06b82f78bab5",
    "doris_digest=838892ec5617b51bbda93fb6310fbc3a729a5054dd8242648e6a6a5632f95a52",
    "source_sample=[['9223369837831520256']]",
    "doris_sample=[['9223369800000000000']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0071-63715b27

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 71，源行 114–114，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '-9223372036854775808.5'::float4::int8;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('-9223372036854775808.5' AS FLOAT) AS BIGINT)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=d37f1303dc98b751907a0195235fec31b7c06857fb89850f6e1e73b547812f62",
    "doris_digest=731965f29101acd6789ac23da8d13b5aeb617efa6f832b7852b12dc66a4bf9ad",
    "source_sample=[['-9223372036854775808']]",
    "doris_sample=[['-9223372000000000000']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0073-8a7309ae

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 73，源行 117–121，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('5e-20'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('5e-20' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT FLOAT4SEND(CAST('5e-20' AS FLOAT));
~~~

实际证据：[probe-01 JSON](../evidence/pg-float4-0073-8a7309ae/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-float4-0073-8a7309ae/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bytea",<br>      "Doris原生类型": "bytea",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-float4-0074-5c131f33

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 74，源行 122–122，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('67e14'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('67e14' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0075-caaebf0f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 75，源行 123–123，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('985e15'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('985e15' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0076-17fb2046

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 76，源行 124–124，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('55895e-16'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('55895e-16' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0077-3fbe6777

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 77，源行 125–125，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('7038531e-32'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('7038531e-32' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0078-ee9f57cc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 78，源行 126–126，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('702990899e-20'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('702990899e-20' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0079-56d41e15

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 79，源行 128–128，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('3e-23'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('3e-23' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0080-ff3d84bc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 80，源行 129–129，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('57e18'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('57e18' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0081-3fd9b918

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 81，源行 130–130，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('789e-35'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('789e-35' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0082-dfb57bdf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 82，源行 131–131，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('2539e-18'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('2539e-18' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0083-ee6ca093

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 83，源行 132–132，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('76173e28'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('76173e28' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0084-559dcf23

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 84，源行 133–133，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('887745e-11'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('887745e-11' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0085-f6047f04

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 85，源行 134–134，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('5382571e-37'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('5382571e-37' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0086-727d8ecc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 86，源行 135–135，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('82381273e-35'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('82381273e-35' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0087-95285bae

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 87，源行 136–136，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('750486563e-38'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('750486563e-38' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0088-b066bdff

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 88，源行 138–146，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('1.17549435e-38'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('1.17549435e-38' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-float4-0089-2d9923cc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)；原语句 89，源行 147–147，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT float4send('1.1754944e-38'::float4);
~~~

社区生成 SQL：


~~~sql
SELECT FLOAT4SEND(CAST('1.1754944e-38' AS FLOAT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'\")",
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
| pg-float4-0036-37bab7aa / SELECT 'N A N'::float4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 36 | invalid input syntax for type real: "N A N" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0037-2365fbf0 / SELECT 'NaN x'::float4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 37 | invalid input syntax for type real: "NaN x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0038-5fca1d84 / SELECT ' INFINITY    x'::float4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 38 | invalid input syntax for type real: " INFINITY    x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0062-7542c795 / SELECT '32767.6'::float4::int2; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 62 | smallint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0064-4f61b554 / SELECT '-32768.6'::float4::int2; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 64 | smallint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0066-07fa63e5 / SELECT '2147483647'::float4::int4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 66 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0068-dc44032a / SELECT '-2147483900'::float4::int4; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 68 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0070-512ed2f2 / SELECT '9223372036854775807'::float4::int8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 70 | bigint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-float4-0072-0ae71c32 / SELECT '-9223380000000000000'::float4::int8; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 72 | bigint out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-float4-0031-8c6d7076 | SELECT 'NaN'::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 31 |
| pg-float4-0032-982df9d8 | SELECT 'nan'::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 32 |
| pg-float4-0033-9fb6cf51 | SELECT '   NAN  '::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 33 |
| pg-float4-0034-2e101523 | SELECT 'infinity'::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 34 |
| pg-float4-0035-bd624b7e | SELECT '          -INFINiTY   '::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 35 |
| pg-float4-0039-14d91d69 | SELECT 'Infinity'::float4 + 100.0; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 39 |
| pg-float4-0040-0df8893f | SELECT 'Infinity'::float4 / 'Infinity'::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 40 |
| pg-float4-0042-78e546a5 | SELECT 'nan'::float4 / 'nan'::float4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 42 |
| pg-float4-0061-8dd21096 | SELECT '32767.4'::float4::int2; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 61 |
| pg-float4-0063-8cbd3d41 | SELECT '-32768.4'::float4::int2; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 63 |
| pg-float4-0065-b794ca3a | SELECT '2147483520'::float4::int4; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/float4.out)，语句 65 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

