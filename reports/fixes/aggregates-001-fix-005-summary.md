# aggregates-001 / fix-005：普通聚合的 FILTER 转换

## 1. 本轮结论

指定任务模式，仅处理 [task-005](../attribution/aggregates-001-attribution-summary.md#task-005)。**已修复并完成普通聚合条件筛选规则的约定验收；整份输入未完成。** 没有 commit/push、Issue/PR、装数、Session 政策或验证框架修改。

实现将已知忽略 NULL 的 SUM、AVG、MIN、MAX、COUNT(expr)、ANY_VALUE 的 FILTER 转为条件参数，保留 DISTINCT；COUNT(*) 单独转为 COUNT(IF(条件,1,NULL))，不生成 COUNT_IF。不对数组聚合、未知聚合、窗口或有序集合盲用同一规则。

| 本轮范围 | 结果与限制 |
| :--- | :--- |
| 8 条关联原查询 | 原来全部 Doris 语法失败；现在按原 .out 为 6 匹配、1 行值差异、1 Doris 执行失败 |
| 实时原生类型补证 | 3 条字段声明一致；3 条值相同但声明不同；1 条值和类型都不同；1 条目标失败，未比较结果。不能把 6 条 .out 匹配称为全部维度等价 |
| 156 条基础边界 | 全部双端成功，字段/别名、类型、重复稳定均核对；155 条行值一致，1 条 AVG(DISTINCT) 浮点尾差保留 |
| 12 条上下文边界 | 分组、HAVING、子查询、CTE、LEFT JOIN、不同 FILTER、受保护 CAST/除法、Decimal 和 BIGINT 均取得一致值/行数/重复次数及必要顺序 |
| 浮点差异独立控制 | 删除 FILTER 后仍有同样差异；PG 二进制确认并非只有文本显示问题。它不是本次 FILTER 引入，未改成通过、未放宽容差 |
| 91 条原查询回归 | 16 个原数据阶段：71 匹配、9 Doris 执行失败、7 行值或顺序不匹配、4 源端负向；此前 65 条匹配全部保持 |

任务验收只关闭 FILTER 语法/条件输入规则，**不关闭**原生 AVG 精度、整数除法、类型推断、Collation 或相关聚合研究；不是宣布全部 168 条边界完全等价。完整 SQL、实际反例和判断依据见[任务报告](tasks/aggregates-001/fix-005/task-005.md)。

## 2. 版本、输入与环境

| 项目 | 实际值 |
| :--- | :--- |
| 目标 checkout / 分支 | `../sqlglot-experiment` / `codex/doris-array-literal` |
| 起止 HEAD | `089891f2521780e2c5b243005017af9db62f25a6`，本轮未切换或刷新基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；未提交或推送 |
| 起始累积 diff SHA256 | `0cb0ae94b56c917d9cd001996ea998a76c307589351385e829aea1397e3aef02` |
| 最终累积 diff SHA256 | `8a6e18fbf1630778b6af86afaa03cdbbbfba17833bcd65ff40eabeb13f64e152`，git diff --binary；包含保留的 task-001 至 task-004，不是一个混合提交计划 |
| 本轮实际修改 | `sqlglot/generators/doris.py` 和 `tests/dialects/test_doris.py`；其他 4 个累积修改文件未变 |
| 验证解释器 / import | `../doris-sql-validator/.venv/bin/python`；PYTHONPATH=`../sqlglot-experiment:src`；实际为 `../sqlglot-experiment/sqlglot/__init__.py`，包版本 `30.25.1.dev355` |
| PostgreSQL | 18.1，127.0.0.1:5432；UTC、DateStyle=ISO, MDY、extra_float_digits=0 |
| Doris | SHOW FRONTENDS 实查 `doris-4.1.3-rc02-7126cf65d96`、Alive=true；127.0.0.1:9030；UTC、enable_strict_cast=false、enable_decimal256=false |
| 原查询与边界库 | 双端 `dsv_wf_agg001_s31`；其他回归使用各自 YAML 的阶段库 |

遵循目标 AGENTS.md、CONTRIBUTING.md、pg-doris-fix Skill、工作流及修复报告模板；没有调用其他 Skill/Agent。工作流已有文档/Skill 改动、SQLGlot 前四轮修改及原社区 checkout 均保留；凭据只从既有 .env 载入进程，不进入文件。

输入为原 `aggregates.sql` / `aggregates.out`，引用[准备说明](../data-preparation/aggregates-001-data-preparation.md)及双端准备 SQL 的 stage-31 段。没有重新建库、装数或核验全部基表，历史数据核验不冒称本轮执行。

| 保持不变的输入 | SHA256 |
| :--- | :--- |
| [stage-31 YAML](../data-preparation/aggregates-001-stage-31-cases.yaml) | `9d395b715af738b02b4c0f06bf0494a53fe081d052f972d705951d9461cd27f6` |
| [stage-31 首轮 JSON](../validation/aggregates-001-stage-31-validation.json) | `c0953af4ac2656d8f5ccd587d8a5f9c53e8648695a8064de7b8a8c27526cccc2` |
| 原 aggregates.sql | `9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62` |

不保存或核验 .out 指纹。版本号本身不能区别未提交修改，须结合 HEAD、diff 和 import。

## 3. 任务与测试

| task | 当前状态 | 实施与提交边界 |
| :--- | :--- | :--- |
| [task-005](tasks/aggregates-001/fix-005/task-005.md) | 已修复并完成约定的条件筛选规则验收 | 复用既有 no_filter_sql，COUNT(*) 目标适配；没有其他 task 的必须实现依赖；未提交、未推送 |

先加测试，在修改前 2 个方法中取得 31 个真实失败断言；补实现后通过。代码按精确聚合节点白名单处理，复制 AST 后调用 helper；COUNT(t.*) 不冒充 COUNT(*)，避免复合行/外连接语义误用。没有新建公共 helper 或给验证器注入 Schema。

| 实际命令，工作目录 ../sqlglot-experiment | 结果 |
| :--- | :--- |
| `PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.dialects.test_mysql` | 145 个方法通过，含本轮 2 个新方法 |
| `python -m unittest discover -s tests/dialects -t .`，同一解释器/PATH | 1,068 个方法通过，包含上面 145 个，不重复相加 |
| `python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens` | 233 个方法通过 |
| Ruff check / format --check，6 个累积修改文件；git diff --check | 通过 |

最后另将新方法的生成调用设为 copy=False，2 个定向方法仍通过，直接验证改写未原地污染输入 AST。没有运行完整 make check、C 扩展、mypy 或依赖 duckdb 的 executor/optimizer 全套，也没有安装/升级依赖。

## 4. 回归事实与剩余问题

2026-11-23（UTC）：09:31:43 复现旧错误；09:33:27–09:33:28 重跑 8 条原文并双端重复、核对 .out；09:34:14–09:34:25 基础边界；09:35:46–09:35:47 上下文/AVG 控制；09:37:48–09:37:50 最终原查询回归。

最终在一个 Python 进程中按阶段调用 CliRunner 的 `run --path <原阶段 YAML> --stdout --id ...`，只向终端返回事实；不保存新验证 JSON，不覆盖首轮。阶段数量：01:21、03:6、06:1、07:5、08:1、09:8、10:2、11:1、15:3、17:9、25:6、30:3、31:17、32:1、42:3、43:4，共 91。

91 = 前轮 75 + 本任务 8 + 相关代码路径的 8 条额外原查询。额外 8 条中，0387/0388/0389/0393 是相关聚合研究，仍 Doris 执行失败；0394–0397 是 .out 源端负向，仍默认不归因。没有把额外查询当作 8 个新修复任务，也没有把源负向算作成功 MATCH。

| 剩余观察 | 处理 |
| :--- | :--- |
| 0381：PG 1000 / Doris 2828.968253968249；bigint / double | 整数除法/类型前提研究，未强制改所有 `/` 为 DIV |
| 0383 及 0387/0388/0389/0393 的外层聚合引用失败 | 复用相关聚合归属研究；不能用表达式级 FILTER 补丁关闭查询级问题 |
| 0384 text / varchar(1)，0385/0392 int4 / tinyint | 表示/类型契约研究；原 .out 缺原生类型，保留“值匹配不等于类型全对齐” |
| AVG(DISTINCT) 浮点尾差 | 本轮带/不带 FILTER 的源与目标均分别相同，确认不是 FILTER 新增；原精确比较仍报差异，源文本读取还叠加 extra_float_digits=0 的显示舍入 |
| 原数组相关的剩余 4 执行失败、6 文本/值差异 | 保留 fix-003/004 的原去向，没有重新归为 FILTER 缺陷 |

## 5. 当前清单与下一步

全批仍为 9 个稳定 task：3 项完成约定验收（002/004/005），2 项已修改未验收（001/003），4 项未处理（006–009）。没有新增/重新打开其他 task；原生浮点、类型和相关查询只补研究证据。

**整份输入未完成。** 本轮未重跑全部 313 条/43 阶段或导入遗漏；未处理及未验收任务、前提问题仍存在。建议下一项 **task-006：PostgreSQL EVERY 归一化与 Doris 布尔聚合**，它尚未实施。由人选择并授权后再继续，不在本轮顺带修改。
