# subselect：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 32 | 31 | 1 | 19 | 12 |


[YAML](../../../../../../cases/postgres/manual/current/subselect.yaml)；[首轮 Markdown](../../../validation/subselect/validation.md) / [首轮 JSON](../../../validation/subselect/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-subselect-0006-05402195

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 6，源行 16–16，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))));
~~~

社区生成 SQL：


~~~sql
SELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))\n--------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nEvery derived table must have its own alias(line 1, pos 14)\\n\\n== SQL ==\\nSELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))\\n--------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0011-ba931994

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 11，源行 24–24，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT (SELECT ARRAY[1,2,3])[1];
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
SELECT (SELECT ARRAY(1, 2, 3))[0];
~~~

实际证据：[probe-01 JSON](../evidence/pg-subselect-0011-ba931994/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-subselect-0011-ba931994/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-subselect-0012-a01c4e7d

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 12，源行 25–25，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ((SELECT ARRAY[1,2,3]))[2];
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
SELECT ((SELECT ARRAY(1, 2, 3)))[1];
~~~

实际证据：[probe-01 JSON](../evidence/pg-subselect-0012-a01c4e7d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-subselect-0012-a01c4e7d/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-subselect-0013-9ff200d9

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 13，源行 26–26，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT (((SELECT ARRAY[1,2,3])))[3];
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
SELECT (((SELECT ARRAY(1, 2, 3))))[2];
~~~

实际证据：[probe-01 JSON](../evidence/pg-subselect-0013-9ff200d9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-subselect-0013-9ff200d9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → tinyint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "tinyint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-subselect-0023-c39da2ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 23，源行 45–45，同文回显第 1 次；历史成功 8 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM SUBSELECT_TBL;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM SUBSELECT_TBL
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=1d59827fd4630221fbcc89554202d0bb06e2108bcc2d1a00cafeb1de16a1b09f",
    "doris_digest=70719430aa48677c365c79df4201288d458d84db17f1aff9f77d098ab13bc79e",
    "source_sample=[['1', '2', '3'], ['2', '3', '4'], ['3', '4', '5'], ['1', '1', '1'], ['2', '2', '2']]",
    "doris_sample=[['1', '1', '1.0'], ['1', '2', '3.0'], ['2', '2', '2.0'], ['2', '3', '4.0'], ['3', '3', '3.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0027-ce6bb68f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 27，源行 59–62，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT f1, f2
  FROM SUBSELECT_TBL
  WHERE (f1, f2) NOT IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL
                         WHERE f3 IS NOT NULL);
~~~

社区生成 SQL：


~~~sql
SELECT f1, f2 FROM SUBSELECT_TBL WHERE NOT (f1, f2) IN (SELECT f2, CAST(f3 AS INT) FROM SUBSELECT_TBL WHERE f3 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 46)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 46)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0029-428204b5

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 29，源行 70–73，同文回显第 1 次；历史成功 5 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT f1 AS "Correlated Field", f3 AS "Second Field"
  FROM SUBSELECT_TBL upper
  WHERE f1 IN
    (SELECT f2 FROM SUBSELECT_TBL WHERE CAST(upper.f2 AS float) = f3);
~~~

社区生成 SQL：


~~~sql
SELECT f1 AS `Correlated Field`, f3 AS `Second Field` FROM SUBSELECT_TBL AS upper WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE CAST(upper.f2 AS DOUBLE) = f3)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=eecbb0f9360a3639d6859e8df2d67481cb7380c036657a9616fb6d7cd04d7b82",
    "doris_digest=a4a2733742071460f67804d04295ae72584afa7a0c4d6ff53d90affd7b0968d0",
    "source_sample=[['2', '4'], ['3', '5'], ['1', '1'], ['2', '2'], ['3', '3']]",
    "doris_sample=[['1', '1.0'], ['2', '2.0'], ['2', '4.0'], ['3', '3.0'], ['3', '5.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0030-9a523825

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 30，源行 75–78，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT f1 AS "Correlated Field", f3 AS "Second Field"
  FROM SUBSELECT_TBL upper
  WHERE f3 IN (SELECT upper.f1 + f2 FROM SUBSELECT_TBL
               WHERE f2 = CAST(f3 AS integer));
~~~

社区生成 SQL：


~~~sql
SELECT f1 AS `Correlated Field`, f3 AS `Second Field` FROM SUBSELECT_TBL AS upper WHERE f3 IN (SELECT upper.f1 + f2 FROM SUBSELECT_TBL WHERE f2 = CAST(f3 AS INT))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Input slot(s) not in child's output: f1#0 in plan: LogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\nchild output is: [f1#3, f2#4, f3#5]\nplan tree:\nLogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\n+--LogicalFilter[231] ( predicates=(f2#4 = cast(f3#5 as INT)) )\n   +--LogicalOlapScan ( qualified=internal.dsv_pg_manual_20261111.subselect_tbl, indexName=<index_not_selected>, selectedIndexId=1791536387852, preAgg=ON, operativeCol=[], virtualColumns=[] )")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Input slot(s) not in child's output: f1#0 in plan: LogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\\nchild output is: [f1#3, f2#4, f3#5]\\nplan tree:\\nLogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\\n+--LogicalFilter[231] ( predicates=(f2#4 = cast(f3#5 as INT)) )\\n   +--LogicalOlapScan ( qualified=internal.dsv_pg_manual_20261111.subselect_tbl, indexName=<index_not_selected>, selectedIndexId=1791536387852, preAgg=ON, operativeCol=[], virtualColumns=[] )\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0031-e04f71f1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 31，源行 80–83，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT f1 AS "Correlated Field"
  FROM SUBSELECT_TBL
  WHERE (f1, f2) IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL
                     WHERE f3 IS NOT NULL);
~~~

社区生成 SQL：


~~~sql
SELECT f1 AS `Correlated Field` FROM SUBSELECT_TBL WHERE (f1, f2) IN (SELECT f2, CAST(f3 AS INT) FROM SUBSELECT_TBL WHERE f3 IS NOT NULL)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 60)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 60)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0039-b3693cb9

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 39，源行 104–104，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM (SELECT * FROM int4_tbl), (VALUES (123456)) WHERE f1 = column1;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1\n--------------^^^\n')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = \\nEvery derived table must have its own alias(line 1, pos 14)\\n\\n== SQL ==\\nSELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1\\n--------------^^^\\n')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0045-76d8e38c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 45，源行 128–135，同文回显第 1 次；历史成功 6 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ss.f1 AS "Correlated Field", ss.f3 AS "Second Field"
  FROM SUBSELECT_TBL ss
  WHERE f1 NOT IN (SELECT f1+1 FROM INT4_TBL
                   WHERE f1 != ss.f1 AND f1 < 2147483647);
~~~

社区生成 SQL：


~~~sql
SELECT ss.f1 AS `Correlated Field`, ss.f3 AS `Second Field` FROM SUBSELECT_TBL AS ss WHERE NOT f1 IN (SELECT f1 + 1 FROM INT4_TBL WHERE f1 <> ss.f1 AND f1 < 2147483647)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=79f757123b73f571839bb60016b3c33532d570971e29a27f1ddb568804c7e719",
    "doris_digest=f81a1c18cb2d55bfab6f658b63918bd993b3ffca650bfefd8d0572c392a15318",
    "source_sample=[['2', '4'], ['3', '5'], ['2', '2'], ['3', '3'], ['6', '8']]",
    "doris_sample=[['3', '3.0'], ['3', '5.0'], ['2', '2.0'], ['2', '4.0'], ['6', '8.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-subselect-0046-b39798f6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)；原语句 46，源行 137–138，同文回显第 1 次；历史成功 2 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select q1, float8(count(*)) / (select count(*) from int8_tbl)
from int8_tbl group by q1 order by q1;
~~~

社区生成 SQL：


~~~sql
SELECT q1, FLOAT8(COUNT(*)) / (SELECT COUNT(*) FROM int8_tbl) FROM int8_tbl GROUP BY q1 ORDER BY CASE WHEN q1 IS NULL THEN 1 ELSE 0 END, q1
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'FLOAT8'\")",
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
| pg-subselect-0036-11fbffbc / SELECT ROW(1, 2) = (SELECT f1, f2 FROM SUBSELECT_TBL); / [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 36 | more than one row returned by a subquery used as an expression | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 7)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-subselect-0001-648f9c3b | SELECT 1 AS one WHERE 1 IN (SELECT 1); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 1 |
| pg-subselect-0002-a346e17e | SELECT 1 AS zero WHERE 1 NOT IN (SELECT 1); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 2 |
| pg-subselect-0003-cab8488e | SELECT 1 AS zero WHERE 1 IN (SELECT 2); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 3 |
| pg-subselect-0004-cd72644a | SELECT * FROM (SELECT 1 AS x) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 4 |
| pg-subselect-0005-957b739b | SELECT * FROM ((SELECT 1 AS x)) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 5 |
| pg-subselect-0007-802e47b9 | (SELECT 2) UNION SELECT 2; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 7 |
| pg-subselect-0009-6719b6f9 | SELECT ((SELECT 2) UNION SELECT 2); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 9 |
| pg-subselect-0010-6011b123 | SELECT (((SELECT 2)) UNION SELECT 2); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 10 |
| pg-subselect-0024-3a618e44 | SELECT f1 AS "Constant Select" FROM SUBSELECT_TBL<br>  WHERE f1 IN (SELECT 1); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 24 |
| pg-subselect-0025-e1d3981a | SELECT f1 AS "Uncorrelated Field" FROM SUBSELECT_TBL<br>  WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 25 |
| pg-subselect-0026-630c97f8 | SELECT f1 AS "Uncorrelated Field" FROM SUBSELECT_TBL<br>  WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE<br>    f2 IN (SELECT f1 FROM SUBSELECT_TBL)); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 26 |
| pg-subselect-0028-5b8190e4 | SELECT f1 AS "Correlated Field", f2 AS "Second Field"<br>  FROM SUBSELECT_TBL upper<br>  WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE f1 = upper.f1); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 28 |
| pg-subselect-0055-7c7828a4 | select count(*) from<br>  (select 1 from tenk1 a<br>   where unique1 IN (select hundred from tenk1 b)) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 55 |
| pg-subselect-0056-ee71a780 | select count(distinct ss.ten) from<br>  (select ten from tenk1 a<br>   where unique1 IN (select hundred from tenk1 b)) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 56 |
| pg-subselect-0057-bf8e16fa | select count(*) from<br>  (select 1 from tenk1 a<br>   where unique1 IN (select distinct hundred from tenk1 b)) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 57 |
| pg-subselect-0058-4e6efae7 | select count(distinct ss.ten) from<br>  (select ten from tenk1 a<br>   where unique1 IN (select distinct hundred from tenk1 b)) ss; | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 58 |
| pg-subselect-0065-a003a0ef | SELECT * FROM foo WHERE id IN<br>    (SELECT id2 FROM (SELECT DISTINCT id1, id2 FROM bar) AS s); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 65 |
| pg-subselect-0066-4489c239 | SELECT * FROM foo WHERE id IN<br>    (SELECT id2 FROM (SELECT id1,id2 FROM bar GROUP BY id1,id2) AS s); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 66 |
| pg-subselect-0067-e7b8bde2 | SELECT * FROM foo WHERE id IN<br>    (SELECT id2 FROM (SELECT id1, id2 FROM bar UNION<br>                      SELECT id1, id2 FROM bar) AS s); | [.out](../../../../../../cases/postgres/manual/current/assets/subselect.out)，语句 67 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

