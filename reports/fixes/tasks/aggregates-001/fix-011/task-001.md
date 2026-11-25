# task-001：数组构造类型核验（fix-011）

## 1. 当前结论

**仍为“已修改但未完成验收”。** 语法构造和既有值保留逻辑没有撤回；本轮完成14条关联原查询及18条既有边界的类型补查。18条边界均成功、当前值和重复执行稳定，但只有9条在本轮取得的全部输出类型约束上对齐；7条存在数组默认元素类型差异，1条存在独立 id 列位宽差异，1条 Decimal 结果精度声明不能判相等。不能把“有了详细类型证据”写成“所有类型通过”。

任务沿用[task-001](../../../../attribution/aggregates-001-attribution-summary.md#task-001)，不新建编号。此前[fix-001报告](../fix-001/task-001.md)保留为历史，本轮补充而不覆盖。共同代码身份、授权、执行入口、142 条原查询回归和测试见[本轮汇总](../../../aggregates-001-fix-011-summary.md)。本轮继续使用 HEAD 089891f2521780e2c5b243005017af9db62f25a6 和前十轮未提交修改，累积 diff SHA256 为 444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18，**本轮没有修改 SQLGlot 代码、框架或数据，未 commit/push**。

## 2. 取证方法与实际范围

原14条按原阶段 YAML/.out 运行，阶段为01、03、17、31、33、40、42；全部实时PG成功，PG文本包装结果与各自 .out 相同。目标来自当前 `SqlglotTranspiler.transpile_case`，没有手写答案代替生成器验收；遇 ARRAY 子查询构造拒绝不执行目标。

18个边界的完整源SQL在[原报告4.2](../fix-001/task-001.md#42-数据库边界实际源-sql-与生成-sql)；本轮逐条从这些源SQL重新转译、双端执行并重复一次，不是重数旧报告。通过 `cursor.pgresult.fmod(i)`、`cursor.description` 与只读 `SELECT oid,typname,typelem FROM pg_type` 补查源字段；目标类型仍来自 EXPLAIN VERBOSE。每条10秒、最多10000行，不使用截断数据。40条共用边界批次结束于2026-11-24 11:12:07（Asia/Shanghai），原查询回归结束于11:12:44。

只对本轮明确取到的原生类型作人工递归核对：_int4↔ARRAY<INT>、_int8↔ARRAY<BIGINT>、_float4↔ARRAY<FLOAT>、_text↔ARRAY<TEXT/STRING>；**不把 _int4↔ARRAY<TINYINT>、TEXT↔VARCHAR(5) 也算成相同**。没有修改 Comparator，原 .out 的文本差异仍保留。

## 3. 十八条边界的类型结论

| 既有边界 | PostgreSQL 原生类型/协议 typmod | Doris 实际类型 | 本轮判断 |
| :--- | :--- | :--- | :--- |
| 普通整数 | _int4; typmod=-1 | array<tinyint> | 真实数组元素类型不同，当前值相同不足以验收 |
| 元素 NULL 与重复 | _int4; typmod=-1 | array<tinyint> | 真实数组元素类型不同，当前值相同不足以验收 |
| 显式 INT 的全 NULL | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| 显式 INT 空数组 | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| 矩形嵌套 | _int4; typmod=-1 | array<array<tinyint>> | 真实数组元素类型不同，当前值相同不足以验收 |
| 显式 BIGINT | _int8; typmod=-1 | array<bigint> | 本次类型约束及值对齐 |
| 显式 Decimal | _numeric(10,2); typmod=655366 | array<decimalv3(10,2)> | 本次类型约束及值对齐 |
| 空字符串/Unicode/NULL | _text; typmod=-1 | array<text> | 本次类型约束及值对齐 |
| 运行时 NULL 与重复行 | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| 单个标量子查询元素 | _int4; typmod=-1 | array<tinyint> | 真实数组元素类型不同，当前值相同不足以验收 |
| 两个标量子查询元素 | _int4; typmod=-1 | array<tinyint> | 真实数组元素类型不同，当前值相同不足以验收 |
| 标量子查询无行 | _int4; typmod=-1 | array<tinyint> | 真实数组元素类型不同，当前值相同不足以验收 |
| 整数组为 SQL NULL | _int4; typmod=-1 | array<int> | 本次类型约束及值对齐 |
| 稳定 id 最终排序 | int4; typmod=-1 / _int4; typmod=-1 | tinyint / array<int> | 数组 INT32 对齐；独立 id 列 int4/tinyint 不同 |
| BIGINT 两端边界 | _int8; typmod=-1 | array<bigint> | 本次类型约束及值对齐 |
| Decimal 正负边界 | _numeric; typmod=-1 | array<decimalv3(13,2)> | 源结果未携带(10,2)；目标(13,2)，不能断言精度声明相同 |
| 未显式类型的全 NULL | _text; typmod=-1 | array<null_type> | 真实数组元素类型不同，当前值相同不足以验收 |
| 显式 REAL | _float4; typmod=-1 | array<float> | 本次类型约束及值对齐 |

所有18条原规则下结构化值比较均为一致，双端各重复一次均稳定；带最终ORDER BY的唯一id查询保持1、2、3，其他查询不要求结果行顺序。数组元素顺序始终保留，没有为类型验收任意排序。

BIGINT 精度另外用Python原生读取核对：`[([-9223372036854775808, 9223372036854775807],)]`；Doris数组文本逐位相同。不能把展示层将大整数转为JavaScript Number后的舍入当数据库结果；本轮未改报告器或框架。

### 3.1 Decimal 元数据的更正

显式 `ARRAY[1.25::DECIMAL(10,2),NULL::DECIMAL(10,2)]` 本轮取得源OID1231、typmod655366、precision10/scale2，目标ARRAY<DECIMALV3(10,2)>，该边界不再笼统记“所有Decimal源元数据都缺失”。

相反，`ARRAY[-99999999.99::DECIMAL(10,2),...]` 的源数组typmod=-1，目标ARRAY<DECIMALV3(13,2)>。前面的负号在AST中是外层Neg，不能拿子CAST的(10,2)当成整个结果的已声明约束。额外标量 `SELECT -CAST(99999999.99 AS DECIMAL(10,2)) AS x` 不含数组也产生PG NUMERIC / Doris DECIMALV3(13,2)。这是通用数值表达式/精度契约问题，不能归为ARRAY构造吞CAST。

[PostgreSQL PQfmod文档](https://www.postgresql.org/docs/18/libpq-exec.html)说明-1表示没有可用的type-modifier信息；它既不是驱动丢失655366，也不能据此证明所有可能数值都由目标固定Decimal完整覆盖。当前值相同，不足以关闭整个类型域。

## 4. 默认类型缺口与独立CAST候选

当前生成与实际类型：

~~~sql
-- PostgreSQL: _int4
SELECT ARRAY[1,NULL,2] AS xs;
-- 当前SQLGlot: ARRAY<TINYINT>
SELECT ARRAY(1, NULL, 2) AS xs;

-- PostgreSQL: _text
SELECT ARRAY[NULL] AS xs;
-- 当前SQLGlot: ARRAY<NULL_TYPE>
SELECT ARRAY(NULL) AS xs;
~~~

额外实际执行的**人工类型候选**：

~~~sql
SELECT CAST(ARRAY(1, NULL, 2) AS ARRAY<INT>) AS xs;
SELECT CAST(ARRAY(NULL) AS ARRAY<STRING>) AS xs;
SELECT CAST(ARRAY('hello', 'world') AS ARRAY<STRING>) AS xs;
~~~

分别得到ARRAY<INT>、ARRAY<TEXT>、ARRAY<TEXT>；本轮样本的源元素类型/值可对齐，说明不应把缺口直接判成“Doris不能表达”。它们不是生成器补丁，不计为已修复。

也实际执行了错误的统一INT候选：

~~~sql
-- 成功源SQL，源数组为int8[]，值为2147483648
SELECT ARRAY[2147483648] AS xs;
-- 不能采用的独立候选：目标返回[NULL]，不是原数值
SELECT CAST(ARRAY(2147483648) AS ARRAY<INT>) AS xs;
~~~

当前未改写的 `ARRAY(2147483648)` 本来正确返回ARRAY<BIGINT>及原值。不能为了小整数样本正确，把所有数组都硬转INT。

### 4.1 为什么本轮不直接接入 annotate_types

实测当前类型推断：`ARRAY[1.25,2]` 标为ARRAY<DOUBLE>，但PG原生为numeric[]；`ARRAY[NULL]` 标为ARRAY<NULL>，但PG为text[]。因此“推断什么就CAST什么”会引入新的错误，不能把通用类型标注当成PG语义分析器。

[PG共同类型规则](https://www.postgresql.org/docs/18/typeconv-union-case.html)同时影响ARRAY、VALUES、CASE等；unknown全体输入默认text，整数/小数/显式类型还要共同求型。后续需要保留可证明的源类型，再生成目标CAST；源类型未知时不能猜，不强制给框架注入表Schema。

## 5. 原查询现状（14条）

| Case / stage | 原 .out 规则的实际结果 | PG / Doris 原生类型 | 具体限制 |
| :--- | :--- | :--- | :--- |
| [0010](../../../../attribution/cases/aggregates-001/pg-aggregates-0010-12bf388c.md) / 01 | 行值或顺序不匹配 | _text / array<varchar(5)> | 值/表示及类型需分别看下文 |
| [0136](../../../../attribution/cases/aggregates-001/pg-aggregates-0136-4243166e.md) / 03 | SQLGlot 转译失败 | _int8 / 无成功目标字段 | ARRAY 子查询构造仍被排除 |
| [0306](../../../../attribution/cases/aggregates-001/pg-aggregates-0306-e70870c4.md) / 17 | 匹配 | text, numeric / varchar(65533), bigint | 仅原 .out 显示匹配；原生类型差异保留 |
| [0410](../../../../attribution/cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md) / 31 | Doris 执行失败 | _int4 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 76)\n") |
| [0411](../../../../attribution/cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md) / 31 | Doris 执行失败 | _float8 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 66)\n") |
| [0412](../../../../attribution/cases/aggregates-001/pg-aggregates-0412-cbdaef84.md) / 31 | Doris 执行失败 | _int4 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 89)\n") |
| [0413](../../../../attribution/cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) / 31 | Doris 执行失败 | _float8 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 97)\n") |
| [0415](../../../../attribution/cases/aggregates-001/pg-aggregates-0415-16b30942.md) / 31 | Doris 执行失败 | _text / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmissing 'BY' at '('(line 1, pos 60)\n") |
| [0434](../../../../attribution/cases/aggregates-001/pg-aggregates-0434-5da33736.md) / 33 | Doris 执行失败 | int8 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 26)\n") |
| [0437](../../../../attribution/cases/aggregates-001/pg-aggregates-0437-d68f01c2.md) / 33 | Doris 执行失败 | numeric / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 27)\n") |
| [0438](../../../../attribution/cases/aggregates-001/pg-aggregates-0438-998adec3.md) / 33 | Doris 执行失败 | regtype / 无成功目标字段 | (1105, "errCode = 2, detailMessage = \nmismatched input 'ARRAY' expecting {')', ',', 'ORDER'}(line 1, pos 37)\n") |
| [0534](../../../../attribution/cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) / 40 | Doris 执行失败 | _float4, _float4 / 无成功目标字段 | (1105, "errCode = 2, detailMessage = Can not found function 'RWAGG'") |
| [0551](../../../../attribution/cases/aggregates-001/pg-aggregates-0551-f476de2c.md) / 42 | 匹配 | text, int4, int8 / varchar(65533), tinyint, bigint | 仅原 .out 显示匹配；原生类型差异保留 |
| [0552](../../../../attribution/cases/aggregates-001/pg-aggregates-0552-7ea82af2.md) / 42 | 匹配 | text, int4, int8 / varchar(65533), tinyint, bigint | 仅原 .out 显示匹配；原生类型差异保留 |

合计3条显示匹配、1条显示/值差异、9条Doris失败、1条转译拒绝。4条双端成功查询仍各有类型差异；不能把其中3条 .out 匹配当类型通过。0136是任务明确排除的ARRAY(SELECT...)，保留关联和事实，不假装补齐。

VARIADIC三条的数据库错误来自CLI真实执行；额外Doris只读补证入口在Parser前置检查即拒绝，不能把该前置拒绝当成又一次数据库执行。WITHIN GROUP、UDF、ARRAY子查询及SUM/CASE返回类型不混入本任务补丁。

## 6. 验收子项与下一步

| 沿用task-001的具体类型验收子项 | 当前状态 | 后续要求 |
| :--- | :--- | :--- |
| 已显式INT/BIGINT/REAL/同约束Decimal元素 | 已测9条可核对，源码不需为这些样本再改 | 保留NULL、空数组、极值、标量子查询和往返回归 |
| 裸整数/子查询整数的源元素类型保留 | 未完成，存在INT32/TINYINT真差异 | 在生成器取得可信源类型；区分INT4/INT8/NUMERIC边界，不硬转INT |
| 全unknown/NULL、字符串默认元素类型 | 未完成，text[]与NULL_TYPE/VARCHAR(n)有差异 | 按PG共同求型规则保留text，不能在Python折叠NULL答案 |
| Decimal结果约束与负号/共同求型 | 部分补证完成，不做全域验收 | 保留typmod事实，明确有/无约束结果的类型契约，不把源子CAST当结果声明 |
| 已有完整查询中的其他类型问题 | 不在数组构造中偷修 | 归到现有通用类型/精度研究，按独立行为另定范围 |

本轮没有已验证的通用类型补丁，所以不为完成标题而修改代码。task-001保持“已修改但未完成验收”；不是认定问题不可修，也不将独立候选通过当最终修复。建议下一轮先限定源共同类型保留的安全实现，再回归这里所有关联Case。没有自动扩大到全局字面量/VALUES/时间/比较器修复。

