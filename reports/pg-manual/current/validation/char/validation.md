# postgres → Doris 确定性验证报告

- 执行时间：2026-11-11T09:40:38.159085+00:00 至 2026-11-11T09:40:38.215145+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/char.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；本轮不连接源数据库，只执行 Doris。

## 1. 总体结果

- 本轮查询总数：**3**；两端成功且已有证据匹配：**1**。
- 成功结果匹配占全部查询比例：**1/3 = 33.33%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**1/3 = 33.33%**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**2**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**0**；源参考结果不可用：**0**；Doris 执行失败：**2**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| 两端执行状态不同：一端成功、一端失败（`EXECUTION_STATUS_MISMATCH`） | 2 |
| 已有证据未发现差异（不代表所有类型和输入均已验证）（`MATCH`） | 1 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时接受 3 条只读查询、跳过 29 条非查询、0 条待确认、0 条解析或输出配对失败。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

| 语句编号 | 源文件行号 | 处理结果 | 原因（保留原始诊断） |
| ---: | :--- | :--- | :--- |
| 2 | 10–15 | 跳过非查询；类型 `create` | Expected one read-only Query, got Create |
| 3 | 17–17 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 4 | 19–19 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 5 | 21–22 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 6 | 24–24 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 7 | 26–26 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 8 | 28–29 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 9 | 31–32 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 10 | 33–33 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 18 | 62–62 | 跳过非查询；类型 `drop` | Expected one read-only Query, got Drop |
| 19 | 64–71 | 跳过非查询；类型 `insert` | Expected one read-only Query, got Insert |
| 11 | 36–36 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 12 | 38–40 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 13 | 42–44 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 14 | 46–48 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 15 | 50–52 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 16 | 54–56 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 17 | 58–60 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 20 | 73–73 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 23 | 78–78 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖表、视图或表值函数；本次未为新脚本准备相应对象与数据阶段 |
| 24 | 80–86 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 25 | 87–87 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 26 | 88–88 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 27 | 89–89 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 28 | 90–90 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 29 | 91–91 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 30 | 92–92 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 31 | 93–93 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |
| 32 | 94–94 | 跳过非查询；类型 `deferred_environment_dependency` | 依赖用户定义的类型、Domain、枚举或复合类型；本次未准备这些对象 |

参考输出：`assets/char.out`；SHA-256（文件内容指纹）：`0ffccfb2ac223e03b41de6cf26ddee25e90c8ffb08b97976c76c0ead099e356f`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 3/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 3/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 3/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 3/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 3/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/3 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-char-0001-07961456` | SELECT char 'c' = char 'c' AS true; | 已生成 | 成功 | 成功 | 已有证据未发现差异（不代表所有类型和输入均已验证） |
| `pg-char-0021-73e37fb1` | SELECT pg_input_is_valid('abcd  ', 'char(4)'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |
| `pg-char-0022-56bce410` | SELECT pg_input_is_valid('abcde', 'char(4)'); | 已生成 | 成功 | 失败：函数不存在或调用形式不受支持 | 两端执行状态不同：一端成功、一端失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-char-0021-73e37fb1 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('abcd  ', 'char(4)');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('abcd  ', 'char(4)')
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

### pg-char-0022-56bce410 — 两端执行状态不同：一端成功、一端失败

#### 源 SQL

```sql
SELECT pg_input_is_valid('abcde', 'char(4)');
```

#### 社区 SQLGlot 生成的 Doris SQL

```sql
SELECT PG_INPUT_IS_VALID('abcde', 'char(4)')
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

- 执行状态：失败：函数不存在或调用形式不受支持；耗时 13.1 ms。
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
