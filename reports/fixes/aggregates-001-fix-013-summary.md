# aggregates-001 / fix-013：task-001 混合数组输入转换

## 1. 本轮结论

已实际修正前轮 `ARRAY['1',2]` 的元素值/类型差异；补齐可确定源类型的整数文本和Boolean文本转换，并尊重显式数组CAST对unknown元素的类型约束。unknown在这里指尚待上下文定型的PG字符串字面量，不是未知列类型。不是只加一个外层CAST：先按PG文法规范化输入，再在ARRAY构造前转换元素。

task-001仍为**已修改但未完成验收**：Float混合输入、未知列/一般表达式和NUMERIC契约仍有余项。本轮只继续task-001，不顺带实施task-003或修改验证器。全批仍7项完成约定验收、2项已修改未验收，整份输入未完成。

| 范围 | 实际结果 |
| :--- | :--- |
| 成功源边界97条 | 前轮37 + 新混合整数24 + 新Boolean22 + 上下文6 + 外层显式CAST8；双端均成功、每端重复一次均稳定 |
| 97条的现有结构化值比较 | 74一致、23个Boolean显示不同；22条新增Boolean另以原生字段投影核对类型/元素值一致，原比较不同仍保留 |
| 前轮37条 | 36值一致、1个Boolean显示不同；原36号真实混合整数差异已修正，其他值比较结论保持 |
| 非法输入边界21条 | PG全部实际报错；RAISE生成全部明确unsupported，不运行Doris；默认排除，不算成功匹配 |
| NUMERIC/Float研究15组 | 15条源成功；9当前值相同、5不同、1源合法但Parser拒绝。包含与边界重复的SQL，不相加为唯一查询数 |
| 原14条关联Case | 原.out仍3匹配、1显示差异、9 Doris执行失败、1转译拒绝；当前PG文本均与原.out相同 |
| 固定原回归142条/19阶段 | 82匹配、36 Doris执行失败、19值/顺序不同、1转译失败、4源端负向；与fix-012逐ID结果完全相同，未引入新的结果回归 |

本轮1项任务的互斥当前状态：已修改但未完成验收1，其余0；没有新增task编号、重新打开已完成任务或将负向用例纳入主修复清单。边界与补查不改首轮313条的分母，也不是原.sql全部可能输入的等价证明。

## 2. 任务入口与代码边界

| 任务 | 报告 | 实际行为变化 | 提交状态 |
| :--- | :--- | :--- | :--- |
| task-001 数组构造/源元素类型 | [task-001.md](tasks/aggregates-001/fix-013/task-001.md) | PG有限共同类型 → 整数/Boolean输入规范化及元素CAST → 源显式数组CAST上下文；含原辅助推型空类型防崩溃与测试 | 未commit/push，无Issue/PR |

唯一当前清单：[归因汇总](../attribution/aggregates-001-attribution-summary.md#task-001)；前轮：[fix-012](aggregates-001-fix-012-summary.md)。14份原Case追加本轮事实，不复制原输入或新增归因/交接索引。

本轮涉及sqlglot/generators/doris.py、sqlglot/parsers/postgres.py、tests/dialects/test_doris.py、tests/dialects/test_postgres.py。行为依赖fix-012的element_type基础；提交时不能把包含其他task的累积dirty文件整体混成一个commit。本轮未获得commit/push授权，不向任何远程发布。

## 3. 共同身份、输入与执行

| 项目 | 实际值 |
| :--- | :--- |
| 实验checkout / 分支 | ../sqlglot-experiment / codex/doris-array-literal |
| 起止HEAD | 089891f2521780e2c5b243005017af9db62f25a6，未拉取/切换基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 起始累积diff SHA256 | 309f2694a0a1ed3760b346c4dbd4d1b02da43c9b55830163c0f036b738b8e675 |
| 当前累积diff SHA256 | b3737ff1ad9a7fafc5c43675efb645a334ccc5795b32c6285de5045f00a1ad55；含前轮修改，不是本轮独立补丁 |
| 保护既有修改 | 原有8个dirty文件仍保留；本轮只在其中4个文件修改相应规则/测试，没有reset或覆盖其他任务 |
| 验证解释器/import | ../doris-sql-validator/.venv/bin/python，Python3.12.15；PYTHONPATH=../sqlglot-experiment:src；实际sqlglot.__file__为../sqlglot-experiment/sqlglot/__init__.py，30.25.1.dev355 |
| PostgreSQL | 18.1；127.0.0.1:5432，UTC、ISO/MDY、extra_float_digits=0 |
| Doris | SHOW FRONTENDS实际doris-4.1.3-rc02-7126cf65d96、Alive=true；127.0.0.1:9030，UTC、strict_cast=false |
| Decimal实际配置补查 | enable_decimal256=false；NUMERIC(39,0)当前值1仍成功，不据文档上限改写执行事实，完整39位值域未验收 |
| 日期/共同检查 | 2026-11-24（Asia/Shanghai），共同身份检查12:18:13；不创建计时工具或伪造整批起止耗时 |
| 社区原checkout | ../sqlglot的tracked文件仍干净，HEAD feb0e08aba28a29590596bb3f5761fbaeb0e98b9；未动未跟踪DORIS_TRANSPILATION.md |

沿用[准备报告](../data-preparation/aggregates-001-data-preparation.md)和同前缀postgres-setup.sql、doris-setup.sql。原SQL/.out继续引用../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql及aggregates.out。阶段YAML为reports/data-preparation/aggregates-001-stage-XX-cases.yaml，首轮JSON为reports/validation/aggregates-001-stage-XX-validation.json，均不修改、不复制、不校验.out指纹。

同一Python进程按实际stage通过CliRunner调用run --path <原YAML> --stdout，同一stage重复--id一次运行选定Case。原Case使用SqlglotTranspiler.transpile_case；新增边界使用parse_one(...,read='postgres').sql('doris',unsupported_level=RAISE)。实际生成目标再交pg_probe.execute_query/compare_probe，10秒、10000行上限。97条在最终逻辑代码下完整重跑，材料和统计复用但不缓存数据库结果。工具事实写进同一任务Markdown，不另存执行JSON/候选/日志/evidence。

## 4. 测试与回归

SQLGlot测试工作目录../sqlglot-experiment，解释器.venv/bin/python，PATH包含.venv/bin：

| 实际命令 | 结果 |
| :--- | :--- |
| python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.dialects.test_mysql | 159方法通过；含新增test_postgres_array_unknown_inputs |
| python -m unittest 上述3个方言模块及 tests.test_expressions tests.test_parser tests.test_transpile tests.test_generator tests.test_tokens tests.test_build tests.test_schema tests.test_lineage | 437方法通过；与上行159有包含关系，不能相加 |
| python -m unittest discover -s tests/dialects -p 'test_*.py' | 1082方法通过；包含前述159，不相加 |
| ruff check、ruff format --check 本轮4个代码/测试文件；git diff --check | 通过 |
| 完整optimizer测试、mypy、C扩展及make check | 未执行；duckdb/mypy不可用，没有安装/升级依赖，不标通过 |

142条阶段范围与fix-012一致：01:50、03:8、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:15、25:6、30:3、31:25、32:1、33:3、40:1、41:1、42:3、43:4。每条原Case结果逐ID核对，无结果改变；不将退出1当整组执行失败。未运行有后端风险记录的301/303/304，未声称执行全313条/43阶段最终验收。

## 5. 已明确的余项与下一步

| 事项 | 实际证据 | 去向 |
| :--- | :--- | :--- |
| unknown字符串 + 已知整数/Boolean | 有限输入文法、极值、NULL/重复、显式类型/嵌套和原生元素补证已完成 | 本轮规则实现；数组Boolean原比较不同仍保留 |
| unknown字符串 + Float | ARRAY[1::REAL,'1e2'] 源[1,100]，目标TEXT ["1","1e2"] | 继续task-001输入转换子项，需补查浮点范围/输入语法，不照整数规则猜 |
| NUMERIC特值/大数 | NaN、±Infinity、1e40当前目标均NULL；有限Decimal精度不能覆盖PG NUMERIC全域 | 现有通用NUMERIC类型研究继续，区分可安全修复与目标表示/精度限制 |
| NUMERIC负Scale | PG成功，当前Parser拒绝合法NUMERIC(3,-1)；本轮仅修辅助推型的AttributeError，不是实现负Scale | 沿已有通用类型研究，不能当源负向或未执行就结案 |
| 未知列/一般表达式 | 没有可信类型时保留原路径，不强制Schema | 继续可信推型研究，不混入task-003/VALUES实现 |
| 完整原Case其他余项 | WITHIN GROUP、VARIADIC、RWAGG、SUM/CASE等仍保留 | 原独立任务/研究，不混成数组构造补丁 |

**整份输入未完成。** task-001/003及既有研究尚未全部验收，未完成最终43阶段全量回归。本轮没有声称所有PG SELECT或全部输入同义。下一轮建议继续task-001的已知Float与unknown文本转换，再细分NUMERIC的可修复范围及目标能力限制；只给出入口，不自动实施未选任务或改变数据/比较规则。

