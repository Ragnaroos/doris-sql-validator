# case：PostgreSQL → Doris 归因明细

参考运行日期：2026-11-13。[汇总](../attribution-summary.md) / [任务](../sqlglot-tasks.md)。

## 1. 输入与范围


| 总数 | 源成功 | 源负向（默认不改写） | 首轮成功匹配 | 主范围差异 |
| :--- | :--- | :--- | :--- | :--- |
| 8 | 8 | 0 | 6 | 2 |


[YAML](../../../../../../cases/postgres/manual/current/case.yaml)；[首轮 Markdown](../../../validation/case/validation.md) / [首轮 JSON](../../../validation/case/validation.json)。原件未修改，每条 .out 均重新读取。

PG 18.1 / Doris 4.1.3-rc02；两端 UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false。执行前后外部只读核验既有 21 张表/视图未变，没有建表装数。NAME/TEXT 到 VARCHAR(512) 等准备映射仍限制类型域。

下文“已确认（当前样本）”仅限当前工具已识别的执行、类型声明、行值及必要顺序，不是全类型域/全边界同义证明；类型元数据不足不当通过。未执行或证据不足不能当成确定缺陷。

## 2. 源端成功但首轮存在差异的查询

### pg-case-0019-fe72fa57

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/case.out)；原语句 19，源行 66–67，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CASE WHEN 1=0 THEN 1/0 WHEN 1=1 THEN 1 ELSE 2/0 END;
~~~

社区生成 SQL：


~~~sql
SELECT CASE WHEN 1 = 0 THEN 1 / 0 WHEN 1 = 1 THEN 1 ELSE 2 / 0 END
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

### pg-case-0020-eef1e7fd

- 结论强度：未执行。

- 源证据：[.out](../../../../../../cases/postgres/manual/current/assets/case.out)；原语句 20，源行 68–68，同文回显第 1 次；历史成功 1 行。

- 首轮：行值、重复次数或要求的顺序不同。

#### 源 SQL、社区输出与首轮差异


~~~sql
SELECT CASE 1 WHEN 0 THEN 1/0 WHEN 1 THEN 1 ELSE 2/0 END;
~~~

社区生成 SQL：


~~~sql
SELECT CASE 1 WHEN 0 THEN 1 / 0 WHEN 1 THEN 1 ELSE 2 / 0 END
~~~

首轮比较信息（最多五行样本，不是完整结果）：


~~~json
{
  "observed_outcome": "ROW_VALUE_MISMATCH",
  "summary": "Normalized result row values differ",
  "details": [
    "source_digest=8ef9fc24093322acce11a5335df997ff0960dabcce3733690efb0a4cc738f0ab",
    "doris_digest=61c7ad9b0d0ce9461f0af1d3abbb2a879c90a16bb9b313dc2279773d1fdab390",
    "source_sample=[['1']]",
    "doris_sample=[['1.0']]"
  ]
}
~~~

#### 下一步

尚未逐条独立改写/执行；当前只证明上述首轮差异，不能直接区分 SQLGlot、Doris、类型/驱动或会话原因。下一步按具体操作阅读 Parser/AST/Generator，构造不依赖源答案的候选，再实测并补相关边界；不能据错误类别直接安排补丁。

## 3. 源端负向用例（默认不纳入主修复）

原 .out 本来报错。本轮无论首轮 MATCH、两端状态不同还是错误不同，均不为复制 PG 错误逐条改写，不作为未完成的错误复刻积压。PG_INPUT_IS_VALID 等函数成功返回 false 不属于负向查询。

本组没有负向查询。

## 4. 首轮成功匹配（简写）

这些查询仅在原 .out 能提供的证据上未发现差异；本轮没有逐条补齐原生类型、顺序与全部边界，不能升级为完整语义证明。


| 编号 | 源 SQL | 原件 |
| :--- | :--- | :--- |
| pg-case-0013-00d1dea8 | SELECT '3' AS "One",<br>  CASE<br>    WHEN 1 < 2 THEN 3<br>  END AS "Simple WHEN"; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 13 |
| pg-case-0014-068371ac | SELECT '<NULL>' AS "One",<br>  CASE<br>    WHEN 1 > 2 THEN 3<br>  END AS "Simple default"; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 14 |
| pg-case-0015-06669704 | SELECT '3' AS "One",<br>  CASE<br>    WHEN 1 < 2 THEN 3<br>    ELSE 4<br>  END AS "Simple ELSE"; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 15 |
| pg-case-0016-2c1e1463 | SELECT '4' AS "One",<br>  CASE<br>    WHEN 1 > 2 THEN 3<br>    ELSE 4<br>  END AS "ELSE default"; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 16 |
| pg-case-0017-47ffe574 | SELECT '6' AS "One",<br>  CASE<br>    WHEN 1 > 2 THEN 3<br>    WHEN 4 < 5 THEN 6<br>    ELSE 7<br>  END AS "Two WHEN with default"; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 17 |
| pg-case-0022-83be6299 | SELECT CASE 'a' WHEN 'a' THEN 1 ELSE 2 END; | [.out](../../../../../../cases/postgres/manual/current/assets/case.out)，语句 22 |


## 5. 导入诊断核查

原完整脚本非普通跳过诊断 0 条，未必处于本轮固定选择中。没有对应源成功证据不能算转换缺陷；DDL/DML 普通跳过不计缺陷。

没有需要单列的解析/配对异常诊断。

