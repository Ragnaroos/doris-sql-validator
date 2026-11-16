# collate：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 4 | 3 | 1 | 3 | 0 |


[YAML](../../../../../../cases/postgres/manual/current/expanded/collate.yaml)；[首轮 Markdown](../../../validation/collate/validation.md) / [首轮 JSON](../../../validation/collate/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-collate-0080-62d6468d / SELECT CAST('42' AS text COLLATE "C"); / [.out](../../../../../../cases/postgres/manual/current/expanded/assets/collate.out)，语句 80 | syntax error at or near "COLLATE" | 两端错误表现不同；(1105, "errCode = 2, detailMessage = \nmissing ')' at 'COLLATE'(line 1, pos 27)\n") | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-collate-0026-af6ea175 | SELECT 'bbc' COLLATE "C" > 'Abc' COLLATE "C" AS "true"; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/collate.out)，语句 26 |
| pg-collate-0027-d8db4eff | SELECT 'bbc' COLLATE "POSIX" < 'Abc' COLLATE "POSIX" AS "false"; | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/collate.out)，语句 27 |
| pg-collate-0076-6c178227 | SELECT a, b, a < b as lt FROM<br>  (VALUES ('a', 'B'), ('A', 'b' COLLATE "C")) v(a,b); | [.out](../../../../../../cases/postgres/manual/current/expanded/assets/collate.out)，语句 76 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 4 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。


| 语句编号 | 源行 | 诊断 | 原因 |
| :--- | :--- | :--- | :--- |
| 129 | 272–272 | error | Invalid expression / Unexpected token. Line 1, Col: 20.<br>  SELECT collation [4mfor[0m ('foo'); |
| 130 | 272–273 | error | Invalid expression / Unexpected token. Line 1, Col: 20.<br>  SELECT collation [4mfor[0m ('foo'::text); |
| 131 | 274–274 | error | Invalid expression / Unexpected token. Line 1, Col: 20.<br>  SELECT collation [4mfor[0m ((SELECT a FROM collate_test1 LIMIT 1)); |
| 132 | 274–275 | error | Invalid expression / Unexpected token. Line 1, Col: 20.<br>  SELECT collation [4mfor[0m ((SELECT b FROM collate_test1 LIMIT 1)); |


