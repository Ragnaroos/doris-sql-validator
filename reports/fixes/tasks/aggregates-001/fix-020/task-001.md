# task-001 / fix-020：源类型职责与文本子数组输入

## 1. 结论、范围与语义依据

整个task-001状态仍为“已修改但未完成验收”。本轮完成两个独立行为：源Parser不再受Doris转换白名单控制；在可靠PG数组类型上下文中转换一维文本子数组输入。不是以原aggregates.sql零报错为目标，不把提前拒绝或边界数当可执行转换完成。首轮/前轮报告不改写。

入口：[统一task清单](../../../../attribution/aggregates-001-attribution-summary.md#task-001)；[本轮汇总](../../../aggregates-001-fix-020-summary.md)；原14条Case及43阶段材料沿用该清单链接。实施前方案已写在原task-001条目中。

源依据：[PG18 ARRAY构造](https://www.postgresql.org/docs/18/sql-expressions.html#SQL-SYNTAX-ARRAY-CONSTRUCTORS)与[共同类型规则](https://www.postgresql.org/docs/18/typeconv-union-case.html)：unknown输入由已知共同类型决定转换；外层数组CAST还会影响内部构造。规则由源SQL和源类型确定，不依据数据库快照、预期输出、文件名或Case ID。

适用范围：目标上下文已可靠确定为SMALLINT/INT/BIGINT/TEXT/BOOLEAN一维子数组，输入是PG普通或已由Tokenizer解码的E字符串字面量；采用默认边界、逗号分隔的一维输入语法。未知列不猜Schema、一般运行时文本不当字面量解析，显式下界、多维文本以及FLOAT/NUMERIC子数组文本不在本次新增转换范围。源array_nulls=on、standard_conforming_strings=on已只读确认；非默认array_nulls语义不宣称支持。

这是一项源语义转换，使用目标原生ARRAY/CAST，没有新增lambda、取负文本算法或引擎Bug包装。E字符串进入此前已存在的NUMERIC/FLOAT转换时仅复用旧规则；其版本补偿通用性并未因此验收，见第7节。

## 2. 真实提交和实现

起点：d0c2e9ea1e187edc157f96657313982ce7929e09。checkout：../sqlglot-functional-commits，分支codex/doris-functional-commits，授权fork https://github.com/Ragnaroos/sqlglot.git。允许本地按功能commit、不push、不创建Issue/PR，不改变数据/原SQL/.out/YAML、框架或Session政策。

| commit | 父commit | 行为与文件 |
| :--- | :--- | :--- |
| 0d1d795278d5666cf5756f696f44f20d63dfed53 | d0c2e9ea1e187edc157f96657313982ce7929e09 | PostgresParser::_array_element_type移除Doris支持白名单，先明确首项非None再共同推型；PG AST/往返/序列化/多目标不变性及Doris诊断测试。3文件，44增/16删 |
| 12b98b50836cad4d4a49e968894f4570ca4b9a52 | 0d1d795278d5666cf5756f696f44f20d63dfed53 | 把已有一维PG数组词法helper复用到dialects/dialect.py::parse_postgres_array_literal；PG原TEXT[]解析显式保留类型，Doris::_coerce_array_input按最终类型构造子数组；PG escape字符串按unknown类型，已解码文本复用既有输入转换；配套测试。5文件，193增/74删 |

两项分别在父commit上完成测试和只读取证再提交，不把同轮全部修改打包；最终工作区干净，全部未push。共享helper移动与目标消费属于同一个输入语法能力，不另造重复解析器，不从Generator调用PG Parser。改写仅发生在目标生成时的副本，不修改原AST；特别保留源外层TEXT[][]要求的前导零。

## 3. 修复前后和实际生成SQL

源成功：
```sql
SELECT ARRAY[ARRAY[1,2],'{3,4}'] AS xs;
```

起点丢失外层类型提示，实际生成：
```sql
SELECT ARRAY(CAST(ARRAY(1, 2) AS ARRAY<INT>), '{3,4}') AS xs;
```
Doris只读实际报错：`Can not find the compatibility function signature: array(ARRAY<INT>, VARCHAR(5))`。TEXT控制同样报`array(ARRAY<TEXT>, VARCHAR(5))`。两者均为PG成功源，不是源负向。

第一项commit后PG AST保留ARRAY<INT>/ARRAY<TEXT>，Doris严格生成暂报`Doris cannot preserve this PostgreSQL array input conversion`。当时只验收源信息和诊断职责，不称已能执行。

第二项最终实际生成：
```sql
SELECT CAST(
  ARRAY(CAST(ARRAY(1, 2) AS ARRAY<INT>),
        CAST(ARRAY(CAST('3' AS INT), CAST('4' AS INT)) AS ARRAY<INT>))
  AS ARRAY<ARRAY<INT>>) AS xs;
```
两端原生值均为[[1,2],[3,4]]，PG元素OID1007，目标array<array<int>>；别名xs、维度、NULL/位置与重复保持。不是读取源结果后把答案替换进目标，3/4来自源字面量的词法内容。

外层CAST的关键反例：
```sql
SELECT ARRAY[ARRAY[1,2],'{01,02}']::TEXT[][] AS xs;
```
PG与最终目标均返回[['1','2'],['01','02']]。生成保留`ARRAY('01', '02')`，不先插入INT CAST丢掉前导零。说明不能仅凭内层暂定INT类型提前改写源AST。

## 4. 已执行的20条源变体

均为本轮边界，不新增原输入Case/YAML/.out，不进入原313条分母。源真值来自PG18.1二进制只读查询，所有目标由当前SQLGlot从以下原文生成。S07有4行，其余各1行；S07按唯一id排序，所有二维数组均逐位置及完整维度核验。

| 编号 | 完整源SQL |
| :--- | :--- |
| S01 | `SELECT ARRAY[ARRAY[1,2],'{3,4}'] AS xs` |
| S02 | `SELECT ARRAY['{3,4}',ARRAY[1,2]] AS xs` |
| S03 | `SELECT ARRAY[(ARRAY[1,2]),'{3,4}'] AS xs` |
| S04 | `SELECT ARRAY[ARRAY['a','b'],'{c,d}'] AS xs` |
| S05 | `SELECT ARRAY[ARRAY[2147483648,2],'{3,4}'] AS xs` |
| S06 | `SELECT ARRAY[(SELECT ARRAY[1,2]),'{3,4}'] AS xs` |
| S07 | `SELECT unique1::INT AS id,ARRAY[ARRAY[unique1::INT,(CASE WHEN unique1%2=0 THEN NULL ELSE unique1 END)::INT],'{3,4}'] AS xs FROM tenk1 WHERE unique1 IN (0,1,2,3) ORDER BY unique1` |
| S08 | `SELECT ARRAY[ARRAY[1,2],'{01,02}']::TEXT[][] AS xs` |
| S09 | `SELECT ARRAY[ARRAY[TRUE,FALSE],'{yes,NULL}'] AS xs` |
| S10 | `SELECT ARRAY[ARRAY['a',NULL],'{NULL,"NULL"}'] AS xs` |
| S11 | `SELECT ARRAY[ARRAY['a,b',' x '],'{"a,b"," x "}'] AS xs` |
| S12 | `SELECT ARRAY[ARRAY[1::SMALLINT,2::SMALLINT],'{-32768,32767}'] AS xs` |
| S13 | `SELECT ARRAY[ARRAY[1,2],'{-2147483648,2147483647}'] AS xs` |
| S14 | `SELECT ARRAY[ARRAY[2147483648,2],'{-9223372036854775808,9223372036854775807}'] AS xs` |
| S15 | `SELECT ARRAY[ARRAY[1,2],'{0x10,1_000}'] AS xs` |
| S16 | `WITH t AS (SELECT ARRAY[ARRAY[1,2],'{3,4}'] AS xs) SELECT xs FROM t` |
| S17 | `SELECT ARRAY[ARRAY['a','b'],'{"",NULL}'] AS xs` |
| S18 | `SELECT ARRAY[ARRAY[1,1],'{1,1}'] AS xs` |
| S19 | `SELECT ARRAY[ARRAY['a','b'], E'{"a\\"b","c\\\\d"}'] AS xs` |
| S20 | `SELECT ARRAY[ARRAY['a','b'], E'{N\\ULL,NULL}'] AS xs` |

20条原目标执行及别名均成功。S01–S20全部取得相应原生元素类型、完整有限行值、NULL、数组维度/位置/重复和必要行序证据，并双端重复稳定。叶类型映射按实际证据：PG1005→SMALLINT，1007→INT，1016→BIGINT，1009→TEXT，1000→BOOLEAN；不要求物理名称逐字相同。

### 4.1 原生核验方法与显示差异

工作流目录，以../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-functional-commits:src，PYTHONDONTWRITEBYTECODE=1加载原.env（不输出凭据）。PG cursor(binary=True)、default_transaction_read_only=on、statement_timeout=10s；Doris pg_probe.execute_query(...,timeout=10,row_limit=100)，原阶段库dsv_wf_agg001_s31，原UTC/严格转换配置不变。

先实际执行SQLGlot生成的完整目标SQL，读取别名及EXPLAIN类型；再对该实际表达式做只读诊断投影：
```sql
SELECT ARRAY_SIZE(xs) AS n, ARRAY_SIZE(xs[1]) AS n1, ARRAY_SIZE(xs[2]) AS n2,
       xs[1][1] AS v1, xs[1][2] AS v2, xs[2][1] AS v3, xs[2][2] AS v4
FROM (<实际生成SQL>) p;
```
S07另保留id并ORDER BY id。这里是Doris原生1-based诊断，不是经SQLGlot转译用户下标，也不是代替生成SQL的手写候选；task-010未实施。每行全部元素和三个维度均与源二进制值核对，Boolean仅在原生字段确认为boolean后做0/1逻辑解码；正式Comparator不变。

S19的数组显示含双引号，Doris原数组文本不能直接json.loads，初次临时补证在此中断，未把截断/未读的S20算通过。最终20条均用上述原生投影重新完整执行，S19/S20正确保留引号/反斜杠及转义NULL。原投影S19的值为源相同的a、b、含引号文本和含反斜杠文本，不对实际元素额外转义以制造JSON。此显示问题可能仍影响框架文本比较，不冒充框架MATCH。

### 4.2 escape字符串的额外兼容控制

新增源unknown类型分类影响其他已知标量数组输入，因此补查以下5条，不只测试子数组成功：
```sql
SELECT ARRAY[1,E'0x10'] AS xs;
SELECT ARRAY[TRUE,E'yes'] AS xs;
SELECT ARRAY[1.25,E'2.00'] AS xs;
SELECT ARRAY[CAST(E'1.235' AS NUMERIC(6,2)),NULL::NUMERIC(6,2)] AS xs;
SELECT ARRAY[1::REAL,E'0.1'] AS xs;
```
5条均执行成功并重复稳定；原生投影分别为[1,16]、[true,true]、[1.25,2.00]、[1.24,NULL]、[1.0,0.10000000149011612]，位置/长度2正确。最后一条用目标内部与源二进制精确DOUBLE值的等值标志核验，两个标志均1，不因文本显示0.1宣称精确一致。NUMERIC分别为目标(3,2)/(6,2)：前者源无固定typmod，只确认值与Scale；后者保留明确源约束。这里复用旧NUMERIC/REAL代码，不新增通用运行时REAL实现或升级旧补偿验收。

## 5. 测试、回归与已知未覆盖

- 第一项：全方言1105、定向/核心316通过；扩充前的首次PG新测试因源文本空格不符合validate_identity规范失败，调整为规范格式后通过。新增标量子查询源往返测试还暴露一个既有PG Generator问题（见第7节），没有把它混进本项Parser提交。
- 第二项：全方言1107、定向/核心318通过；两集合有重叠，不相加。最后新增的引号/反斜杠断言单独通过；最终commit后PG/Doris114条通过。Ruff check、format --check及git diff --check通过。
- 20条初次候选仅18条成功，另2条E输入缺少unknown分类/已解码消费；同一规则内修正后重跑20条，原文没有改成普通字符串以绕过失败。曾有NUMERIC排除控制的错误文本正则太窄，改为断言共同的unsupported前缀，不是接受了该未支持输入。
- 保持显式下界、多维文本、FLOAT/NUMERIC子数组文本为严格unsupported测试；这不表示已完成其可执行转换，不把源成功用例误标为负向。一般字符串列缺Schema、无源类型提示时不猜其为子数组。
- 没有mypy/C扩展/完整optimizer/integration或make check验收；没有安装或升级依赖。

SQLGlot目录的主要测试命令（解释器../sqlglot-experiment/.venv/bin/python，PATH含该venv，PYTHONDONTWRITEBYTECODE=1）：
```bash
python -m unittest discover -s tests/dialects -t .
python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.test_expressions tests.test_parser tests.test_generator tests.test_serde tests.test_transpile
python -m unittest tests.dialects.test_postgres tests.dialects.test_doris
ruff check sqlglot/dialects/dialect.py sqlglot/parsers/postgres.py sqlglot/generators/doris.py tests/dialects/test_postgres.py tests/dialects/test_doris.py
ruff format --check sqlglot/dialects/dialect.py sqlglot/parsers/postgres.py sqlglot/generators/doris.py tests/dialects/test_postgres.py tests/dialects/test_doris.py
git diff --check
```

## 6. 固定原输入回归

用CLI CliRunner按原阶段调用run --path <stage YAML> --stdout；同阶段重复--id批量指定全部安全原Case，不保存新验证JSON、不改变源.out。用起点源码在内存中加载Parser/Generator作生成层控制，不切换/改写工作树。

最终313条逐ID生成SQL/严格错误与d0c2e9ea起点相同；43阶段310条安全原查询实跑为82匹配、25源端负向、69行值/顺序不同、114目标失败、12框架环境标签、8转译失败。原0301/0303/0304后端风险未执行。已取得成功源结果285，匹配率82/285=28.77%，没有原输入新增MATCH。原task-001的14条仍3匹配、6显示不同、4目标失败、1转译失败。

旧56条NUMERIC边界在最终提交重跑，值/Scale和重复稳定56通过；固定声明28对应、另28源无约束NUMERIC域限制继续保留。新增文本子数组规则和原56条补偿不混成一类“通用修复成功”。本轮生成层与原数据状态均未变；没有修改Comparator/Adapter修掉显示问题。

## 7. 既有补偿审查与后续范围

| 范围 | 本轮判断 | 后续动作 |
| :--- | :--- | :--- |
| 源数组类型事实与目标能力分离 | 本轮已纠正并验收这项职责边界 | 后续源推型不能再引用Doris支持白名单 |
| 已知类型下的一维文本子数组输入 | 本轮按源语法规则完成有限范围转换 | 显式下界、多维文本及其他元素域另有依据后再扩展，不假装全部支持 |
| 旧NUMERIC文本中转、运行时ARRAY_MAP及高精度取负 | 当前环境部分必要性已有反例，通用性待验证 | 本轮原生负号控制5通过、1失败，不能按precision<=38盲目替换；类型/算子组合和跨版本能力仍待审查 |
| 旧运行时文本直接REAL | 仍未解决，本轮无新增实现 | 没有新入口/算法就不反复当作下一项已确定可修复任务 |
| 一般NUMERIC类型域、混合Scale、77位/NaN | 原限制仍在，本轮无通用实现 | 区分可证明的源固定约束与目标能力/契约问题，不改成STRING/DOUBLE凑一致 |
| 源PG Generator的标量子查询数组往返 | 新发现、独立研究事项，未实施 | ARRAY[(SELECT ARRAY[1,2]),'{3,4}']回生PG时丢掉后一个元素，生成ARRAY((SELECT ARRAY[1,2]))；影响源SQL再生成，不是本轮Doris输出。需独立审查并按授权处理，不删除失败事实 |

本轮只在task-001继续已有类型/输入子项，没新建task、没实施task-003/010、没自动接管源PG Generator的独立问题。task-001太宽的问题通过原条目分开记录已实现规则、待审查补偿、研究/外部限制，不删除旧任务或把历史通过改写为失败。

### 7.1 旧取负补偿的必要性控制

本轮继续对DorisGenerator::_bounded_numeric_array_sql::preserve_cast做有限审查，没有在两个commit完成后直接停止。保持原decimal256/严格转换设置，分别实测以下(p,s)/输入的原生负号候选；源均是`SELECT ARRAY[-CAST('<输入>' AS NUMERIC(p,s)), -CAST(NULL AS NUMERIC(p,s))] AS xs`：

| p,s | 精确输入 | 原生候选对PG源值 | 观察 |
| :--- | :--- | :--- | :--- |
| 6,2 | 1.235 | 一致 | -1.24、NULL |
| 6,2 | -2.345 | 一致 | 2.35、NULL |
| 38,0 | 99999999999999999999999999999999999999 | 一致 | 相同38位负整数、NULL |
| 38,0 | -99999999999999999999999999999999999999 | 一致 | 相同38位正整数、NULL |
| 38,38 | 0.99999999999999999999999999999999999999 | **不同** | 源为同精确小数的负数，候选为NULL |
| 30,18 | 1.234567890123456789 | 一致 | -1.234567890123456789、NULL |

这些是手写能力控制，不计作SQLGlot修复验收。关键失败候选完整SQL：
```sql
SELECT ARRAY_MAP(v -> CAST(v AS DECIMAL(38,38)),
 ARRAY(CAST(-(ARRAY_MAP(v -> CAST(v AS DECIMAL(38,38)),
   ARRAY('0.99999999999999999999999999999999999999'))[1]) AS STRING),
   CAST(NULL AS STRING))) AS xs;
```
目标成功执行但返回`[null,null]`，不是连接/语法失败。最后再从对应原源SQL用最终SQLGlot生成并执行，既有补偿实际返回`[-0.99999999999999999999999999999999999999]`，原生声明array<decimalv3(38,38)>，值与源一致。

所以不能从几个常见值成功就推导“精度不超过38一律改回原生负号”，本轮没有提交这种未经成立的简化，也没有为了避开NULL改变输入/Scale。当前证据说明部分补偿确有必要，**不等于其所有类型/上下文或其他版本已通过**；尚未追到所有版本/配置的算子推型原因，不臆造能力阈值。

后续具体工作是核对该Doris版本的负号结果类型推导，明确失败的precision/scale与上下文条件，再检查同型列输入、外层CAST及后续运算，决定能否按可靠能力范围简化。没有新的源码/能力依据不继续堆包装，也不重复声称旧REAL已修复；需改Doris、Session或结果契约时先取得额外授权。本轮只完成上述有限必要性审查，不将旧56条回归或本次5个成功控制升级为通用补偿验收。

Skill修改及代码提交/报告均不等于整份输入完成，当前任务仍未全部验收。全部本地提交未push，未创建Issue/PR；无额外交接、候选文件、证据JSON、脚本、日志或patch。

