# task-006 / fix-006：PostgreSQL EVERY 识别与 Doris 布尔聚合

> 代码保存更新（2026-11-24）：原轮次“未提交”为当时事实。此次仅整理既有代码和测试，未增加新功能；本task对应本地commit：`872a926e936e8c12bc3681da4105c85ac2fcb778`。保存EVERY归一化及测试；原约定验收结论不变。 后续checkout为 `../sqlglot-functional-commits`，分支 `codex/doris-functional-commits`，整组HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；未push。各commit父提交、准确测试状态及最终142条/97+41边界回归见[归因汇总的提交重建结果](../../../../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。

## 1. 结论与任务范围

**已修复并完成约定验收。** 原查询 `pg-aggregates-0149-d636fc82` 现在按原 .out 匹配，且实时 PG/Doris 的六个字段、布尔类型、NULL、结果及重复执行一致。不是仅比较文本，也不是仅使用手写 Doris 候选。

- 入口：[原任务](../../../../attribution/aggregates-001-attribution-summary.md#task-006)、[原 Case](../../../../attribution/cases/aggregates-001/pg-aggregates-0149-d636fc82.md)。原语句编号 149，行 390–397，出现序号 1，stage-07。
- 范围：成功源查询中的标准 BOOLEAN `EVERY` 普通聚合，含 NOT、DISTINCT、NULL、空输入及已实测上下文。
- 排除：整数/字符串强制转换、严格内部 booland_statefunc/boolor_statefunc、窗口、FILTER 和聚合内部 ORDER BY 的语义验收；不根据未知 UDF 名称全局替换。
- 独立行为：PostgreSQL 的 EVERY 别名识别。无其他 task 的实现依赖；不夹带布尔 OR、统计函数或查询级改写。
- 模式：指定任务，本轮未 commit/push，未创建 Issue/PR。共同版本、输入指纹、回归及授权见[本轮汇总](../../../aggregates-001-fix-006-summary.md)。整份输入仍未完成。

## 2. 修复依据与实际实现

修复前现场重现：EVERY 被解析为 Anonymous，生成 Doris `EVERY(...)`，目标报错：

```text
(1105, "errCode = 2, detailMessage = Can not found function 'EVERY'")
```

同环境控制 `SELECT BOOL_AND(b2) AS v FROM bool_test` 已解析为 LogicalAnd，原有 Generator 生成 `SELECT MIN(b2) AS v FROM bool_test`；两端成功，PG bool / Doris boolean、值 true / 1 一致。这说明主要缺口是 PG Parser 入口，不能仅因归因用过带 CAST 候选就断言 Generator 也必须改。

[PostgreSQL 18 官方说明](https://www.postgresql.org/docs/18/functions-aggregate.html)明确 EVERY 是 BOOL_AND 的标准名称，忽略 NULL，非 COUNT 聚合的空输入返回 NULL。[Doris MIN 官方说明](https://doris.apache.org/docs/4.x/sql-manual/sql-functions/aggregate-functions/min/)说明忽略 NULL 并保留输入类型。BOOLEAN 支持、空输入和实际返回类型另外以本机 4.1.3 的执行/EXPLAIN VERBOSE 为证，不只根据文档推断。

对于 BOOLEAN 非空值，FALSE 小于 TRUE：存在 FALSE 时 MIN 为 FALSE，否则有 TRUE 时为 TRUE；全 NULL/空输入为 NULL，与 EVERY 的契约一致。这里不依赖表 Schema 传给 SQLGlot，也不对固定列或字面量特判。

| 实际文件 / 入口 | 本轮变动 |
| :--- | :--- |
| `sqlglot/parsers/postgres.py`，PostgresParser.FUNCTIONS | 增加 `"EVERY": exp.LogicalAnd.from_arg_list` 一行 |
| `tests/dialects/test_postgres.py`，test_every | 检查 LogicalAnd AST、与 BOOL_AND 规范化一致、类型推断和多方言生成；保留 schema 限定函数及 CUSTOM_EVERY，不扩大到 MySQL Parser |
| `tests/dialects/test_doris.py`，test_boolean_every | 检查 EVERY/其他现有 LogicalAnd 源拼写到 MIN，及 NOT、DISTINCT、空输入、GROUP BY/HAVING、子查询和目标 round-trip |
| `sqlglot/generators/mysql.py`，既有 TRANSFORMS[LogicalAnd] | 复用原 `rename_func("MIN")`，没有修改 |
| Doris Generator、公共 AST、Tokenizer | 本轮均不修改；不新增 CAST、类型注入或框架规则 |

修复后 PG 自身规范化输出为 BOOL_AND，不要求保留 EVERY 原拼写。app.every 仍是限定函数；CUSTOM_EVERY 仍是未知函数；MySQL 源 EVERY 仍不由本次 PG 入口识别。窗口/FILTER 等外部结构可能随函数识别使用已有公共路径，但不因此宣称这些组合通过数据库语义验收。

## 3. 原查询修复前后执行

源原文保持不变：

```sql
SELECT
  EVERY(b1)     AS "f",
  EVERY(b2)     AS "t",
  EVERY(b3)     AS "f",
  EVERY(b4)     AS "n",
  EVERY(NOT b2) AS "f",
  EVERY(NOT b3) AS "t"
FROM bool_test;
```

修复前实际生成：

```sql
SELECT EVERY(b1) AS `f`, EVERY(b2) AS `t`, EVERY(b3) AS `f`, EVERY(b4) AS `n`, EVERY(NOT b2) AS `f`, EVERY(NOT b3) AS `t` FROM bool_test
```

修复后新进程通过 `parse_one(source_sql, read="postgres").sql("doris")` 实际生成并执行：

```sql
SELECT MIN(b1) AS `f`, MIN(b2) AS `t`, MIN(b3) AS `f`, MIN(b4) AS `n`, MIN(NOT b2) AS `f`, MIN(NOT b3) AS `t` FROM bool_test
```

2026-11-23 UTC，双端 `dsv_wf_agg001_s07`；`execute_query` / `compare_probe`，每条限时 10 秒、结果上限 10,000 行。新进程 import 确认来自 `../sqlglot-experiment`。09:48:14 UTC 的标准框架调用如下，退出 0，1 条匹配：

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=../sqlglot-experiment:src \
  ../doris-sql-validator/.venv/bin/python - <<'PY'
from pathlib import Path
from dotenv import load_dotenv
from typer.testing import CliRunner
from doris_sql_validator.cli import app

load_dotenv(Path("../doris-sql-validator/.env"))
result = CliRunner().invoke(app, [
    "run", "--path", "reports/data-preparation/aggregates-001-stage-07-cases.yaml",
    "--id", "pg-aggregates-0149-d636fc82", "--stdout",
])
print(result.stdout)
print("exit", result.exit_code)
PY
```

实际通过上述解释器/环境，在进程中载入既有 .env 并调用 CLI；凭据不写入命令或文件。没有保存新的验证 JSON，未覆盖首轮。

| 比较维度 | 实际结果 |
| :--- | :--- |
| 执行状态 | PG/Doris 均成功，修复前目标函数不存在错误消失 |
| 字段数 / 显式别名 | 六列，按位置为 f、t、f、n、f、t；包括重名列，均一致 |
| 原生类型 / 声明 | 六列 PG bool / Doris boolean，逐列逻辑类型与 BOOLEAN 声明一致；布尔精度/Scale 不适用 |
| 行数 / 行值 | 均 1 行。PG `[false,true,false,null,false,true]`；Doris 协议 `[0,1,0,null,0,1]`，BOOLEAN 类型下按已有规则一致 |
| NULL 与源 .out | 原 .out `["f","t","f","","f","t"]`。实时 PG 实际 NULL 已确认；转换成 psql 的 t/f/空白显示后与 .out 一致，没有把空白直接猜作 NULL |
| 重复次数 / 顺序 | 原查询只有一行；无最终 ORDER BY，结果行按多重集合比较，不声称需要排序 |
| 重跑 | 源、目标各再执行一次，状态/类型/值和行数保持 |
| 完整 Case | 原 .out 匹配且本次实时约定维度通过；没有发现本 Case 的其他未解决差异 |

本轮另只读取得 stage-07 的三行四列 bool_test，双端 BOOLEAN 类型、NULL、完整行值及重复次数一致；数据没有修改。stage-06 原查询 0146 的 BOOL_AND/BOOL_OR 空表控制仍为两个 BOOLEAN NULL，按原 .out 与实时补证均通过。

## 4. 边界与单元测试

### 4.1 TRUE/FALSE/NULL 与空输入：120 条

实际执行的输入生成方式如下；这是报告内的复现说明，不是新增脚本文件。每次目标 SQL 均来自修改后的 SQLGlot，未手写 MIN 候选替代验收：

```python
from itertools import product
from sqlglot import parse_one, ErrorLevel

for n in range(4):
    for seq in product(("TRUE", "FALSE", "NULL"), repeat=n):
        body = " UNION ALL ".join(
            "SELECT CAST(" + v + " AS BOOLEAN) AS x" for v in seq
        ) if seq else "SELECT CAST(NULL AS BOOLEAN) AS x WHERE FALSE"
        for arg in ("x", "NOT x", "DISTINCT x"):
            source = "SELECT EVERY(" + arg + ") AS v FROM (" + body + ") t"
            target = parse_one(source, read="postgres").sql(
                "doris", unsupported_level=ErrorLevel.RAISE
            )
            # 实际通过 execute_query 分别执行源/目标、compare_probe 比较；
            # 再分别执行一次，检查状态、类型、行值及重复稳定性。
```

序列数 `1+3+9+27=40`，每序列三种参数，共 120 条；包含同值重复、输入顺序变化、全 NULL 和真正零行输入。**120 条均成功，字段/别名、BOOLEAN 类型声明、行数、值、重复次数及双端重跑全部通过。** 它们都是单行普通聚合，无最终顺序要求；没有把 120 次当 120 个原 Case。

| 普通 EVERY 输入 | PG 实际结果 | Doris 实际结果 / 类型 |
| :--- | :--- | :--- |
| 空输入 | NULL | NULL / BOOLEAN |
| TRUE | true | 1 / BOOLEAN |
| FALSE | false | 0 / BOOLEAN |
| NULL | NULL | NULL / BOOLEAN |
| TRUE、NULL | true | 1 / BOOLEAN |
| FALSE、NULL | false | 0 / BOOLEAN |
| TRUE、FALSE、NULL | false | 0 / BOOLEAN |

例如实际生成并执行的混合输入完整 SQL：

```sql
-- PostgreSQL 源变体
SELECT EVERY(x) AS v FROM (SELECT CAST(TRUE AS BOOLEAN) AS x UNION ALL SELECT CAST(FALSE AS BOOLEAN) AS x UNION ALL SELECT CAST(NULL AS BOOLEAN) AS x) t
-- SQLGlot 生成的 Doris SQL
SELECT MIN(x) AS v FROM (SELECT CAST(TRUE AS BOOLEAN) AS x UNION ALL SELECT CAST(FALSE AS BOOLEAN) AS x UNION ALL SELECT CAST(NULL AS BOOLEAN) AS x) AS t
```

### 4.2 上下文及 BOOL_AND 控制：18 条

共用常量输入的 `(g,x)` 实际顺序为：`(1,TRUE),(1,TRUE),(1,NULL),(2,FALSE),(2,FALSE),(2,NULL),(3,NULL),(3,NULL),(4,TRUE),(4,FALSE)`。生成方法与原执行一致：

```python
rows = [(1, "TRUE"), (1, "TRUE"), (1, "NULL"),
        (2, "FALSE"), (2, "FALSE"), (2, "NULL"),
        (3, "NULL"), (3, "NULL"), (4, "TRUE"), (4, "FALSE")]
body = " UNION ALL ".join(
    "SELECT CAST(" + str(g) + " AS INT) AS g, CAST(" + v + " AS BOOLEAN) AS x"
    for g, v in rows
)
base = "(" + body + ") t"
```

以下表中的 `base`、`body` 指上述 Python 字符串变量，未作为 SQL 占位符直接提交。将拼接后的完整源 SQL 逐条交给同一个 `parse_one(...).sql("doris")`，再双端执行和重跑。INT CAST 保持分组键类型，不借助字面量 TINYINT 宽度差异制造布尔测试失败。

| 编号 | 实际源构造 / 检查目标 | 实际结果（布尔按逻辑值展示） |
| :--- | :--- | :--- |
| 1–4 | `SELECT EVERY(x) AS v FROM ` + base，分别追加 WHERE x IS TRUE / x IS FALSE / x IS NULL / FALSE | true、false、NULL、NULL |
| 5 | `SELECT g, EVERY(x) AS v FROM ` + base + ` GROUP BY g ORDER BY g` | (1,true)、(2,false)、(3,NULL)、(4,false) |
| 6 | 上条在 ORDER BY 前加 HAVING EVERY(x) | 仅 (1,true) |
| 7 | HAVING NOT EVERY(x) | (2,false)、(4,false) |
| 8 | HAVING EVERY(x) IS NULL | 仅 (3,NULL) |
| 9 | 编号 5 改为 EVERY(DISTINCT x) | 与编号 5 相同 |
| 10 | `SELECT EVERY(CASE WHEN g = 3 THEN TRUE ELSE x END) AS v FROM ` + base | false |
| 11 | `SELECT EVERY(x IS NULL) AS v FROM ` + base | false |
| 12 | `SELECT NOT EVERY(x) AS v FROM ` + base | true |
| 13 | `SELECT COALESCE(EVERY(x), FALSE) AS v FROM ` + base + ` WHERE FALSE` | false |
| 14 | `SELECT (SELECT EVERY(x) FROM ` + base + `) AS v` | false |
| 15 | `WITH t AS (` + body + `) SELECT g, EVERY(x) AS v FROM t GROUP BY g ORDER BY g DESC` | (4,false)、(3,NULL)、(2,false)、(1,true) |
| 16 | `SELECT EVERY(x) AS v FROM ` + base + ` UNION ALL SELECT EVERY(x) AS v FROM ` + base | 两条 false，重复次数保留 |
| 17–18 | `SELECT BOOL_AND(x) AS v FROM ` + base，分别不加 WHERE / 加 WHERE FALSE | false、NULL |

**18 条全部双端成功，行数、行值/重复次数及类型声明一致，双端重跑稳定。** 5–9、15 的最终排序按唯一 GROUP BY 键 g，源目标实际顺序一致，键唯一性来自构造而非工具推定。其余无最终 ORDER BY，不比较任意返回顺序。

编号 16 的集合查询别名工具自动标为“尚未检查”，本轮另读同一完整变体的字段：两端均单列 `v`、PG bool / Doris boolean、两条 false；补齐列名证据，不把工具未检查写成通过。另一个两行布尔 UNION ALL 小控制也得到相同观察。

### 4.3 单元测试结果

先加 `test_every` 和 `test_boolean_every`，Parser 修改前两个方法共 10 个失败断言；修复后两个方法通过。修复期间发现两条测试期望需要沿用 MySQL SIGNED 和 BigQuery BOOL 的现有类型拼写，已修正测试，没有改这两个 Generator。

| 实际运行 | 通过方法数 | 说明 |
| :--- | ---: | :--- |
| 定向新测试 | 2 | AST 归一化、类型、目标 SQL、多方言读写及 round-trip |
| PostgreSQL / Doris / MySQL | 147 | 含新测试和前轮测试 |
| 全部 dialect | 1,070 | 包含上述 147，不相加 |
| parser/generator/transpile/expressions/serde/build/schema/tokens | 233 | 核心 AST 与序列化等回归 |
| Ruff check、format --check 六个累积文件；git diff --check | 通过 | 没有格式化无关文件 |

完整命令和未运行范围见本轮汇总。BigQuery/Spark/Snowflake 的用例是现有 LogicalAnd 节点的解析/生成回归，没有把这些数据库的执行验证算在 138 条 PG/Doris 对照内。

## 5. 验收、剩余范围与下一步

本任务的 BOOLEAN、NOT、全 NULL、空输入、DISTINCT、字段声明与已测上下文均有实际证据，原 Case 不再发生 EVERY 函数缺失。没有新增 SQLGlot 回归；不需增加 Generator 特判。

全量相关回归 92 条为 72 匹配、9 目标执行失败、7 行值/顺序差异、4 源端负向。此前 71 条匹配保持；剩余差异沿用前轮数组、类型/精度和相关聚合研究，不是本次 EVERY 改写新增。首轮 JSON、历史统计、输入 SQL/.out、YAML 和比较器均未修改。

边界是有限实测，不证明所有函数参数、数据库版本、窗口、FILTER、内部排序或全部可能 PostgreSQL 查询等价；非法源调用默认不为复制其报错进入本任务。当前完成的是 task-006，不是整份输入。

下一建议 task-007：小样本统计聚合的 NULL 行为；需先复现再实施，本轮没有开始。task-001/003 未验收余项和归因汇总中的研究/前提阻断仍保留。本轮代码未 commit/push，也不代表社区认可或已合并。
