# aggregates-001 / fix-014：task-001 有限浮点文本转换

代码保存更新（2026-11-24）：本文件记录fix-014当时的未提交实施状态。之后既有代码已在独立checkout按功能重建为12个本地commit，当前HEAD为`51bf6a4085c5036a236f0ebfa5a720cab5dfb019`，未push；后续使用`../sqlglot-functional-commits`。完整对应关系、最终内容核对和只读回归见[归因汇总](../attribution/aggregates-001-attribution-summary.md#functional-commit-recovery)。task-001/003仍未完成验收，不把提交重建当作新功能修复或整批完成。

## 1. 本轮结论

已先在[归因汇总](../attribution/aggregates-001-attribution-summary.md#task-001)补写现有修复状态、下一轮的具体反例/规则/范围/验收，再继续task-001，实现“unknown十进制文本 + 可信REAL/DOUBLE类型”的有限转换。不再让`ARRAY[1::REAL,'1e2']`变成TEXT数组；REAL舍入中点通过精确输入规范化及ARRAY_MAP运行时转换保留。

**task-001仍为已修改但未完成验收。** 两条已知REAL元素CAST控制仍有真实值差异，已在同一task下补写下一轮的具体修复方案；特殊/十六进制Float输入、NUMERIC和未知类型余项未关闭。全批仍7项完成约定验收、2项已修改未验收，整份输入未完成。

| 范围 | 实际结果 |
| :--- | :--- |
| 本轮41条成功源边界 | PG二进制源查询/Doris生成查询都成功；全部逐元素原生等值/NULL核验为真，字段/已取得类型、行数/位置与重复执行通过 |
| 这41条原比较器结论 | 25值一致、15显示不同、1最大DOUBLE源文本解码失败；原不同和失败保留，不称41条MATCH |
| 直接相关20条限制输入 | 12源负向默认排除；8源成功但RAISE生成unsupported（NaN/±Infinity/十六进制），能力仍未完成 |
| 额外2条已知REAL元素CAST控制 | 原生第二元素均不等；一次定位证据，不冒称已修复或已做完整边界 |
| 前轮97条边界回归 | 74值一致、23Boolean显示不同保持；双端各重复一次稳定 |
| 原142条/19阶段固定回归 | 82匹配、36 Doris执行失败、19值/顺序差异、1转译失败、4源负向；逐ID与fix-013相同 |
| task-001原14条 | 原.out仍3匹配、1显示差异、9目标执行失败、1转译拒绝；实时源TEXT投影全部对上原.out |

本轮实际纳入1项task：已修改但未完成验收1，其余状态0。没有新增或重新打开任务，不把源负向、重试/取证调用或文件数量加成任务数/原输入分母。

## 2. 任务报告与实现边界

| 任务 | 本轮实际变化 | 报告 | 保存状态 |
| :--- | :--- | :--- | :--- |
| task-001 数组构造/源元素类型 | Parser有限FLOAT/DOUBLE共同类型；十进制文本精确舍入；REAL运行时转换；显式/嵌套CAST上下文与测试 | [task-001.md](tasks/aggregates-001/fix-014/task-001.md) | 未commit/push，无Issue/PR |

本轮只修改sqlglot/parsers/postgres.py、sqlglot/generators/doris.py、tests/dialects/test_doris.py、tests/dialects/test_postgres.py；复用fix-012/013的类型提示与输入转换基础。累积dirty文件还有其他任务代码，不能将整份文件差异作为一个独立commit。社区checkout未改；本轮也不修改task-003、验证器、比较器、数据或Session政策。

## 3. 共同版本、输入与执行

| 项目 | 实际值 |
| :--- | :--- |
| 实验checkout / 分支 | ../sqlglot-experiment / codex/doris-array-literal |
| 起止HEAD | 089891f2521780e2c5b243005017af9db62f25a6；未刷新或切换上游基线 |
| 起始累积diff SHA256 | b3737ff1ad9a7fafc5c43675efb645a334ccc5795b32c6285de5045f00a1ad55 |
| 最终累积diff SHA256 | 32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73 |
| 已有修改 | 8个dirty文件保留，本轮只动其中4文件；累积1588增加/22删除，本轮净增加161行，不是独立补丁文件 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 实际运行解释器/import | ../doris-sql-validator/.venv/bin/python；Python3.12.15；PYTHONPATH=../sqlglot-experiment:src；sqlglot.__file__为../sqlglot-experiment/sqlglot/__init__.py；30.25.1.dev355 |
| PostgreSQL | 沿用18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0；精度补证另外使用同原SQL的只读二进制游标，不换主流程Session |
| Doris | 本轮SHOW FRONTENDS：doris-4.1.3-rc02-7126cf65d96，Alive=true；127.0.0.1:9030，沿用UTC/strict_cast=false |
| 数据阶段 | 原dsv_wf_agg001_s01–s43对应库；新增常量/运行时边界只用stage-01；单次10秒/10000行 |
| 日期 | 2026-11-24，Asia/Shanghai；没有建立可复用计时机制或另存执行日志 |
| 社区checkout | ../sqlglot，tracked干净；HEAD feb0e08aba28a29590596bb3f5761fbaeb0e98b9；未改未跟踪DORIS_TRANSPILATION.md |

沿用[准备报告](../data-preparation/aggregates-001-data-preparation.md)和同前缀postgres-setup.sql/doris-setup.sql。原SQL/.out继续在../doris-sql-validator/cases/postgres/manual/current/assets/，不复制/修改，不校验.out指纹。原stage YAML和首轮JSON仍在reports/data-preparation/及reports/validation/，本轮run --stdout不另存JSON。

通过CliRunner在同一Python进程按各实际stage调用run --path <原YAML> --stdout，同stage重复--id。原Case用SqlglotTranspiler.transpile_case；边界由parse_one(...,read='postgres').sql('doris',unsupported_level=RAISE)实际生成，再execute_query/compare_probe执行。41条最终代码完整重跑；旧97条同样双端重复。额外二进制/逐元素核验不替代原.out，不把Doris原生等值为真写成主比较器MATCH。

## 4. 测试与剩余问题

| 最终命令/范围 | 结果 |
| :--- | :--- |
| python -m unittest PG/Doris/MySQL及tests.test_expressions/test_parser/test_transpile/test_generator/test_tokens/test_build/test_schema/test_lineage | 438方法通过，24.480秒 |
| python -m unittest discover -s tests/dialects -p 'test_*.py' | 1083方法通过，4.759秒；与前项有包含关系，不相加 |
| ruff check、ruff format --check 本轮4文件；git diff --check | 通过 |
| 完整optimizer、mypy、C扩展及make check | 未运行；已有环境无duckdb/mypy，没有安装/升级依赖 |

固定142条范围与fix-013一致，详见任务报告。没有执行有后端风险记录的301/303/304，也未做全部313条/43阶段最终验收。原14条当前源TEXT投影均与.out相同，已取得类型差异仍保留。三条VARIADIC的额外安全Parser拦截与正常CLI中的真实Doris语法错误分别记录，不混为一种失败。

| 仍需处理 | 真实依据 | 当前去向 |
| :--- | :--- | :--- |
| 已知REAL元素CAST/共同类型的转换顺序 | `ARRAY['1e2','7.038531e-26'::REAL]`与`ARRAY['1e2',0.1::REAL,2::DOUBLE PRECISION]`均有原生元素差异 | **下一轮优先继续task-001**；修复范围/代码入口/反例/验收已写入归因汇总，不新增task |
| Float特殊/十六进制及长文本 | 8条源成功却unsupported；4096字符保护单测 | 能力未完成，继续补证，不当源负向或Doris永久限制 |
| 原比较器显示及最大DOUBLE文本解码 | 41条中15显示不同、1源驱动失败；二进制/原生核验另通过 | 框架/驱动观察保留，本轮不修改 |
| NUMERIC/负Scale、未知列/表达式、task-003类型 | 前轮具体事实仍有效，本轮未实施 | 既有task/研究，不混成一个大补丁 |
| 完整原Case的WITHIN GROUP/VARIADIC/UDF等 | 原14条/.out结果保持 | 独立问题不关闭 |

## 5. 下一轮与整份输入完成检查

下一轮方案已在[原task-001条目](../attribution/aggregates-001-attribution-summary.md#task-001)更新：先保留已知REAL元素的源转换精度，再参与共同类型；优先复现两条控制，核对内层CAST/外层数组CAST/标量子查询边界，再确定安全实现。验收包括REAL/DOUBLE混合、舍入中点/次正规值、NULL/重复、AST不变性和本轮/历史/固定原回归。源SQL和生成SQL不能由人工候选代替；若需扩大到通用CAST或框架修改，先请求授权。

**整份输入未完成。** task-001/003仍未全部验收，特殊输入/NUMERIC等可修复性仍需调查，也未在最终代码上完成43阶段全量回归。不把本轮有限规则通过当作整个task或全部PostgreSQL SELECT等价。无commit/push；继续时检查fix-015路径未占用，沿用原task编号，不另建交接/索引/evidence/候选/执行JSON。

