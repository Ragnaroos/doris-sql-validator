# aggregates-001 / fix-007：样本统计聚合的小样本 NULL 规则

## 1. 本轮结论与范围

指定任务模式，仅处理 [task-007](../attribution/aggregates-001-attribution-summary.md#task-007)。**已修复并完成有限浮点输入的小样本 NULL 规则验收；整份输入未完成。** 本轮没有 commit/push、Issue/PR、验证框架修改、装数或 Session 政策变更。

修复 PostgreSQL STDDEV、STDDEV_SAMP、VARIANCE、VAR_SAMP 和 COVAR_SAMP 转到 Doris 时的行为：有效样本不足两条返回 NULL；正常多样本继续使用原样本统计函数，不替换成总体统计。协方差只统计两列都非 NULL 的配对。

| 检查范围 | 实际结论 |
| :--- | :--- |
| 7 条关联原查询 | 样本聚合列从错误的 0 变为正确 NULL；5 条实时结果及 FLOAT64 声明一致，2 条 NUMERIC/DOUBLE 类型差异仍保留 |
| 原 .out 整条比较 | **0 匹配、7 行值或顺序不匹配**；共同余项为总体聚合列显示 `0` / `0.0`，不是 NULL 修复未生效。不改比较器或源答案制造 MATCH |
| 212 条基础/配对边界 | 全部双端成功，FLOAT64 类型声明一致、重跑稳定；其中 108 条小样本全部 NULL 一致。184 条值精确一致，28 条浮点尾差均有原生 Doris 控制，未加补偿时同样存在 |
| 13 条上下文边界 | 分组、HAVING、CTE、子查询、LEFT JOIN、重复结果和空组；11 条完整比较一致，2 条仅正常多样本的标准差尾差保留。组键顺序相同，不误称排序缺陷 |
| 99 条原查询回归 | 16 阶段：72 匹配、9 Doris 执行失败、14 行值/顺序不匹配、4 源端负向；此前 72 条匹配全部保持 |
| SQLGlot 单元测试 | 150 个 PG/Doris/MySQL 方法、1,073 个全部方言方法、233 个核心方法通过；前两组有包含关系，不相加 |

任务验收只关闭小样本 NULL 补偿，不关闭浮点尾差、NUMERIC 返回类型、NaN/Infinity、窗口或 FILTER 语义。完整实现和证据见[任务报告](tasks/aggregates-001/fix-007/task-007.md)。

## 2. 版本、输入与环境

| 项目 | 实际值 |
| :--- | :--- |
| SQLGlot checkout / 分支 | `../sqlglot-experiment` / `codex/doris-array-literal` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`，未切换/刷新基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；未提交/推送 |
| 起始累积 diff SHA256 | `497368feb37bbf075a81b602ab2870c8a870bc172695a15d0fc5fd2b0c5d8208` |
| 最终累积 diff SHA256 | `073be5b32f6e6208a2a92cd72d980003879511b1d3097fd254356b34ecc04792`，按 git diff --binary；包含保留的 task-001 至 task-006 修改，不是混合提交计划 |
| 本轮代码/测试归属 | aggregate.py、parsers/postgres.py、generators/doris.py、test_postgres.py、test_doris.py；相对前轮新增 166 行、删除 3 行，parsers/doris.py 未变 |
| 实际验证 import | `../doris-sql-validator/.venv/bin/python`，PYTHONPATH=`../sqlglot-experiment:src`；新进程确认 `../sqlglot-experiment/sqlglot/__init__.py`，版本 `30.25.1.dev355` |
| PostgreSQL | 本轮实查 18.1，127.0.0.1:5432，UTC、extra_float_digits=0；原 Session 保持 |
| Doris | 本轮 SHOW FRONTENDS 实查 `doris-4.1.3-rc02-7126cf65d96`，Alive=true；127.0.0.1:9030，UTC、enable_strict_cast=false。协议 VERSION() 的 5.7.99 不作为产品版本 |
| 主任务阶段 | 双端 `dsv_wf_agg001_s01`，原七条均为常量统计查询，不新增或改动数据 |

遵循目标 AGENTS.md、CONTRIBUTING.md、pg-doris-fix、工作流及修复模板。未调用其他 Skill/Agent。前六轮代码、工作流已有文档/Skill 修改和原社区 checkout 保留；凭据只从既有 .env 载入进程。

| 不变输入 | 路径 / SHA256 |
| :--- | :--- |
| [stage-01 YAML](../data-preparation/aggregates-001-stage-01-cases.yaml) | `cf04cd870b828d26d1d0846d0b5a5be0f38bc25c7c76d100e138f5b9de31d423` |
| [stage-01 首轮 JSON](../validation/aggregates-001-stage-01-validation.json) | `312e26743e1b476ee11278b66aed299ecd347aa741a193864dc5aa83048fe0b0` |
| 原 aggregates.sql | `../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql`，`9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62` |
| 原 .out | 同目录 aggregates.out，仍按原 SQL/出现序号定位；不保存或核验 .out 指纹 |
| 准备材料 | [准备说明](../data-preparation/aggregates-001-data-preparation.md)及同前缀双端 setup.sql。历史完整基表核验不声称本轮重新执行 |

## 3. 实现与独立任务边界

PG Parser 为四种公共 AST 节点记录 `null_on_insufficient_samples=True`，意为“少于两条有效样本时必须返回 NULL”；Doris Generator 只对带此标记的普通聚合补偿。不全局改变 Doris 自身的统计 SQL，也不推断其他方言的 Session 契约。

```sql
-- 一元样本统计
IF(COUNT(x) < 2, NULL, STDDEV_SAMP(x))
IF(COUNT(x) < 2, NULL, VAR_SAMP(x))
-- 二元样本协方差：x 为 NULL 时舍弃该行，y 为 NULL 时 COUNT 同样不计
IF(COUNT(IF(x IS NULL, NULL, y)) < 2, NULL, COVAR_SAMP(x, y))
```

DISTINCT 一元统计使用 COUNT(DISTINCT x)，不拿重复行凑两条有效样本。窗口、FILTER、WITHIN GROUP、内部 ORDER BY 不套用普通聚合规则；Oracle 已有单样本方差规则继续由既有 variance_sql 处理。没有 Schema 注入或字面量 NULL 特判。

| task | 本轮互斥状态 | 提交与依赖 |
| :--- | :--- | :--- |
| [task-007](tasks/aggregates-001/fix-007/task-007.md) | 已修复并完成约定的小样本 NULL 规则验收 | 独立行为与对应测试；无必须依赖其他 task，未提交、未推送 |

## 4. 测试与剩余差异

先新增三个测试方法，补实现前 20 个失败断言。实现过程中一次使用不存在的 Count.lt API 导致定向测试失败，已改为 exp.LT；最终通过，失败尝试不冒称成功。

| 实际命令，工作目录 ../sqlglot-experiment | 结果 |
| :--- | :--- |
| `.venv/bin/python -m unittest tests.dialects.test_postgres.TestPostgres.test_sample_aggregate_null_contract tests.dialects.test_doris.TestDoris.test_sample_aggregate_nulls tests.dialects.test_doris.TestDoris.test_sample_aggregate_exclusions` | 3 个新方法通过 |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql` | 150 个方法通过 |
| 同解释器/PATH：`python -m unittest discover -s tests/dialects` | 1,073 个方法通过；末轮已含 AST 序列化与 copy=False 不污染输入检查 |
| 同解释器/PATH：`python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens` | 233 个方法通过 |
| Ruff check、format --check 六个累积文件；git diff --check | 通过 |

没有执行完整 make check、C 扩展、mypy 或依赖 duckdb 的 executor/optimizer 全套，没有安装或升级依赖。其他方言只做解析/生成回归，不声称连接这些数据库执行。

原七条通过 `run --path <stage-01 YAML> --stdout --id ...` 同批运行；补证通过实际新生成 SQL、execute_query/compare_probe 完成，源目标各重跑。全部七条当前 PG 的文本 `[["0",""]]` 与原 .out 相同。边界另用 PG binary cursor 避免 extra_float_digits=0 的文本舍入；它补充证据，不替换原 .out 或改变框架算法。

最终相关回归为 fix-006 的 92 条加本任务 7 条，同一进程按原阶段调用 CLI，不保存新 JSON。阶段数：01:28、03:6、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:9、25:6、30:3、31:17、32:1、42:3、43:4，共 99；此前 72 个匹配的 Case ID 全部保持。

| 余项 | 结论与去向 |
| :--- | :--- |
| 七条原查询的 `0` / `0.0` | 原 .out 是显示文本，框架仍判不同；实时五条 FLOAT64 结果/类型一致。不为这项显示差异改 SQLGlot 为字符串输出 |
| 0041/0042 NUMERIC / DOUBLE | 真实返回类型差异，保留类型契约研究；COUNT 不会恢复任意精度 NUMERIC |
| 28 条基础及 2 条上下文的尾差 | 新旧 Doris 原生结果对正常多样本的尾差相同；复用已有浮点/表示研究，不当作新 COUNT 规则引入，也不自动放宽比较。尚未区分底层计算与传输/格式化的全部影响 |
| NaN/Infinity 排除范围控制 | 另查 14 条原查询：10 条目标样本列从 0 变 NULL，4 条目标结果不变。不是“非有限数保持原输出”，也不宣称正确；这些仍需独立研究，不计本任务通过或新增 MATCH |
| 原数组、整数除法及相关聚合问题 | 保留 fix-003/004/005 的去向，不因本任务验收而关闭 |

## 5. 当前任务清单与下一步

全批 9 项当前为：**5 项完成约定验收（002/004/005/006/007）、2 项已修改未验收（001/003）、2 项未处理（008/009）**。本轮没有新增或重新打开其他 task；前提、浮点、类型和非有限数研究继续保留在[统一归因汇总](../attribution/aggregates-001-attribution-summary.md)。

**所选 task-007 的有限输入小样本 NULL 规则完成；整份输入未完成。** 未全量重跑 313 条/43 阶段及两条导入遗漏；仍有未处理、未验收与前提/研究事项。

建议下一项 **task-008：FROM 位置的常量整数 GENERATE_SERIES**，先核对当前 Parser/Generator 与输出列/边界证据，再实施独立修复；本轮未开始。代码当前只保存在本地实验 checkout，未提交到 fork。
