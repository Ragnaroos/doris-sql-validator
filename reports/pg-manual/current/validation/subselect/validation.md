# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:19.730674+00:00 至 2026-11-11T09:40:20.566195+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/subselect.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**32**；两端成功且已有证据匹配：**19**。
- 成功结果匹配占全部查询比例：**19/32 = 59.38%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**19/28 = 67.86%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**1**；不计入上述成功匹配分子。
- 需要分析的查询：**13**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**3**；源参考结果不可用：**0**；Doris 执行失败：**7**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 6 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 19 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 3 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 3 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 32 条只读查询、跳过 367 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 14 | 28–34 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 15 | 36–36 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 37–37 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 17 | 38–38 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 39–39 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 19 | 40–40 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 41–41 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 21 | 42–42 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 22 | 43–43 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 32 | 85–88 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 34 | 92–93 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 40 | 106–109 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 42 | 113–115 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 43 | 117–122 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 44 | 124–126 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 48 | 145–147 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 49 | 148–148 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 50 | 150–152 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 52 | 155–160 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 53 | 161–163 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 54 | 164–166 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 59 | 186–192 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 60 | 193–193 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 61 | 195–195 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 62 | 197–197 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 63 | 198–198 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 64 | 199–199 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 71 | 219–228 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 72 | 230–230 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 73 | 231–231 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 232–232 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 75 | 233–233 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 234–234 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 77 | 235–235 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 78 | 236–236 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 79 | 237–237 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 80 | 238–238 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 81 | 239–239 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 82 | 240–240 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 83 | 242–277 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 85 | 281–281 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 86 | 283–291 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 87 | 293–298 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 88 | 300–301 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 89 | 303–304 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 90 | 306–306 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 91 | 308–309 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 93 | 313–315 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 94 | 317–320 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 101 | 354–363 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 102 | 364–364 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 103 | 366–366 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 104 | 367–367 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 107 | 375–380 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 108 | 381–381 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 109 | 382–382 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 111 | 385–389 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 112 | 391–395 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 113 | 397–398 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 114 | 399–399 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 115 | 400–400 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 116 | 401–401 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 117 | 403–403 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 118 | 405–409 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 119 | 411–411 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 120 | 413–413 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 121 | 414–414 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 122 | 415–415 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 123 | 416–416 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 124 | 418–418 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 125 | 420–420 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 126 | 421–421 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 127 | 422–422 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 128 | 423–423 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 129 | 424–424 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 130 | 425–425 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 131 | 426–426 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 132 | 427–427 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 134 | 430–430 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 135 | 432–438 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 136 | 440–440 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 137 | 442–442 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 138 | 444–448 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 139 | 450–450 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 140 | 451–451 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 141 | 453–453 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 142 | 455–455 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 143 | 456–456 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 144 | 457–457 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 145 | 458–458 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 146 | 460–460 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 147 | 462–462 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 148 | 463–463 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 150 | 470–474 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 152 | 481–485 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 153 | 486–486 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 154 | 488–488 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 159 | 495–500 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 164 | 518–527 | 跳过非查询；类型 `delete` | Expected one read-only Query, got Delete |
| 170 | 555–558 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 171 | 559–559 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 172 | 560–560 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 175 | 569–573 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 176 | 574–574 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 177 | 575–575 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 178 | 576–576 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 179 | 577–577 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 180 | 579–579 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 181 | 580–580 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 183 | 584–590 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 184 | 591–591 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 185 | 592–592 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 186 | 593–593 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 187 | 594–594 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 188 | 596–596 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 189 | 597–597 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 190 | 598–598 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 192 | 602–608 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 194 | 612–618 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 199 | 638–640 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 200 | 642–642 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 201 | 644–645 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 203 | 648–651 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 204 | 653–654 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 206 | 657–660 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 207 | 662–663 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 210 | 666–673 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 212 | 677–680 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 214 | 685–686 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 215 | 687–687 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 216 | 688–688 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 217 | 689–689 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 219 | 691–693 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 222 | 706–711 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 223 | 712–714 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 224 | 715–717 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 225 | 718–720 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 226 | 722–732 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 228 | 741–748 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 231 | 758–758 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 232 | 760–767 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 236 | 783–783 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 237 | 785–792 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 240 | 804–817 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 242 | 830–833 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 243 | 834–834 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 244 | 835–835 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 246 | 839–842 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 249 | 855–861 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 251 | 869–875 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 253 | 880–885 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 256 | 899–913 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 258 | 925–929 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 261 | 938–947 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 262 | 949–952 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 264 | 958–959 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 265 | 961–964 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 267 | 970–974 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 269 | 980–987 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 271 | 993–997 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 272 | 999–1002 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 274 | 1008–1009 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 275 | 1011–1014 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 277 | 1020–1020 | 跳过非查询；类型 `drop` | Expecting ). Line 1, Col: 26.   drop function tattle(x [4mint[0m, y int);  Invalid expression / Unexpected token. Line 1, Col: 26.   drop function tattle(x [4mint[0m, y int); |
| 279 | 1028–1028 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 280 | 1029–1029 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 281 | 1030–1033 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 282 | 1035–1038 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 284 | 1043–1048 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 286 | 1055–1057 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 288 | 1061–1064 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 290 | 1069–1073 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 291 | 1075–1078 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 292 | 1080–1082 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 293 | 1083–1083 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 294 | 1084–1084 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 295 | 1085–1085 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 296 | 1087–1090 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 298 | 1095–1098 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 300 | 1103–1106 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 302 | 1111–1119 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 304 | 1128–1131 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 307 | 1138–1144 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 308 | 1145–1153 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 309 | 1155–1167 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 312 | 1173–1173 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 313 | 1175–1175 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 320 | 1200–1200 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 321 | 1201–1201 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 322 | 1203–1204 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 325 | 1210–1220 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 327 | 1228–1235 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 329 | 1244–1250 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 331 | 1259–1267 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 333 | 1276–1283 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 335 | 1292–1300 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 337 | 1309–1316 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 339 | 1325–1334 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 341 | 1344–1352 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 343 | 1362–1369 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 344 | 1371–1374 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 345 | 1376–1379 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 346 | 1381–1384 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 347 | 1386–1389 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 348 | 1391–1394 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 349 | 1396–1398 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 350 | 1400–1408 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 352 | 1418–1425 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 354 | 1435–1438 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 355 | 1440–1442 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 356 | 1444–1448 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 357 | 1450–1453 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 358 | 1455–1457 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 359 | 1459–1463 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 360 | 1465–1469 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 361 | 1471–1475 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 362 | 1477–1480 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 363 | 1482–1486 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 364 | 1488–1491 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 365 | 1493–1500 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 366 | 1502–1506 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 367 | 1508–1511 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 368 | 1513–1515 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 369 | 1517–1520 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 370 | 1522–1523 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 371 | 1525–1526 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 372 | 1528–1529 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 373 | 1531–1534 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 374 | 1535–1537 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 375 | 1539–1541 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 376 | 1542–1545 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 378 | 1552–1552 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 379 | 1553–1553 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 380 | 1554–1554 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 381 | 1555–1555 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 382 | 1556–1556 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 383 | 1557–1557 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 384 | 1559–1561 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 385 | 1562–1563 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 386 | 1564–1565 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 387 | 1567–1570 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 388 | 1572–1575 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 389 | 1577–1581 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 390 | 1583–1585 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 391 | 1586–1587 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 392 | 1589–1591 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 394 | 1601–1601 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 395 | 1602–1602 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 396 | 1604–1607 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 397 | 1609–1612 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 398 | 1614–1617 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 399 | 1619–1623 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 400 | 1625–1629 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 401 | 1631–1639 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 402 | 1641–1648 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 403 | 1650–1659 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 404 | 1661–1670 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 405 | 1672–1681 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 406 | 1683–1688 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 407 | 1690–1694 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 408 | 1696–1701 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 409 | 1703–1708 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 410 | 1710–1713 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 411 | 1715–1718 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 412 | 1720–1723 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 413 | 1725–1728 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 414 | 1730–1733 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 415 | 1735–1737 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 416 | 1739–1743 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 417 | 1745–1748 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 418 | 1750–1757 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 419 | 1759–1763 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 420 | 1765–1769 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 421 | 1771–1774 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 422 | 1776–1778 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 423 | 1779–1779 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 424 | 1780–1780 | 跳过非查询；类型 `alter` | Expected one read-only Query, got Command |
| 425 | 1782–1784 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 427 | 1790–1792 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 428 | 1793–1793 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 429 | 1795–1798 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 431 | 1805–1809 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 432 | 1810–1810 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 433 | 1811–1811 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 434 | 1813–1815 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 8 | 19–19 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 33 | 90–90 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 35 | 95–95 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 37 | 97–101 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 38 | 102–102 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 41 | 111–111 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 47 | 140–143 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 51 | 153–153 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 68 | 210–212 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 69 | 213–214 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 215–217 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 84 | 279–279 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 92 | 311–311 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 95 | 322–322 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 324–326 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 328–336 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 338–341 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 344–350 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 351–351 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 105 | 369–370 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 106 | 372–373 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 149 | 465–468 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 151 | 476–479 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 155 | 490–490 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 156 | 491–491 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 157 | 492–492 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 158 | 493–493 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 160 | 502–502 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 161 | 504–509 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 162 | 510–511 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 166 | 531–541 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 167 | 543–546 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 168 | 548–549 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 173 | 562–562 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 182 | 582–582 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 191 | 600–600 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 193 | 610–610 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 195 | 620–620 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 196 | 622–626 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 197 | 628–634 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 202 | 646–646 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 205 | 655–655 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 208 | 664–664 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 211 | 674–675 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 213 | 681–683 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 220 | 694–695 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 221 | 697–704 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 227 | 734–739 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 229 | 750–752 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 233 | 769–775 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 238 | 794–800 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 241 | 819–828 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 245 | 837–837 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 247 | 843–843 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 248 | 845–853 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 250 | 863–867 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 252 | 876–878 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 254 | 886–887 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 255 | 889–897 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 257 | 915–923 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 259 | 931–934 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 260 | 936–936 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 263 | 954–956 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 266 | 966–968 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 268 | 976–978 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 270 | 989–991 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 273 | 1004–1006 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 276 | 1016–1018 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 289 | 1066–1067 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 310 | 1169–1169 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 323 | 1206–1206 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 326 | 1222–1226 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 328 | 1237–1242 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 330 | 1252–1257 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 332 | 1269–1274 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 334 | 1285–1290 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 336 | 1302–1307 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 338 | 1318–1323 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 340 | 1336–1342 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 342 | 1354–1360 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 426 | 1786–1788 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 430 | 1800–1803 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/subselect.out`；SHA-256（文件内容指纹）：`290b2629f0d9c1cda09d7ebb2d8e9c435b23464746fa6efdf01aa9435e16c12f`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 29/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 29/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 28/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 28/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 28/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/29 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-subselect-0001-648f9c3b` | SELECT 1 AS one WHERE 1 IN (SELECT 1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0002-a346e17e` | SELECT 1 AS zero WHERE 1 NOT IN (SELECT 1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0003-cab8488e` | SELECT 1 AS zero WHERE 1 IN (SELECT 2); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0004-cd72644a` | SELECT * FROM (SELECT 1 AS x) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0005-957b739b` | SELECT * FROM ((SELECT 1 AS x)) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0006-05402195` | SELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y)))); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0007-802e47b9` | (SELECT 2) UNION SELECT 2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0009-6719b6f9` | SELECT ((SELECT 2) UNION SELECT 2); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0010-6011b123` | SELECT (((SELECT 2)) UNION SELECT 2); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0011-ba931994` | SELECT (SELECT ARRAY[1,2,3])[1]; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-subselect-0012-a01c4e7d` | SELECT ((SELECT ARRAY[1,2,3]))[2]; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-subselect-0013-9ff200d9` | SELECT (((SELECT ARRAY[1,2,3])))[3]; | 失败 | 未取得（可能因转译先失败） | 未取得执行结果 | SQLGlot 解析或生成失败 |
| `pg-subselect-0023-c39da2ba` | SELECT * FROM SUBSELECT_TBL; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-subselect-0024-3a618e44` | SELECT f1 AS "Constant Select" FROM SUBSELECT_TBL   WHERE f1 IN (SELECT 1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0025-e1d3981a` | SELECT f1 AS "Uncorrelated Field" FROM SUBSELECT_TBL   WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0026-630c97f8` | SELECT f1 AS "Uncorrelated Field" FROM SUBSELECT_TBL   WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE     f2 IN (SELECT f1 FROM SUBSELECT_TBL)); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0027-ce6bb68f` | SELECT f1, f2   FROM SUBSELECT_TBL   WHERE (f1, f2) NOT IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL                          WHERE f3 IS NOT NULL); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0028-5b8190e4` | SELECT f1 AS "Correlated Field", f2 AS "Second Field"   FROM SUBSELECT_TBL upper   WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE f1 = upper.f1); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0029-428204b5` | SELECT f1 AS "Correlated Field", f3 AS "Second Field"   FROM SUBSELECT_TBL upper   WHERE f1 IN     (SELECT f2 FROM SUBSELECT_TBL WHERE CAST(upper.f2 AS float) = f3); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-subselect-0030-9a523825` | SELECT f1 AS "Correlated Field", f3 AS "Second Field"   FROM SUBSELECT_TBL upper   WHERE f3 IN (SELECT upper.f1 + f2 FROM SUBSELECT_TBL                WHERE f2 = CAST(f3 AS integer)); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0031-e04f71f1` | SELECT f1 AS "Correlated Field"   FROM SUBSELECT_TBL   WHERE (f1, f2) IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL                      WHERE f3 IS NOT NULL); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0036-11fbffbc` | SELECT ROW(1, 2) = (SELECT f1, f2 FROM SUBSELECT_TBL); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：语法解析失败 | 两端均报错，但错误类别不同 |
| `pg-subselect-0039-b3693cb9` | SELECT * FROM (SELECT * FROM int4_tbl), (VALUES (123456)) WHERE f1 = column1; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0045-76d8e38c` | SELECT ss.f1 AS "Correlated Field", ss.f3 AS "Second Field"   FROM SUBSELECT_TBL ss   WHERE f1 NOT IN (SELECT f1+1 FROM INT4_TBL                    WHERE f1 != ss.f1 AND f1 < 2147483647); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-subselect-0046-b39798f6` | select q1, float8(count(*)) / (select count(*) from int8_tbl) from int8_tbl group by q1 order by q1; | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-subselect-0055-7c7828a4` | select count(*) from   (select 1 from tenk1 a    where unique1 IN (select hundred from tenk1 b)) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0056-ee71a780` | select count(distinct ss.ten) from   (select ten from tenk1 a    where unique1 IN (select hundred from tenk1 b)) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0057-bf8e16fa` | select count(*) from   (select 1 from tenk1 a    where unique1 IN (select distinct hundred from tenk1 b)) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0058-4e6efae7` | select count(distinct ss.ten) from   (select ten from tenk1 a    where unique1 IN (select distinct hundred from tenk1 b)) ss; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0065-a003a0ef` | SELECT * FROM foo WHERE id IN     (SELECT id2 FROM (SELECT DISTINCT id1, id2 FROM bar) AS s); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0066-4489c239` | SELECT * FROM foo WHERE id IN     (SELECT id2 FROM (SELECT id1,id2 FROM bar GROUP BY id1,id2) AS s); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-subselect-0067-e7b8bde2` | SELECT * FROM foo WHERE id IN     (SELECT id2 FROM (SELECT id1, id2 FROM bar UNION                       SELECT id1, id2 FROM bar) AS s); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |

## 4. 不匹配、执行失败及负向错误详情

### pg-subselect-0006-05402195 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：x: unknown / 原生类型未知, y: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))\n--------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM ((SELECT 1 AS x)), ((SELECT * FROM ((SELECT 2 AS y))))\n--------------^^^\n')
doris_error_code=1105
```

### pg-subselect-0011-ba931994 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT (SELECT ARRAY[1,2,3])[1];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-subselect-0012-a01c4e7d — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT ((SELECT ARRAY[1,2,3]))[2];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-subselect-0013-9ff200d9 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT (((SELECT ARRAY[1,2,3])))[3];
```

#### SQLGlot 转译错误原文

```text
UnsupportedError: Arrays are not supported by MySQL
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-subselect-0023-c39da2ba — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT * FROM SUBSELECT_TBL;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM SUBSELECT_TBL
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：8；字段：f1: unknown / 原生类型未知, f2: unknown / 原生类型未知, f3: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "2",
    "3"
  ],
  [
    "2",
    "3",
    "4"
  ],
  [
    "3",
    "4",
    "5"
  ],
  [
    "1",
    "1",
    "1"
  ],
  [
    "2",
    "2",
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 20.2 ms。
- 返回行数：8；字段：f1: integer / INT, f2: integer / INT, f3: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1,
    1,
    1.0
  ],
  [
    1,
    2,
    3.0
  ],
  [
    2,
    2,
    2.0
  ],
  [
    2,
    3,
    4.0
  ],
  [
    3,
    3,
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

### pg-subselect-0027-ce6bb68f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT f1, f2
  FROM SUBSELECT_TBL
  WHERE (f1, f2) NOT IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL
                         WHERE f3 IS NOT NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT f1, f2 FROM SUBSELECT_TBL WHERE NOT (f1, f2) IN (SELECT f2, CAST(f3 AS INT) FROM SUBSELECT_TBL WHERE f3 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：3；字段：f1: unknown / 原生类型未知, f2: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "2"
  ],
  [
    "6",
    "7"
  ],
  [
    "8",
    "9"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 46)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-subselect-0029-428204b5 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT f1 AS "Correlated Field", f3 AS "Second Field"
  FROM SUBSELECT_TBL upper
  WHERE f1 IN
    (SELECT f2 FROM SUBSELECT_TBL WHERE CAST(upper.f2 AS float) = f3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT f1 AS `Correlated Field`, f3 AS `Second Field` FROM SUBSELECT_TBL AS upper WHERE f1 IN (SELECT f2 FROM SUBSELECT_TBL WHERE CAST(upper.f2 AS DOUBLE) = f3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：Correlated Field: unknown / 原生类型未知, Second Field: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2",
    "4"
  ],
  [
    "3",
    "5"
  ],
  [
    "1",
    "1"
  ],
  [
    "2",
    "2"
  ],
  [
    "3",
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 24.5 ms。
- 返回行数：5；字段：Correlated Field: integer / INT, Second Field: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1,
    1.0
  ],
  [
    2,
    2.0
  ],
  [
    2,
    4.0
  ],
  [
    3,
    3.0
  ],
  [
    3,
    5.0
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

### pg-subselect-0030-9a523825 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT f1 AS "Correlated Field", f3 AS "Second Field"
  FROM SUBSELECT_TBL upper
  WHERE f3 IN (SELECT upper.f1 + f2 FROM SUBSELECT_TBL
               WHERE f2 = CAST(f3 AS integer));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT f1 AS `Correlated Field`, f3 AS `Second Field` FROM SUBSELECT_TBL AS upper WHERE f3 IN (SELECT upper.f1 + f2 FROM SUBSELECT_TBL WHERE f2 = CAST(f3 AS INT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：4；字段：Correlated Field: unknown / 原生类型未知, Second Field: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "3"
  ],
  [
    "2",
    "4"
  ],
  [
    "3",
    "5"
  ],
  [
    "6",
    "8"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 16.0 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Input slot(s) not in child's output: f1#0 in plan: LogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\nchild output is: [f1#3, f2#4, f3#5]\nplan tree:\nLogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\n+--LogicalFilter[231] ( predicates=(f2#4 = cast(f3#5 as INT)) )\n   +--LogicalOlapScan ( qualified=internal.dsv_pg_manual_20261111.subselect_tbl, indexName=<index_not_selected>, selectedIndexId=1791536387852, preAgg=ON, operativeCol=[], virtualColumns=[] )")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Input slot(s) not in child's output: f1#0 in plan: LogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\nchild output is: [f1#3, f2#4, f3#5]\nplan tree:\nLogicalProject[232] ( distinct=false, projects=[cast((cast(f1#0 as BIGINT) + cast(f2#4 as BIGINT)) as DOUBLE) AS `expr_cast(upper.f1 + f2 as DOUBLE)`#10] )\n+--LogicalFilter[231] ( predicates=(f2#4 = cast(f3#5 as INT)) )\n   +--LogicalOlapScan ( qualified=internal.dsv_pg_manual_20261111.subselect_tbl, indexName=<index_not_selected>, selectedIndexId=1791536387852, preAgg=ON, operativeCol=[], virtualColumns=[] )")
doris_error_code=1105
```

### pg-subselect-0031-e04f71f1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT f1 AS "Correlated Field"
  FROM SUBSELECT_TBL
  WHERE (f1, f2) IN (SELECT f2, CAST(f3 AS int4) FROM SUBSELECT_TBL
                     WHERE f3 IS NOT NULL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT f1 AS `Correlated Field` FROM SUBSELECT_TBL WHERE (f1, f2) IN (SELECT f2, CAST(f3 AS INT) FROM SUBSELECT_TBL WHERE f3 IS NOT NULL)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：Correlated Field: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ],
  [
    "3"
  ],
  [
    "1"
  ],
  [
    "2"
  ],
  [
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 60)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ',' expecting {')', '.', '[', 'AND', 'BETWEEN', 'COLLATE', 'DIV', 'IN', 'IS', 'LIKE', 'MATCH', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'NOT', 'OR', 'REGEXP', 'RLIKE', 'XOR', EQ, '<=>', NEQ, '<', LTE, '>', GTE, '+', '-', '*', '/', '%', 'MOD', '&', '&&', '|', '||', '^'}(line 1, pos 60)\n")
doris_error_code=1105
```

### pg-subselect-0036-11fbffbc — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT ROW(1, 2) = (SELECT f1, f2 FROM SUBSELECT_TBL);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ROW(1, 2) = (SELECT f1, f2 FROM SUBSELECT_TBL)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`more than one row returned by a subquery used as an expression`。

错误原文：

```text
more than one row returned by a subquery used as an expression
```

#### Doris 实际结果

- 执行状态：失败：语法解析失败；耗时 11.3 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 7)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=more than one row returned by a subquery used as an expression
source_error_code=more than one row returned by a subquery used as an expression
doris_error_category=PARSE_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input 'ROW' expecting {'(', '[', '{', '}', 'ACTIONS', 'ADD', 'AFTER', 'AGG_STATE', 'AGGREGATE', 'ALIAS', 'ALL', 'ANALYZED', 'ARRAY', 'AT', 'AUTHORS', 'AUTHENTICATION', 'AUTO_INCREMENT', 'ALWAYS', 'BACKENDS', 'BACKUP', 'BEGIN', 'BELONG', 'BIN', 'BINARY', 'BITAND', 'BITMAP', 'BITMAP_EMPTY', 'BITMAP_UNION', 'BITOR', 'BITXOR', 'BLOB', 'BOOLEAN', 'BRANCH', 'BRIEF', 'BROKER', 'BUCKETS', 'BUILD', 'BUILTIN', 'BULK', 'CACHE', 'CACHED', 'CALL', 'CANCEL', 'CASE', 'CAST', 'CATALOG', 'CATALOGS', 'CEL', 'CHAIN', 'CIPHER', CHAR, 'CHARSET', 'CHECK', 'CLUSTER', 'CLUSTERS', 'COLLATION', 'COLLECT', 'COLOCATE', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETE', 'COMPRESS_TYPE', 'COMPUTE', 'CONDITIONS', 'CONFIG', 'CONNECTION', 'CONNECTION_ID', 'CONSISTENT', 'CONSTRAINTS', 'CONVERT', 'CONVERT_LIGHT_SCHEMA_CHANGE_PROCESS', 'COPY', 'COUNT', 'CREATION', 'CRON', 'CURRENT_CATALOG', 'CURRENT_DATE', 'CURRENT_TIME', 'CURRENT_TIMESTAMP', 'CURRENT_USER', 'DATA', 'DATABASE', 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAYS', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DEFERRED', 'DEMAND', 'DIAGNOSE', 'DIAGNOSIS', 'DICTIONARIES', 'DICTIONARY', 'DISTINCT', 'DISTINCTPC', 'DISTINCTPCSA', 'DO', 'DORIS_INTERNAL_TABLE_ID', 'DOW', 'DOY', 'DUAL', 'DYNAMIC', 'E', 'ENABLE', 'ENCRYPTION', 'ENCRYPTKEY', 'ENCRYPTKEYS', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ERRORS', 'ESCAPE', 'EVENTS', 'EVERY', 'EXCLUDE', 'EXISTS', 'EXPIRED', 'EXTERNAL', 'EXTRACT', 'FAILED_LOGIN_ATTEMPTS', 'FALSE', 'FAST', 'FEATURE', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FORMAT', 'FREE', 'FRONTENDS', 'FUNCTION', 'GENERATED', 'GENERIC', 'GLOBAL', 'GRAPH', 'GROUPING', 'GROUPS', 'GROUP_CONCAT', 'HASH', 'HASH_MAP', 'HDFS', 'HELP', 'HISTOGRAM', 'HLL_UNION', 'HOSTNAME', 'HOTSPOT', 'HOUR', 'HOURS', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'HUB', 'IDENTIFIED', 'IF', 'IGNORE', 'IMMEDIATE', 'INCREMENTAL', 'INTEGRATION', 'INCLUDE', 'INDEXES', 'INSERT', 'INTERVAL', 'INVERTED', 'IP_TRIE', 'IPV4', 'IPV6', 'IS_NOT_NULL_PRED', 'IS_NULL_PRED', 'ISNULL', 'ISOLATION', 'ISSUER', 'JOB', 'JOBS', 'JSON', 'JSONB', 'KEY', 'LABEL', 'LAST', 'LDAP', 'LDAP_ADMIN_PASSWORD', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LINES', 'LINK', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCATION', 'LOCK', 'LOGICAL', 'MANUAL', 'MAP', 'MAPPING', 'MATCHED', 'MATCH_ALL', 'MATCH_ANY', 'MATCH_NAME', 'MATCH_NAME_GLOB', 'MATCH_PHRASE', 'MATCH_PHRASE_EDGE', 'MATCH_PHRASE_PREFIX', 'MATCH_REGEXP', 'MATERIALIZED', 'MAX', 'MEMO', 'MERGE', 'MICROSECOND', 'MID', 'MIGRATE', 'MIGRATIONS', 'MIN', 'MINUTE', 'MINUTES', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MODIFY', 'MONTH', 'MTMV', 'NAME', 'NAMES', 'NEGATIVE', 'NEVER', 'NEXT', 'NGRAM_BF', 'ANN', 'NO', 'NONE', 'NON_NULLABLE', 'NORMALIZER', 'NOT', 'NULL', 'NULLS', 'OF', 'OFFSET', 'OFF', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTIMIZED', 'ORDINALITY', 'PARAMETER', 'PARSED', 'PARTITIONS', 'PACKAGES', 'PASSWORD', 'PASSWORD_EXPIRE', 'PASSWORD_HISTORY', 'PASSWORD_LOCK_TIME', 'PASSWORD_REUSE', 'PATH', 'PAUSE', 'PERCENT', 'PERIOD', 'PERMISSIVE', 'PHYSICAL', 'PI', '?', 'PLAN', 'PRIVILEGES', 'PROCESS', 'PYTHON', 'PLUGIN', 'PLUGINS', 'POLICY', 'POSITION', 'PROC', 'PROCESSLIST', 'PROFILE', 'PROPERTIES', 'PROPERTY', 'QUANTILE_STATE', 'QUANTILE_UNION', 'QUERY', 'QUEUED', 'QUOTA', 'QUALIFY', 'QUARTER', 'RANDOM', 'RECENT', 'RECOVER', 'RECURSIVE', 'RECYCLE', 'REFRESH', 'REGEXP', 'REPEATABLE', 'REPLACE', 'REPLACE_IF_NOT_NULL', 'REPLAYER', 'REPOSITORIES', 'REPOSITORY', 'RESOURCE', 'RESOURCES', 'RESTORE', 'RESTRICTIVE', 'RESUME', 'RETAIN', 'RETENTION', 'REQUIRE', 'RETURNS', 'REWRITTEN', 'RIGHT', 'RLIKE', 'ROLLBACK', 'ROLLUP', 'ROOT', 'ROTATE', 'ROUTINE', 'RULE', 'S3', 'SAMPLE', 'SAN', 'SCHEDULE', 'SCHEDULER', 'SCHEMA', 'SECOND', 'SECOND_MICROSECOND', 'SEPARATOR', 'SERIALIZABLE', 'SESSION', 'SESSION_USER', 'SET_SESSION_VARIABLE', 'SHAPE', 'SKEW', 'SNAPSHOT', 'SNAPSHOTS', 'SONAME', 'SPLIT', 'SQL', 'STAGE', 'STAGES', 'START', 'STARTS', 'STATS', 'STATUS', 'STOP', 'STORAGE', 'STREAM', 'STREAMING', 'STRING', 'STRUCT', 'SUBJECT', 'SUBSTR', 'SUBSTRING', 'SUM', 'TABLES', 'TAG', 'TASK', 'TASKS', 'TDE', 'TEMPORARY', 'TEXT', 'THAN', 'TIME', 'TIMESTAMP', 'TIMESTAMPTZ', 'TRANSACTION', 'TREE', 'TRIGGERS', 'TRIM', 'TRUE', 'TRUNCATE', 'TRY_CAST', 'TYPE', 'TYPES', 'UNCOMMITTED', 'UNLOCK', 'UNNEST', 'UNSET', 'UP', 'USER', 'VALUE', 'VARBINARY', 'VARCHAR', 'VARIABLE', 'VARIABLES', 'VARIANT', 'VAULT', 'VAULTS', 'VERBOSE', 'VERSION', 'VERSIONS', 'VIEW', 'VIEWS', 'WARM', 'WARNINGS', 'WEEK', 'WORK', 'YEAR', 'YEAR_MONTH', '+', '-', '*', 'MOD', '~', '!', '/*+', '*/', '/*', '@', '@@', STRING_LITERAL, VARBINARY_LITERAL, INTEGER_VALUE, EXPONENT_VALUE, DECIMAL_VALUE, IDENTIFIER, BACKQUOTED_IDENTIFIER, GET_FORMAT}(line 1, pos 7)\n")
doris_error_code=1105
```

### pg-subselect-0039-b3693cb9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT * FROM (SELECT * FROM int4_tbl), (VALUES (123456)) WHERE f1 = column1;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：f1: unknown / 原生类型未知, column1: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123456",
    "123456"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1\n--------------^^^\n')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 14)\n\n== SQL ==\nSELECT * FROM (SELECT * FROM int4_tbl), (SELECT 123456) WHERE f1 = column1\n--------------^^^\n')
doris_error_code=1105
```

### pg-subselect-0045-76d8e38c — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT ss.f1 AS "Correlated Field", ss.f3 AS "Second Field"
  FROM SUBSELECT_TBL ss
  WHERE f1 NOT IN (SELECT f1+1 FROM INT4_TBL
                   WHERE f1 != ss.f1 AND f1 < 2147483647);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ss.f1 AS `Correlated Field`, ss.f3 AS `Second Field` FROM SUBSELECT_TBL AS ss WHERE NOT f1 IN (SELECT f1 + 1 FROM INT4_TBL WHERE f1 <> ss.f1 AND f1 < 2147483647)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：6；字段：Correlated Field: unknown / 原生类型未知, Second Field: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2",
    "4"
  ],
  [
    "3",
    "5"
  ],
  [
    "2",
    "2"
  ],
  [
    "3",
    "3"
  ],
  [
    "6",
    "8"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 26.9 ms。
- 返回行数：6；字段：Correlated Field: integer / INT, Second Field: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    3,
    3.0
  ],
  [
    3,
    5.0
  ],
  [
    2,
    2.0
  ],
  [
    2,
    4.0
  ],
  [
    6,
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

### pg-subselect-0046-b39798f6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
select q1, float8(count(*)) / (select count(*) from int8_tbl)
from int8_tbl group by q1 order by q1;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT q1, FLOAT8(COUNT(*)) / (SELECT COUNT(*) FROM int8_tbl) FROM int8_tbl GROUP BY q1 ORDER BY CASE WHEN q1 IS NULL THEN 1 ELSE 0 END, q1
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：2；字段：q1: unknown / 原生类型未知, ?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123",
    "0.4"
  ],
  [
    "4567890123456789",
    "0.6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8'")
doris_error_code=1105
```
