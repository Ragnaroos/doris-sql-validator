# PostgreSQL → Doris：扩展语料首轮验证报告

## 1. 本轮结果

- 本次输入并进入验证器：**1725 条用例**。报告统计来自本次运行结果，不按历史运行情况区分新旧 SQL。
- 按源 SQL 原文去重为 **1714 条**；同文但来源/用例编号不同的记录保留，数量与去重 SQL 数分开说明。
- 两端成功且参考输出匹配：**241 条（13.97%）**。这是固定数据与现有文本证据下的匹配率，不是完整语义证明。
- SQLGlot 转译失败：**136 条**；实际取得 Doris 执行结果：**1589 条**。
- 运行时读取到源端报错的负向用例：**293 条**；其中 **130 条**两端粗粒度错误类别相同，不计入成功匹配，也不证明同因。
- 测试库：`dsv_pg_manual_20261111`。源结果读官方 `.out`；验证器只执行 Doris。没有执行 AI 改写、归因或修复。

## 2. 范围与数据前提

本批表查询使用已准备的 21 张逻辑表/视图；运行前在框架外只读检查了结构、完整记录和初始指纹。证据见 [environment-check.json](environment-check.json)，数据准备文件没有删除或改写。
另外两批 20 组官方脚本中，仅纳入不引用表、没有自定义类型/函数依赖且可固定输出的查询；未运行新的 DDL/DML，没有为新表编造数据。含表值函数的查询也保守留待数据准备。这是本批输入的准备条件，不是验证器对执行历史的记忆。
本批可读取但因环境/对象、确定性或外部资源安全条件未纳入：**1193 条**。完整 SQL、排除原因和每组数量见 [selection.json](../../../cases/postgres/manual/current/expanded/selection.json)；未纳入不表示通过。
3 条 ORDER BY ... USING 查询已纳入普通 YAML 和本轮查询总数；SQLGlot Parser 拒绝的语法记为转译失败，后续参考输出读取、Doris 执行及比较未执行。原文和错误见 [该组验证报告](validation/select_distinct_on/validation.md)。其他未保留为 Case 的导入诊断不计入运行查询分母，也不能直接归为 SQLGlot 缺陷。
`.out` 缺少原生类型和完整 NULL 表示信息；类型、Session、数据库能力、Adapter、比较器或数据前提仍可能导致差异。首轮报告只描述观察到的结果，不提前把不匹配归因给 SQLGlot。

## 3. 互斥结果分类

| 结果 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 51 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 976 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 371 |
| 返回字段数量、名称或类型不同（`RESULT_SCHEMA_MISMATCH`） | 13 |
| 返回记录行数不同（`ROW_COUNT_MISMATCH`） | 5 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 173 |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 136 |

MATCH 包含两端同类报错；成功匹配数已在第一节单独统计。环境错误也单独保留，不隐藏在 SQLGlot 缺陷中。

## 4. 分组详细报告

| 输入文件 | 查询数 | 成功结果匹配 | SQLGlot 转译失败 | 详细报告 |
| :--- | ---: | ---: | ---: | :--- |
| aggregates.sql | 55 | 15 | 1 | [查看](validation/aggregates/validation.md) |
| arrays.sql | 65 | 0 | 41 | [查看](validation/arrays/validation.md) |
| case.sql | 8 | 6 | 0 | [查看](validation/case/validation.md) |
| date.sql | 64 | 11 | 0 | [查看](validation/date/validation.md) |
| groupingsets.sql | 17 | 0 | 2 | [查看](validation/groupingsets/validation.md) |
| int4.sql | 40 | 30 | 0 | [查看](validation/int4/validation.md) |
| interval.sql | 20 | 0 | 0 | [查看](validation/interval/validation.md) |
| join.sql | 58 | 28 | 3 | [查看](validation/join/validation.md) |
| json.sql | 100 | 12 | 15 | [查看](validation/json/validation.md) |
| jsonb.sql | 90 | 4 | 19 | [查看](validation/jsonb/validation.md) |
| numeric.sql | 25 | 0 | 0 | [查看](validation/numeric/validation.md) |
| strings.sql | 25 | 5 | 0 | [查看](validation/strings/validation.md) |
| subselect.sql | 32 | 19 | 3 | [查看](validation/subselect/validation.md) |
| time.sql | 15 | 0 | 0 | [查看](validation/time/validation.md) |
| timestamp.sql | 25 | 0 | 0 | [查看](validation/timestamp/validation.md) |
| timestamptz.sql | 15 | 0 | 1 | [查看](validation/timestamptz/validation.md) |
| union.sql | 20 | 2 | 18 | [查看](validation/union/validation.md) |
| window.sql | 65 | 23 | 19 | [查看](validation/window/validation.md) |
| with.sql | 11 | 5 | 0 | [查看](validation/with/validation.md) |
| bit.sql | 66 | 0 | 0 | [查看](validation/bit/validation.md) |
| collate.sql | 4 | 3 | 0 | [查看](validation/collate/validation.md) |
| multirangetypes.sql | 266 | 0 | 1 | [查看](validation/multirangetypes/validation.md) |
| numerology.sql | 54 | 0 | 0 | [查看](validation/numerology/validation.md) |
| rangetypes.sql | 56 | 0 | 1 | [查看](validation/rangetypes/validation.md) |
| sqljson.sql | 87 | 1 | 2 | [查看](validation/sqljson/validation.md) |
| sqljson_queryfuncs.sql | 74 | 0 | 0 | [查看](validation/sqljson_queryfuncs/validation.md) |
| xml.sql | 70 | 0 | 4 | [查看](validation/xml/validation.md) |
| boolean.sql | 45 | 27 | 0 | [查看](validation/boolean/validation.md) |
| char.sql | 3 | 1 | 0 | [查看](validation/char/validation.md) |
| float4.sql | 46 | 11 | 0 | [查看](validation/float4/validation.md) |
| float8.sql | 114 | 38 | 0 | [查看](validation/float8/validation.md) |
| money.sql | 55 | 0 | 0 | [查看](validation/money/validation.md) |
| rowtypes.sql | 32 | 0 | 3 | [查看](validation/rowtypes/validation.md) |
| select_distinct_on.sql | 3 | 0 | 3 | [查看](validation/select_distinct_on/validation.md) |

## 5. 未进入执行与后续处理

- 没有选中查询的输入脚本：domain、select_having、select_implicit、select_views、enum、functional_deps。依赖本轮未准备的表或对象时不执行，不能把空结果算成通过。
- 所有已运行查询的源 SQL、生成的 Doris SQL、执行错误与比较差异见逐组报告；匹配条目简写，不匹配及负向错误条目展开。
- 旧首轮报告已从 current 移除，恢复副本位于 `reports/pg-manual/archive/first-round-before-expansion-20261111T094004282439Z`，默认不发布到远程。数据准备和其他历史归因文件未删除。
- 下一步可以由人调用归因 Skill 分析本轮报告；本次没有自动执行该步骤。

本次报告更新范围：2026-11-13 仅将 select_distinct_on 的 3 条查询通过普通 run 重新验证，均在 SQLGlot Parser 阶段失败；其余 1,722 条沿用各组已有执行证据，本次未连接数据库、未重跑全批，也未重新归因。
