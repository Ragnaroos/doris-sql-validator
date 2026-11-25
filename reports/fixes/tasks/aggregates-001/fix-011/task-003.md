# task-003：ARRAY_AGG 类型核验（fix-011）

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`d0fcf8f16af727bcfac9993792fa2c9a1be2b766`。保存既有NULL/空输入规则；本轮类型补证本身没有额外代码提交，本task仍未完成类型/精度验收。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 当前结论

**仍为“已修改但未完成验收”。** NULL保留与空输入返回SQL NULL的既有实现不变；22条边界已重新执行并取得数组元素OID/typmod。19条的已有元素类型/标量类型可映射，2条Decimal结果精度声明仍不能判相等，1条TIMESTAMP真实丢微秒。结合值/顺序，18条固定输入可完成本次已取得维度核对；另有DISTINCT无内部排序的实际数组顺序差异，不能偷偷排序成MATCH。

入口沿用[task-003](../../../../attribution/aggregates-001-attribution-summary.md#task-003)，[fix-003](../fix-003/task-003.md)保留。共同代码身份、授权、执行入口、142 条原查询回归和测试见[本轮汇总](../../../aggregates-001-fix-011-summary.md)。本轮继续使用 HEAD 089891f2521780e2c5b243005017af9db62f25a6 和前十轮未提交修改，累积 diff SHA256 为 444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18，**本轮没有修改 SQLGlot 代码、框架或数据，未 commit/push**。

## 2. 二十二条边界的类型补证

完整源SQL及既有NULL/空输入规则见[原报告第5节](../fix-003/task-003.md#5-22-组固定边界)。本轮从相同源SQL重新调用当前生成器，实际普通目标仍为 `NULLIF(ARRAY_AGG(a), ARRAY())`，DISTINCT不删除，源CAST不改，绝非重放手写候选。补查 `pg_type.typelem`、`cursor.pgresult.fmod(i)` 和字段描述，目标类型由EXPLAIN VERBOSE取得；双端各重复一次，22条均成功且端内稳定。10秒/10000行限制，无截断。

| 既有边界 | PostgreSQL 原生类型/协议 typmod | Doris实际类型 | 本轮判断 |
| :--- | :--- | :--- | :--- |
| int-mixed | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| int-all-null | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| int-empty | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| distinct-mixed | _int4; typmod=-1 | array<int> | INT32 类型对齐；无聚合内排序，实际元素顺序不同 |
| distinct-all-null | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| distinct-empty | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| bigint-boundary | _int8; typmod=-1 | array<bigint> | 本次类型约束及值对齐 |
| decimal | _numeric; typmod=-1 | array<decimalv3(10,2)> | 源 typmod=-1 / 目标 DECIMAL(10,2)；精度声明不能判相等 |
| decimal-empty | _numeric; typmod=-1 | array<decimalv3(10,2)> | 源 typmod=-1 / 目标 DECIMAL(10,2)；精度声明不能判相等 |
| string-unicode | _text; typmod=-1 | array<text> | 本次类型约束及值对齐 |
| bool | _bool; typmod=-1 | array<boolean> | BOOLEAN 类型对齐；1/0 显示差异经标量补证确认 |
| float | _float8; typmod=-1 | array<double> | 本次类型约束及值对齐 |
| date | _date; typmod=-1 | array<datev2> | 本次类型约束及值对齐 |
| timestamp | _timestamp; typmod=-1 | array<datetimev2(0)> | 真实微秒丢失，独立 TIMESTAMP 转换问题 |
| grouped | int4; typmod=-1 / _int4; typmod=-1 | int / array<int> | 本次类型约束及值对齐 |
| grouped-empty | int4; typmod=-1 / _int4; typmod=-1 | int / array<int> | 本次类型约束及值对齐 |
| left-join | int4; typmod=-1 / _int4; typmod=-1 | int / array<int> | 本次类型约束及值对齐 |
| scalar-empty | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| scalar-mixed | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| having-empty | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| having-all-null | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| multiple | _int4; typmod=-1 / _int4; typmod=-1 / int8; typmod=-1 | array<int> / array<int> / bigint | 本次类型约束及值对齐 |

类型别名只按实际结构补证，不改框架。例如_int4与ARRAY<INT>是INT32元素映射，而_int4与ARRAY<TINYINT>不相同。行顺序规则仍按原比较策略，数组元素从不默认重排。具有最终ORDER BY的分组和JOIN样本使用明确唯一的分组键/id。

22条中原工具的结构化值比较仍为19条一致、3条不同；其中bool差异经下节原生标量补证，timestamp是真差异，distinct-mixed保留实际未规定的元素顺序差异。Decimal两条当前值相同，但精度声明不足以验收，不能从“数组精度不适用”偷换成“通过”。

BIGINT边界另外以Python原生读取确认为 `[([9223372036854775807, None, -9223372036854775808],)]`，与Doris文本逐位一致；不是展示层Number舍入后的数字。

## 3. 原代表0287：问题发生在聚合之前

原源SQL不变：

~~~sql
SELECT ARRAY_AGG(DISTINCT a)
FROM (VALUES (1),(2),(1),(3),(NULL),(2)) v(a);
~~~

当前实际生成：

~~~sql
SELECT NULLIF(ARRAY_AGG(DISTINCT a), ARRAY()) FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT 1 UNION ALL SELECT 3 UNION ALL SELECT NULL UNION ALL SELECT 2) AS v
~~~

PG为_int4，Doris为ARRAY<TINYINT>；本轮元素顺序和值恰好均为[1,2,3,NULL]，但类型仍不同，原 .out 文本也仍不匹配。

只读去除聚合的控制：

~~~sql
-- PG：int4
SELECT a FROM (VALUES (1),(2),(NULL)) v(a);
-- 当前实际生成的Doris：tinyint
SELECT a FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT NULL) AS v;
~~~

两端行值均1、2、NULL，说明此类位宽差异在输入VALUES求型时已经存在，不是ARRAY_AGG的NULLIF新增了TINYINT。裸 `SELECT 1 AS x` 也为PG int4 / Doris tinyint；全NULL的VALUES列则为PG text / Doris null_type。复用现有共同类型研究，不靠再改函数名掩盖根因。

额外独立候选（不是修复后生成器）已实际执行：

~~~sql
SELECT CAST(NULLIF(ARRAY_AGG(DISTINCT a), ARRAY()) AS ARRAY<INT>) AS xs
FROM (SELECT 1 AS a UNION ALL SELECT 2 UNION ALL SELECT NULL UNION ALL SELECT 1) AS v;
~~~

得到ARRAY<INT>、[1,2,NULL]，本次类型和值可对齐，说明目标有可用表达，不等于已实现默认转换。后续应从可靠源类型生成CAST，而不是给所有聚合强制INT。

### 3.1 不强制Schema也不等于当前标注已能直接用

无Schema的 `qualify` 后再 `annotate_types`，确实能把这个VALUES查询的ARRAY_AGG标成ARRAY<INT>；仅直接标注未限定列的原查询则为UNKNOWN。但当前Generator即使拿到标注，也仍输出原数组类型，没有自动插入保真CAST。

此外通用标注对ARRAY[1.25,2]给DOUBLE、对ARRAY[NULL]给NULL，和本轮PG真实NUMERIC/TEXT不同。因此不能把“这个INT例子推断出来了”推广为PG共同类型规则已实现。没有在框架中加Schema、偷偷执行qualify或用手工标注后的成功冒充默认链路成功。

## 4. Decimal、Boolean、TIMESTAMP与顺序的明确去向

### 4.1 Decimal：协议没有返回约束，不是统一的驱动丢失

两条Decimal聚合的源为OID1231、typelem1700、typmod=-1，目标为ARRAY<DECIMALV3(10,2)>。源参数有CAST(10,2)，但不能据此冒充结果协议也声明了(10,2)。对照task-001的直接同型CAST数组，本轮确实读到了typmod655366/precision10/scale2，说明工具并非一律拿不到数组精度。

当前有限输入值精确相同，空输入同为SQL NULL；结果类型声明仍不能直接判等。PQfmod=-1的解释见[官方文档](https://www.postgresql.org/docs/18/libpq-exec.html)。本轮只补证，不把当前有界值相同当作源NUMERIC所有值域都被固定Decimal覆盖；也不虚构“只要改SQLGlot就能让任意精度变成相同原生类型”。

### 4.2 Boolean：当前样本是表示差异

源_bool/typelem16，目标ARRAY<BOOLEAN>，元素类型已对齐。源数组true/NULL/false，Doris驱动数组文本1/NULL/0。另执行原生Doris1-based下标标量投影，双端三列BOOL/BOOLEAN，值true/NULL/false与1/NULL/0经已有标量布尔比较一致。

诊断目标SQL：

~~~sql
SELECT CAST(xs[1] AS BOOLEAN) AS b1, CAST(xs[2] AS BOOLEAN) AS b2, CAST(xs[3] AS BOOLEAN) AS b3
FROM (SELECT NULLIF(ARRAY_AGG(a), ARRAY()) AS xs
      FROM (SELECT CAST(TRUE AS BOOLEAN) AS a
            UNION ALL SELECT CAST(NULL AS BOOLEAN)
            UNION ALL SELECT CAST(FALSE AS BOOLEAN)) AS v) AS s;
~~~

这不是默认生成器验收。相同源下标当前实际生成0、1、2，本诊断明确改用原生1、2、3，不能据其通过声称下标转换也已修复。未修改Comparator或SQLGlot；数组布尔表示和下标分别沿用已有框架/索引研究。

### 4.3 TIMESTAMP：真实值丢失，独立于ARRAY_AGG

原边界的 .123456 被生成DATETIME(0)后丢失。额外无聚合控制也复现：

~~~sql
-- PG结果2024-02-29T12:34:56.123456
SELECT CAST('2024-02-29 12:34:56.123456' AS TIMESTAMP) AS x;
-- 当前实际生成，Doris结果2024-02-29T12:34:56
SELECT CAST('2024-02-29 12:34:56.123456' AS DATETIME) AS x;
~~~

因此仍复用已有时间精度研究，不把它归为NULL聚合规则错误，也不声称只缺一个类型别名。PG未指定精度仍可以保留本例六位小数；[官方时间类型说明](https://www.postgresql.org/docs/18/datatype-datetime.html)介绍其精度范围。本轮不擅自改通用TIMESTAMP映射。

### 4.4 DISTINCT无内部ORDER BY

原distinct-mixed的PG为[1,2,NULL]、Doris为[1,NULL,2]，INT32元素类型相同。本轮重复稳定，但SQL没有保证数组内部顺序；保留原比较不同，不为制造MATCH手工排序或修改比较器。有明确内部排序的task-004样本另按原规则回归。

## 5. 十条原查询的现状

| Case / stage | 原 .out 规则的实际结果 | PG / Doris 原生类型 | 具体限制 |
| :--- | :--- | :--- | :--- |
| [0276](../../../../attribution/cases/aggregates-001/pg-aggregates-0276-0f1f5154.md) / 17 | Doris 执行失败 | _text / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nEvery derived table must have its own alias(line 1, pos 53)\n\n== SQL ==\nSELECT NULLIF(ARRAY_AGG(DISTINCT val), ARRAY()) FROM (SELECT NULL AS val FROM (SELECT CAST(1 + number * 1 AS INT) AS generate_series FROM NUMBERS('number' = '2')) AS generate_series)\n-----------------------------------------------------^^^\n") |
| [0283](../../../../attribution/cases/aggregates-001/pg-aggregates-0283-9ca01715.md) / 17 | Doris 执行失败 | _int4 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = collect_list doesn't support order by expression") |
| [0284](../../../../attribution/cases/aggregates-001/pg-aggregates-0284-628b13e2.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0285](../../../../attribution/cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0286](../../../../attribution/cases/aggregates-001/pg-aggregates-0286-c689f198.md) / 17 | Doris 执行失败 | _int4 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = collect_list doesn't support order by expression") |
| [0287](../../../../attribution/cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0288](../../../../attribution/cases/aggregates-001/pg-aggregates-0288-1528b423.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0289](../../../../attribution/cases/aggregates-001/pg-aggregates-0289-64071a98.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0290](../../../../attribution/cases/aggregates-001/pg-aggregates-0290-2bc98abf.md) / 17 | 行值或顺序不匹配 | _int4 / array<tinyint> | 值/表示及类型需分别看下文 |
| [0371](../../../../attribution/cases/aggregates-001/pg-aggregates-0371-e4fde69d.md) / 30 | Doris 执行失败 | text / 无成功目标字段 | (1105, "errCode = 2, detailMessage = Unknown column 's' in 'table list' in PROJECT clause(line 1, pos 35)") |

合计6条显示/值差异、4条Doris失败。六条双端成功查询均为PG int4[] / Doris ARRAY<TINYINT>，当前值及已要求的排序已取得对应证据，类型仍未对齐；不能据原 .out 看不见类型就放行。

0276当前首先是无别名派生表，不能继续沿用早期“序列函数不支持”作为当前错误；0283/0286仍为不同键内部排序，0371仍为整行引用/ARRAY_DIMS。真实错误如上，不把失败归为类型已通过。全部10条当前PG文本与原 .out 一致，没有替换源参考。

## 6. 沿用原任务的验收子项

| 具体子项 | 当前结论 | 后续要求 |
| :--- | :--- | :--- |
| 显式INT/BIGINT/FLOAT/DATE/BOOLEAN元素映射 | 已有实际类型证据 | 保持NULL、全NULL、空输入、重复、GROUP BY/HAVING/子查询回归；Boolean原比较误判不在本轮改框架 |
| VALUES裸值进入数组聚合的源类型保留 | 未完成，0287等真位宽差异保留 | 追溯可信源共同类型，缺类型时不猜；不能对所有ARRAY_AGG硬CAST INT |
| Decimal结果精度契约 | 已补到协议层，仍不能直接判相等 | 区分源参数约束、源结果声明与目标固定精度；不能只看顶层数组“不适用” |
| DISTINCT未保证的元素顺序 | 原差异保留 | 不从重复稳定推出全计划顺序；不改原规则 |
| TIMESTAMP/下标/别名/不同键排序/整行引用 | 独立问题的证据保留 | 沿用已有研究或前提项，不混入NULL/空输入规则 |

本轮没有安全通用类型规则可直接验收，因此未增加补丁或声称修复完成。仍保持“已修改但未完成验收”，而非为关闭任务重新缩小原承诺。建议先在原task内落实可证明源类型的保真转换；超出范围的共享类型/时间/框架改动另行授权。

