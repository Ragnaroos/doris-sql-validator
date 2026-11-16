# timestamp：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 25 | 10 | 15 | 0 | 10 |


[YAML](../../../../../../cases/postgres/manual/current/timestamp.yaml)；[首轮 Markdown](../../../validation/timestamp/validation.md) / [首轮 JSON](../../../validation/timestamp/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-timestamp-0027-1be25b6e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 27，源行 52–52，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT timestamp 'infinity' = timestamp '+infinity' AS t;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('infinity' AS DATETIME) = CAST('+infinity' AS DATETIME) AS t
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

### pg-timestamp-0118-05aabd49

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 118，源行 183–200，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2001-01-01') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts);
~~~

社区生成 SQL：


~~~sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2001-01-01' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393' AS DATETIME) AS ts) AS ts
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0119-8bf34e86

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 119，源行 202–217，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2000-01-01 BC') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts);
~~~

社区生成 SQL：


~~~sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2000-01-01 BC' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('0055-6-10 15:44:17.71393 BC' AS DATETIME) AS ts) AS ts
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0120-0f80102f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 120，源行 219–234，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2020-03-02') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts);
~~~

社区生成 SQL：


~~~sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2020-03-02' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393' AS DATETIME) AS ts) AS ts
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0121-e7cf5cac

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 121，源行 236–251，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '0055-06-17 BC') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts);
~~~

社区生成 SQL：


~~~sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('0055-06-17 BC' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('0055-6-10 15:44:17.71393 BC' AS DATETIME) AS ts) AS ts
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0138-6926e893

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 138，源行 335–336，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT date_part('epoch', '294270-01-01 00:00:00'::timestamp);
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=fa96f007cc2f58ad729921b10e3c99c3917119298c295f0f6fc446bcd1d886d6",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['9224097091200']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0139-6926e893

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 139，源行 337–337，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT extract(epoch from '294270-01-01 00:00:00'::timestamp);
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=be17ef27642d4d534c831c522f2b297097c579a2b250db7d35c48d615a82bc39",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['9224097091200.000000']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME));
~~~

实际证据：[probe-01 JSON](../evidence/pg-timestamp-0139-6926e893/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-timestamp-0139-6926e893/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: numeric → decimalv3(12,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 | 1: numeric → decimalv3(12,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(12,0)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-timestamp-0140-b552f818

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 140，源行 338–339，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT extract(epoch from '5000-01-01 00:00:00'::timestamp);
~~~

社区生成 SQL：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('5000-01-01 00:00:00' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=92479be4d755b12ce19c75d034b5f8d790901bfa87d82643c4adb3d5d27e3eb6",
    "doris_digest=940d05aa61c0c5006246e7fc37301701c2c7738ede8fa83dcc39c7b0f80a5cd6",
    "source_sample=[['95617584000.000000']]",
    "doris_sample=[['95617584000']]"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT UNIX_TIMESTAMP(CAST('5000-01-01 00:00:00' AS DATETIME));
~~~

实际证据：[probe-01 JSON](../evidence/pg-timestamp-0140-b552f818/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-timestamp-0140-b552f818/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 一致 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: numeric → decimalv3(12,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 | 1: numeric → decimalv3(12,0)，逻辑=一致，声明=不同，精度/小数位=信息不足 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "numeric",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "numeric",<br>      "Doris原生类型": "decimalv3(12,0)",<br>      "逻辑类型": "一致",<br>      "类型声明": "不同",<br>      "精度与小数位": "信息不足"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-timestamp-0154-25ff4879

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 154，源行 379–385，同文回显第 1 次；历史成功 4 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT to_char(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS US')
   FROM (VALUES
       ('2018-11-02 12:34:56'::timestamp),
       ('2018-11-02 12:34:56.78'),
       ('2018-11-02 12:34:56.78901'),
       ('2018-11-02 12:34:56.78901234')
   ) d(d);
~~~

社区生成 SQL：


~~~sql
SELECT DATE_FORMAT(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS %f') FROM (SELECT CAST('2018-11-02 12:34:56' AS DATETIME) AS d UNION ALL SELECT '2018-11-02 12:34:56.78' UNION ALL SELECT '2018-11-02 12:34:56.78901' UNION ALL SELECT '2018-11-02 12:34:56.78901234') AS d
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=40d62622f3e1c86b50daee611b03b496795000f5304d3c1678603b03924cb424",
    "doris_digest=b6a6ad0e33ab57bc07b15cbad9627b82b02b8460156928023c7eabfb6b527b5b",
    "source_sample=[['0 00 000 0000 00000 000000  0 00 000 0000 00000 000000  000 000000'], ['7 78 780 7800 78000 780000  7 78 780 7800 78000 780000  780 780000'], ['7 78 789 7890 78901 789010  7 78 789 7890 78901 789010  789 789010'], ['7 78 789 7890 78901 789012  7 78 789 7890 78901 789012  789 789012']]",
    "doris_sample=[['FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 000000'], ['FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 780000'], ['FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 789010'], ['FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 789012']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-timestamp-0155-9edb681d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)；原语句 155，源行 387–391，同文回显第 1 次；历史成功 27 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT i,
       to_char(i * interval '1mon', 'rm'),
       to_char(i * interval '1mon', 'RM')
    FROM generate_series(-13, 13) i;
~~~

社区生成 SQL：


~~~sql
SELECT i, DATE_FORMAT(i * INTERVAL '1' MON, 'rm'), DATE_FORMAT(i * INTERVAL '1' MON, 'RM') FROM GENERATE_SERIES(-13, 13) AS i
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MON' expecting {'.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DIV', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'NOT', 'OR', 'QUARTER', 'REGEXP', 'RLIKE', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'XOR', 'YEAR', 'YEAR_MONTH', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 39)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input 'MON' expecting {'.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DIV', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'NOT', 'OR', 'QUARTER', 'REGEXP', 'RLIKE', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'XOR', 'YEAR', 'YEAR_MONTH', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 39)\\n\")",
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
| pg-timestamp-0103-b15d0320 / SELECT '4714-11-23 23:59:59 BC'::timestamp; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 103 | timestamp out of range: "4714-11-23 23:59:59 BC" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0105-fb1ad90f / SELECT '294277-01-01 00:00:00'::timestamp; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 105 | timestamp out of range: "294277-01-01 00:00:00" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0115-612735d5 / SELECT date_trunc( 'timezone', timestamp '2004-02-29 15:44:17.71393' ) AS notsupp_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 115 | unit "timezone" not supported for type timestamp without time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0116-868084d4 / SELECT date_trunc( 'timezone', timestamp 'infinity' ) AS notsupp_inf_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 116 | unit "timezone" not supported for type timestamp without time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0117-374aee7b / SELECT date_trunc( 'ago', timestamp 'infinity' ) AS invalid_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 117 | unit "ago" not recognized for type timestamp without time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0125-8dbc1989 / SELECT date_bin('5 months'::interval, timestamp '2020-02-01 01:01:01', timestamp '2001-01-01'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 125 | timestamps cannot be binned into intervals containing months or years | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0126-5ab4dd7e / SELECT date_bin('5 years'::interval,  timestamp '2020-02-01 01:01:01', timestamp '2001-01-01'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 126 | timestamps cannot be binned into intervals containing months or years | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 34)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0127-14367d1f / SELECT date_bin('0 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 127 | stride must be greater than zero | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 33)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0128-5938d3b4 / SELECT date_bin('-2 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 128 | stride must be greater than zero | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 34)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0129-490e00ba / select date_bin('15 minutes'::interval, timestamp '294276-12-30', timestamp '4000-12-20 BC'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 129 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 37)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0130-3e4d2c86 / select date_bin('200000000 days'::interval, '2024-02-01'::timestamp, '2024-01-01'::timestamp); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 130 | interval out of range | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 41)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0142-dd28e983 / SELECT timestamp '294276-12-31 23:59:59' - timestamp '1999-12-23 19:59:04.224192' AS overflows; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 142 | interval out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0158-b3cd5d0a / select make_timestamp(0, 7, 15, 12, 30, 15); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 158 | date field value out of range: 0-07-15 | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'TIMESTAMP_FROM_PARTS'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0161-66dc7cce / select * from generate_series('2020-01-01 00:00'::timestamp,<br>                              '2020-01-02 03:00'::timestamp,<br>                              '0 hour'::interval); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 161 | step size cannot equal zero | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 34)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamp-0162-9c7414dd / select generate_series(timestamp '1995-08-06 12:12:12', timestamp '1996-08-06 12:12:12', interval 'infinity'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamp.out)，语句 162 | step size cannot be infinite | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at ')'(line 1, pos 129)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

