# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:08.817770+00:00 至 2026-11-11T09:40:09.131310+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/groupingsets.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**17**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/17 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/15 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**17**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**2**；源参考结果不可用：**0**；Doris 执行失败：**11**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 11 |
| 返回记录行数不同（`ROW_COUNT_MISMATCH`） | 4 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 2 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 17 条只读查询、跳过 197 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–11 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 13–14 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 15–15 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 4 | 16–27 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 5 | 28–28 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 6 | 29–32 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 7 | 34–35 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 8 | 36–40 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 42–42 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 10 | 44–50 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 11 | 52–54 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 39 | 157–162 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 48 | 202–202 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 49 | 204–209 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 51 | 217–222 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 53 | 230–235 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 56 | 245–252 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 58 | 261–266 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 60 | 273–277 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 64 | 294–296 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 65 | 298–300 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 78 | 325–327 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 84 | 343–344 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 86 | 348–350 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 87 | 352–355 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 89 | 358–359 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 91 | 362–364 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 93 | 367–368 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 95 | 371–372 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 107 | 404–406 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 111 | 417–418 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 113 | 422–423 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 114 | 425–428 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 117 | 441–446 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 119 | 453–458 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 121 | 462–463 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 124 | 466–467 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 126 | 469–470 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 128 | 476–479 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 130 | 487–491 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 132 | 495–498 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 134 | 503–505 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 136 | 508–510 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 138 | 514–517 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 140 | 523–523 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 141 | 524–524 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 143 | 526–526 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 144 | 527–527 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 148 | 535–535 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 149 | 536–536 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 156 | 549–551 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 157 | 552–552 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 158 | 553–553 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 159 | 554–559 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 160 | 560–565 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 161 | 567–567 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 162 | 568–573 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 165 | 586–587 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 167 | 589–589 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 168 | 590–590 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 169 | 592–592 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 170 | 594–594 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 171 | 595–595 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 173 | 603–611 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 175 | 614–614 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 176 | 615–615 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 177 | 617–617 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 178 | 619–621 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 179 | 622–622 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 180 | 623–623 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 181 | 625–627 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 182 | 629–631 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 183 | 633–635 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 184 | 636–636 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 185 | 638–640 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 186 | 642–644 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 187 | 646–646 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 188 | 647–647 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 189 | 648–648 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 191 | 656–656 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 192 | 657–657 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 197 | 685–687 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 199 | 690–691 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 201 | 694–695 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 202 | 696–696 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 203 | 698–706 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 205 | 717–725 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 207 | 736–738 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 209 | 741–742 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 211 | 745–750 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 213 | 757–761 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 215 | 768–772 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 217 | 779–780 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 219 | 783–786 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 221 | 792–797 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 223 | 804–808 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 18 | 83–85 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 87–90 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 91–93 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 94–96 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 22 | 97–99 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 23 | 100–102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 24 | 103–105 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 25 | 106–108 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 26 | 109–111 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 27 | 112–114 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 33 | 126–129 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 34 | 131–133 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 35 | 135–137 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 36 | 139–141 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 37 | 143–150 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 38 | 152–155 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 40 | 164–166 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 50 | 211–215 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 52 | 224–228 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 54 | 237–241 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 57 | 254–259 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 59 | 268–271 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 61 | 279–282 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 62 | 284–288 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 63 | 290–292 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 67 | 304–305 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 68 | 306–306 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 69 | 307–307 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 309–310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 71 | 311–311 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 72 | 313–315 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 316–316 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 74 | 317–317 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 75 | 318–319 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 320–320 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 77 | 321–323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 79 | 329–330 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 80 | 332–333 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 335–338 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 82 | 340–341 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 83 | 342–342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 85 | 346–347 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 88 | 356–356 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 90 | 360–360 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 92 | 365–365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 94 | 369–369 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 373–373 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 375–378 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 379–381 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 382–384 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 385–387 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 388–390 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 392–394 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 103 | 396–397 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 398–398 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 400–401 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 402–402 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 408–410 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 411–411 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 413–416 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 420–421 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 430–433 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 116 | 435–440 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 118 | 448–452 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 460–461 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 464–464 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 465–465 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 468–468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 472–475 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 481–486 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 492–494 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 133 | 500–502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 135 | 506–507 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 511–513 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 142 | 525–525 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 528–528 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 150 | 537–537 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 152 | 540–541 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 153 | 542–542 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 154 | 544–546 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 155 | 547–547 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 163 | 575–581 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 164 | 582–584 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 172 | 597–601 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 190 | 650–654 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 193 | 659–665 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 194 | 667–671 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 195 | 673–677 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 679–683 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 198 | 688–688 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 200 | 692–692 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 204 | 708–715 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 727–734 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 210 | 743–743 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 212 | 752–755 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 214 | 763–766 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 216 | 774–777 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 218 | 781–781 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 220 | 788–790 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 222 | 799–802 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 224 | 810–813 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/groupingsets.out`；SHA-256（文件内容指纹）：`e4af7795e4588fe492e8c4a07f759c761c27e0a301ba902b13e5702f68b8f55e`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-groupingsets-0012-47939b25` | select a, b, grouping(a,b), sum(v), count(*), max(v)   from gstest1 group by rollup (a,b); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0013-83db7fee` | select a, b, grouping(a,b), sum(v), count(*), max(v)   from gstest1 group by rollup (a,b) order by a,b; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0014-b141c3ba` | select a, b, grouping(a,b), sum(v), count(*), max(v)   from gstest1 group by rollup (a,b) order by b desc, a; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0015-e4cf5a89` | select a, b, grouping(a,b), sum(v), count(*), max(v)   from gstest1 group by rollup (a,b) order by coalesce(a,0)+coalesce(b,0); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0016-15aa8e20` | select a, b, grouping(a,b),        array_agg(v order by v),        string_agg(v::text, ':' order by v desc),        percentile_disc(0.5) within group (order by v),        rank(1,2,12) within group (order by a,b,v)   from gstest1 group by rollup (a,b) order by a,b; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0017-8889a9e8` | select grouping(a), a, array_agg(b),        rank(a) within group (order by b nulls first),        rank(a) within group (order by b nulls last)   from (values (1,1),(1,4),(1,5),(3,1),(3,2)) v(a,b)  group by rollup (a) order by a; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0028-d2a04692` | select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),a); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0029-387a8c8f` | select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),()); | 已生成 | 成功 | 成功 | 返回记录行数不同 |
| `pg-groupingsets-0030-16a2fa51` | select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),(),(),()); | 已生成 | 成功 | 成功 | 返回记录行数不同 |
| `pg-groupingsets-0031-06f6c711` | select sum(v), count(*) from gstest_empty group by grouping sets ((),(),()); | 已生成 | 成功 | 成功 | 返回记录行数不同 |
| `pg-groupingsets-0032-d2827749` | select t1.a, t2.b, sum(t1.v), count(*) from gstest_empty t1, gstest_empty t2  group by grouping sets ((t1.a,t2.b),()); | 已生成 | 成功 | 成功 | 返回记录行数不同 |
| `pg-groupingsets-0041-b9f11f48` | select four, x   from (select four, ten, 'foo'::text as x from tenk1) as t   group by grouping sets (four, x)   having x = 'foo'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0042-433b1d44` | select four, x \|\| 'x'   from (select four, ten, 'foo'::text as x from tenk1) as t   group by grouping sets (four, x)   order by four; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0043-d829133a` | select (x+y)*1, sum(z)  from (select 1 as x, 2 as y, 3 as z) s  group by grouping sets (x+y, x); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0044-399e0bff` | select x, not x as not_x, q2 from   (select *, q1 = 1 as x from int8_tbl i1) as t   group by grouping sets(x, q2)   order by x, q2; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-groupingsets-0045-e2685715` | select x, y   from (select four as x, four as y from tenk1) as t   group by grouping sets (x, y)   having y is null   order by 1, 2; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-groupingsets-0046-ee2dc97b` | select x, y \|\| 'y'   from (select four as x, four as y from tenk1) as t   group by grouping sets (x, y)   order by 1, 2; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-groupingsets-0012-47939b25 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：12；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, grouping: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知, max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "1",
    "0",
    "21",
    "2",
    "11"
  ],
  [
    "1",
    "2",
    "0",
    "25",
    "2",
    "13"
  ],
  [
    "1",
    "3",
    "0",
    "14",
    "1",
    "14"
  ],
  [
    "1",
    "",
    "1",
    "60",
    "5",
    "14"
  ],
  [
    "2",
    "3",
    "0",
    "15",
    "1",
    "15"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 28.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
doris_error_code=1105
```

### pg-groupingsets-0013-83db7fee — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by a,b;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：12；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, grouping: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知, max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "1",
    "0",
    "21",
    "2",
    "11"
  ],
  [
    "1",
    "2",
    "0",
    "25",
    "2",
    "13"
  ],
  [
    "1",
    "3",
    "0",
    "14",
    "1",
    "14"
  ],
  [
    "1",
    "",
    "1",
    "60",
    "5",
    "14"
  ],
  [
    "2",
    "3",
    "0",
    "15",
    "1",
    "15"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
doris_error_code=1105
```

### pg-groupingsets-0014-b141c3ba — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by b desc, a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END DESC, b DESC, CASE WHEN a IS NULL THEN 1 ELSE 0 END, a
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：12；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, grouping: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知, max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "",
    "1",
    "60",
    "5",
    "14"
  ],
  [
    "2",
    "",
    "1",
    "15",
    "1",
    "15"
  ],
  [
    "3",
    "",
    "1",
    "33",
    "2",
    "17"
  ],
  [
    "4",
    "",
    "1",
    "37",
    "2",
    "19"
  ],
  [
    "",
    "",
    "3",
    "145",
    "10",
    "19"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
doris_error_code=1105
```

### pg-groupingsets-0015-e4cf5a89 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, grouping(a,b), sum(v), count(*), max(v)
  from gstest1 group by rollup (a,b) order by coalesce(a,0)+coalesce(b,0);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, GROUPING(a, b), SUM(v), COUNT(*), MAX(v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN COALESCE(a, 0) + COALESCE(b, 0) IS NULL THEN 1 ELSE 0 END, COALESCE(a, 0) + COALESCE(b, 0)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：12；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, grouping: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知, max: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "",
    "3",
    "145",
    "10",
    "19"
  ],
  [
    "1",
    "",
    "1",
    "60",
    "5",
    "14"
  ],
  [
    "1",
    "1",
    "0",
    "21",
    "2",
    "11"
  ],
  [
    "2",
    "",
    "1",
    "15",
    "1",
    "15"
  ],
  [
    "3",
    "",
    "1",
    "33",
    "2",
    "17"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 14.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GROUPING' which has 2 arity. Candidate functions are: [GROUPING(Expression)]")
doris_error_code=1105
```

### pg-groupingsets-0016-15aa8e20 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, grouping(a,b),
       array_agg(v order by v),
       string_agg(v::text, ':' order by v desc),
       percentile_disc(0.5) within group (order by v),
       rank(1,2,12) within group (order by a,b,v)
  from gstest1 group by rollup (a,b) order by a,b;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, GROUPING(a, b), COLLECT_LIST(v ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END, v), GROUP_CONCAT(CAST(v AS STRING) ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END DESC, v DESC, ':'), PERCENTILE_DISC(0.5) WITHIN GROUP (ORDER BY CASE WHEN v IS NULL THEN 1 ELSE 0 END, v), RANK(1, 2, 12) WITHIN GROUP (ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN v IS NULL THEN 1 ELSE 0 END, v) FROM gstest1 GROUP BY ROLLUP (a, b) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN b IS NULL THEN 1 ELSE 0 END, b
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：12；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, grouping: unknown / 原生类型未知, array_agg: unknown / 原生类型未知, string_agg: unknown / 原生类型未知, percentile_disc: unknown / 原生类型未知, rank: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "1",
    "0",
    "{10,11}",
    "11:10",
    "10",
    "3"
  ],
  [
    "1",
    "2",
    "0",
    "{12,13}",
    "13:12",
    "12",
    "1"
  ],
  [
    "1",
    "3",
    "0",
    "{14}",
    "14",
    "14",
    "1"
  ],
  [
    "1",
    "",
    "1",
    "{10,11,12,13,14}",
    "14:13:12:11:10",
    "12",
    "3"
  ],
  [
    "2",
    "3",
    "0",
    "{15}",
    "15",
    "15",
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 228)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 228)\n")
doris_error_code=1105
```

### pg-groupingsets-0017-8889a9e8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select grouping(a), a, array_agg(b),
       rank(a) within group (order by b nulls first),
       rank(a) within group (order by b nulls last)
  from (values (1,1),(1,4),(1,5),(3,1),(3,2)) v(a,b)
 group by rollup (a) order by a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GROUPING(a), a, COLLECT_LIST(b), RANK(a) WITHIN GROUP (ORDER BY b), RANK(a) WITHIN GROUP (ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b) FROM (SELECT 1 AS a, 1 AS b UNION ALL SELECT 1, 4 UNION ALL SELECT 1, 5 UNION ALL SELECT 3, 1 UNION ALL SELECT 3, 2) AS v GROUP BY ROLLUP (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：grouping: unknown / 原生类型未知, a: unknown / 原生类型未知, array_agg: unknown / 原生类型未知, rank: unknown / 原生类型未知, rank: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "1",
    "{1,4,5}",
    "1",
    "1"
  ],
  [
    "0",
    "3",
    "{1,2}",
    "3",
    "3"
  ],
  [
    "1",
    "",
    "{1,4,5,1,2}",
    "1",
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 61)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 61)\n")
doris_error_code=1105
```

### pg-groupingsets-0028-d2a04692 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),a);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), a)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：0；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'a'(line 1, pos 80)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing '(' at 'a'(line 1, pos 80)\n")
doris_error_code=1105
```

### pg-groupingsets-0029-387a8c8f — 返回记录行数不同

#### 源 SQL

```sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),());
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), ())
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "",
    "",
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 32.4 ms。
- 返回行数：0；字段：a: integer / INT, b: integer / INT, SUM(v): integer / BIGINT, COUNT(*): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Result row counts differ
source=1
doris=0
```

### pg-groupingsets-0030-16a2fa51 — 返回记录行数不同

#### 源 SQL

```sql
select a, b, sum(v), count(*) from gstest_empty group by grouping sets ((a,b),(),(),());
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT a, b, SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((a, b), (), (), ())
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "",
    "",
    "0"
  ],
  [
    "",
    "",
    "",
    "0"
  ],
  [
    "",
    "",
    "",
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 28.3 ms。
- 返回行数：0；字段：a: integer / INT, b: integer / INT, SUM(v): integer / BIGINT, COUNT(*): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Result row counts differ
source=3
doris=0
```

### pg-groupingsets-0031-06f6c711 — 返回记录行数不同

#### 源 SQL

```sql
select sum(v), count(*) from gstest_empty group by grouping sets ((),(),());
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUM(v), COUNT(*) FROM gstest_empty GROUP BY GROUPING SETS ((), (), ())
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "0"
  ],
  [
    "",
    "0"
  ],
  [
    "",
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.0 ms。
- 返回行数：0；字段：SUM(v): integer / BIGINT, COUNT(*): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Result row counts differ
source=3
doris=0
```

### pg-groupingsets-0032-d2827749 — 返回记录行数不同

#### 源 SQL

```sql
select t1.a, t2.b, sum(t1.v), count(*) from gstest_empty t1, gstest_empty t2
 group by grouping sets ((t1.a,t2.b),());
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT t1.a, t2.b, SUM(t1.v), COUNT(*) FROM gstest_empty AS t1, gstest_empty AS t2 GROUP BY GROUPING SETS ((t1.a, t2.b), ())
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, sum: unknown / 原生类型未知, count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "",
    "",
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.8 ms。
- 返回行数：0；字段：a: integer / INT, b: integer / INT, SUM(t1.v): integer / BIGINT, COUNT(*): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Result row counts differ
source=1
doris=0
```

### pg-groupingsets-0041-b9f11f48 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select four, x
  from (select four, ten, 'foo'::text as x from tenk1) as t
  group by grouping sets (four, x)
  having x = 'foo';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT four, x FROM (SELECT four, ten, CAST('foo' AS STRING) AS x FROM tenk1) AS t GROUP BY GROUPING SETS (four, x) HAVING x = 'foo'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：four: unknown / 原生类型未知, x: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "",
    "foo"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 17.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 107)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 107)\n")
doris_error_code=1105
```

### pg-groupingsets-0042-433b1d44 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select four, x || 'x'
  from (select four, ten, 'foo'::text as x from tenk1) as t
  group by grouping sets (four, x)
  order by four;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT four, CONCAT(x, 'x') FROM (SELECT four, ten, CAST('foo' AS STRING) AS x FROM tenk1) AS t GROUP BY GROUPING SETS (four, x) ORDER BY CASE WHEN four IS NULL THEN 1 ELSE 0 END, four
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：four: unknown / 原生类型未知, ?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ],
  [
    "1",
    ""
  ],
  [
    "2",
    ""
  ],
  [
    "3",
    ""
  ],
  [
    "",
    "foox"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 120)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing '(' at 'four'(line 1, pos 120)\n")
doris_error_code=1105
```

### pg-groupingsets-0043-d829133a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select (x+y)*1, sum(z)
 from (select 1 as x, 2 as y, 3 as z) s
 group by grouping sets (x+y, x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT (x + y) * 1, SUM(z) FROM (SELECT 1 AS x, 2 AS y, 3 AS z) AS s GROUP BY GROUPING SETS (x + y, x)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：2；字段：?column?: unknown / 原生类型未知, sum: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3",
    "3"
  ],
  [
    "",
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 93)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 93)\n")
doris_error_code=1105
```

### pg-groupingsets-0044-399e0bff — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select x, not x as not_x, q2 from
  (select *, q1 = 1 as x from int8_tbl i1) as t
  group by grouping sets(x, q2)
  order by x, q2;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, NOT x AS not_x, q2 FROM (SELECT *, q1 = 1 AS x FROM int8_tbl AS i1) AS t GROUP BY GROUPING SETS (x, q2) ORDER BY CASE WHEN x IS NULL THEN 1 ELSE 0 END, x, CASE WHEN q2 IS NULL THEN 1 ELSE 0 END, q2
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x: unknown / 原生类型未知, not_x: unknown / 原生类型未知, q2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f",
    "t",
    ""
  ],
  [
    "",
    "",
    "-4567890123456789"
  ],
  [
    "",
    "",
    "123"
  ],
  [
    "",
    "",
    "456"
  ],
  [
    "",
    "",
    "4567890123456789"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 107)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmissing '(' at 'x'(line 1, pos 107)\n")
doris_error_code=1105
```

### pg-groupingsets-0045-e2685715 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select x, y
  from (select four as x, four as y from tenk1) as t
  group by grouping sets (x, y)
  having y is null
  order by 1, 2;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering

'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-groupingsets-0046-ee2dc97b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select x, y || 'y'
  from (select four as x, four as y from tenk1) as t
  group by grouping sets (x, y)
  order by 1, 2;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering

'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。
