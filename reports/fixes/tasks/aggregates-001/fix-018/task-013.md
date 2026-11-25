# task-013：PostgreSQL 文本数组字面量输入

## 1. 结论和范围

已实现有限一维TEXT数组输入的通用解析，原0415完整SQL已由本次SQLGlot实际生成并成功执行，元素`[fred,jill,jim]`和TEXT数组类型与实时PG对应，重复稳定。不是手写替换0415数据；任意同语法文本元素走同一规则。原`.out`仍按文本比较，不因成功补证改成MATCH。百分位算法另见[task-012](task-012.md)，共同环境及BE恢复见[汇总](../../../aggregates-001-fix-018-summary.md)。

依赖task-012及task-001概率上下文以运行原完整查询；TEXT输入解析规则本身可单独用于CAST或UNNEST。父commit为`a499d04cf69a13d831f3943df89c15e60bfcd56c`。不修改原SQL/.out、数据/DDL、框架或比较器，不顺带修task-010。

## 2. 实现及验证范围

`sqlglot/parsers/postgres.py::_parse_text_array_literal`识别花括号、逗号、ASCII空白、双引号及反斜线转义；未引号且未转义的NULL按PG输入语法生成Null AST，`"NULL"`和`\NULL`保留为字符串。这是解析输入语法，不是在Generator中把NULL函数常量折叠成答案。`PostgresParser.build_cast`只规范化可完整识别的字符串字面量→TEXT[] CAST，支持CAST与`::`。结果是公共Array AST及原TEXT[] CAST，沿用既有Doris构造器/类型处理；SQL文本可规范化，源执行文本不变。

空数组由外层CAST确定TEXT类型，不给内层空构造器添加无对应源类型提示；初次单测发现该提示破坏PG往返，已修正。非空构造器保留TEXT提示。Parser/AST序列化、往返、copy=False不变性及CAST/DCOLON两种写法均测试。

范围排除：显式非1下界、多维花括号输入、其他元素类型、一般运行时字符串、E前缀等非Literal输入及不能完整识别的非法输入。这些保持原Cast而非猜数据或生成新答案，不表示已安全转换；本轮没有实现它们。源Session实查`array_nulls=on`，NULL词法含义以此为前提，不声称可跨array_nulls=off保持同义。

`tests/dialects/test_postgres.py`增加输入规范化/排除测试；1097项全方言、308项定向及核心测试通过（两集合重叠），ruff check、format --check、diff检查通过。未跑C扩展/make check，不安装依赖。真实本地commit为`3c9e4bb004bff47a4ca8b750961f5e4470076590`，父`a499d04cf69a13d831f3943df89c15e60bfcd56c`；干净、未push。该HEAD另通过104项PG/Doris测试及原43阶段310条回归，最终结果见汇总；0415仍只因原.out数组显示不同被判不匹配。

## 3. 原查询与真实生成

```sql
-- 原0415，不改源文本
select percentile_disc(array[0.25,0.5,0.75]) within group (order by x)
from unnest('{fred,jim,fred,jack,jill,fred,jill,jim,jim,sheila,jim,sheila}'::text[]) u(x);
```

修复前Doris CAST字符串为ARRAY<STRING>得到NULL，且WITHIN GROUP不可执行。修复后实际生成的FROM是：

```sql
FROM UNNEST(CAST(CAST(ARRAY('fred','jim','fred','jack','jill','fred',
 'jill','jim','jim','sheila','jim','sheila') AS ARRAY<STRING>) AS ARRAY<STRING>)) AS u(x)
```

投影由task-012的COUNT/ARRAY_SORT(COLLECT_LIST)/CEIL树生成，未手写候选代替修复。双端真实结果分别为PG `_text` `[fred,jill,jim]`、Doris EXPLAIN `array<text>` `["fred", "jill", "jim"]`。无显式别名按原规则不比较派生字段名；单行无最终ORDER BY要求，但数组元素顺序逐位置检查。

## 4. 边界与证据限制

全部使用修改后SQLGlot从源变体生成，固定阶段31、UTC和原比较规则，execute_query 10秒/10000行限制；实际import路径为`../sqlglot-functional-commits/sqlglot/__init__.py`。每条检查原执行、目标执行、TEXT类型、NULL/空串、位置及重复，目标重复稳定。

| 源输入或查询变体 | 实际原生元素/行结果 |
| :--- | :--- |
| `{fred,jim,fred}` | fred、jim、fred |
| `{}` | 空数组，长度0 |
| ` {  } ` | 空数组，长度0 |
| `{NULL,null,"NULL",""}` | NULL、NULL、字符串NULL、空串 |
| `{ a , " b " , "a,b" , "{}" }` | a、两边有空格的b、含逗号a,b、字符串{} |
| `{a\,b,a\}b,\NULL,"a\\b","a\"b"}` | a,b、a}b、字符串NULL、a反斜线b、a双引号b |
| `{\ a\ ,"中文",😀}` | 保留两端转义空格、中文、😀 |
| `{a,a,b,NULL,"NULL",""}` | 6项，重复a/NULL/字符串NULL/空串不丢失 |
| 同原0415，p=NULL,0,.25,.5,.75,1 | `[NULL,fred,fred,jill,jim,sheila]` |
| `{fred,jim,NULL,fred,jack}`，p=0,.5,1，DESC | `[jim,jack,fred]` |
| `'{"O''Brien",a}'::text[]` | O'Brien、a |
| UNNEST `{a,a,b,NULL,"NULL",""}` AS u(x)，SELECT x AS item ORDER BY x NULLS FIRST | NULL、空串、字符串NULL、a、a、b；两端6行、TEXT、显式别名与最终顺序相同 |

12条新变体及原0415均执行；11条数组变体另通过只读包装读取实际生成结果的`xs[1]...xs[n],SIZE(xs)`逐位置核对，重复稳定。包装只解码已生成的目标结果，不作为修复后的候选、不替换源SQL/执行结果，也不改框架。之所以补此检查，是Doris数组显示中的反斜线/双引号不总是合法JSON：第一次直接json.loads在转义用例报JSONDecodeError，中断后的用例已完整重跑，未把它当PG错误或修复失败。普通数组可解析显示，特殊字符必须用原生元素证据，不能宽松清洗成相同。

PG外层聚合返回_numeric等类型约束、文本排序Collation等独立限制不因此解决；本任务有限TEXT[]字面量输入验收不意味着任意PG数组输入可移植。
