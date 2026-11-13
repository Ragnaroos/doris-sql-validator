# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:38.462746+00:00 至 2026-11-11T09:40:39.127573+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/float4.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**46**；两端成功且已有证据匹配：**11**。
- 成功结果匹配占全部查询比例：**11/46 = 23.91%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**11/37 = 29.73%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**9**；不计入上述成功匹配分子。
- 需要分析的查询：**35**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**20**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 29 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 11 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 6 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 46 条只读查询、跳过 54 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–5 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 7–7 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 8–8 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 9–9 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 10–10 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 11–11 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 13–14 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 16–16 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 19–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 20–20 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 21–21 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 14 | 22–22 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 15 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 16 | 25–25 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 17 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 27–27 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 19 | 29–30 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 20 | 31–31 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 21 | 32–32 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 22 | 33–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 23 | 34–34 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 24 | 35–35 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 25 | 36–36 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 26 | 37–37 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 59 | 97–99 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 90 | 149–154 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 91 | 155–156 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 92 | 157–158 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 93 | 159–159 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 94 | 160–160 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 95 | 161–161 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 96 | 162–162 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 97 | 163–163 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 100 | 359–360 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 30 | 43–43 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 45 | 63–63 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 46 | 65–65 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 47 | 67–67 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 48 | 69–69 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 49 | 71–71 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 50 | 73–73 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 51 | 75–75 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 52 | 77–78 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 53 | 80–81 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 54 | 83–84 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 55 | 86–87 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 56 | 89–90 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 57 | 92–92 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 58 | 94–95 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 60 | 101–101 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 98 | 165–191 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 99 | 193–357 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/float4.out`；SHA-256（文件内容指纹）：`9bd7c4709d61fa1cfa38d8ea80e136d139ecf6a32b2fb4e4d87de670004ef5e8`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 46/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 37/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 37/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 37/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/46 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-float4-0027-9d7f4076` | SELECT pg_input_is_valid('34.5', 'float4'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0028-1a832cc8` | SELECT pg_input_is_valid('xyz', 'float4'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0029-f6cc5990` | SELECT pg_input_is_valid('1e400', 'float4'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0031-8c6d7076` | SELECT 'NaN'::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0032-982df9d8` | SELECT 'nan'::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0033-9fb6cf51` | SELECT '   NAN  '::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0034-2e101523` | SELECT 'infinity'::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0035-bd624b7e` | SELECT '          -INFINiTY   '::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0036-37bab7aa` | SELECT 'N A N'::float4; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0037-2365fbf0` | SELECT 'NaN x'::float4; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0038-5fca1d84` | SELECT ' INFINITY    x'::float4; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0039-14d91d69` | SELECT 'Infinity'::float4 + 100.0; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0040-0df8893f` | SELECT 'Infinity'::float4 / 'Infinity'::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0041-0785fb35` | SELECT '42'::float4 / 'Infinity'::float4; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0042-78e546a5` | SELECT 'nan'::float4 / 'nan'::float4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0043-b1829e7e` | SELECT 'nan'::float4 / '0'::float4; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0044-48facef7` | SELECT 'nan'::numeric::float4; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0061-8dd21096` | SELECT '32767.4'::float4::int2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0062-7542c795` | SELECT '32767.6'::float4::int2; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0063-8cbd3d41` | SELECT '-32768.4'::float4::int2; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0064-4f61b554` | SELECT '-32768.6'::float4::int2; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0065-b794ca3a` | SELECT '2147483520'::float4::int4; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-float4-0066-07fa63e5` | SELECT '2147483647'::float4::int4; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0067-27fcec9b` | SELECT '-2147483648.5'::float4::int4; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0068-dc44032a` | SELECT '-2147483900'::float4::int4; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0069-908a1692` | SELECT '9223369837831520256'::float4::int8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0070-512ed2f2` | SELECT '9223372036854775807'::float4::int8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0071-63715b27` | SELECT '-9223372036854775808.5'::float4::int8; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-float4-0072-0ae71c32` | SELECT '-9223380000000000000'::float4::int8; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0073-8a7309ae` | SELECT float4send('5e-20'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0074-5c131f33` | SELECT float4send('67e14'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0075-caaebf0f` | SELECT float4send('985e15'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0076-17fb2046` | SELECT float4send('55895e-16'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0077-3fbe6777` | SELECT float4send('7038531e-32'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0078-ee9f57cc` | SELECT float4send('702990899e-20'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0079-56d41e15` | SELECT float4send('3e-23'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0080-ff3d84bc` | SELECT float4send('57e18'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0081-3fd9b918` | SELECT float4send('789e-35'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0082-dfb57bdf` | SELECT float4send('2539e-18'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0083-ee6ca093` | SELECT float4send('76173e28'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0084-559dcf23` | SELECT float4send('887745e-11'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0085-f6047f04` | SELECT float4send('5382571e-37'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0086-727d8ecc` | SELECT float4send('82381273e-35'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0087-95285bae` | SELECT float4send('750486563e-38'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0088-b066bdff` | SELECT float4send('1.17549435e-38'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-float4-0089-2d9923cc` | SELECT float4send('1.1754944e-38'::float4); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-float4-0027-9d7f4076 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('34.5', 'float4');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('34.5', 'float4')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.9 ms。
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

### pg-float4-0028-1a832cc8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('xyz', 'float4');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('xyz', 'float4')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.9 ms。
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

### pg-float4-0029-f6cc5990 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('1e400', 'float4');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('1e400', 'float4')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.9 ms。
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

### pg-float4-0036-37bab7aa — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'N A N'::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('N A N' AS FLOAT)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type real: "N A N"`。

错误原文：

```text
invalid input syntax for type real: "N A N"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.3 ms。
- 返回行数：1；字段：CAST('N A N' AS FLOAT): float / FLOAT。
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
source_error_message=invalid input syntax for type real: "N A N"
source_error_code=invalid input syntax for type real: "N A N"
```

### pg-float4-0037-2365fbf0 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 'NaN x'::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('NaN x' AS FLOAT)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type real: "NaN x"`。

错误原文：

```text
invalid input syntax for type real: "NaN x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：CAST('NaN x' AS FLOAT): float / FLOAT。
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
source_error_message=invalid input syntax for type real: "NaN x"
source_error_code=invalid input syntax for type real: "NaN x"
```

### pg-float4-0038-5fca1d84 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ' INFINITY    x'::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(' INFINITY    x' AS FLOAT)
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type real: " INFINITY    x"`。

错误原文：

```text
invalid input syntax for type real: " INFINITY    x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.5 ms。
- 返回行数：1；字段：CAST(' INFINITY    x' AS FLOAT): float / FLOAT。
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
source_error_message=invalid input syntax for type real: " INFINITY    x"
source_error_code=invalid input syntax for type real: " INFINITY    x"
```

### pg-float4-0041-0785fb35 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '42'::float4 / 'Infinity'::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('42' AS FLOAT) / CAST('Infinity' AS FLOAT)
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

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CAST('42' AS FLOAT) / CAST('Infinity' AS FLOAT): float / DOUBLE。
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

### pg-float4-0043-b1829e7e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::float4 / '0'::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('nan' AS FLOAT) / CAST('0' AS FLOAT)
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

- 执行状态：成功；耗时 11.0 ms。
- 返回行数：1；字段：CAST('nan' AS FLOAT) / CAST('0' AS FLOAT): float / DOUBLE。
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

### pg-float4-0044-48facef7 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 'nan'::numeric::float4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('nan' AS DECIMAL) AS FLOAT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "NaN"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.8 ms。
- 返回行数：1；字段：CAST(CAST('nan' AS DECIMAL) AS FLOAT): float / FLOAT。
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

### pg-float4-0062-7542c795 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '32767.6'::float4::int2;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('32767.6' AS FLOAT) AS SMALLINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`smallint out of range`。

错误原文：

```text
smallint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：CAST(CAST('32767.6' AS FLOAT) AS SMALLINT): integer / SMALLINT。
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

### pg-float4-0064-4f61b554 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-32768.6'::float4::int2;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-32768.6' AS FLOAT) AS SMALLINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`smallint out of range`。

错误原文：

```text
smallint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CAST(CAST('-32768.6' AS FLOAT) AS SMALLINT): integer / SMALLINT。
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

### pg-float4-0066-07fa63e5 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '2147483647'::float4::int4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('2147483647' AS FLOAT) AS INT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.9 ms。
- 返回行数：1；字段：CAST(CAST('2147483647' AS FLOAT) AS INT): integer / INT。
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
source_error_message=integer out of range
source_error_code=integer out of range
```

### pg-float4-0067-27fcec9b — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '-2147483648.5'::float4::int4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-2147483648.5' AS FLOAT) AS INT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：int4: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：CAST(CAST('-2147483648.5' AS FLOAT) AS INT): integer / INT。
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

### pg-float4-0068-dc44032a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-2147483900'::float4::int4;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-2147483900' AS FLOAT) AS INT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：CAST(CAST('-2147483900' AS FLOAT) AS INT): integer / INT。
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
source_error_message=integer out of range
source_error_code=integer out of range
```

### pg-float4-0069-908a1692 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '9223369837831520256'::float4::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('9223369837831520256' AS FLOAT) AS BIGINT)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：int8: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223369837831520256"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.5 ms。
- 返回行数：1；字段：CAST(CAST('9223369837831520256' AS FLOAT) AS BIGINT): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    9223369800000000000
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

### pg-float4-0070-512ed2f2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '9223372036854775807'::float4::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('9223372036854775807' AS FLOAT) AS BIGINT)
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
- 返回行数：1；字段：CAST(CAST('9223372036854775807' AS FLOAT) AS BIGINT): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    9223372000000000000
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

### pg-float4-0071-63715b27 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '-9223372036854775808.5'::float4::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-9223372036854775808.5' AS FLOAT) AS BIGINT)
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

- 执行状态：成功；耗时 11.9 ms。
- 返回行数：1；字段：CAST(CAST('-9223372036854775808.5' AS FLOAT) AS BIGINT): integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -9223372000000000000
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

### pg-float4-0072-0ae71c32 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '-9223380000000000000'::float4::int8;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('-9223380000000000000' AS FLOAT) AS BIGINT)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bigint out of range`。

错误原文：

```text
bigint out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.4 ms。
- 返回行数：1；字段：CAST(CAST('-9223380000000000000' AS FLOAT) AS BIGINT): integer / BIGINT。
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

### pg-float4-0073-8a7309ae — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('5e-20'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('5e-20' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x1f6c1e4a"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0074-5c131f33 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('67e14'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('67e14' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x59be6cea"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.9 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0075-caaebf0f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('985e15'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('985e15' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x5d5ab6c4"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0076-17fb2046 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('55895e-16'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('55895e-16' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x2cc4a9bd"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0077-3fbe6777 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('7038531e-32'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('7038531e-32' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x15ae43fd"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0078-ee9f57cc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('702990899e-20'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('702990899e-20' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x2cf757ca"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0079-56d41e15 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('3e-23'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('3e-23' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x1a111234"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0080-ff3d84bc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('57e18'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('57e18' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x6045c22c"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0081-3fd9b918 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('789e-35'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('789e-35' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x0a23de70"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 16.7 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0082-dfb57bdf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('2539e-18'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('2539e-18' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x2736f449"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0083-ee6ca093 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('76173e28'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('76173e28' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x7616398a"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 15.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0084-559dcf23 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('887745e-11'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('887745e-11' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x3714f05c"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.8 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0085-f6047f04 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('5382571e-37'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('5382571e-37' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x0d2eaca7"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.5 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0086-727d8ecc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('82381273e-35'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('82381273e-35' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x128289d1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.3 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0087-95285bae — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('750486563e-38'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('750486563e-38' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x0f18377e"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.4 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0088-b066bdff — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('1.17549435e-38'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('1.17549435e-38' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x00800000"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.2 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```

### pg-float4-0089-2d9923cc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT float4send('1.1754944e-38'::float4);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT FLOAT4SEND(CAST('1.1754944e-38' AS FLOAT))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：float4send: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "\\x00800000"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
- 错误类别：函数不存在或调用形式不受支持（`FUNCTION_NOT_FOUND`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Can not found function 'FLOAT4SEND'")
doris_error_code=1105
```
