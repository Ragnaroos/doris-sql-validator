# aggregates-001 / fix-003：ARRAY_AGG 的 NULL 和空输入修复

## 1. 结论与范围

**task-003 状态：已修改但未完成验收。** 普通 PostgreSQL ARRAY_AGG 的 NULL 保留和空输入 SQL NULL 已实现；不能把它写成所有关联查询、数组元素类型和顺序都已匹配。

实际生成规则为 `NULLIF(ARRAY_AGG(a), ARRAY())`：有记录时保留 NULL 和重复元素；只有真正的空数组结果转为 SQL NULL，不把 `[NULL]` 当成空输入。PostgreSQL Parser 将空输入要求保存在 AST 中，Doris 原生 ARRAY_AGG 不套该补偿；Hive/Spark COLLECT_LIST 继续走排除 NULL 的原路径。

本次只授权 task-003，未修 task-004 内部排序、序列、类型推断、时间精度或验证框架。没有建表装数、改原 SQL/.out/YAML、commit、push 或创建 Issue/PR。

| 本轮任务状态 | 数量 |
| :--- | ---: |
| 已修改但未完成验收 | 1 |
| 已修复并完成约定验收 / 重新打开 / 当前阻断 / 未处理 / 不需修改 | 各 0 |

复用已有 task-003，没有新增可实施 task；类型/表示和时间精度发现补入原归因汇总的研究项。全批 9 项当前为：task-002 已完成约定验收，task-001/003 已修改未完成验收，task-004–009 未实施。**整份输入未完成。**

## 2. 代码、输入与环境

| 项目 | 实际信息 |
| :--- | :--- |
| checkout / 分支 | [sqlglot-experiment](../../../sqlglot-experiment/) / `codex/doris-array-literal`，保留 task-001/002 既有修改 |
| origin / upstream | `https://github.com/Ragnaroos/sqlglot.git` / `https://github.com/tobymao/sqlglot.git` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`，本轮没有 fetch、切基线或提交 |
| 起始 diff SHA-256 | `4be19b72e29259a100f7fbc73ac30706f0a7e9b53ac52ff1d1d581b0fb335f35`，与 fix-002 最终记录相同 |
| 最终累计 diff | 6 文件，252 行增加/12 行删除，含前两项修复；本轮净增加 97 行/删除 3 行，涉及 5 个文件，不修改既有 Doris Parser |
| 最终 diff SHA-256 | `2de3541799b6c32ded8670f98121fb35a13a3df7d80c413e92ff9827c2d3d46f`；对 `git diff --binary` 输出计算 |
| 实际导入 | Python 3.12.15；`../sqlglot-experiment/sqlglot/__init__.py`；版本字符串 `30.25.1.dev355`，同时用 HEAD/diff 识别代码 |
| 解释器 | 单测使用实验目录 .venv/bin/python；验证使用 `../doris-sql-validator/.venv/bin/python`，`PYTHONPATH=../sqlglot-experiment:src` |
| 双端 | PostgreSQL 18.1，127.0.0.1:5432；Doris `doris-4.1.3-rc02-7126cf65d96`，127.0.0.1:9030，本轮 SHOW FRONTENDS 确认 |
| 数据与会话 | 原 stage-17/30 对应数据库；其他回归使用各自原阶段。补证 UTC、PG ISO/MDY、extra_float_digits=0，Doris enable_strict_cast=false；每条补证 10 秒、10000 行上限 |
| 准备材料 | [数据准备](../data-preparation/aggregates-001-data-preparation.md)；既有 postgres/doris-setup.sql，未重放写入 |
| 原始输入 | `../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql` 及配对 aggregates.out，未复制或替换 |

本轮遵守目标仓库 AGENTS.md/CONTRIBUTING.md 和 pg-doris-fix Skill。凭据只加载到进程，不写入报告；没有额外候选文件、执行 JSON、测试日志、patch 或 evidence 目录。原 `../sqlglot` 不修改。当前工作区包含多项未提交修复，不应把整个 diff 当作 task-003 的一个提交。

## 3. 实现和原查询结果

| task / 范围 | 本轮结果 | 报告与代码归属 |
| :--- | :--- | :--- |
| [task-003](../attribution/aggregates-001-attribution-summary.md#task-003) | NULL/空输入定向修复已生效；类型与完整查询验收仍有未满足项 | [任务报告](tasks/aggregates-001/fix-003/task-003.md)；ArrayAgg AST、PG Parser、Doris Generator、PG/Doris 测试 |

10 条原关联查询全部按实际阶段执行，没有删减或手改目标答案。结果仍是 **9 条 Doris 执行失败、1 条行值或顺序不匹配、0 条完整 MATCH**：

- 7 条包含聚合内部 ORDER BY，本轮明确不改，仍报 `collect_list doesn't support order by expression`。其中按聚合值自身排序的 5 条属于 task-004，另外 2 条是不同排序键的研究事项。
- 0276 仍被 GENERATE_SERIES 语法阻断，关联 task-008。
- 0371 仍把整行别名 s 当成列，还涉及 ARRAY_DIMS，属于独立研究。
- 0287 的真实 NULL 已不再丢失，实时结构化值为 `[1,2,3,NULL]`，但 `.out` 的 `{1,2,3,NULL}` 和目标 JSON 文本仍不相同；PG 元素 INT4 / Doris TINYINT 也是真实类型差异，不能写成完全匹配。

10 条当前 PG 均成功，文本化结果与对应原 .out 一致。不能用“修复后完整 MATCH 数未增加”推断 NULL 修复无效，也不能用它掩盖类型和其他能力尚未解决。

## 4. 实际回归

| 检查 | 结果 |
| :--- | :--- |
| 新增 3 个测试方法，修改实现前运行 | 21 个断言失败、0 个错误，能检出缺口；不是 21 条独立业务查询 |
| PG/Doris/MySQL 定向测试 | 140 个方法通过，包含前两项修复；新增 2 个 Doris 方法、1 个 PG 方法 |
| 全部方言测试 | 1063 个方法通过，包含定向测试，不重复累计 |
| Parser/Generator/Transpile/Expression/Serde/Build/Schema/Token 核心测试 | 233 个方法通过；最终根测试也覆盖这些模块 |
| 最终 `SKIP_INTEGRATION=1 python -m unittest` | 1546 个测试条目：1544 通过，2 个模块因缺 duckdb 导入失败（test_executor、test_optimizer）；不是全套通过 |
| Ruff check、format --check、git diff --check | 通过；未安装缺失依赖，mypy/C 扩展/make check 未运行 |
| 22 个固定 PG 边界，目标由最终修改后 SQLGlot 生成 | 双端均成功；19 组完整行值一致，3 组保留差异；每组两端各重复一次，端内结果均稳定 |
| Doris 原生 ARRAY_AGG / COLLECT_LIST 两项控制 | 前者空输入仍是 []，后者全 NULL 仍是 []，没有错误套 PG 的空输入要求 |
| 最终 CLI 原输入回归 | 75 条、16 个 stage：65 MATCH、9 Doris 错误、1 行值/顺序差异。65 = 首轮 62 + fix-002 新匹配 3，本轮无新增完整 MATCH，也无该范围内的匹配退化 |

完整命令见任务报告。首次核心命令误列不存在的 tests.test_dialects，修正列表后 233 项通过；HAVING 单测最初混用了 PG/Doris 对 IS NOT NULL 的输出形式，改用本范围的 IS NULL 场景后通过，未修改无关格式规则。根测试的缺 duckdb 错误未通过删测试隐藏。没有执行全批 313 条的最终验收。

最终代码的 22 组边界及 75 条 CLI 回归于 2026-11-23 09:03:43–09:03:47 UTC 执行；详细逐条补证另见同一任务报告，不另存执行文件。

## 5. 未满足项和后续处理

| 差异或缺证 | 已取得证据 | 处理方向 |
| :--- | :--- | :--- |
| 无聚合内 ORDER BY 的 DISTINCT 数组顺序 | 一组 PG `[1,2,NULL]`、Doris `[1,NULL,2]`，两端各自重复稳定 | 仍记行值不同；顺序未被源 SQL 保证，不能硬编码排序制造 MATCH，也不能直接认定是 NULL 修复错误 |
| 布尔数组表示 | PG `[true,NULL,false]` / Doris `[1,NULL,0]`；只读拆元素并 CAST BOOLEAN 后，类型和值一致 | 框架的嵌套布尔归一化需另行授权；不把所有数组数字自动改成布尔 |
| 数组元素类型 | 原 0287 的 int4[] / array<tinyint> 真正不同；显式 INT 边界的 _int4 / array<int> 则存在比较器未递归识别别名的问题 | 分开记录真实类型差异与比较器局限，不能一律忽略声明。Decimal 数组元素精度缺完整源元数据，不能照抄工具顶层“不适用”当通过 |
| TIMESTAMP 微秒损失 | 单独 CAST 也丢 `.123456`；独立 Doris DATETIME(6) 对照保留，说明不是 ARRAY_AGG 丢 NULL | 新的类型转换研究项，非本轮引入；未修 SQLGlot 时间规则，须补不同精度/值域后确定安全修复范围 |
| 源数组下标补证路径 | 核对时看到 PG `[1]` 被当前代码生成 `[0]`；布尔表示控制实际使用 Doris 原生 1-based 下标 | 未执行该生成下标变体，不认定其完整根因；数组索引单独研究，不混入 task-003 |

task-003 的 NULL/空输入实现可以供后续规则研究使用，但当前状态不关闭：先明确数组元素类型契约、补齐嵌套类型与精度验收，记录哪些是框架误报、哪些是独立真实类型缺口；不能通过放宽比较器或悄悄加 Schema 来完成验收。之后可单独处理 task-004 的聚合值自身排序，不能声称它解决不同键排序或无 ORDER BY 时所有实现的物理顺序。

本轮没有新增可实施 task-id；独立问题进入归因汇总研究项，确定实现及验收范围后再编号。整份输入未完成，下一轮继续读取当前归因任务清单和本报告；不创建空白 fix-004 文件。
