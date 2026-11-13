# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:11.318351+00:00 至 2026-11-11T09:40:12.742019+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/join.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**58**；两端成功且已有证据匹配：**28**。
- 成功结果匹配占全部查询比例：**28/58 = 48.28%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**28/53 = 52.83%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**2**；不计入上述成功匹配分子。
- 需要分析的查询：**30**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**3**；源参考结果不可用：**0**；Doris 执行失败：**25**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 23 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 30 |
| 返回记录行数不同（`ROW_COUNT_MISMATCH`） | 1 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 1 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 3 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 58 条只读查询、跳过 967 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–10 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 12–15 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 18–18 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 19–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 20–20 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 21–21 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 22–22 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 23–23 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 25–25 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 27–27 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 28–28 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 14 | 30–30 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 15 | 31–31 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 32–32 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 17 | 33–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 34–34 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 19 | 35–35 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 36–36 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 21 | 37–37 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 22 | 38–38 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 23 | 40–41 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 24 | 42–42 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 67 | 213–220 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 68 | 223–231 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 69 | 232–232 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 70 | 233–233 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 71 | 235–235 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 72 | 236–236 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 73 | 237–237 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 238–238 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 75 | 239–239 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 240–240 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 77 | 241–241 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 90 | 325–327 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 91 | 328–328 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 92 | 329–329 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 93 | 330–330 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 94 | 331–331 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 95 | 332–332 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 96 | 334–334 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 97 | 335–335 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 98 | 336–336 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 99 | 337–337 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 100 | 338–338 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 115 | 381–381 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 116 | 382–382 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 119 | 389–395 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 121 | 401–407 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 124 | 427–436 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 126 | 444–455 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 128 | 465–473 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 130 | 481–485 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 131 | 487–491 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 132 | 493–498 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 133 | 500–504 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 134 | 506–510 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 135 | 512–516 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 136 | 518–524 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 137 | 526–532 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 138 | 534–538 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 139 | 540–544 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 140 | 546–551 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 141 | 553–558 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 142 | 560–565 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 143 | 567–572 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 144 | 574–582 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 146 | 589–597 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 148 | 605–605 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 149 | 606–606 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 150 | 607–607 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 151 | 609–618 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 152 | 620–620 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 153 | 621–621 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 154 | 622–622 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 155 | 624–628 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 156 | 629–629 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 157 | 630–630 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 158 | 632–632 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 159 | 633–633 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 160 | 635–638 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 161 | 639–639 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 162 | 640–640 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 163 | 642–642 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 164 | 643–643 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 165 | 644–644 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 166 | 645–645 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 167 | 646–646 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 168 | 647–647 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 169 | 648–648 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 170 | 649–649 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 171 | 650–650 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 172 | 652–652 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 174 | 654–654 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 176 | 656–656 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 178 | 659–661 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 179 | 663–663 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 187 | 693–697 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 188 | 698–698 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 189 | 699–699 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 190 | 701–701 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 191 | 702–702 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 192 | 703–703 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 193 | 705–705 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 194 | 706–706 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 197 | 714–714 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 198 | 715–715 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 199 | 717–721 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 200 | 722–722 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 201 | 723–723 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 203 | 726–726 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 204 | 727–727 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 205 | 729–732 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 207 | 738–738 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 208 | 739–739 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 209 | 741–745 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 210 | 746–746 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 212 | 749–754 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 215 | 768–769 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 216 | 770–770 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 217 | 771–771 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 218 | 772–772 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 219 | 774–778 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 222 | 791–791 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 223 | 792–792 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 224 | 793–793 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 225 | 794–794 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 227 | 797–800 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 229 | 806–809 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 231 | 814–817 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 234 | 824–828 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 235 | 829–829 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 236 | 830–830 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 237 | 832–834 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 239 | 838–838 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 240 | 839–839 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 241 | 840–840 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 242 | 842–846 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 243 | 847–847 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 245 | 850–850 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 246 | 851–851 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 248 | 854–854 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 249 | 856–865 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 251 | 877–877 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 252 | 879–884 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 253 | 885–889 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 255 | 892–894 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 256 | 896–896 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 257 | 898–904 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 258 | 906–909 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 259 | 911–913 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 260 | 915–917 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 261 | 919–921 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 262 | 923–924 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 263 | 925–927 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 264 | 928–928 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 266 | 937–937 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 267 | 939–942 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 268 | 944–948 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 269 | 950–954 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 270 | 956–961 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 271 | 963–969 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 272 | 971–977 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 273 | 979–985 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 274 | 987–992 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 275 | 994–998 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 276 | 1000–1004 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 277 | 1006–1012 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 278 | 1014–1018 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 279 | 1020–1023 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 280 | 1025–1030 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 281 | 1032–1036 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 282 | 1038–1042 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 283 | 1044–1048 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 284 | 1050–1055 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 285 | 1057–1062 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 286 | 1064–1070 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 287 | 1072–1074 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 288 | 1075–1075 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 289 | 1076–1076 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 290 | 1077–1077 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 291 | 1079–1081 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 293 | 1085–1087 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 295 | 1091–1094 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 296 | 1096–1099 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 297 | 1101–1104 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 298 | 1106–1111 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 299 | 1113–1116 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 300 | 1118–1124 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 301 | 1126–1130 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 302 | 1132–1137 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 303 | 1139–1143 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 304 | 1145–1149 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 305 | 1151–1158 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 306 | 1160–1163 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 307 | 1165–1166 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 308 | 1167–1169 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 309 | 1171–1174 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 310 | 1176–1179 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 311 | 1180–1180 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 312 | 1182–1185 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 314 | 1190–1193 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 315 | 1195–1199 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 316 | 1201–1206 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 317 | 1208–1212 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 318 | 1214–1218 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 320 | 1222–1228 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 321 | 1230–1234 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 322 | 1236–1245 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 323 | 1247–1251 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 324 | 1252–1252 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 325 | 1254–1254 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 326 | 1255–1255 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 327 | 1257–1257 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 328 | 1258–1258 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 329 | 1259–1259 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 331 | 1263–1267 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 332 | 1268–1268 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 333 | 1270–1270 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 334 | 1271–1271 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 335 | 1272–1272 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 336 | 1274–1274 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 337 | 1275–1275 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 338 | 1276–1276 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 340 | 1285–1290 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 341 | 1291–1291 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 342 | 1292–1292 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 343 | 1293–1293 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 344 | 1294–1294 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 346 | 1301–1301 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 348 | 1308–1314 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 350 | 1322–1326 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 357 | 1358–1358 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 358 | 1359–1359 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 359 | 1360–1360 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 360 | 1362–1362 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 361 | 1363–1363 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 365 | 1374–1374 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 366 | 1376–1376 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 367 | 1377–1377 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 368 | 1379–1380 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 369 | 1382–1382 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 370 | 1383–1383 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 371 | 1385–1386 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 379 | 1424–1431 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 381 | 1439–1447 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 383 | 1456–1461 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 385 | 1467–1471 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 387 | 1476–1483 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 389 | 1491–1497 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 392 | 1509–1512 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 393 | 1513–1517 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 394 | 1518–1522 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 395 | 1524–1524 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 396 | 1525–1525 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 397 | 1526–1526 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 398 | 1527–1527 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 399 | 1528–1528 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 400 | 1529–1529 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 401 | 1530–1530 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 406 | 1581–1592 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 408 | 1602–1610 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 409 | 1611–1617 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 410 | 1618–1623 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 411 | 1625–1625 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 412 | 1626–1626 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 413 | 1627–1627 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 414 | 1628–1628 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 415 | 1629–1629 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 416 | 1630–1630 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 417 | 1631–1631 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 418 | 1632–1632 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 419 | 1633–1633 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 420 | 1635–1646 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 422 | 1660–1671 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 424 | 1681–1695 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 428 | 1714–1718 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 429 | 1719–1719 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 432 | 1723–1727 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 433 | 1729–1733 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 434 | 1735–1742 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 435 | 1744–1760 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 437 | 1775–1792 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 439 | 1810–1824 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 441 | 1839–1844 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 443 | 1849–1854 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 445 | 1859–1867 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 447 | 1875–1881 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 449 | 1888–1891 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 451 | 1895–1895 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 452 | 1896–1902 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 455 | 1907–1907 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 456 | 1909–1913 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 457 | 1915–1924 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 459 | 1928–1935 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 460 | 1937–1944 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 461 | 1946–1956 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 462 | 1958–1967 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 463 | 1969–1979 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 465 | 1991–1995 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 467 | 2001–2007 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 468 | 2009–2014 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 469 | 2016–2021 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 470 | 2023–2028 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 472 | 2033–2033 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 473 | 2034–2034 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 474 | 2035–2035 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 475 | 2037–2043 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 478 | 2054–2058 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 479 | 2060–2063 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 480 | 2065–2068 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 481 | 2070–2071 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 482 | 2073–2074 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 483 | 2076–2077 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 484 | 2079–2080 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 485 | 2082–2083 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 486 | 2085–2086 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 487 | 2088–2089 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 488 | 2091–2093 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 489 | 2095–2107 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 490 | 2109–2109 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 491 | 2111–2114 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 492 | 2116–2117 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 493 | 2119–2120 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 495 | 2123–2124 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 497 | 2127–2127 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 498 | 2128–2128 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 499 | 2130–2133 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 500 | 2135–2138 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 501 | 2140–2140 | 跳过非查询；类型 `drop` | Expecting ). Line 1, Col: 35.   drop function f_field_select(t [4monek[0m);  Invalid expression / Unexpected token. Line 1, Col: 35.   drop function f_field_select(t [4monek[0m); |
| 502 | 2142–2149 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 503 | 2150–2152 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 504 | 2153–2156 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 505 | 2158–2161 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 506 | 2162–2165 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 507 | 2167–2175 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 508 | 2177–2181 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 509 | 2183–2187 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 511 | 2194–2200 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 513 | 2209–2216 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 515 | 2226–2230 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 517 | 2237–2244 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 519 | 2250–2253 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 521 | 2259–2266 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 523 | 2272–2276 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 525 | 2281–2297 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 527 | 2312–2324 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 529 | 2336–2350 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 531 | 2363–2373 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 533 | 2386–2397 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 535 | 2411–2419 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 537 | 2430–2438 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 538 | 2440–2449 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 539 | 2451–2461 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 541 | 2470–2477 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 543 | 2487–2494 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 545 | 2504–2511 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 548 | 2527–2527 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 549 | 2529–2539 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 551 | 2543–2556 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 553 | 2568–2579 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 555 | 2588–2596 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 557 | 2605–2614 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 559 | 2621–2626 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 561 | 2633–2634 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 562 | 2636–2640 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 564 | 2647–2647 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 565 | 2649–2661 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 566 | 2663–2675 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 568 | 2685–2696 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 569 | 2698–2705 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 571 | 2714–2714 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 572 | 2716–2721 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 575 | 2731–2740 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 577 | 2748–2753 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 578 | 2755–2756 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 579 | 2758–2764 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 580 | 2765–2765 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 581 | 2767–2770 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 583 | 2775–2775 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 584 | 2776–2776 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 585 | 2778–2785 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 587 | 2791–2798 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 589 | 2804–2807 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 591 | 2813–2816 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 593 | 2822–2831 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 596 | 2845–2845 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 597 | 2846–2846 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 598 | 2847–2847 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 599 | 2848–2848 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 600 | 2849–2849 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 601 | 2850–2850 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 602 | 2851–2851 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 603 | 2852–2852 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 604 | 2853–2853 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 605 | 2854–2854 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 606 | 2856–2857 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 607 | 2858–2858 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 608 | 2859–2861 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 609 | 2862–2864 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 610 | 2866–2870 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 611 | 2872–2878 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 612 | 2880–2885 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 613 | 2887–2891 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 614 | 2893–2905 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 615 | 2907–2919 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 616 | 2921–2926 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 617 | 2926–2935 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 618 | 2937–2947 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 619 | 2949–2958 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 620 | 2960–2967 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 621 | 2969–2978 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 622 | 2980–2988 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 623 | 2990–2996 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 624 | 2998–3005 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 625 | 3007–3011 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 626 | 3013–3023 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 627 | 3025–3031 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 628 | 3033–3037 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 629 | 3039–3046 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 630 | 3048–3055 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 631 | 3057–3062 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 632 | 3064–3071 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 633 | 3073–3077 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 634 | 3079–3083 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 635 | 3085–3087 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 636 | 3089–3091 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 637 | 3093–3095 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 638 | 3097–3100 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 639 | 3102–3108 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 640 | 3110–3114 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 641 | 3116–3118 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 642 | 3120–3122 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 643 | 3124–3127 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 644 | 3129–3135 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 646 | 3141–3144 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 647 | 3146–3150 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 648 | 3152–3155 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 649 | 3157–3160 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 650 | 3162–3166 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 651 | 3168–3170 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 652 | 3172–3181 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 653 | 3183–3183 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 654 | 3184–3184 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 655 | 3186–3188 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 656 | 3190–3194 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 657 | 3196–3200 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 658 | 3202–3207 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 660 | 3211–3211 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 661 | 3212–3212 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 662 | 3213–3213 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 663 | 3214–3214 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 665 | 3218–3219 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 667 | 3225–3228 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 669 | 3234–3237 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 671 | 3242–3245 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 674 | 3258–3258 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 675 | 3259–3259 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 676 | 3260–3260 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 677 | 3261–3261 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 682 | 3271–3271 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 683 | 3272–3272 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 685 | 3281–3286 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 686 | 3288–3294 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 687 | 3296–3302 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 690 | 3309–3309 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 691 | 3311–3317 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 692 | 3319–3330 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 696 | 3349–3349 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 697 | 3350–3350 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 698 | 3352–3358 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 702 | 3374–3374 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 703 | 3375–3376 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 704 | 3377–3377 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 705 | 3379–3384 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 709 | 3398–3398 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 710 | 3399–3399 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 711 | 3401–3408 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 715 | 3424–3424 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 716 | 3425–3425 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 717 | 3427–3429 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 721 | 3440–3440 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 722 | 3441–3441 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 723 | 3442–3442 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 724 | 3443–3443 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 725 | 3444–3444 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 726 | 3446–3446 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 727 | 3448–3450 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 731 | 3460–3460 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 732 | 3461–3461 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 733 | 3463–3470 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 734 | 3472–3479 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 737 | 3491–3498 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 739 | 3507–3509 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 740 | 3510–3510 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 741 | 3511–3511 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 742 | 3512–3516 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 747 | 3530–3537 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 748 | 3538–3538 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 749 | 3540–3540 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 750 | 3541–3541 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 752 | 3544–3546 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 754 | 3549–3554 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 756 | 3559–3561 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 757 | 3563–3569 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 758 | 3571–3577 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 759 | 3579–3584 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 760 | 3586–3589 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 761 | 3590–3593 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 762 | 3595–3603 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 763 | 3605–3609 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 764 | 3611–3614 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 765 | 3616–3618 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 766 | 3620–3627 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 767 | 3629–3635 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 768 | 3637–3642 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 769 | 3644–3647 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 770 | 3649–3652 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 771 | 3654–3658 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 772 | 3660–3665 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 773 | 3667–3670 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 774 | 3672–3676 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 775 | 3678–3684 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 776 | 3686–3688 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 778 | 3692–3694 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 780 | 3698–3703 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 782 | 3710–3712 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 784 | 3716–3718 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 786 | 3722–3727 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 788 | 3732–3733 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 789 | 3735–3738 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 790 | 3739–3742 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 791 | 3744–3749 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 793 | 3756–3761 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 795 | 3768–3769 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 796 | 3771–3774 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 797 | 3776–3779 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 798 | 3781–3781 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 799 | 3783–3785 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 800 | 3787–3789 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 801 | 3791–3793 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 802 | 3795–3795 | 跳过非查询；类型 `drop` | Invalid expression / Unexpected token. Line 1, Col: 21.   DROP INDEX sj_fn_idx[4m,[0m sj_temp_idx1, sj_temp_idx; |
| 803 | 3797–3798 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 804 | 3799–3799 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 805 | 3801–3805 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 806 | 3806–3806 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 807 | 3808–3810 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 808 | 3812–3815 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 809 | 3817–3819 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 810 | 3821–3824 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 811 | 3826–3828 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 812 | 3830–3836 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 813 | 3837–3837 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 814 | 3838–3838 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 815 | 3839–3839 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 816 | 3840–3842 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 817 | 3843–3845 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 818 | 3846–3846 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 819 | 3847–3847 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 820 | 3849–3850 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 821 | 3851–3852 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 822 | 3854–3856 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 823 | 3858–3860 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 824 | 3862–3864 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 825 | 3866–3868 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 826 | 3870–3875 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 827 | 3877–3883 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 828 | 3885–3892 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 829 | 3894–3897 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 830 | 3899–3902 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 831 | 3904–3911 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 832 | 3912–3912 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 833 | 3913–3914 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 835 | 3916–3921 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 836 | 3922–3922 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 837 | 3924–3928 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 838 | 3930–3934 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 839 | 3936–3940 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 840 | 3942–3942 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 843 | 3950–3951 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 844 | 3953–3955 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 845 | 3956–3956 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 846 | 3957–3957 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Command |
| 847 | 3959–3960 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 848 | 3961–3967 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 850 | 3975–3977 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 851 | 3978–3980 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 853 | 3984–3987 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 854 | 3988–3988 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 856 | 3991–3993 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 857 | 3995–4001 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 858 | 4002–4007 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 859 | 4009–4011 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 860 | 4013–4016 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 861 | 4018–4019 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 862 | 4020–4022 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 863 | 4024–4028 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 864 | 4030–4034 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 865 | 4036–4039 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 866 | 4040–4040 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 867 | 4041–4041 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 868 | 4042–4042 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 869 | 4044–4044 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 870 | 4045–4045 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 871 | 4047–4064 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 872 | 4066–4067 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 873 | 4068–4068 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 875 | 4071–4074 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 877 | 4080–4086 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 878 | 4088–4088 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 879 | 4089–4089 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 885 | 4114–4118 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 887 | 4126–4128 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 889 | 4131–4133 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 890 | 4134–4136 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 892 | 4139–4141 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 896 | 4150–4151 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 897 | 4152–4153 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 898 | 4154–4156 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 899 | 4158–4162 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 901 | 4167–4172 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 902 | 4174–4180 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 903 | 4181–4184 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 904 | 4185–4191 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 905 | 4192–4197 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 906 | 4198–4202 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 907 | 4203–4206 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 908 | 4208–4215 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 909 | 4217–4225 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 911 | 4233–4236 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 913 | 4240–4243 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 915 | 4247–4252 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 930 | 4297–4300 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 932 | 4304–4307 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 934 | 4312–4317 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 936 | 4323–4330 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 939 | 4342–4342 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 940 | 4344–4350 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 943 | 4361–4365 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 945 | 4368–4370 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 947 | 4373–4377 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 949 | 4383–4389 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 951 | 4396–4405 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 952 | 4407–4412 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 954 | 4419–4430 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 955 | 4432–4438 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 956 | 4440–4444 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 957 | 4446–4449 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 958 | 4450–4452 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 961 | 4467–4473 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 963 | 4480–4490 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 965 | 4501–4509 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 967 | 4517–4525 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 969 | 4534–4536 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 970 | 4537–4537 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 971 | 4539–4544 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 973 | 4551–4551 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 974 | 4553–4559 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 976 | 4566–4566 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 985 | 4582–4584 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 986 | 4586–4587 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 987 | 4588–4588 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 988 | 4589–4590 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 989 | 4591–4592 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 990 | 4594–4595 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 991 | 4596–4596 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 992 | 4597–4597 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 993 | 4599–4603 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 994 | 4604–4604 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 995 | 4605–4605 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 996 | 4606–4606 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 997 | 4607–4607 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 998 | 4608–4608 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 999 | 4609–4609 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1000 | 4610–4614 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1002 | 4620–4620 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1003 | 4621–4621 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1005 | 4629–4629 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1006 | 4630–4630 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1007 | 4631–4631 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1009 | 4634–4638 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1010 | 4640–4641 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 1011 | 4643–4647 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1014 | 4657–4657 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1015 | 4658–4658 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1016 | 4660–4660 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1017 | 4661–4661 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1018 | 4663–4664 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Alter |
| 1021 | 4669–4675 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1023 | 4679–4683 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1024 | 4684–4684 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1025 | 4685–4685 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1026 | 4687–4687 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1027 | 4688–4688 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1028 | 4689–4689 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1032 | 4695–4697 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1033 | 4699–4701 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1034 | 4703–4705 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1035 | 4707–4709 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1036 | 4711–4713 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1037 | 4715–4717 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1038 | 4719–4721 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1039 | 4723–4725 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1040 | 4727–4730 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1041 | 4732–4735 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1042 | 4737–4737 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1043 | 4738–4738 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1044 | 4739–4739 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1045 | 4741–4743 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1046 | 4744–4744 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1047 | 4745–4745 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1048 | 4747–4747 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1049 | 4748–4748 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1050 | 4749–4749 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1054 | 4755–4759 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1055 | 4761–4764 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1056 | 4766–4770 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1057 | 4772–4775 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1058 | 4777–4777 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1059 | 4779–4782 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1060 | 4784–4784 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1061 | 4786–4789 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1062 | 4790–4790 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1063 | 4791–4791 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1064 | 4793–4794 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1065 | 4795–4795 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1068 | 4799–4800 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1069 | 4801–4801 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1070 | 4803–4805 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1072 | 4811–4814 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1074 | 4820–4823 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1076 | 4829–4829 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1077 | 4830–4830 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1078 | 4831–4831 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1079 | 4833–4833 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1080 | 4834–4834 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1081 | 4835–4835 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1082 | 4837–4843 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1083 | 4845–4846 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1085 | 4848–4848 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1086 | 4850–4855 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1087 | 4857–4857 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1088 | 4859–4869 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1089 | 4870–4870 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1090 | 4871–4871 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1092 | 4874–4874 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1093 | 4875–4875 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1094 | 4876–4877 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1096 | 4880–4880 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1097 | 4881–4881 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1098 | 4882–4883 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1099 | 4884–4884 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 1100 | 4886–4886 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1101 | 4887–4887 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1102 | 4888–4888 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1103 | 4890–4892 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1105 | 4896–4896 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1106 | 4897–4897 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 1107 | 4899–4900 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1108 | 4901–4901 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1109 | 4902–4902 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 1111 | 4905–4908 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1112 | 4910–4910 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 1113 | 4912–4916 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1115 | 4922–4929 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1117 | 4933–4935 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1119 | 4939–4949 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 1122 | 4961–4961 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 1123 | 4962–4962 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 1125 | 4965–4971 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 113 | 370–377 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 117 | 383–386 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 120 | 397–399 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 122 | 409–411 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 125 | 438–442 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 127 | 457–463 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 129 | 475–479 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 145 | 584–587 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 147 | 599–603 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 173 | 653–653 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 175 | 655–655 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 177 | 657–657 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 180 | 665–665 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 181 | 667–669 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 671–675 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 195 | 708–710 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 712–712 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 206 | 734–736 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 213 | 756–760 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 228 | 802–804 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 230 | 811–812 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 232 | 819–820 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 238 | 835–836 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 250 | 867–875 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 292 | 1082–1083 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 294 | 1088–1089 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 313 | 1186–1188 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 330 | 1261–1261 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 339 | 1278–1283 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 345 | 1296–1299 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 347 | 1303–1306 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 349 | 1316–1320 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 351 | 1328–1330 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 352 | 1332–1340 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 362 | 1365–1365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 373 | 1390–1395 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 374 | 1397–1399 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 375 | 1401–1403 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 376 | 1405–1409 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 377 | 1411–1416 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 378 | 1418–1422 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 380 | 1432–1437 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 382 | 1448–1454 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 386 | 1472–1474 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 402 | 1532–1540 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 404 | 1544–1562 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 405 | 1564–1579 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 407 | 1594–1600 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 421 | 1648–1658 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 423 | 1673–1679 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 425 | 1697–1706 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 426 | 1708–1711 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 427 | 1712–1712 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 436 | 1762–1773 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 438 | 1794–1808 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 440 | 1826–1837 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 442 | 1845–1847 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 444 | 1855–1857 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 448 | 1882–1886 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 464 | 1981–1989 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 466 | 1997–1999 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 476 | 2045–2050 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 494 | 2121–2121 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 496 | 2125–2125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 510 | 2189–2192 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 512 | 2202–2207 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 514 | 2218–2224 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 516 | 2232–2235 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 518 | 2246–2248 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 520 | 2255–2257 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 522 | 2268–2270 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 524 | 2278–2279 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 526 | 2299–2310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 528 | 2326–2334 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 530 | 2352–2361 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 532 | 2375–2384 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 534 | 2399–2409 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 536 | 2421–2428 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 540 | 2463–2468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 542 | 2479–2485 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 544 | 2496–2502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 546 | 2513–2519 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 552 | 2558–2566 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 554 | 2581–2586 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 556 | 2598–2603 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 558 | 2616–2619 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 560 | 2628–2631 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 563 | 2642–2645 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 573 | 2723–2727 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 576 | 2742–2746 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 582 | 2771–2773 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 586 | 2787–2789 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 588 | 2800–2802 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 590 | 2809–2811 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 592 | 2818–2820 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 594 | 2833–2837 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 645 | 3136–3139 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 664 | 3216–3217 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 666 | 3221–3224 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 668 | 3230–3233 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 670 | 3239–3241 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 672 | 3247–3253 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 678 | 3263–3263 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 679 | 3264–3264 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 684 | 3274–3279 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 693 | 3332–3342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 699 | 3360–3365 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 706 | 3386–3390 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 712 | 3410–3416 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 718 | 3431–3432 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 728 | 3452–3453 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 735 | 3481–3487 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 738 | 3500–3505 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 743 | 3518–3521 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 744 | 3523–3526 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 745 | 3526–3528 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 746 | 3528–3530 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 753 | 3547–3547 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 755 | 3555–3557 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 777 | 3689–3690 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 779 | 3695–3696 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 781 | 3704–3708 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 783 | 3713–3714 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 785 | 3719–3720 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 787 | 3728–3730 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 792 | 3750–3754 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 794 | 3762–3766 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 849 | 3968–3973 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 852 | 3981–3982 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 876 | 4076–4078 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 880 | 4091–4096 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 881 | 4096–4098 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 882 | 4098–4100 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 883 | 4100–4102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 884 | 4102–4112 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 886 | 4120–4125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 888 | 4129–4130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 891 | 4137–4138 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 893 | 4143–4145 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 894 | 4146–4146 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 895 | 4148–4149 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 900 | 4163–4165 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 910 | 4226–4231 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 912 | 4237–4238 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 914 | 4244–4245 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 916 | 4253–4256 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 917 | 4258–4260 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 918 | 4261–4262 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 919 | 4263–4264 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 920 | 4266–4268 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 921 | 4269–4270 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 922 | 4271–4272 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 923 | 4273–4274 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 924 | 4275–4277 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 925 | 4278–4280 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 926 | 4281–4283 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 927 | 4284–4287 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 928 | 4288–4291 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 929 | 4292–4295 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 931 | 4301–4303 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 933 | 4308–4310 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 935 | 4318–4321 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 937 | 4331–4336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 941 | 4352–4357 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 944 | 4366–4367 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 946 | 4371–4372 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 948 | 4378–4381 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 950 | 4390–4394 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 953 | 4414–4417 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 959 | 4454–4462 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 960 | 4464–4465 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 962 | 4474–4478 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 964 | 4492–4499 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 966 | 4510–4515 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 968 | 4526–4532 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 972 | 4545–4549 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 975 | 4560–4564 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 977 | 4568–4569 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 978 | 4570–4570 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 979 | 4571–4571 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 980 | 4572–4572 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 981 | 4573–4574 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 982 | 4575–4575 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 983 | 4576–4578 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 984 | 4579–4580 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1001 | 4615–4618 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1071 | 4807–4809 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1073 | 4816–4818 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1075 | 4825–4827 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1095 | 4878–4878 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1104 | 4893–4894 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1114 | 4918–4920 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1116 | 4930–4931 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1118 | 4936–4937 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1120 | 4951–4955 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 1126 | 4973–4978 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/join.out`；SHA-256（文件内容指纹）：`1960082fa9a95511cbe3ccaf864dad76b840d0147592c311137840955286f0ee`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 55/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 55/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 53/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 53/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 53/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/55 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-join-0026-3d577984` | SELECT *   FROM J1_TBL AS tx; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0027-3d577984` | SELECT *   FROM J1_TBL tx; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0028-f25eea71` | SELECT *   FROM J1_TBL AS t1 (a, b, c); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0029-f25eea71` | SELECT *   FROM J1_TBL t1 (a, b, c); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0030-8603f3ed` | SELECT *   FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0031-f4169150` | SELECT t1.a, t2.e   FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e)   WHERE t1.a = t2.d; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0032-131168ee` | SELECT *   FROM J1_TBL CROSS JOIN J2_TBL; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0033-f5fe6eea` | SELECT i, k, t   FROM J1_TBL CROSS JOIN J2_TBL; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-join-0034-2aef35d2` | SELECT t1.i, k, t   FROM J1_TBL t1 CROSS JOIN J2_TBL t2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0035-06b3f865` | SELECT ii, tt, kk   FROM (J1_TBL CROSS JOIN J2_TBL)     AS tx (ii, jj, tt, ii2, kk); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0036-deb1b49d` | SELECT tx.ii, tx.jj, tx.kk   FROM (J1_TBL t1 (a, b, c) CROSS JOIN J2_TBL t2 (d, e))     AS tx (ii, jj, tt, ii2, kk); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0037-5124334f` | SELECT *   FROM J1_TBL CROSS JOIN J2_TBL a CROSS JOIN J2_TBL b; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0038-ed098b35` | SELECT *   FROM J1_TBL INNER JOIN J2_TBL USING (i); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0039-d48b47ad` | SELECT *   FROM J1_TBL JOIN J2_TBL USING (i); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0040-a96d716e` | SELECT *   FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, d) USING (a)   ORDER BY a, d; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0041-6acaaacd` | SELECT *   FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, b) USING (b)   ORDER BY b, t1.a; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0042-69d99dd0` | SELECT * FROM J1_TBL JOIN J2_TBL USING (i) WHERE J1_TBL.t = 'one'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0044-77d9c458` | SELECT * FROM (J1_TBL JOIN J2_TBL USING (i)) AS x WHERE J1_TBL.t = 'one'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-join-0052-38f1da35` | SELECT *   FROM J1_TBL NATURAL JOIN J2_TBL; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0053-7ab78474` | SELECT *   FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (a, d); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0054-8499874b` | SELECT *   FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (d, a); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0055-e0343680` | SELECT *   FROM J1_TBL t1 (a, b) NATURAL JOIN J2_TBL t2 (a); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0056-4f0fb7e6` | SELECT *   FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i = J2_TBL.i); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0057-a1cdb13d` | SELECT *   FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i = J2_TBL.k); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0058-0eea9375` | SELECT *   FROM J1_TBL JOIN J2_TBL ON (J1_TBL.i <= J2_TBL.k); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0059-59e1a665` | SELECT *   FROM J1_TBL LEFT OUTER JOIN J2_TBL USING (i)   ORDER BY i, k, t; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0060-7e3cb6a7` | SELECT *   FROM J1_TBL LEFT JOIN J2_TBL USING (i)   ORDER BY i, k, t; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0061-af0e5d94` | SELECT *   FROM J1_TBL RIGHT OUTER JOIN J2_TBL USING (i); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0062-f291f66b` | SELECT *   FROM J1_TBL RIGHT JOIN J2_TBL USING (i); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0063-02b7035f` | SELECT *   FROM J1_TBL FULL OUTER JOIN J2_TBL USING (i)   ORDER BY i, k, t; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0064-e44f487a` | SELECT *   FROM J1_TBL FULL JOIN J2_TBL USING (i)   ORDER BY i, k, t; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0065-58560026` | SELECT *   FROM J1_TBL LEFT JOIN J2_TBL USING (i) WHERE (k = 1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0066-efcfad36` | SELECT *   FROM J1_TBL LEFT JOIN J2_TBL USING (i) WHERE (i = 1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0078-ff5cfabb` | SELECT * FROM t1 FULL JOIN t2 USING (name) FULL JOIN t3 USING (name); | 已生成 | 成功 | 成功 | 返回记录行数不同 |
| `pg-join-0079-cfd7eba7` | SELECT * FROM (SELECT * FROM t2) as s2 INNER JOIN (SELECT * FROM t3) s3 USING (name); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0080-76b214df` | SELECT * FROM (SELECT * FROM t2) as s2 LEFT JOIN (SELECT * FROM t3) s3 USING (name); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0081-1853c44b` | SELECT * FROM (SELECT * FROM t2) as s2 FULL JOIN (SELECT * FROM t3) s3 USING (name); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-join-0082-ede1f502` | SELECT * FROM (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2 NATURAL INNER JOIN (SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0083-ad25c0f2` | SELECT * FROM (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2 NATURAL LEFT JOIN (SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0084-d692d7c3` | SELECT * FROM (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2 NATURAL FULL JOIN (SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-join-0085-8f120375` | SELECT * FROM (SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1 NATURAL INNER JOIN (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2 NATURAL INNER JOIN (SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0086-8e4f7296` | SELECT * FROM (SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1 NATURAL FULL JOIN (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2 NATURAL FULL JOIN (SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0087-f13d67d0` | SELECT * FROM (SELECT name, n as s1_n FROM t1) as s1 NATURAL FULL JOIN   (SELECT * FROM     (SELECT name, n as s2_n FROM t2) as s2     NATURAL FULL JOIN     (SELECT name, n as s3_n FROM t3) as s3   ) ss2; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-join-0088-9518261f` | SELECT * FROM (SELECT name, n as s1_n FROM t1) as s1 NATURAL FULL JOIN   (SELECT * FROM     (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2     NATURAL FULL JOIN     (SELECT name, n as s3_n FROM t3) as s3   ) ss2; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-join-0089-7ce60f41` | SELECT * FROM   (SELECT name, n as s1_n FROM t1) as s1 FULL JOIN   (SELECT name, 2 as s2_n FROM t2) as s2 ON (s1_n = s2_n); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0101-1efc0847` | select * from x; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0102-86bdd254` | select * from y; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0103-dd8d1c93` | select * from x left join y on (x1 = y1 and x2 is not null); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0104-f0bdfc8e` | select * from x left join y on (x1 = y1 and y2 is not null); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0105-7b5454e9` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0106-19118909` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1 and x2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0107-cd1a2740` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1 and y2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0108-29622a8a` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1 and xx2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0109-9c15a804` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1) where (x2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0110-bacb7b5f` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1) where (y2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0111-f8035c11` | select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2) on (x1 = xx1) where (xx2 is not null); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-join-0112-e1276d8d` | select count(*) from tenk1 a where unique1 in   (select unique1 from tenk1 b join tenk1 c using (unique1)    where b.unique2 = 42); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-join-0123-7ae195fb` | select count(*) from   (select t3.tenthous as x1, coalesce(t1.stringu1, t2.stringu1) as x2    from tenk1 t1    left join tenk1 t2 on t1.unique1 = t2.unique1    join tenk1 t3 on t1.unique2 = t3.unique2) ss,   tenk1 t4,   tenk1 t5 where t4.thousand = t5.unique1 and ss.x1 = t4.tenthous and ss.x2 = t5.stringu1; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |

## 4. 不匹配、执行失败及负向错误详情

### pg-join-0028-f25eea71 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL AS t1 (a, b, c);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：11；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "4",
    "one"
  ],
  [
    "2",
    "3",
    "two"
  ],
  [
    "3",
    "2",
    "three"
  ],
  [
    "4",
    "1",
    "four"
  ],
  [
    "5",
    "0",
    "five"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
doris_error_code=1105
```

### pg-join-0029-f25eea71 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：11；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "4",
    "one"
  ],
  [
    "2",
    "3",
    "two"
  ],
  [
    "3",
    "2",
    "three"
  ],
  [
    "4",
    "1",
    "four"
  ],
  [
    "5",
    "0",
    "five"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c)\n---------------------^^^\n')
doris_error_code=1105
```

### pg-join-0030-8603f3ed — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：99；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知, d: unknown / 原生类型未知, e: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "4",
    "one",
    "1",
    "-1"
  ],
  [
    "2",
    "3",
    "two",
    "1",
    "-1"
  ],
  [
    "3",
    "2",
    "three",
    "1",
    "-1"
  ],
  [
    "4",
    "1",
    "four",
    "1",
    "-1"
  ],
  [
    "5",
    "0",
    "five",
    "1",
    "-1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 20.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)\n---------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e)\n---------------------^^^\n')
doris_error_code=1105
```

### pg-join-0031-f4169150 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT t1.a, t2.e
  FROM J1_TBL t1 (a, b, c), J2_TBL t2 (d, e)
  WHERE t1.a = t2.d;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：a: unknown / 原生类型未知, e: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    ""
  ],
  [
    "1",
    "-1"
  ],
  [
    "2",
    "2"
  ],
  [
    "2",
    "4"
  ],
  [
    "3",
    "-3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 18.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 30)\n\n== SQL ==\nSELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d\n------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 30)\n\n== SQL ==\nSELECT t1.a, t2.e FROM J1_TBL AS t1(a, b, c), J2_TBL AS t2(d, e) WHERE t1.a = t2.d\n------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0033-f5fe6eea — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT i, k, t
  FROM J1_TBL CROSS JOIN J2_TBL;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i, k, t FROM J1_TBL CROSS JOIN J2_TBL
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`column reference "i" is ambiguous`。

错误原文：

```text
column reference "i" is ambiguous
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = i is ambiguous: i#0, i#3.')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-join-0035-06b3f865 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ii, tt, kk
  FROM (J1_TBL CROSS JOIN J2_TBL)
    AS tx (ii, jj, tt, ii2, kk);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ii, tt, kk FROM (J1_TBL CROSS JOIN J2_TBL) AS tx(ii, jj, tt, ii2, kk)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：99；字段：ii: unknown / 原生类型未知, tt: unknown / 原生类型未知, kk: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "one",
    "-1"
  ],
  [
    "2",
    "two",
    "-1"
  ],
  [
    "3",
    "three",
    "-1"
  ],
  [
    "4",
    "four",
    "-1"
  ],
  [
    "5",
    "five",
    "-1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 50)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 50)\n")
doris_error_code=1105
```

### pg-join-0036-deb1b49d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT tx.ii, tx.jj, tx.kk
  FROM (J1_TBL t1 (a, b, c) CROSS JOIN J2_TBL t2 (d, e))
    AS tx (ii, jj, tt, ii2, kk);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT tx.ii, tx.jj, tx.kk FROM (J1_TBL AS t1(a, b, c) CROSS JOIN J2_TBL AS t2(d, e)) AS tx(ii, jj, tt, ii2, kk)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：99；字段：ii: unknown / 原生类型未知, jj: unknown / 原生类型未知, kk: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "4",
    "-1"
  ],
  [
    "2",
    "3",
    "-1"
  ],
  [
    "3",
    "2",
    "-1"
  ],
  [
    "4",
    "1",
    "-1"
  ],
  [
    "5",
    "0",
    "-1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 86)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 86)\n")
doris_error_code=1105
```

### pg-join-0040-a96d716e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, d) USING (a)
  ORDER BY a, d;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知, d: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "1",
    "4",
    "one",
    "-1"
  ],
  [
    "2",
    "3",
    "two",
    "2"
  ],
  [
    "2",
    "3",
    "two",
    "4"
  ],
  [
    "3",
    "2",
    "three",
    "-3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d\n---------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, d) USING (a) ORDER BY CASE WHEN a IS NULL THEN 1 ELSE 0 END, a, CASE WHEN d IS NULL THEN 1 ELSE 0 END, d\n---------------------^^^\n')
doris_error_code=1105
```

### pg-join-0041-6acaaacd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c) JOIN J2_TBL t2 (a, b) USING (b)
  ORDER BY b, t1.a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：b: unknown / 原生类型未知, a: unknown / 原生类型未知, c: unknown / 原生类型未知, a: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "5",
    "five",
    ""
  ],
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "2",
    "3",
    "three",
    "2"
  ],
  [
    "4",
    "1",
    "one",
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a\n---------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 21)\n\n== SQL ==\nSELECT * FROM J1_TBL AS t1(a, b, c) JOIN J2_TBL AS t2(a, b) USING (b) ORDER BY CASE WHEN b IS NULL THEN 1 ELSE 0 END, b, CASE WHEN t1.a IS NULL THEN 1 ELSE 0 END, t1.a\n---------------------^^^\n')
doris_error_code=1105
```

### pg-join-0044-77d9c458 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT * FROM (J1_TBL JOIN J2_TBL USING (i)) AS x WHERE J1_TBL.t = 'one';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (J1_TBL JOIN J2_TBL USING (i)) AS x WHERE J1_TBL.t = 'one'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid reference to FROM-clause entry for table "j1_tbl"`。

错误原文：

```text
invalid reference to FROM-clause entry for table "j1_tbl"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 18.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'AS' expecting {<EOF>, ';'}(line 1, pos 45)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-join-0052-38f1da35 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL NATURAL JOIN J2_TBL;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL NATURAL JOIN J2_TBL
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：i: unknown / 原生类型未知, j: unknown / 原生类型未知, t: unknown / 原生类型未知, k: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "1",
    "4",
    "one",
    "-1"
  ],
  [
    "2",
    "3",
    "two",
    "2"
  ],
  [
    "2",
    "3",
    "two",
    "4"
  ],
  [
    "3",
    "2",
    "three",
    "-3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 21)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 21)\n")
doris_error_code=1105
```

### pg-join-0053-7ab78474 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (a, d);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c) NATURAL JOIN J2_TBL AS t2(a, d)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知, d: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "1",
    "4",
    "one",
    "-1"
  ],
  [
    "2",
    "3",
    "two",
    "2"
  ],
  [
    "2",
    "3",
    "two",
    "4"
  ],
  [
    "3",
    "2",
    "three",
    "-3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-join-0054-8499874b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b, c) NATURAL JOIN J2_TBL t2 (d, a);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b, c) NATURAL JOIN J2_TBL AS t2(d, a)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, c: unknown / 原生类型未知, d: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "2",
    "3",
    "two",
    "2"
  ],
  [
    "4",
    "1",
    "four",
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-join-0055-e0343680 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT *
  FROM J1_TBL t1 (a, b) NATURAL JOIN J2_TBL t2 (a);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM J1_TBL AS t1(a, b) NATURAL JOIN J2_TBL AS t2(a)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：7；字段：a: unknown / 原生类型未知, b: unknown / 原生类型未知, t: unknown / 原生类型未知, k: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "",
    "zero",
    ""
  ],
  [
    "1",
    "4",
    "one",
    "-1"
  ],
  [
    "2",
    "3",
    "two",
    "2"
  ],
  [
    "2",
    "3",
    "two",
    "4"
  ],
  [
    "3",
    "2",
    "three",
    "-3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 33)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 33)\n")
doris_error_code=1105
```

### pg-join-0078-ff5cfabb — 返回记录行数不同

#### 源 SQL

```sql
SELECT * FROM t1 FULL JOIN t2 USING (name) FULL JOIN t3 USING (name);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM t1 FULL JOIN t2 USING (`name`) FULL JOIN t3 USING (`name`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：name: unknown / 原生类型未知, n: unknown / 原生类型未知, n: unknown / 原生类型未知, n: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "11",
    "12",
    "13"
  ],
  [
    "cc",
    "",
    "22",
    "23"
  ],
  [
    "dd",
    "",
    "",
    "33"
  ],
  [
    "ee",
    "",
    "42",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 25.3 ms。
- 返回行数：5；字段：name: string / STRING, n: integer / INT, n: integer / INT, n: integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    null,
    null,
    42,
    null
  ],
  [
    null,
    null,
    22,
    null
  ],
  [
    null,
    null,
    null,
    23
  ],
  [
    null,
    null,
    null,
    33
  ],
  [
    "bb",
    11,
    12,
    13
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Result row counts differ
source=4
doris=5
```

### pg-join-0081-1853c44b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT * FROM
(SELECT * FROM t2) as s2
FULL JOIN
(SELECT * FROM t3) s3
USING (name);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT * FROM t2) AS s2 LEFT JOIN (SELECT * FROM t3) AS `s3` USING (`name`) UNION ALL SELECT * FROM (SELECT * FROM t2) AS s2 RIGHT JOIN (SELECT * FROM t3) AS `s3` USING (`name`) WHERE NOT EXISTS(SELECT 1 FROM (SELECT * FROM t2) AS s2 WHERE s2.`name` = `s3`.`name`)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：name: unknown / 原生类型未知, n: unknown / 原生类型未知, n: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "12",
    "13"
  ],
  [
    "cc",
    "22",
    "23"
  ],
  [
    "dd",
    "",
    "33"
  ],
  [
    "ee",
    "42",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 31.5 ms。
- 返回行数：4；字段：name: string / STRING, n: integer / INT, n: integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    12,
    13
  ],
  [
    "cc",
    22,
    23
  ],
  [
    "ee",
    42,
    null
  ],
  [
    null,
    null,
    33
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

### pg-join-0082-ede1f502 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL INNER JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL INNER JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：2；字段：name: unknown / 原生类型未知, s2_n: unknown / 原生类型未知, s2_2: unknown / 原生类型未知, s3_n: unknown / 原生类型未知, s3_2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "12",
    "2",
    "13",
    "3"
  ],
  [
    "cc",
    "22",
    "2",
    "23",
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
doris_error_code=1105
```

### pg-join-0083-ad25c0f2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL LEFT JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL LEFT JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：name: unknown / 原生类型未知, s2_n: unknown / 原生类型未知, s2_2: unknown / 原生类型未知, s3_n: unknown / 原生类型未知, s3_2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "12",
    "2",
    "13",
    "3"
  ],
  [
    "cc",
    "22",
    "2",
    "23",
    "3"
  ],
  [
    "ee",
    "42",
    "2",
    "",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
doris_error_code=1105
```

### pg-join-0084-d692d7c3 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL FULL JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
```

#### SQLGlot 转译错误原文

```text
TypeError: 'NoneType' object is not iterable
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-join-0085-8f120375 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1
NATURAL INNER JOIN
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL INNER JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT `name`, n AS s1_n, 1 AS s1_1 FROM t1) AS s1 NATURAL INNER JOIN (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL INNER JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：name: unknown / 原生类型未知, s1_n: unknown / 原生类型未知, s1_1: unknown / 原生类型未知, s2_n: unknown / 原生类型未知, s2_2: unknown / 原生类型未知, s3_n: unknown / 原生类型未知, s3_2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "11",
    "1",
    "12",
    "2",
    "13",
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
doris_error_code=1105
```

### pg-join-0086-8e4f7296 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s1_n, 1 as s1_1 FROM t1) as s1
NATURAL FULL JOIN
(SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
NATURAL FULL JOIN
(SELECT name, n as s3_n, 3 as s3_2 FROM t3) s3;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT `name`, n AS s1_n, 1 AS s1_1 FROM t1) AS s1 NATURAL FULL JOIN (SELECT `name`, n AS s2_n, 2 AS s2_2 FROM t2) AS s2 NATURAL FULL JOIN (SELECT `name`, n AS s3_n, 3 AS s3_2 FROM t3) AS `s3`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：name: unknown / 原生类型未知, s1_n: unknown / 原生类型未知, s1_1: unknown / 原生类型未知, s2_n: unknown / 原生类型未知, s2_2: unknown / 原生类型未知, s3_n: unknown / 原生类型未知, s3_2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "bb",
    "11",
    "1",
    "12",
    "2",
    "13",
    "3"
  ],
  [
    "cc",
    "",
    "",
    "22",
    "2",
    "23",
    "3"
  ],
  [
    "dd",
    "",
    "",
    "",
    "",
    "33",
    "3"
  ],
  [
    "ee",
    "",
    "",
    "42",
    "2",
    "",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'NATURAL' expecting {<EOF>, ';'}(line 1, pos 66)\n")
doris_error_code=1105
```

### pg-join-0087-f13d67d0 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s1_n FROM t1) as s1
NATURAL FULL JOIN
  (SELECT * FROM
    (SELECT name, n as s2_n FROM t2) as s2
    NATURAL FULL JOIN
    (SELECT name, n as s3_n FROM t3) as s3
  ) ss2;
```

#### SQLGlot 转译错误原文

```text
TypeError: 'NoneType' object is not iterable
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-join-0088-9518261f — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT * FROM
(SELECT name, n as s1_n FROM t1) as s1
NATURAL FULL JOIN
  (SELECT * FROM
    (SELECT name, n as s2_n, 2 as s2_2 FROM t2) as s2
    NATURAL FULL JOIN
    (SELECT name, n as s3_n FROM t3) as s3
  ) ss2;
```

#### SQLGlot 转译错误原文

```text
TypeError: 'NoneType' object is not iterable
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-join-0105-7b5454e9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "3",
    "",
    "3",
    "333",
    "3",
    ""
  ],
  [
    "4",
    "44",
    "4",
    "",
    "4",
    "44"
  ],
  [
    "5",
    "",
    "",
    "",
    "5",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0106-19118909 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and x2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "3",
    "",
    "3",
    "333",
    "",
    ""
  ],
  [
    "4",
    "44",
    "4",
    "",
    "4",
    "44"
  ],
  [
    "5",
    "",
    "",
    "",
    "",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0107-cd1a2740 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and y2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "3",
    "",
    "3",
    "333",
    "3",
    ""
  ],
  [
    "4",
    "44",
    "4",
    "",
    "",
    ""
  ],
  [
    "5",
    "",
    "",
    "",
    "",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0108-29622a8a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1 and xx2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "3",
    "",
    "3",
    "333",
    "",
    ""
  ],
  [
    "4",
    "44",
    "4",
    "",
    "4",
    "44"
  ],
  [
    "5",
    "",
    "",
    "",
    "",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1 AND xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0109-9c15a804 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (x2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "4",
    "44",
    "4",
    "",
    "4",
    "44"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (x2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0110-bacb7b5f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (y2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "3",
    "",
    "3",
    "333",
    "3",
    ""
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (y2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```

### pg-join-0111-f8035c11 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select * from (x left join y on (x1 = y1)) left join x xx(xx1,xx2)
on (x1 = xx1) where (xx2 is not null);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：x1: unknown / 原生类型未知, x2: unknown / 原生类型未知, y1: unknown / 原生类型未知, y2: unknown / 原生类型未知, xx1: unknown / 原生类型未知, xx2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "11",
    "1",
    "111",
    "1",
    "11"
  ],
  [
    "2",
    "22",
    "2",
    "222",
    "2",
    "22"
  ],
  [
    "4",
    "44",
    "4",
    "",
    "4",
    "44"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nDo not implemented(line 1, pos 55)\n\n== SQL ==\nSELECT * FROM (x LEFT JOIN y ON (x1 = y1)) LEFT JOIN x AS xx(xx1, xx2) ON (x1 = xx1) WHERE (xx2 IS NOT NULL)\n-------------------------------------------------------^^^\n')
doris_error_code=1105
```
