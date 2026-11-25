# aggregates-001 / fix-009：完成 task-008 的 NULL 参数处理

## 1. 本轮结论

**task-008 已修复并完成常量 INT4/NULL 表序列的约定验收；整份输入未完成。** 本轮继续同一 task，补齐 [fix-008](aggregates-001-fix-008-summary.md) 留下的 NULL 参数缺口，不重写前轮报告。fix-009 是执行轮次，不是 task-009；没有实施 REGR_COUNT。

| 检查范围 | 实际结论 |
| :--- | :--- |
| NULL 输入 | 起点、终点或步长为 NULL，返回带原列名/INT 类型的零行结果；NULL 与零步长共存同样正确 |
| 新增58条有限变体 | 48条使用 NULL 运行时展开，10条非NULL对照；全部双端通过，包括字段名称/类型、行数、值及重复次数、必要顺序，并复跑稳定 |
| 前轮65条边界 | 同一最终代码下全部双端通过；合计123条，不把重复执行算新用例 |
| 原130条相关查询，16阶段 | 80匹配、28 Doris执行失败、17行值/顺序不同、1转译失败、4源端负向；80个既有匹配全部保持 |
| 原task-008关联32条 | 8匹配、3值差异、20 Doris失败、1转译失败；31条可生成SQL与fix-008逐字相同，另1条仍为ARRAY子查询不支持 |
| 非NULL零步长 | 两条源控制均为SQLSTATE 22023；转换明确拒绝，不伪造成功，也不要求复制错误全文 |
| 单元测试 | PG/Doris/MySQL154、全部方言1077、核心233个方法通过；154包含于1077，不相加 |

实现、全部新增变体的源 SQL/实际生成 SQL、类型和结果，以及32条原Case的当前观察见[任务报告](tasks/aggregates-001/fix-009/task-008.md)。完成的是序列表达式规则，不是让32条整条查询全部MATCH；统计类型、NaN/CORR、REGR_R2、自定义聚合、LATERAL/派生表、ARRAY子查询和WITHIN GROUP仍保留各自去向。

## 2. 授权、版本与环境

指定任务模式，只补齐task-008。修改 ../sqlglot-experiment 的 generators/doris.py 和 tests/dialects/test_doris.py；保留前八轮和用户已有修改。不改验证框架、原SQL/.out、YAML、首轮JSON、数据、DDL或Session政策，不装依赖、不启动其他Agent。本轮未commit/push、创建Issue/PR；代码只在本地实验checkout。

| 项目 | 实际值 |
| :--- | :--- |
| checkout / 分支 | ../sqlglot-experiment / codex/doris-array-literal |
| 起止HEAD | 089891f2521780e2c5b243005017af9db62f25a6，未切基线 |
| origin / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 起始累积git diff --binary SHA256 | cdb5d8222785933bb0d3f1d7a40a13a9da077032fb07157ddd559d575a19ce68 |
| 最终累积git diff --binary SHA256 | 2ecc6f54c7579f9968914f9fa850050140fcdbd734d4c740ec8ffd831941c41f，包含保留的前轮修改，不是一个混合提交计划 |
| 本轮代码归属 | 仅Doris序列生成与对应测试，净增110行；其他四个累积修改文件不变。与前轮task-008同一行为的补齐，无必须依赖其他task规则 |
| 实际解释器 / import | ../doris-sql-validator/.venv/bin/python；PYTHONPATH=../sqlglot-experiment:src；../sqlglot-experiment/sqlglot/__init__.py；版本30.25.1.dev355 |
| PostgreSQL | 本轮实测18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | SHOW FRONTENDS本轮实查doris-4.1.3-rc02-7126cf65d96、Alive=true，127.0.0.1:9030；UTC、enable_strict_cast=false。兼容VERSION()不作为产品版本 |
| 时间 | NULL/整数边界批次完成 2026-11-23T11:00:58.156357+00:00；原查询回归完成 2026-11-23T11:02:13.364770+00:00 |
| 数据状态 | 新边界为常量，使用双端dsv_wf_agg001_s01；原查询严格按实际阶段库，不重建装数 |

遵循目标AGENTS.md/CONTRIBUTING.md、pg-doris-fix、修复模板与POSTGRES_MANUAL_WORKFLOW.md。没有修改Skill或通用工作流文档；它们已有的未提交修改保留。

## 3. 实现与固定输入

非NULL整数字面量继续用原NUMBERS长度公式、CAST AS INT和别名规则。本轮增加可空常量路径：一行种子 + 非OUTER EXPLODE_NUMBERS，SQL CASE先判三个参数IS NULL，命中时长度为0，再处理方向与步长。常量类型检查使用不依赖Schema的类型推断，原参数不被COALESCE替换；NULL语义在运行时SQL中实现，不按Python识别字面量NULL返回固定答案。

没有启用动态长度、相关列、用户参数或任意函数表达式。范围仍为INT4/NULL常量及INT CAST；BIGINT/Decimal/时间输入不因值为NULL而降成INT。大INT4纯整数范围仍走NUMBERS，只做生成测试，不执行数十亿行。NULL与另一端INT4极值的变体已实际零行通过，不生成大数组。

| task | 当前状态 | 保存 / 提交边界 |
| :--- | :--- | :--- |
| [task-008](tasks/aggregates-001/fix-009/task-008.md) | 已修复并完成约定验收 | 同一序列表达式契约的NULL补齐及测试；未commit/push，不与其他规则混提交 |

原输入仍为 ../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql/.out，SQL SHA256为9943917f6e4bb149cb89ad834997343370a0a7e6324ffe6723404b9cd60d0a62。保持原 .out 作为框架参考，不核验或保存 .out 指纹。原[准备报告](../data-preparation/aggregates-001-data-preparation.md)及双端setup.sql不变；历史540次基表核验不冒称本轮又执行。

| 本轮只读的主任务输入 / 首轮报告 | SHA256 |
| :--- | :--- |
| [aggregates-001-stage-01-cases.yaml](../data-preparation/aggregates-001-stage-01-cases.yaml) | `cf04cd870b828d26d1d0846d0b5a5be0f38bc25c7c76d100e138f5b9de31d423` |
| [aggregates-001-stage-01-validation.json](../validation/aggregates-001-stage-01-validation.json) | `312e26743e1b476ee11278b66aed299ecd347aa741a193864dc5aa83048fe0b0` |
| [aggregates-001-stage-03-cases.yaml](../data-preparation/aggregates-001-stage-03-cases.yaml) | `6fd4dbbc9bbc3b49c3ecafeedbf6e041699714648ef1793f8e067c4c4f405c01` |
| [aggregates-001-stage-03-validation.json](../validation/aggregates-001-stage-03-validation.json) | `dceca6c2e3bdea8cd7cae7d7c96ab0045bb1f2f2d25238cde076dfbb2d2ec224` |
| [aggregates-001-stage-17-cases.yaml](../data-preparation/aggregates-001-stage-17-cases.yaml) | `c4452ebf80f01193510ef591c849dd551e05d2a42d48bb05fac5de0f6825abd2` |
| [aggregates-001-stage-17-validation.json](../validation/aggregates-001-stage-17-validation.json) | `a35f570ffe0e0f7779f27a82d9973e90966e80f3dafc78f86b3db99fd29ad389` |
| [aggregates-001-stage-31-cases.yaml](../data-preparation/aggregates-001-stage-31-cases.yaml) | `9d395b715af738b02b4c0f06bf0494a53fe081d052f972d705951d9461cd27f6` |
| [aggregates-001-stage-31-validation.json](../validation/aggregates-001-stage-31-validation.json) | `c0953af4ac2656d8f5ccd587d8a5f9c53e8648695a8064de7b8a8c27526cccc2` |

## 4. 测试、回归与剩余范围

先加测试时8个UnsupportedError复现缺口，最终四个序列定向方法通过。NULL网格、极值、别名/星号、LEFT/RIGHT JOIN、重复UNION ALL、聚合空输入、CTE、标量子查询和窗口都已在双端执行，并额外读真实字段名称补足通用工具对集合别名的限制。所有目标均由本轮SQLGlot从源SQL实际生成；没有用手写候选代替验收。123条边界无原 .out，是明确的新变体，不冒用历史参考。

| 实际命令，工作目录 ../sqlglot-experiment | 结果 |
| :--- | :--- |
| .venv/bin/python -m unittest 四个 test_integer_generate_series* 定向方法 | 4方法通过 |
| PATH="$PWD/.venv/bin:$PATH" .venv/bin/python -m unittest tests.dialects.test_postgres tests.dialects.test_doris tests.dialects.test_mysql | 154方法通过 |
| 同PATH/解释器：python -m unittest discover -s tests/dialects | 1077方法通过 |
| 同PATH/解释器：python -m unittest tests.test_parser tests.test_generator tests.test_transpile tests.test_expressions tests.test_serde tests.test_build tests.test_schema tests.test_tokens | 233方法通过 |
| Ruff check、format --check六个累积文件；git diff --check | 通过 |

未运行完整make check、C扩展、mypy或DuckDB executor/optimizer全套，未把缺依赖/未执行写通过。

原查询回归通过一个进程内逐阶段CliRunner调用run --path <原YAML> --stdout --id ...；不新建执行JSON。仍为fix-008的130个唯一Case，不额外纳入负向或改分母；阶段数量和匹配集合保持。32条原序列查询参数都是非NULL，因此本轮预期不增加其MATCH数；完成依据是NULL边界正确和原路径无回归，而不是人为提高通过率。

| 保留余项 | 归属及后续 |
| :--- | :--- |
| task-001/003类型/完整验收 | 仍为已修改未验收，不因task-008关闭而关闭 |
| task-009 REGR_COUNT | 仍未处理，建议下一独立任务；本轮没有开始 |
| 32条原查询的其他问题 | 保留fix-008与Case中的类型、NaN/统计、UDF、查询级、有序聚合研究，不混修 |
| 原 .out与当前PG的7条统计冲突 | 沿用fix-008事实；本轮没有重跑这些实时PG，不静默换基线 |
| 动态NULL参数、NULLIF等表达式、直接LATERAL/SRF | task-008约定范围外；明确unsupported，不声称全部PG集合返回函数已支持 |
| 全输入313条/43阶段、导入遗漏 | 本轮未全量重跑或修导入，保留整批未完成 |

## 5. 当前任务状态与下一步

本轮仅纳入1个task：1项已修复并完成约定验收，其余状态0项。全批9项当前为 **6项完成约定验收（002/004/005/006/007/008）、2项已修改未验收（001/003）、1项未处理（009）**。这是继续已有task的完成事件，没有新增task或改写首轮统计。

**所选task-008完成；整份输入未完成。** 尚有未验收/未处理task、待研究与前提问题、导入遗漏，以及最终全阶段回归未完成。下一独立任务建议task-009：REGR_COUNT成对非NULL计数，需要用户授权后开始。本轮未提交、未推送，未修改社区checkout。

