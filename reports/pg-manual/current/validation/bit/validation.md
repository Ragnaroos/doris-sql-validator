# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:24.959081+00:00 至 2026-11-11T09:40:25.847332+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/bit.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**66**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/66 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/57 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**9**；不计入上述成功匹配分子。
- 需要分析的查询：**66**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**66**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端均报错，但错误类别不同（`ERROR_BEHAVIOR_MISMATCH`） | 1 |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 57 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 8 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 66 条只读查询、跳过 65 条非查询、0 条待确认、1 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–9 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 11–11 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 11–12 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 13–13 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 14–14 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 21–21 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 39.   CREATE TABLE VARBIT_TABLE(v BIT [4mVARYING[0m(11)); |
| 9 | 23–23 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 25–25 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 27–27 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 30 | 69–70 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 31 | 71–71 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 40.   CREATE TABLE varbit_table (a BIT [4mVARYING[0m(16), b BIT VARYING(16)); |
| 32 | 72–72 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 36 | 91–91 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 37 | 93–94 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 38 | 95–95 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 39 | 96–96 | 跳过非查询；类型 `copy` | Expected one read-only Query, got Copy |
| 43 | 115–115 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 85 | 169–174 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 86 | 175–175 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 87 | 176–176 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 88 | 177–177 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 89 | 178–178 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 90 | 179–179 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 96 | 194–194 | 跳过非查询；类型 `create` | Expecting ). Line 1, Col: 45.   CREATE TABLE VARBIT_SHIFT_TABLE(v BIT [4mVARYING[0m(20)); |
| 97 | 195–195 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 98 | 196–196 | 跳过非查询；类型 `insert` | Invalid expression / Unexpected token. Line 1, Col: 68.   INSERT INTO VARBIT_SHIFT_TABLE SELECT CAST(v \|\| B'0' AS BIT VARYING[4m([0m6)) >>1 FROM VARBIT_SHIFT_TABLE; |
| 99 | 197–197 | 跳过非查询；类型 `insert` | Invalid expression / Unexpected token. Line 1, Col: 69.   INSERT INTO VARBIT_SHIFT_TABLE SELECT CAST(v \|\| B'00' AS BIT VARYING[4m([0m8)) >>2 FROM VARBIT_SHIFT_TABLE; |
| 100 | 198–198 | 跳过非查询；类型 `insert` | Invalid expression / Unexpected token. Line 1, Col: 71.   INSERT INTO VARBIT_SHIFT_TABLE SELECT CAST(v \|\| B'0000' AS BIT VARYING[4m([0m12)) >>4 FROM VARBIT_SHIFT_TABLE; |
| 101 | 199–199 | 跳过非查询；类型 `insert` | Invalid expression / Unexpected token. Line 1, Col: 75.   INSERT INTO VARBIT_SHIFT_TABLE SELECT CAST(v \|\| B'00000000' AS BIT VARYING[4m([0m20)) >>8 FROM VARBIT_SHIFT_TABLE; |
| 105 | 209–209 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 106 | 210–210 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 120 | 231–237 | 跳过非查询；类型 `create` | Expecting ). Line 4, Col: 16.   CREATE TABLE bit_defaults(   b1 bit(4) DEFAULT '1001',   b2 bit(4) DEFAULT B'0101',   b3 bit [4mvarying[0m(5) DEFAULT '1001',   b4 bit varying(5) DEFAULT B'0101' ); |
| 121 | 238–239 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 122 | 240–240 | 导入失败；类型 `parse_error` | Expected one read-only Query, got Alias |
| 7 | 15–19 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 14 | 27–30 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 19 | 38–41 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 20 | 43–45 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 21 | 46–47 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 22 | 49–54 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 23 | 55–59 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 27 | 65–65 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 28 | 66–66 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 29 | 67–67 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 33 | 73–86 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 34 | 87–88 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 35 | 89–89 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 40 | 97–110 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 41 | 111–112 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 42 | 113–113 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 91 | 180–183 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 92 | 184–185 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 93 | 186–187 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 94 | 188–189 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 95 | 190–191 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 102 | 200–203 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 103 | 204–205 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 104 | 206–207 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 124 | 244–244 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 126 | 246–246 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 128 | 248–248 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 130 | 251–251 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 132 | 253–253 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/bit.out`；SHA-256（文件内容指纹）：`35d744ebbbf5cdb1910792ea944ef9b05c72a1641eeb97c30b88ecefefab65a4`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 66/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 66/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 57/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 57/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 57/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/66 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-bit-0015-ababd899` | SELECT b' 0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0016-61bca181` | SELECT b'0 '; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0017-d071168a` | SELECT x' 0'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0018-8fbe6087` | SELECT x'0 '; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0024-89958cf4` | SELECT SUBSTRING('01010101'::bit(8) FROM 2 FOR 2147483646) AS "1010101"; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0025-6b3902a8` | SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR 2147483646) AS "01010101"; | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0026-af154103` | SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR -2147483646) AS "error"; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：类型转换失败 | 两端均报错，但错误类别不同 |
| `pg-bit-0044-e16f06ff` | select B'001' & B'10'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0045-1ef7e230` | select B'0111' \| B'011'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0046-479ef11f` | select B'0010' # B'011101'; | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0047-301a8e99` | SELECT POSITION(B'1010' IN B'0000101'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0048-caf7f5b8` | SELECT POSITION(B'1010' IN B'00001010'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0049-595c054b` | SELECT POSITION(B'1010' IN B'00000101'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0050-bb4bcf7c` | SELECT POSITION(B'1010' IN B'000001010'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0051-3a142de9` | SELECT POSITION(B'' IN B'00001010'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0052-00592fea` | SELECT POSITION(B'0' IN B''); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0053-42e1d4df` | SELECT POSITION(B'' IN B''); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0054-1ecd298b` | SELECT POSITION(B'101101' IN B'001011011011011000'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0055-2846a24a` | SELECT POSITION(B'10110110' IN B'001011011011010'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0056-fcfbadfd` | SELECT POSITION(B'1011011011011' IN B'001011011011011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0057-93be16f6` | SELECT POSITION(B'1011011011011' IN B'00001011011011011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0058-30959611` | SELECT POSITION(B'11101011' IN B'11101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0059-58faa847` | SELECT POSITION(B'11101011' IN B'011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0060-92ceb8e3` | SELECT POSITION(B'11101011' IN B'00011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0061-97441cec` | SELECT POSITION(B'11101011' IN B'0000011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0062-d1d81002` | SELECT POSITION(B'111010110' IN B'111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0063-70bb2d0f` | SELECT POSITION(B'111010110' IN B'0111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0064-cb7ca512` | SELECT POSITION(B'111010110' IN B'000111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0065-064bcc08` | SELECT POSITION(B'111010110' IN B'00000111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0066-6b7cee3e` | SELECT POSITION(B'111010110' IN B'11101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0067-0f374bcc` | SELECT POSITION(B'111010110' IN B'011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0068-d261399c` | SELECT POSITION(B'111010110' IN B'00011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0069-dba0b492` | SELECT POSITION(B'111010110' IN B'0000011101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0070-d1d81002` | SELECT POSITION(B'111010110' IN B'111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0071-70bb2d0f` | SELECT POSITION(B'111010110' IN B'0111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0072-cb7ca512` | SELECT POSITION(B'111010110' IN B'000111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0073-064bcc08` | SELECT POSITION(B'111010110' IN B'00000111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0074-d546974c` | SELECT POSITION(B'111010110' IN B'000001110101111101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0075-7a835daf` | SELECT POSITION(B'111010110' IN B'0000001110101111101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0076-14193951` | SELECT POSITION(B'111010110' IN B'000000001110101111101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0077-dfb6069c` | SELECT POSITION(B'111010110' IN B'00000000001110101111101011'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0078-217a86de` | SELECT POSITION(B'111010110' IN B'0000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0079-09b22e90` | SELECT POSITION(B'111010110' IN B'00000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0080-552fd82c` | SELECT POSITION(B'111010110' IN B'0000000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0081-ac8b2e03` | SELECT POSITION(B'111010110' IN B'000000000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0082-21fef106` | SELECT POSITION(B'000000000011101011111010110' IN B'000000000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0083-8313870d` | SELECT POSITION(B'00000000011101011111010110' IN B'000000000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0084-e9975bc6` | SELECT POSITION(B'0000000000011101011111010110' IN B'000000000011101011111010110'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0107-124a125e` | SELECT get_bit(B'0101011000100', 10); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0108-73e11c02` | SELECT set_bit(B'0101011000100100', 15, 1); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0109-73f2b61f` | SELECT set_bit(B'0101011000100100', 16, 1); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-bit-0110-6542d715` | SELECT overlay(B'0101011100' placing '001' from 2 for 3); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0111-0e365504` | SELECT overlay(B'0101011100' placing '101' from 6); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0112-f46cc6df` | SELECT overlay(B'0101011100' placing '001' from 11); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0113-3453faf6` | SELECT overlay(B'0101011100' placing '001' from 20); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0114-941c9a67` | SELECT bit_count(B'0101011100'::bit(10)); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0115-f2a0ef80` | SELECT bit_count(B'1111111111'::bit(10)); | 已生成 | 成功 | 失败：类型转换失败 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0116-3c6fed87` | SELECT bit_count(repeat('0', 100)::bit(100)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0117-2b92a352` | SELECT bit_count(repeat('1', 100)::bit(100)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0118-fc3fdefd` | SELECT bit_count(repeat('01', 500)::bit(1000)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0119-949253dd` | SELECT bit_count(repeat('10101', 200)::bit(1000)); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0123-64e8d6bc` | SELECT pg_input_is_valid('01010001', 'bit(10)'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0125-086339bb` | SELECT pg_input_is_valid('01010Z01', 'bit(8)'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0127-81e3a323` | SELECT pg_input_is_valid('x01010Z01', 'bit(32)'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0129-b5856278` | SELECT pg_input_is_valid('01010Z01', 'varbit'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-bit-0131-d7060d25` | SELECT pg_input_is_valid('x01010Z01', 'varbit'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-bit-0015-ababd899 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT b' 0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b' 0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`" " is not a valid binary digit`。

错误原文：

```text
" " is not a valid binary digit
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 16.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0016-61bca181 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT b'0 ';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'0 '
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`" " is not a valid binary digit`。

错误原文：

```text
" " is not a valid binary digit
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'b' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0017-d071168a — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT x' 0';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x' 0'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`" " is not a valid hexadecimal digit`。

错误原文：

```text
" " is not a valid hexadecimal digit
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0018-8fbe6087 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT x'0 ';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT x'0 '
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`" " is not a valid hexadecimal digit`。

错误原文：

```text
" " is not a valid hexadecimal digit
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = Unknown column 'x' in 'table list' in UNBOUND_ONE_ROW_RELATION clause(line 1, pos 7)")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0024-89958cf4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT SUBSTRING('01010101'::bit(8) FROM 2 FOR 2147483646) AS "1010101";
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUBSTRING(CAST('01010101' AS BIT(8)), 2, 2147483646) AS `1010101`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：1010101: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1010101"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 11.1 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-bit-0025-6b3902a8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR 2147483646) AS "01010101";
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUBSTRING(CAST('01010101' AS BIT(8)), -10, 2147483646) AS `01010101`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：01010101: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "01010101"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.9 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-bit-0026-af154103 — 两端均报错，但错误类别不同

#### 源 SQL

```sql
SELECT SUBSTRING('01010101'::bit(8) FROM -10 FOR -2147483646) AS "error";
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SUBSTRING(CAST('01010101' AS BIT(8)), -10, -2147483646) AS `error`
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`negative substring length not allowed`。

错误原文：

```text
negative substring length not allowed
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 12.2 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed, but normalized error categories differ
source_error_category=EXECUTION_ERROR
source_error_message=negative substring length not allowed
source_error_code=negative substring length not allowed
doris_error_category=CAST_ERROR
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'SUBSTRING(CAST('01010101' AS BIT'(line 1, pos 36)\n")
doris_error_code=1105
```

### pg-bit-0044-e16f06ff — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select B'001' & B'10';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'001' & b'10'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot AND bit strings of different sizes`。

错误原文：

```text
cannot AND bit strings of different sizes
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '&' expecting {<EOF>, ';'}(line 1, pos 14)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0045-1ef7e230 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select B'0111' | B'011';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'0111' | b'011'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot OR bit strings of different sizes`。

错误原文：

```text
cannot OR bit strings of different sizes
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '|' expecting {<EOF>, ';'}(line 1, pos 15)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0046-479ef11f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
select B'0010' # B'011101';
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT b'0010' ^ b'011101'
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`cannot XOR bit strings of different sizes`。

错误原文：

```text
cannot XOR bit strings of different sizes
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '^' expecting {<EOF>, ';'}(line 1, pos 15)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0047-301a8e99 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1010' IN B'0000101');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1010', b'0000101')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0048-caf7f5b8 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1010' IN B'00001010');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1010', b'00001010')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0049-595c054b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1010' IN B'00000101');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1010', b'00000101')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0050-bb4bcf7c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1010' IN B'000001010');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1010', b'000001010')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1010'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0051-3a142de9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'' IN B'00001010');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'', b'00001010')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0052-00592fea — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'0' IN B'');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'0', b'')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''0'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0053-42e1d4df — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'' IN B'');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'', b'')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input '''' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0054-1ecd298b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'101101' IN B'001011011011011000');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'101101', b'001011011011011000')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''101101'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''101101'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0055-2846a24a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'10110110' IN B'001011011011010');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'10110110', b'001011011011010')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''10110110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''10110110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0056-fcfbadfd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1011011011011' IN B'001011011011011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1011011011011', b'001011011011011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "3"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0057-93be16f6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'1011011011011' IN B'00001011011011011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'1011011011011', b'00001011011011011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''1011011011011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0058-30959611 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'11101011' IN B'11101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'11101011', b'11101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 19.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0059-58faa847 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'11101011' IN B'011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'11101011', b'011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 16.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0060-92ceb8e3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'11101011' IN B'00011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'11101011', b'00011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "4"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0061-97441cec — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'11101011' IN B'0000011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'11101011', b'0000011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''11101011'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0062-d1d81002 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0063-70bb2d0f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0064-cb7ca512 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'000111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'000111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "4"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0065-064bcc08 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'00000111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'00000111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0066-6b7cee3e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'11101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'11101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0067-0f374bcc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0068-d261399c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'00011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'00011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0069-dba0b492 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0000011101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0000011101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0070-d1d81002 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0071-70bb2d0f — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0072-cb7ca512 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'000111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'000111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "4"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0073-064bcc08 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'00000111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'00000111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "6"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 12.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0074-d546974c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'000001110101111101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'000001110101111101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0075-7a835daf — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0000001110101111101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0000001110101111101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0076-14193951 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'000000001110101111101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'000000001110101111101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0077-dfb6069c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'00000000001110101111101011');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'00000000001110101111101011')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0078-217a86de — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "14"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0079-09b22e90 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'00000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'00000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "15"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0080-552fd82c — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'0000000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'0000000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "17"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.9 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0081-ac8b2e03 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'111010110' IN B'000000000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'111010110', b'000000000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "19"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0082-21fef106 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'000000000011101011111010110' IN B'000000000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'000000000011101011111010110', b'000000000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0083-8313870d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'00000000011101011111010110' IN B'000000000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'00000000011101011111010110', b'000000000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''00000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''00000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0084-e9975bc6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT POSITION(B'0000000000011101011111010110' IN B'000000000011101011111010110');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT LOCATE(b'0000000000011101011111010110', b'000000000011101011111010110')
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：position: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''0000000000011101011111010110'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0107-124a125e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT get_bit(B'0101011000100', 10);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT GETBIT(b'0101011000100', 10)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：get_bit: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 18.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100'' expecting {')', ',', 'ORDER'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-bit-0108-73e11c02 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT set_bit(B'0101011000100100', 15, 1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SET_BIT(b'0101011000100100', 15, 1)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：set_bit: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0101011000100101"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
doris_error_code=1105
```

### pg-bit-0109-73f2b61f — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT set_bit(B'0101011000100100', 16, 1);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT SET_BIT(b'0101011000100100', 16, 1)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`bit index 16 out of valid range (0..15)`。

错误原文：

```text
bit index 16 out of valid range (0..15)
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.3 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nextraneous input ''0101011000100100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-bit-0110-6542d715 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT overlay(B'0101011100' placing '001' from 2 for 3);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 2 FOR 3)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：overlay: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0001011100"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
doris_error_code=1105
```

### pg-bit-0111-0e365504 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT overlay(B'0101011100' placing '101' from 6);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT OVERLAY(b'0101011100' PLACING '101' FROM 6)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：overlay: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0101010100"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
doris_error_code=1105
```

### pg-bit-0112-f46cc6df — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT overlay(B'0101011100' placing '001' from 11);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 11)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：overlay: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0101011100001"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 15.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
doris_error_code=1105
```

### pg-bit-0113-3453faf6 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT overlay(B'0101011100' placing '001' from 20);
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT OVERLAY(b'0101011100' PLACING '001' FROM 20)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：overlay: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0101011100001"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.2 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input ''0101011100'' expecting {')', ',', 'ORDER'}(line 1, pos 16)\n")
doris_error_code=1105
```

### pg-bit-0114-941c9a67 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(B'0101011100'::bit(10));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(b'0101011100' AS BIT(10)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "5"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'0101011100''(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'0101011100''(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-bit-0115-f2a0ef80 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(B'1111111111'::bit(10));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(b'1111111111' AS BIT(10)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "10"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：类型转换失败；耗时 10.7 ms。
- 错误类别：类型转换失败（`CAST_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'1111111111''(line 1, pos 23)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(b'1111111111''(line 1, pos 23)\n")
doris_error_code=1105
```

### pg-bit-0116-3c6fed87 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(repeat('0', 100)::bit(100));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(REPEAT('0', 100) AS BIT(100)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.4 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-bit-0117-2b92a352 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(repeat('1', 100)::bit(100));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(REPEAT('1', 100) AS BIT(100)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "100"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.6 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 42)\n")
doris_error_code=1105
```

### pg-bit-0118-fc3fdefd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(repeat('01', 500)::bit(1000));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(REPEAT('01', 500) AS BIT(1000)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "500"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 43)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 43)\n")
doris_error_code=1105
```

### pg-bit-0119-949253dd — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bit_count(repeat('10101', 200)::bit(1000));
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT BIT_COUNT(CAST(REPEAT('10101', 200) AS BIT(1000)))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：bit_count: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "600"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.5 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'BIT' expecting {'AGG_STATE', 'ALL', 'ARRAY', 'BIGINT', 'BITMAP', 'BOOLEAN', CHAR, 'DATE', 'DATETIME', 'DATETIMEV2', 'DATEV2', 'DATETIMEV1', 'DATEV1', 'DECIMAL', 'DECIMALV2', 'DECIMALV3', 'DOUBLE', 'FLOAT', 'HLL', 'INT', 'INTEGER', 'IPV4', 'IPV6', 'JSON', 'JSONB', 'LARGEINT', 'MAP', 'QUANTILE_STATE', 'SIGNED', 'SMALLINT', 'STRING', 'STRUCT', 'TEXT', 'TIME', 'TIMESTAMPTZ', 'TINYINT', 'UNSIGNED', 'VARBINARY', 'VARCHAR', 'VARIANT'}(line 1, pos 46)\n")
doris_error_code=1105
```

### pg-bit-0123-64e8d6bc — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('01010001', 'bit(10)');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('01010001', 'bit(10)')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.5 ms。
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

### pg-bit-0125-086339bb — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('01010Z01', 'bit(8)');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('01010Z01', 'bit(8)')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
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

### pg-bit-0127-81e3a323 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('x01010Z01', 'bit(32)');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('x01010Z01', 'bit(32)')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.1 ms。
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

### pg-bit-0129-b5856278 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('01010Z01', 'varbit');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('01010Z01', 'varbit')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 10.9 ms。
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

### pg-bit-0131-d7060d25 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('x01010Z01', 'varbit');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('x01010Z01', 'varbit')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.0 ms。
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
