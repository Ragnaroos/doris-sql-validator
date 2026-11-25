# task-007 / fix-007：有效样本不足两条时返回 NULL

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`0ef0f5173ef4420a8e43b58beea07dc5a3646af0`。保存有限输入的小样本NULL规则及AST/Parser/Generator测试；多样本精度和特殊数值余项保留。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与范围

**已修复并完成有限浮点输入的小样本 NULL 规则验收。** 不等于七条原查询都获得 .out MATCH，也不等于统计函数在所有类型、精度和特殊值上完全等价。

- 入口：[task-007](../../../../attribution/aggregates-001-attribution-summary.md#task-007)，共同版本/授权/命令见[本轮汇总](../../../aggregates-001-fix-007-summary.md)。指定任务模式，无 commit/push/Issue/PR。
- 纳入：PostgreSQL STDDEV / STDDEV_SAMP、VARIANCE / VAR_SAMP、COVAR_SAMP 的普通聚合；0、1、2 及更多有限有效输入，NULL、重复、一元 DISTINCT 和已测上下文。
- 排除：总体统计算法改写、NaN/Infinity、窗口、FILTER、有序集合、内部 ORDER BY、二元 DISTINCT、任意精度 NUMERIC 返回类型与多样本算法精度。有限确定性数值表达式的实测不能推广为任意 UDF/易变表达式等价。
- 独立行为：小样本 NULL 补偿；不用总体方差代替样本方差，不夹带 task-009 的 REGR_COUNT 实现。无其他 task 的必须依赖。
- 七个原 Case 均属 stage-01 / 双端 dsv_wf_agg001_s01；源 SQL/.out、YAML、数据和比较规则不变。

## 2. 修复前事实与实现

修复前七条实际双端执行成功，但 PG 返回 `[0.0,NULL]`（NUMERIC 两条为 Decimal 0 和 NULL），Doris 返回 `[0.0,0.0]`；这是实际 NULL 行为差异，不是只有显示格式不同。原 .out 均为 `[["0",""]]`，实时 PG 也另核对相同文本，实际 NULL 由驱动补证确认。

[PostgreSQL 18 统计聚合文档](https://www.postgresql.org/docs/18/functions-aggregate.html)规定无意义的小样本结果为 NULL，协方差有效 N 为两参数均非 NULL 的行数。Doris [STDDEV_SAMP](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/aggregate-functions/stddev-samp/)与[COVAR_SAMP](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/aggregate-functions/covar-samp/)有自身约定；本轮以本机 4.1.3 的实际执行作为修复证据，不从函数同名推断语义一致。

| 文件 / 实际入口 | 改动与原因 |
| :--- | :--- |
| expressions/aggregate.py：Stddev、StddevSamp、Variance、CovarSamp | 新增可选参数 null_on_insufficient_samples，含义为少于两条有效样本必须返回 NULL；不把任一源库默认行为强加给所有 AST |
| parsers/postgres.py：FUNCTIONS | PG 五个函数拼写构建既有公共节点，并设置上述语义标记；Tokenizer 不变，不需要传入表 Schema |
| generators/doris.py：_sample_aggregate_sql | 共用生成入口服务四个 AST 节点；生成 IF(COUNT(...) < 2,NULL,原样本统计函数)，不修改原生多样本公式 |
| tests/dialects/test_postgres.py | 标记、AST 类型、PG 生成、dump/load 序列化；Doris 源解析无该标记、总体统计不标记 |
| tests/dialects/test_doris.py | NULL 补偿、DISTINCT、成对计数、HAVING、子查询、round-trip、copy=False 输入不变，以及排除范围/原生 Doris 保持 |

一元聚合的 COUNT 与聚合使用同一参数；DISTINCT 同时保留在 COUNT 和统计函数中。协方差使用 `COUNT(IF(x IS NULL,NULL,y))`：x 为 NULL 时不计，x 非 NULL 但 y 为 NULL 时同样不计，因此不会把两列错位的有效值当成有效配对。

仅带 PG 标记且不处于 Window/Filter/WithinGroup、无内部 Order 时补偿。Doris 源 SQL 不带标记，生成后的 IF 在 Doris round-trip 不会被套第二层；Oracle single_value_returns_zero 仍委托既有 variance_sql。没有原地修改输入 AST，也没有给验证框架加条件重写。

## 3. 七条原查询的实际执行

2026-11-23 UTC，修改后新进程 import 为 `../sqlglot-experiment/sqlglot/__init__.py`。使用 `parse_one(source_sql,read="postgres").sql("doris")` 实际生成，下列不是手写候选；execute_query / compare_probe 补查两端，限时 10 秒、完整结果上限 10,000 行，原查询均一行。

```sql
-- 0029：pg-aggregates-0029-d0645c62，原行 60–62
SELECT var_pop(1.0::float8), var_samp(2.0::float8);
-- 实际生成
SELECT VAR_POP(CAST(1.0 AS DOUBLE)), IF(COUNT(CAST(2.0 AS DOUBLE)) < 2, NULL, VAR_SAMP(CAST(2.0 AS DOUBLE)))

-- 0030：pg-aggregates-0030-549b8efa，原行 63
SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8);
-- 实际生成
SELECT STDDEV_POP(CAST(3.0 AS DOUBLE)), IF(COUNT(CAST(4.0 AS DOUBLE)) < 2, NULL, STDDEV_SAMP(CAST(4.0 AS DOUBLE)))

-- 0035：pg-aggregates-0035-daf9210d，原行 68
SELECT var_pop(1.0::float4), var_samp(2.0::float4);
-- 实际生成
SELECT VAR_POP(CAST(1.0 AS FLOAT)), IF(COUNT(CAST(2.0 AS FLOAT)) < 2, NULL, VAR_SAMP(CAST(2.0 AS FLOAT)))

-- 0036：pg-aggregates-0036-7e813a8e，原行 69
SELECT stddev_pop(3.0::float4), stddev_samp(4.0::float4);
-- 实际生成
SELECT STDDEV_POP(CAST(3.0 AS FLOAT)), IF(COUNT(CAST(4.0 AS FLOAT)) < 2, NULL, STDDEV_SAMP(CAST(4.0 AS FLOAT)))

-- 0041：pg-aggregates-0041-6590092b，原行 74
SELECT var_pop(1.0::numeric), var_samp(2.0::numeric);
-- 实际生成
SELECT VAR_POP(CAST(1.0 AS DECIMAL)), IF(COUNT(CAST(2.0 AS DECIMAL)) < 2, NULL, VAR_SAMP(CAST(2.0 AS DECIMAL)))

-- 0042：pg-aggregates-0042-48fe21bd，原行 75
SELECT stddev_pop(3.0::numeric), stddev_samp(4.0::numeric);
-- 实际生成
SELECT STDDEV_POP(CAST(3.0 AS DECIMAL)), IF(COUNT(CAST(4.0 AS DECIMAL)) < 2, NULL, STDDEV_SAMP(CAST(4.0 AS DECIMAL)))

-- 0082：pg-aggregates-0082-f9348d8f，原行 138–139
SELECT covar_pop(1::float8,2::float8), covar_samp(3::float8,4::float8);
-- 实际生成
SELECT COVAR_POP(CAST(1 AS DOUBLE), CAST(2 AS DOUBLE)), IF(COUNT(IF(CAST(3 AS DOUBLE) IS NULL, NULL, CAST(4 AS DOUBLE))) < 2, NULL, COVAR_SAMP(CAST(3 AS DOUBLE), CAST(4 AS DOUBLE)))
```

修改前生成 SQL 与上面目标语句相比，样本列没有 IF/COUNT 补偿，完整旧 SQL/首轮事实保留在各 Case 第 2 节。现在所有目标样本列实际为 NULL，正常总体列不改，仍为 0.0。

| Case | 状态/字段 | 类型声明 | 实时完整结果 | 原 .out 比较 | 本任务验收 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 0029、0030、0035、0036、0082 | 双端成功，两列；无显式 Alias，不要求默认字段名相同 | 两列 PG float8 / Doris double，FLOAT64 一致 | 两端均 `[0.0,NULL]`，数值、NULL 和行数一致 | 仍不匹配：源 `["0",""]` / 目标 `["0.0",""]` | 样本 NULL 修复通过 |
| 0041、0042 | 双端成功，两列；无显式 Alias | PG numeric / Doris double 仍不同；精度/Scale 信息不足 | Decimal 0 / double 0 值一致，第二列均 NULL | 同上，显示比较仍不同 | NULL 规则通过，NUMERIC 完整类型契约不关闭 |

七条源/目标各重跑一次，值与行数稳定；原查询无最终 ORDER BY，按多重集合比较，无排序要求。原源 SQL 没有被替换为类型统一版。当前七条 PG 显示文本另用只读包装 `SELECT CAST(c0 AS TEXT),CAST(c1 AS TEXT) FROM (<原SQL>) checked(c0,c1)` 核对，与原 .out 全部一致；这仅是显示补证，不作为替换源查询。

标准框架实际同批执行方式（从工作流根目录，使用既有 .env）：

```python
load_dotenv(Path("../doris-sql-validator/.env"))
args = ["run", "--path", "reports/data-preparation/aggregates-001-stage-01-cases.yaml", "--stdout"]
for case in loaded.definition.cases:
    if case.statement_index in {29, 30, 35, 36, 41, 42, 82}:
        args += ["--id", case.id]
result = CliRunner().invoke(app, args)
```

解释器 `../doris-sql-validator/.venv/bin/python`，PYTHONPATH=`../sqlglot-experiment:src`；loaded 由 load_case_file 读取上面 YAML。退出 1，七条“行值或顺序不匹配”，没有伪造新的匹配或保存新 JSON。仅看这个退出码看不出 NULL 规则已生效，须结合上表的逐维度补证。

## 4. 有限边界与回归

### 4.1 一元统计和协方差配对：212 条

一元输入序列如下，每序列分别用 REAL / DOUBLE PRECISION、STDDEV / STDDEV_SAMP / VARIANCE / VAR_SAMP、普通 / DISTINCT，共 `12×2×4×2=192` 条。

```python
seqs = [[], [None], [None, None, None], [2], [2, None], [2, 2],
        [2, 4], [2, 2, 4], [1, 2, 3], [-2, 2], [0, 0], [None, 1, 2, None, 3]]
```

实际源构造为 `SELECT <函数>([DISTINCT] x) AS v FROM (<body>) t`。body 按原序列逐项拼接 `SELECT CAST(<值或NULL> AS <类型>) AS x`，使用 UNION ALL 保留重复；空序列为 `SELECT CAST(NULL AS <类型>) AS x WHERE FALSE`。完整源 SQL 每次经本轮 SQLGlot 生成目标，不在框架中改写。

协方差输入如下，每组用 REAL / DOUBLE PRECISION，共 20 条；body 同理为两列 CAST，空组 WHERE FALSE。

```python
pairs = [[], [(None, None)], [(1, None), (None, 2)], [(1, 2)],
         [(1, 2), (None, 3), (4, None)], [(1, 2), (3, 6)], [(1, 2), (1, 2)],
         [(1, 2), (None, 3), (3, 6), (4, None)],
         [(1, 2), (2, 4), (3, 6)], [(None, None), (None, None)]]
# source = "SELECT COVAR_SAMP(x,y) AS v FROM (" + body + ") t"
```

212 条均双端成功、FLOAT64 类型声明一致、各端重跑稳定。有效样本不足两条的 **108 条均为 NULL/NULL**，含 DISTINCT 后只剩一条和两列错位不形成配对。全部结果采集完整，没有截断。

为了不把 PG 的文本显示舍入当作算术值，边界使用既有 PostgresAdapter 建立只读连接，statement_timeout=10s，以 `cursor(binary=True)` 读取字段和结果，pack 后交同一 compare_probe；目标仍使用 execute_query。这个补证没有改变 run 的 .out 规则。

结果为 **184 条值精确相同，28 条正常多样本浮点尾差**；不自动套容差。28 条都去掉新语义标记、生成未补偿的 Doris 原生统计 SQL 作控制，取得同样目标值，证明尾差不是 IF/COUNT 引入。

| 覆盖两种输入类型的尾差组 | 数量 | PG binary / Doris 当前读取值 |
| :--- | ---: | :--- |
| [2,4]，STDDEV / STDDEV_SAMP，普通及 DISTINCT | 8 | 1.4142135623730951 / 1.414213562373095 |
| [2,2,4]，两个标准差拼写，普通 | 4 | 1.1547005383792515 / 1.154700538379251 |
| [2,2,4]，两个标准差拼写，DISTINCT | 4 | 1.4142135623730951 / 1.414213562373095 |
| [2,2,4]，VARIANCE / VAR_SAMP，普通 | 4 | 1.3333333333333333 / 1.333333333333333 |
| [-2,2]，两个标准差拼写，普通及 DISTINCT | 8 | 2.8284271247461903 / 2.82842712474619 |

例如实际生成的两样本标准差：

```sql
-- PostgreSQL 源
SELECT STDDEV_SAMP(x) AS v FROM (SELECT CAST(2 AS REAL) AS x UNION ALL SELECT CAST(4 AS REAL) AS x) t
-- 修改后 SQLGlot 实际目标
SELECT IF(COUNT(x) < 2, NULL, STDDEV_SAMP(x)) AS v FROM (SELECT CAST(2 AS FLOAT) AS x UNION ALL SELECT CAST(4 AS FLOAT) AS x) AS t
-- 控制：仅清除标记后实际生成，得到相同 Doris 值
SELECT STDDEV_SAMP(x) AS v FROM (SELECT CAST(2 AS FLOAT) AS x UNION ALL SELECT CAST(4 AS FLOAT) AS x) AS t
```

Doris 另对标准差和方差直接列值 / CAST 为 STRING 补查，也显示相同尾数；这仍不证明已经排除了所有服务端格式化/协议影响。因此只确认“本补偿未引入尾差”，不直接宣布 Doris 底层浮点算法缺陷，不修改比较器。

### 4.2 上下文：13 条

共同 `(g,x,y)` 输入如下；g 显式 INT，x/y 显式 DOUBLE PRECISION，按原顺序 UNION ALL：

```python
rows = [(1,None,None), (1,None,4), (2,2,4), (2,None,5), (3,1,2),
        (3,3,6), (4,2,4), (4,2,4), (5,3,None), (5,None,6)]
```

以下 `t` 表示上述常量输入组成的派生表，不新建数据库表。源查询按这些明确子句构造，再实际经 SQLGlot 生成和双端执行；这里合并共用输入，避免重复十行常量文本。

| 编号 | 完整查询结构（共用派生输入 t） | 实际结果与限制 |
| :--- | :--- | :--- |
| 1 | SELECT g,STDDEV_SAMP(x) AS s,VAR_SAMP(x) AS v,VAR_POP(x) AS p FROM t GROUP BY g ORDER BY g | NULL/样本方差/总体值正确；g=3 标准差出现上表尾差 |
| 2 | SELECT g,STDDEV_SAMP(DISTINCT x) AS s,VAR_SAMP(DISTINCT x) AS v FROM t GROUP BY g ORDER BY g | g=4 重复值去重后必须 NULL，已通过；g=3 标准差尾差保留 |
| 3 | SELECT g,COVAR_SAMP(x,y) AS c,COVAR_POP(x,y) AS p FROM t GROUP BY g ORDER BY g | 两端 c：NULL、NULL、4、0、NULL；总体对应 NULL、0、2、0、NULL |
| 4 | SELECT g,STDDEV_SAMP(x) AS s FROM t GROUP BY g HAVING STDDEV_SAMP(x) IS NULL ORDER BY g | g=1/2/5，结果一致 |
| 5 | SELECT g,COVAR_SAMP(x,y) AS c FROM t GROUP BY g HAVING COVAR_SAMP(x,y) IS NULL ORDER BY g | g=1/2/5，结果一致 |
| 6 | SELECT (SELECT STDDEV_SAMP(x) FROM t WHERE FALSE) AS s | 一行 NULL；内部 Select 不跨越作用域补 COUNT |
| 7 | WITH t AS (共同输入) SELECT g,VAR_SAMP(x) AS v FROM t GROUP BY g ORDER BY g DESC | (5,NULL)、(4,0)、(3,2)、(2,NULL)、(1,NULL)，一致 |
| 8 | SELECT COALESCE(VAR_SAMP(x),CAST(-1 AS DOUBLE PRECISION)) AS v FROM t WHERE g=2 | -1，一致 |
| 9 | SELECT VAR_SAMP(x) AS v FROM t WHERE g=2 UNION ALL SELECT VAR_SAMP(x) AS v FROM t WHERE g=2 | 两行 NULL，重复次数保留；另直接核对字段名 v 一致 |
| 10 | SELECT STDDEV(x+1) AS s,VARIANCE(x+1) AS v FROM t WHERE g=2 | 两列 NULL，一致 |
| 11 | SELECT g,STDDEV_SAMP(x) AS s FROM t WHERE FALSE GROUP BY g ORDER BY g | 零行，字段类型仍取得并一致 |
| 12 | SELECT g,VAR_SAMP(x) AS v FROM t GROUP BY g HAVING VAR_SAMP(x)>1 ORDER BY g | 仅 (3,2)，一致 |
| 13 | SELECT c.g,VAR_SAMP(t.x) AS v FROM (SELECT CAST(1 AS INT) AS g UNION ALL SELECT CAST(6 AS INT)) c LEFT JOIN t ON c.g=t.g GROUP BY c.g ORDER BY c.g | (1,NULL)、(6,NULL)，空匹配组仍 NULL |

13 条全部成功、字段数/实际别名/类型声明一致，双端重跑稳定；11 条结果精确一致。1/2 两条仍有多样本尾差；直接核对组键顺序均为 1、2、3、4、5，差异位于数值，不是行重排。工具“顺序不同”的通用提示包含该行值差异，不据此归因排序错误。唯一分组键提供稳定排序依据。

1/2 的未补偿控制在 g=3 保留同一标准差尾差，而 g=2/5（以及 DISTINCT 的 g=4）从旧 0 正确改为 NULL。225 条（212+13）整体为 195 条精确值一致、30 条既有尾差，不能称 225 条完全等价；小样本规则没有反例。

### 4.3 排除范围与测试

另查 14 条历史 NaN/Infinity 目标控制（原编号 31–34、37–40、43–46、83/84）：10 条样本目标从 0 变 NULL，4 条不变。**不能说这些非有限数未受影响或已经等价。** 它们不是本任务有限输入验收范围，保留非有限数/类型转换研究，不据这些变化新增 MATCH 或关闭原 Case；源 SQL 不改、没有为它们制造答案。

先加 3 个新方法，修复前 20 个失败断言；一次 Count.lt 不存在的实现错误在单测发现并改为 exp.LT，未进入最终版本。最后实际通过：PG/Doris/MySQL 150 个方法、全部方言 1,073 个方法、相关核心 233 个方法；Ruff check / format 与 git diff --check 通过。完整命令及未执行的 make check、C 扩展、mypy 等范围见汇总。

单测覆盖 AST dump/load、Doris 源无标记、生成后 round-trip 不重复包装、copy=False 不污染输入、现有 Oracle 方差路径及其他方言回归。未连接其他源引擎做数据库验证，未验证二元 DISTINCT、窗口/FILTER 或任意非有限数输入。

## 5. 验收、任务归并与下一步

本任务约定的 NULL 补偿通过：108 条小样本 NULL 边界无反例；COUNT(DISTINCT) 与协方差配对规则正确；正常多样本继续原统计函数。7 条原 Case 的 NULL 已修正，但整条 .out 仍被 `0` / `0.0` 显示差异阻断，0041/0042 另有真实 NUMERIC/DOUBLE 类型差异，不能写成完整 MATCH。

扩大回归 99 条为 72 匹配、9 目标执行失败、14 行值/顺序不匹配、4 源负向；此前 72 条匹配保持。没有新增已匹配查询回归；保留浮点/表示、NUMERIC、非有限数、数组及相关聚合研究，不把它们全部塞进本次修复或新建重复 task。

当前清单为 5 项约定验收、2 项修改未验收、2 项未处理。**task-007 的有限输入 NULL 规则完成，整份输入未完成。** 下一建议 task-008：FROM 位置常量整数 GENERATE_SERIES，本轮未实施。无 commit/push、无社区提交；补丁只保存在本地实验 checkout。
