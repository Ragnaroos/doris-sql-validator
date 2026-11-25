# task-001 / fix-016：数组构造输入转换

## 1. 结论与范围

**状态：已修改但未完成验收。** 本轮连续实现并验收四项限定规则，保存为五个本地 commit（四项规则，加非有限输入保护补漏）；不是在一个小例子通过后交付。整个 task-001 尚有运行时文本→REAL、NUMERIC 与未知类型等余项，不能关闭。

沿用 [统一任务条目](../../../../attribution/aggregates-001-attribution-summary.md#task-001) 及原关联 14 条，不新增 task 编号。共同环境、权限、原输入与完整回归见 [本轮汇总](../../../aggregates-001-fix-016-summary.md)。原 Case 的完整源 SQL 继续见 [fix-015 第5节](../fix-015/task-001.md#5-原输入既有边界与单元测试回归) 及其链接；本轮不复制输入、YAML、.out 或首轮报告。

仅修改 PG 类型已明确的数组构造生成路径和测试。不是全局 CAST 修复，不强制 Schema，不实现 ARRAY(SELECT...)、文本数组解析、下界、UNNEST、UDF 或其他 task。方案在改代码前追加到统一 task 条目；中途发现新路径后，先补方案再实施。

## 2. 实际实现与提交

| 本地完整 SHA | 独立行为 | 父 commit |
| :--- | :--- | :--- |
| `6e92c3f330ea17d6458baf656c7731012dfec95b` | 有限标量投影中的 REAL 输入保持源转换顺序 | `365986d92f426fa6c837d3fc60ba6a41acd0770c` |
| `be74c6b42e63d129d6aa116bab90bac46abc6394` | 十六进制浮点规范化，复用源 IEEE 最近偶数舍入 | `6e92c3f330ea17d6458baf656c7731012dfec95b` |
| `9c3b30efc6aedaf54c3327d44f4ca231d39e3d97` | 接受完整合法拼写的 NaN/±Infinity 浮点输入 | `be74c6b42e63d129d6aa116bab90bac46abc6394` |
| `ce841540a49228d9114a0346abc84283abcbe4c2` | 显式 DOUBLE→REAL 运行时转换在数组提升前执行 | `9c3b30efc6aedaf54c3327d44f4ca231d39e3d97` |
| `6922457c6d223eafb1e3e7c1aaab211f88487874` | 非有限拼写限 ASCII，补齐本轮保护遗漏 | `ce841540a49228d9114a0346abc84283abcbe4c2` |

均在 `../sqlglot-functional-commits` 的 `codex/doris-functional-commits` 分支，本地已提交、未 push。每项代码及测试在不包含下一项修改的父子状态下验收后提交，最终工作区干净；没有把四项混成一个总 commit，也未重写既有历史。

| 文件 / 位置 | 规则与限制 |
| :--- | :--- |
| `sqlglot/generators/doris.py / _coerce_array_input` | 不再用 unnest 跨过标量子查询；仅处理无 FROM、无其他查询修饰、单投影的有限形状，复制并保留查询/别名。复用已有字面量 CAST 顺序；不把外层类型传播进一般查询。 |
| 同函数的运行时 CAST 链 | 仅输入已由显式 DOUBLE 确立、再转 REAL 的链，使用单元素 ARRAY_MAP→取回元素强制运行时转换；保留后续 CAST 和中间负号。输入表达式只出现一次，不猜未知 x 的类型。 |
| `_array_float_input / _PG_HEX_FLOAT_INPUT` | 十六进制尾数与二进制指数先组成精确整数比，再按源 FLOAT32/64 最近偶数舍入。支持可选指数、大小写和符号，避免通过 Python float64 中转 REAL。 |
| `_array_float_input` 的非有限分支 | 接受完整 NaN/Inf/Infinity 拼写及允许的符号/空白；不将有限溢出转为 Infinity，不接受 nans、infi、nan(payload) 等不在本规则内的拼写。 |
| `tests/dialects/test_doris.py` | 新增四个参数化方法：标量 REAL、十六进制、非有限输入、运行时 DOUBLE→REAL；检查生成 SQL、AST 不变、dump/load、相关 round-trip、作用域隔离、一次求值与非法输入保护。 |

本轮未修改 PG Parser、公共 AST、公共 Generator、其他方言、框架或数据。依赖既有数组源类型/输入转换基础及 fix-015 的有限 REAL CAST 链；新提交不是无前置依赖的任意 cherry-pick 补丁。

## 3. 修复前后与真实执行

下列“修复后”均由最终 SQLGlot 从所列源 SQL 生成并实际执行，不是手写候选替代验收。

### 3.1 标量子查询中的 REAL→DOUBLE

~~~sql
-- 源
SELECT ARRAY[(SELECT 0.1::REAL),2::DOUBLE PRECISION] AS xs;

-- 修复前实际生成
SELECT CAST(ARRAY((SELECT CAST(0.1 AS FLOAT)), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs;

-- 修复后实际生成
SELECT CAST(ARRAY((SELECT CAST('0.100000001490116119384765625' AS DOUBLE)), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs;
~~~

PG 二进制第一元素为 `0.10000000149011612`；旧目标是 `0.1`。修复后目标显示 `0.1000000014901161`，目标内提升为 DOUBLE 后与 PG 精确可表示值等值，第二元素及数组长度也通过。主比较器因源文本读取/目标显示精度仍报告不同，未修改该结论。

只改无 FROM、无其他查询修饰的单投影；有 WHERE、LIMIT、FROM、集合或聚合的控制不把该规则推过去。实际零行标量子查询 `SELECT ARRAY[(SELECT 0.1::REAL WHERE FALSE)] AS xs` 仍返回一个 NULL 元素，不用常量替代查询结果。

### 3.2 十六进制浮点

~~~sql
-- 源
SELECT ARRAY[1::REAL, '0x1.000002p0',NULL] AS xs;

-- 修复前
-- UnsupportedError: Doris cannot preserve this PostgreSQL array input conversion

-- 修复后实际生成
SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST(1 AS FLOAT), CAST('1.00000011920928955078125' AS DOUBLE), NULL)) AS xs;
~~~

PG 源成功。Doris 直接 CAST 原十六进制文本实测返回 NULL，不是源 SQL 错误；规范化后原生元素等值及类型通过。半舍入点 `0x1.000001p0` 与略大于它的 `0x1.0000010000000000000001p0` 结果不同，已覆盖，不用 float64 先舍入再模拟 REAL。

保留最多 4096 字符、十六进制指数绝对值最多 20000 的工作量保护；有限非零输入溢出或舍入为零时仍不在此输入转换规则内。部分受保护的长合法输入仍可能被拒绝，不能把这些全部当源负向，也不宣称支持任意长度。

### 3.3 非有限输入

~~~sql
-- 源
SELECT ARRAY[1::REAL,'NaN',NULL,'NaN'] AS xs;

-- 修复前
-- UnsupportedError: Doris cannot preserve this PostgreSQL array input conversion

-- 修复后实际生成
SELECT ARRAY_MAP(_pg_array_value -> CAST(_pg_array_value AS FLOAT), ARRAY(CAST(1 AS FLOAT), CAST('NaN' AS DOUBLE), NULL, CAST('NaN' AS DOUBLE))) AS xs;
~~~

PG 与目标均有两个 NaN，NULL 位置、长度、顺序和 FLOAT32 类型可核对。目标用 `ISNAN` 检查 NaN 类别，Infinity 用 `ISINF` 加正负号检查，不拿 NaN=NaN 作证明，不验证 NaN payload/符号位。原比较器对非有限值的结构化对象/文本表示仍有差异，16 条全部保留“不同”。

本轮收尾审查发现 Python 的 Unicode IGNORECASE 还会接受 `İnf`、`ınf`；PG 实测均 SQLSTATE 22P02，属于源负向。第三项规则增加 ASCII 限制和两个拒绝测试，用第五个补漏 commit 保存，不将两条源负向计入 89 条成功源变体或新增 task。最终提交重新执行全部方言、定向/核心及数据库回归。

### 3.4 运行时 DOUBLE→REAL

~~~sql
-- 源
SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs
FROM (VALUES ('0.1')) t(x);

-- 修复前实际生成
SELECT CAST(ARRAY(CAST(CAST(x AS DOUBLE) AS FLOAT), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs
FROM (SELECT '0.1' AS x) AS t;

-- 修复后实际生成
SELECT CAST(ARRAY(ARRAY_MAP(_pg_real_input -> CAST(_pg_real_input AS FLOAT), ARRAY(CAST(x AS DOUBLE)))[1], CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs
FROM (SELECT '0.1' AS x) AS t;
~~~

单元素 ARRAY_MAP 保留运行时 FLOAT32 值后再进入 DOUBLE 数组，PG 的 `0.10000000149011612` 不再被 `0.1` 替代。DOUBLE→REAL 与文本直接→REAL 的中点行为不同，不能删除源端的 DOUBLE CAST。

额外四行原文如下，实际执行两次：
~~~sql
SELECT id::INT AS id,ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs
FROM (VALUES (1,'0.1'),(2,NULL),(3,'7.038531e-26'),(4,'0.1')) t(id,x)
ORDER BY id;
~~~

id 仍为 1/2/3/4；第 1/4 行重复数组保持，第 2 行首元素 NULL；第 3 行源值为 `7.038531308148791e-26`，不同于文本直接 REAL 的值，目标按源链保留了这个差异。逐行原生核验及行数、重复计数、稳定 id 顺序通过。没有把带 DOUBLE 的查询偷偷改成直接 REAL 的答案。

## 4. 检查方法与逐条范围

- 默认生成：`parse_one(source, read="postgres").sql("doris", unsupported_level=ErrorLevel.RAISE)`；不传 Schema，不增加框架重写。
- PG 使用只读二进制游标取得真实 FLOAT32/64 值，另保留原工具的文本读取比较；目标字段声明来自实际 EXPLAIN VERBOSE，不根据 MySQL 协议 STRING 猜型。
- 对数组长度、每层维度、各位置的值/NULL 逐项检查；有限浮点在目标内转 DOUBLE，与 PG 二进制值的精确十进制表示比较。数组内重复与位置都保留，非有限数单独分类。
- 两端实际查询及目标内核验均重复执行。多行用原生谓词计数核对多重集合，有稳定最终 ORDER BY 的查询补查 id 顺序。
- PG OID 1021/1022 对应 FLOAT32/FLOAT64 数组；本轮每条新变体与目标 array<float>/array<double> 及已知嵌套深度可对齐。工具直接比较原生声明拼写仍可能报告不同，不把这个粗标签当作实测位宽不同。
- 验证只覆盖这些输入；不证明全部输入域、全部查询顺序、NaN payload 或有符号零位级一致性。

新 89 条均源成功、目标成功、原生值核验通过且重复稳定；主比较器 **37 一致、51 不同、1 无行值结论**。最后一项是最大 DOUBLE 在 PG 文本驱动读取时的已知 OverflowError，二进制读取及原生核验成功，不是源负向。

<details>
<summary>89 条完整源 SQL、类型与本轮结果</summary>

| 变体 | 完整源 SQL | PG 数组 OID → 目标原生类型 | 主比较器行值 | 原生值 / 重复执行 |
| :--- | :--- | :--- | :--- | :--- |
| scalar-mixed | `SELECT ARRAY[(SELECT 0.1::REAL),2::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| scalar-alias | `SELECT ARRAY[(SELECT 0.1::REAL AS value)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-neg | `SELECT ARRAY[(SELECT -0.1::REAL)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-nested-query | `SELECT ARRAY[(SELECT (SELECT 0.1::REAL))] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-midpoint | `SELECT ARRAY[(SELECT '1.0000000596046447753906250000000000001'::REAL),2::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| scalar-double-first | `SELECT ARRAY[(SELECT '1.0000000596046447753906250000000000001'::DOUBLE PRECISION::REAL),2::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| scalar-subnormal | `SELECT ARRAY[(SELECT '1e-45'::REAL)] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| scalar-scientific | `SELECT ARRAY[(SELECT '7.038531e-26'::REAL),2::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| scalar-nested-array | `SELECT ARRAY[ARRAY[(SELECT 0.1::REAL)],ARRAY[(SELECT -0.1::REAL)]] AS xs` | 1021 → `array<array<float>>` | 一致 | 通过 / 稳定 |
| scalar-null-duplicate | `SELECT ARRAY[(SELECT NULL::REAL),(SELECT 0.1::REAL),(SELECT 0.1::REAL)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-zero-rows-control | `SELECT ARRAY[(SELECT 0.1::REAL WHERE FALSE)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-exact-control | `SELECT ARRAY[(SELECT 0.5::REAL)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| scalar-outer-cast | `SELECT ARRAY[(SELECT 0.1::REAL)]::DOUBLE PRECISION[] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-basic-REAL | `SELECT ARRAY[1::REAL, '0x1.000002p0',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-basic-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1.000002p0',NULL] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-no-power-REAL | `SELECT ARRAY[1::REAL, '0x1',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-no-power-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1',NULL] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-fraction-REAL | `SELECT ARRAY[1::REAL, '0X.8',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-fraction-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0X.8',NULL] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-neg-REAL | `SELECT ARRAY[1::REAL, '-0x1.8p+01',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-neg-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '-0x1.8p+01',NULL] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-half-REAL | `SELECT ARRAY[1::REAL, '0x1.000001p0',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-half-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1.000001p0',NULL] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-above-half-REAL | `SELECT ARRAY[1::REAL, '0x1.0000010000000000000001p0',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-above-half-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1.0000010000000000000001p0',NULL] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-max-REAL | `SELECT ARRAY[1::REAL, '0x1.fffffep127',NULL] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| hex-max-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1.fffffep127',NULL] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-subnormal-REAL | `SELECT ARRAY[1::REAL, '0x1p-149',NULL] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| hex-subnormal-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '0x1p-149',NULL] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-signed-zero-REAL | `SELECT ARRAY[1::REAL, '-0x0p0',NULL] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-signed-zero-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION, '-0x0p0',NULL] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-double-min | `SELECT ARRAY[1::DOUBLE PRECISION,'0x1p-1074'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| hex-double-max | `SELECT ARRAY[1::DOUBLE PRECISION,'0x1.fffffffffffffp1023'] AS xs` | 1022 → `array<double>` | 源文本驱动解码失败 | 通过 / 稳定 |
| hex-real-cast-double | `SELECT ARRAY['0x1.0000010000000000000001p0'::REAL,2::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-double-cast | `SELECT ARRAY['0x1.0000000000001p0'::DOUBLE PRECISION] AS xs` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| hex-scalar-hex | `SELECT ARRAY[(SELECT '0x1.8p0'::REAL)] AS xs` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| hex-nested-hex | `SELECT ARRAY[ARRAY[1::REAL,'0x1.000002p0'],ARRAY[NULL::REAL,'-0x.8']] AS xs` | 1021 → `array<array<float>>` | 一致 | 通过 / 稳定 |
| nonfinite-NaN-REAL | `SELECT ARRAY[1::REAL,'NaN',NULL,'NaN'] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite-NaN-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,'NaN',NULL,'NaN'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite-+nAn-REAL | `SELECT ARRAY[1::REAL,'+nAn',NULL,'+nAn'] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite-+nAn-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,'+nAn',NULL,'+nAn'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite--NaN-REAL | `SELECT ARRAY[1::REAL,'-NaN',NULL,'-NaN'] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite--NaN-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,'-NaN',NULL,'-NaN'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite- inf -REAL | `SELECT ARRAY[1::REAL,' inf ',NULL,' inf '] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite- inf -DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,' inf ',NULL,' inf '] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite-+INF-REAL | `SELECT ARRAY[1::REAL,'+INF',NULL,'+INF'] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite-+INF-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,'+INF',NULL,'+INF'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite--infinity-REAL | `SELECT ARRAY[1::REAL,'-infinity',NULL,'-infinity'] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite--infinity-DOUBLE PRECISION | `SELECT ARRAY[1::DOUBLE PRECISION,'-infinity',NULL,'-infinity'] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite-real-cast | `SELECT ARRAY['NaN'::REAL,'-Infinity'::REAL] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite-cast-promotion | `SELECT ARRAY['-Infinity'::REAL,2::DOUBLE PRECISION,'NaN'::REAL] AS xs` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| nonfinite-scalar | `SELECT ARRAY[(SELECT 'NaN'::REAL)] AS xs` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| nonfinite-nested | `SELECT ARRAY[ARRAY[1::REAL,'NaN'],ARRAY[NULL::REAL,'-inf']] AS xs` | 1021 → `array<array<float>>` | 不同 | 通过 / 稳定 |
| runtime-real-0 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('0.1')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-promote-0 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('0.1')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-0 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('0.1')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-0 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('0.1')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-real-1 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('7.038531e-26')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-promote-1 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('7.038531e-26')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-1 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('7.038531e-26')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-1 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('7.038531e-26')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-real-2 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('1.0000000596046447753906250000000000001')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-promote-2 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('1.0000000596046447753906250000000000001')) t(x)` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| runtime-neg-2 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('1.0000000596046447753906250000000000001')) t(x)` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| runtime-chain-2 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('1.0000000596046447753906250000000000001')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-real-3 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('1e-45')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-promote-3 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('1e-45')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-3 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('1e-45')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-3 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('1e-45')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-real-4 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('3.4028234663852886e38')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-promote-4 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('3.4028234663852886e38')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-4 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('3.4028234663852886e38')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-4 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('3.4028234663852886e38')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-real-5 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('-0.1')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-promote-5 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('-0.1')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-5 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('-0.1')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-5 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('-0.1')) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-real-6 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('Infinity')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-promote-6 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('Infinity')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-6 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('Infinity')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-6 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('Infinity')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-real-7 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('NaN')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-promote-7 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES ('NaN')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-neg-7 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES ('NaN')) t(x)` | 1022 → `array<double>` | 不同 | 通过 / 稳定 |
| runtime-chain-7 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES ('NaN')) t(x)` | 1021 → `array<float>` | 不同 | 通过 / 稳定 |
| runtime-real-8 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL] AS xs FROM (VALUES (NULL)) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |
| runtime-promote-8 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL,2::DOUBLE PRECISION] AS xs FROM (VALUES (NULL)) t(x)` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| runtime-neg-8 | `SELECT ARRAY[(-x::DOUBLE PRECISION)::REAL::DOUBLE PRECISION] AS xs FROM (VALUES (NULL)) t(x)` | 1022 → `array<double>` | 一致 | 通过 / 稳定 |
| runtime-chain-8 | `SELECT ARRAY[x::DOUBLE PRECISION::REAL::DOUBLE PRECISION::REAL] AS xs FROM (VALUES (NULL)) t(x)` | 1021 → `array<float>` | 一致 | 通过 / 稳定 |

</details>

## 5. 既有边界、原查询与测试

既有 185 条的完整源 SQL 直接读取 [fix-012](../fix-012/task-001.md)、[fix-013](../fix-013/task-001.md)、[fix-014](../fix-014/task-001.md)、[fix-015](../fix-015/task-001.md) 对应表，不手工改动 SQL。重跑两端均成功、重复稳定；原比较器分别为：

| 来源 / 数量 | 行值一致 | 行值不同 | 无行值结论 |
| :--- | ---: | ---: | ---: |
| fix-012 / 37 | 36 | 1 | 0 |
| fix-013 新扩展 / 60 | 38 | 22 | 0 |
| fix-014 / 41 | 25 | 15 | 1 |
| fix-015 / 47 | 26 | 21 | 0 |
| 合计 185 | 125 | 59 | 1 |

178 条单行数组先通过原生元素核验；其余 7 条包括 SQL NULL 数组与多行结果，另以实际输出名、原生 WHERE 谓词计数核对，不忽略重复行。fix-012 的 9/13/14/37 及后三轮 runtime-null-order/ordered-duplicate-runtime 全部值与计数通过，带唯一 id 排序的四条也保持实际顺序。独立 id 的 PG INT/Doris TINYINT 以及 Decimal 结果声明等既有类型余项没有因此关闭。

原输入实际重跑 310 条、43 阶段，排除后端风险 Case 0301/0303/0304；原关联 14 条当前结果如下。它们的完整源 SQL 仍见原 Case 文档，不替换为下面的新边界。

| 原 Case / 阶段 | 当前结果 | 实际错误或限制 |
| :--- | :--- | :--- |
| 0010 / 01 | 行值或顺序不匹配 | PG 文本数组显示与目标 JSON 数组显示不同，原 .out 不放宽 |
| 0136 / 03 | SQLGlot 转译失败 | UnsupportedError: Doris does not support ARRAY subquery constructors；任务排除范围 |
| 0306 / 17 | 匹配 | Recorded Output 无原生类型；历史外层 SUM NUMERIC/BIGINT 差异不因此消失 |
| 0410/0411/0412/0413/0415 / 31 | 5 条 Doris 执行失败 | 原 WITHIN GROUP 调用实际报 missing 'BY' at '('，位置分别 76/66/89/97/60 |
| 0434/0437/0438 / 33 | 3 条 Doris 执行失败 | VARIADIC 调用实际报 mismatched input 'ARRAY' expecting {')', ',', 'ORDER'}，位置 26/27/37 |
| 0534 / 40 | Doris 执行失败 | Can not found function 'RWAGG' |
| 0551/0552 / 42 | 2 条匹配 | 外层 CASE 等原生类型余项仍保留，未重新声明全类型一致 |

本轮起点的 Doris Generator 从 Git 只读加载到内存，与最终生成结果逐条比较，可解析原查询生成 SQL/错误无变化。没有在磁盘保存源码副本，不将该生成层核对写成起点的双端执行回归。扩展 310 条有 82 匹配、25 源负向、64 值/顺序差异、119 Doris 执行失败、12 环境标签、8 转译失败；分母、分类限制和具体环境错误解释见本轮汇总。

最终代码的 443 项定向/核心、1088 项全部方言测试通过，二者重叠不相加。新增四个 unittest 方法含多个参数变体，不是新增 443/1088 条 SQL。每个功能提交前的准确父子状态测试、PATH 环境失败及重跑说明见汇总；本轮未运行完整 optimizer、mypy、C 扩展或 make check。

## 6. 剩余问题与下一步

### 6.1 未知文本列直接转 REAL：仍未解决

~~~sql
SELECT ARRAY[x::REAL,2::DOUBLE PRECISION] AS xs
FROM (VALUES ('7.038531e-26')) t(x);
~~~

PG 原生首元素为 `7.038530691851209e-26`。原直接 CAST 不一致；独立候选把文本放到 `ARRAY_MAP(v -> CAST(v AS FLOAT), ARRAY(x))[1]` 后，仍得到 `7.038531308148791e-26`。另一文本中点 `1.0000000596046447753906250000000000001`，该候选返回 1，但 PG 直接 REAL 为 1.0000001192092896。不能因为 `0.1` 通过就推广这个候选。

第四项修复只针对**显式 DOUBLE 再 REAL**，源端本来就要求先按 DOUBLE 舍入，因此不是上述直接文本转换的替代答案。静态字面量可以精确解析，运行时列不能在转译时预计算；未知列也不能猜成文本/DOUBLE。

下一步继续原 task-001 的该子项，先调查目标是否有直接 FLOAT32 输入入口，或能在不改变原类型/输入域的条件下安全实现单次舍入。要求覆盖普通值、中点两侧、次正规数、NULL、多行与原生位宽，并验证运行时路径；若只能解决有显式源类型或有限输入域的部分，必须公开限定，不新增“全覆盖”结论。没有已验证的通用候选前不提交一个只对普通值正确的补丁。若需要改 Doris、添加 Schema 前提或改变数据/比较契约，超出本轮权限，先说明再申请。

### 6.2 NUMERIC：区分可补的有限范围与目标类型限制

本轮只读复核如下，不把一次默认 CAST 失败归为“Doris 完全不能表示这个数”。

| 源与独立目标检查 | 实际结果 | 去向 |
| :--- | :--- | :--- |
| `ARRAY['NaN'::NUMERIC(10,2)]` | PG Decimal NaN，目标 DECIMAL(10,2) 为 NULL；PG 结果 typmod 655366 | NUMERIC 非有限值不能用 FLOAT NaN 冒充，后者已改变结果类型 |
| `ARRAY['Infinity'::NUMERIC]` | PG Decimal Infinity，目标默认 Decimal 为 NULL | 无约束 NUMERIC 非有限域的目标类型限制 |
| `ARRAY[1e40::NUMERIC]` | PG 精确 1e40，默认 Decimal 为 NULL | 默认精度不够，不是 1e40 在 Doris 完全不可表示 |
| 独立 `DECIMAL(41,0)` 候选承载 1e40 | 目标实际成功、精确返回 1e40 | 有限精度路径可以继续研究；单样本值正确不等于保留无约束 NUMERIC 域 |
| `DECIMAL(76,0)` 承载 1e80 | 目标返回 NULL；`DECIMAL(77,0)` 声明报 precision should in (0, 76] | 目标可表示域有界，不能用固定 Decimal 完整冒充源无约束域 |
| `ARRAY[NULL::NUMERIC(10,2),1.25::NUMERIC(10,2)]` | 两端当前值及源 typmod 655366 可核对 | 本身已可运行，不重复制造修复 |
| 明确 NUMERIC(39,0) 的 39 位数 | 当前目标成功返回完整值，PG typmod 2555908 | 不能仅因 enable_decimal256=false 就伪造失败；保留本版本实际观察 |

负 Scale 的源合法语法还有既有 Parser 缺口，见 fix-013 的 NUMERIC(3,-1) 证据；它属于通用类型语法/映射研究，不夹入本轮数组浮点提交。无约束结果没有 typmod 并不证明当前某个 CAST 的有限范围无效，但不能据此宣称目标完整覆盖源域。

### 6.3 其他限制和独立问题

- 无 Schema 的未知列/参数/一般表达式不能安全恢复全部 PG 求型；既有推型仅在可信类型上生效，不能为了让输出同形就统一 INT/DOUBLE。
- 有 FROM、过滤、集合、聚合、多行及关联作用域的标量查询没有被第一项跨作用域改写。相关 REAL 值转换仍需独立评估，不因为简单投影通过就全部关闭。
- 十六进制输入仍有工作量限制；有符号零仅核验数值为零，未宣称位级一致；非有限数未证明 PG/Doris 下游所有比较和聚合规则相同。
- 原 WITHIN GROUP、VARIADIC、RWAGG、SUM/CASE/VALUES 类型及 ARRAY(SELECT...) 不是本任务数组构造规则。原 14 条整句未全匹配，不能为了凑数扩大当前提交。
- 扩展原输入里的 ONLY 修饰、缺表等问题不属于本轮数组规则，也没有因此自动修改数据或实现其他 task。框架“环境问题”是初步标签，具体归因需读错误和生成 SQL。

**本轮停止点不是“已完成一个 commit”或“报告写完”，而是四项可独立安全验证的规则已实现，剩余运行时文本/无约束类型问题尚无经过核验的通用实现；不能用已失败的 CAST/lambda 候选继续冒充修复。** task-001 继续保持未验收。下一轮从 `6922457c6d223eafb1e3e7c1aaab211f88487874` 与本节恢复研究，不重新读取最初全部材料，不重复开 task；未对外推送。

