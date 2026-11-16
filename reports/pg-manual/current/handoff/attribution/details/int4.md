# int4：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 40 | 34 | 6 | 30 | 4 |


[YAML](../../../../../../cases/postgres/manual/current/int4.yaml)；[首轮 Markdown](../../../validation/int4/validation.md) / [首轮 JSON](../../../validation/int4/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-int4-0040-453402df

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/int4.out)；原语句 40，源行 86–86，同文回显第 1 次；历史成功 5 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT i.f1, i.f1 / int2 '2' AS x FROM INT4_TBL i;
~~~

社区生成 SQL：


~~~sql
SELECT i.f1, i.f1 / CAST('2' AS SMALLINT) AS x FROM INT4_TBL AS i
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=6552d66a5fc53b4eab60d0fece328cf32edbf1f8e70c599f416710c0397bf8d9",
    "doris_digest=60e187ecf39a0f77b1b37f963f6251c6186e4d6b8a27e70c9d9bd2bdf6a3cfe5",
    "source_sample=[['0', '0'], ['123456', '61728'], ['-123456', '-61728'], ['2147483647', '1073741823'], ['-2147483647', '-1073741823']]",
    "doris_sample=[['-2147483647', '-1073741823.5'], ['-123456', '-61728.0'], ['0', '0.0'], ['123456', '61728.0'], ['2147483647', '1073741823.5']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-int4-0041-7027be1a

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/int4.out)；原语句 41，源行 88–88，同文回显第 1 次；历史成功 5 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT i.f1, i.f1 / int4 '2' AS x FROM INT4_TBL i;
~~~

社区生成 SQL：


~~~sql
SELECT i.f1, i.f1 / CAST('2' AS INT) AS x FROM INT4_TBL AS i
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=6552d66a5fc53b4eab60d0fece328cf32edbf1f8e70c599f416710c0397bf8d9",
    "doris_digest=60e187ecf39a0f77b1b37f963f6251c6186e4d6b8a27e70c9d9bd2bdf6a3cfe5",
    "source_sample=[['0', '0'], ['123456', '61728'], ['-123456', '-61728'], ['2147483647', '1073741823'], ['-2147483647', '-1073741823']]",
    "doris_sample=[['-2147483647', '-1073741823.5'], ['-123456', '-61728.0'], ['0', '0.0'], ['123456', '61728.0'], ['2147483647', '1073741823.5']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-int4-0051-b8fd3a8e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/int4.out)；原语句 51，源行 113–113，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT 2 + 2 / 2 AS three;
~~~

社区生成 SQL：


~~~sql
SELECT 2 + 2 / 2 AS three
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7e5acccc8c8fd7375f8700c06ef68c1dbf50eb98c0bb12527a571aade278a5a7",
    "doris_digest=3bb8608d7cea8e84f6ca133a32de72a928d916997d2a0d4933d1d60b03d47714",
    "source_sample=[['3']]",
    "doris_sample=[['3.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-int4-0052-78fd8444

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/int4.out)；原语句 52，源行 115–115，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT (2 + 2) / 2 AS two;
~~~

社区生成 SQL：


~~~sql
SELECT (2 + 2) / 2 AS two
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a0a88ee57364f8f632469bb45e2fd5057419c8c1c1f6d52216176988ab0fbb90",
    "doris_digest=069ad5bfea6175ddb5c7be34b4c5ed1e9db905ab759a002e8b54040c721d3ed9",
    "source_sample=[['2']]",
    "doris_sample=[['2.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-int4-0028-eefe8f02 / SELECT i.f1, i.f1 * int2 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 28 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-int4-0030-6b7df65d / SELECT i.f1, i.f1 * int4 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 30 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-int4-0032-3a22f62e / SELECT i.f1, i.f1 + int2 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 32 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-int4-0034-6b91aedb / SELECT i.f1, i.f1 + int4 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 34 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-int4-0036-e81aa3e1 / SELECT i.f1, i.f1 - int2 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 36 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-int4-0038-a51d16a9 / SELECT i.f1, i.f1 - int4 '2' AS x FROM INT4_TBL i; / [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 38 | integer out of range | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-int4-0009-078b9c31 | SELECT * FROM INT4_TBL; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 9 |
| pg-int4-0014-c8657bed | SELECT i.* FROM INT4_TBL i WHERE i.f1 <> int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 14 |
| pg-int4-0015-82a1513e | SELECT i.* FROM INT4_TBL i WHERE i.f1 <> int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 15 |
| pg-int4-0016-31c9f66b | SELECT i.* FROM INT4_TBL i WHERE i.f1 = int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 16 |
| pg-int4-0017-074bc95e | SELECT i.* FROM INT4_TBL i WHERE i.f1 = int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 17 |
| pg-int4-0018-e2dc2ba8 | SELECT i.* FROM INT4_TBL i WHERE i.f1 < int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 18 |
| pg-int4-0019-e5704751 | SELECT i.* FROM INT4_TBL i WHERE i.f1 < int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 19 |
| pg-int4-0020-11086ee7 | SELECT i.* FROM INT4_TBL i WHERE i.f1 <= int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 20 |
| pg-int4-0021-21a0f97d | SELECT i.* FROM INT4_TBL i WHERE i.f1 <= int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 21 |
| pg-int4-0022-a6f61707 | SELECT i.* FROM INT4_TBL i WHERE i.f1 > int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 22 |
| pg-int4-0023-80e75b67 | SELECT i.* FROM INT4_TBL i WHERE i.f1 > int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 23 |
| pg-int4-0024-d9210ff8 | SELECT i.* FROM INT4_TBL i WHERE i.f1 >= int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 24 |
| pg-int4-0025-62c22a17 | SELECT i.* FROM INT4_TBL i WHERE i.f1 >= int4 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 25 |
| pg-int4-0026-92feef12 | SELECT i.* FROM INT4_TBL i WHERE (i.f1 % int2 '2') = int2 '1'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 26 |
| pg-int4-0027-085daa53 | SELECT i.* FROM INT4_TBL i WHERE (i.f1 % int4 '2') = int2 '0'; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 27 |
| pg-int4-0029-4c7c4839 | SELECT i.f1, i.f1 * int2 '2' AS x FROM INT4_TBL i<br>WHERE abs(f1) < 1073741824; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 29 |
| pg-int4-0031-67c41555 | SELECT i.f1, i.f1 * int4 '2' AS x FROM INT4_TBL i<br>WHERE abs(f1) < 1073741824; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 31 |
| pg-int4-0033-5c001408 | SELECT i.f1, i.f1 + int2 '2' AS x FROM INT4_TBL i<br>WHERE f1 < 2147483646; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 33 |
| pg-int4-0035-d0213214 | SELECT i.f1, i.f1 + int4 '2' AS x FROM INT4_TBL i<br>WHERE f1 < 2147483646; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 35 |
| pg-int4-0037-487a22b0 | SELECT i.f1, i.f1 - int2 '2' AS x FROM INT4_TBL i<br>WHERE f1 > -2147483647; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 37 |
| pg-int4-0039-b96c072f | SELECT i.f1, i.f1 - int4 '2' AS x FROM INT4_TBL i<br>WHERE f1 > -2147483647; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 39 |
| pg-int4-0042-39e2d6da | SELECT -2+3 AS one; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 42 |
| pg-int4-0043-d3556909 | SELECT 4-2 AS two; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 43 |
| pg-int4-0044-f3e02ee8 | SELECT 2- -1 AS three; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 44 |
| pg-int4-0045-59e42e3a | SELECT 2 - -2 AS four; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 45 |
| pg-int4-0046-f781f855 | SELECT int2 '2' * int2 '2' = int2 '16' / int2 '4' AS true; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 46 |
| pg-int4-0047-2218e186 | SELECT int4 '2' * int2 '2' = int2 '16' / int4 '4' AS true; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 47 |
| pg-int4-0048-1f470dee | SELECT int2 '2' * int4 '2' = int4 '16' / int2 '4' AS true; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 48 |
| pg-int4-0049-6c0d3f66 | SELECT int4 '1000' < int4 '999' AS false; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 49 |
| pg-int4-0050-ea0ab753 | SELECT 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 AS ten; | [.out](../../../../../../cases/postgres/manual/current/assets/int4.out)，语句 50 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

