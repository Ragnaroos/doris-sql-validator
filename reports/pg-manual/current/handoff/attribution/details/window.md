# window：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 65 | 65 | 0 | 23 | 42 |


[YAML](../../../../../../cases/postgres/manual/current/window.yaml)；[首轮 Markdown](../../../validation/window/validation.md) / [首轮 JSON](../../../validation/window/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-window-0005-80a45b07

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 5，源行 28–30，同文回显第 1 次；历史成功 20 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four, ten, SUM(SUM(four)) OVER (PARTITION BY four), AVG(ten) FROM tenk1
GROUP BY four, ten ORDER BY four, ten;
~~~

社区生成 SQL：


~~~sql
SELECT four, ten, SUM(SUM(four)) OVER (PARTITION BY four), AVG(ten) FROM tenk1 GROUP BY four, ten ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a5c341723112dd38adba4b93cd5f527f4aed047832b65ed5b78553eeb0580bf1",
    "doris_digest=1c4264e0a27674d26bcb4ac5cba19d854f46f6b45a11e89a096651b1f287f132",
    "source_sample=[['0', '0', '0', '0.00000000000000000000'], ['0', '2', '0', '2.0000000000000000'], ['0', '4', '0', '4.0000000000000000'], ['0', '6', '0', '6.0000000000000000'], ['0', '8', '0', '8.0000000000000000']]",
    "doris_sample=[['0', '0', '0', '0.0'], ['0', '2', '0', '2.0'], ['0', '4', '0', '4.0'], ['0', '6', '0', '6.0'], ['0', '8', '0', '8.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0006-bf2d68e1

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 6，源行 32–32，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT depname, empno, salary, sum(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname);
~~~

社区生成 SQL：


~~~sql
SELECT depname, empno, salary, SUM(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 48)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 48)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT depname, empno, salary, SUM(salary) OVER (PARTITION BY depname) FROM empsalary;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0006-bf2d68e1/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0006-bf2d68e1/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: varchar → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 48)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0007-d8c07fd5

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 7，源行 34–34，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT depname, empno, salary, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary) ORDER BY rank() OVER w;
~~~

社区生成 SQL：


~~~sql
SELECT depname, empno, salary, RANK() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary) ORDER BY CASE WHEN RANK() OVER w IS NULL THEN 1 ELSE 0 END, RANK() OVER w
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 43)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 43)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT depname, empno, salary, RANK() OVER (PARTITION BY depname ORDER BY salary NULLS LAST) FROM empsalary ORDER BY RANK() OVER (PARTITION BY depname ORDER BY salary NULLS LAST) NULLS LAST;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0007-d8c07fd5/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0007-d8c07fd5/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 不同，需检查并列排序 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: varchar → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "本次顺序一致，排序键唯一性未证明",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "varchar",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "不同，需检查并列排序",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 43)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0009-fbac9f79

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 9，源行 39–39，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT COUNT(*) OVER w FROM tenk1 WHERE unique2 < 10 WINDOW w AS ();
~~~

社区生成 SQL：


~~~sql
SELECT COUNT(*) OVER w FROM tenk1 WHERE unique2 < 10 WINDOW w AS ()
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 21)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 21)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT COUNT(*) OVER () FROM tenk1 WHERE unique2 < 10;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0009-fbac9f79/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0009-fbac9f79/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 21)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0010-ac7b0db2

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 10，源行 41–42，同文回显第 1 次；历史成功 0 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four FROM tenk1 WHERE FALSE WINDOW w AS (PARTITION BY ten);
~~~

社区生成 SQL：


~~~sql
SELECT four FROM tenk1 WHERE FALSE WINDOW w AS (PARTITION BY ten)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'WINDOW' expecting {<EOF>, ';'}(line 1, pos 35)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'WINDOW' expecting {<EOF>, ';'}(line 1, pos 35)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT four FROM tenk1 WHERE FALSE;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0010-ac7b0db2/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0010-ac7b0db2/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'WINDOW' expecting {<EOF>, ';'}(line 1, pos 35)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0020-3478fa0b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 20，源行 63–63，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lag(ten, four) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT LAG(ten, four, NULL) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT LAG(ten, four, NULL) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0020-3478fa0b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0020-3478fa0b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-window-0021-2c2c92ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 21，源行 65–65，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lag(ten, four, 0) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT LAG(ten, four, 0) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), 0)')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), 0)')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0022-1b2ffa99

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 22，源行 66–66，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lag(ten, four, 0.7) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten;
~~~

社区生成 SQL：


~~~sql
SELECT LAG(ten, four, 0.7) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(cast(ten as DECIMALV3(11, 1)), cast(four as BIGINT), 0.7)')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(cast(ten as DECIMALV3(11, 1)), cast(four as BIGINT), 0.7)')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0026-3b0a0a4f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 26，源行 73–73，同文回显第 1 次；历史成功 10 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT lead(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten;
~~~

社区生成 SQL：


~~~sql
SELECT LEAD(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=b3d4cbf0cfde317ad68a4e649921eab603549ff37ca1de0dbc6ff0d74fd44b5f",
    "doris_digest=3c01777eb2b72098ebdf8bc7b68550f0eed4659a8864062ade71f700aa9a2d47",
    "source_sample=[['0', '0', '0'], ['8', '0', '0'], ['-1.4', '4', '0'], ['2', '1', '1'], ['14', '1', '1']]",
    "doris_sample=[['0.0', '0', '0'], ['8.0', '0', '0'], ['-1.4', '4', '0'], ['2.0', '1', '1'], ['14.0', '1', '1']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0028-b7db4122

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 28，源行 77–78，同文回显第 1 次；历史成功 10 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT last_value(four) OVER (ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT LAST_VALUE(four) OVER (ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=d633b33b7ab5cbacf5eb39b2f0cb2cab3566f777aeb662c85319295f0520fd00",
    "doris_digest=bacc9310412700778bfa4ab1441dbafbafcdbe307155f80e1ecdd8dba750f411",
    "source_sample=[['0', '0', '0'], ['0', '0', '2'], ['0', '0', '0'], ['1', '1', '1'], ['1', '1', '3']]",
    "doris_sample=[['2', '0', '0'], ['2', '0', '0'], ['2', '0', '2'], ['1', '1', '3'], ['1', '1', '1']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0029-cebcaa74

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 29，源行 80–82，同文回显第 1 次；历史成功 10 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT last_value(ten) OVER (PARTITION BY four), ten, four FROM
	(SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s
	ORDER BY four, ten;
~~~

社区生成 SQL：


~~~sql
SELECT LAST_VALUE(ten) OVER (PARTITION BY four), ten, four FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten) AS s ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=238713c6c57d189dccde25a632fc14769f60e3bb20d9ee5811e425081a12e5c9",
    "doris_digest=ed08d6ac64ccad2070403e24062fd29c341b1827ceb1b46a50f3779e1817c3b4",
    "source_sample=[['4', '0', '0'], ['4', '0', '0'], ['4', '4', '0'], ['9', '1', '1'], ['9', '1', '1']]",
    "doris_sample=[['0', '0', '0'], ['0', '0', '0'], ['0', '4', '0'], ['9', '1', '1'], ['9', '1', '1']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0030-297e95fe

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 30，源行 84–85，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT nth_value(ten, four + 1) OVER (PARTITION BY four), ten, four
	FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s;
~~~

社区生成 SQL：


~~~sql
SELECT NTH_VALUE(ten, four + 1) OVER (PARTITION BY four), ten, four FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten) AS s
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT NTH_VALUE(ten, four + 1) OVER (PARTITION BY four), ten, four FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten) AS s;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0030-297e95fe/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0030-297e95fe/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-window-0035-926fba7b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 35，源行 106–106，同文回显第 1 次；历史成功 10 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT avg(four) OVER (PARTITION BY four ORDER BY thousand / 100) FROM tenk1 WHERE unique2 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT AVG(four) OVER (PARTITION BY four ORDER BY CASE WHEN thousand / 100 IS NULL THEN 1 ELSE 0 END, thousand / 100) FROM tenk1 WHERE unique2 < 10
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=46bd3015ad7b9c9243d1fa2d8e15ea98f84e8d7dc046f55ffcc81b8d85f5bb67",
    "doris_digest=6847d604859864c9392124fcbb171f167c10536ced42ccd277a8247dc2f55e23",
    "source_sample=[['0.00000000000000000000'], ['0.00000000000000000000'], ['0.00000000000000000000'], ['1.00000000000000000000'], ['1.00000000000000000000']]",
    "doris_sample=[['0.0'], ['0.0'], ['0.0'], ['3.0'], ['3.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0036-1d9414c5

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 36，源行 108–109，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ten, two, sum(hundred) AS gsum, sum(sum(hundred)) OVER win AS wsum
FROM tenk1 GROUP BY ten, two WINDOW win AS (PARTITION BY two ORDER BY ten);
~~~

社区生成 SQL：


~~~sql
SELECT ten, two, SUM(hundred) AS gsum, SUM(SUM(hundred)) OVER win AS wsum FROM tenk1 GROUP BY ten, two WINDOW win AS (PARTITION BY two ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'win' expecting '('(line 1, pos 62)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'win' expecting '('(line 1, pos 62)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ten, two, SUM(hundred) AS gsum, SUM(SUM(hundred)) OVER (PARTITION BY two ORDER BY ten NULLS LAST) AS wsum FROM tenk1 GROUP BY ten, two;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0036-1d9414c5/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0036-1d9414c5/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: numeric → bigint，逻辑=不同，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'win' expecting '('(line 1, pos 62)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0038-4aba58d8

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 38，源行 117–119，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(salary) OVER w1, count(*) OVER w2
FROM empsalary WINDOW w1 AS (ORDER BY salary), w2 AS (ORDER BY salary);
~~~

社区生成 SQL：


~~~sql
SELECT SUM(salary) OVER w1, COUNT(*) OVER w2 FROM empsalary WINDOW w1 AS (ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary), w2 AS (ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w1' expecting '('(line 1, pos 24)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w1' expecting '('(line 1, pos 24)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT SUM(salary) OVER (ORDER BY salary NULLS LAST), COUNT(*) OVER (ORDER BY salary NULLS LAST) FROM empsalary;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0038-4aba58d8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0038-4aba58d8/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w1' expecting '('(line 1, pos 24)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0041-1b9507b3

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 41，源行 128–129，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(salary) OVER w, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
~~~

社区生成 SQL：


~~~sql
SELECT SUM(salary) OVER w, RANK() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END DESC, salary DESC)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 24)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 24)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT SUM(salary) OVER (PARTITION BY depname ORDER BY salary DESC NULLS FIRST), RANK() OVER (PARTITION BY depname ORDER BY salary DESC NULLS FIRST) FROM empsalary;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0041-1b9507b3/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0041-1b9507b3/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 24)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0046-181af42b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 46，源行 156–158，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select x, lag(x, 1) over (order by x), lead(x, 3) over (order by x)
from (select x::numeric as x from generate_series(1,10) x);
~~~

社区生成 SQL：


~~~sql
SELECT x, LAG(x, 1, NULL) OVER (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x), LEAD(x, 3, NULL) OVER (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x) FROM (SELECT CAST(x AS DECIMAL) AS x FROM GENERATE_SERIES(1, 10) AS x)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 217)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting EQ(line 1, pos 217)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0048-536e1e97

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 48，源行 166–169，同文回显第 1 次；历史成功 20 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four, ten,
	sum(ten) over (partition by four order by ten range between unbounded preceding and current row),
	last_value(ten) over (partition by four order by ten range between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT four, ten, SUM(ten) OVER (PARTITION BY four ORDER BY ten NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(ten) OVER (PARTITION BY four ORDER BY ten NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0048-536e1e97/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0048-536e1e97/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-window-0049-f467131d

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 49，源行 171–174，同文回显第 1 次；历史成功 20 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four, ten,
	sum(ten) over (partition by four order by ten range between unbounded preceding and unbounded following),
	last_value(ten) over (partition by four order by ten range between unbounded preceding and unbounded following)
FROM (select distinct ten, four from tenk1) ss;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT four, ten, SUM(ten) OVER (PARTITION BY four ORDER BY ten NULLS LAST range BETWEEN UNBOUNDED preceding AND UNBOUNDED following), LAST_VALUE(ten) OVER (PARTITION BY four ORDER BY ten NULLS LAST range BETWEEN UNBOUNDED preceding AND UNBOUNDED following) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0049-f467131d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0049-f467131d/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-window-0050-8b853a62

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 50，源行 176–179，同文回显第 1 次；历史成功 20 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four, ten/4 as two,
	sum(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row),
	last_value(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

PG-DORIS-010 保留已知整数输入的 PostgreSQL 除法：窗口查询中的整数列除法在 Doris 变成分数，改变 ORDER BY/RANGE 的分组和结果；DIV 加 INT 类型对齐候选修复了两个具体样本的行值。

代码位置：[sqlglot/generator.py:4621](../../../../../../../sqlglot/sqlglot/generator.py)（行 4621）；[sqlglot/parsers/postgres.py](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)；[sqlglot/optimizer/annotate_types.py](../../../../../../../sqlglot/sqlglot/optimizer/annotate_types.py)。

第一次候选：


~~~sql
SELECT four, ten / 4 AS two, SUM(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

后续候选 probe-02：


~~~sql
SELECT four, CAST(ten DIV 4 AS INT) AS two, SUM(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST range BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0050-8b853a62/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0050-8b853a62/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-window-0050-8b853a62/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-window-0050-8b853a62/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| integer-division-negative | [源 SQL](../evidence/boundaries/integer-division-negative/source.sql) / [候选](../evidence/boundaries/integer-division-negative/candidate.sql) | [probe](../evidence/boundaries/integer-division-negative/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

利用可靠类型信息生成整数除法和正确返回位宽，保留朝零截断；未知列类型时不得把所有 / 改成 DIV。 限制：若必须依赖 annotate_types/Schema，说明调用条件，不能在验证器中偷偷补类型或注入改写。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)；[PG-DORIS-010](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0051-ce3792dc

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 51，源行 181–184，同文回显第 1 次；历史成功 20 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT four, ten/4 as two,
	sum(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row),
	last_value(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

PG-DORIS-010 保留已知整数输入的 PostgreSQL 除法：窗口查询中的整数列除法在 Doris 变成分数，改变 ORDER BY/RANGE 的分组和结果；DIV 加 INT 类型对齐候选修复了两个具体样本的行值。

代码位置：[sqlglot/generator.py:4621](../../../../../../../sqlglot/sqlglot/generator.py)（行 4621）；[sqlglot/parsers/postgres.py](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)；[sqlglot/optimizer/annotate_types.py](../../../../../../../sqlglot/sqlglot/optimizer/annotate_types.py)。

第一次候选：


~~~sql
SELECT four, ten / 4 AS two, SUM(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST rows BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(ten / 4) OVER (PARTITION BY four ORDER BY ten / 4 NULLS LAST rows BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

后续候选 probe-02：


~~~sql
SELECT four, CAST(ten DIV 4 AS INT) AS two, SUM(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST rows BETWEEN UNBOUNDED preceding AND CURRENT ROW), LAST_VALUE(CAST(ten DIV 4 AS INT)) OVER (PARTITION BY four ORDER BY CAST(ten DIV 4 AS INT) NULLS LAST rows BETWEEN UNBOUNDED preceding AND CURRENT ROW) FROM (SELECT DISTINCT ten, four FROM tenk1) AS ss;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0051-ce3792dc/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0051-ce3792dc/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-window-0051-ce3792dc/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-window-0051-ce3792dc/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| null-order-ascending | [源 SQL](../evidence/boundaries/null-order-ascending/source.sql) / [候选](../evidence/boundaries/null-order-ascending/candidate.sql) | [probe](../evidence/boundaries/null-order-ascending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| null-order-descending | [源 SQL](../evidence/boundaries/null-order-descending/source.sql) / [候选](../evidence/boundaries/null-order-descending/candidate.sql) | [probe](../evidence/boundaries/null-order-descending/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| integer-division-negative | [源 SQL](../evidence/boundaries/integer-division-negative/source.sql) / [候选](../evidence/boundaries/integer-division-negative/candidate.sql) | [probe](../evidence/boundaries/integer-division-negative/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

核对并覆盖 Doris 的能力标志，保留原排序表达式与 ASC/DESC；不得把解除这一阻断当成修好整个查询。 限制：一些候选仍因集合 ALL、数组操作、整数除法或 EXCLUDE 失败，必须另行归因。

利用可靠类型信息生成整数除法和正确返回位宽，保留朝零截断；未知列类型时不得把所有 / 改成 DIV。 限制：若必须依赖 annotate_types/Schema，说明调用条件，不能在验证器中偷偷补类型或注入改写。

修复任务：[PG-DORIS-002](../sqlglot-tasks.md)；[PG-DORIS-010](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0052-682b3131

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 52，源行 186–188，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (order by four range between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM
~~~

#### 代码依据、候选与执行

PG-DORIS-002 启用经实测支持的 Doris 原生 NULL 排序：Doris 继承 MySQL 的 NULL_ORDERING_SUPPORTED=None，导致位置排序和部分窗口直接拒绝；只读实测支持 NULLS FIRST/LAST。

代码位置：[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）；[sqlglot/generator.py:3317](../../../../../../../sqlglot/sqlglot/generator.py)（行 3317）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT SUM(unique1) OVER (ORDER BY four NULLS LAST range BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0052-682b3131/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0052-682b3131/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-window-0053-57f76f70

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 53，源行 190–192，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0054-dd5aa38f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 54，源行 194–196，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 2 following), unique1, four FROM tenk1 WHERE unique1 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0055-461f08dc

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 55，源行 198–200，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude no others),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

后续候选 probe-02：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 2 following), unique1, four FROM tenk1 WHERE unique1 < 10;
~~~

实际证据：[probe-02 JSON](../evidence/pg-window-0055-461f08dc/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-window-0055-461f08dc/probe-02/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0056-323a4316

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 56，源行 202–204，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0057-e7f23b7b

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 57，源行 206–208，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0058-a6d78a71

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 58，源行 210–212，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0059-b05800ec

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 59，源行 214–216，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0060-fb3b911d

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 60，源行 218–220，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0061-82375ee3

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 61，源行 222–224，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0062-c3b04485

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 62，源行 226–228，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0063-39c9997e

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 63，源行 230–232，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0064-2e7cfd65

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 64，源行 234–236，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0065-af9e0271

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 65，源行 238–240，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 2 preceding and 1 preceding),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 1 preceding), unique1, four FROM tenk1 WHERE unique1 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0066-ab2af0c3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 66，源行 242–244，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between 1 following and 3 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN 1 following AND 3 following), unique1, four FROM tenk1 WHERE unique1 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0067-f71d781e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 67，源行 246–248，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (rows between unbounded preceding and 1 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (rows BETWEEN UNBOUNDED preceding AND 1 following), unique1, four FROM tenk1 WHERE unique1 < 10
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-window-0068-06f27850

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 68，源行 250–252，同文回显第 1 次；历史成功 10 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (w range between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
~~~

社区生成 SQL：


~~~sql
SELECT SUM(unique1) OVER (w range BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'w' expecting {')', 'ORDER', 'PARTITION', 'RANGE', 'ROWS'}(line 1, pos 26)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'w' expecting {')', 'ORDER', 'PARTITION', 'RANGE', 'ROWS'}(line 1, pos 26)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT SUM(unique1) OVER (ORDER BY four NULLS LAST range BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10;
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0068-06f27850/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0068-06f27850/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "int8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int8",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'w' expecting {')', 'ORDER', 'PARTITION', 'RANGE', 'ROWS'}(line 1, pos 26)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0069-289c97b4

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 69，源行 254–256，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0070-e6a99045

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 70，源行 258–260，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0071-d0e8311e

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 71，源行 262–264，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
~~~

#### 代码依据、候选与执行

PG-DORIS-020 明确窗口 EXCLUDE 与无 ORDER BY 帧的兼容范围：部分源查询被生成器的 EXCLUDE 限制阻断；移除 NO OTHERS 的样本又被 Doris 要求 frame 必须有 ORDER BY 拒绝。

代码位置：[sqlglot/generator.py:3699](../../../../../../../sqlglot/sqlglot/generator.py)（行 3699）；[sqlglot/generators/mysql.py:127](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 127）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
EXCLUDE clause is not supported in the WINDOW clause
~~~

实际证据：没有完整工具证据。

没有完整对照 JSON；类型、行值、顺序均不能宣布通过。先解决候选生成或只读校验/序列化阻断。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

区分无操作 NO OTHERS、CURRENT ROW/GROUP/TIES 和目标 frame 限制；不能凭空补一个 ORDER BY 改变源语义或宣称 EXCLUDE 已支持。 限制：当前没有通用安全模拟；保留明确限制而不是把所有窗口失败都归给 NULL 排序。

修复任务：[PG-DORIS-020](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-window-0072-75e7d362

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/window.out)；原语句 72，源行 266–270，同文回显第 1 次；历史成功 10 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT first_value(unique1) over w,
	nth_value(unique1, 2) over w AS nth_2,
	last_value(unique1) over w, unique1, four
FROM tenk1 WHERE unique1 < 10
WINDOW w AS (order by four range between current row and unbounded following);
~~~

SQLGlot 原错误：


~~~text
AttributeError: 'Identifier' object has no attribute 'sql_name'
~~~

#### 代码依据、候选与执行

PG-DORIS-003 将命名 WINDOW 内联到实际窗口表达式：未内联的 OVER w / WINDOW w AS 在本版 Doris 被拒绝；使用社区已有 eliminate_window_clause 构造的独立候选可以执行。

代码位置：[sqlglot/transforms.py:1058](../../../../../../../sqlglot/sqlglot/transforms.py)（行 1058）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT FIRST_VALUE(unique1) OVER w, NTH_VALUE(unique1, 2) OVER w AS nth_2, LAST_VALUE(unique1) OVER w, unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (ORDER BY four NULLS LAST range BETWEEN CURRENT ROW AND UNBOUNDED following);
~~~

实际证据：[probe-01 JSON](../evidence/pg-window-0072-75e7d362/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-window-0072-75e7d362/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmismatched input 'w' expecting '('(line 1, pos 33)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| named-window-null-peers | [源 SQL](../evidence/boundaries/named-window-null-peers/source.sql) / [候选](../evidence/boundaries/named-window-null-peers/candidate.sql) | [probe](../evidence/boundaries/named-window-null-peers/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int8 → bigint，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

复用已有作用域内联变换，按 Doris 的 preprocess 顺序接入，保留继承窗口的 partition/order/frame。 限制：例如 SUM(SUM(INT)) 的 PG NUMERIC 与 Doris BIGINT 仍不同，窗口内联不解决聚合类型契约。

修复任务：[PG-DORIS-003](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。

本组没有负向查询。

## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-window-0003-d9b289b5 | SELECT depname, empno, salary, sum(salary) OVER (PARTITION BY depname) FROM empsalary ORDER BY depname, salary; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 3 |
| pg-window-0004-960303b3 | SELECT depname, empno, salary, rank() OVER (PARTITION BY depname ORDER BY salary) FROM empsalary; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 4 |
| pg-window-0008-53f03910 | SELECT COUNT(*) OVER () FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 8 |
| pg-window-0011-6486afe4 | SELECT sum(four) OVER (PARTITION BY ten ORDER BY unique2) AS sum_1, ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 11 |
| pg-window-0012-7af7cea6 | SELECT row_number() OVER (ORDER BY unique2) FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 12 |
| pg-window-0013-e076c183 | SELECT rank() OVER (PARTITION BY four ORDER BY ten) AS rank_1, ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 13 |
| pg-window-0014-1f84bd82 | SELECT dense_rank() OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 14 |
| pg-window-0017-22839a3f | SELECT ntile(3) OVER (ORDER BY ten, four), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 17 |
| pg-window-0019-4a0f9f7e | SELECT lag(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 19 |
| pg-window-0023-16d45482 | SELECT lead(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 23 |
| pg-window-0024-b67f33a9 | SELECT lead(ten * 2, 1) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 24 |
| pg-window-0025-edfe2123 | SELECT lead(ten * 2, 1, -1) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 25 |
| pg-window-0027-2328adcf | SELECT first_value(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 27 |
| pg-window-0031-bf38d1ba | SELECT ten, two, sum(hundred) AS gsum, sum(sum(hundred)) OVER (PARTITION BY two ORDER BY ten) AS wsum<br>FROM tenk1 GROUP BY ten, two; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 31 |
| pg-window-0032-15576266 | SELECT count(*) OVER (PARTITION BY four), four FROM (SELECT * FROM tenk1 WHERE two = 1)s WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 32 |
| pg-window-0033-329f5631 | SELECT (count(*) OVER (PARTITION BY four ORDER BY ten) +<br>  sum(hundred) OVER (PARTITION BY four ORDER BY ten))::varchar AS cntsum<br>  FROM tenk1 WHERE unique2 < 10; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 33 |
| pg-window-0034-e48cbd50 | SELECT * FROM(<br>  SELECT count(*) OVER (PARTITION BY four ORDER BY ten) +<br>    sum(hundred) OVER (PARTITION BY two ORDER BY ten) AS total,<br>    count(*) OVER (PARTITION BY four ORDER BY ten) AS fourcount,<br>    sum(hundred) OVER (PARTITION BY two ORDER BY ten) AS twosum<br>    FROM tenk1<br>)sub<br>WHERE total <> fourcount + twosum; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 34 |
| pg-window-0037-954ddd27 | SELECT sum(salary),<br>	row_number() OVER (ORDER BY depname),<br>	sum(sum(salary)) OVER (ORDER BY depname DESC)<br>FROM empsalary GROUP BY depname; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 37 |
| pg-window-0040-08952902 | SELECT count(*) OVER (PARTITION BY four) FROM (SELECT * FROM tenk1 WHERE FALSE)s; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 40 |
| pg-window-0042-c250e5f4 | SELECT empno, depname, salary, bonus, depadj, MIN(bonus) OVER (ORDER BY empno), MAX(depadj) OVER () FROM(<br>	SELECT *,<br>		CASE WHEN enroll_date < '2008-01-01' THEN 2008 - extract(YEAR FROM enroll_date) END * 500 AS bonus,<br>		CASE WHEN<br>			AVG(salary) OVER (PARTITION BY depname) < salary<br>		THEN 200 END AS depadj FROM empsalary<br>)s; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 42 |
| pg-window-0043-19c41ea1 | SELECT SUM(COUNT(f1)) OVER () FROM int4_tbl WHERE f1=42; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 43 |
| pg-window-0044-f6e494e0 | select ten,<br>  sum(unique1) + sum(unique2) as res,<br>  rank() over (order by sum(unique1) + sum(unique2)) as rank<br>from tenk1<br>group by ten order by ten; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 44 |
| pg-window-0047-b6d9c64a | SELECT four, ten,<br>	sum(ten) over (partition by four order by ten),<br>	last_value(ten) over (partition by four order by ten)<br>FROM (select distinct ten, four from tenk1) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/window.out)，语句 47 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

