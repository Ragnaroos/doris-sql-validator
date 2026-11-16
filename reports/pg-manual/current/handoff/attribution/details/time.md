# time：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 15 | 8 | 7 | 0 | 8 |


[YAML](../../../../../../cases/postgres/manual/current/time.yaml)；[首轮 Markdown](../../../validation/time/validation.md) / [首轮 JSON](../../../validation/time/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-time-0018-df2485c4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 18，源行 33–34，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT '23:59:59.999999'::time;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('23:59:59.999999' AS TIME)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=9bb1245ead3fedb68084cff56de60ae5571763a6e7709cb5323f959bc6463b8f",
    "doris_digest=96adb1ee47cf191f2ffc7adf394eb7b35978918d861a0068f59463b675478de7",
    "source_sample=[['23:59:59.999999']]",
    "doris_sample=[['1 day, 0:00:00']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0032-ce54a135

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 32，源行 61–64，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MICROSECOND FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=36229b76a49178ca49a99a011201dacc4be3916d1d05cc8054cbed0fad515b8a",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['25575401']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0033-c230bada

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 33，源行 65–65，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MILLISECOND FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MILLISECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLISECOND' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MILLISECOND' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0034-c3c729bb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 34，源行 66–66，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(SECOND      FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(SECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f01d507cbbca214ee363992c2b006a97191a1e640b7fd44fe33797c2f8c1a571",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['25.575401']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0035-71c4492f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 35，源行 67–67，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(MINUTE      FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MINUTE FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8c4aeb54f80801f8ee5810986e91f838ca579deb581c668f0f7d25108ac927ab",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['30']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0036-42ebd4b8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 36，源行 68–68，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(HOUR        FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(HOUR FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=412cf3d771dce5f97db3e44a5a8603bfe7f1f6dc4b6928b864b713513d5ca03b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['13']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0040-341de9e7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 40，源行 71–72，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT EXTRACT(EPOCH       FROM TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=61c5a4847160b2f356fd7584cd494eb6c35141cfcc199da2ca0dbb5aa649ac26",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['48625.575401']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-time-0041-ce54a135

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/time.out)；原语句 41，源行 74–76，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT date_part('microsecond', TIME '2020-05-26 13:30:25.575401');
~~~

社区生成 SQL：


~~~sql
SELECT EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=36229b76a49178ca49a99a011201dacc4be3916d1d05cc8054cbed0fad515b8a",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['25575401']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-time-0022-333b380a / SELECT '24:00:00.01'::time; / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 22 | date/time field value out of range: "24:00:00.01" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0023-aab2582a / SELECT '23:59:60.01'::time; / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 23 | date/time field value out of range: "23:59:60.01" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0024-3f651a00 / SELECT '24:01:00'::time; / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 24 | date/time field value out of range: "24:01:00" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0025-df167988 / SELECT '25:00:00'::time; / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 25 | date/time field value out of range: "25:00:00" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0037-3411a8d0 / SELECT EXTRACT(DAY         FROM TIME '2020-05-26 13:30:25.575401'); / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 37 | unit "day" not supported for type time without time zone | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0038-cc79ba84 / SELECT EXTRACT(FORTNIGHT   FROM TIME '2020-05-26 13:30:25.575401'); / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 38 | unit "fortnight" not recognized for type time without time zone | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'FORTNIGHT' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-time-0039-98f3ca62 / SELECT EXTRACT(TIMEZONE    FROM TIME '2020-05-26 13:30:25.575401'); / [.out](../../../../../../cases/postgres/manual/current/assets/time.out)，语句 39 | unit "timezone" not supported for type time without time zone | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'TIMEZONE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

