# task-001 / fix-018：百分位概率数组的源类型上下文

## 1. 当前结论与提交

**整个task-001仍已修改但未完成验收；本轮所选五条的有限转换已补齐。** 先修正概率上下文，再分别实现task-011/012/013；最终五条均生成成功并在Doris执行，实时元素/类型对应。原.out数组显示不同仍不计MATCH，直接REAL/一般NUMERIC等原task余项不因此关闭。恢复后的当前证据见第7节；下面第3至6节保留中断前事实，不当作最终状态。

独立本地commit：2aef92e0c755132bf2253a34280e99adf27f98d0，父commit为4dc65a35a7efa92551cb9fb00c2315fcb8ff659f。文件仅sqlglot/parsers/postgres.py、tests/dialects/test_postgres.py，60行增加，最终干净，未push。实施前方案已先写入[原task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)。共同环境/权限/输入见[本轮汇总](../../../aggregates-001-fix-018-summary.md)。

## 2. 为什么需要修正上下文

[PG18函数签名](https://www.postgresql.org/docs/18/functions-aggregate.html)规定百分位概率数组为double precision[]。本轮实际查询pg_proc，并对五条原文EXPLAIN(VERBOSE,COSTS OFF)：均得到概率数组向DOUBLE数组的隐式转换。排序参数的类型则不同：CONT数值输入转DOUBLE，DISC保留排序值类型。不能因原数组中0、0.25等字面量Scale不同就断言此处无法转换。

PostgresParser._parse_window在真正WITHIN GROUP节点建立后，对直接概率数组及明确嵌套记录DOUBLE元素hint；只限没有Query/Column/Placeholder及内部显式数组CAST的构造。普通NUMERIC数组仍保留NUMERIC；显式数组CAST、未知类型和一般作用域不强行覆盖。原PG SQL语法不改，metadata支持dump/load、PG round-trip及copy=False不变性。这个commit不包含Doris函数实现。

## 3. 第一次上下文commit后的历史生成结果

各条均属原stage-31，引用原YAML/首轮JSON和配对aggregates.out，不新建输入。PG原文实际执行成功，结果如下；目标均在本轮commit代码生成并实际执行，不是手写候选。

### 0410：离散整数数组

~~~sql
select percentile_disc(array[0,0.1,0.25,0.5,0.75,0.9,1]) within group (order by thousand)
from tenk1;

SELECT PERCENTILE_DISC(CAST(ARRAY(0, 0.1, 0.25, 0.5, 0.75, 0.9, 1) AS ARRAY<DOUBLE>)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

PG OID1007、值[0,99,249,499,749,899,999]。目标报missing 'BY' at '('，pos99；没有取得目标结果类型/行值。

### 0411：连续整数排序值

~~~sql
select percentile_cont(array[0,0.25,0.5,0.75,1]) within group (order by thousand)
from tenk1;

SELECT PERCENTILE_CONT(CAST(ARRAY(0, 0.25, 0.5, 0.75, 1) AS ARRAY<DOUBLE>)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

PG OID1022、值[0.0,249.75,499.5,749.25,999.0]；目标同类语法错误pos89。

### 0412：多维及NULL概率

~~~sql
select percentile_disc(array[[null,1,0.5],[0.75,0.25,null]]) within group (order by thousand)
from tenk1;

SELECT PERCENTILE_DISC(CAST(ARRAY(CAST(ARRAY(NULL, 1, 0.5) AS ARRAY<DOUBLE>), CAST(ARRAY(0.75, 0.25, NULL) AS ARRAY<DOUBLE>)) AS ARRAY<ARRAY<DOUBLE>>)) WITHIN GROUP (ORDER BY thousand NULLS LAST) FROM tenk1
~~~

PG OID1007、值[[NULL,999,499],[749,249,NULL]]；目标同类语法错误pos165。

### 0413：重复及非排序概率

~~~sql
select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x)
from generate_series(1,6) x;

SELECT PERCENTILE_CONT(CAST(ARRAY(0, 1, 0.25, 0.75, 0.5, 1, 0.3, 0.32, 0.35, 0.38, 0.4) AS ARRAY<DOUBLE>)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM (SELECT CAST(1 + number * 1 AS INT) AS x FROM NUMBERS('number' = '6')) AS x
~~~

PG OID1022、值[1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3]；目标同类语法错误pos120。

### 0415：文本排序值及PG文本数组输入

~~~sql
select percentile_disc(array[0.25,0.5,0.75]) within group (order by x)
from unnest('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}'::text[]) u(x);

SELECT PERCENTILE_DISC(CAST(ARRAY(0.25, 0.5, 0.75) AS ARRAY<DOUBLE>)) WITHIN GROUP (ORDER BY x NULLS LAST) FROM UNNEST(CAST('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}' AS ARRAY<STRING>)) AS u(x)
~~~

PG OID1009、值[fred,jill,jim]；目标同类语法错误pos83。另外本机Doris把'{fred,jim}'直接CAST ARRAY<STRING>实测返回NULL；UNNEST(ARRAY('fred','jim'))则能执行。因此后续不能只改百分位函数名而忽略输入数组解析。

五条此前都报Doris cannot preserve this PostgreSQL NUMERIC array domain；现在恢复正确DOUBLE参数处理，但这不是完整查询修复。修复后主框架run --stdout/整阶段回归尚未完成，不能给新的总体匹配率。

## 4. 函数可行性及失败路径

[Doris PERCENTILE_ARRAY](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/aggregate-functions/percentile-array/)为连续计算结果，不等于PG离散百分位。本轮手写候选仅用于探路，均未变成已验收的生成规则：

| 实测路径 | 实际观察 |
| :--- | :--- |
| PERCENTILE_ARRAY(thousand,ARRAY(0,0.25,0.5,0.75,1)) | 成功，array<double>，值[0,249.75,499.5,749.25,999] |
| PERCENTILE_DISC(thousand,0.25) | 函数不存在，不能直接改调用形式 |
| 排序COLLECT_LIST后按max(1,ceil(p*N))取值，平面lambda | 成功，array<int>，[0,99,249,499,749,899,999]；文本控制返回[fred,jill,jim]及array<text> |
| PERCENTILE_ARRAY带NULL概率 | INVALID_ARGUMENT：quantiles in func percentile_array should not have null |
| lambda内PERCENTILE(x,p) | 第二参数必须常量，不能把lambda参数当SQL常量 |
| 内层lambda直接引用聚合列 | Unknown lambda slot；嵌套需要不同组织方式 |
| 分别展开常量概率、用COALESCE处理传给PERCENTILE的NULL，再用运行时IF还原NULL | 有限控制成功，array<double>，[NULL,1.5]；仍需完整边界/空组/类型验证 |
| 直接构造多维离散结果的有限控制 | 成功，array<array<int>>，[[NULL,0],[499,NULL]]；尚未证明一般Decimal/作用域 |

这些只是候选，不把它们替换原源SQL或当作修复后生成SQL。

## 5. 段错误候选与中断时数据库状态（恢复见第7节）

以下候选在2026-11-25 11:32:25（Asia/Shanghai）执行期间断连，**禁止自动重试**：

~~~sql
SELECT ARRAY_MAP((row_p,s) -> ARRAY_MAP(p -> IF(p IS NULL,NULL,s[GREATEST(1,CAST(CEIL(p*SIZE(s)) AS BIGINT))]),row_p), ARRAY(ARRAY(NULL,1,0.5),ARRAY(0.75,0.25,NULL)), ARRAY_MAP(r -> ARRAY_SORT(COLLECT_LIST(thousand)),ARRAY(ARRAY(NULL,1,0.5),ARRAY(0.75,0.25,NULL)))) AS xs FROM tenk1
~~~

工具先返回(2013, Lost connection to MySQL server during query)。随后只读docker inspect/logs确认：BE Segmentation fault、rc=139；容器doris退出码1，OOMKilled=false，9030拒绝连接；日志包含相同候选的查询重试记录。不是普通解析/行值错误，不能继续无保护地重放该族候选。

没有重启、删除、重建容器或重新装数。已请求允许仅docker start doris恢复原环境；恢复前暂停目标数据库验收，不把服务退出记成5条SQL的语义结论。当前没有新的Doris Generator修改或未提交代码。后续优先考虑明确常量概率展开、避开此嵌套聚合lambda路径，再重新验证精度、NULL、空组、嵌套、重复、分组及返回类型。

## 6. 中断前测试和当时的后续计划

98项PG/Doris测试、1091项全方言、302项定向/核心扩展测试通过，集合有重叠，不相加。ruff及git diff --check通过。源参数测试包括CONT/DISC×平面/嵌套/内层REAL CAST、普通NUMERIC不变、动态列和内部显式数组CAST不越界，以及AST copy=False、dump/load、PG round-trip。没有完整优化器/mypy/C扩展或崩溃后目标数据库回归，未运行不写通过。

下一步仍是用户选定的这五条，不自动开始task-010或其他无关任务。需要先恢复原Doris可连接状态；完整CONT、DISC及文本数组输入是不同机制，分别形成有证据的独立方案/commit。原task-001整体仍有既有余项；本轮仅提交参数上下文，不宣称五条已解决或工作流完成。

## 7. 获准恢复后完成的修复与验收

用户明确允许启动原容器，已执行docker start doris；FE/BE健康、原tenk1为10000行，最终回归后仍保持。未删除/重建/装数、未重试第5节高风险候选。后续改用无lambda的常量展开，按实施前方案拆为[task-011](task-011.md)、[task-012](task-012.md)、[task-013](task-013.md)，各自代码和测试独立本地commit：fa20f2cf768dc09e887eb8cf7449f41f4b1eb548、a499d04cf69a13d831f3943df89c15e60bfcd56c、3c9e4bb004bff47a4ca8b750961f5e4470076590。依赖顺序及范围见汇总，不混入原概率上下文commit。

当前实际由parse_one原SQL生成后执行：0410 `[0,99,249,499,749,899,999]`及array<int>；0411 `[0,249.75,499.5,749.25,999]`及array<double>；0412 `[[NULL,999,499],[749,249,NULL]]`及array<array<int>>；0413 `[1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3]`及array<double>；0415 `[fred,jill,jim]`及array<text>。全部实时PG对应元素/NULL/形状相同且目标重复稳定。单行无最终ORDER BY；无显式Alias按原政策不比较派生字段名。五条原run仍因花括号/方括号数组显示被判不同，不能写5条MATCH；真实SQL和有限边界分别见上述任务报告。

最终HEAD为3c9e4bb004bff47a4ca8b750961f5e4470076590，分支累积24个本地功能commit，干净、未push。1097项方言、308项定向/核心及提交后104项PG/Doris测试通过（集合重叠）；最终43阶段310条为82匹配、25负向、69值/顺序不同、114目标失败、12环境类、8转译失败。原82个匹配保留；风险0301/0303/0304未执行，历轮全部边界未重跑，未做全输入等价证明。

所选五条的有限转换完成，不将数组显示误报硬改为文本输出。新规则排除动态概率、FILTER/OVER、一般类型/排序前提等未证明域；文本数组仅一维TEXT字面量及默认array_nulls=on。原task-001直接REAL/一般NUMERIC、task-003及未实施task-010仍保留，整份输入未完成。
