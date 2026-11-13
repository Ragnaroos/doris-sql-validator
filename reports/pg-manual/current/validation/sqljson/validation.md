# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:33.109682+00:00 至 2026-11-11T09:40:34.321780+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/sqljson.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**87**；两端成功且已有证据匹配：**1**。
- 成功结果匹配占全部查询比例：**1/87 = 1.15%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**1/55 = 1.82%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**30**；不计入上述成功匹配分子。
- 需要分析的查询：**86**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**2**；源参考结果不可用：**0**；Doris 执行失败：**74**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 3 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 44 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 28 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 10 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 2 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 87 条只读查询、跳过 190 条非查询、0 条待确认、55 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 4 | 5–5 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT JSON('{ "a" : 1 } ' [4mFORMAT[0m JSON);  Invalid expression / Unexpected token. Line 1, Col: 38.   SELECT JSON('{ "a" : 1 } ' FORMAT [4mJSON[0m); |
| 5 | 6–6 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT JSON('{ "a" : 1 } ' [4mFORMAT[0m JSON ENCODING UTF8);  Invalid expression / Unexpected token. Line 1, Col: 38.   SELECT JSON('{ "a" : 1 } ' FORMAT [4mJSON[0m ENCODING UTF8); |
| 6 | 7–7 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON('{ "a" : 1 } '::bytea [4mFORMAT[0m JSON ENCODING UTF8);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON('{ "a" : 1 } '::bytea FORMAT [4mJSON[0m ENCODING UTF8); |
| 10 | 12–12 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 32.   SELECT JSON('   1   '::json [4mWITH[0m UNIQUE KEYS);  Invalid expression / Unexpected token. Line 1, Col: 32.   SELECT JSON('   1   '::json [4mWITH[0m UNIQUE KEYS); |
| 13 | 16–16 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 35.   SELECT JSON('{"a": 1, "a": 2}' [4mWITH[0m UNIQUE KEYS);  Invalid expression / Unexpected token. Line 1, Col: 35.   SELECT JSON('{"a": 1, "a": 2}' [4mWITH[0m UNIQUE KEYS); |
| 14 | 17–17 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT JSON('{"a": 1, "a": 2}' [4mWITHOUT[0m UNIQUE KEYS);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT JSON('{"a": 1, "a": 2}' WITHOUT [4mUNIQUE[0m KEYS); |
| 15 | 19–19 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 16 | 20–20 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 17 | 21–21 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 18 | 22–22 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 19 | 23–23 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 20 | 24–24 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 21 | 26–26 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 36 | 44–44 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 37 | 45–45 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 43 | 53–53 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 32.   SELECT JSON_SERIALIZE('1' [4mFORMAT[0m JSON);  Invalid expression / Unexpected token. Line 1, Col: 37.   SELECT JSON_SERIALIZE('1' FORMAT [4mJSON[0m); |
| 44 | 54–54 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m bytea);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m bytea); |
| 45 | 55–55 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar); |
| 47 | 58–59 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m jsonb);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m jsonb); |
| 48 | 62–62 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 49 | 63–63 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 73 | 91–92 | 导入失败；类型 `parse_error` | Required keyword: 'this' missing for <class 'sqlglot.expressions.core.DPipe'>. Line 1, Col: 28.   SELECT JSON_OBJECT('a' \|\| 2[4m:[0m 1);  Invalid expression / Unexpected token. Line 1, Col: 28.   SELECT JSON_OBJECT('a' \|\| 2[4m:[0m 1); |
| 79 | 101–103 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 30.   SELECT JSON_OBJECT(json '[1]'[4m:[0m 123); |
| 104 | 158–160 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 105 | 161–162 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 107 | 164–164 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 108 | 166–168 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 109 | 169–171 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 110 | 172–172 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 112 | 174–174 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 113 | 175–175 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 114 | 176–176 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 116 | 180–180 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m json);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m json); |
| 117 | 181–181 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m json FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m json FORMAT JSON); |
| 118 | 182–182 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m jsonb);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m jsonb); |
| 119 | 183–183 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m jsonb FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m jsonb FORMAT JSON); |
| 120 | 184–184 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text); |
| 121 | 185–185 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON); |
| 122 | 186–186 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING UTF8);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING UTF8); |
| 123 | 187–187 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING INVALID_ENCODING);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m text FORMAT JSON ENCODING INVALID_ENCODING); |
| 124 | 188–188 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea); |
| 125 | 189–189 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON); |
| 126 | 190–190 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF8);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF8); |
| 127 | 191–191 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF16);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF16); |
| 128 | 192–192 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF32);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT JSON_ARRAY([4mRETURNING[0m bytea FORMAT JSON ENCODING UTF32); |
| 130 | 196–196 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT JSON_ARRAY('a',  NULL, 'b' [4mNULL[0m   ON NULL);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY('a',  NULL, 'b' NULL   [4mON[0m NULL); |
| 131 | 197–197 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON_ARRAY('a',  NULL, 'b' [4mABSENT[0m ON NULL);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY('a',  NULL, 'b' ABSENT [4mON[0m NULL); |
| 132 | 198–198 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON_ARRAY(NULL, NULL, 'b' [4mABSENT[0m ON NULL);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY(NULL, NULL, 'b' ABSENT [4mON[0m NULL); |
| 133 | 199–199 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT JSON_ARRAY('a',  NULL, 'b' [4mNULL[0m   ON NULL RETURNING jsonb);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY('a',  NULL, 'b' NULL   [4mON[0m NULL RETURNING jsonb); |
| 134 | 200–200 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON_ARRAY('a',  NULL, 'b' [4mABSENT[0m ON NULL RETURNING jsonb);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY('a',  NULL, 'b' ABSENT [4mON[0m NULL RETURNING jsonb); |
| 135 | 201–201 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 40.   SELECT JSON_ARRAY(NULL, NULL, 'b' [4mABSENT[0m ON NULL RETURNING jsonb);  Invalid expression / Unexpected token. Line 1, Col: 43.   SELECT JSON_ARRAY(NULL, NULL, 'b' ABSENT [4mON[0m NULL RETURNING jsonb); |
| 136 | 203–203 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text));  Expecting ). Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text));  Invalid expression / Unexpected token. Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m text)); |
| 137 | 204–204 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text));  Expecting ). Line 1, Col: 51.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text));  Invalid expression / Unexpected token. Line 1, Col: 56.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' FORMAT [4mJSON[0m RETURNING text)); |
| 138 | 205–205 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text) FORMAT JSON);  Expecting ). Line 1, Col: 51.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mFORMAT[0m JSON RETURNING text) FORMAT JSON);  Invalid expression / Unexpected token. Line 1, Col: 56.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' FORMAT [4mJSON[0m RETURNING text) FORMAT JSON); |
| 141 | 210–210 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 117.   SON_ARRAY(SELECT i FROM (VALUES (NULL::int[]), ('{1,2}'), (NULL), (NULL), ('{3,4}'), (NULL)) foo(i) [4mRETURNING[0m jsonb);  Invalid expression / Unexpected token. Line 1, Col: 117.   SON_ARRAY(SELECT i FROM (VALUES (NULL::int[]), ('{1,2}'), (NULL), (NULL), ('{3,4}'), (NULL)) foo(i) [4mRETURNING[0m jsonb); |
| 143 | 214–214 | 导入失败；类型 `parse_error` | values does not support CTE. Line 1, Col: 53.   SELECT JSON_ARRAY(WITH x AS (SELECT 1) VALUES (TRUE)[4m)[0m; |
| 146 | 220–225 | 导入失败；类型 `parse_error` | Expecting ). Line 4, Col: 13.   LL), (4)) t1(a) WHERE JSON_ARRAY(     SELECT b FROM (VALUES (1), (2), (3)) t2(b) WHERE b = t1.a     [4mRETURNING[0m jsonb ) = '[]'::jsonb;  Invalid expression / Unexpected token. Line 4, Col: 13.   LL), (4)) t1(a) WHERE JSON_ARRAY(     SELECT b FROM (VALUES (1), (2), (3)) t2(b) WHERE b = t1.a     [4mRETURNING[0m jsonb ) = '[]'::jsonb; |
| 147 | 227–229 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(1));  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(1)); |
| 148 | 230–230 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(1));  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(1)); |
| 149 | 231–232 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(3));  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_ARRAY(SELECT 1 [4mRETURNING[0m varchar(3)); |
| 150 | 233–233 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 48.   SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(2));  Invalid expression / Unexpected token. Line 1, Col: 48.   SELECT JSON_ARRAY(SELECT 1 WHERE FALSE [4mRETURNING[0m varchar(2)); |
| 154 | 240–243 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 27.   SELECT	JSON_ARRAYAGG(i) IS NULL, 		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) IS NULL FROM generate_series(1, 0) i;  Invalid expression / Unexpected token. Line 2, Col: 27.   SELECT	JSON_ARRAYAGG(i) IS NULL, 		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) IS NULL FROM generate_series(1, 0) i; |
| 155 | 245–247 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 27.   SELECT	JSON_ARRAYAGG(i), 		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) FROM generate_series(1, 5) i;  Invalid expression / Unexpected token. Line 2, Col: 27.   SELECT	JSON_ARRAYAGG(i), 		JSON_ARRAYAGG(i [4mRETURNING[0m jsonb) FROM generate_series(1, 5) i; |
| 158 | 255–256 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 50.   SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON) FROM generate_series(1, 5) i;  Expecting ). Line 1, Col: 50.   SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON) FROM generate_series(1, 5) i;  Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT JSON_ARRAYAGG(JSON_ARRAY(i, i + 1 [4mRETURNING[0m text) FORMAT JSON) FROM generate_series(1, 5) i; |
| 159 | 258–260 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 30.   SELECT	JSON_ARRAYAGG(NULL), 		JSON_ARRAYAGG(NULL [4mRETURNING[0m jsonb) FROM generate_series(1, 5);  Invalid expression / Unexpected token. Line 2, Col: 30.   SELECT	JSON_ARRAYAGG(NULL), 		JSON_ARRAYAGG(NULL [4mRETURNING[0m jsonb) FROM generate_series(1, 5); |
| 160 | 262–264 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 30.   SELECT	JSON_ARRAYAGG(NULL [4mNULL[0m ON NULL), 		JSON_ARRAYAGG(NULL NULL ON NULL RETURNING jsonb) FROM generate_series(1, 5);  Invalid expression / Unexpected token. Line 1, Col: 33.   SELECT	JSON_ARRAYAGG(NULL NULL [4mON[0m NULL), 		JSON_ARRAYAGG(NULL NULL ON NULL RETURNING jsonb) FROM generate_series(1, 5); |
| 161 | 266–279 | 导入失败；类型 `parse_error` | Expecting ). Line 3, Col: 28.   SELECT 	JSON_ARRAYAGG(bar) as no_options, 	JSON_ARRAYAGG(bar [4mRETURNING[0m jsonb) as returning_jsonb, 	JSON_ARRAYAGG(bar ABSENT ON NULL) as absent_on_null, 	JSON_ARRAYAGG(bar  Invalid expression / Unexpected token. Line 3, Col: 28.   SELECT 	JSON_ARRAYAGG(bar) as no_options, 	JSON_ARRAYAGG(bar [4mRETURNING[0m jsonb) as returning_jsonb, 	JSON_ARRAYAGG(bar ABSENT ON NULL) as absent_on_null, 	JSON_ARRAYAGG(bar |
| 175 | 335–337 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 176 | 339–340 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 177 | 342–344 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 183 | 364–366 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 184 | 368–369 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 28.   CREATE VIEW json_array_view AS SELECT JSON_ARRAY('1' [4mFORMAT[0m JSON, 2 RETURNING json); |
| 185 | 371–373 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 186 | 375–378 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 187 | 380–382 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 188 | 384–386 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 189 | 388–390 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 190 | 392–395 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 191 | 397–399 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 192 | 401–403 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 47.   CREATE VIEW json_arrayagg_view AS SELECT JSON_ARRAYAGG(('111' \|\| i)::bytea [4mFORMAT[0m JSON NULL ON NULL RETURNING text) FILTER (WHERE i > 3) FROM generate_series(1,5) i; |
| 193 | 405–407 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 194 | 409–411 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 195 | 413–414 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 79.   W json_array_subquery_view AS SELECT JSON_ARRAY(SELECT i FROM (VALUES (1), (2), (NULL), (4)) foo(i) [4mRETURNING[0m jsonb); |
| 196 | 416–419 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 197 | 421–422 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 98.   ry_view AS SELECT JSON_ARRAY(SELECT i FROM (VALUES (1), (2), (NULL), (4)) foo(i) ORDER BY i LIMIT 3 [4mRETURNING[0m jsonb); |
| 198 | 424–426 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 199 | 428–433 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 200 | 435–440 | 跳过非查询；类型 `create` | Expecting ). Line 5, Col: 13.   LL), (4)) t1(a) WHERE JSON_ARRAY(     SELECT b FROM (VALUES (1), (2), (3)) t2(b) WHERE b = t1.a     [4mRETURNING[0m jsonb ) = '[]'::jsonb; |
| 201 | 442–444 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 202 | 446–448 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 203 | 450–451 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 79.   W json_array_subquery_view AS SELECT JSON_ARRAY(SELECT i FROM (VALUES (1), (2), (NULL), (4)) foo(i) [4mRETURNING[0m text); |
| 204 | 453–455 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 205 | 457–459 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 53.   CREATE VIEW json_array_subquery_view AS SELECT JSON_ARRAY(SELECT '{"a": 1}'::text FORMAT [4mJSON[0m);  Invalid expression / Unexpected token. Line 2, Col: 54.   CREATE VIEW json_array_subquery_view AS SELECT JSON_ARRAY(SELECT '{"a": 1}'::text FORMAT JSON[4m)[0m; |
| 206 | 461–463 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 207 | 465–466 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 208 | 467–467 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 209 | 468–468 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 210 | 469–469 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 211 | 470–470 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 212 | 471–477 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 213 | 479–480 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 214 | 481–481 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 215 | 482–482 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 60, start: 51, end: 59, comments: []>. Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m jsonb)); |
| 216 | 483–483 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m json));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 60, start: 51, end: 59, comments: []>. Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m json));  Expecting ). Line 1, Col: 60.   create index xx on test_mutability(json_arrayagg(a [4mreturning[0m json)); |
| 217 | 485–486 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(a [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 54, start: 45, end: 53, comments: []>. Line 1, Col: 54.   create index on test_mutability(json_array(a [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(a [4mreturning[0m jsonb)); |
| 218 | 486–487 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(b [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 54, start: 45, end: 53, comments: []>. Line 1, Col: 54.   create index on test_mutability(json_array(b [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(b [4mreturning[0m jsonb)); |
| 219 | 487–488 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(c [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 54, start: 45, end: 53, comments: []>. Line 1, Col: 54.   create index on test_mutability(json_array(c [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(c [4mreturning[0m jsonb)); |
| 220 | 488–489 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(d [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 54, start: 45, end: 53, comments: []>. Line 1, Col: 54.   create index on test_mutability(json_array(d [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 54.   create index on test_mutability(json_array(d [4mreturning[0m jsonb)); |
| 221 | 489–490 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f1 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f1 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f1 [4mreturning[0m jsonb)); |
| 222 | 490–491 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f2 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f2 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f2 [4mreturning[0m jsonb)); |
| 223 | 491–492 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f3 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f3 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f3 [4mreturning[0m jsonb)); |
| 224 | 492–493 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f4 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f4 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f4 [4mreturning[0m jsonb)); |
| 225 | 493–494 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f5 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f5 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f5 [4mreturning[0m jsonb)); |
| 226 | 494–495 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f6 [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 55, start: 46, end: 54, comments: []>. Line 1, Col: 55.   create index on test_mutability(json_array(f6 [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 55.   create index on test_mutability(json_array(f6 [4mreturning[0m jsonb)); |
| 227 | 495–498 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 228 | 498–499 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 229 | 499–500 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 230 | 500–501 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 231 | 501–502 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 232 | 502–503 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 233 | 503–504 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 234 | 504–505 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 235 | 505–506 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 236 | 506–507 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 237 | 507–512 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 91.   alter table test_mutability add column f10 json generated always as (json_array(a [4mreturning[0m json));  Expecting ). Line 1, Col: 91.   alter table test_mutability add column f10 json generated always as (json_array(a [4mreturning[0m json)); |
| 238 | 512–513 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(b [4mreturning[0m json));  Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(b [4mreturning[0m json)); |
| 239 | 513–514 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(c [4mreturning[0m json));  Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(c [4mreturning[0m json)); |
| 240 | 514–515 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(d [4mreturning[0m json));  Expecting ). Line 1, Col: 91.   alter table test_mutability add column f11 json generated always as (json_array(d [4mreturning[0m json)); |
| 241 | 515–516 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f1 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f1 [4mreturning[0m json)); |
| 242 | 516–517 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f2 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f2 [4mreturning[0m json)); |
| 243 | 517–518 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f3 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f3 [4mreturning[0m json)); |
| 244 | 518–519 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f4 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f4 [4mreturning[0m json)); |
| 245 | 519–520 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f5 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f5 [4mreturning[0m json)); |
| 246 | 520–521 | 跳过非查询；类型 `alter` | Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f6 [4mreturning[0m json));  Expecting ). Line 1, Col: 92.   alter table test_mutability add column f11 json generated always as (json_array(f6 [4mreturning[0m json)); |
| 247 | 521–526 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 248 | 526–527 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 249 | 527–528 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 250 | 528–529 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 251 | 529–530 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 252 | 530–531 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 253 | 531–532 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 254 | 532–533 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 255 | 533–534 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 256 | 534–535 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 257 | 535–537 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 258 | 538–538 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 259 | 539–539 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 260 | 540–540 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 261 | 541–541 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 262 | 542–542 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 263 | 544–545 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 264 | 546–546 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 265 | 547–547 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 59.   create index on test_range_immutable(json_array(r [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 59, start: 50, end: 58, comments: []>. Line 1, Col: 59.   create index on test_range_immutable(json_array(r [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 59.   create index on test_range_immutable(json_array(r [4mreturning[0m jsonb)); |
| 266 | 547–548 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 59.   create index on test_range_immutable(json_array(m [4mreturning[0m jsonb));  Expected table name but got <Token token_type: TokenType.RETURNING, text: returning, line: 1, col: 59, start: 50, end: 58, comments: []>. Line 1, Col: 59.   create index on test_range_immutable(json_array(m [4mreturning[0m jsonb));  Expecting ). Line 1, Col: 59.   create index on test_range_immutable(json_array(m [4mreturning[0m jsonb)); |
| 267 | 548–549 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 268 | 549–550 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 269 | 550–551 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 270 | 552–552 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 278 | 563–564 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 279 | 565–565 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 280 | 566–566 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 281 | 567–567 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 282 | 568–568 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 288 | 579–585 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 289 | 586–587 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 290 | 588–593 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 292 | 594–595 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 41.   SELECT JSON('{"a":1}'::sqljson_mystr [4mWITH[0m UNIQUE KEYS);  Invalid expression / Unexpected token. Line 1, Col: 41.   SELECT JSON('{"a":1}'::sqljson_mystr [4mWITH[0m UNIQUE KEYS); |
| 293 | 595–597 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 295 | 599–600 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 296 | 601–609 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 298 | 613–613 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 299 | 614–614 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 302 | 620–620 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 303 | 622–638 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 308 | 692–694 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 309 | 696–697 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 310 | 699–701 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 311 | 703–704 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar(2));  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT JSON_SERIALIZE('{ "a" : 1 } ' [4mRETURNING[0m varchar(2)); |
| 313 | 706–706 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2)));  Expecting ). Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2)));  Invalid expression / Unexpected token. Line 1, Col: 54.   SELECT JSON_ARRAY(JSON_ARRAY('{ "a" : 123 }' [4mRETURNING[0m varchar(2))); |
| 314 | 707–707 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT JSON_ARRAYAGG(('111' \|\| i)::bytea [4mFORMAT[0m JSON NULL ON NULL RETURNING varchar(2)) FROM generate_series(1,1) i;  Invalid expression / Unexpected token. Line 1, Col: 52.   SELECT JSON_ARRAYAGG(('111' \|\| i)::bytea FORMAT [4mJSON[0m NULL ON NULL RETURNING varchar(2)) FROM generate_series(1,1) i; |
| 316 | 710–711 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 317 | 712–712 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 37.   SELECT JSON_SERIALIZE('123' [4mRETURNING[0m sqljson_char2);  Invalid expression / Unexpected token. Line 1, Col: 37.   SELECT JSON_SERIALIZE('123' [4mRETURNING[0m sqljson_char2); |
| 318 | 713–713 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 36.   SELECT JSON_SERIALIZE('12' [4mRETURNING[0m sqljson_char2);  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT JSON_SERIALIZE('12' [4mRETURNING[0m sqljson_char2); |
| 319 | 715–719 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 320 | 720–720 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 321 | 721–721 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 323 | 723–723 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 325 | 725–725 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 327 | 727–727 | 跳过非查询；类型 `drop` | Invalid expression / Unexpected token. Line 1, Col: 27.   DROP FUNCTION volatile_one[4m,[0m stable_one; |
| 328 | 729–740 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 329 | 741–749 | 导入失败；类型 `parse_error` | Expecting ). Line 2, Col: 37.   SELECT i % 2 AS g, 	JSON_ARRAYAGG(i ORDER BY i [4mRETURNING[0m jsonb) AS ja, 	JSON_ARRAYAGG(i ORDER BY i RETURNING text) AS ja_text, 	JSON_ARRAYAGG(i ORDER BY i N  Invalid expression / Unexpected token. Line 2, Col: 37.   SELECT i % 2 AS g, 	JSON_ARRAYAGG(i ORDER BY i [4mRETURNING[0m jsonb) AS ja, 	JSON_ARRAYAGG(i ORDER BY i RETURNING text) AS ja_text, 	JSON_ARRAYAGG(i ORDER BY i N |
| 330 | 751–756 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 331 | 757–759 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 27.   SELECT JSON_ARRAYAGG(i [4mNULL[0m ON NULL RETURNING jsonb) OVER (ORDER BY i DESC) AS ja, 	row_number() OVER (ORDER BY i) AS rn FROM g  Invalid expression / Unexpected token. Line 1, Col: 30.   SELECT JSON_ARRAYAGG(i NULL [4mON[0m NULL RETURNING jsonb) OVER (ORDER BY i DESC) AS ja, 	row_number() OVER (ORDER BY i) AS rn FROM gene |
| 332 | 761–768 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 23 | 29–30 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 24 | 31–31 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 25 | 32–32 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 26 | 33–33 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 27 | 34–34 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 28 | 35–35 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 29 | 36–36 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 30 | 37–37 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 31 | 38–38 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 32 | 39–39 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 33 | 40–40 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 34 | 41–41 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 35 | 42–42 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_scalar；本次不安装 UDF |
| 38 | 47–48 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 39 | 49–49 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 40 | 50–50 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 41 | 51–51 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 42 | 52–52 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 46 | 56–56 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_serialize；本次不安装 UDF |
| 106 | 163–163 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_object_inline_test；本次不安装 UDF |
| 111 | 173–173 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 115 | 178–179 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 129 | 194–194 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 139 | 207–208 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 140 | 209–209 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 142 | 211–213 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 144 | 216–217 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 145 | 218–218 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 151 | 235–236 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 152 | 237–237 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 153 | 238–238 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_array；本次不安装 UDF |
| 156 | 249–250 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 157 | 252–253 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 162 | 280–285 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：json_arrayagg；本次不安装 UDF |
| 166 | 296–302 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 174 | 332–333 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 283 | 570–571 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 284 | 572–572 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 285 | 574–575 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 286 | 575–576 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 287 | 576–579 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 291 | 594–594 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 294 | 598–598 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 297 | 610–611 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 304 | 640–651 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 305 | 653–664 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 306 | 666–677 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 307 | 679–690 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 315 | 708–708 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 322 | 722–722 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：volatile_one；本次不安装 UDF |
| 324 | 724–724 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：stable_one；本次不安装 UDF |

参考输出：`assets/sqljson.out`；SHA-256（文件内容指纹）：`2ad89ffcb3053ce19283794f837584360a4fc6bb72d733d45bc79383c5cba3c5`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 85/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 85/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 55/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 55/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 55/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-sqljson-0001-77f7d4f6` | SELECT JSON(); | 已生成 | 失败：语法解析失败 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-sqljson-0002-346f0009` | SELECT JSON(NULL); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0003-a9569d2c` | SELECT JSON('{ "a" : 1 } '); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0007-7e3bd2d6` | SELECT pg_typeof(JSON('{ "a" : 1 } ')); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0008-08261502` | SELECT JSON('   1   '::json); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0009-9360d8e4` | SELECT JSON('   1   '::jsonb); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0011-44407adb` | SELECT JSON(123); | 已生成 | 失败：类型转换失败 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-sqljson-0012-15c90301` | SELECT JSON('{"a": 1, "a": 2}'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0022-d7d54d91` | SELECT pg_typeof(JSON('123')); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0050-90a4ab71` | SELECT JSON_OBJECT(); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-sqljson-0051-e3442d62` | SELECT JSON_OBJECT(RETURNING json); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0052-39a48994` | SELECT JSON_OBJECT(RETURNING json FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0053-8e6196dd` | SELECT JSON_OBJECT(RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0054-93e19cf4` | SELECT JSON_OBJECT(RETURNING jsonb FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0055-bf277f7e` | SELECT JSON_OBJECT(RETURNING text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0056-27679350` | SELECT JSON_OBJECT(RETURNING text FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0057-4e7cbe3a` | SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING UTF8); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0058-85507464` | SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING INVALID_ENCODING); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0059-1e1245ec` | SELECT JSON_OBJECT(RETURNING bytea); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0060-b4f9dd0f` | SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0061-488b91cc` | SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF8); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0062-93593d80` | SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF16); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0063-4b63a422` | SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF32); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0064-0d7459f4` | SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0065-9043d551` | SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON ENCODING UTF8); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0066-195f92ad` | SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0067-59f72b1a` | SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON ENCODING UTF8); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0068-134f492c` | SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0069-df18a825` | SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON ENCODING UTF8); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0070-3ed43f9d` | SELECT JSON_OBJECT(NULL: 1); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0071-d2f3c48a` | SELECT JSON_OBJECT('a': 2 + 3); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0072-d2f3c48a` | SELECT JSON_OBJECT('a' VALUE 2 + 3); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0074-47c9e80c` | SELECT JSON_OBJECT(('a' \|\| 2) VALUE 1); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0075-671952eb` | SELECT JSON_OBJECT('a': 2::text); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0076-671952eb` | SELECT JSON_OBJECT('a' VALUE 2::text); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0077-ebc7ac8a` | SELECT JSON_OBJECT(1::text: 2); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0078-72a2205c` | SELECT JSON_OBJECT((1::text) VALUE 2); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0080-13b666a6` | SELECT JSON_OBJECT(ARRAY[1,2,3]: 'aaa'); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-sqljson-0081-b9d917c8` | SELECT JSON_OBJECT( 	'a': '123', 	1.23: 123, 	'c': json '[ 1,true,{ } ]', 	'd': jsonb '{ "x" : 123.45 }' ); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0082-793614ae` | SELECT JSON_OBJECT( 	'a': '123', 	1.23: 123, 	'c': json '[ 1,true,{ } ]', 	'd': jsonb '{ "x" : 123.45 }' 	RETURNING jsonb ); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0083-aaaaf0cc` | SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa')); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0084-fe2afc9b` | SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa' RETURNING jsonb)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0085-cf7e7536` | SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0086-c06829ab` | SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text) FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0087-390d22a4` | SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0088-00c725f2` | SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea) FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0089-ccef3b65` | SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-sqljson-0090-4100b949` | SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 NULL ON NULL); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0091-d5dec91a` | SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 ABSENT ON NULL); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0092-3790e5f7` | SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, repeat('x', 1000): 1, 2: repeat('a', 100) WITH UNIQUE); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0093-acbaa7d0` | SELECT JSON_OBJECT(1: 1, '1': NULL WITH UNIQUE); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0094-f73d48c0` | SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0095-8c86e00c` | SELECT JSON_OBJECT(1: 1, '1': NULL NULL ON NULL WITH UNIQUE RETURNING jsonb); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0096-1dd063a7` | SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE RETURNING jsonb); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0097-0e919246` | SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 NULL ON NULL WITH UNIQUE); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0098-89651d9e` | SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0099-58eb4d86` | SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0100-4b5d20e7` | SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE RETURNING jsonb); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0101-593d412a` | SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0102-fd2215ab` | SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, 4: NULL, '5': 'a' ABSENT ON NULL WITH UNIQUE RETURNING jsonb); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0103-9cacb58a` | SELECT CASE 'x' WHEN JSON_OBJECT('a': 'b' RETURNING text) THEN 1 ELSE 0 END; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0163-abd3e937` | SELECT	JSON_OBJECTAGG('key': 1) IS NULL, 		JSON_OBJECTAGG('key': 1 RETURNING jsonb) IS NULL WHERE FALSE; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0164-af03a290` | SELECT JSON_OBJECTAGG(NULL: 1); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-sqljson-0165-a1180034` | SELECT JSON_OBJECTAGG(NULL: 1 RETURNING jsonb); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0167-73cfdf71` | SELECT 	JSON_OBJECTAGG(k: v), 	JSON_OBJECTAGG(k: v NULL ON NULL), 	JSON_OBJECTAGG(k: v ABSENT ON NULL), 	JSON_OBJECTAGG(k: v RETURNING jsonb), 	JSON_OBJECTAGG(k: v NULL ON NULL RETURNING jsonb), 	JSON_OBJECTAGG(k: v ABSENT ON NULL RETURNING jsonb) FROM 	(VALUES (1, 1), (1, NULL), (2, NULL), (3, 3)) foo(k, v); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0168-c9ed413f` | SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS) FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0169-37cd8fa3` | SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS) FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0170-c919f1c8` | SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS) FROM (VALUES (1, 1), (0, NULL), (3, NULL), (2, 2), (4, NULL)) foo(k, v); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0171-2e6e989c` | SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS RETURNING jsonb) FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0172-dcca672d` | SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb) FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0173-d56175c2` | SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb) FROM (VALUES (1, 1), (0, NULL),(4, null), (5, null),(6, null),(2, 2)) foo(k, v); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0178-9008fe3b` | SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k) FROM (VALUES (1,1), (2,2)) a(k,v); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0179-042a7503` | SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k) FROM (VALUES (1,1), (1,2), (2,2)) a(k,v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0180-cd2e0593` | SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL WITH UNIQUE KEYS)    OVER (ORDER BY k) FROM (VALUES (1,1), (1,null), (2,2)) a(k,v); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0181-cd2e0593` | SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL) OVER (ORDER BY k) FROM (VALUES (1,1), (1,null), (2,2)) a(k,v); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0182-0b849be1` | SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL) OVER (ORDER BY k RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) FROM (VALUES (1,1), (1,null), (2,2)) a(k,v); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-sqljson-0271-ef876352` | SELECT NULL IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0272-4206dfb2` | SELECT NULL IS NOT JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0273-41ef498e` | SELECT NULL::json IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0274-b22967f6` | SELECT NULL::jsonb IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0275-e37eaee8` | SELECT NULL::text IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0276-3725ca72` | SELECT NULL::bytea IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0277-a43252a0` | SELECT NULL::int IS JSON; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0300-c4b3e4db` | SELECT '' IS JSON; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-sqljson-0301-fa18fe76` | SELECT bytea '\x00' IS JSON; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0312-4933fc10` | SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING varchar(2))); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-sqljson-0326-0f327300` | SELECT JSON_OBJECT('a': JSON_OBJECTAGG('b': 1 RETURNING text) FORMAT JSON); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-sqljson-0001-77f7d4f6 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON();
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON()
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`syntax error at or near ")"`。

错误原文：

```text
syntax error at or near ")"
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 30.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=syntax error at or near ")"
source_error_code=syntax error at or near ")"
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0002-346f0009 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON(NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON(NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json: unknown / 原生类型未知。
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
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0003-a9569d2c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON('{ "a" : 1 } ');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON('{ "a" : 1 } ')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{ \"a\" : 1 }"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0007-7e3bd2d6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_typeof(JSON('{ "a" : 1 } '));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_TYPEOF(JSON('{ "a" : 1 } '))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_typeof: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "json"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0008-08261502 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON('   1   '::json);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON(CAST('   1   ' AS JSON))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0009-9360d8e4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON('   1   '::jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON(CAST('   1   ' AS JSONB))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0011-44407adb — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON(123);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON(123)
```

#### 源端参考结果

- 执行状态：失败：类型转换失败；耗时 0.0 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`cannot cast type integer to json`。

错误原文：

```text
cannot cast type integer to json
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=CAST_ERROR
source_error_message=cannot cast type integer to json
source_error_code=cannot cast type integer to json
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0012-15c90301 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON('{"a": 1, "a": 2}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON('{"a": 1, "a": 2}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": 1, \"a\": 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0022-d7d54d91 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_typeof(JSON('123'));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_TYPEOF(JSON('123'))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_typeof: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "json"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON'")
doris_error_code=1105
```

### pg-sqljson-0051-e3442d62 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING json);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `json`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0052-39a48994 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING json FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `json` FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '`json`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0053-8e6196dd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0054-93e19cf4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING jsonb FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `jsonb` FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '`jsonb`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0055-bf277f7e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `text`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0056-27679350 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING text FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `text` FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0057-4e7cbe3a — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING UTF8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `text` FORMAT JSON ENCODING UTF8)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot set JSON encoding for non-bytea output types`。

错误原文：

```text
cannot set JSON encoding for non-bytea output types
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0058-85507464 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING text FORMAT JSON ENCODING INVALID_ENCODING);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING `text` FORMAT JSON ENCODING INVALID_ENCODING)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unrecognized JSON encoding: invalid_encoding`。

错误原文：

```text
unrecognized JSON encoding: invalid_encoding
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '`text`' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0059-1e1245ec — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING bytea);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING bytea)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x7b7d"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0060-b4f9dd0f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x7b7d"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0061-488b91cc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON ENCODING UTF8)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x7b7d"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0062-93593d80 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF16);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON ENCODING UTF16)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unsupported JSON encoding`。

错误原文：

```text
unsupported JSON encoding
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0063-4b63a422 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(RETURNING bytea FORMAT JSON ENCODING UTF32);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT( RETURNING bytea FORMAT JSON ENCODING UTF32)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unsupported JSON encoding`。

错误原文：

```text
unsupported JSON encoding
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'bytea' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0064-0d7459f4 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS INT) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot use non-string types with explicit FORMAT JSON clause`。

错误原文：

```text
cannot use non-string types with explicit FORMAT JSON clause
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0065-9043d551 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::int FORMAT JSON ENCODING UTF8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS INT) FORMAT JSON ENCODING UTF8)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON ENCODING clause is only allowed for bytea input type`。

错误原文：

```text
JSON ENCODING clause is only allowed for bytea input type
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0066-195f92ad — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSON) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"foo\" : null}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
doris_error_code=1105
```

### pg-sqljson-0067-59f72b1a — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::json FORMAT JSON ENCODING UTF8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSON) FORMAT JSON ENCODING UTF8)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON ENCODING clause is only allowed for bytea input type`。

错误原文：

```text
JSON ENCODING clause is only allowed for bytea input type
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0068-134f492c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSONB) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"foo\": null}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-sqljson-0069-df18a825 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT('foo': NULL::jsonb FORMAT JSON ENCODING UTF8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('foo', CAST(NULL AS JSONB) FORMAT JSON ENCODING UTF8)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`JSON ENCODING clause is only allowed for bytea input type`。

错误原文：

```text
JSON ENCODING clause is only allowed for bytea input type
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'FORMAT' expecting {')', ',', 'ORDER'}(line 1, pos 46)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0070-3ed43f9d — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(NULL: 1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(NULL, 1)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`null value not allowed for object key`。

错误原文：

```text
null value not allowed for object key
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = json_object key can't be NULL: json_object(NULL, 1)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0071-d2f3c48a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': 2 + 3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', 2 + 3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : 5}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：JSON_OBJECT('a', 2 + 3): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":5}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0072-d2f3c48a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a' VALUE 2 + 3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', 2 + 3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : 5}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.0 ms。
- 返回行数：1；字段：JSON_OBJECT('a', 2 + 3): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":5}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0074-47c9e80c — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT(('a' || 2) VALUE 1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT((CONCAT('a', 2)), 1)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a2\" : 1}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.4 ms。
- 返回行数：1；字段：JSON_OBJECT((CONCAT('a', 2)), 1): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a2\":1}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0075-671952eb — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': 2::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', CAST(2 AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"2\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.0 ms。
- 返回行数：1；字段：JSON_OBJECT('a', CAST(2 AS STRING)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":\"2\"}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0076-671952eb — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a' VALUE 2::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', CAST(2 AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"2\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.7 ms。
- 返回行数：1；字段：JSON_OBJECT('a', CAST(2 AS STRING)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":\"2\"}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0077-ebc7ac8a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT(1::text: 2);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(CAST(1 AS STRING), 2)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\" : 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.1 ms。
- 返回行数：1；字段：JSON_OBJECT(CAST(1 AS STRING), 2): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\":2}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0078-72a2205c — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT((1::text) VALUE 2);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT((CAST(1 AS STRING)), 2)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\" : 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.8 ms。
- 返回行数：1；字段：JSON_OBJECT((CAST(1 AS STRING)), 2): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\":2}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0080-13b666a6 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(ARRAY[1,2,3]: 'aaa');
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-sqljson-0081-b9d917c8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT(
	'a': '123',
	1.23: 123,
	'c': json '[ 1,true,{ } ]',
	'd': jsonb '{ "x" : 123.45 }'
);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '123', 1.23, 123, 'c', '[ 1,true,{ } ]', 'd', CAST('{ "x" : 123.45 }' AS JSONB))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": \"123\", \"c\": [1, true, {}], \"d\": {\"x\": 123.45}, \"1.23\": 123}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 32.0 ms。
- 返回行数：1；字段：JSON_OBJECT('a', '123', 1.23, 123, 'c', '[ 1,true,{ } ]', 'd', CAST('{ "x" : 123.45 }' AS JSONB)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":\"123\",\"1.23\":123,\"c\":\"[ 1,true,{ } ]\",\"d\":{\"x\":123.45}}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0082-793614ae — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(
	'a': '123',
	1.23: 123,
	'c': json '[ 1,true,{ } ]',
	'd': jsonb '{ "x" : 123.45 }'
	RETURNING jsonb
);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '123', 1.23, 123, 'c', '[ 1,true,{ } ]', 'd', CAST('{ "x" : 123.45 }' AS JSONB) RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": \"123\", \"c\": [1, true, {}], \"d\": {\"x\": 123.45}, \"1.23\": 123}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 104)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 104)\n")
doris_error_code=1105
```

### pg-sqljson-0083-aaaaf0cc — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa'));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '123', 'b', JSON_OBJECT('a', 111, 'b', 'aaa'))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"123\", \"b\" : {\"a\" : 111, \"b\" : \"aaa\"}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.9 ms。
- 返回行数：1；字段：JSON_OBJECT('a', '123', 'b', JSON_OBJECT('a', 111, 'b', 'aaa')): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":\"123\",\"b\":{\"a\":111,\"b\":\"aaa\"}}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0084-fe2afc9b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': '123', 'b': JSON_OBJECT('a': 111, 'b': 'aaa' RETURNING jsonb));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '123', 'b', JSON_OBJECT('a', 111, 'b', 'aaa' RETURNING `jsonb`))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": \"123\", \"b\": {\"a\": 111, \"b\": \"aaa\"}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 69)\n")
doris_error_code=1105
```

### pg-sqljson-0085-cf7e7536 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING `text`))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"{\\\"b\\\" : 1}\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0086-c06829ab — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING text) FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING `text`) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : {\"b\" : 1}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0087-390d22a4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING bytea))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"\\\\x7b226222203a20317d\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0088-00c725f2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING bytea) FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING bytea) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : {\"b\" : 1}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0089-ccef3b65 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"1\", \"b\" : null, \"c\" : 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 17.2 ms。
- 返回行数：1；字段：JSON_OBJECT('a', '1', 'b', NULL, 'c', 2): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\":\"1\",\"b\":null,\"c\":2}"
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Normalized result row values differ
```

### pg-sqljson-0090-4100b949 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 NULL ON NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2 NULL ON NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"1\", \"b\" : null, \"c\" : 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
doris_error_code=1105
```

### pg-sqljson-0091-d5dec91a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': '1', 'b': NULL, 'c': 2 ABSENT ON NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', '1', 'b', NULL, 'c', 2 ABSENT ON NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : \"1\", \"c\" : 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 47)\n")
doris_error_code=1105
```

### pg-sqljson-0092-3790e5f7 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, repeat('x', 1000): 1, 2: repeat('a', 100) WITH UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '3', 1, REPEAT('x', 1000), 1, 2, REPEAT('a', 100) WITH UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "2"`。

错误原文：

```text
duplicate JSON object key value: "2"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 86)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0093-acbaa7d0 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '1': NULL WITH UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '1', NULL WITH UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0094-f73d48c0 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '1', NULL ABSENT ON NULL WITH UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0095-8c86e00c — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '1': NULL NULL ON NULL WITH UNIQUE RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '1', NULL NULL ON NULL WITH UNIQUE KEYS RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value`。

错误原文：

```text
duplicate JSON object key value
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0096-1dd063a7 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '1': NULL ABSENT ON NULL WITH UNIQUE RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '1', NULL ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value`。

错误原文：

```text
duplicate JSON object key value
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 35)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0097-0e919246 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 NULL ON NULL WITH UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 NULL ON NULL WITH UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0098-89651d9e — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITH UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0099-58eb4d86 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITHOUT UNIQUE KEYS)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\" : 1, \"1\" : 1}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 14.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0100-4b5d20e7 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITH UNIQUE RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value`。

错误原文：

```text
duplicate JSON object key value
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0101-593d412a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '1': 1 ABSENT ON NULL WITHOUT UNIQUE RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '1', 1 ABSENT ON NULL WITHOUT UNIQUE KEYS RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\": 1}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-sqljson-0102-fd2215ab — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT(1: 1, '2': NULL, '3': 1, 4: NULL, '5': 'a' ABSENT ON NULL WITH UNIQUE RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT(1, 1, '2', NULL, '3', 1, 4, NULL, '5', 'a' ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\": 1, \"3\": 1, \"5\": \"a\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 62)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 62)\n")
doris_error_code=1105
```

### pg-sqljson-0103-9cacb58a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT CASE 'x' WHEN JSON_OBJECT('a': 'b' RETURNING text) THEN 1 ELSE 0 END;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CASE 'x' WHEN JSON_OBJECT('a', 'b' RETURNING `text`) THEN 1 ELSE 0 END
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：case: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-sqljson-0163-abd3e937 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT	JSON_OBJECTAGG('key': 1) IS NULL,
		JSON_OBJECTAGG('key': 1 RETURNING jsonb) IS NULL
WHERE FALSE;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG('key', 1) IS NULL, JSON_OBJECTAGG('key', 1 RETURNING `jsonb`) IS NULL WHERE FALSE
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知, ?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 65)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 65)\n")
doris_error_code=1105
```

### pg-sqljson-0164-af03a290 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(NULL: 1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(NULL, 1)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`null value not allowed for object key`。

错误原文：

```text
null value not allowed for object key
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_OBJECTAGG'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=null value not allowed for object key
source_error_code=null value not allowed for object key
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_OBJECTAGG'")
doris_error_code=1105
```

### pg-sqljson-0165-a1180034 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(NULL: 1 RETURNING jsonb);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(NULL, 1 RETURNING `jsonb`)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`field name must not be null`。

错误原文：

```text
field name must not be null
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 30)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0167-73cfdf71 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
	JSON_OBJECTAGG(k: v),
	JSON_OBJECTAGG(k: v NULL ON NULL),
	JSON_OBJECTAGG(k: v ABSENT ON NULL),
	JSON_OBJECTAGG(k: v RETURNING jsonb),
	JSON_OBJECTAGG(k: v NULL ON NULL RETURNING jsonb),
	JSON_OBJECTAGG(k: v ABSENT ON NULL RETURNING jsonb)
FROM
	(VALUES (1, 1), (1, NULL), (2, NULL), (3, 3)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v), JSON_OBJECTAGG(k, v NULL ON NULL), JSON_OBJECTAGG(k, v ABSENT ON NULL), JSON_OBJECTAGG(k, v RETURNING `jsonb`), JSON_OBJECTAGG(k, v NULL ON NULL RETURNING `jsonb`), JSON_OBJECTAGG(k, v ABSENT ON NULL RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, NULL UNION ALL SELECT 3, 3) AS foo
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_objectagg: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{ \"1\" : 1, \"1\" : null, \"2\" : null, \"3\" : 3 }",
    "{ \"1\" : 1, \"1\" : null, \"2\" : null, \"3\" : 3 }",
    "{ \"1\" : 1, \"3\" : 3 }",
    "{\"1\": null, \"2\": null, \"3\": 3}",
    "{\"1\": null, \"2\": null, \"3\": 3}",
    "{\"1\": 1, \"3\": 3}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'NULL' expecting {')', ',', 'ORDER'}(line 1, pos 49)\n")
doris_error_code=1105
```

### pg-sqljson-0168-c9ed413f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS)
FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v WITH UNIQUE KEYS) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS foo
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0169-37cd8fa3 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS)
FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS foo
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0170-c919f1c8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS)
FROM (VALUES (1, 1), (0, NULL), (3, NULL), (2, 2), (4, NULL)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 0, NULL UNION ALL SELECT 3, NULL UNION ALL SELECT 2, 2 UNION ALL SELECT 4, NULL) AS foo
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_objectagg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{ \"1\" : 1, \"2\" : 2 }"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
doris_error_code=1105
```

### pg-sqljson-0171-2e6e989c — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v WITH UNIQUE KEYS RETURNING jsonb)
FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v WITH UNIQUE KEYS RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS foo
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value`。

错误原文：

```text
duplicate JSON object key value
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0172-dcca672d — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb)
FROM (VALUES (1, 1), (1, NULL), (2, 2)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS foo
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value`。

错误原文：

```text
duplicate JSON object key value
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0173-d56175c2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECTAGG(k: v ABSENT ON NULL WITH UNIQUE KEYS RETURNING jsonb)
FROM (VALUES (1, 1), (0, NULL),(4, null), (5, null),(6, null),(2, 2)) foo(k, v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS RETURNING `jsonb`) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 0, NULL UNION ALL SELECT 4, NULL UNION ALL SELECT 5, NULL UNION ALL SELECT 6, NULL UNION ALL SELECT 2, 2) AS foo
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_objectagg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"1\": 1, \"2\": 2}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n")
doris_error_code=1105
```

### pg-sqljson-0178-9008fe3b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k)
FROM (VALUES (1,1), (2,2)) a(k,v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v WITH UNIQUE KEYS) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 2, 2) AS a
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：2；字段：a: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"k\":1,\"v\":1}",
    "{ \"1\" : 1 }"
  ],
  [
    "{\"k\":2,\"v\":2}",
    "{ \"1\" : 1, \"2\" : 2 }"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-0179-042a7503 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v WITH UNIQUE KEYS) OVER (ORDER BY k)
FROM (VALUES (1,1), (1,2), (2,2)) a(k,v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v WITH UNIQUE KEYS) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, 2 UNION ALL SELECT 2, 2) AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'WITH' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0180-cd2e0593 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL WITH UNIQUE KEYS)
   OVER (ORDER BY k)
FROM (VALUES (1,1), (1,null), (2,2)) a(k,v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v ABSENT ON NULL WITH UNIQUE KEYS) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`duplicate JSON object key value: "1"`。

错误原文：

```text
duplicate JSON object key value: "1"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0181-cd2e0593 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL)
OVER (ORDER BY k)
FROM (VALUES (1,1), (1,null), (2,2)) a(k,v);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(a) AS a, JSON_OBJECTAGG(k, v ABSENT ON NULL) OVER (ORDER BY CASE WHEN k IS NULL THEN 1 ELSE 0 END, k) FROM (SELECT 1 AS k, 1 AS v UNION ALL SELECT 1, NULL UNION ALL SELECT 2, 2) AS a
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：a: unknown / 原生类型未知, json_objectagg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"k\":1,\"v\":1}",
    "{ \"1\" : 1 }"
  ],
  [
    "{\"k\":1,\"v\":null}",
    "{ \"1\" : 1 }"
  ],
  [
    "{\"k\":2,\"v\":2}",
    "{ \"1\" : 1, \"2\" : 2 }"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ABSENT' expecting {')', ',', 'ORDER'}(line 1, pos 44)\n")
doris_error_code=1105
```

### pg-sqljson-0182-0b849be1 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT to_json(a) AS a, JSON_OBJECTAGG(k : v ABSENT ON NULL)
OVER (ORDER BY k RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING)
FROM (VALUES (1,1), (1,null), (2,2)) a(k,v);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function J_S_O_N_OBJECT_AGG
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-sqljson-0271-ef876352 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NULL IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-sqljson-0272-4206dfb2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL IS NOT JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NOT NULL IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 19)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 19)\n")
doris_error_code=1105
```

### pg-sqljson-0273-41ef498e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL::json IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(NULL AS JSON) IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 29)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 29)\n")
doris_error_code=1105
```

### pg-sqljson-0274-b22967f6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL::jsonb IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(NULL AS JSONB) IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 30)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 30)\n")
doris_error_code=1105
```

### pg-sqljson-0275-e37eaee8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL::text IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(NULL AS STRING) IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
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
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 31)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 31)\n")
doris_error_code=1105
```

### pg-sqljson-0276-3725ca72 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT NULL::bytea IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(NULL AS VARBINARY) IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 34)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 34)\n")
doris_error_code=1105
```

### pg-sqljson-0277-a43252a0 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT NULL::int IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(NULL AS INT) IS JSON
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot use type integer in IS JSON predicate`。

错误原文：

```text
cannot use type integer in IS JSON predicate
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 28)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0300-c4b3e4db — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '' IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT '' IS JSON
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 13)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 13)\n")
doris_error_code=1105
```

### pg-sqljson-0301-fa18fe76 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT bytea '\x00' IS JSON;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('\\x00' AS VARBINARY) IS JSON
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid byte sequence for encoding "UTF8": 0x00`。

错误原文：

```text
invalid byte sequence for encoding "UTF8": 0x00
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS JSON'(line 1, pos 37)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0312-4933fc10 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECT('b': 1 RETURNING varchar(2)));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECT('b', 1 RETURNING VARCHAR(2)))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value too long for type character varying(2)`。

错误原文：

```text
value too long for type character varying(2)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'RETURNING' expecting {')', ',', 'ORDER'}(line 1, pos 43)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-sqljson-0326-0f327300 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT JSON_OBJECT('a': JSON_OBJECTAGG('b': 1 RETURNING text) FORMAT JSON);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_OBJECT('a', JSON_OBJECTAGG('b', 1 RETURNING `text`) FORMAT JSON)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_object: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\" : { \"b\" : 1 }}"
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
