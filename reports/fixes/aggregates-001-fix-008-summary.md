# aggregates-001 / fix-008：FROM 常量整数 GENERATE_SERIES

## 1. 本轮结论

仅处理 [task-008](../attribution/aggregates-001-attribution-summary.md#task-008)。**非 NULL 的常量 INT4 序列主路径已修复；NULL 参数仍未覆盖，因此 task-008 为“已修改但未完成全部验收”。整份输入未完成。** 未缩小原任务的验收条件来宣布完成，也未开始 task-009。

| 实测范围 | 结果 |
| :--- | :--- |
| 32 条关联原查询，4 个实际阶段 | 8 与原 .out 匹配、3 行值/顺序不同、20 Doris 执行失败、1 转译失败 |
| 八条新增 .out 匹配的类型补证 | 0051/0054/0058 类型声明一致；另五条保留 NUMERIC 与 BIGINT/DOUBLE/DECIMAL 差异，不称全部完整匹配 |
| 65 条有限边界与上下文 | 双端成功，值/重复次数、字段数、已取得类型和必要顺序一致；各端均重跑一次，稳定。含负步长、空区间、INT4 极值和 1001 行，无固定 1000 上限 |
| NULL 参数 | 四种成功源调用返回零行，但当前转译报 UnsupportedError；不当成源端负向或通过 |
| 非 NULL 的零步长 | PG SQLSTATE 22023；当前明确拒绝，不输出伪成功空关系，不默认复制错误全文 |
| 130 条相关原查询，16 阶段 | 80 匹配、28 Doris 执行失败、17 行值/顺序不同、1 转译失败、4 源端负向；此前 72 条匹配全部保持 |
| 单元测试 | PG/Doris/MySQL 152、全部方言 1075、核心 233 个方法通过；152 被 1075 包含，不相加 |

实现、全部 32 条源 SQL/真实新生成 SQL/字段与具体错误、边界和限制见[任务报告](tasks/aggregates-001/fix-008/task-008.md)。报告区分序列规则与整条查询，未把保留的 UDF、统计/NaN、LATERAL、派生表别名或 WITHIN GROUP 问题误记为序列完成或新增回归。

## 2. 授权、代码与环境

指定任务模式，目标 ../sqlglot-experiment；不修改验证框架、数据准备、原 SQL/.out/YAML/首轮 JSON，也未装数、更改 Session 政策、安装依赖或派发子 Agent。遵循 pg-doris-fix、目标 AGENTS.md/CONTRIBUTING.md、工作流与模板。前七轮代码与工作流原有修改保留。

| 项目 | 本轮事实 |
| :--- | :--- |
| 分支 / 起止 HEAD | codex/doris-array-literal / 089891f2521780e2c5b243005017af9db62f25a6，未切换或刷新基线 |
| origin / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 起始 / 最终累积 git diff --binary SHA256 | 073be5b32f6e6208a2a92cd72d980003879511b1d3097fd254356b34ecc04792 / cdb5d8222785933bb0d3f1d7a40a13a9da077032fb07157ddd559d575a19ce68 |
| 本轮独立代码归属 | generators/doris.py 的表位置序列转换/未支持诊断，tests/dialects/test_doris.py 两个方法；相对前轮增加 135 行、删除 7 行，含原 table_sql 位置合并。其他四个累积修改文件不变 |
| 保存状态 | 代码仅本地未提交；没有 commit/push、Issue/PR。该规则及对应测试可独立整理，不将同文件的前七轮混为一个提交 |
| 实际运行 import | ../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-experiment:src，版本30.25.1.dev355；../sqlglot-experiment/sqlglot/__init__.py |
| 当前 PG | 18.1，127.0.0.1:5432；UTC、DateStyle ISO/MDY、extra_float_digits=0 |
| 当前 Doris | SHOW FRONTENDS 实查 doris-4.1.3-rc02-7126cf65d96，Alive=true；127.0.0.1:9030，UTC、enable_strict_cast=false；VERSION()兼容值不充当产品版本 |
| 主任务双端数据库 | dsv_wf_agg001_s01、s03、s17、s31，均取实际阶段 YAML；未重建/重装 |
| 主要执行时间 | 2026-11-23T10:44:03+00:00 起；32 条逐条事实整理完成于 2026-11-23T10:47:14.875742+00:00；后续补查 UNION ALL 双端列名均为 v |

## 3. 固定输入与执行方式

原 aggregates.sql/.out 位于 ../doris-sql-validator/cases/postgres/manual/current/assets/；源 SQL SHA256 仍为 9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62。原 .out 仅按内容定位使用，不额外保存/核验指纹。[准备说明](../data-preparation/aggregates-001-data-preparation.md)和同前缀双端 setup.sql 保持；540 次表核验是历史准备事实，不宣称本轮重新执行。

| 主任务输入/首轮报告 | SHA256（本轮只读，未覆盖） |
| :--- | :--- |
| [aggregates-001-stage-01-cases.yaml](../data-preparation/aggregates-001-stage-01-cases.yaml) | `cf04cd870b828d26d1d0846d0b5a5be0f38bc25c7c76d100e138f5b9de31d423` |
| [aggregates-001-stage-01-validation.json](../validation/aggregates-001-stage-01-validation.json) | `312e26743e1b476ee11278b66aed299ecd347aa741a193864dc5aa83048fe0b0` |
| [aggregates-001-stage-03-cases.yaml](../data-preparation/aggregates-001-stage-03-cases.yaml) | `6fd4dbbc9bbc3b49c3ecafeedbf6e041699714648ef1793f8e067c4c4f405c01` |
| [aggregates-001-stage-03-validation.json](../validation/aggregates-001-stage-03-validation.json) | `dceca6c2e3bdea8cd7cae7d7c96ab0045bb1f2f2d25238cde076dfbb2d2ec224` |
| [aggregates-001-stage-17-cases.yaml](../data-preparation/aggregates-001-stage-17-cases.yaml) | `c4452ebf80f01193510ef591c849dd551e05d2a42d48bb05fac5de0f6825abd2` |
| [aggregates-001-stage-17-validation.json](../validation/aggregates-001-stage-17-validation.json) | `a35f570ffe0e0f7779f27a82d9973e90966e80f3dafc78f86b3db99fd29ad389` |
| [aggregates-001-stage-31-cases.yaml](../data-preparation/aggregates-001-stage-31-cases.yaml) | `9d395b715af738b02b4c0f06bf0494a53fe081d052f972d705951d9461cd27f6` |
| [aggregates-001-stage-31-validation.json](../validation/aggregates-001-stage-31-validation.json) | `c0953af4ac2656d8f5ccd587d8a5f9c53e8648695a8064de7b8a8c27526cccc2` |

在一个 Python 进程按阶段通过 CliRunner 调用 `run --path <实际阶段 YAML> --stdout --id ...`；没有保存新的验证 JSON。每个选定 Case 真正调用修改后 SQLGlot。只读补证使用实际生成 SQL、execute_query/compare_probe，10 秒超时和10000行上限，完整取得本轮有限结果；不是拿手写候选当修复验证。工具函数每次仍独立连接，本轮没有实现连接池或改框架。

32 条当前 PG 原文全部成功。25 条当前 PG 文本与历史 .out 相同；0085/0086/0093/0094/0095/0099/0100 共7条统计结果不同，原 .out 保留，不用实时值静默换答案。边界是新变体，不借原 .out 充当对应答案；有最终 ORDER BY 比顺序，无则比保留重复次数的多重集合，类型另查。

## 4. 实现与验收边界

FROM 中的 ExplodingGenerateSeries 仅对非 NULL 常量 INT4 的 start/end/step 转成 NUMBERS 派生关系，长度用精确整数公式计算，结果列 CAST AS INT。保留默认 generate_series 名、AS g 的标量列 g、AS g(x) 的 x 与引号/限定引用，保留 JOIN，不改变输入 AST。错误方向生成 NUMBERS('number'='0')，不是一条 NULL 记录。

NULL、零步长及其他排除上下文在 RAISE 下明确不支持；没有按字面量 NULL 硬编码结果。当前静态 NUMBERS 方案尚不能完成成功源 NULL 调用的语义，需要继续设计运行时路径；这属于同一 task-008 的未完成项，而不是 Doris 已被证明做不到。较大 INT4 范围只检查生成，不执行数十亿行；不宣称资源性能已验收。

| 当前任务 | 状态 | 代码/提交边界 |
| :--- | :--- | :--- |
| [task-008](tasks/aggregates-001/fix-008/task-008.md) | 已修改但未完成全部验收 | 常量整数表关系一项独立行为；无必须依赖前七轮的规则，当前未提交/推送 |

## 5. 回归、余项与下一步

实际命令、逐条与边界见任务报告。先补测试时19个失败断言，最终通过；最后1075个全部方言和233个核心方法在最终代码/测试状态复跑通过。Ruff check/format --check与git diff --check通过。未运行完整make check、C扩展、mypy或DuckDB相关全套，不把缺依赖当通过。

130 是前轮99与本任务32的并集，0276只计一次；阶段查询数为01:48、03:8、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:14、25:6、30:3、31:21、32:1、42:3、43:4。首轮313条统计、既有历史报告不改；本轮没有全量回归43阶段。

| 余项 | 当前去向 |
| :--- | :--- |
| NULL 参数成功源查询 | 同 task-008 未完成；先补运行时方案和边界，不提前标完成 |
| 0052/0053/0055/0056/0057 类型契约 | 保留既有类型/精度研究，八条显示NULL匹配不关闭它 |
| 0059/0060 NaN、0087 CORR近常数 | 保留非有限数/数值算法研究；不是序列值生成错误 |
| 9条 REGR_R2 缺失 | 保留回归统计研究，与 task-009 REGR_COUNT 不是同一函数能力，不混修 |
| 0134 LATERAL、0136 ARRAY子查询 | 复用已有查询级重写/数组研究，未扩大 task-008 |
| 0276 派生表缺别名 | 新生成SQL已越过序列表语法；现在暴露独立的未命名派生表问题，记录到查询级兼容研究，需核对命名与作用域后立规则；未在本轮顺便修 |
| 0293/0294/0295/0296/0299 自定义聚合 | 外部 UDF/聚合迁移范围，不绑定任意同名函数到SQLGlot核心 |
| 0398/0413/0427/0428 WITHIN GROUP | 保留有序/假想集合实现研究，不以序列修好宣称整条成功 |

全批9项当前：5项完成约定验收（002/004/005/006/007）、3项已修改未验收（001/003/008）、1项未处理（009）。本轮没有新增或重新打开其他task。当前优先是补齐 task-008 的NULL范围；task-009仍为下一项独立能力，必须由用户授权后开始。

**整份输入未完成。** 尚有未验收和未处理task、前提/研究范围、导入遗漏，且未在最终状态回归全部313条/43阶段。没有以某条MATCH、代码保存或当前130条无匹配回归代替整份完成条件。

