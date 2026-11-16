# xml：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 70 | 64 | 6 | 0 | 64 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/xml.yaml)；[首轮 Markdown](../../../validation/xml/validation.md) / [首轮 JSON](../../../validation/xml/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-xml-0006-3da45c5b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 6，源行 19–20，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('<value>one</value>', 'xml');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('<value>one</value>', 'xml')
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

### pg-xml-0007-1fc6788e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 7，源行 21–21，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('<value>one</', 'xml');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('<value>one</', 'xml')
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

### pg-xml-0009-73d43442

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 9，源行 23–23，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT pg_input_is_valid('<?xml version="1.0" standalone="y"?><foo/>', 'xml');
~~~

社区生成 SQL：


~~~sql
SELECT PG_INPUT_IS_VALID('<?xml version="1.0" standalone="y"?><foo/>', 'xml')
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

### pg-xml-0011-1b0b43cc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 11，源行 27–27，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlcomment('test');
~~~

社区生成 SQL：


~~~sql
SELECT XMLCOMMENT('test')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0012-d38a2456

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 12，源行 28–28，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlcomment('-test');
~~~

社区生成 SQL：


~~~sql
SELECT XMLCOMMENT('-test')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0015-e02263c2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 15，源行 31–31，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlcomment('te st');
~~~

社区生成 SQL：


~~~sql
SELECT XMLCOMMENT('te st')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0026-0e66108b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 26，源行 54–54，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name element, xmlelement(name nested, 'stuff'));
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME element, XMLELEMENT(NAME nested, 'stuff'))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'element' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'element' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0029-deff914b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 29，源行 60–60，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name num, 37);
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME num, 37)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'num' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'num' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0030-6137a003

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 30，源行 61–61，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, text 'bar');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS STRING))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0031-31a8ba50

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 31，源行 62–62，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, xml 'bar');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS XML))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0032-887a7a59

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 32，源行 63–63，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, text 'b<a/>r');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('b<a/>r' AS STRING))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0033-790e6265

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 33，源行 64–64，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, xml 'b<a/>r');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('b<a/>r' AS XML))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0034-0de0843b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 34，源行 65–65，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, array[1, 2, 3]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT XMLELEMENT(NAME foo, ARRAY(1, 2, 3));
~~~

实际证据：[probe-01 JSON](../evidence/pg-xml-0034-0de0843b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-xml-0034-0de0843b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "xml",<br>      "Doris原生类型": "xml",<br>      "逻辑类型": "信息不足",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| array-null-elements | [源 SQL](../evidence/boundaries/array-null-elements/source.sql) / [候选](../evidence/boundaries/array-null-elements/candidate.sql) | [probe](../evidence/boundaries/array-null-elements/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-empty-typed | [源 SQL](../evidence/boundaries/array-empty-typed/source.sql) / [候选](../evidence/boundaries/array-empty-typed/candidate.sql) | [probe](../evidence/boundaries/array-empty-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-nested-typed | [源 SQL](../evidence/boundaries/array-nested-typed/source.sql) / [候选](../evidence/boundaries/array-nested-typed/candidate.sql) | [probe](../evidence/boundaries/array-nested-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<array<int>>，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为元素列表构造器增加 Doris 实现；静态可知元素类型时保留 PG 的元素位宽。ARRAY(SELECT...) 单独处理，不把查询构造器伪装成元素列表。 限制：_int4 与 array<tinyint> 的实际位宽不同；_int4 与 array<int> 也会被当前类型声明比较器误报。需要区分表示别名与真实类型差异。

修复任务：[PG-DORIS-001](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-xml-0036-a1df635c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 36，源行 67–67，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, bytea 'bar');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS VARBINARY))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0038-a1df635c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 38，源行 69–69，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmlelement(name foo, bytea 'bar');
~~~

社区生成 SQL：


~~~sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS VARBINARY))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0111-42532778

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 111，源行 213–214，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml '<foo>bar</foo>' IS DOCUMENT;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('<foo>bar</foo>' AS XML) IS DOCUMENT
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0112-13862e79

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 112，源行 215–215，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml '<foo>bar</foo><bar>foo</bar>' IS DOCUMENT;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('<foo>bar</foo><bar>foo</bar>' AS XML) IS DOCUMENT
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0113-76dc3083

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 113，源行 216–216，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml '<abc/>' IS NOT DOCUMENT;
~~~

社区生成 SQL：


~~~sql
SELECT NOT CAST('<abc/>' AS XML) IS DOCUMENT
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 28)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 28)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0114-cf2c8a74

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 114，源行 217–217，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml 'abc' IS NOT DOCUMENT;
~~~

社区生成 SQL：


~~~sql
SELECT NOT CAST('abc' AS XML) IS DOCUMENT
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 25)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 25)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0116-06ff7e3d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 116，源行 220–225，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CASE WHEN ('2019-12-16T00:00:00.000'::xml) IS DOCUMENT
    THEN (xpath('/*/text()', '2019-12-16T00:00:00.000'::xml))[1]
    ELSE '2019-12-16T00:00:00.000'::xml
END;
~~~

社区生成 SQL：


~~~sql
SELECT CASE WHEN (CAST('2019-12-16T00:00:00.000' AS XML)) IS DOCUMENT THEN (XPATH('/*/text()', CAST('2019-12-16T00:00:00.000' AS XML)))[0] ELSE CAST('2019-12-16T00:00:00.000' AS XML) END
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'WHEN' expecting {<EOF>, ';'}(line 1, pos 12)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'WHEN' expecting {<EOF>, ';'}(line 1, pos 12)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0151-c5683e82

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 151，源行 279–279，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//text()', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('//text()', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0152-481c458f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 152，源行 280–280，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//loc:piece/@id', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT XPATH('//loc:piece/@id', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY(ARRAY('loc', 'http://127.0.0.1')));
~~~

实际证据：[probe-01 JSON](../evidence/pg-xml-0152-481c458f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-xml-0152-481c458f/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_xml",<br>      "Doris原生类型": "_xml",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| array-null-elements | [源 SQL](../evidence/boundaries/array-null-elements/source.sql) / [候选](../evidence/boundaries/array-null-elements/candidate.sql) | [probe](../evidence/boundaries/array-null-elements/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-empty-typed | [源 SQL](../evidence/boundaries/array-empty-typed/source.sql) / [候选](../evidence/boundaries/array-empty-typed/candidate.sql) | [probe](../evidence/boundaries/array-empty-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-nested-typed | [源 SQL](../evidence/boundaries/array-nested-typed/source.sql) / [候选](../evidence/boundaries/array-nested-typed/candidate.sql) | [probe](../evidence/boundaries/array-nested-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<array<int>>，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为元素列表构造器增加 Doris 实现；静态可知元素类型时保留 PG 的元素位宽。ARRAY(SELECT...) 单独处理，不把查询构造器伪装成元素列表。 限制：_int4 与 array<tinyint> 的实际位宽不同；_int4 与 array<int> 也会被当前类型声明比较器误报。需要区分表示别名与真实类型差异。

修复任务：[PG-DORIS-001](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-xml-0153-4b9bd07b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 153，源行 281–281，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT XPATH('//loc:piece', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY(ARRAY('loc', 'http://127.0.0.1')));
~~~

实际证据：[probe-01 JSON](../evidence/pg-xml-0153-4b9bd07b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-xml-0153-4b9bd07b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_xml",<br>      "Doris原生类型": "_xml",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| array-null-elements | [源 SQL](../evidence/boundaries/array-null-elements/source.sql) / [候选](../evidence/boundaries/array-null-elements/candidate.sql) | [probe](../evidence/boundaries/array-null-elements/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-empty-typed | [源 SQL](../evidence/boundaries/array-empty-typed/source.sql) / [候选](../evidence/boundaries/array-empty-typed/candidate.sql) | [probe](../evidence/boundaries/array-empty-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-nested-typed | [源 SQL](../evidence/boundaries/array-nested-typed/source.sql) / [候选](../evidence/boundaries/array-nested-typed/candidate.sql) | [probe](../evidence/boundaries/array-nested-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<array<int>>，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为元素列表构造器增加 Doris 实现；静态可知元素类型时保留 PG 的元素位宽。ARRAY(SELECT...) 单独处理，不把查询构造器伪装成元素列表。 限制：_int4 与 array<tinyint> 的实际位宽不同；_int4 与 array<int> 也会被当前类型声明比较器误报。需要区分表示别名与真实类型差异。

修复任务：[PG-DORIS-001](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-xml-0154-303139cc

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 154，源行 282–282，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1" xmlns="http://127.0.0.2"><local:piece id="1"><internal>number one</internal><internal2/></local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT XPATH('//loc:piece', '<local:data xmlns:local="http://127.0.0.1" xmlns="http://127.0.0.2"><local:piece id="1"><internal>number one</internal><internal2/></local:piece><local:piece id="2" /></local:data>', ARRAY(ARRAY('loc', 'http://127.0.0.1')));
~~~

实际证据：[probe-01 JSON](../evidence/pg-xml-0154-303139cc/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-xml-0154-303139cc/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_xml",<br>      "Doris原生类型": "_xml",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| array-null-elements | [源 SQL](../evidence/boundaries/array-null-elements/source.sql) / [候选](../evidence/boundaries/array-null-elements/candidate.sql) | [probe](../evidence/boundaries/array-null-elements/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-empty-typed | [源 SQL](../evidence/boundaries/array-empty-typed/source.sql) / [候选](../evidence/boundaries/array-empty-typed/candidate.sql) | [probe](../evidence/boundaries/array-empty-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<int>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| array-nested-typed | [源 SQL](../evidence/boundaries/array-nested-typed/source.sql) / [候选](../evidence/boundaries/array-nested-typed/candidate.sql) | [probe](../evidence/boundaries/array-nested-typed/probe/probe-evidence.json)：值与重复次数=一致；1: _int4 → array<array<int>>，逻辑=一致，声明=不同，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为元素列表构造器增加 Doris 实现；静态可知元素类型时保留 PG 的元素位宽。ARRAY(SELECT...) 单独处理，不把查询构造器伪装成元素列表。 限制：_int4 与 array<tinyint> 的实际位宽不同；_int4 与 array<int> 也会被当前类型声明比较器误报。需要区分表示别名与真实类型差异。

修复任务：[PG-DORIS-001](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-xml-0155-47bed3f8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 155，源行 283–283，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//b', '<a>one <b>two</b> three <b>etc</b></a>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('//b', '<a>one <b>two</b> three <b>etc</b></a>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0156-dd022cbd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 156，源行 284–284，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//text()', '<root>&lt;</root>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('//text()', '<root>&lt;</root>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0157-0ad3cbce

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 157，源行 285–285，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//@value', '<root value="&lt;"/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('//@value', '<root value="&lt;"/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0158-402d1ed5

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 158，源行 286–286，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('''<<invalid>>''', '<root/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('''<<invalid>>''', '<root/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0159-149897d4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 159，源行 287–287，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('count(//*)', '<root><sub/><sub/></root>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('count(//*)', '<root><sub/><sub/></root>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0160-2159d462

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 160，源行 288–288，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('count(//*)=0', '<root><sub/><sub/></root>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('count(//*)=0', '<root><sub/><sub/></root>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0161-6453f40b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 161，源行 289–289，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('count(//*)=3', '<root><sub/><sub/></root>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('count(//*)=3', '<root><sub/><sub/></root>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0162-d898c649

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 162，源行 290–290，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('name(/*)', '<root><sub/><sub/></root>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('name(/*)', '<root><sub/><sub/></root>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0163-dd64e568

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 163，源行 291–291，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('/nosuchtag', '<root/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('/nosuchtag', '<root/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0164-1f7be078

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 164，源行 292–292，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('root', '<root/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('root', '<root/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0165-92b15222

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 165，源行 293–293，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('//namespace::foo', '<root xmlns:foo="http://127.0.0.1"/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('//namespace::foo', '<root xmlns:foo="http://127.0.0.1"/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0170-59f81c22

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 170，源行 333–333，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath_exists('//town[text() = ''Toronto'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml);
~~~

社区生成 SQL：


~~~sql
SELECT XPATH_EXISTS('//town[text() = ''Toronto'']', CAST('<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>' AS XML))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0171-1c60ab2d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 171，源行 334–334，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath_exists('//town[text() = ''Cwmbran'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml);
~~~

社区生成 SQL：


~~~sql
SELECT XPATH_EXISTS('//town[text() = ''Cwmbran'']', CAST('<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>' AS XML))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0172-be98889b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 172，源行 335–335，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath_exists('count(/nosuchtag)', '<root/>'::xml);
~~~

社区生成 SQL：


~~~sql
SELECT XPATH_EXISTS('count(/nosuchtag)', CAST('<root/>' AS XML))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 59)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 59)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0190-155fd751

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 190，源行 358–360，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed_document('<foo>bar</foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED_DOCUMENT('<foo>bar</foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0191-332d1f4a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 191，源行 361–361，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed_document('abc');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED_DOCUMENT('abc')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0192-f6b81b25

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 192，源行 362–362，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed_content('<foo>bar</foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED_CONTENT('<foo>bar</foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0193-2bde595b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 193，源行 363–363，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed_content('abc');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED_CONTENT('abc')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0195-3a732bd3

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 195，源行 366–366，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('abc');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('abc')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT XML_IS_WELL_FORMED('abc');
~~~

实际证据：[probe-01 JSON](../evidence/pg-xml-0195-3a732bd3/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-xml-0195-3a732bd3/probe-01/probe-report.md)。

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
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-xml-0196-f5fdc51b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 196，源行 367–367，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0197-bc3cb386

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 197，源行 368–368，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<abc/>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<abc/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0198-8b081a00

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 198，源行 369–369，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<foo>bar</foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<foo>bar</foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0199-a7caf810

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 199，源行 370–370，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<foo>bar</foo');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<foo>bar</foo')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0200-d01b88ca

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 200，源行 371–371，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<foo><bar>baz</foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<foo><bar>baz</foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0201-1f4ac082

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 201，源行 372–372，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0202-7aea02b8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 202，源行 373–373，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0203-53b2f485

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 203，源行 374–374，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0204-a7526694

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 204，源行 375–375，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<invalidentity>&</abc>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<invalidentity>&</abc>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0205-cccedf72

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 205，源行 376–376，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<undefinedentity>&idontexist;</abc>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<undefinedentity>&idontexist;</abc>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0206-2fef6086

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 206，源行 377–377，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<invalidns xmlns=''&lt;''/>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<invalidns xmlns=''&lt;''/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0207-43d3734b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 207，源行 378–378，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<relativens xmlns=''relative''/>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<relativens xmlns=''relative''/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0208-4135f1c1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 208，源行 379–379，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('<twoerrors>&idontexist;</unbalanced>');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('<twoerrors>&idontexist;</unbalanced>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0210-3a732bd3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 210，源行 382–382，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xml_is_well_formed('abc');
~~~

社区生成 SQL：


~~~sql
SELECT XML_IS_WELL_FORMED('abc')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0213-64278f8c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 213，源行 401–403，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xpath('/*', '<relativens xmlns=''relative''/>');
~~~

社区生成 SQL：


~~~sql
SELECT XPATH('/*', '<relativens xmlns=''relative''/>')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XPATH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0268-7122cca4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 268，源行 721–721，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext(NULL);
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT(NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLTEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0269-0012adb9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 269，源行 722–722，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext('');
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT('')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLTEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0270-4b4238b0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 270，源行 723–723，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext('  ');
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT('  ')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLTEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0271-bdcdcd13

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 271，源行 724–724，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext('foo `$_-+?=*^%!|/\()[]{}');
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT('foo `$_-+?=*^%!|/\\()[]{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLTEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0272-ccdf0a7b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 272，源行 725–725，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext('foo & <"bar">');
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT('foo & <"bar">')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'XMLTEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-xml-0273-2d89ec89

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)；原语句 273，源行 726–726，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT xmltext('x'|| '<P>73</P>'::xml || .42 || true || 'j'::char);
~~~

社区生成 SQL：


~~~sql
SELECT XMLTEXT(CONCAT('x', CAST('<P>73</P>' AS XML), 0.42, TRUE, CAST('j' AS CHAR)))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 47)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 47)\\n\")",
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
| pg-xml-0013-4d04eeb1 / SELECT xmlcomment('test-'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 13 | invalid XML comment | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-xml-0014-c8ea170b / SELECT xmlcomment('--test'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 14 | invalid XML comment | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-xml-0115-bdd66802 / SELECT '<>' IS NOT DOCUMENT; / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 115 | invalid XML content | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS DOCUMENT'(line 1, pos 19)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-xml-0150-2c905588 / SELECT xpath('', '<!-- error -->'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 150 | empty XPath expression | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-xml-0211-7470af89 / SELECT xpath('/*', '<invalidns xmlns=''&lt;''/>'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 211 | could not parse XML document | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-xml-0212-a9816d95 / SELECT xpath('/*', '<nosuchprefix:tag/>'); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/xml.out)，语句 212 | could not parse XML document | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 97 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 5 | 10–17 | error | Invalid expression / Unexpected token. Line 1, Col: 47.<br>  SELECT count(*) = 0 AS skip_test FROM xmltest [4m\[0mgset<br>-- pg_regress psql command omitted<br>-- pg_regress psql command omitted<br>-- pg_regress psql comman |
| 43 | 77–77 | error | Expecting ). Line 1, Col: 26.<br>  SELECT xmlparse(content [4m''[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 26.<br>  SELECT xmlparse(content [4m''[0m); |
| 44 | 78–78 | error | Expecting ). Line 1, Col: 28.<br>  SELECT xmlparse(content [4m'  '[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 28.<br>  SELECT xmlparse(content [4m'  '[0m); |
| 45 | 79–79 | error | Expecting ). Line 1, Col: 29.<br>  SELECT xmlparse(content [4m'abc'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 29.<br>  SELECT xmlparse(content [4m'abc'[0m); |
| 46 | 80–80 | error | Expecting ). Line 1, Col: 38.<br>  SELECT xmlparse(content [4m'<abc>x</abc>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 38.<br>  SELECT xmlparse(content [4m'<abc>x</abc>'[0m); |
| 47 | 81–81 | error | Expecting ). Line 1, Col: 58.<br>  SELECT xmlparse(content [4m'<invalidentity>&</invalidentity>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT xmlparse(content [4m'<invalidentity>&</invalidentity>'[0m); |
| 48 | 82–82 | error | Expecting ). Line 1, Col: 73.<br>  SELECT xmlparse(content [4m'<undefinedentity>&idontexist;</undefinedentity>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 73.<br>  SELECT xmlparse(content [4m'<undefinedentity>&idontexist;</undefinedentity>'[0m); |
| 49 | 83–83 | error | Expecting ). Line 1, Col: 53.<br>  SELECT xmlparse(content [4m'<invalidns xmlns=''&lt;''/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 53.<br>  SELECT xmlparse(content [4m'<invalidns xmlns=''&lt;''/>'[0m); |
| 50 | 84–84 | error | Expecting ). Line 1, Col: 58.<br>  SELECT xmlparse(content [4m'<relativens xmlns=''relative''/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT xmlparse(content [4m'<relativens xmlns=''relative''/>'[0m); |
| 51 | 85–85 | error | Expecting ). Line 1, Col: 64.<br>  SELECT xmlparse(content [4m'<twoerrors>&idontexist;</unbalanced>  '[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 64.<br>  SELECT xmlparse(content [4m'<twoerrors>&idontexist;</unbalanced>  '[0m); |
| 52 | 86–86 | error | Expecting ). Line 1, Col: 45.<br>  SELECT xmlparse(content [4m'<nosuchprefix:tag/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT xmlparse(content [4m'<nosuchprefix:tag/>'[0m); |
| 53 | 88–88 | error | Expecting ). Line 1, Col: 28.<br>  SELECT xmlparse(document [4m'!'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 28.<br>  SELECT xmlparse(document [4m'!'[0m); |
| 54 | 89–89 | error | Expecting ). Line 1, Col: 30.<br>  SELECT xmlparse(document [4m'abc'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 30.<br>  SELECT xmlparse(document [4m'abc'[0m); |
| 55 | 90–90 | error | Expecting ). Line 1, Col: 39.<br>  SELECT xmlparse(document [4m'<abc>x</abc>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 39.<br>  SELECT xmlparse(document [4m'<abc>x</abc>'[0m); |
| 56 | 91–91 | error | Expecting ). Line 1, Col: 51.<br>  SELECT xmlparse(document [4m'<invalidentity>&</abc>  '[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 51.<br>  SELECT xmlparse(document [4m'<invalidentity>&</abc>  '[0m); |
| 57 | 92–92 | error | Expecting ). Line 1, Col: 64.<br>  SELECT xmlparse(document [4m'<undefinedentity>&idontexist;</abc>  '[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 64.<br>  SELECT xmlparse(document [4m'<undefinedentity>&idontexist;</abc>  '[0m); |
| 58 | 93–93 | error | Expecting ). Line 1, Col: 54.<br>  SELECT xmlparse(document [4m'<invalidns xmlns=''&lt;''/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 54.<br>  SELECT xmlparse(document [4m'<invalidns xmlns=''&lt;''/>'[0m); |
| 59 | 94–94 | error | Expecting ). Line 1, Col: 59.<br>  SELECT xmlparse(document [4m'<relativens xmlns=''relative''/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 59.<br>  SELECT xmlparse(document [4m'<relativens xmlns=''relative''/>'[0m); |
| 60 | 95–95 | error | Expecting ). Line 1, Col: 65.<br>  SELECT xmlparse(document [4m'<twoerrors>&idontexist;</unbalanced>  '[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 65.<br>  SELECT xmlparse(document [4m'<twoerrors>&idontexist;</unbalanced>  '[0m); |
| 61 | 96–96 | error | Expecting ). Line 1, Col: 46.<br>  SELECT xmlparse(document [4m'<nosuchprefix:tag/>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 46.<br>  SELECT xmlparse(document [4m'<nosuchprefix:tag/>'[0m); |
| 62 | 99–99 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mfoo[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 22.<br>  SELECT xmlpi(name foo[4m)[0m; |
| 63 | 100–100 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mxml[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 22.<br>  SELECT xmlpi(name xml[4m)[0m; |
| 64 | 101–101 | error | Expecting ). Line 1, Col: 26.<br>  SELECT xmlpi(name [4mxmlstuff[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 27.<br>  SELECT xmlpi(name xmlstuff[4m)[0m; |
| 65 | 102–102 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mfoo[0m, 'bar');<br><br>Invalid expression / Unexpected token. Line 1, Col: 29.<br>  SELECT xmlpi(name foo, 'bar'[4m)[0m; |
| 66 | 103–103 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mfoo[0m, 'in?>valid');<br><br>Invalid expression / Unexpected token. Line 1, Col: 35.<br>  SELECT xmlpi(name foo, 'in?>valid'[4m)[0m; |
| 67 | 104–104 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mfoo[0m, null);<br><br>Invalid expression / Unexpected token. Line 1, Col: 28.<br>  SELECT xmlpi(name foo, null[4m)[0m; |
| 68 | 105–105 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mxml[0m, null);<br><br>Invalid expression / Unexpected token. Line 1, Col: 28.<br>  SELECT xmlpi(name xml, null[4m)[0m; |
| 69 | 106–106 | error | Expecting ). Line 1, Col: 26.<br>  SELECT xmlpi(name [4mxmlstuff[0m, null);<br><br>Invalid expression / Unexpected token. Line 1, Col: 33.<br>  SELECT xmlpi(name xmlstuff, null[4m)[0m; |
| 70 | 107–107 | error | Expecting ). Line 1, Col: 34.<br>  SELECT xmlpi(name [4m"xml-stylesheet"[0m, 'href="mystyle.css" type="text/css"');<br><br>Invalid expression / Unexpected token. Line 1, Col: 73.<br>  SELECT xmlpi(name "xml-stylesheet", 'href="mystyle.css" type="text/css"'[4m)[0m; |
| 71 | 108–108 | error | Expecting ). Line 1, Col: 21.<br>  SELECT xmlpi(name [4mfoo[0m, '   bar');<br><br>Invalid expression / Unexpected token. Line 1, Col: 32.<br>  SELECT xmlpi(name foo, '   bar'[4m)[0m; |
| 72 | 111–111 | error | Expecting ). Line 1, Col: 39.<br>  SELECT xmlroot(xml '<foo/>', version [4mno[0m value, standalone no value);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT xmlroot(xml '<foo/>', version no [4mvalue[0m, standalone no value); |
| 73 | 112–112 | error | Expecting ). Line 1, Col: 42.<br>  SELECT xmlroot(xml '<foo/>', version [4m'2.0'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 42.<br>  SELECT xmlroot(xml '<foo/>', version [4m'2.0'[0m); |
| 74 | 113–113 | error | Expecting ). Line 1, Col: 39.<br>  SELECT xmlroot(xml '<foo/>', version [4mno[0m value, standalone yes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 45.<br>  SELECT xmlroot(xml '<foo/>', version no [4mvalue[0m, standalone yes); |
| 75 | 114–114 | error | Expecting ). Line 1, Col: 60.<br>  SELECT xmlroot(xml '<?xml version="1.1"?><foo/>', version [4mno[0m value, standalone yes);<br><br>Invalid expression / Unexpected token. Line 1, Col: 66.<br>  SELECT xmlroot(xml '<?xml version="1.1"?><foo/>', version no [4mvalue[0m, standalone yes); |
| 76 | 115–115 | error | Expecting ). Line 1, Col: 50.<br>  SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no);<br><br>Expecting ). Line 1, Col: 50.<br>  SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no);<br><br>Invalid expression / Unexpected token. Line 1, Col: 50.<br>  SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no); |
| 77 | 116–116 | error | Expecting ). Line 1, Col: 73.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value, standalone no);<br><br>Invalid expression / Unexpected token. Line 1, Col: 79.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m, standalone no); |
| 78 | 117–117 | error | Expecting ). Line 1, Col: 73.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value, standalone no value);<br><br>Invalid expression / Unexpected token. Line 1, Col: 79.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m, standalone no value); |
| 79 | 118–118 | error | Expecting ). Line 1, Col: 73.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value);<br><br>Invalid expression / Unexpected token. Line 1, Col: 79.<br>  SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m); |
| 80 | 121–135 | error | Expecting ). Line 13, Col: 15.<br>  S name,<br>      1 + 1 AS num<br>    ),<br>    xmlelement (<br>      NAME qux,<br>      'foo'<br>    )<br>  ),<br>  version [4m'1.0'[0m,<br>  standalone yes<br>);<br><br>Invalid expression / Unexpected token. Line 13, Col: 15.<br>  S name,<br>      1 + 1 AS num<br>    ),<br>    xmlelement (<br>      NAME qux,<br>      'foo'<br>    )<br>  ),<br>  version [4m'1.0'[0m,<br>  standalone yes<br>); |
| 81 | 138–138 | error | Expecting ). Line 1, Col: 32.<br>  SELECT xmlserialize(content [4mdata[0m as character varying(20)) FROM xmltest;<br><br>Invalid expression / Unexpected token. Line 1, Col: 35.<br>  SELECT xmlserialize(content data [4mas[0m character varying(20)) FROM xmltest; |
| 82 | 139–139 | error | Expecting ). Line 1, Col: 34.<br>  SELECT xmlserialize(content [4m'good'[0m as char(10));<br><br>Invalid expression / Unexpected token. Line 1, Col: 34.<br>  SELECT xmlserialize(content [4m'good'[0m as char(10)); |
| 83 | 140–140 | error | Expecting ). Line 1, Col: 34.<br>  SELECT xmlserialize(document [4m'bad'[0m as text);<br><br>Invalid expression / Unexpected token. Line 1, Col: 34.<br>  SELECT xmlserialize(document [4m'bad'[0m as text); |
| 84 | 142–143 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT); |
| 85 | 144–144 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT); |
| 86 | 145–146 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT); |
| 87 | 147–147 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT); |
| 88 | 148–149 | error | Expecting ). Line 1, Col: 74.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 74.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 89 | 150–150 | error | Expecting ). Line 1, Col: 74.<br>  SELECT xmlserialize(CONTENT  [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 74.<br>  SELECT xmlserialize(CONTENT  [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 90 | 151–152 | error | Expecting ). Line 1, Col: 92.<br>  SELECT xmlserialize(DOCUMENT [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 92.<br>  SELECT xmlserialize(DOCUMENT [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 91 | 153–153 | error | Expecting ). Line 1, Col: 92.<br>  SELECT xmlserialize(CONTENT  [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 92.<br>  SELECT xmlserialize(CONTENT  [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 92 | 154–155 | error | Expecting ). Line 1, Col: 111.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 111.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT); |
| 93 | 156–156 | error | Expecting ). Line 1, Col: 111.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 111.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT); |
| 94 | 157–158 | error | Expecting ). Line 1, Col: 31.<br>  SELECT xmlserialize(DOCUMENT [4m''[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 31.<br>  SELECT xmlserialize(DOCUMENT [4m''[0m AS text INDENT); |
| 95 | 159–159 | error | Expecting ). Line 1, Col: 31.<br>  SELECT xmlserialize(CONTENT  [4m''[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 31.<br>  SELECT xmlserialize(CONTENT  [4m''[0m AS text INDENT); |
| 96 | 160–161 | error | Expecting ). Line 1, Col: 33.<br>  SELECT xmlserialize(DOCUMENT [4m'  '[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 33.<br>  SELECT xmlserialize(DOCUMENT [4m'  '[0m AS text INDENT); |
| 97 | 162–162 | error | Expecting ). Line 1, Col: 33.<br>  SELECT xmlserialize(CONTENT  [4m'  '[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 33.<br>  SELECT xmlserialize(CONTENT  [4m'  '[0m AS text INDENT); |
| 98 | 163–164 | error | Expecting ). Line 1, Col: 33.<br>  SELECT xmlserialize(DOCUMENT [4mNULL[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT xmlserialize(DOCUMENT NULL [4mAS[0m text INDENT); |
| 99 | 165–165 | error | Expecting ). Line 1, Col: 33.<br>  SELECT xmlserialize(CONTENT  [4mNULL[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 36.<br>  SELECT xmlserialize(CONTENT  NULL [4mAS[0m text INDENT); |
| 100 | 166–167 | error | Expecting ). Line 1, Col: 104.<br>  SELECT xmlserialize(DOCUMENT [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 104.<br>  SELECT xmlserialize(DOCUMENT [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT); |
| 101 | 168–168 | error | Expecting ). Line 1, Col: 104.<br>  SELECT xmlserialize(CONTENT  [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 104.<br>  SELECT xmlserialize(CONTENT  [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT); |
| 102 | 169–170 | error | Expecting ). Line 1, Col: 47.<br>  SELECT xmlserialize(DOCUMENT [4m'<!DOCTYPE a><a/>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 47.<br>  SELECT xmlserialize(DOCUMENT [4m'<!DOCTYPE a><a/>'[0m AS text INDENT); |
| 103 | 171–171 | error | Expecting ). Line 1, Col: 47.<br>  SELECT xmlserialize(CONTENT  [4m'<!DOCTYPE a><a/>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 47.<br>  SELECT xmlserialize(CONTENT  [4m'<!DOCTYPE a><a/>'[0m AS text INDENT); |
| 104 | 172–173 | error | Expecting ). Line 1, Col: 53.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 53.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar></bar></foo>'[0m AS text INDENT); |
| 105 | 174–174 | error | Expecting ). Line 1, Col: 53.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar></bar></foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 53.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar></bar></foo>'[0m AS text INDENT); |
| 106 | 175–176 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(DOCUMENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(DOCUMENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT); |
| 107 | 177–177 | error | Expecting ). Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(CONTENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 72.<br>  SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(CONTENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT); |
| 108 | 178–179 | error | Expecting ). Line 1, Col: 60.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo>   <bar></bar>    </foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 60.<br>  SELECT xmlserialize(DOCUMENT [4m'<foo>   <bar></bar>    </foo>'[0m AS text INDENT); |
| 109 | 180–180 | error | Expecting ). Line 1, Col: 69.<br>  SELECT xmlserialize(CONTENT  [4m'text node<foo>    <bar></bar>   </foo>'[0m AS text INDENT);<br><br>Invalid expression / Unexpected token. Line 1, Col: 69.<br>  SELECT xmlserialize(CONTENT  [4m'text node<foo>    <bar></bar>   </foo>'[0m AS text INDENT); |
| 110 | 182–211 | error | Expected one read-only Query, got Command |
| 120 | 233–235 | error | Expecting ). Line 1, Col: 39.<br>  SELECT xmlpi(name [4m":::_xml_abc135.%-&_"[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 40.<br>  SELECT xmlpi(name ":::_xml_abc135.%-&_"[4m)[0m; |
| 121 | 236–236 | error | Expecting ). Line 1, Col: 23.<br>  SELECT xmlpi(name [4m"123"[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 24.<br>  SELECT xmlpi(name "123"[4m)[0m; |
| 122 | 239–239 | error | Expected one read-only Query, got Command |
| 124 | 242–242 | error | Expected one read-only Query, got Command |
| 125 | 243–243 | error | Expected one read-only Query, got Command |
| 128 | 247–247 | error | Expected one read-only Query, got Command |
| 129 | 248–248 | error | Expected one read-only Query, got Command |
| 166 | 295–327 | error | Expected one read-only Query, got Command |
| 167 | 329–330 | error | Expecting ). Line 1, Col: 55.<br>  SELECT xmlexists('//town[text() = ''Toronto'']' [4mPASSING[0m BY REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>');<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT xmlexists('//town[text() = ''Toronto'']' PASSING [4mBY[0m REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'); |
| 168 | 331–331 | error | Expecting ). Line 1, Col: 55.<br>  SELECT xmlexists('//town[text() = ''Cwmbran'']' [4mPASSING[0m BY REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>');<br><br>Invalid expression / Unexpected token. Line 1, Col: 58.<br>  SELECT xmlexists('//town[text() = ''Cwmbran'']' PASSING [4mBY[0m REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'); |
| 169 | 332–332 | error | Expecting ). Line 1, Col: 44.<br>  SELECT xmlexists('count(/nosuchtag)' [4mPASSING[0m BY REF '<root/>');<br><br>Invalid expression / Unexpected token. Line 1, Col: 47.<br>  SELECT xmlexists('count(/nosuchtag)' PASSING [4mBY[0m REF '<root/>'); |
| 177 | 342–342 | error | Expecting ). Line 1, Col: 66.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m data);<br><br>Invalid expression / Unexpected token. Line 1, Col: 66.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m data); |
| 178 | 343–343 | error | Expecting ). Line 1, Col: 66.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m BY REF data BY REF);<br><br>Invalid expression / Unexpected token. Line 1, Col: 66.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m BY REF data BY REF); |
| 179 | 344–344 | error | Expecting ). Line 1, Col: 67.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers' [4mPASSING[0m BY REF data);<br><br>Invalid expression / Unexpected token. Line 1, Col: 67.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers' [4mPASSING[0m BY REF data); |
| 180 | 345–345 | error | Expecting ). Line 1, Col: 93.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers/name[text() = ''Molson'']' [4mPASSING[0m BY REF data);<br><br>Invalid expression / Unexpected token. Line 1, Col: 93.<br>  SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers/name[text() = ''Molson'']' [4mPASSING[0m BY REF data); |
| 189 | 356–356 | error | Expecting ). Line 1, Col: 65.<br>  SELECT COUNT(id) FROM xmltest, query WHERE xmlexists(expr [4mPASSING[0m BY REF data);<br><br>Invalid expression / Unexpected token. Line 1, Col: 65.<br>  SELECT COUNT(id) FROM xmltest, query WHERE xmlexists(expr [4mPASSING[0m BY REF data); |
| 214 | 405–406 | error | Expecting ). Line 1, Col: 90.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/passwd">]><foo>&c;</foo>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 90.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/passwd">]><foo>&c;</foo>'[0m); |
| 215 | 407–407 | error | Expecting ). Line 1, Col: 96.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/no.such.file">]><foo>&c;</foo>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 96.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/no.such.file">]><foo>&c;</foo>'[0m); |
| 216 | 408–409 | error | Expecting ). Line 1, Col: 175.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"><chapter>&nbsp;</chapter>'[0m);<br><br>Invalid expression / Unexpected token. Line 1, Col: 175.<br>  SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"><chapter>&nbsp;</chapter>'[0m); |
| 224 | 480–481 | error | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 27.<br>  SELECT * FROM XMLTABLE ([4mROW[0m () PASSING null COLUMNS v1 timestamp) AS f (v1, v2);<br><br>Invalid expression / Unexpected token. Line 1, Col: 29.<br>  SELECT * FROM XMLTABLE (ROW [4m([0m) PASSING null COLUMNS v1 timestamp) AS f (v1, v2); |
| 225 | 483–483 | error | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 27.<br>  SELECT * FROM XMLTABLE ([4mROW[0m () PASSING null COLUMNS v1 timestamp __pg__is_not_null 1) AS f (v1);<br><br>Invalid expression / Unexpected token. Line 1, Col: 29.<br>  SELECT * FROM XMLTABLE (ROW [4m([0m) PASSING null COLUMNS v1 timestamp __pg__is_not_null 1) AS f (v1); |
| 231 | 509–522 | error | Expected one read-only Query, got Command |
| 232 | 524–524 | error | Expected one read-only Query, got Command |
| 255 | 655–677 | error | Required keyword: 'expressions' missing for <class 'sqlglot.expressions.core.Bracket'>. Line 4, Col: 84.<br>   as proargnames,<br>                case when proargtypes <> '' then array_to_string(proargtypes::oid[][4m,[0m',') end as proargtypes<br>           FROM pg_proc WHERE proname = 'f_leak'),<br>   y AS (SELECT xmlelemen |
| 256 | 679–700 | error | Required keyword: 'expressions' missing for <class 'sqlglot.expressions.core.Bracket'>. Line 4, Col: 84.<br>   as proargnames,<br>                case when proargtypes <> '' then array_to_string(proargtypes::oid[][4m,[0m',') end as proargtypes<br>           FROM pg_proc),<br>   y AS (SELECT xmlelement(name data,<br>             |
| 262 | 709–709 | error | Invalid expression / Unexpected token. Line 1, Col: 91.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable('/d/r' PASSING x COLUMNS a int PATH '' [4m\|\|[0m lower(_path) \|\| 'c'); |
| 263 | 710–710 | error | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 51.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable([4m([0m'/d/r/' \|\| lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.');<br><br>Expecting ). Line 1, Col: 61.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.');<br><br>Invalid expression / Unexpected token. Line 1, Col: 61.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.'); |
| 264 | 711–711 | error | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 51.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable([4m([0m'/d/r/' \|\| lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54);<br><br>Expecting ). Line 1, Col: 61.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54);<br><br>Invalid expression / Unexpected token. Line 1, Col: 61.<br>  SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54); |


