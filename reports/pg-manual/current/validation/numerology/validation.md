# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:30.658825+00:00 至 2026-11-11T09:40:31.589779+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/numerology.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**54**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/54 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/33 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**21**；不计入上述成功匹配分子。
- 需要分析的查询：**54**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**24**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 27 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 8 |
| 返回字段数量、名称或类型不同（`RESULT_SCHEMA_MISMATCH`） | 13 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 5 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 54 条只读查询、跳过 24 条非查询、0 条待确认、11 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 36 | 54–54 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 37 | 55–55 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 52 | 76–76 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m000_005; |
| 53 | 77–77 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m; |
| 55 | 79–79 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m5e0_1; |
| 56 | 81–88 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 61 | 96–96 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 14.   SELECT 1_000_[4m.[0m5; |
| 62 | 97–97 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m_5; |
| 63 | 98–98 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m5_; |
| 64 | 99–99 | 导入失败；类型 `parse_error` | Invalid expression / Unexpected token. Line 1, Col: 13.   SELECT 1_000[4m.[0m5e_1; |
| 65 | 101–101 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Command |
| 66 | 103–109 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 67 | 111–112 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 68 | 114–115 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 70 | 120–122 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 71 | 124–126 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 72 | 128–129 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 74 | 134–136 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 75 | 138–140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 142–144 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 78 | 149–153 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 79 | 155–157 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 80 | 159–161 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 86 | 189–189 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 87 | 191–191 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 88 | 193–193 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 89 | 195–195 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 69 | 117–118 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 73 | 131–132 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 77 | 146–147 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 81 | 163–163 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 82 | 165–168 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 83 | 170–175 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 84 | 177–180 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 85 | 182–187 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/numerology.out`；SHA-256（文件内容指纹）：`f9d55aa1c39d7c79e50d747c3da16e0190a9e90c8fd5233c46258e808c0c955a`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 54/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 33/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 33/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 33/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/54 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-numerology-0001-bf1fea25` | SELECT 0b100101; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0002-4393fd29` | SELECT 0o273; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0003-bc278c1f` | SELECT 0x42F; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numerology-0004-5b3e7f7e` | SELECT 0b1111111111111111111111111111111; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0005-68d49865` | SELECT 0b10000000000000000000000000000000; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0006-2c1a7e8b` | SELECT 0o17777777777; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0007-113b58a4` | SELECT 0o20000000000; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0008-e7bc3623` | SELECT 0x7FFFFFFF; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numerology-0009-69ae7cae` | SELECT 0x80000000; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numerology-0010-8616092f` | SELECT -0b10000000000000000000000000000000; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0011-d12aadfa` | SELECT -0b10000000000000000000000000000001; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0012-8e6f36b0` | SELECT -0o20000000000; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0013-749586fe` | SELECT -0o20000000001; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0014-997ce8ed` | SELECT -0x80000000; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0015-19d5c006` | SELECT -0x80000001; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0016-554fa98c` | SELECT 0b111111111111111111111111111111111111111111111111111111111111111; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0017-73d4763f` | SELECT 0b1000000000000000000000000000000000000000000000000000000000000000; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0018-7a05d9a2` | SELECT 0o777777777777777777777; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0019-335c2dae` | SELECT 0o1000000000000000000000; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0020-885d9173` | SELECT 0x7FFFFFFFFFFFFFFF; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numerology-0021-65b661c9` | SELECT 0x8000000000000000; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-numerology-0022-72c6b526` | SELECT -0b1000000000000000000000000000000000000000000000000000000000000000; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0023-529faf1e` | SELECT -0b1000000000000000000000000000000000000000000000000000000000000001; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0024-6a9c516b` | SELECT -0o1000000000000000000000; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0025-f8ec6ef6` | SELECT -0o1000000000000000000001; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0026-ffe92375` | SELECT -0x8000000000000000; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0027-c26c0457` | SELECT -0x8000000000000001; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0028-4f02026b` | SELECT 123abc; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0029-c7e45ec9` | SELECT 0x0o; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0030-c1db4386` | SELECT 0.a; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0031-71d2199a` | SELECT 0.0a; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0032-71d2199a` | SELECT .0a; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0033-33a201b2` | SELECT 0.0e1a; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0034-0597a37e` | SELECT 0.0e; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0035-97a6754a` | SELECT 0.0e+a; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0038-40292161` | SELECT 0b; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0039-2cf24225` | SELECT 1b; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0040-33157fdf` | SELECT 0b0x; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0041-4efe6eaa` | SELECT 0o; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0042-077be3a9` | SELECT 1o; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0043-c31d8dd1` | SELECT 0o0x; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0044-a9ff2e9b` | SELECT 0x; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0045-c3b9b519` | SELECT 1x; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0046-cf0a0c41` | SELECT 0x0y; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0047-b021aae2` | SELECT 1_000_000; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0048-28a108ba` | SELECT 1_2_3; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0049-9b45177b` | SELECT 0x1EEE_FFFF; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0050-0c169c9a` | SELECT 0o2_73; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0051-33408a72` | SELECT 0b_10_0101; | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0054-8a209ea6` | SELECT .000_005; | 已生成 | 成功 | 成功 | 返回字段数量、名称或类型不同 |
| `pg-numerology-0057-f1dc0d67` | SELECT _100; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-numerology-0058-3d65d0e3` | SELECT 100_; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0059-d73d9e0e` | SELECT 100__000; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-numerology-0060-be24813a` | SELECT _1_000.5; | 已生成 | 失败：语法解析失败 | 失败：执行失败，需阅读具体错误 | 两端均报错，但错误类别不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-numerology-0001-bf1fea25 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b100101;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'100101'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "37"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0002-4393fd29 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o273;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o273
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "187"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.0 ms。
- 返回行数：1；字段：o273: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o273'
```

### pg-numerology-0003-bc278c1f — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0x42F;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'42F'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1071"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 41.9 ms。
- 返回行数：1；字段：x'42F': string / VAR_STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$binary": "BC8="
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

### pg-numerology-0004-5b3e7f7e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b1111111111111111111111111111111;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'1111111111111111111111111111111'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483647"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0005-68d49865 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b10000000000000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'10000000000000000000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0006-2c1a7e8b — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o17777777777;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o17777777777
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483647"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 40.3 ms。
- 返回行数：1；字段：o17777777777: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o17777777777'
```

### pg-numerology-0007-113b58a4 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o20000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o20000000000
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 17.9 ms。
- 返回行数：1；字段：o20000000000: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o20000000000'
```

### pg-numerology-0008-e7bc3623 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0x7FFFFFFF;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'7FFFFFFF'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483647"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 31.5 ms。
- 返回行数：1；字段：x'7FFFFFFF': string / VAR_STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$binary": "f////w=="
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

### pg-numerology-0009-69ae7cae — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0x80000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'80000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.2 ms。
- 返回行数：1；字段：x'80000000': string / VAR_STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$binary": "gAAAAA=="
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

### pg-numerology-0010-8616092f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0b10000000000000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -b'10000000000000000000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 14.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0011-d12aadfa — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0b10000000000000000000000000000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -b'10000000000000000000000000000001'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483649"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 71.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0012-8e6f36b0 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT -0o20000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -0 AS o20000000000
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：o20000000000: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o20000000000'
```

### pg-numerology-0013-749586fe — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT -0o20000000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -0 AS o20000000001
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483649"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.6 ms。
- 返回行数：1；字段：o20000000001: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o20000000001'
```

### pg-numerology-0014-997ce8ed — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0x80000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -x'80000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483648"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.1 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
doris_error_code=1105
```

### pg-numerology-0015-19d5c006 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0x80000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -x'80000001'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-2147483649"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.4 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
doris_error_code=1105
```

### pg-numerology-0016-554fa98c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b111111111111111111111111111111111111111111111111111111111111111;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'111111111111111111111111111111111111111111111111111111111111111'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775807"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0017-73d4763f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b1000000000000000000000000000000000000000000000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'1000000000000000000000000000000000000000000000000000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0018-7a05d9a2 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o777777777777777777777;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o777777777777777777777
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775807"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.0 ms。
- 返回行数：1；字段：o777777777777777777777: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o777777777777777777777'
```

### pg-numerology-0019-335c2dae — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o1000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o1000000000000000000000
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：o1000000000000000000000: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o1000000000000000000000'
```

### pg-numerology-0020-885d9173 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0x7FFFFFFFFFFFFFFF;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'7FFFFFFFFFFFFFFF'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775807"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.8 ms。
- 返回行数：1；字段：x'7FFFFFFFFFFFFFFF': string / VAR_STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$binary": "f/////////8="
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

### pg-numerology-0021-65b661c9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 0x8000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'8000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.8 ms。
- 返回行数：1；字段：x'8000000000000000': string / VAR_STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$binary": "gAAAAAAAAAA="
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

### pg-numerology-0022-72c6b526 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0b1000000000000000000000000000000000000000000000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -b'1000000000000000000000000000000000000000000000000000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0023-529faf1e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0b1000000000000000000000000000000000000000000000000000000000000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -b'1000000000000000000000000000000000000000000000000000000000000001'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775809"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0024-6a9c516b — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT -0o1000000000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -0 AS o1000000000000000000000
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：o1000000000000000000000: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o1000000000000000000000'
```

### pg-numerology-0025-f8ec6ef6 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT -0o1000000000000000000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -0 AS o1000000000000000000001
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775809"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：o1000000000000000000001: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o1000000000000000000001'
```

### pg-numerology-0026-ffe92375 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0x8000000000000000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -x'8000000000000000'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775808"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
doris_error_code=1105
```

### pg-numerology-0027-c26c0457 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT -0x8000000000000001;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT -x'8000000000000001'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "-9223372036854775809"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
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
doris_error_message=(1105, 'errCode = 2, detailMessage = Cannot cast from VARBINARY(2147483647) to numeric type.')
doris_error_code=1105
```

### pg-numerology-0028-4f02026b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 123abc;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 123 AS abc
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "123abc"`。

错误原文：

```text
trailing junk after numeric literal at or near "123abc"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：abc: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    123
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
source_error_message=trailing junk after numeric literal at or near "123abc"
source_error_code=trailing junk after numeric literal at or near "123abc"
```

### pg-numerology-0029-c7e45ec9 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0x0o;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT `0x0o`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0x0o"`。

错误原文：

```text
trailing junk after numeric literal at or near "0x0o"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '0x0o' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0030-c1db4386 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0.a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0. AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0.a"`。

错误原文：

```text
trailing junk after numeric literal at or near "0.a"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：a: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0"
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
source_error_message=trailing junk after numeric literal at or near "0.a"
source_error_code=trailing junk after numeric literal at or near "0.a"
```

### pg-numerology-0031-71d2199a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0.0a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.0 AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0.0a"`。

错误原文：

```text
trailing junk after numeric literal at or near "0.0a"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：a: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0.0"
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
source_error_message=trailing junk after numeric literal at or near "0.0a"
source_error_code=trailing junk after numeric literal at or near "0.0a"
```

### pg-numerology-0032-71d2199a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT .0a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.0 AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near ".0a"`。

错误原文：

```text
trailing junk after numeric literal at or near ".0a"
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.8 ms。
- 返回行数：1；字段：a: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0.0"
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
source_error_message=trailing junk after numeric literal at or near ".0a"
source_error_code=trailing junk after numeric literal at or near ".0a"
```

### pg-numerology-0033-33a201b2 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0.0e1a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.0e1 AS a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0.0e1a"`。

错误原文：

```text
trailing junk after numeric literal at or near "0.0e1a"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.5 ms。
- 返回行数：1；字段：a: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0"
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
source_error_message=trailing junk after numeric literal at or near "0.0e1a"
source_error_code=trailing junk after numeric literal at or near "0.0e1a"
```

### pg-numerology-0034-0597a37e — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0.0e;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.0e
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0.0e"`。

错误原文：

```text
trailing junk after numeric literal at or near "0.0e"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Can not dereference field: 0e')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0035-97a6754a — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0.0e+a;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.0e + a
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0.0e+"`。

错误原文：

```text
trailing junk after numeric literal at or near "0.0e+"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 16.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, 'errCode = 2, detailMessage = Can not dereference field: 0e')
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0038-40292161 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0b;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT `0b`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid binary integer at or near "0b"`。

错误原文：

```text
invalid binary integer at or near "0b"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '0b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0039-2cf24225 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 1b;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 1 AS b
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "1b"`。

错误原文：

```text
trailing junk after numeric literal at or near "1b"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：b: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1
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
source_error_message=trailing junk after numeric literal at or near "1b"
source_error_code=trailing junk after numeric literal at or near "1b"
```

### pg-numerology-0040-33157fdf — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0b0x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT `0b0x`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0b0x"`。

错误原文：

```text
trailing junk after numeric literal at or near "0b0x"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '0b0x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0041-4efe6eaa — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0o;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid octal integer at or near "0o"`。

错误原文：

```text
invalid octal integer at or near "0o"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：o: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0
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
source_error_message=invalid octal integer at or near "0o"
source_error_code=invalid octal integer at or near "0o"
```

### pg-numerology-0042-077be3a9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 1o;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 1 AS o
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "1o"`。

错误原文：

```text
trailing junk after numeric literal at or near "1o"
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.5 ms。
- 返回行数：1；字段：o: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1
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
source_error_message=trailing junk after numeric literal at or near "1o"
source_error_code=trailing junk after numeric literal at or near "1o"
```

### pg-numerology-0043-c31d8dd1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0o0x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o0x
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0o0x"`。

错误原文：

```text
trailing junk after numeric literal at or near "0o0x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.1 ms。
- 返回行数：1；字段：o0x: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    0
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
source_error_message=trailing junk after numeric literal at or near "0o0x"
source_error_code=trailing junk after numeric literal at or near "0o0x"
```

### pg-numerology-0044-a9ff2e9b — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT `0x`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`invalid hexadecimal integer at or near "0x"`。

错误原文：

```text
invalid hexadecimal integer at or near "0x"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '0x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0045-c3b9b519 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 1x;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 1 AS x
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "1x"`。

错误原文：

```text
trailing junk after numeric literal at or near "1x"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.9 ms。
- 返回行数：1；字段：x: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1
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
source_error_message=trailing junk after numeric literal at or near "1x"
source_error_code=trailing junk after numeric literal at or near "1x"
```

### pg-numerology-0046-cf0a0c41 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT 0x0y;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT `0x0y`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "0x0y"`。

错误原文：

```text
trailing junk after numeric literal at or near "0x0y"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '0x0y' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0047-b021aae2 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 1_000_000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 1 AS _000_000
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1000000"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.5 ms。
- 返回行数：1；字段：_000_000: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Canonical result schemas differ
column[0] name: source='?column?', doris='_000_000'
```

### pg-numerology-0048-28a108ba — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 1_2_3;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 1 AS _2_3
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "123"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.5 ms。
- 返回行数：1；字段：_2_3: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    1
  ]
]
```

#### 后续应如何判断

- 读取实际字段、结果样本和错误；必要时连接 PostgreSQL 补取类型、完整结果及错误原因。
- 用独立 Doris 候选区分 SQLGlot 转换问题、Doris 原生行为/能力限制和比较器误报；一个候选失败不证明 Doris 无法实现。
- 独立候选须另存执行证据，分别检查类型、值、要求的顺序以及有意义的 NULL、空输入、重复行或非法输入边界。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Canonical result schemas differ
column[0] name: source='?column?', doris='_2_3'
```

### pg-numerology-0049-9b45177b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0x1EEE_FFFF;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'1EEE_FFFF'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "518979583"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0050-0c169c9a — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT 0o2_73;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0 AS o2_73
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "187"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.7 ms。
- 返回行数：1；字段：o2_73: integer / TINYINT。
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
Canonical result schemas differ
column[0] name: source='?column?', doris='o2_73'
```

### pg-numerology-0051-33408a72 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 0b_10_0101;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'_10_0101'
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "37"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
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
doris_error_message=(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
doris_error_code=1105
```

### pg-numerology-0054-8a209ea6 — 返回字段数量、名称或类型不同

#### 源 SQL

```sql
SELECT .000_005;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 0.000 AS _005
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：?column?: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0.000005"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.9 ms。
- 返回行数：1；字段：_005: decimal / DECIMAL。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$decimal": "0.000"
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
Canonical result schemas differ
column[0] name: source='?column?', doris='_005'
```

### pg-numerology-0057-f1dc0d67 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT _100;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT _100
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`column "_100" does not exist`。

错误原文：

```text
column "_100" does not exist
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column '_100' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-numerology-0058-3d65d0e3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 100_;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 100 AS _
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "100_"`。

错误原文：

```text
trailing junk after numeric literal at or near "100_"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：_: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    100
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
source_error_message=trailing junk after numeric literal at or near "100_"
source_error_code=trailing junk after numeric literal at or near "100_"
```

### pg-numerology-0059-d73d9e0e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT 100__000;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 100 AS __000
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`trailing junk after numeric literal at or near "100__000"`。

错误原文：

```text
trailing junk after numeric literal at or near "100__000"
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.0 ms。
- 返回行数：1；字段：__000: integer / TINYINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    100
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
source_error_message=trailing junk after numeric literal at or near "100__000"
source_error_code=trailing junk after numeric literal at or near "100__000"
```

### pg-numerology-0060-be24813a — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT _1_000.5;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT _1_000.5
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`syntax error at or near ".5"`。

错误原文：

```text
syntax error at or near ".5"
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '.5' expecting {<EOF>, ';'}(line 1, pos 13)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=PARSE_ERROR
source_error_message=syntax error at or near ".5"
source_error_code=syntax error at or near ".5"
doris_error_category=EXECUTION_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '.5' expecting {<EOF>, ';'}(line 1, pos 13)\n")
doris_error_code=1105
```
