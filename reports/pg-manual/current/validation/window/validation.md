# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:23.040929+00:00 至 2026-11-11T09:40:24.083696+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/window.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**65**；两端成功且已有证据匹配：**23**。
- 成功结果匹配占全部查询比例：**23/65 = 35.38%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**23/46 = 50.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**42**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**19**；源参考结果不可用：**0**；Doris 执行失败：**18**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 18 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 23 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 5 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 19 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 65 条只读查询、跳过 375 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–10 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 12–22 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 45 | 150–154 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 74 | 278–280 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 77 | 286–288 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 80 | 294–296 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 83 | 302–304 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 86 | 310–312 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 89 | 318–319 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 92 | 325–325 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 93 | 327–329 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 128 | 504–515 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 130 | 518–524 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 133 | 530–535 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 135 | 538–544 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 138 | 550–551 | 跳过非查询；类型 `drop` | Invalid expression / Unexpected token. Line 1, Col: 38.   DROP FUNCTION unbounded_syntax_test1a[4m,[0m unbounded_syntax_test1b,               unbounded_syntax_test2a, unbounded_syntax_test2b; |
| 139 | 553–554 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 143 | 568–568 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 152 | 602–609 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 153 | 611–621 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 173 | 700–711 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 174 | 713–725 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 245 | 1068–1069 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 246 | 1070–1070 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 248 | 1074–1078 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 253 | 1091–1095 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 263 | 1121–1121 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 264 | 1123–1123 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 272 | 1145–1167 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 273 | 1169–1180 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 275 | 1193–1202 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 276 | 1204–1211 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 277 | 1213–1220 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 281 | 1241–1248 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 283 | 1257–1264 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 285 | 1273–1280 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 287 | 1289–1295 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 289 | 1304–1310 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 290 | 1312–1318 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 291 | 1320–1327 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 292 | 1329–1336 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 294 | 1346–1354 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 295 | 1356–1364 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 297 | 1375–1384 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 298 | 1386–1394 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 299 | 1396–1405 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 301 | 1414–1424 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 303 | 1437–1444 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 304 | 1446–1452 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 305 | 1454–1465 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 306 | 1467–1475 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 307 | 1477–1485 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 308 | 1487–1494 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 309 | 1496–1509 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 310 | 1511–1519 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 311 | 1521–1529 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 312 | 1531–1538 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 313 | 1540–1547 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 314 | 1549–1556 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 315 | 1558–1565 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 316 | 1567–1574 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 317 | 1576–1583 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 318 | 1586–1593 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 319 | 1595–1604 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 320 | 1606–1615 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 321 | 1617–1617 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 322 | 1619–1629 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 323 | 1631–1641 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 324 | 1643–1643 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 325 | 1645–1650 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 326 | 1652–1662 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 328 | 1674–1674 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 329 | 1676–1676 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 330 | 1678–1683 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 331 | 1685–1685 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 332 | 1687–1688 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 333 | 1690–1692 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 57.   CREATE FUNCTION nth_value_def(val anyelement, n integer [4m=[0m 1) RETURNS anyelement   LANGUAGE internal WINDOW IMMUTABLE STRICT AS 'window_nth_value';  Required keyword: 'this' missing for <class 'sqlglot.expressions.properties.Property'>. Line 1, Col: 60.   CREATE FUNCTION nth_value_def(val anyelement, n integer = 1[4m)[0m RETURNS anyelement   LANGUAGE internal WINDOW IMMUTABLE STRICT AS 'window_nth_value';  Invalid expression / Unexpected token. Line 1, Col: 60.   CREATE FUNCTION nth_value_def(val anyelement, n integer = 1[4m)[0m RETURNS anyelement   LANGUAGE internal WINDOW IMMUTABLE STRICT AS 'window_nth_value'; |
| 336 | 1700–1709 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 337 | 1711–1713 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 338 | 1715–1717 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 339 | 1719–1726 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 340 | 1728–1737 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 341 | 1739–1741 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 342 | 1743–1745 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 343 | 1747–1749 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 344 | 1751–1758 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 345 | 1760–1769 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 351 | 1854–1861 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 352 | 1863–1870 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 401 | 2070–2080 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 402 | 2082–2089 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 403 | 2091–2096 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 404 | 2098–2103 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 406 | 2113–2119 | 跳过非查询；类型 `create` | Required keyword: 'expressions' missing for <class 'sqlglot.expressions.core.Bracket'>. Line 2, Col: 2.   CREATE FUNCTION pg_temp.f(group_size BIGINT) RETURNS SETOF integer[] [4mAS[0m $$     SELECT array_agg(s) OVER w       FROM generate_series(1,5) s     WINDOW w AS (ORDER BY s ROW |
| 407 | 2121–2121 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 409 | 2124–2130 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 410 | 2132–2142 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 411 | 2144–2153 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 443 | 2248–2251 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 451 | 2306–2307 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 452 | 2308–2312 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 455 | 2320–2320 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 458 | 2326–2326 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 461 | 2334–2335 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 15 | 53–53 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 55–55 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 18 | 59–59 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 39 | 121–123 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 272–276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 75 | 282–282 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 78 | 290–290 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 298–298 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 84 | 306–306 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 87 | 314–314 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 90 | 321–321 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 95 | 333–336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 338–340 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 342–344 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 346–353 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 355–357 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 359–363 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 365–367 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 369–371 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 103 | 373–375 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 377–379 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 381–383 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 385–387 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 389–391 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 393–395 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 397–399 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 401–402 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 111 | 404–405 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 407–408 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 113 | 410–411 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 114 | 413–414 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 416–417 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 116 | 419–422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 117 | 424–426 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 118 | 428–433 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 119 | 435–438 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 440–443 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 121 | 445–449 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 451–455 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 457–461 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 463–472 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 474–482 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 484–492 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 494–502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 526–527 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 132 | 528–528 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 136 | 546–547 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 548–548 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 140 | 556–558 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 570–573 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 575–576 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 146 | 578–579 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 147 | 581–582 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 148 | 584–585 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 149 | 587–588 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 150 | 590–594 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 151 | 596–600 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 154 | 623–626 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 155 | 627–630 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 156 | 631–634 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 157 | 635–638 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 158 | 639–642 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 159 | 643–646 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 160 | 646–651 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 161 | 652–655 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 162 | 656–659 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 163 | 660–663 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 164 | 664–667 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 165 | 668–671 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 166 | 671–676 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 167 | 677–680 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 168 | 681–684 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 169 | 684–688 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 170 | 689–692 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 171 | 693–696 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 172 | 697–700 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 727–730 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 176 | 732–735 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 737–740 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 178 | 740–745 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 179 | 747–750 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 180 | 752–755 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 181 | 757–761 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 761–766 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 183 | 768–771 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 184 | 773–776 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 185 | 776–781 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 186 | 783–786 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 187 | 788–791 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 188 | 793–797 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 189 | 797–802 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 190 | 804–807 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 191 | 809–812 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 192 | 812–817 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 193 | 819–822 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 194 | 824–827 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 195 | 829–833 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 833–838 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 197 | 840–843 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 198 | 845–848 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 199 | 848–853 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 200 | 855–858 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 201 | 860–863 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 202 | 865–869 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 203 | 869–874 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 204 | 876–879 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 205 | 881–884 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 884–889 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 207 | 891–894 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 896–899 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 209 | 901–905 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 210 | 905–909 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 211 | 911–912 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 212 | 914–915 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 213 | 917–918 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 214 | 920–921 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 215 | 923–924 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 216 | 926–927 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 217 | 929–930 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 218 | 932–936 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 219 | 938–940 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 220 | 942–944 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 221 | 946–948 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 222 | 950–952 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 223 | 954–956 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 224 | 958–960 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 225 | 962–964 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 226 | 966–968 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 227 | 970–972 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 228 | 974–976 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 229 | 978–980 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 230 | 982–984 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 231 | 986–988 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 232 | 990–992 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 233 | 994–996 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 234 | 998–1001 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 235 | 1003–1005 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 236 | 1007–1012 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 237 | 1014–1017 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 238 | 1019–1025 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 239 | 1027–1032 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 240 | 1034–1039 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 241 | 1041–1047 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 242 | 1049–1055 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 243 | 1057–1063 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 244 | 1065–1066 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 247 | 1072–1074 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 249 | 1079–1081 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 250 | 1082–1084 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 251 | 1085–1087 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 252 | 1089–1091 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 254 | 1096–1098 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 255 | 1099–1101 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 256 | 1102–1104 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 257 | 1106–1107 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 258 | 1109–1110 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 259 | 1112–1113 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 260 | 1115–1115 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 261 | 1117–1117 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 262 | 1119–1119 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 265 | 1125–1125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 266 | 1127–1127 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 267 | 1129–1129 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 268 | 1131–1131 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 269 | 1133–1133 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 270 | 1135–1135 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 271 | 1137–1143 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 274 | 1182–1191 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 278 | 1222–1227 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 279 | 1229–1233 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 280 | 1235–1239 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 282 | 1250–1255 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 284 | 1266–1271 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 286 | 1282–1287 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 288 | 1297–1302 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 293 | 1338–1344 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 296 | 1366–1373 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 300 | 1407–1412 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 327 | 1664–1672 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 334 | 1694–1695 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 335 | 1697–1698 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 346 | 1771–1790 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 347 | 1792–1812 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 348 | 1814–1827 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 349 | 1829–1841 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 350 | 1843–1852 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 353 | 1872–1890 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 354 | 1892–1898 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 355 | 1900–1901 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 356 | 1903–1904 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 357 | 1906–1907 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 358 | 1909–1910 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 359 | 1912–1927 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 360 | 1929–1935 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 361 | 1937–1943 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 362 | 1945–1946 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 363 | 1948–1949 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 364 | 1951–1952 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 365 | 1954–1955 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 366 | 1957–1958 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 367 | 1960–1961 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 368 | 1963–1964 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 369 | 1966–1967 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 370 | 1969–1970 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 371 | 1972–1973 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 372 | 1975–1976 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 373 | 1978–1979 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 374 | 1981–1982 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 375 | 1984–1985 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 376 | 1987–1988 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 377 | 1990–1991 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 378 | 1993–1994 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 379 | 1996–1997 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 380 | 1999–2000 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 381 | 2002–2003 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 382 | 2005–2006 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 383 | 2008–2009 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 384 | 2011–2012 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 385 | 2014–2015 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 386 | 2017–2018 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 387 | 2020–2021 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 388 | 2023–2024 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 389 | 2026–2027 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 390 | 2029–2030 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 391 | 2032–2033 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 392 | 2035–2036 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 393 | 2038–2039 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 394 | 2041–2042 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 395 | 2044–2046 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 396 | 2048–2049 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 397 | 2051–2052 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 398 | 2054–2057 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 399 | 2059–2064 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 400 | 2066–2068 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 405 | 2105–2111 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 408 | 2122–2122 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 419 | 2224–2225 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 420 | 2225–2226 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 421 | 2226–2227 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 422 | 2227–2228 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 423 | 2228–2229 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 424 | 2229–2230 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 425 | 2230–2231 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 426 | 2231–2232 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 427 | 2232–2233 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 428 | 2233–2234 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 429 | 2234–2235 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 430 | 2235–2236 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 431 | 2236–2237 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 432 | 2237–2238 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 433 | 2238–2239 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 434 | 2239–2240 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 435 | 2240–2241 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 436 | 2241–2242 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 437 | 2242–2243 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 438 | 2243–2244 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 439 | 2244–2245 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 440 | 2245–2246 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 441 | 2246–2247 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 442 | 2247–2248 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 446 | 2276–2280 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 447 | 2281–2284 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 448 | 2286–2293 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 449 | 2294–2299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 450 | 2300–2304 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 453 | 2314–2317 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 454 | 2318–2318 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 456 | 2321–2323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 457 | 2324–2324 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 459 | 2327–2331 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 460 | 2332–2332 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/window.out`；SHA-256（文件内容指纹）：`386c5ded204f53c8084841076afa45fe7b73046e01e7db4f401a499362ef4aad`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-window-0003-d9b289b5` | SELECT depname, empno, salary, sum(salary) OVER (PARTITION BY depname) FROM empsalary ORDER BY depname, salary; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0004-960303b3` | SELECT depname, empno, salary, rank() OVER (PARTITION BY depname ORDER BY salary) FROM empsalary; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0005-80a45b07` | SELECT four, ten, SUM(SUM(four)) OVER (PARTITION BY four), AVG(ten) FROM tenk1 GROUP BY four, ten ORDER BY four, ten; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-window-0006-bf2d68e1` | SELECT depname, empno, salary, sum(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0007-d8c07fd5` | SELECT depname, empno, salary, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary) ORDER BY rank() OVER w; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0008-53f03910` | SELECT COUNT(*) OVER () FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0009-fbac9f79` | SELECT COUNT(*) OVER w FROM tenk1 WHERE unique2 < 10 WINDOW w AS (); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0010-ac7b0db2` | SELECT four FROM tenk1 WHERE FALSE WINDOW w AS (PARTITION BY ten); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0011-6486afe4` | SELECT sum(four) OVER (PARTITION BY ten ORDER BY unique2) AS sum_1, ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0012-7af7cea6` | SELECT row_number() OVER (ORDER BY unique2) FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0013-e076c183` | SELECT rank() OVER (PARTITION BY four ORDER BY ten) AS rank_1, ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0014-1f84bd82` | SELECT dense_rank() OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0017-22839a3f` | SELECT ntile(3) OVER (ORDER BY ten, four), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0019-4a0f9f7e` | SELECT lag(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0020-3478fa0b` | SELECT lag(ten, four) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0021-2c2c92ba` | SELECT lag(ten, four, 0) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0022-1b2ffa99` | SELECT lag(ten, four, 0.7) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0023-16d45482` | SELECT lead(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0024-b67f33a9` | SELECT lead(ten * 2, 1) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0025-edfe2123` | SELECT lead(ten * 2, 1, -1) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0026-3b0a0a4f` | SELECT lead(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-window-0027-2328adcf` | SELECT first_value(ten) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0028-b7db4122` | SELECT last_value(four) OVER (ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-window-0029-cebcaa74` | SELECT last_value(ten) OVER (PARTITION BY four), ten, four FROM 	(SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s 	ORDER BY four, ten; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-window-0030-297e95fe` | SELECT nth_value(ten, four + 1) OVER (PARTITION BY four), ten, four 	FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0031-bf38d1ba` | SELECT ten, two, sum(hundred) AS gsum, sum(sum(hundred)) OVER (PARTITION BY two ORDER BY ten) AS wsum FROM tenk1 GROUP BY ten, two; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0032-15576266` | SELECT count(*) OVER (PARTITION BY four), four FROM (SELECT * FROM tenk1 WHERE two = 1)s WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0033-329f5631` | SELECT (count(*) OVER (PARTITION BY four ORDER BY ten) +   sum(hundred) OVER (PARTITION BY four ORDER BY ten))::varchar AS cntsum   FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0034-e48cbd50` | SELECT * FROM(   SELECT count(*) OVER (PARTITION BY four ORDER BY ten) +     sum(hundred) OVER (PARTITION BY two ORDER BY ten) AS total,     count(*) OVER (PARTITION BY four ORDER BY ten) AS fourcount,     sum(hundred) OVER (PARTITION BY two ORDER BY ten) AS twosum     FROM tenk1 )sub WHERE total <> fourcount + twosum; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0035-926fba7b` | SELECT avg(four) OVER (PARTITION BY four ORDER BY thousand / 100) FROM tenk1 WHERE unique2 < 10; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-window-0036-1d9414c5` | SELECT ten, two, sum(hundred) AS gsum, sum(sum(hundred)) OVER win AS wsum FROM tenk1 GROUP BY ten, two WINDOW win AS (PARTITION BY two ORDER BY ten); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0037-954ddd27` | SELECT sum(salary), 	row_number() OVER (ORDER BY depname), 	sum(sum(salary)) OVER (ORDER BY depname DESC) FROM empsalary GROUP BY depname; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0038-4aba58d8` | SELECT sum(salary) OVER w1, count(*) OVER w2 FROM empsalary WINDOW w1 AS (ORDER BY salary), w2 AS (ORDER BY salary); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0040-08952902` | SELECT count(*) OVER (PARTITION BY four) FROM (SELECT * FROM tenk1 WHERE FALSE)s; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0041-1b9507b3` | SELECT sum(salary) OVER w, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary DESC); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0042-c250e5f4` | SELECT empno, depname, salary, bonus, depadj, MIN(bonus) OVER (ORDER BY empno), MAX(depadj) OVER () FROM( 	SELECT *, 		CASE WHEN enroll_date < '2008-01-01' THEN 2008 - extract(YEAR FROM enroll_date) END * 500 AS bonus, 		CASE WHEN 			AVG(salary) OVER (PARTITION BY depname) < salary 		THEN 200 END AS depadj FROM empsalary )s; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0043-19c41ea1` | SELECT SUM(COUNT(f1)) OVER () FROM int4_tbl WHERE f1=42; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0044-f6e494e0` | select ten,   sum(unique1) + sum(unique2) as res,   rank() over (order by sum(unique1) + sum(unique2)) as rank from tenk1 group by ten order by ten; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0046-181af42b` | select x, lag(x, 1) over (order by x), lead(x, 3) over (order by x) from (select x::numeric as x from generate_series(1,10) x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0047-b6d9c64a` | SELECT four, ten, 	sum(ten) over (partition by four order by ten), 	last_value(ten) over (partition by four order by ten) FROM (select distinct ten, four from tenk1) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-window-0048-536e1e97` | SELECT four, ten, 	sum(ten) over (partition by four order by ten range between unbounded preceding and current row), 	last_value(ten) over (partition by four order by ten range between unbounded preceding and current row) FROM (select distinct ten, four from tenk1) ss; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0049-f467131d` | SELECT four, ten, 	sum(ten) over (partition by four order by ten range between unbounded preceding and unbounded following), 	last_value(ten) over (partition by four order by ten range between unbounded preceding and unbounded following) FROM (select distinct ten, four from tenk1) ss; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0050-8b853a62` | SELECT four, ten/4 as two, 	sum(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row), 	last_value(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row) FROM (select distinct ten, four from tenk1) ss; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0051-ce3792dc` | SELECT four, ten/4 as two, 	sum(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row), 	last_value(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row) FROM (select distinct ten, four from tenk1) ss; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0052-682b3131` | SELECT sum(unique1) over (order by four range between current row and unbounded following), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0053-57f76f70` | SELECT sum(unique1) over (rows between current row and unbounded following), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0054-dd5aa38f` | SELECT sum(unique1) over (rows between 2 preceding and 2 following), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0055-461f08dc` | SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude no others), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0056-323a4316` | SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude current row), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0057-e7f23b7b` | SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude group), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0058-a6d78a71` | SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude ties), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0059-b05800ec` | SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0060-fb3b911d` | SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0061-82375ee3` | SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0062-c3b04485` | SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0063-39c9997e` | SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0064-2e7cfd65` | SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0065-af9e0271` | SELECT sum(unique1) over (rows between 2 preceding and 1 preceding), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0066-ab2af0c3` | SELECT sum(unique1) over (rows between 1 following and 3 following), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0067-f71d781e` | SELECT sum(unique1) over (rows between unbounded preceding and 1 following), 	unique1, four FROM tenk1 WHERE unique1 < 10; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0068-06f27850` | SELECT sum(unique1) over (w range between current row and unbounded following), 	unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-window-0069-289c97b4` | SELECT sum(unique1) over (w range between unbounded preceding and current row exclude current row), 	unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0070-e6a99045` | SELECT sum(unique1) over (w range between unbounded preceding and current row exclude group), 	unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0071-d0e8311e` | SELECT sum(unique1) over (w range between unbounded preceding and current row exclude ties), 	unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-window-0072-75e7d362` | SELECT first_value(unique1) over w, 	nth_value(unique1, 2) over w AS nth_2, 	last_value(unique1) over w, unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four range between current row and unbounded following); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-window-0005-80a45b07 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT four, ten, SUM(SUM(four)) OVER (PARTITION BY four), AVG(ten) FROM tenk1
GROUP BY four, ten ORDER BY four, ten;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT four, ten, SUM(SUM(four)) OVER (PARTITION BY four), AVG(ten) FROM tenk1 GROUP BY four, ten ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：20；字段：four: unknown / 原生类型未知, ten: unknown / 原生类型未知, sum: unknown / 原生类型未知, avg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0",
    "0.00000000000000000000"
  ],
  [
    "0",
    "2",
    "0",
    "2.0000000000000000"
  ],
  [
    "0",
    "4",
    "0",
    "4.0000000000000000"
  ],
  [
    "0",
    "6",
    "0",
    "6.0000000000000000"
  ],
  [
    "0",
    "8",
    "0",
    "8.0000000000000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 31.4 ms。
- 返回行数：20；字段：four: integer / INT, ten: integer / INT, SUM(SUM(four)) OVER (PARTITION BY four): integer / BIGINT, AVG(ten): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0,
    0,
    0,
    0.0
  ],
  [
    0,
    2,
    0,
    2.0
  ],
  [
    0,
    4,
    0,
    4.0
  ],
  [
    0,
    6,
    0,
    6.0
  ],
  [
    0,
    8,
    0,
    8.0
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

### pg-window-0006-bf2d68e1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT depname, empno, salary, sum(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT depname, empno, salary, SUM(salary) OVER w FROM empsalary WINDOW w AS (PARTITION BY depname)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：depname: unknown / 原生类型未知, empno: unknown / 原生类型未知, salary: unknown / 原生类型未知, sum: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "develop",
    "11",
    "5200",
    "25100"
  ],
  [
    "develop",
    "7",
    "4200",
    "25100"
  ],
  [
    "develop",
    "9",
    "4500",
    "25100"
  ],
  [
    "develop",
    "8",
    "6000",
    "25100"
  ],
  [
    "develop",
    "10",
    "5200",
    "25100"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 48)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 48)\n")
doris_error_code=1105
```

### pg-window-0007-d8c07fd5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT depname, empno, salary, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary) ORDER BY rank() OVER w;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT depname, empno, salary, RANK() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary) ORDER BY CASE WHEN RANK() OVER w IS NULL THEN 1 ELSE 0 END, RANK() OVER w
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：depname: unknown / 原生类型未知, empno: unknown / 原生类型未知, salary: unknown / 原生类型未知, rank: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "develop",
    "7",
    "4200",
    "1"
  ],
  [
    "personnel",
    "5",
    "3500",
    "1"
  ],
  [
    "sales",
    "3",
    "4800",
    "1"
  ],
  [
    "sales",
    "4",
    "4800",
    "1"
  ],
  [
    "personnel",
    "2",
    "3900",
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-window-0009-fbac9f79 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT COUNT(*) OVER w FROM tenk1 WHERE unique2 < 10 WINDOW w AS ();
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT COUNT(*) OVER w FROM tenk1 WHERE unique2 < 10 WINDOW w AS ()
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "10"
  ],
  [
    "10"
  ],
  [
    "10"
  ],
  [
    "10"
  ],
  [
    "10"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 21)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 21)\n")
doris_error_code=1105
```

### pg-window-0010-ac7b0db2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT four FROM tenk1 WHERE FALSE WINDOW w AS (PARTITION BY ten);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT four FROM tenk1 WHERE FALSE WINDOW w AS (PARTITION BY ten)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：0；字段：four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'WINDOW' expecting {<EOF>, ';'}(line 1, pos 35)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'WINDOW' expecting {<EOF>, ';'}(line 1, pos 35)\n")
doris_error_code=1105
```

### pg-window-0020-3478fa0b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lag(ten, four) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LAG(ten, four, NULL) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：lag: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "0",
    "0"
  ],
  [
    "4",
    "4",
    "0"
  ],
  [
    "",
    "1",
    "1"
  ],
  [
    "1",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')
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
doris_error_category=CAST_ERROR
doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), NULL)')
doris_error_code=1105
```

### pg-window-0021-2c2c92ba — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lag(ten, four, 0) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LAG(ten, four, 0) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：lag: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "0",
    "0"
  ],
  [
    "4",
    "4",
    "0"
  ],
  [
    "0",
    "1",
    "1"
  ],
  [
    "1",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), 0)')
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
doris_error_category=CAST_ERROR
doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(ten, cast(four as BIGINT), 0)')
doris_error_code=1105
```

### pg-window-0022-1b2ffa99 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lag(ten, four, 0.7) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LAG(ten, four, 0.7) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：lag: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "0",
    "0"
  ],
  [
    "4",
    "4",
    "0"
  ],
  [
    "0.7",
    "1",
    "1"
  ],
  [
    "1",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 13.4 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(cast(ten as DECIMALV3(11, 1)), cast(four as BIGINT), 0.7)')
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
doris_error_category=CAST_ERROR
doris_error_message=(1105, 'errCode = 2, detailMessage = The parameter 2 of LAG/LEAD must be a constant value: lag(cast(ten as DECIMALV3(11, 1)), cast(four as BIGINT), 0.7)')
doris_error_code=1105
```

### pg-window-0026-3b0a0a4f — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT lead(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LEAD(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：lead: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "8",
    "0",
    "0"
  ],
  [
    "-1.4",
    "4",
    "0"
  ],
  [
    "2",
    "1",
    "1"
  ],
  [
    "14",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 26.4 ms。
- 返回行数：10；字段：LEAD(ten * 2, 1, -1.4) OVER (PARTITION BY four ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten): decimal / DECIMAL, ten: integer / INT, four: integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0.0"
    },
    0,
    0
  ],
  [
    {
      "$decimal": "8.0"
    },
    0,
    0
  ],
  [
    {
      "$decimal": "-1.4"
    },
    4,
    0
  ],
  [
    {
      "$decimal": "2.0"
    },
    1,
    1
  ],
  [
    {
      "$decimal": "14.0"
    },
    1,
    1
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

### pg-window-0028-b7db4122 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT last_value(four) OVER (ORDER BY ten), ten, four FROM tenk1 WHERE unique2 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LAST_VALUE(four) OVER (ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten), ten, four FROM tenk1 WHERE unique2 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：last_value: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "0",
    "2"
  ],
  [
    "0",
    "0",
    "0"
  ],
  [
    "1",
    "1",
    "1"
  ],
  [
    "1",
    "1",
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.5 ms。
- 返回行数：10；字段：LAST_VALUE(four) OVER (ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten): integer / INT, ten: integer / INT, four: integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    2,
    0,
    0
  ],
  [
    2,
    0,
    0
  ],
  [
    2,
    0,
    2
  ],
  [
    1,
    1,
    3
  ],
  [
    1,
    1,
    1
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

### pg-window-0029-cebcaa74 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT last_value(ten) OVER (PARTITION BY four), ten, four FROM
	(SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s
	ORDER BY four, ten;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LAST_VALUE(ten) OVER (PARTITION BY four), ten, four FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten) AS s ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：last_value: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "4",
    "0",
    "0"
  ],
  [
    "4",
    "0",
    "0"
  ],
  [
    "4",
    "4",
    "0"
  ],
  [
    "9",
    "1",
    "1"
  ],
  [
    "9",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 25.8 ms。
- 返回行数：10；字段：LAST_VALUE(ten) OVER (PARTITION BY four): integer / INT, ten: integer / INT, four: integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0,
    0,
    0
  ],
  [
    0,
    0,
    0
  ],
  [
    0,
    4,
    0
  ],
  [
    9,
    1,
    1
  ],
  [
    9,
    1,
    1
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

### pg-window-0030-297e95fe — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT nth_value(ten, four + 1) OVER (PARTITION BY four), ten, four
	FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY four, ten)s;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT NTH_VALUE(ten, four + 1) OVER (PARTITION BY four), ten, four FROM (SELECT * FROM tenk1 WHERE unique2 < 10 ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four, CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten) AS s
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：nth_value: unknown / 原生类型未知, ten: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "0",
    "0"
  ],
  [
    "0",
    "4",
    "0"
  ],
  [
    "1",
    "1",
    "1"
  ],
  [
    "1",
    "1",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.9 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')
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
doris_error_category=CAST_ERROR
doris_error_message=(1105, 'errCode = 2, detailMessage = The offset parameter of NthValue must be a constant positive integer: (cast(four as BIGINT) + 1)#17')
doris_error_code=1105
```

### pg-window-0035-926fba7b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT avg(four) OVER (PARTITION BY four ORDER BY thousand / 100) FROM tenk1 WHERE unique2 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT AVG(four) OVER (PARTITION BY four ORDER BY CASE WHEN thousand / 100 IS NULL THEN 1 ELSE 0 END, thousand / 100) FROM tenk1 WHERE unique2 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：avg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.00000000000000000000"
  ],
  [
    "0.00000000000000000000"
  ],
  [
    "0.00000000000000000000"
  ],
  [
    "1.00000000000000000000"
  ],
  [
    "1.00000000000000000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.2 ms。
- 返回行数：10；字段：AVG(four) OVER (PARTITION BY four ORDER BY CASE WHEN thousand / 100 IS NULL THEN 1 ELSE 0 END, thousand / 100): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0
  ],
  [
    0.0
  ],
  [
    0.0
  ],
  [
    3.0
  ],
  [
    3.0
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

### pg-window-0036-1d9414c5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ten, two, sum(hundred) AS gsum, sum(sum(hundred)) OVER win AS wsum
FROM tenk1 GROUP BY ten, two WINDOW win AS (PARTITION BY two ORDER BY ten);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ten, two, SUM(hundred) AS gsum, SUM(SUM(hundred)) OVER win AS wsum FROM tenk1 GROUP BY ten, two WINDOW win AS (PARTITION BY two ORDER BY CASE WHEN ten IS NULL THEN 1 ELSE 0 END, ten)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：ten: unknown / 原生类型未知, two: unknown / 原生类型未知, gsum: unknown / 原生类型未知, wsum: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "45000",
    "45000"
  ],
  [
    "2",
    "0",
    "47000",
    "92000"
  ],
  [
    "4",
    "0",
    "49000",
    "141000"
  ],
  [
    "6",
    "0",
    "51000",
    "192000"
  ],
  [
    "8",
    "0",
    "53000",
    "245000"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'win' expecting '('(line 1, pos 62)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'win' expecting '('(line 1, pos 62)\n")
doris_error_code=1105
```

### pg-window-0038-4aba58d8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(salary) OVER w1, count(*) OVER w2
FROM empsalary WINDOW w1 AS (ORDER BY salary), w2 AS (ORDER BY salary);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(salary) OVER w1, COUNT(*) OVER w2 FROM empsalary WINDOW w1 AS (ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary), w2 AS (ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3500",
    "1"
  ],
  [
    "7400",
    "2"
  ],
  [
    "11600",
    "3"
  ],
  [
    "16100",
    "4"
  ],
  [
    "25700",
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w1' expecting '('(line 1, pos 24)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'w1' expecting '('(line 1, pos 24)\n")
doris_error_code=1105
```

### pg-window-0041-1b9507b3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(salary) OVER w, rank() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY salary DESC);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(salary) OVER w, RANK() OVER w FROM empsalary WINDOW w AS (PARTITION BY depname ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END DESC, salary DESC)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, rank: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6000",
    "1"
  ],
  [
    "16400",
    "2"
  ],
  [
    "16400",
    "2"
  ],
  [
    "20900",
    "4"
  ],
  [
    "25100",
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 24)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'w' expecting '('(line 1, pos 24)\n")
doris_error_code=1105
```

### pg-window-0046-181af42b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select x, lag(x, 1) over (order by x), lead(x, 3) over (order by x)
from (select x::numeric as x from generate_series(1,10) x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, LAG(x, 1, NULL) OVER (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x), LEAD(x, 3, NULL) OVER (ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x) FROM (SELECT CAST(x AS DECIMAL) AS x FROM GENERATE_SERIES(1, 10) AS x)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：x: unknown / 原生类型未知, lag: unknown / 原生类型未知, lead: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "",
    "4"
  ],
  [
    "2",
    "1",
    "5"
  ],
  [
    "3",
    "2",
    "6"
  ],
  [
    "4",
    "3",
    "7"
  ],
  [
    "5",
    "4",
    "8"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 217)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 217)\n")
doris_error_code=1105
```

### pg-window-0048-536e1e97 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT four, ten,
	sum(ten) over (partition by four order by ten range between unbounded preceding and current row),
	last_value(ten) over (partition by four order by ten range between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0049-f467131d — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT four, ten,
	sum(ten) over (partition by four order by ten range between unbounded preceding and unbounded following),
	last_value(ten) over (partition by four order by ten range between unbounded preceding and unbounded following)
FROM (select distinct ten, four from tenk1) ss;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0050-8b853a62 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT four, ten/4 as two,
	sum(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row),
	last_value(ten/4) over (partition by four order by ten/4 range between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0051-ce3792dc — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT four, ten/4 as two,
	sum(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row),
	last_value(ten/4) over (partition by four order by ten/4 rows between unbounded preceding and current row)
FROM (select distinct ten, four from tenk1) ss;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM

'NULLS LAST' translation not supported in window function LAST_VALUE
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0052-682b3131 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (order by four range between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function SUM
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0053-57f76f70 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (rows BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "45",
    "4",
    "0"
  ],
  [
    "41",
    "2",
    "2"
  ],
  [
    "39",
    "1",
    "1"
  ],
  [
    "38",
    "6",
    "2"
  ],
  [
    "32",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
doris_error_code=1105
```

### pg-window-0054-dd5aa38f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 2 following), unique1, four FROM tenk1 WHERE unique1 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "7",
    "4",
    "0"
  ],
  [
    "13",
    "2",
    "2"
  ],
  [
    "22",
    "1",
    "1"
  ],
  [
    "26",
    "6",
    "2"
  ],
  [
    "29",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
doris_error_code=1105
```

### pg-window-0055-461f08dc — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude no others),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0056-323a4316 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0057-e7f23b7b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0058-a6d78a71 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0059-b05800ec — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0060-fb3b911d — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0061-82375ee3 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT first_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function FIRST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0062-c3b04485 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0063-39c9997e — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0064-2e7cfd65 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT last_value(unique1) over (ORDER BY four rows between current row and 2 following exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported in window function LAST_VALUE

EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0065-af9e0271 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 2 preceding and 1 preceding),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (rows BETWEEN 2 preceding AND 1 preceding), unique1, four FROM tenk1 WHERE unique1 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "4",
    "0"
  ],
  [
    "4",
    "2",
    "2"
  ],
  [
    "6",
    "1",
    "1"
  ],
  [
    "3",
    "6",
    "2"
  ],
  [
    "7",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
doris_error_code=1105
```

### pg-window-0066-ab2af0c3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between 1 following and 3 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (rows BETWEEN 1 following AND 3 following), unique1, four FROM tenk1 WHERE unique1 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9",
    "4",
    "0"
  ],
  [
    "16",
    "2",
    "2"
  ],
  [
    "23",
    "1",
    "1"
  ],
  [
    "22",
    "6",
    "2"
  ],
  [
    "16",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
doris_error_code=1105
```

### pg-window-0067-f71d781e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (rows between unbounded preceding and 1 following),
	unique1, four
FROM tenk1 WHERE unique1 < 10;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (rows BETWEEN UNBOUNDED preceding AND 1 following), unique1, four FROM tenk1 WHERE unique1 < 10
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6",
    "4",
    "0"
  ],
  [
    "7",
    "2",
    "2"
  ],
  [
    "13",
    "1",
    "1"
  ],
  [
    "22",
    "6",
    "2"
  ],
  [
    "30",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = WindowFrame clause requires OrderBy clause')
doris_error_code=1105
```

### pg-window-0068-06f27850 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT sum(unique1) over (w range between current row and unbounded following),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(unique1) OVER (w range BETWEEN CURRENT ROW AND UNBOUNDED following), unique1, four FROM tenk1 WHERE unique1 < 10 WINDOW w AS (ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：10；字段：sum: unknown / 原生类型未知, unique1: unknown / 原生类型未知, four: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "45",
    "0",
    "0"
  ],
  [
    "45",
    "8",
    "0"
  ],
  [
    "45",
    "4",
    "0"
  ],
  [
    "33",
    "5",
    "1"
  ],
  [
    "33",
    "9",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'w' expecting {')', 'ORDER', 'PARTITION', 'RANGE', 'ROWS'}(line 1, pos 26)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'w' expecting {')', 'ORDER', 'PARTITION', 'RANGE', 'ROWS'}(line 1, pos 26)\n")
doris_error_code=1105
```

### pg-window-0069-289c97b4 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude current row),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0070-e6a99045 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude group),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0071-d0e8311e — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT sum(unique1) over (w range between unbounded preceding and current row exclude ties),
	unique1, four
FROM tenk1 WHERE unique1 < 10 WINDOW w AS (order by four);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: EXCLUDE clause is not supported in the WINDOW clause
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-window-0072-75e7d362 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT first_value(unique1) over w,
	nth_value(unique1, 2) over w AS nth_2,
	last_value(unique1) over w, unique1, four
FROM tenk1 WHERE unique1 < 10
WINDOW w AS (order by four range between current row and unbounded following);
```

#### SQLGlot 转译错误原文

```text
AttributeError: 'Identifier' object has no attribute 'sql_name'
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。
