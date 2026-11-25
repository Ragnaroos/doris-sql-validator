# aggregates-001 / fix-015：保留 REAL 字面量的转换顺序

## 1. 本轮结论与范围

继续原task-001，修正“已有REAL字面量先转换、再提升到数组共同类型”的精度差异，包含连续REAL/DOUBLE CAST及负号。**本次有限规则通过验证，整个task-001仍未完成验收；整份输入未完成。** 没有实施其他task，也没有修改验证框架、比较策略、数据或原输入。

两个既有反例的目标原生逐元素结果分别由[1,0] / [1,0,1]改为全部为真。本轮47条成功源边界全部原生值/NULL核验通过且重复稳定；主比较器26一致、21显示不同保留。原142条结果逐ID不变，原82个匹配没有回退；不是匹配率提升。

| 本轮互斥task状态 | 数量 |
| :--- | ---: |
| 已修复并完成约定验收 | 0 |
| 已修改但未完成验收 | 1 |
| 重新打开 / 当前阻断 / 未处理 / 不需修改 | 各0 |

本轮复用1项、新增0项、重新打开0项。全批唯一清单仍为9项：7项完成约定验收、2项未完成（task-001/003）；局部规则通过不把整个task计完成。

## 2. 任务与本地提交

| task / 功能范围 | 任务报告 | commit与保存状态 |
| :--- | :--- | :--- |
| task-001：有限字面量REAL/DOUBLE CAST链先舍入再参与数组提升；含负号及测试 | [完整实施、执行和剩余方案](tasks/aggregates-001/fix-015/task-001.md) | `365986d92f426fa6c837d3fc60ba6a41acd0770c`，本地已提交，未push，无Issue/PR |

父commit为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`；同一干净重建分支上只追加本规则与配套测试，4文件126增加/5删除。复用既有数组类型提示、浮点精确舍入及运行时FLOAT转换。没有按文件拆提交，也没有夹带task-003或其他功能。准确暂存树与commit树相同，commit后161项定向测试通过，工作区干净。

## 3. 共同环境、输入与执行方式

| 项目 | 本轮实际情况 |
| :--- | :--- |
| SQLGlot checkout / branch | ../sqlglot-functional-commits / codex/doris-functional-commits |
| 起止HEAD | `51bf6a4085c5036a236f0ebfa5a720cab5dfb019` → `365986d92f426fa6c837d3fc60ba6a41acd0770c` |
| 单次diff SHA256 | `62c4afd57e161117d870ea07b21b6580a67f7c9a0e6ea2ea5143fdb3342dd76d` |
| fork / upstream | https://github.com/Ragnaroos/sqlglot.git / https://github.com/tobymao/sqlglot.git；无push |
| 原有用户改动 | 开始时新checkout干净；原sqlglot-experiment的dirty内容及社区checkout均未修改 |
| 实际导入 | ../sqlglot-functional-commits/sqlglot/__init__.py |
| 数据库运行环境 | ../doris-sql-validator/.venv/bin/python，PYTHONPATH=../sqlglot-functional-commits:src；版本字符串30.25.1.dev6 |
| 单元测试运行环境 | ../sqlglot-experiment/.venv/bin/python，PYTHONPATH为新checkout；版本字符串30.25.1.dev355；安装元数据差异不代替实际import/SHA核对 |
| PostgreSQL | 本轮确认18.1；127.0.0.1:5432；UTC、ISO/MDY、extra_float_digits=0 |
| Doris | 本轮SHOW FRONTENDS确认doris-4.1.3-rc02-7126cf65d96、Alive=true；127.0.0.1:9030；enable_strict_cast=false；执行沿用UTC |
| 阶段 / 限制 | 原Case使用对应阶段库；常量边界用dsv_wf_agg001_s01；单次10秒/10000行，只读 |
| 原输入与准备材料 | [准备报告](../data-preparation/aggregates-001-data-preparation.md)及同前缀postgres-setup.sql、doris-setup.sql；原.sql/.out仍在../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql / aggregates.out |
| YAML / 首轮JSON | reports/data-preparation/aggregates-001-stage-<NN>-cases.yaml；reports/validation/aggregates-001-stage-<NN>-validation.json；原件不改、不增加.out指纹 |
| 归因入口 | [唯一task清单](../attribution/aggregates-001-attribution-summary.md#task-001)；实施前方案和本轮结果在同条目维护 |

原Case由CliRunner按各stage执行run --path <原YAML> --stdout并重复--id，读原.out、真正转译执行，不另存JSON。边界由修改后的parse_one(...,read='postgres').sql('doris',unsupported_level=RAISE)生成，再execute_query/compare_probe并重复执行。PG二进制游标与目标原生逐元素等值是精度补证，不替换原主比较结论。

## 4. 实际验证结果

| 范围 | 结果及限制 |
| :--- | :--- |
| 本轮47条成功源边界 | 全部源/目标成功、字段/别名/已取得类型、行数/数组位置、原生等值/NULL及重复稳定通过；主比较26一致、21显示不同 |
| 两条既有REAL反例 | 原生第二元素由不等变为相等；主比较仍按实际显示记差异，不伪造MATCH |
| 原142条 / 19阶段 | 82匹配、36 Doris失败、19值/顺序不同、1转译失败、4源负向；逐ID与父状态一致，无缺失ID |
| task-001原14条 | 3匹配、1显示不同、9Doris失败、1转译拒绝；生成SQL/错误另与原最终代码逐条核对一致 |
| 旧97条边界 | 双端成功、重复稳定；74值一致、23Boolean显示差异保持 |
| 旧41条浮点边界 | 全部原生核验/重复稳定通过；主比较25一致、15显示不同、1最大DOUBLE源驱动OverflowError保持 |
| 直接相关6条源负向 | 4条范围错误22003、2条非法文本22P02；默认排除，不为复制源错误新增任务 |
| 额外5条组合控制 | 链中负号遗漏已补入本规则；仍发现子查询提升及运行时列转换真差异，详见任务报告；与47条有重叠，不计原Case数量 |
| 单元测试 | 439定向/核心通过（25.989秒）；全部方言1084通过（4.807秒）；commit后161定向通过（0.767秒）；三组重叠不相加 |
| 风格 / 未运行 | Ruff及diff检查通过；完整optimizer、mypy、C扩展、make check未运行，没有安装依赖 |

没有执行有后端风险的301/303/304；没有进行全部313条/43阶段最终验收。原匹配不代表所有原生类型被.out证明，47条也不证明任意输入同义。原41条的最大DOUBLE驱动解码失败不是源负向，继续保留。

## 5. 后续问题与下一轮

| 真实剩余问题 | 本轮证据 | 处理建议 |
| :--- | :--- | :--- |
| 标量子查询REAL值提升到DOUBLE | `ARRAY[(SELECT 0.1::REAL),2::DOUBLE PRECISION]`首元素原生不等；独立Doris精确输入候选取得[1,1] | 下一轮优先继续task-001，有限无FROM单常量投影的子查询；具体范围/规则/验收已写入task条目 |
| 运行时列CAST REAL | VALUES文本列0.1和7.038531e-26参与REAL→DOUBLE数组，非NULL行首元素原生不等 | 同task继续研究运行时转换，不用字面量预计算冒充通用列转换 |
| 非有限/十六进制、NUMERIC、未知类型及task-003 | 前轮限制仍未关闭，本轮没有完成这些实现 | 保留未完成，不因候选失败直接认定Doris永远不支持 |

**整份输入未完成。** 未满足条件包括：task-001/003仍未完成验收、仍有待调查/可修复性未定项、未做全阶段最终回归，也未逐条证实所有剩余差异都只能由外部系统解决。本轮没有新的未解决回归；完成的是一项独立有限规则及其本地提交，不是整个workflow。下一轮从当前HEAD `365986d92f426fa6c837d3fc60ba6a41acd0770c` 恢复，继续原task-001，不回到旧dirty目录重新叠加修改。

