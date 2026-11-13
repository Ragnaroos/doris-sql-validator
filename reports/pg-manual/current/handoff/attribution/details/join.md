# join：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 58 | 56 | 2 | 28 | 28 |


[YAML](../../../../../../cases/postgres/manual/current/join.yaml)；[首轮 Markdown](../../../validation/join/validation.md) / [首轮 JSON](../../../validation/join/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-join-0028-f25eea71

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 28，源行 58–59，同文回显第 1 次；历史成功 11 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL AS t1 (a, b, c);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c)\\n---------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-004 支持基表别名后的列名列表：AS t(a,b,c) 被直接生成到 Doris 后失败。显式投影候选可行；后续 CTE 列名列表候选也已实测，可避免默认读取表 Schema。

代码位置：[sqlglot/generator.py:1628](../../../../../../../sqlglot/sqlglot/generator.py)（行 1628）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT * FROM (SELECT i AS a, j AS b, t AS c FROM J1_TBL) AS t1;
~~~

后续候选 probe-02：


~~~sql
WITH _dsv_t1(a,b,c) AS (SELECT * FROM J1_TBL) SELECT * FROM _dsv_t1 AS t1;
~~~

实际证据：[probe-01 JSON](../evidence/pg-join-0028-f25eea71/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-join-0028-f25eea71/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-join-0028-f25eea71/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-join-0028-f25eea71/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c)\\n---------------------^^^\\n')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

研究将基表列重命名下沉到 CTE 列别名，或在已有 Schema 时改写投影；处理命名冲突和作用域，不硬编码 J1_TBL 的列。 限制：现有表数据类型映射限制不是本规则造成；不能把有限 VARCHAR 说成全域 TEXT。

修复任务：[PG-DORIS-004](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0029-f25eea71

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 29，源行 61–62，同文回显第 1 次；历史成功 11 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c)\\n---------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-004 支持基表别名后的列名列表：AS t(a,b,c) 被直接生成到 Doris 后失败。显式投影候选可行；后续 CTE 列名列表候选也已实测，可避免默认读取表 Schema。

代码位置：[sqlglot/generator.py:1628](../../../../../../../sqlglot/sqlglot/generator.py)（行 1628）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT * FROM (SELECT i AS a, j AS b, t AS c FROM J1_TBL) AS t1;
~~~

实际证据：[probe-01 JSON](../evidence/pg-join-0029-f25eea71/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-join-0029-f25eea71/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c)\\n---------------------^^^\\n')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

研究将基表列重命名下沉到 CTE 列别名，或在已有 Schema 时改写投影；处理命名冲突和作用域，不硬编码 J1_TBL 的列。 限制：现有表数据类型映射限制不是本规则造成；不能把有限 VARCHAR 说成全域 TEXT。

修复任务：[PG-DORIS-004](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0030-8603f3ed

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 30，源行 64–65，同文回显第 1 次；历史成功 99 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)\n---------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)\\n---------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-004 支持基表别名后的列名列表：AS t(a,b,c) 被直接生成到 Doris 后失败。显式投影候选可行；后续 CTE 列名列表候选也已实测，可避免默认读取表 Schema。

代码位置：[sqlglot/generator.py:1628](../../../../../../../sqlglot/sqlglot/generator.py)（行 1628）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT * FROM (SELECT i AS a, j AS b, t AS c FROM J1_TBL) AS t1 CROSS JOIN (SELECT i AS d, k AS e FROM J2_TBL) AS t2;
~~~

实际证据：[probe-01 JSON](../evidence/pg-join-0030-8603f3ed/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-join-0030-8603f3ed/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；5: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)\\n---------------------^^^\\n')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

研究将基表列重命名下沉到 CTE 列别名，或在已有 Schema 时改写投影；处理命名冲突和作用域，不硬编码 J1_TBL 的列。 限制：现有表数据类型映射限制不是本规则造成；不能把有限 VARCHAR 说成全域 TEXT。

修复任务：[PG-DORIS-004](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0031-f4169150

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 31，源行 67–69，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT t1.a, t2.e
  FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e)
  WHERE t1.a = t2.d;
~~~

社区生成 SQL：


~~~sql
SELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 30)\n\n== SQL ==\nSELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d\n------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 30)\\n\\n== SQL ==\\nSELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d\\n------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-004 支持基表别名后的列名列表：AS t(a,b,c) 被直接生成到 Doris 后失败。显式投影候选可行；后续 CTE 列名列表候选也已实测，可避免默认读取表 Schema。

代码位置：[sqlglot/generator.py:1628](../../../../../../../sqlglot/sqlglot/generator.py)（行 1628）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT t1.a, t2.e FROM (SELECT i AS a, j AS b, t AS c FROM J1_TBL) AS t1 CROSS JOIN (SELECT i AS d, k AS e FROM J2_TBL) AS t2 WHERE t1.a=t2.d;
~~~

后续候选 probe-02：


~~~sql
WITH _dsv_t1(a,b,c) AS (SELECT * FROM J1_TBL), _dsv_t2(d,e) AS (SELECT * FROM J2_TBL) SELECT t1.a,t2.e FROM _dsv_t1 t1 CROSS JOIN _dsv_t2 t2 WHERE t1.a=t2.d;
~~~

实际证据：[probe-01 JSON](../evidence/pg-join-0031-f4169150/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-join-0031-f4169150/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-join-0031-f4169150/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-join-0031-f4169150/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 30)\\n\\n== SQL ==\\nSELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d\\n------------------------------^^^\\n')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

研究将基表列重命名下沉到 CTE 列别名，或在已有 Schema 时改写投影；处理命名冲突和作用域，不硬编码 J1_TBL 的列。 限制：现有表数据类型映射限制不是本规则造成；不能把有限 VARCHAR 说成全域 TEXT。

修复任务：[PG-DORIS-004](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0035-06b3f865

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 35，源行 89–91，同文回显第 1 次；历史成功 99 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ii, tt, kk
  FROM (J1_TBL CROSS JOIN J2_TBL)
    AS tx (ii, jj, tt, ii2, kk);
~~~

社区生成 SQL：


~~~sql
SELECT ii, tt, kk FROM (J1_TBL CROSS JOIN J2_TBL) AS tx(ii, jj, tt, ii2, kk)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 50)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 50)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0036-deb1b49d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 36，源行 93–95，同文回显第 1 次；历史成功 99 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT tx.ii, tx.jj, tx.kk
  FROM (J1_TBL t1 (a, b, c) CROSS JOIN J2_TBL t2 (d, e))
    AS tx (ii, jj, tt, ii2, kk);
~~~

社区生成 SQL：


~~~sql
SELECT tx.ii, tx.jj, tx.kk FROM (J1_TBL AS t1(a, b, c) CROSS JOIN J2_TBL AS t2(d, e)) AS tx(ii, jj, tt, ii2, kk)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 86)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 86)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0040-a96d716e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 40，源行 121–123，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, d) USING (a)
  ORDER BY a, d;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d\n---------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d\\n---------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0041-6acaaacd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 41，源行 125–127，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, b) USING (b)
  ORDER BY b, t1.a;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a\n---------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 21)\\n\\n== SQL ==\\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a\\n---------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0052-38f1da35

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 52，源行 141–147，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL NATURAL JOIN J2_TBL;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL NATURAL JOIN J2_TBL
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 21)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 21)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0053-7ab78474

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 53，源行 149–150，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (a, d);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c) NATURAL JOIN J2_TBL AS t2(a, d)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0054-8499874b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 54，源行 152–153，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (d, a);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b, c) NATURAL JOIN J2_TBL AS t2(d, a)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0055-e0343680

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 55，源行 155–158，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT *
  FROM J1_TBL t1 (a, b) NATURAL JOIN J2_TBL t2 (a);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM J1_TBL AS t1(a, b) NATURAL JOIN J2_TBL AS t2(a)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 33)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 33)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0078-ff5cfabb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 78，源行 243–243，同文回显第 1 次；历史成功 4 行。

- 首轮：行数不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM t1 FULL JOIN t2 USING (name) FULL JOIN t3 USING (name);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM t1 FULL JOIN t2 USING (`name`) FULL JOIN t3 USING (`name`)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_COUNT_MISMATCH",
  "summary": "Result row counts differ",
  "details": [
    "source=4",
    "doris=5"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0081-1853c44b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 81，源行 262–266，同文回显第 1 次；历史成功 4 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT * FROM t2) as s2
FULL JOIN
(SELECT * FROM t3) s3
USING (name);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT * FROM t2) AS s2 LEFT JOIN (SELECT * FROM t3) AS `s3` USING (`name`) UNION ALL SELECT * FROM (SELECT * FROM t2) AS s2 RIGHT JOIN (SELECT * FROM t3) AS `s3` USING (`name`) WHERE NOT EXISTS(SELECT 1 FROM (SELECT * FROM t2) AS s2 WHERE s2.`name` = `s3`.`name`)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=cd4d0e762d39d7131e8a8c500c950dc74655dc20d21c02b9e5d38dc82a4321a4",
    "doris_digest=43edac1fe88167d312ef7246e063a528f8f28263f18500d877ebf1237570adb1",
    "source_sample=[['bb', '12', '13'], ['cc', '22', '23'], ['dd', '', '33'], ['ee', '42', '']]",
    "doris_sample=[['bb', '12', '13'], ['cc', '22', '23'], ['ee', '42', ''], ['', '', '33']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0082-ede1f502

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 82，源行 268–273，同文回显第 1 次；历史成功 2 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL INNER JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL INNER JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0083-ad25c0f2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 83，源行 275–278，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL LEFT JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL LEFT JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0084-d692d7c3

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 84，源行 280–283，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL FULL JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

SQLGlot 原错误：


~~~text
TypeError: 'NoneType' object is not iterable
~~~

#### 代码依据、候选与执行

PG-DORIS-012 避免 NATURAL FULL JOIN 在 MySQL 兼容变换中崩溃：eliminate_full_outer_join 对 NATURAL FULL JOIN 的 using=None 迭代触发 TypeError，3 条合法查询无法生成。显式 FULL JOIN ON + COALESCE 的独立候选行值一致。

代码位置：[sqlglot/transforms.py:685](../../../../../../../sqlglot/sqlglot/transforms.py)（行 685）；[sqlglot/transforms.py:706](../../../../../../../sqlglot/sqlglot/transforms.py)（行 706）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
'NoneType' object is not iterable
~~~

后续候选 probe-02：


~~~sql
SELECT COALESCE(s2.name,s3.name) AS name,s2.s2_n,s2.s2_2,s3.s3_n,s3.s3_2 FROM (SELECT name,n AS s2_n,2 AS s2_2 FROM t2) s2 FULL JOIN (SELECT name,n AS s3_n,3 AS s3_2 FROM t3) s3 ON s2.name=s3.name;
~~~

实际证据：[probe-02 JSON](../evidence/pg-join-0084-d692d7c3/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-join-0084-d692d7c3/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；5: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

Doris 不应无条件沿用 MySQL 的 FULL JOIN 模拟；对 NATURAL/USING 的公共列识别和投影有明确策略，不能仅吞掉 TypeError。 限制：类型受准备阶段 NAME/TEXT→VARCHAR(512) 影响，不能据本批行值一致证明全类型域。

修复任务：[PG-DORIS-012](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0085-8f120375

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 85，源行 285–290，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1
NATURAL INNER JOIN
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL INNER JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT `name`, n AS s1_n, 1 AS s1_1 FROM t1) AS s1 NATURAL INNER JOIN (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL INNER JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0086-8e4f7296

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 86，源行 292–297，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1
NATURAL FULL JOIN
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL FULL JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT `name`, n AS s1_n, 1 AS s1_1 FROM t1) AS s1 NATURAL FULL JOIN (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL FULL JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0087-f13d67d0

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 87，源行 299–306，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s1_n FROM t1) as s1
NATURAL FULL JOIN
  (SELECT * FROM
    (SELECT name, n as s2_n FROM t2) as s2
    NATURAL FULL JOIN
    (SELECT name, n as s3_n FROM t3) as s3
  ) ss2;
~~~

SQLGlot 原错误：


~~~text
TypeError: 'NoneType' object is not iterable
~~~

#### 代码依据、候选与执行

PG-DORIS-012 避免 NATURAL FULL JOIN 在 MySQL 兼容变换中崩溃：eliminate_full_outer_join 对 NATURAL FULL JOIN 的 using=None 迭代触发 TypeError，3 条合法查询无法生成。显式 FULL JOIN ON + COALESCE 的独立候选行值一致。

代码位置：[sqlglot/transforms.py:685](../../../../../../../sqlglot/sqlglot/transforms.py)（行 685）；[sqlglot/transforms.py:706](../../../../../../../sqlglot/sqlglot/transforms.py)（行 706）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
'NoneType' object is not iterable
~~~

后续候选 probe-02：


~~~sql
SELECT COALESCE(s1.name,ss2.name) AS name,s1.s1_n,ss2.s2_n,ss2.s3_n FROM (SELECT name,n AS s1_n FROM t1) s1 FULL JOIN (SELECT COALESCE(s2.name,s3.name) AS name,s2.s2_n,s3.s3_n FROM (SELECT name,n AS s2_n FROM t2) s2 FULL JOIN (SELECT name,n AS s3_n FROM t3) s3 ON s2.name=s3.name) ss2 ON s1.name=ss2.name;
~~~

实际证据：[probe-02 JSON](../evidence/pg-join-0087-f13d67d0/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-join-0087-f13d67d0/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

Doris 不应无条件沿用 MySQL 的 FULL JOIN 模拟；对 NATURAL/USING 的公共列识别和投影有明确策略，不能仅吞掉 TypeError。 限制：类型受准备阶段 NAME/TEXT→VARCHAR(512) 影响，不能据本批行值一致证明全类型域。

修复任务：[PG-DORIS-012](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0088-9518261f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 88，源行 308–315，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
(SELECT name, n as s1_n FROM t1) as s1
NATURAL FULL JOIN
  (SELECT * FROM
    (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
    NATURAL FULL JOIN
    (SELECT name, n as s3_n FROM t3) as s3
  ) ss2;
~~~

SQLGlot 原错误：


~~~text
TypeError: 'NoneType' object is not iterable
~~~

#### 代码依据、候选与执行

PG-DORIS-012 避免 NATURAL FULL JOIN 在 MySQL 兼容变换中崩溃：eliminate_full_outer_join 对 NATURAL FULL JOIN 的 using=None 迭代触发 TypeError，3 条合法查询无法生成。显式 FULL JOIN ON + COALESCE 的独立候选行值一致。

代码位置：[sqlglot/transforms.py:685](../../../../../../../sqlglot/sqlglot/transforms.py)（行 685）；[sqlglot/transforms.py:706](../../../../../../../sqlglot/sqlglot/transforms.py)（行 706）；[sqlglot/generators/mysql.py:189](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 189）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
'NoneType' object is not iterable
~~~

后续候选 probe-02：


~~~sql
SELECT COALESCE(s1.name,ss2.name) AS name,s1.s1_n,ss2.s2_n,ss2.s2_2,ss2.s3_n FROM (SELECT name,n AS s1_n FROM t1) s1 FULL JOIN (SELECT COALESCE(s2.name,s3.name) AS name,s2.s2_n,s2.s2_2,s3.s3_n FROM (SELECT name,n AS s2_n,2 AS s2_2 FROM t2) s2 FULL JOIN (SELECT name,n AS s3_n FROM t3) s3 ON s2.name=s3.name) ss2 ON s1.name=ss2.name;
~~~

实际证据：[probe-02 JSON](../evidence/pg-join-0088-9518261f/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-join-0088-9518261f/probe-02/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → varchar(512)，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；3: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用；4: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用；5: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "varchar(512)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 3,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 4,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 5,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

Doris 不应无条件沿用 MySQL 的 FULL JOIN 模拟；对 NATURAL/USING 的公共列识别和投影有明确策略，不能仅吞掉 TypeError。 限制：类型受准备阶段 NAME/TEXT→VARCHAR(512) 影响，不能据本批行值一致证明全类型域。

修复任务：[PG-DORIS-012](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-join-0105-7b5454e9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 105，源行 346–347，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0106-19118909

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 106，源行 348–349，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and x2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0107-cd1a2740

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 107，源行 350–351，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and y2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0108-29622a8a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 108，源行 352–353，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and xx2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0109-9c15a804

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 109，源行 354–356，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (x2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0110-bacb7b5f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 110，源行 357–358，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (y2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-join-0111-f8035c11

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/join.out)；原语句 111，源行 359–360，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (xx2 is not null);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nDo not implemented(line 1, pos 55)\\n\\n== SQL ==\\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)\\n-------------------------------------------------------^^^\\n')",
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
| pg-join-0033-f5fe6eea / SELECT i, k, t<br>  FROM J1_TBL CROSS JOIN J2_TBL; / [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 33 | column reference "i" is ambiguous | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = i is ambiguous: i#0, i#3.') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-join-0044-77d9c458 / SELECT * FROM (J1_TBL JOIN J2_TBL USING (i)) AS x WHERE J1_TBL.t = 'one'; / [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 44 | invalid reference to FROM-clause entry for table "j1_tbl" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 45)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-join-0026-3d577984 | SELECT *<br>  FROM J1_TBL AS tx; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 26 |
| pg-join-0027-3d577984 | SELECT *<br>  FROM J1_TBL tx; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 27 |
| pg-join-0032-131168ee | SELECT *<br>  FROM J1_TBL CROSS JOIN J2_TBL; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 32 |
| pg-join-0034-2aef35d2 | SELECT t1.i, k, t<br>  FROM J1_TBL t1 CROSS JOIN J2_TBL t2; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 34 |
| pg-join-0037-5124334f | SELECT *<br>  FROM J1_TBL CROSS JOIN J2_TBL a CROSS JOIN J2_TBL b; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 37 |
| pg-join-0038-ed098b35 | SELECT *<br>  FROM J1_TBL INNER JOIN J2_TBL USING (i); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 38 |
| pg-join-0039-d48b47ad | SELECT *<br>  FROM J1_TBL JOIN J2_TBL USING (i); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 39 |
| pg-join-0042-69d99dd0 | SELECT * FROM J1_TBL JOIN J2_TBL USING (i) WHERE J1_TBL.t = 'one'; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 42 |
| pg-join-0056-4f0fb7e6 | SELECT *<br>  FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i = J2_TBL.i); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 56 |
| pg-join-0057-a1cdb13d | SELECT *<br>  FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i = J2_TBL.k); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 57 |
| pg-join-0058-0eea9375 | SELECT *<br>  FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i <= J2_TBL.k); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 58 |
| pg-join-0059-59e1a665 | SELECT *<br>  FROM J1_TBL LEFT OUTER JOIN J2_TBL USING (i)<br>  ORDER BY i, k, t; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 59 |
| pg-join-0060-7e3cb6a7 | SELECT *<br>  FROM J1_TBL LEFT JOIN J2_TBL USING (i)<br>  ORDER BY i, k, t; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 60 |
| pg-join-0061-af0e5d94 | SELECT *<br>  FROM J1_TBL RIGHT OUTER JOIN J2_TBL USING (i); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 61 |
| pg-join-0062-f291f66b | SELECT *<br>  FROM J1_TBL RIGHT JOIN J2_TBL USING (i); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 62 |
| pg-join-0063-02b7035f | SELECT *<br>  FROM J1_TBL FULL OUTER JOIN J2_TBL USING (i)<br>  ORDER BY i, k, t; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 63 |
| pg-join-0064-e44f487a | SELECT *<br>  FROM J1_TBL FULL JOIN J2_TBL USING (i)<br>  ORDER BY i, k, t; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 64 |
| pg-join-0065-58560026 | SELECT *<br>  FROM J1_TBL LEFT JOIN J2_TBL USING (i) WHERE (k = 1); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 65 |
| pg-join-0066-efcfad36 | SELECT *<br>  FROM J1_TBL LEFT JOIN J2_TBL USING (i) WHERE (i = 1); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 66 |
| pg-join-0079-cfd7eba7 | SELECT * FROM<br>(SELECT * FROM t2) as s2<br>INNER JOIN<br>(SELECT * FROM t3) s3<br>USING (name); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 79 |
| pg-join-0080-76b214df | SELECT * FROM<br>(SELECT * FROM t2) as s2<br>LEFT JOIN<br>(SELECT * FROM t3) s3<br>USING (name); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 80 |
| pg-join-0089-7ce60f41 | SELECT * FROM<br>  (SELECT name, n as s1_n FROM t1) as s1<br>FULL JOIN<br>  (SELECT name, 2 as s2_n FROM t2) as s2<br>ON (s1_n = s2_n); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 89 |
| pg-join-0101-1efc0847 | select * from x; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 101 |
| pg-join-0102-86bdd254 | select * from y; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 102 |
| pg-join-0103-dd8d1c93 | select * from x left join y on (x1 = y1 and x2 is not null); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 103 |
| pg-join-0104-f0bdfc8e | select * from x left join y on (x1 = y1 and y2 is not null); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 104 |
| pg-join-0112-e1276d8d | select count(*) from tenk1 a where unique1 in<br>  (select unique1 from tenk1 b join tenk1 c using (unique1)<br>   where b.unique2 = 42); | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 112 |
| pg-join-0123-7ae195fb | select count(*)<br>from<br>  (select t3.tenthous as x1, coalesce(t1.stringu1, t2.stringu1) as x2<br>   from tenk1 t1<br>   left join tenk1 t2 on t1.unique1 = t2.unique1<br>   join tenk1 t3 on t1.unique2 = t3.unique2) ss,<br>  tenk1 t4,<br>  tenk1 t5<br>where t4.thousand = t5.unique1 and ss.x1 = t4.tenthous and ss.x2 = t5.stringu1; | [.out](../../../../../../cases/postgres/manual/current/assets/join.out)，语句 123 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

