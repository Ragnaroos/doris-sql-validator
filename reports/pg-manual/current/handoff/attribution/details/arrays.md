# arrays：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 65 | 56 | 9 | 0 | 56 |


[YAML](../../../../../../cases/postgres/manual/current/arrays.yaml)；[首轮 Markdown](../../../validation/arrays/validation.md) / [首轮 JSON](../../../validation/arrays/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-arrays-0036-7d12e6be

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 36，源行 122–123，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{{1,2,3},{4,5,6},{7,8,9}}'::int[];
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{{1,2,3},{4,5,6},{7,8,9}}' AS ARRAY<INT>)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=3196cd60dc5e76b6b6c5849ed2c2789852b343279e364d90607f9fc99c8cc34b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['{{1,2,3},{4,5,6},{7,8,9}}']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0037-fa7e96c0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 37，源行 124–124，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select ('{{1,2,3},{4,5,6},{7,8,9}}'::int[])[1:2][2];
~~~

社区生成 SQL：


~~~sql
SELECT (CAST('{{1,2,3},{4,5,6},{7,8,9}}' AS ARRAY<INT>))[1:2][1]
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=472927cd3e2f6b5e46eb4c9149d1183fee687d6f8f4d9e49c84b5b1af1865799",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['{{1,2},{4,5}}']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0038-4f0e4a0d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 38，源行 125–125，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[0:2][0:2]={{1,2,3},{4,5,6},{7,8,9}}'::int[];
~~~

社区生成 SQL：


~~~sql
SELECT CAST('[0:2][0:2]={{1,2,3},{4,5,6},{7,8,9}}' AS ARRAY<INT>)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e3851d28eb72df3e928fec5a7b5c8d6347fd7dee6b6aae88cbd7f4765dee8e4a",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['[0:2][0:2]={{1,2,3},{4,5,6},{7,8,9}}']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0039-c4ef99ba

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 39，源行 126–126，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select ('[0:2][0:2]={{1,2,3},{4,5,6},{7,8,9}}'::int[])[1:2][2];
~~~

社区生成 SQL：


~~~sql
SELECT (CAST('[0:2][0:2]={{1,2,3},{4,5,6},{7,8,9}}' AS ARRAY<INT>))[1:2][1]
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=119b3b947f3a49de6a7836a82b91838d728571c7a212186a27ddeb4fbf911d96",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['{{5,6},{8,9}}']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0129-97df5e76

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 129，源行 268–271，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT t.f[1][3][1] AS "131", t.f[2][2][1] AS "221" FROM (
  SELECT ARRAY[[[111,112],[121,122],[131,132]],[[211,212],[221,122],[231,232]]] AS f
) AS t;
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 6 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT t.f[0][2][0] AS `131`, t.f[1][1][0] AS `221` FROM (SELECT ARRAY(ARRAY(ARRAY(111, 112), ARRAY(121, 122), ARRAY(131, 132)), ARRAY(ARRAY(211, 212), ARRAY(221, 122), ARRAY(231, 232))) AS f) AS t;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0129-97df5e76/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0129-97df5e76/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → smallint，逻辑=一致，声明=不同，精度/小数位=不适用；2: int4 → smallint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "smallint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "smallint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0130-1a544234

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 130，源行 272–272，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[[[[[['hello'],['world']]]]]];
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 4 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY(ARRAY(ARRAY(ARRAY(ARRAY(ARRAY('hello'), ARRAY('world'))))));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0130-1a544234/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0130-1a544234/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _text → array<array<array<array<array<array<varchar(5)>>>>>>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "_text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "array<array<array<array<array<array<varchar(5)>>>>>>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0131-c7124ae8

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 131，源行 273–273，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[ARRAY['hello'],ARRAY['world']];
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY(ARRAY('hello'), ARRAY('world'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0131-c7124ae8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0131-c7124ae8/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _text → array<array<varchar(5)>>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "_text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "array<array<varchar(5)>>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0133-10846546

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 133，源行 276–277，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '{1,null,3}'::int[];
~~~

社区生成 SQL：


~~~sql
SELECT CAST('{1,null,3}' AS ARRAY<INT>)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=6bcc73f66142af242ebf0bbd055a068d365799907a4a9f720e1103c49eb13519",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['{1,NULL,3}']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0134-9c537f22

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 134，源行 278–278，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[1,NULL,3];
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY(1, NULL, 3);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0134-9c537f22/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0134-9c537f22/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → array<tinyint>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "array<tinyint>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0135-33e4f75c

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 135，源行 280–281，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_append(array[42], 6) AS "{42,6}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_APPEND(ARRAY(42), 6) AS `{42,6}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0135-33e4f75c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0135-33e4f75c/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → array<tinyint>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "array<tinyint>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0136-911e2fbc

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 136，源行 282–282，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_prepend(6, array[42]) AS "{6,42}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_PREPEND(ARRAY(42), 6) AS `{6,42}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0136-911e2fbc/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0136-911e2fbc/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_PREPEND'\")"
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

### pg-arrays-0137-c6d3924c

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 137，源行 283–283，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_cat(ARRAY[1,2], ARRAY[3,4]) AS "{1,2,3,4}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_CONCAT(ARRAY(1, 2), ARRAY(3, 4)) AS `{1,2,3,4}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0137-c6d3924c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0137-c6d3924c/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → array<tinyint>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "array<tinyint>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0138-ae9e4f97

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 138，源行 284–284，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_cat(ARRAY[1,2], ARRAY[[3,4],[5,6]]) AS "{{1,2},{3,4},{5,6}}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 1 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_CONCAT(ARRAY(1, 2), ARRAY(ARRAY(3, 4), ARRAY(5, 6))) AS `{{1,2},{3,4},{5,6}}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0138-ae9e4f97/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0138-ae9e4f97/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = AnyDataType can not cast to catalog data type')"
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

### pg-arrays-0139-8147b663

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 139，源行 285–285，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_cat(ARRAY[[3,4],[5,6]], ARRAY[1,2]) AS "{{3,4},{5,6},{1,2}}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 1 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_CONCAT(ARRAY(ARRAY(3, 4), ARRAY(5, 6)), ARRAY(1, 2)) AS `{{3,4},{5,6},{1,2}}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0139-8147b663/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0139-8147b663/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = AnyDataType can not cast to catalog data type')"
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

### pg-arrays-0140-1ae879f3

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 140，源行 287–287，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position(ARRAY[1,2,3,4,5], 4);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ARRAY(1, 2, 3, 4, 5), 4);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0140-1ae879f3/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0140-1ae879f3/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0141-e83ebde6

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 141，源行 288–288，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position(ARRAY[5,3,4,2,1], 4);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ARRAY(5, 3, 4, 2, 1), 4);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0141-e83ebde6/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0141-e83ebde6/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0143-d4ff47e9

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 143，源行 290–290，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position(ARRAY['sun','mon','tue','wed','thu','fri','sat'], 'mon');
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ARRAY('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'), 'mon');
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0143-d4ff47e9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0143-d4ff47e9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0144-215ce358

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 144，源行 291–291，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position(ARRAY['sun','mon','tue','wed','thu','fri','sat'], 'sat');
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ARRAY('sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat'), 'sat');
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0144-215ce358/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0144-215ce358/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0146-1dba32e8

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 146，源行 293–293，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position(ARRAY['sun','mon','tue','wed','thu',NULL,'fri','sat'], NULL);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ARRAY('sun', 'mon', 'tue', 'wed', 'thu', NULL, 'fri', 'sat'), NULL);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0146-1dba32e8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0146-1dba32e8/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: int4 → bigint，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "bigint",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0150-c883f965

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 150，源行 298–298，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_positions(ARRAY[1,2,3,4,5,6,1,2,3,4,5,6], 4);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITIONS(ARRAY(1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6), 4);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0150-c883f965/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0150-c883f965/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_POSITIONS'\")"
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

### pg-arrays-0152-5f46c961

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 152，源行 300–300，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_positions(ARRAY[1,2,3,4,5,6,1,2,3,4,5,6], NULL);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITIONS(ARRAY(1, 2, 3, 4, 5, 6, 1, 2, 3, 4, 5, 6), NULL);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0152-5f46c961/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0152-5f46c961/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_POSITIONS'\")"
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

### pg-arrays-0153-1bce402b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 153，源行 301–301，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_positions(ARRAY[1,2,3,NULL,5,6,1,2,3,NULL,5,6], NULL);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITIONS(ARRAY(1, 2, 3, NULL, 5, 6, 1, 2, 3, NULL, 5, 6), NULL);
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0153-1bce402b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0153-1bce402b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_POSITIONS'\")"
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

### pg-arrays-0154-879640d2

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 154，源行 302–304，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_length(array_positions(ARRAY(SELECT 'AAAAAAAAAAAAAAAAAAAAAAAAA'::text || i % 10
                                          FROM generate_series(1,100) g(i)),
                                  'AAAAAAAAAAAAAAAAAAAAAAAAA5'), 1);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

首次候选构造失败（即使后续成功仍保留）：


~~~text
诊断尚未实现 ARRAY 查询构造器
~~~

实际证据：没有完整工具证据。

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

### pg-arrays-0156-819bf833

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 156，源行 320–320，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_position('[2:4]={1,2,3}'::int[], 1);
~~~

社区生成 SQL：


~~~sql
SELECT ARRAY_POSITION(CAST('[2:4]={1,2,3}' AS ARRAY<INT>), 1)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a0a88ee57364f8f632469bb45e2fd5057419c8c1c1f6d52216176988ab0fbb90",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['2']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0157-529928e3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 157，源行 321–321，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_positions('[2:4]={1,2,3}'::int[], 1);
~~~

社区生成 SQL：


~~~sql
SELECT ARRAY_POSITIONS(CAST('[2:4]={1,2,3}' AS ARRAY<INT>), 1)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'ARRAY_POSITIONS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_POSITIONS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0158-76e9e56b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 158，源行 323–330，同文回显第 1 次；历史成功 2 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
    array_position(ids, (1, 1)),
    array_positions(ids, (1, 1))
        FROM
(VALUES
    (ARRAY[(0, 0), (1, 1)]),
    (ARRAY[(1, 1)])
) AS f (ids);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT ARRAY_POSITION(ids, (1, 1)), ARRAY_POSITIONS(ids, (1, 1)) FROM (SELECT ARRAY((0, 0), (1, 1)) AS ids UNION ALL SELECT ARRAY((1, 1))) AS f;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0158-76e9e56b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0158-76e9e56b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "int4",<br>      "Doris原生类型": "int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    },<br>    {<br>      "字段位置": 2,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nmissing ')' at ','(line 1, pos 29)\\n\")"
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

### pg-arrays-0160-d80d5020

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 160，源行 334–334，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT NOT ARRAY[1.1,1.2,1.3] = ARRAY[1.1,1.2,1.3] AS "FALSE";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT NOT ARRAY(1.1, 1.2, 1.3) = ARRAY(1.1, 1.2, 1.3) AS `FALSE`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0160-d80d5020/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0160-d80d5020/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0161-c1ad99d8

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 161，源行 335–335，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[1,2] || 3 AS "{1,2,3}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(ARRAY(1, 2), 3) AS `{1,2,3}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0161-c1ad99d8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0161-c1ad99d8/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → varchar(7)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "varchar(7)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0162-94f706e5

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 162，源行 336–336，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 0 || ARRAY[1,2] AS "{0,1,2}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(0, ARRAY(1, 2)) AS `{0,1,2}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0162-94f706e5/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0162-94f706e5/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → varchar(7)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "varchar(7)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0163-7e801567

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 163，源行 337–337，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[1,2] || ARRAY[3,4] AS "{1,2,3,4}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(ARRAY(1, 2), ARRAY(3, 4)) AS `{1,2,3,4}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0163-7e801567/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0163-7e801567/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → varchar(12)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "varchar(12)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0164-eba9ca06

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 164，源行 338–338，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[[['hello','world']]] || ARRAY[[['happy','birthday']]] AS "ARRAY";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 3 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(ARRAY(ARRAY(ARRAY('hello', 'world'))), ARRAY(ARRAY(ARRAY('happy', 'birthday')))) AS `ARRAY`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0164-eba9ca06/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0164-eba9ca06/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _text → varchar(47)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "_text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "varchar(47)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0165-befda27f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 165，源行 339–339，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[[1,2],[3,4]] || ARRAY[5,6] AS "{{1,2},{3,4},{5,6}}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 1 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(ARRAY(ARRAY(1, 2), ARRAY(3, 4)), ARRAY(5, 6)) AS `{{1,2},{3,4},{5,6}}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0165-befda27f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0165-befda27f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → varchar(22)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "varchar(22)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0166-8cc7f264

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 166，源行 340–340，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[0,0] || ARRAY[1,1] || ARRAY[2,2] AS "{0,0,1,1,2,2}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CONCAT(ARRAY(0, 0), ARRAY(1, 1), ARRAY(2, 2)) AS `{0,0,1,1,2,2}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0166-8cc7f264/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0166-8cc7f264/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _int4 → varchar(18)，逻辑=不同，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "_int4",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_int4",<br>      "Doris原生类型": "varchar(18)",<br>      "逻辑类型": "不同",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0169-b96c5dcc

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 169，源行 343–343，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_agg(x) || array_agg(x) FROM (VALUES (ROW(1,2)), (ROW(3,4))) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT CONCAT(COLLECT_LIST(x), COLLECT_LIST(x)) FROM (SELECT ROW(1, 2) AS x UNION ALL SELECT ROW(3, 4)) AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 61)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 61)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0170-6f9b07e0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 170，源行 344–344，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ROW(1,2) || array_agg(x) FROM (VALUES (ROW(3,4)), (ROW(5,6))) v(x);
~~~

社区生成 SQL：


~~~sql
SELECT CONCAT(ROW(1, 2), COLLECT_LIST(x)) FROM (SELECT ROW(3, 4) AS x UNION ALL SELECT ROW(5, 6)) AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 14)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 14)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0197-7667c505

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 197，源行 374–375，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[1,2,3]::text[]::int[]::float8[] AS "{1,2,3}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CAST(CAST(CAST(ARRAY(1, 2, 3) AS ARRAY<STRING>) AS ARRAY<INT>) AS ARRAY<DOUBLE>) AS `{1,2,3}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0197-7667c505/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0197-7667c505/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _float8 → array<double>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_float8",<br>      "Doris原生类型": "_float8",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_float8",<br>      "Doris原生类型": "array<double>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0199-5d28259f

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 199，源行 377–377，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ARRAY[['a','bc'],['def','hijk']]::text[]::varchar[] AS "{{a,bc},{def,hijk}}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CAST(CAST(ARRAY(ARRAY('a', 'bc'), ARRAY('def', 'hijk')) AS ARRAY<STRING>) AS ARRAY<VARCHAR>) AS `{{a,bc},{def,hijk}}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0199-5d28259f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0199-5d28259f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _varchar → array<varchar(65533)>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_varchar",<br>      "Doris原生类型": "_varchar",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_varchar",<br>      "Doris原生类型": "array<varchar(65533)>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0201-43f9dae0

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 201，源行 379–379，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CAST(ARRAY[[[[[['a','bb','ccc']]]]]] as text[]) as "{{{{{{a,bb,ccc}}}}}}";
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL

... and 3 more
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT CAST(ARRAY(ARRAY(ARRAY(ARRAY(ARRAY(ARRAY('a', 'bb', 'ccc')))))) AS ARRAY<STRING>) AS `{{{{{{a,bb,ccc}}}}}}`;
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0201-43f9dae0/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0201-43f9dae0/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 一致 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: _text → array<text>，逻辑=一致，声明=不同，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "_text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "_text",<br>      "Doris原生类型": "array<text>",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0203-533b91c4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 203，源行 382–383，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 = any ('{1,2,3}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 = ANY('{1,2,3}')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['f']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0204-d5036a68

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 204，源行 384–384，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 = any ('{1,2,33}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 = ANY('{1,2,33}')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c1fc917cb0eae91bab50aa5654d09e17cec3656dd19d850587d575060c14665b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['t']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0205-0a9de597

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 205，源行 385–385，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 = all ('{1,2,33}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 = ALL('{1,2,33}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 12)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 12)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0206-4bb30472

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 206，源行 386–386，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 >= all ('{1,2,33}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 >= ALL('{1,2,33}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 13)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 13)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0208-cc4455d7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 208，源行 389–389，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select null::int >= all ('{}');
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS INT) >= ALL('{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0209-9298267b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 209，源行 390–390，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select null::int >= any ('{}');
~~~

社区生成 SQL：


~~~sql
SELECT CAST(NULL AS INT) >= ANY('{}')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['f']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0210-f27d4da8

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 210，源行 391–392，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33.4 = any (array[1,2,3]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 33.4 = ANY(ARRAY(1, 2, 3));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0210-f27d4da8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0210-f27d4da8/probe-01/probe-report.md)。

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
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = unsupported comparison predicate (33.4 = any_value(array(1, 2, 3)))')"
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

### pg-arrays-0211-3e580130

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 211，源行 393–393，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33.4 > all (array[1,2,3]);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 33.4 > ALL(ARRAY(1, 2, 3));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0211-3e580130/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0211-3e580130/probe-01/probe-report.md)。

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
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 14)\\n\")"
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

### pg-arrays-0217-0d45cd6b

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 217，源行 401–401，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 = any ('{1,null,33}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 = ANY('{1,null,33}')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c1fc917cb0eae91bab50aa5654d09e17cec3656dd19d850587d575060c14665b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['t']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0220-dabf973c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 220，源行 404–404，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 33 = all ('{1,null,3}');
~~~

社区生成 SQL：


~~~sql
SELECT 33 = ALL('{1,null,3}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 12)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=PARSE_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 12)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-arrays-0246-58760171

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 246，源行 460–463，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' like any (array['%a', '%o']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' LIKE ANY(ARRAY('%a', '%o'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0246-58760171/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0246-58760171/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0247-933ca919

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 247，源行 463–464，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' like any (array['%a', '%b']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' LIKE ANY(ARRAY('%a', '%b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0247-933ca919/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0247-933ca919/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0248-c6f58b28

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 248，源行 464–465，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' like all (array['f%', '%o']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' LIKE ALL (ARRAY('f%', '%o'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0248-c6f58b28/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0248-c6f58b28/probe-01/probe-report.md)。

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
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 18)\\n\")"
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

### pg-arrays-0249-e2238cac

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 249，源行 465–466，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' like all (array['f%', '%b']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' LIKE ALL (ARRAY('f%', '%b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0249-e2238cac/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0249-e2238cac/probe-01/probe-report.md)。

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
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 18)\\n\")"
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

### pg-arrays-0250-7b229df0

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 250，源行 466–467，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' not like any (array['%a', '%b']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' NOT LIKE ANY(ARRAY('%a', '%b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0250-7b229df0/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0250-7b229df0/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0251-f4b1710d

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 251，源行 467–468，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' not like all (array['%a', '%o']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT 'foo' NOT LIKE ALL (ARRAY('%a', '%o'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0251-f4b1710d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0251-f4b1710d/probe-01/probe-report.md)。

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
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ALL' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 22)\\n\")"
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

### pg-arrays-0252-ce30e209

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 252，源行 468–469，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' ilike any (array['%A', '%O']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT LOWER('foo') LIKE LOWER(ANY(ARRAY('%A', '%O')));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0252-ce30e209/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0252-ce30e209/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

### pg-arrays-0253-be3c6fa6

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)；原语句 253，源行 469–470，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'foo' ilike all (array['F%', '%O']);
~~~

SQLGlot 原错误：


~~~text
UnsupportedError: Arrays are not supported by MySQL
~~~

#### 代码依据、候选与执行

PG-DORIS-001 Doris 数组元素构造器不应沿用 MySQL 的整体禁用：DorisGenerator 继承 array_sql 的 MySQL unsupported；多个成功源查询在到达 Doris 前即被阻断。独立 ARRAY(...) 可以执行，但后续数组索引、聚合和比较未必正确。

代码位置：[sqlglot/generators/mysql.py:654](../../../../../../../sqlglot/sqlglot/generators/mysql.py)（行 654）；[sqlglot/generators/doris.py:26](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 26）。

第一次候选：


~~~sql
SELECT LOWER('foo') LIKE LOWER(ALL (ARRAY('F%', '%O')));
~~~

实际证据：[probe-01 JSON](../evidence/pg-arrays-0253-be3c6fa6/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-arrays-0253-be3c6fa6/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 未执行 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 不同 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


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

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-arrays-0040-3d472683 / SELECT ('{}'::int[])[1][2][3][4][5][6][7]; / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 40 | number of array dimensions (7) exceeds the maximum allowed (6) | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0142-f591dad6 / SELECT array_position(ARRAY[[1,2],[3,4]], 3); / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 142 | searching for elements in multidimensional arrays is not supported | SQLGlot 解析/生成失败；UnsupportedError: Arrays are not supported by MySQL<br><br>Arrays are not supported by MySQL<br><br>Arrays are not supported by MySQL | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0151-a8ec270d / SELECT array_positions(ARRAY[[1,2],[3,4]], 4); / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 151 | searching for elements in multidimensional arrays is not supported | SQLGlot 解析/生成失败；UnsupportedError: Arrays are not supported by MySQL<br><br>Arrays are not supported by MySQL<br><br>Arrays are not supported by MySQL | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0212-7828127c / select 33 * any ('{1,2,3}'); / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 212 | op ANY/ALL (array) requires operator to yield boolean | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0213-6ba3fda2 / select 33 * any (44); / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 213 | op ANY/ALL (array) requires array on right side | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0254-f061d5ef / select '{{1,{2}},{2,3}}'::text[]; / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 254 | malformed array literal: "{{1,{2}},{2,3}}" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0255-5d1db28f / select E'{{1,2},\\{2,3}}'::text[]; / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 255 | malformed array literal: "{{1,2},\{2,3}}" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0256-0c5267b3 / select '{"a"b}'::text[]; / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 256 | malformed array literal: "{"a"b}" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-arrays-0257-dad51229 / select '{a"b"}'::text[]; / [.out](../../../../../../cases/postgres/manual/current/assets/arrays.out)，语句 257 | malformed array literal: "{a"b"}" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

