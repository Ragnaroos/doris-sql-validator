# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:24.382017+00:00 至 2026-11-11T09:40:24.694093+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/with.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**11**；两端成功且已有证据匹配：**5**。
- 成功结果匹配占全部查询比例：**5/11 = 45.45%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**5/10 = 50.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**1**；不计入上述成功匹配分子。
- 需要分析的查询：**6**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**6**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 5 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 5 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 11 条只读查询、跳过 217 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 6 | 42–46 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 8 | 50–53 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 18 | 142–156 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 19 | 158–158 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 159–159 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 21 | 160–160 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 22 | 161–161 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 23 | 162–162 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 24 | 163–163 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 25 | 164–164 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 26 | 165–165 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 34 | 252–263 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 38 | 271–278 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 42 | 313–319 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 43 | 321–323 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 47 | 364–364 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 48 | 365–365 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 50 | 376–381 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 51 | 383–386 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 52 | 388–393 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 53 | 395–397 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 54 | 399–404 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 55 | 406–414 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 58 | 434–442 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 61 | 462–470 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 63 | 480–487 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 71 | 557–566 | 跳过非查询；类型 `create` | Failed to parse any statement following CTE. Line 8, Col: 26.   g 	union all 	select g.* 	from graph0 g, search_graph sg 	where g.f = sg.t ) search depth first by f[4m,[0m t set seq select f, t, label from search_graph;  Invalid expression / Unexpected token. Line 8, Col: 26.   g 	union all 	select g.* 	from graph0 g, search_graph sg 	where g.f = sg.t ) search depth first by f[4m,[0m t set seq select f, t, label from search_graph; |
| 74 | 572–575 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 75 | 577–583 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 79 | 614–624 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 82 | 644–651 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 98 | 802–811 | 跳过非查询；类型 `create` | Failed to parse any statement following CTE. Line 8, Col: 10.   ect * from graph g 	union all 	select g.* 	from graph g, search_graph sg 	where g.f = sg.t ) cycle f[4m,[0m t set is_cycle using path select f, t, label from search_graph;  Invalid expression / Unexpected token. Line 8, Col: 10.   ect * from graph g 	union all 	select g.* 	from graph g, search_graph sg 	where g.f = sg.t ) cycle f[4m,[0m t set is_cycle using path select f, t, label from search_graph; |
| 99 | 813–821 | 跳过非查询；类型 `create` | Failed to parse any statement following CTE. Line 8, Col: 10.   ect * from graph g 	union all 	select g.* 	from graph g, search_graph sg 	where g.f = sg.t ) cycle f[4m,[0m t set is_cycle to 'Y' default 'N' using path select f, t, label from search_graph;  Invalid expression / Unexpected token. Line 8, Col: 10.   ect * from graph g 	union all 	select g.* 	from graph g, search_graph sg 	where g.f = sg.t ) cycle f[4m,[0m t set is_cycle to 'Y' default 'N' using path select f, t, label from search_graph; |
| 110 | 875–879 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 111 | 880–880 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 118 | 906–906 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 131 | 973–973 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 132 | 974–974 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 150 | 1079–1080 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 151 | 1081–1082 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 157 | 1111–1118 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 175 | 1302–1304 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 178 | 1313–1313 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 179 | 1315–1317 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 183 | 1326–1326 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 184 | 1328–1330 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 188 | 1338–1342 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 190 | 1347–1349 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 191 | 1351–1352 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 193 | 1354–1354 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 197 | 1363–1365 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 198 | 1367–1367 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 199 | 1368–1368 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 200 | 1370–1370 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 201 | 1371–1373 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 202 | 1374–1374 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 203 | 1376–1376 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 209 | 1386–1393 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 211 | 1402–1408 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 219 | 1448–1449 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 220 | 1450–1450 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 230 | 1504–1504 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 231 | 1506–1507 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 232 | 1508–1508 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 236 | 1523–1528 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 239 | 1538–1543 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 242 | 1553–1558 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 243 | 1560–1560 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 245 | 1565–1565 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 246 | 1566–1566 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 254 | 1591–1591 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 255 | 1593–1598 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 256 | 1600–1601 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 259 | 1615–1615 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 260 | 1617–1618 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 263 | 1632–1632 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 264 | 1634–1639 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 265 | 1641–1642 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 268 | 1656–1656 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 269 | 1657–1657 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 270 | 1659–1661 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 271 | 1662–1662 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 272 | 1663–1663 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 273 | 1665–1665 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 274 | 1666–1666 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 275 | 1667–1667 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 284 | 1689–1693 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 289 | 1724–1725 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 291 | 1730–1730 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 293 | 1735–1735 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 295 | 1740–1740 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 297 | 1745–1746 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 300 | 1751–1751 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 301 | 1753–1754 | 跳过非查询；类型 `create` | Expecting (. Line 1, Col: 27.   create table foo (with baz[4m)[0m;  Required keyword: 'this' missing for <class 'sqlglot.expressions.query.CTE'>. Line 1, Col: 27.   create table foo (with baz[4m)[0m;  Failed to parse any statement following CTE. Line 1, Col: 27.   create table foo (with baz[4m)[0m;  ... and 3 more |
| 302 | 1754–1755 | 跳过非查询；类型 `create` | Expecting (. Line 1, Col: 34.   create table foo (with ordinality[4m)[0m;  Required keyword: 'this' missing for <class 'sqlglot.expressions.query.CTE'>. Line 1, Col: 34.   create table foo (with ordinality[4m)[0m;  Failed to parse any statement following CTE. Line 1, Col: 34.   create table foo (with ordinality[4m)[0m;  ... and 3 more |
| 305 | 1761–1764 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 308 | 1767–1767 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 309 | 1769–1783 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 310 | 1785–1790 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 311 | 1792–1796 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 312 | 1798–1802 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 2 | 9–15 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 7 | 48–48 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 9 | 55–55 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 10 | 57–62 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 11 | 64–69 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 12 | 71–76 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 13 | 78–80 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 14 | 82–87 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 15 | 89–96 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 98–116 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 17 | 117–140 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 35 | 265–265 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 39 | 280–289 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 40 | 291–301 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 41 | 303–311 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 44 | 325–338 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 45 | 340–352 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 46 | 354–362 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 49 | 367–374 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 62 | 472–478 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 64 | 489–495 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 547–555 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 570–570 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 585–592 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 77 | 594–602 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 78 | 604–612 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 83 | 653–659 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 84 | 661–668 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 86 | 689–695 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 826–826 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 103 | 827–827 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 829–835 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 837–841 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 843–848 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 850–855 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 857–864 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 866–873 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 113 | 888–888 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 895–895 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 117 | 904–904 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 119 | 908–913 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 915–917 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 121 | 919–920 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 922–924 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 926–927 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 929–931 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 933–935 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 937–943 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 945–951 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 128 | 953–958 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 960–964 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 133 | 976–981 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 134 | 983–987 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 135 | 989–993 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 136 | 995–998 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 1000–1002 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 138 | 1004–1005 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 139 | 1007–1009 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 140 | 1011–1013 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 141 | 1015–1017 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 142 | 1019–1023 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 143 | 1025–1029 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 1031–1038 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 1040–1047 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 146 | 1049–1055 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 147 | 1057–1063 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 148 | 1065–1070 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 149 | 1072–1077 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 153 | 1088–1088 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 154 | 1090–1094 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 156 | 1100–1109 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 158 | 1120–1122 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 159 | 1124–1137 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 160 | 1139–1149 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 161 | 1151–1157 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 162 | 1159–1165 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 163 | 1167–1172 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 164 | 1174–1186 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 165 | 1188–1216 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 166 | 1218–1242 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 168 | 1266–1266 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 170 | 1276–1276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 172 | 1286–1286 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 174 | 1300–1300 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 1311–1311 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 180 | 1319–1319 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 1324–1324 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 186 | 1335–1335 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 187 | 1336–1336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 1361–1361 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 205 | 1381–1381 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 1382–1382 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 207 | 1383–1383 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 1384–1384 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 210 | 1395–1400 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 212 | 1410–1415 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 214 | 1428–1428 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 216 | 1438–1438 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 218 | 1446–1446 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 223 | 1468–1469 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 235 | 1520–1521 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 238 | 1535–1536 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 241 | 1550–1551 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 248 | 1575–1575 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 249 | 1576–1576 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 251 | 1585–1585 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 252 | 1586–1586 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 258 | 1613–1613 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 262 | 1630–1630 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 267 | 1654–1654 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 277 | 1672–1672 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 279 | 1677–1677 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 281 | 1682–1682 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 283 | 1687–1687 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 303 | 1755–1756 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 307 | 1766–1766 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/with.out`；SHA-256（文件内容指纹）：`0175fc6ec46ef53702199d2eb35d5496177e30da91844d71584946fcd57e9d52`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 11/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 11/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 10/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 10/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 10/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/11 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-with-0001-33ab03b0` | WITH q1(x,y) AS (SELECT 1,2) SELECT * FROM q1, q1 AS q2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-with-0003-18c284af` | WITH RECURSIVE t(n) AS (     VALUES (1) UNION ALL     SELECT n+1 FROM t WHERE n < 100 ) SELECT sum(n) FROM t; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-with-0004-599c41ea` | WITH RECURSIVE t(n) AS (     SELECT (VALUES(1)) UNION ALL     SELECT n+1 FROM t WHERE n < 5 ) SELECT * FROM t; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-with-0005-37ebdc8c` | WITH RECURSIVE t(n) AS (     VALUES ('01'::varbit) UNION     SELECT n \|\| '10'::varbit FROM t WHERE n < '100'::varbit ) SELECT n FROM t; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：类型转换失败 | 两端均报错，但错误类别不同 |
| `pg-with-0027-08d06e3c` | WITH RECURSIVE subdepartment AS ( 	-- non recursive term 	SELECT name as root_name, * FROM department WHERE name = 'A'  	UNION ALL  	-- recursive term 	SELECT sd.root_name, d.* FROM department AS d, subdepartment AS sd 		WHERE d.parent_department = sd.id ) SELECT * FROM subdepartment ORDER BY name; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-with-0028-95f86b76` | WITH RECURSIVE subdepartment(level, id, parent_department, name) AS ( 	-- non recursive term 	SELECT 1, * FROM department WHERE name = 'A'  	UNION ALL  	-- recursive term 	SELECT sd.level + 1, d.* FROM department AS d, subdepartment AS sd 		WHERE d.parent_department = sd.id ) SELECT * FROM subdepartment ORDER BY name; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-with-0029-22d7351d` | WITH RECURSIVE subdepartment(level, id, parent_department, name) AS ( 	-- non recursive term 	SELECT 1, * FROM department WHERE name = 'A'  	UNION ALL  	-- recursive term 	SELECT sd.level + 1, d.* FROM department AS d, subdepartment AS sd 		WHERE d.parent_department = sd.id ) SELECT * FROM subdepartment WHERE level >= 2 ORDER BY name; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-with-0030-a5b15ec4` | WITH RECURSIVE subdepartment AS ( 	-- note lack of recursive UNION structure 	SELECT * FROM department WHERE name = 'A' ) SELECT * FROM subdepartment ORDER BY name; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-with-0031-3ad31abd` | WITH RECURSIVE subdepartment AS ( 	-- select all columns to prevent projection 	SELECT id, parent_department, name FROM department WHERE name = 'A'  	UNION  	-- joins do projection 	SELECT d.id, d.parent_department, d.name FROM department AS d 	INNER JOIN subdepartment AS sd ON d.parent_department = sd.id ) SELECT * FROM subdepartment ORDER BY name; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-with-0032-b27e3270` | SELECT count(*) FROM (     WITH RECURSIVE t(n) AS (         SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 500     )     SELECT * FROM t) AS t WHERE n < (         SELECT count(*) FROM (             WITH RECURSIVE t(n) AS (                    SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 100                 )             SELECT * FROM t WHERE n < 50000          ) AS t WHERE n < 100); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-with-0033-8592b31e` | WITH q1(x,y) AS (     SELECT hundred, sum(ten) FROM tenk1 GROUP BY hundred   ) SELECT count(*) FROM q1 WHERE y > (SELECT sum(y)/100 FROM q1 qsub); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |

## 4. 不匹配、执行失败及负向错误详情

### pg-with-0003-18c284af — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH RECURSIVE t(n) AS (
    VALUES (1)
UNION ALL
    SELECT n+1 FROM t WHERE n < 100
)
SELECT sum(n) FROM t;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT 1) AS _values UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT SUM(n) FROM t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5050"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.2 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
doris_error_message=(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
doris_error_code=1105
```

### pg-with-0004-599c41ea — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
WITH RECURSIVE t(n) AS (
    SELECT (VALUES(1))
UNION ALL
    SELECT n+1 FROM t WHERE n < 5
)
SELECT * FROM t;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH RECURSIVE t(n) AS (SELECT (VALUES (1)) UNION ALL SELECT n + 1 FROM t WHERE n < 5) SELECT * FROM t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：n: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    "2"
  ],
  [
    "3"
  ],
  [
    "4"
  ],
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.2 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
doris_error_message=(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
doris_error_code=1105
```

### pg-with-0005-37ebdc8c — 两端均报错，但错误类别不同

#### 源 SQL

```sql
WITH RECURSIVE t(n) AS (
    VALUES ('01'::varbit)
UNION
    SELECT n || '10'::varbit FROM t WHERE n < '100'::varbit
)
SELECT n FROM t;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT CAST('01' AS varbit)) AS _values UNION SELECT CONCAT(n, CAST('10' AS varbit)) FROM t WHERE n < CAST('100' AS varbit)) SELECT n FROM t
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`could not implement recursive UNION`。

错误原文：

```text
could not implement recursive UNION
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.2 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT CAST('01' AS varbit'(line 1, pos 59)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=could not implement recursive UNION
source_error_code=could not implement recursive UNION
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'WITH RECURSIVE t(n) AS (SELECT * FROM (SELECT CAST('01' AS varbit'(line 1, pos 59)\n")
doris_error_code=1105
```

### pg-with-0028-95f86b76 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
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
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH RECURSIVE subdepartment(`level`, id, parent_department, `name`) AS (/* non recursive term */ SELECT 1, * FROM department WHERE `name` = 'A' UNION ALL /* recursive term */ SELECT sd.`level` + 1, d.* FROM department AS d, subdepartment AS sd WHERE d.parent_department = sd.id) SELECT * FROM subdepartment ORDER BY CASE WHEN `name` IS NULL THEN 1 ELSE 0 END, `name`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：level: unknown / 原生类型未知, id: unknown / 原生类型未知, parent_department: unknown / 原生类型未知, name: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "1",
    "0",
    "A"
  ],
  [
    "2",
    "2",
    "1",
    "B"
  ],
  [
    "3",
    "3",
    "2",
    "C"
  ],
  [
    "3",
    "4",
    "2",
    "D"
  ],
  [
    "4",
    "6",
    "4",
    "F"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.6 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
doris_error_message=(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
doris_error_code=1105
```

### pg-with-0029-22d7351d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
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
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
WITH RECURSIVE subdepartment(`level`, id, parent_department, `name`) AS (/* non recursive term */ SELECT 1, * FROM department WHERE `name` = 'A' UNION ALL /* recursive term */ SELECT sd.`level` + 1, d.* FROM department AS d, subdepartment AS sd WHERE d.parent_department = sd.id) SELECT * FROM subdepartment WHERE `level` >= 2 ORDER BY CASE WHEN `name` IS NULL THEN 1 ELSE 0 END, `name`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：level: unknown / 原生类型未知, id: unknown / 原生类型未知, parent_department: unknown / 原生类型未知, name: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2",
    "2",
    "1",
    "B"
  ],
  [
    "3",
    "3",
    "2",
    "C"
  ],
  [
    "3",
    "4",
    "2",
    "D"
  ],
  [
    "4",
    "6",
    "4",
    "F"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.1 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
doris_error_message=(1105, "errCode = 2, detailMessage = subdepartment recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
doris_error_code=1105
```

### pg-with-0032-b27e3270 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
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
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT COUNT(*) FROM (WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 500) SELECT * FROM t) AS t WHERE n < (SELECT COUNT(*) FROM (WITH RECURSIVE t(n) AS (SELECT 1 UNION ALL SELECT n + 1 FROM t WHERE n < 100) SELECT * FROM t WHERE n < 50000) AS t WHERE n < 100)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "98"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.2 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
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
doris_error_message=(1105, "errCode = 2, detailMessage = t recursive child's 1 column's datatype in select list SMALLINT is different from anchor child's output datatype TINYINT, please add cast manually to get expect datatype")
doris_error_code=1105
```
