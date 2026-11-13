# postgres → Doris 确定性验证报告

- 执行时间：2026-11-13T04:02:55.484734+00:00 至 2026-11-13T04:02:55.489194+00:00
- SQLGlot 版本：`30.25.1.dev6`；提交：`feb0e08aba28a29590596bb3f5761fbaeb0e98b9`。
- 原始输入：`assets/select_distinct_on.sql`；格式：`pg-regress`。
- 源结果来源：读取 .out 历史输出；不连接源数据库，转译成功后才读取对应结果并执行 Doris。

## 1. 总体结果

- 本轮查询总数：**3**；两端成功且已有证据匹配：**0**。
- 成功结果匹配占全部查询比例：**0/3 = 0.00%**。这是结果匹配比例，不是全部语义或类型验证通过率。
- 已取得成功源结果的查询匹配率：**无可计算分母**。源结果未取得、转换先失败及负向用例不在这个分母中，需同时看失败数。
- 源端报错的负向用例：**0**；不计入上述成功匹配分子。
- 需要分析的查询：**3**；包括报错原因待确认的负向用例。
- SQLGlot 转译失败：**3**；源参考结果不可用：**0**；Doris 执行失败：**0**。

本报告只记录实际运行和自动比较结果，不调用大模型、不自动改写 SQL、不判定修复责任。匹配不证明所有输入同义；类型或参考输出信息缺失不算相应维度通过。

### 差异分类统计

| 自动结果及含义 | 查询数 |
| :--- | ---: |
| SQLGlot 解析或生成失败（`TRANSLATION_FAILED`） | 3 |

这些是互斥的自动结果分类；上面的执行失败等指标可能重叠，不能相加当总数。两端粗粒度报错相同仍可能保留旧内部 MATCH 代码，但已从成功匹配数排除。

## 2. 输入处理与证据限制

导入时保留 3 条待验证查询、跳过 0 条非查询、0 条待确认、0 条解析或输出配对诊断。保留的查询可包含 Parser 尚不支持的语法；解析失败由普通运行记录为转译失败，不会执行数据库查询。诊断数与保留数可能重叠。导入摘要是整个 YAML 的信息，按 --id 筛选运行不改变它。

验证器不执行建表、装数和数据一致性检查，默认这些已由外部数据准备流程完成。表查询标记为 unverified 只表示验证器自身没有核验；外部准备证据应随人工交接材料提供，不会成为运行拦截条件。

DDL、INSERT、COPY 等输入被跳过，不是转换失败。导入阶段的 SELECT 解析失败或 .out 配对失败也必须进入人工分析，不能仅查看已运行查询的不匹配。

参考输出：`assets/select_distinct_on.out`；SHA-256（文件内容指纹）：`b5254efae56908b5537674959ce2eb3dfe29a6207ce7557d5660cbbe9a023421`。指纹仅用于防止索引指向被修改的文件，不证明预期输出正确。

### 能比较什么

| 比较内容 | 本轮证据情况 |
| :--- | :--- |
| 执行成功或失败 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 错误类别 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段数量 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回字段名称 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 字段类型 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 返回记录数 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |
| 复杂类型 | 0/0 条源结果声明可提供此证据；仅表示可检查，不表示比较已通过 |

.out 通常只有显示文本，没有原生字段类型；NULL 与空字符串、数值显示、JSON/数组显示可能存在歧义。实时驱动类型映射也不完整。当前通用比较器遇到字段或行数差异会提前返回，后续维度并未执行；完整类型、逐查询边界和根因判断留给人工调用的归因流程。

比较规则：最终有 ORDER BY 时逐行比较；否则忽略行顺序但保留每种行的重复次数。名称仅在当前代码识别出全部输出均为显式别名时检查；实时浮点比较默认使用 1e-12 相对/绝对容差，.out 文本比较不自动套用数值容差。

## 3. 全部查询结果

成功匹配的查询在下表简写；其他查询在下一节展开。

| 查询编号 | 源 SQL | SQLGlot 转译 | 源参考结果 | Doris 执行 | 本次结论 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `pg-select-distinct-on-0001` | SELECT DISTINCT ON (string4) string4, two, ten    FROM onek    ORDER BY string4 using <, two using >, ten using <; | 失败 | 未执行（SQLGlot 解析或生成先失败） | 未执行（SQLGlot 解析或生成先失败） | SQLGlot 解析或生成失败 |
| `pg-select-distinct-on-0002` | SELECT DISTINCT ON (string4, ten) string4, two, ten    FROM onek    ORDER BY string4 using <, two using <, ten using <; | 失败 | 未执行（SQLGlot 解析或生成先失败） | 未执行（SQLGlot 解析或生成先失败） | SQLGlot 解析或生成失败 |
| `pg-select-distinct-on-0003` | SELECT DISTINCT ON (string4, ten) string4, ten, two    FROM onek    ORDER BY string4 using <, ten using >, two using <; | 失败 | 未执行（SQLGlot 解析或生成先失败） | 未执行（SQLGlot 解析或生成先失败） | SQLGlot 解析或生成失败 |

## 4. 不匹配、执行失败及负向错误详情

### pg-select-distinct-on-0001 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
```

失败阶段：**源 SQL 解析（SQLGlot Parser）**。源参考结果获取、Doris 执行和结果比较均未执行，不计为 Doris 执行错误。

#### SQLGlot 转译错误原文

```text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using >, ten using <;
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-select-distinct-on-0002 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT DISTINCT ON (string4, ten) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using <, ten using <;
```

失败阶段：**源 SQL 解析（SQLGlot Parser）**。源参考结果获取、Doris 执行和结果比较均未执行，不计为 Doris 执行错误。

#### SQLGlot 转译错误原文

```text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4, ten) string4, two, ten
   FROM onek
   ORDER BY string4 using <, two using <, ten using <;
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。

### pg-select-distinct-on-0003 — SQLGlot 解析或生成失败

#### 源 SQL

```sql
SELECT DISTINCT ON (string4, ten) string4, ten, two
   FROM onek
   ORDER BY string4 using <, ten using >, two using <;
```

失败阶段：**源 SQL 解析（SQLGlot Parser）**。源参考结果获取、Doris 执行和结果比较均未执行，不计为 Doris 执行错误。

#### SQLGlot 转译错误原文

```text
ParseError: Invalid expression / Unexpected token. Line 3, Col: 25.
  SELECT DISTINCT ON (string4, ten) string4, ten, two
   FROM onek
   ORDER BY string4 using <, ten using >, two using <;
```

#### 后续应如何判断

- 对照合法 PostgreSQL 源语法检查 SQLGlot Parser/Generator 和当前版本；独立 Doris 写法需实际执行，不能仅凭候选文本宣称可修复。
