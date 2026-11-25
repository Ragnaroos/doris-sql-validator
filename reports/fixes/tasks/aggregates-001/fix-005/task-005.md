# task-005：普通忽略 NULL 聚合的 FILTER 转换

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`4a3bd8ab312bda4c993c3b08e5806c14e4ae7f2e`。保存普通聚合FILTER规则及测试，不扩大为相关聚合或全部FILTER支持。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与范围

**已修复并完成普通聚合条件筛选规则的约定验收。** 本任务关闭 FILTER 的生成缺口，不宣称底层聚合、整数除法、类型、Collation、相关查询都已经跨库等价。168 条边界有 167 条行值一致；另 1 条已由无 FILTER 控制证明是原生 AVG 浮点尾差，仍记录不同，不伪造全部通过。

入口：[task-005](../../../../attribution/aggregates-001-attribution-summary.md#task-005)；共同身份/输入/权限与测试见[fix-005 汇总](../../../aggregates-001-fix-005-summary.md)。仅修改 sqlglot-experiment，保留前四轮未提交修改；没有 commit、push、Issue/PR、数据或验证框架改动。

实现覆盖普通 SUM、AVG、MIN、MAX、COUNT(expr)、COUNT(*)、ANY_VALUE 及单值 DISTINCT。排除窗口、内部 ORDER BY、有序集合、ARRAY_AGG、未知/自定义聚合、多参数或多值 DISTINCT；COUNT(t.*) 不冒充 COUNT(*)。不做相关聚合归属/查询级提升，不要求 Schema，也不修整数除法或 Collation。ANY_VALUE 仍允许任选非 NULL 值，不改成 MIN 来制造固定答案。

关联 8 条均在 stage-31、双端 dsv_wf_agg001_s31；每条原位置、出现序号和原 .out 见下文 Case 链接。只读查询限 10 秒、完整结果上限 10,000 行；本轮结果均未被截断。

## 2. 修复前证据与实现

2026-11-23 09:31:43 UTC，在当前累计 task-001 至 task-004 的代码上真实重跑，8 条 PG 成功，Doris 都拒绝 FILTER，典型错误：

```text
(1105, "errCode = 2, detailMessage = \nmismatched input '(' expecting {<EOF>, ';'}(line 1, pos 26)\n")
```

最小源文 `SELECT MIN(unique1) FILTER(WHERE unique1>100) FROM tenk1` 旧生成仍含 FILTER。新生成是 `SELECT MIN(IF(unique1>100,unique1,NULL)) FROM tenk1`；当前实际完整格式见第 3 节。

| 文件/方法 | 本轮修改 |
| :--- | :--- |
| sqlglot/generators/doris.py / DorisGenerator.filter_sql | 精确节点白名单，仅对已知忽略 NULL 的普通聚合调用公共 no_filter_sql；检查 Window 时遇 Select 停止，避免外层窗口误伤内层独立查询 |
| 同方法的 COUNT(*) 分支 | 在复制的 Count 中将星号换为 IF(predicate,1,NULL)，保留 Count 其他语义；不用公共 helper 会生成的 CountIf / COUNT_IF |
| no_filter_sql 调用 | 传入 expression.copy()，helper 只改副本；保留 DISTINCT 在参数外，条件包裹真正的输入值，不生成 IF(predicate,DISTINCT x,NULL) |
| tests/dialects/test_doris.py | 2 个新方法覆盖 6 类聚合、DISTINCT、COUNT(*)、FALSE/NULL、空输入、HAVING/分组/子查询、copy=False 输入 AST 不变及排除上下文 |

先加测试，在旧生成器上 2 个方法有 31 个失败断言；实施后定向与扩展测试通过。公共 no_filter_sql 本身没改，不影响其他目标方言；PG Parser、公共 AST、前四轮代码也未被重写。

[PostgreSQL FILTER 语义](https://www.postgresql.org/docs/18/sql-expressions.html) 只把条件为 TRUE 的行送入对应聚合，不是全局 WHERE。对忽略 NULL 的函数可把未入选行改成 NULL 参数，但 COUNT(*) 不能直接把星号放进 IF，保留 NULL 的 ARRAY_AGG 也不能盲用这个方案。[Doris ANY_VALUE](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/aggregate-functions/any-value/) 的非 NULL 选择约定支撑本轮白名单；它不承诺多种可选值时两端选择同一个。

未来保存代码时，本规则和测试应独立于数组等行为提交；当前未产生新 commit，完整累积 diff 不是本任务单独补丁。代码身份指纹见汇总。

## 3. 八条原查询及实际生成

09:33:27–09:33:28 UTC，SqlglotTranspiler.transpile_case 真正从原 SQL 生成，pg_probe.execute_query / compare_probe 分别读取两端，并各额外重复一次。随后 CliRunner 调用原 stage-31 YAML 的 run --stdout；最终整体回归又重跑本组。

原 .out 仍为主参考；本轮另将实时 PG 每列 CAST AS TEXT，与对应 .out 的完整显示行多重集合核对，8 条均相同。NULL 显示为空白的核对只是文本兼容证据，NULL 的实际值来自另外取得的实时结果，未无声替换基线。

```sql
-- pg-aggregates-0380-caa8b35c
select min(unique1) filter (where unique1 > 100) from tenk1;
-- 生成
SELECT MIN(IF(unique1 > 100, unique1, NULL)) FROM tenk1;

-- pg-aggregates-0381-b9be07f7
select sum(1/ten) filter (where ten > 0) from tenk1;
-- 生成
SELECT SUM(IF(ten > 0, 1 / ten, NULL)) FROM tenk1;

-- pg-aggregates-0382-9b691678
select ten, sum(distinct four) filter (where four::text ~ '123') from onek a
group by ten;
-- 生成
SELECT ten, SUM(DISTINCT IF(REGEXP(CAST(four AS STRING), '123'), four, NULL)) FROM onek AS a GROUP BY ten;

-- pg-aggregates-0383-ae4a4309
select ten, sum(distinct four) filter (where four > 10) from onek a
group by ten
having exists (select 1 from onek b where sum(distinct a.four) = b.four);
-- 生成
SELECT ten, SUM(DISTINCT IF(four > 10, four, NULL)) FROM onek AS a GROUP BY ten HAVING EXISTS(SELECT 1 FROM onek AS b WHERE SUM(DISTINCT a.four) = b.four);

-- pg-aggregates-0384-e4a241c8
select max(foo COLLATE "C") filter (where (bar collate "POSIX") > '0')
from (values ('a', 'b')) AS v(foo,bar);
-- 生成
SELECT MAX(IF((bar COLLATE `POSIX`) > '0', foo COLLATE `C`, NULL)) FROM (SELECT 'a' AS foo, 'b' AS bar) AS v;

-- pg-aggregates-0385-51f943b1
select any_value(v) filter (where v > 2) from (values (1), (2), (3)) as v (v);
-- 生成
SELECT ANY_VALUE(IF(v > 2, v, NULL)) FROM (SELECT 1 AS v UNION ALL SELECT 2 UNION ALL SELECT 3) AS v;

-- pg-aggregates-0390-d0eefd0f
select sum(unique1) FILTER (WHERE
  unique1 IN (SELECT unique1 FROM onek where unique1 < 100)) FROM tenk1;
-- 生成
SELECT SUM(IF(unique1 IN (SELECT unique1 FROM onek WHERE unique1 < 100), unique1, NULL)) FROM tenk1;

-- pg-aggregates-0392-17dd7649
select max(0) filter (where b1) from bool_test;
-- 生成
SELECT MAX(IF(b1, 0, NULL)) FROM bool_test;
```

| Case / 逐条归因 | CLI 结果 | 实时状态、行值、类型与剩余问题 |
| :--- | :--- | :--- |
| [0380](../../../../attribution/cases/aggregates-001/pg-aggregates-0380-caa8b35c.md) | 匹配 | 双端 1 列/1 行 101；int4 / int 声明一致 |
| [0381](../../../../attribution/cases/aggregates-001/pg-aggregates-0381-b9be07f7.md) | 行值或顺序不匹配 | 双端成功、各 1 列/1 行；PG 1000、int8；Doris 2828.968253968249、double。FILTER 已改写，整数 `/` 的独立差异未修，不强换 DIV |
| [0382](../../../../attribution/cases/aggregates-001/pg-aggregates-0382-9b691678.md) | 匹配 | 两端各 2 列/10 行，ten=0…9 的 SUM 均 SQL NULL；完整多重集合一致；int4/int、int8/bigint 一致 |
| [0383](../../../../attribution/cases/aggregates-001/pg-aggregates-0383-ae4a4309.md) | Doris 执行失败 | PG 2 列/5 行；Doris 报 `(1105, "errCode = 2, detailMessage = Unknown column 'four' in 'a' in FILTER clause(line 1, pos 137)")`。错误中的 FILTER 指内部计划，不是目标仍残留 SQL FILTER；目标字段/值未取得 |
| [0384](../../../../attribution/cases/aggregates-001/pg-aggregates-0384-e4a241c8.md) | 匹配 | 双端 1 列/1 行 a；text / varchar(1) 声明不同。样本通过不证明 C/POSIX 与 Doris 任意 Collation 等价 |
| [0385](../../../../attribution/cases/aggregates-001/pg-aggregates-0385-51f943b1.md) | 匹配 | 双端 1 列/1 行 3；int4 / tinyint 真正位宽不同。这里只有一个合格非 NULL 值，未强行规定一般 ANY_VALUE 的选择 |
| [0390](../../../../attribution/cases/aggregates-001/pg-aggregates-0390-d0eefd0f.md) | 匹配 | 双端 1 列/1 行 4950；int8 / bigint 一致，谓词的非相关 IN 子查询保留 |
| [0392](../../../../attribution/cases/aggregates-001/pg-aggregates-0392-17dd7649.md) | 匹配 | 双端 1 列/1 行 0；int4 / tinyint 真正位宽不同 |

8 条都没有最终 ORDER BY 或显式 Alias：默认列名不强比、结果行按多重集合保留重复次数，不凭返回顺序判错。7 条目标成功查询各自重复一次的值/重复次数稳定；PG 8 条也稳定。0383 重复仍失败，没有结果稳定性通过的结论。6 条 CLI 匹配中只有 3 条补证为当前原生类型声明也对齐，另 3 条类型不同不隐藏。

## 4. 156 条基础边界

09:34:14–09:34:25 UTC，在同一阶段执行；每条目标均由改后 SQLGlot 生成，两端各执行两次，不使用原 .out 给变体作答案。

完整生成规则为：

```sql
SELECT <函数>(<去重前缀>x) FILTER(WHERE <谓词>) AS v
FROM (VALUES <每行的 CAST 值>) t(x,p)<过滤条件>
```

函数为 SUM/AVG/MIN/MAX/COUNT/ANY_VALUE；去重前缀为空或 DISTINCT；谓词为 TRUE、FALSE、NULL、p。AVG 的 x 为 DOUBLE PRECISION，其余为 INT；所有 p 都 CAST AS BOOLEAN。每行分别为 `(CAST(<x或NULL> AS <类型>),CAST(<TRUE/FALSE/NULL> AS BOOLEAN))`。

| 输入组 | 具体 (x,p) | 过滤条件 | 每函数组合 |
| :--- | :--- | :--- | ---: |
| mixed | (2,TRUE),(2,TRUE),(NULL,TRUE),(99,FALSE),(77,NULL)；ANY_VALUE 的 99/77 换为 2，避免任选多个合法值的非确定性 | 无 | 8 |
| all-null | (NULL,TRUE),(NULL,FALSE) | 无 | 8 |
| empty | (2,TRUE) | WHERE FALSE | 8 |

6×24=144。另有 COUNT(*) 的同样 3 组×4 谓词=12：mixed 为 (2,TRUE),(NULL,TRUE),(99,FALSE),(77,NULL)，all-null/empty 同上；x 固定 CAST INT、NULL 谓词值明确为 BOOLEAN。合计 156，不将双端重复执行计为新变体。

最终：156 条双端成功、字段数/别名一致，原生类型对应 int4/int 72 次、int8/bigint 60 次、float8/double 24 次；每端重复稳定。155 条完整值一致，1 条不同，详见第 6 节。FALSE/NULL 不送入有效值；COUNT(*) 的 NULL 参数行仍可计数，COUNT(x) 忽略 NULL；全 NULL 和空输入 COUNT 为 0、其他受测函数为 SQL NULL；DISTINCT 保留正确去重语义。没有 AVG 或任意输入的全域等价声明。

## 5. 12 条上下文与类型边界

09:35:46–09:35:47 UTC，以下是完整源 SQL；同样从改后生成器生成、真实执行并各重复一次，不是手写 Doris 候选验收：

```sql
-- grouped
SELECT g, SUM(x) FILTER(WHERE p) AS s, COUNT(*) FILTER(WHERE p) AS c FROM (VALUES (CAST(1 AS INT),CAST(2 AS INT),TRUE),(CAST(1 AS INT),CAST(NULL AS INT),TRUE),(CAST(2 AS INT),CAST(8 AS INT),FALSE),(CAST(NULL AS INT),CAST(5 AS INT),CAST(NULL AS BOOLEAN))) t(g,x,p) GROUP BY g ORDER BY g;
-- grouped-empty
SELECT g, SUM(x) FILTER(WHERE p) AS s FROM (VALUES (CAST(1 AS INT),CAST(2 AS INT),TRUE)) t(g,x,p) WHERE FALSE GROUP BY g ORDER BY g;
-- having-empty
SELECT COUNT(*) FILTER(WHERE p) AS c FROM (VALUES (CAST(1 AS INT),TRUE)) t(x,p) WHERE FALSE HAVING COUNT(*) FILTER(WHERE p)=0;
-- scalar-empty
SELECT (SELECT SUM(x) FILTER(WHERE p) FROM (VALUES (CAST(1 AS INT),TRUE)) t(x,p) WHERE FALSE) AS s;
-- cte
WITH t(x,p) AS (VALUES (CAST(2 AS INT),TRUE),(CAST(99 AS INT),FALSE)) SELECT SUM(x) FILTER(WHERE p) AS s FROM t;
-- left-join
SELECT l.id, COUNT(r.x) FILTER(WHERE TRUE) AS c, COUNT(*) FILTER(WHERE r.x IS NULL) AS n FROM (VALUES (CAST(1 AS INT)),(CAST(2 AS INT))) l(id) LEFT JOIN (VALUES (CAST(1 AS INT),CAST(9 AS INT))) r(id,x) ON l.id=r.id GROUP BY l.id ORDER BY l.id;
-- predicate-subquery
SELECT SUM(x) FILTER(WHERE x IN (SELECT y FROM (VALUES (CAST(2 AS INT))) u(y))) AS s FROM (VALUES (CAST(2 AS INT)),(CAST(8 AS INT))) t(x);
-- protected-cast
SELECT SUM(CAST(x AS INT)) FILTER(WHERE p) AS s FROM (VALUES ('2',TRUE),('bad',FALSE),(NULL,TRUE)) t(x,p);
-- protected-division
SELECT SUM(CAST(12 AS DOUBLE PRECISION)/CAST(x AS DOUBLE PRECISION)) FILTER(WHERE x>0) AS s FROM (VALUES (CAST(0 AS INT)),(CAST(2 AS INT)),(CAST(3 AS INT))) t(x);
-- decimal-contract
SELECT CAST(SUM(x) FILTER(WHERE p) AS DECIMAL(18,2)) AS s FROM (VALUES (CAST(1.20 AS DECIMAL(10,2)),TRUE),(CAST(1.20 AS DECIMAL(10,2)),TRUE),(CAST(NULL AS DECIMAL(10,2)),TRUE),(CAST(99 AS DECIMAL(10,2)),FALSE)) t(x,p);
-- bigint-min
SELECT MIN(x) FILTER(WHERE p) AS m FROM (VALUES (CAST(9223372036854775807 AS BIGINT),TRUE),(CAST(-9223372036854775808 AS BIGINT),TRUE),(CAST(NULL AS BIGINT),TRUE)) t(x,p);
-- independent-filters
SELECT COUNT(*) FILTER(WHERE x>0) AS c, SUM(x) FILTER(WHERE x<0) AS s FROM (VALUES (CAST(2 AS INT)),(CAST(2 AS INT)),(CAST(-3 AS INT)),(CAST(NULL AS INT))) t(x);
```

12 条的状态、字段数/显式别名、行数、完整值/重复次数一致；重复稳定。grouped 为 `(1,2,2),(2,NULL,0),(NULL,NULL,0)`；grouped-empty 0 行；having-empty 为 0、scalar-empty SQL NULL；LEFT JOIN 为 `(1,1,0),(2,0,1)`，没有把未匹配行的 COUNT(expr) 错计为 COUNT(*)。CAST 被保护结果 2；除零所在行未贡献，结果 DOUBLE 10；Decimal 两侧精确 2.40，取得 Precision=18、Scale=2；BIGINT 最小值 -9223372036854775808；独立 FILTER 得 `(2,-3)`。

有最终 ORDER BY 的分组/连接实际逐行一致，输出键在对应分组结果中唯一；其他按多重集合。整数和 Double 的逻辑/声明类型对齐。Decimal 在工具中仍显示 numeric / decimalv3(18,2) 名称不同，但源实际返回精度/小数位与目标均为 18/2，符合本变体源 SQL 的显式契约；不能推广为无界 NUMERIC 都等价。没有放宽比较规则，工具名称差异仍保留。

目标采用 `SUM(IF(p,CAST(x AS INT),NULL))`、`SUM(IF(x>0,CAST(12 AS DOUBLE)/CAST(x AS DOUBLE),NULL))` 等形式，把保护条件放在参数求值路径中；没有把 CASE 放在聚合结果外来掩盖预先求值。当前 Doris strict_cast=false，本例成功不证明所有严格异常策略都相同。

## 6. AVG 尾差：不是 FILTER 引入，也没有被消除

失败变体为：

```sql
SELECT AVG(DISTINCT x) FILTER(WHERE TRUE) AS v FROM (VALUES (CAST(2 AS DOUBLE PRECISION)),(CAST(2 AS DOUBLE PRECISION)),(CAST(NULL AS DOUBLE PRECISION)),(CAST(99 AS DOUBLE PRECISION)),(CAST(77 AS DOUBLE PRECISION))) t(x);
-- 生成
SELECT AVG(DISTINCT IF(TRUE, x, NULL)) AS v FROM (SELECT CAST(2 AS DOUBLE) AS x UNION ALL SELECT CAST(2 AS DOUBLE) UNION ALL SELECT CAST(NULL AS DOUBLE) UNION ALL SELECT CAST(99 AS DOUBLE) UNION ALL SELECT CAST(77 AS DOUBLE)) AS t;
-- 独立控制的源文：移除 FILTER，其他值和类型不变
SELECT AVG(DISTINCT x) AS v FROM (VALUES (CAST(2 AS DOUBLE PRECISION)),(CAST(2 AS DOUBLE PRECISION)),(CAST(NULL AS DOUBLE PRECISION)),(CAST(99 AS DOUBLE PRECISION)),(CAST(77 AS DOUBLE PRECISION))) t(x);
-- 控制的真实生成
SELECT AVG(DISTINCT x) AS v FROM (SELECT CAST(2 AS DOUBLE) AS x UNION ALL SELECT CAST(2 AS DOUBLE) UNION ALL SELECT CAST(NULL AS DOUBLE) UNION ALL SELECT CAST(99 AS DOUBLE) UNION ALL SELECT CAST(77 AS DOUBLE)) AS t;
```

两种源 SQL 的当前文本驱动读取都是 59.3333333333333，PG `cursor(binary=True)` 实际都是 59.333333333333336；两种 Doris SQL 都是 59.33333333333334，返回声明均 Double。二进制补证只读、10 秒超时，没有改变原 Session 政策或源基线。

因此包含两层差异：extra_float_digits=0 的显示舍入，以及二进制 PG/Doris 之间仍存在的真实尾差。带与不带 FILTER 在各自引擎结果相同，已证明本例不是 FILTER 新引入；不因此宣称原生 AVG 全域同义或尾差可忽略。精确比较仍判不同，未加容差、未硬编码答案。复用现有原生聚合精度研究，任务验收仅关闭条件筛选规则。

## 7. 测试、扩大回归与去向

新增 2 个方法的方向/排除断言通过；PG/Doris/MySQL 145、全部方言 1,068、所选核心 233 个方法通过，145 已包含在 1,068 中。最后 copy=False 断言另跑 2 个方法通过；完整命令、lint 和未运行项见汇总。

最终 91 条原查询、16 阶段的 run --stdout：71 匹配、9 目标执行失败、7 行值/顺序差异、4 源端负向。此前 65 条匹配无回归；本任务新取得 6 条 .out 匹配。四个相关查询 0387/0388/0393 报 `access outer query's column in aggregate is not supported`，0389 报外层列解析失败；只有表达式条件改写，没有实现 PG 聚合归属，因此不称相关查询已修。原 0383 的剩余错误同类研究，不把一次失败说成 Doris 永远不可模拟。

0394–0397 的 .out 本就报 `aggregate functions are not allowed in FILTER` 或 `aggregate function calls cannot be nested`；当前目标也失败，仍默认不归因，不进行报错逐字复制，不生成新负向 Case 报告。本轮对相关四条仅跑 Recorded Output 目标回归，没有重新取得实时 PG 的完整类型/边界证据。

168 个新边界没有覆盖任意数据/Collation、未知 UDF、窗口、有序集合、一般 ANY_VALUE 多种可选值、全部 NUMERIC/浮点算法或相关查询级重写。原 .out 六条匹配不证明其原生类型全部相同。当前唯一任务清单保留类型/浮点/相关研究，不改历史首轮数量或前轮报告。

下一项建议 task-006（EVERY），尚未实施；本任务与其他任务不因同文件而捆绑提交。整份输入未完成。
