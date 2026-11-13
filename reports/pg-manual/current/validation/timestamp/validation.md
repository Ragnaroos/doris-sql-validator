# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:21.372080+00:00 至 2026-11-11T09:40:21.759203+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/timestamp.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**25**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/25 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/10 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**15**；不计入上述成功匹配分子。
- 需要分析的查询：**25**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**17**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 8 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 11 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 5 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 25 条只读查询、跳过 147 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–5 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 16–16 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 18–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 20–20 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 28–28 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 13 | 30–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 37–37 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 39–39 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 24 | 47–48 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 25 | 49–49 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 26 | 50–50 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 28 | 54–55 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 29 | 57–58 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 30 | 59–59 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 31 | 60–60 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 32 | 61–61 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 33 | 62–62 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 34 | 64–65 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 35 | 66–66 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 36 | 67–67 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 37 | 68–68 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 38 | 69–69 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 39 | 70–70 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 40 | 71–71 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 41 | 72–72 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 42 | 74–75 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 43 | 76–76 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 44 | 77–77 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 45 | 78–78 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 46 | 79–79 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 47 | 81–82 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 48 | 83–83 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 49 | 84–84 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 50 | 85–85 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 51 | 86–86 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 52 | 87–87 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 53 | 88–88 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 54 | 89–89 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 55 | 90–90 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 56 | 91–91 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 57 | 92–92 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 58 | 93–93 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 59 | 94–94 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 60 | 95–95 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 61 | 96–97 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 67 | 106–107 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 68 | 109–109 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 69 | 110–110 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 70 | 111–111 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 71 | 112–112 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 72 | 113–113 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 73 | 114–114 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 115–115 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 75 | 117–117 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 118–118 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 77 | 119–119 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 78 | 120–120 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 79 | 121–121 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 80 | 122–122 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 81 | 123–123 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 82 | 124–124 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 83 | 125–125 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 84 | 127–127 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 85 | 128–128 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 86 | 129–129 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 87 | 130–130 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 88 | 131–131 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 89 | 132–132 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 90 | 133–133 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 91 | 134–134 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 92 | 135–135 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 93 | 136–136 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 94 | 137–137 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 95 | 138–138 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 96 | 139–139 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 97 | 140–140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 98 | 141–141 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 99 | 143–144 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 100 | 145–145 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 22–22 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 9 | 23–23 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 10 | 24–24 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 14 | 34–34 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 17 | 38–38 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 40–40 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 41–41 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 42–42 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 62 | 99–100 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 63 | 101–101 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 64 | 102–102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 65 | 103–103 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 66 | 104–104 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 147–147 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 149–150 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 104 | 151–152 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 153–157 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 159–160 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 162–163 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 165–166 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 168–169 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 111 | 171–172 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 174–175 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 113 | 177–177 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 114 | 178–178 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 253–270 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 123 | 272–273 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 275–276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 291–291 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 132 | 293–297 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 133 | 299–304 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 134 | 306–309 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 135 | 311–315 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 136 | 317–323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 137 | 325–333 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 141 | 341–342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 143 | 345–347 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 349–350 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 352–353 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 146 | 355–356 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 147 | 358–359 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 148 | 361–362 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 149 | 364–365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 150 | 367–368 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 151 | 370–371 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 152 | 373–374 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 153 | 376–377 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 156 | 393–394 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 157 | 395–395 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 159 | 399–402 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 160 | 403–407 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 163 | 413–413 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 164 | 416–417 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 165 | 418–418 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 166 | 419–419 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 167 | 420–420 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 168 | 421–421 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 169 | 422–422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 170 | 424–425 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 171 | 426–426 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 172 | 427–427 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 173 | 428–428 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 174 | 429–429 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 430–430 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 176 | 432–433 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 434–434 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/timestamp.out`；SHA-256（文件内容指纹）：`b08dfd20e0de3a6a13ba1cedcf20b90198bc72d51d9cd00b581ca69b09668e36`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 25/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 25/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 10/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 10/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 10/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/25 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-timestamp-0027-1be25b6e` | SELECT timestamp 'infinity' = timestamp '+infinity' AS t; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamp-0103-b15d0320` | SELECT '4714-11-23 23:59:59 BC'::timestamp; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0105-fb1ad90f` | SELECT '294277-01-01 00:00:00'::timestamp; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0115-612735d5` | SELECT date_trunc( 'timezone', timestamp '2004-02-29 15:44:17.71393' ) AS notsupp_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0116-868084d4` | SELECT date_trunc( 'timezone', timestamp 'infinity' ) AS notsupp_inf_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0117-374aee7b` | SELECT date_trunc( 'ago', timestamp 'infinity' ) AS invalid_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0118-05aabd49` | SELECT   str,   interval,   date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2001-01-01') AS equal FROM (   VALUES   ('week', '7 d'),   ('day', '1 d'),   ('hour', '1 h'),   ('minute', '1 m'),   ('second', '1 s'),   ('millisecond', '1 ms'),   ('microsecond', '1 us') ) intervals (str, interval), (VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0119-8bf34e86` | SELECT   str,   interval,   date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2000-01-01 BC') AS equal FROM (   VALUES   ('week', '7 d'),   ('day', '1 d'),   ('hour', '1 h'),   ('minute', '1 m'),   ('second', '1 s'),   ('millisecond', '1 ms'),   ('microsecond', '1 us') ) intervals (str, interval), (VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0120-0f80102f` | SELECT   str,   interval,   date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2020-03-02') AS equal FROM (   VALUES   ('week', '7 d'),   ('day', '1 d'),   ('hour', '1 h'),   ('minute', '1 m'),   ('second', '1 s'),   ('millisecond', '1 ms'),   ('microsecond', '1 us') ) intervals (str, interval), (VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0121-e7cf5cac` | SELECT   str,   interval,   date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '0055-06-17 BC') AS equal FROM (   VALUES   ('week', '7 d'),   ('day', '1 d'),   ('hour', '1 h'),   ('minute', '1 m'),   ('second', '1 s'),   ('millisecond', '1 ms'),   ('microsecond', '1 us') ) intervals (str, interval), (VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0125-8dbc1989` | SELECT date_bin('5 months'::interval, timestamp '2020-02-01 01:01:01', timestamp '2001-01-01'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0126-5ab4dd7e` | SELECT date_bin('5 years'::interval,  timestamp '2020-02-01 01:01:01', timestamp '2001-01-01'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0127-14367d1f` | SELECT date_bin('0 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0128-5938d3b4` | SELECT date_bin('-2 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0129-490e00ba` | select date_bin('15 minutes'::interval, timestamp '294276-12-30', timestamp '4000-12-20 BC'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0130-3e4d2c86` | select date_bin('200000000 days'::interval, '2024-02-01'::timestamp, '2024-01-01'::timestamp); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0138-6926e893` | SELECT date_part('epoch', '294270-01-01 00:00:00'::timestamp); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamp-0139-6926e893` | SELECT extract(epoch from '294270-01-01 00:00:00'::timestamp); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamp-0140-b552f818` | SELECT extract(epoch from '5000-01-01 00:00:00'::timestamp); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamp-0142-dd28e983` | SELECT timestamp '294276-12-31 23:59:59' - timestamp '1999-12-23 19:59:04.224192' AS overflows; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0154-25ff4879` | SELECT to_char(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS US')    FROM (VALUES        ('2018-11-02 12:34:56'::timestamp),        ('2018-11-02 12:34:56.78'),        ('2018-11-02 12:34:56.78901'),        ('2018-11-02 12:34:56.78901234')    ) d(d); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamp-0155-9edb681d` | SELECT i,        to_char(i * interval '1mon', 'rm'),        to_char(i * interval '1mon', 'RM')     FROM generate_series(-13, 13) i; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamp-0158-b3cd5d0a` | select make_timestamp(0, 7, 15, 12, 30, 15); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-timestamp-0161-66dc7cce` | select * from generate_series('2020-01-01 00:00'::timestamp,                               '2020-01-02 03:00'::timestamp,                               '0 hour'::interval); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamp-0162-9c7414dd` | select generate_series(timestamp '1995-08-06 12:12:12', timestamp '1996-08-06 12:12:12', interval 'infinity'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |

## 4. 不匹配、执行失败及负向错误详情

### pg-timestamp-0027-1be25b6e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT timestamp 'infinity' = timestamp '+infinity' AS t;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('infinity' AS DATETIME) = CAST('+infinity' AS DATETIME) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：t: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.4 ms。
- 返回行数：1；字段：t: boolean / BOOLEAN。
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

### pg-timestamp-0103-b15d0320 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '4714-11-23 23:59:59 BC'::timestamp;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('4714-11-23 23:59:59 BC' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamp out of range: "4714-11-23 23:59:59 BC"`。

错误原文：

```text
timestamp out of range: "4714-11-23 23:59:59 BC"
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.0 ms。
- 返回行数：1；字段：CAST('4714-11-23 23:59:59 BC' AS DATETIME): timestamp / DATETIME。
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
source_error_category=EXECUTION_ERROR
source_error_message=timestamp out of range: "4714-11-23 23:59:59 BC"
source_error_code=timestamp out of range: "4714-11-23 23:59:59 BC"
```

### pg-timestamp-0105-fb1ad90f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '294277-01-01 00:00:00'::timestamp;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('294277-01-01 00:00:00' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamp out of range: "294277-01-01 00:00:00"`。

错误原文：

```text
timestamp out of range: "294277-01-01 00:00:00"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.3 ms。
- 返回行数：1；字段：CAST('294277-01-01 00:00:00' AS DATETIME): timestamp / DATETIME。
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
source_error_category=EXECUTION_ERROR
source_error_message=timestamp out of range: "294277-01-01 00:00:00"
source_error_code=timestamp out of range: "294277-01-01 00:00:00"
```

### pg-timestamp-0115-612735d5 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'timezone', timestamp '2004-02-29 15:44:17.71393' ) AS notsupp_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('2004-02-29 15:44:17.71393' AS DATETIME), 'TIMEZONE') AS notsupp_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type timestamp without time zone`。

错误原文：

```text
unit "timezone" not supported for type timestamp without time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year|quarter|month|week|day|hour|minute|second')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0116-868084d4 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'timezone', timestamp 'infinity' ) AS notsupp_inf_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'TIMEZONE') AS notsupp_inf_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type timestamp without time zone`。

错误原文：

```text
unit "timezone" not supported for type timestamp without time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year|quarter|month|week|day|hour|minute|second')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0117-374aee7b — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'ago', timestamp 'infinity' ) AS invalid_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'AGO') AS invalid_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "ago" not recognized for type timestamp without time zone`。

错误原文：

```text
unit "ago" not recognized for type timestamp without time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = date_trunc function time unit param only support argument is year|quarter|month|week|day|hour|minute|second')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0118-05aabd49 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2001-01-01') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2001-01-01' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393' AS DATETIME) AS ts) AS ts
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：str: unknown / 原生类型未知, interval: unknown / 原生类型未知, equal: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "week",
    "7 d",
    "t"
  ],
  [
    "day",
    "1 d",
    "t"
  ],
  [
    "hour",
    "1 h",
    "t"
  ],
  [
    "minute",
    "1 m",
    "t"
  ],
  [
    "second",
    "1 s",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
doris_error_code=1105
```

### pg-timestamp-0119-8bf34e86 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2000-01-01 BC') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2000-01-01 BC' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('0055-6-10 15:44:17.71393 BC' AS DATETIME) AS ts) AS ts
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：str: unknown / 原生类型未知, interval: unknown / 原生类型未知, equal: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "week",
    "7 d",
    "t"
  ],
  [
    "day",
    "1 d",
    "t"
  ],
  [
    "hour",
    "1 h",
    "t"
  ],
  [
    "minute",
    "1 m",
    "t"
  ],
  [
    "second",
    "1 s",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
doris_error_code=1105
```

### pg-timestamp-0120-0f80102f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '2020-03-02') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '2020-02-29 15:44:17.71393')) ts (ts);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2020-03-02' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393' AS DATETIME) AS ts) AS ts
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：str: unknown / 原生类型未知, interval: unknown / 原生类型未知, equal: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "week",
    "7 d",
    "t"
  ],
  [
    "day",
    "1 d",
    "t"
  ],
  [
    "hour",
    "1 h",
    "t"
  ],
  [
    "minute",
    "1 m",
    "t"
  ],
  [
    "second",
    "1 s",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
doris_error_code=1105
```

### pg-timestamp-0121-e7cf5cac — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
  str,
  interval,
  date_trunc(str, ts) = date_bin(interval::interval, ts, timestamp '0055-06-17 BC') AS equal
FROM (
  VALUES
  ('week', '7 d'),
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamp '0055-6-10 15:44:17.71393 BC')) ts (ts);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('0055-06-17 BC' AS DATETIME)) AS equal FROM (SELECT 'week' AS str, '7 d' AS `interval` UNION ALL SELECT 'day', '1 d' UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('0055-6-10 15:44:17.71393 BC' AS DATETIME) AS ts) AS ts
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：str: unknown / 原生类型未知, interval: unknown / 原生类型未知, equal: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "week",
    "7 d",
    "t"
  ],
  [
    "day",
    "1 d",
    "t"
  ],
  [
    "hour",
    "1 h",
    "t"
  ],
  [
    "minute",
    "1 m",
    "t"
  ],
  [
    "second",
    "1 s",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 76)\n")
doris_error_code=1105
```

### pg-timestamp-0125-8dbc1989 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('5 months'::interval, timestamp '2020-02-01 01:01:01', timestamp '2001-01-01');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('5 months' AS INTERVAL), CAST('2020-02-01 01:01:01' AS DATETIME), CAST('2001-01-01' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamps cannot be binned into intervals containing months or years`。

错误原文：

```text
timestamps cannot be binned into intervals containing months or years
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 35)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0126-5ab4dd7e — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('5 years'::interval,  timestamp '2020-02-01 01:01:01', timestamp '2001-01-01');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('5 years' AS INTERVAL), CAST('2020-02-01 01:01:01' AS DATETIME), CAST('2001-01-01' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamps cannot be binned into intervals containing months or years`。

错误原文：

```text
timestamps cannot be binned into intervals containing months or years
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 34)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0127-14367d1f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('0 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('0 days' AS INTERVAL), CAST('1970-01-01 01:00:00' AS DATETIME), CAST('1970-01-01 00:00:00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`stride must be greater than zero`。

错误原文：

```text
stride must be greater than zero
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 33)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0128-5938d3b4 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('-2 days'::interval, timestamp '1970-01-01 01:00:00' , timestamp '1970-01-01 00:00:00');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('-2 days' AS INTERVAL), CAST('1970-01-01 01:00:00' AS DATETIME), CAST('1970-01-01 00:00:00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`stride must be greater than zero`。

错误原文：

```text
stride must be greater than zero
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 34)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0129-490e00ba — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select date_bin('15 minutes'::interval, timestamp '294276-12-30', timestamp '4000-12-20 BC');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('15 minutes' AS INTERVAL), CAST('294276-12-30' AS DATETIME), CAST('4000-12-20 BC' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`interval out of range`。

错误原文：

```text
interval out of range
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 37)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0130-3e4d2c86 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select date_bin('200000000 days'::interval, '2024-02-01'::timestamp, '2024-01-01'::timestamp);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('200000000 days' AS INTERVAL), CAST('2024-02-01' AS DATETIME), CAST('2024-01-01' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`interval out of range`。

错误原文：

```text
interval out of range
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'INTERVAL' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 41)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0138-6926e893 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT date_part('epoch', '294270-01-01 00:00:00'::timestamp);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：date_part: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9224097091200"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.3 ms。
- 返回行数：1；字段：UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME)): decimal / DECIMAL。
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

### pg-timestamp-0139-6926e893 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT extract(epoch from '294270-01-01 00:00:00'::timestamp);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9224097091200.000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.9 ms。
- 返回行数：1；字段：UNIX_TIMESTAMP(CAST('294270-01-01 00:00:00' AS DATETIME)): decimal / DECIMAL。
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

### pg-timestamp-0140-b552f818 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT extract(epoch from '5000-01-01 00:00:00'::timestamp);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT UNIX_TIMESTAMP(CAST('5000-01-01 00:00:00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "95617584000.000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：UNIX_TIMESTAMP(CAST('5000-01-01 00:00:00' AS DATETIME)): decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "95617584000"
    }
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

### pg-timestamp-0142-dd28e983 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT timestamp '294276-12-31 23:59:59' - timestamp '1999-12-23 19:59:04.224192' AS overflows;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('294276-12-31 23:59:59' AS DATETIME) - CAST('1999-12-23 19:59:04.224192' AS DATETIME) AS overflows
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`interval out of range`。

错误原文：

```text
interval out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.3 ms。
- 返回行数：1；字段：overflows: integer / BIGINT。
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
source_error_category=EXECUTION_ERROR
source_error_message=interval out of range
source_error_code=interval out of range
```

### pg-timestamp-0154-25ff4879 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT to_char(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS US')
   FROM (VALUES
       ('2018-11-02 12:34:56'::timestamp),
       ('2018-11-02 12:34:56.78'),
       ('2018-11-02 12:34:56.78901'),
       ('2018-11-02 12:34:56.78901234')
   ) d(d);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_FORMAT(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS %f') FROM (SELECT CAST('2018-11-02 12:34:56' AS DATETIME) AS d UNION ALL SELECT '2018-11-02 12:34:56.78' UNION ALL SELECT '2018-11-02 12:34:56.78901' UNION ALL SELECT '2018-11-02 12:34:56.78901234') AS d
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：to_char: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0 00 000 0000 00000 000000  0 00 000 0000 00000 000000  000 000000"
  ],
  [
    "7 78 780 7800 78000 780000  7 78 780 7800 78000 780000  780 780000"
  ],
  [
    "7 78 789 7890 78901 789010  7 78 789 7890 78901 789010  789 789010"
  ],
  [
    "7 78 789 7890 78901 789012  7 78 789 7890 78901 789012  789 789012"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.3 ms。
- 返回行数：4；字段：DATE_FORMAT(d, 'FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS %f'): string / STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 000000"
  ],
  [
    "FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 780000"
  ],
  [
    "FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 789010"
  ],
  [
    "FF1 FF2 FF3 FF4 FF5 FF6  ff1 ff2 ff3 ff4 ff5 ff6  MS 789012"
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

### pg-timestamp-0155-9edb681d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i,
       to_char(i * interval '1mon', 'rm'),
       to_char(i * interval '1mon', 'RM')
    FROM generate_series(-13, 13) i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i, DATE_FORMAT(i * INTERVAL '1' MON, 'rm'), DATE_FORMAT(i * INTERVAL '1' MON, 'RM') FROM GENERATE_SERIES(-13, 13) AS i
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：27；字段：i: unknown / 原生类型未知, to_char: unknown / 原生类型未知, to_char: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-13",
    "xii",
    "XII"
  ],
  [
    "-12",
    "i",
    "I"
  ],
  [
    "-11",
    "ii",
    "II"
  ],
  [
    "-10",
    "iii",
    "III"
  ],
  [
    "-9",
    "iv",
    "IV"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MON' expecting {'.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DIV', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'NOT', 'OR', 'QUARTER', 'REGEXP', 'RLIKE', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'XOR', 'YEAR', 'YEAR_MONTH', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 39)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'MON' expecting {'.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DIV', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'NOT', 'OR', 'QUARTER', 'REGEXP', 'RLIKE', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'XOR', 'YEAR', 'YEAR_MONTH', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 39)\n")
doris_error_code=1105
```

### pg-timestamp-0158-b3cd5d0a — 两端均报错，但错误类别不同

#### 源 SQL

```sql
select make_timestamp(0, 7, 15, 12, 30, 15);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TIMESTAMP_FROM_PARTS(0, 7, 15, 12, 30, 15)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`date field value out of range: 0-07-15`。

错误原文：

```text
date field value out of range: 0-07-15
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'TIMESTAMP_FROM_PARTS'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=date field value out of range: 0-07-15
source_error_code=date field value out of range: 0-07-15
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'TIMESTAMP_FROM_PARTS'")
doris_error_code=1105
```

### pg-timestamp-0161-66dc7cce — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select * from generate_series('2020-01-01 00:00'::timestamp,
                              '2020-01-02 03:00'::timestamp,
                              '0 hour'::interval);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM GENERATE_SERIES(CAST('2020-01-01 00:00' AS DATETIME), CAST('2020-01-02 03:00' AS DATETIME), CAST('0 hour' AS INTERVAL))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`step size cannot equal zero`。

错误原文：

```text
step size cannot equal zero
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 16.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting EQ(line 1, pos 34)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-timestamp-0162-9c7414dd — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select generate_series(timestamp '1995-08-06 12:12:12', timestamp '1996-08-06 12:12:12', interval 'infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT UNNEST(GENERATE_SERIES(CAST('1995-08-06 12:12:12' AS DATETIME), CAST('1996-08-06 12:12:12' AS DATETIME), INTERVAL infinity))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`step size cannot be infinite`。

错误原文：

```text
step size cannot be infinite
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmissing {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'} at ')'(line 1, pos 129)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```
