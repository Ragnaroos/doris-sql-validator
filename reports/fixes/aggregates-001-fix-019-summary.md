# aggregates-001 / fix-019：NUMERIC 数组类型与转换

## 1. 本轮范围与状态

按用户要求持续处理原task-001的已知类型/转换余项；fix按修复范围组织，commit按独立功能拆分。只修改既有SQLGlot checkout及测试，允许本地commit，不push、不建Issue/PR、不改原SQL/.out、YAML、数据、Session政策或框架比较器。

本轮在同一次调用中连续完成五个独立功能提交：固定精度数组CAST、先保留元素CAST、数组内NUMERIC取负、NUMERIC/unknown字符串共同输入、有限无约束NUMERIC数组CAST。最终固定版本回归已完成；task-001状态为“已修改但未完成验收”，整个输入未完成，不因五项功能提交而关闭任务。

## 2. 代码、输入和环境

- checkout：../sqlglot-functional-commits；分支codex/doris-functional-commits；fork https://github.com/Ragnaroos/sqlglot.git。
- 起点：3c9e4bb004bff47a4ca8b750961f5e4470076590；本轮当前HEAD：d0c2e9ea1e187edc157f96657313982ce7929e09。原checkout干净，旧sqlglot-experiment用户修改保留。
- 统一任务清单：[归因汇总](../attribution/aggregates-001-attribution-summary.md#task-001)。14条原查询来自清单既有链接，313条/43阶段来自既有reports/data-preparation/aggregates-001-stage-XX-cases.yaml；原输入/准备材料不变。
- 原报告：reports/validation/对应阶段JSON，不覆盖。回归run --stdout，不另存JSON；新56条边界仅完整列在任务Markdown中。
- PG18.1/Doris4.1.3-rc02、原冻结阶段库、UTC、原比较策略不变；不重放此前BE崩溃的嵌套聚合lambda，不执行已知风险0301/0303/0304。
- 单测和数据库解释器、API、逐条源SQL/代表生成SQL/类型限制均见[task-001本轮报告](tasks/aggregates-001/fix-019/task-001.md)。只生成本汇总和逐task报告两类，不增加候选、证据目录、脚本、执行日志或patch。

## 3. 功能提交与任务导航

本轮只继续原task-001，不以每个commit新建task，不实施task-003/010或其他独立任务。五项真实完整SHA、父commit及对应行为见[任务报告第2节](tasks/aggregates-001/fix-019/task-001.md#2-功能拆分与真实提交)。全部本地保存，未push；本轮原始14条的完整查询结果与构造规则验收分开统计。

## 4. 最终回归

| 范围/维度 | 实际结果 |
| :--- | :--- |
| 新增56条边界/控制，双端成功、别名、值/Scale、NULL、数组位置/重复与必要顺序 | 56条通过，双端重复稳定；相对起点26条值/Scale/表示不同、7条执行失败、1条转译失败已消除，22条原本正确 |
| 数组声明约束 | 28条固定precision/scale与目标对应；另28条PG无固定typmod，值相同也不宣称全类型域等价 |
| 旧75条边界 | 62条构造/控制原生值/Scale相同；13条既有下标错误保留task-010；75条重复稳定。与新56条有重叠，不相加成唯一查询数 |
| 原task-001关联14条 | 3匹配、6行值/显示不同、4目标执行失败、1转译失败，与fix-018相同；本轮没有新增原输入MATCH |
| 原313条生成层对照 | 起点/最终逐ID生成SQL或严格错误均不变 |
| 原43阶段、310条安全查询 | 82匹配、25源端负向、69行值/顺序不同、114目标执行失败、12框架环境标签、8转译失败；3条既有BE风险未执行 |
| 自动测试 | 最终功能提交前相同代码1103项方言测试通过；提交后314项定向/核心通过，集合重叠不相加 |
| 代码质量/隔离 | Ruff检查和格式通过、git diff --check通过、SQLGlot工作区干净；旧experiment修改指纹保持，社区checkout未改 |

原范围成功源分母285，82/285=28.77%，与fix-018相同。新边界修复不放入原输入分母；源端负向默认不进入主修复清单。mypy当前未安装，C扩展、完整optimizer/integration及make check未执行，不宣称全部项目测试通过。逐条源SQL、真实执行方法、失败尝试与具体限制见[任务报告第4至8节](tasks/aggregates-001/fix-019/task-001.md#6-最终head的实际核验)。

## 5. 整份输入状态

整份输入未完成，当前13项task仍为10项完成各自约定验收、2项（001/003）已修改未完整验收、1项（010）未实施。本轮只处理task-001，新增/复用/重新打开任务数量分别为0/1/0，没有把每个commit拆成新task。

原输入余项与本轮具体阻断分开：

- **运行时未知文本直接REAL**：最终HEAD重测两条四行反例，Doris内部与PG二进制精确结果的等值标志均为0；此前40个候选没有找到安全通用入口。需要可验证的直接FLOAT32运行时解析/算法，不能改用先DOUBLE再REAL冒充；若要修改Doris/加UDF/改变输入前提，须另获授权。
- **一般NUMERIC**：PG混合Scale转换TEXT为`1.25`和`2`，目标固定Scale为`1.25`和`2.00`；77位DECIMAL被目标拒绝，NUMERIC NaN在目标控制中变NULL。固定域的有限正确转换已经补齐，不能称覆盖源无约束类型域；这也不证明任何未来SQL算法都不可行。
- **独立问题**：原VARIADIC/UDF、ARRAY子查询、task-010下标和task-003聚合类型不自动混进本次数组构造修复。原14条不是全部完整匹配。

本轮没有每做一小项就停；五项实现、功能commit、旧边界和固定原输入最终回归在同一次调用内完成。其他已知余项尚无经验证、在当前权限内可安全交付的通用实现，保留真实反例及恢复条件，不无限重试、不强行改答案/比较器，也不把任务标完成。下一次继续时从任务报告第8节和统一清单读取当前余项，不重新修已通过的有限转换。

最终本地分支累积29个功能提交，本轮5个，全部未push。Doris只读查询成功、原阶段31 tenk1仍10000行；没有执行已知BE崩溃候选。workflow已有10份受控文件修改未覆盖，也未额外提交或推送workflow。
