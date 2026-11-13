# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:09.411151+00:00 至 2026-11-11T09:40:10.223592+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/int4.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**40**；两端成功且已有证据匹配：**30**。
- 成功结果匹配占全部查询比例：**30/40 = 75.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**30/34 = 88.24%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**6**；不计入上述成功匹配分子。
- 需要分析的查询：**10**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**0**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 6 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 30 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 4 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 40 条只读查询、跳过 61 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–8 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 2 | 9–9 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 10–10 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 11–11 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 12–12 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 13–13 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 14–14 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 20–21 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 11 | 22–22 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 12 | 23–23 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 13 | 24–24 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 53 | 117–118 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 54 | 119–119 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 55 | 121–122 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 56 | 123–123 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 57 | 124–124 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 58 | 125–125 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 59 | 126–126 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 60 | 127–127 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 61 | 129–130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 62 | 130–131 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 63 | 131–132 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 64 | 133–133 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 65 | 134–134 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 66 | 134–135 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 67 | 136–136 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 68 | 136–146 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 69 | 148–156 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 70 | 158–166 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 71 | 168–168 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 72 | 168–169 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 73 | 169–178 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 74 | 180–180 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 75 | 180–181 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 76 | 181–186 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 77 | 187–187 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 78 | 188–188 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 79 | 190–190 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 80 | 191–191 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 81 | 192–192 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 82 | 194–195 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 83 | 196–196 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 84 | 197–197 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 85 | 198–198 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 86 | 199–199 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 87 | 200–200 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 88 | 202–202 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 89 | 203–203 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 90 | 204–204 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 91 | 205–205 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 92 | 206–206 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 93 | 207–207 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 94 | 210–212 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 95 | 213–213 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 96 | 214–214 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 97 | 215–215 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 98 | 216–216 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 99 | 218–219 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 100 | 220–220 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 101 | 221–221 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/int4.out`；SHA-256（文件内容指纹）：`274c048e39f94094b53d371170d7a3eecd8750ea303dbc36a5eba347ebe48b2a`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 40/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 40/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 34/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 34/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 34/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/40 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-int4-0009-078b9c31` | SELECT * FROM INT4_TBL; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0014-c8657bed` | SELECT i.* FROM INT4_TBL i WHERE i.f1 <> int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0015-82a1513e` | SELECT i.* FROM INT4_TBL i WHERE i.f1 <> int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0016-31c9f66b` | SELECT i.* FROM INT4_TBL i WHERE i.f1 = int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0017-074bc95e` | SELECT i.* FROM INT4_TBL i WHERE i.f1 = int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0018-e2dc2ba8` | SELECT i.* FROM INT4_TBL i WHERE i.f1 < int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0019-e5704751` | SELECT i.* FROM INT4_TBL i WHERE i.f1 < int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0020-11086ee7` | SELECT i.* FROM INT4_TBL i WHERE i.f1 <= int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0021-21a0f97d` | SELECT i.* FROM INT4_TBL i WHERE i.f1 <= int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0022-a6f61707` | SELECT i.* FROM INT4_TBL i WHERE i.f1 > int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0023-80e75b67` | SELECT i.* FROM INT4_TBL i WHERE i.f1 > int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0024-d9210ff8` | SELECT i.* FROM INT4_TBL i WHERE i.f1 >= int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0025-62c22a17` | SELECT i.* FROM INT4_TBL i WHERE i.f1 >= int4 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0026-92feef12` | SELECT i.* FROM INT4_TBL i WHERE (i.f1 % int2 '2') = int2 '1'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0027-085daa53` | SELECT i.* FROM INT4_TBL i WHERE (i.f1 % int4 '2') = int2 '0'; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0028-eefe8f02` | SELECT i.f1, i.f1 * int2 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0029-4c7c4839` | SELECT i.f1, i.f1 * int2 '2' AS x FROM INT4_TBL i WHERE abs(f1) < 1073741824; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0030-6b7df65d` | SELECT i.f1, i.f1 * int4 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0031-67c41555` | SELECT i.f1, i.f1 * int4 '2' AS x FROM INT4_TBL i WHERE abs(f1) < 1073741824; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0032-3a22f62e` | SELECT i.f1, i.f1 + int2 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0033-5c001408` | SELECT i.f1, i.f1 + int2 '2' AS x FROM INT4_TBL i WHERE f1 < 2147483646; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0034-6b91aedb` | SELECT i.f1, i.f1 + int4 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0035-d0213214` | SELECT i.f1, i.f1 + int4 '2' AS x FROM INT4_TBL i WHERE f1 < 2147483646; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0036-e81aa3e1` | SELECT i.f1, i.f1 - int2 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0037-487a22b0` | SELECT i.f1, i.f1 - int2 '2' AS x FROM INT4_TBL i WHERE f1 > -2147483647; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0038-a51d16a9` | SELECT i.f1, i.f1 - int4 '2' AS x FROM INT4_TBL i; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-int4-0039-b96c072f` | SELECT i.f1, i.f1 - int4 '2' AS x FROM INT4_TBL i WHERE f1 > -2147483647; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0040-453402df` | SELECT i.f1, i.f1 / int2 '2' AS x FROM INT4_TBL i; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-int4-0041-7027be1a` | SELECT i.f1, i.f1 / int4 '2' AS x FROM INT4_TBL i; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-int4-0042-39e2d6da` | SELECT -2+3 AS one; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0043-d3556909` | SELECT 4-2 AS two; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0044-f3e02ee8` | SELECT 2- -1 AS three; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0045-59e42e3a` | SELECT 2 - -2 AS four; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0046-f781f855` | SELECT int2 '2' * int2 '2' = int2 '16' / int2 '4' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0047-2218e186` | SELECT int4 '2' * int2 '2' = int2 '16' / int4 '4' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0048-1f470dee` | SELECT int2 '2' * int4 '2' = int4 '16' / int2 '4' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0049-6c0d3f66` | SELECT int4 '1000' < int4 '999' AS false; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0050-ea0ab753` | SELECT 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 AS ten; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-int4-0051-b8fd3a8e` | SELECT 2 + 2 / 2 AS three; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-int4-0052-78fd8444` | SELECT (2 + 2) / 2 AS two; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-int4-0028-eefe8f02 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 * int2 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 * CAST('2' AS SMALLINT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 21.3 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -4294967294
  ],
  [
    -123456,
    -246912
  ],
  [
    0,
    0
  ],
  [
    123456,
    246912
  ],
  [
    2147483647,
    4294967294
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

### pg-int4-0030-6b7df65d — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 * int4 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 * CAST('2' AS INT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.8 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -4294967294
  ],
  [
    -123456,
    -246912
  ],
  [
    0,
    0
  ],
  [
    123456,
    246912
  ],
  [
    2147483647,
    4294967294
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

### pg-int4-0032-3a22f62e — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 + int2 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 + CAST('2' AS SMALLINT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 23.3 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -2147483645
  ],
  [
    -123456,
    -123454
  ],
  [
    0,
    2
  ],
  [
    123456,
    123458
  ],
  [
    2147483647,
    2147483649
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

### pg-int4-0034-6b91aedb — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 + int4 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 + CAST('2' AS INT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 17.1 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -2147483645
  ],
  [
    -123456,
    -123454
  ],
  [
    0,
    2
  ],
  [
    123456,
    123458
  ],
  [
    2147483647,
    2147483649
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

### pg-int4-0036-e81aa3e1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 - int2 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 - CAST('2' AS SMALLINT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.8 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -2147483649
  ],
  [
    -123456,
    -123458
  ],
  [
    0,
    -2
  ],
  [
    123456,
    123454
  ],
  [
    2147483647,
    2147483645
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

### pg-int4-0038-a51d16a9 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT i.f1, i.f1 - int4 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 - CAST('2' AS INT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`integer out of range`。

错误原文：

```text
integer out of range
```

#### Doris 实际结果

- 执行状态：成功；耗时 17.1 ms。
- 返回行数：5；字段：f1: integer / INT, x: integer / BIGINT。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -2147483649
  ],
  [
    -123456,
    -123458
  ],
  [
    0,
    -2
  ],
  [
    123456,
    123454
  ],
  [
    2147483647,
    2147483645
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

### pg-int4-0040-453402df — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT i.f1, i.f1 / int2 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 / CAST('2' AS SMALLINT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：f1: unknown / 原生类型未知, x: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0"
  ],
  [
    "123456",
    "61728"
  ],
  [
    "-123456",
    "-61728"
  ],
  [
    "2147483647",
    "1073741823"
  ],
  [
    "-2147483647",
    "-1073741823"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 25.5 ms。
- 返回行数：5；字段：f1: integer / INT, x: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -1073741823.5
  ],
  [
    -123456,
    -61728.0
  ],
  [
    0,
    0.0
  ],
  [
    123456,
    61728.0
  ],
  [
    2147483647,
    1073741823.5
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

### pg-int4-0041-7027be1a — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT i.f1, i.f1 / int4 '2' AS x FROM INT4_TBL i;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT i.f1, i.f1 / CAST('2' AS INT) AS x FROM INT4_TBL AS i
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：5；字段：f1: unknown / 原生类型未知, x: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "0",
    "0"
  ],
  [
    "123456",
    "61728"
  ],
  [
    "-123456",
    "-61728"
  ],
  [
    "2147483647",
    "1073741823"
  ],
  [
    "-2147483647",
    "-1073741823"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 18.6 ms。
- 返回行数：5；字段：f1: integer / INT, x: float / DOUBLE。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    -2147483647,
    -1073741823.5
  ],
  [
    -123456,
    -61728.0
  ],
  [
    0,
    0.0
  ],
  [
    123456,
    61728.0
  ],
  [
    2147483647,
    1073741823.5
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

### pg-int4-0051-b8fd3a8e — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT 2 + 2 / 2 AS three;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT 2 + 2 / 2 AS three
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

- 执行状态：成功；耗时 10.9 ms。
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

### pg-int4-0052-78fd8444 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT (2 + 2) / 2 AS two;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT (2 + 2) / 2 AS two
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：two: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "2"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.1 ms。
- 返回行数：1；字段：two: float / DOUBLE。
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
