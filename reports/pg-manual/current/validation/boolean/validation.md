# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:37.194820+00:00 至 2026-11-11T09:40:37.910149+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/boolean.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**45**；两端成功且已有证据匹配：**27**。
- 成功结果匹配占全部查询比例：**27/45 = 60.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**27/33 = 81.82%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**12**；不计入上述成功匹配分子。
- 需要分析的查询：**18**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**2**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 14 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 27 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 4 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 45 条只读查询、跳过 53 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 44 | 97–99 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 45 | 101–101 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 46 | 103–103 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 47 | 105–105 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 52 | 125–125 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 54 | 132–132 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 55 | 134–134 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 56 | 136–136 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 57 | 138–138 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 58 | 140–140 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 59 | 142–145 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 73 | 209–212 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 74 | 213–213 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 75 | 214–214 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 76 | 215–215 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 78 | 228–231 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 79 | 232–232 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 95 | 259–266 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 96 | 268–268 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 97 | 270–270 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 98 | 272–272 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 29 | 68–68 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 48 | 108–109 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 49 | 112–114 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 50 | 117–119 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 51 | 121–123 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 53 | 127–129 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 60 | 147–148 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 61 | 151–153 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 62 | 156–158 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 63 | 161–163 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 64 | 166–169 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 65 | 171–179 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 66 | 181–183 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 67 | 185–187 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 68 | 189–191 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 69 | 193–195 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 70 | 197–199 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 71 | 201–203 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 72 | 205–207 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 77 | 217–225 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 80 | 233–237 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 81 | 238–238 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 82 | 239–239 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 83 | 240–240 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 84 | 241–241 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 85 | 242–242 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 86 | 244–246 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 87 | 247–247 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 88 | 248–248 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 89 | 249–249 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 90 | 250–250 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 91 | 251–251 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |

参考输出：`assets/boolean.out`；SHA-256（文件内容指纹）：`d26265fe1695de91e102b575dd88806078568f2c42b39fc9bd2defb472250307`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 45/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 45/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 33/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 33/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 33/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/45 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-boolean-0001-70d501bd` | SELECT 1 AS one; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0002-cd7e4191` | SELECT true AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0003-c5856e9a` | SELECT false AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0004-3bf7e474` | SELECT bool 't' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0005-97c5885a` | SELECT bool '   f           ' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0006-2b4f6271` | SELECT bool 'true' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0007-e1b1ef89` | SELECT bool 'test' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0008-7393cacc` | SELECT bool 'false' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0009-38386ada` | SELECT bool 'foo' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0010-222849e6` | SELECT bool 'y' AS true; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-boolean-0011-8724fe67` | SELECT bool 'yes' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0012-81dee7f4` | SELECT bool 'yeah' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0013-41441aee` | SELECT bool 'n' AS false; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-boolean-0014-820ec7d1` | SELECT bool 'no' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0015-9a4316f3` | SELECT bool 'nay' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0016-a26417ca` | SELECT bool 'on' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0017-bb8e4812` | SELECT bool 'off' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0018-0e6e96f9` | SELECT bool 'of' AS false; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-boolean-0019-75c89fd3` | SELECT bool 'o' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0020-c50756c3` | SELECT bool 'on_' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0021-7dfc6ac1` | SELECT bool 'off_' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0022-e5ab58c0` | SELECT bool '1' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0023-f8e04b2d` | SELECT bool '11' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0024-107f4ce0` | SELECT bool '0' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0025-2c6fc490` | SELECT bool '000' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0026-2c8a99f3` | SELECT bool '' AS error; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0027-1e7243be` | SELECT pg_input_is_valid('true', 'bool'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0028-50f4807b` | SELECT pg_input_is_valid('asdf', 'bool'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0030-926c4ad4` | SELECT bool 't' or bool 'f' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0031-8355bac8` | SELECT bool 't' and bool 'f' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0032-9502db2a` | SELECT not bool 'f' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0033-f3dc7c01` | SELECT bool 't' = bool 'f' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0034-beb69ffd` | SELECT bool 't' <> bool 'f' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0035-88080971` | SELECT bool 't' > bool 'f' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0036-126950bd` | SELECT bool 't' >= bool 'f' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0037-1424908a` | SELECT bool 'f' < bool 't' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0038-de0b0e95` | SELECT bool 'f' <= bool 't' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0039-06126331` | SELECT 'TrUe'::text::boolean AS true, 'fAlse'::text::boolean AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0040-5c5709be` | SELECT '    true   '::text::boolean AS true,        '     FALSE'::text::boolean AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0041-8fceef7a` | SELECT true::boolean::text AS true, false::boolean::text AS false; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-boolean-0042-5862abf0` | SELECT '  tru e '::text::boolean AS invalid; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0043-f35e4f2d` | SELECT ''::text::boolean AS invalid; | 已生成 | 失败：语法解析失败 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-boolean-0092-bf6ced1a` | SELECT 0::boolean; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0093-b8e9145c` | SELECT 1::boolean; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-boolean-0094-35e4dc2f` | SELECT 2::boolean; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |

## 4. 不匹配、执行失败及负向错误详情

### pg-boolean-0007-e1b1ef89 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'test' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('test' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "test"`。

错误原文：

```text
invalid input syntax for type boolean: "test"
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.4 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "test"
source_error_code=invalid input syntax for type boolean: "test"
```

### pg-boolean-0009-38386ada — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'foo' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('foo' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "foo"`。

错误原文：

```text
invalid input syntax for type boolean: "foo"
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.5 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "foo"
source_error_code=invalid input syntax for type boolean: "foo"
```

### pg-boolean-0010-222849e6 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT bool 'y' AS true;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('y' AS BOOLEAN) AS `true`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：true: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "t"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.5 ms。
- 返回行数：1；字段：true: boolean / BOOLEAN。
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

### pg-boolean-0012-81dee7f4 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'yeah' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('yeah' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "yeah"`。

错误原文：

```text
invalid input syntax for type boolean: "yeah"
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.1 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "yeah"
source_error_code=invalid input syntax for type boolean: "yeah"
```

### pg-boolean-0013-41441aee — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT bool 'n' AS false;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('n' AS BOOLEAN) AS `false`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：false: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：false: boolean / BOOLEAN。
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

### pg-boolean-0015-9a4316f3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'nay' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('nay' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "nay"`。

错误原文：

```text
invalid input syntax for type boolean: "nay"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "nay"
source_error_code=invalid input syntax for type boolean: "nay"
```

### pg-boolean-0018-0e6e96f9 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT bool 'of' AS false;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('of' AS BOOLEAN) AS `false`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：false: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "f"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.3 ms。
- 返回行数：1；字段：false: boolean / BOOLEAN。
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

### pg-boolean-0019-75c89fd3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'o' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('o' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "o"`。

错误原文：

```text
invalid input syntax for type boolean: "o"
```

#### Doris 实际结果

- 执行状态：成功；耗时 10.9 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "o"
source_error_code=invalid input syntax for type boolean: "o"
```

### pg-boolean-0020-c50756c3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'on_' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('on_' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "on_"`。

错误原文：

```text
invalid input syntax for type boolean: "on_"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "on_"
source_error_code=invalid input syntax for type boolean: "on_"
```

### pg-boolean-0021-7dfc6ac1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool 'off_' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('off_' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "off_"`。

错误原文：

```text
invalid input syntax for type boolean: "off_"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "off_"
source_error_code=invalid input syntax for type boolean: "off_"
```

### pg-boolean-0023-f8e04b2d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool '11' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('11' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "11"`。

错误原文：

```text
invalid input syntax for type boolean: "11"
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.4 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "11"
source_error_code=invalid input syntax for type boolean: "11"
```

### pg-boolean-0025-2c6fc490 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool '000' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('000' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "000"`。

错误原文：

```text
invalid input syntax for type boolean: "000"
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.6 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "000"
source_error_code=invalid input syntax for type boolean: "000"
```

### pg-boolean-0026-2c8a99f3 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT bool '' AS error;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('' AS BOOLEAN) AS error
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: ""`。

错误原文：

```text
invalid input syntax for type boolean: ""
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.6 ms。
- 返回行数：1；字段：error: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: ""
source_error_code=invalid input syntax for type boolean: ""
```

### pg-boolean-0027-1e7243be — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('true', 'bool');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('true', 'bool')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 12.3 ms。
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

### pg-boolean-0028-50f4807b — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('asdf', 'bool');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('asdf', 'bool')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 11.6 ms。
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

### pg-boolean-0041-8fceef7a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT true::boolean::text AS true, false::boolean::text AS false;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST(TRUE AS BOOLEAN) AS STRING) AS `true`, CAST(CAST(FALSE AS BOOLEAN) AS STRING) AS `false`
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：true: unknown / 原生类型未知, false: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "true",
    "false"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.5 ms。
- 返回行数：1；字段：true: string / STRING, false: string / STRING。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1",
    "0"
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

### pg-boolean-0042-5862abf0 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '  tru e '::text::boolean AS invalid;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('  tru e ' AS STRING) AS BOOLEAN) AS invalid
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: "  tru e "`。

错误原文：

```text
invalid input syntax for type boolean: "  tru e "
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.8 ms。
- 返回行数：1；字段：invalid: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: "  tru e "
source_error_code=invalid input syntax for type boolean: "  tru e "
```

### pg-boolean-0043-f35e4f2d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT ''::text::boolean AS invalid;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST(CAST('' AS STRING) AS BOOLEAN) AS invalid
```

#### 源端参考结果

- 执行状态：失败：语法解析失败；耗时 0.0 ms。
- 错误类别：语法解析失败（`PARSE_ERROR`）；错误码：`invalid input syntax for type boolean: ""`。

错误原文：

```text
invalid input syntax for type boolean: ""
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.6 ms。
- 返回行数：1；字段：invalid: boolean / BOOLEAN。
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
source_error_message=invalid input syntax for type boolean: ""
source_error_code=invalid input syntax for type boolean: ""
```
