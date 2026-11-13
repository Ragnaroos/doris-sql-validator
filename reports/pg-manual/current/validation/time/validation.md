# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:20.823836+00:00 至 2026-11-11T09:40:21.101231+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/time.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**15**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/15 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**0/8 = 0.00%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**7**；不计入上述成功匹配分子。
- 需要分析的查询：**15**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**3**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 6 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 2 |
| 返回记录值、重复次数或要求的顺序不同（`ROW_VALUE_MISMATCH`） | 7 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 15 条只读查询、跳过 29 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 1 | 1–5 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 2 | 7–7 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 3 | 8–8 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 9–10 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 11–11 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 12–12 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 13–13 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 14–14 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 15–15 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 18–18 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 12 | 19–20 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 13 | 23–23 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 14 | 25–25 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 15 | 27–27 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 16 | 29–29 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 17 | 31–31 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 19 | 35–35 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 20 | 35–36 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 21 | 36–37 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 26 | 41–44 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 27 | 45–45 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 28 | 46–46 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 29 | 47–47 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 30 | 48–48 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 31 | 50–59 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 42 | 77–77 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 43 | 78–78 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |
| 44 | 79–79 | 跳过非查询；类型 `out_of_scope_query` | 本次固定初始数据阶段/样本范围之外，不是 SQLGlot 失败 |

参考输出：`assets/time.out`；SHA-256（文件内容指纹）：`df3987ba69811f227876432b3fd209a4c1fcda311459c6c1a60330d2aad02e08`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 15/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 8/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 8/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 8/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/15 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-time-0018-df2485c4` | SELECT '23:59:59.999999'::time; | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0022-333b380a` | SELECT '24:00:00.01'::time; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0023-aab2582a` | SELECT '23:59:60.01'::time; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0024-3f651a00` | SELECT '24:01:00'::time; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0025-df167988` | SELECT '25:00:00'::time; | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0032-ce54a135` | SELECT EXTRACT(MICROSECOND FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0033-c230bada` | SELECT EXTRACT(MILLISECOND FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 失败：执行失败，需阅读具体错误 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0034-c3c729bb` | SELECT EXTRACT(SECOND      FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0035-71c4492f` | SELECT EXTRACT(MINUTE      FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0036-42ebd4b8` | SELECT EXTRACT(HOUR        FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0037-3411a8d0` | SELECT EXTRACT(DAY         FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 失败：执行失败，需阅读具体错误 | 成功 | 两端执行状态不同：一端成功、一端失败 |
| `pg-time-0038-cc79ba84` | SELECT EXTRACT(FORTNIGHT   FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-time-0039-98f3ca62` | SELECT EXTRACT(TIMEZONE    FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 失败：执行失败，需阅读具体错误 | 失败：执行失败，需阅读具体错误 | 两端同类报错，具体原因尚未确认；不计入成功结果匹配数 |
| `pg-time-0040-341de9e7` | SELECT EXTRACT(EPOCH       FROM TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |
| `pg-time-0041-ce54a135` | SELECT date_part('microsecond', TIME '2020-05-26 13:30:25.575401'); | 已生成 | 成功 | 成功 | 返回记录值、重复次数或要求的顺序不同 |

## 4. 不匹配、执行失败及负向错误详情

### pg-time-0018-df2485c4 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT '23:59:59.999999'::time;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('23:59:59.999999' AS TIME)
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：time: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "23:59:59.999999"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 19.3 ms。
- 返回行数：1；字段：CAST('23:59:59.999999' AS TIME): time / TIME。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$repr": "datetime.timedelta(days=1)"
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

### pg-time-0022-333b380a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '24:00:00.01'::time;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('24:00:00.01' AS TIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`date/time field value out of range: "24:00:00.01"`。

错误原文：

```text
date/time field value out of range: "24:00:00.01"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.7 ms。
- 返回行数：1；字段：CAST('24:00:00.01' AS TIME): time / TIME。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$repr": "datetime.timedelta(days=1)"
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
source_error_message=date/time field value out of range: "24:00:00.01"
source_error_code=date/time field value out of range: "24:00:00.01"
```

### pg-time-0023-aab2582a — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '23:59:60.01'::time;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('23:59:60.01' AS TIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`date/time field value out of range: "23:59:60.01"`。

错误原文：

```text
date/time field value out of range: "23:59:60.01"
```

#### Doris 实际结果

- 执行状态：成功；耗时 15.1 ms。
- 返回行数：1；字段：CAST('23:59:60.01' AS TIME): time / TIME。
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
source_error_message=date/time field value out of range: "23:59:60.01"
source_error_code=date/time field value out of range: "23:59:60.01"
```

### pg-time-0024-3f651a00 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '24:01:00'::time;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('24:01:00' AS TIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`date/time field value out of range: "24:01:00"`。

错误原文：

```text
date/time field value out of range: "24:01:00"
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：CAST('24:01:00' AS TIME): time / TIME。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$repr": "datetime.timedelta(days=1, seconds=60)"
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
source_error_message=date/time field value out of range: "24:01:00"
source_error_code=date/time field value out of range: "24:01:00"
```

### pg-time-0025-df167988 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT '25:00:00'::time;
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT CAST('25:00:00' AS TIME)
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`date/time field value out of range: "25:00:00"`。

错误原文：

```text
date/time field value out of range: "25:00:00"
```

#### Doris 实际结果

- 执行状态：成功；耗时 43.5 ms。
- 返回行数：1；字段：CAST('25:00:00' AS TIME): time / TIME。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    {
      "$repr": "datetime.timedelta(days=1, seconds=3600)"
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
source_error_message=date/time field value out of range: "25:00:00"
source_error_code=date/time field value out of range: "25:00:00"
```

### pg-time-0032-ce54a135 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT EXTRACT(MICROSECOND FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "25575401"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.2 ms。
- 返回行数：1；字段：EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / INT。
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

### pg-time-0033-c230bada — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT EXTRACT(MILLISECOND FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(MILLISECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "25575.401"
  ]
]
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 11.1 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLISECOND' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
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
doris_error_message=(1105, "errCode = 2, detailMessage = \nmismatched input 'MILLISECOND' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
doris_error_code=1105
```

### pg-time-0034-c3c729bb — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT EXTRACT(SECOND      FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(SECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "25.575401"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.3 ms。
- 返回行数：1；字段：EXTRACT(SECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / TINYINT。
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

### pg-time-0035-71c4492f — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT EXTRACT(MINUTE      FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(MINUTE FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "30"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.9 ms。
- 返回行数：1；字段：EXTRACT(MINUTE FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / TINYINT。
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

### pg-time-0036-42ebd4b8 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT EXTRACT(HOUR        FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(HOUR FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "13"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 12.6 ms。
- 返回行数：1；字段：EXTRACT(HOUR FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / INT。
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

### pg-time-0037-3411a8d0 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT EXTRACT(DAY         FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(DAY FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "day" not supported for type time without time zone`。

错误原文：

```text
unit "day" not supported for type time without time zone
```

#### Doris 实际结果

- 执行状态：成功；耗时 13.8 ms。
- 返回行数：1；字段：EXTRACT(DAY FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / TINYINT。
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
source_error_message=unit "day" not supported for type time without time zone
source_error_code=unit "day" not supported for type time without time zone
```

### pg-time-0038-cc79ba84 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT EXTRACT(FORTNIGHT   FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(FORTNIGHT FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "fortnight" not recognized for type time without time zone`。

错误原文：

```text
unit "fortnight" not recognized for type time without time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 10.7 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'FORTNIGHT' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-time-0039-98f3ca62 — 两端同类报错，具体原因尚未确认；不计入成功结果匹配数

#### 源 SQL

```sql
SELECT EXTRACT(TIMEZONE    FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(TIMEZONE FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 0.0 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`unit "timezone" not supported for type time without time zone`。

错误原文：

```text
unit "timezone" not supported for type time without time zone
```

#### Doris 实际结果

- 执行状态：失败：执行失败，需阅读具体错误；耗时 13.8 ms。
- 错误类别：执行失败，需阅读具体错误（`EXECUTION_ERROR`）；错误码：`1105`。

错误原文：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input 'TIMEZONE' expecting {'DAY', 'DAYOFWEEK', 'DAYOFYEAR', 'DAY_HOUR', 'DAY_MICROSECOND', 'DAY_MINUTE', 'DAY_SECOND', 'DOW', 'DOY', 'HOUR', 'HOUR_MICROSECOND', 'HOUR_MINUTE', 'HOUR_SECOND', 'MICROSECOND', 'MINUTE', 'MINUTE_MICROSECOND', 'MINUTE_SECOND', 'MONTH', 'QUARTER', 'SECOND', 'SECOND_MICROSECOND', 'WEEK', 'YEAR', 'YEAR_MONTH'}(line 1, pos 15)\n")
```

#### 后续应如何判断

- 这是源端报错的负向用例：核对实际错误原因，不能因两端同类报错就认定同义，也不能把目标返回成功当改写成功。

自动比较器诊断原文（可能含英文程序字段，不是最终根因）：

```text
Both sides failed with compatible recorded/live error behavior
```

### pg-time-0040-341de9e7 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT EXTRACT(EPOCH       FROM TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT UNIX_TIMESTAMP(CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：extract: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "48625.575401"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 16.8 ms。
- 返回行数：1；字段：UNIX_TIMESTAMP(CAST('2020-05-26 13:30:25.575401' AS TIME)): decimal / DECIMAL。
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

### pg-time-0041-ce54a135 — 返回记录值、重复次数或要求的顺序不同

#### 源 SQL

```sql
SELECT date_part('microsecond', TIME '2020-05-26 13:30:25.575401');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME))
```

#### 源端参考结果

- 执行状态：成功；耗时 0.0 ms。
- 返回行数：1；字段：date_part: unknown / 原生类型未知。
- 结果样本（最多前五行，完整结果并未保存在此样本中）：

```json
[
  [
    "25575401"
  ]
]
```

#### Doris 实际结果

- 执行状态：成功；耗时 14.2 ms。
- 返回行数：1；字段：EXTRACT(MICROSECOND FROM CAST('2020-05-26 13:30:25.575401' AS TIME)): integer / INT。
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
