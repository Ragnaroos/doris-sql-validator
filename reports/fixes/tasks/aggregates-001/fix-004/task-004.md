# task-004：ARRAY_AGG 按聚合值自身排序

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`4052036e400c7ce0fe24ef6132fb5b17bf930a50`。依赖task-003的NULL/空输入基础提交d0fcf8f16af727bcfac9993792fa2c9a1be2b766；保存约定自值排序规则及测试，类型余项不因保存commit而关闭。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与范围

**已修复并完成约定验收：单键与聚合值同一表达式的整数排序，含 ASC/DESC、NULLS FIRST/LAST、DISTINCT、重复元素、全 NULL 和空输入。** 这不是 5 条原 Case 已完整 MATCH；原查询还有真实元素位宽差异和 .out 文本表示差异。

本轮 fix-004，仅选 [task-004](../../../../attribution/aggregates-001-attribution-summary.md#task-004)，沿用 task-003 已实现的 NULL/空输入契约。共同身份、权限、测试和整体余项见[汇总](../../../aggregates-001-fix-004-summary.md)。没有 commit/push、社区 Issue/PR、数据写入或框架修改。task-003 尚未完成的类型/精度验收不被本报告关闭。

排除不同排序键、多键、Collation、易变表达式、复合类型、窗口和 FILTER。实现保守地不转换含普通函数调用、子查询或 Collate 的聚合值（CAST 除外）；不假装能识别所有 UDF 的稳定性。无 Schema 的列类型未知，不声明任意字符串排序规则、复合值或所有数据库版本均兼容。

关联原 Case：0284、0285、0288、0289、0290，完整编号及原文见第 4 节；全部是 stage-17、双端 `dsv_wf_agg001_s17`。原位置、.out 出现序号见各 Case 第 2 节，未重新编号或改写输入。

## 2. 修改依据与实现

本轮修改前已实际重跑这 5 条源 SQL。PG 全部成功；当时已有 task-002/003 的生成器仍生成 `COLLECT_LIST(a ORDER BY a ...)`，Doris 全部报：

```text
(1105, "errCode = 2, detailMessage = collect_list doesn't support order by expression")
```

这是生成器缺少目标端可执行改写，而不是缺表/数据问题。不同排序键不能简单排序聚合结果，因此必须检查 AST 中唯一排序键与聚合值严格相同，不能只比列名或删除 ORDER BY。

| 文件/位置 | 本轮变化与必要性 |
| :--- | :--- |
| `sqlglot/generators/doris.py` / DorisGenerator.arrayagg_sql | 识别 Order、单键、同一表达式、单值 DISTINCT；排除查询/Collate/一般函数和最近作用域的 Window/Filter/WithinGroup；遇 Select 停止向外查祖先 |
| 同方法的排序组合 | ARRAY_AGG 保留 NULL；COLLECT_LIST 只取得非 NULL 部分；ARRAY_SORT 或 ARRAY_REVERSE_SORT 排非 NULL 值；ARRAY_SLICE 取得升序数组开头的 NULL 段；ARRAY_CONCAT 按 NULL 方向拼接；PG 标志存在时最外层 NULLIF(...,ARRAY()) 补偿空输入 |
| DorisGenerator.ARRAY_SIZE_NAME | 设置 ARRAY_SIZE，供新组合的数组长度计算使用；继承的 ARRAY_LENGTH 在本环境不存在 |
| `tests/dialects/test_doris.py` | 新增 3 个方法：方向/DISTINCT/CAST/往返且不修改输入 AST；HAVING/分组/子查询及长度映射；不同键/多键/Collate/易变函数/窗口/FILTER 不套用。把原排除测试的自值排序改为真正排除的异值排序 |

本轮未改公共 AST、PG Parser 和 Doris Parser；此前 task-001/002/003 修改均保留。没有人为 CAST 原查询为 INT，没有对整数取负排序，也没有改比较器。实现用公共 Expression 和 self.func 构造，不拼接算术 SQL 字符串。

NULL 段长度为 `ARRAY_SIZE(ARRAY_AGG(value)) - ARRAY_SIZE(COLLECT_LIST(value))`，两边 DISTINCT 标志一致。普通输入保留所有 NULL 和重复值；DISTINCT 只保留一个 NULL。长度来自同一聚合参数，不额外引入 COUNT(*) 改变关联聚合归属。输入为空时两数组均空，最后由 PG 的 null_on_empty 标志返回 SQL NULL；全 NULL 的非空数组不能被误判为空输入。

[Doris ARRAY_SORT](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/scalar-functions/array-functions/array-sort/) 的原生升序将 NULL 放前；本轮也实际验证了这一点。[ARRAY_SLICE](https://doris.apache.org/docs/dev/sql-manual/sql-functions/scalar-functions/array-functions/array-slice/) 的第三参数是长度。最终按长度截取 NULL 段并保留原元素类型，再独立决定 NULL 段放前或放后。

本任务是独立排序行为修复，依赖 task-003 基础；未来保存 commit 时不能把本轮累积 diff 当作一个混合提交。本轮未提交/推送，没有可填写的新 SHA 或提交链接。

## 3. 实际失败尝试与修正

1. 先添加方向与排除测试，在旧生成器上真实失败（2 个方法，36 个子断言失败），确认测试确实能暴露缺口。
2. 第一版用 ARRAY_FILTER 的 lambda 分离 NULL，原 5 条运行成功；68 组边界中 66 组通过，两条 HAVING 查询失败：`(1105, 'errCode = 2, detailMessage = x should be grouped by.')`。不把它归为独立外部限制后直接验收。
3. 改用无 lambda 的 NULL 长度/切片方案。第一轮生成仍继承 ARRAY_LENGTH，68 组均因 `Can not found function 'ARRAY_LENGTH'` 失败；调整 ARRAY_SIZE_NAME 后重跑同一范围。
4. **最终 68 组全部执行成功并通过本节后列出的比较。** 临时 ARRAY_FILTER Parser/Generator 及其测试已从本任务改动移除，未保留无用辅助能力。另一个控制调用 ARRAY_REVERSE 报不存在，最终用实际支持的 ARRAY_REVERSE_SORT，没有把控制失败混入最终通过统计。

失败尝试不计为新 Case 或新 task；没有把后来的成功覆盖成“第一版一直通过”。

## 4. 五条原查询：实际生成与比较

最终执行时间：2026-11-23 09:23:47–09:23:50 UTC。新进程实际导入 `../sqlglot-experiment/sqlglot/__init__.py`，经 SqlglotTranspiler.transpile_case 生成目标后调用 pg_probe.execute_query / compare_probe。每侧再执行一次；另用 `SELECT CAST(c0 AS TEXT) FROM (<原查询去末尾分号>) checked(c0)` 核对实时 PG 与原 .out 显示文本，五条均一致。这个包装只用于补证，不替换原查询或 .out。

以下为完整原查询与最终实际生成 SQL（便于阅读并列展示，真实执行为逐条只读调用）：

```sql
-- pg-aggregates-0284-628b13e2
select array_agg(a order by a)
  from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SORT(COLLECT_LIST(a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(a)), 1, ARRAY_SIZE(ARRAY_AGG(a)) - ARRAY_SIZE(COLLECT_LIST(a)))), ARRAY()) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- pg-aggregates-0285-ee2a7bc2
select array_agg(a order by a desc)
  from (values (1,4),(2,3),(3,1),(4,2)) v(a,b);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(a)), 1, ARRAY_SIZE(ARRAY_AGG(a)) - ARRAY_SIZE(COLLECT_LIST(a))), ARRAY_REVERSE_SORT(COLLECT_LIST(a))), ARRAY()) FROM (SELECT 1 AS a, 4 AS b UNION ALL SELECT 2, 3 UNION ALL SELECT 3, 1 UNION ALL SELECT 4, 2) AS v;

-- pg-aggregates-0288-1528b423
select array_agg(distinct a order by a)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SORT(COLLECT_LIST(DISTINCT a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(DISTINCT a)), 1, ARRAY_SIZE(ARRAY_AGG(DISTINCT a)) - ARRAY_SIZE(COLLECT_LIST(DISTINCT a)))), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- pg-aggregates-0289-64071a98
select array_agg(distinct a order by a desc)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(DISTINCT a)), 1, ARRAY_SIZE(ARRAY_AGG(DISTINCT a)) - ARRAY_SIZE(COLLECT_LIST(DISTINCT a))), ARRAY_REVERSE_SORT(COLLECT_LIST(DISTINCT a))), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;

-- pg-aggregates-0290-2bc98abf
select array_agg(distinct a order by a desc nulls last)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_REVERSE_SORT(COLLECT_LIST(DISTINCT a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(DISTINCT a)), 1, ARRAY_SIZE(ARRAY_AGG(DISTINCT a)) - ARRAY_SIZE(COLLECT_LIST(DISTINCT a)))), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v;
```

| Case / 逐条归因 | 实时两端的结构化数组 | 原 .out 显示 / Doris 显示 |
| :--- | :--- | :--- |
| [0284](../../../../attribution/cases/aggregates-001/pg-aggregates-0284-628b13e2.md) | `[1,2,3,4]` | `{1,2,3,4}` / `[1, 2, 3, 4]` |
| [0285](../../../../attribution/cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md) | `[4,3,2,1]` | `{4,3,2,1}` / `[4, 3, 2, 1]` |
| [0288](../../../../attribution/cases/aggregates-001/pg-aggregates-0288-1528b423.md) | `[1,2,3,NULL]` | `{1,2,3,NULL}` / `[1, 2, 3, null]` |
| [0289](../../../../attribution/cases/aggregates-001/pg-aggregates-0289-64071a98.md) | `[NULL,3,2,1]` | `{NULL,3,2,1}` / `[null, 3, 2, 1]` |
| [0290](../../../../attribution/cases/aggregates-001/pg-aggregates-0290-2bc98abf.md) | `[3,2,1,NULL]` | `{3,2,1,NULL}` / `[3, 2, 1, null]` |

这五条每条均：双端成功、1 列/1 行、值/重复次数一致、数组内部顺序一致、重复稳定；没有显式 Alias，默认列名不强比。没有最终 ORDER BY，结果行采用多重集合，但**没有把数组元素重排后再比**。原生元素声明每条均 `_int4` / `array<tinyint>`，是真正 32 位/8 位差异，不是别名问题，整数不适用 Decimal Scale 也不能掩盖此差异。原 .out 不含原生字段类型。

CLI 原规则仍将五条记为“行值或顺序不匹配”，直接反例就是上表两种显示文本；本轮另用实时 PG 的列表和 Doris JSON 数组进行结构化补证。结构化补证不覆盖 CLI 结论，不以 AI 手写 SQL代替生成器验收。

## 5. 68 组边界与比较范围

最终时间 2026-11-23 09:23:02–09:23:09 UTC，双端同 stage-17。每条 PG SQL 由下列完整构造规则确定，经修改后的 `parse_one(sql,read='postgres').sql('doris',unsupported_level=ErrorLevel.RAISE)` 生成后实际执行；未借用原查询的 .out。边界生成规则用于说明已执行范围，不是另加到框架的功能。

60 条基础组合的源 SQL 模板：

```sql
SELECT ARRAY_AGG(<去重前缀>a ORDER BY <排序表达式>) AS xs
FROM (VALUES <逐行 CAST 后的值>) v(a)<过滤条件>
```

去重前缀为 `空` 或 `DISTINCT `；排序表达式依次为 `a`、`a ASC NULLS FIRST`、`a ASC NULLS LAST`、`a DESC`、`a DESC NULLS FIRST`、`a DESC NULLS LAST`。每个输入值必须完整写成 `(CAST(<值或 NULL> AS <类型>))`，没有省略隐式类型差异。

| 输入组 | 类型 | 按出现顺序的输入值 | 过滤条件 | 实测组合 |
| :--- | :--- | :--- | :--- | ---: |
| mixed | INT | `3,NULL,1,3,-2,NULL,0` | 无 | 12 |
| all-null | INT | `NULL,NULL` | 无 | 12 |
| empty | INT | `1` | `WHERE FALSE` | 12 |
| int32-extreme | INT | `2147483647,-2147483648,NULL,0` | 无 | 12 |
| int64-extreme | BIGINT | `9223372036854775807,-9223372036854775808,NULL,0` | 无 | 12 |

例如 mixed 的默认升序完整源文与真实生成：

```sql
SELECT ARRAY_AGG(a ORDER BY a) AS xs FROM (VALUES (CAST(3 AS INT)),(CAST(NULL AS INT)),(CAST(1 AS INT)),(CAST(3 AS INT)),(CAST(-2 AS INT)),(CAST(NULL AS INT)),(CAST(0 AS INT))) v(a);
-- 生成
SELECT NULLIF(ARRAY_CONCAT(ARRAY_SORT(COLLECT_LIST(a)), ARRAY_SLICE(ARRAY_SORT(ARRAY_AGG(a)), 1, ARRAY_SIZE(ARRAY_AGG(a)) - ARRAY_SIZE(COLLECT_LIST(a)))), ARRAY()) AS xs FROM (SELECT CAST(3 AS INT) AS a UNION ALL SELECT CAST(NULL AS INT) UNION ALL SELECT CAST(1 AS INT) UNION ALL SELECT CAST(3 AS INT) UNION ALL SELECT CAST(-2 AS INT) UNION ALL SELECT CAST(NULL AS INT) UNION ALL SELECT CAST(0 AS INT)) AS v;
```

默认升序两端 `[-2,0,1,3,3,NULL,NULL]`；默认降序 `[NULL,NULL,3,3,1,0,-2]`；DISTINCT 同时去除重复 3 和重复 NULL。全 NULL 普通聚合 `[NULL,NULL]`，DISTINCT `[NULL]`；空输入 1 行 SQL NULL，不是空数组。BIGINT 极值精确保留，没有通过取负或转 Float 实现排序。

另外 8 条完整源文：

```sql
-- grouped
SELECT g, ARRAY_AGG(a ORDER BY a DESC NULLS FIRST) AS xs FROM (VALUES (CAST(1 AS INT),CAST(2 AS INT)),(CAST(1 AS INT),CAST(NULL AS INT)),(CAST(1 AS INT),CAST(2 AS INT)),(CAST(2 AS INT),CAST(NULL AS INT)),(CAST(2 AS INT),CAST(NULL AS INT))) v(g,a) GROUP BY g ORDER BY g;
-- grouped-empty
SELECT g, ARRAY_AGG(a ORDER BY a) AS xs FROM (VALUES (CAST(1 AS INT),CAST(2 AS INT))) v(g,a) WHERE FALSE GROUP BY g ORDER BY g;
-- scalar-empty
SELECT (SELECT ARRAY_AGG(a ORDER BY a DESC) FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE) AS xs;
-- having-empty
SELECT ARRAY_AGG(a ORDER BY a) AS xs FROM (VALUES (CAST(1 AS INT))) v(a) WHERE FALSE HAVING ARRAY_AGG(a ORDER BY a) IS NULL;
-- having-all-null
SELECT ARRAY_AGG(a ORDER BY a) AS xs FROM (VALUES (CAST(NULL AS INT))) v(a) HAVING ARRAY_AGG(a ORDER BY a) IS NULL;
-- multiple
SELECT ARRAY_AGG(a ORDER BY a) AS xs, ARRAY_AGG(DISTINCT a ORDER BY a DESC) AS ys FROM (VALUES (CAST(2 AS INT)),(CAST(NULL AS INT)),(CAST(2 AS INT)),(CAST(1 AS INT))) v(a);
-- left-join
SELECT l.id, ARRAY_AGG(r.a ORDER BY r.a) AS xs FROM (VALUES (CAST(1 AS INT)),(CAST(2 AS INT))) l(id) LEFT JOIN (VALUES (CAST(1 AS INT),CAST(9 AS INT))) r(id,a) ON l.id=r.id GROUP BY l.id ORDER BY l.id;
-- expression
SELECT ARRAY_AGG(CAST(a AS BIGINT)+1 ORDER BY CAST(a AS BIGINT)+1 DESC) AS xs FROM (VALUES (CAST(2 AS INT)),(CAST(NULL AS INT)),(CAST(-3 AS INT))) v(a);
```

| 变体 | 实际双端结果 |
| :--- | :--- |
| grouped | `(1,[NULL,2,2]),(2,[NULL,NULL])`，最终按 g 顺序相同 |
| grouped-empty | 0 行，不凭空生成分组 |
| scalar-empty / having-empty | 各 1 行 SQL NULL |
| having-all-null | 0 行，[NULL] 不是 SQL NULL |
| multiple | 1 行两数组：`[1,2,2,NULL]` 和 `[NULL,2,1]` |
| left-join | `(1,[9]),(2,[NULL])`；未匹配连接行不同于没有输入行，按 id 顺序相同 |
| expression | `[NULL,3,-2]`，BIGINT CAST 和同表达式排序正确 |

最终 68/68：双端成功、字段数量/显式 Alias、行数、完整有限行值/重复次数均一致；每端额外重复一次，执行与记录均稳定。有最终 ORDER BY 的分组/连接按结果行顺序核对，g/id 在这些分组结果中唯一；其他查询忽略结果行顺序，但保留数组元素顺序。未放宽 Float 容差。

类型补证：60 个基本组合及其余 8 条实际取得 `_int4` / `array<int>` 或 `_int8` / `array<bigint>`，分组键为 `int4` / `int`；按明确元素类型逐项核对，同为 32 位或 64 位有符号整数。工具本身仍会把数组别名记作声明不同，未改工具，而是在报告说明原生声明及对应关系。整数无 Decimal Precision/Scale；没有据此宣称 Decimal/Timestamp 或所有嵌套元数据已验收。

额外 3 条原生 Doris 控制：有序 ARRAY_AGG 的空输入重新解析/生成后仍是 []；COLLECT_LIST 的全 NULL 输入仍是 []；ARRAY_SIZE(ARRAY(1,NULL,2)) 为 BIGINT 3。未给非 PG 来源误加 null_on_empty。

## 6. 单元测试、回归与后续

新增 `test_array_agg_value_ordering`、`test_array_agg_value_ordering_contexts`、`test_array_agg_value_ordering_exclusions`。严格生成、12 种方向/DISTINCT 组合、CAST、输入 AST 不变、生成 SQL 往返、HAVING/分组/子查询、ARRAY_SIZE 名称及排除边界均执行；相关 PG/Doris/MySQL 143 个方法、全部方言 1,066 个方法和所选核心 233 个方法通过，命令与未运行范围见汇总。不把 143 个子集再加到 1,066 上。

75 条原查询按原 YAML/.out、16 个阶段真实重跑：65 匹配、4 Doris 执行失败、6 行值或顺序不匹配。此前 65 个匹配全部保留；五个排序查询由执行失败变为显示差异。其余错误为 0276 序列、0283/0286 异值排序、0371 整行/维度，均没有被静默套用本规则。没有重跑全部 313 条，也没有修改历史 validation JSON。

本任务的单键整数排序条件已验收；5 条完整 Case 的类型/表示仍有差异，因此不宣称五条已完全等价。未覆盖任意 Collation、浮点 NaN 排序、复合类型、易变计算、窗口/FILTER、多键/异值排序、数组下界和大规模性能；本轮生成较长且包含两种聚合，不声称资源开销与 PG 相同。

同规则的 HAVING 遗漏在本轮继续修复，没有新建任务；ARRAY_SIZE 是该组合的必要函数名适配。类型/表示复用既有研究，不擅自新增或实施其他能力。建议下一项 task-005（普通忽略 NULL 聚合的 FILTER），本轮未执行。整份输入仍未完成，当前统一状态见归因汇总。
