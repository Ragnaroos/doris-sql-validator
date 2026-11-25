# aggregates-001 / fix-010：REGR_COUNT 成对计数

## 1. 本轮结论

**task-009 已修复并完成普通数值参数成对计数的约定验收；整份输入未完成。** 只处理用户选定的 task-009。fix-010 是本轮执行编号，不是新任务；前一轮 fix-009 是 task-008 的 NULL 参数补齐。

| 检查范围 | 实际结果 |
| :--- | :--- |
| 两条关联原查询 | 0073 从 Doris 找不到函数变为匹配；0544 能执行，第三列计数与 BIGINT 类型正确，整条仍因其他统计/类型问题不匹配 |
| 67 条 REGR_COUNT 边界与上下文 | 66 条执行、字段类型、别名、行值、重复次数及必要顺序通过；1 条外层 SUM(BIGINT) 的 NUMERIC/BIGINT 类型差异保留，计数和值正确；全部双端复跑稳定 |
| 额外无 REGR_COUNT 的类型控制 | COUNT(*) 后再 SUM，同样出现 NUMERIC/BIGINT 差异，证明该外层类型问题不依赖本改写 |
| 额外负向控制 | 非法字符串 CAST：PG 22P02；转译明确 UnsupportedError，不执行 Doris，不伪造匹配 |
| 132 条原查询，17 个阶段 | 81 匹配、28 Doris 执行失败、18 行值/顺序不同、1 转译失败、4 源端负向；此前 80 个匹配全部保持，新增匹配仅 0073 |
| 单元测试 | PG/Doris/MySQL 156 方法、全部方言 1079 方法、核心 233 方法通过；156 包含于 1079，不相加 |

本轮互斥任务状态：已修复并完成约定验收 1 项，其他状态均 0 项。全批九项当前为 **7 项完成约定验收、2 项已修改但未完成验收、0 项未处理**；task-001/003 的类型验收和待研究事项没有关闭，不能据初始任务都已实施宣称整份输入完成。

详细生成 SQL、原查询结果、边界组合及限制见 [task-009 报告](tasks/aggregates-001/fix-010/task-009.md)。首轮 JSON、原归因和以前各轮修复报告不覆盖。

## 2. 授权与代码身份

仅修改 `../sqlglot-experiment/sqlglot/generators/doris.py` 与 `tests/dialects/test_doris.py`，净增 114 行。保留此前六个累积修改文件和工作流已有修改；不改验证框架、Skill、原 SQL/.out、YAML、首轮 JSON、DDL、数据或 Session 政策，不升级依赖、不启动其他 Agent。

| 项目 | 实际值 |
| :--- | :--- |
| checkout / 分支 | ../sqlglot-experiment / codex/doris-array-literal |
| 起止 HEAD | 089891f2521780e2c5b243005017af9db62f25a6，未切换基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 起始累积 diff SHA256 | 2ecc6f54c7579f9968914f9fa850050140fcdbd734d4c740ec8ffd831941c41f |
| 最终累积 diff SHA256 | 444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18 |
| 框架解释器 | ../doris-sql-validator/.venv/bin/python |
| 实际 import | ../sqlglot-experiment/sqlglot/__init__.py，30.25.1.dev355；PYTHONPATH=../sqlglot-experiment:src |
| PostgreSQL | 本轮实测 18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | SHOW FRONTENDS 本轮实测 doris-4.1.3-rc02-7126cf65d96、Alive=true；127.0.0.1:9030；UTC、enable_strict_cast=false |
| 执行时间 | 2026-11-24；64 条基础边界批次结束 02:18:56 UTC，132 条原查询回归结束 02:19:47 UTC；随后完成三条补充边界和两条控制 |
| 保存/发布 | 代码仅在本地，未 commit/push，未创建 Issue/PR |

diff 指纹包含保留的全部前轮修改，不表示要把九项混成一次提交。task-009 的提交边界是一个成对计数行为与对应测试，无必须依赖其他 task 的实现；将来提交时仍需另获授权并隔离现有修改。社区 checkout `../sqlglot` 的受版本控制文件未修改。

## 3. 输入与执行方式

原输入仍是 `../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql` 和同名 `.out`；不复制或修改，不核验 .out 指纹。准备前提引用 [准备报告](../data-preparation/aggregates-001-data-preparation.md)及同前缀双端 setup.sql，本轮没有重新装数或把历史 540 次核验称为本轮执行。

| 任务输入与首轮报告 | SHA256 |
| :--- | :--- |
| [stage-01 YAML](../data-preparation/aggregates-001-stage-01-cases.yaml) | cf04cd870b828d26d1d0846d0b5a5be0f38bc25c7c76d100e138f5b9de31d423 |
| [stage-41 YAML](../data-preparation/aggregates-001-stage-41-cases.yaml) | 95a8c112c1580bd1648a95ed907da70e60c5c0495931ecc37af27d25cd2425d4 |
| [stage-01 首轮 JSON](../validation/aggregates-001-stage-01-validation.json) | 312e26743e1b476ee11278b66aed299ecd347aa741a193864dc5aa83048fe0b0 |
| [stage-41 首轮 JSON](../validation/aggregates-001-stage-41-validation.json) | a4b8002060b46227d6a7da3d4180fc721c17ee3ece62db3d838b962b50b0c41c |

在一个 Python 进程内，按实际阶段调用 `CliRunner().invoke(app, ['run','--path',<原 YAML>,'--stdout','--id',<ID>,...])`。范围为 fix-009 的原 130 条，加 0073、0544 两条；不改变原 130 条的分母，也不宣称重跑了全部 313 条。每阶段的查询数：01:49、03:8、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:14、25:6、30:3、31:21、32:1、41:1、42:3、43:4，合计 132。

运行时真正从源 SQL 调用 `SqlglotTranspiler.transpile_case` / `parse_one(..., read='postgres').sql('doris', unsupported_level=RAISE)` 生成目标，未用手写候选代替。实时补证调用 `pg_probe.execute_query` 与 `compare_probe`，每条限时 10 秒、完整结果上限 10000 行；只读连接、每条重复一次。数据阶段分别为 dsv_wf_agg001_s01、s41 等；常量边界使用 s01，不建临时表。只向终端返回事实，不新建执行 JSON、日志或 evidence 目录。

## 4. 测试与剩余问题

工作目录 `../sqlglot-experiment`，解释器 `.venv/bin/python`，测试 PATH 包含该 `.venv/bin`：

| 实际命令 | 结果 |
| :--- | :--- |
| python -m unittest tests.dialects.test_doris.TestDoris.test_regr_count tests.dialects.test_doris.TestDoris.test_regr_count_exclusions | 2 方法通过；补丁前对应 16 个子测试失败，复现缺口 |
| python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql | 156 方法通过 |
| python -m unittest discover -s tests/dialects | 最终代码下 1079 方法通过 |
| python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens | 233 方法通过 |
| .venv/bin/ruff check 与 format --check 六个累积修改文件；git diff --check | 通过 |

未运行完整 make check、C 扩展、mypy 或 DuckDB executor/optimizer 全套；不将未运行写成通过。

| 保留问题 | 去向 |
| :--- | :--- |
| 0544 方差 NUMERIC/DOUBLE、SUM NUMERIC/BIGINT | 复用现有类型/精度研究，不混入成对计数规则；原 Case 追加本轮证据 |
| 外层 SUM(BIGINT) 类型差异 | 无 REGR_COUNT 控制也复现，复用同一类型研究，不增加重复 task |
| task-001/003 数组元素类型及完整验收 | 仍未关闭，建议下一轮先补齐这些已有任务的类型证据和安全实现范围 |
| FILTER、窗口、DISTINCT、内部排序、易变/任意表达式、字符串隐式转换 | 本 task 不支持；RAISE 模式明确拒绝，不以能生成文本冒称等价 |
| 超出可表示数值域、CAST 的跨库异常/溢出、NaN/Infinity | 未完成通用保证；没有放宽比较或吞异常来关闭这些范围 |

## 5. 完成条件

所选 task-009 完成约定验收，无本轮发现的既有匹配回归。整份输入仍未完成：task-001/003 未验收、待研究/前提阻断仍存在，本轮未进行最终全部 43 阶段回归，也未覆盖两个既知导入遗漏。下一轮建议回到已有类型验收，而不是凭九项都已实施就结束工作流；具体任务仍由用户授权。没有自动开始下一项。
