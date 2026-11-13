# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:04.734410+00:00 至 2026-11-11T09:40:06.027295+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/aggregates.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**55**；两端成功且已有证据匹配：**15**。
- 成功结果匹配占全部查询比例：**15/55 = 27.27%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**15/54 = 27.78%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**40**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**1**；源参考结果不可用：**0**；Doris 执行失败：**6**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 6 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 15 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 33 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 1 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 55 条只读查询、跳过 493 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–9 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 2 | 11–15 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 17–18 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Command |
| 102 | 184–185 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 103 | 186–186 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 116 | 206–206 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 133 | 250–257 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 135 | 264–267 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 139 | 282–292 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 141 | 301–301 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 145 | 363–367 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 147 | 375–375 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 151 | 408–415 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 153 | 417–418 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 155 | 420–421 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 157 | 423–424 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 160 | 432–432 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 161 | 433–434 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 164 | 438–440 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 166 | 442–443 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 168 | 446–449 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 170 | 453–455 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 172 | 457–458 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 174 | 460–461 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 176 | 463–464 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 178 | 466–467 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 180 | 470–473 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 182 | 476–477 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 184 | 480–481 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 185 | 482–482 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 186 | 483–483 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 187 | 484–484 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 188 | 485–485 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 189 | 486–486 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 190 | 487–487 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 191 | 488–488 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 192 | 490–490 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 193 | 491–491 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 194 | 492–492 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 195 | 493–493 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 196 | 495–496 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 198 | 499–501 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 200 | 504–504 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 202 | 508–508 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 203 | 509–511 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 209 | 523–527 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 210 | 528–528 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 211 | 529–529 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 212 | 531–532 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 213 | 534–535 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 214 | 537–540 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 215 | 542–545 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 216 | 547–548 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 217 | 550–550 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 218 | 552–553 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 219 | 555–556 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 220 | 558–564 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 221 | 565–565 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 222 | 566–566 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 223 | 568–569 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 224 | 571–571 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 225 | 573–575 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 226 | 577–578 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 227 | 579–579 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 228 | 581–584 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 229 | 586–588 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 230 | 590–591 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 231 | 592–592 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 232 | 593–593 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 233 | 595–598 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 234 | 599–599 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 235 | 600–600 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 236 | 601–601 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 237 | 603–603 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 238 | 604–604 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 239 | 605–605 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 240 | 606–606 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 241 | 608–612 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 242 | 614–618 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 243 | 619–619 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 244 | 620–623 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 245 | 624–625 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 247 | 627–627 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 248 | 629–631 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 249 | 632–635 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 250 | 637–639 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 252 | 642–644 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 254 | 647–649 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 256 | 652–652 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 257 | 653–653 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 258 | 655–659 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 259 | 660–660 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 266 | 678–680 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 268 | 683–683 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 269 | 684–684 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 270 | 686–693 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 271 | 695–701 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 272 | 703–708 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 273 | 710–717 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 274 | 719–727 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 275 | 729–738 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 277 | 744–745 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 278 | 746–747 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 279 | 748–748 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 280 | 750–756 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 281 | 758–761 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 282 | 763–767 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 302 | 832–833 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 305 | 842–842 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 307 | 853–857 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 310 | 862–865 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 313 | 870–873 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 316 | 878–880 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 319 | 885–887 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 322 | 892–894 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 38.   create or replace view agg_view1 as   select aggfns(a,b,c order by c [4musing[0m ~<~)     from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c); |
| 325 | 899–902 | 跳过非查询；类型 `create` | Expecting ). Line 2, Col: 49.   create or replace view agg_view1 as   select aggfns(distinct a,b,c order by a,c [4musing[0m ~<~,b)     from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c),          gener |
| 328 | 907–907 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 341 | 930–933 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 343 | 937–937 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 345 | 941–941 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 351 | 950–950 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 352 | 951–951 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 355 | 956–956 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 356 | 958–959 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 357 | 960–962 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 358 | 964–964 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 359 | 965–965 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 360 | 966–966 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 361 | 967–967 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 362 | 968–968 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 363 | 969–969 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 364 | 971–997 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 366 | 1002–1003 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 367 | 1005–1006 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 369 | 1009–1010 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 370 | 1011–1012 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 372 | 1015–1016 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 373 | 1017–1017 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 374 | 1018–1018 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 375 | 1019–1019 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 376 | 1020–1020 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 377 | 1021–1021 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 378 | 1023–1023 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 379 | 1024–1024 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 429 | 1161–1168 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 432 | 1172–1172 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 440 | 1187–1187 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 441 | 1189–1191 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 442 | 1193–1195 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 443 | 1197–1199 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 444 | 1201–1203 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 445 | 1205–1207 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 446 | 1209–1211 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 447 | 1213–1216 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 450 | 1223–1223 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 451 | 1225–1245 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 452 | 1247–1256 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 453 | 1258–1267 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 454 | 1269–1274 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 455 | 1276–1281 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 465 | 1318–1325 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 466 | 1327–1333 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 467 | 1335–1341 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 472 | 1355–1373 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 473 | 1375–1384 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 474 | 1386–1390 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 475 | 1392–1397 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 479 | 1410–1419 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 480 | 1421–1427 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 483 | 1433–1439 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 484 | 1440–1440 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 486 | 1443–1443 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 487 | 1444–1444 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 488 | 1446–1448 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 489 | 1450–1452 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 490 | 1454–1457 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 491 | 1459–1460 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 492 | 1461–1461 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 493 | 1462–1465 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 494 | 1466–1466 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 495 | 1467–1467 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 496 | 1469–1471 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 497 | 1473–1475 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 498 | 1477–1479 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 499 | 1480–1482 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 500 | 1484–1492 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 502 | 1494–1494 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 503 | 1495–1495 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 504 | 1497–1500 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 506 | 1505–1512 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 507 | 1513–1517 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 508 | 1519–1519 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 509 | 1520–1520 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 510 | 1521–1521 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 511 | 1523–1525 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 512 | 1526–1526 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 513 | 1527–1527 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 515 | 1530–1532 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 516 | 1534–1534 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 517 | 1536–1536 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 518 | 1538–1538 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 519 | 1539–1539 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 521 | 1545–1555 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 522 | 1557–1564 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 523 | 1566–1567 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 524 | 1568–1568 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 525 | 1569–1569 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 526 | 1571–1571 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 530 | 1579–1584 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 531 | 1586–1595 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 532 | 1597–1601 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 533 | 1603–1609 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 537 | 1618–1618 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 538 | 1619–1619 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 539 | 1620–1620 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 540 | 1621–1621 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 541 | 1622–1622 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 542 | 1623–1623 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 543 | 1625–1633 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 545 | 1641–1648 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 553 | 1676–1680 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 554 | 1681–1681 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 556 | 1688–1688 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 557 | 1689–1689 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 558 | 1691–1696 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 559 | 1698–1699 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 561 | 1702–1703 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 563 | 1706–1708 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 564 | 1710–1710 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 565 | 1712–1714 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 566 | 1716–1718 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 567 | 1720–1729 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 568 | 1731–1731 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 569 | 1733–1735 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 570 | 1737–1739 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 571 | 1741–1743 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 572 | 1744–1744 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 573 | 1746–1746 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 574 | 1748–1750 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 575 | 1752–1754 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 576 | 1756–1765 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 577 | 1767–1767 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 578 | 1769–1771 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 579 | 1773–1775 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 580 | 1777–1777 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 581 | 1778–1778 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 586 | 1798–1798 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 587 | 1799–1799 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 588 | 1800–1800 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 589 | 1801–1801 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 590 | 1802–1802 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 591 | 1803–1803 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 592 | 1804–1804 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 593 | 1805–1805 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 8 | 28–28 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 12 | 37–37 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 43–43 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 48–48 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 51 | 87–88 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 52 | 89–89 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 53 | 90–90 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 54 | 91–91 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 55 | 92–92 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 56 | 93–93 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 57 | 94–94 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 58 | 95–95 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 72 | 124–125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 127–128 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 74 | 129–129 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 75 | 130–130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 131–131 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 77 | 132–132 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 78 | 133–133 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 79 | 134–134 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 80 | 135–135 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 136–136 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 82 | 138–139 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 83 | 140–140 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 84 | 141–141 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 85 | 143–146 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 86 | 147–148 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 87 | 149–150 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 88 | 152–154 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 89 | 155–156 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 90 | 157–158 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 91 | 159–160 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 92 | 161–162 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 93 | 164–167 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 94 | 168–170 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 95 | 171–173 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 174–174 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 175–175 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 177–179 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 180–180 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 181–181 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 182–182 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 187–188 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 189–190 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 191–191 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 192–192 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 193–194 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 195–196 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 197–197 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 111 | 198–198 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 199–199 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 113 | 200–201 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 114 | 202–203 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 204–205 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 117 | 208–209 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 118 | 210–210 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 119 | 212–213 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 215–216 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 121 | 218–219 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 220–220 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 221–221 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 222–222 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 223–223 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 224–224 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 226–227 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 128 | 228–228 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 229–229 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 130 | 231–236 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 238–242 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 132 | 244–248 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 134 | 258–262 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 136 | 268–270 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 272–276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 138 | 278–280 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 140 | 294–299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 143 | 330–347 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 349–361 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 146 | 369–373 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 149 | 390–397 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 150 | 399–406 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 152 | 416–416 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 154 | 419–419 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 156 | 422–422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 158 | 425–425 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 162 | 435–435 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 165 | 441–441 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 167 | 444–444 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 169 | 450–451 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 171 | 456–456 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 173 | 459–459 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 462–462 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 465–465 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 179 | 468–468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 181 | 474–474 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 183 | 478–478 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 197 | 497–497 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 199 | 502–502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 204 | 512–513 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 516–517 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 207 | 518–518 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 519–521 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 246 | 626–626 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 255 | 650–650 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 260 | 662–662 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 261 | 663–663 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 262 | 664–664 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 263 | 665–666 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 264 | 668–671 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 265 | 673–676 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 276 | 740–742 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 283 | 769–774 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 284 | 775–776 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 285 | 777–778 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 286 | 779–780 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 287 | 782–783 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 288 | 784–785 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 289 | 786–787 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 290 | 788–789 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 291 | 791–794 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 292 | 795–796 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 293 | 798–800 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 294 | 801–803 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 295 | 805–807 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 296 | 808–810 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 299 | 820–822 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 306 | 844–851 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 308 | 859–859 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 311 | 867–867 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 314 | 875–875 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 317 | 882–882 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 320 | 889–889 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 323 | 896–896 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 326 | 904–904 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 329 | 909–912 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 330 | 913–914 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 331 | 915–916 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 332 | 917–918 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 333 | 920–921 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 334 | 922–922 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 335 | 923–923 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 336 | 924–924 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 337 | 926–927 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 338 | 927–928 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 339 | 928–929 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 340 | 929–930 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 342 | 935–935 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 344 | 939–939 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 346 | 943–943 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 347 | 944–944 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 348 | 945–945 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 349 | 947–947 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 350 | 948–948 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 353 | 953–953 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 354 | 954–954 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 365 | 999–1000 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 368 | 1007–1007 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 371 | 1013–1013 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 380 | 1026–1028 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 381 | 1030–1030 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 382 | 1032–1033 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 383 | 1035–1037 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 384 | 1039–1040 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 385 | 1042–1042 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 386 | 1044–1047 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 387 | 1047–1050 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 388 | 1050–1053 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 389 | 1053–1057 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 390 | 1057–1061 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 392 | 1068–1069 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 393 | 1070–1070 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 394 | 1072–1073 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 395 | 1074–1074 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 396 | 1075–1075 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 397 | 1076–1076 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 398 | 1079–1084 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 399 | 1086–1089 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 401 | 1096–1099 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 402 | 1101–1101 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 403 | 1102–1102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 404 | 1103–1103 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 405 | 1104–1104 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 406 | 1105–1106 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 407 | 1107–1108 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 408 | 1109–1110 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 409 | 1111–1112 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 410 | 1114–1115 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 411 | 1116–1117 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 412 | 1118–1119 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 413 | 1120–1121 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 414 | 1123–1123 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 415 | 1125–1126 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 416 | 1128–1130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 417 | 1132–1134 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 418 | 1135–1135 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 419 | 1137–1138 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 420 | 1140–1143 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 421 | 1145–1146 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 422 | 1148–1149 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 423 | 1150–1150 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 424 | 1151–1151 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 425 | 1152–1153 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 426 | 1154–1155 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 427 | 1156–1156 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 428 | 1158–1159 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 431 | 1171–1171 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 433 | 1174–1175 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 434 | 1176–1176 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 435 | 1178–1178 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 436 | 1179–1179 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 437 | 1180–1180 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 438 | 1181–1181 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 456 | 1283–1284 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 457 | 1286–1287 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 458 | 1289–1290 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 459 | 1292–1293 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 460 | 1295–1296 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 461 | 1298–1299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 462 | 1301–1305 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 463 | 1307–1310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 464 | 1312–1316 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 468 | 1343–1344 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 469 | 1346–1347 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 476 | 1399–1400 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 481 | 1429–1429 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 505 | 1501–1503 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 527 | 1572–1572 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 534 | 1611–1611 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 544 | 1635–1639 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 546 | 1650–1654 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 548 | 1658–1659 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 549 | 1662–1665 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 550 | 1666–1666 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 551 | 1668–1671 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 552 | 1672–1674 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 555 | 1683–1686 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 582 | 1780–1784 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 583 | 1786–1788 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 584 | 1790–1792 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 585 | 1794–1796 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/aggregates.out`；SHA-256（文件内容指纹）：`843b8b36b24d067eb2bdfd7316a38b16237efdfc9800146412843c0fd10e8708`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-aggregates-0005-11b43275` | SELECT avg(four) AS avg_1 FROM onek; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0006-86de303b` | SELECT avg(a) AS avg_32 FROM aggtest WHERE a < 100; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0007-36217afd` | SELECT any_value(v) FROM (VALUES (1), (2), (3)) AS v (v); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0009-c20340c6` | SELECT any_value(v) FROM (VALUES (NULL), (1), (2)) AS v (v); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0010-12bf388c` | SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-aggregates-0011-c9923b58` | SELECT avg(b)::numeric(10,3) AS avg_107_943 FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0013-004fee08` | SELECT sum(four) AS sum_1500 FROM onek; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0014-f595a22a` | SELECT sum(a) AS sum_198 FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0015-4a78a728` | SELECT sum(b) AS avg_431_773 FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0017-d957972d` | SELECT max(four) AS max_3 FROM onek; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0018-d740b4f5` | SELECT max(a) AS max_100 FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0019-9598b30b` | SELECT max(aggtest.b) AS max_324_78 FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0021-7678f6ba` | SELECT stddev_pop(b) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0022-d52a63cf` | SELECT stddev_samp(b) FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0023-251c8665` | SELECT var_pop(b) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0024-495ab595` | SELECT var_samp(b) FROM aggtest; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0025-d78c66c7` | SELECT stddev_pop(b::numeric) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0026-54749b3e` | SELECT stddev_samp(b::numeric) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0027-6d80b91b` | SELECT var_pop(b::numeric) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0028-7de34821` | SELECT var_samp(b::numeric) FROM aggtest; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0029-d0645c62` | SELECT var_pop(1.0::float8), var_samp(2.0::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0030-549b8efa` | SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0031-db84a9eb` | SELECT var_pop('inf'::float8), var_samp('inf'::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0032-73c05241` | SELECT stddev_pop('inf'::float8), stddev_samp('inf'::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0033-027391b8` | SELECT var_pop('nan'::float8), var_samp('nan'::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0034-b0e2e780` | SELECT stddev_pop('nan'::float8), stddev_samp('nan'::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0035-daf9210d` | SELECT var_pop(1.0::float4), var_samp(2.0::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0036-7e813a8e` | SELECT stddev_pop(3.0::float4), stddev_samp(4.0::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0037-9e86a590` | SELECT var_pop('inf'::float4), var_samp('inf'::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0038-474e8581` | SELECT stddev_pop('inf'::float4), stddev_samp('inf'::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0039-4005fc5e` | SELECT var_pop('nan'::float4), var_samp('nan'::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0040-a02080ac` | SELECT stddev_pop('nan'::float4), stddev_samp('nan'::float4); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0041-6590092b` | SELECT var_pop(1.0::numeric), var_samp(2.0::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0042-48fe21bd` | SELECT stddev_pop(3.0::numeric), stddev_samp(4.0::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0043-dbb54239` | SELECT var_pop('inf'::numeric), var_samp('inf'::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0044-507b44d8` | SELECT stddev_pop('inf'::numeric), stddev_samp('inf'::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0045-195c7ba3` | SELECT var_pop('nan'::numeric), var_samp('nan'::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0046-fc983fe4` | SELECT stddev_pop('nan'::numeric), stddev_samp('nan'::numeric); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0047-027f1f0b` | SELECT max(row(a,b)) FROM aggtest; | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0048-a1525a74` | SELECT max(row(b,a)) FROM aggtest; | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0049-df94fed3` | SELECT min(row(a,b)) FROM aggtest; | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0050-5a9fb934` | SELECT min(row(b,a)) FROM aggtest; | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0059-6e8dac37` | select sum('NaN'::numeric) from generate_series(1,3); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0060-10dc4c9b` | select avg('NaN'::numeric) from generate_series(1,3); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-aggregates-0061-70f83399` | SELECT sum(x::float8), avg(x::float8), var_pop(x::float8) FROM (VALUES ('1'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0062-87607e80` | SELECT sum(x::float8), avg(x::float8), var_pop(x::float8) FROM (VALUES ('infinity'), ('1')) v(x); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0063-b5e1533c` | SELECT sum(x::float8), avg(x::float8), var_pop(x::float8) FROM (VALUES ('infinity'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0064-c5f11c18` | SELECT sum(x::float8), avg(x::float8), var_pop(x::float8) FROM (VALUES ('-infinity'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0065-de46c84d` | SELECT sum(x::float8), avg(x::float8), var_pop(x::float8) FROM (VALUES ('-infinity'), ('-infinity')) v(x); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-aggregates-0066-82b28760` | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('1'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0067-d68e127a` | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('infinity'), ('1')) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0068-a8a0f897` | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('infinity'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0069-dbe867f2` | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('-infinity'), ('infinity')) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0070-59676ab5` | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('-infinity'), ('-infinity')) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-aggregates-0071-3dc674b8` | SELECT avg(x::float8), var_pop(x::float8) FROM (VALUES (100000003), (100000004), (100000006), (100000007)) v(x); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-aggregates-0005-11b43275 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT avg(four) AS avg_1 FROM onek;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT AVG(four) AS avg_1 FROM onek
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：avg_1: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.5000000000000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 89.9 ms。
- 返回行数：1；字段：avg_1: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.5
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

### pg-aggregates-0006-86de303b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT avg(a) AS avg_32 FROM aggtest WHERE a < 100;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT AVG(a) AS avg_32 FROM aggtest WHERE a < 100
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：avg_32: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "32.6666666666666667"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 37.0 ms。
- 返回行数：1；字段：avg_32: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    32.66666666666666
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

### pg-aggregates-0010-12bf388c — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-aggregates-0015-4a78a728 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(b) AS avg_431_773 FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(b) AS avg_431_773 FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：avg_431_773: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "431.773"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 38.7 ms。
- 返回行数：1；字段：avg_431_773: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    431.7726090922952
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

### pg-aggregates-0021-7678f6ba — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop(b) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(b) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "131.10703231895"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.9 ms。
- 返回行数：1；字段：STDDEV_POP(b): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    131.1070323189505
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

### pg-aggregates-0023-251c8665 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop(b) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(b) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "17189.0539234823"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 22.1 ms。
- 返回行数：1；字段：VAR_POP(b): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    17189.05392348233
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

### pg-aggregates-0025-d78c66c7 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop(b::numeric) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST(b AS DECIMAL)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "131.107032862199"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 30.4 ms。
- 返回行数：1；字段：STDDEV_POP(CAST(b AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    131.107032318818
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

### pg-aggregates-0026-54749b3e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_samp(b::numeric) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_SAMP(CAST(b AS DECIMAL)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "151.389361431288"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 24.8 ms。
- 返回行数：1；字段：STDDEV_SAMP(CAST(b AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    151.3893608038451
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

### pg-aggregates-0027-6d80b91b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop(b::numeric) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST(b AS DECIMAL)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "17189.054065929769"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 37.6 ms。
- 返回行数：1；字段：VAR_POP(CAST(b AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    17189.05392344758
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

### pg-aggregates-0028-7de34821 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_samp(b::numeric) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_SAMP(CAST(b AS DECIMAL)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "22918.738754573025"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.4 ms。
- 返回行数：1；字段：VAR_SAMP(CAST(b AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    22918.73856459678
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

### pg-aggregates-0029-d0645c62 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop(1.0::float8), var_samp(2.0::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST(1.0 AS DOUBLE)), VAR_SAMP(CAST(2.0 AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.8 ms。
- 返回行数：1；字段：VAR_POP(CAST(1.0 AS DOUBLE)): float / DOUBLE, VAR_SAMP(CAST(2.0 AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0030-549b8efa — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), STDDEV_SAMP(CAST(4.0 AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.0 ms。
- 返回行数：1；字段：STDDEV_POP(CAST(3.0 AS DOUBLE)): float / DOUBLE, STDDEV_SAMP(CAST(4.0 AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0031-db84a9eb — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('inf'::float8), var_samp('inf'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('inf' AS DOUBLE)), VAR_SAMP(CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.5 ms。
- 返回行数：1；字段：VAR_POP(CAST('inf' AS DOUBLE)): float / DOUBLE, VAR_SAMP(CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0032-73c05241 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('inf'::float8), stddev_samp('inf'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('inf' AS DOUBLE)), STDDEV_SAMP(CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 22.2 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('inf' AS DOUBLE)): float / DOUBLE, STDDEV_SAMP(CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0033-027391b8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('nan'::float8), var_samp('nan'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('nan' AS DOUBLE)), VAR_SAMP(CAST('nan' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.2 ms。
- 返回行数：1；字段：VAR_POP(CAST('nan' AS DOUBLE)): float / DOUBLE, VAR_SAMP(CAST('nan' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0034-b0e2e780 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('nan'::float8), stddev_samp('nan'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('nan' AS DOUBLE)), STDDEV_SAMP(CAST('nan' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 17.4 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('nan' AS DOUBLE)): float / DOUBLE, STDDEV_SAMP(CAST('nan' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0035-daf9210d — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop(1.0::float4), var_samp(2.0::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST(1.0 AS FLOAT)), VAR_SAMP(CAST(2.0 AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.8 ms。
- 返回行数：1；字段：VAR_POP(CAST(1.0 AS FLOAT)): float / DOUBLE, VAR_SAMP(CAST(2.0 AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0036-7e813a8e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop(3.0::float4), stddev_samp(4.0::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST(3.0 AS FLOAT)), STDDEV_SAMP(CAST(4.0 AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.5 ms。
- 返回行数：1；字段：STDDEV_POP(CAST(3.0 AS FLOAT)): float / DOUBLE, STDDEV_SAMP(CAST(4.0 AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0037-9e86a590 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('inf'::float4), var_samp('inf'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('inf' AS FLOAT)), VAR_SAMP(CAST('inf' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.3 ms。
- 返回行数：1；字段：VAR_POP(CAST('inf' AS FLOAT)): float / DOUBLE, VAR_SAMP(CAST('inf' AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0038-474e8581 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('inf'::float4), stddev_samp('inf'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('inf' AS FLOAT)), STDDEV_SAMP(CAST('inf' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.7 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('inf' AS FLOAT)): float / DOUBLE, STDDEV_SAMP(CAST('inf' AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0039-4005fc5e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('nan'::float4), var_samp('nan'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('nan' AS FLOAT)), VAR_SAMP(CAST('nan' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.9 ms。
- 返回行数：1；字段：VAR_POP(CAST('nan' AS FLOAT)): float / DOUBLE, VAR_SAMP(CAST('nan' AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0040-a02080ac — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('nan'::float4), stddev_samp('nan'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('nan' AS FLOAT)), STDDEV_SAMP(CAST('nan' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.4 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('nan' AS FLOAT)): float / DOUBLE, STDDEV_SAMP(CAST('nan' AS FLOAT)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0041-6590092b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop(1.0::numeric), var_samp(2.0::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST(1.0 AS DECIMAL)), VAR_SAMP(CAST(2.0 AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.6 ms。
- 返回行数：1；字段：VAR_POP(CAST(1.0 AS DECIMAL)): float / DOUBLE, VAR_SAMP(CAST(2.0 AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0042-48fe21bd — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop(3.0::numeric), stddev_samp(4.0::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST(3.0 AS DECIMAL)), STDDEV_SAMP(CAST(4.0 AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.8 ms。
- 返回行数：1；字段：STDDEV_POP(CAST(3.0 AS DECIMAL)): float / DOUBLE, STDDEV_SAMP(CAST(4.0 AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0,
    0.0
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

### pg-aggregates-0043-dbb54239 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('inf'::numeric), var_samp('inf'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('inf' AS DECIMAL)), VAR_SAMP(CAST('inf' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.8 ms。
- 返回行数：1；字段：VAR_POP(CAST('inf' AS DECIMAL)): float / DOUBLE, VAR_SAMP(CAST('inf' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null
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

### pg-aggregates-0044-507b44d8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('inf'::numeric), stddev_samp('inf'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('inf' AS DECIMAL)), STDDEV_SAMP(CAST('inf' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.1 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('inf' AS DECIMAL)): float / DOUBLE, STDDEV_SAMP(CAST('inf' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null
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

### pg-aggregates-0045-195c7ba3 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT var_pop('nan'::numeric), var_samp('nan'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT VAR_POP(CAST('nan' AS DECIMAL)), VAR_SAMP(CAST('nan' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：var_pop: unknown / 原生类型未知, var_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.7 ms。
- 返回行数：1；字段：VAR_POP(CAST('nan' AS DECIMAL)): float / DOUBLE, VAR_SAMP(CAST('nan' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null
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

### pg-aggregates-0046-fc983fe4 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT stddev_pop('nan'::numeric), stddev_samp('nan'::numeric);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT STDDEV_POP(CAST('nan' AS DECIMAL)), STDDEV_SAMP(CAST('nan' AS DECIMAL))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：stddev_pop: unknown / 原生类型未知, stddev_samp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.8 ms。
- 返回行数：1；字段：STDDEV_POP(CAST('nan' AS DECIMAL)): float / DOUBLE, STDDEV_SAMP(CAST('nan' AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null
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

### pg-aggregates-0047-027f1f0b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT max(row(a,b)) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT MAX(ROW(a, b)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(100,99.097)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 13.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
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
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
doris_error_code=1105
```

### pg-aggregates-0048-a1525a74 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT max(row(b,a)) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT MAX(ROW(b, a)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(324.78,42)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
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
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
doris_error_code=1105
```

### pg-aggregates-0049-df94fed3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT min(row(a,b)) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT MIN(ROW(a, b)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：min: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(0,0.09561)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 10.5 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
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
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
doris_error_code=1105
```

### pg-aggregates-0050-5a9fb934 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT min(row(b,a)) FROM aggtest;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT MIN(ROW(b, a)) FROM aggtest
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：min: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(0.09561,0)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
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
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 11)\n")
doris_error_code=1105
```

### pg-aggregates-0059-6e8dac37 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select sum('NaN'::numeric) from generate_series(1,3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST('NaN' AS DECIMAL)) FROM GENERATE_SERIES(1, 3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 57)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 57)\n")
doris_error_code=1105
```

### pg-aggregates-0060-10dc4c9b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select avg('NaN'::numeric) from generate_series(1,3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT AVG(CAST('NaN' AS DECIMAL)) FROM GENERATE_SERIES(1, 3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：avg: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 57)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 57)\n")
doris_error_code=1105
```

### pg-aggregates-0066-82b28760 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric)
FROM (VALUES ('1'), ('infinity')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST(x AS DECIMAL)), AVG(CAST(x AS DECIMAL)), VAR_POP(CAST(x AS DECIMAL)) FROM (SELECT '1' AS x UNION ALL SELECT 'infinity') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知, avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "Infinity",
    "Infinity",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.1 ms。
- 返回行数：1；字段：SUM(CAST(x AS DECIMAL)): decimal / DECIMAL, AVG(CAST(x AS DECIMAL)): decimal / DECIMAL, VAR_POP(CAST(x AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "1.000000000"
    },
    {
      "$decimal": "1.000000000"
    },
    0.0
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

### pg-aggregates-0067-d68e127a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric)
FROM (VALUES ('infinity'), ('1')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST(x AS DECIMAL)), AVG(CAST(x AS DECIMAL)), VAR_POP(CAST(x AS DECIMAL)) FROM (SELECT 'infinity' AS x UNION ALL SELECT '1') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知, avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "Infinity",
    "Infinity",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.3 ms。
- 返回行数：1；字段：SUM(CAST(x AS DECIMAL)): decimal / DECIMAL, AVG(CAST(x AS DECIMAL)): decimal / DECIMAL, VAR_POP(CAST(x AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "1.000000000"
    },
    {
      "$decimal": "1.000000000"
    },
    0.0
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

### pg-aggregates-0068-a8a0f897 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric)
FROM (VALUES ('infinity'), ('infinity')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST(x AS DECIMAL)), AVG(CAST(x AS DECIMAL)), VAR_POP(CAST(x AS DECIMAL)) FROM (SELECT 'infinity' AS x UNION ALL SELECT 'infinity') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知, avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "Infinity",
    "Infinity",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.9 ms。
- 返回行数：1；字段：SUM(CAST(x AS DECIMAL)): decimal / DECIMAL, AVG(CAST(x AS DECIMAL)): decimal / DECIMAL, VAR_POP(CAST(x AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null,
    null
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

### pg-aggregates-0069-dbe867f2 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric)
FROM (VALUES ('-infinity'), ('infinity')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST(x AS DECIMAL)), AVG(CAST(x AS DECIMAL)), VAR_POP(CAST(x AS DECIMAL)) FROM (SELECT '-infinity' AS x UNION ALL SELECT 'infinity') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知, avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN",
    "NaN",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.9 ms。
- 返回行数：1；字段：SUM(CAST(x AS DECIMAL)): decimal / DECIMAL, AVG(CAST(x AS DECIMAL)): decimal / DECIMAL, VAR_POP(CAST(x AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null,
    null
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

### pg-aggregates-0070-59676ab5 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric)
FROM (VALUES ('-infinity'), ('-infinity')) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(CAST(x AS DECIMAL)), AVG(CAST(x AS DECIMAL)), VAR_POP(CAST(x AS DECIMAL)) FROM (SELECT '-infinity' AS x UNION ALL SELECT '-infinity') AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sum: unknown / 原生类型未知, avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-Infinity",
    "-Infinity",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.1 ms。
- 返回行数：1；字段：SUM(CAST(x AS DECIMAL)): decimal / DECIMAL, AVG(CAST(x AS DECIMAL)): decimal / DECIMAL, VAR_POP(CAST(x AS DECIMAL)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null,
    null
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

### pg-aggregates-0071-3dc674b8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT avg(x::float8), var_pop(x::float8)
FROM (VALUES (100000003), (100000004), (100000006), (100000007)) v(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT AVG(CAST(x AS DOUBLE)), VAR_POP(CAST(x AS DOUBLE)) FROM (SELECT 100000003 AS x UNION ALL SELECT 100000004 UNION ALL SELECT 100000006 UNION ALL SELECT 100000007) AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：avg: unknown / 原生类型未知, var_pop: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "100000005",
    "2.5"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.6 ms。
- 返回行数：1；字段：AVG(CAST(x AS DOUBLE)): float / DOUBLE, VAR_POP(CAST(x AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    100000005.0,
    2.500000004967054
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
