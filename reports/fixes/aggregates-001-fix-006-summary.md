# aggregates-001 / fix-006：识别 PostgreSQL EVERY 布尔聚合

## 1. 本轮结论与范围

指定任务模式，仅处理 [task-006](../attribution/aggregates-001-attribution-summary.md#task-006)。**已修复并完成普通 BOOLEAN 聚合的约定验收；整份输入未完成。** 未 commit/push、创建 Issue/PR、修改验证框架、装数或改变 Session 政策。

本轮只在 PostgreSQL Parser 增加 `EVERY → exp.LogicalAnd`。Doris 原有 `LogicalAnd → MIN` 已能正确处理 BOOLEAN、NULL 和空输入，实测返回 BOOLEAN，因而不新增 Generator 规则或多余 CAST。此前归因中的 `CAST(MIN(...) AS BOOLEAN)` 是可行候选，不是必须照搬的补丁。

| 验证范围 | 实际结果 |
| :--- | :--- |
| 关联原查询 `pg-aggregates-0149-d636fc82`，stage-07 | 从 Doris 找不到 EVERY 函数变为原 .out 匹配；实时 PG 补证：六列别名、BOOLEAN 类型、NULL、行值和重复执行均一致 |
| 120 条基础边界 | TRUE/FALSE/NULL 的长度 0–3 输入序列，共 40 种；分别验证普通参数、NOT、DISTINCT。全部双端成功，类型/行值/重复次数及双端重跑一致 |
| 18 条上下文与 BOOL_AND 控制 | WHERE、分组、HAVING、CASE、COALESCE、子查询、CTE、重复结果、现有 BOOL_AND 均通过；分组按唯一组键排序。集合查询别名另行实查，不冒充工具已自动检查 |
| 92 条原查询回归 | 16 个实际阶段：72 匹配、9 Doris 执行失败、7 行值或顺序不匹配、4 源端负向。此前 71 条匹配全部保持 |
| SQLGlot 测试 | 147 个 PG/Doris/MySQL 方法、1,070 个全部方言方法、233 个相关核心方法通过；前两组重叠，不相加 |

实现、完整原 SQL/生成 SQL、边界生成方法、具体结果与限制见[任务报告](tasks/aggregates-001/fix-006/task-006.md)。不将单个任务完成称为全部 PostgreSQL 查询同义。

## 2. 共同版本与输入

| 项目 | 实际值 |
| :--- | :--- |
| checkout / 分支 | `../sqlglot-experiment` / `codex/doris-array-literal` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`；本轮不刷新基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；本轮未提交或推送 |
| 起始累积 diff SHA256 | `8a6e18fbf1630778b6af86afaa03cdbbbfba17833bcd65ff40eabeb13f64e152` |
| 最终累积 diff SHA256 | `497368feb37bbf075a81b602ab2870c8a870bc172695a15d0fc5fd2b0c5d8208`，按 `git diff --binary`；包含 task-001 至 task-005 的既有修改，不是混合提交计划 |
| 本轮新增修改 | `sqlglot/parsers/postgres.py`、`tests/dialects/test_postgres.py`、`tests/dialects/test_doris.py`，共新增 56 行；其他既有修改保留 |
| 验证解释器 | `../doris-sql-validator/.venv/bin/python`，`PYTHONPATH=../sqlglot-experiment:src`；新进程确认 import 为 `../sqlglot-experiment/sqlglot/__init__.py`，版本 `30.25.1.dev355` |
| PostgreSQL | 18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | `SHOW FRONTENDS` 实查 `doris-4.1.3-rc02-7126cf65d96`，Alive=true；127.0.0.1:9030；UTC、enable_strict_cast=false。`VERSION()` 的 5.7.99 仅是协议兼容值 |
| 主查询/边界库 | 双端 `dsv_wf_agg001_s07`；空表 BOOL_AND 控制使用 `dsv_wf_agg001_s06`；其他查询使用各自 YAML 阶段库 |

遵循目标 AGENTS.md、CONTRIBUTING.md、项目 pg-doris-fix Skill、工作流和修复模板；未调用其他 Skill/Agent。工作流已有文档/Skill 修改、前五轮 SQLGlot 修改、原社区 checkout 均保留。凭据只从既有 .env 载入进程。

| 不变输入 | 路径 / SHA256 |
| :--- | :--- |
| 本任务 YAML | [stage-07](../data-preparation/aggregates-001-stage-07-cases.yaml)：`cb156ed0d2afe77870646f54dd1efc8c9bc94dfa94c7dfaaa41d3bc6f7a32f2b` |
| 首轮 JSON | [stage-07](../validation/aggregates-001-stage-07-validation.json)：`a9692c4285fe7d03e7f5e416b3fb899e312e26b9806bfaa202d81495b9f96250` |
| 原 SQL | `../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql`：`9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62` |
| 原 .out | 与 SQL 同目录的 `aggregates.out`；成功读取原回显和出现序号，不保存或核验 .out 指纹 |
| 准备材料 | [准备说明](../data-preparation/aggregates-001-data-preparation.md)及同前缀双端 setup.sql；stage-07 为三行四列 BOOLEAN，stage-06 为空表 |

本轮只读核对 stage-07 的全部三行 bool_test：四列类型、NULL、行值和重复次数一致。没有重做全部历史基表核验。

## 3. 修改与测试

| task | 本轮状态 | 独立提交边界 |
| :--- | :--- | :--- |
| [task-006](tasks/aggregates-001/fix-006/task-006.md) | 已修复并完成约定验收 | PostgreSQL EVERY 函数识别及相关测试；无其他 task 的必须实现依赖。未提交、未推送 |

先新增两个测试方法，修改 Parser 前实际产生 10 个失败断言；增加单行函数映射后通过。之后更正两条测试期望中的已有 MySQL/BQ 类型拼写（SIGNED/BOOL），未改变实现或其他方言生成逻辑。

| SQLGlot checkout 内实际命令 | 结果 |
| :--- | :--- |
| `.venv/bin/python -m unittest tests.dialects.test_postgres.TestPostgres.test_every tests.dialects.test_doris.TestDoris.test_boolean_every` | 修复后 2 个方法通过 |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql` | 147 个方法通过 |
| 同一解释器/PATH：`python -m unittest discover -s tests/dialects` | 1,070 个方法通过 |
| 同一解释器/PATH：`python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens` | 233 个方法通过 |
| `.venv/bin/ruff check` / `ruff format --check` 六个累积修改文件；`git diff --check` | 通过 |

未执行完整 make check、C 扩展、mypy、依赖 duckdb 的 executor/optimizer 全套；未安装/升级依赖。其他源方言只有解析/生成单测，不声称已连接它们的数据库执行。

## 4. 原查询回归与剩余问题

2026-11-23 UTC，本轮新进程通过 `parse_one(..., read="postgres").sql("doris")` 实际生成，`execute_query` / `compare_probe` 补查实时类型与结果。原查询第一次修复后 `run --stdout` 时间为 09:48:14 UTC。每次只读查询限时 10 秒，最多完整采集 10,000 行；本任务原查询和边界均未超过上限。

最终回归在一个 Python 进程按阶段调用 `CliRunner().invoke(app, ["run", "--path", 原阶段YAML, "--stdout", "--id", ...])`，不保存新 JSON。范围是 fix-005 的 91 条加本任务 1 条。阶段数量：01:21、03:6、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:9、25:6、30:3、31:17、32:1、42:3、43:4，共 92 条。

| 当前结果 | 数量 | 与本任务关系 |
| :--- | ---: | :--- |
| 匹配 | 72 | 此前 71 条保持，0149 新增匹配；.out 缺原生类型，不能据此称这 72 条全部类型一致 |
| Doris 执行失败 | 9 | 保留前轮数组、不同排序键/整行引用及相关聚合研究；未因 EVERY 修复而新增 |
| 行值或顺序不匹配 | 7 | 保留前轮数组显示/类型及 0381 整数除法等差异，未改比较器或源答案 |
| 源端负向 | 4 | 0394–0397，仍默认不归因、不进入修复清单 |

本轮没有新暴露的 SQLGlot 回归，也没有新增 task。关联 Case 0149 已按实际维度验收；其他类型/浮点/相关查询、task-001/003 的余项不因本任务完成而关闭。

## 5. 当前清单与下一步

全批 9 个稳定 task 当前为：**4 项完成约定验收（002/004/005/006）、2 项已修改未完成验收（001/003）、3 项未处理（007/008/009）**。统一索引仍在[归因汇总](../attribution/aggregates-001-attribution-summary.md)，0149 的后续证据追加到原 Case 文档。

**所选 task-006 完成；整份输入未完成。** 没有重跑全部 313 条/43 阶段或两条已知导入遗漏；仍有未处理、未验收及前提/研究事项，不能宣布全批完成。

建议下一独立任务为 **task-007：小样本统计聚合的 NULL 行为**，先复现当前版本与 Doris 的实际表现，再确定安全改写。下一任务未在本轮实施；需要人明确选择。当前代码仅保存在本地实验 checkout，没有提交到 fork。
