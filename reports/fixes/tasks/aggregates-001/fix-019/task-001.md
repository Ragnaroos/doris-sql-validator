# task-001 / fix-019：NUMERIC 数组输入与显式转换

## 1. 范围与当前状态

本轮持续处理原task-001的类型/转换余项，不改框架、比较器、原SQL/.out、YAML或数据。本轮起点3c9e4bb004bff47a4ca8b750961f5e4470076590，实际checkout为../sqlglot-functional-commits、分支codex/doris-functional-commits；原工作区干净。只允许功能本地commit，不push、不创建Issue/PR。具体实施前方案和新增反例已先写入[统一清单](../../../../attribution/aggregates-001-attribution-summary.md#task-001)。共同版本、最终回归及整份输入状态见[汇总](../../../aggregates-001-fix-019-summary.md)。

状态：**已修改但未完成整个task的验收**。本轮五项功能均已保存为独立本地commit，最终合并回归已完成。下面56条是新补的边界/控制，不替代原14条，也不计入原313条匹配率。34条相对本轮起点消除了转译失败、执行失败或值/Scale差异，22条原本就正确；这不是原输入新增34条MATCH。运行时文本直接REAL和一般NUMERIC类型域等余项仍未解决，见第8节。

## 2. 功能拆分与真实提交

| 功能 | commit / 父commit | 实现与证据范围 |
| :--- | :--- | :--- |
| 显式固定NUMERIC(p,s)数组CAST | ba7fb6989650ae4e1662a29669b9001df44728dc / 3c9e4bb004bff47a4ca8b750961f5e4470076590 | 保留(p,s)，用精确输入文本在运行时转换，避免数组先经DOUBLE；17条A组 |
| 显式NUMERIC元素CAST先于数组共同类型 | 5ec631410471210358e164b98a107e963abeee2f / ba7fb6989650ae4e1662a29669b9001df44728dc | 保留中间CAST和舍入，避免大数数组收窄为38位；13条B组 |
| 数组内高精度NUMERIC取负 | 58135f86a50fc449ca45a3b6d7e5393d3e55665c / 5ec631410471210358e164b98a107e963abeee2f | 先执行原CAST，再在规范数值文本上切换符号，回到NUMERIC；仅数组内，9条C组 |
| NUMERIC与unknown字符串共同输入 | fcc68bb35fc49628692cb270b256403e82b9c539 / 58135f86a50fc449ca45a3b6d7e5393d3e55665c | 源共同类型明确为NUMERIC，不再生成TEXT数组；仅有限、统一原Scale，9条D组 |
| 无约束NUMERIC[]构造CAST | d0c2e9ea1e187edc157f96657313982ce7929e09 / fcc68bb35fc49628692cb270b256403e82b9c539 | 不追加目标默认(38,9)而再次补零/溢出；有限可证明域，8条E组 |

修改文件：sqlglot/generators/doris.py的cast_sql、_array_cast_types、_bounded_numeric_array_sql；sqlglot/parsers/postgres.py的_array_element_type；配套tests/dialects/test_doris.py和test_postgres.py。公共Generator、其他源方言、普通标量CAST/Neg不作全局改写；不猜列Schema。最终输出仍是NUMERIC/DECIMAL数组，内部字符串仅承载精确输入，不把结果改成字符串制造匹配。

PG同型显式NUMERIC元素保留固定typmod；未知NULL/字符串或不同精度混合时不能继承某个成员的固定Scale。此处依据实际PG二进制元数据核对，不从to字符串猜类型。原型中的Neg高精度失败已独立留给第三项，不混成第二项已完成；第三项已用实际生成SQL修复该控制。

## 3. 已复现的错误和代表性生成SQL

- 整数组CAST前：ARRAY[1e40,2]::NUMERIC(50,0)[]得到10000000000000000302727418506697047212060，而非精确10^40。
- 元素CAST前：两个NUMERIC(40,0)构造收窄为array<decimalv3(38,0)>，39位数变NULL。
- 取负控制：ARRAY[-CAST(1e40 AS NUMERIC(50,0))]报scale should not smaller than 0, but real scale is -12。不是BE崩溃；旧直接负号路径同样有此问题。
- 混合NUMERIC/unknown字符串前：NUMERIC数组错误变成array<text>，例如[1.25,'2.00']返回字符串元素。
- 无约束数组CAST前：目标默认DECIMAL(38,9)，1.25变成1.250000000；1e40变NULL。

```sql
-- A01源
SELECT ARRAY[1e40,2]::NUMERIC(50,0)[] AS xs;
-- 实际生成
SELECT CAST(ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(50, 0)),
  ARRAY('10000000000000000000000000000000000000000', '2')) AS ARRAY<DECIMAL(50, 0)>) AS xs;

-- B04源：两次舍入不能折成一次
SELECT ARRAY['1.245'::NUMERIC(6,2)::NUMERIC(6,1)] AS xs;
-- 实际生成，结果1.3，不是直接(6,1)得到的1.2
SELECT ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(6, 1)),
 ARRAY(CAST(ARRAY_MAP(_pg_numeric_cast_0 -> CAST(_pg_numeric_cast_0 AS DECIMAL(6, 1)),
 ARRAY(CAST(ARRAY_MAP(_pg_numeric_cast_1 -> CAST(_pg_numeric_cast_1 AS DECIMAL(6, 2)),
 ARRAY('1.245'))[1] AS STRING)))[1] AS STRING))) AS xs;

-- D02源
SELECT ARRAY[1.25,'2.00'] AS xs;
-- 实际生成，元素仍为NUMERIC
SELECT ARRAY_MAP(_pg_numeric_input -> CAST(_pg_numeric_input AS DECIMAL(3, 2)), ARRAY('1.25', '2.00')) AS xs;
```

## 4. 新边界与控制的完整源SQL

编号仅用于本报告定位，不是新的框架Case ID。A固定数组CAST、B元素CAST、C取负、D混合输入、E无约束数组CAST。没有生成这些变体的YAML/.out；实际源真值来自本轮只读PG。所有目标SQL由修改后的SQLGlot从下表源语句生成，未用手写目标答案。

| 编号 | 侧重 | 完整源SQL |
| :--- | :--- | :--- |
| A01 | wide | `SELECT ARRAY[1e40,2]::NUMERIC(50,0)[] AS xs` |
| A02 | wide-p-only | `SELECT ARRAY[1e40,2]::NUMERIC(50)[] AS xs` |
| A03 | mixed-scale | `SELECT ARRAY[1.25,2]::NUMERIC(10,2)[] AS xs` |
| A04 | text-round | `SELECT ARRAY['1.235','-2.345',NULL]::NUMERIC(6,2)[] AS xs` |
| A05 | carry-round | `SELECT ARRAY[9.995,-9.995]::NUMERIC(4,2)[] AS xs` |
| A06 | even-ties | `SELECT ARRAY[1.225,-1.225,1.235,-1.235]::NUMERIC(6,2)[] AS xs` |
| A07 | nested | `SELECT ARRAY[[1e40,2],[3,NULL]]::NUMERIC(50,0)[][] AS xs` |
| A08 | scale76 | `SELECT ARRAY[1e-76,NULL]::NUMERIC(76,76)[] AS xs` |
| A09 | precision76 | `SELECT ARRAY[9999999999999999999999999999999999999999999999999999999999999999999999999999,NULL]::NUMERIC(76,0)[] AS xs` |
| A10 | nulls | `SELECT ARRAY[NULL,NULL]::NUMERIC(50,0)[] AS xs` |
| A11 | empty | `SELECT ARRAY[]::NUMERIC(50,0)[] AS xs` |
| A12 | radix | `SELECT ARRAY['0x10','0b11','0o17','-0Xff']::NUMERIC(6,2)[] AS xs` |
| A13 | underscore | `SELECT ARRAY['1_2.3_4','+1.2e+1_0']::NUMERIC(20,2)[] AS xs` |
| A14 | zero | `SELECT ARRAY[-0.0000,0e-4,0]::NUMERIC(10,4)[] AS xs` |
| A15 | paren | `SELECT (ARRAY[1e40,2])::NUMERIC(50,0)[] AS xs` |
| A16 | multirow | `SELECT unique1::INT AS id,ARRAY[1e40,unique1::INT,NULL]::NUMERIC(50,0)[] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` |
| A17 | outer-query | `SELECT xs FROM (SELECT ARRAY[1e40,2]::NUMERIC(50,0)[] AS xs) t` |
| B01 | wide-elements | `SELECT ARRAY[123456789012345678901234567890123456789::NUMERIC(40,0),2::NUMERIC(40,0)] AS xs` |
| B02 | precise-elements | `SELECT ARRAY[1.234567890123456789::NUMERIC(30,18),NULL::NUMERIC(30,18)] AS xs` |
| B03 | scalar-rounding | `SELECT ARRAY['1.235'::NUMERIC(6,2),'-2.345'::NUMERIC(6,2)] AS xs` |
| B04 | double-rounding | `SELECT ARRAY['1.245'::NUMERIC(6,2)::NUMERIC(6,1)] AS xs` |
| B05 | array-second-round | `SELECT ARRAY['1.245'::NUMERIC(6,2)]::NUMERIC(6,1)[] AS xs` |
| B06 | typed-nulls | `SELECT ARRAY[NULL::NUMERIC(50,0),NULL::NUMERIC(50,0)] AS xs` |
| B07 | untyped-null | `SELECT ARRAY[1e40::NUMERIC(50,0),NULL] AS xs` |
| B08 | different-precision | `SELECT ARRAY[1.20::NUMERIC(6,2),2.00::NUMERIC(10,2)] AS xs` |
| B09 | nested-elements | `SELECT ARRAY[[1e40::NUMERIC(50,0),2::NUMERIC(50,0)],[3::NUMERIC(50,0),NULL::NUMERIC(50,0)]] AS xs` |
| B10 | p-only | `SELECT ARRAY[1e40::NUMERIC(50),2::NUMERIC(50)] AS xs` |
| B11 | scale76 | `SELECT ARRAY[1e-76::NUMERIC(76,76),NULL::NUMERIC(76,76)] AS xs` |
| B12 | runtime-integer | `SELECT unique1::INT AS id,ARRAY[(unique1::INT)::NUMERIC(50,0),NULL::NUMERIC(50,0)] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` |
| B13 | runtime-text | `SELECT unique1::INT AS id,ARRAY[(CASE WHEN unique1%2=0 THEN '1.235' ELSE '-2.345' END)::NUMERIC(6,2),NULL::NUMERIC(6,2)] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` |
| C01 | neg-wide | `SELECT ARRAY[-CAST(1e40 AS NUMERIC(50,0))] AS xs` |
| C02 | neg-negative | `SELECT ARRAY[-CAST(-1e40 AS NUMERIC(50,0))] AS xs` |
| C03 | double-neg | `SELECT ARRAY[-(-CAST(1e40 AS NUMERIC(50,0)))] AS xs` |
| C04 | null | `SELECT ARRAY[-CAST(NULL AS NUMERIC(50,0))] AS xs` |
| C05 | zero | `SELECT ARRAY[-CAST(0.0049 AS NUMERIC(6,2))] AS xs` |
| C06 | rounding | `SELECT ARRAY[-CAST('1.245' AS NUMERIC(6,2))::NUMERIC(6,1)] AS xs` |
| C07 | nested-sign | `SELECT ARRAY[[-CAST(1e40 AS NUMERIC(50,0)),-CAST(NULL AS NUMERIC(50,0))],[-CAST(-1e40 AS NUMERIC(50,0)),-CAST(0 AS NUMERIC(50,0))]] AS xs` |
| C08 | precision76 | `SELECT ARRAY[-CAST(9999999999999999999999999999999999999999999999999999999999999999999999999999 AS NUMERIC(76,0))] AS xs` |
| C09 | runtime | `SELECT unique1::INT AS id,ARRAY[-CAST((CASE WHEN unique1%2=0 THEN '1.235' ELSE '-2.345' END) AS NUMERIC(6,2))] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` |
| D01 | large-unknown | `SELECT ARRAY[9223372036854775808,'18446744073709551616',NULL] AS xs` |
| D02 | decimal-unknown | `SELECT ARRAY[1.25,'2.00'] AS xs` |
| D03 | unknown-first | `SELECT ARRAY['1.20',2.00] AS xs` |
| D04 | cast-unknown | `SELECT ARRAY[1.20::NUMERIC(6,2),'2.00'] AS xs` |
| D05 | radix | `SELECT ARRAY[9223372036854775808,'0x_ff','1_000'] AS xs` |
| D06 | nested | `SELECT ARRAY[[9223372036854775808,'0x10'],[2,NULL]] AS xs` |
| D07 | scientific | `SELECT ARRAY[1e40,'2e40'] AS xs` |
| D08 | repeat | `SELECT ARRAY[1.25,'1.25',NULL,'1.25'] AS xs` |
| D09 | space-sign | `SELECT ARRAY[1.25,'  +2.00  ','-3.50'] AS xs` |
| E01 | text-numeric | `SELECT ARRAY['1.25','2.00']::NUMERIC[] AS xs` |
| E02 | wide-numeric | `SELECT ARRAY[1e40,2]::NUMERIC[] AS xs` |
| E03 | null-numeric | `SELECT ARRAY[NULL,NULL]::NUMERIC[] AS xs` |
| E04 | empty-numeric | `SELECT ARRAY[]::NUMERIC[] AS xs` |
| E05 | nested-numeric | `SELECT ARRAY[ARRAY['1.25','2.00'],ARRAY['3.50',NULL]]::NUMERIC[][] AS xs` |
| E06 | parentheses | `SELECT (ARRAY[1e40,2])::NUMERIC[] AS xs` |
| E07 | keep-rounding | `SELECT ARRAY['1.245'::NUMERIC(6,2)]::NUMERIC[] AS xs` |
| E08 | large-text | `SELECT ARRAY['9223372036854775808','18446744073709551616']::NUMERIC[] AS xs` |

## 5. 验证方式与证据边界

加载既有.env但不输出凭据，数据库解释器../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-functional-commits:src；SQLGlot单测解释器../sqlglot-experiment/.venv/bin/python，PYTHONDONTWRITEBYTECODE=1。两端均原dsv_wf_agg001_s31；源用只读二进制cursor、10秒statement_timeout，目标execute_query(..., timeout=10, row_limit=10000)及EXPLAIN。比较完整有限结果、Decimal精确值和str(Decimal)表示的Scale、NULL、数组位置/重复、显式别名、必要最终ORDER BY，重复两端查询验证稳定。不改主框架.out显示文本规则；Doris数组文本用Decimal解析，不经float。

固定源typmod解码为(p,s)，对照目标EXPLAIN的decimalv3(p,s)；typmod=-1意味着源无固定约束，不当作元数据遗漏。即使本次值相同，目标有界DECIMAL也不是PG无约束NUMERIC的整个类型域，需单列而非宣称完整类型匹配。

首次单测中发现旧NUMERIC CAST测试只断言原样输出，已随新增功能更新预期，保留AST不变和往返验证。第四项首次补丁未应用到白名单时，新单测失败，补齐后才继续；这些不是数据库通过证据。每项精确内容先测试、再commit，不在未提交功能上叠加下一项。

## 6. 最终HEAD的实际核验

最终解释器确认：`sqlglot.__file__=../sqlglot-functional-commits/sqlglot/__init__.py`，版本`30.25.1.dev6`，HEAD `d0c2e9ea1e187edc157f96657313982ce7929e09`，受版本控制的工作区干净。本轮五项修改只涉及第2节的四个文件，合计270行增加、15行删除；没有把旧experiment工作区的修改重新算成本轮修复。

### 6.1 56条边界的值、类型与稳定性

| 比较维度 | 最终结果 | 限制 |
| :--- | :--- | :--- |
| 源端/目标成功、字段数量与显式别名 | 56/56通过 | 每条SQL均实际执行；不是只检查生成文本 |
| 完整有限行值、Decimal精确值与Scale、NULL、数组位置和重复次数 | 56/56通过 | 不使用浮点容差、不删除尾零、不丢弃重复元素 |
| 双端重复执行、必要最终顺序 | 56/56稳定 | A16、B12、B13、C09按唯一id排序；其他单行数组保留内部顺序 |
| 源有固定typmod的数组声明 | 28/28 precision/scale与目标原生声明对应 | A组17条，B组除B07/B08外11条；嵌套层数也保留 |
| 源无固定typmod的NUMERIC声明 | 28条不能宣称全类型域相等 | B07/B08及C/D/E组；PG typmod=-1并非驱动丢失信息，目标仍是有界DECIMAL |

最终批处理首次汇总的类型正则多写了转义，错误打印了固定声明不匹配；原生类型和typmod采集本身正常。随后对保留的实际元组按整数precision/scale重新核对，28条均对应。没有修改SQL/数据库/正式比较器以取得这一结果。

为了量化实际改进，在内存中读取`git show 3c9e4bb:sqlglot/parsers/postgres.py`与`sqlglot/generators/doris.py`，加载历史Parser/Generator生成旧目标SQL，再恢复最终类生成新SQL。同一批56条源SQL、同一数据库和读取方法，不修改checkout、不保存历史副本：

| 本轮起点对这56条的结果 | 数量 | 最终HEAD |
| :--- | ---: | :--- |
| 值/Scale原本相同的控制 | 22 | 22条保持相同 |
| 值、Scale或元素类型表示不同 | 26 | 26条值/Scale相同，元素为NUMERIC/DECIMAL而非错误TEXT |
| 目标执行失败 | 7 | 7条执行成功且值/Scale相同 |
| SQLGlot严格转译失败 | 1 | 1条执行成功且值/Scale相同 |
| 合计 | 56 | 56条均取得本次值/Scale证据 |

该历史控制仅替换两份本轮确实改变的生产模块，其他依赖未变；它是起点源码控制，不冒称当前进程的HEAD曾切回旧版本。28条无约束NUMERIC不能因为此表通过就写成完整类型等价。

### 6.2 既有数组边界回归

从[fix-017第4节](../fix-017/task-001.md#4-实际sql与比较范围)提取原75条完整SQL，原样从最终SQLGlot生成并双端重复执行：

- 75条均执行成功且重复稳定；62条构造/控制的原生值、Decimal Scale和NULL相同。
- 另13条`decimal-text-1`至`decimal-text-13`仍为源文本非NULL、目标NULL，原因是源`[1]`被生成成目标`[0]`，保持归入task-010；本轮没有更改用户数组下标。
- BIGINT/DOUBLE按各自原生类型解码，Decimal才按Decimal读取。首次临时补证把所有JSON数字都读成Decimal，造成两个控制的假差异；纠正诊断解码后重跑75条取得上述结果。正式框架、原.out和比较规则均未改变。
- 该75条集合与本轮56条有重叠，不能相加成131条唯一查询，也不是原输入新增覆盖数。

## 7. 原输入和测试结果

### 7.1 原task-001关联14条

在原阶段YAML执行`run --path <实际阶段YAML> --stdout`，以同一进程按阶段批量调用CLI、同阶段重复传`--id`，不生成新验证文件：

| 原Case语句编号 | 结果 | 仍存在的原因或限制 |
| :--- | :--- | :--- |
| 0306、0551、0552 | 3条匹配 | 沿用.out比较结论；外层SUM/CASE等已知类型差异不因此消失 |
| 0010、0410、0411、0412、0413、0415 | 6条行值/顺序不同 | 原.out的PG数组花括号显示与Doris方括号显示不同；之前已取得的结构化/原生补证见前轮，未放宽比较器制造MATCH |
| 0434、0437、0438 | 3条Doris执行失败 | `VARIADIC ARRAY(...)`调用形式被目标拒绝，具体为`mismatched input 'ARRAY' expecting {')', ',', 'ORDER'}`，分别pos26/27/37；不是数组括号构造规则未生效 |
| 0534 | 1条Doris执行失败 | `Can not found function 'RWAGG'`，依赖PG测试自定义聚合，不用数组CAST规则伪造其实现 |
| 0136 | 1条转译失败 | `ARRAY(SELECT...)`子查询构造不在本轮已验收的字面量/有限表达式构造范围 |

14条整体分类与fix-018保持相同。逐条原SQL、阶段和首轮Case入口沿用统一任务清单，不改写首轮证据。不能将原生构造规则的改善说成14条全部完整验收。

### 7.2 43阶段的固定范围回归

对43个原阶段YAML共313条逐ID比较起点/最终代码：**313条生成SQL或严格转译错误均未改变**。然后实际执行310条安全原查询；0301/0303/0304沿用既有BE风险排除，未执行，不把313当执行分母。

| 原比较规则下的结果 | 数量 |
| :--- | ---: |
| 匹配 | 82 |
| 源端负向用例 | 25 |
| 行值或顺序不匹配 | 69 |
| Doris执行失败 | 114 |
| Doris环境问题（框架原分类，非本轮重新根因判定） | 12 |
| SQLGlot转译失败 | 8 |
| 实际执行/处理合计 | 310 |

与fix-018的固定范围分类数量相同；成功源结果分母285，匹配82/285=28.77%。本轮未增加原输入MATCH，不能将34条新增边界的修复移入该分母。原.out只是可用文本证据，不提供所有原生类型；上述匹配不是静态证明所有输入同义。源端负向单列，不因本轮安排逐条错误复刻或加入主修复清单。

### 7.3 自动测试与提交后的检查

SQLGlot工作目录均为`../sqlglot-functional-commits`，使用`../sqlglot-experiment/.venv/bin/python`且`PYTHONDONTWRITEBYTECODE=1`：

```bash
# 最终功能提交前的相同代码内容
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" ../sqlglot-experiment/.venv/bin/python -m unittest discover -s tests/dialects -t .
# 1103条通过；此前每个功能父commit也分别通过相关测试，见第2节提交顺序。

# 最终commit后
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" ../sqlglot-experiment/.venv/bin/python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.test_expressions tests.test_parser tests.test_generator tests.test_serde tests.test_transpile
# 314条通过（与1103集合重叠，不相加）。

PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" ruff check sqlglot/generators/doris.py sqlglot/parsers/postgres.py tests/dialects/test_doris.py tests/dialects/test_postgres.py
PATH="$PWD/../sqlglot-experiment/.venv/bin:$PATH" ruff format --check sqlglot/generators/doris.py sqlglot/parsers/postgres.py tests/dialects/test_doris.py tests/dialects/test_postgres.py
git diff --check
git status --short
```

Ruff检查及格式通过、diff检查通过、工作区干净。没有运行完整optimizer/integration/C扩展或完整`make check`，不声称全项目所有测试通过；当前测试环境没有mypy，未做该静态类型验收，没有安装或升级依赖。

## 8. 剩余问题、停止依据与恢复条件

这不是“完成一个commit就停止”。同一次调用已连续复现、实现、验收并提交五种独立规则，再做最终固定范围回归；下面问题没有用改答案、改Session、换STRING结果或提前拒绝冒充解决。

### 8.1 运行时未知文本直接转换REAL

[fix-017第5节](../fix-017/task-001.md#5-运行时文本直接real仍未解决)已有40个有限候选和对应源码证据，没有得到同时保留普通值、极小数、中点和最大值的通用运行时路径。本轮最终HEAD再次从真实tenk1构造两条各四行反例，目标由当前SQLGlot生成：

```sql
SELECT unique1::INT AS id,
 ARRAY[(CASE WHEN unique1%2=0 THEN '7.038531e-26' ELSE '0.1' END)::REAL,
       2::DOUBLE PRECISION] AS xs
FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1;

SELECT unique1::INT AS id,
 ARRAY[(CASE WHEN unique1%2=0 THEN '1.0000000596046447753906250000000000001'
             ELSE '0.1' END)::REAL, 2::DOUBLE PRECISION] AS xs
FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1;
```

PG二进制读取的偶数行首元素分别为`7.038530691851209e-26`、`1.0000001192092896`，奇数行均为`0.10000000149011612`。当前生成仍是`CAST(ARRAY(CAST(CASE ... AS FLOAT), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>)`。目标文本协议的数字显示本身不足以判定真实差异，因此另外把**实际生成SQL**作为子查询，在Doris内部验证：

```sql
-- <generated>是上面每条源SQL的实际生成结果，不是替代候选；这只是元素诊断。
-- 第一条even值为7.038530691851209e-26，第二条为1.0000001192092896。
SELECT id,
 xs[1] = CAST(CASE WHEN id % 2 = 0 THEN '<even>'
                  ELSE '0.10000000149011612' END AS DOUBLE) AS exact_value_matches
FROM (<generated>) p ORDER BY id;
```

两条的4个等值标志均为0，说明不只是输出显示精度。这里目标原生`xs[1]`只做诊断，不是修改task-010，也没有替换修复验收SQL。此前字面量REAL和显式DOUBLE→REAL的已验收实现不能冒称解决本入口。

目前没有经过验证的通用安全SQLGlot改写；不证明所有可能SQL算法都不可能。继续需要找到/验证不经DOUBLE丢失中点信息的FLOAT32运行时入口或算法。若只能修改Doris解析/转换实现、添加UDF或改变输入类型前提，超出本次权限，需额外授权。本轮不重复40条旧包装、也不重放任何已知崩溃候选来凑进度。

### 8.2 NUMERIC类型域和可观察Scale

以下是**能力控制**，不是声称由当前SQLGlot生成并验收的修复SQL；原文和实际结果均在本轮只读执行：

```sql
-- PG
SELECT x::TEXT AS v FROM UNNEST(ARRAY[1.25,2]) u(x) ORDER BY x;
-- Doris固定Scale能力控制
SELECT CAST(x AS STRING) AS v
FROM UNNEST(CAST(ARRAY(1.25,2) AS ARRAY<DECIMAL(3,2)>)) u(x) ORDER BY x;
```

PG返回`1.25`、`2`，Doris返回`1.25`、`2.00`。显式整个数组`::NUMERIC(10,2)[]`可以统一Scale，已经纳入本轮A组；**没有该源CAST时不能擅自补零再称全语义等价**。一般NUMERIC数组每个元素的Scale以及无约束类型域无法通过一个固定DECIMAL声明完全照搬；不以“数值相等”抹掉文本转换等下游可观察差异。

- PG `SELECT ARRAY[1e76] AS xs`成功，实际为77位整数。Doris能力控制`SELECT ARRAY_MAP(x -> CAST(x AS DECIMAL(77,0)), ARRAY('1e76')) AS xs`报`precision should in (0, 76], but real precision is 77`。不能降成DOUBLE/STRING还声称相同NUMERIC输出。
- PG `SELECT ARRAY['NaN'::NUMERIC(10,2)] AS xs`返回NUMERIC NaN。Doris控制`SELECT ARRAY_MAP(x -> CAST(x AS DECIMAL(10,2)), ARRAY('NaN')) AS xs`返回`[null]`，并非等价NULL。已有FLOAT NaN支持不能代替NUMERIC NaN契约。
- 28条typmod=-1的本轮成功边界仍是有限数据上的值/Scale成功，不意味着Doris新增无约束NUMERIC。未知列、一般NUMERIC表达式没有可靠Schema或值域前提时，不猜类型/精度；负Scale、Scale大于precision、ARRAY子查询等未覆盖能力不打包进本轮五项转换。

依据[PG18 NUMERIC说明](https://www.postgresql.org/docs/18/datatype-numeric.html)与[Doris4.x DECIMAL说明](https://doris.apache.org/docs/4.x/sql-manual/basic-element/sql-data-types/numeric/DECIMAL/)，两者类型域及Scale规则并不相同。官方Doris文档还区分decimal256开关；本机原设置`enable_decimal256=false`下，某些显式运行时CAST计划实际取得50/76位声明与正确值，已经记录实际证据，**不把这些有限成功推广到所有算子或其他版本/配置**，不改Session强行扩大通过范围。

### 8.3 当前任务清单与交付边界

task-001保持“已修改但未完成验收”；不是把上述余项全部认定为SQLGlot一定不能解决，也不以先拒绝算已修复。继续入口是本节的直接REAL运行时实现研究和一般NUMERIC可保留契约；有新安全路径时在原task追加具体方案与验收，不重复修已通过的有限NUMERIC规则。task-010下标、task-003聚合类型及VARIADIC/UDF等独立能力不在本次选定范围，不自动实施。

当前可安全实现且取得本轮证据的五项已提交；其余已知问题在既有安全替代失败或目标类型契约限制下，尚无已验证、可在当前权限中交付的通用实现。故停止重复尝试，保留未完成状态和上述恢复条件，不承诺会话结束后后台继续。最终Doris查询成功，阶段31 tenk1仍10000行；未重建、重装数据或重启容器。全部五个commit只在本地，未push/创建Issue/PR。

