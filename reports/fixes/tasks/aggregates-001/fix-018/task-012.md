# task-012：常量数组离散百分位转换

## 1. 当前结论

有限常量概率数组的离散规则已完成本轮约定验收；原0410、0412由语法失败变为执行成功，INT元素和多维形状对齐。0415在task-013补齐文本数组输入后也已成功，元素为[fred,jill,jim]、TEXT数组类型对应。与task-011共享范围检查，但这是不同算法，独立提交。初步方案见[统一任务清单](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，环境和恢复见[汇总](../../../aggregates-001-fix-018-summary.md)。

Doris没有可直接替换的精确原生PERCENTILE_DISC，不能换成连续或近似百分位。新规则对COLLECT_LIST收集的非NULL值排序，按`GREATEST(1,CEIL(CAST(p AS DOUBLE)*COUNT(x)))`取原类型元素。p=0取首项；概率NULL与空/全NULL组在SQL运行时处理；按概率构造树展开，保留概率顺序、重复和多维，不使用lambda。内部Bracket明确使用目标原生offset，不改变task-010用户下标规则。DESC用原生ARRAY_REVERSE_SORT；第一次边界试验发现ARRAY_REVERSE不存在，已替换并重复实测，失败尝试保留。

范围：非空常量字面量概率数组、简单可排序列/数值或文本CAST、当前已确认类型与排序前提。动态概率、CAST概率、一般键表达式、显式COLLATE、FILTER/OVER排除。没有声称任意PG排序规则、NaN/Infinity、高于Doris精度上限的NUMERIC或数组键全部等价。DECIMAL(6,2)额外用例值/Scale正确，但PG聚合返回_numeric未声明typmod，不能宣称它与Doris固定DECIMAL约束完整相同。排序列的真实类型仍依赖外部匹配DDL，不注入Schema或猜列类型。

## 2. 代码、测试与提交

- `sqlglot/generators/doris.py::withingroup_sql`：复用task-011概率树及作用域检查，按CONT/DISC选择算法；DISC不把键值CAST成DOUBLE，BIGINT精确值可保留。
- `tests/dialects/test_doris.py::test_percentile_disc_array`、`test_percentile_disc_array_exclusions`：精确SQL、AST不变、Doris往返、多维/重复/DESC及范围排除。
- 父commit为task-011 `fa20f2cf768dc09e887eb8cf7449f41f4b1eb548`。准确拟提交代码已运行1095项全方言测试通过，ruff check及git diff --check通过；格式化完成。全方言已包含PG/Doris，不将重叠测试相加；未跑C扩展/make check。
- 真实本地commit为`a499d04cf69a13d831f3943df89c15e60bfcd56c`，父`fa20f2cf768dc09e887eb8cf7449f41f4b1eb548`，提交后干净、不push。最终HEAD/43阶段310条及1097方言、308定向/核心、提交后104项PG/Doris通过（重叠）见汇总。三条原查询最终均执行成功、类型/元素对应，原.out数组显示不同仍保留。

## 3. 数据库验证

沿用原阶段31、解释器和`parse_one(..., read="postgres").sql("doris", unsupported_level=RAISE)`生成，再execute_query执行源/目标，目标重复两次。不是重放手写候选。10秒/10000行上限；读实际EXPLAIN类型。结构化数组补证（NUMERIC用Decimal而非float容差）不改主框架文本比较。

```sql
-- 最小源查询
SELECT percentile_disc(ARRAY[0.5,NULL]) WITHIN GROUP (ORDER BY x) AS xs FROM t;
-- 生成的Doris查询
SELECT IF(COUNT(x)=0,NULL,ARRAY(
  IF(CAST(0.5 AS DOUBLE) IS NULL,NULL,
    ARRAY_SORT(COLLECT_LIST(x))[GREATEST(1,CAST(CEIL(COALESCE(CAST(0.5 AS DOUBLE),0)*COUNT(x)) AS BIGINT))]),
  IF(CAST(NULL AS DOUBLE) IS NULL,NULL,
    ARRAY_SORT(COLLECT_LIST(x))[GREATEST(1,CAST(CEIL(COALESCE(CAST(NULL AS DOUBLE),0)*COUNT(x)) AS BIGINT))]))) AS xs FROM t;
```

| 查询/变体 | 源与目标对应元素 | 类型/顺序/稳定性 |
| :--- | :--- | :--- |
| 原0410 | `[0,99,249,499,749,899,999]` | PG _int4 / Doris array<int>，重复稳定 |
| 原0412 | `[[NULL,999,499],[749,249,NULL]]` | PG _int4多维 / Doris array<array<int>>，重复稳定 |
| p=0,.25,.5,.75,1，x为INT的1、2、2、NULL | `[1,1,2,2,2]` | array<int>，NULL被排除，重复值保留 |
| p=NULL,.5，同数据 | `[NULL,2]` | NULL概率位置保留 |
| p=1,.5,.5,0，同数据 | `[2,2,2,1]` | 不排序/去重概率数组 |
| p=0,.5,1，同数据WHERE x>99 | NULL | 空组返回NULL，不是空数组 |
| 仅CAST(NULL AS INT) | NULL | 全NULL组 |
| 仅INT 7，p=0,.5,1 | `[7,7,7]` | 单值 |
| p=0,.25,.5,.75,1，同数据DESC | `[2,2,2,1,1]` | 修正ARRAY_REVERSE后重复成功 |
| x=INT -7、-2、5，p=0,.25,.5,1 | `[-7,-7,-2,5]` | 保留负数 |
| CAST(x AS BIGINT)，p=0,.5,1 | `[1,2,2]` | PG _int8 / array<bigint> |
| DECIMAL(6,2) 1.20、2.40，p=0,.5,1 | `[1.20,1.20,2.40]` | 值/Scale对应；返回约束限制见上文 |
| p=[[NULL,1],[.5,NULL]]，INT普通数据 | `[[NULL,2],[2,NULL]]` | 形状/NULL正确 |
| TEXT a、b、b、NULL，p=0,.25,.5,1 | `[a,a,b,b]` | _text / array<text>；ASCII本地排序前提 |
| generate_series(1,100)，p=.07,.14,.28,.58,.9999999999999999 | `[8,15,29,58,100]` | PG概率是DOUBLE；不能用DECIMAL精确乘法替换 |
| 分组g1有INT1、3，g2有NULL，p=0,.5,1 | `(1,[1,1,3]),(2,NULL)` | CAST(g AS INT)，GROUP BY g ORDER BY g，最终序一致 |
| BIGINT 9007199254740993、9007199254740995，p=0,.5,1 | `[9007199254740993,9007199254740993,9007199254740995]` | 精确整数，不经DOUBLE丢位 |
| DECIMAL(6,2)同前，p=[[0,.5],[.5,1]] | `[[1.20,1.20],[1.20,2.40]]` | 多维Decimal类型由EXPLAIN确认，约束未整体等价 |

2条原文及16条变体，最终各项成功且目标重复稳定；15条变体初次测试中DESC失败，修正后重跑DESC，并新增多维Decimal，共16条。别名xs及分组g一致；原查询无显式别名，派生字段名按原政策不要求相等。仅分组查询要求最终顺序，其余单行；全部数组元素顺序保留。

固定原YAML执行`run --stdout --id pg-aggregates-0410-f6f52dc3 --id pg-aggregates-0412-cbdaef84`：两条仍是行值或顺序不匹配，实际只见PG花括号数组与Doris方括号数组显示不同。返回元素和INT类型已另补证；没有将主报告改成MATCH。
