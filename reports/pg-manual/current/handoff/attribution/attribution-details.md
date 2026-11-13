# PostgreSQL → Doris：详细归因报告

## 1. 输入与实际完成范围

报告日期：2026-11-13。只按新版 pg-doris-attribute Skill 执行步骤四，不修复代码或准备数据。上一轮步骤四和五的 981 个文件已按要求删除，没有备份；原 SQL/.out/YAML、数据准备、首轮报告、步骤三索引保持不变。

固定 34 组、1,725 条逐条重新读取 .out：源端成功 1,427 条、源端负向 298 条、源端环境/对象前提 0 条、输出读取异常 0 条。成功源查询中，241 条首轮匹配、1,186 条存在差异；本轮选择调查 204 条，982 条尚未逐条独立复核。读取全部记录、保留全部 SQL 不等于完成全量根因分析。

176 个不同主范围 Case 有完整关联对照记录：174 个实际重跑原 SQL，2 个 ORDER BY USING 查询因工具共同 Parser 阻断，只执行了保存的 ASC/DESC 规范化源变体；原文成功证据来自 .out。负向查询默认只说明，不逐条改写；MAKE_DATE 正常输入另作新变体真实执行。

## 2. 版本、环境与数据前提

| 项目 | 本轮实际值 |
| :--- | :--- |
| 社区 SQLGlot | 30.25.1.dev6，feb0e08aba28a29590596bb3f5761fbaeb0e98b9；受版本控制的文件未改 |
| PostgreSQL | 18.1 |
| Doris 实际 FE 版本 | doris-4.1.3-rc02-7126cf65d96；VERSION() 的 5.7.99 是协议兼容返回，不是真实版本 |
| 双端数据库 | dsv_pg_manual_20261111 |
| 时间与格式 | 两端 UTC；PG ISO, MDY、extra_float_digits=0 |
| Doris Session | ONLY_FULL_GROUP_BY；enable_strict_cast=false |
| 数据复核 | 对照前后只读核验 21 张既有表/视图的结构、全部行多重集合和初始指纹；未变化 |
| 类型域限制 | 外部准备的 NAME/TEXT 等到 VARCHAR(512) 映射不是全类型域等价 |

完整前后核验、会话与进度在 [attribution-statistics.json](attribution-statistics.json)。核验由本轮在框架外只读执行，不是新增 Fixture Gate，没有建表、导入、清库或修改原数据。

原入口：[首轮 SUMMARY](../../SUMMARY.md)、[首轮统计](../../validation-summary.json)、[步骤三根索引](../evidence-index.json)。步骤三索引仍是既有 33 组，通过 parser_failure_report_file 指向 select_distinct_on 普通失败报告；本轮直接读取第 34 组的 YAML/validation，没有改写交接原件，也没有创建额外 HANDOFF 总导航。

## 3. 主范围进度与阅读说明

| 互斥进度 | 查询数 | 具体含义 |
| :--- | ---: | :--- |
| 已确认（当前样本） | 49 | 当前工具识别的执行、类型声明、行值及必要顺序对齐；并非全输入/全边界同义 |
| 部分确认 | 127 | 取得完整记录，但仍存在差异/元数据不足，或仅完成原句控制重跑 |
| 证据不足 | 28 | 候选构造、校验、序列化等阻断，未取得完整有效对照 |
| 未执行 | 982 | 尚无逐条独立复核，具体首轮事实保留，不直接认定修复点 |

查询级进度取本轮最新候选，记录级数量另计。各组主范围记录保留完整源 SQL、社区 SQL/转译错误、目标错误、.out 原件与出现次数；已选择的记录补充候选、代码依据、分维度比较、边界、限制和下一步。未选择的记录明确未执行，而不是用“行为差异”代替归因。

负向 SQL 在同组简表保留源错误、已有目标表现和处理理由，不强制填写空候选章节、不列为主修复积压。成功匹配简写，不把历史显示文本匹配宣称为原生类型和所有边界通过。

## 4. 逐组报告

| 输入组 | 总数 | 源成功 | 源负向 | 首轮成功匹配 | 主范围差异 | 详情 |
| :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| aggregates | 55 | 55 | 0 | 15 | 40 | [查看](details/aggregates.md) |
| arrays | 65 | 56 | 9 | 0 | 56 | [查看](details/arrays.md) |
| case | 8 | 8 | 0 | 6 | 2 | [查看](details/case.md) |
| date | 64 | 47 | 17 | 11 | 36 | [查看](details/date.md) |
| groupingsets | 17 | 17 | 0 | 0 | 17 | [查看](details/groupingsets.md) |
| int4 | 40 | 34 | 6 | 30 | 4 | [查看](details/int4.md) |
| interval | 20 | 11 | 9 | 0 | 11 | [查看](details/interval.md) |
| join | 58 | 56 | 2 | 28 | 28 | [查看](details/join.md) |
| json | 100 | 77 | 23 | 12 | 65 | [查看](details/json.md) |
| jsonb | 90 | 85 | 5 | 4 | 81 | [查看](details/jsonb.md) |
| numeric | 25 | 11 | 14 | 0 | 11 | [查看](details/numeric.md) |
| strings | 25 | 15 | 10 | 5 | 10 | [查看](details/strings.md) |
| subselect | 32 | 31 | 1 | 19 | 12 | [查看](details/subselect.md) |
| time | 15 | 8 | 7 | 0 | 8 | [查看](details/time.md) |
| timestamp | 25 | 10 | 15 | 0 | 10 | [查看](details/timestamp.md) |
| timestamptz | 15 | 2 | 13 | 0 | 2 | [查看](details/timestamptz.md) |
| union | 20 | 20 | 0 | 2 | 18 | [查看](details/union.md) |
| window | 65 | 65 | 0 | 23 | 42 | [查看](details/window.md) |
| with | 11 | 10 | 1 | 5 | 5 | [查看](details/with.md) |
| bit | 66 | 57 | 9 | 0 | 57 | [查看](details/bit.md) |
| collate | 4 | 3 | 1 | 3 | 0 | [查看](details/collate.md) |
| multirangetypes | 266 | 265 | 1 | 0 | 265 | [查看](details/multirangetypes.md) |
| numerology | 54 | 33 | 21 | 0 | 33 | [查看](details/numerology.md) |
| rangetypes | 56 | 53 | 3 | 0 | 53 | [查看](details/rangetypes.md) |
| sqljson | 87 | 56 | 31 | 1 | 55 | [查看](details/sqljson.md) |
| sqljson_queryfuncs | 74 | 55 | 19 | 0 | 55 | [查看](details/sqljson_queryfuncs.md) |
| xml | 70 | 64 | 6 | 0 | 64 | [查看](details/xml.md) |
| boolean | 45 | 33 | 12 | 27 | 6 | [查看](details/boolean.md) |
| char | 3 | 3 | 0 | 1 | 2 | [查看](details/char.md) |
| float4 | 46 | 37 | 9 | 11 | 26 | [查看](details/float4.md) |
| float8 | 114 | 88 | 26 | 38 | 50 | [查看](details/float8.md) |
| money | 55 | 34 | 21 | 0 | 34 | [查看](details/money.md) |
| rowtypes | 32 | 26 | 6 | 0 | 26 | [查看](details/rowtypes.md) |
| select_distinct_on | 3 | 2 | 1 | 0 | 2 | [查看](details/select_distinct_on.md) |

## 5. 比较方案与证据限制

初轮 Recorded Output 使用 .out 的显示文本，仅比较其可提供的证据，不凭空补原生类型。此次 probe 真实连接 PG/Doris，重跑原 PG、已有社区 Doris、独立候选与重复执行，并保存完整有限结果、原生类型与分维度比较。

分别记录执行状态/具体错误、字段数、应保留的显式 Alias、逻辑/原生类型及精度/Scale、行数、行值及重复次数、最终顺序和重复执行。类型不同不阻断值比较，未知类型不当通过。无最终 ORDER BY 比较行多重集合；有最终排序另查顺序。同一多重集合只表示各行及其出现次数相同，不代表类型或顺序相同。

每个工具执行限 10 秒/10,000 行，超限不算通过。Float 未自动放宽容差，Decimal 精确比较。JSON 对象与 TEXT、SQL NULL 与 JSON null、数组与显示字符串分开。PG _int4 与 Doris array<int> 的类型别名表示和 array<tinyint> 的真实位宽差异不可混为一谈。PG 浮点显示/驱动解码仍有研究依赖。

非唯一排序即使重跑稳定也没证明唯一；数组下界、全类型域、Collation、无界 NUMERIC、每条 SQL 的全部边界没有全量验证。不能仅据当前工具的类型声明一致宣称完全同义。

## 6. 边界、失败尝试与后续任务

19 个边界设计，18 个不同边界取得完整证据，共 19 份执行记录（JSON 字符串边界重试一次）。0o0 AS value 被当前 PG SQLGlot Parser 阻断，未取得完整双端证据。新变体不借用旧 .out，均明确保存源 SQL；共享规则边界不代表所有复杂原查询都测过相同边界。

MAKE_DATE 原始非法日期仍作为负向说明；补正常日期、闰日、NULL 的新变体在 PG 成功后，才建立对应功能任务。json-text-string 的首次反斜杠错误来自手工候选，第二次修正且保留两次证据，不算 SQLGlot 缺陷。JSON 对象 TEXT 空格差异、AVG 循环小数等不利证据均未隐去。

[候选/工具失败/边界索引](probe-index.json)记录生成失败、完整对照路径与限制；[SQLGlot 任务](sqlglot-tasks.md)列出 20 个受限修复建议或研究事项；[汇总](attribution-summary.md)说明完成范围。全部后续修复由人显式调用，不自动执行。

