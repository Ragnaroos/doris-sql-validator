# with：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 11 | 10 | 1 | 5 | 5 |


[YAML](../../../../../../cases/postgres/manual/current/with.yaml)；[首轮 Markdown](../../../validation/with/validation.md) / [首轮 JSON](../../../validation/with/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-with-0003-18c284af

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/with.out)；原语句 3，源行 17–25，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
~~~

社区生成 SQL：


~~~sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT 1) AS _values UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-009 对齐递归 CTE 的锚点和递归列类型：PG 锚点 VALUES(1) 的 INT 语义没有传到 Doris 的最小宽度字面量；当前 Doris 报 TINYINT 锚点与 SMALLINT 递归列不一致。显式双端 INT 的递归候选成功。

代码位置：[sqlglot/generator.py:1610](../../../../../../../sqlglot/sqlglot/generator.py)（行 1610）；[sqlglot/generator.py:1801](../../../../../../../sqlglot/sqlglot/generator.py)（行 1801）；[sqlglot/optimizer/annotate_types.py](../../../../../../../sqlglot/sqlglot/optimizer/annotate_types.py)。

第一次候选：


~~~sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT 1) AS _values UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t;
~~~

后续候选 probe-02：


~~~sql
WITH RECURSIVE t(n) AS (SELECT CAST(1 AS INT) UNION ALL SELECT CAST(n+1 AS INT) FROM t WHERE n<100) SELECT SUM(n) FROM t;
~~~

实际证据：[probe-01 JSON](../evidence/pg-with-0003-18c284af/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-with-0003-18c284af/probe-01/probe-report.md)；[probe-02 JSON](../evidence/pg-with-0003-18c284af/probe-02/probe-evidence.json) / [可读对照](../evidence/pg-with-0003-18c284af/probe-02/probe-report.md)。

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
  "类别": "类型转换失败",
  "程序错误代码": "CAST_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| recursive-cte-integer-anchor | [源 SQL](../evidence/boundaries/recursive-cte-integer-anchor/source.sql) / [候选](../evidence/boundaries/recursive-cte-integer-anchor/candidate.sql) | [probe](../evidence/boundaries/recursive-cte-integer-anchor/probe/probe-evidence.json)：值与重复次数=一致；1: int4 → int，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

在静态可推断的递归列中对齐类型，不全局把每个数字写成 INT；列、NULL、联合和溢出场景说明所需元数据。 限制：不能靠放大/缩小数据或更改递归终止条件绕过问题。

修复任务：[PG-DORIS-009](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-with-0004-599c41ea

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/with.out)；原语句 4，源行 27–32，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH RECURSIVE t(n) AS (
    SELECT (VALUES(1))
UNION ALL
    SELECT n+1 FROM t WHERE n < 5
)
SELECT * FROM t;
~~~

社区生成 SQL：


~~~sql
WITH RECURSIVE t(n) AS (SELECT (VALUES (1)) UNION ALL SELECT n + 1 FROM t WHERE n < 5) SELECT * FROM t
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-with-0028-95f86b76

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/with.out)；原语句 28，源行 182–194，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH RECURSIVE subdepartment(level, id, parent_department, name) AS
(
	-- non recursive term
	SELECT 1, * FROM department WHERE name = 'A'

	UNION ALL

	-- recursive term
	SELECT sd.level + 1, d.* FROM department AS d, subdepartment AS sd
		WHERE d.parent_department = sd.id
)
SELECT * FROM subdepartment ORDER BY name;
~~~

社区生成 SQL：


~~~sql
WITH RECURSIVE subdepartment(`level`, id, parent_department, `name`) AS (/* non recursive term */ SELECT 1, * FROM department WHERE `name` = 'A' UNION ALL /* recursive term */ SELECT sd.`level` + 1, d.* FROM department AS d, subdepartment AS sd WHERE d.parent_department = sd.id) SELECT * FROM subdepartment ORDER BY CASE WHEN `name` IS NULL THEN 1 ELSE 0 END, `name`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-with-0029-22d7351d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/with.out)；原语句 29，源行 196–209，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
WITH RECURSIVE subdepartment(level, id, parent_department, name) AS
(
	-- non recursive term
	SELECT 1, * FROM department WHERE name = 'A'

	UNION ALL

	-- recursive term
	SELECT sd.level + 1, d.* FROM department AS d, subdepartment AS sd
		WHERE d.parent_department = sd.id
)
SELECT * FROM subdepartment WHERE level >= 2 ORDER BY name;
~~~

社区生成 SQL：


~~~sql
WITH RECURSIVE subdepartment(`level`, id, parent_department, `name`) AS (/* non recursive term */ SELECT 1, * FROM department WHERE `name` = 'A' UNION ALL /* recursive term */ SELECT sd.`level` + 1, d.* FROM department AS d, subdepartment AS sd WHERE d.parent_department = sd.id) SELECT * FROM subdepartment WHERE `level` >= 2 ORDER BY CASE WHEN `name` IS NULL THEN 1 ELSE 0 END, `name`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-with-0032-b27e3270

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/with.out)；原语句 32，源行 233–244，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT count(*) FROM (
    WITH RECURSIVE t(n) AS (
        SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 500
    )
    SELECT * FROM t) AS t WHERE n < (
        SELECT count(*) FROM (
            WITH RECURSIVE t(n) AS (
                   SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 100
                )
            SELECT * FROM t WHERE n < 50000
         ) AS t WHERE n < 100);
~~~

社区生成 SQL：


~~~sql
SELECT COUNT(*) FROM (WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 500) SELECT * FROM t) AS t WHERE n < (SELECT COUNT(*) FROM (WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT * FROM t WHERE n < 50000) AS t WHERE n < 100)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype\")",
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
| pg-with-0005-37ebdc8c / WITH RECURSIVE t(n) AS (<br>    VALUES ('01'::varbit)<br>UNION<br>    SELECT n \|\| '10'::varbit FROM t WHERE n < '100'::varbit<br>)<br>SELECT n FROM t; / [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 5 | could not implement recursive UNION | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT CAST('01' AS varbit'(line 1, pos 59)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-with-0001-33ab03b0 | WITH q1(x,y) AS (SELECT 1,2)<br>SELECT * FROM q1, q1 AS q2; | [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 1 |
| pg-with-0027-08d06e3c | WITH RECURSIVE subdepartment AS<br>(<br>	-- non recursive term<br>	SELECT name as root_name, * FROM department WHERE name = 'A'<br><br>	UNION ALL<br><br>	-- recursive term<br>	SELECT sd.root_name, d.* FROM department AS d, subdepartment AS sd<br>		WHERE d.parent_department = sd.id<br>)<br>SELECT * FROM subdepartment ORDER BY name; | [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 27 |
| pg-with-0030-a5b15ec4 | WITH RECURSIVE subdepartment AS<br>(<br>	-- note lack of recursive UNION structure<br>	SELECT * FROM department WHERE name = 'A'<br>)<br>SELECT * FROM subdepartment ORDER BY name; | [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 30 |
| pg-with-0031-3ad31abd | WITH RECURSIVE subdepartment AS<br>(<br>	-- select all columns to prevent projection<br>	SELECT id, parent_department, name FROM department WHERE name = 'A'<br><br>	UNION<br><br>	-- joins do projection<br>	SELECT d.id, d.parent_department, d.name FROM department AS d<br>	INNER JOIN subdepartment AS sd ON d.parent_department = sd.id<br>)<br>SELECT * FROM subdepartment ORDER BY name; | [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 31 |
| pg-with-0033-8592b31e | WITH q1(x,y) AS (<br>    SELECT hundred, sum(ten) FROM tenk1 GROUP BY hundred<br>  )<br>SELECT count(*) FROM q1 WHERE y > (SELECT sum(y)/100 FROM q1 qsub); | [.out](../../../../../../cases/postgres/manual/current/assets/with.out)，语句 33 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

