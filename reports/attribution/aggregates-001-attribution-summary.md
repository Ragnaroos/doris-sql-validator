# aggregates-001：PostgreSQL → Doris 转换归因与 SQLGlot 修复任务

最新状态（fix-020）：按更新后的Skill先确认源语义、适用条件和目标能力，不以测试文件零报错为目标。本轮继续task-001，分别本地commit源类型职责解耦`0d1d795278d5666cf5756f696f44f20d63dfed53`和已知类型下的文本子数组转换`12b98b50836cad4d4a49e968894f4570ca4b9a52`，后者为当前HEAD；整个分支31个本地commit，工作区干净、均未push。20条新文本子数组变体原目标成功且原生类型/值/维度/NULL/必要顺序与重复执行通过，另5条escape输入兼容控制通过；原313条生成层不变，310条安全查询仍82匹配，未新增原输入MATCH。旧数值补偿归为“特定版本补偿，通用性待验证”，原生负号控制5通过/1失败，不能盲目按precision<=38删去补偿；原REAL/一般NUMERIC余项仍未解决，无新增通用实现。完整依据见[fix-020汇总](../fixes/aggregates-001-fix-020-summary.md)及[任务报告](../fixes/tasks/aggregates-001/fix-020/task-001.md)。task-001/003仍未完成、010未实施，整份输入未完成；下方fix-019及更早记录保留历史含义，不表示当前HEAD。

最新代码与任务状态（fix-019，2026-11-25）：[本轮汇总](../fixes/aggregates-001-fix-019-summary.md)继续原task-001，同一次调用完成NUMERIC固定数组CAST、保留元素CAST、数组内取负、NUMERIC/unknown字符串输入及有限无约束NUMERIC[] CAST五个独立功能commit。HEAD `d0c2e9ea1e187edc157f96657313982ce7929e09`，整个分支29个本地commit、工作区干净、均未push。56条新边界全部值/Scale与重复执行通过，其中34条在起点代码下有差异或失败，22条原本正确；28条固定precision/scale对应，另28条无约束NUMERIC不宣称全类型域相同。原313条生成层逐ID未变；43阶段310条安全查询仍82匹配、25负向、69值/顺序不同、114目标失败、12环境标签、8转译失败，未新增原输入MATCH。task-001仍未完成整个验收：直接REAL运行时舍入、一般NUMERIC类型域/混合Scale等具体反例和恢复条件见[本轮任务报告第8节](../fixes/tasks/aggregates-001/fix-019/task-001.md#8-剩余问题停止依据与恢复条件)。当前13项task仍10项完成各自约定验收、001/003两项未完成、010未实施；整份输入未完成。以下fix-018及更早记录保留当时历史含义，不能当作当前HEAD。

代码保存状态更新（2026-11-25）：最新[fix-018](../fixes/aggregates-001-fix-018-summary.md)已补齐所选5条百分位查询的有限转换：DOUBLE概率上下文、连续百分位、精确离散百分位及一维TEXT数组输入，共4个独立本地commit；整个分支累积24个，均未push。使用`../sqlglot-functional-commits`，HEAD `3c9e4bb004bff47a4ca8b750961f5e4470076590`。原0410/0411/0412/0413/0415全部执行成功，实时元素/NULL/形状及已取得类型对齐；原.out因数组花括号/方括号显示仍判不同，未伪造MATCH。用户已授权启动原Doris容器，FE/BE和原阶段表恢复且最终健康；未重试段错误候选。当前13项task中10项完成各自约定验收、task-001/003两项未完成、task-010未实施；整份输入未完成。下文首轮和前轮统计保留历史含义。

## 1. 执行摘要

本批分析 PostgreSQL aggregates.sql/.out 在 43 个冻结数据阶段的 313 条查询记录，涵盖统计聚合、NULL/特殊数值、数组聚合与排序、FILTER、序列/相关子查询、有序集合、用户定义聚合及目录观测。不是 PostgreSQL 全部 SELECT 语法覆盖。

首轮有 62 条成功源查询在可用 .out 显示证据上匹配，成功匹配率 **62 / 288 = 21.53%**；25 条源端负向默认不归因。其余 226 条均已阅读首轮、核对源参考并形成逐条报告；**133 条原因已定位、71 条调查未完成、22 条前提阻断**。建齐报告不等于 226 条都已经归因或获得通用同义改写。

形成 **9 个可独立实施/审查的 task**（详见第 7 节），建议以 task 而非 Case 为默认 PR 单位。数组构造、原生 NULL 排序、ARRAY_AGG 的 NULL/空输入、受限内部排序、普通 FILTER、EVERY、小样本统计 NULL、FROM 常量整数序列及 REGR_COUNT 分别验收。其余算法、类型、查询级转换和外部前提列为待补证事项，不把所有差异强行算作 SQLGlot 缺陷。

本轮仅归因，未修改 SQLGlot/验证器、未进入修复、未提交 PR。候选是诊断方案，不是已实现规则。一次行值一致不证明类型、顺序、边界及全输入同义。已定位显示比较误报、PG 专属目录/状态接口、UDF 未迁移、Doris 参数限制等非核心修复原因。

后续修复状态（不改上面的首轮统计）：[fix-001](../fixes/aggregates-001-fix-001-summary.md) 的 task-001 已修改但未完成类型验收；[fix-002](../fixes/aggregates-001-fix-002-summary.md) 的 task-002 已完成当前环境的排序验收，0137 的实时 PG/.out 冲突保留。[fix-003](../fixes/aggregates-001-fix-003-summary.md) 实现 task-003 的 NULL/空输入规则，类型/精度余项仍未关闭；[fix-004](../fixes/aggregates-001-fix-004-summary.md) 完成 task-004 的约定整数自值排序验收，原 Case 的类型/表示差异保留。[fix-005](../fixes/aggregates-001-fix-005-summary.md) 完成 task-005 的普通聚合条件筛选规则：8 条原查询按 .out 为 6 匹配、1 整数除法值差异、1 相关聚合执行失败；6 个匹配不代表原生类型全部一致。168 组边界有 167 条行值一致，1 条 AVG 尾差已由无 FILTER/二进制控制证明不是本改写引入，仍保留不同，不冒称全部通过。[fix-006](../fixes/aggregates-001-fix-006-summary.md) 完成 PostgreSQL EVERY 函数识别：复用现有 LogicalAnd → MIN，无需额外 CAST，原 0149 的 .out 和实时六列 BOOLEAN/NULL 结果均通过，138 条边界与上下文双端通过。[fix-007](../fixes/aggregates-001-fix-007-summary.md) 完成有限输入的样本统计 NULL 规则：108 条小样本边界全部 NULL 一致；225 条基础/上下文共 195 条精确值一致、30 条既有多样本尾差保留。七条原 Case 的样本 NULL 已修正，但原 .out 整条仍因总体列 `0`/`0.0` 不匹配，0041/0042 另有 NUMERIC/DOUBLE 类型差异；不能称全部 MATCH。[fix-008](../fixes/aggregates-001-fix-008-summary.md) 实现 FROM 非 NULL 常量 INT4 GENERATE_SERIES 主路径；65 条有限边界通过，32 条原查询为 8 匹配、3 值差异、20 Doris 失败、1 转译失败。该轮 NULL 参数仍未支持，task-008 未完成全部验收。最新相关回归 130 条为 80 匹配、28 Doris 执行失败、17 行值/顺序差异、1 转译失败、4 源端负向；此前 72 条匹配保持。最新 [fix-009](../fixes/aggregates-001-fix-009-summary.md) 补齐常量 NULL 参数的运行时零行规则，123 条边界/上下文双端通过并复跑稳定，原 130 条结果和 80 个匹配保持；task-008 完成约定验收。截至 fix-009，全批 9 项为 6 项完成约定验收、2 项已修改未验收、1 项未处理；整份输入未完成。该轮建议下一独立任务 task-009；task-001/003 及类型/浮点/非有限数/相关研究仍保留，未自动实施下一项，未提交/推送。按独立修复 commit 交付，不以社区 PR 为结束条件；下文 PR 字样保留首轮拆分依据，不表示已创建或获准创建 PR。

[fix-010](../fixes/aggregates-001-fix-010-summary.md) 完成 task-009 的普通数值参数 REGR_COUNT 成对计数：两条原查询中 0073 新增匹配，0544 第三列 BIGINT 40000 正确但方差/SUM 余项保留。67 条计数边界/上下文中 66 条完整通过、1 条外层 SUM 类型不同，额外无 REGR_COUNT 控制也复现该类型差异；不冒称全部匹配。132 条原查询跨 17 阶段回归为 81 匹配、28 Doris 执行失败、18 值/顺序不同、1 转译失败、4 源端负向，原有 80 个匹配全部保持。当前九项为 **7 项完成约定验收、2 项已修改但未完成验收、0 项未处理**。整份输入未完成，下一步建议回到 task-001/003 的类型验收及现有待研究项；未自动开始，未提交/推送。

前轮 [fix-011](../fixes/aggregates-001-fix-011-summary.md)完成task-001/003本轮类型补查，仍未关闭两项验收。24条关联原查询当前PG文本均与.out相同；40条既有边界取得元素OID/typmod并双端重复，区分递归别名与真实默认类型/结果约束差异。142条扩展回归为82匹配、36 Doris失败、19值/顺序不同、1转译失败、4源端负向，前轮81个匹配全部保持；多出0306的匹配只是扩大范围（fix-001已匹配），不是本轮新增修复。本轮代码diff与fix-010相同，没有安全通用类型补丁则不强行修改；在原任务中列明默认元素类型保留、VALUES输入类型与Decimal结果约束等子项，不新增编号。全批仍为7项约定验收、2项未验收，整份输入未完成，未提交/推送。

前轮 [fix-012](../fixes/aggregates-001-fix-012-summary.md)实际实现task-001的有限源元素类型保留：PG Parser把可信类型放入Array AST，Doris Generator在默认链路生成ARRAY<INT/BIGINT/STRING等>的CAST，不需要Schema。前轮18条边界中7条默认类型差异已修正，原0010的数组元素也由VARCHAR(5)改为TEXT；本轮37条边界均双端成功并重复稳定，35条结构化值一致，另保留Boolean显示和混合字符串/整数真差异。142条同范围回归逐ID结果不变，原82匹配全部保持；不是.out匹配数提升。混合输入转换、Decimal/超INT64 NUMERIC及未知列类型仍未全部验收，task-001保持“已修改但未完成验收”，task-003本轮未实施。全批仍7项约定验收、2项未验收，整份输入未完成，未commit/push。

最新 [fix-013](../fixes/aggregates-001-fix-013-summary.md)继续task-001，实现unknown字符串与已知整数/Boolean的输入转换：规范化PG支持的整数格式/布尔拼写，在构造数组前转换元素，并尊重显式数组CAST。fix-012留下的ARRAY['1',2]真值差异已修正。最终97条成功源边界均双端成功、重复稳定；74条现有结构化值一致，23条Boolean显示不同保留，其中22条新增Boolean另以原生元素投影核对一致。21条补充非法输入均源端报错并默认排除。15组NUMERIC/Float补查进一步细分为9当前值相同、5不同、1源合法但Parser拒绝，不能把NaN/Infinity/大数或负Scale混作输出样式差异。142条原回归结果逐ID不变，82个匹配保持。task-001仍未关闭Float/NUMERIC/未知类型余项，task-003未实施；仍7项完成约定验收、2项未验收，整份输入未完成，未commit/push。

最新[fix-014](../fixes/aggregates-001-fix-014-summary.md)已按实施前方案继续task-001，补齐有限十进制unknown文本与FLOAT/DOUBLE的输入转换。41条源成功变体经PG二进制及目标原生元素核验均取得通过证据；主比较器仍保留25值一致、15显示差异和1最大DOUBLE源驱动解码失败。前轮97边界/原142条回归结果保持。两条额外控制证明已有REAL元素CAST仍有真实精度差异，下一轮具体方案已写入[task-001](#task-001)，不只留下任务标题。全批仍7项完成约定验收、2项未验收；整份输入未完成，未commit/push。

<a id="inputs"></a>

## 2. 输入与覆盖范围

调查时间（UTC）：2026-11-20T02:15:38.487043+00:00 → 2026-11-20T02:51:38.953608+00:00。

- 源 SQL：../../../doris-sql-validator/cases/postgres/manual/current/assets/aggregates.sql。
- 历史输出：同目录 aggregates.out；保持原件，按原文和出现序号读取，不校验或保存 .out 指纹。
- 数据准备：[说明](../data-preparation/aggregates-001-data-preparation.md)、[PostgreSQL SQL](../data-preparation/aggregates-001-postgres-setup.sql)、[Doris SQL](../data-preparation/aggregates-001-doris-setup.sql)。准备由独立流程完成，本轮不建表、不装数。
- 社区 SQLGlot：30.25.1.dev6；提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9，[checkout](../../../sqlglot/)（相对项目根目录为 ../sqlglot）。**未刷新远端最新 main**，task 缺口只对该基线成立；真正提交前还需在拟提 PR 的最新基线上复核。
- PostgreSQL 18.1，127.0.0.1:5432；Doris doris-4.1.3-rc02-7126cf65d96，127.0.0.1:9030；MySQL 协议 VERSION() 的 5.7.99 不是产品版本。数据库 dsv_wf_agg001_s01–s43。
- 会话：UTC；PG DateStyle=ISO, MDY，extra_float_digits=0；Doris enable_strict_cast=false、enable_decimal256=false。只读调用超时 10 秒，有限完整结果上限 10000 行；样本最多 3 行。凭据不进入报告。

| 覆盖项目 | 实际范围 | 统计与限制 |
| :--- | :--- | :--- |
| 验证记录 | 313 | 每次出现单独计数；原 Case ID 保留，未语义去重 |
| 不同原文 | 294；多出的重复出现 19 | 使用读取器的 PostgreSQL 回显识别，不表示 294 个独立语义问题 |
| 数据阶段 | 43 | 装数、改视图、函数/聚合及事务状态变化；同文查询在不同状态不能合并执行 |
| YAML / validation JSON | 各 43 份 | 每个 stage 一份输入和一次首轮结果，文件名下表给出；不是 43×313 条查询 |
| 源端成功 / 负向 | 288 / 25 | .out 均可定位；Parser 拒绝的成功源例仍纳入 313 |
| 逐条归因 | 226 份 Markdown + 1 份本汇总 | 无额外交接、候选 SQL、执行 JSON 或 evidence 目录 |
| 导入范围限制 | 两个 COPY … NULL 后的 SELECT 块未被当前导入器提取 | 源文件行 302–328、376–388；不是本批 313 中的失败，需修读取器后另运行 |
| 数据准备记录 | 历史 540 次阶段对象全记录核验 | 引用已有准备材料，不是本轮又执行 540 条；6 个阶段对象未映射，不宣称所有类型/继承前提完整 |

普通 DDL/DML 不在验证器中运行；历史数据核验不等于继承 ONLY、复合排序、二进制及所有数据域都等价。7 个复合数组视图有明确 `ARRAY<STRUCT>` 映射，本轮另做结构诊断，不再将其当缺表。

### 2.1 阶段材料导航

| 阶段 | 查询数 | Case YAML | 首轮 JSON |
| :--- | ---: | :--- | :--- |
| aggregates-001-stage-01 | 97 | [YAML](../data-preparation/aggregates-001-stage-01-cases.yaml) | [validation](../validation/aggregates-001-stage-01-validation.json) |
| aggregates-001-stage-02 | 12 | [YAML](../data-preparation/aggregates-001-stage-02-cases.yaml) | [validation](../validation/aggregates-001-stage-02-validation.json) |
| aggregates-001-stage-03 | 20 | [YAML](../data-preparation/aggregates-001-stage-03-cases.yaml) | [validation](../validation/aggregates-001-stage-03-validation.json) |
| aggregates-001-stage-04 | 1 | [YAML](../data-preparation/aggregates-001-stage-04-cases.yaml) | [validation](../validation/aggregates-001-stage-04-validation.json) |
| aggregates-001-stage-05 | 2 | [YAML](../data-preparation/aggregates-001-stage-05-cases.yaml) | [validation](../validation/aggregates-001-stage-05-validation.json) |
| aggregates-001-stage-06 | 1 | [YAML](../data-preparation/aggregates-001-stage-06-cases.yaml) | [validation](../validation/aggregates-001-stage-06-validation.json) |
| aggregates-001-stage-07 | 6 | [YAML](../data-preparation/aggregates-001-stage-07-cases.yaml) | [validation](../validation/aggregates-001-stage-07-validation.json) |
| aggregates-001-stage-08 | 1 | [YAML](../data-preparation/aggregates-001-stage-08-cases.yaml) | [validation](../validation/aggregates-001-stage-08-validation.json) |
| aggregates-001-stage-09 | 10 | [YAML](../data-preparation/aggregates-001-stage-09-cases.yaml) | [validation](../validation/aggregates-001-stage-09-validation.json) |
| aggregates-001-stage-10 | 2 | [YAML](../data-preparation/aggregates-001-stage-10-cases.yaml) | [validation](../validation/aggregates-001-stage-10-validation.json) |
| aggregates-001-stage-11 | 1 | [YAML](../data-preparation/aggregates-001-stage-11-cases.yaml) | [validation](../validation/aggregates-001-stage-11-validation.json) |
| aggregates-001-stage-12 | 3 | [YAML](../data-preparation/aggregates-001-stage-12-cases.yaml) | [validation](../validation/aggregates-001-stage-12-validation.json) |
| aggregates-001-stage-13 | 1 | [YAML](../data-preparation/aggregates-001-stage-13-cases.yaml) | [validation](../validation/aggregates-001-stage-13-validation.json) |
| aggregates-001-stage-14 | 3 | [YAML](../data-preparation/aggregates-001-stage-14-cases.yaml) | [validation](../validation/aggregates-001-stage-14-validation.json) |
| aggregates-001-stage-15 | 6 | [YAML](../data-preparation/aggregates-001-stage-15-cases.yaml) | [validation](../validation/aggregates-001-stage-15-validation.json) |
| aggregates-001-stage-16 | 1 | [YAML](../data-preparation/aggregates-001-stage-16-cases.yaml) | [validation](../validation/aggregates-001-stage-16-validation.json) |
| aggregates-001-stage-17 | 23 | [YAML](../data-preparation/aggregates-001-stage-17-cases.yaml) | [validation](../validation/aggregates-001-stage-17-validation.json) |
| aggregates-001-stage-18 | 2 | [YAML](../data-preparation/aggregates-001-stage-18-cases.yaml) | [validation](../validation/aggregates-001-stage-18-validation.json) |
| aggregates-001-stage-19 | 2 | [YAML](../data-preparation/aggregates-001-stage-19-cases.yaml) | [validation](../validation/aggregates-001-stage-19-validation.json) |
| aggregates-001-stage-20 | 2 | [YAML](../data-preparation/aggregates-001-stage-20-cases.yaml) | [validation](../validation/aggregates-001-stage-20-validation.json) |
| aggregates-001-stage-21 | 2 | [YAML](../data-preparation/aggregates-001-stage-21-cases.yaml) | [validation](../validation/aggregates-001-stage-21-validation.json) |
| aggregates-001-stage-22 | 2 | [YAML](../data-preparation/aggregates-001-stage-22-cases.yaml) | [validation](../validation/aggregates-001-stage-22-validation.json) |
| aggregates-001-stage-23 | 2 | [YAML](../data-preparation/aggregates-001-stage-23-cases.yaml) | [validation](../validation/aggregates-001-stage-23-validation.json) |
| aggregates-001-stage-24 | 2 | [YAML](../data-preparation/aggregates-001-stage-24-cases.yaml) | [validation](../validation/aggregates-001-stage-24-validation.json) |
| aggregates-001-stage-25 | 12 | [YAML](../data-preparation/aggregates-001-stage-25-cases.yaml) | [validation](../validation/aggregates-001-stage-25-validation.json) |
| aggregates-001-stage-26 | 1 | [YAML](../data-preparation/aggregates-001-stage-26-cases.yaml) | [validation](../validation/aggregates-001-stage-26-validation.json) |
| aggregates-001-stage-27 | 1 | [YAML](../data-preparation/aggregates-001-stage-27-cases.yaml) | [validation](../validation/aggregates-001-stage-27-validation.json) |
| aggregates-001-stage-28 | 5 | [YAML](../data-preparation/aggregates-001-stage-28-cases.yaml) | [validation](../validation/aggregates-001-stage-28-validation.json) |
| aggregates-001-stage-29 | 2 | [YAML](../data-preparation/aggregates-001-stage-29-cases.yaml) | [validation](../validation/aggregates-001-stage-29-validation.json) |
| aggregates-001-stage-30 | 3 | [YAML](../data-preparation/aggregates-001-stage-30-cases.yaml) | [validation](../validation/aggregates-001-stage-30-validation.json) |
| aggregates-001-stage-31 | 49 | [YAML](../data-preparation/aggregates-001-stage-31-cases.yaml) | [validation](../validation/aggregates-001-stage-31-validation.json) |
| aggregates-001-stage-32 | 2 | [YAML](../data-preparation/aggregates-001-stage-32-cases.yaml) | [validation](../validation/aggregates-001-stage-32-validation.json) |
| aggregates-001-stage-33 | 6 | [YAML](../data-preparation/aggregates-001-stage-33-cases.yaml) | [validation](../validation/aggregates-001-stage-33-validation.json) |
| aggregates-001-stage-34 | 9 | [YAML](../data-preparation/aggregates-001-stage-34-cases.yaml) | [validation](../validation/aggregates-001-stage-34-validation.json) |
| aggregates-001-stage-35 | 2 | [YAML](../data-preparation/aggregates-001-stage-35-cases.yaml) | [validation](../validation/aggregates-001-stage-35-validation.json) |
| aggregates-001-stage-36 | 1 | [YAML](../data-preparation/aggregates-001-stage-36-cases.yaml) | [validation](../validation/aggregates-001-stage-36-validation.json) |
| aggregates-001-stage-37 | 1 | [YAML](../data-preparation/aggregates-001-stage-37-cases.yaml) | [validation](../validation/aggregates-001-stage-37-validation.json) |
| aggregates-001-stage-38 | 1 | [YAML](../data-preparation/aggregates-001-stage-38-cases.yaml) | [validation](../validation/aggregates-001-stage-38-validation.json) |
| aggregates-001-stage-39 | 1 | [YAML](../data-preparation/aggregates-001-stage-39-cases.yaml) | [validation](../validation/aggregates-001-stage-39-validation.json) |
| aggregates-001-stage-40 | 1 | [YAML](../data-preparation/aggregates-001-stage-40-cases.yaml) | [validation](../validation/aggregates-001-stage-40-validation.json) |
| aggregates-001-stage-41 | 2 | [YAML](../data-preparation/aggregates-001-stage-41-cases.yaml) | [validation](../validation/aggregates-001-stage-41-validation.json) |
| aggregates-001-stage-42 | 6 | [YAML](../data-preparation/aggregates-001-stage-42-cases.yaml) | [validation](../validation/aggregates-001-stage-42-validation.json) |
| aggregates-001-stage-43 | 4 | [YAML](../data-preparation/aggregates-001-stage-43-cases.yaml) | [validation](../validation/aggregates-001-stage-43-validation.json) |

## 3. 首轮验证统计与归因范围

| 首轮分流（互斥） | 查询数 | 后续处理 |
| :--- | ---: | :--- |
| 可用证据下匹配 | 62 | 简写，不生成逐条文档，不纳入修复积压 |
| 源端负向 | 25 | .out 本来报错；默认不独立改写、不要求目标复刻同一错误 |
| 不匹配且非负向 | 226 | 每条一份 Markdown，保留前提阻断 |
| 合计 | 313 | 无 .out 定位失败 |


```text
313 条查询记录 − 62 条匹配 − 25 条源端负向 = 226 份应有逐条归因报告
226 份已生成 + 0 份缺失 = 226 份
首轮成功匹配率 = 62 / 288 条源成功查询 = 21.53%
```

| 首轮观察标签 | 数量 | 含义及本轮纠正 |
| :--- | ---: | :--- |
| Doris 执行失败 | 134 | 源成功，目标报错；不直接等同 SQLGlot 缺陷 |
| SQLGlot 转译失败 | 27 | 9 条源 Parser 失败、18 条生成拒绝；PG 成功源句不能因此被判非法 |
| 行值或顺序不匹配 | 53 | 含显示文本、真实数值/NULL/数组差异，需分开解释 |
| Doris 环境问题 | 12 | 10 条确有缺对象前提；另 2 条 ONLY 被当成表名，属于转换/能力问题，不能创建 ONLY 表解决 |

首轮比较按显示文本，不自动应用有类型浮点容差；.out 不提供原生字段类型，空单元格不可靠区分 NULL/空字符串。故 62 条匹配只表示已有证据未发现差异，**不是完整语义通过率**。本轮补查结果不回写首轮 MATCH。

## 4. 调查进度与执行覆盖

| 互斥进度 | 数量 | 实际含义 |
| :--- | ---: | :--- |
| 原因已定位 | 133 | 代码/错误/实际值足以解释本样本差异；可仍缺通用模拟或完整类型边界。 |
| 调查未完成 | 71 | 已执行控制或候选，但数值算法、返回契约或查询级安全性仍缺关键证据。 |
| 前提阻断 | 22 | 3 条安全阻断、6 条当前 PG 与历史成功条件不兼容、4 条 avg_rec、9 条 BYTEA。 |
| 尚未开展 | 0 | 无；所有 226 条均阅读并保留调查事实，不代表每条都独立改写成功。 |

| 实际工作量 | 数量 | 口径 |
| :--- | ---: | :--- |
| 原文 PG 实际成功 | 217 | 211 条经标准工具 + 6 条经审阅的原文直连（工具 Parser 阻断） |
| 原文 PG 实际失败 / 未执行 | 6 / 3 | 6 条历史版本/语义不兼容；3 条危险同族不重试 |
| 已保存社区 SQL 的控制重跑 | 199 | 不是独立候选；失败与工具阻断亦保留具体事实 |
| 有候选调用的不同 Case | 143 | 其中 142 条有文本不同的候选、1 条只有相同文本控制；每条可多次尝试；其余 83 条保留代码、控制或前提证据 |
| 候选尝试总数 | 171 | 163 次文本不同；失败也计次数，不是缺陷数量 |
| 候选尝试未成功执行 | 43 | 不等于该语义绝对无法在 Doris 实现 |
| 最新候选成功执行 | 119 | 不等于与源匹配 |
| 最新候选行值与重复次数一致 | 96 | 有最终 ORDER BY 时另查顺序；不表示类型全部对齐 |
| 最新候选已识别类型声明/逻辑/精度检查均对齐 | 74 | 与上一行可重叠；嵌套类型别名尚需人工解释 |
| 最新候选值、已识别类型且未发现所需顺序/别名差异 | 57 | 仅当前输入和工具可识别证据；不是“所有边界通过” |
| PG 二进制补查 | 146 | 原 SQL 不变，排除 text 协议显示舍入；不改变浮点容差 |
| 共享边界变体 | 18 | 分别真实执行 PG/Doris；只说明所列变体，不覆盖每条复杂 Case 的所有边界 |
| 已知复合数组结构诊断 | 7 | PG TO_JSONB 变体与目标结构值一致；不替换原 SELECT 的历史参考 |

候选通过分维度判断，不使用一个未解释的“已验证同义”标签。统计未自动要求排序键唯一，不以重复执行稳定证明唯一。边界中 ARRAY_AGG 未排序 DISTINCT 的元素顺序仍不同、原生空输入返回 [] 而非 NULL、按位聚合候选实际报错，均保留。

### 4.1 历史 .out 与实时 PostgreSQL

226 条主范围的文本多重集合补查：196 条与历史相同；21 条值或显示不同；6 条当前 PG 原文执行失败；3 条安全阻断。21 条并不都是真实数值变化，包含视图反解析的文字/空白变化；极端浮点与 avg_rec 则有实质差异，见逐条。此补查不替换 .out，也不是最终顺序验证。

## 5. 逐查询导航

| Case 与详情 | 源 SQL 摘要 | 首轮问题 | 原因摘要 | SQLGlot 处理 | 进度 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| [pg-aggregates-0005-11b43275](cases/aggregates-001/pg-aggregates-0005-11b43275.md) | SELECT avg(four) AS avg_1 FROM onek; | 行值或顺序不匹配 | 1.5000000000000000 与 1.5 的显示差异之外，PG AVG(INT) 为 NUMERIC，Doris 为 DOUBLE；数值相同不消除真实返回类型契约差异 | 需类型感知方案，尚未形成独立可实施任务 | 调查未完成 |
| [pg-aggregates-0006-86de303b](cases/aggregates-001/pg-aggregates-0006-86de303b.md) | SELECT avg(a) AS avg_32 FROM aggtest WHERE a < 100; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0010-12bf388c](cases/aggregates-001/pg-aggregates-0010-12bf388c.md) | SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v); | SQLGlot 转译失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0012-3a87f04b](cases/aggregates-001/pg-aggregates-0012-3a87f04b.md) | SELECT avg(gpa) AS avg_3_4 FROM ONLY student; | Doris 环境问题 | 生成器保留 ONLY，Doris 将其当作表名而报缺表 | 先讨论明确 unsupported 或继承映射方案 | 原因已定位 |
| [pg-aggregates-0015-4a78a728](cases/aggregates-001/pg-aggregates-0015-4a78a728.md) | SELECT sum(b) AS avg_431_773 FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0016-e67c8e38](cases/aggregates-001/pg-aggregates-0016-e67c8e38.md) | SELECT sum(gpa) AS avg_6_8 FROM ONLY student; | Doris 环境问题 | 生成器保留 ONLY，Doris 将其当作表名而报缺表 | 先讨论明确 unsupported 或继承映射方案 | 原因已定位 |
| [pg-aggregates-0021-7678f6ba](cases/aggregates-001/pg-aggregates-0021-7678f6ba.md) | SELECT stddev_pop(b) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0023-251c8665](cases/aggregates-001/pg-aggregates-0023-251c8665.md) | SELECT var_pop(b) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0025-d78c66c7](cases/aggregates-001/pg-aggregates-0025-d78c66c7.md) | SELECT stddev_pop(b::numeric) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0026-54749b3e](cases/aggregates-001/pg-aggregates-0026-54749b3e.md) | SELECT stddev_samp(b::numeric) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0027-6d80b91b](cases/aggregates-001/pg-aggregates-0027-6d80b91b.md) | SELECT var_pop(b::numeric) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0028-7de34821](cases/aggregates-001/pg-aggregates-0028-7de34821.md) | SELECT var_samp(b::numeric) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0029-d0645c62](cases/aggregates-001/pg-aggregates-0029-d0645c62.md) | SELECT var_pop(1.0::float8), var_samp(2.0::float8); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0030-549b8efa](cases/aggregates-001/pg-aggregates-0030-549b8efa.md) | SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0031-db84a9eb](cases/aggregates-001/pg-aggregates-0031-db84a9eb.md) | SELECT var_pop('inf'::float8), var_samp('inf'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0032-73c05241](cases/aggregates-001/pg-aggregates-0032-73c05241.md) | SELECT stddev_pop('inf'::float8), stddev_samp('inf'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0033-027391b8](cases/aggregates-001/pg-aggregates-0033-027391b8.md) | SELECT var_pop('nan'::float8), var_samp('nan'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0034-b0e2e780](cases/aggregates-001/pg-aggregates-0034-b0e2e780.md) | SELECT stddev_pop('nan'::float8), stddev_samp('nan'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0035-daf9210d](cases/aggregates-001/pg-aggregates-0035-daf9210d.md) | SELECT var_pop(1.0::float4), var_samp(2.0::float4); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0036-7e813a8e](cases/aggregates-001/pg-aggregates-0036-7e813a8e.md) | SELECT stddev_pop(3.0::float4), stddev_samp(4.0::float4); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0037-9e86a590](cases/aggregates-001/pg-aggregates-0037-9e86a590.md) | SELECT var_pop('inf'::float4), var_samp('inf'::float4); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0038-474e8581](cases/aggregates-001/pg-aggregates-0038-474e8581.md) | SELECT stddev_pop('inf'::float4), stddev_samp('inf'::float4); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0039-4005fc5e](cases/aggregates-001/pg-aggregates-0039-4005fc5e.md) | SELECT var_pop('nan'::float4), var_samp('nan'::float4); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0040-a02080ac](cases/aggregates-001/pg-aggregates-0040-a02080ac.md) | SELECT stddev_pop('nan'::float4), stddev_samp('nan'::float4); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0041-6590092b](cases/aggregates-001/pg-aggregates-0041-6590092b.md) | SELECT var_pop(1.0::numeric), var_samp(2.0::numeric); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0042-48fe21bd](cases/aggregates-001/pg-aggregates-0042-48fe21bd.md) | SELECT stddev_pop(3.0::numeric), stddev_samp(4.0::numeric); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0043-dbb54239](cases/aggregates-001/pg-aggregates-0043-dbb54239.md) | SELECT var_pop('inf'::numeric), var_samp('inf'::numeric); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0044-507b44d8](cases/aggregates-001/pg-aggregates-0044-507b44d8.md) | SELECT stddev_pop('inf'::numeric), stddev_samp('inf'::numeric); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0045-195c7ba3](cases/aggregates-001/pg-aggregates-0045-195c7ba3.md) | SELECT var_pop('nan'::numeric), var_samp('nan'::numeric); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0046-fc983fe4](cases/aggregates-001/pg-aggregates-0046-fc983fe4.md) | SELECT stddev_pop('nan'::numeric), stddev_samp('nan'::numeric); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0047-027f1f0b](cases/aggregates-001/pg-aggregates-0047-027f1f0b.md) | SELECT max(row(a,b)) FROM aggtest; | Doris 执行失败 | ROW(a,b) 没有映射成目标行值；补成 NAMED_STRUCT 后该 Doris 仍拒绝 MIN/MAX(STRUCT) | 尚无可验收通用改写 | 原因已定位 |
| [pg-aggregates-0048-a1525a74](cases/aggregates-001/pg-aggregates-0048-a1525a74.md) | SELECT max(row(b,a)) FROM aggtest; | Doris 执行失败 | ROW(a,b) 没有映射成目标行值；补成 NAMED_STRUCT 后该 Doris 仍拒绝 MIN/MAX(STRUCT) | 尚无可验收通用改写 | 原因已定位 |
| [pg-aggregates-0049-df94fed3](cases/aggregates-001/pg-aggregates-0049-df94fed3.md) | SELECT min(row(a,b)) FROM aggtest; | Doris 执行失败 | ROW(a,b) 没有映射成目标行值；补成 NAMED_STRUCT 后该 Doris 仍拒绝 MIN/MAX(STRUCT) | 尚无可验收通用改写 | 原因已定位 |
| [pg-aggregates-0050-5a9fb934](cases/aggregates-001/pg-aggregates-0050-5a9fb934.md) | SELECT min(row(b,a)) FROM aggtest; | Doris 执行失败 | ROW(a,b) 没有映射成目标行值；补成 NAMED_STRUCT 后该 Doris 仍拒绝 MIN/MAX(STRUCT) | 尚无可验收通用改写 | 原因已定位 |
| [pg-aggregates-0051-6f50d445](cases/aggregates-001/pg-aggregates-0051-6f50d445.md) | select sum(null::int4) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0052-57717b1c](cases/aggregates-001/pg-aggregates-0052-57717b1c.md) | select sum(null::int8) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0053-80bc631f](cases/aggregates-001/pg-aggregates-0053-80bc631f.md) | select sum(null::numeric) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0054-9d43ca75](cases/aggregates-001/pg-aggregates-0054-9d43ca75.md) | select sum(null::float8) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0055-a2bc4e59](cases/aggregates-001/pg-aggregates-0055-a2bc4e59.md) | select avg(null::int4) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0056-ed925b77](cases/aggregates-001/pg-aggregates-0056-ed925b77.md) | select avg(null::int8) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0057-54488b60](cases/aggregates-001/pg-aggregates-0057-54488b60.md) | select avg(null::numeric) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0058-774c37d9](cases/aggregates-001/pg-aggregates-0058-774c37d9.md) | select avg(null::float8) from generate_series(1,3); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0059-6e8dac37](cases/aggregates-001/pg-aggregates-0059-6e8dac37.md) | select sum('NaN'::numeric) from generate_series(1,3); | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0060-10dc4c9b](cases/aggregates-001/pg-aggregates-0060-10dc4c9b.md) | select avg('NaN'::numeric) from generate_series(1,3); | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0066-82b28760](cases/aggregates-001/pg-aggregates-0066-82b28760.md) | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('1'), ('infinity')) v(x); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0067-d68e127a](cases/aggregates-001/pg-aggregates-0067-d68e127a.md) | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('infinity'), ('1')) v(x); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0068-a8a0f897](cases/aggregates-001/pg-aggregates-0068-a8a0f897.md) | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('infinity'), ('infinity')) v(x… | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0069-dbe867f2](cases/aggregates-001/pg-aggregates-0069-dbe867f2.md) | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('-infinity'), ('infinity')) v(… | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0070-59676ab5](cases/aggregates-001/pg-aggregates-0070-59676ab5.md) | SELECT sum(x::numeric), avg(x::numeric), var_pop(x::numeric) FROM (VALUES ('-infinity'), ('-infinity')) v… | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0071-3dc674b8](cases/aggregates-001/pg-aggregates-0071-3dc674b8.md) | SELECT avg(x::float8), var_pop(x::float8) FROM (VALUES (100000003), (100000004), (100000006), (100000007)… | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0072-7639b7e8](cases/aggregates-001/pg-aggregates-0072-7639b7e8.md) | SELECT avg(x::float8), var_pop(x::float8) FROM (VALUES (7000000000005), (7000000000007)) v(x); | 行值或顺序不匹配 | 历史 .out 按显示文本比较产生差异；本轮 PG 二进制结果与社区 Doris 数值相同，已知字段类型也对齐 | 不需为本样本修改 SQLGlot | 原因已定位 |
| [pg-aggregates-0073-ba8ee5d1](cases/aggregates-001/pg-aggregates-0073-ba8ee5d1.md) | SELECT regr_count(b, a) FROM aggtest; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0074-2817dc87](cases/aggregates-001/pg-aggregates-0074-2817dc87.md) | SELECT regr_sxx(b, a) FROM aggtest; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0075-e8c75ef7](cases/aggregates-001/pg-aggregates-0075-e8c75ef7.md) | SELECT regr_syy(b, a) FROM aggtest; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0076-6582f296](cases/aggregates-001/pg-aggregates-0076-6582f296.md) | SELECT regr_sxy(b, a) FROM aggtest; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0077-e9c8d047](cases/aggregates-001/pg-aggregates-0077-e9c8d047.md) | SELECT regr_avgx(b, a), regr_avgy(b, a) FROM aggtest; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0078-f2583996](cases/aggregates-001/pg-aggregates-0078-f2583996.md) | SELECT regr_r2(b, a) FROM aggtest; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0079-18883aa1](cases/aggregates-001/pg-aggregates-0079-18883aa1.md) | SELECT regr_slope(b, a), regr_intercept(b, a) FROM aggtest; | 行值或顺序不匹配 | 历史 .out 按显示文本比较产生差异；本轮 PG 二进制结果与社区 Doris 数值相同，已知字段类型也对齐 | 不需为本样本修改 SQLGlot | 原因已定位 |
| [pg-aggregates-0080-b740db4f](cases/aggregates-001/pg-aggregates-0080-b740db4f.md) | SELECT covar_pop(b, a), covar_samp(b, a) FROM aggtest; | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0081-60dd4d15](cases/aggregates-001/pg-aggregates-0081-60dd4d15.md) | SELECT corr(b, a) FROM aggtest; | 行值或顺序不匹配 | 历史 .out 按显示文本比较产生差异；本轮 PG 二进制结果与社区 Doris 数值相同，已知字段类型也对齐 | 不需为本样本修改 SQLGlot | 原因已定位 |
| [pg-aggregates-0082-f9348d8f](cases/aggregates-001/pg-aggregates-0082-f9348d8f.md) | SELECT covar_pop(1::float8,2::float8), covar_samp(3::float8,4::float8); | 行值或顺序不匹配 | PG 样本统计在不足两条有效输入时返回 NULL，Doris 返回 0；COUNT 条件补偿已实际修正当前行值 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0083-5557b995](cases/aggregates-001/pg-aggregates-0083-5557b995.md) | SELECT covar_pop(1::float8,'inf'::float8), covar_samp(3::float8,'inf'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0084-9a824985](cases/aggregates-001/pg-aggregates-0084-9a824985.md) | SELECT covar_pop(1::float8,'nan'::float8), covar_samp(3::float8,'nan'::float8); | 行值或顺序不匹配 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0085-b2d1da4b](cases/aggregates-001/pg-aggregates-0085-b2d1da4b.md) | SELECT corr(0.09, g), regr_r2(0.09, g) FROM generate_series(1, 30) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0086-94d0e96a](cases/aggregates-001/pg-aggregates-0086-94d0e96a.md) | SELECT corr(g, 0.09), regr_r2(g, 0.09), regr_slope(g, 0.09), regr_intercept(g, 0.09) FROM generate_series… | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0087-c50d900b](cases/aggregates-001/pg-aggregates-0087-c50d900b.md) | SELECT corr(1.3 + g * 1e-16, 1.3 + g * 1e-16) FROM generate_series(1, 3) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0088-e73d81f2](cases/aggregates-001/pg-aggregates-0088-e73d81f2.md) | with data(x) as (values (1::float8),(2::float8),(3::float8)) select covar_pop(x, 0::float8) from data; | 行值或顺序不匹配 | 历史 .out 按显示文本比较产生差异；本轮 PG 二进制结果与社区 Doris 数值相同，已知字段类型也对齐 | 不需为本样本修改 SQLGlot | 原因已定位 |
| [pg-aggregates-0093-d3a22e61](cases/aggregates-001/pg-aggregates-0093-d3a22e61.md) | SELECT corr(1e-100 + g * 1e-105, 1e-100 + g * 1e-105), regr_r2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105) … | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0094-75ff7206](cases/aggregates-001/pg-aggregates-0094-75ff7206.md) | SELECT corr(1e-100 + g * 1e-105, 1e-100 + g * 1e-105), regr_r2(1e-100 + g * 1e-105, 1e-100 + g * 1e-105) … | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0095-5046511e](cases/aggregates-001/pg-aggregates-0095-5046511e.md) | SELECT corr(1e100 + g * 1e95, 1e100 + g * 1e95), regr_r2(1e100 + g * 1e95, 1e100 + g * 1e95) FROM generat… | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0096-fdbe460d](cases/aggregates-001/pg-aggregates-0096-fdbe460d.md) | SELECT regr_intercept(y, x) FROM (VALUES (-1e150, 0), (2e150, 3e150)) v(x, y); | 行值或顺序不匹配 | 历史极端浮点回归结果与当前 PG 18.1 不同；当前 PG 二进制值与社区 Doris 相同，但历史 .out 不可被静默替换 | 当前证据不支持直接修 SQLGlot | 调查未完成 |
| [pg-aggregates-0097-9b7a3291](cases/aggregates-001/pg-aggregates-0097-9b7a3291.md) | SELECT regr_intercept(y, x) FROM (VALUES (-1e-131, 0), (2e-131, 3e-131)) v(x, y); | 行值或顺序不匹配 | 历史极端浮点回归结果与当前 PG 18.1 不同；当前 PG 二进制值与社区 Doris 相同，但历史 .out 不可被静默替换 | 当前证据不支持直接修 SQLGlot | 调查未完成 |
| [pg-aggregates-0098-b1e5567b](cases/aggregates-001/pg-aggregates-0098-b1e5567b.md) | SELECT corr(g, 'NaN'), regr_r2(g, 'NaN') FROM generate_series(1, 30) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0099-bed0f6ec](cases/aggregates-001/pg-aggregates-0099-bed0f6ec.md) | SELECT corr(0.1, 'NaN'), regr_r2(0.1, 'NaN') FROM generate_series(1, 30) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0100-3b815f6a](cases/aggregates-001/pg-aggregates-0100-3b815f6a.md) | SELECT corr('NaN', 0.1), regr_r2('NaN', 0.1) FROM generate_series(1, 30) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0101-7fc3b3aa](cases/aggregates-001/pg-aggregates-0101-7fc3b3aa.md) | SELECT corr('NaN', 'NaN'), regr_r2('NaN', 'NaN') FROM generate_series(1, 30) g; | Doris 执行失败 | NaN/Infinity、接近常数或极端尺度输入在 CAST/统计算法中不具有相同数值域或稳定性；目标 NULL/NaN/有限数表现见实际记录，不能用普通函数改名保证等价 | 除相关基本能力外，数值算法仍待研究 | 调查未完成 |
| [pg-aggregates-0104-6106ddbe](cases/aggregates-001/pg-aggregates-0104-6106ddbe.md) | SELECT count(*), sum(x), regr_sxx(y,x), sum(y),regr_syy(y,x), regr_sxy(y,x) FROM regr_test WHERE x IN (10… | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0105-de9d85b5](cases/aggregates-001/pg-aggregates-0105-de9d85b5.md) | SELECT count(*), sum(x), regr_sxx(y,x), sum(y),regr_syy(y,x), regr_sxy(y,x) FROM regr_test; | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0106-3a4b5ac2](cases/aggregates-001/pg-aggregates-0106-3a4b5ac2.md) | SELECT float8_accum('{4,140,2900}'::float8[], 100); | Doris 执行失败 | float8_accum/float8_combine 是 PG 内部聚合状态函数，Doris 没有已确认的同状态接口；输入/输出不是普通 SQL 标准统计值 | 不安排简单改名式补丁 | 原因已定位 |
| [pg-aggregates-0107-38a6d915](cases/aggregates-001/pg-aggregates-0107-38a6d915.md) | SELECT float8_regr_accum('{4,140,2900,1290,83075,15050,100,0}'::float8[], 200, 100); | Doris 执行失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0108-9eefe369](cases/aggregates-001/pg-aggregates-0108-9eefe369.md) | SELECT count(*), sum(x), regr_sxx(y,x), sum(y),regr_syy(y,x), regr_sxy(y,x) FROM regr_test WHERE x IN (10… | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0109-1472d5a7](cases/aggregates-001/pg-aggregates-0109-1472d5a7.md) | SELECT count(*), sum(x), regr_sxx(y,x), sum(y),regr_syy(y,x), regr_sxy(y,x) FROM regr_test WHERE x IN (80… | Doris 执行失败 | 社区保留 REGR_SXX/SYY/SXY/AVGX/AVGY/R2 名称后该 Doris 缺对应函数 | 缺口已确认，安全算法仍需研究 | 调查未完成 |
| [pg-aggregates-0110-2e0b20b6](cases/aggregates-001/pg-aggregates-0110-2e0b20b6.md) | SELECT float8_combine('{3,60,200}'::float8[], '{0,0,0}'::float8[]); | Doris 执行失败 | float8_accum/float8_combine 是 PG 内部聚合状态函数，Doris 没有已确认的同状态接口；输入/输出不是普通 SQL 标准统计值 | 不安排简单改名式补丁 | 原因已定位 |
| [pg-aggregates-0111-4b466106](cases/aggregates-001/pg-aggregates-0111-4b466106.md) | SELECT float8_combine('{0,0,0}'::float8[], '{2,180,200}'::float8[]); | Doris 执行失败 | float8_accum/float8_combine 是 PG 内部聚合状态函数，Doris 没有已确认的同状态接口；输入/输出不是普通 SQL 标准统计值 | 不安排简单改名式补丁 | 原因已定位 |
| [pg-aggregates-0112-6c1a5662](cases/aggregates-001/pg-aggregates-0112-6c1a5662.md) | SELECT float8_combine('{3,60,200}'::float8[], '{2,180,200}'::float8[]); | Doris 执行失败 | float8_accum/float8_combine 是 PG 内部聚合状态函数，Doris 没有已确认的同状态接口；输入/输出不是普通 SQL 标准统计值 | 不安排简单改名式补丁 | 原因已定位 |
| [pg-aggregates-0113-1a65bedb](cases/aggregates-001/pg-aggregates-0113-1a65bedb.md) | SELECT float8_regr_combine('{3,60,200,750,20000,2000,1,NaN}'::float8[], '{0,0,0,0,0,0,0,0}'::float8[]); | Doris 执行失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0114-d556fd00](cases/aggregates-001/pg-aggregates-0114-d556fd00.md) | SELECT float8_regr_combine('{0,0,0,0,0,0,0,0}'::float8[], '{2,180,200,740,57800,-3400,NaN,1}'::float8[]); | Doris 执行失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0115-561bfb29](cases/aggregates-001/pg-aggregates-0115-561bfb29.md) | SELECT float8_regr_combine('{3,60,200,750,20000,2000,7,8}'::float8[], '{2,180,200,740,57800,-3400,7,9}'::… | Doris 执行失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0121-6b24fa4d](cases/aggregates-001/pg-aggregates-0121-6b24fa4d.md) | SELECT newavg(four) AS avg_1 FROM onek; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0122-4ead625a](cases/aggregates-001/pg-aggregates-0122-4ead625a.md) | SELECT newsum(four) AS sum_1500 FROM onek; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0123-3d80ad43](cases/aggregates-001/pg-aggregates-0123-3d80ad43.md) | SELECT newcnt(four) AS cnt_1000 FROM onek; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0124-8a698015](cases/aggregates-001/pg-aggregates-0124-8a698015.md) | SELECT newcnt(*) AS cnt_1000 FROM onek; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0125-f5fb1ddf](cases/aggregates-001/pg-aggregates-0125-f5fb1ddf.md) | SELECT oldcnt(*) AS cnt_1000 FROM onek; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0126-43383f4c](cases/aggregates-001/pg-aggregates-0126-43383f4c.md) | SELECT sum2(q1,q2) FROM int8_tbl; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0129-89f16cca](cases/aggregates-001/pg-aggregates-0129-89f16cca.md) | SELECT sum(q1*2000), sum(-q1*2000), 2000*sum(q1) FROM int8_tbl; | 行值或顺序不匹配 | PG 的 BIGINT SUM 返回 NUMERIC；Doris BIGINT SUM 溢出，27407340740741226000 变成 8960596667031674384 | 需要类型感知设计，尚无全域可验收改写 | 调查未完成 |
| [pg-aggregates-0130-3caf0694](cases/aggregates-001/pg-aggregates-0130-3caf0694.md) | select ten, sum(distinct four) from onek a group by ten having exists (select 1 from onek b where sum(dis… | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0132-8462e8e9](cases/aggregates-001/pg-aggregates-0132-8462e8e9.md) | select (select max((select i.unique2 from tenk1 i where i.unique1 = o.unique1))) from tenk1 o; | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0134-429eb1f7](cases/aggregates-001/pg-aggregates-0134-429eb1f7.md) | select s1, s2, sm from generate_series(1, 3) s1, lateral (select s2, sum(s1 + s2) sm from generate_series… | SQLGlot 转译失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0136-4243166e](cases/aggregates-001/pg-aggregates-0136-4243166e.md) | select array(select sum(x+y) s from generate_series(1,3) y group by y order by s) from generate_series(1,… | SQLGlot 转译失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0137-2237979d](cases/aggregates-001/pg-aggregates-0137-2237979d.md) | select two + four as g, (select f1 from int4_tbl where f1 = (two + four)) from tenk1 t1 group by two + fo… | SQLGlot 转译失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0138-e2be6583](cases/aggregates-001/pg-aggregates-0138-e2be6583.md) | select q1, (select q1) as ss -- q1 is actually a COALESCE expression here from int8_tbl i81 full outer jo… | Doris 执行失败 | 历史 .out 成功，但当前 PG 18.1 原文执行失败 | 不能据本次执行确认通用补丁 | 前提阻断 |
| [pg-aggregates-0140-ba04d3f5](cases/aggregates-001/pg-aggregates-0140-ba04d3f5.md) | SELECT BIT_AND(i2) AS "?", BIT_OR(i4) AS "?", BIT_XOR(i8) AS "?" FROM bitwise_test; | Doris 执行失败 | MySQL 继承的 BIT_AND/BIT_OR/BIT_XOR 聚合名称被该 Doris 拒绝；BIT_AND_AGG 与 BITAND_AGG 两种候选也实际报函数不存在 | 暂不安排未经验证的名称替换 | 原因已定位 |
| [pg-aggregates-0143-5a8265a3](cases/aggregates-001/pg-aggregates-0143-5a8265a3.md) | SELECT -- boolean and transitions -- null because strict booland_statefunc(NULL, NULL) IS NULL AS "t", bo… | Doris 执行失败 | PG booland_statefunc/boolor_statefunc 是 STRICT 内部状态函数；普通 AND/OR 的三值逻辑不能替代 | 可研究专门状态函数支持，不并入 EVERY | 原因已定位 |
| [pg-aggregates-0144-32971c70](cases/aggregates-001/pg-aggregates-0144-32971c70.md) | SELECT -- boolean or transitions -- null because strict boolor_statefunc(NULL, NULL) IS NULL AS "t", bool… | Doris 执行失败 | PG booland_statefunc/boolor_statefunc 是 STRICT 内部状态函数；普通 AND/OR 的三值逻辑不能替代 | 可研究专门状态函数支持，不并入 EVERY | 原因已定位 |
| [pg-aggregates-0149-d636fc82](cases/aggregates-001/pg-aggregates-0149-d636fc82.md) | SELECT EVERY(b1) AS "f", EVERY(b2) AS "t", EVERY(b3) AS "f", EVERY(b4) AS "n", EVERY(NOT b2) AS "f", EVER… | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0169-fb0ce421](cases/aggregates-001/pg-aggregates-0169-fb0ce421.md) | select f1, (select min(unique1) from tenk1 where unique1 > f1) AS gt from int4_tbl; | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0173-5bef76d3](cases/aggregates-001/pg-aggregates-0173-5bef76d3.md) | select max(unique2) from tenk1 order by 1; | SQLGlot 转译失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0179-8eb5c0b1](cases/aggregates-001/pg-aggregates-0179-8eb5c0b1.md) | select max(unique2), generate_series(1,3) as g from tenk1 order by g desc; | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0246-3fc2fc89](cases/aggregates-001/pg-aggregates-0246-3fc2fc89.md) | select a, b from t_opf group by a, b order by b; | Doris 环境问题 | avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失 | 先处理类型和数据前提；Parser 缺口另行设计 | 前提阻断 |
| [pg-aggregates-0251-b9e80dc2](cases/aggregates-001/pg-aggregates-0251-b9e80dc2.md) | select a, count(*) from t_having group by a having a *= row(1.0)::avg_rec; | SQLGlot 转译失败 | avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失 | 先处理类型和数据前提；Parser 缺口另行设计 | 前提阻断 |
| [pg-aggregates-0253-f0a8749a](cases/aggregates-001/pg-aggregates-0253-f0a8749a.md) | select a, count(*) from t_having group by a having a *= any (array[row(1.0)::avg_rec]); | SQLGlot 转译失败 | avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失 | 先处理类型和数据前提；Parser 缺口另行设计 | 前提阻断 |
| [pg-aggregates-0255-476afef2](cases/aggregates-001/pg-aggregates-0255-476afef2.md) | select a, count(*) from t_having group by a having a = row(1.0)::avg_rec; | Doris 执行失败 | avg_rec 复合类型及比较/分组语义未在 Doris 建立；t_opf/t_having 缺失 | 先处理类型和数据前提；Parser 缺口另行设计 | 前提阻断 |
| [pg-aggregates-0264-e3b16e8d](cases/aggregates-001/pg-aggregates-0264-e3b16e8d.md) | select f1, count(*) from t1 x(x0,x1) left join (t1 left join t2 using(f1)) on (x0 = 0) group by f1; | Doris 执行失败 | Doris 拒绝基表别名的列名列表 t1 x(x0,x1) | 需 Schema 感知的投影/USING 类型方案 | 调查未完成 |
| [pg-aggregates-0265-6c4951ae](cases/aggregates-001/pg-aggregates-0265-6c4951ae.md) | select f2, count(*) from t1 x(x0,x1) left join (t1 left join t2 using(f2)) on (x0 = 0) group by f2; | Doris 执行失败 | Doris 拒绝基表别名的列名列表 t1 x(x0,x1) | 需 Schema 感知的投影/USING 类型方案 | 调查未完成 |
| [pg-aggregates-0267-c35cf02c](cases/aggregates-001/pg-aggregates-0267-c35cf02c.md) | select pg_get_viewdef('v1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0276-0f1f5154](cases/aggregates-001/pg-aggregates-0276-0f1f5154.md) | select array_agg(distinct val) from (select null as val from generate_series(1, 2)); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0283-9ca01715](cases/aggregates-001/pg-aggregates-0283-9ca01715.md) | select array_agg(a order by b) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0284-628b13e2](cases/aggregates-001/pg-aggregates-0284-628b13e2.md) | select array_agg(a order by a) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0285-ee2a7bc2](cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md) | select array_agg(a order by a desc) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0286-c689f198](cases/aggregates-001/pg-aggregates-0286-c689f198.md) | select array_agg(b order by a desc) from (values (1,4),(2,3),(3,1),(4,2)) v(a,b); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0287-a6b4ea06](cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md) | select array_agg(distinct a) from (values (1),(2),(1),(3),(null),(2)) v(a); | 行值或顺序不匹配 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0288-1528b423](cases/aggregates-001/pg-aggregates-0288-1528b423.md) | select array_agg(distinct a order by a) from (values (1),(2),(1),(3),(null),(2)) v(a); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0289-64071a98](cases/aggregates-001/pg-aggregates-0289-64071a98.md) | select array_agg(distinct a order by a desc) from (values (1),(2),(1),(3),(null),(2)) v(a); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0290-2bc98abf](cases/aggregates-001/pg-aggregates-0290-2bc98abf.md) | select array_agg(distinct a order by a desc nulls last) from (values (1),(2),(1),(3),(null),(2)) v(a); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0291-40c04ecb](cases/aggregates-001/pg-aggregates-0291-40c04ecb.md) | select aggfstr(a,b,c) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0292-68d79c0b](cases/aggregates-001/pg-aggregates-0292-68d79c0b.md) | select aggfns(a,b,c) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0293-3e365a0a](cases/aggregates-001/pg-aggregates-0293-3e365a0a.md) | select aggfstr(distinct a,b,c) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c), … | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0294-5412623b](cases/aggregates-001/pg-aggregates-0294-5412623b.md) | select aggfns(distinct a,b,c) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) v(a,b,c), g… | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0295-bf759c5f](cases/aggregates-001/pg-aggregates-0295-bf759c5f.md) | select aggfstr(distinct a,b,c order by b) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz'))… | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0296-a77bafc5](cases/aggregates-001/pg-aggregates-0296-a77bafc5.md) | select aggfns(distinct a,b,c order by b) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) … | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0297-ce288841](cases/aggregates-001/pg-aggregates-0297-ce288841.md) | select aggfns(distinct a,a,c order by c using ~<~,a) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(… | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0298-261e1b98](cases/aggregates-001/pg-aggregates-0298-261e1b98.md) | select aggfns(distinct a,a,c order by c using ~<~) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,… | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0299-d52780a5](cases/aggregates-001/pg-aggregates-0299-d52780a5.md) | select aggfns(distinct a,a,c order by a) from (values (1,3,'foo'),(0,null,null),(2,2,'bar'),(3,1,'baz')) … | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0300-a22a64cf](cases/aggregates-001/pg-aggregates-0300-a22a64cf.md) | select aggfns(distinct a,b,c order by a,c using ~<~,b) from (values (1,3,'foo'),(0,null,null),(2,2,'bar')… | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0301-8e89d955](cases/aggregates-001/pg-aggregates-0301-8e89d955.md) | select array_agg(distinct r order by r using <, r using *<) from (values (row(-0.0::float8)), (row(0.0::f… | SQLGlot 转译失败 | SQLGlot 不解析 ORDER BY USING < / *<；同族原查询此前触发 PostgreSQL 18.1 后端崩溃，本轮禁止重试 | 暂不实施；先解决安全执行条件 | 前提阻断 |
| [pg-aggregates-0303-8e89d955](cases/aggregates-001/pg-aggregates-0303-8e89d955.md) | select array_agg(distinct r order by r using <, r using *<) from (values (row(-0.0::float8)), (row(0.0::f… | SQLGlot 转译失败 | SQLGlot 不解析 ORDER BY USING < / *<；同族原查询此前触发 PostgreSQL 18.1 后端崩溃，本轮禁止重试 | 暂不实施；先解决安全执行条件 | 前提阻断 |
| [pg-aggregates-0304-1e9d5cdf](cases/aggregates-001/pg-aggregates-0304-1e9d5cdf.md) | select array_agg(r order by r using <, r using *<) from (values (row(-0.0::float8)), (row(0.0::float8))) … | SQLGlot 转译失败 | SQLGlot 不解析 ORDER BY USING < / *<；同族原查询此前触发 PostgreSQL 18.1 后端崩溃，本轮禁止重试 | 暂不实施；先解决安全执行条件 | 前提阻断 |
| [pg-aggregates-0306-e70870c4](cases/aggregates-001/pg-aggregates-0306-e70870c4.md) | select string_agg(distinct 'a', ','), sum(( select sum(1) from (values(1)) b(id) where a.id = b.id )) fro… | SQLGlot 转译失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0308-ad9e3ab0](cases/aggregates-001/pg-aggregates-0308-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0309-e95cf6b4](cases/aggregates-001/pg-aggregates-0309-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0311-ad9e3ab0](cases/aggregates-001/pg-aggregates-0311-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0312-e95cf6b4](cases/aggregates-001/pg-aggregates-0312-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0314-ad9e3ab0](cases/aggregates-001/pg-aggregates-0314-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0315-e95cf6b4](cases/aggregates-001/pg-aggregates-0315-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0317-ad9e3ab0](cases/aggregates-001/pg-aggregates-0317-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0318-e95cf6b4](cases/aggregates-001/pg-aggregates-0318-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0320-ad9e3ab0](cases/aggregates-001/pg-aggregates-0320-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0321-e95cf6b4](cases/aggregates-001/pg-aggregates-0321-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0323-ad9e3ab0](cases/aggregates-001/pg-aggregates-0323-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0324-e95cf6b4](cases/aggregates-001/pg-aggregates-0324-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0326-ad9e3ab0](cases/aggregates-001/pg-aggregates-0326-ad9e3ab0.md) | select * from agg_view1; | 行值或顺序不匹配 | 源返回 aggtype[] 的 PG 复合数组显示文本，Doris 返回 ARRAY<STRUCT> 的 JSON 显示；现有比较器未解码 PG 复合数组 | 不需改写这个 SELECT；完善类型映射/结构解码 | 原因已定位 |
| [pg-aggregates-0327-e95cf6b4](cases/aggregates-001/pg-aggregates-0327-e95cf6b4.md) | select pg_get_viewdef('agg_view1'::regclass); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0342-dddcf200](cases/aggregates-001/pg-aggregates-0342-dddcf200.md) | select string_agg(v, '') from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0344-dddcf200](cases/aggregates-001/pg-aggregates-0344-dddcf200.md) | select string_agg(v, '') from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0346-dddcf200](cases/aggregates-001/pg-aggregates-0346-dddcf200.md) | select string_agg(v, '') from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0347-431bb4d7](cases/aggregates-001/pg-aggregates-0347-431bb4d7.md) | select string_agg(v, NULL) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0348-e9f2b704](cases/aggregates-001/pg-aggregates-0348-e9f2b704.md) | select string_agg(v, decode('ee', 'hex')) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0349-87cb7e26](cases/aggregates-001/pg-aggregates-0349-87cb7e26.md) | select min(v) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0350-1159bcab](cases/aggregates-001/pg-aggregates-0350-1159bcab.md) | select max(v) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0353-87cb7e26](cases/aggregates-001/pg-aggregates-0353-87cb7e26.md) | select min(v) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0354-1159bcab](cases/aggregates-001/pg-aggregates-0354-1159bcab.md) | select max(v) from bytea_test_table; | Doris 环境问题 | Doris 的 bytea_test_table 未准备：BYTEA 二进制域映射仍受限 | 目前不安排 SQLGlot 补丁 | 前提阻断 |
| [pg-aggregates-0371-e4fde69d](cases/aggregates-001/pg-aggregates-0371-e4fde69d.md) | select array_dims(array_agg(s)) from (select * from pagg_test) s; | Doris 执行失败 | PG 表别名 s 在聚合参数中代表整行复合值，目标当成不存在的标量列；还叠加 ARRAY_DIMS 与 PG 数组维度语义，单改 ARRAY_AGG 不足 | 需 Schema/整行值与数组维度独立方案 | 原因已定位 |
| [pg-aggregates-0380-caa8b35c](cases/aggregates-001/pg-aggregates-0380-caa8b35c.md) | select min(unique1) filter (where unique1 > 100) from tenk1; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0381-b9be07f7](cases/aggregates-001/pg-aggregates-0381-b9be07f7.md) | select sum(1/ten) filter (where ten > 0) from tenk1; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0382-9b691678](cases/aggregates-001/pg-aggregates-0382-9b691678.md) | select ten, sum(distinct four) filter (where four::text ~ '123') from onek a group by ten; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0383-ae4a4309](cases/aggregates-001/pg-aggregates-0383-ae4a4309.md) | select ten, sum(distinct four) filter (where four > 10) from onek a group by ten having exists (select 1 … | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0384-e4a241c8](cases/aggregates-001/pg-aggregates-0384-e4a241c8.md) | select max(foo COLLATE "C") filter (where (bar collate "POSIX") > '0') from (values ('a', 'b')) AS v(foo,… | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0385-51f943b1](cases/aggregates-001/pg-aggregates-0385-51f943b1.md) | select any_value(v) filter (where v > 2) from (values (1), (2), (3)) as v (v); | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0387-68e5c03f](cases/aggregates-001/pg-aggregates-0387-68e5c03f.md) | select (select count(*) filter (where outer_c <> 0) from (values (1)) t0(inner_c)) from (values (2),(3)) … | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0388-a7ae3863](cases/aggregates-001/pg-aggregates-0388-a7ae3863.md) | select (select count(inner_c) filter (where outer_c <> 0) from (values (1)) t0(inner_c)) from (values (2)… | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0389-fc7103c6](cases/aggregates-001/pg-aggregates-0389-fc7103c6.md) | select (select max((select i.unique2 from tenk1 i where i.unique1 = o.unique1)) filter (where o.unique1 <… | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0390-d0eefd0f](cases/aggregates-001/pg-aggregates-0390-d0eefd0f.md) | select sum(unique1) FILTER (WHERE unique1 IN (SELECT unique1 FROM onek where unique1 < 100)) FROM tenk1; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0391-fce06d52](cases/aggregates-001/pg-aggregates-0391-fce06d52.md) | select aggfns(distinct a,b,c order by a,c using ~<~,b) filter (where a > 1) from (values (1,3,'foo'),(0,n… | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0392-17dd7649](cases/aggregates-001/pg-aggregates-0392-17dd7649.md) | select max(0) filter (where b1) from bool_test; | Doris 执行失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0393-8196c25e](cases/aggregates-001/pg-aggregates-0393-8196c25e.md) | select (select max(0) filter (where b1)) from bool_test; | Doris 执行失败 | 涉及相关聚合的归属层级、标量子查询或投影/LATERAL 集合返回函数；当前候选只证明已列固定数据的行为，不能用普通表达式改名代替查询级重写 | 部分基础 task 可修；查询级算法待补证 | 调查未完成 |
| [pg-aggregates-0398-73d63cba](cases/aggregates-001/pg-aggregates-0398-73d63cba.md) | select p, percentile_cont(p) within group (order by x::float8) from generate_series(1,5) x, (values (0::f… | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0402-03bcfbf3](cases/aggregates-001/pg-aggregates-0402-03bcfbf3.md) | select percentile_cont(0.5) within group (order by b) from aggtest; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0403-1e765a0a](cases/aggregates-001/pg-aggregates-0403-1e765a0a.md) | select percentile_cont(0.5) within group (order by b), sum(b) from aggtest; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0404-565ced59](cases/aggregates-001/pg-aggregates-0404-565ced59.md) | select percentile_cont(0.5) within group (order by thousand) from tenk1; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0405-3dbf4d44](cases/aggregates-001/pg-aggregates-0405-3dbf4d44.md) | select percentile_disc(0.5) within group (order by thousand) from tenk1; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0406-5e4718d4](cases/aggregates-001/pg-aggregates-0406-5e4718d4.md) | select rank(3) within group (order by x) from (values (1),(1),(2),(2),(3),(3),(4)) v(x); | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0407-dea6404c](cases/aggregates-001/pg-aggregates-0407-dea6404c.md) | select cume_dist(3) within group (order by x) from (values (1),(1),(2),(2),(3),(3),(4)) v(x); | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0408-e463cacf](cases/aggregates-001/pg-aggregates-0408-e463cacf.md) | select percent_rank(3) within group (order by x) from (values (1),(1),(2),(2),(3),(3),(4),(5)) v(x); | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0409-d4deac02](cases/aggregates-001/pg-aggregates-0409-d4deac02.md) | select dense_rank(3) within group (order by x) from (values (1),(1),(2),(2),(3),(3),(4)) v(x); | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0410-f6f52dc3](cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md) | select percentile_disc(array[0,0.1,0.25,0.5,0.75,0.9,1]) within group (order by thousand) from tenk1; | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0411-b38c2a1f](cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md) | select percentile_cont(array[0,0.25,0.5,0.75,1]) within group (order by thousand) from tenk1; | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0412-cbdaef84](cases/aggregates-001/pg-aggregates-0412-cbdaef84.md) | select percentile_disc(array[[null,1,0.5],[0.75,0.25,null]]) within group (order by thousand) from tenk1; | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0413-6ccabd9a](cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md) | select percentile_cont(array[0,1,0.25,0.75,0.5,1,0.3,0.32,0.35,0.38,0.4]) within group (order by x) from … | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0414-66a94e8f](cases/aggregates-001/pg-aggregates-0414-66a94e8f.md) | select ten, mode() within group (order by string4) from tenk1 group by ten; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0415-16b30942](cases/aggregates-001/pg-aggregates-0415-16b30942.md) | select percentile_disc(array[0.25,0.5,0.75]) within group (order by x) from unnest('{fred,jim,fred,jack,j… | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0416-a678f5c1](cases/aggregates-001/pg-aggregates-0416-a678f5c1.md) | select pg_collation_for(percentile_disc(1) within group (order by x collate "POSIX")) from (values ('fred… | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0417-277c66fb](cases/aggregates-001/pg-aggregates-0417-277c66fb.md) | select test_rank(3) within group (order by x) from (values (1),(1),(2),(2),(3),(3),(4)) v(x); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0418-748c83ea](cases/aggregates-001/pg-aggregates-0418-748c83ea.md) | select test_percentile_disc(0.5) within group (order by thousand) from tenk1; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0426-31226e20](cases/aggregates-001/pg-aggregates-0426-31226e20.md) | select rank('adam'::varchar) within group (order by x) from (values ('fred'),('jim')) v(x); | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0427-1ad928b9](cases/aggregates-001/pg-aggregates-0427-1ad928b9.md) | select rank('3') within group (order by x) from generate_series(1,5) x; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0428-5c5a2a90](cases/aggregates-001/pg-aggregates-0428-5c5a2a90.md) | select percent_rank(0) within group (order by x) from generate_series(1,0) x; | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0430-b1f99924](cases/aggregates-001/pg-aggregates-0430-b1f99924.md) | select pg_get_viewdef('aggordview1'); | Doris 执行失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0433-90ca229d](cases/aggregates-001/pg-aggregates-0433-90ca229d.md) | select least_agg(q1,q2) from int8_tbl; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0434-5da33736](cases/aggregates-001/pg-aggregates-0434-5da33736.md) | select least_agg(variadic array[q1,q2]) from int8_tbl; | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0435-9277b1b7](cases/aggregates-001/pg-aggregates-0435-9277b1b7.md) | select cleast_agg(q1,q2) from int8_tbl; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0436-476708aa](cases/aggregates-001/pg-aggregates-0436-476708aa.md) | select cleast_agg(4.5,f1) from int4_tbl; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0437-d68f01c2](cases/aggregates-001/pg-aggregates-0437-d68f01c2.md) | select cleast_agg(variadic array[4.5,f1]) from int4_tbl; | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0438-998adec3](cases/aggregates-001/pg-aggregates-0438-998adec3.md) | select pg_typeof(cleast_agg(variadic array[4.5,f1])) from int4_tbl; | SQLGlot 转译失败 | 查询的是 PostgreSQL 目录/反解析/原生类型或排序规则身份，不是跨库共同数据结果；Doris 不具备同一 PG catalog | 不安排按固定输出伪造 catalog 的 SQLGlot 修复 | 原因已定位 |
| [pg-aggregates-0456-ace8bfc0](cases/aggregates-001/pg-aggregates-0456-ace8bfc0.md) | select my_avg(one),my_avg(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0457-760d6f2a](cases/aggregates-001/pg-aggregates-0457-760d6f2a.md) | select my_avg(one),my_sum(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0458-c9c45da8](cases/aggregates-001/pg-aggregates-0458-c9c45da8.md) | select my_avg(distinct one),my_sum(distinct one) from (values(1),(3),(1)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0459-6dcd9e87](cases/aggregates-001/pg-aggregates-0459-6dcd9e87.md) | select my_avg(distinct one),my_sum(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0460-a2e1068b](cases/aggregates-001/pg-aggregates-0460-a2e1068b.md) | select my_avg(one) filter (where one > 1),my_sum(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0461-2928ead0](cases/aggregates-001/pg-aggregates-0461-2928ead0.md) | select my_avg(one),my_sum(two) from (values(1,2),(3,4)) t(one,two); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0462-507973b2](cases/aggregates-001/pg-aggregates-0462-507973b2.md) | select percentile_cont(0.5) within group (order by a), percentile_disc(0.5) within group (order by a) fro… | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0463-fb0a8e65](cases/aggregates-001/pg-aggregates-0463-fb0a8e65.md) | select percentile_cont(0.25) within group (order by a), percentile_disc(0.5) within group (order by a) fr… | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0464-1a2659a1](cases/aggregates-001/pg-aggregates-0464-1a2659a1.md) | select rank(4) within group (order by a), dense_rank(4) within group (order by a) from (values(1),(3),(5)… | Doris 执行失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0468-863e535b](cases/aggregates-001/pg-aggregates-0468-863e535b.md) | select my_sum_init(one),my_avg_init(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0469-b5c0f3a2](cases/aggregates-001/pg-aggregates-0469-b5c0f3a2.md) | select my_sum_init(one),my_avg_init2(one) from (values(1),(3)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0476-10fb059b](cases/aggregates-001/pg-aggregates-0476-10fb059b.md) | select my_sum(one),my_half_sum(one) from (values(1),(2),(3),(4)) t(one); | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0481-e31d0ffb](cases/aggregates-001/pg-aggregates-0481-e31d0ffb.md) | SELECT balk(hundred) FROM tenk1; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0505-e2ced71d](cases/aggregates-001/pg-aggregates-0505-e2ced71d.md) | SELECT avg(c1.f ORDER BY c1.x, c1.y) FROM group_agg_pk c1 JOIN group_agg_pk c2 ON c1.x = c2.x GROUP BY c1… | Doris 执行失败 | 普通聚合内 ORDER BY 被原样输出；Doris 对 MIN 报错参数个数，对 AVG 不支持该调用形式 | 待明确可安全丢排序的条件，或给 unsupported 诊断 | 调查未完成 |
| [pg-aggregates-0527-e31d0ffb](cases/aggregates-001/pg-aggregates-0527-e31d0ffb.md) | SELECT balk(hundred) FROM tenk1; | Doris 执行失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0534-1b68ef98](cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) | SELECT eatarray(rwagg(ARRAY[1.0::real])), eatarray(rwagg(ARRAY[1.0::real])); | SQLGlot 转译失败 | 原脚本自定义聚合/函数在 Doris 未定义 | 仅关联基础 task；UDF 定义迁移另行处理 | 原因已定位 |
| [pg-aggregates-0544-3a307492](cases/aggregates-001/pg-aggregates-0544-3a307492.md) | SELECT variance(unique1::int4), sum(unique1::int8), regr_count(unique1::float8, unique1::float8) FROM (SE… | Doris 执行失败 | REGR_COUNT 未映射，普通成对计数候选使查询可执行；其余 VAR_SAMP/SUM 返回类型及数值精度仍有差异，不把整条标为已修复 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0546-739e31be](cases/aggregates-001/pg-aggregates-0546-739e31be.md) | SELECT variance(unique1::int8), avg(unique1::numeric) FROM (SELECT * FROM tenk1 UNION ALL SELECT * FROM t… | 行值或顺序不匹配 | 源与目标的统计/聚合返回类型、累计精度或有限浮点算法存在差异；已用 PG 二进制读取排查显示舍入，实际数值/类型见分维度证据 | 尚无保全源类型与数值域的通用补丁 | 调查未完成 |
| [pg-aggregates-0548-bcd73bfc](cases/aggregates-001/pg-aggregates-0548-bcd73bfc.md) | SELECT dense_rank(x) WITHIN GROUP (ORDER BY x) FROM (VALUES (1),(1),(2),(2),(3),(3)) v(x) GROUP BY (x) OR… | SQLGlot 转译失败 | WITHIN GROUP 有序集合/假想集合语法直接输出后被 Doris 拒绝；连续分位数常量、离散分位数、众数及假想排名需要不同实现 | 基础 task 之外，待查询级设计和类型/边界证据 | 原因已定位 |
| [pg-aggregates-0549-9bc0dfb2](cases/aggregates-001/pg-aggregates-0549-9bc0dfb2.md) | SELECT min(x ORDER BY y) FROM (VALUES(1, NULL)) AS d(x,y); | Doris 执行失败 | 普通聚合内 ORDER BY 被原样输出；Doris 对 MIN 报错参数个数，对 AVG 不支持该调用形式 | 待明确可安全丢排序的条件，或给 unsupported 诊断 | 调查未完成 |
| [pg-aggregates-0550-cff4ea50](cases/aggregates-001/pg-aggregates-0550-cff4ea50.md) | SELECT min(x ORDER BY y) FROM (VALUES(1, 2)) AS d(x,y); | Doris 执行失败 | 普通聚合内 ORDER BY 被原样输出；Doris 对 MIN 报错参数个数，对 AVG 不支持该调用形式 | 待明确可安全丢排序的条件，或给 unsupported 诊断 | 调查未完成 |
| [pg-aggregates-0551-f476de2c](cases/aggregates-001/pg-aggregates-0551-f476de2c.md) | select v\|\|'a', case v\|\|'a' when 'aa' then 1 else 0 end, count(*) from unnest(array['a','b']) u(v) group b… | SQLGlot 转译失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |
| [pg-aggregates-0552-7ea82af2](cases/aggregates-001/pg-aggregates-0552-7ea82af2.md) | select v\|\|'a', case when v\|\|'a' = 'aa' then 1 else 0 end, count(*) from unnest(array['a','b']) u(v) group… | SQLGlot 转译失败 | 锁定版本继承 MySQL 的数组/NULL 排序/聚合生成约定，或保留了目标不支持的函数/调用形式；具体 AST 缺口与实际候选在下文，相关独立 task 分别验收 | 需修改，但不承诺本条全部匹配 | 原因已定位 |

## 6. 原因汇总

原因可重叠，不能相加作为查询总数；task 数量也不是缺陷查询数。

| 有证据的原因 | 涉及查询数 | 独立问题口径 | 处理方向 |
| :--- | ---: | :--- | :--- |
| SQLGlot 解析/生成缺口 | 128 | 9 个可实施 task，另有查询级/运算符/类型待研究，未把整个类别计为一个缺陷 | 见逐条结论与待补证事项 |
| Doris 执行语义差异 | 63 | 小样本 NULL 有受限补偿 task；精度/类型/非有限域没有统一安全补丁 | 见逐条结论与待补证事项 |
| Doris 能力限制 | 106 | 目录、内部状态、UDF、有序集合等多类；尚未找到候选不等于永远不可模拟 | 见逐条结论与待补证事项 |
| 框架/驱动问题 | 12 | 显示数值、嵌套类型声明、复合数组解码；不安排伪 SQLGlot 修复 | 见逐条结论与待补证事项 |
| 数据/会话/输出前提 | 37 | 6 未映射对象、继承与历史 PG 行为、3 安全阻断；外部准备处理 | 见逐条结论与待补证事项 |
| 尚未确定 | 0 | 逐条保留需要补证的原因，不凭自动标签确认缺陷 | 见逐条结论与待补证事项 |

<a id="tasks"></a>

## 7. SQLGlot 修复任务索引

### 功能提交重建计划（2026-11-24，补救历史未提交改动）

本次已获本地拆分重建/commit授权，不push、不新增转换规则。原`../sqlglot-experiment`保留不动，HEAD为`089891f2521780e2c5b243005017af9db62f25a6`，原8个改动文件最终diff SHA256为`32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73`。重建位置为`../sqlglot-functional-commits`，分支`codex/doris-functional-commits`，从同一基线开始，不复刻旧轮次时间或假造历史SHA。

拟按依赖保存约12个语义提交：数组构造(task-001)、NULL排序(task-002)、数组聚合NULL/空输入(task-003)、聚合值自身排序(task-004，依赖前者)、普通聚合FILTER(task-005)、EVERY(task-006)、小样本NULL(task-007)、常量序列及NULL参数(task-008，合并原两轮的同一能力)、REGR_COUNT(task-009)、数组源类型保留(task-001，含AST/公共生成器基础)、整数/Boolean输入(task-001)、浮点输入(task-001)。各项配套测试随代码提交，不按文件或fix轮次分割；真实不可分割的依赖需在此说明后调整。

每个阶段在不含未来功能的准确工作树中运行PG/Doris/MySQL相关测试及全部方言回归，涉及公共AST/生成器时增加核心测试；提交前检查暂存内容、提交后核对SHA和干净状态。最后逐字节比对所有跟踪文件，重跑原142条/19阶段及已有97+41边界的必要最终回归，明确未覆盖项。task-001/003未验收状态保留，其实验性子项按本次授权保存；不得用代码重建完成取代SQL能力验收。新SHA/依赖/真实测试追加到本汇总及各任务已有修复报告，不覆盖过去“未提交”的事实，也不新增台账。以下清单仍反映功能验收状态；重建结果在执行后补充。

<a id="functional-commit-recovery"></a>

### 功能提交重建结果（2026-11-24）

**已将8个文件中混合的既有修改重建为12个本地功能提交，未push、未创建Issue/PR。** 这不是恢复过去每轮的精确补丁或提交时间，而是在同一基线上重新组织现在已有的代码与测试；没有增加新转换能力。

后续继续修复使用 `../sqlglot-functional-commits`（绝对路径 `../sqlglot-functional-commits`），分支 `codex/doris-functional-commits`，重建完成当时HEAD为 `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`。原 `../sqlglot-experiment` 的分支、HEAD、8个未提交文件及未跟踪内容均未清理或覆盖，仍作为原状态保留；它没有因新分支提交而自动变干净。社区checkout `../sqlglot` 未修改。

#### 提交范围、父提交与测试

下表按实际Git父子顺序排列：第1项父提交是 `089891f2521780e2c5b243005017af9db62f25a6`，其后每项的父提交就是上一行的完整SHA。所有提交仅在本地，可用 `git show <SHA>` 查看；未推送的SHA目前没有可访问的fork远程提交页面。

“定向 / 全部方言”是两组unittest方法数，定向为Doris、PostgreSQL、MySQL三个模块，已包含在全部方言中，**不能相加**。填写实际准确代码状态的结果；未单独运行的组不从最终状态倒填为通过。每项提交前核对diff和测试，提交后核对工作区干净。核心组结果单列；注明“含定向”的数字是合并组方法总数，不是额外新增测试数。

| 顺序 | 功能与task | 本地commit（完整SHA） | 定向 / 全部方言通过数 | 额外核心测试通过数 |
| :--- | :--- | :--- | ---: | :--- |
| 1 | task-001：ARRAY 构造与 Doris Parser；拒绝 ARRAY 子查询构造 | `4d5cf168daac70cddba9a7edda81cd7646cc302d` | 136 / 1059 | 本阶段未另跑核心组 |
| 2 | task-002：原生 NULLS FIRST/LAST 排序 | `64d2701093f675f7b757510d5fdbfb04fa53c3ec` | 137 / 1060 | 本阶段未另跑核心组 |
| 3 | task-003：ARRAY_AGG 保留 NULL / 空输入返回 SQL NULL | `d0fcf8f16af727bcfac9993792fa2c9a1be2b766` | 140 / 1063 | 199 |
| 4 | task-004：ARRAY_AGG 按聚合值自身排序 | `4052036e400c7ce0fe24ef6132fb5b17bf930a50` | 143 / 1066 | 本阶段未另跑核心组 |
| 5 | task-005：普通聚合 FILTER 转换 | `4a3bd8ab312bda4c993c3b08e5806c14e4ae7f2e` | 145 / 1068 | 本阶段未另跑核心组 |
| 6 | task-006：PostgreSQL EVERY 归一化为 LogicalAnd | `872a926e936e8c12bc3681da4105c85ac2fcb778` | 147 / 1070 | 本阶段未另跑核心组 |
| 7 | task-007：小样本统计聚合返回 NULL | `0ef0f5173ef4420a8e43b58beea07dc5a3646af0` | 150 / 1073 | 199 |
| 8 | task-008：FROM 常量 INT4 序列，包含 NULL 参数 | `be0918f1a48384e1f842d8705afc05824fc3eb36` | 154 / 1077 | 本阶段未另跑核心组 |
| 9 | task-009：REGR_COUNT 成对非 NULL 计数 | `f7492dc5b7e3d999ced4429d69ceed7ed4a6f1d8` | 156 / 1079 | 本阶段未另跑核心组 |
| 10 | task-001：数组源元素类型：Parser、AST 与公共/目标 Generator | `696de7c98a06eff49b6ba83a70d345457fe641db` | 158 / 1081 | 278 |
| 11 | task-001：数组 unknown 整数/Boolean 输入与显式 CAST | `523cd4c161d7a83d4ad56a534c74d29bf3c3921a` | 159 / 1082 | 278 |
| 12 | task-001：有限十进制浮点输入、精确舍入与运行时 REAL 转换 | `51bf6a4085c5036a236f0ebfa5a720cab5dfb019` | 160 / 1083 | 438（含160项定向） |
| 13 | task-001：有限 REAL 字面量 CAST 链与负号顺序（fix-015） | `365986d92f426fa6c837d3fc60ba6a41acd0770c` | 161 / 1084 | 439（含161项定向） |
| 14 | task-001：有限标量投影的 REAL 转换（fix-016） | `6e92c3f330ea17d6458baf656c7731012dfec95b` | 162 / 未单独运行 | 333（含162项定向） |
| 15 | task-001：十六进制浮点数组输入（fix-016） | `be74c6b42e63d129d6aa116bab90bac46abc6394` | 163 / 未单独运行 | 334（含163项定向） |
| 16 | task-001：NaN/Infinity 浮点数组输入（fix-016） | `9c3b30efc6aedaf54c3327d44f4ca231d39e3d97` | 164 / 未单独运行 | 335（含164项定向） |
| 17 | task-001：显式 DOUBLE→REAL 的运行时数组转换（fix-016） | `ce841540a49228d9114a0346abc84283abcbe4c2` | 165 / 1088 | 443（含165项定向） |
| 18 | task-001：非有限输入 ASCII 拼写保护补漏（fix-016） | `6922457c6d223eafb1e3e7c1aaab211f88487874` | 165 / 1088 | 443（含165项定向） |

顺序体现可验证的父提交状态，不意味着任意一行都能脱离前序提交单独cherry-pick。第4项复用第3项的数组聚合NULL/空输入实现；第10项在第1项构造能力上添加源类型元信息及公共生成基础，第11项依赖第10项，第12项依赖第10/11项的类型和输入转换入口。其他任务的功能边界独立，但交互回归会使用前序能力，移植时必须复查测试依赖。第8项合并fix-008/009的常量序列及NULL补齐，因为它们属于同一规则；第10–12项拆分task-001的不同可验证行为，不机械按fix轮次或文件分commit。公共AST、Parser、Generator及其测试随对应规则一起提交，没有另作“所有源码 / 所有测试”式拆分。

第1项初跑全部方言时曾有1项环境错误：lazy-load测试启动的子进程找不到 `python`。补齐测试PATH后，在干净的第1项commit上重跑1059项全部通过；没有修改或amend该提交。重建中发现的中间状态组装错误也在对应提交前修正，表中记录的是修正后的实际通过结果，不把失败尝试计作通过。

#### 最终内容和环境核对

- 比对全部364个跟踪文件的内容/可执行属性，均与原实验目录最终状态一致；子模块 `sqlglot-integration-tests` 的Git引用同为 `e1e97091c6b83a87596cd8a94bdc62a75dd620cd`，未额外拉取或声称运行其集成测试。
- 新HEAD相对基线的 `git diff --binary` SHA256 与原目录未提交diff均为 `32db8ab6ab081f983e9e0d473f36e7063014c38c43b7091b99c2e6d6e40a8e73`，净差异仍为8文件、1588增加/22删除。原目录HEAD与该指纹均未改变。
- 最终438项定向/核心测试、1083项全部方言测试通过；最终commit后另跑160项定向测试通过。Ruff检查全部8个变动文件通过；格式检查四个Parser/Generator/方言测试文件通过，未为格式化重写其他基线文件。
- 单测用 `../sqlglot-experiment/.venv/bin/python`，实际import为新checkout的 `sqlglot/__init__.py`，报告版本字符串为 `30.25.1.dev355`；数据库回归用 `../doris-sql-validator/.venv/bin/python` 加 `PYTHONPATH=../sqlglot-functional-commits:src`，实际import同一新源码，版本字符串为 `30.25.1.dev6`。两个环境的安装元数据不同，因此以实际import路径、完整Git SHA及内容核对共同识别代码，不仅凭版本字符串认定源码。
- 核心组为 `tests.test_expressions/test_parser/test_generator/test_transpile/test_tokens/test_build/test_schema/test_lineage`；第3/7项运行其中199项子集，第10/11项运行完整278项，第12项加160项方言定向合计438项。全部方言由unittest discovery加载 `tests/dialects/test_*.py`。
- 未运行完整optimizer、mypy、C扩展或 `make check`；没有为此安装/升级依赖。单测通过不是完整SQL语义验收，也不证明任意边界已覆盖。

#### 最终数据库回归

实际在上述新HEAD执行，而非重放手写候选：原查询通过 `CliRunner.invoke(app, ["run", "--path", <各实际阶段YAML>, "--stdout", "--id", ...])`；边界使用 `parse_one(..., read="postgres").sql("doris", unsupported_level=RAISE)`，再调用 `execute_query/compare_probe`。沿用固定SQL/.out、阶段数据库、Session、10秒/10000行限制和比较策略；只读查询，不改数据，不生成新的JSON/日志/证据目录。前一轮各边界的源SQL和逐条事实继续见[fix-013](../fixes/tasks/aggregates-001/fix-013/task-001.md)及[fix-014](../fixes/tasks/aggregates-001/fix-014/task-001.md)。

| 重跑范围 | 本次结果 | 与重建前相比 |
| :--- | :--- | :--- |
| 142条原查询、19个实际stage | 82匹配、36 Doris执行失败、19值/顺序不同、1转译失败、4源端负向 | 全部逐ID一致，缺失ID为0；不是全部313条/43阶段最终验收 |
| 97条既有数组边界 | 双端成功、重复稳定；74值一致、23 Boolean显示不同保留 | 与fix-014相同，没有放宽比较器 |
| 41条浮点相关边界 | PG二进制查询和Doris查询成功且重复稳定，逐元素原生等值/NULL核验全部通过，已取得元素类型保持；主比较仍25值一致、15显示不同、1源驱动解码失败 | 与fix-014相同；原生核验通过不冒称41条主流程MATCH |
| 两条已知REAL元素CAST控制 | `ARRAY['1e2','7.038531e-26'::REAL]`第二元素等值为0；`ARRAY['1e2',0.1::REAL,2::DOUBLE PRECISION]`第二元素也为0；均可重复 | 已知真值差异仍存在，未假称修复 |

41条中 `double-edge-1` 的源文本驱动仍抛 `OverflowError: value too large to convert to float`，同源SQL的PG二进制读取与目标原生核验成功；这是驱动解码问题，不是源端负向，也不写MATCH。没有重新执行有后端风险记录的301/303/304，也没有重新跑历轮全部独立任务边界；本次结论仅是代码内容保持及上述固定范围无回退。

**重建完成当时仍为7项完成约定验收、2项已修改但未完成验收，整份输入未完成。** task-001/003的代码按本次授权保存为本地提交，不因此关闭类型、精度等余项；当时安排的下一功能修复是原task-001“已知REAL元素自身CAST精度”，具体方案见其原条目。各任务最近报告已补写提交对应关系，原轮次中的“当时未提交”保留为历史事实。当前已推进到fix-017，另已登记未实施的task-010；以最新任务表和条目为准。

以下是唯一当前修复清单：初轮9项、fix-017的task-010及fix-018的3项百分位前置能力，共13项；10项完成各自约定验收，task-001/003已修改但未完成，task-010未实施。是否完成以“当前状态 / 最近实际报告”为准；初轮9项及原313条查询的数量不因边界发现改变。各条目的初始依据不覆盖后续实际结果。fix-018后共24个本地修复commit，尚未推送；不创建社区PR。最新SHA见本页开头；不能把首轮锁定版本缺口直接称为最新main缺口。

| task 与详细计划 | 目标 | 关联 Case 数 | 独立修复 / 实现依赖 | 优先级 | 当前状态 / 最近实际报告 |
| :--- | :--- | ---: | :--- | :--- | :--- |
| [task-001](#task-001) | Doris 数组字面量生成 | 14 | 独立规则；子项依赖既有数组类型/浮点基础 | 高 | 已修改但未完成；最新[fix-020](../fixes/tasks/aggregates-001/fix-020/task-001.md)纠正源Parser的目标耦合，补已知类型下的一维文本子数组输入，两项独立commit。20条原生边界/5条escape控制通过，原14条仍3匹配/6显示不同/4目标失败/1转译失败。旧NUMERIC/REAL补偿通用性及研究限制分开审查，不以样本成功关闭整个任务 |
| [task-002](#task-002) | Doris 使用原生 NULLS FIRST/LAST 排序 | 6 | 独立规则；无必须依赖 | 高 | 已修复并完成约定验收；[fix-002](../fixes/tasks/aggregates-001/fix-002/task-002.md)，已本地提交、未推送（SHA见上表） |
| [task-003](#task-003) | ARRAY_AGG 保留 NULL 并补偿空输入 | 10 | 独立规则；无必须依赖 | 高 | 已修改但未完成验收；最新[fix-011类型核验](../fixes/tasks/aggregates-001/fix-011/task-003.md)，VALUES元素类型、Decimal结果约束与原差异保留；原NULL/空输入实现见fix-003 |
| [task-004](#task-004) | ARRAY_AGG 按聚合值自身排序 | 5 | 独立规则；复用 task-003 已实现的 NULL/空输入基础，未关闭其类型余项 | 中 | 已修复并完成约定整数排序验收；[fix-004](../fixes/tasks/aggregates-001/fix-004/task-004.md)，完整原 Case 仍有类型/表示差异 |
| [task-005](#task-005) | 普通忽略 NULL 聚合的 FILTER 转换 | 8 | 独立规则；无必须依赖 | 高 | 已修复并完成条件筛选规则约定验收；[fix-005](../fixes/tasks/aggregates-001/fix-005/task-005.md)，原生聚合/类型及相关查询差异仍保留 |
| [task-006](#task-006) | PostgreSQL EVERY 归一化与 Doris 布尔聚合 | 1 | 独立规则；无必须依赖 | 中 | 已修复并完成普通 BOOLEAN 聚合约定验收；[fix-006](../fixes/tasks/aggregates-001/fix-006/task-006.md)，已本地提交、未推送（SHA见上表） |
| [task-007](#task-007) | 样本统计聚合在有效样本不足时返回 NULL | 7 | 独立规则；无必须依赖 | 中 | 已修复并完成有限输入小样本 NULL 规则验收；[fix-007](../fixes/tasks/aggregates-001/fix-007/task-007.md)，原 .out 显示、NUMERIC 类型及浮点/非有限数余项保留 |
| [task-008](#task-008) | FROM 位置的常量整数 GENERATE_SERIES | 32 | 独立规则；无必须依赖 | 中 | 已修复并完成常量 INT4/NULL 序列约定验收；[fix-009](../fixes/tasks/aggregates-001/fix-009/task-008.md)，其他独立 Case 问题保留；已本地提交、未推送（SHA见上表） |
| [task-009](#task-009) | REGR_COUNT 成对非 NULL 计数 | 2 | 独立规则；无必须依赖 | 中 | 已修复并完成普通数值参数成对计数约定验收；[fix-010](../fixes/tasks/aggregates-001/fix-010/task-009.md)，0544 的统计/SUM 余项保留；已本地提交、未推送（SHA见上表） |
| [task-010](#task-010) | Doris 数组下标位置与越界行为 | 本轮13条文本投影及3条INT控制，不计入原313 | 独立规则；不是NUMERIC输入转换 | 高 | 未实施；源[1]生成目标[0]，源[0]生成目标[-1]并错误取到末元素。须独立验证正负/动态下标、NULL、嵌套及Map/JSON隔离，不能只全局加1 |
| [task-011](#task-011) | 常量数组连续百分位 | 2：0411、0413 | 概率上下文依赖task-001；与离散算法分开 | 高 | 已修复并完成有限数值/字面量概率规则验收；[fix-018](../fixes/tasks/aggregates-001/fix-018/task-011.md)，fa20f2cf768dc09e887eb8cf7449f41f4b1eb548，未push。原.out数组显示限制保留 |
| [task-012](#task-012) | 常量数组精确离散百分位 | 3：0410、0412、0415 | 复用task-011的有限范围检查；0415输入依赖task-013 | 高 | 已修复并完成有限INT/BIGINT/TEXT等已核验规则；[fix-018](../fixes/tasks/aggregates-001/fix-018/task-012.md)，a499d04cf69a13d831f3943df89c15e60bfcd56c，未push。NUMERIC约束、任意Collation/非有限数不在完整验收范围 |
| [task-013](#task-013) | PG一维TEXT数组字面量解析 | 1：0415，与task-012重叠 | 解析本身独立；完整0415需task-012 | 高 | 已修复并完成标准array_nulls=on下有限语法验收；[fix-018](../fixes/tasks/aggregates-001/fix-018/task-013.md)，3c9e4bb004bff47a4ca8b750961f5e4470076590，未push。运行时文本、多维花括号和非默认下界未实现 |

原问题组拆分关系：数组问题分为构造(task-001)、聚合 NULL/空输入(task-003)、值自身排序(task-004)；排序能力单列 task-002。统计问题拆成小样本 NULL(task-007)、REGR_COUNT(task-009)，其余回归/精度算法暂不立 task。序列只纳入 FROM 常量整数(task-008)，不囊括投影/LATERAL。聚合 FILTER(task-005) 不囊括相关聚合归属。fix-017另将已实际补证的数组下标研究登记为独立task-010，尚未实施。

<a id="task-001"></a>

### fix-018 新增前置任务计划（启动恢复后、实施前）

- 用户已授权 `docker start doris`；原容器恢复 healthy，FE SELECT 1 成功，SHOW BACKENDS Alive=true，阶段31 tenk1仍为10000行。未重建或装数；禁止重放段错误候选。
- **task-011：常量数组连续百分位生成**。关联0411、0413，依赖概率DOUBLE上下文commit `2aef92e0c755132bf2253a34280e99adf27f98d0`。当前WITHIN GROUP被Doris拒绝；拟在`sqlglot/generators/doris.py::withingroup_sql`把有限常量概率数组逐元素转为原生精确连续PERCENTILE，保留NULL概率、重复、数组维度及空/全NULL组返回NULL；键仅简单数值列/数值CAST，避免重复执行易变表达式。NULL在SQL运行时处理，不以Python输出预置答案。新增Doris测试；分别检查源码生成、原0411/0413、普通/重复/NULL/空组、分组/排序及类型。FILTER/OVER、动态概率、INTERVAL及一般表达式不默认为已支持。独立本地commit，不push。
- **task-012：常量数组离散百分位生成**。关联0410、0412、0415。连续/近似算法不能代替离散分位；拟排序COLLECT_LIST非NULL值，按PG DOUBLE概率的ceil(p*N)（0取首项）取原类型元素，以常量树展开保留NULL和多维形状；不使用lambda。复用task-011有限范围检查，独立代码/测试/commit；验证整数与ASCII文本、重复、NULL、端点、嵌套、空组和类型。排序表达式求值、浮点rank边界及非默认文本排序须明确限制，不顺带修task-010。
- **task-013：PG文本数组字面量输入**。0415还被原始`'{...}'::text[]`输入阻断，Doris直接CAST返回NULL。先查现有解析能力；仅在有通用合法输入解析及引号/转义/NULL/空串边界证据时实现，不替换固定数据或表。与百分位规则分开commit；显式维度下界、多维/一般运行时文本须明确未覆盖。此任务是五条目标查询的前置能力，不是框架装数。
- 新任务编号只扩展当前修复清单，不改变313条原输入/首轮统计。分别记录实际验收，不因候选成功或返回提前拒绝而结案；仅生成本轮既定汇总和实际task报告。

### task-001：Doris 数组字面量生成

- **最新实施与验收（fix-020）**：[任务报告](../fixes/tasks/aggregates-001/fix-020/task-001.md)。使用源ARRAY共同类型和字面量语法作为规则依据，移除PG Parser内Doris转换白名单（commit `0d1d795278d5666cf5756f696f44f20d63dfed53`）；复用一维词法helper，在Doris最终类型上下文转换INT/BIGINT/SMALLINT/TEXT/BOOLEAN子数组文本、处理已解码E输入，保留外层TEXT CAST的01/02（commit `12b98b50836cad4d4a49e968894f4570ca4b9a52`，父为前项）。两项均本地保存、未push。20条新源变体原目标执行及原生类型/完整有限值/维度/NULL/位置/重复/必要顺序和双端重复通过；1条数组显示不是有效JSON，另以原生投影证实实际元素正确，未改正式比较器。额外5条escape兼容控制通过，不升级旧NUMERIC/REAL补偿结论。全方言1107、定向/核心318及最终PG/Doris114通过（集合重叠），旧56边界保持且无约束域限制保留。原313条逐ID生成不变、310安全原查询分类与前轮相同，原MATCH未增加；3条BE风险未执行。当前任务仍“已修改但未完成验收”，不把第一项unsupported提前诊断当可执行转换完成。
- **补偿审查与具体剩余项（fix-020后）**：旧NUMERIC文本/ARRAY_MAP/取负归为特定版本补偿，通用性待验证。此次6个原生取负能力控制5同值，DECIMAL(38,38)接近1的反例却返回NULL；当前已生成补偿仍正确。因此未提交“precision<=38一律原生负号”这种猜测性简化。下一项是核对该Doris版本算子推型及配置前提，再验证外层CAST/运算/同型列，决定能否有依据缩小补偿范围；没有新能力依据不继续包装碰答案。原运行时文本直接REAL/一般NUMERIC/混合Scale本轮无新增实现，不重复算进展。另发现源PG Generator在ARRAY[(SELECT ARRAY[1,2]),'{3,4}']往返时丢第二成员，登记独立研究事项，未混入当前Doris转换；当前原文直接生成Doris已执行正确。源任务编号和首轮/历史事实不改写。
- **fix-020实施前方案（语义/职责审查）**：按更新后的修复Skill，先修已有补丁中的目标耦合，不继续追逐原文件零报错。起点`d0c2e9ea1e187edc157f96657313982ce7929e09`，目标仍`../sqlglot-functional-commits`与原分支，允许按功能本地commit、不push。PG18.1已只读确认`SELECT ARRAY[ARRAY[1,2],'{3,4}'] AS xs`及字符串在前、TEXT二维变体均成功；当前PG Parser却因Doris输入转换白名单丢掉外层已知ARRAY类型，生成器随后输出数组/字符串混合构造。源依据为PG18表达式4.2.12及类型转换10.5：ARRAY以源共同类型转换unknown输入，源类型事实不应取决于目标是否已有实现。
  - **拟改规则和提交边界**：从`PostgresParser::_array_element_type`移除目标转换白名单，只保留已能可靠推导的PG共同类型，未知列仍不猜型。目标`DorisGenerator::_coerce_array_input`已有unsupported检查；确认它能在严格模式拒绝缺失的数组文本输入转换，不能直接关闭该检查输出错误混合构造。补PG AST/往返/序列化、多目标生成和Doris严格拒绝测试；这是“源语义信息与目标能力分离”的独立提交，不声称补齐未知文本子数组的Doris转换。
  - **验收与排除**：原313条生成层和310条安全查询回归；新合法源变体对照AST与实际PG类型/值，Doris新拒绝只计安全诊断、不算可执行转换完成。NULL子数组若源因维度失败，不当成功源证明。已有文本中转/取负/lambda补偿保留历史事实并标待通用性审查，本轮不凭旧56条值一致升级其状态；不改Schema、数据、比较器或其他任务，不执行原BE风险查询。
  - **同轮第二项实施前方案**：第一项已独立提交`0d1d795278d5666cf5756f696f44f20d63dfed53`，父为本轮起点；8条源合法变体取得类型信息，Doris严格拒绝不计转换完成。继续原task-001的源输入转换：对源共同类型已明确为一维INT/BIGINT/SMALLINT/TEXT/BOOLEAN子数组的unknown字符串，拟在Doris输入转换侧复用PG已有一维数组字面量词法解析，构造有目标元素类型的数组AST，交给既有标量输入规则。把已有私有解析helper移到共享dialect helpers，PG原显式TEXT[]解析也复用，不让目标Generator调用源Parser或改写原源AST。
    - 依据仍是PG ARRAY共同类型与array输入语法，不根据.out答案拼数组。不预先在源Parser插入INT CAST，否则外层`::TEXT[][]`可能错误丢掉unknown文本的前导零；目标生成时按最终上下文决定，必须验证此反例。只支持已有词法helper识别的一维默认边界文本，带显式维度/下界或多维文本不猜解析；不扩展NUMERIC/REAL补偿、一般运行时字符串列、未知列Schema、用户下标或数组子查询构造。候选没有新lambda/取负字符串操作，生成大小与原字面量元素数线性对应。
    - 独立提交需包含helper复用、Doris转换和类型/引号/转义/NULL/重复、先后顺序、显式外层CAST、已有TEXT数组解析回归。用真实源/改后生成目标核验普通、列/CASE、CTE上下文和必要排序；若实际限制无法满足则保留未验收，不与第一项架构提交混算。原313条/43阶段及旧56条回归范围保持不变。
    - **本项调试发现**：20条初次变体18条通过，两条`E'...'`源成功但仍失败。PG Tokenizer已将escape字符串解码为`ByteString(is_bytes=None)`；源数组推型没有把这种PG文本输入当unknown，目标也未复用其已解码文本。这是同一文本子数组输入规则的必要词法变体：补PG源unknown分类，仅在目标数组上下文读取非二进制ByteString的已解码文本，不重新实现转义或顺带修普通标量E字符串。两条失败保留实际事实，重测后才能计入成功；不改写成普通字符串绕开测试。
- **最新实施与验收（fix-019）**：[任务报告](../fixes/tasks/aggregates-001/fix-019/task-001.md)。同次调用连续完成五种可独立验证的规则，按功能本地commit：固定NUMERIC数组CAST `ba7fb6989650ae4e1662a29669b9001df44728dc`；元素CAST先执行 `5ec631410471210358e164b98a107e963abeee2f`；数组内高精度取负 `58135f86a50fc449ca45a3b6d7e5393d3e55665c`；NUMERIC与unknown字符串输入 `fcc68bb35fc49628692cb270b256403e82b9c539`；有限无精度数组CAST `d0c2e9ea1e187edc157f96657313982ce7929e09`。父commit依次为前项，第一项父为`3c9e4bb004bff47a4ca8b750961f5e4470076590`；未push。56条新边界值/Scale、NULL、别名、位置/重复及必要顺序通过并双端重复稳定；起点22条已正确，26条值/Scale/表示不同、7条目标失败、1条转译失败本轮修正。固定声明28条对应，另28条PG typmod=-1意味着无固定约束，不能冒称全类型域等价。旧75条62构造/控制原生值一致，13条独立下标错误保留task-010，75重复稳定。原313条生成SQL/严格错误逐ID未变，310条原回归分类与fix-018相同，原14条为3匹配/6显示不同/4目标失败/1转译失败；未增加原MATCH。1103项方言及提交后314项定向/核心通过（重叠不相加），ruff/格式/diff通过。整个task状态仍“已修改但未完成验收”，不把提前拒绝、完成commit或新增边界数量当任务完成。
- **当前余项与恢复条件（fix-019后）**：直接REAL运行时文本入口最终再次以两条四行反例验证，Doris内部精确等值标志均0；此前40种包装未得通用安全路径，下一步须找到可验证的FLOAT32直接解析入口/算法，而非重复先DOUBLE后REAL。一般NUMERIC仍有混合Scale可观察差异、77位目标拒绝、NUMERIC NaN变NULL以及源无约束类型域；本轮固定/有限规则已解决的情况不能继续列为未实现。需要改Doris/添加UDF或改变Schema/Session/结果契约时先获得额外授权，不强行改SQLGlot骗过结果。task-010、ARRAY子查询、VARIADIC/UDF以及task-003不自动混进当前任务。本轮在五项功能和最终回归之后，因剩余尚无经验证的安全通用实现停止重复试验，保留未完成；不要求每个小commit都由人再次说继续，也不承诺后台自动执行。
- **fix-019实施前方案**：本次按用户要求连续处理原task-001暴露的剩余问题，fix按实际范围组织，commit仍按独立行为拆分。起点`3c9e4bb004bff47a4ca8b750961f5e4470076590`，原checkout/分支干净；允许本地功能commit，不push、不改数据/原输入/比较器。已实测两条成功源反例：`ARRAY[1e40,2]::NUMERIC(50,0)[]`在PG为精确10^40，在Doris为10000000000000000302727418506697047212060；两个NUMERIC(40,0)元素构造在目标变成array<decimal(38,0)>且大数为NULL。
  - 第一项拟修`DorisGenerator.cast_sql/_array_cast_types/_bounded_numeric_array_sql`的显式固定(p,s)数组CAST：保留已知目标精度和统一Scale，有限数字/十进制文本/NULL先保留为输入文本，再运行时按原精度转换，避免先经DOUBLE；显式目标Scale允许其源输入Scale不同。原无约束NUMERIC数组仍不混成固定类型。验证正负舍入、NULL、空/嵌套、39至76位、指数、声明类型/typmod及超域保护；不顺带修用户下标。
  - 第二项独立研究并修PG Parser中显式NUMERIC元素的共同类型与Doris构造：原始每项CAST必须先完成再参与数组共同类型，不能吞掉中间舍入/Scale。只有能证明输入域及返回声明的范围才实施；与整数组CAST分开commit及测试。混合Scale、无约束域和动态参数不预先宣布可全部覆盖。
  - 随后继续原范围的其他CAST及类型问题，按新实测反例更新本条并实施安全修复；运行时未知文本直接REAL已在fix-017有40个失败候选及源码证据，不重复同一包装试验、不换DOUBLE冒充。一般NUMERIC全域超目标类型域等需具体说明阻断，不能无限扩大输入域或仅提前拒绝就算修复。多项均归入fix-019既定汇总/逐task报告，不每个commit停止调用。每项从改后SQLGlot生成SQL、实际两端核验及回归后本地提交，最后固定原14条及43阶段安全范围回归。
  - **同轮新证据与下一独立提交（实施前）**：第二项13个无外层Neg变体值/Scale与已取得类型通过；额外负号控制`ARRAY[-CAST(1e40 AS NUMERIC(50,0))]`源成功、Doris报`scale should not smaller than 0, but real scale is -12`。该失败也存在于旧直接负号路径，不把它算构造规则已通过；第二项保留原Neg不推型，随后独立修“显式NUMERIC元素取负”：先保留原CAST与舍入，再对其规范数值文本切换符号，最后按原域解析，避开Doris高精度负号运算；只用于数组元素，不全局替换Neg。须实测NULL、零、正负/双重负号、p76、嵌套CAST及运行时多行，一次求值，独立commit。
  - **同轮后续独立提交计划（实施前）**：第三项9条符号变体已全部成功。又复现`ARRAY[9223372036854775808,'18446744073709551616',NULL]`、`ARRAY[1.25,'2.00']`及`ARRAY[1.20::NUMERIC(6,2),'2.00']`：源为NUMERIC数组，当前Doris错误返回TEXT数组。拟在PG Parser的unknown字符串可转换类型白名单纳入已知NUMERIC，并复用有限十进制/进制/下划线输入规范化；不把未知列猜成NUMERIC，不继承已知CAST的固定Scale强行截断unknown字符串。只接受可证明统一原Scale、最多76位的有限域；不同原Scale仍不能用补零隐藏文本可观察差异。单独commit与正常/NULL/嵌套/字符串在首项、类型/Scale及外部边界测试，不并入取负提交。
  - **同轮无约束数组CAST计划（实施前）**：第四项9条混合输入已经全部取得正确数值/Scale，类型由错误TEXT改为有界DECIMAL；PG本身typmod=-1的声明差异仍保留。又实测`ARRAY['1.25','2.00']::NUMERIC[]`目标默认为DECIMAL(38,9)而多出尾零，`ARRAY[1e40,2]::NUMERIC[]`目标大数为NULL。拟在Doris的显式无约束NUMERIC数组CAST中保留该输入上下文，对可证明有限统一Scale的构造使用既有精确输入路径，不再追加会重新强制(38,9)的目标CAST；独立commit，覆盖NULL/空/嵌套和已知舍入链。不能声称Doris获得PG无约束NUMERIC类型；不明确的动态输入/混合Scale仍拒绝或保留未覆盖，源/目标类型域不等价须在报告标明。

- **最新进展（fix-018）**：[本轮报告](../fixes/tasks/aggregates-001/fix-018/task-001.md)。源DOUBLE概率上下文已本地提交，连续/离散/文本数组输入分别登记task-011/012/013并独立提交。用户授权启动原容器后完成五条原查询及边界验收：均执行成功、元素/NULL/形状和对应类型一致，原.out显示仍不同。最终1097项方言、308项定向/核心通过（集合重叠）；310条安全原查询/43阶段为82匹配、25负向、69值/顺序不同、114目标失败、12环境类、8转译失败。五条从“提前拒绝/目标报错”真正变为可执行，但整个task-001仍有直接REAL/一般NUMERIC等余项。分支24个本地commit、未push、干净；高风险候选禁止重试，最终BE在线。详见各task报告，不把候选或显示清洗当修复。
- **fix-018实施前方案（2026-11-25）**：用户明确要求继续解决0410/0411/0412/0413/0415这5条，而非仅把错误提前。起点`4dc65a35a7efa92551cb9fb00c2315fcb8ff659f`，目标仍为干净的`../sqlglot-functional-commits`、原分支，本地按功能commit、不push。只读核对PG18的pg_proc及5条原文EXPLAIN确认概率参数被转为double precision[]，故fix-017的无上下文NUMERIC Scale保护过于保守。第一项拟在PG Parser识别WITHIN GROUP百分位函数的直接数组构造概率参数，记录源签名确定的DOUBLE元素类型（含明确嵌套维度），不改变普通NUMERIC数组、不覆盖显式内部CAST或猜排序列Schema；独立提交及Parser/Generator/AST/跨方言回归。该项只恢复正确参数处理，不把重新出现的目标WITHIN GROUP错误算修复。
  - **后续同轮范围**：继续研究并实现这5条所需的有序集合转换；连续百分位、离散百分位及0415文本数组输入是不同机制，先取得可行性和边界证据，再分别登记/更新对应task、具体方案及独立提交，不混入源数组类型commit。已验证Doris PERCENTILE_ARRAY能返回0411的连续结果，离散百分位需排序后按ceil(p*N)选原类型元素，不能改用连续或近似算法。NULL概率、空组、多维形状、重复、返回类型、必要顺序、FILTER/分组/作用域与输入表达式求值必须专项核验；没有证据时不宣称全域支持。不得改原SQL/.out、数据、比较规则或顺带修task-010下标；run --stdout重跑原阶段及受影响安全范围。本轮报告使用未占用fix-018两类路径，按实际task合并，不生成额外执行材料。
- **最新结果（fix-017）**：[详细报告](../fixes/tasks/aggregates-001/fix-017/task-001.md)。有限整数NUMERIC提交`3281a9848a342660b8b47a9145846d562db5fb35`；同Scale有限小数/指数提交`4dc65a35a7efa92551cb9fb00c2315fcb8ff659f`。62条构造/控制取得相应值与类型证据，13条完整查询因既有下标错误仍不同，转task-010；不是task-001全部完成。274条既有边界中273条双端重跑稳定，1条`ARRAY[1.25,2]`因混合Scale由错误类型输出改为严格拒绝。原310条为82匹配、25负向、64值/顺序差异、114目标失败、12环境标签、13转译失败；5条WITHIN GROUP原错误被NUMERIC保护提前拦截，不算修复或匹配增加。1090项方言、301项定向/核心通过（两组有重叠），详见报告。当前20个本地commit，未push。
- **下一步具体范围（fix-017后）**：数组下标失败归入独立task-010，建议下一轮由人明确授权；不能在NUMERICcommit里顺带实施。原task-001保留：运行时文本直接REAL须找到不经DOUBLE的安全入口/等价算法；混合Scale、一般NUMERIC/非有限、未知类型/一般作用域须先明确可保留的类型与表示契约。不重复把本轮已通过的76位整数、同Scale小数和指数当新修复。超过76位或不确定源类型不是换DOUBLE就能解决；需改Doris或增加类型前提时先申请授权。
- **fix-017 实施前方案（2026-11-25）**：从干净的 `6922457c6d223eafb1e3e7c1aaab211f88487874` 继续本 task；允许按功能保存本地 commit，不 push。先补查运行时文本→REAL：本机对应 Doris 提交的文本解析及 Decimal 转换均经过 DOUBLE，PG 则直接 `strtof`；真实表字段的中点反例仍不同，JSON、Decimal、lambda 等手写路径也没有同时通过边界，因此不提交一个声称解决通用直接 REAL 的补丁。此限制不关闭整个 task。
  - **下一项独立修复**：保留超出 INT64 的裸整数字面量所确定的源 NUMERIC 数组类型，只实现可静态证明为有限整数域的数组构造。修改 PG Parser 的有限共同类型判断及 Doris Generator；源 AST 只记 NUMERIC 基础类型，不虚构源 precision/scale。目标根据整数位数或显式 SMALLINT/INT/BIGINT 的有限范围选择 `DECIMAL(p,0)`，通过运行时 `ARRAY_MAP` 保留精度，必要时把大整数输入写成精确文本，避免目标 LARGEINT 词法上限。直接常量 Decimal 数组 CAST 的 39 位错值及 76 位 NULL 候选不采用。
  - **范围与保护**：同规则内核验 NULL、正负/INT64 边界、19/38/39/76 位、已知整数 CAST 的运行时输入、嵌套矩形数组、重复及稳定排序，保留源表达式的求值顺序和未知参数。超过目标 76 位、无约束/非有限 NUMERIC、一般 Decimal 输入及未知类型不冒称支持；不把其结果换成 DOUBLE/文本，不修改 Schema、输入数据、比较器或其他 task。显式整个数组 CAST 需独立核对，不能因新类型提示引入错误默认 Decimal 参数。
  - **验收与提交**：先测 Parser/Generator、AST 不变性及其他方言，再实际执行修改后生成的 SQL，核对 Decimal 原生类型、精确整数文本、NULL/重复/必要顺序并重复执行；随后回归前轮边界与原输入的安全范围。主比较器仍报告的表示/类型差异单列，不用手写候选代替验收。该整数 NUMERIC 规则及相应测试作为一个本地功能 commit；若发现其他独立可安全修复规则，先追加方案再单独提交，同轮记录在 fix-017 两份报告。
  - **未提交实现的实测修正**：平面运行时 Decimal 解析可保住 76 位，但 `ARRAY(Decimal数组,Decimal数组)` 在当前 decimal256 默认设置下会被共同类型推导收窄到 38 位，39/76 位嵌套样本变成 NULL。因此不保留这一候选；拟先构造全层文本数组，再按原维度逐层 ARRAY_MAP，在叶层统一 CAST 到已证明足够的 precision。8 条初始运行时边界 SQL 的 `-9223372036854775808::BIGINT` 会先 CAST 正数再取负，源端就溢出；改成 `(-9223372036854775808)::BIGINT` 后重新执行，不把初次源错误算修复通过。比较脚本中不同无主键行使用同一组谓词的问题也需纠正为逐行精确文本核验，不修改正式比较器。
  - **第二项实施前方案**：第一项已验收并独立提交为 `3281a9848a342660b8b47a9145846d562db5fb35`，工作区干净。13条手写候选证明有限小数/指数可由同一运行时入口精确解析，包括 `1e40`、`1e-76`、`1.2300`。拟在同 task 内独立补有限 NUMERIC 小数及科学计数法字面量：源 Parser 保留 NUMERIC，目标以 Decimal 元组计算整数位数/scale，不经 float；沿用逐层 ARRAY_MAP、76位与工作量保护。特别限制为所有非 NULL 已知输入的源 scale 相同；PG NUMERIC 元素可以各带不同 scale，而 Doris 数组统一 Decimal scale，混合 scale 不能直接补零冒称等价。未知/一般 NUMERIC、非有限值和精度总和超过76位继续明确未支持。测试需覆盖 NULL、同 scale 不同大小、嵌套、CAST到文本的可观察 scale、指数正负边界、负零、超精度和原整数规则回归；作为第二个本地功能 commit，不混入第一项或其他 task。
- **最新实现与验收（fix-016）**：[详细报告](../fixes/tasks/aggregates-001/fix-016/task-001.md)。同一次调用完成标量投影REAL、十六进制浮点输入、NaN/Infinity、显式DOUBLE→REAL运行时转换四项规则，分别本地commit；收尾另补非有限拼写ASCII保护，合计5个commit。89条新变体原生元素/类型及重复核验通过，另补四行排序/重复查询；原比较37一致、51不同、1源文本驱动解码失败保留。185条既有边界原生值/计数和必要排序补齐，原比较125一致、59不同、1无行值结论。最终443项定向/核心、1088项方言测试通过。原输入扩展310条/43阶段，3条后端风险未跑；82匹配、25负向、64值/顺序不同、119目标失败、12环境标签、8转译失败，详见汇总的分类限制；原查询生成层与起点无变化，不宣称匹配率提升。当前HEAD `6922457c6d223eafb1e3e7c1aaab211f88487874`，未push。整个task仍未完成验收。
- **下一步具体范围（fix-016后）**：继续原task-001，先研究运行时未知文本直接→REAL的单次舍入，不重复对已通过的字面量/显式DOUBLE链做同样的小修。反例、两条失败的CAST/lambda路径、中点与次正规数依据见本轮报告第6.1节。先找目标可用的直接FLOAT32输入入口或安全实现，验证类型、普通/边界/NULL/多行；不能先转DOUBLE替代源直接REAL。无可信源类型时不猜型、不强制Schema。NUMERIC有限精度可移植子域与无约束/非有限域分别研究：1e40的DECIMAL(41,0)候选已成功，不能声称数值本身不可表示；但固定Decimal不能覆盖PG无约束NUMERIC。缺少安全通用实现的部分保留未验收；若需要改Doris、Schema/数据或比较契约，先申请额外授权。本轮未实施其他task，也未将旧失败候选当新补丁。
- **fix-016 实施前方案（2026-11-24）**：从干净的 `365986d92f426fa6c837d3fc60ba6a41acd0770c` 继续所选 task-001，本轮连续处理可安全独立验证的余项，每项规则分别本地 commit，不 push。第一项在 `_coerce_array_input` 中处理无 FROM、无其他查询修饰、单个有限常量 CAST 投影的标量子查询，保留子查询与别名，不传播外层类型进入未知文本或一般查询。第二项研究已知数组浮点输入的十六进制和非有限数，先核验源有效输入/目标运行时转换，再单独实现、测试和提交。每项均核对原生值/类型、NULL、重复、顺序与 AST 不变性，重跑此前边界及原查询的明确范围。
  - **第二项实施细化**：先独立实现有限十六进制浮点文本到源 IEEE FLOAT/DOUBLE 的精确整数比值转换，复用既有最近偶数舍入，不使用 Python float64 中转 REAL。覆盖可选二进制指数、大小写/符号、半舍入点、最大值/次正规数、已知 REAL CAST 链、NULL/嵌套；限制输入长度和指数工作量，非法/溢出仍明确拒绝。源成功的 `ARRAY[1::REAL,'0x1.000002p0']` 当前转译拒绝，Doris 直接 CAST 返回 NULL，说明需要 SQLGlot 输入规范化，而不是假定目标支持原文本。NaN/Infinity 不混入该有限值 commit，另行核验与提交。
  - **第三项实施前补证与方案**：Doris 当前版本实测支持 FLOAT/DOUBLE 的 NaN/±Infinity，`ISNAN/ISINF` 可只读核验；此前未知文本入口拒绝这些合法 PG 输入属于过度拒绝。拟在仅 PG 类型明确的数组输入规范化中接受完整、大小写不敏感的 NaN/Inf/Infinity（可带符号及允许的首尾空白），交由目标 CAST 产生非有限值；不把有限溢出自动改成 Infinity，不把非法文本改成 NaN。分别核验类别、Infinity 符号、NULL位置、元素个数/重复和类型，不用 NaN=NaN 作为等价证明，不声称 NaN payload/符号位一致。单独 commit，保留原比较器的表示差异。
  - **第四项实施前补证与方案**：明确 DOUBLE→REAL 的运行时 CAST 链存在可独立修复的路径。对 VALUES 列 `x::DOUBLE PRECISION::REAL`，将 DOUBLE→REAL 放入单元素 ARRAY_MAP 后再取回元素，6 行候选（普通、微小数、中点、次正规数、负值、NULL）与 PG 二进制值对齐。拟只在 PG 类型已知数组构造的连续浮点 CAST 链中，对输入已由显式 DOUBLE 确立的 REAL 转换使用该运行时路径；保留每层 CAST/负号顺序，表达式仅求值一次。不猜 x 的类型，不宣称修复未知文本直接→REAL；不越过查询作用域，不实现全局 CAST。独立提交并测试多层链、NULL/重复/排序、AST/其他方言隔离，以及发生溢出的源负向限制，不能由6行候选直接宣称任意列等价。
  - **运行时列的实测限制**：直接用 `ARRAY_MAP(v -> CAST(v AS FLOAT), ARRAY(x))[1]`，`x='0.1'` 可恢复 REAL→DOUBLE 的源值，但 `x='7.038531e-26'` 返回 `7.038531308148791e-26`，PG 为 `7.038530691851209e-26`；半舍入点文本也错误舍入为 1，而 PG 为 1.0000001192092896。因此不能把一条普通值通过的 lambda 候选推广成通用运行时 CAST 修复。继续区分可信字面量、一般列与目标浮点解析能力；不改比较器掩盖差异。
- **前轮实现与验收（fix-015，历史事实）**：[详细报告](../fixes/tasks/aggregates-001/fix-015/task-001.md)。有限十进制字面量的已有REAL/DOUBLE CAST链按内向外精确舍入，再进入数组共同类型；包含负号及PG已知负FLOAT/DOUBLE类型提示。47条源成功边界全部原生元素等值/NULL核验、已取得类型和重复稳定通过；主比较26一致、21显示不同保留。原142条逐ID不变，旧97+41边界保持；439项定向/核心及1084项方言测试通过，commit后161项定向通过。独立本地commit `365986d92f426fa6c837d3fc60ba6a41acd0770c`，父commit `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`，未push。连续CAST中间负号在提交前发现并补齐，不隐藏该失败尝试。整个task仍未完成验收。
- **fix-015结束时的下一项方案（历史；有限标量部分已在fix-016实施）**：优先处理有限标量子查询中的REAL值提升。当前反例 `SELECT ARRAY[(SELECT 0.1::REAL),2::DOUBLE PRECISION] AS xs` 的PG二进制首元素为0.10000000149011612，当前目标原生等值为[0,1]；独立Doris候选 `SELECT CAST(ARRAY((SELECT CAST('0.100000001490116119384765625' AS DOUBLE)), CAST(2 AS DOUBLE)) AS ARRAY<DOUBLE>) AS xs` 已实际执行，类型为ARRAY<DOUBLE>且原生等值[1,1]，只是可行性证据，不是生成器已实现。拟在Doris数组元素的有限标量投影路径中复用本轮舍入，保留投影REAL再外层DOUBLE的顺序；仅纳入无FROM、单一可信有限字面量投影及括号/别名/NULL和有限CAST链，不越过一般查询作用域，不改全局CAST或Schema。表/相关/多行/聚合/窗口/集合查询、运行时列、NUMERIC/特殊值等排除。先检查空/多行语义和类型，再明确允许的AST形状，补FLOAT/DOUBLE、内外CAST、中点/次正规数、NULL/重复、AST不变及作用域隔离测试；回归当前47条、旧97+41及原142条。当前单独 `ARRAY[(SELECT 0.1::REAL)]` 的原生值相同，不能将所有子查询一概归错。运行时VALUES文本列REAL→DOUBLE也有真差异：id1/id3首元素不等、NULL行相同，留在同task研究，不靠字面量预计算冒充已修列转换。下一轮起点为上述fix-015完整SHA；应按独立行为追加commit，不混入运行时列或其他task，这是fix-015结束时的状态，不覆盖上方fix-016的实现结果。

- **fix-015实施前方案（2026-11-24）**：本轮从干净的`../sqlglot-functional-commits`、分支`codex/doris-functional-commits`、HEAD `51bf6a4085c5036a236f0ebfa5a720cab5dfb019`继续原task-001；已授权修改/只读回归及按功能本地commit，不push。上轮两个REAL反例已在该HEAD再次执行，原生第二元素等值分别仍为0（`[1,0]`、`[1,0,1]`），不是仅文本显示不同。
  - **独立行为与代码位置**：在`DorisGenerator._coerce_array_input/array_sql`的PG数组类型提示路径中，保留已有字面量REAL转换后再参与共同类型的顺序。复用`_array_float_input`，按连续REAL/DOUBLE CAST由内向外精确舍入；数组结果为REAL时仍用已验证的运行时ARRAY_MAP路径。不能把内层REAL直接去掉、用Python float64代算REAL或改比较器。
  - **纳入/排除**：纳入带可信PG数组类型的直接字面量REAL CAST，以及仅由REAL/DOUBLE组成、以有限十进制字符串/数值为叶子的CAST链，覆盖括号、负数、NULL、重复、矩形嵌套及外层数组CAST。无Schema列/参数、一般表达式、跨子查询类型传播、NUMERIC规则、特殊/十六进制Float输入、task-003等不在本次实现范围；直接DOUBLE没有REAL层时不扩大改写。源非法输入默认排除，源合法但暂不支持不能标负向。
  - **验收与提交边界**：一个本地功能commit保存此规则及Doris测试，依赖已有数组源类型/输入转换提交`696de7c98a06eff49b6ba83a70d345457fe641db`、`523cd4c161d7a83d4ad56a534c74d29bf3c3921a`、`51bf6a4085c5036a236f0ebfa5a720cab5dfb019`。新增生成SQL/AST不变性/其他方言隔离测试；双端二进制及原生元素核验两条反例、FLOAT/DOUBLE顺序、舍入中点、次正规数、外层/嵌套CAST及NULL/重复/必要排序，分别保留主比较结论。回归原142条/19阶段、已有97+41边界；不运行已有后端风险的301/303/304，不宣称全313条最终验收。实际结果写入fix-015两类既定报告并回填本条；整个task仍有其他余项，不因本子项成功而关闭。

- **前轮实现与验收（fix-014，历史事实）**：[详细报告](../fixes/tasks/aggregates-001/fix-014/task-001.md)。本轮先补写下面的实施前方案，再修改代码；实现有限十进制/科学计数法unknown字面量按FLOAT32/64的最近偶数舍入。REAL输入通过ARRAY_MAP运行时转换，避免实测到的常量数组CAST精度差异。41条成功源边界（由PG二进制读取确认）全部原生元素等值核验通过并重复稳定；原比较器仍为25值一致、15显示不同、1最大DOUBLE源文本驱动解码失败，不伪造MATCH。前轮97边界和原142条回归结果均保持；两条额外控制仍有已知REAL元素CAST的真值差异。task-001仍未完成验收，未commit/push。
- **fix-015之前提出的方案（历史依据；有限字面量部分已实施）**：优先处理“已知REAL元素自身的CAST精度”，不是再给unknown文本重复增加CAST。反例一 `SELECT ARRAY['1e2','7.038531e-26'::REAL] AS xs`，源第二元素二进制为`7.038530691851209e-26`，当前生成查询内第二元素原生等值核验失败；反例二 `SELECT ARRAY['1e2',0.1::REAL,2::DOUBLE PRECISION] AS xs`，源第二元素是REAL先舍入再提升的`0.10000000149011612`，目标仍不等。拟在Doris数组元素生成路径中保留“先按显式REAL转换，再参与共同类型”的顺序，复用本轮精确输入规范化和运行时转换；先核对内层CAST/外层数组CAST/标量子查询边界，不能把显式REAL直接删成DOUBLE。只从本数组构造语义内的可信输入入手，不做全局通用CAST、Schema猜型或task-003修改；无法安全复用时先写阻断/方案修正。验收须包括这两条原文、REAL/DOUBLE混合、上下文与NULL/重复、舍入中点/次正规值、AST不变性及原142条和本轮边界回归，目标均从修改后SQLGlot生成，分别记录原比较结论与原生类型/元素证据。NaN/Infinity、十六进制、4096字符以上输入及NUMERIC仍未验收，后续另补证，不因一次拒绝判断Doris不能支持。该方案不表示已经执行下一轮或获得commit/push授权。

- **fix-014实施前方案（2026-11-24，保留决策过程）**：本轮继续原task-001，不新增任务。起点为fix-013的未提交代码（HEAD `089891f2521780e2c5b243005017af9db62f25a6`，累积diff SHA256 `b3737ff1ad9a7fafc5c43675efb645a334ccc5795b32c6285de5045f00a1ad55`）；以下是当时写下的方案，不是执行结果，实际结果以上方fix-014记录及报告为准。
  - **实施前只读补证与方案修正**：2026-11-24实际核查发现，直接文本CAST不能覆盖REAL舍入；将`7.038531e-26`放入包含已有表字段的真实ARRAY后，PG二进制值为`7.038530691851209e-26`，Doris实际元素提升为DOUBLE后为`7.038531308148791e-26`。因此下述“直接转换”的初始候选不采用；拟以十进制字符串的精确整数比值实现IEEE 754最近偶数舍入，输出精确可表示的十进制文本，再CAST到FLOAT/DOUBLE。不用Python float64作REAL中间值；这一规则只用于已确定类型的unknown字面量输入，不在Python求整条查询答案。十六进制和非有限字符串本轮先明确unsupported，有限值上溢/非零下溢到零也拒绝；这些限制不是能力已补齐。源端`extra_float_digits=0`会使文本读取丢精度甚至在最大DOUBLE处驱动溢出，精度核验另用只读二进制游标与目标原生等值查询，不改主流程的Session或比较器。
  - **具体问题**：`SELECT ARRAY[1::REAL, '1e2'] AS value` 在前轮源端返回FLOAT32数组 `[1,100]`，目标返回TEXT数组 `["1","1e2"]`。Parser的`_array_element_type`主动排除了Float混合unknown字符串，Doris的`_coerce_array_input`也没有浮点输入分支，不能只给整个数组加CAST便假定类型和值都正确。
  - **拟修改位置和规则**：先用双端只读查询核对十进制/科学计数法文本直接CAST为FLOAT/DOUBLE的实际语法、精度及溢出行为；若有可验证的安全范围，在`sqlglot/parsers/postgres.py`保留可信FLOAT/DOUBLE共同类型，在`sqlglot/generators/doris.py`先将unknown元素按该类型转换再构造数组，并让直接/括号/嵌套显式数组CAST传递类型。只规范化输入文法，不先用Python float64计算REAL字面量，避免二次舍入。若发现目标转换差异，先补证并缩小规则，不能把未验证的通用转换写成实现。
  - **纳入及排除**：纳入已有显式REAL/DOUBLE元素、unknown字符串/NULL、重复值、矩形嵌套、显式数组CAST的有限可信上下文；未知列/参数、一般表达式、NUMERIC/Decimal、ARRAY(SELECT...)、文本数组CAST、task-003的VALUES传播和其他独立聚合问题不在本轮实现范围。NaN/Infinity、十六进制、上溢/下溢须实测并写明支持/拒绝/待研究，不能默默当NULL或宣称全部支持。
  - **验收方法**：新增PG Parser类型及Doris实际生成SQL、AST不变性和其他方言不受影响的测试；双端核对字段/显式别名、FLOAT32/64、行数、元素值及重复次数、数组内顺序/必要最终顺序，分别说明协议显示与真实二进制值，不放宽原比较器。覆盖指数、正负零、小数、舍入中点（含PG文档的`7.038531e-26`）、有限范围边界、NULL和嵌套/子查询边界，逐端重复执行。源负向只作直接相关边界，不计成功匹配。重跑原14条关联Case及原142条/19阶段固定回归，保留所有原.out结论和其他独立余项。
  - **依赖、权限与完成条件**：复用fix-012/013的AST类型/输入转换基础；先更新方案再改代码，本轮只授权本地SQLGlot及测试和只读数据库回归，不commit/push，不改数据、原输入、框架或比较策略。仅当上述有限规则取得有效证据才关闭该子项；task-001仍有NUMERIC/未知类型余项，不因本轮结束整体标完成。真实实现和失败尝试写入fix-014原有约定的两类报告，结束时回填本条当前状态。

- **前轮实现与验收（fix-013，历史事实）**：[详细报告](../fixes/tasks/aggregates-001/fix-013/task-001.md)。已实现unknown字符串与已知SMALLINT/INT/BIGINT/Boolean的有限输入转换，含符号/空白/合法下划线/进制格式/范围、布尔唯一前缀及显式直接/括号/嵌套数组CAST；旧ARRAY['1',2]反例的值和INT32类型已对齐。97条边界双端成功并重复稳定；23条Boolean显示不同保留，22条新增原生Boolean投影另核对一致。142条原Case结果不变，不能将变体修复写成.out匹配数提升。未修改比较器或数据，仍未完成整个task，未commit/push。
- **fix-015结束时的剩余子项（历史）**：当时标量子查询、运行时列、非有限/十六进制Float、NUMERIC及未知类型未完成；其中有限标量、十六进制、非有限Float、显式DOUBLE→REAL已在fix-016取得限定证据。**当前余项以上方fix-016状态/下一步和该轮报告第6节为准**，不再把这些已实现规则统统记为待实施。未知文本直接REAL、一般作用域、NUMERIC和未知类型仍保留；不强制Schema，不顺带实施task-003，源合法但Parser拒绝不能列为负向。
- **前轮实现与验收（fix-012，历史事实）**：[详细报告](../fixes/tasks/aggregates-001/fix-012/task-001.md)。默认链路实际保留有限整数/标量子查询INT32或INT64、纯字符串及全unknown/NULL的TEXT类型，并支持已知类型和矩形嵌套。前轮7条默认数组元素类型反例已修正；18条旧边界值全部一致，16条全部已取得字段类型/约束可对齐，另保留独立id位宽和Decimal约束。当时混合字符串/整数仍是真值差异，该反例已在fix-013修正；超INT64、Decimal约束和Boolean显示余项保留。14条原查询和142条同范围回归结果未改变；0010类型改善不冒充原.out MATCH。历史状态未完成验收，未commit/push。
- **前轮类型核验（fix-011，历史事实）**：[详细报告](../fixes/tasks/aggregates-001/fix-011/task-001.md)。14条原查询全部补查实时PG/.out，18条既有边界双端重跑；当时9条已取得的全部输出类型约束对齐，7条数组默认元素类型不同、1条独立id列位宽不同、1条Decimal结果约束不能直接判等。该轮没有代码补丁、提交或推送；其7条默认类型余项本轮已修正，不能继续当作当前未实现。
- **fix-011记录的类型子项（历史依据）**：①保留裸整数/标量子查询的可信源元素类型，区分INT4/INT8/NUMERIC；②保留全unknown/NULL、字符串默认text元素类型；③区分Decimal参数CAST与结果typmod。独立CAST候选在部分样本可行，但统一INT的反例已把2147483648变成NULL；通用annotate_types对小数/全NULL也不是PG完整求型，不能直接照标注强转。具体历史SQL、验收与未覆盖范围在fix-011，当前实现/余项以上述fix-012为准。

- **目标与依据**：ARRAY[...] 的标量、NULL、空数组与嵌套字面量；按 AST 类型保留元素 CAST。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0010-12bf388c](cases/aggregates-001/pg-aggregates-0010-12bf388c.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
SELECT any_value(v) FROM (VALUES (array['hello', 'world'])) AS v (v);
```

- **纳入范围**：ARRAY[...] 的标量、NULL、空数组与嵌套字面量；按 AST 类型保留元素 CAST。
- **排除范围**：ARRAY(SELECT ...)、PG 文本数组 CAST、数组下界、UNNEST 展开算法、用户定义类型。
- **实施建议**：为 Doris 实现数组构造输出，复用 exp.Array/元素生成而非继承 MySQL unsupported；必要时复用已有 array 函数 helper，不给具体表名特判。
- **代码依据**：sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py array_sql:654；公共节点 exp.Array（非子查询构造）。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无实现依赖。与 task-002/008 同时影响某些 Case 不构成代码依赖。
- **关联证据**：[pg-aggregates-0010-12bf388c](cases/aggregates-001/pg-aggregates-0010-12bf388c.md), [pg-aggregates-0136-4243166e](cases/aggregates-001/pg-aggregates-0136-4243166e.md), [pg-aggregates-0306-e70870c4](cases/aggregates-001/pg-aggregates-0306-e70870c4.md), [pg-aggregates-0410-f6f52dc3](cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md), [pg-aggregates-0411-b38c2a1f](cases/aggregates-001/pg-aggregates-0411-b38c2a1f.md), [pg-aggregates-0412-cbdaef84](cases/aggregates-001/pg-aggregates-0412-cbdaef84.md), [pg-aggregates-0413-6ccabd9a](cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md), [pg-aggregates-0415-16b30942](cases/aggregates-001/pg-aggregates-0415-16b30942.md), [pg-aggregates-0434-5da33736](cases/aggregates-001/pg-aggregates-0434-5da33736.md), [pg-aggregates-0437-d68f01c2](cases/aggregates-001/pg-aggregates-0437-d68f01c2.md), [pg-aggregates-0438-998adec3](cases/aggregates-001/pg-aggregates-0438-998adec3.md), [pg-aggregates-0534-1b68ef98](cases/aggregates-001/pg-aggregates-0534-1b68ef98.md), [pg-aggregates-0551-f476de2c](cases/aggregates-001/pg-aggregates-0551-f476de2c.md), [pg-aggregates-0552-7ea82af2](cases/aggregates-001/pg-aggregates-0552-7ea82af2.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：普通/NULL/空/嵌套、显式元素类型；read=postgres/write=doris 的 Parser/Generator 单元测试，相关 Doris/MySQL 回归。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：数组构造正确不等于整个含 UDF、UNNEST、WITHIN GROUP 的查询正确。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-002"></a>

### task-002：Doris 使用原生 NULLS FIRST/LAST 排序

- **最新状态（fix-002）**：已修复并完成当前 Doris 4.1.3-rc02 环境约定的排序验收；本地未提交/未推送，完整实现、19 组边界、6 条原查询及剩余问题见[任务报告](../fixes/tasks/aggregates-001/fix-002/task-002.md)。6 条均完成严格转译，按原 .out 3 条匹配、3 条执行失败；后者不伪造 MATCH。0551/0552 类型声明仍有独立差异，0137 实时 PG 与 .out 冲突先核对源前提。下列基线和未实施描述是首轮归因历史，不覆盖它们。
- **目标与依据**：Doris 已实测支持的最终排序与位置/别名排序，保留源端默认 NULL 方向。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0173-5bef76d3](cases/aggregates-001/pg-aggregates-0173-5bef76d3.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
select max(unique2) from tenk1 order by 1;
```

- **纳入范围**：Doris 已实测支持的最终排序与位置/别名排序，保留源端默认 NULL 方向。
- **排除范围**：自定义 ORDER BY USING 运算符、排序键唯一性、不同 Collation、聚合内部排序算法。
- **实施建议**：覆盖继承的 NULL 排序能力标志；使用已存在的 ordered_sql，避免对 ORDER BY 1 的 NULLS LAST 错误拒绝或展开成错误键。
- **代码依据**：sqlglot/generators/doris.py DorisGenerator；sqlglot/generators/mysql.py NULL_ORDERING_SUPPORTED:127；sqlglot/generator.py ordered_sql；公共节点 exp.Ordered；能力标志。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无；只涉及相同 Case 的数组或序列问题单独验收。
- **关联证据**：[pg-aggregates-0134-429eb1f7](cases/aggregates-001/pg-aggregates-0134-429eb1f7.md), [pg-aggregates-0137-2237979d](cases/aggregates-001/pg-aggregates-0137-2237979d.md), [pg-aggregates-0173-5bef76d3](cases/aggregates-001/pg-aggregates-0173-5bef76d3.md), [pg-aggregates-0179-8eb5c0b1](cases/aggregates-001/pg-aggregates-0179-8eb5c0b1.md), [pg-aggregates-0551-f476de2c](cases/aggregates-001/pg-aggregates-0551-f476de2c.md), [pg-aggregates-0552-7ea82af2](cases/aggregates-001/pg-aggregates-0552-7ea82af2.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：ASC/DESC、显式与默认 NULLS、位置序号/别名、NULL 和重复键；顶层排序逐行核对，非唯一键只验证有保证的相对顺序。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：已实测版本为 Doris 4.1.3-rc02；支持的最早版本需在提交前确认并写入测试/说明。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-003"></a>

### task-003：ARRAY_AGG 保留 NULL 并补偿空输入

- **最新类型核验（fix-011）**：[详细报告](../fixes/tasks/aggregates-001/fix-011/task-003.md)。10条原查询及22条既有边界均重跑。22条中19条取得的类型可映射，2条Decimal结果约束不能直接判等，1条TIMESTAMP真实丢微秒；值/顺序另保留DISTINCT无保证顺序与Boolean显示问题。0287等原查询的INT32/TINYINT差异仍在，不能验收。去掉聚合查询VALUES列也复现位宽差异；不把它误归为NULLIF引入，不仅改聚合函数名。未新增补丁、提交或推送。
- **继续原task的类型子项**：①从可信VALUES/列来源保留数组元素类型，不给所有ARRAY_AGG硬CAST INT；②核对Decimal结果协议typmod=-1与目标固定(10,2)的契约，不把源参数约束冒充结果声明；③BOOL、TIMESTAMP与未排序DISTINCT差异分别沿用已有表示/时间/顺序研究。18条边界在本次已取得维度可核对，不等于本task整体通过。默认Schema仍非强制，不将手动qualify/标注或独立候选成功冒充默认转译链路已修复。

- **历史状态（fix-003）**：已修改但未完成验收。实际采用 PG AST 的 null_on_empty 标志和 Doris `NULLIF(ARRAY_AGG(...), ARRAY())`，不添加 COUNT(*)；源明确排除 NULL 时保留 COLLECT_LIST，内部排序/窗口/FILTER 不顺带实现。22 组边界 19 组完整行值一致，另 3 组分别为未保证的 DISTINCT 元素顺序、布尔嵌套表示和独立 TIMESTAMP 精度问题；0287 还存在真实 int4[]/array<tinyint> 差异。最新执行、类型、源码与限制见[任务报告](../fixes/tasks/aggregates-001/fix-003/task-003.md)。未提交/推送，下列首轮建议和未实施描述保留为历史依据。
- **目标与依据**：普通非窗口、非 FILTER 的 ARRAY_AGG，含 DISTINCT；源语义要求保留 NULL 时不得使用丢 NULL 的 COLLECT_LIST；空输入返回 SQL NULL。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0287-a6b4ea06](cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
select array_agg(distinct a)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
```

- **纳入范围**：普通非窗口、非 FILTER 的 ARRAY_AGG，含 DISTINCT；源语义要求保留 NULL 时不得使用丢 NULL 的 COLLECT_LIST；空输入返回 SQL NULL。
- **排除范围**：窗口、FILTER、内部排序算法、复合行类型、数组下界；未指定 ORDER BY 的数组元素顺序不得伪造保证。
- **实施建议**：依据源 AST 的 NULL 契约选择 Doris ARRAY_AGG；利用同聚合层 COUNT(*)=0 做空输入 NULL 补偿，不能只改函数名（已实测 Doris ARRAY_AGG 空输入返回 []）。检查 nulls_excluded 的现有跨方言含义，必要时先在 Parser 明确源约定。
- **代码依据**：sqlglot/generators/doris.py TRANSFORMS exp.ArrayAgg:63；sqlglot/expressions/aggregate.py ArrayAgg:77；公共节点 exp.ArrayAgg/nulls_excluded。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：普通列参数无实现依赖；常量数组测试可用 task-001，但不应为其强行合并 PR。
- **关联证据**：[pg-aggregates-0276-0f1f5154](cases/aggregates-001/pg-aggregates-0276-0f1f5154.md), [pg-aggregates-0283-9ca01715](cases/aggregates-001/pg-aggregates-0283-9ca01715.md), [pg-aggregates-0284-628b13e2](cases/aggregates-001/pg-aggregates-0284-628b13e2.md), [pg-aggregates-0285-ee2a7bc2](cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md), [pg-aggregates-0286-c689f198](cases/aggregates-001/pg-aggregates-0286-c689f198.md), [pg-aggregates-0287-a6b4ea06](cases/aggregates-001/pg-aggregates-0287-a6b4ea06.md), [pg-aggregates-0288-1528b423](cases/aggregates-001/pg-aggregates-0288-1528b423.md), [pg-aggregates-0289-64071a98](cases/aggregates-001/pg-aggregates-0289-64071a98.md), [pg-aggregates-0290-2bc98abf](cases/aggregates-001/pg-aggregates-0290-2bc98abf.md), [pg-aggregates-0371-e4fde69d](cases/aggregates-001/pg-aggregates-0371-e4fde69d.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：一个/全 NULL、重复、DISTINCT 含 NULL、空输入、普通非 NULL；字段类型、元素顺序保证及聚合层级分别验收。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：DISTINCT 且无 ORDER BY 的一个边界实际数组顺序不同，不能按固定 PG 输出排序来造 MATCH；返回类型嵌套别名需人工核对而非只比较类型字符串。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-004"></a>

### task-004：ARRAY_AGG 按聚合值自身排序

- **最新状态（fix-004）**：已修复并完成约定整数排序验收。最终用 ARRAY_SORT/ARRAY_REVERSE_SORT 排非 NULL 值、ARRAY_SLICE 按长度截取 NULL 段，再按指定 NULL 方向拼接；保留 task-003 空输入契约。68 组实际生成边界的状态、字段/别名、整数元素类型、行值/重复次数及必要顺序通过，每端额外重复一次稳定；其中 HAVING 的 lambda 问题在本轮已修正。5 条原查询由执行失败变为成功，实时数组内容/顺序一致；仍有 int4[] / array<tinyint> 和 .out 显示差异，不是完整 Case MATCH。未提交/推送，详见[任务报告](../fixes/tasks/aggregates-001/fix-004/task-004.md)。下列实施建议/未实施措辞为首轮依据，不覆盖本次结果。

- **目标与依据**：单排序键与聚合值同一表达式；当前已实测的可比较整数、ASC/DESC、NULLS FIRST/LAST、DISTINCT。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0288-1528b423](cases/aggregates-001/pg-aggregates-0288-1528b423.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
select array_agg(distinct a order by a)
  from (values (1),(2),(1),(3),(null),(2)) v(a);
```

- **纳入范围**：单排序键与聚合值同一表达式；当前已实测的可比较整数、ASC/DESC、NULLS FIRST/LAST、DISTINCT。
- **排除范围**：不同排序键、多键、任意 Collation、易变表达式、复合类型、窗口/FILTER。
- **实施建议**：专用 ArrayAgg 生成路径识别值自身排序，组合 ARRAY_SORT 与非 NULL/NULL 部分拼接实现指定方向；复用 task-003 的空输入/NULL 规则，不照抄按特定整数取负的候选。
- **代码依据**：sqlglot/generators/doris.py exp.ArrayAgg；sqlglot/generator.py order_sql/ordered_sql；公共节点 exp.ArrayAgg/exp.Order/exp.Distinct。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：依赖 task-003 的 ArrayAgg 生成基础与空输入契约；建议先合并 task-003，再独立提交排序增强。
- **关联证据**：[pg-aggregates-0284-628b13e2](cases/aggregates-001/pg-aggregates-0284-628b13e2.md), [pg-aggregates-0285-ee2a7bc2](cases/aggregates-001/pg-aggregates-0285-ee2a7bc2.md), [pg-aggregates-0288-1528b423](cases/aggregates-001/pg-aggregates-0288-1528b423.md), [pg-aggregates-0289-64071a98](cases/aggregates-001/pg-aggregates-0289-64071a98.md), [pg-aggregates-0290-2bc98abf](cases/aggregates-001/pg-aggregates-0290-2bc98abf.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：ASC/DESC × NULL 方向、全 NULL/空输入、DISTINCT/重复、相同值；不同键/多键明确 unsupported 或保留后续研究，不静默套用。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：同一 Case 还可能有整数推断为 TINYINT 的返回类型差异，本任务不能把它掩盖成完全匹配。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-005"></a>

### task-005：普通忽略 NULL 聚合的 FILTER 转换

- **最新状态（fix-005）**：已修复并完成条件筛选规则约定验收。DorisGenerator.filter_sql 对 SUM/AVG/MIN/MAX/COUNT/ANY_VALUE 使用节点白名单和复制后的 no_filter_sql，COUNT(*) 单独生成 COUNT(IF(条件,1,NULL))；没有开放未知聚合、数组聚合或窗口的同类改写。8 条原查询为 6 个 .out 匹配、1 值/类型差异、1 相关聚合错误；类型补证仍区分真实差异。156 基础 + 12 上下文边界有 167 条行值一致；1 条 AVG 尾差带/不带 FILTER 各自相同，原精确比较仍报不同。验收只关闭条件输入规则，详见[任务报告](../fixes/tasks/aggregates-001/fix-005/task-005.md)。未提交/推送；下列未实施描述保留首轮依据。

- **目标与依据**：非窗口、非相关作用域变化的 SUM/MIN/MAX/COUNT(expr)/COUNT(*) 等已确认忽略 NULL 的普通聚合，含 DISTINCT。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0380-caa8b35c](cases/aggregates-001/pg-aggregates-0380-caa8b35c.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
select min(unique1) filter (where unique1 > 100) from tenk1;
```

- **纳入范围**：非窗口、非相关作用域变化的 SUM/MIN/MAX/COUNT(expr)/COUNT(*) 等已确认忽略 NULL 的普通聚合，含 DISTINCT。
- **排除范围**：ARRAY_AGG、用户自定义聚合、有序集合聚合、相关聚合归属分析；不同 Collation/整数除法不捆绑修复。
- **实施建议**：在 Doris 复用 no_filter_sql 的条件聚合机制，生成 AGG(IF(predicate,value,NULL))；COUNT(*) 用 COUNT(IF(predicate,1,NULL)) 或对应可靠实现，不能留下该版本不存在的 COUNT_IF；不可对任何 Anonymous 函数盲用 helper。
- **代码依据**：sqlglot/dialects/dialect.py no_filter_sql:1441；sqlglot/generator.py filter_sql:2012；sqlglot/generators/doris.py；公共节点 exp.Filter 与普通聚合。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无必须实现依赖；task-001/008 等只是部分 Case 的其他问题。
- **关联证据**：[pg-aggregates-0380-caa8b35c](cases/aggregates-001/pg-aggregates-0380-caa8b35c.md), [pg-aggregates-0381-b9be07f7](cases/aggregates-001/pg-aggregates-0381-b9be07f7.md), [pg-aggregates-0382-9b691678](cases/aggregates-001/pg-aggregates-0382-9b691678.md), [pg-aggregates-0383-ae4a4309](cases/aggregates-001/pg-aggregates-0383-ae4a4309.md), [pg-aggregates-0384-e4a241c8](cases/aggregates-001/pg-aggregates-0384-e4a241c8.md), [pg-aggregates-0385-51f943b1](cases/aggregates-001/pg-aggregates-0385-51f943b1.md), [pg-aggregates-0390-d0eefd0f](cases/aggregates-001/pg-aggregates-0390-d0eefd0f.md), [pg-aggregates-0392-17dd7649](cases/aggregates-001/pg-aggregates-0392-17dd7649.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：TRUE/FALSE/NULL 谓词、空输入、COUNT(*) 与 COUNT(expr) NULL、DISTINCT、除零表达式受 FILTER 保护；保持正确聚合层级。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：Case 381 的整数除法已有 div_sql 类型感知路径，仍需 Schema/注解前提；不把它包装成 FILTER 修复。Case 383 只验本层 FILTER，完整查询还依赖相关聚合研究。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-006"></a>

### task-006：PostgreSQL EVERY 归一化与 Doris 布尔聚合

- **最新状态（fix-006）**：已修复并完成约定验收。PostgresParser.FUNCTIONS 增加 EVERY → exp.LogicalAnd；当前 Doris 继承的 MIN(BOOLEAN) 已保留 BOOLEAN、NULL 和空输入契约，实测不需要额外 CAST，也未修改 Generator。原 0149 按原 .out 匹配，实时六列类型/别名/NULL/值及重复执行一致；120 条基础边界与 18 条上下文/BOOL_AND 控制通过。相关回归 92 条为 72 匹配、9 目标失败、7 值/顺序差异、4 源负向，此前 71 条匹配保持。详见[任务报告](../fixes/tasks/aggregates-001/fix-006/task-006.md)。本轮未提交/推送；下列实施建议和未执行描述保留首轮归因依据，不代表最新状态。

- **目标与依据**：标准布尔 EVERY 普通聚合，TRUE/FALSE/NULL、全 NULL 与空输入。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0149-d636fc82](cases/aggregates-001/pg-aggregates-0149-d636fc82.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
SELECT
  EVERY(b1)     AS "f",
  EVERY(b2)     AS "t",
  EVERY(b3)     AS "f",
  EVERY(b4)     AS "n",
  EVERY(NOT b2) AS "f",
  EVERY(NOT b3) AS "t"
FROM bool_test;
```

- **纳入范围**：标准布尔 EVERY 普通聚合，TRUE/FALSE/NULL、全 NULL 与空输入。
- **排除范围**：booland_statefunc/boolor_statefunc 严格状态函数、整数/字符串强制转换、窗口语义。
- **实施建议**：PG Parser 识别 EVERY 而非 Anonymous；复用 LogicalAnd 公共 AST，为 Doris 生成保留布尔结果与 NULL 契约的实现（当前 CAST(MIN(bool) AS BOOLEAN) 已实测）。不按未知 UDF 名进行全局替换。
- **代码依据**：sqlglot/parsers/postgres.py FUNCTIONS:134；sqlglot/expressions/aggregate.py LogicalAnd:174；sqlglot/generators/doris.py；公共节点 PG EVERY → exp.LogicalAnd。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无；Parser 与 Generator 同属一个能力，建议同一个 PR。
- **关联证据**：[pg-aggregates-0149-d636fc82](cases/aggregates-001/pg-aggregates-0149-d636fc82.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：混合 TRUE/FALSE/NULL、只有 TRUE、全 NULL/空输入、NOT 表达式及返回 BOOLEAN；其他既有 LogicalAnd 源方言回归。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：源端严格内部状态函数另列讨论，不合并为同一个函数改名 PR。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-007"></a>

### task-007：样本统计聚合在有效样本不足时返回 NULL

- **最新状态（fix-007）**：已修复并完成有限浮点输入的小样本 NULL 规则验收。PG Parser 标记 Stddev/StddevSamp/Variance/CovarSamp，Doris 用 IF(COUNT(...) < 2,NULL,原样本统计)；一元 DISTINCT 同步计数去重值，协方差按两列非 NULL 配对。108 条小样本均为正确 NULL；225 条边界/上下文有 195 条精确值一致、30 条原生多样本尾差，未放宽比较。原七条样本 NULL 已修正，完整 .out 仍因总体列 `0`/`0.0` 不匹配，0041/0042 的 NUMERIC/DOUBLE 类型差异不关闭。99 条回归中此前 72 条匹配保持。NaN/Infinity 另查 14 条目标控制，10 条输出改变、4 条不变，不宣称已支持，仍属独立研究。详见[任务报告](../fixes/tasks/aggregates-001/fix-007/task-007.md)，未提交/推送；下列首轮未执行描述保留为历史依据。

- **目标与依据**：源语义为样本方差/标准差/协方差的普通聚合；有效样本数小于 2 时的 NULL 契约；协方差按成对非 NULL 计数。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0030-549b8efa](cases/aggregates-001/pg-aggregates-0030-549b8efa.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
SELECT stddev_pop(3.0::float8), stddev_samp(4.0::float8);
```

- **纳入范围**：源语义为样本方差/标准差/协方差的普通聚合；有效样本数小于 2 时的 NULL 契约；协方差按成对非 NULL 计数。
- **排除范围**：总体统计不改、非有限数、窗口、Decimal 类型及累计算法精度；COUNT 补偿不解决 NUMERIC→DOUBLE。
- **实施建议**：在 Doris 路径使用 CASE WHEN 有效COUNT<2 THEN NULL ELSE 原样本聚合 END；区分 Stddev 与 StddevSamp，不能只覆盖一个 AST 类；协方差共享正确成对计数表达式。
- **代码依据**：sqlglot/generators/mysql.py 统计聚合映射；sqlglot/generators/doris.py；sqlglot/expressions/aggregate.py；公共节点 Stddev/StddevSamp/Variance/CovarSamp（不改总体统计）。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无；task-009 的成对计数可复用概念但不强制代码依赖，若提出共享 helper 必须保持独立可审查。
- **关联证据**：[pg-aggregates-0029-d0645c62](cases/aggregates-001/pg-aggregates-0029-d0645c62.md), [pg-aggregates-0030-549b8efa](cases/aggregates-001/pg-aggregates-0030-549b8efa.md), [pg-aggregates-0035-daf9210d](cases/aggregates-001/pg-aggregates-0035-daf9210d.md), [pg-aggregates-0036-7e813a8e](cases/aggregates-001/pg-aggregates-0036-7e813a8e.md), [pg-aggregates-0041-6590092b](cases/aggregates-001/pg-aggregates-0041-6590092b.md), [pg-aggregates-0042-48fe21bd](cases/aggregates-001/pg-aggregates-0042-48fe21bd.md), [pg-aggregates-0082-f9348d8f](cases/aggregates-001/pg-aggregates-0082-f9348d8f.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：0/1/2 有效行、NULL 掺杂、成对缺失、FLOAT4/FLOAT8；NUMERIC Case 单列仍有类型差异；正常多样本不退化，别改成 POP。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：已确认的是小样本 NULL 差异；统计精度、NaN/Infinity 和任意类型全域需另行研究。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-008"></a>

### task-008：FROM 位置的常量整数 GENERATE_SERIES

- **最新状态（fix-009）**：已修复并完成约定的常量 INT4/NULL 表序列验收。运行时 CASE 与非 OUTER EXPLODE_NUMBERS 保证任一参数 NULL（含 NULL 与零步长共存）返回带正确列名/INT 类型的零行结果；全非 NULL 零步长仍明确拒绝。123 条有限边界/上下文通过并逐端复跑稳定；原130条的80个匹配保持。31条原生成SQL与fix-008逐字相同，0136仍为ARRAY子查询不支持；原Case的聚合类型、统计/UDF、LATERAL/派生表及WITHIN GROUP余项不关闭。代码、全部新增变体和实际SQL见 [fix-009任务报告](../fixes/tasks/aggregates-001/fix-009/task-008.md)；无动态参数/NULLIF/BIGINT等扩围，未提交/推送。fix-009是轮次，task-009仍未开始。

- **前轮进展（fix-008，不覆盖以下首轮依据）**：非 NULL 常量 INT4 起止、非零正/负步长转换为 NUMBERS 关系，保留输出列/别名/INT 类型和空区间。65 条有限边界与上下文双端通过；32 条原 Case 为 8 个 .out 匹配、3 个值差异、20 个 Doris 执行失败、1 个转译失败。八个 .out 匹配中五条仍有聚合类型声明差异，不把显示 NULL 相同称为完整类型一致。NULL 参数四种源成功调用本应返回零行，当前明确 UnsupportedError，故本 task 维持“已修改但未完成全部验收”，不重新编号或提前关闭。零步长源负向默认排除。实际 SQL、类型、错误和边界见 [fix-008](../fixes/tasks/aggregates-001/fix-008/task-008.md)；未提交/推送。0276 已越过序列语法后暴露无别名派生表错误，复用查询级兼容研究，需另核对作用域/别名规则；不混入本任务。

- **目标与依据**：FROM 中非相关、整数常量起止与步长、源端 INT4 范围；别名和输出列，正/负步长与空区间。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0051-6f50d445](cases/aggregates-001/pg-aggregates-0051-6f50d445.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
select sum(null::int4) from generate_series(1,3);
```

- **纳入范围**：FROM 中非相关、整数常量起止与步长、源端 INT4 范围；别名和输出列，正/负步长与空区间。
- **排除范围**：投影位置 SRF、相关/LATERAL、时间/Decimal 序列、动态长度、溢出、大范围资源风险。
- **实施建议**：在表位置生成 Doris NUMBERS 关系，加起点/步长与行数计算并 CAST 保留 INT；明确零/NULL 步长和空区间，不把源 AS g 错当成缺失的 g 列。候选运行中的 1000 安全上限不是应写进社区规则的固定限制。
- **代码依据**：sqlglot/parsers/postgres.py _build_generate_series/FUNCTIONS:146；sqlglot/generator.py explodinggenerateseries_sql:5821；sqlglot/generators/doris.py；公共节点 exp.ExplodingGenerateSeries/GenerateSeries 的表位置。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无；投影位置 179 和 LATERAL 查询需要独立查询级算法，不能算本任务未完成而扩大 PR。
- **关联证据**：[pg-aggregates-0051-6f50d445](cases/aggregates-001/pg-aggregates-0051-6f50d445.md), [pg-aggregates-0052-57717b1c](cases/aggregates-001/pg-aggregates-0052-57717b1c.md), [pg-aggregates-0053-80bc631f](cases/aggregates-001/pg-aggregates-0053-80bc631f.md), [pg-aggregates-0054-9d43ca75](cases/aggregates-001/pg-aggregates-0054-9d43ca75.md), [pg-aggregates-0055-a2bc4e59](cases/aggregates-001/pg-aggregates-0055-a2bc4e59.md), [pg-aggregates-0056-ed925b77](cases/aggregates-001/pg-aggregates-0056-ed925b77.md), [pg-aggregates-0057-54488b60](cases/aggregates-001/pg-aggregates-0057-54488b60.md), [pg-aggregates-0058-774c37d9](cases/aggregates-001/pg-aggregates-0058-774c37d9.md), [pg-aggregates-0059-6e8dac37](cases/aggregates-001/pg-aggregates-0059-6e8dac37.md), [pg-aggregates-0060-10dc4c9b](cases/aggregates-001/pg-aggregates-0060-10dc4c9b.md), [pg-aggregates-0085-b2d1da4b](cases/aggregates-001/pg-aggregates-0085-b2d1da4b.md), [pg-aggregates-0086-94d0e96a](cases/aggregates-001/pg-aggregates-0086-94d0e96a.md), [pg-aggregates-0087-c50d900b](cases/aggregates-001/pg-aggregates-0087-c50d900b.md), [pg-aggregates-0093-d3a22e61](cases/aggregates-001/pg-aggregates-0093-d3a22e61.md), [pg-aggregates-0094-75ff7206](cases/aggregates-001/pg-aggregates-0094-75ff7206.md), [pg-aggregates-0095-5046511e](cases/aggregates-001/pg-aggregates-0095-5046511e.md), [pg-aggregates-0098-b1e5567b](cases/aggregates-001/pg-aggregates-0098-b1e5567b.md), [pg-aggregates-0099-bed0f6ec](cases/aggregates-001/pg-aggregates-0099-bed0f6ec.md), [pg-aggregates-0100-3b815f6a](cases/aggregates-001/pg-aggregates-0100-3b815f6a.md), [pg-aggregates-0101-7fc3b3aa](cases/aggregates-001/pg-aggregates-0101-7fc3b3aa.md), [pg-aggregates-0134-429eb1f7](cases/aggregates-001/pg-aggregates-0134-429eb1f7.md), [pg-aggregates-0136-4243166e](cases/aggregates-001/pg-aggregates-0136-4243166e.md), [pg-aggregates-0276-0f1f5154](cases/aggregates-001/pg-aggregates-0276-0f1f5154.md), [pg-aggregates-0293-3e365a0a](cases/aggregates-001/pg-aggregates-0293-3e365a0a.md), [pg-aggregates-0294-5412623b](cases/aggregates-001/pg-aggregates-0294-5412623b.md), [pg-aggregates-0295-bf759c5f](cases/aggregates-001/pg-aggregates-0295-bf759c5f.md), [pg-aggregates-0296-a77bafc5](cases/aggregates-001/pg-aggregates-0296-a77bafc5.md), [pg-aggregates-0299-d52780a5](cases/aggregates-001/pg-aggregates-0299-d52780a5.md), [pg-aggregates-0398-73d63cba](cases/aggregates-001/pg-aggregates-0398-73d63cba.md), [pg-aggregates-0413-6ccabd9a](cases/aggregates-001/pg-aggregates-0413-6ccabd9a.md), [pg-aggregates-0427-1ad928b9](cases/aggregates-001/pg-aggregates-0427-1ad928b9.md), [pg-aggregates-0428-5c5a2a90](cases/aggregates-001/pg-aggregates-0428-5c5a2a90.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：默认/显式步长、负数/负步长/空区间、NULL 参数与零步长、别名列、INT 边界与资源限制；不能按本批输出硬编码行数。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：较大新表函数能力提交前建议先与社区讨论；先支持清晰受限范围，不承诺全部 PG SRF。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-009"></a>

### task-009：REGR_COUNT 成对非 NULL 计数

- **最新修复（fix-010）**：[任务报告](../fixes/tasks/aggregates-001/fix-010/task-009.md)。新增 DorisGenerator.regrcount_sql，不改公共 AST/Parser，保留显式数值 CAST；普通数值列/常量成对非 NULL 计数、空输入 BIGINT 0 已验收。0073 匹配，0544 第三列 40000/BIGINT 正确，其他统计类型/精度不关闭。67 条边界中 66 条完整通过，1 条外层 SUM 类型差异经无 REGR_COUNT 控制复现；132 条相关回归保留全部原 80 匹配并新增 0073。当前状态：已修复并完成约定验收，代码未提交/推送；以下计划和基线代码缺口保留为历史依据。

- **目标与依据**：普通 REGR_COUNT(y,x) 数值列参数；两者都非 NULL 的行数，空输入为 BIGINT 0。 原锁定提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 上存在相应缺口，见代表 [pg-aggregates-0073-ba8ee5d1](cases/aggregates-001/pg-aggregates-0073-ba8ee5d1.md) 的实际候选与边界。未检查最新 main。
- **成功源最小复现**：原代表源 SQL 如下（对应 .out 成功及本轮只读执行证据见 Case；复杂 Case 的各个任务不得混为整条已修复）：

```sql
SELECT regr_count(b, a) FROM aggtest;
```

- **纳入范围**：普通 REGR_COUNT(y,x) 数值列参数；两者都非 NULL 的行数，空输入为 BIGINT 0。
- **排除范围**：其余回归函数、参数隐式字符串转数值与易变表达式、窗口。
- **实施建议**：复用 AST this/expression，生成 COUNT(IF(x IS NOT NULL AND y IS NOT NULL,1,NULL))；有类型转换语义的表达式必须先保留源 coercion，不能因忽略参数值而吞掉本应发生的转换错误。
- **代码依据**：sqlglot/expressions/aggregate.py RegrCount；sqlglot/generators/doris.py 无专门映射；Generator 默认保留函数名；公共节点 exp.RegrCount。
- **PR 边界**：一个独立行为契约、最小复现及必要边界形成一份建议 PR；与其他 task 在同文件/同 Case 不能作为捆绑理由。相关 Parser/AST/Generator 可以同改以交付本能力。
- **依赖与顺序**：无；不与回归算法、序列生成或大整数 SUM 绑成 PR。
- **关联证据**：[pg-aggregates-0073-ba8ee5d1](cases/aggregates-001/pg-aggregates-0073-ba8ee5d1.md), [pg-aggregates-0544-3a307492](cases/aggregates-001/pg-aggregates-0544-3a307492.md)。各 Case 第 2 节链接其实际 stage YAML 与验证 JSON，不使用统一最终状态。
- **验收**：全有效、任一 NULL、全 NULL/空输入、返回 BIGINT；Case 544 的其他统计/SUM 类型问题分别保留。 使用改后 SQLGlot 从原源 SQL 重新生成并只读执行，不用手写候选代替修复验收；运行对应 tests/dialects/test_doris.py、test_postgres.py 及受影响核心/继承方言测试。任务目标修好而 Case 仍受其他问题影响时，记录余项，不扩大 PR。
- **交付限制**：表达式求值次数/异常输入不能未经分析直接优化掉；本轮无所有参数类型等价证明。 本轮未执行代码单元测试或提交补丁；实际已测变体在代表 Case 中，未测项是后续验收要求，不写成已通过。

<a id="task-010"></a>

### task-010：Doris 数组下标位置与越界行为

- **状态与来源**：未实施。复用已有“数组下标补证”研究，经[fix-017详细报告](../fixes/tasks/aggregates-001/fix-017/task-001.md#6-独立问题数组下标)取得实际证据后登记独立任务；不新增原始Case、不改首轮统计。此次仅授权实施task-001，故不自动修改此task。
- **成功源复现**：`SELECT (ARRAY[1,2,3])[1] AS value`，PG返回1；实际生成`SELECT (CAST(ARRAY(1, 2, 3) AS ARRAY<INT>))[0] AS value`，Doris返回NULL。源[2]返回2、目标[1]返回1；源[0]返回NULL、目标[-1]返回3。原生Doris控制`SELECT ARRAY(1,2,3)[1] AS value`返回1，不是Doris没有取数组元素能力。13条NUMERIC元素转TEXT变体也因相同问题返回NULL。
- **代码与规则边界**：核查`sqlglot/dialects/doris.py`的下标约定、Doris/MySQL/Public Generator的`bracket_sql`继承、PG Parser下标归一化及`exp.Bracket`的类型/offset信息。需保留源位置、NULL与越界行为，不按数字文本全局加1；Doris负下标可从末端取元素，PG默认数组负下标可能应返回NULL。未知列可能不是数组，Map/JSON键和其他源方言不能误改。
- **纳入与排除**：先证明默认一维数组及明确数组类型的正/零/负/动态下标，覆盖NULL数组/下标、越界、重复、嵌套和Alias。自定义数组下界、切片、未知Schema的泛化、其他方言负索引契约分别确认，不伪称全部覆盖；不强制用户提供Schema来绕过已知字面量反例。
- **实施与验收要求**：获授权后先补AST方案，独立本地功能commit，不与NUMERIC构造或task-003混合。由修改后的SQLGlot从源SQL生成目标并实际执行；核对值/类型、边界、NULL与一次求值，重跑13条TEXT投影、3条INT控制、既有数组规则和原安全阶段回归。不用手写Doris控制替代修复后生成SQL，保留Recorded Output证据限制。

<a id="task-011"></a>

### task-011：常量数组连续百分位

- 实施前具体反例、代码规则、范围及提交边界见本节开头fix-018新增任务计划；当前完成有限规则验收，实际代码/测试/SQL/类型/边界及未覆盖条件见[任务报告](../fixes/tasks/aggregates-001/fix-018/task-011.md)。0411、0413均由修改后的SQLGlot生成并执行成功，FLOAT8数组类型对应；不是手写候选。
- 原生PERCENTILE逐常量概率展开，运行时处理NULL和空组，保留概率顺序/重复/多维。只覆盖已核验有限数值列/CAST，非有限极端、INTERVAL、动态概率、FILTER/OVER等不宣称支持。不把原.out显示差异归为本规则未执行。
- 本地commit `fa20f2cf768dc09e887eb8cf7449f41f4b1eb548`，父`2aef92e0c755132bf2253a34280e99adf27f98d0`，未push。

<a id="task-012"></a>

### task-012：常量数组精确离散百分位

- 实施前方案见fix-018新增任务计划；当前完成有限类型/排序前提下规则验收。原0410、0412和依赖task-013的0415成功，具体值/类型、概率DOUBLE舍入、空组、NULL、多维、重复、ASC/DESC及NUMERIC限制见[任务报告](../fixes/tasks/aggregates-001/fix-018/task-012.md)。
- 排序COLLECT_LIST非NULL元素，按DOUBLE概率ceil(p*N)取原类型值；不使用连续或近似函数、不经DOUBLE转换键值、不使用嵌套lambda。原生目标内部下标只服务此生成式，不修task-010用户下标。任意Collation/高精度NUMERIC全域约束仍未证明。
- 本地commit `a499d04cf69a13d831f3943df89c15e60bfcd56c`，父`fa20f2cf768dc09e887eb8cf7449f41f4b1eb548`，未push。

<a id="task-013"></a>

### task-013：PG一维TEXT数组字面量输入

- 实施前方案见fix-018新增任务计划；当前完成标准array_nulls=on下有限语法验收。原0415不再把PG花括号字符串直接CAST成目标NULL；Parser识别合法一维TEXT[]字面量并生成公共Array AST。引号、转义、NULL/字符串NULL、空串/空数组、Unicode、重复及原生逐位置/UNNEST行序证据见[任务报告](../fixes/tasks/aggregates-001/fix-018/task-013.md)。
- 只规范化可完整识别的Cast/DCOLON字符串字面量；多维花括号、非默认下界、一般运行时文本和其他类型不猜。Doris特殊字符数组显示并非总是合法JSON，报告保留限制，以原生元素补证，不改比较器。
- 本地commit `3c9e4bb004bff47a4ca8b750961f5e4470076590`，父`a499d04cf69a13d831f3943df89c15e60bfcd56c`，未push。

<a id="pending"></a>

### 待补证与讨论事项

fix-011 类型补查：直接同型DECIMAL(10,2)数组确实可取得源OID1231、typmod655366及(10,2)，但ARRAY_AGG/外层Neg等结果协议typmod为-1；不能统一说“驱动漏掉精度”，也不能由源子CAST推定整个返回类型的约束。18条数组构造/22条聚合边界的INT/BIGINT/FLOAT/BOOL/DATE递归别名已按实际元素OID核对，不再把这些同义声明统统算缺陷；真实TINYINT、TEXT/NULL_TYPE、TIMESTAMP精度差异仍保留。见[fix-011汇总](../fixes/aggregates-001-fix-011-summary.md)。这些是原task-001/003的验收子项与既有研究，不新增task或改首轮原因数。

fix-010 追加：`SUM(REGR_COUNT结果) OVER ()` 的 PG NUMERIC / Doris BIGINT 类型差异，在不含 REGR_COUNT 的 `SUM(COUNT(*)结果) OVER ()` 控制中同样复现；值与重复执行一致，但类型不一致仍保留。复用下方聚合类型/精度研究，不新建重复 task，不因 task-009 关闭而忽略；0544 的 VAR_SAMP 数值与 SUM 类型问题亦沿用该研究。见 [fix-010](../fixes/tasks/aggregates-001/fix-010/task-009.md#43-外层类型控制与直接相关负向)。

fix-003 新证据追加，不更改首轮原因计数，也不把研究项直接当作可实施任务：

| 问题 | 最新证据 / 去向 |
| :--- | :--- |
| 数组元素类型与嵌套声明/精度 | 原 0287 的 PG int4[] / Doris array<tinyint> 是真实差异；受控 CAST INT 的 _int4 / array<int> 则需要递归别名核对。Decimal 元素精度无完整源元数据，不能用顶层“不适用”结案。沿用类型契约研究，task-003 不关闭，详见 [fix-003](../fixes/tasks/aggregates-001/fix-003/task-003.md#类型证据不能只看工具的一句不同) |
| 布尔数组的 true/false 与 1/0 表示 | 类型为 _bool / array<boolean>；原生只读拆元素并 CAST BOOLEAN 后，本样本类型和值一致。框架未递归按布尔元素归一化，不在 SQLGlot 里硬转字符串制造匹配；见同一任务报告第 6 节 |
| PostgreSQL TIMESTAMP 默认精度转换 | 不含聚合的最小 CAST 也从 .123456 变为整秒；Doris DATETIME(6) 独立对照保留当前值。属于既有类型研究下的新独立发现，先明确默认/显式精度、值域和跨方言影响再形成安全修复，不混入 task-003 |
| 数组下标补证范围 | fix-003当时仅观察、未执行；fix-017已对13条文本投影及3条INT控制实际复现，并登记独立[task-010](#task-010)，尚未修复。不改首轮Case数，不与NUMERIC构造混合提交 |

fix-013 补充到既有NUMERIC/非有限数/类型研究（不新增重复task）：本轮NaN、±Infinity、1e40源端成功而目标为NULL，不能只按样式归因；NUMERIC(10,2)两端声明一致也有NaN值差异。PG合法NUMERIC(3,-1)原生执行成功返回0，但当前Parser拒绝；本轮仅修收集错误时辅助推型的AttributeError，未实现该语法。Float混合文本ARRAY[1::REAL,'1e2']也有真实类型/值差异。15组具体SQL、typmod、目标输出及其限制见 [fix-013研究证据](../fixes/tasks/aggregates-001/fix-013/task-001.md#4-numericfloat余项的具体证据)。这些事实不能当成所有NUMERIC都不可安全转译，也不能列为源负向后排除。

fix-005 的新增证据（不新增 task 或改变首轮原因数）：原 0381 的整数除法仍为 PG 1000 / Doris 2828.968253968249；0384 的 text/varchar(1)、0385/0392 的 int4/tinyint 差异保留。新 AVG(DISTINCT DOUBLE) 边界带/不带 FILTER 均分别为 PG 二进制 59.333333333333336 / Doris 59.33333333333334，另有 PG 文本舍入；不是 FILTER 引入，原精确比较仍不同。相关 0387/0388/0389/0393 目标仍拒绝外层引用，未实现查询级归属。复用下表的类型/精度及相关查询研究，证据见 [fix-005](../fixes/tasks/aggregates-001/fix-005/task-005.md)，这些余项不因普通 FILTER 规则验收而关闭。

fix-007 的新增证据（复用现有类型/显示、浮点及非有限数研究，不新建重复 task）：0029/0030/0035/0036/0041/0042/0082 的样本列 NULL 已修正，整条 .out 仍为 `["0",""]` / `["0.0",""]`；0041/0042 原生 numeric/double 仍不同。28 条基础及 2 条分组正常样本尾差均在未补偿的原生 Doris 控制中存在；例如 PG binary 标准差 1.4142135623730951 / Doris 当前读取 1.414213562373095，尚不直接断言底层算法缺陷。非有限数的 14 条目标控制中 10 条样本从 0 变 NULL、4 条不变，不视为支持或新增匹配。见 [fix-007](../fixes/tasks/aggregates-001/fix-007/task-007.md)，这些范围不因有限输入的 NULL 规则验收而关闭。

| 问题范围与代表证据 | 当前缺口 / 风险 | 下一步及转为 task 的条件 |
| :--- | :--- | :--- |
| 输入类型、NUMERIC 默认 CAST、返回精度/累计溢出与稳定算法；[pg-aggregates-0005-11b43275](cases/aggregates-001/pg-aggregates-0005-11b43275.md), [pg-aggregates-0006-86de303b](cases/aggregates-001/pg-aggregates-0006-86de303b.md), [pg-aggregates-0015-4a78a728](cases/aggregates-001/pg-aggregates-0015-4a78a728.md), [pg-aggregates-0025-d78c66c7](cases/aggregates-001/pg-aggregates-0025-d78c66c7.md), [pg-aggregates-0071-3dc674b8](cases/aggregates-001/pg-aggregates-0071-3dc674b8.md), [pg-aggregates-0129-89f16cca](cases/aggregates-001/pg-aggregates-0129-89f16cca.md), [pg-aggregates-0546-739e31be](cases/aggregates-001/pg-aggregates-0546-739e31be.md) | 当前不列为可直接实施的通用修复 | 带 Schema 与数值域验证精度/溢出；BIGINT SUM 固定宽度提升不等同 PG 任意精度，不能只靠一次值相同立通用规则。 |
| NaN/Infinity、近常数/极端尺度与历史 PG 算法变化；[pg-aggregates-0031-db84a9eb](cases/aggregates-001/pg-aggregates-0031-db84a9eb.md), [pg-aggregates-0033-027391b8](cases/aggregates-001/pg-aggregates-0033-027391b8.md), [pg-aggregates-0066-82b28760](cases/aggregates-001/pg-aggregates-0066-82b28760.md), [pg-aggregates-0085-b2d1da4b](cases/aggregates-001/pg-aggregates-0085-b2d1da4b.md), [pg-aggregates-0093-d3a22e61](cases/aggregates-001/pg-aggregates-0093-d3a22e61.md), [pg-aggregates-0096-fdbe460d](cases/aggregates-001/pg-aggregates-0096-fdbe460d.md), [pg-aggregates-0097-9b7a3291](cases/aggregates-001/pg-aggregates-0097-9b7a3291.md) | 当前不列为可直接实施的通用修复 | 恢复历史版本契约，区分真正数值差异与格式；明确可支持类型和算法后再讨论补偿。 |
| 其余回归函数的 COUNT×VAR/COV 或 CORR² 候选存在精度/边界差异；[pg-aggregates-0074-2817dc87](cases/aggregates-001/pg-aggregates-0074-2817dc87.md), [pg-aggregates-0075-e8c75ef7](cases/aggregates-001/pg-aggregates-0075-e8c75ef7.md), [pg-aggregates-0076-6582f296](cases/aggregates-001/pg-aggregates-0076-6582f296.md), [pg-aggregates-0077-e9c8d047](cases/aggregates-001/pg-aggregates-0077-e9c8d047.md), [pg-aggregates-0078-f2583996](cases/aggregates-001/pg-aggregates-0078-f2583996.md), [pg-aggregates-0104-6106ddbe](cases/aggregates-001/pg-aggregates-0104-6106ddbe.md), [pg-aggregates-0108-9eefe369](cases/aggregates-001/pg-aggregates-0108-9eefe369.md) | 当前不列为可直接实施的通用修复 | 不要和 REGR_COUNT 绑 PR；验证成对 NULL、常量轴、极端尺度、类型及稳定累计。 |
| ONLY 继承语义，删除关键字当前实际错误；[pg-aggregates-0012-3a87f04b](cases/aggregates-001/pg-aggregates-0012-3a87f04b.md), [pg-aggregates-0016-e67c8e38](cases/aggregates-001/pg-aggregates-0016-e67c8e38.md) | 当前不列为可直接实施的通用修复 | 明确父表专属对象映射；否则讨论准确 unsupported，不造 ONLY 表、不静默丢继承约束。 |
| 整行 MIN/MAX 的 STRUCT 比较仍被 Doris 拒绝；[pg-aggregates-0047-027f1f0b](cases/aggregates-001/pg-aggregates-0047-027f1f0b.md), [pg-aggregates-0048-a1525a74](cases/aggregates-001/pg-aggregates-0048-a1525a74.md), [pg-aggregates-0049-df94fed3](cases/aggregates-001/pg-aggregates-0049-df94fed3.md), [pg-aggregates-0050-5a9fb934](cases/aggregates-001/pg-aggregates-0050-5a9fb934.md) | 当前不列为可直接实施的通用修复 | 按字典序、字段 NULL、空输入与平局设计选择算法；不是把 ROW 改名即可。 |
| 按位聚合名称和内部状态接口；普通布尔运算不保留 STRICT；[pg-aggregates-0140-ba04d3f5](cases/aggregates-001/pg-aggregates-0140-ba04d3f5.md), [pg-aggregates-0143-5a8265a3](cases/aggregates-001/pg-aggregates-0143-5a8265a3.md), [pg-aggregates-0144-32971c70](cases/aggregates-001/pg-aggregates-0144-32971c70.md), [pg-aggregates-0106-3a4b5ac2](cases/aggregates-001/pg-aggregates-0106-3a4b5ac2.md), [pg-aggregates-0110-2e0b20b6](cases/aggregates-001/pg-aggregates-0110-2e0b20b6.md) | 当前不列为可直接实施的通用修复 | 确定实际 Doris API/支持域；bool 状态可以有专门方案但不是 EVERY 别名；内部浮点状态版本化。 |
| 相关聚合归属、LATERAL/投影 SRF、标量多行错误；[pg-aggregates-0130-3caf0694](cases/aggregates-001/pg-aggregates-0130-3caf0694.md), [pg-aggregates-0132-8462e8e9](cases/aggregates-001/pg-aggregates-0132-8462e8e9.md), [pg-aggregates-0134-429eb1f7](cases/aggregates-001/pg-aggregates-0134-429eb1f7.md), [pg-aggregates-0136-4243166e](cases/aggregates-001/pg-aggregates-0136-4243166e.md), [pg-aggregates-0169-fb0ce421](cases/aggregates-001/pg-aggregates-0169-fb0ce421.md), [pg-aggregates-0179-8eb5c0b1](cases/aggregates-001/pg-aggregates-0179-8eb5c0b1.md), [pg-aggregates-0383-ae4a4309](cases/aggregates-001/pg-aggregates-0383-ae4a4309.md), [pg-aggregates-0387-68e5c03f](cases/aggregates-001/pg-aggregates-0387-68e5c03f.md), [pg-aggregates-0388-a7ae3863](cases/aggregates-001/pg-aggregates-0388-a7ae3863.md), [pg-aggregates-0389-fc7103c6](cases/aggregates-001/pg-aggregates-0389-fc7103c6.md), [pg-aggregates-0393-8196c25e](cases/aggregates-001/pg-aggregates-0393-8196c25e.md) | 当前不列为可直接实施的通用修复 | 候选仅固定数据；补重复外行、空输入、多行错误及外层/内层归属后，按不同查询级算法拆 task。 |
| 基表列别名列表与 USING 合并列类型；[pg-aggregates-0264-e3b16e8d](cases/aggregates-001/pg-aggregates-0264-e3b16e8d.md), [pg-aggregates-0265-6c4951ae](cases/aggregates-001/pg-aggregates-0265-6c4951ae.md) | 当前不列为可直接实施的通用修复 | 已改成投影但现样本为空，缺非空/重复/NULL 键；需要 Schema 感知且保留输出提升类型。 |
| 不同键 ARRAY_AGG 排序、整行引用、数组维度；[pg-aggregates-0283-9ca01715](cases/aggregates-001/pg-aggregates-0283-9ca01715.md), [pg-aggregates-0286-c689f198](cases/aggregates-001/pg-aggregates-0286-c689f198.md), [pg-aggregates-0371-e4fde69d](cases/aggregates-001/pg-aggregates-0371-e4fde69d.md) | 当前不列为可直接实施的通用修复 | 负键排序候选不适用于溢出/NULL/任意类型；明确多键/NULL/维度与行值再单独讨论。 |
| 有序集合：连续/离散分位数、概率数组、多维/NULL、MODE；[pg-aggregates-0398-73d63cba](cases/aggregates-001/pg-aggregates-0398-73d63cba.md), [pg-aggregates-0402-03bcfbf3](cases/aggregates-001/pg-aggregates-0402-03bcfbf3.md), [pg-aggregates-0403-1e765a0a](cases/aggregates-001/pg-aggregates-0403-1e765a0a.md), [pg-aggregates-0404-565ced59](cases/aggregates-001/pg-aggregates-0404-565ced59.md), [pg-aggregates-0405-3dbf4d44](cases/aggregates-001/pg-aggregates-0405-3dbf4d44.md), [pg-aggregates-0410-f6f52dc3](cases/aggregates-001/pg-aggregates-0410-f6f52dc3.md), [pg-aggregates-0412-cbdaef84](cases/aggregates-001/pg-aggregates-0412-cbdaef84.md), [pg-aggregates-0414-66a94e8f](cases/aggregates-001/pg-aggregates-0414-66a94e8f.md), [pg-aggregates-0415-16b30942](cases/aggregates-001/pg-aggregates-0415-16b30942.md), [pg-aggregates-0462-507973b2](cases/aggregates-001/pg-aggregates-0462-507973b2.md) | 当前不列为可直接实施的通用修复 | 常量连续参数候选可用但浮点仍差；动态概率被限制，离散/众数需不同查询级实现，分别验证空组/平局/Collation/类型。 |
| 假想集合排名，当前单键计数候选部分可行；[pg-aggregates-0406-5e4718d4](cases/aggregates-001/pg-aggregates-0406-5e4718d4.md), [pg-aggregates-0407-dea6404c](cases/aggregates-001/pg-aggregates-0407-dea6404c.md), [pg-aggregates-0408-e463cacf](cases/aggregates-001/pg-aggregates-0408-e463cacf.md), [pg-aggregates-0409-d4deac02](cases/aggregates-001/pg-aggregates-0409-d4deac02.md), [pg-aggregates-0426-31226e20](cases/aggregates-001/pg-aggregates-0426-31226e20.md), [pg-aggregates-0427-1ad928b9](cases/aggregates-001/pg-aggregates-0427-1ad928b9.md), [pg-aggregates-0428-5c5a2a90](cases/aggregates-001/pg-aggregates-0428-5c5a2a90.md), [pg-aggregates-0464-1a2659a1](cases/aggregates-001/pg-aggregates-0464-1a2659a1.md), [pg-aggregates-0548-bcd73bfc](cases/aggregates-001/pg-aggregates-0548-bcd73bfc.md) | 当前不列为可直接实施的通用修复 | 补 NULL、空输入、多键/降序、类型强转和排序规则；不能泛化到窗口 RANK。 |
| ORDER BY USING 自定义比较；部分源例可执行、3 条危险；[pg-aggregates-0297-ce288841](cases/aggregates-001/pg-aggregates-0297-ce288841.md), [pg-aggregates-0298-261e1b98](cases/aggregates-001/pg-aggregates-0298-261e1b98.md), [pg-aggregates-0300-a22a64cf](cases/aggregates-001/pg-aggregates-0300-a22a64cf.md), [pg-aggregates-0301-8e89d955](cases/aggregates-001/pg-aggregates-0301-8e89d955.md), [pg-aggregates-0303-8e89d955](cases/aggregates-001/pg-aggregates-0303-8e89d955.md), [pg-aggregates-0304-1e9d5cdf](cases/aggregates-001/pg-aggregates-0304-1e9d5cdf.md), [pg-aggregates-0391-fce06d52](cases/aggregates-001/pg-aggregates-0391-fce06d52.md) | 当前不列为可直接实施的通用修复 | Parser/公共 AST 如何保留运算符需先设计；危险原文不重试，不能把 < 与 *< 或 ~<~ 全替换 ASC。 |
| 脚本自定义聚合和 UDF；[pg-aggregates-0291-40c04ecb](cases/aggregates-001/pg-aggregates-0291-40c04ecb.md), [pg-aggregates-0292-68d79c0b](cases/aggregates-001/pg-aggregates-0292-68d79c0b.md), [pg-aggregates-0293-3e365a0a](cases/aggregates-001/pg-aggregates-0293-3e365a0a.md), [pg-aggregates-0121-6b24fa4d](cases/aggregates-001/pg-aggregates-0121-6b24fa4d.md), [pg-aggregates-0126-43383f4c](cases/aggregates-001/pg-aggregates-0126-43383f4c.md), [pg-aggregates-0417-277c66fb](cases/aggregates-001/pg-aggregates-0417-277c66fb.md), [pg-aggregates-0433-90ca229d](cases/aggregates-001/pg-aggregates-0433-90ca229d.md), [pg-aggregates-0434-5da33736](cases/aggregates-001/pg-aggregates-0434-5da33736.md), [pg-aggregates-0456-ace8bfc0](cases/aggregates-001/pg-aggregates-0456-ace8bfc0.md), [pg-aggregates-0481-e31d0ffb](cases/aggregates-001/pg-aggregates-0481-e31d0ffb.md), [pg-aggregates-0527-e31d0ffb](cases/aggregates-001/pg-aggregates-0527-e31d0ffb.md), [pg-aggregates-0534-1b68ef98](cases/aggregates-001/pg-aggregates-0534-1b68ef98.md) | 当前不列为可直接实施的通用修复 | 定义、STRICT、初值、转移/最终函数、VARIADIC 是外部迁移范围；按名称绑定 core 规则不可接受，BALK 常量候选确实失败。 |
| 普通聚合内部 ORDER BY；[pg-aggregates-0505-e2ced71d](cases/aggregates-001/pg-aggregates-0505-e2ced71d.md), [pg-aggregates-0549-9bc0dfb2](cases/aggregates-001/pg-aggregates-0549-9bc0dfb2.md), [pg-aggregates-0550-cff4ea50](cases/aggregates-001/pg-aggregates-0550-cff4ea50.md) | 当前不列为可直接实施的通用修复 | 当前删除排序行值相同不够；验证表达式异常/易变与浮点累加顺序，分开 MIN/MAX 与 AVG。 |
| avg_rec 与 BYTEA 未映射/缺表；[pg-aggregates-0246-3fc2fc89](cases/aggregates-001/pg-aggregates-0246-3fc2fc89.md), [pg-aggregates-0251-b9e80dc2](cases/aggregates-001/pg-aggregates-0251-b9e80dc2.md), [pg-aggregates-0253-f0a8749a](cases/aggregates-001/pg-aggregates-0253-f0a8749a.md), [pg-aggregates-0255-476afef2](cases/aggregates-001/pg-aggregates-0255-476afef2.md), [pg-aggregates-0342-dddcf200](cases/aggregates-001/pg-aggregates-0342-dddcf200.md), [pg-aggregates-0348-e9f2b704](cases/aggregates-001/pg-aggregates-0348-e9f2b704.md), [pg-aggregates-0349-87cb7e26](cases/aggregates-001/pg-aggregates-0349-87cb7e26.md), [pg-aggregates-0354-1159bcab](cases/aggregates-001/pg-aggregates-0354-1159bcab.md) | 当前不列为可直接实施的通用修复 | 外部准备修复对象和值域，不改 SELECT 遮盖缺表；avg_rec 当前源行为和历史还不同。 |
| 显示比较与驱动/嵌套结构表示；[pg-aggregates-0308-ad9e3ab0](cases/aggregates-001/pg-aggregates-0308-ad9e3ab0.md), [pg-aggregates-0311-ad9e3ab0](cases/aggregates-001/pg-aggregates-0311-ad9e3ab0.md), [pg-aggregates-0314-ad9e3ab0](cases/aggregates-001/pg-aggregates-0314-ad9e3ab0.md), [pg-aggregates-0317-ad9e3ab0](cases/aggregates-001/pg-aggregates-0317-ad9e3ab0.md), [pg-aggregates-0320-ad9e3ab0](cases/aggregates-001/pg-aggregates-0320-ad9e3ab0.md), [pg-aggregates-0323-ad9e3ab0](cases/aggregates-001/pg-aggregates-0323-ad9e3ab0.md), [pg-aggregates-0326-ad9e3ab0](cases/aggregates-001/pg-aggregates-0326-ad9e3ab0.md), [pg-aggregates-0072-7639b7e8](cases/aggregates-001/pg-aggregates-0072-7639b7e8.md), [pg-aggregates-0079-18883aa1](cases/aggregates-001/pg-aggregates-0079-18883aa1.md), [pg-aggregates-0081-60dd4d15](cases/aggregates-001/pg-aggregates-0081-60dd4d15.md), [pg-aggregates-0088-e73d81f2](cases/aggregates-001/pg-aggregates-0088-e73d81f2.md) | 当前不列为可直接实施的通用修复 | 已知结构值或二进制值相同，首轮报告保持；单独完善比较证据，保留真实类型差异，不改 SQLGlot 造相同文本。 |
| PG catalog / deparse / 类型身份；[pg-aggregates-0267-c35cf02c](cases/aggregates-001/pg-aggregates-0267-c35cf02c.md), [pg-aggregates-0309-e95cf6b4](cases/aggregates-001/pg-aggregates-0309-e95cf6b4.md), [pg-aggregates-0430-b1f99924](cases/aggregates-001/pg-aggregates-0430-b1f99924.md), [pg-aggregates-0416-a678f5c1](cases/aggregates-001/pg-aggregates-0416-a678f5c1.md), [pg-aggregates-0438-998adec3](cases/aggregates-001/pg-aggregates-0438-998adec3.md) | 当前不列为可直接实施的通用修复 | 本身不是跨库共同结果，不硬编码 PG 目录输出；需要能力线索时抽取公共语义。 |
| 当前 PG 18.1 拒绝历史成功源原文；[pg-aggregates-0107-38a6d915](cases/aggregates-001/pg-aggregates-0107-38a6d915.md), [pg-aggregates-0113-1a65bedb](cases/aggregates-001/pg-aggregates-0113-1a65bedb.md), [pg-aggregates-0114-d556fd00](cases/aggregates-001/pg-aggregates-0114-d556fd00.md), [pg-aggregates-0115-561bfb29](cases/aggregates-001/pg-aggregates-0115-561bfb29.md), [pg-aggregates-0137-2237979d](cases/aggregates-001/pg-aggregates-0137-2237979d.md), [pg-aggregates-0138-e2be6583](cases/aggregates-001/pg-aggregates-0138-e2be6583.md) | 当前不列为可直接实施的通用修复 | 锁定历史版本与内部状态/分组条件后恢复只读复现，不把当前失败当 .out 负向。 |

## 8. 阻断与已知限制

- **安全**：原语句 301、303、304 属同族复合行比较查询；前次源后端崩溃后本轮不重试，不能让修复 Agent 自动跑这些 Case。保留历史成功，不当成负向。
- **历史一致性**：21 条当前文本与 .out 不同、6 条当前源原文失败；只有恢复对应版本/会话/数据契约才能据历史值验收。显示空白变化与实质值变化须按 Case 区分。
- **数据域**：540 次核验是准备阶段历史记录，不是本轮又核验；avg_rec/BYTEA、继承、PG 内部状态、目录/UDF 不能凭相同表名假定等价。
- **比较范围**：原 .out 无原生类型/可靠 NULL 标签；probe 更强但仍有复杂声明归一化限制、未知元数据和非唯一 ORDER BY。浮点补查不改原策略；候选值相同也不承诺所有边界。
- **报告完整性与因果强度**：226 条均有报告且无未开展项，但仍有 71 条调查未完成与 22 条前提阻断；独立候选调用数、成功执行数、值相同数、可实施任务数分别统计，不能互相替代。
- **后续入口**：由人选择第7节task-id并授权，Agent按最新方案实施。task-001已推进到fix-020，当前已实现规则、待审查补偿和研究阻断分开见该条目及fix-020报告第7节。下一项以DECIMAL(38,38)原生负号反例核对算子类型/能力前提，不笼统反复写“继续修REAL/NUMERIC”，也不重复修已通过的有限规则。独立[task-010](#task-010)未在本轮实施。Skill规定处理规则，Agent据此判断修复顺序；用户决定授权范围。task-003及其他研究余项保留，10项已验收task只关闭各自约定规则，不关闭同Case其他问题。整份输入未完成。
