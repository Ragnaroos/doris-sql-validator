# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:22.621443+00:00 至 2026-11-11T09:40:22.688002+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/union.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**20**；两端成功且已有证据匹配：**2**。
- 成功结果匹配占全部查询比例：**2/20 = 10.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**2/2 = 100.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**18**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**18**；源参考结果不可用：**0**；Doris 执行失败：**0**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 2 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 18 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 20 条只读查询、跳过 179 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 40 | 121–123 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 41 | 125–127 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 43 | 131–133 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 45 | 137–138 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 46 | 140–141 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 48 | 144–144 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 49 | 146–148 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 52 | 152–152 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 53 | 154–156 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 55 | 160–162 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 57 | 166–167 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 59 | 170–172 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 60 | 174–174 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 61 | 176–177 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 62 | 179–180 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 63 | 182–182 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 64 | 184–185 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 65 | 187–187 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 66 | 189–190 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 67 | 192–193 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 69 | 195–196 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 71 | 198–199 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 73 | 202–204 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 75 | 207–207 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 76 | 209–210 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 78 | 212–213 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 80 | 215–216 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 82 | 219–219 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 83 | 221–222 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 84 | 224–225 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 86 | 227–228 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 88 | 230–231 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 90 | 234–239 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 92 | 242–244 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 93 | 245–246 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 95 | 248–248 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 96 | 250–250 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 97 | 252–253 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 99 | 255–256 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 101 | 258–259 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 103 | 262–266 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 104 | 268–268 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 120 | 322–323 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 121 | 324–324 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 122 | 326–327 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 123 | 328–329 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 130 | 338–339 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 131 | 340–340 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 132 | 342–343 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 133 | 344–345 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 142 | 365–365 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 143 | 366–366 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 146 | 382–387 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 147 | 388–388 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 148 | 389–389 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 149 | 390–390 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 150 | 391–391 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 151 | 393–393 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 152 | 394–394 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 153 | 395–395 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 154 | 396–396 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 155 | 398–403 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 156 | 405–410 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 157 | 412–417 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 158 | 418–418 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 159 | 419–419 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 160 | 420–420 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 161 | 421–421 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 162 | 422–422 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 163 | 424–424 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 164 | 425–425 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 165 | 427–432 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 167 | 440–440 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 168 | 441–441 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 169 | 442–442 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 170 | 443–443 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 171 | 445–447 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 172 | 448–448 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 173 | 449–449 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 174 | 451–456 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 175 | 458–458 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 176 | 460–460 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 177 | 462–472 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 179 | 480–488 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 180 | 490–495 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 181 | 497–502 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 182 | 504–509 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 183 | 511–517 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 184 | 519–524 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 185 | 526–532 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 186 | 534–539 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 187 | 541–542 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 188 | 544–549 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 189 | 551–557 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 190 | 559–559 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 191 | 561–568 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 192 | 570–576 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 193 | 578–585 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 195 | 594–600 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 197 | 609–615 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 199 | 624–631 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 201 | 639–644 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 203 | 652–656 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 204 | 658–658 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 205 | 659–659 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 207 | 662–665 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 209 | 670–670 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 210 | 671–671 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 211 | 673–679 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 213 | 686–695 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 214 | 697–702 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 215 | 704–706 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 216 | 708–712 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 18 | 43–50 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 52–54 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 56–59 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 61–63 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 22 | 65–70 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 23 | 72–75 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 24 | 77–80 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 25 | 82–84 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 26 | 86–91 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 30 | 103–103 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 31 | 105–105 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 32 | 107–107 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 33 | 109–109 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 34 | 111–111 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 35 | 113–113 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 36 | 115–116 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 37 | 117–117 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 38 | 118–118 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 39 | 119–119 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 42 | 128–129 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 44 | 134–135 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 47 | 142–142 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 50 | 149–149 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 51 | 150–150 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 54 | 157–158 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 56 | 163–164 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 58 | 168–168 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 68 | 194–194 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 197–197 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 72 | 200–200 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 74 | 205–205 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 77 | 211–211 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 79 | 214–214 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 217–217 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 85 | 226–226 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 87 | 229–229 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 89 | 232–232 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 91 | 240–240 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 94 | 247–247 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 254–254 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 257–257 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 102 | 260–260 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 270–274 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 276–276 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 107 | 278–282 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 108 | 284–284 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 109 | 286–286 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 110 | 288–288 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 111 | 290–290 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 112 | 292–292 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 113 | 294–300 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 114 | 302–303 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 115 | 305–306 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 116 | 308–312 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 124 | 331–331 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 126 | 333–333 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 144 | 368–377 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 379–380 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 178 | 474–478 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 194 | 587–592 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 602–607 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 198 | 617–622 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 200 | 633–637 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 202 | 646–650 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 666–668 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 212 | 680–684 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/union.out`；SHA-256（文件内容指纹）：`150cd07e6da4475134b0174333d5bfdcd1081512e53fa1e107711b2848770776`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 2/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 2/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 2/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 2/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 2/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/2 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-union-0001-8842af4e` | SELECT 1 AS two UNION SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0002-46978a15` | SELECT 1 AS one UNION SELECT 1 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0003-ada5fa95` | SELECT 1 AS two UNION ALL SELECT 2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-union-0004-f86b7384` | SELECT 1 AS two UNION ALL SELECT 1; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-union-0005-4e651bba` | SELECT 1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0006-20935b45` | SELECT 1 AS two UNION SELECT 2 UNION SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0007-dee35ffd` | SELECT 1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0008-3b1c7020` | SELECT 1.1 AS two UNION SELECT 2.2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0009-774cd2a0` | SELECT 1.1 AS two UNION SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0010-84c85402` | SELECT 1 AS two UNION SELECT 2.2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0011-043dbbe9` | SELECT 1 AS one UNION SELECT 1.0::float8 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0012-69bca50e` | SELECT 1.1 AS two UNION ALL SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0013-6809b41b` | SELECT 1.0::float8 AS two UNION ALL SELECT 1 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0014-e4feb980` | SELECT 1.1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0015-0cb45014` | SELECT 1.1::float8 AS two UNION SELECT 2 UNION SELECT 2.0::float8 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0016-75c00d8c` | SELECT 1.1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0017-86fb9d5a` | SELECT 1.1 AS two UNION (SELECT 2 UNION ALL SELECT 2) ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0027-021c0d72` | SELECT q2 FROM int8_tbl INTERSECT SELECT q1 FROM int8_tbl ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0028-cb1f47b2` | SELECT q2 FROM int8_tbl INTERSECT ALL SELECT q1 FROM int8_tbl ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-union-0029-6c7c44d0` | SELECT q2 FROM int8_tbl EXCEPT SELECT q1 FROM int8_tbl ORDER BY 1; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-union-0001-8842af4e — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS two UNION SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0002-46978a15 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS one UNION SELECT 1 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0005-4e651bba — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0006-20935b45 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS two UNION SELECT 2 UNION SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0007-dee35ffd — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0008-3b1c7020 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS two UNION SELECT 2.2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0009-774cd2a0 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS two UNION SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0010-84c85402 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS two UNION SELECT 2.2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0011-043dbbe9 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1 AS one UNION SELECT 1.0::float8 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0012-69bca50e — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS two UNION ALL SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0013-6809b41b — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.0::float8 AS two UNION ALL SELECT 1 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0014-e4feb980 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS three UNION SELECT 2 UNION SELECT 3 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0015-0cb45014 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1::float8 AS two UNION SELECT 2 UNION SELECT 2.0::float8 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0016-75c00d8c — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS three UNION SELECT 2 UNION ALL SELECT 2 ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0017-86fb9d5a — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT 1.1 AS two UNION (SELECT 2 UNION ALL SELECT 2) ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0027-021c0d72 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT q2 FROM int8_tbl INTERSECT SELECT q1 FROM int8_tbl ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0028-cb1f47b2 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT q2 FROM int8_tbl INTERSECT ALL SELECT q1 FROM int8_tbl ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-union-0029-6c7c44d0 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT q2 FROM int8_tbl EXCEPT SELECT q1 FROM int8_tbl ORDER BY 1;
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: 'NULLS LAST' translation not supported with positional ordering
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。
