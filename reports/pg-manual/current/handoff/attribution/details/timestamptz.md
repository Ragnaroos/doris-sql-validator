# timestamptz：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 15 | 2 | 13 | 0 | 2 |


[YAML](../../../../../../cases/postgres/manual/current/timestamptz.yaml)；[首轮 Markdown](../../../validation/timestamptz/validation.md) / [首轮 JSON](../../../validation/timestamptz/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-timestamptz-0029-d176b7af

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)；原语句 29，源行 53–53，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT timestamptz 'infinity' = timestamptz '+infinity' AS t;
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

### pg-timestamptz-0156-7733d5eb

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)；原语句 156，源行 232–246，同文回显第 1 次；历史成功 6 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT
  str,
  interval,
  date_trunc(str, ts, 'Australia/Sydney') = date_bin(interval::interval, ts, timestamp with time zone '2001-01-01+11') AS equal
FROM (
  VALUES
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamptz '2020-02-29 15:44:17.71393+00')) ts (ts);
~~~

社区生成 SQL：


~~~sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2001-01-01+11' AS DATETIME)) AS equal FROM (SELECT 'day' AS str, '1 d' AS `interval` UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393+00' AS DATETIME) AS ts) AS ts
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

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-timestamptz-0067-004efc58 / SELECT '19970710 173201' AT TIME ZONE 'America/Does_not_exist'; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 67 | time zone "America/Does_not_exist" not recognized | SQLGlot 解析/生成失败；UnsupportedError: AT TIME ZONE is not supported by MySQL | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0078-463ca246 / SELECT 'Jan 01 00:00:00 2024 LMT'::timestamptz; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 78 | invalid input syntax for type timestamp with time zone: "Jan 01 00:00:00 2024 LMT" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0133-f2a3bb29 / SELECT '4714-11-23 23:59:59+00 BC'::timestamptz; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 133 | timestamp out of range: "4714-11-23 23:59:59+00 BC" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0136-d60d38d1 / SELECT '294277-01-01 00:00:00+00'::timestamptz; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 136 | timestamp out of range: "294277-01-01 00:00:00+00" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0137-811b7b6e / SELECT '294277-12-31 16:00:00-08'::timestamptz; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 137 | timestamp out of range: "294277-12-31 16:00:00-08" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0147-1d73992e / SELECT date_trunc( 'timezone', timestamp with time zone '2004-02-29 15:44:17.71393' ) AS notsupp_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 147 | unit "timezone" not supported for type timestamp with time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0148-226a4a04 / SELECT date_trunc( 'timezone', timestamp with time zone 'infinity' ) AS notsupp_inf_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 148 | unit "timezone" not supported for type timestamp with time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0149-fd702113 / SELECT date_trunc( 'ago', timestamp with time zone 'infinity' ) AS invalid_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 149 | unit "ago" not recognized for type timestamp with time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0153-e98782eb / SELECT date_trunc('timezone', timestamp with time zone 'infinity', 'GMT') AS notsupp_zone_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 153 | unit "timezone" not supported for type timestamp with time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0155-a8efda7d / SELECT date_trunc('ago', timestamp with time zone 'infinity', 'GMT') AS invalid_zone_trunc; / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 155 | unit "ago" not recognized for type timestamp with time zone | 已有证据未发现差异；(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year\|quarter\|month\|week\|day\|hour\|minute\|second') | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0160-7802bb90 / SELECT date_bin('5 months'::interval, timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 160 | timestamps cannot be binned into intervals containing months or years | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 35)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0161-856f8667 / SELECT date_bin('5 years'::interval,  timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 161 | timestamps cannot be binned into intervals containing months or years | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 34)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-timestamptz-0162-e22468e0 / SELECT date_bin('0 days'::interval, timestamp with time zone '1970-01-01 01:00:00+00' , timestamp with time zone '1970-01-01 00:00:00+00'); / [.out](../../../../../../cases/postgres/manual/current/assets/timestamptz.out)，语句 162 | stride must be greater than zero | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 33)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

