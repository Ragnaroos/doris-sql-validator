# task-001：REAL 元素先转换再参与数组类型提升（fix-015）

## 1. 结论与范围

**本次有限字面量规则已通过约定验证；整个task-001仍为“已修改但未完成验收”。** 两个既有精度反例已经修正，47条本轮边界的源查询/Doris生成查询成功、逐元素原生等值/NULL核验全部为真、双端重复执行稳定。主比较器仍为26条值一致、21条文本/驱动显示差异，不把它们一律改成MATCH。

本轮按指定任务继续原[task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，不新增编号，不重新打开其他任务。实施前方案已在原task条目写入fix-015，前轮证据见[fix-014](../fix-014/task-001.md)。只修改SQLGlot及配套测试；不修改源SQL/.out、阶段YAML、框架、比较器、数据或Session政策。共同环境、提交与整体完成检查见[本轮汇总](../../../aggregates-001-fix-015-summary.md)。

纳入：带PG可信数组元素类型的有限十进制字面量REAL CAST、连续REAL/DOUBLE CAST、根部/链中负号、括号、NULL/重复、矩形嵌套和外层数组CAST。只规范化字面量输入，不在Python求整条查询结果，不强制Schema。无REAL层的直接DOUBLE CAST不扩大改写；非有限/十六进制、超长/上溢/非零下溢等不支持的已知CAST输入保留原生成行为，未知字符串原有unsupported规则不放宽。

标量子查询和运行时列的转换没有在本轮实现；第6节给出当前实测反例与下一轮方案。task-003及NUMERIC相关事项未实施。

## 2. 为什么需要修改SQLGlot

PG中的REAL值必须先按FLOAT32转换，然后再提升到数组共同类型。此前类型提示只确保数组最终是FLOAT/DOUBLE，却没有保留已有REAL CAST的实际舍入结果。Doris当前环境的常量FLOAT转换路径不能直接保真，因此单纯在数组外增加CAST没有解决问题。这是当前目标下可通过生成规则修复的缺口，不把Doris内部差异一概说成SQLGlot语法错误。

PG文档说明了[ARRAY的共同类型规则](https://www.postgresql.org/docs/18/typeconv-union-case.html)及[REAL/DOUBLE的IEEE精度和输出限制](https://www.postgresql.org/docs/18/datatype-numeric.html)。下面的具体差异和修复有效性来自当前数据库实测，而非仅凭文档推断。

### 2.1 两条修复前反例

第一条完整源SQL：

~~~sql
SELECT ARRAY['1e2','7.038531e-26'::REAL] AS xs;
~~~

父提交实际生成：

~~~sql
SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('7.038531e-26' AS FLOAT))) AS xs
~~~

当前实际生成：

~~~sql
SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE))) AS xs
~~~

源第二元素二进制读取得到 `7.038530691851209e-26`。用源二进制值的精确十进制表示在目标内逐位置比较：修复前为 `[1,0]`，修复后为 `[1,1]`，重复稳定。不是把显示字符串相近当作正确。

第二条完整源SQL：

~~~sql
SELECT ARRAY['1e2',0.1::REAL,2::DOUBLE PRECISION] AS xs;
~~~

父提交实际生成：

~~~sql
SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST(0.1 AS FLOAT), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs
~~~

当前实际生成：

~~~sql
SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('0.100000001490116119384765625' AS DOUBLE), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs
~~~

源第二元素是REAL先舍入后的 `0.10000000149011612`，并非原十进制0.1直接转DOUBLE。目标原生逐元素比较由 `[1,0,1]` 变为 `[1,1,1]`。主比较器仍因两端文本显示精度不同保留差异，不改规则制造MATCH。

### 2.2 连续转换顺序不能交换

以下两条源SQL均实际执行，得到不同结果，本次生成也保留该差别：

~~~sql
SELECT ARRAY['1.0000000596046447753906250000000000001'::DOUBLE PRECISION::REAL] AS xs;
SELECT ARRAY['1.0000000596046447753906250000000000001'::REAL::DOUBLE PRECISION] AS xs;
~~~

前者源结果为 `[1.0]`；后者为 `[1.0000001192092896]`。实现按内层到外层逐次舍入，不将整个CAST链直接按最终类型一次转换。

## 3. 实际代码、测试与commit

| 文件 / 入口 | 实际修改 | 边界 |
| :--- | :--- | :--- |
| [Doris Generator](../../../../../../sqlglot-functional-commits/sqlglot/generators/doris.py) / array_sql | 先得到转换后的元素；只要FLOAT数组元素发生了本规则转换，即使用既有运行时ARRAY_MAP | 不仅检查原文是否含unknown字符串；纯已有REAL字面量数组也能受益 |
| 同文件 / _coerce_array_input | 在带PG类型提示的数组内提取有限字面量REAL/DOUBLE链，按内向外复用精确浮点舍入；保留负号顺序，输出已按源REAL舍入的精确DOUBLE输入 | 不改全局cast_sql，不跨子查询、不猜列类型；精确可表示输入沿用原CAST |
| [PG Parser](../../../../../../sqlglot-functional-commits/sqlglot/parsers/postgres.py) / _array_element_type.resolve | 为负号下的已知FLOAT/DOUBLE保留类型 | 首次验证发现 `-0.1::REAL` 的外层Neg会丢失数组提示，故补此同规则入口；不推广为任意负表达式推型 |
| [Doris测试](../../../../../../sqlglot-functional-commits/tests/dialects/test_doris.py) / test_postgres_array_real_cast_inputs | 两个精度反例、CAST顺序/负号、AST不变、dump/load、PG/Doris往返、低Decimal上下文、次正规数/最大REAL、其他方言与标量隔离 | 保留未覆盖子查询/列及非有限输入原行为，不将其写成已支持 |
| [PG测试](../../../../../../sqlglot-functional-commits/tests/dialects/test_postgres.py) / test_array_element_type_contract | 新增负REAL及与DOUBLE混合的类型提示/序列化/往返检查 | 不要求Schema |

直接负数字面量取值不能经过Decimal上下文相关的负号运算，否则低精度Python上下文可能改变舍入中点；测试在 `localcontext().prec=2` 下验证正/负已知结果。实现没有使用Python float64作为REAL的求值中间值。

提交前补查还发现 `CAST(-CAST(0.1 AS REAL) AS DOUBLE PRECISION)` 仍有差异，已将负号作为链中的独立操作保存，并补单测。早先44条通过不是最终唯一验收；最终准确代码重跑扩展后的47条和测试，结果见下文。

| 修复SHA | 父commit / 前置能力 | 本地/远程状态 |
| :--- | :--- | :--- |
| `365986d92f426fa6c837d3fc60ba6a41acd0770c` | `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；依赖已有数组类型、整数/Boolean及有限浮点输入基础 | 已本地commit，未push，无Issue/PR；整个task未完成 |

提交只含上面4个代码/测试文件，126增加/5删除，行为目标只有“保留已知REAL字面量转换顺序”。单次diff SHA256为 `62c4afd57e161117d870ea07b21b6580a67f7c9a0e6ea2ea5143fdb3342dd76d`。测试时的暂存树与提交树一致；提交后工作区干净，另外重跑161项方言定向测试通过。不是将其他未提交功能一起打包，也不把提交成功当task完成。

## 4. 双端执行与边界

### 4.1 执行和比较方法

在工作流根目录使用：

~~~bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../sqlglot-functional-commits:src \
  ../doris-sql-validator/.venv/bin/python -
~~~

内联Python批量调用 `parse_one(source, read="postgres").sql("doris", unsupported_level=ErrorLevel.RAISE)`，再用 `execute_query/compare_probe` 真正执行；不落盘临时SQL/脚本/执行JSON。每条源/目标各重复一次，10秒/10000行上限。边界用stage-01的 `dsv_wf_agg001_s01`，原Case按自身stage。

PG主流程沿用 `extra_float_digits=0`；精度补证对同一源SQL使用只读 `cursor(binary=True)`，不改主流程输出或比较策略。将实际二进制值用Decimal精确展开，在Doris内对实际生成查询的每个数组位置核验DOUBLE等值或IS NULL，并重复一次。多行边界用唯一id定位每行，数组内部始终按位置比较，保留NULL和重复次数，不排序数组制造一致。

47条全部取得成功状态、正确字段数量和显式别名、行数/数组形状、已取得FLOAT32/64类型映射、逐元素值/NULL及重复稳定证据。嵌套数组的PG OID不编码维度，另以实际嵌套记录和每层下标核验形状。带最终ORDER BY的运行时用例按唯一id检查顺序；其余无最终ORDER BY时不要求行排列一致。未验证负零的全部位级可观测行为、NaN或任意输入域，不称所有边界已覆盖。

### 4.2 最终47条明细

主比较器26条一致、21条不同；21条均另取得本轮原生等值证据，但主结论不修改。下表记录实际生成的完整目标SQL；OID1021/1022分别是PG FLOAT32/FLOAT64数组，23是INT32字段。目标声明来自EXPLAIN VERBOSE，不用协议STRING猜数组类型。

<details>
<summary>展开47条完整源SQL、生成SQL、类型与执行观察</summary>

| 变体标识 | 完整源SQL | 当前SQLGlot实际生成 | 源OID → Doris声明 | 主比较器行值 | 逐元素等值/NULL与重复执行 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| text-real-1 | `SELECT ARRAY['1e2',CAST('0.1' AS REAL),NULL,CAST('0.1' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('0.100000001490116119384765625' AS DOUBLE), NULL, CAST('0.100000001490116119384765625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-1 | `SELECT ARRAY[CAST(0.1 AS REAL),NULL,CAST(0.1 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), NULL, CAST('0.100000001490116119384765625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-1 | `SELECT ARRAY['1e2',CAST('0.1' AS REAL),2::DOUBLE PRECISION,NULL,CAST('0.1' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('0.100000001490116119384765625' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('0.100000001490116119384765625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-2 | `SELECT ARRAY['1e2',CAST('-0.1' AS REAL),NULL,CAST('-0.1' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('-0.100000001490116119384765625' AS DOUBLE), NULL, CAST('-0.100000001490116119384765625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-2 | `SELECT ARRAY[CAST(-0.1 AS REAL),NULL,CAST(-0.1 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('-0.100000001490116119384765625' AS DOUBLE), NULL, CAST('-0.100000001490116119384765625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-2 | `SELECT ARRAY['1e2',CAST('-0.1' AS REAL),2::DOUBLE PRECISION,NULL,CAST('-0.1' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('-0.100000001490116119384765625' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('-0.100000001490116119384765625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-3 | `SELECT ARRAY['1e2',CAST('7.038531e-26' AS REAL),NULL,CAST('7.038531e-26' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), NULL, CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| number-real-3 | `SELECT ARRAY[CAST(7.038531e-26 AS REAL),NULL,CAST(7.038531e-26 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), NULL, CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| promotes-double-3 | `SELECT ARRAY['1e2',CAST('7.038531e-26' AS REAL),2::DOUBLE PRECISION,NULL,CAST('7.038531e-26' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-4 | `SELECT ARRAY['1e2',CAST('1.0000000596046447753906250000000000001' AS REAL),NULL,CAST('1.0000000596046447753906250000000000001' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('1.00000011920928955078125' AS DOUBLE), NULL, CAST('1.00000011920928955078125' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-4 | `SELECT ARRAY[CAST(1.0000000596046447753906250000000000001 AS REAL),NULL,CAST(1.0000000596046447753906250000000000001 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('1.00000011920928955078125' AS DOUBLE), NULL, CAST('1.00000011920928955078125' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-4 | `SELECT ARRAY['1e2',CAST('1.0000000596046447753906250000000000001' AS REAL),2::DOUBLE PRECISION,NULL,CAST('1.0000000596046447753906250000000000001' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('1.00000011920928955078125' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('1.00000011920928955078125' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| text-real-5 | `SELECT ARRAY['1e2',CAST('1.000000059604644775390625' AS REAL),NULL,CAST('1.000000059604644775390625' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('1' AS DOUBLE), NULL, CAST('1' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-5 | `SELECT ARRAY[CAST(1.000000059604644775390625 AS REAL),NULL,CAST(1.000000059604644775390625 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('1' AS DOUBLE), NULL, CAST('1' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-5 | `SELECT ARRAY['1e2',CAST('1.000000059604644775390625' AS REAL),2::DOUBLE PRECISION,NULL,CAST('1.000000059604644775390625' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('1' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('1' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| text-real-6 | `SELECT ARRAY['1e2',CAST('1.000000178813934326171875' AS REAL),NULL,CAST('1.000000178813934326171875' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('1.0000002384185791015625' AS DOUBLE), NULL, CAST('1.0000002384185791015625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-6 | `SELECT ARRAY[CAST(1.000000178813934326171875 AS REAL),NULL,CAST(1.000000178813934326171875 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('1.0000002384185791015625' AS DOUBLE), NULL, CAST('1.0000002384185791015625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-6 | `SELECT ARRAY['1e2',CAST('1.000000178813934326171875' AS REAL),2::DOUBLE PRECISION,NULL,CAST('1.000000178813934326171875' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('1.0000002384185791015625' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('1.0000002384185791015625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-7 | `SELECT ARRAY['1e2',CAST('1e-40' AS REAL),NULL,CAST('1e-40' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE), NULL, CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| number-real-7 | `SELECT ARRAY[CAST(1e-40 AS REAL),NULL,CAST(1e-40 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE), NULL, CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| promotes-double-7 | `SELECT ARRAY['1e2',CAST('1e-40' AS REAL),2::DOUBLE PRECISION,NULL,CAST('1e-40' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('0.0000000000000000000000000000000000000000999994610111475958152591905227349949604220526961919185041279068749432712426283842432894743978977203369140625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| text-real-8 | `SELECT ARRAY['1e2',CAST('1e-45' AS REAL),NULL,CAST('1e-45' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE), NULL, CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| number-real-8 | `SELECT ARRAY[CAST(1e-45 AS REAL),NULL,CAST(1e-45 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE), NULL, CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| promotes-double-8 | `SELECT ARRAY['1e2',CAST('1e-45' AS REAL),2::DOUBLE PRECISION,NULL,CAST('1e-45' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('0.00000000000000000000000000000000000000000000140129846432481707092372958328991613128026194187651577175706828388979108268586060148663818836212158203125' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-9 | `SELECT ARRAY['1e2',CAST('3.4028234663852886e38' AS REAL),NULL,CAST('3.4028234663852886e38' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('340282346638528859811704183484516925440' AS DOUBLE), NULL, CAST('340282346638528859811704183484516925440' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| number-real-9 | `SELECT ARRAY[CAST(3.4028234663852886e38 AS REAL),NULL,CAST(3.4028234663852886e38 AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('340282346638528859811704183484516925440' AS DOUBLE), NULL, CAST('340282346638528859811704183484516925440' AS DOUBLE))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| promotes-double-9 | `SELECT ARRAY['1e2',CAST('3.4028234663852886e38' AS REAL),2::DOUBLE PRECISION,NULL,CAST('3.4028234663852886e38' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('340282346638528859811704183484516925440' AS DOUBLE), CAST(2 AS DOUBLE), NULL, CAST('340282346638528859811704183484516925440' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| text-real-10 | `SELECT ARRAY['1e2',CAST('-0' AS REAL),NULL,CAST('-0' AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('100' AS DOUBLE), CAST('-0' AS FLOAT), NULL, CAST('-0' AS FLOAT))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| number-real-10 | `SELECT ARRAY[CAST(-0 AS REAL),NULL,CAST(-0 AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST(-0 AS FLOAT), NULL, CAST(-0 AS FLOAT)) AS ARRAY<FLOAT>) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| promotes-double-10 | `SELECT ARRAY['1e2',CAST('-0' AS REAL),2::DOUBLE PRECISION,NULL,CAST('-0' AS REAL)] AS xs` | `SELECT CAST(ARRAY(CAST('100' AS DOUBLE), CAST('-0' AS FLOAT), CAST(2 AS DOUBLE), NULL, CAST('-0' AS FLOAT)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| double-real-midpoint | `SELECT ARRAY['1.0000000596046447753906250000000000001'::DOUBLE PRECISION::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('1' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| real-double-midpoint | `SELECT ARRAY['1.0000000596046447753906250000000000001'::REAL::DOUBLE PRECISION] AS xs` | `SELECT CAST(ARRAY(CAST('1.00000011920928955078125' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| negative-double-real-midpoint | `SELECT ARRAY['-1.0000000596046447753906250000000000001'::DOUBLE PRECISION::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('-1' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| negative-real-double-midpoint | `SELECT ARRAY['-1.0000000596046447753906250000000000001'::REAL::DOUBLE PRECISION] AS xs` | `SELECT CAST(ARRAY(CAST('-1.00000011920928955078125' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 一致 | 全部为真；稳定 |
| outer-double | `SELECT ARRAY['7.038531e-26'::REAL,2]::DOUBLE PRECISION[] AS xs` | `SELECT CAST(CAST(ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), 2) AS ARRAY<DOUBLE>) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| outer-real | `SELECT ARRAY[0.1::REAL,2::DOUBLE PRECISION]::REAL[] AS xs` | `SELECT CAST(ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), CAST(2 AS DOUBLE))) AS ARRAY<FLOAT>) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| outer-paren | `SELECT (ARRAY['7.038531e-26'::REAL,2])::DOUBLE PRECISION[] AS xs` | `SELECT CAST((CAST(ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), 2) AS ARRAY<DOUBLE>)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| nested-real | `SELECT ARRAY[ARRAY['7.038531e-26'::REAL,NULL::REAL],ARRAY[0.1::REAL,0.1::REAL]] AS xs` | `SELECT CAST(ARRAY(ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), CAST(NULL AS FLOAT))), ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), CAST('0.100000001490116119384765625' AS DOUBLE)))) AS ARRAY<ARRAY<FLOAT>>) AS xs` | 1021 → array<array<float>> | 不同 | 全部为真；稳定 |
| nested-double | `SELECT ARRAY[ARRAY['7.038531e-26'::REAL,2::DOUBLE PRECISION],ARRAY[0.1::REAL,0.1::REAL]] AS xs` | `SELECT CAST(ARRAY(CAST(ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>), ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), CAST('0.100000001490116119384765625' AS DOUBLE)))) AS ARRAY<ARRAY<DOUBLE>>) AS xs` | 1022 → array<array<double>> | 不同 | 全部为真；稳定 |
| outer-nested | `SELECT ARRAY[ARRAY['7.038531e-26'::REAL,1],ARRAY[0.1::REAL,NULL]]::DOUBLE PRECISION[][] AS xs` | `SELECT CAST(CAST(ARRAY(CAST(ARRAY(CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), 1) AS ARRAY<DOUBLE>), CAST(ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), NULL) AS ARRAY<DOUBLE>)) AS ARRAY<ARRAY<DOUBLE>>) AS ARRAY<ARRAY<DOUBLE>>) AS xs` | 1022 → array<array<double>> | 不同 | 全部为真；稳定 |
| unary-negative | `SELECT ARRAY[-0.1::REAL,NULL::REAL,-0.1::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(-CAST('0.100000001490116119384765625' AS DOUBLE), CAST(NULL AS FLOAT), -CAST('0.100000001490116119384765625' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| unary-negative-text | `SELECT ARRAY[-'7.038531e-26'::REAL,NULL::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(-CAST('0.00000000000000000000000007038530691851209120859188017140306974105991300039164570989669300615787506103515625' AS DOUBLE), CAST(NULL AS FLOAT))) AS xs` | 1021 → array<float> | 不同 | 全部为真；稳定 |
| parenthesized-negative | `SELECT ARRAY[(-0.1)::REAL,NULL::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('-0.100000001490116119384765625' AS DOUBLE), CAST(NULL AS FLOAT))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| ordered-duplicate-runtime | `SELECT CAST(id AS INT) AS id,ARRAY[0.1::REAL,CAST(x AS REAL),NULL,0.1::REAL] AS xs FROM (VALUES(1,2),(2,NULL),(3,2)) t(id,x) ORDER BY id` | `SELECT CAST(id AS INT) AS id, ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('0.100000001490116119384765625' AS DOUBLE), CAST(x AS FLOAT), NULL, CAST('0.100000001490116119384765625' AS DOUBLE))) AS xs FROM (SELECT 1 AS id, 2 AS x UNION ALL SELECT 2, NULL UNION ALL SELECT 3, 2) AS t ORDER BY id NULLS LAST` | 23/1021 → int/array<float> | 一致 | 全部为真；稳定 |
| neg-inside-cast-chain | `SELECT ARRAY[CAST(-CAST(0.1 AS REAL) AS DOUBLE PRECISION)] AS xs` | `SELECT CAST(ARRAY(CAST('-0.100000001490116119384765625' AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` | 1022 → array<double> | 不同 | 全部为真；稳定 |
| negative-number-midpoint | `SELECT ARRAY[(-1.0000000596046447753906250000000000001)::REAL] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('-1.00000011920928955078125' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |
| negative-number-double-real | `SELECT ARRAY[CAST(CAST(-1.0000000596046447753906250000000000001 AS DOUBLE PRECISION) AS REAL)] AS xs` | `SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST('-1' AS DOUBLE))) AS xs` | 1021 → array<float> | 一致 | 全部为真；稳定 |

</details>

### 4.3 直接相关源端负向

另查6条独立源变体：将 `1e400`、`1e-4000`、`bad` 分别用于下列两种完整查询：

~~~sql
SELECT ARRAY[CAST('1e400' AS REAL)] AS xs;
SELECT ARRAY[CAST('1e400' AS DOUBLE PRECISION)] AS xs;
~~~

前两种文本共4条源端报SQLSTATE `22003`（out of range），`bad`两条报 `22P02`（invalid input syntax）。这里是对明确列出的3种文本逐一替换执行的6条，不是SQLGlot Parser无法读源SQL。工具把22P02归在“语法解析失败”的粗分类，真实异常为InvalidTextRepresentation，应以原文解释为非法浮点输入。默认不进入修复清单，不额外运行目标追求同错误；未计入上述47条成功源边界。特殊/十六进制的源成功情况不能据此归为负向，前轮限制仍保留。

## 5. 原输入、既有边界与单元测试回归

原142条覆盖19个实际阶段，使用CliRunner在同一Python进程按阶段调用 `run --path <原stage YAML> --stdout`，同阶段重复 `--id`；读取原.out并真正执行目标，不另存验证JSON。142条逐ID与父状态一致，无缺失ID：82匹配、36 Doris执行失败、19行值/顺序不同、1转译失败、4源负向。不是313条/43阶段全量最终验收，未执行有后端风险记录的301/303/304。

task-001关联14条均包含在固定回归内，生成SQL/转译错误还从新代码与保留的原最终checkout逐条核对一致。该原checkout与父提交的内容一致已在提交重建时确认；没有用旧探查中缺失的VARIADIC目标SQL冒充新输出。

| 原Case / stage | 当前原.out比较结果 | 生成层核对 |
| :--- | :--- | :--- |
| [pg-aggregates-0010-12bf388c](../../../../attribution/cases/aggregates-001/pg-aggregates-0010-12bf388c.md) / 01 | 行值或顺序不匹配 | 生成SQL与父状态一致 |
| [pg-aggregates-0136-4243166e](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md) / 03 | SQLGlot 转译失败 | 保持相同unsupported错误 |
| [pg-aggregates-0306-e70870c4](../../../../attribution/cases/aggregates-001/pg-aggregates-0306-e70870c4.md) / 17 | 匹配 | 生成SQL与父状态一致 |
| [pg-aggregates-0410-f6f52dc3](../../../../attribution/cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md) / 31 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0411-b38c2a1f](../../../../attribution/cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md) / 31 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0412-cbdaef84](../../../../attribution/cases/aggregates-001/pg-aggregates-0412-cbdaef84.md) / 31 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0413-6ccabd9a](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) / 31 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0415-16b30942](../../../../attribution/cases/aggregates-001/pg-aggregates-0415-16b30942.md) / 31 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0434-5da33736](../../../../attribution/cases/aggregates-001/pg-aggregates-0434-5da33736.md) / 33 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0437-d68f01c2](../../../../attribution/cases/aggregates-001/pg-aggregates-0437-d68f01c2.md) / 33 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0438-998adec3](../../../../attribution/cases/aggregates-001/pg-aggregates-0438-998adec3.md) / 33 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0534-1b68ef98](../../../../attribution/cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) / 40 | Doris 执行失败 | 生成SQL与父状态一致 |
| [pg-aggregates-0551-f476de2c](../../../../attribution/cases/aggregates-001/pg-aggregates-0551-f476de2c.md) / 42 | 匹配 | 生成SQL与父状态一致 |
| [pg-aggregates-0552-7ea82af2](../../../../attribution/cases/aggregates-001/pg-aggregates-0552-7ea82af2.md) / 42 | 匹配 | 生成SQL与父状态一致 |

14条仍为3匹配、1显示差异、9目标执行失败、1转译拒绝。WITHIN GROUP、VARIADIC、RWAGG及外层SUM/CASE类型等历史问题保留；没有把新边界修复称为原输入匹配率提升。本轮未重新取得14条的全部实时字段元信息，历史类型观察见[fix-014第5节](../fix-014/task-001.md#5-原输入与已有修复回归)，不冒称已经再次全面验收。

| 其余回归 / 测试 | 本轮准确代码的实际结果 |
| :--- | :--- |
| 旧97条数组边界 | 双端成功、重复稳定；74值一致、23 Boolean显示差异，结果保持 |
| 旧41条浮点边界 | 全部原生等值/NULL核验及重复稳定通过；主比较25一致、15显示差异、1源文本驱动OverflowError保持，不计41条MATCH |
| unittest定向/核心 | Doris/PG/MySQL及expressions/parser/generator/transpile/tokens/build/schema/lineage：439方法通过，25.989秒 |
| 全部方言unittest discovery | 1084方法通过，4.807秒；与前项重叠，不相加 |
| commit后Doris/PG/MySQL定向 | 161方法通过，0.767秒 |
| Ruff与diff | 4个变动文件ruff check / format --check、git diff --check通过 |
| 完整optimizer、mypy、C扩展、make check | 未运行；未安装/升级依赖，不能写成全仓所有测试通过 |

单测命令使用 `../sqlglot-experiment/.venv/bin/python` 和 `PYTHONPATH=$PWD`，通过unittest loader运行上述模块/discovery，PATH加入该venv以供lazy-load子进程。运行时实际import均为 `../sqlglot-functional-commits/sqlglot/__init__.py`。数据库进程用旧验证器venv，版本字符串 `30.25.1.dev6`；单测venv版本字符串 `30.25.1.dev355`。安装元数据不同，不能只凭该字符串判断源码；完整commit和准确提交树为本轮代码身份。

## 6. 剩余反例、下一步和完成判断

额外5条控制中，连续CAST中间负号的遗漏已补入本轮；另一条负数字面量链也通过。以下两类当前仍有真实差异，不归为显示问题：

| 当前源SQL / 范围 | 真实执行证据 | 去向 |
| :--- | :--- | :--- |
| `SELECT ARRAY[(SELECT 0.1::REAL),2::DOUBLE PRECISION] AS xs` | PG二进制第一元素0.10000000149011612；当前生成目标原生等值为[0,1]，重复稳定 | 继续task-001：标量子查询边界内先转换后提升 |
| `SELECT CAST(id AS INT) AS id,ARRAY[CAST(x AS REAL),2::DOUBLE PRECISION] AS xs FROM (VALUES(1,'0.1'),(2,NULL),(3,'7.038531e-26')) t(id,x) ORDER BY id` | id1/id3的首元素原生等值为0，NULL行两元素为真；数组元素是实际列转换，不是显示差异 | 同task的运行时转换研究；不靠Schema猜值，也不认定一次失败证明不可修 |

对照 `SELECT ARRAY[(SELECT 0.1::REAL)] AS xs` 当前原生值相同，说明不能把所有子查询一概标错；差异与外层类型提升相关。运行时控制的工具“最终行顺序不同”是整行值比较也失败的综合提示，实际id已按1/2/3排列，不能据此单独断言排序缺陷。

下一轮优先处理**无FROM、仅单一可信常量投影的标量子查询**：在不越过一般查询作用域的前提下，保留投影REAL字面量的源舍入再参与外层共同类型。已实际执行下列独立Doris候选，得到ARRAY<DOUBLE>且原生等值[1,1]：

~~~sql
SELECT CAST(ARRAY((SELECT CAST('0.100000001490116119384765625' AS DOUBLE)), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs
~~~

它只是下一轮可行性证据，**不是本轮生成器已实现的输出**。方案已补入统一task条目：仅考虑该有限标量形状，排除表查询/相关查询/聚合/窗口/集合/多行等；先检查表达式类型保留和外层转换顺序，补子查询NULL/别名/括号、FLOAT/DOUBLE、中点/次正规数和作用域隔离测试，继续跑当前47条、旧97+41及142条回归。运行时列、非有限/十六进制、NUMERIC、未知类型和task-003仍另需研究/验收，不在本轮顺带实现。

当前task-001未完成验收；全批仍7项完成约定验收、2项已修改但未完成验收，整份输入未完成。此次只提交已验证的有限字面量行为，未push；没有新增候选文件、执行JSON、日志、patch或证据目录。

