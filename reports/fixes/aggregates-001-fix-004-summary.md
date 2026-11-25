# aggregates-001 / fix-004：ARRAY_AGG 按聚合值自身排序

## 1. 本轮结论

指定任务模式，仅处理 [task-004](../attribution/aggregates-001-attribution-summary.md#task-004)。**已修复并完成本次约定的整数自值排序验收；整份输入未完成。** 没有 commit、push、Issue 或 PR，没有修改验证框架、原 SQL/.out、数据阶段或比较规则。

| 本轮观察 | 数量 | 含义 |
| :--- | ---: | :--- |
| 本轮修复任务 | 1 | task-004，不是 5 个 Case 各算一个任务 |
| 关联原查询 | 5 | 都从修改后的 SQLGlot 重新生成 SQL；Doris 由执行失败变为成功 |
| 原查询实时结构化数组一致 | 5 | 元素值、内部顺序、NULL 位置及重复次数一致；不是完整 Case MATCH |
| 固定边界 | 68 | 成功状态、字段数、显式别名、行数/值/重复次数及必要顺序均一致；INT/BIGINT 元素声明逐项核对；每侧再执行一次均稳定 |
| 原查询 CLI 回归 | 75 | 16 个实际数据阶段，65 匹配、4 Doris 执行失败、6 行值或顺序不匹配 |
| 此前匹配查询的回归 | 65 | 首轮 62 条加 fix-002 新匹配 3 条，全部保持匹配 |

5 条关联查询仍没有完整 MATCH：原 .out 用 `{1,2,...}` 表示数组，Doris 用 `[1, 2, ...]`；实时类型也仍是 PG `int4[]` / Doris `array<tinyint>`。未修改比较器或强制 CAST 来消除这些独立差异。详细 SQL、执行事实和验收边界见[任务报告](tasks/aggregates-001/fix-004/task-004.md)。

全批 9 项当前为：2 项已完成约定验收（task-002/004），2 项已修改未完成验收（task-001/003），5 项未处理（task-005 至 task-009）。task-003 的 NULL/空输入实现已被复用，但本轮没有把其类型/精度余项宣告完成。

## 2. 代码与运行环境

| 项目 | 实际值 |
| :--- | :--- |
| 修改 checkout / 分支 | `../sqlglot-experiment` / `codex/doris-array-literal` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`，本轮未切基线或提交 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；本轮未 fetch 或推送 |
| 起始累积 diff SHA256 | `2de3541799b6c32ded8670f98121fb35a13a3df7d80c413e92ff9827c2d3d46f` |
| 最终累积 diff SHA256 | `0cb0ae94b56c917d9cd001996ea998a76c307589351385e829aea1397e3aef02`，`git diff --binary`；包含保留的 task-001/002/003，不是本任务独立 patch |
| 本轮实际代码变化 | Doris Generator 和 Doris 方言测试；未改公共 AST、PG Parser 或 Doris Parser 的既有修改 |
| 验证器解释器 | `../doris-sql-validator/.venv/bin/python`；`PYTHONPATH=../sqlglot-experiment:src`，工作目录为本工作流根目录 |
| 实际 import | `../sqlglot-experiment/sqlglot/__init__.py` |
| 包版本 | `30.25.1.dev355`；以 HEAD、diff、import 路径共同识别，不能只按版本号判断 |
| PostgreSQL | 18.1；127.0.0.1:5432；UTC、DateStyle=ISO, MDY、extra_float_digits=0 |
| Doris | `doris-4.1.3-rc02-7126cf65d96`，SHOW FRONTENDS 实查 Alive=true；127.0.0.1:9030；UTC、enable_strict_cast=false、enable_decimal256=false |
| 原查询/边界数据库 | 双端 `dsv_wf_agg001_s17`；其他回归使用各自 YAML 的阶段库 |

适用指令为 SQLGlot checkout 的 AGENTS.md、CONTRIBUTING.md，以及项目 pg-doris-fix Skill、工作流与修复报告模板。原有 6 个 SQLGlot 修改文件和工作流的既有文档/Skill 改动均保留；没有触碰 `../sqlglot` 的社区 checkout。无凭据进入报告。

输入为原 `aggregates.sql` / `aggregates.out`，位置见[准备报告](../data-preparation/aggregates-001-data-preparation.md)。关联 [stage-17 YAML](../data-preparation/aggregates-001-stage-17-cases.yaml) 和[首轮 JSON](../validation/aggregates-001-stage-17-validation.json) 保持原件，SHA256 分别为 `c4452ebf80f01193510ef591c849dd551e05d2a42d48bb05fac5de0f6825abd2`、`a35f570ffe0e0f7779f27a82d9973e90966e80f3dafc78f86b3db99fd29ad389`；源 SQL 为 `9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62`。不保存 .out 指纹。

## 3. 实施与验收导航

| 任务 | 状态 | 实现依赖与保存状态 | 任务报告 |
| :--- | :--- | :--- | :--- |
| task-004：ARRAY_AGG 按聚合值自身排序 | 已修复并完成约定验收，仅限本报告实测整数规则 | 复用 task-003 的 NULL/空输入基础；未提交、未推送；未来与 task-003 分开保存行为修复 | [task-004.md](tasks/aggregates-001/fix-004/task-004.md) |

本轮尝试过 lambda 分区方案，实际发现 HAVING 拒绝 lambda；改为 ARRAY_SLICE 截取 NULL 前缀。中途还发现继承的 ARRAY_LENGTH 名称不能在 Doris 执行，最终以 ARRAY_SIZE_NAME 映射到 ARRAY_SIZE。失败事实和最终重测都保存在同一任务报告，没有生成额外执行文件。

## 4. 实际回归

单位测试在 `../sqlglot-experiment`，使用该目录 `.venv/bin/python`，PATH 包含同目录 `.venv/bin`：

| 实际命令 | 结果 |
| :--- | :--- |
| `python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.dialects.test_mysql` | 143 个方法通过，包含本轮 3 个新方法 |
| `python -m unittest discover -s tests/dialects -t .` | 1,066 个方法通过；上面 143 个已包含在内，不重复相加 |
| `python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens` | 233 个方法通过 |
| `.venv/bin/ruff check <6 个累积修改文件>` / `ruff format --check <同文件>` / `git diff --check` | 均通过 |

本轮没有运行完整 make check、C 扩展测试、mypy 或依赖 duckdb 的 executor/optimizer 全套；没有安装/升级依赖。以上测试范围不是全仓验收声明。

数据库最终边界执行：2026-11-23 09:23:02–09:23:09 UTC；最终原查询回归与补证：09:23:47–09:23:50 UTC。每个实际 stage 一次 CliRunner 调用 `run --path <对应 YAML> --stdout --id ...`，未保存新的 JSON。回归阶段和数量：01:21、03:6、06:1、07:5、08:1、09:8、10:2、11:1、15:3、17:9、25:6、30:3、31:1、32:1、42:3、43:4，合计 75。

| 剩余观察 | 去向 |
| :--- | :--- |
| 0284/0285/0288/0289/0290 的原 .out 数组文本不同及实际元素位宽不同 | 表示/类型契约研究，不再重复判定为本轮排序未生效；不把完整 Case 改成 MATCH |
| 0287 未指定排序的 DISTINCT 数组 | 沿用 task-003 报告的表示、类型和未指定内部顺序限制 |
| 0276 的 GENERATE_SERIES 仍语法失败 | 复用 task-008，不顺带修序列 |
| 0283/0286 按另一个值排序仍失败 | 沿用不同排序键研究，不能套用自值排序规则 |
| 0371 整行引用/ARRAY_DIMS 仍失败 | 沿用复合类型与维度研究 |

## 5. 整份输入状态与下一步

**整份输入未完成。** 本轮仅复查选定任务及 75 条相关原查询，没有重新运行全部 313 条、43 个阶段、导入遗漏或其他研究项。task-001/003 尚有类型/精度验收余项，task-005 至 task-009 未实施，故不满足整份输入完成条件。

建议下一项为 **task-005：普通忽略 NULL 聚合的 FILTER 转换**：已有独立范围、8 条关联证据和高优先级，不必混入数组排序提交。它尚未执行；继续修复须由人授权。task-001/003 的类型补证仍保留，不因安排下一独立任务而关闭。当前代码起点和本轮入口见本报告第 2/3 节，当前统一任务清单仍在原归因汇总。
