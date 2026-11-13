# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:34.672539+00:00 至 2026-11-11T09:40:35.691795+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/sqljson_queryfuncs.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**74**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/74 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/55 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**19**；不计入上述成功匹配分子。
- 需要分析的查询：**74**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**74**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 6 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 55 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 13 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 74 条只读查询、跳过 145 条非查询、0 条待确认、145 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 9 | 11–12 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_EXISTS(jsonb '1', 'strict $.a' [4mERROR[0m ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_EXISTS(jsonb '1', 'strict $.a' ERROR [4mON[0m ERROR); |
| 19 | 24–24 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 69.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' [4mPASSING[0m 1 AS x);  Invalid expression / Unexpected token. Line 1, Col: 71.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' PASSING [4m1[0m AS x); |
| 20 | 25–25 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 69.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' [4mPASSING[0m '1' AS x);  Invalid expression / Unexpected token. Line 1, Col: 73.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x)' PASSING [4m'1'[0m AS x); |
| 21 | 26–26 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 79.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' [4mPASSING[0m 0 AS x, 2 AS y);  Invalid expression / Unexpected token. Line 1, Col: 81.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' PASSING [4m0[0m AS x, 2 AS y); |
| 22 | 27–27 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 79.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' [4mPASSING[0m 0 AS x, 1 AS y);  Invalid expression / Unexpected token. Line 1, Col: 81.   SELECT JSON_EXISTS(jsonb '{"a": 1, "b": 2}', '$.* ? (@ > $x && @ < $y)' PASSING [4m0[0m AS x, 1 AS y); |
| 24 | 31–31 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_EXISTS(jsonb '1', '$.a > 2' [4mERROR[0m ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_EXISTS(jsonb '1', '$.a > 2' ERROR [4mON[0m ERROR); |
| 55 | 72–73 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 61 | 79–79 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 62 | 80–80 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 86 | 109–109 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 65.   SELECT JSON_VALUE(jsonb '["1"]', '$[*]' RETURNING int FORMAT [4mJSON[0m); |
| 93 | 122–132 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 5, Col: 28.   SELECT 	x, 	JSON_VALUE( 		jsonb '{"a": 1, "b": 2}', 		'$.* ? (@ > $x)' PASSING [4mx[0m AS x 		RETURNING int 		DEFAULT -1 ON EMPTY 		DEFAULT -2 ON ERROR 	) y FROM 	generate_series(0, 2) x |
| 97 | 148–150 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 34.   SELECT x IS NULL AS is_null,        json_query(x, '$.a' [4mDEFAULT[0m '"empty"' ON EMPTY) AS jq FROM (VALUES ('{}'::jsonb), (NULL), ('{}'::jsonb)) v(x);  Invalid expression / Unexpected token. Line 2, Col: 44.   SELECT x IS NULL AS is_null,        json_query(x, '$.a' DEFAULT [4m'"empty"'[0m ON EMPTY) AS jq FROM (VALUES ('{}'::jsonb), (NULL), ('{}'::jsonb)) v(x); |
| 98 | 152–154 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 39.   SELECT x IS NULL AS is_null,        json_exists(x, 'strict $.a' [4mTRUE[0m ON ERROR) AS je FROM (VALUES ('1'::jsonb), (NULL), ('1'::jsonb)) v(x);  Invalid expression / Unexpected token. Line 2, Col: 42.   SELECT x IS NULL AS is_null,        json_exists(x, 'strict $.a' TRUE [4mON[0m ERROR) AS je FROM (VALUES ('1'::jsonb), (NULL), ('1'::jsonb)) v(x); |
| 100 | 160–160 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a); |
| 101 | 161–161 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a RETURNING point); |
| 102 | 162–162 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mpoint[0m ' (1, 2 )' AS a RETURNING point ERROR ON ERROR); |
| 103 | 164–165 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts); |
| 104 | 166–166 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamptz); |
| 105 | 167–167 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamp); |
| 106 | 168–168 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mdate[0m '2018-02-21 12:34:56 +10' AS ts RETURNING date); |
| 107 | 169–169 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtime[0m '2018-02-21 12:34:56 +10' AS ts RETURNING time); |
| 108 | 170–170 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 52.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimetz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timetz); |
| 109 | 171–171 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 55.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamp[0m '2018-02-21 12:34:56 +10' AS ts RETURNING timestamp); |
| 110 | 173–174 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING json); |
| 111 | 175–175 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_VALUE(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb); |
| 115 | 185–199 | 导入失败；类型 `parse_error` | Expecting ). Line 3, Col: 27.   SELECT 	JSON_QUERY(js, '$') AS "unspec", 	JSON_QUERY(js, '$' [4mWITHOUT[0m WRAPPER) AS "without", 	JSON_QUERY(js, '$' WITH CONDITIONAL WRAPPER) AS "with cond", 	JSON_QUERY(js  Invalid expression / Unexpected token. Line 3, Col: 35.   SELECT 	JSON_QUERY(js, '$') AS "unspec", 	JSON_QUERY(js, '$' WITHOUT [4mWRAPPER[0m) AS "without", 	JSON_QUERY(js, '$' WITH CONDITIONAL WRAPPER) AS "with cond", 	JSON_QUERY(js, '$' WI |
| 116 | 201–218 | 导入失败；类型 `parse_error` | Expecting ). Line 3, Col: 37.   SELECT 	JSON_QUERY(js, 'strict $[*]') AS "unspec", 	JSON_QUERY(js, 'strict $[*]' [4mWITHOUT[0m WRAPPER) AS "without", 	JSON_QUERY(js, 'strict $[*]' WITH CONDITIONAL WRAPPER) AS "with cond", 	JSO  Invalid expression / Unexpected token. Line 3, Col: 45.   SELECT 	JSON_QUERY(js, 'strict $[*]') AS "unspec", 	JSON_QUERY(js, 'strict $[*]' WITHOUT [4mWRAPPER[0m) AS "without", 	JSON_QUERY(js, 'strict $[*]' WITH CONDITIONAL WRAPPER) AS "with cond", 	JSON_QUERY( |
| 117 | 220–220 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text); |
| 118 | 221–221 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES); |
| 119 | 222–222 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES ON SCALAR STRING);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text KEEP QUOTES ON SCALAR STRING); |
| 120 | 223–223 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES); |
| 121 | 224–224 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES ON SCALAR STRING);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m text OMIT QUOTES ON SCALAR STRING); |
| 122 | 225–225 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mOMIT[0m QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"aaa"', '$' OMIT [4mQUOTES[0m ERROR ON ERROR); |
| 123 | 226–226 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m json OMIT QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m json OMIT QUOTES ERROR ON ERROR); |
| 124 | 227–227 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m bytea FORMAT JSON OMIT QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m bytea FORMAT JSON OMIT QUOTES ERROR ON ERROR); |
| 125 | 229–230 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) ERROR ON ERROR); |
| 126 | 231–231 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3));  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3)); |
| 127 | 232–232 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) OMIT QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '"aaa"', '$' [4mRETURNING[0m char(3) OMIT QUOTES ERROR ON ERROR); |
| 128 | 233–233 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT 'bb' ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT 'bb' ON EMPTY); |
| 129 | 234–234 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT '"bb"'::jsonb ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"aaa"', '$.a' [4mRETURNING[0m char(2) OMIT QUOTES DEFAULT '"bb"'::jsonb ON EMPTY); |
| 130 | 236–238 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m WRAPPER OMIT QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 39.   SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m WRAPPER OMIT QUOTES); |
| 131 | 239–239 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m CONDITIONAL WRAPPER OMIT QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 39.   SELECT JSON_QUERY(jsonb '[1]', '$' [4mWITH[0m CONDITIONAL WRAPPER OMIT QUOTES); |
| 132 | 240–241 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m CONDITIONAL WRAPPER KEEP QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m CONDITIONAL WRAPPER KEEP QUOTES); |
| 133 | 242–242 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m UNCONDITIONAL WRAPPER KEEP QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m UNCONDITIONAL WRAPPER KEEP QUOTES); |
| 134 | 243–243 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m WRAPPER KEEP QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITH[0m WRAPPER KEEP QUOTES); |
| 135 | 244–244 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITHOUT[0m WRAPPER OMIT QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 55.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' WITHOUT [4mWRAPPER[0m OMIT QUOTES); |
| 136 | 245–245 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' [4mWITHOUT[0m WRAPPER KEEP QUOTES);  Invalid expression / Unexpected token. Line 1, Col: 55.   SELECT JSON_QUERY(jsonb '["1"]', '$[*]' WITHOUT [4mWRAPPER[0m KEEP QUOTES); |
| 137 | 247–248 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] omit quotes);  Invalid expression / Unexpected token. Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] omit quotes); |
| 138 | 249–249 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes);  Invalid expression / Unexpected token. Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes); |
| 139 | 250–250 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes error on error);  Invalid expression / Unexpected token. Line 1, Col: 62.   SELECT JSON_QUERY(jsonb'{"rec": "{1,2,3}"}', '$.rec' [4mreturning[0m int[] keep quotes error on error); |
| 140 | 251–251 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 60.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range omit quotes);  Invalid expression / Unexpected token. Line 1, Col: 60.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range omit quotes); |
| 141 | 252–252 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 60.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range keep quotes);  Invalid expression / Unexpected token. Line 1, Col: 60.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' [4mreturning[0m int4range keep quotes); |
| 142 | 253–253 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 61.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' 	[4mreturning[0m int4range keep quotes error on error);  Invalid expression / Unexpected token. Line 1, Col: 61.   SELECT JSON_QUERY(jsonb'{"rec": "[1,2]"}', '$.rec' 	[4mreturning[0m int4range keep quotes error on error); |
| 143 | 254–254 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 144 | 255–255 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 145 | 256–256 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_char_domain OMIT QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_char_domain OMIT QUOTES ERROR ON ERROR); |
| 146 | 257–257 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_jsonb_domain OMIT QUOTES ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '"1"', '$' [4mRETURNING[0m qf_jsonb_domain OMIT QUOTES ERROR ON ERROR); |
| 147 | 258–258 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 149 | 261–261 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mNULL[0m ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '[]', '$[*]' NULL [4mON[0m EMPTY); |
| 150 | 262–262 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mON[0m EMPTY); |
| 151 | 263–263 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m ARRAY ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mARRAY[0m ON EMPTY); |
| 152 | 264–264 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mEMPTY[0m OBJECT ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[]', '$[*]' EMPTY [4mOBJECT[0m ON EMPTY); |
| 153 | 265–265 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY); |
| 154 | 266–266 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mDEFAULT[0m '"empty"' ON EMPTY);  Invalid expression / Unexpected token. Line 1, Col: 54.   SELECT JSON_QUERY(jsonb '[]', '$[*]' DEFAULT [4m'"empty"'[0m ON EMPTY); |
| 155 | 268–268 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY NULL ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY NULL ON ERROR); |
| 156 | 269–269 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY EMPTY ARRAY ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY EMPTY ARRAY ON ERROR); |
| 157 | 270–270 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY EMPTY OBJECT ON ERROR); |
| 158 | 271–271 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON EMPTY ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m EMPTY ERROR ON ERROR); |
| 159 | 272–272 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT JSON_QUERY(jsonb '[]', '$[*]' [4mERROR[0m ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[]', '$[*]' ERROR [4mON[0m ERROR); |
| 160 | 272–274 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mERROR[0m ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' ERROR [4mON[0m ERROR); |
| 161 | 275–275 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mDEFAULT[0m '"empty"' ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' DEFAULT [4m'"empty"'[0m ON ERROR); |
| 162 | 277–277 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json); |
| 163 | 278–278 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m json FORMAT JSON); |
| 164 | 279–279 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb); |
| 165 | 280–280 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m jsonb FORMAT JSON); |
| 166 | 281–281 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text); |
| 167 | 282–282 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m char(10));  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m char(10)); |
| 168 | 283–283 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m text FORMAT JSON); |
| 169 | 284–284 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea); |
| 170 | 285–285 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '[1,2]', '$' [4mRETURNING[0m bytea FORMAT JSON); |
| 171 | 287–287 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea EMPTY OBJECT ON ERROR); |
| 172 | 288–288 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea FORMAT JSON EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m bytea FORMAT JSON EMPTY OBJECT ON ERROR); |
| 173 | 289–289 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m json EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m json EMPTY OBJECT ON ERROR); |
| 174 | 290–290 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m jsonb EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mRETURNING[0m jsonb EMPTY OBJECT ON ERROR); |
| 175 | 291–291 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR); |
| 176 | 292–292 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '"[3,4]"', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '"[3,4]"', '$[*]' [4mRETURNING[0m bigint[] EMPTY OBJECT ON ERROR); |
| 177 | 294–295 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 error on error); |
| 178 | 296–296 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int4 error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int4 error on error); |
| 179 | 297–297 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int8 error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int8 error on error); |
| 180 | 298–298 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m bool error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m bool error on error); |
| 181 | 299–299 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m numeric error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m numeric error on error); |
| 182 | 300–300 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m real error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m real error on error); |
| 183 | 301–301 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 error on error); |
| 184 | 302–303 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 omit quotes error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m int2 omit quotes error on error); |
| 185 | 304–304 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 omit quotes error on error);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb '"123.1"', '$' [4mRETURNING[0m float8 omit quotes error on error); |
| 186 | 306–307 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m anyarray EMPTY OBJECT ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 49.   SELECT JSON_QUERY(jsonb '[3,4]', '$[*]' [4mRETURNING[0m anyarray EMPTY OBJECT ON ERROR); |
| 187 | 309–320 | 导入失败；类型 `parse_error` | Expecting ). Line 6, Col: 9.   SELECT 	x, y, 	JSON_QUERY( 		jsonb '[1,2,3,4,5,null]', 		'$[*] ? (@ >= $x && @ <= $y)' 		[4mPASSING[0m x AS x, y AS y 		WITH CONDITIONAL WRAPPER 		EMPTY ARRAY ON EMPTY 	) list FROM 	generate_series(0, 4  Invalid expression / Unexpected token. Line 6, Col: 11.   SELECT 	x, y, 	JSON_QUERY( 		jsonb '[1,2,3,4,5,null]', 		'$[*] ? (@ >= $x && @ <= $y)' 		PASSING [4mx[0m AS x, y AS y 		WITH CONDITIONAL WRAPPER 		EMPTY ARRAY ON EMPTY 	) list FROM 	generate_series(0, 4)  |
| 188 | 322–323 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 189 | 324–324 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc omit quotes);  Invalid expression / Unexpected token. Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc omit quotes); |
| 190 | 325–325 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes);  Invalid expression / Unexpected token. Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes); |
| 191 | 326–326 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes error on error);  Invalid expression / Unexpected token. Line 1, Col: 74.   SELECT JSON_QUERY(jsonb'{"rec": "(abc,42,01.02.2003)"}', '$.rec' [4mreturning[0m comp_abc keep quotes error on error); |
| 192 | 327–327 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 193 | 329–330 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 194 | 331–331 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 195 | 333–333 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec);  Invalid expression / Unexpected token. Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec); |
| 196 | 334–334 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 138.   ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 138.   ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec ERROR ON ERROR); |
| 197 | 335–335 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 138.   ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec);  Invalid expression / Unexpected token. Line 1, Col: 138.   ": "a", "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m sqljsonb_rec); |
| 198 | 336–336 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 114.   T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);  Expecting ). Line 1, Col: 114.   T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);  Expecting ). Line 1, Col: 114.   T * FROM unnest((JSON_QUERY(jsonb '{"jsa":  [{"a": 1, "b": ["foo"]}, {"a": 2, "c": {}}, 123]}', '$' [4mRETURNING[0m sqljsonb_rec)).jsa);  ... and 1 more |
| 199 | 337–337 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 122.    unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);  Expecting ). Line 1, Col: 122.    unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);  Expecting ). Line 1, Col: 122.    unnest((JSON_QUERY(jsonb '{"reca": [{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]}', '$' [4mRETURNING[0m sqljsonb_reca)).reca);  ... and 1 more |
| 200 | 339–339 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath);  Invalid expression / Unexpected token. Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath); |
| 201 | 340–340 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 136.   "a": 1, "b": "foo", "t": "aaa", "js": [1, "2", {}], "jb": {"x": [1, "2", {}]}},  {"a": 2}]', '$[0]' [4mRETURNING[0m jsonpath ERROR ON ERROR); |
| 202 | 342–343 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"3"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"3"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER); |
| 203 | 344–344 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER ERROR ON ERROR); |
| 204 | 345–345 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '[1,2,null,"a"]', '$[*]' [4mRETURNING[0m int[] WITH WRAPPER); |
| 205 | 346–346 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 111.   LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[]));  Expecting ). Line 1, Col: 111.   LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[]));  Invalid expression / Unexpected token. Line 1, Col: 111.   LECT * FROM unnest(JSON_QUERY(jsonb '[{"a": 1, "t": ["foo", []]}, {"a": 2, "jb": [{}, true]}]', '$' [4mRETURNING[0m sqljsonb_rec[])); |
| 206 | 348–349 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.a' [4mRETURNING[0m sqljsonb_int_not_null);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.a' [4mRETURNING[0m sqljsonb_int_not_null); |
| 207 | 350–350 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null); |
| 208 | 351–351 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null ERROR ON EMPTY ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": 1}', '$.b' [4mRETURNING[0m sqljsonb_int_not_null ERROR ON EMPTY ERROR ON ERROR); |
| 209 | 353–354 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts);  Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts); |
| 210 | 355–355 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts RETURNING json);  Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING json); |
| 211 | 356–356 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_QUERY(jsonb 'null', '$ts' [4mPASSING[0m timestamptz '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb);  Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_QUERY(jsonb 'null', '$ts' PASSING [4mtimestamptz[0m '2018-02-21 12:34:56 +10' AS ts RETURNING jsonb); |
| 212 | 358–374 | 跳过非查询；类型 `create` | Expecting ). Line 4, Col: 54.    TABLE test_jsonb_constraints ( 	js text, 	i int, 	x jsonb DEFAULT JSON_QUERY(jsonb '[1,2]', '$[*]' [4mWITH[0m WRAPPER) 	CONSTRAINT test_jsonb_constraint1 		CHECK (js IS JSON) 	CONSTRAINT test_jsonb_constraint2  Expecting (. Line 4, Col: 62.   E test_jsonb_constraints ( 	js text, 	i int, 	x jsonb DEFAULT JSON_QUERY(jsonb '[1,2]', '$[*]' WITH [4mWRAPPER[0m) 	CONSTRAINT test_jsonb_constraint1 		CHECK (js IS JSON) 	CONSTRAINT test_jsonb_constraint2 		CHECK  Required keyword: 'expressions' missing for <class 'sqlglot.expressions.properties.Properties'>. Line 4, Col: 62.   E test_jsonb_constraints ( 	js text, 	i int, 	x jsonb DEFAULT JSON_QUERY(jsonb '[1,2]', '$[*]' WITH [4mWRAPPER[0m) 	CONSTRAINT test_jsonb_constraint1 		CHECK (js IS JSON) 	CONSTRAINT test_jsonb_constraint2 		CHECK  ... and 1 more |
| 215 | 388–388 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 216 | 389–389 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 217 | 390–390 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 218 | 391–391 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 219 | 392–392 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 220 | 393–393 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 221 | 395–395 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 222 | 397–398 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 223 | 399–399 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 224 | 400–400 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 225 | 401–401 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 226 | 402–402 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 227 | 403–403 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 228 | 404–404 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 229 | 405–405 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 230 | 407–407 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 231 | 408–408 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 232 | 409–409 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 233 | 410–410 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 234 | 411–411 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 235 | 412–412 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 236 | 414–414 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 237 | 415–415 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 238 | 416–416 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 239 | 417–417 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 240 | 418–418 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 241 | 419–419 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 242 | 420–420 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 77.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.date() < $x' [4mPASSING[0m '12:34'::timetz AS x));  Expecting ). Line 1, Col: 85.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.date() < $x' PASSING [4m'12:34'[0m::timetz AS x)); |
| 243 | 421–421 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 77.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.date() < $x' [4mPASSING[0m '1234'::int AS x));  Expecting ). Line 1, Col: 84.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.date() < $x' PASSING [4m'1234'[0m::int AS x)); |
| 244 | 422–422 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 245 | 424–424 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 246 | 425–425 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 247 | 426–426 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 248 | 427–427 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 249 | 428–428 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 250 | 429–429 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 251 | 430–430 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 252 | 431–431 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 92.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("HH:MI TZH") < $x' [4mPASSING[0m '12:34'::timetz AS x));  Expecting ). Line 1, Col: 100.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("HH:MI TZH") < $x' PASSING [4m'12:34'[0m::timetz AS x)); |
| 253 | 432–432 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 92.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("HH:MI TZH") < $y' [4mPASSING[0m '12:34'::timetz AS x));  Expecting ). Line 1, Col: 100.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("HH:MI TZH") < $y' PASSING [4m'12:34'[0m::timetz AS x)); |
| 254 | 433–433 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 81.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() < $x' [4mPASSING[0m '12:34'::timetz AS x));  Expecting ). Line 1, Col: 89.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() < $x' PASSING [4m'12:34'[0m::timetz AS x)); |
| 255 | 434–434 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 81.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() < $x' [4mPASSING[0m '1234'::int AS x));  Expecting ). Line 1, Col: 88.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() < $x' PASSING [4m'1234'[0m::int AS x)); |
| 256 | 435–435 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 88.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() ? (@ == $x)' [4mPASSING[0m '12:34'::time AS x));  Expecting ). Line 1, Col: 96.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime() ? (@ == $x)' PASSING [4m'12:34'[0m::time AS x)); |
| 257 | 436–436 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 98.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("YY-MM-DD") ? (@ == $x)' [4mPASSING[0m '2020-07-14'::date AS x));  Expecting ). Line 1, Col: 111.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$.datetime("YY-MM-DD") ? (@ == $x)' PASSING [4m'2020-07-14'[0m::date AS x)); |
| 258 | 437–437 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 96.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, $.a ? (@.datetime() == $x)]' [4mPASSING[0m '12:34'::time AS x));  Expecting ). Line 1, Col: 104.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, $.a ? (@.datetime() == $x)]' PASSING [4m'12:34'[0m::time AS x)); |
| 259 | 438–438 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 101.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, 0 to $.a ? (@.datetime() == $x)]' [4mPASSING[0m '12:34'::time AS x));  Expecting ). Line 1, Col: 109.   EATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, 0 to $.a ? (@.datetime() == $x)]' PASSING [4m'12:34'[0m::time AS x)); |
| 260 | 439–439 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 103.   CREATE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, $.a ? (@.datetime("HH:MI") == $x)]' [4mPASSING[0m '12:34'::time AS x));  Expecting ). Line 1, Col: 111.   TE INDEX ON test_jsonb_mutability (JSON_QUERY(js, '$[1, $.a ? (@.datetime("HH:MI") == $x)]' PASSING [4m'12:34'[0m::time AS x)); |
| 261 | 440–440 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 262 | 442–442 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 263 | 443–443 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 264 | 444–444 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 265 | 445–445 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 266 | 446–446 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 267 | 447–447 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 268 | 448–448 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 269 | 449–449 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 270 | 451–458 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 271 | 459–459 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT ret_setint() ON ERROR) FROM test_jsonb_mutability;  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT ret_setint() ON ERROR) FROM test_jsonb_mutability; |
| 272 | 460–460 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT b + 1 ON ERROR) FROM test_jsonb_mutability;  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT b + 1 ON ERROR) FROM test_jsonb_mutability; |
| 273 | 461–461 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT sum(1) over() ON ERROR) FROM test_jsonb_mutability;  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT sum(1) over() ON ERROR) FROM test_jsonb_mutability; |
| 274 | 462–462 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT (SELECT 1) ON ERROR) FROM test_jsonb_mutability;  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_QUERY(js, '$'  [4mRETURNING[0m int DEFAULT (SELECT 1) ON ERROR) FROM test_jsonb_mutability; |
| 275 | 463–463 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 276 | 464–464 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 277 | 466–466 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 282 | 472–476 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT '"1"')::jsonb ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT '"1"')::jsonb ON ERROR); |
| 283 | 477–478 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON_QUERY('"a"', '$.a' [4mRETURNING[0m queryfuncs_test_domain DEFAULT (select '"1"')::queryfuncs_test_domain ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 40.   SELECT JSON_QUERY('"a"', '$.a' [4mRETURNING[0m queryfuncs_test_domain DEFAULT (select '"1"')::queryfuncs_test_domain ON ERROR); |
| 284 | 479–480 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT 1)::oid::int ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int DEFAULT (SELECT 1)::oid::int ON ERROR); |
| 285 | 481–482 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::oid[]::int[] ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::oid[]::int[] ON ERROR); |
| 286 | 483–484 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::text COLLATE "C" ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m int[] DEFAULT (SELECT '{1}')::text COLLATE "C" ON ERROR); |
| 287 | 485–486 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 288 | 487–487 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 289 | 488–488 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m someparent DEFAULT (SELECT '(1)')::somechild::someparent ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON_QUERY('"a"', '$.a'  [4mRETURNING[0m someparent DEFAULT (SELECT '(1)')::somechild::someparent ON ERROR); |
| 290 | 490–490 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 291 | 491–491 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 296 | 498–498 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 60.   SELECT JSON_QUERY(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'a' [4mWITH[0m WRAPPER);  Invalid expression / Unexpected token. Line 1, Col: 60.   SELECT JSON_QUERY(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'a' [4mWITH[0m WRAPPER); |
| 297 | 499–499 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 76.   SELECT JSON_QUERY(jsonb '{"a": 123}', ('$' \|\| '.' \|\| 'a' \|\| NULL)::date [4mWITH[0m WRAPPER);  Invalid expression / Unexpected token. Line 1, Col: 76.   SELECT JSON_QUERY(jsonb '{"a": 123}', ('$' \|\| '.' \|\| 'a' \|\| NULL)::date [4mWITH[0m WRAPPER); |
| 300 | 505–505 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 29.   SELECT JSON_QUERY(NULL [4mFORMAT[0m JSON, '$');  Invalid expression / Unexpected token. Line 1, Col: 34.   SELECT JSON_QUERY(NULL FORMAT [4mJSON[0m, '$'); |
| 301 | 507–508 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 304 | 512–513 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb 'null', '$xyz' [4mPASSING[0m 1 AS xy);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb 'null', '$xyz' PASSING [4m1[0m AS xy); |
| 305 | 514–514 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT JSON_QUERY(jsonb 'null', '$xy' [4mPASSING[0m 1 AS xyz);  Invalid expression / Unexpected token. Line 1, Col: 47.   SELECT JSON_QUERY(jsonb 'null', '$xy' PASSING [4m1[0m AS xyz); |
| 306 | 515–515 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb 'null', '$xyz' [4mPASSING[0m 1 AS xyz);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb 'null', '$xyz' PASSING [4m1[0m AS xyz); |
| 307 | 516–516 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb 'null', '$Xyz' [4mPASSING[0m 1 AS Xyz);  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb 'null', '$Xyz' PASSING [4m1[0m AS Xyz); |
| 308 | 517–517 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb 'null', '$Xyz' [4mPASSING[0m 1 AS "Xyz");  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_QUERY(jsonb 'null', '$Xyz' PASSING [4m1[0m AS "Xyz"); |
| 309 | 518–518 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_QUERY(jsonb 'null', '$"Xyz"' [4mPASSING[0m 1 AS "Xyz");  Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_QUERY(jsonb 'null', '$"Xyz"' PASSING [4m1[0m AS "Xyz"); |
| 310 | 520–521 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 311 | 522–522 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 312 | 523–525 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 313 | 526–526 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 314 | 527–529 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 316 | 532–533 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_VALUE(jsonb 'null', '$a' PASSING [4mt[0m AS a) = t AS ok   FROM test_passing_toast; |
| 317 | 534–534 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 318 | 536–537 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON_EXISTS(jsonb '1', '$' [4mDEFAULT[0m 1 ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_EXISTS(jsonb '1', '$' DEFAULT [4m1[0m ON ERROR); |
| 320 | 539–539 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 37.   SELECT JSON_QUERY(jsonb '1', '$' [4mTRUE[0m ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 40.   SELECT JSON_QUERY(jsonb '1', '$' TRUE [4mON[0m ERROR); |
| 323 | 545–545 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (NULL::sqljsonb_int_not_null + 0) ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 38.   SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (NULL::sqljsonb_int_not_null + 0) ON ERROR); |
| 325 | 547–547 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (('a' \|\| (random() * 0)::int)::int + 0) ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 38.   SELECT JSON_QUERY('"a"', '$' [4mRETURNING[0m int DEFAULT (('a' \|\| (random() * 0)::int)::int + 0) ON ERROR); |
| 327 | 552–553 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 329 | 555–555 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m int[] DEFAULT '{11}' ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m int[] DEFAULT '{11}' ON ERROR); |
| 331 | 557–557 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m queryfuncs_int[] DEFAULT '{11}' ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_QUERY(jsonb '["x"]', '$' [4mRETURNING[0m queryfuncs_int[] DEFAULT '{11}' ON ERROR); |
| 332 | 559–559 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 333 | 560–560 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": "x"}', '$' [4mRETURNING[0m compcoalesce);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT JSON_QUERY(jsonb '{"a": "x"}', '$' [4mRETURNING[0m compcoalesce); |
| 334 | 561–561 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": 11}', '$' [4mRETURNING[0m compcoalesce);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": 11}', '$' [4mRETURNING[0m compcoalesce); |
| 335 | 562–562 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 59.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": "B"}', '$' [4mRETURNING[0m compcoalesce);  Invalid expression / Unexpected token. Line 1, Col: 59.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": "B"}', '$' [4mRETURNING[0m compcoalesce); |
| 336 | 563–563 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 57.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": 0}', '$' [4mRETURNING[0m compcoalesce);  Invalid expression / Unexpected token. Line 1, Col: 57.   SELECT JSON_QUERY(jsonb '{"a": 1, "b": 0}', '$' [4mRETURNING[0m compcoalesce); |
| 337 | 563–564 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 338 | 565–565 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 339 | 567–569 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 340 | 570–570 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 341 | 571–571 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 ERROR ON ERROR); |
| 342 | 572–572 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 DEFAULT '1' ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2 DEFAULT '1' ON ERROR); |
| 343 | 573–573 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk ERROR ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk ERROR ON ERROR); |
| 344 | 574–574 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk DEFAULT '1' ON ERROR);  Invalid expression / Unexpected token. Line 1, Col: 44.   SELECT JSON_QUERY(jsonb '123', '$' [4mRETURNING[0m queryfuncs_char2_chk DEFAULT '1' ON ERROR); |
| 349 | 579–579 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 350 | 581–584 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 358 | 592–592 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 1 | 1–2 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 2 | 3–3 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 3 | 4–4 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 4 | 6–6 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 5 | 7–7 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 6 | 8–8 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 7 | 10–10 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 8 | 11–11 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 10 | 13–13 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 11 | 14–14 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 12 | 15–15 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 13 | 15–16 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 14 | 17–17 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 15 | 18–18 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 16 | 20–20 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 17 | 21–21 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 18 | 22–22 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 23 | 29–30 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 56 | 74–74 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 57 | 75–75 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 58 | 76–76 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 59 | 77–77 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 60 | 78–78 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 63 | 81–81 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 64 | 82–82 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 65 | 83–85 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 92 | 119–120 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 96 | 144–146 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 99 | 155–158 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 148 | 260–260 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_query；本次不安装 UDF |
| 213 | 376–381 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 214 | 383–386 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 278 | 467–467 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 279 | 468–468 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 280 | 469–469 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 281 | 470–470 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 292 | 493–494 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 295 | 497–497 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_query；本次不安装 UDF |
| 298 | 500–501 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_query；本次不安装 UDF |
| 299 | 503–504 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_exists；本次不安装 UDF |
| 302 | 509–509 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 303 | 510–510 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 315 | 530–531 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 321 | 541–543 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 322 | 544–544 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 324 | 546–546 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖时间、随机、Session、版本或有状态函数；不作为固定输出回归 |
| 326 | 548–550 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 330 | 556–556 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 345 | 575–575 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 346 | 576–576 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 347 | 577–577 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 348 | 578–578 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 351 | 585–585 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 352 | 586–586 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 353 | 587–587 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |

参考输出：`assets/sqljson_queryfuncs.out`；SHA-256（文件内容指纹）：`525356edfadbd9ebf14fe4f06c172440dc060b0090fb4d605495b034cd26d7f4`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 74/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 74/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 55/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 55/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 55/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/74 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-sqljson-queryfuncs-0025-2e24b896` | SELECT JSON_VALUE(NULL::jsonb, '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0026-38745d07` | SELECT JSON_VALUE(jsonb 'null', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0027-d66894eb` | SELECT JSON_VALUE(jsonb 'null', '$' RETURNING int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0028-080a25b5` | SELECT JSON_VALUE(jsonb 'true', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0029-8138825c` | SELECT JSON_VALUE(jsonb 'true', '$' RETURNING bool); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0030-17c170f7` | SELECT JSON_VALUE(jsonb '123', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0031-4f86e17d` | SELECT JSON_VALUE(jsonb '123', '$' RETURNING int) + 234; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0032-bd95d946` | SELECT JSON_VALUE(jsonb '123', '$' RETURNING text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0033-dde545e7` | SELECT JSON_VALUE(jsonb '123', '$' RETURNING bytea ERROR ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0034-2188e922` | SELECT JSON_VALUE(jsonb '1.23', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0035-b84d7e2c` | SELECT JSON_VALUE(jsonb '1.23', '$' RETURNING int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0036-2b6a5ea9` | SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING numeric); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0037-a5f418ce` | SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING int ERROR ON ERROR); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0038-d7147527` | SELECT JSON_VALUE(jsonb '"aaa"', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0039-0cd9e40c` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0040-7e2f34ba` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(5)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0041-05967d19` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2) ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0042-c2907fe7` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0043-6cb858d2` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(3) ERROR ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0044-2033aaa6` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0045-90c16c7e` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0046-2b8a023d` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json ERROR ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0047-f792d638` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb ERROR ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0048-b4527b25` | SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING json); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0049-96898d76` | SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0050-50c3e3bd` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0051-9a2a57fa` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int ERROR ON ERROR); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0052-f82b9920` | SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int DEFAULT 111 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0053-ee35c348` | SELECT JSON_VALUE(jsonb '"123"', '$' RETURNING int) + 234; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0054-557bf181` | SELECT JSON_VALUE(jsonb '"2017-02-20"', '$' RETURNING date) + 9; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0066-1f960c70` | SELECT JSON_VALUE(jsonb '[]', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0067-ff8839fa` | SELECT JSON_VALUE(jsonb '[]', '$' ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0068-b4bc6a7a` | SELECT JSON_VALUE(jsonb '{}', '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0069-d1d29700` | SELECT JSON_VALUE(jsonb '{}', '$' ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0070-00d59bcd` | SELECT JSON_VALUE(jsonb '1', '$.a'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0071-0a70fa3f` | SELECT JSON_VALUE(jsonb '1', 'strict $.a' ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0072-1278b801` | SELECT JSON_VALUE(jsonb '1', 'strict $.a' DEFAULT 'error' ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0073-bb4e0659` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0074-fa9f7b22` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0075-abc0de9c` | SELECT JSON_VALUE(jsonb '1', 'strict $.*' DEFAULT 2 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0076-b6c58a98` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT 2 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0077-800ba813` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0078-da6f3e1a` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' NULL ON EMPTY DEFAULT '2' ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0079-69f4f96a` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY DEFAULT '3' ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0080-38413d71` | SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY DEFAULT '3' ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0081-d479382c` | SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0082-fb1bee1a` | SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' DEFAULT '0' ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0083-4f6061d4` | SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int ERROR ON ERROR); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0084-881a2588` | SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0085-5ebde80a` | SELECT JSON_VALUE(jsonb '["1"]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0087-60a477e6` | SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT 99999.999 ON EMPTY); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0088-ec1cd510` | SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING varchar(3) DEFAULT 'toolong'::varchar(10) ON EMPTY); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0089-29bd6f64` | SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT NULL::numeric ON EMPTY); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0090-2055fe2d` | SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING bit(3) DEFAULT b'10101' ON EMPTY); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0091-ada5e2dc` | SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT abs(NULL::numeric) ON EMPTY); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0094-88ebeb21` | SELECT x IS NULL AS is_null,        json_value(x, '$.a' RETURNING int DEFAULT 42 ON EMPTY) AS jv FROM (VALUES ('{}'), (NULL), ('{}')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0095-3198a481` | SELECT x IS NULL AS is_null,        json_value(x, 'strict $.a' RETURNING int DEFAULT 42 ON ERROR) AS jv FROM (VALUES ('1'), (NULL), ('1')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0112-c017eeab` | select json_value('{"a": 1.234}', '$.a' returning int error on error); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0113-71c80245` | select json_value('{"a": "1.234"}', '$.a' returning int error on error); | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0114-2e24b896` | SELECT JSON_VALUE(NULL::jsonb, '$'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0293-69cc7045` | SELECT JSON_VALUE(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'a'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0294-1411b7ba` | SELECT JSON_VALUE(jsonb '{"a": 123}', '$' \|\| '.' \|\| 'b' DEFAULT 'foo' ON EMPTY); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0319-10a7c60f` | SELECT JSON_VALUE(jsonb '1', '$' EMPTY ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0328-38effc65` | SELECT JSON_VALUE(jsonb '"x"', '$' RETURNING int DEFAULT 11 ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0354-e456510b` | SELECT JSON_VALUE(jsonb '"111"', '$'  RETURNING bit(2) ERROR ON ERROR); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0355-9a967b5b` | SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1 ON ERROR); | 已生成 | 失败：类型转换失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-sqljson-queryfuncs-0356-3b4096cf` | SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1::bit(3) ON ERROR); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0357-fb7679a6` | SELECT JSON_VALUE(jsonb '"111"', '$.a'  RETURNING bit(3) DEFAULT '1111' ON EMPTY); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-queryfuncs-0359-afd861ac` | SELECT JSON_VALUE('null', '$' RETURNING jsonb), JSON_VALUE('123', '$' RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0360-bf372197` | SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), ('null'), ('2')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0361-85025945` | SELECT JSON_VALUE(x, '$' RETURNING json) FROM (VALUES ('1'::json), ('null'), ('2')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0362-e7974a66` | SELECT JSON_VALUE(x, '$.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('{}'), ('{"a": 2}')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0363-fab5929f` | SELECT JSON_VALUE(x, 'strict $.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('[]'), ('{"a": 2}')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-queryfuncs-0364-20eac327` | SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), (NULL), ('2')) v(x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-sqljson-queryfuncs-0025-2e24b896 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(NULL::jsonb, '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST(NULL AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 20.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0026-38745d07 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb 'null', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('null' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0027-d66894eb — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb 'null', '$' RETURNING int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('null' AS JSONB), '$' RETURNING INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0028-080a25b5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb 'true', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('true' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0029-8138825c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb 'true', '$' RETURNING bool);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('true' AS JSONB), '$' RETURNING BOOLEAN)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0030-17c170f7 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '123', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0031-4f86e17d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING int) + 234;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING INT) + 234
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "357"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0032-bd95d946 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING STRING)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0033-dde545e7 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '123', '$' RETURNING bytea ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('123' AS JSONB), '$' RETURNING VARBINARY ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x313233"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0034-2188e922 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1.23', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1.23' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.23"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0035-b84d7e2c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1.23', '$' RETURNING int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1.23' AS JSONB), '$' RETURNING INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0036-2b6a5ea9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"1.23"' AS JSONB), '$' RETURNING DECIMAL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.23"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0037-a5f418ce — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"1.23"', '$' RETURNING int ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"1.23"' AS JSONB), '$' RETURNING INT ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type integer: "1.23"`。

错误原文：

```text
invalid input syntax for type integer: "1.23"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type integer: "1.23"
source_error_code=invalid input syntax for type integer: "1.23"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0038-d7147527 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "aaa"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0039-0cd9e40c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING STRING)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "aaa"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0040-7e2f34ba — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(5));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(5))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "aaa"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0041-05967d19 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2) ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(2) ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value too long for type character(2)`。

错误原文：

```text
value too long for type character(2)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0042-c2907fe7 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(2));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(2))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0043-6cb858d2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING char(3) ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING CHAR(3) ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "aaa"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0044-2033aaa6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"aaa\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0045-90c16c7e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSONB)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"aaa\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0046-2b8a023d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING json ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSON ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"aaa\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0047-f792d638 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING jsonb ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING JSONB ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"aaa\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0048-b4527b25 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING json);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"\\"aaa\\""' AS JSONB), '$' RETURNING JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"\\\"aaa\\\"\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0049-96898d76 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"\"aaa\""', '$' RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"\\"aaa\\""' AS JSONB), '$' RETURNING JSONB)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"\\\"aaa\\\"\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 52)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0050-50c3e3bd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0051-9a2a57fa — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING INT ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type integer: "aaa"`。

错误原文：

```text
invalid input syntax for type integer: "aaa"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type integer: "aaa"
source_error_code=invalid input syntax for type integer: "aaa"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0052-f82b9920 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"aaa"', '$' RETURNING int DEFAULT 111 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"aaa"' AS JSONB), '$' RETURNING INT DEFAULT 111 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "111"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0053-ee35c348 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"123"', '$' RETURNING int) + 234;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"123"' AS JSONB), '$' RETURNING INT) + 234
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "357"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0054-557bf181 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"2017-02-20"', '$' RETURNING date) + 9;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"2017-02-20"' AS JSONB), '$' RETURNING DATE) + 9
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "03-01-2017"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 53)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 53)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0066-1f960c70 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[]', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[]' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0067-ff8839fa — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[]', '$' ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[]' AS JSONB), '$' ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON path expression in JSON_VALUE must return single scalar item`。

错误原文：

```text
JSON path expression in JSON_VALUE must return single scalar item
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0068-b4bc6a7a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0069-d1d29700 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$' ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$' ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON path expression in JSON_VALUE must return single scalar item`。

错误原文：

```text
JSON path expression in JSON_VALUE must return single scalar item
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0070-00d59bcd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', '$.a');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), '$.a')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0071-0a70fa3f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'strict $.a' ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'strict $.a' ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`jsonpath member accessor can only be applied to an object`。

错误原文：

```text
jsonpath member accessor can only be applied to an object
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0072-1278b801 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'strict $.a' DEFAULT 'error' ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'strict $.a' DEFAULT 'error' ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "error"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0073-bb4e0659 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0074-fa9f7b22 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' ERROR ON EMPTY ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`no SQL/JSON item found for specified path`。

错误原文：

```text
no SQL/JSON item found for specified path
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0075-abc0de9c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'strict $.*' DEFAULT 2 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'strict $.*' DEFAULT 2 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 51)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0076-b6c58a98 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT 2 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT 2 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0077-800ba813 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT '2' ON EMPTY)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0078-da6f3e1a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' NULL ON EMPTY DEFAULT '2' ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' NULL ON EMPTY DEFAULT '2' ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0079-69f4f96a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' DEFAULT '2' ON EMPTY DEFAULT '3' ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' DEFAULT '2' ON EMPTY DEFAULT '3' ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0080-38413d71 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', 'lax $.a' ERROR ON EMPTY DEFAULT '3' ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), 'lax $.a' ERROR ON EMPTY DEFAULT '3' ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`no SQL/JSON item found for specified path`。

错误原文：

```text
no SQL/JSON item found for specified path
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0081-d479382c — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[1,2]' AS JSONB), '$[*]' ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON path expression in JSON_VALUE must return single scalar item`。

错误原文：

```text
JSON path expression in JSON_VALUE must return single scalar item
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ERROR' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0082-fb1bee1a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[1,2]', '$[*]' DEFAULT '0' ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[1,2]' AS JSONB), '$[*]' DEFAULT '0' ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 14.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0083-4f6061d4 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[" "]' AS JSONB), '$[*]' RETURNING INT ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type integer: " "`。

错误原文：

```text
invalid input syntax for type integer: " "
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type integer: " "
source_error_code=invalid input syntax for type integer: " "
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0084-881a2588 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '[" "]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('[" "]' AS JSONB), '$[*]' RETURNING INT DEFAULT 2 + 3 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0085-5ebde80a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '["1"]', '$[*]' RETURNING int DEFAULT 2 + 3 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('["1"]' AS JSONB), '$[*]' RETURNING INT DEFAULT 2 + 3 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0087-60a477e6 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT 99999.999 ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING DECIMAL(4, 1) DEFAULT 99999.999 ON EMPTY)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`numeric field overflow`。

错误原文：

```text
numeric field overflow
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0088-ec1cd510 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING varchar(3) DEFAULT 'toolong'::varchar(10) ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING VARCHAR(3) DEFAULT CAST('toolong' AS VARCHAR(10)) ON EMPTY)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value too long for type character varying(3)`。

错误原文：

```text
value too long for type character varying(3)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0089-29bd6f64 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT NULL::numeric ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING DECIMAL(4, 1) DEFAULT CAST(NULL AS DECIMAL) ON EMPTY)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0090-2055fe2d — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING bit(3) DEFAULT b'10101' ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING BIT(3) DEFAULT 21 ON EMPTY)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bit string length 5 does not match type bit(3)`。

错误原文：

```text
bit string length 5 does not match type bit(3)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0091-ada5e2dc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{}', '$.a' RETURNING numeric(4,1) DEFAULT abs(NULL::numeric) ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{}' AS JSONB), '$.a' RETURNING DECIMAL(4, 1) DEFAULT ABS(CAST(NULL AS DECIMAL)) ON EMPTY)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0094-88ebeb21 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x IS NULL AS is_null,
       json_value(x, '$.a' RETURNING int DEFAULT 42 ON EMPTY) AS jv
FROM (VALUES ('{}'), (NULL), ('{}')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x IS NULL AS is_null, JSON_VALUE(x, '$.a' RETURNING INT DEFAULT 42 ON EMPTY) AS jv FROM (SELECT '{}' AS x UNION ALL SELECT NULL UNION ALL SELECT '{}') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：is_null: unknown / 原生类型未知, jv: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f",
    "42"
  ],
  [
    "t",
    ""
  ],
  [
    "f",
    "42"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0095-3198a481 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x IS NULL AS is_null,
       json_value(x, 'strict $.a' RETURNING int DEFAULT 42 ON ERROR) AS jv
FROM (VALUES ('1'), (NULL), ('1')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x IS NULL AS is_null, JSON_VALUE(x, 'strict $.a' RETURNING INT DEFAULT 42 ON ERROR) AS jv FROM (SELECT '1' AS x UNION ALL SELECT NULL UNION ALL SELECT '1') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：is_null: unknown / 原生类型未知, jv: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f",
    "42"
  ],
  [
    "t",
    ""
  ],
  [
    "f",
    "42"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 56)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 56)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0112-c017eeab — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select json_value('{"a": 1.234}', '$.a' returning int error on error);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE('{"a": 1.234}', '$.a' RETURNING INT ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type integer: "1.234"`。

错误原文：

```text
invalid input syntax for type integer: "1.234"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 40)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type integer: "1.234"
source_error_code=invalid input syntax for type integer: "1.234"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 40)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0113-71c80245 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select json_value('{"a": "1.234"}', '$.a' returning int error on error);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE('{"a": "1.234"}', '$.a' RETURNING INT ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type integer: "1.234"`。

错误原文：

```text
invalid input syntax for type integer: "1.234"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type integer: "1.234"
source_error_code=invalid input syntax for type integer: "1.234"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0114-2e24b896 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(NULL::jsonb, '$');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST(NULL AS JSONB), '$')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0293-69cc7045 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{"a": 123}', '$' || '.' || 'a');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{"a": 123}' AS JSONB), CONCAT('$', '.', 'a'))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_VALUE'")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0294-1411b7ba — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '{"a": 123}', '$' || '.' || 'b' DEFAULT 'foo' ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('{"a": 123}' AS JSONB), CONCAT('$', '.', 'b') DEFAULT 'foo' ON EMPTY)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "foo"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'DEFAULT' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0319-10a7c60f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1', '$' EMPTY ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1' AS JSONB), '$' EMPTY ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid ON ERROR behavior`。

错误原文：

```text
invalid ON ERROR behavior
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'EMPTY' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0328-38effc65 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"x"', '$' RETURNING int DEFAULT 11 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"x"' AS JSONB), '$' RETURNING INT DEFAULT 11 ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "11"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0354-e456510b — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"111"', '$'  RETURNING bit(2) ERROR ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"111"' AS JSONB), '$' RETURNING BIT(2) ERROR ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bit string length 3 does not match type bit(2)`。

错误原文：

```text
bit string length 3 does not match type bit(2)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0355-9a967b5b — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1 ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1234' AS JSONB), '$' RETURNING BIT(3) DEFAULT 1 ON ERROR)
```

#### 源端参考结果

- 执行状态：失败：类型转换失败；耗时 0.0 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`cannot cast behavior expression of type integer to bit`。

错误原文：

```text
cannot cast behavior expression of type integer to bit
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=CAST_ERROR
source_error_message=cannot cast behavior expression of type integer to bit
source_error_code=cannot cast behavior expression of type integer to bit
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0356-3b4096cf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '1234', '$' RETURNING bit(3)  DEFAULT 1::bit(3) ON ERROR);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('1234' AS JSONB), '$' RETURNING BIT(3) DEFAULT CAST(1 AS BIT(3)) ON ERROR)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "001"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0357-fb7679a6 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_VALUE(jsonb '"111"', '$.a'  RETURNING bit(3) DEFAULT '1111' ON EMPTY);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(CAST('"111"' AS JSONB), '$.a' RETURNING BIT(3) DEFAULT '1111' ON EMPTY)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bit string length 4 does not match type bit(3)`。

错误原文：

```text
bit string length 4 does not match type bit(3)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 48)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-queryfuncs-0359-afd861ac — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE('null', '$' RETURNING jsonb), JSON_VALUE('123', '$' RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE('null', '$' RETURNING JSONB), JSON_VALUE('123', '$' RETURNING JSONB)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_value: unknown / 原生类型未知, json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "123"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0360-bf372197 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), ('null'), ('2')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING JSONB) FROM (SELECT CAST('1' AS JSONB) AS x UNION ALL SELECT 'null' UNION ALL SELECT '2') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    ""
  ],
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0361-85025945 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING json) FROM (VALUES ('1'::json), ('null'), ('2')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING JSON) FROM (SELECT CAST('1' AS JSON) AS x UNION ALL SELECT 'null' UNION ALL SELECT '2') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    ""
  ],
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0362-e7974a66 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(x, '$.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('{}'), ('{"a": 2}')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(x, '$.a' RETURNING JSONB) FROM (SELECT CAST('{"a": 1}' AS JSONB) AS x UNION ALL SELECT '{}' UNION ALL SELECT '{"a": 2}') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    ""
  ],
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0363-fab5929f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(x, 'strict $.a' RETURNING jsonb) FROM (VALUES ('{"a": 1}'::jsonb), ('[]'), ('{"a": 2}')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(x, 'strict $.a' RETURNING JSONB) FROM (SELECT CAST('{"a": 1}' AS JSONB) AS x UNION ALL SELECT '[]' UNION ALL SELECT '{"a": 2}') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    ""
  ],
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 34)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 34)\n")
doris_error_code=1105
```

### pg-sqljson-queryfuncs-0364-20eac327 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING jsonb) FROM (VALUES ('1'::jsonb), (NULL), ('2')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_VALUE(x, '$' RETURNING JSONB) FROM (SELECT CAST('1' AS JSONB) AS x UNION ALL SELECT NULL UNION ALL SELECT '2') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    ""
  ],
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=True
doris_success=False
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 25)\n")
doris_error_code=1105
```
