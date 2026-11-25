# aggregates-001 / fix-002：Doris 原生 NULL 排序修复

## 1. 本轮结论与范围

**task-002 已修复并完成本次约定的排序验收，整份输入未完成。** 本次为指定任务模式，仅修改 Doris 的原生 NULL 排序能力及相关测试，没有开始修复其他 task，没有 commit、push 或创建 Issue/PR。

修复前，PostgreSQL 的 `ORDER BY 1` 在严格转译时可能报 `'NULLS LAST' translation not supported with positional ordering`。修复后直接生成 Doris 支持的 `ORDER BY 1 NULLS LAST`；别名排序也不再展开为额外的 CASE 排序键。

| 本轮互斥任务状态 | 数量 |
| :--- | ---: |
| 已修复并完成约定验收 | 1 |
| 已修改但未完成验收 | 0 |
| 重新打开 | 0 |
| 当前阻断 | 0 |
| 未处理 | 0 |
| 不需修改 | 0 |

本轮复用已有 task-002，没有新增或重新打开 task。全批现有 9 个 task：task-001 仍为已修改但未完成验收，task-002 完成本次排序验收，task-003–009 尚未实施。

## 2. 实际代码和环境

| 项目 | 本轮实际值 |
| :--- | :--- |
| checkout / 分支 | [sqlglot-experiment](../../../sqlglot-experiment/)；`codex/doris-array-literal`，沿用已有实验分支 |
| origin / upstream | `https://github.com/Ragnaroos/sqlglot.git` / `https://github.com/tobymao/sqlglot.git` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`；本轮没有 fetch、切换基线或提交 |
| 与 fix-001 的关系 | fix-001 报告记录的 HEAD 是 b812ff95；本轮开始时 checkout 已是上述 089891f。先在实际当前代码复现，不把两轮当成同一基线 |
| 原有修改 | task-001 的 3 个文件、88 行增加/1 行删除，完整保留；起始 diff SHA-256 为 `a09017a32b5c305aea4cca6f27d6361d30505e962db44bc1c37841830ba2a819` |
| 本轮改动 | Doris Generator 增加 `NULL_ORDERING_SUPPORTED = True`；test_doris.py 增加排序测试并更新 4 条 LAG/LEAD 的 PostgreSQL 转译预期；未修改 Parser 或验证框架 |
| 最终累计 diff | 相对 HEAD 为 3 文件、155 行增加/9 行删除，包含原 task-001；本轮净增量为 67 行增加/8 行删除 |
| 最终 diff SHA-256 | `4be19b72e29259a100f7fbc73ac30706f0a7e9b53ac52ff1d1d581b0fb335f35`，计算命令为 `git diff --binary` 后 SHA-256 |
| 实际运行身份 | Python 3.12.15；`sqlglot.__file__` 为 `../sqlglot-experiment/sqlglot/__init__.py`；版本字符串 `30.25.1.dev355`。以模块路径、HEAD 和 diff 共同识别代码，不仅凭版本字符串 |
| 数据库 | PostgreSQL 18.1；Doris `doris-4.1.3-rc02-7126cf65d96`，本轮 `SHOW FRONTENDS` 实测；127.0.0.1:5432 / 9030 |
| 输入与数据 | 原 SQL/.out、阶段 YAML 和首轮 JSON 均不改写；6 条原查询使用 stage-03/09/42 的同名双端阶段库；既有匹配回归按各自原阶段执行 |
| Session 与保护 | 补证工具设置 UTC、PG ISO/MDY，实测 extra_float_digits=0、Doris enable_strict_cast=false；补证每条 10 秒、上限 10000 行，未使用截断结果 |
| 凭据 | 在进程中加载既有 `../doris-sql-validator/.env`，不复制或展示密码；没有建表装数或修改数据 |

SQLGlot 代码按目标仓库 AGENTS.md / CONTRIBUTING.md 检查。本轮没有改原 `../sqlglot` 或其他实验 checkout。SQLGlot 原有未提交修改和工作流既有文档修改均未覆盖。

## 3. 任务和完整查询结果

| 任务 | 本轮验收 | 完整查询结果 | 详细报告 | 保存状态 |
| :--- | :--- | :--- | :--- | :--- |
| [task-002](../attribution/aggregates-001-attribution-summary.md#task-002)：Doris 原生 NULL 排序 | 排序规则及必要回归通过 | 6 条均完成转译；按原 .out 为 3 条匹配、3 条 Doris 执行失败 | [task-002.md](tasks/aggregates-001/fix-002/task-002.md) | 本地未提交、未推送；排序与数组是独立修改范围，不能按本轮混为一个 commit |

匹配的是 Case 0173、0551、0552。0134 仍涉及 GENERATE_SERIES/LATERAL，0179 仍缺少投影位置的 GENERATE_SERIES 转换，0137 仍涉及分组相关子查询。排序修复没有把这些问题一起解决。

**3 条匹配也不等于所有类型一致**：0551/0552 的实时 PG `text` / Doris `varchar(65533)`、PG CASE `int4` / Doris `tinyint` 仍不同；count 的 int8/bigint 一致。排序和行值通过，其他类型问题单列保留。

另有一项必须先核对的源证据：0137 的原 .out 记录成功，但本轮本机 PG 18.1 报 `42803: subquery uses ungrouped column "t1.two" from outer query`。不替换原 .out，也不将它改记为源端负向或两端成功匹配；先确认源输出对应的 PostgreSQL 版本/行为，不能据此认定相关子查询转换已经验收。

## 4. 实际验证

| 范围 / 命令 | 结果及限制 |
| :--- | :--- |
| 新增 test_null_ordering 在修改能力标志前运行 | 失败：28 个断言失败、5 个子测试错误，确认测试能检出缺口；不是 33 条独立业务查询 |
| `.venv/bin/python -m unittest tests.dialects.test_doris tests.dialects.test_mysql tests.dialects.test_postgres` | 137 个测试通过；首次加标志时 4 个旧 LAG/LEAD 预期未保留 PG 默认 NULL 方向，更新预期并保留原生 Doris identity 检查后通过 |
| `PATH="$PWD/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest discover -s tests/dialects -t .` | 1060 个测试通过，包含上述定向测试，数字不累加；首次未设 PATH 时 lazy-load 测试找不到 python，调整执行环境后重跑通过 |
| `PATH="$PWD/.venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions` | 199 个核心测试通过 |
| Ruff check、Ruff format --check、git diff --check | 通过；检查 3 个累计改动文件，不修改无关代码 |
| 6 条关联原查询，3 个 stage，实际 CLI `run --stdout --id ...` | 3 匹配、3 Doris 执行失败、0 转译失败；与首轮/前轮事实分开保存，不覆盖 JSON |
| 同 6 条实时 PG/Doris 补证 | 3 条双端成功，字段数、值/重复次数和顺序一致，声明差异保留；3 条目标失败，不伪造类型/值通过。其中 1 条 PG 当前状态与 .out 冲突 |
| 19 组固定边界及各增加一次双端执行 | 两端成功，行值/重复次数、顺序及重复结果均一致；18 组所有输出声明按现有映射一致，1 组表达式别名存在 int4/bigint 差异，作为独立算术类型问题保留 |
| 首轮已匹配的 62 条，跨 15 个原 stage | 62 条仍按原 .out 匹配；不是全批 313 条重跑，也不证明 .out 缺少的类型维度 |
| `.venv/bin/mypy ...` | 未运行：该解释器环境没有 mypy 可执行文件；没有擅自安装依赖 |

补证原查询时间为 2026-11-23 08:13:59–08:14:01 UTC，边界为 08:14:36–08:14:38 UTC，62 条回归为 08:15:36–08:15:38 UTC。没有进行通用计时功能开发或保存独立日志。完整根测试集、C 扩展、完整 mypy / make check、其他 Doris 版本及最早支持版本尚未验证。

## 5. 剩余问题与下一项建议

| 观察 | 任务或去向 | 下一步 |
| :--- | :--- | :--- |
| 0134 的 FROM GENERATE_SERIES 以及 LATERAL 仍失败 | 普通非相关 FROM 序列基础可关联 task-008；相关/LATERAL 明确不在其完整承诺范围 | 基础序列和相关查询算法分别调查，不能声称只做 task-008 就整条通过 |
| 0179 投影位置 GENERATE_SERIES 不存在 | 既有查询级待研究事项，task-008 明确排除投影 SRF | 先确认先聚合后展开、NULL、空输入和类型契约，不能强套 FROM 规则 |
| 0137 分组相关子查询失败，且实时源端与 .out 冲突 | 源版本/执行前提核对；仍关联既有相关子查询研究事项 | 先补齐源证据，再判断是否有可安全实现的独立 SQLGlot 任务 |
| 0551/0552 CASE 声明、别名边界 INT 加法声明不同 | 既有类型契约待研究事项 | 不在排序任务中自动增加 CAST，不放宽比较规则 |
| task-001 数组隐式类型和 Decimal 证据仍未验收 | 沿用 task-001 | 不因 task-002 通过而关闭数组任务 |

**建议下一项独立实现 task-003：ARRAY_AGG 保留 NULL 并补偿空输入。** 不是因为它编号为 003，而是已有归因确认当前 Doris 的 COLLECT_LIST 路径会丢失源端应保留的 NULL，且空输入需要单独处理；它也是 task-004 聚合内部排序的前置任务，范围清楚、可独立验证。当前代码仍保留 `exp.ArrayAgg: rename_func("COLLECT_LIST")`；具体原例和对照见[task-003](../attribution/aggregates-001-attribution-summary.md#task-003)及[Case 0287](../attribution/cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md)。本轮没有实施或验收 task-003，开始时仍需在届时代码上复现。

本次新暴露的序列/相关子查询问题没有经过足够补证形成新的可实施任务，不强行编号，也不因为一次失败就断言 Doris 永远不能模拟。本次未发现所测范围内由排序修改引入的回归；未覆盖范围不能据此推定无回归。

**整份输入未完成**：task-001 未验收，task-003–009 未实施，研究和外部前提仍在，未做最终同版全部 stage 回归。下一轮沿用 aggregates-001，读取本报告和归因汇总当前任务清单，在明确授权后处理 task-003 或用户另选任务。没有创建空白 fix-003 文件。
