# groupingsets：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 17 | 17 | 0 | 0 | 17 |


[YAML](../../../../../../cases/postgres/manual/current/groupingsets.yaml)；[首轮 Markdown](../../../validation/groupingsets/validation.md) / [首轮 JSON](../../../validation/groupingsets/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-groupingsets-0012-47939b25

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 12，源行 54–60，同文回显第 1 次；历史成功 12 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b);
~~~

社区生成 SQL：


~~~sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-011 将多参数 GROUPING 对齐为 Doris GROUPING_ID：当前 GROUPING(a,b) 在 Doris 失败；GROUPING_ID(a,b) 可以执行。后续候选显式转 INT 以保留 PG grouping 返回类型。

代码位置：[sqlglot/expressions/aggregate.py:144](../../../../../../../sqlglot/sqlglot/expressions/aggregate.py)（行 144）；[sqlglot/generators/doris.py:57](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 57）。

第一次候选：


~~~sql
SELECT a,b,GROUPING_ID(a,b),SUM(v),COUNT(*),MAX(v) FROM gstest1 GROUP BY ROLLUP(a,b);
~~~

后续候选 probe-02：


~~~sql
SELECT a,b,CAST(GROUPING_ID(a,b) AS INT),SUM(v),COUNT(*),MAX(v) FROM gstest1 GROUP BY ROLLUP(a,b);
~~~

实际证据：[probe-01 JSON](../evidence/pg-groupingsets-0012-47939b25/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-groupingsets-0012-47939b25/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-groupingsets-0012-47939b25/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-groupingsets-0012-47939b25/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；5: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；6: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 6,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

为多参数 Grouping 建立 Doris 生成规则，核实位序和返回类型；不要混淆 Grouping 与 GroupingId。 限制：当前只对选中 gstest1 样本实际对照，复杂 ordered-set 聚合不是本任务已修内容。

修复任务：[PG-DORIS-011](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-groupingsets-0013-83db7fee

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 13，源行 61–62，同文回显第 1 次；历史成功 12 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by a,b;
~~~

社区生成 SQL：


~~~sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0014-b141c3ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 14，源行 63–64，同文回显第 1 次；历史成功 12 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by b desc, a;
~~~

社区生成 SQL：


~~~sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END DESC, b DESC, CASE WHEN a IS NULL THEN 1 ELSE 0 END, a
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0015-e4cf5a89

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 15，源行 65–66，同文回显第 1 次；历史成功 12 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by coalesce(a,0)+coalesce(b,0);
~~~

社区生成 SQL：


~~~sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN COALESCE(a, 0) + COALESCE(b, 0) IS NULL THEN 1 ELSE 0 END, COALESCE(a, 0) + COALESCE(b, 0)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0016-15aa8e20

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 16，源行 68–74，同文回显第 1 次；历史成功 12 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, grouping(a,b),
       array_agg(v order by v),
       string_agg(v::text, ':' order by v desc),
       percentile_disc(0.5) within group (order by v),
       rank(1,2,12) within group (order by a,b,v)
  from gstest1 group by rollup (a,b) order by a,b;
~~~

社区生成 SQL：


~~~sql
SELECT a, b, GROUPING(a, b), COLLECT_LIST(v ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END, v), GROUP_CONCAT(CAST(v AS STRING) ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END DESC, v DESC, ':'), PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END, v), RANK(1, 2, 12) WITHIN GROUP (ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN v IS NULL THEN 1 ELSE 0 END, v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 228)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing 'BY' at '('(line 1, pos 228)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0017-8889a9e8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 17，源行 76–81，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select grouping(a), a, array_agg(b),
       rank(a) within group (order by b nulls first),
       rank(a) within group (order by b nulls last)
  from (values (1,1),(1,4),(1,5),(3,1),(3,2)) v(a,b)
 group by rollup (a) order by a;
~~~

社区生成 SQL：


~~~sql
SELECT GROUPING(a), a, COLLECT_LIST(b), RANK(a) WITHIN GROUP (ORDER BY b), RANK(a) WITHIN GROUP (ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b) FROM (SELECT 1 AS a, 1 AS b UNION ALL SELECT 1, 4 UNION ALL SELECT 1, 5 UNION ALL SELECT 3, 1 UNION ALL SELECT 3, 2) AS v GROUP BY ROLLUP (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 61)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing 'BY' at '('(line 1, pos 61)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0028-d2a04692

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 28，源行 116–117，同文回显第 1 次；历史成功 0 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),a);
~~~

社区生成 SQL：


~~~sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), a)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'a'(line 1, pos 80)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'a'(line 1, pos 80)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0029-387a8c8f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 29，源行 118–118，同文回显第 1 次；历史成功 1 行。

- 首轮：行数不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),());
~~~

社区生成 SQL：


~~~sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), ())
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_COUNT_MISMATCH",
  "summary": "Result row counts differ",
  "details": [
    "source=1",
    "doris=0"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0030-16a2fa51

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 30，源行 119–119，同文回显第 1 次；历史成功 3 行。

- 首轮：行数不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),(),(),());
~~~

社区生成 SQL：


~~~sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), (), (), ())
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_COUNT_MISMATCH",
  "summary": "Result row counts differ",
  "details": [
    "source=3",
    "doris=0"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0031-06f6c711

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 31，源行 120–120，同文回显第 1 次；历史成功 3 行。

- 首轮：行数不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select sum(v), count(*) from gstest_empty group by grouping sets ((),(),());
~~~

社区生成 SQL：


~~~sql
SELECT SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((), (), ())
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_COUNT_MISMATCH",
  "summary": "Result row counts differ",
  "details": [
    "source=3",
    "doris=0"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0032-d2827749

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 32，源行 122–124，同文回显第 1 次；历史成功 1 行。

- 首轮：行数不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select t1.a, t2.b, sum(t1.v), count(*) from gstest_empty t1, gstest_empty t2
 group by grouping sets ((t1.a,t2.b),());
~~~

社区生成 SQL：


~~~sql
SELECT t1.a, t2.b, SUM(t1.v), COUNT(*) FROM gstest_empty AS t1, gstest_empty AS t2 GROUP BY GROUPING SETS ((t1.a, t2.b), ())
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_COUNT_MISMATCH",
  "summary": "Result row counts differ",
  "details": [
    "source=1",
    "doris=0"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0041-b9f11f48

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 41，源行 168–172，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select four, x
  from (select four, ten, 'foo'::text as x from tenk1) as t
  group by grouping sets (four, x)
  having x = 'foo';
~~~

社区生成 SQL：


~~~sql
SELECT four, x FROM (SELECT four, ten, CAST('foo' AS STRING) AS x FROM tenk1) AS t GROUP BY GROUPING SETS (four, x) HAVING x = 'foo'
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 107)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'four'(line 1, pos 107)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0042-433b1d44

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 42，源行 174–177，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select four, x || 'x'
  from (select four, ten, 'foo'::text as x from tenk1) as t
  group by grouping sets (four, x)
  order by four;
~~~

社区生成 SQL：


~~~sql
SELECT four, CONCAT(x, 'x') FROM (SELECT four, ten, CAST('foo' AS STRING) AS x FROM tenk1) AS t GROUP BY GROUPING SETS (four, x) ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 120)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'four'(line 1, pos 120)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0043-d829133a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 43，源行 179–181，同文回显第 1 次；历史成功 2 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select (x+y)*1, sum(z)
 from (select 1 as x, 2 as y, 3 as z) s
 group by grouping sets (x+y, x);
~~~

社区生成 SQL：


~~~sql
SELECT (x + y) * 1, SUM(z) FROM (SELECT 1 AS x, 2 AS y, 3 AS z) AS s GROUP BY GROUPING SETS (x + y, x)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 93)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'x'(line 1, pos 93)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0044-399e0bff

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 44，源行 183–186，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select x, not x as not_x, q2 from
  (select *, q1 = 1 as x from int8_tbl i1) as t
  group by grouping sets(x, q2)
  order by x, q2;
~~~

社区生成 SQL：


~~~sql
SELECT x, NOT x AS not_x, q2 FROM (SELECT *, q1 = 1 AS x FROM int8_tbl AS i1) AS t GROUP BY GROUPING SETS (x, q2) ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x, CASE WHEN q2 IS NULL THEN 1 ELSE 0 END, q2
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 107)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'x'(line 1, pos 107)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-groupingsets-0045-e2685715

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 45，源行 188–192，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select x, y
  from (select four as x, four as y from tenk1) as t
  group by grouping sets (x, y)
  having y is null
  order by 1, 2;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering

'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT x, y FROM (SELECT four AS x, four AS y FROM tenk1) AS t GROUP BY GROUPING SETS (x, y) HAVING y IS NULL ORDER BY 1 NULLS LAST, 2 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-groupingsets-0045-e2685715/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-groupingsets-0045-e2685715/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'x'(line 1, pos 87)\\n\")"
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

### pg-groupingsets-0046-ee2dc97b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/groupingsets.out)；原语句 46，源行 194–197，同文回显第 1 次；历史成功 8 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select x, y || 'y'
  from (select four as x, four as y from tenk1) as t
  group by grouping sets (x, y)
  order by 1, 2;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering

'NULLS LAST' translation not supported with positional ordering
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT x, CONCAT(y, 'y') FROM (SELECT four AS x, four AS y FROM tenk1) AS t GROUP BY GROUPING SETS (x, y) ORDER BY 1 NULLS LAST, 2 NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-groupingsets-0046-ee2dc97b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-groupingsets-0046-ee2dc97b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmissing '(' at 'x'(line 1, pos 100)\\n\")"
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

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。

本组没有负向查询。

## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

