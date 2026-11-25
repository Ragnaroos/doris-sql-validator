# task-001：混合数组的 PostgreSQL 整数/布尔输入转换（fix-013）

## 1. 结论与本轮范围

状态：**已修改但未完成验收**。本轮继续原 [task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，不是新task。已实际补齐“unknown字符串 + 已知整数/布尔类型”的有限输入转换，以及显式数组CAST对这些unknown元素的类型约束；不把所有字符串都转数字，不要求Schema。

这里的 unknown 指PostgreSQL中尚待上下文确定类型的字符串字面量，不是“数据库列类型未知”。上一轮反例 `ARRAY['1',2]` 现在生成 `CAST(ARRAY(CAST('1' AS INT),2) AS ARRAY<INT>)`，本次元素值[1,2]和INT32类型均对齐。新规则支持SMALLINT/INT/BIGINT的符号、ASCII首尾空白、合法下划线及二/八/十六进制字符串，并按源目标位宽检查范围；Boolean按源支持的拼写、唯一前缀和大小写规范化。纯字符串数组仍是TEXT，保留“01”等原文。

| 范围 | 本轮实际结果 |
| :--- | :--- |
| 97条成功源边界 | 37条前轮边界 + 24条混合整数 + 22条混合Boolean + 6条上下文 + 8条显式外层CAST；双端均成功、每端重复一次均稳定 |
| 上述97条的现有结构化值比较 | 74条一致、23条Boolean显示不同；其中22条新增Boolean另外取得原生标量Boolean投影，状态/类型/元素值一致。原比较不同仍保留，不改框架 |
| 21条直接相关非法输入 | PG全部实际报错；当前RAISE生成全部明确unsupported，不执行目标。默认不进入主修复范围，不算成功匹配 |
| 15组NUMERIC/Float补查 | 15条源成功；9条当前值相同、5条值不同、1条源合法但SQLGlot Parser拒绝。与97条有重复SQL，不能相加当唯一查询数 |
| 原14条关联Case | 原.out仍3匹配、1显示差异、9 Doris失败、1转译拒绝；实时源文本均与原.out相同 |
| 原142条回归 | 19阶段，逐ID与fix-012完全不变，82条匹配保持，无新增结果回归 |

上一轮见 [fix-012](../fix-012/task-001.md)，共同身份与测试见[本轮汇总](../../../aggregates-001-fix-013-summary.md)。本轮不修task-003、比较器、DDL/数据、通用CAST、未知列类型传播、任意浮点输入或NUMERIC全域。指定任务模式，不commit/push，不创建社区Issue/PR。

## 2. 代码依据与实现

| 代码/测试 | 本轮改动 | 安全条件 |
| :--- | :--- | :--- |
| [parsers/postgres.py](../../../../../../sqlglot-experiment/sqlglot/parsers/postgres.py) / _array_element_type | 允许unknown字符串与已知整数/Boolean共同求型；Float/NUMERIC混合文本不猜；错误收集阶段的Cast.to为空时不崩溃 | 字符串不能决定把INT提升为BIGINT；选型由已知输入/显式构造CAST决定 |
| [generators/doris.py](../../../../../../sqlglot-experiment/sqlglot/generators/doris.py) / _coerce_array_input | 在构造ARRAY前显式转换unknown字面量。整数先验证PG输入文法、规范化为十进制文本，再CAST到相应整数；Boolean转为规范true/false文本再CAST | 不把非PG数组、纯TEXT、未知列或一般函数当unknown字面量；NULL仍运行时处理，不返回固定NULL答案 |
| 同文件 / cast_sql、_array_cast_types | 源显式数组CAST优先于构造器临时推断；对直接括号/嵌套构造器沿对应数组类型传播，使用副本，不跨Subquery或内层独立CAST | 不先将2147483648强转INT，不将外层TEXT中的01提前变成1；未支持的显式元素类型清除临时提示，保留原生成路径，不冒称实现通用CAST |
| tests/dialects/test_doris.py / test_postgres_array_unknown_inputs | 完整生成SQL、整数输入格式/边界、Boolean、显式CAST、嵌套、AST不变性、非法输入防静默NULL、非PG不改；5000个前导0单元反例 | 子查询/内层INT CAST失败不能因外层BIGINT而被偷偷放宽 |
| tests/dialects/test_postgres.py / test_array_element_type_contract | 确认收集模式下未支持的NUMERIC负Scale保留ParseError，而不是辅助推型AttributeError | 修正内部崩溃不等于实现负Scale语法 |

整数文法和边界根据 [PostgreSQL 18 numutils.c](https://github.com/postgres/postgres/blob/REL_18_STABLE/src/backend/utils/adt/numutils.c)并实测；Boolean依据 [PG布尔输入规则](https://www.postgresql.org/docs/18/datatype-boolean.html)；共同类型依据 [PG类型解析规则](https://www.postgresql.org/docs/18/typeconv-union-case.html)。只规范化字面量输入文法，不在Python计算整条查询或按Case答案特判。

长整数文本先去掉前导0，再按可表示位数限制解析长度，避免Python十进制转换长度限制。超过相应有符号范围或文法非法时明确unsupported，不能让Doris宽松CAST把源失败输入悄悄变成NULL/舍入整数。RAISE模式错误为：

~~~text
UnsupportedError: Doris cannot preserve this PostgreSQL array input conversion
~~~

### 修复前后的关键例子

~~~sql
-- PG源；fix-012目标为ARRAY('1',2)，元素变成字符串
SELECT ARRAY['1',2] AS value;
-- 本轮真实生成（Doris保留原别名引用）
SELECT CAST(ARRAY(CAST('1' AS INT), 2) AS ARRAY<INT>) AS `value`;

-- PG支持整数文本0x7f；不能直接依赖Doris CAST('0x7f' AS INT)
SELECT ARRAY['0x7f',1] AS xs;
-- 本轮规则生成
SELECT CAST(ARRAY(CAST('127' AS INT), 1) AS ARRAY<INT>) AS xs;
~~~

上面的0x7f是完整规则的简写例子；下表保留实际执行的各条带NULL/重复元素的SQL，不能拿简写冒充另一次数据库执行。

显式CAST必须优先：实际PG `ARRAY['2147483648',1]::BIGINT[]` 成功，`ARRAY['01',1]::TEXT[]` 保留“01”。初始实现若先用INT共同类型会误拒绝前者、改坏后者；本轮取证后已修正并加回归，不掩盖失败尝试。

## 3. 实际执行方法与比较维度

工作流根目录，解释器/PYTHONPATH见本轮汇总。边界使用 `parse_one(source, read='postgres').sql('doris', unsupported_level=ErrorLevel.RAISE)`，原Case使用 `SqlglotTranspiler.transpile_case`；目标均来自实际修改后代码，随后 `pg_probe.execute_query / compare_probe`，单次10秒/10000行，97条双端各两次。

比较状态、字段数量/显式别名、已取得原生类型、行数、值、重复次数及必要顺序。整数按元素OID映射INT2→SMALLINT、INT4→INT、INT8→BIGINT，不因字符串名称不同判缺陷；数组元素顺序不变。没有ORDER BY时结果行按多重集合保留重复次数；runtime-null-order显式CAST的id为1/2/3，唯一并保持最终顺序。旧边界独立id位宽和NUMERIC约束余项仍保留。

Boolean原结果保持报告中的不同：源数组为布尔值，Doris协议显示0/1。22条新增用例另执行 `SELECT xs[1] AS c1,...,xs[4] AS c4 FROM (<原源SQL/实际生成SQL>) p`，各端按本端原生1-based下标取回所有四个Boolean字段；类型BOOL/BOOLEAN及本次四个元素值一致。这是绑定实际生成数组的表示诊断，不是手写候选替换目标，也不代表修复SQLGlot的下标转换。未放宽框架规则；旧Boolean边界另1条本轮只保留原结果，不借用这22条投影的证据。

BIGINT结果在Python内比较后用repr字符串展示，避免JavaScript把9223372036854775807舍入。本轮没有创建执行JSON、候选SQL、脚本、日志或evidence目录。初次终端截断后补取，并在最终代码下完整重跑97条，以下数据以最终批次为准，不把重试当新增Case。

### 3.1 前轮37条与本轮60条扩展

前37条完整SQL见 [fix-012第4节](../fix-012/task-001.md#4-37条边界与未通过项)；本轮原样重跑，不重复抄写。原36号混合字符串反例已修正，其他36条按现有值比较结论不变。现在37条为36值一致、1条Boolean显示不同；独立id位宽、Decimal结果声明、NUMERIC/LARGEINT类型余项仍保留，不把值相同当全部类型验收。

| 编号 | 完整源 SQL | 修改后实际生成并执行的 Doris SQL | 本次已取得原生类型 | 观察 |
| :--- | :--- | :--- | :--- | :--- |
| integer-1 | `` SELECT ARRAY[1,'1',NULL,'1'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('1' AS INT), NULL, CAST('1' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-2 | `` SELECT ARRAY[1,'+1',NULL,'+1'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('1' AS INT), NULL, CAST('1' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-3 | `` SELECT ARRAY[1,'-1',NULL,'-1'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('-1' AS INT), NULL, CAST('-1' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-4 | `` SELECT ARRAY[1,'  +01 ',NULL,'  +01 '] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('1' AS INT), NULL, CAST('1' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-5 | `` SELECT ARRAY[1,'1_000',NULL,'1_000'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('1000' AS INT), NULL, CAST('1000' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-6 | `` SELECT ARRAY[1,'0x7f',NULL,'0x7f'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('127' AS INT), NULL, CAST('127' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-7 | `` SELECT ARRAY[1,'-0x80',NULL,'-0x80'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('-128' AS INT), NULL, CAST('-128' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-8 | `` SELECT ARRAY[1,'0X_7_F',NULL,'0X_7_F'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('127' AS INT), NULL, CAST('127' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-9 | `` SELECT ARRAY[1,'0o17',NULL,'0o17'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('15' AS INT), NULL, CAST('15' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-10 | `` SELECT ARRAY[1,'0b101',NULL,'0b101'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('5' AS INT), NULL, CAST('5' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-11 | `` SELECT ARRAY[1,'0B_1_0',NULL,'0B_1_0'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('2' AS INT), NULL, CAST('2' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-12 | `` SELECT ARRAY[1,'-0',NULL,'-0'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('0' AS INT), NULL, CAST('0' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-13 | `` SELECT ARRAY[1,' +0x7f ',NULL,' +0x7f '] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('127' AS INT), NULL, CAST('127' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-14 | `` SELECT ARRAY[1,'2147483647',NULL,'2147483647'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('2147483647' AS INT), NULL, CAST('2147483647' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| integer-15 | `` SELECT ARRAY[1,'-2147483648',NULL,'-2147483648'] AS xs `` | `` SELECT CAST(ARRAY(1, CAST('-2147483648' AS INT), NULL, CAST('-2147483648' AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| SMALLINT-1 | `` SELECT ARRAY[CAST(1 AS SMALLINT),'32767',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS SMALLINT), CAST('32767' AS SMALLINT), NULL) AS ARRAY<SMALLINT>) AS xs `` | `` _int2 → array<smallint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| SMALLINT-2 | `` SELECT ARRAY[CAST(1 AS SMALLINT),'-32768',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS SMALLINT), CAST('-32768' AS SMALLINT), NULL) AS ARRAY<SMALLINT>) AS xs `` | `` _int2 → array<smallint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| SMALLINT-3 | `` SELECT ARRAY[CAST(1 AS SMALLINT),'0x7fff',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS SMALLINT), CAST('32767' AS SMALLINT), NULL) AS ARRAY<SMALLINT>) AS xs `` | `` _int2 → array<smallint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| SMALLINT-4 | `` SELECT ARRAY[CAST(1 AS SMALLINT),'-0x8000',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS SMALLINT), CAST('-32768' AS SMALLINT), NULL) AS ARRAY<SMALLINT>) AS xs `` | `` _int2 → array<smallint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| BIGINT-1 | `` SELECT ARRAY[CAST(1 AS BIGINT),'2147483648',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST('2147483648' AS BIGINT), NULL) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| BIGINT-2 | `` SELECT ARRAY[CAST(1 AS BIGINT),'9223372036854775807',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST('9223372036854775807' AS BIGINT), NULL) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| BIGINT-3 | `` SELECT ARRAY[CAST(1 AS BIGINT),'-9223372036854775808',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST('-9223372036854775808' AS BIGINT), NULL) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| BIGINT-4 | `` SELECT ARRAY[CAST(1 AS BIGINT),'0x7fff_ffff_ffff_ffff',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST('9223372036854775807' AS BIGINT), NULL) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| BIGINT-5 | `` SELECT ARRAY[CAST(1 AS BIGINT),'-0x8000_0000_0000_0000',NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST(1 AS BIGINT), CAST('-9223372036854775808' AS BIGINT), NULL) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| boolean-1 | `` SELECT ARRAY[FALSE,'true',NULL,'true'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-2 | `` SELECT ARRAY[FALSE,'t',NULL,'t'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-3 | `` SELECT ARRAY[FALSE,'tr',NULL,'tr'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-4 | `` SELECT ARRAY[FALSE,'tru',NULL,'tru'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-5 | `` SELECT ARRAY[FALSE,'yes',NULL,'yes'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-6 | `` SELECT ARRAY[FALSE,'y',NULL,'y'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-7 | `` SELECT ARRAY[FALSE,'ye',NULL,'ye'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-8 | `` SELECT ARRAY[FALSE,'on',NULL,'on'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-9 | `` SELECT ARRAY[FALSE,'1',NULL,'1'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-10 | `` SELECT ARRAY[FALSE,'false',NULL,'false'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-11 | `` SELECT ARRAY[FALSE,'f',NULL,'f'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-12 | `` SELECT ARRAY[FALSE,'fa',NULL,'fa'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-13 | `` SELECT ARRAY[FALSE,'fal',NULL,'fal'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-14 | `` SELECT ARRAY[FALSE,'fals',NULL,'fals'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-15 | `` SELECT ARRAY[FALSE,'no',NULL,'no'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-16 | `` SELECT ARRAY[FALSE,'n',NULL,'n'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-17 | `` SELECT ARRAY[FALSE,'off',NULL,'off'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-18 | `` SELECT ARRAY[FALSE,'of',NULL,'of'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-19 | `` SELECT ARRAY[FALSE,'0',NULL,'0'] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-20 | `` SELECT ARRAY[FALSE,' TrUe ',NULL,' TrUe '] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-21 | `` SELECT ARRAY[FALSE,' YES ',NULL,' YES '] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('true' AS BOOLEAN), NULL, CAST('true' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| boolean-22 | `` SELECT ARRAY[FALSE,' oFf ',NULL,' oFf '] AS xs `` | `` SELECT CAST(ARRAY(FALSE, CAST('false' AS BOOLEAN), NULL, CAST('false' AS BOOLEAN)) AS ARRAY<BOOLEAN>) AS xs `` | `` _bool → array<boolean> `` | 原比较显示不同；原生Boolean投影的状态/类型/四个元素值相同 |
| nested-int | `` SELECT ARRAY[ARRAY['1',2],ARRAY['0x7f',3]] AS xs `` | `` SELECT CAST(ARRAY(CAST(ARRAY(CAST('1' AS INT), 2) AS ARRAY<INT>), CAST(ARRAY(CAST('127' AS INT), 3) AS ARRAY<INT>)) AS ARRAY<ARRAY<INT>>) AS xs `` | `` _int4 → array<array<int>> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| scalar-int | `` SELECT ARRAY['1_000',(SELECT 1),NULL] AS xs `` | `` SELECT CAST(ARRAY(CAST('1000' AS INT), (SELECT 1), NULL) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| runtime-null-order | `` SELECT CAST(id AS INT) AS id,ARRAY['0x7f',CAST(x AS INT),NULL] AS xs FROM (VALUES(1,2),(2,NULL),(3,2)) t(id,x) ORDER BY id `` | `` SELECT CAST(id AS INT) AS id, CAST(ARRAY(CAST('127' AS INT), CAST(x AS INT), NULL) AS ARRAY<INT>) AS xs FROM (SELECT 1 AS id, 2 AS x UNION ALL SELECT 2, NULL UNION ALL SELECT 3, 2) AS t ORDER BY id NULLS LAST `` | `` int4 / _int4 → int / array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| explicit-outer-bigint | `` SELECT ARRAY['2147483647',1]::BIGINT[] AS xs `` | `` SELECT CAST(CAST(ARRAY(CAST('2147483647' AS BIGINT), 1) AS ARRAY<BIGINT>) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| pure-text | `` SELECT ARRAY['0x7f','yes',NULL] AS xs `` | `` SELECT CAST(ARRAY('0x7f', 'yes', NULL) AS ARRAY<STRING>) AS xs `` | `` _text → array<text> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| known-small-promotes-int | `` SELECT ARRAY['32768',1::SMALLINT,2::INT] AS xs `` | `` SELECT CAST(ARRAY(CAST('32768' AS INT), CAST(1 AS SMALLINT), CAST(2 AS INT)) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-1 | `` SELECT ARRAY['2147483648',1]::BIGINT[] AS xs `` | `` SELECT CAST(CAST(ARRAY(CAST('2147483648' AS BIGINT), 1) AS ARRAY<BIGINT>) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-2 | `` SELECT ARRAY['01',1]::TEXT[] AS xs `` | `` SELECT CAST(CAST(ARRAY('01', 1) AS ARRAY<STRING>) AS ARRAY<STRING>) AS xs `` | `` _text → array<text> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-3 | `` SELECT (ARRAY['0x7fff',1])::SMALLINT[] AS xs `` | `` SELECT CAST((CAST(ARRAY(CAST('32767' AS SMALLINT), 1) AS ARRAY<SMALLINT>)) AS ARRAY<SMALLINT>) AS xs `` | `` _int2 → array<smallint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-4 | `` SELECT ARRAY[ARRAY['2147483648',1],ARRAY[2,3]]::BIGINT[][] AS xs `` | `` SELECT CAST(CAST(ARRAY(CAST(ARRAY(CAST('2147483648' AS BIGINT), 1) AS ARRAY<BIGINT>), CAST(ARRAY(2, 3) AS ARRAY<BIGINT>)) AS ARRAY<ARRAY<BIGINT>>) AS ARRAY<ARRAY<BIGINT>>) AS xs `` | `` _int8 → array<array<bigint>> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-5 | `` SELECT ARRAY['1.5',1]::NUMERIC(10,2)[] AS xs `` | `` SELECT CAST(ARRAY('1.5', 1) AS ARRAY<DECIMAL(10, 2)>) AS xs `` | `` _numeric → array<decimalv3(10,2)> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-6 | `` SELECT ARRAY[TRUE,'01']::INT[] AS xs `` | `` SELECT CAST(CAST(ARRAY(TRUE, CAST('1' AS INT)) AS ARRAY<INT>) AS ARRAY<INT>) AS xs `` | `` _int4 → array<int> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-7 | `` SELECT ARRAY['0x7fff_ffff_ffff_ffff',1]::BIGINT[] AS xs `` | `` SELECT CAST(CAST(ARRAY(CAST('9223372036854775807' AS BIGINT), 1) AS ARRAY<BIGINT>) AS ARRAY<BIGINT>) AS xs `` | `` _int8 → array<bigint> `` | 本次状态、字段、可核对类型、值及重复次数一致 |
| outer-8 | `` SELECT ARRAY['001',1]::TEXT[] AS xs `` | `` SELECT CAST(CAST(ARRAY('001', 1) AS ARRAY<STRING>) AS ARRAY<STRING>) AS xs `` | `` _text → array<text> `` | 本次状态、字段、可核对类型、值及重复次数一致 |

所有表中60条均执行成功并重复稳定。24条混合整数、6条上下文、8条外层CAST的现有行值比较均一致；22条Boolean按前述原生投影补证，同时保留直接数组比较不同。外层NUMERIC(10,2)案例当前值和约束对齐，不推广为所有NUMERIC输入拼写都已实现。

### 3.2 21条负向输入

这些是直接相关的补充边界，不属于原.out的4条负向，也不进入主修复清单。21条PG实际失败，当前RAISE全部unsupported，未再次执行Doris；不要求错误文本/错误码相同，不把共同失败称为成功匹配。

| 编号 | 完整源SQL | PG SQLSTATE | PG实际错误 |
| ---: | :--- | :--- | :--- |
| 1 | `` SELECT ARRAY['1__0',1] AS xs `` | 22P02 | invalid input syntax for type integer: "1__0" LINE 1: SELECT ARRAY['1__0',1] AS xs                      ^ |
| 2 | `` SELECT ARRAY['_1',1] AS xs `` | 22P02 | invalid input syntax for type integer: "_1" LINE 1: SELECT ARRAY['_1',1] AS xs                      ^ |
| 3 | `` SELECT ARRAY['1_',1] AS xs `` | 22P02 | invalid input syntax for type integer: "1_" LINE 1: SELECT ARRAY['1_',1] AS xs                      ^ |
| 4 | `` SELECT ARRAY['0x',1] AS xs `` | 22P02 | invalid input syntax for type integer: "0x" LINE 1: SELECT ARRAY['0x',1] AS xs                      ^ |
| 5 | `` SELECT ARRAY['0x__1',1] AS xs `` | 22P02 | invalid input syntax for type integer: "0x__1" LINE 1: SELECT ARRAY['0x__1',1] AS xs                      ^ |
| 6 | `` SELECT ARRAY['1e2',1] AS xs `` | 22P02 | invalid input syntax for type integer: "1e2" LINE 1: SELECT ARRAY['1e2',1] AS xs                      ^ |
| 7 | `` SELECT ARRAY['1.0',1] AS xs `` | 22P02 | invalid input syntax for type integer: "1.0" LINE 1: SELECT ARRAY['1.0',1] AS xs                      ^ |
| 8 | `` SELECT ARRAY['+ 1',1] AS xs `` | 22P02 | invalid input syntax for type integer: "+ 1" LINE 1: SELECT ARRAY['+ 1',1] AS xs                      ^ |
| 9 | `` SELECT ARRAY['',1] AS xs `` | 22P02 | invalid input syntax for type integer: "" LINE 1: SELECT ARRAY['',1] AS xs                      ^ |
| 10 | `` SELECT ARRAY[' ',1] AS xs `` | 22P02 | invalid input syntax for type integer: " " LINE 1: SELECT ARRAY[' ',1] AS xs                      ^ |
| 11 | `` SELECT ARRAY['１',1] AS xs `` | 22P02 | invalid input syntax for type integer: "１" LINE 1: SELECT ARRAY['１',1] AS xs                      ^ |
| 12 | `` SELECT ARRAY[' 1 ',1] AS xs `` | 22P02 | invalid input syntax for type integer: " 1 " LINE 1: SELECT ARRAY[' 1 ',1] AS xs                      ^ |
| 13 | `` SELECT ARRAY['2147483648',1] AS xs `` | 22003 | value "2147483648" is out of range for type integer LINE 1: SELECT ARRAY['2147483648',1] AS xs                      ^ |
| 14 | `` SELECT ARRAY[TRUE,'o'] AS xs `` | 22P02 | invalid input syntax for type boolean: "o" LINE 1: SELECT ARRAY[TRUE,'o'] AS xs                           ^ |
| 15 | `` SELECT ARRAY[TRUE,'truth'] AS xs `` | 22P02 | invalid input syntax for type boolean: "truth" LINE 1: SELECT ARRAY[TRUE,'truth'] AS xs                           ^ |
| 16 | `` SELECT ARRAY[TRUE,' '] AS xs `` | 22P02 | invalid input syntax for type boolean: " " LINE 1: SELECT ARRAY[TRUE,' '] AS xs                           ^ |
| 17 | `` SELECT ARRAY[TRUE,'10'] AS xs `` | 22P02 | invalid input syntax for type boolean: "10" LINE 1: SELECT ARRAY[TRUE,'10'] AS xs                           ^ |
| 18 | `` SELECT ARRAY[TRUE,'0x1'] AS xs `` | 22P02 | invalid input syntax for type boolean: "0x1" LINE 1: SELECT ARRAY[TRUE,'0x1'] AS xs                           ^ |
| 19 | `` SELECT ARRAY[TRUE,'yesno'] AS xs `` | 22P02 | invalid input syntax for type boolean: "yesno" LINE 1: SELECT ARRAY[TRUE,'yesno'] AS xs                           ^ |
| 20 | `` SELECT ARRAY['32768',1::SMALLINT] AS xs `` | 22003 | value "32768" is out of range for type smallint LINE 1: SELECT ARRAY['32768',1::SMALLINT] AS xs                      ^ |
| 21 | `` SELECT ARRAY['9223372036854775808',1::BIGINT] AS xs `` | 22003 | value "9223372036854775808" is out of range for type bigint LINE 1: SELECT ARRAY['9223372036854775808',1::BIGINT] AS xs                      ^ |

## 4. NUMERIC/Float余项的具体证据

15组实际补查请求中9条当前值相同、5条不同、1条不能生成目标；所有15条PG源成功。第14条不被工具Parser接受，另以受限的PG原生只读连接执行原SELECT、读字段与 `cursor.pgresult.fmod(i)`，确认源成功且结果0；不能把SQLGlot Parser拒绝当源负向。表中typmod是协议返回的类型修饰信息；-1仅表示无可用结果修饰信息，不单凭它证明所有值都属于无约束类型域，也不代表目标精度已经相等。

| 编号 | 完整PG源SQL | 当前实际生成Doris SQL | 类型与源typmod | 具体结论 |
| ---: | :--- | :--- | :--- | :--- |
| 1 | `` SELECT ARRAY[1.25,2] AS xs `` | `` SELECT ARRAY(1.25, 2) AS xs `` | `` _numeric → array<decimalv3(3,2)> ``；源typmod=-1 | 值一致；源typmod=-1，目标固定(3,2)，不是完整声明契约通过。 |
| 2 | `` SELECT ARRAY[-99.99::NUMERIC(10,2),99.99::NUMERIC(10,2)] AS xs `` | `` SELECT ARRAY(-CAST(99.99 AS DECIMAL(10, 2)), CAST(99.99 AS DECIMAL(10, 2))) AS xs `` | `` _numeric → array<decimalv3(13,2)> ``；源typmod=-1 | 值一致；外层负号后的源结果typmod=-1，不拿子CAST(10,2)替代结果声明。 |
| 3 | `` SELECT ARRAY[9223372036854775808] AS xs `` | `` SELECT ARRAY(9223372036854775808) AS xs `` | `` _numeric → array<largeint> ``；源typmod=-1 | 值一致；NUMERIC / LARGEINT类型不同，不能转BIGINT。 |
| 4 | `` SELECT ARRAY[NULL::NUMERIC(10,2),1.25::NUMERIC(10,2)] AS xs `` | `` SELECT ARRAY(CAST(NULL AS DECIMAL(10, 2)), CAST(1.25 AS DECIMAL(10, 2))) AS xs `` | `` _numeric → array<decimalv3(10,2)> ``；源typmod=655366 | 当前(10,2)约束和值可核对。 |
| 5 | `` SELECT ARRAY['1.5',1]::NUMERIC[] AS xs `` | `` SELECT CAST(ARRAY('1.5', 1) AS ARRAY<DECIMAL>) AS xs `` | `` _numeric → array<decimalv3(38,9)> ``；源typmod=-1 | 值一致；源无约束NUMERIC，目标(38,9)，仍有可表示域限制。 |
| 6 | `` SELECT ARRAY['1.5',1]::NUMERIC(10,2)[] AS xs `` | `` SELECT CAST(ARRAY('1.5', 1) AS ARRAY<DECIMAL(10, 2)>) AS xs `` | `` _numeric → array<decimalv3(10,2)> ``；源typmod=655366 | 当前(10,2)约束和值可核对；不推广成全部数值输入格式都兼容。 |
| 7 | `` SELECT ARRAY[1.25::NUMERIC(10,2),2::INT] AS xs `` | `` SELECT ARRAY(CAST(1.25 AS DECIMAL(10, 2)), CAST(2 AS INT)) AS xs `` | `` _numeric → array<decimalv3(12,2)> ``；源typmod=-1 | 值一致；混合INT后源结果typmod=-1，目标(12,2)。 |
| 8 | `` SELECT ARRAY[1.25::NUMERIC(10,2),2.125::NUMERIC(11,3)] AS xs `` | `` SELECT ARRAY(CAST(1.25 AS DECIMAL(10, 2)), CAST(2.125 AS DECIMAL(11, 3))) AS xs `` | `` _numeric → array<decimalv3(11,3)> ``；源typmod=-1 | 值一致；源结果typmod=-1，目标(11,3)。 |
| 9 | `` SELECT ARRAY['NaN'::NUMERIC(10,2)] AS xs `` | `` SELECT ARRAY(CAST('NaN' AS DECIMAL(10, 2))) AS xs `` | `` _numeric → array<decimalv3(10,2)> ``；源typmod=655366 | 真实值差异：源NaN，目标NULL；即使两边(10,2)也不等价。 |
| 10 | `` SELECT ARRAY['Infinity'::NUMERIC] AS xs `` | `` SELECT ARRAY(CAST('Infinity' AS DECIMAL)) AS xs `` | `` _numeric → array<decimalv3(38,9)> ``；源typmod=-1 | 真实值差异：源Infinity，目标NULL。 |
| 11 | `` SELECT ARRAY['-Infinity'::NUMERIC] AS xs `` | `` SELECT ARRAY(CAST('-Infinity' AS DECIMAL)) AS xs `` | `` _numeric → array<decimalv3(38,9)> ``；源typmod=-1 | 真实值差异：源-Infinity，目标NULL。 |
| 12 | `` SELECT ARRAY[1e40::NUMERIC] AS xs `` | `` SELECT ARRAY(CAST(1e40 AS DECIMAL)) AS xs `` | `` _numeric → array<decimalv3(38,9)> ``；源typmod=-1 | 真实值差异：源1e40，目标默认DECIMAL(38,9)溢出后NULL。 |
| 13 | `` SELECT ARRAY[1::NUMERIC(39,0)] AS xs `` | `` SELECT ARRAY(CAST(1 AS DECIMAL(39, 0))) AS xs `` | `` _numeric → array<decimalv3(39,0)> ``；源typmod=2555908 | 当前样本1在目标(39,0)成功；不能据此证明完整39位数值域。 |
| 14 | `` SELECT ARRAY[1::NUMERIC(3,-1)] AS xs `` | 未生成；见ParseError | `` _numeric → 无成功字段 ``；源typmod=198659 | PG源成功返回0；SQLGlot不支持NUMERIC负Scale语法，生成前ParseError。不是源负向。 |
| 15 | `` SELECT ARRAY[1::REAL,'1e2'] AS xs `` | `` SELECT ARRAY(CAST(1 AS FLOAT), '1e2') AS xs `` | `` _float4 → array<text> ``；源typmod=-1 | 真实值/类型差异：源FLOAT [1,100]，目标TEXT ["1","1e2"]；尚未支持浮点输入转换。 |

第9–12条实际目标均返回 `[null]`：NaN、Infinity、-Infinity、1e40并不是NULL。第15条源值为 `[1.0,100.0]`，目标为文本 `["1","1e2"]`。这些不是“只差输出样式”，也没有因为字段类型不同而跳过值比较。

第14条实际错误：

~~~text
ParseError: Expected type. Line 1, Col: 23.
  SELECT ARRAY[1::NUMERIC(3,-1)] AS xs
~~~

本轮还修正了前轮辅助推型在Parser收集错误时对缺失Cast.to调用is_type而产生AttributeError的问题，保留真正Parser错误。但PG NUMERIC负Scale语法仍未实现；这是已有通用类型研究的具体新证据，不在本轮偷做通用Parser改写。SOURCE成功0、原生精度3/Scale-1、typmod198659均来自实际读取。

[PG NUMERIC说明](https://www.postgresql.org/docs/18/datatype-numeric.html)允许无约束精度、NaN和Infinity以及负Scale；[Doris类型说明](https://doris.apache.org/docs/4.x/table-design/data-type/)定义的是有界Decimal。不能用统一INT/DOUBLE或任意有限Decimal冒充PG NUMERIC全域；NaN/Infinity当前也不能靠换一个(p,s)CAST保留为Decimal值。1e40默认精度溢出与有限可表示输入的类型保留仍需细分研究，不能把一次失败当作所有场景都无法安全转译。

本轮 SHOW VARIABLES 读到 enable_decimal256=false，但第13条 `NUMERIC(39,0)` 的**当前值1**成功且目标报告ARRAY<DECIMALV3(39,0)>；如实保留这个版本的实际观察，不据文档上限伪造其失败，也不由值1证明所有39位值可表示。未改变该Session政策。

## 5. 14条原Case与固定回归

本轮原14条PG均成功，另按原字段TEXT投影，与RecordedOutputProvider读取的原.out多重集合逐条一致；投影仅补查当前源证据，不替代原生类型/排序验收，不更换.out基线。

| Case / stage | 原.out实际结果 | PG → Doris已取得类型 | 具体错误或限制 |
| :--- | :--- | :--- | :--- |
| [0010](../../../../attribution/cases/aggregates-001/pg-aggregates-0010-12bf388c.md) / 01 | 行值或顺序不匹配 | `` _text → array<text> `` | 结构化TEXT数组相同，.out显示差异保留。 |
| [0136](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md) / 03 | SQLGlot 转译失败 | `` _int8 → 无成功字段 `` | UnsupportedError: Doris does not support ARRAY subquery constructors |
| [0306](../../../../attribution/cases/aggregates-001/pg-aggregates-0306-e70870c4.md) / 17 | 匹配 | `` text / numeric → varchar(65533) / bigint `` | 外层其他字段类型余项保留。 |
| [0410](../../../../attribution/cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md) / 31 | Doris 执行失败 | `` _int4 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 76)\n") |
| [0411](../../../../attribution/cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md) / 31 | Doris 执行失败 | `` _float8 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 66)\n") |
| [0412](../../../../attribution/cases/aggregates-001/pg-aggregates-0412-cbdaef84.md) / 31 | Doris 执行失败 | `` _int4 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 89)\n") |
| [0413](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) / 31 | Doris 执行失败 | `` _float8 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 97)\n") |
| [0415](../../../../attribution/cases/aggregates-001/pg-aggregates-0415-16b30942.md) / 31 | Doris 执行失败 | `` _text → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 60)\n") |
| [0434](../../../../attribution/cases/aggregates-001/pg-aggregates-0434-5da33736.md) / 33 | Doris 执行失败 | `` int8 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 26)\n") |
| [0437](../../../../attribution/cases/aggregates-001/pg-aggregates-0437-d68f01c2.md) / 33 | Doris 执行失败 | `` numeric → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") |
| [0438](../../../../attribution/cases/aggregates-001/pg-aggregates-0438-998adec3.md) / 33 | Doris 执行失败 | `` regtype → 无成功字段 `` | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 37)\n") |
| [0534](../../../../attribution/cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) / 40 | Doris 执行失败 | `` _float4 / _float4 → 无成功字段 `` | (1105, "errCode = 2, detailMessage = Can not found function 'RWAGG'") |
| [0551](../../../../attribution/cases/aggregates-001/pg-aggregates-0551-f476de2c.md) / 42 | 匹配 | `` text / int4 / int8 → varchar(65533) / tinyint / bigint `` | 外层其他字段类型余项保留。 |
| [0552](../../../../attribution/cases/aggregates-001/pg-aggregates-0552-7ea82af2.md) / 42 | 匹配 | `` text / int4 / int8 → varchar(65533) / tinyint / bigint `` | 外层其他字段类型余项保留。 |

VARIADIC三条的额外pg_probe在目标Parser前置检查拒绝，未再执行目标；上表Doris数据库报错来自真正run。本节生成SQL取自本轮run/Transpiler，不把工具前置失败写成生成器未生成。0010当前结构化TEXT数组相同仍不等于.out MATCH；0306/0551/0552的SUM/CASE等独立类型问题保留。

### 完整原查询与本轮实际生成SQL

### Case 0010 / stage-01

~~~sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
~~~

本轮默认生成：

~~~sql
SELECT ANY_VALUE(v) FROM (SELECT CAST(ARRAY('hello', 'world') AS ARRAY<STRING>) AS v) AS v
~~~

### Case 0136 / stage-03

~~~sql
select array(select sum(x+y) s
            from generate_series(1,3) y group by y order by s)
  from generate_series(1,3) x;
~~~

实际SQLGlot错误：Doris does not support ARRAY subquery constructors。

### Case 0306 / stage-17

~~~sql
select
    string_agg(distinct 'a', ','),
    sum((
        select sum(1)
        from (values(1)) b(id)
        where a.id = b.id
)) from unnest(array[1]) a(id);
~~~

本轮默认生成：

~~~sql
SELECT GROUP_CONCAT(DISTINCT 'a', ','), SUM((SELECT SUM(1) FROM (SELECT 1 AS id) AS b WHERE a.id = b.id)) FROM UNNEST(CAST(ARRAY(1) AS ARRAY<INT>)) AS a(id)
~~~

### Case 0410 / stage-31

~~~sql
select percentile_disc(array[0,0.1,0.25,0.5,0.75,0.9,1]) within group (order by thousand)
from tenk1;
~~~

本轮默认生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(0, 0.1, 0.25, 0.5, 0.75, 0.9, 1)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0411 / stage-31

~~~sql
select percentile_cont(array[0,0.25,0.5,0.75,1]) within group (order by thousand)
from tenk1;
~~~

本轮默认生成：

~~~sql
SELECT PERCENTILE_CONT(ARRAY(0, 0.25, 0.5, 0.75, 1)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0412 / stage-31

~~~sql
select percentile_disc(array[[null,1,0.5],[0.75,0.25,null]]) within group (order by thousand)
from tenk1;
~~~

本轮默认生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(ARRAY(NULL, 1, 0.5), ARRAY(0.75, 0.25, NULL))) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

### Case 0413 / stage-31

~~~sql
select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x)
from generate_series(1,6) x;
~~~

本轮默认生成：

~~~sql
SELECT PERCENTILE_CONT(ARRAY(0, 1, 0.25, 0.75, 0.5, 1, 0.3, 0.32, 0.35, 0.38, 0.4)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '6')) AS x
~~~

### Case 0415 / stage-31

~~~sql
select percentile_disc(array[0.25,0.5,0.75]) within group (order by x)
from unnest('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}'::text[]) u(x);
~~~

本轮默认生成：

~~~sql
SELECT PERCENTILE_DISC(ARRAY(0.25, 0.5, 0.75)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM UNNEST(CAST('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}' AS ARRAY<STRING>)) AS u(x)
~~~

### Case 0434 / stage-33

~~~sql
select least_agg(variadic array[q1,q2]) from int8_tbl;
~~~

本轮默认生成：

~~~sql
SELECT LEAST_AGG(VARIADIC ARRAY(q1, q2)) FROM int8_tbl
~~~

### Case 0437 / stage-33

~~~sql
select cleast_agg(variadic array[4.5,f1]) from int4_tbl;
~~~

本轮默认生成：

~~~sql
SELECT CLEAST_AGG(VARIADIC ARRAY(4.5, f1)) FROM int4_tbl
~~~

### Case 0438 / stage-33

~~~sql
select pg_typeof(cleast_agg(variadic array[4.5,f1])) from int4_tbl;
~~~

本轮默认生成：

~~~sql
SELECT PG_TYPEOF(CLEAST_AGG(VARIADIC ARRAY(4.5, f1))) FROM int4_tbl
~~~

### Case 0534 / stage-40

~~~sql
SELECT eatarray(rwagg(ARRAY[1.0::real])), eatarray(rwagg(ARRAY[1.0::real]));
~~~

本轮默认生成：

~~~sql
SELECT EATARRAY(RWAGG(CAST(ARRAY(CAST(1.0 AS FLOAT)) AS ARRAY<FLOAT>))), EATARRAY(RWAGG(CAST(ARRAY(CAST(1.0 AS FLOAT)) AS ARRAY<FLOAT>)))
~~~

### Case 0551 / stage-42

~~~sql
select v||'a', case v||'a' when 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
~~~

本轮默认生成：

~~~sql
SELECT CONCAT(v, 'a'), CASE CONCAT(v, 'a') WHEN 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(CAST(ARRAY('a', 'b') AS ARRAY<STRING>)) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST
~~~

### Case 0552 / stage-42

~~~sql
select v||'a', case when v||'a' = 'aa' then 1 else 0 end, count(*)
  from unnest(array['a','b']) u(v)
 group by v||'a' order by 1;
~~~

本轮默认生成：

~~~sql
SELECT CONCAT(v, 'a'), CASE WHEN CONCAT(v, 'a') = 'aa' THEN 1 ELSE 0 END, COUNT(*) FROM UNNEST(CAST(ARRAY('a', 'b') AS ARRAY<STRING>)) AS u(v) GROUP BY CONCAT(v, 'a') ORDER BY 1 NULLS LAST
~~~


## 6. 测试、提交边界与下一步

实际测试见本轮汇总：437方法组合测试通过（159个PG/Doris/MySQL + 278个core等方法），全部方言1082方法通过，前者159包含在1082内，不相加。ruff/format/git diff --check通过。缺duckdb/mypy；未执行完整optimizer套件、C扩展或make check，不标通过。

新增test_postgres_array_unknown_inputs在实现前运行1个方法，其中19个子用例（subTest）失败，确认复现缺口；实现、外层CAST修正及最终回归后通过。类型辅助None防护有ErrorLevel.RAISE回归，源负Scale合法语法仍明确未支持。

本轮只涉及PG _array_element_type、Doris数组输入/显式CAST上下文以及对应测试，依赖fix-012的element_type和原task-001数组构造基础。当前四个本轮修改文件与前轮任务在同文件共存，不把累积diff整体当本轮独立commit。HEAD仍089891f2521780e2c5b243005017af9db62f25a6；当前累积diff SHA256为b3737ff1ad9a7fafc5c43675efb645a334ccc5795b32c6285de5045f00a1ad55。无commit/push、Issue/PR。

| 具体子项 | 本轮去向 |
| :--- | :--- |
| unknown字符串 + 已知SMALLINT/INT/BIGINT/Boolean | 本轮约定有限输入规则已实现并完成上述类型/元素/NULL/重复与上下文核对；原Boolean显示不同保留 |
| 显式直接/括号/矩形嵌套数组CAST对unknown输入的类型约束 | 本轮列出的8条边界通过；不声称实现所有通用CAST或PG数组维数语义 |
| unknown字符串 + Float/一般表达式/未知列 | 未实现，Float实例有真实差异；继续原task-001的安全输入转换/可信推型子项，不强制Schema或猜类型 |
| NUMERIC/Decimal有/无约束、非有限、大数与负Scale | 具体事实已细分，已有通用类型研究继续；不能把全部差异都塞进数组构造CAST |
| task-003及外层SUM/CASE、UDF等 | 未实施；沿原独立事项处理，不用其他问题拖成一个混合补丁 |

task-001仍有反例和未完成类型契约，保持“已修改但未完成验收”。下一轮建议优先研究已知Float类型与unknown文本输入，再按上表细分NUMERIC的可安全修复范围、Doris表示限制及通用Parser能力。整份输入未完成。

