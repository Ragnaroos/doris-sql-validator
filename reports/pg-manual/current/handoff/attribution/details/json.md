# json：PostgreSQL → Doris 归因明细

报告日期：2026-11-13。仅重做步骤四，不实施修复。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 100 | 77 | 23 | 12 | 65 |


[YAML](../../../../../../cases/postgres/manual/current/json.yaml)；[首轮 Markdown](../../../validation/json/validation.md) / [首轮 JSON](../../../validation/json/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-json-0010-cb8ffd73

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 10，源行 13–20，同文回显第 1 次；历史成功 38 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(j)::jsonb FROM (
  SELECT left(E'abcdefghijklmnopqrstuv"\twxyz012345678', a) AS a
  FROM generate_series(0,37) a
) j;
~~~

社区生成 SQL：


~~~sql
SELECT CAST(ROW_TO_JSON(j) AS JSONB) FROM (SELECT LEFT('abcdefghijklmnopqrstuv"\twxyz012345678', a) AS a FROM GENERATE_SERIES(0, 37) AS a) AS j
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 127)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting EQ(line 1, pos 127)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0057-738e7b11

- 结论强度：证据不足。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 57，源行 96–99，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json(array(select 1 as a));
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

### pg-json-0058-9bb364f3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 58，源行 100–100，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json(array_agg(q),false) from (select x as b, x * 2 as c from generate_series(1,3) x) q;
~~~

社区生成 SQL：


~~~sql
SELECT ARRAY_TO_JSON(COLLECT_LIST(q), FALSE) FROM (SELECT x AS b, x * 2 AS c FROM GENERATE_SERIES(1, 3) AS x) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 99)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting EQ(line 1, pos 99)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0060-0cb6c97c

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 60，源行 102–107，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json(array_agg(q),false)
  FROM ( SELECT $$a$$ || x AS b, y AS c,
               ARRAY[ROW(x.*,ARRAY[1,2,3]),
               ROW(y.*,ARRAY[4,5,6])] AS z
         FROM generate_series(1,2) x,
              generate_series(4,5) y) q;
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
SELECT ARRAY_TO_JSON(COLLECT_LIST(q), FALSE) FROM (SELECT CONCAT('a', x) AS b, y AS c, ARRAY(ROW(x.*, ARRAY(1, 2, 3)), ROW(y.*, ARRAY(4, 5, 6))) AS z FROM GENERATE_SERIES(1, 2) AS x, GENERATE_SERIES(4, 5) AS y) AS q;
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0060-0cb6c97c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0060-0cb6c97c/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 93)\\n\")"
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

### pg-json-0061-afcbc0b7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 61，源行 108–108，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json(array_agg(x),false) from generate_series(5,10) x;
~~~

社区生成 SQL：


~~~sql
SELECT ARRAY_TO_JSON(COLLECT_LIST(x), FALSE) FROM GENERATE_SERIES(5, 10) AS x
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 67)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ',' expecting EQ(line 1, pos 67)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0062-0fa82900

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 62，源行 109–109，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT array_to_json('{{1,5},{99,100}}'::int[]);
~~~

社区生成 SQL：


~~~sql
SELECT ARRAY_TO_JSON(CAST('{{1,5},{99,100}}' AS ARRAY<INT>))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'ARRAY_TO_JSON'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'ARRAY_TO_JSON'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0063-7e24ac8c

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 63，源行 111–112，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(row(1,'foo'));
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(ROW(1, 'foo'))
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT ROW_TO_JSON(ROW(1, 'foo'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0063-7e24ac8c/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0063-7e24ac8c/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\\n\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\\n\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-json-0064-dce5ae8b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 64，源行 114–120，同文回显第 1 次；历史成功 4 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(q)
FROM (SELECT $$a$$ || x AS b,
         y AS c,
         ARRAY[ROW(x.*,ARRAY[1,2,3]),
               ROW(y.*,ARRAY[4,5,6])] AS z
      FROM generate_series(1,2) x,
           generate_series(4,5) y) q;
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
SELECT ROW_TO_JSON(q) FROM (SELECT CONCAT('a', x) AS b, y AS c, ARRAY(ROW(x.*, ARRAY(1, 2, 3)), ROW(y.*, ARRAY(4, 5, 6))) AS z FROM GENERATE_SERIES(1, 2) AS x, GENERATE_SERIES(4, 5) AS y) AS q;
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0064-dce5ae8b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0064-dce5ae8b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "语法解析失败",
  "程序错误代码": "PARSE_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 70)\\n\")"
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

### pg-json-0068-c724f117

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 68，源行 137–137，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(row((select array_agg(x) as d from generate_series(5,10) x)),false);
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(ROW((SELECT COLLECT_LIST(x) AS d FROM GENERATE_SERIES(5, 10) AS x)), FALSE)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0071-d1f20a64

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 71，源行 149–151，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(timestamp '2014-05-28 12:22:35.614298');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('2014-05-28 12:22:35.614298' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=4ed4e42c33c04e6da47f4052f38f4f3a96b70ab3f3ecf65a1e36decf81c341c8",
    "doris_digest=c68c69bda40cac60f9217f55ac6da9a0eadbbcde767e15302f03d3784ae3c740",
    "source_sample=[['\"2014-05-28T12:22:35.614298\"']]",
    "doris_sample=[['\"2014-05-28 12:22:36\"']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0079-f44824a3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 79，源行 162–162，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(date 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('Infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a1b82863eebd43c7488b2db3942b2466c75d878789d30544f807fe8d57348b8b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0080-bf0070b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 80，源行 163–163，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(date '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('-Infinity' AS DATE))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e5558525f7b7ba2f25fef6b82c21303e4c2023e17495280827849b78eeb4ca2e",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"-infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0081-2bcf40b3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 81，源行 164–164，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(timestamp 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('Infinity' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a1b82863eebd43c7488b2db3942b2466c75d878789d30544f807fe8d57348b8b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0082-82638770

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 82，源行 165–165，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(timestamp '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('-Infinity' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e5558525f7b7ba2f25fef6b82c21303e4c2023e17495280827849b78eeb4ca2e",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"-infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0083-a4e2831c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 83，源行 166–166，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(timestamptz 'Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('Infinity' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a1b82863eebd43c7488b2db3942b2466c75d878789d30544f807fe8d57348b8b",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0084-fcf1ca0f

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 84，源行 167–167，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select to_json(timestamptz '-Infinity');
~~~

社区生成 SQL：


~~~sql
SELECT TO_JSON(CAST('-Infinity' AS DATETIME))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=e5558525f7b7ba2f25fef6b82c21303e4c2023e17495280827849b78eeb4ca2e",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\"-infinity\"']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0089-eb7daff4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 89，源行 186–188，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(q)
FROM (SELECT 'NaN'::float8 AS "float8field") q;
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('NaN' AS DOUBLE) AS `float8field`) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0090-e2fc96bf

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 90，源行 190–191，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(q)
FROM (SELECT 'Infinity'::float8 AS "float8field") q;
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('Infinity' AS DOUBLE) AS `float8field`) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0091-f2eba6f2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 91，源行 193–194，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(q)
FROM (SELECT '-Infinity'::float8 AS "float8field") q;
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('-Infinity' AS DOUBLE) AS `float8field`) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0092-3eab2396

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 92，源行 196–198，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT row_to_json(q)
FROM (SELECT '{"a":1,"b": [2,3,4,"d","e","f"],"c":{"p":1,"q":2}}'::json AS "jsonfield") q;
~~~

社区生成 SQL：


~~~sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('{"a":1,"b": [2,3,4,"d","e","f"],"c":{"p":1,"q":2}}' AS JSON) AS `jsonfield`) AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0124-97d7a8af

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 124，源行 305–305，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[{"b": "c"}, {"b": "cc"}]'::json -> 1;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f09349e33be7894bd8d5a303da628698e0aaae728156824b39ea48b915299a13",
    "doris_digest=f43465d9bf5efce6d59890b33766f59b61d54ded98b2eac04bf3e3bc657c8b6e",
    "source_sample=[['{\"b\": \"cc\"}']]",
    "doris_sample=[['{\"b\":\"cc\"}']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0135-0315e130

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 135，源行 317–317，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[{"b": "c"}, {"b": "cc"}]'::json ->> 1;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=f09349e33be7894bd8d5a303da628698e0aaae728156824b39ea48b915299a13",
    "doris_digest=f43465d9bf5efce6d59890b33766f59b61d54ded98b2eac04bf3e3bc657c8b6e",
    "source_sample=[['{\"b\": \"cc\"}']]",
    "doris_sample=[['{\"b\":\"cc\"}']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]'), NULL, JSON_EXTRACT_STRING(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0135-0315e130/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0135-0315e130/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 不同 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: text → json，逻辑=不同，声明=不同，精度/小数位=不适用 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "不同",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0141-88ef2e6c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 141，源行 324–326，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_ARRAY_LENGTH('[1,2,3,{"f1":1,"f2":[5,6]},4]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0142-f298c4a6

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 142，源行 328–328，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT json_array_length('[]');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_ARRAY_LENGTH('[]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0145-0361b143

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 145，源行 334–336，同文回显第 1 次；历史成功 3 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each(cast(\\'{\"f1\":[1,2,3],\"f2\":{\"f3\":1},\"f4\":null}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0146-a330ea38

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 146，源行 337–337，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 87)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ')' expecting EQ(line 1, pos 87)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0147-25b95a0c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 147，源行 339–339，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each_text(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}\' as JSON))')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each_text(cast(\\'{\"f1\":[1,2,3],\"f2\":{\"f3\":1},\"f4\":null,\"f5\":\"null\"}\\' as JSON))')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0148-6cfaea21

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 148，源行 340–340，同文回显第 1 次；历史成功 5 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 92)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ')' expecting EQ(line 1, pos 92)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0151-c71ce0d8

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 151，源行 346–346，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2', CAST(0 AS STRING))
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0152-73a3e57c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 152，源行 347–347，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2', CAST(1 AS STRING))
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0153-859161a9

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 153，源行 348–348，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6')
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=4ab6c6d09d2097db8226d87cf6e440965b965b379c7026b11464cf815538de90",
    "doris_digest=06390ba898c4e3a89b08d765b51a164b73c4e26114bd70bbe697c89dade6ce8d",
    "source_sample=[['stringy']]",
    "doris_sample=[['\"stringy\"']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6'), NULL, JSON_EXTRACT_STRING('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0153-859161a9/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0153-859161a9/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 未发现需检查的显式别名 | 未发现需检查的显式别名 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: text → json，逻辑=不同，声明=不同，精度/小数位=不适用 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0155-579440b1

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 155，源行 350–350，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', '$.f2[0]'), NULL, JSON_EXTRACT_STRING('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', '$.f2[0]'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0155-579440b1/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0155-579440b1/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0156-f9da221f

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 156，源行 351–351，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text);
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', '$.f2[1]'), NULL, JSON_EXTRACT_STRING('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', '$.f2[1]'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0156-f9da221f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0156-f9da221f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 不同 | 一致 |
| 字段数量 | 未执行 | 一致 |
| 显式别名 | 未执行 | 未发现需检查的显式别名 |
| 记录行数 | 未执行 | 一致 |
| 记录值及重复次数 | 未执行 | 一致 |
| 最终行顺序 | 未执行 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 未取得可用类型 | 1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0158-382f7a2f

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 158，源行 356–356，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}','f4','f5') is null as expect_true;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}', '$.f4.f5') IS NULL AS expect_true
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c1fc917cb0eae91bab50aa5654d09e17cec3656dd19d850587d575060c14665b",
    "doris_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "source_sample=[['t']]",
    "doris_sample=[['f']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}', '$.f4.f5'), NULL, JSON_EXTRACT_STRING('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}', '$.f4.f5')) IS NULL AS expect_true;
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0158-382f7a2f/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0158-382f7a2f/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0160-7531df7d

- 结论强度：已确认（当前样本）。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 160，源行 358–358，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_extract_path_text('{"f2":{"f3":1},"f4":[0,1,2,null]}','f4','3') is null as expect_true;
~~~

社区生成 SQL：


~~~sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]') IS NULL AS expect_true
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c1fc917cb0eae91bab50aa5654d09e17cec3656dd19d850587d575060c14665b",
    "doris_digest=5654a7c216fea9e9ad62a75c66621161751e267d6681767f1c7819530a35dee8",
    "source_sample=[['t']]",
    "doris_sample=[['f']]"
  ]
}
~~~

#### 代码依据、候选与执行

PG-DORIS-005 修正 JSON 文本提取、路径参数和 JSON null：JSONExtractScalar 当前生成 JSON_EXTRACT，丢失文本提取和 JSON null→SQL NULL 语义；json_extract_path_text 的附加路径也未完整生成。

代码位置：[sqlglot/generators/doris.py:75](../../../../../../../sqlglot/sqlglot/generators/doris.py)（行 75）；[sqlglot/parsers/postgres.py:151](../../../../../../../sqlglot/sqlglot/parsers/postgres.py)（行 151）。

第一次候选：


~~~sql
SELECT IF(JSON_EXTRACT_ISNULL('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]'), NULL, JSON_EXTRACT_STRING('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]')) IS NULL AS expect_true;
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0160-7531df7d/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0160-7531df7d/probe-01/probe-report.md)。

#### 最新候选分维度比较


| 比较维度 | 社区 SQL 实际结果 | 独立候选实际结果 |
| :--- | :--- | :--- |
| 执行状态 | 一致 | 一致 |
| 字段数量 | 一致 | 一致 |
| 显式别名 | 一致 | 一致 |
| 记录行数 | 一致 | 一致 |
| 记录值及重复次数 | 不同 | 一致 |
| 最终行顺序 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 | 无最终 ORDER BY，忽略结果行顺序但保留重复次数 |
| 原生/逻辑类型、精度/小数位 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 | 1: bool → boolean，逻辑=一致，声明=一致，精度/小数位=不适用 |
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "bool",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "一致",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "bool",<br>      "Doris原生类型": "boolean",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} |


每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分


| 共享规则变体 | SQL 原件 | 实际结果与限制 |
| :--- | :--- | :--- |
| json-text-json-null | [源 SQL](../evidence/boundaries/json-text-json-null/source.sql) / [候选](../evidence/boundaries/json-text-json-null/candidate.sql) | [probe](../evidence/boundaries/json-text-json-null/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-missing | [源 SQL](../evidence/boundaries/json-text-missing/source.sql) / [候选](../evidence/boundaries/json-text-missing/candidate.sql) | [probe](../evidence/boundaries/json-text-missing/probe/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |
| json-text-string | [源 SQL](../evidence/boundaries/json-text-string/source.sql) / [候选](../evidence/boundaries/json-text-string/candidate.sql) | [probe](../evidence/boundaries/json-text-string/probe/probe-evidence.json)：值与重复次数=不同；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用；[probe-02](../evidence/boundaries/json-text-string/probe-02/probe-evidence.json)：值与重复次数=一致；1: text → text，逻辑=一致，声明=一致，精度/小数位=不适用 |

这些是共享规则的有限变体，不代表所有关联复杂查询都完成逐查询边界测试。

#### 原因、修复条件与下一步

为 Doris 生成适当文本提取并补 JSON null 判断；构造完整路径，区分数组下标与对象键；正确转义目标字符串。 限制：对象输出仍有 {"b": "cc"} 与 {"b":"cc"} 差异。首次手写边界的转义错误已通过第二次候选修正，不能把该候选错误算作 SQLGlot 缺陷。

修复任务：[PG-DORIS-005](../sqlglot-tasks.md)。后续由人选择任务调用修复 Skill，真正修改后的 SQLGlot 生成结果还须回归；候选通过不等于已修复。

### pg-json-0161-635df7fb

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 161，源行 360–362，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f4','f6'];
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
SELECT JSONB_EXTRACT(CAST('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f4', 'f6'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0161-635df7fb/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0161-635df7fb/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "无法可靠归一化，需人工核对：Expecting value: line 1 column 1 (char 0)",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['f4', 'f6']\")"
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

### pg-json-0162-6b380766

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 162，源行 363–363，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2'];
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
SELECT JSONB_EXTRACT(CAST('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0162-6b380766/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0162-6b380766/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['f2']\")"
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

### pg-json-0163-093476ed

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 163，源行 364–364，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','0'];
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
SELECT JSONB_EXTRACT(CAST('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2', '0'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0163-093476ed/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0163-093476ed/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "无法可靠归一化，需人工核对：Expecting value: line 1 column 1 (char 0)",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['f2', '0']\")"
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

### pg-json-0164-0923d889

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 164，源行 365–365，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','1'];
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
SELECT JSONB_EXTRACT(CAST('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2', '1'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0164-0923d889/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0164-0923d889/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['f2', '1']\")"
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

### pg-json-0165-7c004789

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 165，源行 367–367，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f4','f6'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f4', 'f6'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0165-7c004789/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0165-7c004789/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0166-6c15e0b8

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 166，源行 368–368，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0166-6c15e0b8/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0166-6c15e0b8/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0167-f3c33896

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 167，源行 369–369，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','0'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2', '0'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0167-f3c33896/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0167-f3c33896/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0168-d6b16d12

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 168，源行 370–370，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','1'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}' AS JSON), ARRAY('f2', '1'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0168-d6b16d12/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0168-d6b16d12/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0169-9fd69726

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 169，源行 372–373，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0170-8b87c6e3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 170，源行 374–374，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[1,2,3]'::json #> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT(CAST('[1,2,3]' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0171-474250d3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 171，源行 375–375，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '"foo"'::json #> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT(CAST('"foo"' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0172-2baee281

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 172，源行 376–376，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '42'::json #> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT(CAST('42' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0173-95c2a2f0

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 173，源行 377–377，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select 'null'::json #> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT(CAST('null' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
    "doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0174-ff8d41d2

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 174，源行 378–378，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #> array['a'];
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
SELECT JSONB_EXTRACT(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0174-ff8d41d2/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0174-ff8d41d2/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['a']\")"
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

### pg-json-0177-0fec5401

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 177，源行 381–381，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #> array['a','b'];
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
SELECT JSONB_EXTRACT(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a', 'b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0177-0fec5401/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0177-0fec5401/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "json",<br>      "Doris原生类型": "json",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "执行失败，需阅读具体错误",
  "程序错误代码": "EXECUTION_ERROR",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: ['a', 'b']\")"
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

### pg-json-0189-38c2bdc3

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 189，源行 394–394，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT_SCALAR(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0190-1355b395

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 190，源行 395–395，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '[1,2,3]'::json #>> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT_SCALAR(CAST('[1,2,3]' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0191-09aa37c5

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 191，源行 396–396，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '"foo"'::json #>> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT_SCALAR(CAST('"foo"' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 代码依据、候选与执行

本例为原句控制重跑或未形成安全改写；同文重跑不算独立改写，也不证明目标绝对无法模拟。

第一次候选：


~~~sql
SELECT JSONB_EXTRACT_SCALAR(CAST('"foo"' AS JSON), '{}');
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0191-09aa37c5/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0191-09aa37c5/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


社区Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
}
~~~

独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
}
~~~

每次工具记录保存完整有限行及重复次数、类型与重复执行；超时上限 10 秒、结果上限 10,000 行。完整值见 JSON，不只比较五行样本。Float 未自动放宽容差，Decimal 精确比较。

#### 已测边界和未覆盖部分

本规则没有新边界执行记录；不能宣称本例全部边界通过。

#### 原因、修复条件与下一步

只确认本输入的具体目标限制/差异，尚无可验收通用改写；继续核查源操作与可表达类型域，不把 unknown function 一次错误当成绝对不可能模拟。

### pg-json-0192-7c14c3b1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 192，源行 397–397，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '42'::json #>> '{}';
~~~

社区生成 SQL：


~~~sql
SELECT JSONB_EXTRACT_SCALAR(CAST('42' AS JSON), '{}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0194-013c6457

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 194，源行 399–399，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0194-013c6457/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0194-013c6457/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0197-ffab593b

- 结论强度：部分确认。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 197，源行 402–402，同文回显第 1 次；历史成功 1 行。

- 首轮：SQLGlot 解析/生成失败。

#### 源 SQL、社区输出与首轮差异


~~~sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a','b'];
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
SELECT JSONB_EXTRACT_SCALAR(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), ARRAY('a', 'b'));
~~~

实际证据：[probe-01 JSON](../evidence/pg-json-0197-ffab593b/probe-01/probe-evidence.json) / [可读对照](../evidence/pg-json-0197-ffab593b/probe-01/probe-report.md)。

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
| PG 重复稳定性 | {<br>  "执行状态": "一致",<br>  "字段数量": "一致",<br>  "显式别名": "未发现需检查的显式别名",<br>  "字段类型": [<br>    {<br>      "字段位置": 1,<br>      "源原生类型": "text",<br>      "Doris原生类型": "text",<br>      "逻辑类型": "一致",<br>      "类型声明": "一致",<br>      "精度与小数位": "不适用"<br>    }<br>  ],<br>  "记录行数": "一致",<br>  "记录值及重复次数": "一致",<br>  "最终行顺序": "无最终 ORDER BY，忽略结果行顺序但保留重复次数",<br>  "浮点容差": "未自动放宽精确比较；有浮点差异时须另存误差与明确容差策略",<br>  "证据范围": "仅本次输入；未自动验证所有边界、数组下界、排序唯一性及全部类型契约"<br>} | 重复稳定不证明排序键唯一 |
| 候选重复执行后与源比较 | 不适用 | {<br>  "执行状态": "不同",<br>  "错误原因": "一端成功一端失败",<br>  "结果字段和记录": "至少一端没有完整成功结果，未比较"<br>} |


独立Doris实际结果 具体错误：


~~~text
{
  "类别": "函数不存在或调用形式不受支持",
  "程序错误代码": "FUNCTION_NOT_FOUND",
  "异常类": "OperationalError",
  "PostgreSQL标准错误状态码": "HY000",
  "原文": "(1105, \"errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'\")"
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

### pg-json-0209-aeb87cd2

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 209，源行 415–417，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_ARRAY_ELEMENTS('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_ELEMENTS'")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_ELEMENTS'\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0210-22d857f7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 210，源行 418–418，同文回显第 1 次；历史成功 7 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
select * from json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]') q;
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_ARRAY_ELEMENTS('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]') AS q
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 97)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input ')' expecting EQ(line 1, pos 97)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0302-3c69d4c1

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 302，源行 562–562，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT json_populate_record(row(1,2), '{"f1": 0, "f2": 1}');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_POPULATE_RECORD(ROW(1, 2), '{"f1": 0, "f2": 1}')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0303-cbcb2e92

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 303，源行 563–564，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
  json_populate_record(null::record, '{"x": 776}') AS (x int, y int);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_POPULATE_RECORD(CAST(NULL AS record), '{"x": 776}') AS _t0(x INT, y INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting EQ(line 1, pos 39)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0319-8d0c4542

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 319，源行 589–589，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT json_populate_recordset(row(1,2), '[{"f1": 0, "f2": 1}]');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_POPULATE_RECORDSET(ROW(1, 2), '[{"f1": 0, "f2": 1}]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0320-baa89283

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 320，源行 590–591，同文回显第 1 次；历史成功 4 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT i, json_populate_recordset(row(i,50), '[{"f1":"42"},{"f2":"43"}]')
FROM (VALUES (1),(2)) v(i);
~~~

社区生成 SQL：


~~~sql
SELECT i, JSON_POPULATE_RECORDSET(ROW(i, 50), '[{"f1":"42"},{"f2":"43"}]') FROM (SELECT 1 AS i UNION ALL SELECT 2) AS v
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 34)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 34)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0321-520ea364

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 321，源行 592–593，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
  json_populate_recordset(null::record, '[{"x": 776}]') AS (x int, y int);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[{"x": 776}]') AS _t0(x INT, y INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting EQ(line 1, pos 42)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0323-4b6a9697

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 323，源行 597–597，同文回显第 1 次；历史成功 0 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT json_populate_recordset(row(1,2), '[]');
~~~

社区生成 SQL：


~~~sql
SELECT JSON_POPULATE_RECORDSET(ROW(1, 2), '[]')
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-json-0325-eb75b13d

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/json.out)；原语句 325，源行 599–600，同文回显第 1 次；历史成功 0 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT * FROM
  json_populate_recordset(null::record, '[]') AS (x int, y int);
~~~

社区生成 SQL：


~~~sql
SELECT * FROM JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[]') AS _t0(x INT, y INT)
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
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
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nmismatched input '(' expecting EQ(line 1, pos 42)\\n\")",
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
| pg-json-0002-a9391cc9 / SELECT $$''$$::json; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 2 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0004-8c23f394 / SELECT '"abc'::json; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 4 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0005-337abb27 / SELECT '"abc<br>def"'::json; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 5 | invalid input syntax for type json | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0143-0c4db36e / SELECT json_array_length('{"f1":1,"f2":[5,6]}'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 143 | cannot get array length of a non-array | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0144-98130b06 / SELECT json_array_length('4'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 144 | cannot get array length of a scalar | 两端错误表现不同；(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0227-20e44f1c / select * from json_populate_record(row('x',3,'2012-12-31 15:30:56')::jpop,'{"c":[100,200,false],"x":43.2}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 227 | invalid input syntax for type timestamp: "[100,200,false]" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0229-42b1c6de / SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"x": 43.2}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 229 | domain js_int_not_null does not allow null values | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0230-f2548d30 / SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"i": null}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 230 | domain js_int_not_null does not allow null values | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0233-033a5496 / SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": 123}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 233 | expected JSON array | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0236-8da8813f / SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], 2]}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 236 | expected JSON array | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0237-bf9a4bfe / SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], [2, 3]]}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 237 | malformed JSON array | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0240-4b741b3d / SELECT ia1 FROM json_populate_record(NULL::jsrec, '{"ia1": 123}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 240 | expected JSON array | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 41)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0244-a7d926ba / SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": 123}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 244 | expected JSON array | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0245-2664dfc2 / SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": [1, "2", null, 4]}') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 245 | value for domain js_int_array_1d violates check constraint "js_int_array_1d_check" | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0301-4a500f7b / SELECT json_populate_record(null::record, '{"x": 0, "y": 1}'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 301 | could not determine row type for result of json_populate_record | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 41)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0306-96555daa / SELECT json_populate_record(row(1,2)::j_ordered_pair, '{"x": 1, "y": 0}'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 306 | value for domain j_ordered_pair violates check constraint "j_ordered_pair_check" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 33)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0312-8e4d5fdb / select * from json_populate_recordset(row('def',99,null)::jpop,'[{"c":[100,200,300],"x":43.2},{"a":{"z":true},"b":3,"c":"2012-01-20 10:42:53"}]') q; / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 312 | invalid input syntax for type timestamp: "[100,200,300]" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0318-ef190f63 / SELECT json_populate_recordset(null::record, '[{"x": 0, "y": 1}]'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 318 | could not determine row type for result of json_populate_recordset | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0322-407e5563 / SELECT json_populate_recordset(null::record, '[]'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 322 | could not determine row type for result of json_populate_recordset | 已有证据未发现差异；(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 44)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0328-37e9bde0 / SELECT json_populate_recordset(row(1,2)::j_ordered_pair, '[{"x": 1, "y": 0}]'); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 328 | value for domain j_ordered_pair violates check constraint "j_ordered_pair_check" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 36)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0329-6f800f54 / select * from json_populate_recordset(row(0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 329 | function return row and query-specified return row do not match | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0330-2fc0f965 / select * from json_populate_recordset(row(0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 330 | function return row and query-specified return row do not match | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-json-0331-a68233a0 / select * from json_populate_recordset(row(0::int,0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); / [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 331 | function return row and query-specified return row do not match | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-json-0001-ac1e931c | SELECT '""'::json; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 1 |
| pg-json-0003-a8fd7c0f | SELECT '"abc"'::json; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 3 |
| pg-json-0006-91cdacbb | SELECT '"\n\"\\"'::json; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 6 |
| pg-json-0008-e7cb155d | SELECT ('"'\|\|repeat('.', 12)\|\|'abc"')::json; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 8 |
| pg-json-0009-313655d2 | SELECT ('"'\|\|repeat('.', 12)\|\|'abc\n"')::json; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 9 |
| pg-json-0078-eeeb5bc2 | select to_json(date '2014-05-28'); | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 78 |
| pg-json-0127-00bf016f | select '{"a": "c", "b": null}'::json -> 'b'; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 127 |
| pg-json-0149-87b9e9bb | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6'); | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 149 |
| pg-json-0150-61dc1a45 | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f2'); | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 150 |
| pg-json-0154-fc734092 | select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f2'); | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 154 |
| pg-json-0157-3bafa8b8 | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}','f4','f5') is null as expect_false; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 157 |
| pg-json-0159-72282a2d | select json_extract_path('{"f2":{"f3":1},"f4":[0,1,2,null]}','f4','3') is null as expect_false; | [.out](../../../../../../cases/postgres/manual/current/assets/json.out)，语句 159 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

