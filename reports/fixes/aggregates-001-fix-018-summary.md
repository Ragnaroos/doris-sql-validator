# aggregates-001 / fix-018：百分位数组转换修复

## 1. 当前结论

本轮处理0410、0411、0412、0413、0415五条原查询，**五条现已全部由修改后的SQLGlot生成可执行Doris SQL，实时PG/Doris数组元素、NULL、形状和已取得类型对应。** 不是仅提前拒绝，也不是用手写候选代替最终验收。原.out花括号数组与Doris方括号数组显示不同，框架仍判五条不匹配；未修改比较器或数据。有限规则验收不证明全部输入同义，整份输入仍未完成。

本轮纳入4项：task-001概率上下文子项，以及按实现机制拆出的task-011连续百分位、task-012离散百分位、task-013文本数组输入。后三项完成各自有限规则验收，task-001整体仍未完成。全批当前13项中10项完成约定验收、task-001/003两项已修改未完成、task-010未处理；关联Case可重叠，不能相加当查询数。没有修改源SQL/.out、YAML、数据、框架或比较器，没有push、Issue或PR。

## 2. 代码与输入

| 项目 | 实际情况 |
| :--- | :--- |
| checkout / 分支 | ../sqlglot-functional-commits / codex/doris-functional-commits |
| 起点 | 4dc65a35a7efa92551cb9fb00c2315fcb8ff659f |
| 本地修复commit | 本轮4个独立功能commit，依次见下表；本次获准恢复后新增3个 |
| 最终HEAD / tree | 3c9e4bb004bff47a4ca8b750961f5e4470076590 / 353567091d2e75c1728dff6ddeb7c20435eb4ff4 |
| 对本轮起点binary diff SHA256 | f8fdef42885ccca62ade08c287d04fa66cf0cfcc04aa22629f22c85d38061b73；4个文件371行增加 |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；本轮未刷新main或推送 |
| 保存状态 | 工作区干净；累积24个本地功能commit，均未push，不将本轮视为整个task-001关闭 |
| 原阶段 | reports/data-preparation/aggregates-001-stage-31-cases.yaml；双端dsv_wf_agg001_s31 |
| 原报告 | reports/validation/aggregates-001-stage-31-validation.json，保留首轮；本轮没有覆盖 |
| 原输入/准备材料 | 沿用[归因汇总输入](../attribution/aggregates-001-attribution-summary.md#inputs)和[准备报告](../data-preparation/aggregates-001-data-preparation.md)，未改或重新装数 |
| 解释器/导入 | 单测../sqlglot-experiment/.venv/bin/python；数据库../doris-sql-validator/.venv/bin/python，显式PYTHONPATH=../sqlglot-functional-commits:src；SQLGlot实际来自该checkout，不靠旧安装版本字符串识别源码 |

只生成本轮汇总和逐task报告两类，未增加候选文件、执行JSON、日志、patch或evidence目录。已有Case文档追加后续事实，首轮JSON不覆盖。

| task / 实际规则 | 本地commit（依赖顺序） | 报告及当前状态 |
| :--- | :--- | :--- |
| task-001：PG概率数组DOUBLE上下文 | 2aef92e0c755132bf2253a34280e99adf27f98d0，父为本轮起点 | [报告](tasks/aggregates-001/fix-018/task-001.md)；此子项完成，整个任务仍有REAL/NUMERIC等余项 |
| task-011：常量数组连续百分位 | fa20f2cf768dc09e887eb8cf7449f41f4b1eb548，父为2aef92e0c… | [报告](tasks/aggregates-001/fix-018/task-011.md)；完成有限规则验收 |
| task-012：常量数组精确离散百分位 | a499d04cf69a13d831f3943df89c15e60bfcd56c，父为fa20f2cf7… | [报告](tasks/aggregates-001/fix-018/task-012.md)；完成有限类型/排序前提下验收 |
| task-013：PG一维TEXT数组输入 | 3c9e4bb004bff47a4ca8b750961f5e4470076590，父为a499d04cf… | [报告](tasks/aggregates-001/fix-018/task-013.md)；完成array_nulls=on下有限语法验收 |

四项均按代码和测试独立本地提交，不创建PR、不推送；各任务实施前方案写在统一归因清单。没有实施task-010。

## 3. 已完成子项及尚未完成部分

PG18.1的pg_proc以及五条原文EXPLAIN均证明概率数组实际被转换为double precision[]。前轮直接套NUMERIC混合Scale保护漏掉了这个上下文。本轮PostgresParser._parse_window只对WITHIN GROUP百分位的有限直接数组构造记录DOUBLE类型，支持明确嵌套，不改普通NUMERIC数组、不覆盖内部显式数组CAST、不猜列Schema。6个函数/参数组合及排除控制纳入测试。

第一项commit时五条仍在WITHIN GROUP报missing 'BY' at '('，当时没有宣称完整转换修复。恢复后继续实现目标生成：CONT按常量概率展开精确PERCENTILE；DISC按DOUBLE概率排名取排序后原类型值，不使用连续/近似替代；0415的PG字符串数组输入由Parser通用解析为Array AST。后续这五条SQL不再含原函数的WITHIN GROUP，且全部实际执行成功。

早期PERCENTILE_ARRAY和lambda只是可行性候选，失败尝试保留在task-001。正式实现不用lambda，NULL概率/空组以运行时IF/COALESCE处理；多维、重复、ASC/DESC等证据见task-011/012。动态概率、FILTER/OVER、任意Collation、非有限数/高精度全域等并未声称支持，不能由五条推广到所有百分位。

## 4. 数据库中断、获准恢复与安全限制

2026-11-25 11:32:25（Asia/Shanghai），一条带双参数及嵌套lambda的只读候选执行期间连接中断。日志确认BE Segmentation fault、rc=139；all-in-one入口随后退出，容器doris为Exited(1)，OOMKilled=false，9030连接被拒绝。不是普通SQL解析错误，也不是数据结果不匹配。

中断时停止并请求授权；用户随后明确允许启动原容器。已执行docker start doris，容器healthy、SELECT 1成功、SHOW BACKENDS Alive=true，阶段31 tenk1仍10000行；最终回归后再次确认BE在线和行数保持。没有删除、重建或重新装数，不改变Session策略。禁止重放高风险候选及嵌套聚合lambda路径，原文只在task-001保留为事故证据。

## 5. 最终回归、限制与下一步

最终准确代码运行1097项全方言及308项PG/Doris加核心测试通过；ruff check、format --check和git diff --check通过。目录为SQLGlot checkout，解释器如上；全方言子进程PATH显式包含../sqlglot-experiment/.venv/bin。两集合重叠，不相加；没有运行mypy、C扩展或完整make check，也没有安装依赖。

命令分别为`python -m unittest discover -s tests/dialects -t .`及`python -m unittest tests.dialects.test_doris tests.dialects.test_postgres tests.test_expressions tests.test_parser tests.test_generator tests.test_serde tests.test_transpile`；python指上述实验venv，PYTHONDONTWRITEBYTECODE=1。新边界CONT 13条、DISC 16条、TEXT输入/UNNEST 12条，连同5条原文实际执行及必要重复、类型/顺序检查见任务报告；Decimal全域约束和特殊字符数组显示限制保留。没有重跑历轮所有独立任务边界，不冒称全量边界证明。

最终HEAD用CliRunner逐阶段调用原`run --path <stage YAML> --stdout --id ...`，43个阶段310条安全原查询取得报告；既有风险0301/0303/0304未执行。主参考仍是原.out，不另存JSON。最终统计：

| 原规则结果 | 数量 | 含义 |
| :--- | ---: | :--- |
| 匹配 | 82 | 可用显示证据匹配，不表示原生类型全域验收 |
| 源端负向 | 25 | 默认不列主修复范围 |
| 行值或顺序不同 | 69 | 含本次5条只见数组显示不同；其他差异不因此结案 |
| Doris执行失败 | 114 | 仍有其他函数/语法/类型问题 |
| Doris环境类问题 | 12 | 框架标签，须具体排查，不据此证明都是数据缺失 |
| SQLGlot转译失败 | 8 | 其他未支持语法/安全保护，不是本次五条 |
| 合计 | 310 | 另3条风险未执行；成功源分母285，82/285=28.77% |

与fix-017同范围统计相比，5条从转译失败变为成功执行但显示文本不同：转译失败13→8、值/顺序不同64→69，其他数量不变。额外在内存关闭本次恢复后withingroup/build_cast两个新入口、清理dispatch缓存作生成控制（不改文件、不冒称旧checkout执行），313条中只上述5条SQL/拒绝结果改变，其余308条相同。当前43阶段回归中原82条匹配保持，没有改变分母或放宽规则。

五条均为实时PG/Doris成功：0410 _int4→array<int>，0411/0413 _float8→array<double>，0412 _int4多维→array<array<int>>，0415 _text→array<text>；元素/NULL/形状一致且目标重复稳定。均单行且无最终ORDER BY；不比较无Alias的自动字段名。原.out为`{...}`或`{{...}}`，Doris为`[...]`或`[[...]]`，原报告仍是不匹配，不称5条MATCH。

另以PG `cursor(binary=True)`重读五条原文，避免extra_float_digits或数组显示截断隐藏精度差异；目标只对实际生成表达式加xs别名和逐位置原生读取包装，不改变表达式。共32个元素位置（含NULL）精确对应，PG和Doris各重复两次稳定；其中16个DOUBLE位置的Python float.hex()也逐一相同，例如0413的2.6两端均`0x1.4cccccccccccdp+1`、2.9均`0x1.7333333333333p+1`。目标元素协议分别为INT、DOUBLE、TEXT，与前述EXPLAIN类型相符。包装只是解码补证，不是替代生成SQL的手写候选，也不修改主比较器。

所选五条的有限执行转换已补齐，整份输入未完成。task-001直接REAL/一般NUMERIC、task-003类型等余项仍需继续，task-010尚未实施且本轮未获新授权。下一次以统一归因清单选择具体范围，不重放崩溃候选或重新装数。Skill促使恢复后继续完成独立规则并分别commit、保留真实文本比较结果，而不是以一次候选或提前拒绝结束。
