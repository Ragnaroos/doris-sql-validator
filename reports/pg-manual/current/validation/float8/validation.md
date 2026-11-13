# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:39.414666+00:00 至 2026-11-11T09:40:41.247502+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/float8.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**114**；两端成功且已有证据匹配：**38**。
- 成功结果匹配占全部查询比例：**38/114 = 33.33%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**38/88 = 43.18%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**26**；不计入上述成功匹配分子。
- 需要分析的查询：**76**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**22**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 8 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 32 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 38 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 36 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 114 条只读查询、跳过 70 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–10 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 12–12 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 13–13 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 14–14 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 16–16 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 27–28 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 29–29 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 14 | 30–30 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 15 | 31–31 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 32–32 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 17 | 33–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 34–34 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 19 | 35–35 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 57 | 116–117 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 100 | 182–184 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 132 | 232–235 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 134 | 246–246 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 135 | 248–251 | 跳过非查询；类型 `set` | Expected one read-only Query, got Set |
| 148 | 269–269 | 跳过非查询；类型 `reset` | Expected one read-only Query, got Command |
| 149 | 271–272 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 150 | 274–274 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 151 | 276–276 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 152 | 278–278 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 153 | 280–280 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 173 | 343–349 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 174 | 350–351 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 175 | 352–353 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 176 | 354–354 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 177 | 355–355 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 178 | 356–356 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 179 | 357–357 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 180 | 358–358 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 181 | 359–359 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 184 | 537–538 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 23 | 41–41 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 38 | 61–61 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 39 | 63–63 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 40 | 65–65 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 41 | 67–67 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 42 | 69–69 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 43 | 71–71 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 44 | 73–73 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 45 | 75–77 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 46 | 79–81 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 47 | 83–85 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 48 | 87–89 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 49 | 91–92 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 50 | 94–96 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 51 | 98–100 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 52 | 102–104 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 53 | 106–107 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 54 | 108–108 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 55 | 110–111 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 56 | 113–114 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 60 | 124–126 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 95 | 166–169 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 98 | 177–177 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 99 | 180–180 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 101 | 186–186 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 102 | 188–188 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 104 | 192–192 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 105 | 194–194 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 106 | 196–196 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 107 | 198–198 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 108 | 200–200 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 154 | 282–284 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 172 | 337–341 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 182 | 361–386 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 183 | 388–535 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/float8.out`；SHA-256（文件内容指纹）：`08e9bf36f99413d3c86541bacf552ad4d867e34ad61a68a885da0eac5836a5e1`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 114/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 114/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 88/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 88/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 88/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/114 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-float8-0007-88440e0e` | SELECT '10e400'::float8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0008-cd413fb2` | SELECT '-10e400'::float8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0009-c9fe8398` | SELECT '10e-400'::float8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0010-7b8ae6f8` | SELECT '-10e-400'::float8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0011-6ab989be` | SELECT float8send('2.2250738585072014E-308'::float8); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0020-309c7b69` | SELECT pg_input_is_valid('34.5', 'float8'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0021-537262c3` | SELECT pg_input_is_valid('xyz', 'float8'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0022-eb12c7c1` | SELECT pg_input_is_valid('1e4000', 'float8'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0024-c1a914ec` | SELECT 'NaN'::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0025-6616e5ff` | SELECT 'nan'::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0026-e24d20f0` | SELECT '   NAN  '::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0027-5327a329` | SELECT 'infinity'::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0028-dbdcc7e0` | SELECT '          -INFINiTY   '::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0029-7bf74ce8` | SELECT 'N A N'::float8; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0030-cb4f1143` | SELECT 'NaN x'::float8; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0031-f4d72ba1` | SELECT ' INFINITY    x'::float8; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0032-2ed2fe36` | SELECT 'Infinity'::float8 + 100.0; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0033-fab0f874` | SELECT 'Infinity'::float8 / 'Infinity'::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0034-b19cea1b` | SELECT '42'::float8 / 'Infinity'::float8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0035-98f3140d` | SELECT 'nan'::float8 / 'nan'::float8; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0036-2499e7b1` | SELECT 'nan'::float8 / '0'::float8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0037-78ceabd8` | SELECT 'nan'::numeric::float8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0058-93ee51d9` | SELECT sqrt(float8 '64') AS eight; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0059-93ee51d9` | SELECT \|/ float8 '64' AS eight; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0061-8c09f610` | SELECT power(float8 '144', float8 '0.5'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0062-1d0158b0` | SELECT power(float8 'NaN', float8 '0.5'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0063-3b58d3ae` | SELECT power(float8 '144', float8 'NaN'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0064-29084e2c` | SELECT power(float8 'NaN', float8 'NaN'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0065-3a2a1fed` | SELECT power(float8 '-1', float8 'NaN'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0066-32a6f72c` | SELECT power(float8 '1', float8 'NaN'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0067-47f22839` | SELECT power(float8 'NaN', float8 '0'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0068-ce75067e` | SELECT power(float8 'inf', float8 '0'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0069-45a0403b` | SELECT power(float8 '-inf', float8 '0'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0070-d81797b6` | SELECT power(float8 '0', float8 'inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0071-012234df` | SELECT power(float8 '0', float8 '-inf'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0072-4b7595fc` | SELECT power(float8 '1', float8 'inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0073-5fa95364` | SELECT power(float8 '1', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0074-dcc2fab4` | SELECT power(float8 '-1', float8 'inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0075-3211ff12` | SELECT power(float8 '-1', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0076-c3a3e121` | SELECT power(float8 '0.1', float8 'inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0077-97dc9f6a` | SELECT power(float8 '-0.1', float8 'inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0078-fcd3a905` | SELECT power(float8 '1.1', float8 'inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0079-3a0d29d4` | SELECT power(float8 '-1.1', float8 'inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0080-fa0c31da` | SELECT power(float8 '0.1', float8 '-inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0081-db4c6e0a` | SELECT power(float8 '-0.1', float8 '-inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0082-e2449205` | SELECT power(float8 '1.1', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0083-9c0182b1` | SELECT power(float8 '-1.1', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0084-a3c7d189` | SELECT power(float8 'inf', float8 '-2'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0085-1d6f83d3` | SELECT power(float8 'inf', float8 '2'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0086-ad3650f5` | SELECT power(float8 'inf', float8 'inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0087-16088520` | SELECT power(float8 'inf', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0088-086db460` | SELECT power(float8 '-inf', float8 '-2') = '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0089-f731dc20` | SELECT power(float8 '-inf', float8 '-3'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0090-dfe0b3d9` | SELECT power(float8 '-inf', float8 '2'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0091-101f01f3` | SELECT power(float8 '-inf', float8 '3'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0092-86201c1e` | SELECT power(float8 '-inf', float8 '3.5'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0093-1b9189db` | SELECT power(float8 '-inf', float8 'inf'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0094-e437580b` | SELECT power(float8 '-inf', float8 '-inf'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0096-285130b3` | SELECT exp('inf'::float8), exp('-inf'::float8), exp('nan'::float8); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0097-a14fc3c2` | SELECT \|\|/ float8 '27' AS three; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0103-c9b3ade2` | SELECT 0 ^ 0 + 0 ^ 1 + 0 ^ 0.0 + 0 ^ 0.5; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0109-ed5a37d8` | SELECT sinh(float8 '1'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0110-b7f4cc0b` | SELECT cosh(float8 '1'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0111-e3136b56` | SELECT tanh(float8 '1'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0112-793e70b9` | SELECT asinh(float8 '1'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0113-0f62ba6b` | SELECT acosh(float8 '2'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0114-5dfbae93` | SELECT atanh(float8 '0.5'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0115-e81acbb2` | SELECT sinh(float8 'infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0116-a5bc31de` | SELECT sinh(float8 '-infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0117-fdb20380` | SELECT sinh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0118-1a8c506f` | SELECT cosh(float8 'infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0119-ce38a8c0` | SELECT cosh(float8 '-infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0120-ff137ba2` | SELECT cosh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0121-43d168cf` | SELECT tanh(float8 'infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0122-34c43150` | SELECT tanh(float8 '-infinity'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0123-7a12cdce` | SELECT tanh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0124-6e06598a` | SELECT asinh(float8 'infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0125-33896df8` | SELECT asinh(float8 '-infinity'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0126-53f0039a` | SELECT asinh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0127-d9cb28b5` | SELECT acosh(float8 '-infinity'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0128-04142f37` | SELECT acosh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0129-ff445481` | SELECT atanh(float8 'infinity'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0130-d6edd65a` | SELECT atanh(float8 '-infinity'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0131-91778068` | SELECT atanh(float8 'nan'); | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0133-1686bfe4` | SELECT x,        erf(x),        erfc(x) FROM (VALUES (float8 '-infinity'),       (-28), (-6), (-3.4), (-2.1), (-1.1), (-0.45),       (-1.2e-9), (-2.3e-13), (-1.2e-17), (0),       (1.2e-17), (2.3e-13), (1.2e-9),       (0.45), (1.1), (2.1), (3.4), (6), (28),       (float8 'infinity'), (float8 'nan')) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0136-1407357d` | SELECT x,        gamma(x),        lgamma(x) FROM (VALUES (0.5), (1), (2), (3), (4), (5),              (float8 'infinity'), (float8 'nan')) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0137-5cb14dc7` | SELECT gamma(float8 '-infinity'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0138-64577def` | SELECT lgamma(float8 '-infinity'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0139-1db07e6d` | SELECT gamma(float8 '-1000.5'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0140-ac1c1632` | SELECT lgamma(float8 '-1000.5'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0141-3bc04443` | SELECT gamma(float8 '-1'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0142-de3bfeba` | SELECT lgamma(float8 '-1'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0143-2cddd068` | SELECT gamma(float8 '0'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0144-bd18f753` | SELECT lgamma(float8 '0'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0145-08c21a50` | SELECT gamma(float8 '1000'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0146-6496a2bb` | SELECT lgamma(float8 '1000'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0147-8523fd1a` | SELECT lgamma(float8 '1e308'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：函数不存在或调用形式不受支持 | 两端均报错，但错误类别不同 |
| `pg-float8-0155-f8b09ed2` | SELECT '32767.4'::float8::int2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0156-dbb86232` | SELECT '32767.6'::float8::int2; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0157-5d91cc84` | SELECT '-32768.4'::float8::int2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0158-df00ee2c` | SELECT '-32768.6'::float8::int2; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0159-269e8ceb` | SELECT '2147483647.4'::float8::int4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0160-c5ba41f5` | SELECT '2147483647.6'::float8::int4; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0161-1c93a18d` | SELECT '-2147483648.4'::float8::int4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float8-0162-902a328b` | SELECT '-2147483648.6'::float8::int4; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0163-6ca27d28` | SELECT '9223372036854773760'::float8::int8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0164-7ca4124d` | SELECT '9223372036854775807'::float8::int8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0165-05c5bbe3` | SELECT '-9223372036854775808.5'::float8::int8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float8-0166-170d0b04` | SELECT '-9223372036854780000'::float8::int8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0167-04b2aa54` | SELECT x,        sind(x),        sind(x) IN (-1,-0.5,0,0.5,1) AS sind_exact FROM (VALUES (0), (30), (90), (150), (180),       (210), (270), (330), (360)) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0168-a8fd9aee` | SELECT x,        cosd(x),        cosd(x) IN (-1,-0.5,0,0.5,1) AS cosd_exact FROM (VALUES (0), (60), (90), (120), (180),       (240), (270), (300), (360)) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0169-763c8507` | SELECT x,        tand(x),        tand(x) IN ('-Infinity'::float8,-1,0,                    1,'Infinity'::float8) AS tand_exact,        cotd(x),        cotd(x) IN ('-Infinity'::float8,-1,0,                    1,'Infinity'::float8) AS cotd_exact FROM (VALUES (0), (45), (90), (135), (180),       (225), (270), (315), (360)) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0170-b46298bf` | SELECT x,        asind(x),        asind(x) IN (-90,-30,0,30,90) AS asind_exact,        acosd(x),        acosd(x) IN (0,60,90,120,180) AS acosd_exact FROM (VALUES (-1), (-0.5), (0), (0.5), (1)) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float8-0171-b35da73e` | SELECT x,        atand(x),        atand(x) IN (-90,-45,0,45,90) AS atand_exact FROM (VALUES ('-Infinity'::float8), (-1), (0), (1),       ('Infinity'::float8)) AS t(x); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-float8-0007-88440e0e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '10e400'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('10e400' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`"10e400" is out of range for type double precision`。

错误原文：

```text
"10e400" is out of range for type double precision
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.5 ms。
- 返回行数：1；字段：CAST('10e400' AS DOUBLE): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$float": "infinity"
    }
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
source_error_message="10e400" is out of range for type double precision
source_error_code="10e400" is out of range for type double precision
```

### pg-float8-0008-cd413fb2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-10e400'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('-10e400' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`"-10e400" is out of range for type double precision`。

错误原文：

```text
"-10e400" is out of range for type double precision
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.0 ms。
- 返回行数：1；字段：CAST('-10e400' AS DOUBLE): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$float": "-infinity"
    }
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
source_error_message="-10e400" is out of range for type double precision
source_error_code="-10e400" is out of range for type double precision
```

### pg-float8-0009-c9fe8398 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '10e-400'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('10e-400' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`"10e-400" is out of range for type double precision`。

错误原文：

```text
"10e-400" is out of range for type double precision
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：CAST('10e-400' AS DOUBLE): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.0
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
source_error_message="10e-400" is out of range for type double precision
source_error_code="10e-400" is out of range for type double precision
```

### pg-float8-0010-7b8ae6f8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-10e-400'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('-10e-400' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`"-10e-400" is out of range for type double precision`。

错误原文：

```text
"-10e-400" is out of range for type double precision
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：CAST('-10e-400' AS DOUBLE): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -0.0
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
source_error_message="-10e-400" is out of range for type double precision
source_error_code="-10e-400" is out of range for type double precision
```

### pg-float8-0011-6ab989be — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float8send('2.2250738585072014E-308'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT8SEND(CAST('2.2250738585072014E-308' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float8send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x0010000000000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT8SEND'")
doris_error_code=1105
```

### pg-float8-0020-309c7b69 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('34.5', 'float8');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('34.5', 'float8')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-float8-0021-537262c3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('xyz', 'float8');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('xyz', 'float8')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-float8-0022-eb12c7c1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('1e4000', 'float8');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('1e4000', 'float8')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：pg_input_is_valid: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'PG_INPUT_IS_VALID'")
doris_error_code=1105
```

### pg-float8-0029-7bf74ce8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'N A N'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('N A N' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type double precision: "N A N"`。

错误原文：

```text
invalid input syntax for type double precision: "N A N"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.8 ms。
- 返回行数：1；字段：CAST('N A N' AS DOUBLE): float / DOUBLE。
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
source_error_message=invalid input syntax for type double precision: "N A N"
source_error_code=invalid input syntax for type double precision: "N A N"
```

### pg-float8-0030-cb4f1143 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'NaN x'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('NaN x' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type double precision: "NaN x"`。

错误原文：

```text
invalid input syntax for type double precision: "NaN x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：CAST('NaN x' AS DOUBLE): float / DOUBLE。
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
source_error_message=invalid input syntax for type double precision: "NaN x"
source_error_code=invalid input syntax for type double precision: "NaN x"
```

### pg-float8-0031-f4d72ba1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ' INFINITY    x'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(' INFINITY    x' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type double precision: " INFINITY    x"`。

错误原文：

```text
invalid input syntax for type double precision: " INFINITY    x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.8 ms。
- 返回行数：1；字段：CAST(' INFINITY    x' AS DOUBLE): float / DOUBLE。
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
source_error_message=invalid input syntax for type double precision: " INFINITY    x"
source_error_code=invalid input syntax for type double precision: " INFINITY    x"
```

### pg-float8-0034-b19cea1b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '42'::float8 / 'Infinity'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('42' AS DOUBLE) / CAST('Infinity' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.3 ms。
- 返回行数：1；字段：CAST('42' AS DOUBLE) / CAST('Infinity' AS DOUBLE): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0036-2499e7b1 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::float8 / '0'::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('nan' AS DOUBLE) / CAST('0' AS DOUBLE)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：CAST('nan' AS DOUBLE) / CAST('0' AS DOUBLE): float / DOUBLE。
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

### pg-float8-0037-78ceabd8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::numeric::float8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('nan' AS DECIMAL) AS DOUBLE)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float8: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：CAST(CAST('nan' AS DECIMAL) AS DOUBLE): float / DOUBLE。
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

### pg-float8-0058-93ee51d9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sqrt(float8 '64') AS eight;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SQRT(CAST('64' AS DOUBLE)) AS eight
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：eight: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "8"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.9 ms。
- 返回行数：1；字段：eight: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0059-93ee51d9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT |/ float8 '64' AS eight;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SQRT(CAST('64' AS DOUBLE)) AS eight
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：eight: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "8"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.9 ms。
- 返回行数：1；字段：eight: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0061-8c09f610 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '144', float8 '0.5');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('144' AS DOUBLE), CAST('0.5' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "12"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.9 ms。
- 返回行数：1；字段：POWER(CAST('144' AS DOUBLE), CAST('0.5' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    12.0
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

### pg-float8-0066-32a6f72c — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '1', float8 'NaN');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('NaN' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：POWER(CAST('1' AS DOUBLE), CAST('NaN' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0067-47f22839 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 'NaN', float8 '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('NaN' AS DOUBLE), CAST('0' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：POWER(CAST('NaN' AS DOUBLE), CAST('0' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0068-ce75067e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 'inf', float8 '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('0' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.7 ms。
- 返回行数：1；字段：POWER(CAST('inf' AS DOUBLE), CAST('0' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0069-45a0403b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-inf', float8 '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('0' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：POWER(CAST('-inf' AS DOUBLE), CAST('0' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0070-d81797b6 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '0', float8 'inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('0' AS DOUBLE), CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：POWER(CAST('0' AS DOUBLE), CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0071-012234df — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT power(float8 '0', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('0' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`zero raised to a negative power is undefined`。

错误原文：

```text
zero raised to a negative power is undefined
```

#### Doris 实际结果

- 执行状态：成功；耗时 20.5 ms。
- 返回行数：1；字段：POWER(CAST('0' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$float": "infinity"
    }
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
source_error_message=zero raised to a negative power is undefined
source_error_code=zero raised to a negative power is undefined
```

### pg-float8-0072-4b7595fc — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '1', float8 'inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.3 ms。
- 返回行数：1；字段：POWER(CAST('1' AS DOUBLE), CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0073-5fa95364 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '1', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('1' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.9 ms。
- 返回行数：1；字段：POWER(CAST('1' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0074-dcc2fab4 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-1', float8 'inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-1' AS DOUBLE), CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：POWER(CAST('-1' AS DOUBLE), CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0075-3211ff12 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-1', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-1' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.4 ms。
- 返回行数：1；字段：POWER(CAST('-1' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0076-c3a3e121 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '0.1', float8 'inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('0.1' AS DOUBLE), CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.2 ms。
- 返回行数：1；字段：POWER(CAST('0.1' AS DOUBLE), CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0077-97dc9f6a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-0.1', float8 'inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-0.1' AS DOUBLE), CAST('inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.1 ms。
- 返回行数：1；字段：POWER(CAST('-0.1' AS DOUBLE), CAST('inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0082-e2449205 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '1.1', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('1.1' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：POWER(CAST('1.1' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0083-9c0182b1 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-1.1', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-1.1' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.8 ms。
- 返回行数：1；字段：POWER(CAST('-1.1' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0084-a3c7d189 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 'inf', float8 '-2');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('-2' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.7 ms。
- 返回行数：1；字段：POWER(CAST('inf' AS DOUBLE), CAST('-2' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0087-16088520 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 'inf', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('inf' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.4 ms。
- 返回行数：1；字段：POWER(CAST('inf' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0089-f731dc20 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-inf', float8 '-3');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('-3' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.8 ms。
- 返回行数：1；字段：POWER(CAST('-inf' AS DOUBLE), CAST('-3' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -0.0
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

### pg-float8-0092-86201c1e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT power(float8 '-inf', float8 '3.5');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('3.5' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`a negative number raised to a non-integer power yields a complex result`。

错误原文：

```text
a negative number raised to a non-integer power yields a complex result
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：POWER(CAST('-inf' AS DOUBLE), CAST('3.5' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$float": "nan"
    }
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
source_error_message=a negative number raised to a non-integer power yields a complex result
source_error_code=a negative number raised to a non-integer power yields a complex result
```

### pg-float8-0094-e437580b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT power(float8 '-inf', float8 '-inf');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(CAST('-inf' AS DOUBLE), CAST('-inf' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：power: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.1 ms。
- 返回行数：1；字段：POWER(CAST('-inf' AS DOUBLE), CAST('-inf' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0096-285130b3 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT exp('inf'::float8), exp('-inf'::float8), exp('nan'::float8);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXP(CAST('inf' AS DOUBLE)), EXP(CAST('-inf' AS DOUBLE)), EXP(CAST('nan' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：exp: unknown / 原生类型未知, exp: unknown / 原生类型未知, exp: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "Infinity",
    "0",
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.4 ms。
- 返回行数：1；字段：EXP(CAST('inf' AS DOUBLE)): float / DOUBLE, EXP(CAST('-inf' AS DOUBLE)): float / DOUBLE, EXP(CAST('nan' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$float": "infinity"
    },
    0.0,
    {
      "$float": "nan"
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

### pg-float8-0097-a14fc3c2 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT ||/ float8 '27' AS three;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CBRT(CAST('27' AS DOUBLE)) AS three
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：three: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 24.9 ms。
- 返回行数：1；字段：three: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
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

### pg-float8-0103-c9b3ade2 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0 ^ 0 + 0 ^ 1 + 0 ^ 0.0 + 0 ^ 0.5;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT POWER(0, 0) + POWER(0, 1) + POWER(0, 0.0) + POWER(0, 0.5)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：POWER(0, 0) + POWER(0, 1) + POWER(0, 0.0) + POWER(0, 0.5): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    2.0
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

### pg-float8-0109-ed5a37d8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT sinh(float8 '1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SINH(CAST('1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：sinh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.1752011936438"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.9 ms。
- 返回行数：1；字段：SINH(CAST('1' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.175201193643801
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

### pg-float8-0110-b7f4cc0b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT cosh(float8 '1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT COSH(CAST('1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：cosh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.54308063481524"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.0 ms。
- 返回行数：1；字段：COSH(CAST('1' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.543080634815244
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

### pg-float8-0111-e3136b56 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT tanh(float8 '1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TANH(CAST('1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：tanh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.761594155955765"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：TANH(CAST('1' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.7615941559557649
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

### pg-float8-0112-793e70b9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT asinh(float8 '1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ASINH(CAST('1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：asinh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.881373587019543"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 80.5 ms。
- 返回行数：1；字段：ASINH(CAST('1' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.8813735870195429
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

### pg-float8-0113-0f62ba6b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT acosh(float8 '2');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ACOSH(CAST('2' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：acosh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1.31695789692482"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.5 ms。
- 返回行数：1；字段：ACOSH(CAST('2' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.316957896924817
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

### pg-float8-0114-5dfbae93 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT atanh(float8 '0.5');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ATANH(CAST('0.5' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：atanh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.549306144334055"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：ATANH(CAST('0.5' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0.5493061443340549
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

### pg-float8-0121-43d168cf — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT tanh(float8 'infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TANH(CAST('infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：tanh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：TANH(CAST('infinity' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1.0
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

### pg-float8-0122-34c43150 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT tanh(float8 '-infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT TANH(CAST('-infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：tanh: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：TANH(CAST('-infinity' AS DOUBLE)): float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -1.0
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

### pg-float8-0127-d9cb28b5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT acosh(float8 '-infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ACOSH(CAST('-infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`input is out of range`。

错误原文：

```text
input is out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：ACOSH(CAST('-infinity' AS DOUBLE)): float / DOUBLE。
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
source_error_message=input is out of range
source_error_code=input is out of range
```

### pg-float8-0129-ff445481 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT atanh(float8 'infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ATANH(CAST('infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`input is out of range`。

错误原文：

```text
input is out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：ATANH(CAST('infinity' AS DOUBLE)): float / DOUBLE。
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
source_error_message=input is out of range
source_error_code=input is out of range
```

### pg-float8-0130-d6edd65a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT atanh(float8 '-infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT ATANH(CAST('-infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`input is out of range`。

错误原文：

```text
input is out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.3 ms。
- 返回行数：1；字段：ATANH(CAST('-infinity' AS DOUBLE)): float / DOUBLE。
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
source_error_message=input is out of range
source_error_code=input is out of range
```

### pg-float8-0133-1686bfe4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       erf(x),
       erfc(x)
FROM (VALUES (float8 '-infinity'),
      (-28), (-6), (-3.4), (-2.1), (-1.1), (-0.45),
      (-1.2e-9), (-2.3e-13), (-1.2e-17), (0),
      (1.2e-17), (2.3e-13), (1.2e-9),
      (0.45), (1.1), (2.1), (3.4), (6), (28),
      (float8 'infinity'), (float8 'nan')) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, ERF(x), ERFC(x) FROM (SELECT CAST('-infinity' AS DOUBLE) AS x UNION ALL SELECT -28 UNION ALL SELECT -6 UNION ALL SELECT -3.4 UNION ALL SELECT -2.1 UNION ALL SELECT -1.1 UNION ALL SELECT -0.45 UNION ALL SELECT -1.2e-9 UNION ALL SELECT -2.3e-13 UNION ALL SELECT -1.2e-17 UNION ALL SELECT 0 UNION ALL SELECT 1.2e-17 UNION ALL SELECT 2.3e-13 UNION ALL SELECT 1.2e-9 UNION ALL SELECT 0.45 UNION ALL SELECT 1.1 UNION ALL SELECT 2.1 UNION ALL SELECT 3.4 UNION ALL SELECT 6 UNION ALL SELECT 28 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：22；字段：x: unknown / 原生类型未知, erf: unknown / 原生类型未知, erfc: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-Infinity",
    "-1",
    "2"
  ],
  [
    "-28",
    "-1",
    "2"
  ],
  [
    "-6",
    "-1",
    "2"
  ],
  [
    "-3.4",
    "-0.99999847800664",
    "1.9999984780066"
  ],
  [
    "-2.1",
    "-0.99702053334367",
    "1.9970205333437"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 14.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'ERF'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'ERF'")
doris_error_code=1105
```

### pg-float8-0136-1407357d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       gamma(x),
       lgamma(x)
FROM (VALUES (0.5), (1), (2), (3), (4), (5),
             (float8 'infinity'), (float8 'nan')) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, GAMMA(x), LGAMMA(x) FROM (SELECT 0.5 AS x UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT CAST('infinity' AS DOUBLE) UNION ALL SELECT CAST('nan' AS DOUBLE)) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：8；字段：x: unknown / 原生类型未知, gamma: unknown / 原生类型未知, lgamma: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.5",
    "1.7724538509055",
    "0.5723649429247"
  ],
  [
    "1",
    "1",
    "0"
  ],
  [
    "2",
    "1",
    "0"
  ],
  [
    "3",
    "2",
    "0.69314718055995"
  ],
  [
    "4",
    "6",
    "1.7917594692281"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0137-5cb14dc7 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT gamma(float8 '-infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GAMMA(CAST('-infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 63.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0138-64577def — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lgamma(float8 '-infinity');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('-infinity' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：lgamma: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "Infinity"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0139-1db07e6d — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT gamma(float8 '-1000.5');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GAMMA(CAST('-1000.5' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: underflow`。

错误原文：

```text
value out of range: underflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: underflow
source_error_code=value out of range: underflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0140-ac1c1632 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lgamma(float8 '-1000.5');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('-1000.5' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：lgamma: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-5914.4377011169"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0141-3bc04443 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT gamma(float8 '-1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GAMMA(CAST('-1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0142-de3bfeba — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT lgamma(float8 '-1');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('-1' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0143-2cddd068 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT gamma(float8 '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GAMMA(CAST('0' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0144-bd18f753 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT lgamma(float8 '0');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('0' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0145-08c21a50 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT gamma(float8 '1000');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GAMMA(CAST('1000' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'GAMMA'")
doris_error_code=1105
```

### pg-float8-0146-6496a2bb — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT lgamma(float8 '1000');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('1000' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：lgamma: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5905.2204232092"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0147-8523fd1a — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT lgamma(float8 '1e308');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LGAMMA(CAST('1e308' AS DOUBLE))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`value out of range: overflow`。

错误原文：

```text
value out of range: overflow
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=value out of range: overflow
source_error_code=value out of range: overflow
doris_error_category=FUNCTION_NOT_FOUND
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'LGAMMA'")
doris_error_code=1105
```

### pg-float8-0156-dbb86232 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '32767.6'::float8::int2;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('32767.6' AS DOUBLE) AS SMALLINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`smallint out of range`。

错误原文：

```text
smallint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.7 ms。
- 返回行数：1；字段：CAST(CAST('32767.6' AS DOUBLE) AS SMALLINT): integer / SMALLINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    32767
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
source_error_message=smallint out of range
source_error_code=smallint out of range
```

### pg-float8-0158-df00ee2c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-32768.6'::float8::int2;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-32768.6' AS DOUBLE) AS SMALLINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`smallint out of range`。

错误原文：

```text
smallint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.7 ms。
- 返回行数：1；字段：CAST(CAST('-32768.6' AS DOUBLE) AS SMALLINT): integer / SMALLINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -32768
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
source_error_message=smallint out of range
source_error_code=smallint out of range
```

### pg-float8-0160-c5ba41f5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '2147483647.6'::float8::int4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('2147483647.6' AS DOUBLE) AS INT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.4 ms。
- 返回行数：1；字段：CAST(CAST('2147483647.6' AS DOUBLE) AS INT): integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    2147483647
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
source_error_message=integer out of range
source_error_code=integer out of range
```

### pg-float8-0162-902a328b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-2147483648.6'::float8::int4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-2147483648.6' AS DOUBLE) AS INT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 9.7 ms。
- 返回行数：1；字段：CAST(CAST('-2147483648.6' AS DOUBLE) AS INT): integer / INT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483648
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
source_error_message=integer out of range
source_error_code=integer out of range
```

### pg-float8-0163-6ca27d28 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '9223372036854773760'::float8::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('9223372036854773760' AS DOUBLE) AS BIGINT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：int8: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854773760"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：CAST(CAST('9223372036854773760' AS DOUBLE) AS BIGINT): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    9223372036854773800
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

### pg-float8-0164-7ca4124d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '9223372036854775807'::float8::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('9223372036854775807' AS DOUBLE) AS BIGINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bigint out of range`。

错误原文：

```text
bigint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.6 ms。
- 返回行数：1；字段：CAST(CAST('9223372036854775807' AS DOUBLE) AS BIGINT): integer / BIGINT。
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
source_error_message=bigint out of range
source_error_code=bigint out of range
```

### pg-float8-0165-05c5bbe3 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '-9223372036854775808.5'::float8::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-9223372036854775808.5' AS DOUBLE) AS BIGINT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：int8: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.4 ms。
- 返回行数：1；字段：CAST(CAST('-9223372036854775808.5' AS DOUBLE) AS BIGINT): integer / BIGINT。
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

### pg-float8-0166-170d0b04 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-9223372036854780000'::float8::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-9223372036854780000' AS DOUBLE) AS BIGINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bigint out of range`。

错误原文：

```text
bigint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.4 ms。
- 返回行数：1；字段：CAST(CAST('-9223372036854780000' AS DOUBLE) AS BIGINT): integer / BIGINT。
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
source_error_message=bigint out of range
source_error_code=bigint out of range
```

### pg-float8-0167-04b2aa54 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       sind(x),
       sind(x) IN (-1,-0.5,0,0.5,1) AS sind_exact
FROM (VALUES (0), (30), (90), (150), (180),
      (210), (270), (330), (360)) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, SIND(x), SIND(x) IN (-1, -0.5, 0, 0.5, 1) AS sind_exact FROM (SELECT 0 AS x UNION ALL SELECT 30 UNION ALL SELECT 90 UNION ALL SELECT 150 UNION ALL SELECT 180 UNION ALL SELECT 210 UNION ALL SELECT 270 UNION ALL SELECT 330 UNION ALL SELECT 360) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：9；字段：x: unknown / 原生类型未知, sind: unknown / 原生类型未知, sind_exact: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "t"
  ],
  [
    "30",
    "0.5",
    "t"
  ],
  [
    "90",
    "1",
    "t"
  ],
  [
    "150",
    "0.5",
    "t"
  ],
  [
    "180",
    "0",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 25.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'SIND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'SIND'")
doris_error_code=1105
```

### pg-float8-0168-a8fd9aee — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       cosd(x),
       cosd(x) IN (-1,-0.5,0,0.5,1) AS cosd_exact
FROM (VALUES (0), (60), (90), (120), (180),
      (240), (270), (300), (360)) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, COSD(x), COSD(x) IN (-1, -0.5, 0, 0.5, 1) AS cosd_exact FROM (SELECT 0 AS x UNION ALL SELECT 60 UNION ALL SELECT 90 UNION ALL SELECT 120 UNION ALL SELECT 180 UNION ALL SELECT 240 UNION ALL SELECT 270 UNION ALL SELECT 300 UNION ALL SELECT 360) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：9；字段：x: unknown / 原生类型未知, cosd: unknown / 原生类型未知, cosd_exact: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "1",
    "t"
  ],
  [
    "60",
    "0.5",
    "t"
  ],
  [
    "90",
    "0",
    "t"
  ],
  [
    "120",
    "-0.5",
    "t"
  ],
  [
    "180",
    "-1",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'COSD'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'COSD'")
doris_error_code=1105
```

### pg-float8-0169-763c8507 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       tand(x),
       tand(x) IN ('-Infinity'::float8,-1,0,
                   1,'Infinity'::float8) AS tand_exact,
       cotd(x),
       cotd(x) IN ('-Infinity'::float8,-1,0,
                   1,'Infinity'::float8) AS cotd_exact
FROM (VALUES (0), (45), (90), (135), (180),
      (225), (270), (315), (360)) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, TAND(x), TAND(x) IN (CAST('-Infinity' AS DOUBLE), -1, 0, 1, CAST('Infinity' AS DOUBLE)) AS tand_exact, COTD(x), COTD(x) IN (CAST('-Infinity' AS DOUBLE), -1, 0, 1, CAST('Infinity' AS DOUBLE)) AS cotd_exact FROM (SELECT 0 AS x UNION ALL SELECT 45 UNION ALL SELECT 90 UNION ALL SELECT 135 UNION ALL SELECT 180 UNION ALL SELECT 225 UNION ALL SELECT 270 UNION ALL SELECT 315 UNION ALL SELECT 360) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：9；字段：x: unknown / 原生类型未知, tand: unknown / 原生类型未知, tand_exact: unknown / 原生类型未知, cotd: unknown / 原生类型未知, cotd_exact: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0",
    "t",
    "Infinity",
    "t"
  ],
  [
    "45",
    "1",
    "t",
    "1",
    "t"
  ],
  [
    "90",
    "Infinity",
    "t",
    "0",
    "t"
  ],
  [
    "135",
    "-1",
    "t",
    "-1",
    "t"
  ],
  [
    "180",
    "0",
    "t",
    "-Infinity",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 29.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'TAND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'TAND'")
doris_error_code=1105
```

### pg-float8-0170-b46298bf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       asind(x),
       asind(x) IN (-90,-30,0,30,90) AS asind_exact,
       acosd(x),
       acosd(x) IN (0,60,90,120,180) AS acosd_exact
FROM (VALUES (-1), (-0.5), (0), (0.5), (1)) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, ASIND(x), ASIND(x) IN (-90, -30, 0, 30, 90) AS asind_exact, ACOSD(x), ACOSD(x) IN (0, 60, 90, 120, 180) AS acosd_exact FROM (SELECT -1 AS x UNION ALL SELECT -0.5 UNION ALL SELECT 0 UNION ALL SELECT 0.5 UNION ALL SELECT 1) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x: unknown / 原生类型未知, asind: unknown / 原生类型未知, asind_exact: unknown / 原生类型未知, acosd: unknown / 原生类型未知, acosd_exact: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-1",
    "-90",
    "t",
    "180",
    "t"
  ],
  [
    "-0.5",
    "-30",
    "t",
    "120",
    "t"
  ],
  [
    "0",
    "0",
    "t",
    "90",
    "t"
  ],
  [
    "0.5",
    "30",
    "t",
    "60",
    "t"
  ],
  [
    "1",
    "90",
    "t",
    "0",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'ASIND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'ASIND'")
doris_error_code=1105
```

### pg-float8-0171-b35da73e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT x,
       atand(x),
       atand(x) IN (-90,-45,0,45,90) AS atand_exact
FROM (VALUES ('-Infinity'::float8), (-1), (0), (1),
      ('Infinity'::float8)) AS t(x);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x, ATAND(x), ATAND(x) IN (-90, -45, 0, 45, 90) AS atand_exact FROM (SELECT CAST('-Infinity' AS DOUBLE) AS x UNION ALL SELECT -1 UNION ALL SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT CAST('Infinity' AS DOUBLE)) AS t
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：x: unknown / 原生类型未知, atand: unknown / 原生类型未知, atand_exact: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-Infinity",
    "-90",
    "t"
  ],
  [
    "-1",
    "-45",
    "t"
  ],
  [
    "0",
    "0",
    "t"
  ],
  [
    "1",
    "45",
    "t"
  ],
  [
    "Infinity",
    "90",
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'ATAND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'ATAND'")
doris_error_code=1105
```
