# aggregates-001 / fix-020：源语义规则与数组输入转换

## 1. 结论与范围

按更新后的pg-doris-fix继续task-001：先纠正源Parser受目标能力控制的问题，再实现由PG共同类型及数组输入语法决定的文本子数组转换。没有以aggregates.sql零报错为目标，也没有增加新的精度/取负文本或lambda补偿。两个独立行为已各自本地commit，未push/创建Issue/PR；整个task-001及整份输入仍未完成。

本轮复用1个task、没有新增/重新打开task；当前互斥状态为1项“已修改但未完成验收”。其中源类型职责和明确范围的一维文本子数组转换已验收，旧数值补偿的通用性及研究事项另列，不把它们混为一个“全部修好”。全批13项仍10项完成各自约定验收、001/003两项未完成、010未实施；首轮统计和历史报告不改写。

## 2. Skill调整及决策

使用skill-creator修改项目pg-doris-attribute/pg-doris-fix及修复报告模板，并同步docs/POSTGRES_MANUAL_WORKFLOW.md；两份Skill的quick_validate.py均通过。没有新增Skill、工作流步骤、交接或证据文件；未提交/推送workflow原有及本次文档修改。

新规则要求先说明源语义依据、可从SQL/可靠类型/明确配置判断的适用条件、目标能力和必要上下文验证。Parser只记录源事实，目标决定如何转换；有限值成功、零报错和commit数量不等于通用能力。明确区分源语义转换、特定版本补偿与研究阻断；同一旧反例只复测未解决时写“无新增实现”。按新规则审查现有补丁后选取本轮两个行为，而不是继续向旧NUMERIC路径叠加包装。

## 3. 代码、环境及提交

- SQLGlot checkout：../sqlglot-functional-commits；分支codex/doris-functional-commits；fork https://github.com/Ragnaroos/sqlglot.git。
- 起点d0c2e9ea1e187edc157f96657313982ce7929e09；最终HEAD 12b98b50836cad4d4a49e968894f4570ca4b9a52，受控工作区干净。整个分支31个本地功能commit，本轮2个，均未push。
- 数据解释器../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-functional-commits:src；sqlglot实际导入该checkout的sqlglot/__init__.py，版本30.25.1.dev6。测试解释器../sqlglot-experiment/.venv/bin/python，PATH显式包含该venv，PYTHONDONTWRITEBYTECODE=1。
- PG18.1/Doris4.1.3-rc02，原43阶段库和UTC/比较规则不变；补充变体用dsv_wf_agg001_s31、只读源连接、10秒超时/100行采集上限。PG array_nulls/standard_conforming_strings均on。Doris原enable_strict_cast/decimal256设置不变，不重建或装数。
- 原SQL/.out、阶段YAML和首轮JSON沿用[统一清单](../attribution/aggregates-001-attribution-summary.md#task-001)，不复制或覆盖；执行run --stdout，不保存额外JSON/脚本/日志。

| 本地commit | 父commit | 行为 | 报告 |
| :--- | :--- | :--- | :--- |
| 0d1d795278d5666cf5756f696f44f20d63dfed53 | d0c2e9ea1e187edc157f96657313982ce7929e09 | PG源数组类型不再由Doris转换白名单控制，目标能力由Generator判断 | [task-001](tasks/aggregates-001/fix-020/task-001.md) |
| 12b98b50836cad4d4a49e968894f4570ca4b9a52 | 0d1d795278d5666cf5756f696f44f20d63dfed53 | 复用一维PG数组文本词法helper，按最终可靠类型生成子数组；处理PG escape文本输入、保留外层CAST上下文 | [task-001](tasks/aggregates-001/fix-020/task-001.md) |

两项分别在准确父commit上完成对应测试/取证后保存，不重写旧commit；共享词法helper和目标消费属于同一输入转换机制。普通标量表达式、未知列Schema、用户数组下标及其他task不扩入本轮。

## 4. 实际验收与回归

| 范围 | 结果及限制 |
| :--- | :--- |
| 源类型职责 | 8条成功PG源变体实测；旧Parser无外层类型提示，新Parser按已知源元素保留INT/BIGINT/TEXT/NUMERIC子数组信息。不支持的目标转换仍在目标侧诊断，不把第一项的提前拒绝当完成转换 |
| 新文本子数组转换 | 20条普通/反向/括号、整数边界、Boolean、NULL/空串、引号/反斜杠、重复、真实列/CASE、CTE及外层TEXT CAST均原目标成功；原生元素类型、完整有限值/维度/位置/重复、必要顺序和双端重复稳定均通过 |
| 显示限制 | 20条中1条Doris数组显示不能当JSON解析，另做原生元素和维度投影核对正确；不修饰真实值、不改Comparator制造MATCH |
| Escape输入兼容 | 额外5条INT/BOOL/NUMERIC/REAL旧规则控制实际执行通过并重复稳定；NUMERIC无约束域及旧REAL补偿限制不因此关闭 |
| 原313条生成层 | 相对本轮起点逐ID生成SQL/严格错误不变 |
| 原43阶段310条安全查询 | 82匹配、25源端负向、69值/顺序不同、114目标失败、12框架环境标签、8转译失败；3条既有BE风险未执行 |
| 原task-001关联14条 | 3匹配、6显示不同、4目标失败、1转译失败，未新增原输入MATCH |
| 旧56条NUMERIC边界 | 最终commit实跑56值/Scale相同、重复稳定，28固定声明对应、28源无约束域限制保留；不升级旧补偿的通用性结论 |
| 旧取负补偿审查 | 6条原生负号控制5同值/1返回NULL；最终生成器对关键DECIMAL(38,38)反例仍正确。没有凭常见值成功就按precision阈值盲目删补偿，尚未完成跨版本/上下文审查 |
| 自动测试 | 第一项1105方言/316定向核心；第二项1107方言/318定向核心；最终commit后PG/Doris114通过。集合重叠不相加，最后新增转义断言另单独通过 |

Ruff检查、格式和git diff --check通过。未运行mypy/C扩展、完整optimizer/integration或make check，未升级依赖。原成功源分母285，82/285=28.77%，与前轮相同；新增边界不进入原输入匹配率。实际源/生成SQL、取证API/解释器、错误、失败尝试及源码路径见[任务报告](tasks/aggregates-001/fix-020/task-001.md)。

## 5. 当前剩余范围

- 新转换只覆盖可靠源类型下的一维默认边界字面量输入；显式下界、多维文本、一般运行时文本列、FLOAT/NUMERIC文本子数组不假装已支持，未知列不猜型。
- 旧NUMERIC文本/lambda/取负补偿保留已实测事实，归为“特定版本补偿，通用性待验证”；本轮有限审查证明不能盲目按precision<=38改为原生负号，不能据此宣布旧补偿全正确或全无效。
- 运行时文本直接REAL、一般NUMERIC域/混合Scale仍是旧未解决事项，本轮没有新增通用实现，不继续当作每轮新修复进展。
- 新查到源PG Generator在标量子查询数组往返时可能丢成员，已写入原任务的独立研究事项；不影响本轮从原文直接生成Doris的成功执行，未顺带修改。

下一步应沿已补证的DECIMAL(38,38)负号反例核对Doris算子推型/能力前提，再决定哪些原生生成能简化旧补偿、哪些需要保留限制，不继续盲目增加包装。当前资料尚不足以安全决定跨版本阈值/统一替代，故未提交第三项猜测性简化；若需改Doris、Session或结果契约，另取授权。所有未完成项保留在统一task清单，整份输入未完成，不以两项commit或文档完成代替语义验收。
