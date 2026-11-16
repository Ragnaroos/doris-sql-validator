# numeric：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 25 | 11 | 14 | 0 | 11 |


[YAML](../../../../../../cases/postgres/manual/current/numeric.yaml)；[首轮 Markdown](../../../validation/numeric/validation.md) / [首轮 JSON](../../../validation/numeric/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-numeric-0525-c4b5f8ba

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 525，源行 637–649，同文回显第 1 次；历史成功 49 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan'))
SELECT x1, x2,
  x1 + x2 AS sum,
  x1 - x2 AS diff,
  x1 * x2 AS prod
FROM v AS v1(x1), v AS v2(x2);
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 279)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 279)\\n\\n== SQL ==\\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)\\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2);
~~~

实际证据：[probe-01 JSON](../evidence/pg-numeric-0525-c4b5f8ba/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-numeric-0525-c4b5f8ba/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 279)\\n\\n== SQL ==\\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2)\\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\\n\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 279)\\n\\n== SQL ==\\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 + x2 AS `sum`, x1 - x2 AS diff, x1 * x2 AS prod FROM v AS v1(x1), v AS v2(x2);\\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-numeric-0526-8a2839bf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 526，源行 651–657，同文回显第 1 次；历史成功 42 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('inf'),('-inf'),('nan'))
SELECT x1, x2,
  x1 / x2 AS quot,
  x1 % x2 AS mod,
  div(x1, x2) AS div
FROM v AS v1(x1), v AS v2(x2) WHERE x2 != 0;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 297)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 297)\\n\\n== SQL ==\\nWITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, x1 / x2 AS quot, x1 % x2 AS mod, CAST(x1 DIV x2 AS DECIMAL) AS `div` FROM v AS v1(x1), v AS v2(x2) WHERE x2 <> 0\\n---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0529-d53a9922

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 529，源行 661–661，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::numeric / '0';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('nan' AS DECIMAL) / '0'
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

### pg-numeric-0533-2a259c60

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 533，源行 665–665，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 'nan'::numeric % '0';
~~~

社区生成 SQL：


~~~sql
SELECT CAST('nan' AS DECIMAL) % '0'
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

### pg-numeric-0537-76b7cab4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 537，源行 669–669，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT div('nan'::numeric, '0');
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('nan' AS DECIMAL) DIV '0' AS DECIMAL)
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

### pg-numeric-0539-e8cd2f84

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 539，源行 672–675，同文回显第 1 次；历史成功 8 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan'))
SELECT x, -x as minusx, abs(x), floor(x), ceil(x), sign(x), numeric_inc(x) as inc
FROM v;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x, -x AS minusx, ABS(x), FLOOR(x), CEIL(x), SIGN(x), NUMERIC_INC(x) AS inc FROM v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'NUMERIC_INC'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'NUMERIC_INC'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0540-4f39a445

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 540，源行 677–680，同文回显第 1 次；历史成功 8 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('inf'),('-inf'),('nan'))
SELECT x, round(x), round(x,1) as round1, trunc(x), trunc(x,1) as trunc1
FROM v;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT x, ROUND(x), ROUND(x, 1) AS round1, TRUNCATE(x, 0), TRUNCATE(x, 1) AS trunc1 FROM v
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=225c6ec3006eb93f357ae965547e5fea5b6ca102d87dc05514504f5f3c72a3eb",
    "doris_digest=ceb8685c4c1f868b5dc129bed2237498ba806c1d5c4551f7197b122c5185d470",
    "source_sample=[['0', '0', '0.0', '0', '0.0'], ['1', '1', '1.0', '1', '1.0'], ['-1', '-1', '-1.0', '-1', '-1.0'], ['4.2', '4', '4.2', '4', '4.2'], ['-7.777', '-8', '-7.8', '-7', '-7.7']]",
    "doris_sample=[['0E-9', '0', '0.0', '0', '0.0'], ['1', '1', '1.0', '1', '1.0'], ['-1', '-1', '-1.0', '-1', '-1.0'], ['4.2', '4', '4.2', '4', '4.2'], ['-7.777', '-8', '-7.8', '-7', '-7.7']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0541-215fd527

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 541，源行 682–688，同文回显第 1 次；历史成功 13 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('-1'),('4.2'),('-7.777'),('1e340'),('-1e340'),
         ('inf'),('-inf'),('nan'),
         ('inf'),('-inf'),('nan'))
SELECT substring(x::text, 1, 32)
FROM v ORDER BY x;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '-1' UNION ALL SELECT '4.2' UNION ALL SELECT '-7.777' UNION ALL SELECT '1e340' UNION ALL SELECT '-1e340' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan' UNION ALL SELECT 'inf' UNION ALL SELECT '-inf' UNION ALL SELECT 'nan') AS _values) SELECT SUBSTRING(CAST(x AS STRING), 1, 32) FROM v ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a00b9f01e6c6c5d32d904c73ff055f5e1f4e46eeb024637c9912c27cd2bd9d10",
    "doris_digest=02d4ad16aed6af83182fa23973740c6535e5b8718cac1d69a6a5d50f49f120dd",
    "source_sample=[['-Infinity'], ['-Infinity'], ['-1000000000000000000000000000000'], ['-7.777'], ['-1']]",
    "doris_sample=[['-1'], ['-1e340'], ['-7.777'], ['-inf'], ['-inf']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0542-ec3f1242

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 542，源行 690–693，同文回显第 1 次；历史成功 5 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('0'::numeric),('1'),('4.2'),('inf'),('nan'))
SELECT x, sqrt(x)
FROM v;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('0' AS DECIMAL) UNION ALL SELECT '1' UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x, SQRT(x) FROM v
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=3b520b1b21fdb4bc0a195853177a4e7e569741b6dbfc93da26fb4a768977b9b8",
    "doris_digest=045e786a2f2e3d50751ad4949a75b479034de4f3421fbd58f77c6d2115b955dc",
    "source_sample=[['0', '0.000000000000000'], ['1', '1.000000000000000'], ['4.2', '2.049390153191920'], ['Infinity', 'Infinity'], ['NaN', 'NaN']]",
    "doris_sample=[['0E-9', '0.0'], ['1', '1.0'], ['4.2', '2.04939015319192'], ['inf', 'Infinity'], ['nan', 'NaN']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0545-f34f959e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 545，源行 698–704，同文回显第 1 次；历史成功 4 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('1'::numeric),('4.2'),('inf'),('nan'))
SELECT x,
  log(x),
  log10(x),
  ln(x)
FROM v;
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('1' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x, LOG(x), LOG(10, x), LN(x) FROM v
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=b1df8c4ae48f59104f01e39e03bf4fbd30c6203dd53ea4305744485ba576423b",
    "doris_digest=35338a6156e60c28a1ae277d9507f2ef3f1282564044a7c64acbd28d80dd9e28",
    "source_sample=[['1', '0.0000000000000000', '0.0000000000000000', '0.0000000000000000'], ['4.2', '0.6232492903979005', '0.6232492903979005', '1.4350845252893226'], ['Infinity', 'Infinity', 'Infinity', 'Infinity'], ['NaN', 'NaN', 'NaN', 'NaN']]",
    "doris_sample=[['1.000000000', '0.0', '0.0', '0.0'], ['4.2', '1.435084525289323', '0.6232492903979004', '1.435084525289323'], ['inf', 'Infinity', 'Infinity', 'Infinity'], ['nan', 'NaN', 'NaN', 'NaN']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-numeric-0549-3d2249da

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)；原语句 549，源行 710–714，同文回显第 1 次；历史成功 16 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH v(x) AS
  (VALUES('2'::numeric),('4.2'),('inf'),('nan'))
SELECT x1, x2,
  log(x1, x2)
FROM v AS v1(x1), v AS v2(x2);
~~~

社区生成 SQL：


~~~sql
WITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nDo not implemented(line 1, pos 173)\n\n== SQL ==\nWITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 173)\\n\\n== SQL ==\\nWITH v(x) AS (SELECT * FROM (SELECT CAST('2' AS DECIMAL) UNION ALL SELECT '4.2' UNION ALL SELECT 'inf' UNION ALL SELECT 'nan') AS _values) SELECT x1, x2, LOG(x1, x2) FROM v AS v1(x1), v AS v2(x2)\\n-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------^^^\\n\")",
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
| pg-numeric-0527-853087af / SELECT 'inf'::numeric / '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 527 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0528-5c708c93 / SELECT '-inf'::numeric / '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 528 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0530-92fc4082 / SELECT '0'::numeric / '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 530 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0531-005b6940 / SELECT 'inf'::numeric % '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 531 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0532-970512c5 / SELECT '-inf'::numeric % '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 532 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0534-066224c8 / SELECT '0'::numeric % '0'; / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 534 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0535-fc163301 / SELECT div('inf'::numeric, '0'); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 535 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0536-4370cc9d / SELECT div('-inf'::numeric, '0'); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 536 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0538-739933ff / SELECT div('0'::numeric, '0'); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 538 | division by zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0543-0a26f3a1 / SELECT sqrt('-1'::numeric); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 543 | cannot take square root of a negative number | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0544-97db210d / SELECT sqrt('-inf'::numeric); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 544 | cannot take square root of a negative number | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0546-e870226f / SELECT ln('0'::numeric); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 546 | cannot take logarithm of zero | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0547-c845e747 / SELECT ln('-1'::numeric); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 547 | cannot take logarithm of a negative number | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-numeric-0548-84f27093 / SELECT ln('-inf'::numeric); / [.out](../../../../../../cases/postgres/manual/current/assets/numeric.out)，语句 548 | cannot take logarithm of a negative number | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

