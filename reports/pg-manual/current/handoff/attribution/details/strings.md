# strings：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 25 | 15 | 10 | 5 | 10 |


[YAML](../../../../../../cases/postgres/manual/current/strings.yaml)；[首轮 Markdown](../../../validation/strings/validation.md) / [首轮 JSON](../../../validation/strings/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-strings-0020-46869892

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 20，源行 60–60，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT E'\\xDeAdBeEf'::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('\\xDeAdBeEf' AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=01c9c470e9cd10a6d35a6ef5ea454bd7607a7591b66747395ef445d62db67893",
    "doris_digest=c5e635c4ec9ab2719fda17c1bec96a47ececd8dd968c4c3a84b666a151b2f4bd",
    "source_sample=[['\\\\xdeadbeef']]",
    "doris_sample=[['\\\\x5c784465416442654566']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0021-ae59d612

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 21，源行 61–61，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT E'\\x De Ad Be Ef '::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('\\x De Ad Be Ef ' AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=01c9c470e9cd10a6d35a6ef5ea454bd7607a7591b66747395ef445d62db67893",
    "doris_digest=eb4bcf7a9b9db0a1dec554d29513b130681a76fc1273931d8674468b0532b071",
    "source_sample=[['\\\\xdeadbeef']]",
    "doris_sample=[['\\\\x5c7820446520416420426520456620']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0024-6c140ab7

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 24，源行 64–64，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT E'\\xDe00BeEf'::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST('\\xDe00BeEf' AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=a982288662f311ce3e738173b49874fb514c22729686aa47327acc00e39375b1",
    "doris_digest=7fc8df761980ec4fc55bda12b81066c301b372ffbaa1be3a89ce88afc82d8f1d",
    "source_sample=[['\\\\xde00beef']]",
    "doris_sample=[['\\\\x5c784465303042654566']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0031-8e9f8b96

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 31，源行 72–72，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT reverse(''::bytea);
~~~

社区生成 SQL：


~~~sql
SELECT REVERSE(CAST('' AS VARBINARY))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7fbd83b939069a093f42c70edd4b51dbe46a49e9fe30b3cb941b3b9d39b7a1b3",
    "doris_digest=c6bb4cfd0414fb9422955049899642caafb6bada2194f68145f385cf34bb4daf",
    "source_sample=[['\\\\x']]",
    "doris_sample=[['']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0032-725f994c

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 32，源行 73–73，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT reverse('\xaa'::bytea);
~~~

社区生成 SQL：


~~~sql
SELECT REVERSE(CAST('\\xaa' AS VARBINARY))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=840a6651e3777e3de029fa353cd4e0cd5f5b8341be2de32c48e9bf978cf8d9ec",
    "doris_digest=bb51b246c970af4b09a7267b6b1579445edd33c632a67e7e462203f53f0934aa",
    "source_sample=[['\\\\xaa']]",
    "doris_sample=[['161687C5']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0033-94ebc8b4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 33，源行 74–74，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT reverse('\xabcd'::bytea);
~~~

社区生成 SQL：


~~~sql
SELECT REVERSE(CAST('\\xabcd' AS VARBINARY))
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=14f89d22920f0e792d61d24c31b9c0e7c045b58d8bb09190a372e9a47821c084",
    "doris_digest=8021410479cea8adf9b9aecdf77cc339c19f7797001c9d0432537aa3e260a446",
    "source_sample=[['\\\\xcdab']]",
    "doris_sample=[['4636261687C5']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0034-3f6aec47

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 34，源行 76–76，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ('\x' || repeat(' ', 32))::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST((CONCAT('\\x', REPEAT(' ', 32))) AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=7fbd83b939069a093f42c70edd4b51dbe46a49e9fe30b3cb941b3b9d39b7a1b3",
    "doris_digest=18320019829bdad51caf4d032bc44f107629fa21d0d28c38a5683d102b9c040c",
    "source_sample=[['\\\\x']]",
    "doris_sample=[['\\\\x5c782020202020202020202020202020202020202020202020202020202020202020']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0037-bde4500e

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 37，源行 79–79，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ('\x' || repeat('0', 34))::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST((CONCAT('\\x', REPEAT('0', 34))) AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=b67036c8203a7d119de7852befba20fb8bf9276c5518eb71791b33324479b92a",
    "doris_digest=3f82b5f36cde3d4e73014d0496657c3587c86c5b8dbc228a4be09578a2378044",
    "source_sample=[['\\\\x0000000000000000000000000000000000']]",
    "doris_sample=[['\\\\x5c7830303030303030303030303030303030303030303030303030303030303030303030']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0038-ea34a948

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 38，源行 80–80，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT ('\x' || repeat('9', 32))::bytea;
~~~

社区生成 SQL：


~~~sql
SELECT CAST((CONCAT('\\x', REPEAT('9', 32))) AS VARBINARY)
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=c5f981581c01b541c4a3c0bbf0853b09332f2fa536ac24724b0e67d3e03c3cea",
    "doris_digest=167b56a8a015661b6366bf18a92855d0db449b36fd1c9beb4ed77c4d04361854",
    "source_sample=[['\\\\x99999999999999999999999999999999']]",
    "doris_sample=[['\\\\x5c783939393939393939393939393939393939393939393939393939393939393939']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-strings-0063-9c7971d4

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/strings.out)；原语句 63，源行 116–116，同文回显第 1 次；历史成功 1 行。

- 首轮：两端执行状态不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CAST(name 'namefield' AS text) AS "text(name)";
~~~

社区生成 SQL：


~~~sql
SELECT CAST(CAST('namefield' AS NAME) AS STRING) AS `text(name)`
~~~

Doris 原错误：


~~~text
(1105, "errCode = 2, detailMessage = \nno viable alternative at input 'CAST(CAST('namefield' AS NAME'(line 1, pos 32)\n")
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "EXECUTION_STATUS_MISMATCH",
  "summary": "Source evidence and Doris execution status differ",
  "details": [
    "source_success=True",
    "doris_success=False",
    "doris_error_category=CAST_ERROR",
    "doris_error_message=(1105, \"errCode = 2, detailMessage = \\nno viable alternative at input 'CAST(CAST('namefield' AS NAME'(line 1, pos 32)\\n\")",
    "doris_error_code=1105"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。


| 查询编号、完整源 SQL 与原件 | 源端具体错误 | 首轮已有目标表现 | 本轮处理与理由 | 正常输入线索 |
| :--- | :--- | :--- | :--- | :--- |
| pg-strings-0002-23a85b3e / SELECT 'first line'<br>' - next line' /* this comment is not allowed here */<br>' - third line'<br>	AS "Illegal comment within continuation"; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 2 | syntax error at or near "' - third line'" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0008-628bbef4 / SELECT E'wrong: \u061'; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 8 | invalid Unicode escape | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0009-3773aff8 / SELECT E'wrong: \U0061'; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 9 | invalid Unicode escape | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0010-d78059f9 / SELECT E'wrong: \udb99'; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 10 | invalid Unicode surrogate pair at or near "'" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0011-b4e07692 / SELECT E'wrong: \udb99xy'; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 11 | invalid Unicode surrogate pair at or near "x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0022-83bb66d5 / SELECT E'\\xDeAdBeE'::bytea; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 22 | invalid hexadecimal data: odd number of digits | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0023-888566e4 / SELECT E'\\xDeAdBeEx'::bytea; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 23 | invalid hexadecimal digit: "x" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0035-e6cacfe5 / SELECT ('\x' \|\| repeat('!', 32))::bytea; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 35 | invalid hexadecimal digit: "!" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0036-5df2fb83 / SELECT ('\x' \|\| repeat('/', 34))::bytea; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 36 | invalid hexadecimal digit: "/" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |
| pg-strings-0039-1b312cd9 / SELECT ('\x' \|\| repeat(':', 32))::bytea; / [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 39 | invalid hexadecimal digit: ":" | 两端执行状态不同；Doris 执行成功 | 默认不纳入主修复范围，未安排独立改写 | 本轮未据本条单独建立修复任务 |


## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-strings-0001-13d8d27f | SELECT 'first line'<br>' - next line'<br>	' - third line'<br>	AS "Three lines to one"; | [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 1 |
| pg-strings-0005-bd29f989 | SELECT U&'a\\b' AS "a\b"; | [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 5 |
| pg-strings-0007-dc647027 | SELECT E'a\\b' AS "a\b"; | [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 7 |
| pg-strings-0025-7c862617 | SELECT E'DeAdBeEf'::bytea; | [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 25 |
| pg-strings-0064-545e0a8a | SELECT CAST(f1 AS char(10)) AS "char(text)" FROM TEXT_TBL; | [.out](../../../../../../cases/postgres/manual/current/assets/strings.out)，语句 64 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

