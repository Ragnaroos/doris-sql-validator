# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:36.008892+00:00 至 2026-11-11T09:40:36.930238+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/xml.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**70**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/70 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/60 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**6**；不计入上述成功匹配分子。
- 需要分析的查询：**70**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**4**；源参考结果不可用：**0**；Doris 执行失败：**66**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 5 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 60 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 1 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 4 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 70 条只读查询、跳过 106 条非查询、0 条待确认、97 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–4 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 6–6 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 7–7 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 8–8 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 10–17 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 47.   SELECT count(*) = 0 AS skip_test FROM xmltest [4m\[0mgset -- pg_regress psql command omitted -- pg_regress psql command omitted -- pg_regress psql comman |
| 35 | 66–66 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 37 | 68–68 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 43 | 77–77 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 26.   SELECT xmlparse(content [4m''[0m);  Invalid expression / Unexpected token. Line 1, Col: 26.   SELECT xmlparse(content [4m''[0m); |
| 44 | 78–78 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 28.   SELECT xmlparse(content [4m'  '[0m);  Invalid expression / Unexpected token. Line 1, Col: 28.   SELECT xmlparse(content [4m'  '[0m); |
| 45 | 79–79 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 29.   SELECT xmlparse(content [4m'abc'[0m);  Invalid expression / Unexpected token. Line 1, Col: 29.   SELECT xmlparse(content [4m'abc'[0m); |
| 46 | 80–80 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 38.   SELECT xmlparse(content [4m'<abc>x</abc>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 38.   SELECT xmlparse(content [4m'<abc>x</abc>'[0m); |
| 47 | 81–81 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT xmlparse(content [4m'<invalidentity>&</invalidentity>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT xmlparse(content [4m'<invalidentity>&</invalidentity>'[0m); |
| 48 | 82–82 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 73.   SELECT xmlparse(content [4m'<undefinedentity>&idontexist;</undefinedentity>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 73.   SELECT xmlparse(content [4m'<undefinedentity>&idontexist;</undefinedentity>'[0m); |
| 49 | 83–83 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 53.   SELECT xmlparse(content [4m'<invalidns xmlns=''&lt;''/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 53.   SELECT xmlparse(content [4m'<invalidns xmlns=''&lt;''/>'[0m); |
| 50 | 84–84 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 58.   SELECT xmlparse(content [4m'<relativens xmlns=''relative''/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT xmlparse(content [4m'<relativens xmlns=''relative''/>'[0m); |
| 51 | 85–85 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 64.   SELECT xmlparse(content [4m'<twoerrors>&idontexist;</unbalanced>  '[0m);  Invalid expression / Unexpected token. Line 1, Col: 64.   SELECT xmlparse(content [4m'<twoerrors>&idontexist;</unbalanced>  '[0m); |
| 52 | 86–86 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 45.   SELECT xmlparse(content [4m'<nosuchprefix:tag/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT xmlparse(content [4m'<nosuchprefix:tag/>'[0m); |
| 53 | 88–88 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 28.   SELECT xmlparse(document [4m'!'[0m);  Invalid expression / Unexpected token. Line 1, Col: 28.   SELECT xmlparse(document [4m'!'[0m); |
| 54 | 89–89 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 30.   SELECT xmlparse(document [4m'abc'[0m);  Invalid expression / Unexpected token. Line 1, Col: 30.   SELECT xmlparse(document [4m'abc'[0m); |
| 55 | 90–90 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT xmlparse(document [4m'<abc>x</abc>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 39.   SELECT xmlparse(document [4m'<abc>x</abc>'[0m); |
| 56 | 91–91 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 51.   SELECT xmlparse(document [4m'<invalidentity>&</abc>  '[0m);  Invalid expression / Unexpected token. Line 1, Col: 51.   SELECT xmlparse(document [4m'<invalidentity>&</abc>  '[0m); |
| 57 | 92–92 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 64.   SELECT xmlparse(document [4m'<undefinedentity>&idontexist;</abc>  '[0m);  Invalid expression / Unexpected token. Line 1, Col: 64.   SELECT xmlparse(document [4m'<undefinedentity>&idontexist;</abc>  '[0m); |
| 58 | 93–93 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 54.   SELECT xmlparse(document [4m'<invalidns xmlns=''&lt;''/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 54.   SELECT xmlparse(document [4m'<invalidns xmlns=''&lt;''/>'[0m); |
| 59 | 94–94 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 59.   SELECT xmlparse(document [4m'<relativens xmlns=''relative''/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 59.   SELECT xmlparse(document [4m'<relativens xmlns=''relative''/>'[0m); |
| 60 | 95–95 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 65.   SELECT xmlparse(document [4m'<twoerrors>&idontexist;</unbalanced>  '[0m);  Invalid expression / Unexpected token. Line 1, Col: 65.   SELECT xmlparse(document [4m'<twoerrors>&idontexist;</unbalanced>  '[0m); |
| 61 | 96–96 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 46.   SELECT xmlparse(document [4m'<nosuchprefix:tag/>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 46.   SELECT xmlparse(document [4m'<nosuchprefix:tag/>'[0m); |
| 62 | 99–99 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mfoo[0m);  Invalid expression / Unexpected token. Line 1, Col: 22.   SELECT xmlpi(name foo[4m)[0m; |
| 63 | 100–100 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mxml[0m);  Invalid expression / Unexpected token. Line 1, Col: 22.   SELECT xmlpi(name xml[4m)[0m; |
| 64 | 101–101 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 26.   SELECT xmlpi(name [4mxmlstuff[0m);  Invalid expression / Unexpected token. Line 1, Col: 27.   SELECT xmlpi(name xmlstuff[4m)[0m; |
| 65 | 102–102 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mfoo[0m, 'bar');  Invalid expression / Unexpected token. Line 1, Col: 29.   SELECT xmlpi(name foo, 'bar'[4m)[0m; |
| 66 | 103–103 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mfoo[0m, 'in?>valid');  Invalid expression / Unexpected token. Line 1, Col: 35.   SELECT xmlpi(name foo, 'in?>valid'[4m)[0m; |
| 67 | 104–104 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mfoo[0m, null);  Invalid expression / Unexpected token. Line 1, Col: 28.   SELECT xmlpi(name foo, null[4m)[0m; |
| 68 | 105–105 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mxml[0m, null);  Invalid expression / Unexpected token. Line 1, Col: 28.   SELECT xmlpi(name xml, null[4m)[0m; |
| 69 | 106–106 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 26.   SELECT xmlpi(name [4mxmlstuff[0m, null);  Invalid expression / Unexpected token. Line 1, Col: 33.   SELECT xmlpi(name xmlstuff, null[4m)[0m; |
| 70 | 107–107 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 34.   SELECT xmlpi(name [4m"xml-stylesheet"[0m, 'href="mystyle.css" type="text/css"');  Invalid expression / Unexpected token. Line 1, Col: 73.   SELECT xmlpi(name "xml-stylesheet", 'href="mystyle.css" type="text/css"'[4m)[0m; |
| 71 | 108–108 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 21.   SELECT xmlpi(name [4mfoo[0m, '   bar');  Invalid expression / Unexpected token. Line 1, Col: 32.   SELECT xmlpi(name foo, '   bar'[4m)[0m; |
| 72 | 111–111 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT xmlroot(xml '<foo/>', version [4mno[0m value, standalone no value);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT xmlroot(xml '<foo/>', version no [4mvalue[0m, standalone no value); |
| 73 | 112–112 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 42.   SELECT xmlroot(xml '<foo/>', version [4m'2.0'[0m);  Invalid expression / Unexpected token. Line 1, Col: 42.   SELECT xmlroot(xml '<foo/>', version [4m'2.0'[0m); |
| 74 | 113–113 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT xmlroot(xml '<foo/>', version [4mno[0m value, standalone yes);  Invalid expression / Unexpected token. Line 1, Col: 45.   SELECT xmlroot(xml '<foo/>', version no [4mvalue[0m, standalone yes); |
| 75 | 114–114 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 60.   SELECT xmlroot(xml '<?xml version="1.1"?><foo/>', version [4mno[0m value, standalone yes);  Invalid expression / Unexpected token. Line 1, Col: 66.   SELECT xmlroot(xml '<?xml version="1.1"?><foo/>', version no [4mvalue[0m, standalone yes); |
| 76 | 115–115 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 50.   SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no);  Expecting ). Line 1, Col: 50.   SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no);  Invalid expression / Unexpected token. Line 1, Col: 50.   SELECT xmlroot(xmlroot(xml '<foo/>', version [4m'1.0'[0m), version '1.1', standalone no); |
| 77 | 116–116 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 73.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value, standalone no);  Invalid expression / Unexpected token. Line 1, Col: 79.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m, standalone no); |
| 78 | 117–117 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 73.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value, standalone no value);  Invalid expression / Unexpected token. Line 1, Col: 79.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m, standalone no value); |
| 79 | 118–118 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 73.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version [4mno[0m value);  Invalid expression / Unexpected token. Line 1, Col: 79.   SELECT xmlroot('<?xml version="1.1" standalone="yes"?><foo/>', version no [4mvalue[0m); |
| 80 | 121–135 | 导入失败；类型 `parse_error` | Expecting ). Line 13, Col: 15.   S name,       1 + 1 AS num     ),     xmlelement (       NAME qux,       'foo'     )   ),   version [4m'1.0'[0m,   standalone yes );  Invalid expression / Unexpected token. Line 13, Col: 15.   S name,       1 + 1 AS num     ),     xmlelement (       NAME qux,       'foo'     )   ),   version [4m'1.0'[0m,   standalone yes ); |
| 81 | 138–138 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 32.   SELECT xmlserialize(content [4mdata[0m as character varying(20)) FROM xmltest;  Invalid expression / Unexpected token. Line 1, Col: 35.   SELECT xmlserialize(content data [4mas[0m character varying(20)) FROM xmltest; |
| 82 | 139–139 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 34.   SELECT xmlserialize(content [4m'good'[0m as char(10));  Invalid expression / Unexpected token. Line 1, Col: 34.   SELECT xmlserialize(content [4m'good'[0m as char(10)); |
| 83 | 140–140 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 34.   SELECT xmlserialize(document [4m'bad'[0m as text);  Invalid expression / Unexpected token. Line 1, Col: 34.   SELECT xmlserialize(document [4m'bad'[0m as text); |
| 84 | 142–143 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT); |
| 85 | 144–144 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text INDENT); |
| 86 | 145–146 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT); |
| 87 | 147–147 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text NO INDENT); |
| 88 | 148–149 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 74.   SELECT xmlserialize(DOCUMENT [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 74.   SELECT xmlserialize(DOCUMENT [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 89 | 150–150 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 74.   SELECT xmlserialize(CONTENT  [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 74.   SELECT xmlserialize(CONTENT  [4m'<foo>73</foo><bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 90 | 151–152 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 92.   SELECT xmlserialize(DOCUMENT [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 92.   SELECT xmlserialize(DOCUMENT [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 91 | 153–153 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 92.   SELECT xmlserialize(CONTENT  [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 92.   SELECT xmlserialize(CONTENT  [4m'text node<foo>73</foo>text node<bar><val x="y">42</val></bar>'[0m AS text INDENT); |
| 92 | 154–155 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 111.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 111.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT); |
| 93 | 156–156 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 111.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 111.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val><val x="y">text node<val>73</val></val></bar></foo>'[0m AS text INDENT); |
| 94 | 157–158 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 31.   SELECT xmlserialize(DOCUMENT [4m''[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 31.   SELECT xmlserialize(DOCUMENT [4m''[0m AS text INDENT); |
| 95 | 159–159 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 31.   SELECT xmlserialize(CONTENT  [4m''[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 31.   SELECT xmlserialize(CONTENT  [4m''[0m AS text INDENT); |
| 96 | 160–161 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT xmlserialize(DOCUMENT [4m'  '[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 33.   SELECT xmlserialize(DOCUMENT [4m'  '[0m AS text INDENT); |
| 97 | 162–162 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT xmlserialize(CONTENT  [4m'  '[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 33.   SELECT xmlserialize(CONTENT  [4m'  '[0m AS text INDENT); |
| 98 | 163–164 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT xmlserialize(DOCUMENT [4mNULL[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT xmlserialize(DOCUMENT NULL [4mAS[0m text INDENT); |
| 99 | 165–165 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 33.   SELECT xmlserialize(CONTENT  [4mNULL[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 36.   SELECT xmlserialize(CONTENT  NULL [4mAS[0m text INDENT); |
| 100 | 166–167 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 104.   SELECT xmlserialize(DOCUMENT [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 104.   SELECT xmlserialize(DOCUMENT [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT); |
| 101 | 168–168 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 104.   SELECT xmlserialize(CONTENT  [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 104.   SELECT xmlserialize(CONTENT  [4m'<?xml version="1.0" encoding="UTF-8"?><foo><bar><val>73</val></bar></foo>'[0m AS text INDENT); |
| 102 | 169–170 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT xmlserialize(DOCUMENT [4m'<!DOCTYPE a><a/>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 47.   SELECT xmlserialize(DOCUMENT [4m'<!DOCTYPE a><a/>'[0m AS text INDENT); |
| 103 | 171–171 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 47.   SELECT xmlserialize(CONTENT  [4m'<!DOCTYPE a><a/>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 47.   SELECT xmlserialize(CONTENT  [4m'<!DOCTYPE a><a/>'[0m AS text INDENT); |
| 104 | 172–173 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 53.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 53.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar></bar></foo>'[0m AS text INDENT); |
| 105 | 174–174 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 53.   SELECT xmlserialize(CONTENT  [4m'<foo><bar></bar></foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 53.   SELECT xmlserialize(CONTENT  [4m'<foo><bar></bar></foo>'[0m AS text INDENT); |
| 106 | 175–176 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(DOCUMENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(DOCUMENT [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(DOCUMENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT); |
| 107 | 177–177 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(CONTENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT);  Invalid expression / Unexpected token. Line 1, Col: 72.   SELECT xmlserialize(CONTENT  [4m'<foo><bar><val x="y">42</val></bar></foo>'[0m AS text) = xmlserialize(CONTENT '<foo><bar><val x="y">42</val></bar></foo>' AS text NO INDENT); |
| 108 | 178–179 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 60.   SELECT xmlserialize(DOCUMENT [4m'<foo>   <bar></bar>    </foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 60.   SELECT xmlserialize(DOCUMENT [4m'<foo>   <bar></bar>    </foo>'[0m AS text INDENT); |
| 109 | 180–180 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 69.   SELECT xmlserialize(CONTENT  [4m'text node<foo>    <bar></bar>   </foo>'[0m AS text INDENT);  Invalid expression / Unexpected token. Line 1, Col: 69.   SELECT xmlserialize(CONTENT  [4m'text node<foo>    <bar></bar>   </foo>'[0m AS text INDENT); |
| 110 | 182–211 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 120 | 233–235 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 39.   SELECT xmlpi(name [4m":::_xml_abc135.%-&_"[0m);  Invalid expression / Unexpected token. Line 1, Col: 40.   SELECT xmlpi(name ":::_xml_abc135.%-&_"[4m)[0m; |
| 121 | 236–236 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 23.   SELECT xmlpi(name [4m"123"[0m);  Invalid expression / Unexpected token. Line 1, Col: 24.   SELECT xmlpi(name "123"[4m)[0m; |
| 122 | 239–239 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 123 | 241–241 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 124 | 242–242 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 125 | 243–243 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 127 | 246–246 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 128 | 247–247 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 129 | 248–248 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 136 | 257–259 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 137 | 260–260 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 138 | 261–261 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 139 | 262–262 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 140 | 263–263 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 62.   CREATE VIEW xmlview5 AS SELECT xmlparse(content [4m'<abc>x</abc>'[0m); |
| 141 | 264–264 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 45.   CREATE VIEW xmlview6 AS SELECT xmlpi(name [4mfoo[0m, 'bar');  Invalid expression / Unexpected token. Line 1, Col: 53.   CREATE VIEW xmlview6 AS SELECT xmlpi(name foo, 'bar'[4m)[0m; |
| 142 | 265–265 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 63.   CREATE VIEW xmlview7 AS SELECT xmlroot(xml '<foo/>', version [4mno[0m value, standalone yes); |
| 143 | 266–266 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 58.   CREATE VIEW xmlview8 AS SELECT xmlserialize(content [4m'good'[0m as char(10)); |
| 144 | 267–267 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 58.   CREATE VIEW xmlview9 AS SELECT xmlserialize(content [4m'good'[0m as text); |
| 145 | 268–268 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 80.   CREATE VIEW xmlview10 AS SELECT xmlserialize(document [4m'<foo><bar>42</bar></foo>'[0m AS text indent); |
| 146 | 269–269 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 80.   CREATE VIEW xmlview11 AS SELECT xmlserialize(document [4m'<foo><bar>42</bar></foo>'[0m AS character varying no indent); |
| 166 | 295–327 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 167 | 329–330 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 55.   SELECT xmlexists('//town[text() = ''Toronto'']' [4mPASSING[0m BY REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>');  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT xmlexists('//town[text() = ''Toronto'']' PASSING [4mBY[0m REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'); |
| 168 | 331–331 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 55.   SELECT xmlexists('//town[text() = ''Cwmbran'']' [4mPASSING[0m BY REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>');  Invalid expression / Unexpected token. Line 1, Col: 58.   SELECT xmlexists('//town[text() = ''Cwmbran'']' PASSING [4mBY[0m REF '<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'); |
| 169 | 332–332 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 44.   SELECT xmlexists('count(/nosuchtag)' [4mPASSING[0m BY REF '<root/>');  Invalid expression / Unexpected token. Line 1, Col: 47.   SELECT xmlexists('count(/nosuchtag)' PASSING [4mBY[0m REF '<root/>'); |
| 173 | 337–337 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 174 | 338–338 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 175 | 339–339 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 176 | 340–340 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 177 | 342–342 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 66.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m data);  Invalid expression / Unexpected token. Line 1, Col: 66.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m data); |
| 178 | 343–343 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 66.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m BY REF data BY REF);  Invalid expression / Unexpected token. Line 1, Col: 66.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beer' [4mPASSING[0m BY REF data BY REF); |
| 179 | 344–344 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 67.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers' [4mPASSING[0m BY REF data);  Invalid expression / Unexpected token. Line 1, Col: 67.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers' [4mPASSING[0m BY REF data); |
| 180 | 345–345 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 93.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers/name[text() = ''Molson'']' [4mPASSING[0m BY REF data);  Invalid expression / Unexpected token. Line 1, Col: 93.   SELECT COUNT(id) FROM xmltest WHERE xmlexists('/menu/beers/name[text() = ''Molson'']' [4mPASSING[0m BY REF data); |
| 187 | 354–354 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 188 | 355–355 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 189 | 356–356 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 65.   SELECT COUNT(id) FROM xmltest, query WHERE xmlexists(expr [4mPASSING[0m BY REF data);  Invalid expression / Unexpected token. Line 1, Col: 65.   SELECT COUNT(id) FROM xmltest, query WHERE xmlexists(expr [4mPASSING[0m BY REF data); |
| 194 | 365–365 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 209 | 381–381 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 214 | 405–406 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 90.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/passwd">]><foo>&c;</foo>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 90.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/passwd">]><foo>&c;</foo>'[0m); |
| 215 | 407–407 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 96.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/no.such.file">]><foo>&c;</foo>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 96.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE foo [<!ENTITY c SYSTEM "/etc/no.such.file">]><foo>&c;</foo>'[0m); |
| 216 | 408–409 | 导入失败；类型 `parse_error` | Expecting ). Line 1, Col: 175.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"><chapter>&nbsp;</chapter>'[0m);  Invalid expression / Unexpected token. Line 1, Col: 175.   SELECT XMLPARSE(DOCUMENT [4m'<!DOCTYPE chapter PUBLIC "-//OASIS//DTD DocBook XML V4.1.2//EN" "http://www.oasis-open.org/docbook/xml/4.1.2/docbookx.dtd"><chapter>&nbsp;</chapter>'[0m); |
| 217 | 411–412 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 218 | 413–444 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 220 | 460–471 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 222 | 475–477 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 223 | 478–478 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 224 | 480–481 | 导入失败；类型 `parse_error` | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 27.   SELECT * FROM XMLTABLE ([4mROW[0m () PASSING null COLUMNS v1 timestamp) AS f (v1, v2);  Invalid expression / Unexpected token. Line 1, Col: 29.   SELECT * FROM XMLTABLE (ROW [4m([0m) PASSING null COLUMNS v1 timestamp) AS f (v1, v2); |
| 225 | 483–483 | 导入失败；类型 `parse_error` | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 27.   SELECT * FROM XMLTABLE ([4mROW[0m () PASSING null COLUMNS v1 timestamp __pg__is_not_null 1) AS f (v1);  Invalid expression / Unexpected token. Line 1, Col: 29.   SELECT * FROM XMLTABLE (ROW [4m([0m) PASSING null COLUMNS v1 timestamp __pg__is_not_null 1) AS f (v1); |
| 227 | 491–494 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 231 | 509–522 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 232 | 524–524 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 245 | 544–556 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 247 | 561–562 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 248 | 564–565 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 249 | 567–584 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 250 | 586–597 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 253 | 626–639 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 255 | 655–677 | 导入失败；类型 `parse_error` | Required keyword: 'expressions' missing for <class 'sqlglot.expressions.core.Bracket'>. Line 4, Col: 84.    as proargnames,                 case when proargtypes <> '' then array_to_string(proargtypes::oid[][4m,[0m',') end as proargtypes            FROM pg_proc WHERE proname = 'f_leak'),    y AS (SELECT xmlelemen |
| 256 | 679–700 | 导入失败；类型 `parse_error` | Required keyword: 'expressions' missing for <class 'sqlglot.expressions.core.Bracket'>. Line 4, Col: 84.    as proargnames,                 case when proargtypes <> '' then array_to_string(proargtypes::oid[][4m,[0m',') end as proargtypes            FROM pg_proc),    y AS (SELECT xmlelement(name data,              |
| 257 | 702–702 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 258 | 704–704 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 259 | 705–705 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 260 | 706–706 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 261 | 707–707 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 262 | 709–709 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 91.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable('/d/r' PASSING x COLUMNS a int PATH '' [4m\|\|[0m lower(_path) \|\| 'c'); |
| 263 | 710–710 | 导入失败；类型 `parse_error` | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 51.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable([4m([0m'/d/r/' \|\| lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.');  Expecting ). Line 1, Col: 61.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.');  Invalid expression / Unexpected token. Line 1, Col: 61.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH '.'); |
| 264 | 711–711 | 导入失败；类型 `parse_error` | Required keyword: 'this' missing for <class 'sqlglot.expressions.functions.XMLTable'>. Line 1, Col: 51.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable([4m([0m'/d/r/' \|\| lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54);  Expecting ). Line 1, Col: 61.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54);  Invalid expression / Unexpected token. Line 1, Col: 61.   SELECT xmltable.* FROM xmltest2, LATERAL xmltable(('/d/r/' [4m\|\|[0m lower(_path) \|\| 'c') PASSING x COLUMNS a int PATH 'x' DEFAULT ascii(_path) - 54); |
| 8 | 22–22 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 10 | 24–24 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 16 | 34–36 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 17 | 38–38 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 18 | 39–39 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 19 | 40–40 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 20 | 41–41 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 21 | 42–42 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 22 | 43–43 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 23 | 44–44 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlconcat；本次不安装 UDF |
| 24 | 47–49 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 25 | 51–52 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 27 | 56–56 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 28 | 58–58 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 39 | 71–71 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 40 | 72–72 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 41 | 73–73 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 42 | 74–74 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖自定义/无法确认的函数或构造器：xmlattributes；本次不安装 UDF |
| 117 | 228–228 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 118 | 229–229 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 119 | 230–230 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 126 | 244–244 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 130 | 249–249 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 131 | 250–250 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 132 | 251–251 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 133 | 252–252 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 134 | 253–253 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 135 | 254–254 | 跳过非查询；类型 `deferred_environment_dependency` | XML 输入涉及 DTD/外部实体；本轮不执行可能访问外部资源的查询 |
| 147 | 271–272 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 148 | 274–276 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 149 | 277–277 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 181 | 347–347 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 182 | 348–348 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 183 | 349–349 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 184 | 350–350 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 185 | 351–351 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 186 | 352–352 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 219 | 446–458 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 221 | 473–473 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 226 | 485–489 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 228 | 496–496 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 229 | 498–503 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 230 | 505–507 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 233 | 526–526 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 234 | 527–527 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 235 | 528–528 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 236 | 529–529 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 237 | 530–530 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 238 | 531–531 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 239 | 532–532 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 240 | 534–534 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 241 | 535–535 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 242 | 535–538 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 243 | 540–541 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 244 | 542–542 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 246 | 558–559 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 251 | 599–610 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 252 | 612–624 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 254 | 641–653 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 265 | 713–714 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 266 | 715–716 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 267 | 717–719 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/xml.out`；SHA-256（文件内容指纹）：`0d1da2a7e6fa501bd4606e93f9577c27dff5266a64cd803938874ba3f33bc72d`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 66/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 66/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 60/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 60/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 60/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-xml-0006-3da45c5b` | SELECT pg_input_is_valid('<value>one</value>', 'xml'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0007-1fc6788e` | SELECT pg_input_is_valid('<value>one</', 'xml'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0009-73d43442` | SELECT pg_input_is_valid('<?xml version="1.0" standalone="y"?><foo/>', 'xml'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0011-1b0b43cc` | SELECT xmlcomment('test'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0012-d38a2456` | SELECT xmlcomment('-test'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0013-4d04eeb1` | SELECT xmlcomment('test-'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-xml-0014-c8ea170b` | SELECT xmlcomment('--test'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-xml-0015-e02263c2` | SELECT xmlcomment('te st'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0026-0e66108b` | SELECT xmlelement(name element, xmlelement(name nested, 'stuff')); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0029-deff914b` | SELECT xmlelement(name num, 37); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0030-6137a003` | SELECT xmlelement(name foo, text 'bar'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0031-31a8ba50` | SELECT xmlelement(name foo, xml 'bar'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0032-887a7a59` | SELECT xmlelement(name foo, text 'b<a/>r'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0033-790e6265` | SELECT xmlelement(name foo, xml 'b<a/>r'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0034-0de0843b` | SELECT xmlelement(name foo, array[1, 2, 3]); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-xml-0036-a1df635c` | SELECT xmlelement(name foo, bytea 'bar'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0038-a1df635c` | SELECT xmlelement(name foo, bytea 'bar'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0111-42532778` | SELECT xml '<foo>bar</foo>' IS DOCUMENT; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0112-13862e79` | SELECT xml '<foo>bar</foo><bar>foo</bar>' IS DOCUMENT; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0113-76dc3083` | SELECT xml '<abc/>' IS NOT DOCUMENT; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0114-cf2c8a74` | SELECT xml 'abc' IS NOT DOCUMENT; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0115-bdd66802` | SELECT '<>' IS NOT DOCUMENT; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-xml-0116-06ff7e3d` | SELECT CASE WHEN ('2019-12-16T00:00:00.000'::xml) IS DOCUMENT     THEN (xpath('/*/text()', '2019-12-16T00:00:00.000'::xml))[1]     ELSE '2019-12-16T00:00:00.000'::xml END; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0150-2c905588` | SELECT xpath('', '<!-- error -->'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-xml-0151-c5683e82` | SELECT xpath('//text()', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0152-481c458f` | SELECT xpath('//loc:piece/@id', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-xml-0153-4b9bd07b` | SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-xml-0154-303139cc` | SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1" xmlns="http://127.0.0.2"><local:piece id="1"><internal>number one</internal><internal2/></local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-xml-0155-47bed3f8` | SELECT xpath('//b', '<a>one <b>two</b> three <b>etc</b></a>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0156-dd022cbd` | SELECT xpath('//text()', '<root>&lt;</root>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0157-0ad3cbce` | SELECT xpath('//@value', '<root value="&lt;"/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0158-402d1ed5` | SELECT xpath('''<<invalid>>''', '<root/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0159-149897d4` | SELECT xpath('count(//*)', '<root><sub/><sub/></root>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0160-2159d462` | SELECT xpath('count(//*)=0', '<root><sub/><sub/></root>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0161-6453f40b` | SELECT xpath('count(//*)=3', '<root><sub/><sub/></root>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0162-d898c649` | SELECT xpath('name(/*)', '<root><sub/><sub/></root>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0163-dd64e568` | SELECT xpath('/nosuchtag', '<root/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0164-1f7be078` | SELECT xpath('root', '<root/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0165-92b15222` | SELECT xpath('//namespace::foo', '<root xmlns:foo="http://127.0.0.1"/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0170-59f81c22` | SELECT xpath_exists('//town[text() = ''Toronto'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0171-1c60ab2d` | SELECT xpath_exists('//town[text() = ''Cwmbran'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0172-be98889b` | SELECT xpath_exists('count(/nosuchtag)', '<root/>'::xml); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0190-155fd751` | SELECT xml_is_well_formed_document('<foo>bar</foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0191-332d1f4a` | SELECT xml_is_well_formed_document('abc'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0192-f6b81b25` | SELECT xml_is_well_formed_content('<foo>bar</foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0193-2bde595b` | SELECT xml_is_well_formed_content('abc'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0195-3a732bd3` | SELECT xml_is_well_formed('abc'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0196-f5fdc51b` | SELECT xml_is_well_formed('<>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0197-bc3cb386` | SELECT xml_is_well_formed('<abc/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0198-8b081a00` | SELECT xml_is_well_formed('<foo>bar</foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0199-a7caf810` | SELECT xml_is_well_formed('<foo>bar</foo'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0200-d01b88ca` | SELECT xml_is_well_formed('<foo><bar>baz</foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0201-1f4ac082` | SELECT xml_is_well_formed('<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0202-7aea02b8` | SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0203-53b2f485` | SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0204-a7526694` | SELECT xml_is_well_formed('<invalidentity>&</abc>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0205-cccedf72` | SELECT xml_is_well_formed('<undefinedentity>&idontexist;</abc>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0206-2fef6086` | SELECT xml_is_well_formed('<invalidns xmlns=''&lt;''/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0207-43d3734b` | SELECT xml_is_well_formed('<relativens xmlns=''relative''/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0208-4135f1c1` | SELECT xml_is_well_formed('<twoerrors>&idontexist;</unbalanced>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0210-3a732bd3` | SELECT xml_is_well_formed('abc'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0211-7470af89` | SELECT xpath('/*', '<invalidns xmlns=''&lt;''/>'); | 已生成 | 失败：语法解析失败 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-xml-0212-a9816d95` | SELECT xpath('/*', '<nosuchprefix:tag/>'); | 已生成 | 失败：语法解析失败 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-xml-0213-64278f8c` | SELECT xpath('/*', '<relativens xmlns=''relative''/>'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0268-7122cca4` | SELECT xmltext(NULL); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0269-0012adb9` | SELECT xmltext(''); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0270-4b4238b0` | SELECT xmltext('  '); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0271-bdcdcd13` | SELECT xmltext('foo `$_-+?=*^%!\|/\()[]{}'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0272-ccdf0a7b` | SELECT xmltext('foo & <"bar">'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-xml-0273-2d89ec89` | SELECT xmltext('x'\|\| '<P>73</P>'::xml \|\| .42 \|\| true \|\| 'j'::char); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-xml-0006-3da45c5b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('<value>one</value>', 'xml');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('<value>one</value>', 'xml')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 17.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-xml-0007-1fc6788e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('<value>one</', 'xml');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('<value>one</', 'xml')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-xml-0009-73d43442 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('<?xml version="1.0" standalone="y"?><foo/>', 'xml');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('<?xml version="1.0" standalone="y"?><foo/>', 'xml')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 18.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-xml-0011-1b0b43cc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlcomment('test');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLCOMMENT('test')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlcomment: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<!--test-->"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
doris_error_code=1105
```

### pg-xml-0012-d38a2456 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlcomment('-test');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLCOMMENT('-test')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlcomment: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<!---test-->"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
doris_error_code=1105
```

### pg-xml-0013-4d04eeb1 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT xmlcomment('test-');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLCOMMENT('test-')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid XML comment`。

错误原文：

```text
invalid XML comment
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=invalid XML comment
source_error_code=invalid XML comment
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
doris_error_code=1105
```

### pg-xml-0014-c8ea170b — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT xmlcomment('--test');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLCOMMENT('--test')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid XML comment`。

错误原文：

```text
invalid XML comment
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=invalid XML comment
source_error_code=invalid XML comment
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
doris_error_code=1105
```

### pg-xml-0015-e02263c2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlcomment('te st');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLCOMMENT('te st')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlcomment: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<!--te st-->"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLCOMMENT'")
doris_error_code=1105
```

### pg-xml-0026-0e66108b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name element, xmlelement(name nested, 'stuff'));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME element, XMLELEMENT(NAME nested, 'stuff'))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<element><nested>stuff</nested></element>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'element' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'element' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0029-deff914b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name num, 37);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME num, 37)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<num>37</num>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'num' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'num' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0030-6137a003 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, text 'bar');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>bar</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0031-31a8ba50 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, xml 'bar');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS XML))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>bar</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0032-887a7a59 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, text 'b<a/>r');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('b<a/>r' AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>b&lt;a/&gt;r</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0033-790e6265 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, xml 'b<a/>r');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('b<a/>r' AS XML))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>b<a/>r</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0034-0de0843b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, array[1, 2, 3]);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-xml-0036-a1df635c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, bytea 'bar');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS VARBINARY))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>YmFy</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0038-a1df635c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmlelement(name foo, bytea 'bar');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLELEMENT(NAME foo, CAST('bar' AS VARBINARY))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmlelement: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "<foo>626172</foo>"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'foo' expecting {')', ',', 'ORDER'}(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-xml-0111-42532778 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml '<foo>bar</foo>' IS DOCUMENT;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('<foo>bar</foo>' AS XML) IS DOCUMENT
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 32)\n")
doris_error_code=1105
```

### pg-xml-0112-13862e79 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml '<foo>bar</foo><bar>foo</bar>' IS DOCUMENT;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('<foo>bar</foo><bar>foo</bar>' AS XML) IS DOCUMENT
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

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-xml-0113-76dc3083 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml '<abc/>' IS NOT DOCUMENT;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NOT CAST('<abc/>' AS XML) IS DOCUMENT
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

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 28)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 28)\n")
doris_error_code=1105
```

### pg-xml-0114-cf2c8a74 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml 'abc' IS NOT DOCUMENT;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NOT CAST('abc' AS XML) IS DOCUMENT
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 25)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 25)\n")
doris_error_code=1105
```

### pg-xml-0115-bdd66802 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT '<>' IS NOT DOCUMENT;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NOT '<>' IS DOCUMENT
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid XML content`。

错误原文：

```text
invalid XML content
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'IS DOCUMENT'(line 1, pos 19)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-xml-0116-06ff7e3d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT CASE WHEN ('2019-12-16T00:00:00.000'::xml) IS DOCUMENT
    THEN (xpath('/*/text()', '2019-12-16T00:00:00.000'::xml))[1]
    ELSE '2019-12-16T00:00:00.000'::xml
END;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CASE WHEN (CAST('2019-12-16T00:00:00.000' AS XML)) IS DOCUMENT THEN (XPATH('/*/text()', CAST('2019-12-16T00:00:00.000' AS XML)))[0] ELSE CAST('2019-12-16T00:00:00.000' AS XML) END
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：case: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2019-12-16T00:00:00.000"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'WHEN' expecting {<EOF>, ';'}(line 1, pos 12)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'WHEN' expecting {<EOF>, ';'}(line 1, pos 12)\n")
doris_error_code=1105
```

### pg-xml-0150-2c905588 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT xpath('', '<!-- error -->');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('', '<!-- error -->')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`empty XPath expression`。

错误原文：

```text
empty XPath expression
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=empty XPath expression
source_error_code=empty XPath expression
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0151-c5683e82 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('//text()', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('//text()', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"number one\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0152-481c458f — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT xpath('//loc:piece/@id', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-xml-0153-4b9bd07b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-xml-0154-303139cc — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT xpath('//loc:piece', '<local:data xmlns:local="http://127.0.0.1" xmlns="http://127.0.0.2"><local:piece id="1"><internal>number one</internal><internal2/></local:piece><local:piece id="2" /></local:data>', ARRAY[ARRAY['loc', 'http://127.0.0.1']]);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-xml-0155-47bed3f8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('//b', '<a>one <b>two</b> three <b>etc</b></a>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('//b', '<a>one <b>two</b> three <b>etc</b></a>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{<b>two</b>,<b>etc</b>}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0156-dd022cbd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('//text()', '<root>&lt;</root>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('//text()', '<root>&lt;</root>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{&lt;}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0157-0ad3cbce — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('//@value', '<root value="&lt;"/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('//@value', '<root value="&lt;"/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{&lt;}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0158-402d1ed5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('''<<invalid>>''', '<root/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('''<<invalid>>''', '<root/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{&lt;&lt;invalid&gt;&gt;}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0159-149897d4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('count(//*)', '<root><sub/><sub/></root>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('count(//*)', '<root><sub/><sub/></root>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{3}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0160-2159d462 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('count(//*)=0', '<root><sub/><sub/></root>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('count(//*)=0', '<root><sub/><sub/></root>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{false}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0161-6453f40b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('count(//*)=3', '<root><sub/><sub/></root>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('count(//*)=3', '<root><sub/><sub/></root>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{true}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0162-d898c649 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('name(/*)', '<root><sub/><sub/></root>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('name(/*)', '<root><sub/><sub/></root>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{root}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0163-dd64e568 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('/nosuchtag', '<root/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('/nosuchtag', '<root/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0164-1f7be078 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('root', '<root/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('root', '<root/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{<root/>}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0165-92b15222 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('//namespace::foo', '<root xmlns:foo="http://127.0.0.1"/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('//namespace::foo', '<root xmlns:foo="http://127.0.0.1"/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{http://127.0.0.1}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0170-59f81c22 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath_exists('//town[text() = ''Toronto'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH_EXISTS('//town[text() = ''Toronto'']', CAST('<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>' AS XML))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath_exists: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
doris_error_code=1105
```

### pg-xml-0171-1c60ab2d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath_exists('//town[text() = ''Cwmbran'']','<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>'::xml);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH_EXISTS('//town[text() = ''Cwmbran'']', CAST('<towns><town>Bidford-on-Avon</town><town>Cwmbran</town><town>Bristol</town></towns>' AS XML))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath_exists: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 146)\n")
doris_error_code=1105
```

### pg-xml-0172-be98889b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath_exists('count(/nosuchtag)', '<root/>'::xml);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH_EXISTS('count(/nosuchtag)', CAST('<root/>' AS XML))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath_exists: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 59)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 59)\n")
doris_error_code=1105
```

### pg-xml-0190-155fd751 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed_document('<foo>bar</foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED_DOCUMENT('<foo>bar</foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed_document: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
doris_error_code=1105
```

### pg-xml-0191-332d1f4a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed_document('abc');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED_DOCUMENT('abc')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed_document: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_DOCUMENT'")
doris_error_code=1105
```

### pg-xml-0192-f6b81b25 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed_content('<foo>bar</foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED_CONTENT('<foo>bar</foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed_content: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
doris_error_code=1105
```

### pg-xml-0193-2bde595b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed_content('abc');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED_CONTENT('abc')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed_content: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED_CONTENT'")
doris_error_code=1105
```

### pg-xml-0195-3a732bd3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('abc');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('abc')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0196-f5fdc51b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0197-bc3cb386 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<abc/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<abc/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0198-8b081a00 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<foo>bar</foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<foo>bar</foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0199-a7caf810 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<foo>bar</foo');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<foo>bar</foo')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0200-d01b88ca — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<foo><bar>baz</foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<foo><bar>baz</foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0201-1f4ac082 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<local:data xmlns:local="http://127.0.0.1"><local:piece id="1">number one</local:piece><local:piece id="2" /></local:data>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 20.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0202-7aea02b8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</my:foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0203-53b2f485 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<pg:foo xmlns:pg="http://postgresql.org/stuff">bar</pg:foo>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0204-a7526694 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<invalidentity>&</abc>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<invalidentity>&</abc>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0205-cccedf72 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<undefinedentity>&idontexist;</abc>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<undefinedentity>&idontexist;</abc>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0206-2fef6086 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<invalidns xmlns=''&lt;''/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<invalidns xmlns=''&lt;''/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0207-43d3734b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<relativens xmlns=''relative''/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<relativens xmlns=''relative''/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0208-4135f1c1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('<twoerrors>&idontexist;</unbalanced>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('<twoerrors>&idontexist;</unbalanced>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0210-3a732bd3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xml_is_well_formed('abc');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XML_IS_WELL_FORMED('abc')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xml_is_well_formed: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XML_IS_WELL_FORMED'")
doris_error_code=1105
```

### pg-xml-0211-7470af89 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT xpath('/*', '<invalidns xmlns=''&lt;''/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('/*', '<invalidns xmlns=''&lt;''/>')
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`could not parse XML document`。

错误原文：

```text
could not parse XML document
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=could not parse XML document
source_error_code=could not parse XML document
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0212-a9816d95 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT xpath('/*', '<nosuchprefix:tag/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('/*', '<nosuchprefix:tag/>')
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`could not parse XML document`。

错误原文：

```text
could not parse XML document
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=could not parse XML document
source_error_code=could not parse XML document
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0213-64278f8c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xpath('/*', '<relativens xmlns=''relative''/>');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XPATH('/*', '<relativens xmlns=''relative''/>')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xpath: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"<relativens xmlns=\\\"relative\\\"/>\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XPATH'")
doris_error_code=1105
```

### pg-xml-0268-7122cca4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext(NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT(NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
doris_error_code=1105
```

### pg-xml-0269-0012adb9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext('');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT('')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
doris_error_code=1105
```

### pg-xml-0270-4b4238b0 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext('  ');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT('  ')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
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
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
doris_error_code=1105
```

### pg-xml-0271-bdcdcd13 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext('foo `$_-+?=*^%!|/\()[]{}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT('foo `$_-+?=*^%!|/\\()[]{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "foo `$_-+?=*^%!|/\\()[]{}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
doris_error_code=1105
```

### pg-xml-0272-ccdf0a7b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext('foo & <"bar">');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT('foo & <"bar">')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "foo &amp; &lt;&quot;bar&quot;&gt;"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'XMLTEXT'")
doris_error_code=1105
```

### pg-xml-0273-2d89ec89 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT xmltext('x'|| '<P>73</P>'::xml || .42 || true || 'j'::char);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT XMLTEXT(CONCAT('x', CAST('<P>73</P>' AS XML), 0.42, TRUE, CAST('j' AS CHAR)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：xmltext: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "x&lt;P&gt;73&lt;/P&gt;0.42truej"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 47)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'XML' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 47)\n")
doris_error_code=1105
```
