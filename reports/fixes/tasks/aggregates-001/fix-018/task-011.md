# task-011：常量数组连续百分位转换

## 1. 结论与范围

已实现并完成本轮有限规则验收：原0411、0413从Doris语法失败变为成功执行，实时PG的数组元素和DOUBLE类型均对齐。原`.out`仍显示`{...}`，Doris显示`[...]`，原比较器仍判两条行值不同，未改规则或伪造MATCH。归因方案见[统一任务清单](../../../../attribution/aggregates-001-attribution-summary.md#task-001)中fix-018实施前计划。共同环境及恢复事实见[本轮汇总](../../../aggregates-001-fix-018-summary.md)。

范围是非空、有限字面量概率数组（含NULL及矩形嵌套）、单个数值列或数值CAST排序键。按概率展开原生精确PERCENTILE，不用近似算法或嵌套lambda；保留概率顺序及重复。源键CAST为DOUBLE与PG连续百分位数值签名一致；DESC先取负排序、结果再取负，不通过`1-p`改变概率舍入。空或全NULL组用COUNT判断返回NULL，每项概率用运行时IS NULL和COALESCE处理。NULL语法白名单只做范围检查，不在Python计算查询结果。

排除动态概率、概率CAST/表达式、空构造器、INTERVAL键、易变或一般键表达式、FILTER/OVER。本轮没有声称支持非有限排序键、全部浮点插值极端或任意文本排序；概率之外没有注入Schema。原标量PERCENTILE_CONT路径不变。多个标量聚合可能增加计算成本，未做性能基准。

## 2. 代码与测试

- `sqlglot/generators/doris.py::withingroup_sql`：有限范围检查、树形展开、运行时NULL/空组处理和DESC。
- `tests/dialects/test_doris.py::test_percentile_cont_array`、`test_percentile_cont_array_exclusions`：输出、AST不变、往返、嵌套/重复及排除条件。
- PG参数上下文测试改为直接验证概率Array的Doris生成结果，不再把整个函数必须保留WITHIN GROUP/ARRAY CAST作为Parser测试前提。Parser的DOUBLE元数据、序列化和PG往返断言保留。
- 初次定向测试暴露旧测试将全函数文本与Parser类型规则耦合，以及REAL概率CAST尚不在新范围；未隐瞒失败。现在前者独立测试数组，后者明确排除，未冒称REAL概率已有执行验收。
- 本次准确代码状态运行1093项全方言通过，其中包含100项PG/Doris；ruff check、format --check、git diff --check通过，不将包含关系的数量相加。解释器和PATH见汇总；未安装依赖、未跑C扩展或make check。

## 3. 实际执行与类型

数据库解释器为`../doris-sql-validator/.venv/bin/python`，`PYTHONPATH=../sqlglot-functional-commits:src`，实际import路径为该SQLGlot checkout。源/目标均阶段31，固定原数据/Session，调用`parse_one(source, read="postgres").sql("doris", unsupported_level=RAISE)`生成，再`execute_query`执行两端并重复目标查询；10秒/10000行上限。结构化数组核对是补证，不替换原`.out`显示文本比较。

最小例：

```sql
-- PG，行数据含1、2、2、NULL
SELECT percentile_cont(ARRAY[NULL,0.5]) WITHIN GROUP (ORDER BY x) AS xs
FROM (SELECT 1 AS x UNION ALL SELECT 2 UNION ALL SELECT 2 UNION ALL SELECT NULL) t;

-- 本次SQLGlot实际生成
SELECT IF(COUNT(CAST(x AS DOUBLE)) = 0, NULL,
  ARRAY(IF(CAST(NULL AS DOUBLE) IS NULL, NULL,
    PERCENTILE(CAST(x AS DOUBLE), COALESCE(CAST(NULL AS DOUBLE),0))),
  IF(CAST(0.5 AS DOUBLE) IS NULL, NULL,
    PERCENTILE(CAST(x AS DOUBLE), COALESCE(CAST(0.5 AS DOUBLE),0))))) AS xs
FROM (SELECT 1 AS x UNION ALL SELECT 2 UNION ALL SELECT 2 UNION ALL SELECT NULL) AS t;
```

| 查询/变体 | 真实结果（源/目标元素相同） | 类型、顺序与稳定性 |
| :--- | :--- | :--- |
| 原0411 | `[0,249.75,499.5,749.25,999]` | PG `_float8` / Doris `array<double>`；无最终ORDER BY、单行；重复稳定 |
| 原0413 | `[1,6,2.25,4.75,3.5,6,2.5,2.6,2.75,2.9,3]` | 同上；generate_series仍由task-008生成；重复稳定 |
| ARRAY[0,0.25,0.5,1]；数据1、2、2、NULL | `[1,1.5,2,2]` | DOUBLE数组，xs别名一致、重复稳定 |
| ARRAY[NULL,0.5]，同数据 | `[NULL,2]` | 同上 |
| ARRAY[1,0.5,0.5,0]，同数据 | `[2,2,2,1]` | 概率顺序/重复保留 |
| 同数据WHERE x>99 | NULL | 空组，不返回空数组 |
| 单行CAST(NULL AS INT) | NULL | 全NULL组 |
| 单行7 | `[7,7,7]` | ARRAY[0,0.5,1] |
| ARRAY[0,0.25,1] ORDER BY x DESC，同数据 | `[2,2,1]` | 反向排序已实测 |
| ARRAY[0,0.25,0.5,1]；数据-7、-2、5 | `[-7,-4.5,-2,5]` | 负数与插值 |
| ARRAY[0,0.5,1] ORDER BY CAST(x AS DOUBLE)，同数据 | `[1,2,2]` | 显式键CAST |
| 数据DECIMAL(6,2)的1.20及2.40 | `[1.2,1.8,2.4]` | 源结果也为DOUBLE，不误保留DECIMAL |
| ARRAY[[NULL,1],[0.5,NULL]]，同数据 | `[[NULL,2],[2,NULL]]` | PG `_float8`多维 / Doris `array<array<double>>` |
| g=1有x=1、3，g=2有NULL；GROUP BY g ORDER BY g | `(1,[1,2,3]),(2,NULL)` | CAST(g AS INT)双端int；最终行顺序一致 |
| 外层SELECT xs，内层聚合上述普通数据 | `[2]` | 子查询边界保持 |

共2条原查询及13条变体，两端成功、元素/NULL/重复和已取得类型对应，目标重复稳定；仅分组变体要求最终行序。原查询无显式Alias，生成器派生字段名不同按原规则不比较；变体显式xs/g一致。DOUBLE实际显示成整数不改变类型；未把数组文本显示差异修成字符串输出。

最终HEAD另外用PG二进制cursor重读原0411/0413，两端各重复两次；Doris在实际生成表达式外加逐位置读取包装。16个原生DOUBLE位置精确对应，float.hex逐个相同，2.6为`0x1.4cccccccccccdp+1`，2.9为`0x1.7333333333333p+1`。没有依赖PG文本浮点显示或Doris数组显示判断精度；包装只解码输出，不是替换生成SQL的候选。

固定YAML用CliRunner调用`run --path reports/data-preparation/aggregates-001-stage-31-cases.yaml --stdout --id pg-aggregates-0411-b38c2a1f --id pg-aggregates-0413-6ccabd9a`：2条均“行值或顺序不匹配”，反例分别是`{0,249.75,499.5,749.25,999}`对`[0, 249.75, 499.5, 749.25, 999]`及0413对应相同元素的两种显示。退出1，JSON有效；未保存额外文件。

独立本地commit为`fa20f2cf768dc09e887eb8cf7449f41f4b1eb548`，父`2aef92e0c755132bf2253a34280e99adf27f98d0`，提交后无剩余diff；未push。最终HEAD及310条/43阶段结果见[汇总](../../../aggregates-001-fix-018-summary.md)，两条仍执行成功，仅原.out显示不同。最终1097项全方言、308项定向/核心、commit后104项PG/Doris通过（重叠）。本任务有限规则验收不等于整个百分位功能或原输入全部MATCH。
