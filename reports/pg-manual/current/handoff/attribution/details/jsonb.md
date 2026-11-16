# jsonb：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 90 | 85 | 5 | 4 | 81 |


[YAML](../../../../../../cases/postgres/manual/current/jsonb.yaml)；[首轮 Markdown](../../../validation/jsonb/validation.md) / [首轮 JSON](../../../validation/jsonb/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-jsonb-0057-0dd4ec19

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 57，源行 95–96，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json(ARRAY [jsonb '{"a":1}', jsonb '{"b":[2,3]}']);
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
SELECT ARRAY_TO_JSON(ARRAY(CAST('{"a":1}' AS JSONB), CAST('{"b":[2,3]}' AS JSONB)));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0057-0dd4ec19/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0057-0dd4ec19/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = array does not support jsonb/variant type')"
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

### pg-jsonb-0061-59e84f7a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 61，源行 112–114，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(timestamp '2014-05-28 12:22:35.614298');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('2014-05-28 12:22:35.614298' AS DATETIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0068-24547f30

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 68，源行 123–123，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(date '2014-05-28');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('2014-05-28' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0069-7d87d71e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 69，源行 125–125，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(date 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('Infinity' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0070-319ea39f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 70，源行 126–126，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(date '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('-Infinity' AS DATE))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0071-c8f77fd2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 71，源行 127–127，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(timestamp 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('Infinity' AS DATETIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0072-4dc6e784

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 72，源行 128–128，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(timestamp '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('-Infinity' AS DATETIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0073-1c627585

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 73，源行 129–129，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(timestamptz 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('Infinity' AS DATETIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0074-02cab6be

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 74，源行 130–130，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_jsonb(timestamptz '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSONB(CAST('-Infinity' AS DATETIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'TO_JSONB'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'TO_JSONB'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0075-27aae931

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 75，源行 132–139，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_agg(q)
  FROM ( SELECT $$a$$ || x AS b, y AS c,
               ARRAY[ROW(x.*,ARRAY[1,2,3]),
               ROW(y.*,ARRAY[4,5,6])] AS z
         FROM generate_series(1,2) x,
              generate_series(4,5) y) q;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）；[sqlglot/generators/doris.py:26](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L26)（行 26）。

第一次候选：


~~~sql
SELECT JSONB_AGG(q) FROM (SELECT CONCAT('a', x) AS b, y AS c, ARRAY(ROW(x.*, ARRAY(1, 2, 3)), ROW(y.*, ARRAY(4, 5, 6))) AS z FROM GENERATE_SERIES(1, 2) AS x, GENERATE_SERIES(4, 5) AS y) AS q;
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0075-27aae931/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0075-27aae931/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "jsonb",<br>      "Doris原生类型": "jsonb",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 68)\\n\")"
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

### pg-jsonb-0112-a9632d75

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 112，源行 201–201，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[{"b": "c"}, {"b": "cc"}]'::jsonb -> 1;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f09349e33be7894bd8d5a303da628698e0aaae728156824b39ea48b915299a13",
    "doris_digest=f43465d9bf5efce6d59890b33766f59b61d54ded98b2eac04bf3e3bc657c8b6e",
    "source_sample=[['{\"b\": \"cc\"}']]",
    "doris_sample=[['{\"b\":\"cc\"}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0124-ce70ecc5

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 124，源行 214–214，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[{"b": "c"}, {"b": "cc"}]'::jsonb ->> 1;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f09349e33be7894bd8d5a303da628698e0aaae728156824b39ea48b915299a13",
    "doris_digest=f43465d9bf5efce6d59890b33766f59b61d54ded98b2eac04bf3e3bc657c8b6e",
    "source_sample=[['{\"b\": \"cc\"}']]",
    "doris_sample=[['{\"b\":\"cc\"}']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L75)（行 75）；[sqlglot/parsers/postgres.py:151](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/parsers/postgres.py#L151)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]'), NULL, JSON_EXTRACT_STRING(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSONB), '$[1]'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0124-ce70ecc5/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0124-ce70ecc5/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: text → json，逻辑=不同，声明=不同，精度/小数位=不适用 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0131-2a035c9d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 131，源行 222–223，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"x":"y"}'::jsonb = '{"x":"y"}'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"x":"y"}' AS JSONB) = CAST('{"x":"y"}' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"x":"y"}\' as JSON) = cast(\'{"x":"y"}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"x\":\"y\"}\\' as JSON) = cast(\\'{\"x\":\"y\"}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0132-18f40d74

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 132，源行 224–224，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"x":"y"}'::jsonb = '{"x":"z"}'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"x":"y"}' AS JSONB) = CAST('{"x":"z"}' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"x":"y"}\' as JSON) = cast(\'{"x":"z"}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"x\":\"y\"}\\' as JSON) = cast(\\'{\"x\":\"z\"}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0133-c0125259

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 133，源行 226–226，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"x":"y"}'::jsonb <> '{"x":"y"}'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"x":"y"}' AS JSONB) <> CAST('{"x":"y"}' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"x":"y"}\' as JSON) = cast(\'{"x":"y"}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"x\":\"y\"}\\' as JSON) = cast(\\'{\"x\":\"y\"}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0134-ab0b7f6c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 134，源行 227–227，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"x":"y"}'::jsonb <> '{"x":"z"}'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"x":"y"}' AS JSONB) <> CAST('{"x":"z"}' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"x":"y"}\' as JSON) = cast(\'{"x":"z"}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"x\":\"y\"}\\' as JSON) = cast(\\'{\"x\":\"z\"}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0135-6b4dd957

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 135，源行 229–230，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"b"}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0135-6b4dd957/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0135-6b4dd957/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0136-4e07d50c

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 136，源行 231–231，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"b", "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b", "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b", "c":null}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0136-4e07d50c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0136-4e07d50c/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0137-26e8e6c3

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 137，源行 232–232，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"b", "g":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b", "g":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b", "g":null}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0137-26e8e6c3/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0137-26e8e6c3/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0138-0f3fc6a3

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 138，源行 233–233，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"g":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"g":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"g":null}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0138-0f3fc6a3/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0138-0f3fc6a3/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0139-c3fabcbb

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 139，源行 234–234，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"c"}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"c"}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"c"}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0139-c3fabcbb/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0139-c3fabcbb/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0140-6b4dd957

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 140，源行 235–235，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contains('{"a":"b", "b":1, "c":null}', '{"a":"b"}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-006 补充 JSONB_CONTAINS 的 Doris 映射并区分 JSON 与数组算子：JSONB_CONTAINS 原样输出没有对应 Doris 函数；JSON_CONTAINS 加布尔类型对齐的候选已执行。PG @> 还可能解析成 ArrayContainsAll，不能仅按操作符全局替换。

代码位置：[sqlglot/expressions/json.py:49](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/expressions/json.py#L49)（行 49）；[sqlglot/generators/doris.py:57](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/doris.py#L57)（行 57）；[sqlglot/generators/mysql.py:654](https://github.com/tobymao/sqlglot/blob/feb0e08aba28a29590596bb3f5761fbaeb0e98b9/sqlglot/generators/mysql.py#L654)（行 654）。

第一次候选：


~~~sql
SELECT CAST(JSON_CONTAINS('{"a":"b", "b":1, "c":null}', '{"a":"b"}') AS BOOLEAN);
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0140-6b4dd957/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0140-6b4dd957/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINS'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-containment-null | [源 SQL](../evidence/boundaries/json-containment-null/source.sql) / [候选](../evidence/boundaries/json-containment-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-array-duplicates | [源 SQL](../evidence/boundaries/json-containment-array-duplicates/source.sql) / [候选](../evidence/boundaries/json-containment-array-duplicates/candidate.sql) | [probe](../evidence/boundaries/json-containment-array-duplicates/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-containment-sql-null | [源 SQL](../evidence/boundaries/json-containment-sql-null/source.sql) / [候选](../evidence/boundaries/json-containment-sql-null/candidate.sql) | [probe](../evidence/boundaries/json-containment-sql-null/probe/probe-evidence.json)：值与重复次数=一致；1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

先处理已识别 JSONBContains AST；对 @>/<@ 仅在 JSON 类型已知时采用 JSON 规则，保留数组的不同语义。 限制：当前六条函数样本和有限边界不证明全部 PG JSONB 包含规则。

修复任务：[PG-DORIS-006](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-jsonb-0142-f3ac9275

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 142，源行 237–237，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"a":"b"}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"a":"b"}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0143-0ed4934b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 143，源行 238–238，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"a":"b", "c":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"a":"b", "c":null}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0144-fab22f38

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 144，源行 239–239，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"a":"b", "g":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"a":"b", "g":null}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0145-298e5f00

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 145，源行 240–240，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"g":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"g":null}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0146-2a40e047

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 146，源行 241–241，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"a":"c"}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"a":"c"}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0147-f3ac9275

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 147，源行 242–242，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "b":1, "c":null}'::jsonb @> '{"a":"b"}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "b":1, "c":null}' AS JSONB) @> '{"a":"b"}'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '@' expecting {<EOF>, ';'}(line 1, pos 51)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0152-0b2c1dd6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 152，源行 248–248，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '[1,2,2]'::jsonb <@ '[1,2]'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('[1,2,2]' AS JSONB) <@ CAST('[1,2]' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 39)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 39)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0153-6253161a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 153，源行 249–249，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '[1,2,2]'::jsonb <@ '[1,1,2]'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('[1,2,2]' AS JSONB) <@ CAST('[1,1,2]' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 39)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 39)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0154-7aebce24

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 154，源行 250–250，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '[[1,2,2]]'::jsonb <@ '[[1,2]]'::jsonb;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('[[1,2,2]]' AS JSONB) <@ CAST('[[1,2]]' AS JSONB)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 41)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 41)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0155-b3452c40

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 155，源行 252–252，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"a":"b"}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"a":"b"}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0156-6e1e386c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 156，源行 253–253，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"a":"b", "c":null}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"a":"b", "c":null}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0157-89fcccc3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 157，源行 254–254，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"a":"b", "g":null}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"a":"b", "g":null}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0158-afdd0d3f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 158，源行 255–255，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"g":null}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"g":null}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0159-f7f432b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 159，源行 256–256，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"a":"c"}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"a":"c"}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0160-b3452c40

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 160，源行 257–257，同文回显第 2 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_contained('{"a":"b"}', '{"a":"b", "b":1, "c":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_CONTAINED('{"a":"b"}', '{"a":"b", "b":1, "c":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_CONTAINED'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0162-298a8e02

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 162，源行 259–259，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b"}'::jsonb <@ '{"a":"b", "b":1, "c":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b"}' AS JSONB) <@ '{"a":"b", "b":1, "c":null}'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"a":"b"}\' as JSON) < @\'{"a":"b", "b":1, "c":null}\')')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"a\":\"b\"}\\' as JSON) < @\\'{\"a\":\"b\", \"b\":1, \"c\":null}\\')')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0163-62653dc7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 163，源行 260–260，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "c":null}'::jsonb <@ '{"a":"b", "b":1, "c":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "c":null}' AS JSONB) <@ '{"a":"b", "b":1, "c":null}'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"a":"b", "c":null}\' as JSON) < @\'{"a":"b", "b":1, "c":null}\')')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"a\":\"b\", \"c\":null}\\' as JSON) < @\\'{\"a\":\"b\", \"b\":1, \"c\":null}\\')')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0164-2311d37d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 164，源行 261–261，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{"a":"b", "g":null}'::jsonb <@ '{"a":"b", "b":1, "c":null}';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"b", "g":null}' AS JSONB) <@ '{"a":"b", "b":1, "c":null}'
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\'{"a":"b", "g":null}\' as JSON) < @\'{"a":"b", "b":1, "c":null}\')')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = comparison predicate could not contains json type: (cast(\\'{\"a\":\"b\", \"g\":null}\\' as JSON) < @\\'{\"a\":\"b\", \"b\":1, \"c\":null}\\')')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0176-305ab79b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 176，源行 278–279，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_ARRAY_LENGTH('[1,2,3,{"f1":1,"f2":[5,6]},4]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0177-09c2002a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 177，源行 280–280，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_array_length('[]');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_ARRAY_LENGTH('[]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0180-ec9441c8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 180，源行 284–285，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EACH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EACH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0181-73a19e0a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 181，源行 286–286，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_each('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}'::jsonb) AS q;
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EACH(CAST('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}' AS JSONB)) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EACH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EACH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0182-3e4d6ce7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 182，源行 287–287，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM jsonb_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSONB_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 88)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ')' expecting EQ(line 1, pos 88)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0183-4e2856b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 183，源行 288–288，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM jsonb_each('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}'::jsonb) AS q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSONB_EACH(CAST('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}' AS JSONB)) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 29)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting EQ(line 1, pos 29)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0184-d763bf70

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 184，源行 290–290，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EACH_TEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EACH_TEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0185-7621b1ed

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 185，源行 291–291，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_each_text('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}'::jsonb) AS q;
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EACH_TEXT(CAST('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}' AS JSONB)) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EACH_TEXT'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EACH_TEXT'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0186-0755f124

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 186，源行 292–292，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM jsonb_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSONB_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 93)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ')' expecting EQ(line 1, pos 93)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0187-b59da278

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 187，源行 293–293，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM jsonb_each_text('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}'::jsonb) AS q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSONB_EACH_TEXT(CAST('{"a":{"b":"c","c":"b","1":"first"},"b":[1,2],"c":"cc","1":"first","n":null}' AS JSONB)) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 34)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting EQ(line 1, pos 34)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0188-2593b2f7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 188，源行 295–296，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists('{"a":null, "b":"qq"}', 'a');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS('{"a":null, "b":"qq"}', '$.a')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0189-f4ba1336

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 189，源行 297–297，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists('{"a":null, "b":"qq"}', 'b');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS('{"a":null, "b":"qq"}', '$.b')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0190-861f819f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 190，源行 298–298，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists('{"a":null, "b":"qq"}', 'c');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS('{"a":null, "b":"qq"}', '$.c')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0191-1739ab30

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 191，源行 299–299，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists('{"a":"null", "b":"qq"}', 'a');
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS('{"a":"null", "b":"qq"}', '$.a')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0192-09e510e7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 192，源行 300–300，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ? 'a';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ? 'a'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0193-913cb16f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 193，源行 301–301，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ? 'b';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ? 'b'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0194-bc1de876

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 194，源行 302–302，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ? 'c';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ? 'c'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0195-a9674a9e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 195，源行 303–303，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":"null", "b":"qq"}' ? 'a';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":"null", "b":"qq"}' AS JSONB) ? 'a'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 47)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 47)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0199-6e48a507

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 199，源行 312–312，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_any('{"a":null, "b":"qq"}', ARRAY['a','b']);
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
SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', ARRAY('a', 'b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0199-6e48a507/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0199-6e48a507/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'\")"
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

### pg-jsonb-0200-15e82b89

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 200，源行 313–313，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_any('{"a":null, "b":"qq"}', ARRAY['b','a']);
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
SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', ARRAY('b', 'a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0200-15e82b89/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0200-15e82b89/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'\")"
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

### pg-jsonb-0201-639d32ce

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 201，源行 314–314，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_any('{"a":null, "b":"qq"}', ARRAY['c','a']);
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
SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', ARRAY('c', 'a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0201-639d32ce/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0201-639d32ce/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'\")"
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

### pg-jsonb-0202-107bfecc

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 202，源行 315–315，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_any('{"a":null, "b":"qq"}', ARRAY['c','d']);
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
SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', ARRAY('c', 'd'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0202-107bfecc/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0202-107bfecc/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'\")"
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

### pg-jsonb-0203-b8ea4044

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 203，源行 316–316，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_any('{"a":null, "b":"qq"}', '{}'::text[]);
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS_ANY('{"a":null, "b":"qq"}', CAST('{}' AS ARRAY<STRING>))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ANY'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0204-522fac2b

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 204，源行 317–317，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?| ARRAY['a','b'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('a', 'b');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseOr'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('a', 'b'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0205-5f02749a

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 205，源行 318–318，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?| ARRAY['b','a'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('b', 'a');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseOr'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('b', 'a'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0206-7b83fddf

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 206，源行 319–319，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?| ARRAY['c','a'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('c', 'a');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseOr'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('c', 'a'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0207-007c4486

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 207，源行 320–320，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?| ARRAY['c','d'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('c', 'd');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseOr'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| ARRAY('c', 'd'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0208-b09c06d0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 208，源行 321–321，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?| '{}'::text[];
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?| CAST('{}' AS ARRAY<STRING>)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0209-2a965830

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 209，源行 323–323，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_all('{"a":null, "b":"qq"}', ARRAY['a','b']);
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
SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', ARRAY('a', 'b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0209-2a965830/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0209-2a965830/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'\")"
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

### pg-jsonb-0210-b407053e

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 210，源行 324–324，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_all('{"a":null, "b":"qq"}', ARRAY['b','a']);
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
SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', ARRAY('b', 'a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0210-b407053e/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0210-b407053e/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'\")"
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

### pg-jsonb-0211-0441451f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 211，源行 325–325，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_all('{"a":null, "b":"qq"}', ARRAY['c','a']);
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
SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', ARRAY('c', 'a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0211-0441451f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0211-0441451f/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'\")"
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

### pg-jsonb-0212-60b91a2b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 212，源行 326–326，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_all('{"a":null, "b":"qq"}', ARRAY['c','d']);
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
SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', ARRAY('c', 'd'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-jsonb-0212-60b91a2b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-jsonb-0212-60b91a2b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'\")"
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

### pg-jsonb-0213-fb307cf8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 213，源行 327–327，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_exists_all('{"a":null, "b":"qq"}', '{}'::text[]);
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXISTS_ALL('{"a":null, "b":"qq"}', CAST('{}' AS ARRAY<STRING>))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXISTS_ALL'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0214-7ee1efe4

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 214，源行 328–328，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& ARRAY['a','b'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('a', 'b');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseAnd'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('a', 'b'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0215-44efa3b4

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 215，源行 329–329，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& ARRAY['b','a'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('b', 'a');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseAnd'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('b', 'a'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0216-65489bec

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 216，源行 330–330，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& ARRAY['c','a'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('c', 'a');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseAnd'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('c', 'a'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0217-79898f60

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 217，源行 331–331，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& ARRAY['c','d'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('c', 'd');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseAnd'>. Line 1, Col: 63.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('c', 'd'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0218-eb3572a8

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 218，源行 332–332，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& ARRAY['a','a', 'b', 'b', 'b'];
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
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('a', 'a', 'b', 'b', 'b');
~~~

实际证据：没有完整工具证据。

工具尝试失败，不是完整对照或 Doris 运行结果：


~~~text
ParseError: Required keyword: 'this' missing for <class 'sqlglot.expressions.core.BitwiseAnd'>. Line 1, Col: 78.
  SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& ARRAY('a', 'a', 'b', 'b', 'b'[4m)[0m;
~~~

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

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

### pg-jsonb-0219-9b8af671

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 219，源行 333–333，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb '{"a":null, "b":"qq"}' ?& '{}'::text[];
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{"a":null, "b":"qq"}' AS JSONB) ?& CAST('{}' AS ARRAY<STRING>)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '?' expecting {<EOF>, ';'}(line 1, pos 45)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0220-a2bf4922

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 220，源行 335–336，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_typeof('{}') AS object;
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_TYPEOF('{}') AS object
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_TYPEOF'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_TYPEOF'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-jsonb-0221-0ee559d2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)；原语句 221，源行 337–337，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT jsonb_typeof('{"c":3,"p":"o"}') AS object;
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_TYPEOF('{"c":3,"p":"o"}') AS object
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_TYPEOF'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_TYPEOF'\")",
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
| pg-jsonb-0004-41b71ffc / SELECT $$''$$::jsonb; / [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 4 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-jsonb-0006-11228d2f / SELECT '"abc'::jsonb; / [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 6 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-jsonb-0007-2717d218 / SELECT '"abc<br>def"'::jsonb; / [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 7 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-jsonb-0178-24aca196 / SELECT jsonb_array_length('{"f1":1,"f2":[5,6]}'); / [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 178 | cannot get array length of a non-array | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-jsonb-0179-453fd54d / SELECT jsonb_array_length('4'); / [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 179 | cannot get array length of a scalar | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_ARRAY_LENGTH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-jsonb-0003-8b8c3f64 | SELECT '""'::jsonb; | [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 3 |
| pg-jsonb-0005-4e9df29c | SELECT '"abc"'::jsonb; | [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 5 |
| pg-jsonb-0008-ee506bd4 | SELECT '"\n\"\\"'::jsonb; | [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 8 |
| pg-jsonb-0115-5fb6c32b | select '{"a": "c", "b": null}'::jsonb -> 'b'; | [.out](../../../../../../cases/postgres/manual/current/assets/jsonb.out)，语句 115 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

