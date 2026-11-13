# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:13.108743+00:00 至 2026-11-11T09:40:14.654183+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/json.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**100**；两端成功且已有证据匹配：**12**。
- 成功结果匹配占全部查询比例：**12/100 = 12.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**12/62 = 19.35%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**23**；不计入上述成功匹配分子。
- 需要分析的查询：**88**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**15**；源参考结果不可用：**0**；Doris 执行失败：**58**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 9 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 41 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 23 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 12 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 15 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 100 条只读查询、跳过 358 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 37 | 54–57 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 40 | 60–60 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 66 | 130–132 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 73 | 154–154 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 75 | 156–156 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 87 | 181–181 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 93 | 201–206 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 94 | 208–211 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 213 | 422–423 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 214 | 425–425 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 215 | 426–426 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 216 | 427–427 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 217 | 429–429 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 218 | 430–430 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 219 | 432–450 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 220 | 452–454 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 313 | 580–580 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 333 | 613–614 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 334 | 616–622 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 336 | 626–626 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 337 | 627–627 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 338 | 628–628 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 339 | 629–629 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 340 | 630–630 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 341 | 631–631 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 342 | 632–632 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 380 | 712–712 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 381 | 713–713 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 382 | 714–714 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 383 | 715–715 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 386 | 722–722 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 8–9 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 11 | 22–25 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 12 | 25–26 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 13 | 26–27 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 14 | 27–28 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 15 | 28–29 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 29–30 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 17 | 30–31 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 18 | 31–32 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 32–33 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 33–34 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 34–37 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 22 | 37–38 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 23 | 38–39 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 24 | 39–40 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 25 | 40–41 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 26 | 41–42 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 27 | 42–45 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 28 | 45–46 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 29 | 46–47 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 30 | 47–48 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 31 | 48–49 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 32 | 49–50 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 33 | 50–51 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 34 | 51–52 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 35 | 52–53 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 36 | 53–54 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 38 | 58–58 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 39 | 59–59 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 41 | 62–63 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 42 | 63–64 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 43 | 64–65 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 44 | 65–66 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 45 | 66–67 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 46 | 67–68 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 47 | 68–69 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 48 | 69–70 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 49 | 70–71 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 50 | 71–72 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 52 | 79–84 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 53 | 85–88 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 54 | 89–92 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 55 | 93–93 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 56 | 94–94 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 143–147 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 74 | 155–155 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 157–157 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 95 | 213–215 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 217–219 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 221–223 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 225–227 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 229–231 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 233–235 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 237–239 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 241–243 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 103 | 245–247 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 249–251 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 253–253 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 254–254 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 256–256 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 257–257 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 258–258 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 260–262 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 111 | 264–266 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 268–270 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 114 | 279–283 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 285–287 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 116 | 289–291 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 117 | 293–295 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 118 | 297–299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 119 | 300–300 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 301–301 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 121 | 302–302 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 303–303 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 304–304 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 306–306 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 307–307 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 128 | 309–309 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 310–310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 130 | 312–312 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 313–313 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 132 | 314–314 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 133 | 315–315 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 134 | 316–316 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 136 | 318–318 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 319–319 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 138 | 320–320 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 139 | 321–321 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 140 | 322–322 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 379–379 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 176 | 380–380 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 178 | 382–382 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 179 | 383–383 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 180 | 384–384 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 181 | 385–385 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 386–386 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 183 | 387–387 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 184 | 388–388 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 185 | 389–389 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 186 | 390–390 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 187 | 391–391 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 188 | 392–392 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 193 | 398–398 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 195 | 400–400 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 401–401 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 198 | 403–403 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 199 | 404–404 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 200 | 405–405 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 201 | 406–406 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 202 | 407–407 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 203 | 408–408 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 204 | 409–409 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 205 | 410–410 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 411–411 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 207 | 412–412 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 413–413 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 211 | 419–419 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 212 | 420–420 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 221 | 456–456 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 222 | 457–457 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 223 | 459–459 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 224 | 460–460 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 225 | 462–462 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 226 | 463–463 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 228 | 466–466 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 231 | 470–470 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 232 | 472–472 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 234 | 474–474 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 235 | 475–475 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 238 | 478–478 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 239 | 480–480 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 241 | 482–482 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 242 | 483–483 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 243 | 485–485 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 246 | 488–488 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 247 | 490–490 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 248 | 491–491 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 249 | 492–492 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 250 | 493–493 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 251 | 494–494 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 252 | 496–496 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 253 | 497–497 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 254 | 499–499 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 255 | 500–500 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 256 | 501–501 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 257 | 502–502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 258 | 503–503 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 259 | 504–504 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 260 | 506–506 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 261 | 507–507 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 262 | 508–508 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 263 | 509–509 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 264 | 511–511 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 265 | 512–512 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 266 | 513–513 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 267 | 514–514 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 268 | 516–516 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 269 | 517–517 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 270 | 518–518 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 271 | 519–519 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 272 | 520–520 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 273 | 522–522 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 274 | 523–523 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 275 | 524–524 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 276 | 525–525 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 277 | 526–526 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 278 | 527–527 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 279 | 528–528 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 280 | 530–530 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 281 | 531–531 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 282 | 532–532 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 283 | 533–533 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 284 | 534–534 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 285 | 535–535 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 286 | 536–536 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 287 | 538–538 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 288 | 539–539 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 289 | 540–540 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 290 | 541–541 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 291 | 543–543 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 292 | 544–544 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 293 | 545–545 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 294 | 546–546 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 295 | 548–548 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 296 | 549–549 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 297 | 550–550 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 298 | 551–551 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 299 | 552–552 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 300 | 554–558 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 304 | 566–567 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 305 | 568–568 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 307 | 571–573 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 308 | 574–574 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 309 | 575–575 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 310 | 576–576 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 311 | 577–577 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 314 | 581–581 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 315 | 583–583 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 316 | 584–584 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 317 | 585–585 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 324 | 598–598 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 326 | 602–603 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 327 | 604–604 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 332 | 611–611 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 335 | 624–624 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 343 | 634–647 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 344 | 649–651 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 345 | 652–652 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 346 | 652–653 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 347 | 653–654 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 348 | 654–655 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 349 | 655–656 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 350 | 656–657 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 351 | 657–658 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 352 | 658–659 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 353 | 659–661 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 354 | 663–666 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 355 | 667–667 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 356 | 667–668 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 357 | 668–669 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 358 | 669–670 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 359 | 670–671 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 360 | 671–672 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 361 | 672–673 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 362 | 673–674 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 363 | 674–675 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 364 | 675–676 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 365 | 676–677 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 366 | 677–678 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 367 | 678–679 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 368 | 679–682 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 369 | 684–684 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 370 | 686–687 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 371 | 689–690 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 372 | 692–692 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 373 | 694–694 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 374 | 696–696 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 375 | 698–699 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 376 | 700–700 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 377 | 702–703 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 378 | 705–706 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 379 | 708–710 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 384 | 717–718 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 385 | 720–720 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 387 | 723–723 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 388 | 725–727 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 389 | 729–730 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 391 | 737–738 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 398 | 758–760 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 399 | 762–763 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 400 | 765–767 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 401 | 769–769 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 402 | 771–773 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 403 | 775–777 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 404 | 779–780 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 405 | 782–785 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 406 | 787–788 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 407 | 790–791 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 408 | 793–795 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 409 | 797–799 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 410 | 801–801 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 411 | 802–802 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 412 | 803–803 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 413 | 804–804 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 414 | 805–805 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 415 | 806–806 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 416 | 808–808 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 417 | 809–809 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 418 | 810–810 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 419 | 812–812 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 420 | 813–813 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 421 | 814–814 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 422 | 815–815 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 423 | 816–816 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 424 | 817–817 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 425 | 819–821 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 426 | 823–823 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 427 | 825–825 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 428 | 827–827 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 429 | 829–829 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 430 | 831–831 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 431 | 833–833 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 432 | 835–836 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 433 | 838–840 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 434 | 842–842 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 435 | 844–844 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 436 | 846–846 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 437 | 848–848 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 438 | 850–850 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 439 | 852–852 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 440 | 854–855 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 441 | 857–858 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 442 | 860–861 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 443 | 863–864 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 444 | 866–867 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 445 | 869–870 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 446 | 871–871 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 447 | 872–872 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 448 | 873–873 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 449 | 874–874 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 450 | 875–875 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 451 | 877–877 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 452 | 878–878 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 453 | 879–879 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 454 | 880–880 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 455 | 881–881 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 456 | 882–882 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 457 | 884–885 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 458 | 886–886 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 459 | 887–887 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 460 | 888–888 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 461 | 890–891 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 462 | 892–892 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 463 | 893–893 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 464 | 894–894 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 465 | 896–896 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 466 | 897–897 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 467 | 898–898 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 468 | 899–899 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 469 | 900–900 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 470 | 902–903 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 471 | 904–904 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 472 | 905–905 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 473 | 906–906 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 474 | 908–909 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 475 | 910–910 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 476 | 911–911 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/json.out`；SHA-256（文件内容指纹）：`74ad74a6c44bfb59bbc164a2da580f6f1b9bb963539ccc1e15c9931ee9000666`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 85/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 85/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 62/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 62/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 62/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/85 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-json-0001-ac1e931c` | SELECT '""'::json; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0002-a9391cc9` | SELECT $$''$$::json; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0003-a8fd7c0f` | SELECT '"abc"'::json; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0004-8c23f394` | SELECT '"abc'::json; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0005-337abb27` | SELECT '"abc def"'::json; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0006-91cdacbb` | SELECT '"\n\"\\"'::json; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0008-e7cb155d` | SELECT ('"'\|\|repeat('.', 12)\|\|'abc"')::json; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0009-313655d2` | SELECT ('"'\|\|repeat('.', 12)\|\|'abc\n"')::json; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0010-cb8ffd73` | SELECT row_to_json(j)::jsonb FROM (   SELECT left(E'abcdefghijklmnopqrstuv"\twxyz012345678', a) AS a   FROM generate_series(0,37) a ) j; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0057-738e7b11` | SELECT array_to_json(array(select 1 as a)); | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0058-9bb364f3` | SELECT array_to_json(array_agg(q),false) from (select x as b, x * 2 as c from generate_series(1,3) x) q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0060-0cb6c97c` | SELECT array_to_json(array_agg(q),false)   FROM ( SELECT $$a$$ \|\| x AS b, y AS c,                ARRAY[ROW(x.*,ARRAY[1,2,3]),                ROW(y.*,ARRAY[4,5,6])] AS z          FROM generate_series(1,2) x,               generate_series(4,5) y) q; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0061-afcbc0b7` | SELECT array_to_json(array_agg(x),false) from generate_series(5,10) x; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0062-0fa82900` | SELECT array_to_json('{{1,5},{99,100}}'::int[]); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0063-7e24ac8c` | SELECT row_to_json(row(1,'foo')); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0064-dce5ae8b` | SELECT row_to_json(q) FROM (SELECT $$a$$ \|\| x AS b,          y AS c,          ARRAY[ROW(x.*,ARRAY[1,2,3]),                ROW(y.*,ARRAY[4,5,6])] AS z       FROM generate_series(1,2) x,            generate_series(4,5) y) q; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0068-c724f117` | SELECT row_to_json(row((select array_agg(x) as d from generate_series(5,10) x)),false); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0071-d1f20a64` | select to_json(timestamp '2014-05-28 12:22:35.614298'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0078-eeeb5bc2` | select to_json(date '2014-05-28'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0079-f44824a3` | select to_json(date 'Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0080-bf0070b1` | select to_json(date '-Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0081-2bcf40b3` | select to_json(timestamp 'Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0082-82638770` | select to_json(timestamp '-Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0083-a4e2831c` | select to_json(timestamptz 'Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0084-fcf1ca0f` | select to_json(timestamptz '-Infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0089-eb7daff4` | SELECT row_to_json(q) FROM (SELECT 'NaN'::float8 AS "float8field") q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0090-e2fc96bf` | SELECT row_to_json(q) FROM (SELECT 'Infinity'::float8 AS "float8field") q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0091-f2eba6f2` | SELECT row_to_json(q) FROM (SELECT '-Infinity'::float8 AS "float8field") q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0092-3eab2396` | SELECT row_to_json(q) FROM (SELECT '{"a":1,"b": [2,3,4,"d","e","f"],"c":{"p":1,"q":2}}'::json AS "jsonfield") q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0124-97d7a8af` | select '[{"b": "c"}, {"b": "cc"}]'::json -> 1; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0127-00bf016f` | select '{"a": "c", "b": null}'::json -> 'b'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0135-0315e130` | select '[{"b": "c"}, {"b": "cc"}]'::json ->> 1; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0141-88ef2e6c` | SELECT json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0142-f298c4a6` | SELECT json_array_length('[]'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0143-0c4db36e` | SELECT json_array_length('{"f1":1,"f2":[5,6]}'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-json-0144-98130b06` | SELECT json_array_length('4'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-json-0145-0361b143` | select json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0146-a330ea38` | select * from json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0147-25b95a0c` | select json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0148-6cfaea21` | select * from json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0149-87b9e9bb` | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0150-61dc1a45` | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f2'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0151-c71ce0d8` | select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0152-73a3e57c` | select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0153-859161a9` | select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0154-fc734092` | select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f2'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0155-579440b1` | select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0156-f9da221f` | select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0157-3bafa8b8` | select json_extract_path('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}','f4','f5') is null as expect_false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0158-382f7a2f` | select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}','f4','f5') is null as expect_true; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0159-72282a2d` | select json_extract_path('{"f2":{"f3":1},"f4":[0,1,2,null]}','f4','3') is null as expect_false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-json-0160-7531df7d` | select json_extract_path_text('{"f2":{"f3":1},"f4":[0,1,2,null]}','f4','3') is null as expect_true; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-json-0161-635df7fb` | select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f4','f6']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0162-6b380766` | select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0163-093476ed` | select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','0']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0164-0923d889` | select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','1']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0165-7c004789` | select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f4','f6']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0166-6c15e0b8` | select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0167-f3c33896` | select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','0']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0168-d6b16d12` | select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','1']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0169-9fd69726` | select '{"a": {"b":{"c": "foo"}}}'::json #> '{}'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0170-8b87c6e3` | select '[1,2,3]'::json #> '{}'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0171-474250d3` | select '"foo"'::json #> '{}'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0172-2baee281` | select '42'::json #> '{}'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0173-95c2a2f0` | select 'null'::json #> '{}'; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0174-ff8d41d2` | select '{"a": {"b":{"c": "foo"}}}'::json #> array['a']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0177-0fec5401` | select '{"a": {"b":{"c": "foo"}}}'::json #> array['a','b']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0189-38c2bdc3` | select '{"a": {"b":{"c": "foo"}}}'::json #>> '{}'; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0190-1355b395` | select '[1,2,3]'::json #>> '{}'; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0191-09aa37c5` | select '"foo"'::json #>> '{}'; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0192-7c14c3b1` | select '42'::json #>> '{}'; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0194-013c6457` | select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0197-ffab593b` | select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a','b']; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-json-0209-aeb87cd2` | select json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0210-22d857f7` | select * from json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]') q; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0227-20e44f1c` | select * from json_populate_record(row('x',3,'2012-12-31 15:30:56')::jpop,'{"c":[100,200,false],"x":43.2}') q; | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-json-0229-42b1c6de` | SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"x": 43.2}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0230-f2548d30` | SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"i": null}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0233-033a5496` | SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": 123}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0236-8da8813f` | SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], 2]}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0237-bf9a4bfe` | SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], [2, 3]]}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0240-4b741b3d` | SELECT ia1 FROM json_populate_record(NULL::jsrec, '{"ia1": 123}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0244-a7d926ba` | SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": 123}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0245-2664dfc2` | SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": [1, "2", null, 4]}') q; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0301-4a500f7b` | SELECT json_populate_record(null::record, '{"x": 0, "y": 1}'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0302-3c69d4c1` | SELECT json_populate_record(row(1,2), '{"f1": 0, "f2": 1}'); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0303-cbcb2e92` | SELECT * FROM   json_populate_record(null::record, '{"x": 776}') AS (x int, y int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0306-96555daa` | SELECT json_populate_record(row(1,2)::j_ordered_pair, '{"x": 1, "y": 0}'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：类型转换失败 | 两端均报错，但错误类别不同 |
| `pg-json-0312-8e4d5fdb` | select * from json_populate_recordset(row('def',99,null)::jpop,'[{"c":[100,200,300],"x":43.2},{"a":{"z":true},"b":3,"c":"2012-01-20 10:42:53"}]') q; | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |
| `pg-json-0318-ef190f63` | SELECT json_populate_recordset(null::record, '[{"x": 0, "y": 1}]'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0319-8d0c4542` | SELECT json_populate_recordset(row(1,2), '[{"f1": 0, "f2": 1}]'); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0320-baa89283` | SELECT i, json_populate_recordset(row(i,50), '[{"f1":"42"},{"f2":"43"}]') FROM (VALUES (1),(2)) v(i); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0321-520ea364` | SELECT * FROM   json_populate_recordset(null::record, '[{"x": 776}]') AS (x int, y int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0322-407e5563` | SELECT json_populate_recordset(null::record, '[]'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-json-0323-4b6a9697` | SELECT json_populate_recordset(row(1,2), '[]'); | 已生成 | 成功 | 失败：语法解析失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0325-eb75b13d` | SELECT * FROM   json_populate_recordset(null::record, '[]') AS (x int, y int); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-json-0328-37e9bde0` | SELECT json_populate_recordset(row(1,2)::j_ordered_pair, '[{"x": 1, "y": 0}]'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：类型转换失败 | 两端均报错，但错误类别不同 |
| `pg-json-0329-6f800f54` | select * from json_populate_recordset(row(0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); | 已生成 | 失败：函数不存在或调用形式不受支持 | 失败：语法解析失败 | 两端均报错，但错误类别不同 |
| `pg-json-0330-2fc0f965` | select * from json_populate_recordset(row(0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); | 已生成 | 失败：函数不存在或调用形式不受支持 | 失败：语法解析失败 | 两端均报错，但错误类别不同 |
| `pg-json-0331-a68233a0` | select * from json_populate_recordset(row(0::int,0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text); | 已生成 | 失败：函数不存在或调用形式不受支持 | 失败：语法解析失败 | 两端均报错，但错误类别不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-json-0002-a9391cc9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT $$''$$::json;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('''''' AS JSON)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type json`。

错误原文：

```text
invalid input syntax for type json
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.9 ms。
- 返回行数：1；字段：CAST('''''' AS JSON): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type json
source_error_code=invalid input syntax for type json
```

### pg-json-0004-8c23f394 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '"abc'::json;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('"abc' AS JSON)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type json`。

错误原文：

```text
invalid input syntax for type json
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.1 ms。
- 返回行数：1；字段：CAST('"abc' AS JSON): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type json
source_error_code=invalid input syntax for type json
```

### pg-json-0005-337abb27 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '"abc
def"'::json;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('"abc\ndef"' AS JSON)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type json`。

错误原文：

```text
invalid input syntax for type json
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.8 ms。
- 返回行数：1；字段：CAST('"abc\ndef"' AS JSON): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null
  ]
]
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Source evidence and Doris execution status differ
source_success=False
doris_success=True
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type json
source_error_code=invalid input syntax for type json
```

### pg-json-0010-cb8ffd73 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(j)::jsonb FROM (
  SELECT left(E'abcdefghijklmnopqrstuv"\twxyz012345678', a) AS a
  FROM generate_series(0,37) a
) j;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(ROW_TO_JSON(j) AS JSONB) FROM (SELECT LEFT('abcdefghijklmnopqrstuv"\twxyz012345678', a) AS a FROM GENERATE_SERIES(0, 37) AS a) AS j
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：38；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": \"\"}"
  ],
  [
    "{\"a\": \"a\"}"
  ],
  [
    "{\"a\": \"ab\"}"
  ],
  [
    "{\"a\": \"abc\"}"
  ],
  [
    "{\"a\": \"abcd\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 127)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 127)\n")
doris_error_code=1105
```

### pg-json-0057-738e7b11 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT array_to_json(array(select 1 as a));
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0058-9bb364f3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT array_to_json(array_agg(q),false) from (select x as b, x * 2 as c from generate_series(1,3) x) q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ARRAY_TO_JSON(COLLECT_LIST(q), FALSE) FROM (SELECT x AS b, x * 2 AS c FROM GENERATE_SERIES(1, 3) AS x) AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：array_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "[{\"b\":1,\"c\":2},{\"b\":2,\"c\":4},{\"b\":3,\"c\":6}]"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 99)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 99)\n")
doris_error_code=1105
```

### pg-json-0060-0cb6c97c — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT array_to_json(array_agg(q),false)
  FROM ( SELECT $$a$$ || x AS b, y AS c,
               ARRAY[ROW(x.*,ARRAY[1,2,3]),
               ROW(y.*,ARRAY[4,5,6])] AS z
         FROM generate_series(1,2) x,
              generate_series(4,5) y) q;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0061-afcbc0b7 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT array_to_json(array_agg(x),false) from generate_series(5,10) x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ARRAY_TO_JSON(COLLECT_LIST(x), FALSE) FROM GENERATE_SERIES(5, 10) AS x
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：array_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "[5,6,7,8,9,10]"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 67)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting EQ(line 1, pos 67)\n")
doris_error_code=1105
```

### pg-json-0062-0fa82900 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT array_to_json('{{1,5},{99,100}}'::int[]);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ARRAY_TO_JSON(CAST('{{1,5},{99,100}}' AS ARRAY<INT>))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：array_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "[[1,5],[99,100]]"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'ARRAY_TO_JSON'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'ARRAY_TO_JSON'")
doris_error_code=1105
```

### pg-json-0063-7e24ac8c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(row(1,'foo'));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(ROW(1, 'foo'))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"f1\":1,\"f2\":\"foo\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.8 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
doris_error_code=1105
```

### pg-json-0064-dce5ae8b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT row_to_json(q)
FROM (SELECT $$a$$ || x AS b,
         y AS c,
         ARRAY[ROW(x.*,ARRAY[1,2,3]),
               ROW(y.*,ARRAY[4,5,6])] AS z
      FROM generate_series(1,2) x,
           generate_series(4,5) y) q;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL

Arrays are not supported by MySQL

Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0068-c724f117 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(row((select array_agg(x) as d from generate_series(5,10) x)),false);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(ROW((SELECT COLLECT_LIST(x) AS d FROM GENERATE_SERIES(5, 10) AS x)), FALSE)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"f1\":[5,6,7,8,9,10]}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.6 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 19)\n")
doris_error_code=1105
```

### pg-json-0071-d1f20a64 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(timestamp '2014-05-28 12:22:35.614298');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('2014-05-28 12:22:35.614298' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"2014-05-28T12:22:35.614298\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.6 ms。
- 返回行数：1；字段：TO_JSON(CAST('2014-05-28 12:22:35.614298' AS DATETIME)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"2014-05-28 12:22:36\""
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

### pg-json-0079-f44824a3 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(date 'Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('Infinity' AS DATE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：TO_JSON(CAST('Infinity' AS DATE)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0080-bf0070b1 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(date '-Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('-Infinity' AS DATE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"-infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：TO_JSON(CAST('-Infinity' AS DATE)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0081-2bcf40b3 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(timestamp 'Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('Infinity' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：TO_JSON(CAST('Infinity' AS DATETIME)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0082-82638770 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(timestamp '-Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('-Infinity' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"-infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.2 ms。
- 返回行数：1；字段：TO_JSON(CAST('-Infinity' AS DATETIME)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0083-a4e2831c — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(timestamptz 'Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('Infinity' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.1 ms。
- 返回行数：1；字段：TO_JSON(CAST('Infinity' AS DATETIME)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0084-fcf1ca0f — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select to_json(timestamptz '-Infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TO_JSON(CAST('-Infinity' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"-infinity\""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：TO_JSON(CAST('-Infinity' AS DATETIME)): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-json-0089-eb7daff4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(q)
FROM (SELECT 'NaN'::float8 AS "float8field") q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('NaN' AS DOUBLE) AS `float8field`) AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"float8field\":\"NaN\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
doris_error_code=1105
```

### pg-json-0090-e2fc96bf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(q)
FROM (SELECT 'Infinity'::float8 AS "float8field") q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('Infinity' AS DOUBLE) AS `float8field`) AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"float8field\":\"Infinity\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
doris_error_code=1105
```

### pg-json-0091-f2eba6f2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(q)
FROM (SELECT '-Infinity'::float8 AS "float8field") q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('-Infinity' AS DOUBLE) AS `float8field`) AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"float8field\":\"-Infinity\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
doris_error_code=1105
```

### pg-json-0092-3eab2396 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT row_to_json(q)
FROM (SELECT '{"a":1,"b": [2,3,4,"d","e","f"],"c":{"p":1,"q":2}}'::json AS "jsonfield") q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW_TO_JSON(q) FROM (SELECT CAST('{"a":1,"b": [2,3,4,"d","e","f"],"c":{"p":1,"q":2}}' AS JSON) AS `jsonfield`) AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：row_to_json: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"jsonfield\":{\"a\":1,\"b\": [2,3,4,\"d\",\"e\",\"f\"],\"c\":{\"p\":1,\"q\":2}}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'q' in 'table list' in PROJECT clause(line 1, pos 19)")
doris_error_code=1105
```

### pg-json-0124-97d7a8af — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select '[{"b": "c"}, {"b": "cc"}]'::json -> 1;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"b\": \"cc\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.0 ms。
- 返回行数：1；字段：JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]'): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"b\":\"cc\"}"
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

### pg-json-0135-0315e130 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select '[{"b": "c"}, {"b": "cc"}]'::json ->> 1;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"b\": \"cc\"}"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.4 ms。
- 返回行数：1；字段：JSON_EXTRACT(CAST('[{"b": "c"}, {"b": "cc"}]' AS JSON), '$[1]'): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"b\":\"cc\"}"
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

### pg-json-0141-88ef2e6c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT json_array_length('[1,2,3,{"f1":1,"f2":[5,6]},4]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_ARRAY_LENGTH('[1,2,3,{"f1":1,"f2":[5,6]},4]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_array_length: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
doris_error_code=1105
```

### pg-json-0142-f298c4a6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT json_array_length('[]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_ARRAY_LENGTH('[]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_array_length: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 76.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
doris_error_code=1105
```

### pg-json-0143-0c4db36e — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT json_array_length('{"f1":1,"f2":[5,6]}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_ARRAY_LENGTH('{"f1":1,"f2":[5,6]}')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot get array length of a non-array`。

错误原文：

```text
cannot get array length of a non-array
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 25.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=cannot get array length of a non-array
source_error_code=cannot get array length of a non-array
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
doris_error_code=1105
```

### pg-json-0144-98130b06 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT json_array_length('4');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_ARRAY_LENGTH('4')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot get array length of a scalar`。

错误原文：

```text
cannot get array length of a scalar
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 16.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=cannot get array length of a scalar
source_error_code=cannot get array length of a scalar
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_LENGTH'")
doris_error_code=1105
```

### pg-json-0145-0361b143 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：json_each: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(f1,\"[1,2,3]\")"
  ],
  [
    "(f2,\"{\"\"f3\"\":1}\")"
  ],
  [
    "(f4,null)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null}\' as JSON))')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null}\' as JSON))')
doris_error_code=1105
```

### pg-json-0146-a330ea38 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from json_each('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_EACH('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：key: unknown / 原生类型未知, value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f1",
    "[1,2,3]"
  ],
  [
    "f2",
    "{\"f3\":1}"
  ],
  [
    "f4",
    "null"
  ],
  [
    "f5",
    "99"
  ],
  [
    "f6",
    "\"stringy\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 87)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 87)\n")
doris_error_code=1105
```

### pg-json-0147-25b95a0c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：json_each_text: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(f1,\"[1,2,3]\")"
  ],
  [
    "(f2,\"{\"\"f3\"\":1}\")"
  ],
  [
    "(f4,)"
  ],
  [
    "(f5,null)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 20.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each_text(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}\' as JSON))')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = LOGICAL_PROJECT can not contains TableGeneratingFunction expression: json_each_text(cast(\'{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":"null"}\' as JSON))')
doris_error_code=1105
```

### pg-json-0148-6cfaea21 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from json_each_text('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_EACH_TEXT('{"f1":[1,2,3],"f2":{"f3":1},"f4":null,"f5":99,"f6":"stringy"}') AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：key: unknown / 原生类型未知, value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f1",
    "[1,2,3]"
  ],
  [
    "f2",
    "{\"f3\":1}"
  ],
  [
    "f4",
    ""
  ],
  [
    "f5",
    "99"
  ],
  [
    "f6",
    "stringy"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 92)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 92)\n")
doris_error_code=1105
```

### pg-json-0151-c71ce0d8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2', CAST(0 AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_extract_path: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"f3\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
doris_error_code=1105
```

### pg-json-0152-73a3e57c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_extract_path('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2', CAST(1 AS STRING))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_extract_path: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 17.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
doris_error_code=1105
```

### pg-json-0153-859161a9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}','f4','f6');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_extract_path_text: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "stringy"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 28.3 ms。
- 返回行数：1；字段：JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}', '$.f4.f6'): string / JSON。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"stringy\""
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

### pg-json-0155-579440b1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',0::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_extract_path_text: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 17.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
doris_error_code=1105
```

### pg-json-0156-f9da221f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_extract_path_text('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}','f2',1::text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}', 'f2')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_extract_path_text: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: f2')
doris_error_code=1105
```

### pg-json-0158-382f7a2f — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select json_extract_path_text('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}','f4','f5') is null as expect_true;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":{"f5":null,"f6":"stringy"}}', '$.f4.f5') IS NULL AS expect_true
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：expect_true: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.3 ms。
- 返回行数：1；字段：expect_true: boolean / BOOLEAN。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0
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

### pg-json-0160-7531df7d — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
select json_extract_path_text('{"f2":{"f3":1},"f4":[0,1,2,null]}','f4','3') is null as expect_true;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_EXTRACT('{"f2":{"f3":1},"f4":[0,1,2,null]}', '$.f4[3]') IS NULL AS expect_true
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：expect_true: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：expect_true: boolean / BOOLEAN。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0
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

### pg-json-0161-635df7fb — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f4','f6'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0162-6b380766 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0163-093476ed — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','0'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0164-0923d889 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>array['f2','1'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0165-7c004789 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f4','f6'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0166-6c15e0b8 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":{"f3":1},"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0167-f3c33896 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','0'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0168-d6b16d12 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"f2":["f3",1],"f4":{"f5":99,"f6":"stringy"}}'::json#>>array['f2','1'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0169-9fd69726 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": {\"b\":{\"c\": \"foo\"}}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 14.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
doris_error_code=1105
```

### pg-json-0170-8b87c6e3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '[1,2,3]'::json #> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT(CAST('[1,2,3]' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "[1,2,3]"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
doris_error_code=1105
```

### pg-json-0171-474250d3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '"foo"'::json #> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT(CAST('"foo"' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\"foo\""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
doris_error_code=1105
```

### pg-json-0172-2baee281 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '42'::json #> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT(CAST('42' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "42"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
doris_error_code=1105
```

### pg-json-0173-95c2a2f0 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select 'null'::json #> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT(CAST('null' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "null"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = (127.0.0.1)[INVALID_ARGUMENT]Json path error: Invalid Json Path for value: {}')
doris_error_code=1105
```

### pg-json-0174-ff8d41d2 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #> array['a'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0177-0fec5401 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #> array['a','b'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0189-38c2bdc3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT_SCALAR(CAST('{"a": {"b":{"c": "foo"}}}' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "{\"a\": {\"b\":{\"c\": \"foo\"}}}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
doris_error_code=1105
```

### pg-json-0190-1355b395 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '[1,2,3]'::json #>> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT_SCALAR(CAST('[1,2,3]' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "[1,2,3]"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 19.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
doris_error_code=1105
```

### pg-json-0191-09aa37c5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '"foo"'::json #>> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT_SCALAR(CAST('"foo"' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "foo"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
doris_error_code=1105
```

### pg-json-0192-7c14c3b1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select '42'::json #>> '{}';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSONB_EXTRACT_SCALAR(CAST('42' AS JSON), '{}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "42"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSONB_EXTRACT_SCALAR'")
doris_error_code=1105
```

### pg-json-0194-013c6457 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0197-ffab593b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
select '{"a": {"b":{"c": "foo"}}}'::json #>> array['a','b'];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-json-0209-aeb87cd2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_ARRAY_ELEMENTS('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：json_array_elements: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    "true"
  ],
  [
    "[1,[2,3]]"
  ],
  [
    "null"
  ],
  [
    "{\"f1\":1,\"f2\":[7,8,9]}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_ELEMENTS'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'JSON_ARRAY_ELEMENTS'")
doris_error_code=1105
```

### pg-json-0210-22d857f7 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from json_array_elements('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_ARRAY_ELEMENTS('[1,true,[1,[2,3]],null,{"f1":1,"f2":[7,8,9]},false,"stringy"]') AS q
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：value: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ],
  [
    "true"
  ],
  [
    "[1,[2,3]]"
  ],
  [
    "null"
  ],
  [
    "{\"f1\":1,\"f2\":[7,8,9]}"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 97)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ')' expecting EQ(line 1, pos 97)\n")
doris_error_code=1105
```

### pg-json-0227-20e44f1c — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select * from json_populate_record(row('x',3,'2012-12-31 15:30:56')::jpop,'{"c":[100,200,false],"x":43.2}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORD(CAST(ROW('x', 3, '2012-12-31 15:30:56') AS jpop), '{"c":[100,200,false],"x":43.2}') AS q
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type timestamp: "[100,200,false]"`。

错误原文：

```text
invalid input syntax for type timestamp: "[100,200,false]"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 107.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type timestamp: "[100,200,false]"
source_error_code=invalid input syntax for type timestamp: "[100,200,false]"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
doris_error_code=1105
```

### pg-json-0229-42b1c6de — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"x": 43.2}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec_i_not_null), '{"x": 43.2}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`domain js_int_not_null does not allow null values`。

错误原文：

```text
domain js_int_not_null does not allow null values
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0230-f2548d30 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT i FROM json_populate_record(NULL::jsrec_i_not_null, '{"i": null}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec_i_not_null), '{"i": null}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`domain js_int_not_null does not allow null values`。

错误原文：

```text
domain js_int_not_null does not allow null values
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0233-033a5496 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": 123}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia": 123}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`expected JSON array`。

错误原文：

```text
expected JSON array
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0236-8da8813f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], 2]}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia": [[1], 2]}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`expected JSON array`。

错误原文：

```text
expected JSON array
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0237-bf9a4bfe — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia FROM json_populate_record(NULL::jsrec, '{"ia": [[1], [2, 3]]}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia": [[1], [2, 3]]}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`malformed JSON array`。

错误原文：

```text
malformed JSON array
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 40)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0240-4b741b3d — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia1 FROM json_populate_record(NULL::jsrec, '{"ia1": 123}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia1 FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia1": 123}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`expected JSON array`。

错误原文：

```text
expected JSON array
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 41)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0244-a7d926ba — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": 123}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia1d FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia1d": 123}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`expected JSON array`。

错误原文：

```text
expected JSON array
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0245-2664dfc2 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT ia1d FROM json_populate_record(NULL::jsrec, '{"ia1d": [1, "2", null, 4]}') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ia1d FROM JSON_POPULATE_RECORD(CAST(NULL AS jsrec), '{"ia1d": [1, "2", null, 4]}') AS q
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value for domain js_int_array_1d violates check constraint "js_int_array_1d_check"`。

错误原文：

```text
value for domain js_int_array_1d violates check constraint "js_int_array_1d_check"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0301-4a500f7b — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT json_populate_record(null::record, '{"x": 0, "y": 1}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORD(CAST(NULL AS record), '{"x": 0, "y": 1}')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`could not determine row type for result of json_populate_record`。

错误原文：

```text
could not determine row type for result of json_populate_record
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 9.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 41)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0302-3c69d4c1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT json_populate_record(row(1,2), '{"f1": 0, "f2": 1}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORD(ROW(1, 2), '{"f1": 0, "f2": 1}')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_populate_record: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(0,1)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 10.2 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 28)\n")
doris_error_code=1105
```

### pg-json-0303-cbcb2e92 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
  json_populate_record(null::record, '{"x": 776}') AS (x int, y int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORD(CAST(NULL AS record), '{"x": 776}') AS _t0(x INT, y INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：x: unknown / 原生类型未知, y: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "776",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 39)\n")
doris_error_code=1105
```

### pg-json-0306-96555daa — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT json_populate_record(row(1,2)::j_ordered_pair, '{"x": 1, "y": 0}');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORD(CAST(ROW(1, 2) AS j_ordered_pair), '{"x": 1, "y": 0}')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"`。

错误原文：

```text
value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 33)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
source_error_code=value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 33)\n")
doris_error_code=1105
```

### pg-json-0312-8e4d5fdb — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select * from json_populate_recordset(row('def',99,null)::jpop,'[{"c":[100,200,300],"x":43.2},{"a":{"z":true},"b":3,"c":"2012-01-20 10:42:53"}]') q;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(CAST(ROW('def', 99, NULL) AS jpop), '[{"c":[100,200,300],"x":43.2},{"a":{"z":true},"b":3,"c":"2012-01-20 10:42:53"}]') AS q
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type timestamp: "[100,200,300]"`。

错误原文：

```text
invalid input syntax for type timestamp: "[100,200,300]"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=invalid input syntax for type timestamp: "[100,200,300]"
source_error_code=invalid input syntax for type timestamp: "[100,200,300]"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-json-0318-ef190f63 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT json_populate_recordset(null::record, '[{"x": 0, "y": 1}]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[{"x": 0, "y": 1}]')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`could not determine row type for result of json_populate_recordset`。

错误原文：

```text
could not determine row type for result of json_populate_recordset
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 18.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0319-8d0c4542 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT json_populate_recordset(row(1,2), '[{"f1": 0, "f2": 1}]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORDSET(ROW(1, 2), '[{"f1": 0, "f2": 1}]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：json_populate_recordset: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "(0,1)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 12.5 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
doris_error_code=1105
```

### pg-json-0320-baa89283 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i, json_populate_recordset(row(i,50), '[{"f1":"42"},{"f2":"43"}]')
FROM (VALUES (1),(2)) v(i);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i, JSON_POPULATE_RECORDSET(ROW(i, 50), '[{"f1":"42"},{"f2":"43"}]') FROM (SELECT 1 AS i UNION ALL SELECT 2) AS v
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：i: unknown / 原生类型未知, json_populate_recordset: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "(42,50)"
  ],
  [
    "1",
    "(1,43)"
  ],
  [
    "2",
    "(42,50)"
  ],
  [
    "2",
    "(2,43)"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 13.1 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 34)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 34)\n")
doris_error_code=1105
```

### pg-json-0321-520ea364 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
  json_populate_recordset(null::record, '[{"x": 776}]') AS (x int, y int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[{"x": 776}]') AS _t0(x INT, y INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：x: unknown / 原生类型未知, y: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "776",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-json-0322-407e5563 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT json_populate_recordset(null::record, '[]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[]')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`could not determine row type for result of json_populate_recordset`。

错误原文：

```text
could not determine row type for result of json_populate_recordset
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'record' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 44)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-json-0323-4b6a9697 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT json_populate_recordset(row(1,2), '[]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORDSET(ROW(1, 2), '[]')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：0；字段：json_populate_recordset: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 10.9 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', ')', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 31)\n")
doris_error_code=1105
```

### pg-json-0325-eb75b13d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
  json_populate_recordset(null::record, '[]') AS (x int, y int);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(CAST(NULL AS record), '[]') AS _t0(x INT, y INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：0；字段：x: unknown / 原生类型未知, y: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-json-0328-37e9bde0 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT json_populate_recordset(row(1,2)::j_ordered_pair, '[{"x": 1, "y": 0}]');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT JSON_POPULATE_RECORDSET(CAST(ROW(1, 2) AS j_ordered_pair), '[{"x": 1, "y": 0}]')
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"`。

错误原文：

```text
value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.6 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 36)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
source_error_code=value for domain j_ordered_pair violates check constraint "j_ordered_pair_check"
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(ROW'(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-json-0329-6f800f54 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select * from json_populate_recordset(row(0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(ROW(CAST(0 AS INT)), '[{"a":"1","b":"2"},{"a":"3"}]') AS q(a STRING, b STRING)
```

#### 源端参考结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 0.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`function return row and query-specified return row do not match`。

错误原文：

```text
function return row and query-specified return row do not match
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.5 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=FUNCTION_NOT_FOUND
source_error_message=function return row and query-specified return row do not match
source_error_code=function return row and query-specified return row do not match
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
doris_error_code=1105
```

### pg-json-0330-2fc0f965 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select * from json_populate_recordset(row(0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(ROW(CAST(0 AS INT), CAST(0 AS INT)), '[{"a":"1","b":"2"},{"a":"3"}]') AS q(a STRING, b STRING)
```

#### 源端参考结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 0.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`function return row and query-specified return row do not match`。

错误原文：

```text
function return row and query-specified return row do not match
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 12.5 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=FUNCTION_NOT_FOUND
source_error_message=function return row and query-specified return row do not match
source_error_code=function return row and query-specified return row do not match
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
doris_error_code=1105
```

### pg-json-0331-a68233a0 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select * from json_populate_recordset(row(0::int,0::int,0::int),'[{"a":"1","b":"2"},{"a":"3"}]') q (a text, b text);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM JSON_POPULATE_RECORDSET(ROW(CAST(0 AS INT), CAST(0 AS INT), CAST(0 AS INT)), '[{"a":"1","b":"2"},{"a":"3"}]') AS q(a STRING, b STRING)
```

#### 源端参考结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 0.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`function return row and query-specified return row do not match`。

错误原文：

```text
function return row and query-specified return row do not match
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=FUNCTION_NOT_FOUND
source_error_message=function return row and query-specified return row do not match
source_error_code=function return row and query-specified return row do not match
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'ROW' expecting {')', '[', '{', '}', 'ACTIONS', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXPIRED', 'EXTERNAL', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LESS', 'LEVEL', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '-', 'MOD', '/*+', '*/', '/*', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 38)\n")
doris_error_code=1105
```
