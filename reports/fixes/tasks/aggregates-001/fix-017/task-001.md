# task-001 / fix-017：有限 NUMERIC 数组输入

## 1. 结论与范围

**状态：已修改但未完成验收。** 继续 [task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，完成两个独立规则，各保存一个本地commit；未push、创建Issue或PR。共同环境见[本轮汇总](../../../aggregates-001-fix-017-summary.md)。

第一项保留超出INT64的有限整数NUMERIC数组，支持最多76位、嵌套、显式整数CAST确定的运行时有限域；第二项补相同源Scale的有限小数/科学计数法NUMERIC字面量。75条新变体实际执行：32条第一项/显式CAST控制、30条第二项数组构造、13条元素转TEXT。前62条取得对应值/类型或控制证据，后13条因独立下标缺陷仍不同；**不是75条MATCH，也不是整个task已完成。**

源NUMERIC无约束域、运行时文本直接REAL、混合Scale、一般NUMERIC CAST/未知列类型、非有限NUMERIC、一般查询作用域等未全部覆盖。实施前方案、实测修正、两项commit边界均先写入统一任务条目。没有顺带实施其他task；已有下标研究经本轮补证登记为[task-010](../../../../attribution/aggregates-001-attribution-summary.md#task-010)，未修改下标代码。

## 2. 实现与本地提交

| 完整本地SHA | 独立规则 | 父commit |
| :--- | :--- | :--- |
| 3281a9848a342660b8b47a9145846d562db5fb35 | 有限整数NUMERIC数组的类型/精确值/嵌套 | 6922457c6d223eafb1e3e7c1aaab211f88487874 |
| 4dc65a35a7efa92551cb9fb00c2315fcb8ff659f | 同Scale有限小数/指数及工作量/Scale保护 | 3281a9848a342660b8b47a9145846d562db5fb35 |

checkout为../sqlglot-functional-commits，分支codex/doris-functional-commits。第一项实现、测试和双端验证后先commit，第二项再追加；最终干净。第二项收尾全方言测试一次因PATH缺少python失败，补正确PATH后在最终commit上1090项通过，保留这一环境失败说明。没有合并/改写旧提交。

| 文件/入口 | 实际变化及条件 |
| :--- | :--- |
| sqlglot/parsers/postgres.py / _array_element_type | 大于INT64的整数以及小数/指数确定源NUMERIC，不用通用DOUBLE猜型。先看整数token有效位数，避免Python int长度上限。hint只记源NUMERIC基础类型，不虚构源precision/scale；一般NUMERIC CAST和未知字符串的NUMERIC输入函数没有凭空支持。 |
| sqlglot/generators/doris.py / array_sql、_bounded_numeric_array_sql | 已知有限字面量及显式SMALLINT/INT/BIGINT CAST证明目标范围，选择DECIMAL(p,s)，总精度最多76。全层先构造文本数组，再逐层ARRAY_MAP，在叶层运行时CAST，避开大整数词法上限、常量Decimal精度损失及嵌套类型收窄。 |
| 同helper的保护 | Decimal元组推导，不经float或有context舍入的数值计算。各非NULL已知输入Scale须相同；单token最多4096字符、指数绝对值最多10000。不能证明范围/Scale或超过76位时严格模式unsupported。NULL表达式保留给运行时CAST，不在Python返回预计算NULL答案。 |
| tests/dialects/test_postgres.py、test_doris.py | 源类型、INT64边界、19–76位、嵌套、运行时整数、小数/指数/Scale、超长/超精度、AST不变、dump/load、PG round-trip、其他方言及标量隔离。 |

依赖已有数组hint和构造基础，不是无依赖的任意cherry-pick。未修改公共AST、框架、比较器、输入SQL/.out、YAML或数据库数据。

## 3. 修复前后与失败尝试

~~~sql
-- 源
SELECT ARRAY[9223372036854775808,NULL,1] AS xs;
-- 修复前：值可能相同，但目标数组元素为LARGEINT，源为NUMERIC
SELECT ARRAY(9223372036854775808, NULL, 1) AS xs;
-- 最终生成形状
SELECT ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(19, 0)),
  ARRAY('9223372036854775808', CAST(NULL AS STRING), '1')) AS xs;

-- 第二项实际源查询与生成SQL
SELECT ARRAY[1.25,2.00,NULL] AS xs;
SELECT ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(3, 2)),
  ARRAY('1.25', '2.00', CAST(NULL AS STRING))) AS xs;
~~~

上面的三元素整数是规则说明；数据库验收实际使用第4节的完整SQL（包含重复/括号/运行时列），不另把说明变体计入75条。小数示例对应decimal-uniform-scale，实际生成并执行。1e40生成DECIMAL(41,0)，1e-76生成DECIMAL(76,76)。

没有采用的真实候选：

- 常量CAST(ARRAY(CAST('<整数>' AS DECIMAL(p,0)),NULL,1) AS ARRAY<DECIMAL(p,0)>)：39位123456789012345678901234567890123456789被改为123456789012345684702176977901352255488，76位为NULL。不是Doris不能表示这些值，而是该转换路径不安全。
- 初次未提交实现直接嵌套Decimal子数组：当前enable_decimal256=false下共同类型收窄到array<array<decimalv3(38,0)>>，39/76位变NULL。改为全层文本后逐层lambda，最终plan保留实际39/76位，未更改会话设置。
- 初次8条运行时测试写成-9223372036854775808::BIGINT，源先CAST正数再取负而溢出；更正为(-9223372036854775808)::BIGINT后重跑。初次无主键多行核验还曾错误套用同一组谓词，纠正为逐行完整元素文本；二者不算产品修复或新增源负向。

混合Scale的ARRAY[1.25,2]目前严格拒绝：PG第二元素转TEXT是2，统一目标Scale2会成为2.00，数学值相同不足以覆盖这个可观察差异。这是本轮明确的接受范围变化，不写旧边界全部保持。

## 4. 实际SQL与比较范围

使用原stage-01及已有tenk1，不装数。源只读二进制游标避免文本驱动精度丢失；目标每次由最终SQLGlot生成。两端重复执行，核对字段数量/显式名称、源数组OID、目标EXPLAIN VERBOSE类型、行数、NULL/重复/数组元素顺序；最终ORDER BY按id核对。

目标逐元素CAST STRING后完整读回，与PG Decimal固定点精确文本比较，不经float读取76位数。嵌套逐层展开；无最终ORDER BY按保留重复次数的多重集合核验。这是诊断补证，不替换主框架Recorded Output比较。

### 4.1 第一项及显式CAST控制：32条

29条精确元素文本通过且重复稳定；另2条显式TEXT/DECIMAL控制结构化值相同。显式DOUBLE控制直接结构化比较有显示/二进制差异，追加目标内与PG精确DOUBLE等值及NULL检查得到(1,1)；不标主流程MATCH。

| 变体ID | 完整源SQL | 源OID | 目标数组类型 | 实测 |
| :--- | :--- | :--- | :--- | :--- |
| flat-1 | `SELECT ARRAY[(9223372036854775808),NULL,1,9223372036854775808] AS xs` | 1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| nested-1 | `SELECT ARRAY[ARRAY[9223372036854775808,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(19,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-1 | `SELECT id::INT AS id, ARRAY[9223372036854775808,x::BIGINT,NULL,9223372036854775808] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| flat-2 | `SELECT ARRAY[(-9223372036854775809),NULL,1,-9223372036854775809] AS xs` | 1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| nested-2 | `SELECT ARRAY[ARRAY[-9223372036854775809,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(19,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-2 | `SELECT id::INT AS id, ARRAY[-9223372036854775809,x::BIGINT,NULL,-9223372036854775809] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| flat-3 | `SELECT ARRAY[(18446744073709551616),NULL,1,18446744073709551616] AS xs` | 1231 | `array<decimalv3(20,0)>` | 精确元素文本通过；重复稳定 |
| nested-3 | `SELECT ARRAY[ARRAY[18446744073709551616,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(20,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-3 | `SELECT id::INT AS id, ARRAY[18446744073709551616,x::BIGINT,NULL,18446744073709551616] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(20,0)>` | 精确元素文本通过；重复稳定 |
| flat-4 | `SELECT ARRAY[(99999999999999999999999999999999999999),NULL,1,99999999999999999999999999999999999999] AS xs` | 1231 | `array<decimalv3(38,0)>` | 精确元素文本通过；重复稳定 |
| nested-4 | `SELECT ARRAY[ARRAY[99999999999999999999999999999999999999,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(38,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-4 | `SELECT id::INT AS id, ARRAY[99999999999999999999999999999999999999,x::BIGINT,NULL,99999999999999999999999999999999999999] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(38,0)>` | 精确元素文本通过；重复稳定 |
| flat-5 | `SELECT ARRAY[(100000000000000000000000000000000000000),NULL,1,100000000000000000000000000000000000000] AS xs` | 1231 | `array<decimalv3(39,0)>` | 精确元素文本通过；重复稳定 |
| nested-5 | `SELECT ARRAY[ARRAY[100000000000000000000000000000000000000,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(39,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-5 | `SELECT id::INT AS id, ARRAY[100000000000000000000000000000000000000,x::BIGINT,NULL,100000000000000000000000000000000000000] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(39,0)>` | 精确元素文本通过；重复稳定 |
| flat-6 | `SELECT ARRAY[(123456789012345678901234567890123456789),NULL,1,123456789012345678901234567890123456789] AS xs` | 1231 | `array<decimalv3(39,0)>` | 精确元素文本通过；重复稳定 |
| nested-6 | `SELECT ARRAY[ARRAY[123456789012345678901234567890123456789,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(39,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-6 | `SELECT id::INT AS id, ARRAY[123456789012345678901234567890123456789,x::BIGINT,NULL,123456789012345678901234567890123456789] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(39,0)>` | 精确元素文本通过；重复稳定 |
| flat-7 | `SELECT ARRAY[(9999999999999999999999999999999999999999999999999999999999999999999999999999),NULL,1,9999999999999999999999999999999999999999999999999999999999999999999999999999] AS xs` | 1231 | `array<decimalv3(76,0)>` | 精确元素文本通过；重复稳定 |
| nested-7 | `SELECT ARRAY[ARRAY[9999999999999999999999999999999999999999999999999999999999999999999999999999,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(76,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-7 | `SELECT id::INT AS id, ARRAY[9999999999999999999999999999999999999999999999999999999999999999999999999999,x::BIGINT,NULL,9999999999999999999999999999999999999999999999999999999999999999999999999999] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(76,0)>` | 精确元素文本通过；重复稳定 |
| flat-8 | `SELECT ARRAY[(-9999999999999999999999999999999999999999999999999999999999999999999999999999),NULL,1,-9999999999999999999999999999999999999999999999999999999999999999999999999999] AS xs` | 1231 | `array<decimalv3(76,0)>` | 精确元素文本通过；重复稳定 |
| nested-8 | `SELECT ARRAY[ARRAY[-9999999999999999999999999999999999999999999999999999999999999999999999999999,NULL],ARRAY[1,-1]] AS xs` | 1231 | `array<array<decimalv3(76,0)>>` | 精确元素文本通过；重复稳定 |
| runtime-8 | `SELECT id::INT AS id, ARRAY[-9999999999999999999999999999999999999999999999999999999999999999999999999999,x::BIGINT,NULL,-9999999999999999999999999999999999999999999999999999999999999999999999999999] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 23,1231 | `array<decimalv3(76,0)>` | 精确元素文本通过；重复稳定 |
| runtime-real-table | `SELECT unique1::INT AS id, ARRAY[9223372036854775808,unique1::INT,NULL] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` | 23,1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| nested-shared-width | `SELECT ARRAY[ARRAY[9223372036854775808,1],ARRAY[9999999999999999999999999999999999999999999999999999999999999999999999999999,NULL]] AS xs` | 1231 | `array<array<decimalv3(76,0)>>` | 精确元素文本通过；重复稳定 |
| smallint | `SELECT ARRAY[9223372036854775808,x::SMALLINT,NULL] AS xs FROM (VALUES(-32768),(32767),(NULL)) t(x)` | 1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| integer | `SELECT ARRAY[9223372036854775808,x::INT,NULL] AS xs FROM (VALUES(-2147483648),(2147483647),(NULL)) t(x)` | 1231 | `array<decimalv3(19,0)>` | 精确元素文本通过；重复稳定 |
| bigint-control | `SELECT ARRAY[-9223372036854775808,9223372036854775807,NULL] AS xs` | 1016 | `array<bigint>` | 精确元素文本通过；重复稳定 |
| explicit-text | `SELECT ARRAY[9223372036854775808,NULL]::TEXT[] AS xs` | 1009 | `array<text>` | 结构化值通过；显式CAST控制 |
| explicit-decimal | `SELECT ARRAY[9223372036854775808,NULL]::NUMERIC(30,2)[] AS xs` | 1231 | `array<decimalv3(30,2)>` | 结构化值通过；显式CAST控制 |
| explicit-double | `SELECT ARRAY[9223372036854775808,NULL]::DOUBLE PRECISION[] AS xs` | 1022 | `array<double>` | 结构化显示差异；追加原生等值通过 |

### 4.2 第二项及元素转TEXT：43条

30条数组构造的精确值/元素文本Scale、NULL、plan类型与重复执行通过；13条TEXT投影是实际错误，源非NULL、目标NULL，见第6节，不记为通过。

| 变体ID | 完整源SQL | 实测 |
| :--- | :--- | :--- |
| decimal-flat-1 | `SELECT ARRAY[1.25,NULL,1.25] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-1 | `SELECT ARRAY[ARRAY[1.25,NULL],ARRAY[1.25,1.25]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-1 | `SELECT (ARRAY[1.25,NULL,1.25])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-2 | `SELECT ARRAY[0.1,NULL,0.1] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-2 | `SELECT ARRAY[ARRAY[0.1,NULL],ARRAY[0.1,0.1]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-2 | `SELECT (ARRAY[0.1,NULL,0.1])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-3 | `SELECT ARRAY[-0.01,NULL,-0.01] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-3 | `SELECT ARRAY[ARRAY[-0.01,NULL],ARRAY[-0.01,-0.01]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-3 | `SELECT (ARRAY[-0.01,NULL,-0.01])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-4 | `SELECT ARRAY[1.2300,NULL,1.2300] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-4 | `SELECT ARRAY[ARRAY[1.2300,NULL],ARRAY[1.2300,1.2300]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-4 | `SELECT (ARRAY[1.2300,NULL,1.2300])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-5 | `SELECT ARRAY[1e40,NULL,1e40] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-5 | `SELECT ARRAY[ARRAY[1e40,NULL],ARRAY[1e40,1e40]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-5 | `SELECT (ARRAY[1e40,NULL,1e40])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-6 | `SELECT ARRAY[1e-40,NULL,1e-40] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-6 | `SELECT ARRAY[ARRAY[1e-40,NULL],ARRAY[1e-40,1e-40]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-6 | `SELECT (ARRAY[1e-40,NULL,1e-40])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-7 | `SELECT ARRAY[1.25e2,NULL,1.25e2] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-7 | `SELECT ARRAY[ARRAY[1.25e2,NULL],ARRAY[1.25e2,1.25e2]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-7 | `SELECT (ARRAY[1.25e2,NULL,1.25e2])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-8 | `SELECT ARRAY[1.25e-2,NULL,1.25e-2] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-8 | `SELECT ARRAY[ARRAY[1.25e-2,NULL],ARRAY[1.25e-2,1.25e-2]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-8 | `SELECT (ARRAY[1.25e-2,NULL,1.25e-2])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-9 | `SELECT ARRAY[1e-76,NULL,1e-76] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-9 | `SELECT ARRAY[ARRAY[1e-76,NULL],ARRAY[1e-76,1e-76]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-9 | `SELECT (ARRAY[1e-76,NULL,1e-76])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-10 | `SELECT ARRAY[1e75,NULL,1e75] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-10 | `SELECT ARRAY[ARRAY[1e75,NULL],ARRAY[1e75,1e75]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-10 | `SELECT (ARRAY[1e75,NULL,1e75])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-11 | `SELECT ARRAY[0e-76,NULL,0e-76] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-11 | `SELECT ARRAY[ARRAY[0e-76,NULL],ARRAY[0e-76,0e-76]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-11 | `SELECT (ARRAY[0e-76,NULL,0e-76])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-12 | `SELECT ARRAY[-0.0000,NULL,-0.0000] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-12 | `SELECT ARRAY[ARRAY[-0.0000,NULL],ARRAY[-0.0000,-0.0000]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-12 | `SELECT (ARRAY[-0.0000,NULL,-0.0000])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-flat-13 | `SELECT ARRAY[99999999999999999999999999999999999999.9,NULL,99999999999999999999999999999999999999.9] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-13 | `SELECT ARRAY[ARRAY[99999999999999999999999999999999999999.9,NULL],ARRAY[99999999999999999999999999999999999999.9,99999999999999999999999999999999999999.9]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-text-13 | `SELECT (ARRAY[99999999999999999999999999999999999999.9,NULL,99999999999999999999999999999999999999.9])[1]::TEXT AS value` | 目标NULL、源非NULL文本：独立下标错误 |
| decimal-uniform-scale | `SELECT ARRAY[1.25,2.00,NULL] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-nested-uniform-scale | `SELECT ARRAY[ARRAY[1.25,2.00],ARRAY[-99.99,NULL]] AS xs` | 精确元素文本/Scale通过；重复稳定 |
| decimal-runtime-scale0 | `SELECT id::INT AS id, ARRAY[1e40,x::BIGINT,NULL,1e40] AS xs FROM (VALUES(1,2::BIGINT),(2,NULL::BIGINT),(3,(-9223372036854775808)::BIGINT),(4,2::BIGINT)) t(id,x) ORDER BY id` | 精确元素文本/Scale通过；重复稳定 |
| decimal-zero | `SELECT ARRAY[0.00,0.00,NULL] AS xs` | 精确元素文本/Scale通过；重复稳定 |

75条直接结构化读取为61相同、13下标错误、1显式DOUBLE表示差异。追加原生控制后前62条有各自规则证据，但不等于完整声明契约或全输入同义。未生成这些变体的.out/YAML，也不创造框架MATCH统计。

## 5. 运行时文本直接REAL：仍未解决

核对本机对应提交的源码：

- [Doris StringParser](https://github.com/apache/doris/blob/7126cf65d96/be/src/util/string_parser.hpp)先读为double再返回目标类型；[CastToFloat/Decimal转换](https://github.com/apache/doris/blob/7126cf65d96/be/src/exprs/function/cast/cast_to_basic_number_common.h)也有double中间值。
- [PG18.1 float.c](https://github.com/postgres/postgres/blob/REL_18_1/src/backend/utils/adt/float.c)直接使用strtof，明确说明double rounding，含7.038531e-26例子。
- [Doris数值SerDe](https://github.com/apache/doris/blob/7126cf65d96/be/src/core/data_type_serde/data_type_number_serde.cpp)仍调用同一浮点转换路径，换输入包装不等于换了解析器。

5个输入各测8条手写可行性路径，共40次，不计入修复验收：直接FLOAT、lambda FLOAT、FROM_JSON、JSON后CAST、JSON_EXTRACT_DOUBLE后CAST、Decimal(76,60)、Decimal(76,30)、lambda Decimal后FLOAT。FROM_JSON本机5次均不存在；其他路径没有同时保住普通值、中点、次正规数和最大值。

| 输入 / PG REAL再提升DOUBLE | 关键目标结果 | 结论 |
| :--- | :--- | :--- |
| 7.038531e-26 / 7.038530691851209e-26 | lambda等路径为7.038531308148791e-26 | 真值差异，不是显示 |
| 1.0000000596046447753906250000000000001 / 1.0000001192092896 | 多条运行时路径为1.0 | double中转丢失中点两侧差别 |
| 0.1 / 0.10000000149011612 | lambda等原生等值通过，直接常量路径仍不等 | 普通值不足以证明中点正确 |
| 1e-45 | 部分路径正确，Decimal(76,30)变零 | 固定Scale不能通用代替 |
| 最大REAL附近3.4028234663852886e38 | 部分正确，Decimal(76,60)为NULL | 整数位与小数位不能同时任意增大 |

还用真实表字段分别以7.038531e-26、上表第二个中点、0.1执行以下参数化说明对应的3条查询，每条四行；两端成功且重复稳定，但当前生成目标的精确元素等值标志均为[0,0,0,0]：

~~~sql
-- <v>分别替换为上述3个已测值；此代码块是说明，不另算第4条
SELECT unique1::INT AS id,
 ARRAY[(CASE WHEN unique1%2=0 THEN '<v>' ELSE '0.1' END)::REAL,
       2::DOUBLE PRECISION] AS xs
FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1;
~~~

没有将运行时列预计算成字面量，没有改Doris源码或比较容差。“尚未找到安全通用路径”不等于证明任何SQL算法都不可能。此余项保持task-001未验收；若需改变Doris、类型前提、数据或比较契约，先取得新授权。

## 6. 独立问题：数组下标

13条TEXT投影以第一条为例，源为'1.25'，实际生成目标把下标写成[0]并返回NULL：

~~~sql
SELECT (ARRAY[1.25,NULL,1.25])[1]::TEXT AS value;
SELECT CAST((ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(3, 2)), ARRAY('1.25', CAST(NULL AS STRING), '1.25')))[0] AS STRING) AS `value`;
~~~

普通INT数组也复现，证明不是新增NUMERIC转换造成。源控制均是SELECT (ARRAY[1,2,3])[下标] AS value；实际目标数组为CAST(ARRAY(1, 2, 3) AS ARRAY<INT>)：

| 源下标 | PG值 | 实际目标下标 / 值 |
| :--- | :--- | :--- |
| [1] | 1 | [0] / NULL |
| [2] | 2 | [1] / 1 |
| [0] | NULL | [-1] / 3 |

手写原生Doris控制SELECT ARRAY(1,2,3)[1] AS value返回1，证明目标具备能力，不作为已修复验收。已登记独立task-010，未改代码。后续需单独处理正/零/负/动态下标、越界NULL、嵌套、一次求值、Map/JSON/其他方言隔离，不能机械全局加1。

## 7. 回归与剩余工作

- 最终1090项全方言、301项定向/核心通过；有重叠，不相加当唯一测试数。lint、format、diff通过。共同命令见汇总。
- 274条旧边界中273条双端成功并重复稳定，NaN按类别判断；1条ARRAY[1.25,2]由原DOUBLE错类型输出改为严格拒绝。原生/结构补查不冒充主框架MATCH。
- 原310条/43阶段：82匹配、25源负向、64值/顺序差异、114目标失败、12环境标签、13转译失败。原0410/0411/0412/0413/0415由WITHIN GROUP目标错误改为混合Scale提前拒绝；没有修复WITHIN GROUP或提高匹配率。
- 原task-001关联14条：3匹配、1值/显示差异、4目标失败、6转译拒绝；先前9目标失败/1拒绝中的5条只是阶段变化。原全文沿用前轮报告和首轮JSON。
- 301/303/304有已记录的源后端风险，未执行；全部优化器、mypy、C扩展、任意数据库版本及全数据域未验收，不安装依赖。

task-001仍未完成。下一独立修复建议task-010；本task继续保留直接REAL、混合Scale/一般NUMERIC/显式数组CAST、一般作用域与未知类型余项。不强转DOUBLE、不改答案、不改比较器来制造完成。没有自动开始下一task。

