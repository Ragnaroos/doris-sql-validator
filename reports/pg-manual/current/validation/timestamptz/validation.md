# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:22.121320+00:00 至 2026-11-11T09:40:22.341069+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/timestamptz.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**15**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/15 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/2 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**12**；不计入上述成功匹配分子。
- 需要分析的查询：**15**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**1**；源参考结果不可用：**0**；Doris 执行失败：**9**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 5 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 8 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 1 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 1 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 15 条只读查询、跳过 376 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–5 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 16–16 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 18–18 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 19–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 14 | 29–29 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 15 | 31–34 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 38–38 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 40–40 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 26 | 48–49 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 27 | 50–50 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 28 | 51–51 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 30 | 55–56 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 31 | 58–59 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 32 | 60–60 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 33 | 61–61 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 34 | 62–62 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 35 | 63–63 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 36 | 65–66 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 37 | 67–67 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 38 | 68–68 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 39 | 69–69 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 40 | 70–70 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 41 | 71–71 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 42 | 72–72 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 43 | 73–73 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 44 | 75–76 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 45 | 77–77 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 46 | 78–78 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 47 | 79–79 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 48 | 80–80 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 49 | 82–83 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 50 | 84–84 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 51 | 85–85 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 52 | 86–86 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 53 | 87–87 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 54 | 88–88 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 55 | 89–89 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 56 | 90–90 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 57 | 91–91 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 58 | 92–92 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 59 | 93–93 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 60 | 94–94 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 61 | 95–95 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 62 | 97–98 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 64 | 100–100 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 66 | 102–102 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 115–115 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 77 | 118–119 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 80 | 122–123 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 84 | 127–127 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 90 | 136–137 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 91 | 139–139 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 92 | 140–140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 93 | 141–141 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 94 | 142–142 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 95 | 143–143 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 96 | 144–144 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 97 | 145–145 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 98 | 147–147 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 99 | 148–148 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 100 | 149–149 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 101 | 150–150 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 102 | 151–151 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 103 | 152–152 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 104 | 153–153 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 105 | 154–154 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 106 | 155–155 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 107 | 157–157 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 108 | 158–158 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 109 | 159–159 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 110 | 160–160 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 111 | 161–161 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 112 | 162–162 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 113 | 163–163 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 114 | 164–164 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 115 | 165–165 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 116 | 166–166 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 117 | 167–167 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 118 | 168–168 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 119 | 169–169 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 120 | 170–170 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 121 | 171–171 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 122 | 173–174 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 123 | 175–175 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 191 | 387–388 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 193 | 390–390 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 195 | 392–392 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 197 | 394–394 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 199 | 396–396 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 201 | 398–398 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 203 | 400–400 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 205 | 402–402 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 207 | 404–404 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 209 | 406–406 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 210 | 408–409 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 212 | 411–411 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 214 | 413–413 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 216 | 415–415 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 218 | 417–417 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 220 | 419–419 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 222 | 421–421 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 224 | 423–423 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 226 | 425–425 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 228 | 427–427 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 229 | 430–430 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 230 | 432–433 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 231 | 434–434 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 232 | 435–435 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 233 | 436–436 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 234 | 437–437 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 235 | 438–438 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 237 | 441–442 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 238 | 444–445 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 257 | 482–482 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 263 | 500–501 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 269 | 517–517 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 270 | 519–525 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 336 | 606–606 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 349 | 622–622 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 375 | 656–656 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 378 | 659–659 | 跳过非查询；类型 `set` | Expected one read-only Query, got Command |
| 381 | 662–662 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 382 | 663–667 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 385 | 671–672 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 387 | 675–678 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 388 | 679–679 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 389 | 680–681 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 8 | 21–21 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 9 | 22–22 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 10 | 23–23 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 11 | 24–24 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 12 | 25–25 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 35–35 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 39–39 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 41–41 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 22 | 42–42 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 23 | 43–43 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 63 | 99–99 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 65 | 101–101 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 68 | 105–106 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 69 | 106–107 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 107–109 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 71 | 109–110 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 72 | 110–113 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 114–114 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 75 | 116–116 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 117–117 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 79 | 120–122 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 124–124 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 82 | 125–125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 83 | 126–126 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 85 | 129–130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 86 | 131–131 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 87 | 132–132 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 88 | 133–133 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 89 | 134–134 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 177–179 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 180–180 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 181–181 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 182–182 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 128 | 183–183 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 185–185 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 130 | 187–188 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 131 | 189–189 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 132 | 190–190 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 134 | 191–192 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 135 | 193–193 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 138 | 195–199 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 139 | 201–202 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 140 | 204–205 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 141 | 207–208 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 142 | 210–211 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 143 | 213–214 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 216–217 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 219–219 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 146 | 220–220 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 150 | 225–225 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 151 | 225–226 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 152 | 226–227 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 154 | 229–229 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 157 | 248–265 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 158 | 267–268 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 159 | 270–271 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 163 | 280–281 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 164 | 283–284 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 165 | 285–285 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 166 | 286–286 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 167 | 288–291 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 168 | 293–298 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 169 | 300–303 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 170 | 305–309 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 171 | 311–317 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 172 | 319–323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 173 | 325–333 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 174 | 335–336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 337–337 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 176 | 338–339 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 341–342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 178 | 343–343 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 179 | 345–347 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 180 | 349–350 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 181 | 352–353 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 355–356 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 183 | 358–359 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 184 | 361–362 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 185 | 364–365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 186 | 367–368 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 187 | 370–371 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 188 | 373–374 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 189 | 376–377 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 190 | 379–385 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 192 | 389–389 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 194 | 391–391 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 393–393 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 198 | 395–395 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 200 | 397–397 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 202 | 399–399 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 204 | 401–401 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 403–403 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 405–405 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 211 | 410–410 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 213 | 412–412 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 215 | 414–414 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 217 | 416–416 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 219 | 418–418 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 221 | 420–420 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 223 | 422–422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 225 | 424–424 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 227 | 426–426 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 236 | 439–440 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 239 | 447–448 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 240 | 449–449 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 241 | 450–450 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 242 | 451–456 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 243 | 458–459 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 244 | 460–460 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 245 | 461–461 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 246 | 463–464 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 247 | 466–467 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 248 | 468–468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 249 | 469–469 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 250 | 470–470 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 251 | 471–471 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 252 | 472–472 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 253 | 474–475 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 254 | 476–476 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 255 | 477–477 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 256 | 479–480 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 258 | 484–487 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 259 | 488–492 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 260 | 493–496 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 261 | 497–497 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 262 | 498–498 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 264 | 503–504 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 265 | 505–507 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 266 | 508–509 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 267 | 510–512 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 268 | 513–516 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 271 | 527–527 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 272 | 528–528 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 273 | 529–529 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 274 | 530–530 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 275 | 531–531 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 276 | 532–532 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 277 | 533–533 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 278 | 534–534 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 279 | 535–535 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 280 | 537–537 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 281 | 538–538 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 282 | 539–539 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 283 | 540–540 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 284 | 541–541 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 285 | 542–542 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 286 | 543–543 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 287 | 544–544 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 288 | 545–545 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 289 | 547–547 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 290 | 548–548 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 291 | 549–549 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 292 | 550–550 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 293 | 551–551 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 294 | 553–553 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 295 | 554–554 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 296 | 555–555 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 297 | 556–556 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 298 | 557–557 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 299 | 559–559 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 300 | 560–560 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 301 | 561–561 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 302 | 562–562 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 303 | 563–563 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 304 | 564–564 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 305 | 565–565 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 306 | 566–566 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 307 | 567–567 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 308 | 569–569 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 309 | 570–570 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 310 | 571–571 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 311 | 572–572 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 312 | 573–573 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 313 | 574–574 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 314 | 575–575 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 315 | 576–576 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 316 | 577–577 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 317 | 579–579 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 318 | 580–580 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 319 | 581–581 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 320 | 582–582 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 321 | 583–583 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 322 | 585–585 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 323 | 586–586 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 324 | 587–587 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 325 | 588–588 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 326 | 589–589 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 327 | 591–591 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 328 | 592–592 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 329 | 594–594 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 330 | 594–595 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 331 | 595–596 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 332 | 596–598 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 333 | 598–601 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 334 | 602–602 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 335 | 603–603 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 337 | 608–608 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 338 | 609–609 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 339 | 610–610 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 340 | 611–611 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 341 | 612–612 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 342 | 613–613 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 343 | 614–614 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 344 | 616–616 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 345 | 617–617 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 346 | 618–618 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 347 | 619–619 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 348 | 620–620 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 350 | 624–624 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 351 | 625–625 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 352 | 626–626 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 353 | 627–627 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 354 | 628–628 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 355 | 629–629 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 356 | 630–630 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 357 | 632–632 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 358 | 633–633 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 359 | 634–634 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 360 | 635–635 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 361 | 636–636 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 362 | 638–638 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 363 | 639–639 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 364 | 640–640 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 365 | 641–641 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 366 | 642–642 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 367 | 643–643 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 368 | 644–644 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 369 | 646–646 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 370 | 647–647 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 371 | 648–648 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 372 | 649–649 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 373 | 650–650 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 390 | 682–682 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 391 | 684–685 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 392 | 686–686 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 393 | 687–687 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 394 | 688–688 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 395 | 689–689 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 396 | 690–690 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 397 | 692–693 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 398 | 694–694 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 399 | 695–695 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 400 | 696–696 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 401 | 697–697 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 402 | 698–698 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 403 | 700–701 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 404 | 702–702 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/timestamptz.out`；SHA-256（文件内容指纹）：`e6f104c2b3a5ac46a7c2b0a41d5ce79b3803b2ceb91fc66662c887a7f6667b87`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 14/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 14/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 2/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 2/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 2/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/14 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-timestamptz-0029-d176b7af` | SELECT timestamptz 'infinity' = timestamptz '+infinity' AS t; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-timestamptz-0067-004efc58` | SELECT '19970710 173201' AT TIME ZONE 'America/Does_not_exist'; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-timestamptz-0078-463ca246` | SELECT 'Jan 01 00:00:00 2024 LMT'::timestamptz; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamptz-0133-f2a3bb29` | SELECT '4714-11-23 23:59:59+00 BC'::timestamptz; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamptz-0136-d60d38d1` | SELECT '294277-01-01 00:00:00+00'::timestamptz; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamptz-0137-811b7b6e` | SELECT '294277-12-31 16:00:00-08'::timestamptz; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamptz-0147-1d73992e` | SELECT date_trunc( 'timezone', timestamp with time zone '2004-02-29 15:44:17.71393' ) AS notsupp_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0148-226a4a04` | SELECT date_trunc( 'timezone', timestamp with time zone 'infinity' ) AS notsupp_inf_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0149-fd702113` | SELECT date_trunc( 'ago', timestamp with time zone 'infinity' ) AS invalid_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0153-e98782eb` | SELECT date_trunc('timezone', timestamp with time zone 'infinity', 'GMT') AS notsupp_zone_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0155-a8efda7d` | SELECT date_trunc('ago', timestamp with time zone 'infinity', 'GMT') AS invalid_zone_trunc; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0156-7733d5eb` | SELECT   str,   interval,   date_trunc(str, ts, 'Australia/Sydney') = date_bin(interval::interval, ts, timestamp with time zone '2001-01-01+11') AS equal FROM (   VALUES   ('day', '1 d'),   ('hour', '1 h'),   ('minute', '1 m'),   ('second', '1 s'),   ('millisecond', '1 ms'),   ('microsecond', '1 us') ) intervals (str, interval), (VALUES (timestamptz '2020-02-29 15:44:17.71393+00')) ts (ts); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-timestamptz-0160-7802bb90` | SELECT date_bin('5 months'::interval, timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0161-856f8667` | SELECT date_bin('5 years'::interval,  timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-timestamptz-0162-e22468e0` | SELECT date_bin('0 days'::interval, timestamp with time zone '1970-01-01 01:00:00+00' , timestamp with time zone '1970-01-01 00:00:00+00'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |

## 4. 不匹配、执行失败及负向错误详情

### pg-timestamptz-0029-d176b7af — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT timestamptz 'infinity' = timestamptz '+infinity' AS t;
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

- 执行状态：成功；耗时 19.7 ms。
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

### pg-timestamptz-0067-004efc58 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT '19970710 173201' AT TIME ZONE 'America/Does_not_exist';
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: AT TIME ZONE is not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-timestamptz-0078-463ca246 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'Jan 01 00:00:00 2024 LMT'::timestamptz;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('Jan 01 00:00:00 2024 LMT' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type timestamp with time zone: "Jan 01 00:00:00 2024 LMT"`。

错误原文：

```text
invalid input syntax for type timestamp with time zone: "Jan 01 00:00:00 2024 LMT"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.0 ms。
- 返回行数：1；字段：CAST('Jan 01 00:00:00 2024 LMT' AS DATETIME): timestamp / DATETIME。
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
source_error_message=invalid input syntax for type timestamp with time zone: "Jan 01 00:00:00 2024 LMT"
source_error_code=invalid input syntax for type timestamp with time zone: "Jan 01 00:00:00 2024 LMT"
```

### pg-timestamptz-0133-f2a3bb29 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '4714-11-23 23:59:59+00 BC'::timestamptz;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('4714-11-23 23:59:59+00 BC' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamp out of range: "4714-11-23 23:59:59+00 BC"`。

错误原文：

```text
timestamp out of range: "4714-11-23 23:59:59+00 BC"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CAST('4714-11-23 23:59:59+00 BC' AS DATETIME): timestamp / DATETIME。
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
source_error_message=timestamp out of range: "4714-11-23 23:59:59+00 BC"
source_error_code=timestamp out of range: "4714-11-23 23:59:59+00 BC"
```

### pg-timestamptz-0136-d60d38d1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '294277-01-01 00:00:00+00'::timestamptz;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('294277-01-01 00:00:00+00' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamp out of range: "294277-01-01 00:00:00+00"`。

错误原文：

```text
timestamp out of range: "294277-01-01 00:00:00+00"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CAST('294277-01-01 00:00:00+00' AS DATETIME): timestamp / DATETIME。
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
source_error_message=timestamp out of range: "294277-01-01 00:00:00+00"
source_error_code=timestamp out of range: "294277-01-01 00:00:00+00"
```

### pg-timestamptz-0137-811b7b6e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '294277-12-31 16:00:00-08'::timestamptz;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('294277-12-31 16:00:00-08' AS DATETIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamp out of range: "294277-12-31 16:00:00-08"`。

错误原文：

```text
timestamp out of range: "294277-12-31 16:00:00-08"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.3 ms。
- 返回行数：1；字段：CAST('294277-12-31 16:00:00-08' AS DATETIME): timestamp / DATETIME。
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
source_error_message=timestamp out of range: "294277-12-31 16:00:00-08"
source_error_code=timestamp out of range: "294277-12-31 16:00:00-08"
```

### pg-timestamptz-0147-1d73992e — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'timezone', timestamp with time zone '2004-02-29 15:44:17.71393' ) AS notsupp_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('2004-02-29 15:44:17.71393' AS DATETIME), 'TIMEZONE') AS notsupp_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type timestamp with time zone`。

错误原文：

```text
unit "timezone" not supported for type timestamp with time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
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

### pg-timestamptz-0148-226a4a04 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'timezone', timestamp with time zone 'infinity' ) AS notsupp_inf_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'TIMEZONE') AS notsupp_inf_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type timestamp with time zone`。

错误原文：

```text
unit "timezone" not supported for type timestamp with time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
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

### pg-timestamptz-0149-fd702113 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc( 'ago', timestamp with time zone 'infinity' ) AS invalid_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'AGO') AS invalid_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "ago" not recognized for type timestamp with time zone`。

错误原文：

```text
unit "ago" not recognized for type timestamp with time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 14.4 ms。
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

### pg-timestamptz-0153-e98782eb — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc('timezone', timestamp with time zone 'infinity', 'GMT') AS notsupp_zone_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'TIMEZONE') AS notsupp_zone_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type timestamp with time zone`。

错误原文：

```text
unit "timezone" not supported for type timestamp with time zone
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

### pg-timestamptz-0155-a8efda7d — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_trunc('ago', timestamp with time zone 'infinity', 'GMT') AS invalid_zone_trunc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_TRUNC(CAST('infinity' AS DATETIME), 'AGO') AS invalid_zone_trunc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "ago" not recognized for type timestamp with time zone`。

错误原文：

```text
unit "ago" not recognized for type timestamp with time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
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

### pg-timestamptz-0156-7733d5eb — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT
  str,
  interval,
  date_trunc(str, ts, 'Australia/Sydney') = date_bin(interval::interval, ts, timestamp with time zone '2001-01-01+11') AS equal
FROM (
  VALUES
  ('day', '1 d'),
  ('hour', '1 h'),
  ('minute', '1 m'),
  ('second', '1 s'),
  ('millisecond', '1 ms'),
  ('microsecond', '1 us')
) intervals (str, interval),
(VALUES (timestamptz '2020-02-29 15:44:17.71393+00')) ts (ts);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT str, `interval`, DATE_TRUNC(ts, 'STR') = DATE_BIN(CAST(`interval` AS INTERVAL), ts, CAST('2001-01-01+11' AS DATETIME)) AS equal FROM (SELECT 'day' AS str, '1 d' AS `interval` UNION ALL SELECT 'hour', '1 h' UNION ALL SELECT 'minute', '1 m' UNION ALL SELECT 'second', '1 s' UNION ALL SELECT 'millisecond', '1 ms' UNION ALL SELECT 'microsecond', '1 us') AS intervals, (SELECT CAST('2020-02-29 15:44:17.71393+00' AS DATETIME) AS ts) AS ts
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：6；字段：str: unknown / 原生类型未知, interval: unknown / 原生类型未知, equal: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
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
  ],
  [
    "millisecond",
    "1 ms",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
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

### pg-timestamptz-0160-7802bb90 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('5 months'::interval, timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('5 months' AS INTERVAL), CAST('2020-02-01 01:01:01+00' AS DATETIME), CAST('2001-01-01+00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamps cannot be binned into intervals containing months or years`。

错误原文：

```text
timestamps cannot be binned into intervals containing months or years
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
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

### pg-timestamptz-0161-856f8667 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('5 years'::interval,  timestamp with time zone '2020-02-01 01:01:01+00', timestamp with time zone '2001-01-01+00');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('5 years' AS INTERVAL), CAST('2020-02-01 01:01:01+00' AS DATETIME), CAST('2001-01-01+00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`timestamps cannot be binned into intervals containing months or years`。

错误原文：

```text
timestamps cannot be binned into intervals containing months or years
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
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

### pg-timestamptz-0162-e22468e0 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT date_bin('0 days'::interval, timestamp with time zone '1970-01-01 01:00:00+00' , timestamp with time zone '1970-01-01 00:00:00+00');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT DATE_BIN(CAST('0 days' AS INTERVAL), CAST('1970-01-01 01:00:00+00' AS DATETIME), CAST('1970-01-01 00:00:00+00' AS DATETIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`stride must be greater than zero`。

错误原文：

```text
stride must be greater than zero
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.1 ms。
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
