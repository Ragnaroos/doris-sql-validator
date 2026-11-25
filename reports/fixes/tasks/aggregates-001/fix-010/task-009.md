# task-009：REGR_COUNT 成对非 NULL 计数

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`f7492dc5b7e3d999ced4429d69ceed7ed4a6f1d8`。保存普通数值参数的成对计数及测试，不将0544的统计/SUM余项算作本task已解决。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与范围

**已修复并完成约定验收。** 原普通数值列 `REGR_COUNT(y,x)` 改为 Doris `COUNT(IF(NOT y IS NULL AND NOT x IS NULL,1,NULL))`。两个参数都非 NULL 才计数；全部无效或空输入返回 BIGINT 0。`NOT x IS NULL` 是本生成器的实际输出，等价于 `x IS NOT NULL`。

任务来自[统一清单](../../../../attribution/aggregates-001-attribution-summary.md#task-009)，关联 [0073](../../../../attribution/cases/aggregates-001/pg-aggregates-0073-ba8ee5d1.md) 和 [0544](../../../../attribution/cases/aggregates-001/pg-aggregates-0544-3a307492.md)。本轮是首次实现 task-009；[fix-009](../../../aggregates-001-fix-009-summary.md)处理的是 task-008。共同环境、权限、版本/diff 指纹和测试范围见[本轮汇总](../../../aggregates-001-fix-010-summary.md)。

验收范围：源端成功、参数为数值列或常量及可表示范围内的显式数值 CAST；普通聚合、GROUP BY/HAVING、非相关子查询/CTE、重复行、空输入。未强制传入 Schema；列的真实数值类型来自源查询与准备前提，不声称无 Schema 能识别所有非法列类型。

不纳入其他 REGR_*、DISTINCT、聚合内 ORDER BY、FILTER、直接 OVER、任意/易变函数及算术参数、字符串隐式转换。数值转换本身的溢出、极端 NUMERIC 和非有限数的跨库兼容没有通用证明。完成的是成对计数，不是所有外层操作或全部 PostgreSQL 输入同义。

## 2. 实现与独立提交边界

| 文件/函数 | 本轮修改 |
| :--- | :--- |
| [sqlglot/generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py)，DorisGenerator.regrcount_sql | 自动命名入口，复用已有 exp.RegrCount 的 this/expression，构造运行时成对非 NULL 条件与 COUNT；不新增 Parser/公共 AST |
| [tests/dialects/test_doris.py](../../../../../../sqlglot-experiment/tests/dialects/test_doris.py)，test_regr_count / test_regr_count_exclusions | 生成、round-trip、不修改输入 AST、CAST/NULL/限定名与引用名、分组/子查询作用域，以及明确排除范围 |

先检查最近 Window/Filter/WithinGroup/Select 祖先，Select 作为边界，不跨子查询误判外层窗口。参数检查只决定保守支持范围：保留原始显式数值 CAST；可空叶节点的资格检查复用 COALESCE 类型推断，但生成 SQL 不用 COALESCE 替换参数。NULL 处理在 SQL 的 IS NULL 条件中执行，不在 Python 中把 NULL 输入替换成固定计数答案。

两个原参数在计数条件中各出现一次；不通过乘法、相加等消除 NULL，不对表名/列名/参考结果特判。RAISE 模式对未纳入形状给出 UnsupportedError。非 RAISE 模式保留原函数文本并发出诊断；该文本不是已支持能力。没有改变原比较规则或以转字符串制造相同。

本轮代码与测试净增 114 行，行为独立，无必须依赖其他 task 的代码。工作区已有前轮修改均保留；整体 diff 不是本 task 的提交边界。**未 commit/push，无 Issue/PR。**

## 3. 两条原查询的修复后执行

使用原 YAML/数据库与原 .out，生成器为本轮实验 checkout。实时 PG 是补证，不替换 .out；本轮这两条实时源值与其 .out 一致。

### 3.1 0073 / stage-01

源 SQL（原文件 127–128 行附近，语句 73；准确 Case 源位置沿用 YAML）：

```sql
SELECT regr_count(b, a) FROM aggtest;
```

修复前本轮已重现：PG 成功返回 4，Doris SQL 为 `SELECT REGR_COUNT(b, a) FROM aggtest`，报 `(1105, "errCode = 2, detailMessage = Can not found function 'REGR_COUNT'")`。

修复后实际生成并执行：

```sql
SELECT COUNT(IF(NOT b IS NULL AND NOT a IS NULL, 1, NULL)) FROM aggtest
```

| 维度 | 实测 |
| :--- | :--- |
| 状态 / 字段数量 | 双端成功，1 列 |
| 类型 | PG int8，Doris bigint（精度 20、scale 0）；均为有符号 64 位整数，类型声明一致 |
| 行数、值与重复次数 | 双端 1 行 `[[4]]`；.out 为 `[["4"]]`；框架结果为匹配 |
| 名称 | 无显式别名，按原规则不要求表达式自动列名相同；PG 名称 regr_count 与 Doris 表达式名确实不同 |
| 顺序 / 稳定性 | 单行，无最终 ORDER BY；双端重复一次，结果均稳定 |

### 3.2 0544 / stage-41

源 SQL：

```sql
SELECT variance(unique1::int4), sum(unique1::int8), regr_count(unique1::float8, unique1::float8)
FROM (SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1
      UNION ALL SELECT * FROM tenk1) u;
```

修复后实际生成（第一列的 IF 来自已保留的 task-007，不属于本轮新增）：

```sql
SELECT IF(COUNT(CAST(unique1 AS INT)) < 2, NULL, VAR_SAMP(CAST(unique1 AS INT))), SUM(CAST(unique1 AS BIGINT)), COUNT(IF(NOT CAST(unique1 AS DOUBLE) IS NULL AND NOT CAST(unique1 AS DOUBLE) IS NULL, 1, NULL)) FROM (SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1 UNION ALL SELECT * FROM tenk1) AS u
```

| 维度 | 实测 |
| :--- | :--- |
| 状态 / 字段数量 | 从找不到 REGR_COUNT 变为双端成功，3 列、1 行 |
| 第一列 | PG NUMERIC `8333541.588539713493`；Doris DOUBLE `8333541.588539706`，值/类型不同 |
| 第二列 | 数值均 199980000；PG NUMERIC / Doris BIGINT，类型不同 |
| 第三列（本任务） | 双端 40000，PG int8 / Doris bigint（20,0），值与类型声明一致 |
| 名称 / 顺序 | 无显式别名，不比较自动列名；无最终 ORDER BY、单行 |
| 重复执行 | 本轮双端完整结果各重复一次均稳定；不证明并行方差算法全输入稳定 |
| 完整 Case | **行值或顺序不匹配**，不改写为 MATCH；第一/二列复用既有类型/精度研究 |

原 `.out` 为 `[["8333541.588539713493","199980000","40000"]]`。没有替换参考答案、调整容差或手写目标答案。

## 4. 边界与上下文的执行事实

同一进程逐条调用以下入口；生成在新进程导入本轮代码后执行，目标不是手写候选：

```python
target_sql = parse_one(source_sql, read="postgres").sql(
    "doris", unsupported_level=ErrorLevel.RAISE
)
source = execute_query("postgres", source_sql, "dsv_wf_agg001_s01", timeout=10, row_limit=10000)
target = execute_query("doris", target_sql, "dsv_wf_agg001_s01", timeout=10, row_limit=10000)
checks = compare_probe(source, target, source_sql)
```

每条双端再执行一次，检查记录/字段稳定性；重复调用不计为新用例。完整有限结果参与比较，没有以样本冒充完整结果。未放宽浮点容差：输出计数为 BIGINT，无需浮点误差策略。

### 4.1 六种类型 × 八种状态：48 条均通过

类型分别为 SMALLINT、INT、BIGINT、REAL、DOUBLE PRECISION、NUMERIC(12,3)。每个状态的每个数值/NULL 都显式 CAST 为该类型，以避免把驱动默认推断当类型边界。源 SQL 的精确构造模板如下，`<rows>` 为下表记录逐值 CAST 后的 VALUES 列表；只有 empty 状态追加 `WHERE FALSE`：

```sql
SELECT REGR_COUNT(y,x) AS n FROM (VALUES <rows>) v(x,y)
```

实际生成遵循同一规则，VALUES 按 SQLGlot 现有实现改写为 SELECT/UNION ALL，数值 CAST 保留（REAL → FLOAT，DOUBLE PRECISION → DOUBLE）：

```sql
SELECT COUNT(IF(NOT y IS NULL AND NOT x IS NULL, 1, NULL)) AS n
FROM (SELECT CAST(1 AS DOUBLE) AS x, CAST(2 AS DOUBLE) AS y
      UNION ALL SELECT CAST(NULL AS DOUBLE), CAST(3 AS DOUBLE)) AS v
```

上面的目标形状只用于说明展开方式，不作为一次额外计数的用例；实际八组输入如下：

| 状态 | 输入 (x,y) | 双端计数，每种类型均实测 |
| :--- | :--- | ---: |
| valid | (1,2),(3,4) | 2 |
| left-null | (NULL,2) | 0 |
| right-null | (1,NULL) | 0 |
| both-null | (NULL,NULL) | 0 |
| duplicate-mixed | (1,2),(1,2),(NULL,2),(1,NULL),(NULL,NULL) | 2 |
| empty | (1,2)，追加 WHERE FALSE | 0 |
| zeros | (0,0),(-1,0),(0,-1) | 3 |
| all-null | (NULL,NULL),(NULL,NULL) | 0 |

48 条均：双端成功、字段 n、PG int8 / Doris bigint、1 行、精确值与重复次数一致、复跑稳定。无最终 ORDER BY，不要求行顺序；单行不存在排序歧义。

### 4.2 上下文与数值边界：19 条，18 条完整通过

为避免重复整段输入，下面引用 V 的上下文使用相同的完整关系表达式，执行时将 V **展开为括号内 VALUES 原文**，不是查询名或已创建表：

```sql
(VALUES (CAST(1 AS INT),CAST(1 AS DOUBLE PRECISION),CAST(2 AS DOUBLE PRECISION)),
        (1,NULL,2),(2,1,NULL),(2,NULL,NULL),(3,1,2),(3,1,2)) v(g,x,y)
```

| 实测源 SQL，V 按上述原文展开 | 双端观察 |
| :--- | :--- |
| SELECT g,REGR_COUNT(y,x) AS n FROM V GROUP BY g ORDER BY g | [[1,1],[2,0],[3,2]]；g 为 INT，n 为 BIGINT；唯一 g 排序一致 |
| SELECT g,REGR_COUNT(y,x) AS n FROM V GROUP BY g HAVING REGR_COUNT(y,x)>0 ORDER BY g | [[1,1],[3,2]]，类型与顺序一致 |
| SELECT g,REGR_COUNT(y,x) AS n FROM V WHERE FALSE GROUP BY g ORDER BY g | 零行，INT/BIGINT 字段仍一致 |
| WITH c AS (SELECT g,x,y FROM V) SELECT REGR_COUNT(y,x) AS n FROM c | [[3]]，BIGINT |
| SELECT (SELECT REGR_COUNT(y,x) FROM V) AS n | [[3]]，BIGINT |
| SELECT REGR_COUNT(v.y,v.x) AS n FROM V | [[3]]，BIGINT；限定名保留 |
| SELECT REGR_COUNT(y,x) AS n FROM V UNION ALL SELECT REGR_COUNT(y,x) AS n FROM V | [[3],[3]]，BIGINT；两条重复结果保留；另外核实两端别名均为 n |
| SELECT REGR_COUNT(CAST(y AS DOUBLE PRECISION),CAST(x AS DOUBLE PRECISION)) AS n FROM V | [[3]]，BIGINT；目标显式 CAST 均保留 |
| SELECT REGR_COUNT(y,x) AS "Pair Count" FROM V | [[3]]，BIGINT；两端字段名均为 Pair Count |
| SELECT REGR_COUNT(NULL,NULL) AS n | [[0]]，BIGINT |
| SELECT REGR_COUNT(-1.5,2) AS n | [[1]]，BIGINT |
| SELECT REGR_COUNT(CAST(NULL AS DOUBLE PRECISION),CAST(1 AS INT)) AS n | [[0]]，BIGINT |
| SELECT SUM(n) OVER () AS total FROM (SELECT g,REGR_COUNT(y,x) AS n FROM V GROUP BY g) c ORDER BY g | 数值均三行 3，顺序稳定；PG NUMERIC / Doris BIGINT，**类型不同，不记完整通过** |
| SELECT REGR_COUNT(v.y,v.x) AS n FROM (VALUES(CAST(4 AS INT))) k(g) LEFT JOIN V ON k.g=v.g | [[0]]，BIGINT；无匹配右表的 NULL 扩展行不误计为 1 |
| SELECT CAST(SUM(n) OVER () AS BIGINT) AS total FROM (SELECT g,REGR_COUNT(y,x) AS n FROM V GROUP BY g) c ORDER BY g | [[3],[3],[3]]，BIGINT，顺序一致；这是独立的显式类型变体，不替换上一条失败 |
| SELECT REGR_COUNT(CAST(y AS INT),CAST(x AS DOUBLE PRECISION)) AS n FROM V | [[3]]，BIGINT |
| SELECT REGR_COUNT(CAST(CAST(y AS REAL) AS DOUBLE PRECISION),CAST(x AS INT)) AS n FROM V | [[3]]，BIGINT；嵌套数值 CAST 保留 |

另外两条完整数值边界 SQL，均返回正确 BIGINT，并复跑稳定：

```sql
SELECT REGR_COUNT(y,x) AS n
FROM (VALUES (CAST(1e308 AS DOUBLE PRECISION),CAST(1e-300 AS DOUBLE PRECISION)),
             (-1e308,0),(NULL,1e308)) v(x,y);
-- 双端 [[2]]

SELECT REGR_COUNT(y,x) AS n
FROM (VALUES (CAST(-9223372036854775808 AS BIGINT),CAST(9223372036854775807 AS BIGINT)),
             (NULL,0)) v(x,y);
-- 双端 [[1]]
```

因此总共 **48 + 19 = 67** 条 REGR_COUNT 变体，**66 条完整通过、1 条外层 SUM 类型不同**；所有计数与重复执行稳定性通过。不是“67 条全部匹配”。19 条中的最终 ORDER BY 都以分组后的唯一 g 为键；不据一次顺序相同声称任意并列排序确定。

### 4.3 外层类型控制与直接相关负向

额外执行以下不含 REGR_COUNT 的控制（V 同样展开），双端数值都是三行 6，PG 仍 NUMERIC / Doris 仍 BIGINT，重复稳定：

```sql
SELECT SUM(n) OVER () AS total
FROM (SELECT g,COUNT(*) AS n FROM V GROUP BY g) c ORDER BY g;
```

这支持将外层 SUM(BIGINT) 类型问题复用到既有类型研究，不归为本轮计数改写新引入。未通过额外 CAST 修改原 Case 来制造匹配。

负向控制原文：

```sql
SELECT REGR_COUNT(CAST('bad' AS DOUBLE PRECISION),1) AS n;
```

本轮 PG 报 `InvalidTextRepresentation`、SQLSTATE **22P02**：`invalid input syntax for type double precision: "bad"`。工具粗分类为 PARSE_ERROR，但真实含义是非法输入转换，不是 SQL 语法未被识别。修改后转译为 UnsupportedError：`Doris REGR_COUNT requires two numeric columns or constants, optionally with numeric CASTs, without DISTINCT, ORDER BY, FILTER or OVER`，未执行 Doris。源端负向不计通过率，也不要求复制源异常全文。其他数值域溢出和 CAST 异常未做通用兼容承诺。

## 5. 原查询回归与单元测试

132 条/17 阶段回归、精确命令与解释器见[本轮汇总](../../../aggregates-001-fix-010-summary.md#3-输入与执行方式)。这次是在 fix-009 的 130 条基础上增加两条关联查询，之前 80 个匹配 ID 全部保持；新增匹配仅 0073。结果为 81 匹配、28 Doris 执行失败、18 行值/顺序不同、1 转译失败、4 源端负向。原 130 条的数量分布与前轮相同；不将加入新查询后的数量直接当同分母改善。

新增两方法：`test_regr_count` 包含 9 个生成/AST 不变/round-trip 形状；`test_regr_count_exclusions` 包含 11 个拒绝形状和 PostgreSQL 输出保持测试。补丁前先运行，当时 5 个正向形状与 11 个拒绝形状共 16 个子测试失败；补丁后和后加的 4 个正向形状均通过。具体排除：OVER、FILTER、DISTINCT、内部排序、缺参数、RANDOM、算术参数、字符串常量、字符串 CAST、非数值 CAST、占位符。不用这些拒绝案例声称目标已有相应可执行能力。

最终 PG/Doris/MySQL 156、全部方言 1079、核心 233 方法通过；Ruff check/format 与 diff 检查通过。未运行 make check、C/mypy/依赖 DuckDB 的全套测试，不伪称全仓测试已通过。

## 6. 验收与后续

全有效、任一 NULL、全 NULL、空输入、分组、重复行、显式 CAST、BIGINT 返回类型及已纳入的有限边界均有实际生成 SQL 和双端执行证据，task-009 可关闭约定范围。0544 的其他列、额外 SUM 类型控制及超范围表达式限制保留；没有新增未解决的既有匹配回归。

当前全批为 7 项完成约定验收、task-001/003 两项已修改但未完成验收；整份输入未完成。建议下一轮回到这两个现有任务的数组元素类型/完整类型验收，先确定安全规则再修改，不自动新建 task-010 或实施下一项。仍需最终全阶段回归与待研究/前提事项处理。代码未提交、未推送。
