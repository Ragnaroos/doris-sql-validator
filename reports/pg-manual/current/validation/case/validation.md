# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:07.180742+00:00 至 2026-11-11T09:40:07.309037+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/case.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**8**；两端成功且已有证据匹配：**6**。
- 成功结果匹配占全部查询比例：**6/8 = 75.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**6/8 = 75.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**2**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**0**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 6 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 2 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 8 条只读查询、跳过 50 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–9 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 11–14 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 16–16 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 18–18 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 19–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 21–21 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 22–22 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 23–23 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 25–25 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 33 | 140–143 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 34 | 145–146 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 35 | 148–149 | 跳过非查询；类型 `explain` | Expected one read-only Query, got Command |
| 36 | 151–157 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 38 | 161–163 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 40 | 167–171 | 跳过非查询；类型 `update` | Expected one read-only Query, got Update |
| 43 | 190–191 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 45 | 203–204 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 46 | 206–207 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 47 | 209–210 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 48 | 212–213 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 52 | 224–224 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 53 | 226–231 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 54 | 233–234 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 55 | 236–237 | 跳过非查询；类型 `create` | Expected one read-only Query, got Command |
| 60 | 255–255 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 63 | 265–269 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 64 | 270–270 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 18 | 62–64 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 70–72 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 23 | 77–85 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 24 | 87–91 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 25 | 93–100 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 26 | 102–109 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 27 | 111–121 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 28 | 123–123 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 29 | 125–126 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 30 | 128–130 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 31 | 132–134 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 32 | 136–138 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 37 | 159–159 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 39 | 165–165 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 41 | 173–173 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 44 | 193–201 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 49 | 215–215 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 56 | 239–243 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 57 | 245–248 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 61 | 257–261 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/case.out`；SHA-256（文件内容指纹）：`0140fcf76eb375bee96bb6ab9419e47701f01627f59230504c6eef23e4463d22`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 8/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 8/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 8/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 8/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 8/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/8 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-case-0013-00d1dea8` | SELECT '3' AS "One",   CASE     WHEN 1 < 2 THEN 3   END AS "Simple WHEN"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-case-0014-068371ac` | SELECT '<NULL>' AS "One",   CASE     WHEN 1 > 2 THEN 3   END AS "Simple default"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-case-0015-06669704` | SELECT '3' AS "One",   CASE     WHEN 1 < 2 THEN 3     ELSE 4   END AS "Simple ELSE"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-case-0016-2c1e1463` | SELECT '4' AS "One",   CASE     WHEN 1 > 2 THEN 3     ELSE 4   END AS "ELSE default"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-case-0017-47ffe574` | SELECT '6' AS "One",   CASE     WHEN 1 > 2 THEN 3     WHEN 4 < 5 THEN 6     ELSE 7   END AS "Two WHEN with default"; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-case-0019-fe72fa57` | SELECT CASE WHEN 1=0 THEN 1/0 WHEN 1=1 THEN 1 ELSE 2/0 END; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-case-0020-eef1e7fd` | SELECT CASE 1 WHEN 0 THEN 1/0 WHEN 1 THEN 1 ELSE 2/0 END; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-case-0022-83be6299` | SELECT CASE 'a' WHEN 'a' THEN 1 ELSE 2 END; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |

## 4. 不匹配、执行失败及负向错误详情

### pg-case-0019-fe72fa57 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT CASE WHEN 1=0 THEN 1/0 WHEN 1=1 THEN 1 ELSE 2/0 END;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CASE WHEN 1 = 0 THEN 1 / 0 WHEN 1 = 1 THEN 1 ELSE 2 / 0 END
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：case: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.7 ms。
- 返回行数：1；字段：CASE WHEN 1 = 0 THEN 1 / 0 WHEN 1 = 1 THEN 1 ELSE 2 / 0 END: float / DOUBLE。
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

### pg-case-0020-eef1e7fd — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT CASE 1 WHEN 0 THEN 1/0 WHEN 1 THEN 1 ELSE 2/0 END;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CASE 1 WHEN 0 THEN 1 / 0 WHEN 1 THEN 1 ELSE 2 / 0 END
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：case: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "1"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 11.0 ms。
- 返回行数：1；字段：CASE 1 WHEN 0 THEN 1 / 0 WHEN 1 THEN 1 ELSE 2 / 0 END: float / DOUBLE。
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
