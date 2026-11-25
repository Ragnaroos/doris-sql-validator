# aggregates-001 / fix-012：task-001 数组源元素类型保留

## 1. 本轮结果

这轮继续 task-001，并实际实现了有限源类型保留，不是再次只审计。默认 SQLGlot 链路现在会为可确定的PG数组类型生成整体 CAST：小整数为ARRAY<INT>，INT64字面量为ARRAY<BIGINT>，全NULL/纯字符串为ARRAY<STRING>。未知列、Decimal/超INT64数值和混合字符串输入转换不猜类型。

| 范围 | 实际结果 |
| :--- | :--- |
| task-001 前轮18条边界 | 18条状态/当前值一致，双端重复稳定；上轮7条默认类型差异已修正；当前16条全部已取得字段类型/约束可对齐，另1条独立id位宽、1条Decimal结果约束保留 |
| 新增19条边界 | 19条两端成功并重复稳定；17条现有结构化值比较一致；2条保留Boolean显示和混合字符串/整数真差异，详见任务报告 |
| task-001 原14条查询 | 原.out规则仍为3匹配、1显示差异、9Doris失败、1转译拒绝；0010数组元素类型已由VARCHAR(5)改为TEXT，但不是整条.out MATCH |
| 源证据补查 | 14条当前PG成功结果的文本投影均与原.out相同；不替换基线，不由文本投影证明原生类型/顺序 |
| 固定原查询回归 | 142条、19阶段：82匹配、36 Doris执行失败、19值/顺序不同、1转译失败、4源端负向；逐ID对比fix-011，0条结果改变，82个原匹配均保持 |
| 代码检查 | 全部方言1081方法通过；另core四模块199方法、tokens/build/schema/lineage四模块79方法通过；ruff与diff检查通过 |

本轮只纳入1项任务：**已修改但未完成验收1项**，其余状态0。全批仍为7项完成约定验收、2项已修改未验收；没有新增task、重新打开已完成task或自动实施task-003。代码改善不能用.out匹配率体现时，明确记录类型事实，不制造百分比提升。

## 2. 任务导航与修改边界

| 任务 | 本轮报告 | 当前状态 | 独立行为边界 |
| :--- | :--- | :--- | :--- |
| task-001 Doris数组构造 | [task-001.md](tasks/aggregates-001/fix-012/task-001.md) | 已修改但未完成验收 | PG Parser保留有限源元素类型 → Array AST.element_type → Doris CAST；必要公共Array生成和测试属于同一规则 |

原当前清单：[归因汇总 task-001](../attribution/aggregates-001-attribution-summary.md#task-001)；前轮：[fix-011](aggregates-001-fix-011-summary.md)。14份原Case文档追加本轮事实，没有复制归因文件或另建索引。

本轮仅修改SQLGlot实验checkout及测试和规定报告；不改验证框架、数据准备、源SQL/.out、YAML、Session政策或比较器。task-003、通用VALUES/CASE/SUM类型、索引偏移、时间精度和UDF等未实施。源端负向保持单列，不以两边报错算匹配。

## 3. 代码、环境与运行方式

| 项目 | 实际身份/状态 |
| :--- | :--- |
| SQLGlot checkout / branch | ../sqlglot-experiment / codex/doris-array-literal |
| 起止 HEAD | 089891f2521780e2c5b243005017af9db62f25a6，未更新基线 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git |
| 起始累积未提交diff SHA256 | 444fdb8de935a0b8bea12534309b9fecf894246a2fe531d0d0e0a4b1ab48cf18 |
| 当前累积未提交diff SHA256 | 309f2694a0a1ed3760b346c4dbd4d1b02da43c9b55830163c0f036b738b8e675；包含前轮修改，不是本轮独立补丁 |
| 原有修改保护 | 进入本轮前6个修改文件；本轮共同涉及其中PG Parser、Doris Generator和两个测试，新增Array AST和公共Generator修改，合计8个dirty文件。此前aggregate.py、parsers/doris.py等修改保留 |
| 验证解释器 | ../doris-sql-validator/.venv/bin/python，Python3.12.15；PYTHONDONTWRITEBYTECODE=1、PYTHONPATH=../sqlglot-experiment:src |
| 实际import | ../sqlglot-experiment/sqlglot/__init__.py；30.25.1.dev355 |
| PostgreSQL | 18.1，127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | SHOW FRONTENDS实际doris-4.1.3-rc02-7126cf65d96、Alive=true；127.0.0.1:9030，UTC、strict_cast=false |
| 实测日期/身份复核 | 2026-11-24，Asia/Shanghai；共同检查时间11:55:50、11:58:52；不将这些时间冒充全部查询的起止计时 |
| 保存/发布 | 无commit/push，无Issue/PR；普通修复授权不自动扩大为推送授权 |
| 社区原checkout | ../sqlglot的tracked文件仍干净，HEAD feb0e08aba28a29590596bb3f5761fbaeb0e98b9；未动未跟踪DORIS_TRANSPILATION.md |

原材料及固定阶段继续引用 [数据准备报告](../data-preparation/aggregates-001-data-preparation.md)及同前缀postgres-setup.sql、doris-setup.sql；原SQL/.out位于../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql及aggregates.out，未复制。YAML为reports/data-preparation/aggregates-001-stage-XX-cases.yaml；首轮JSON为reports/validation/aggregates-001-stage-XX-validation.json。只读执行，不重建/重装数据，不新增.out指纹检查。

同一Python进程按阶段通过 CliRunner().invoke(app, ['run','--path',<原YAML>,'--stdout','--id',<ID>,...]) 批量重跑；边界和实时类型通过默认转译及pg_probe.execute_query/compare_probe，10秒、10000行上限。全部事实留在内存/终端，必要SQL、字段、错误和反例写进同一任务Markdown，不另建执行JSON、evidence、候选、日志或patch。

## 4. 测试与原查询回归

SQLGlot工作目录../sqlglot-experiment，命令解释器为其.venv/bin/python，PATH含.venv/bin：

| 实际命令 | 结果 |
| :--- | :--- |
| python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.dialects.test_mysql | 158方法通过，含两个新增方法；属于下行1081范围，不相加 |
| python -m unittest discover -s tests/dialects -p 'test_*.py' | 1081方法通过；最终代码已重跑 |
| python -m unittest tests.test_expressions tests.test_parser tests.test_transpile tests.test_generator | 199方法通过 |
| python -m unittest tests.test_tokens tests.test_build tests.test_schema tests.test_lineage | 79方法通过 |
| ruff check / ruff format --check 本轮6个代码/测试文件 | 通过 |
| git diff --check | 通过 |
| make check、C扩展、完整optimizer套件及mypy | 未执行；duckdb、mypy不可用，未升级/安装依赖，不标通过 |

142条原查询分阶段范围与fix-011相同：01:50、03:8、06:1、07:6、08:1、09:8、10:2、11:1、15:3、17:15、25:6、30:3、31:25、32:1、33:3、40:1、41:1、42:3、43:4。未执行有过后端风险的301/303/304；未宣称跑完全部313条或最终43阶段验收。退出1的阶段仍产生有效终端JSON，按逐查询结果读取，不把CLI退出码作为类型验收。

## 5. 剩余问题与后续入口

| 事项 | 已取得证据 | 去向 |
| :--- | :--- | :--- |
| 混合unknown字符串与整数 | ARRAY['1',2] 源INT32元素[1,2]，当前目标TEXT元素["1","2"] | 继续原task-001的输入共同类型/转换子项，研究安全规则；不把统一CAST当全域修复 |
| Decimal/超INT64 NUMERIC | 当前值可以相同，但无约束NUMERIC与固定Decimal/LARGEINT契约不能直接判等 | 继续原task-001类型余项；区分结果typmod、输入CAST和目标可表示域 |
| 未知列与参数 | 不加猜测类型，部分样本由原显式CAST自然得到正确INT，未证明一般类型传播 | 原类型研究继续；不偷改task-003或强制Schema |
| 其他原完整Case失败 | WITHIN GROUP、VARIADIC、RWAGG及SUM/CASE类型等仍保留 | 沿原独立问题/研究处理，不混入数组构造补丁 |
| Boolean数组展示 | 原生BOOL/BOOLEAN一致，现有工具仍报[true,false,null] / [1,0,null]不同 | 既有Adapter/表示研究，本轮不修改比较器 |

**整份输入未完成。** 未满足项包括task-001/003的剩余验收、其他待研究/前提事项及最终完整43阶段回归。下一轮建议继续task-001的混合输入和NUMERIC安全范围；不自动实施，沿本轮checkout和原批次材料恢复。代码保存状态与任务完成状态分开，未用一次样本匹配声称所有输入同义。

