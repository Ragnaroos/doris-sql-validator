# PostgreSQL → Doris：数据准备、验证、归因与修复流程

## 1. 组件与职责

当前只将 PostgreSQL 这条链路接通；不为 Hive 自动增加 AI 流程。三个 Skill 分别负责数据准备、归因和修复，均只能由人显式调用。工作流的项目内目录名、文件名及路径占位符统一使用英文，正文默认中文；Parser、AST、Generator、Schema、Session、Adapter、Comparator 等通用术语允许使用英文，不直观的状态和结论仍需解释，不能用自创缩写代替原因。JSON 保留已有稳定程序字段名并提供中文说明，错误原文保留原语言。项目上层实际目录（例如“网站维护”）不在本次改名范围。

执行约束：用户要求“按框架流水线运行”时，只生成该次获授权阶段已有命令或 Skill 模板约定的产物，不自行增加总导航、说明文档、额外总结或新的报告种类。需要新增产物时先说明用途并取得授权；解释优先在会话中给出。不得因为进入后续阶段而覆盖首轮证据或擅自修改 SQLGlot；当前 SQLGlot 试验补丁已撤回，重新修复须另获明确授权。

| 阶段 | 人调用什么 | 做什么 | 不做什么 | 产物 |
| :--- | :--- | :--- | :--- | :--- |
| 数据准备 | `pg-doris-prepare-data` Skill | 阅读完整 DDL/DML/COPY 和输出，准备经授权的独立双端测试库，核验逻辑数据及类型映射 | 不改原测试 SQL/答案，不调用验证器内的 AI | `data-preparation.md`、双端准备 SQL、`data-verification.json` |
| 首轮验证 | `import-cases`、`run` 确定性命令 | 提取只读查询、读 `.out`、调用社区 SQLGlot、执行 Doris、比较并报告 | 不连接 PG（有 `.out` 时），不建表装数、不调用模型、不生成 AI 候选 | Case YAML、`validation.md/json` |
| 人工交接 | `prepare-pg-review` 确定性命令 | 核对原文件和查询对应关系，生成路径、指纹及待分析项引用 | 不复制文件、不改写 YAML、不执行 SQL、不调用 Skill | 仅 `HANDOFF.md`、`evidence-index.json` |
| 归因 | `pg-doris-attribute` Skill | 先按对应 `.out` 分流，主要分析源端成功查询的转换不足，实际执行必要的独立对照并生成任务 | 源端负向默认只说明、不逐条改写或复刻错误；不修代码、不改数据、不自动调用后续 Agent | `attribution-details.md`、`attribution-summary.md`、`sqlglot-tasks.md` |
| 对照执行 | 人或已显式调用的 Skill 使用 `probe-pg-case` | 按给定 SQL 执行 PG、报告中保存的社区 Doris、独立 Doris 和重复执行 | 不生成 SQL，不自动作最终归因，不自动生成边界 | `probe-report.md`、`probe-evidence.json` |
| 修复 | 人显式调用 `pg-doris-fix` Skill | 按任务修改 SQLGlot；仅在明确授权时修框架；补测试并用新生成 SQL 回归 | 不自动启动、不改原答案/数据、不自动 commit/push/PR | 代码与测试、`implementation-report.md`、`regression-report.md` |

Skill 是给人工调用的大模型的工作说明，不是框架运行时组件；确定性命令只是普通 Python 程序，不内嵌模型 API、提示词调用、模型循环或 Agent 调度。

## 2. 当前实际目录与产物来源

本节以 2026-11-13 的实际目录为准。<group> 代表输入脚本组，不是不同数据库。当前普通首轮报告 34 组、1,725 条，包含 select_distinct_on 的 3 条 source_parse 失败记录。既有步骤三交接索引仍为 33 组，通过 parser_failure_report_file 引用第 34 组普通报告。本轮只重做步骤四，未重跑首轮、未执行步骤五；.DS_Store 不是框架产物。

### 2.1 实现、Skill 与本批辅助脚本

```text
.agents/skills/
  pg-doris-prepare-data/
    SKILL.md                        人工准备双端数据的步骤、写入范围与核验要求
    agents/openai.yaml              中文界面说明；禁止隐式调用
    assets/data-preparation-template.md  实际数据准备报告的结构，不是已执行结果
  pg-doris-attribute/
    SKILL.md                        人工归因流程、代码分析和候选/边界证据要求
    agents/openai.yaml              中文界面说明；禁止隐式调用
    assets/attribution-report-template.md  详细报告与汇总报告模板
    assets/sqlglot-tasks-template.md       修复 Skill 的任务与验收要求
  pg-doris-fix/
    SKILL.md                        读取归因任务，实施代码修改并实际重跑回归
    agents/openai.yaml              中文界面说明；禁止隐式调用
    assets/implementation-report-template.md  修复实施记录模板
    assets/regression-report-template.md      修复前后与边界回归报告模板

src/doris_sql_validator/
  cli.py                            确定性命令入口，没有模型调用
  importing/importer.py              原脚本到精简 YAML；跳过 DDL/DML
  recorded_output/parsers.py         .out 定位与显示文本解析，不凭空补字段类型
  service.py / comparison.py         执行、状态/字段/记录比较；不自动归因
  reporting.py / report_labels.py    中文首轮报告、明确统计口径和程序代码解释
  handoff.py                        离线原文件引用、指纹和查询对应关系校验，不生成副本
  pg_probe.py                       人工触发的双端只读对照和分维度证据采集

scripts/
  pg_manual_sample.py                本批数据准备、复核和早期首轮助手，不是 run 的内部步骤
  pg_expanded_first_round.py         扩展到 33 组的首轮助手，合并生成 SUMMARY.md 等批次统计
  pg_manual_attribution_batch.py     旧 109 条研究助手，仅本地保留、不发布；不是新版归因入口
```

### 2.2 当前报告总目录

~~~text
reports/pg-manual/
├── archive/                         已有本地历史归档，不是当前结果；本次没有扩大清理范围
├── current/                         首轮 34 组、1,725 条；2026-11-13 只重做步骤四
│   ├── data-preparation/            步骤一原有外部准备/核验材料，本轮未改
│   ├── validation/<group>/          步骤二 validation.md/json，本轮未改
│   ├── handoff/                     原步骤三索引 + 新 attribution/；当前没有 fixes/
│   ├── environment-check.json       首轮只读数据复核，不是 run 的 Gate
│   ├── SUMMARY.md                   首轮确定性汇总，不是本轮归因总结，本轮未改
│   └── validation-summary.json      首轮统计和各组原件路径，本轮未改
└── smoke/                           更早冒烟及迁移记录，不计入 current
~~~

本次按用户要求删除上一轮 attribution/、fixes/ 共 981 个文件，没有备份；只重新生成步骤四 attribution/，不创建额外 handoff/HANDOFF.md 总导航。

### 2.3 步骤一：共享数据准备材料

```text
reports/pg-manual/current/data-preparation/
├── execution-start.json             首次准备的数据库名、开始时间、输入及脚本指纹，用于追溯来源
├── postgres-setup.sql               源 PG 准备 SQL；部分 COPY 数据另外位于 cases/.../setup/data/
├── doris-setup.sql                  本批目标 Doris 实际执行的建表、插入和必要视图 SQL
├── data-verification.json           双端结构、完整记录核验、类型映射限制、版本/Session 等实际证据
└── data-preparation.md              数据准备报告；本批由 pg_manual_sample.py 的 report_preparation()
                                      根据准备/只读复核结果生成，不由交接命令或 run 重新准备数据
```

### 2.4 步骤二：统一的首轮验证报告

~~~text
reports/pg-manual/current/validation/
└── <group>/                         34 组，包含 select_distinct_on
    ├── validation.md                run → write_reports：统计、SQL、失败阶段和具体错误
    └── validation.json              同次运行结构化结果，行样本最多五行，不是完整结果导出

select_distinct_on 的 3 条也使用普通 Case YAML 和上述统一报告结构：
  status=TRANSLATION_FAILED          SQLGlot Parser 拒绝 ORDER BY ... USING，未执行 Doris
  failure_stage=source_parse        表示失败环节，不表示源 PostgreSQL 本身执行失败
  source_evidence=null              首轮转译先失败未读 .out；归因仍必须读原 .out
  不再单列 import-failure.json 或例外说明报告。

current 根目录没有 validation.md/json；跨组 SUMMARY.md 和 validation-summary.json
由批次助手合并逐组结果，不由 AI 归因阶段生成。
~~~

### 2.5 步骤三：只引用原文件的交接索引

~~~text
reports/pg-manual/current/handoff/
├── evidence-index.json             既有 inventory() 的 33 组路径、指纹、查询和首轮记录
│                                     parser_failure_report_file 引用 select_distinct_on 普通报告
│                                     不是后续归因/修复动态索引，不证明数据或 SQL 等价
├── groups/<group>/                 33 个既有单组引用索引，不复制输入/准备材料/验证报告
│   ├── HANDOFF.md                  prepare-pg-review 按固定模板生成的原件链接
│   └── evidence-index.json         原件相对路径、指纹、待分析编号和导入诊断
└── attribution/                    本轮步骤四，见 2.6；本轮没有 fixes/

原 YAML 位于 cases/postgres/manual/current/ 或 expanded/；
首轮结果位于 current/validation/<group>/；准备材料位于 current/data-preparation/。
指纹只检测文件对应关系，不做备份/恢复，也不证明数据库数据相同。
本轮直接读取第 34 组的 YAML/validation，没有改写已有交接索引。
~~~

### 2.6 步骤四：新版 Skill 的归因与实际对照

~~~text
reports/pg-manual/current/handoff/attribution/
├── attribution-summary.md           源成功/负向分流、主范围进度、具体原因和限制
├── attribution-details.md           详细报告入口、环境/比较口径、34 组明细链接
├── details/<group>.md               逐条 SQL/错误/候选/实际比较；负向简表；匹配简写
├── sqlglot-tasks.md                 20 项受限修复建议或研究事项，没有实施代码修改
├── attribution-statistics.json      分流/进度、版本/Session、对照前后完整数据核验
├── probe-index.json                 候选、后续尝试、实际执行路径、生成/工具失败和边界
└── evidence/
    ├── <case-id>/
    │   ├── candidate.sql            首次独立候选，生成失败时不存在
    │   ├── candidate-02.sql         部分问题的后续候选，首次失败尝试不覆盖
    │   ├── source.sql               明确实测规范化源语法变体时存在
    │   ├── probe-01/                完整采集时由 probe-pg-case 生成
    │   │   ├── probe-report.md      确定性维度比较和错误，不自动归因
    │   │   └── probe-evidence.json  完整有限记录、原生类型、重复执行
    │   └── probe-02/                部分后续候选同样两类执行证据
    └── boundaries/<variant>/        19 个共享规则边界设计，不代表每条原 SQL 全部测过
        ├── source.sql              新 PG 变体，不借用旧 .out
        ├── candidate.sql           独立 Doris 候选
        ├── candidate-02.sql        JSON 字符串转义边界的后续候选，仅该边界存在
        ├── probe/                  成功采集时的 probe-report.md / probe-evidence.json
        └── probe-02/               JSON 字符串边界的第二次实际对照

没有额外 successful-matches.md：241 条匹配按新版 Skill 在各组明细中简写。
候选生成/工具失败集中记录在 probe-index.json，不把缺 JSON 的尝试当完整验证。
~~~

本轮全部 1,725 条 .out 重新读取：源成功 1,427、负向 298、读取异常 0。成功源中 1,186 条差异为主范围；选择调查 204 条，176 个 Case 有完整关联对照，982 条尚未逐条独立复核。负向默认只说明，不逐条改写、不安排错误复刻；MAKE_DATE 补正常新变体并实测源成功后才形成任务。不能把全量分流写成全量归因完成。

模型按 Skill 解读证据、阅读实现、设计候选并归因；probe-pg-case 仅执行显式只读查询与确定性比较。临时 AST/生成器候选不是社区默认输出或生产 fallback；排版/汇总也不等于自动根因分析。

### 2.7 步骤五：当前未执行

~~~text
reports/pg-manual/current/handoff/fixes/   已按用户要求删除，本轮没有重新创建

上一轮 implementation-report.md、regression-report.md、patch、修复前后报告、
测试日志及其他历史试验文件均在本次删除范围内，没有备份。
SQLGlot 的试验修改早已撤回，当前受版本控制文件仍与锁定社区提交一致。

后续仅在人明确选择任务并调用 pg-doris-fix 时，才重新生成
fixes/<batch>/implementation-report.md、regression-report.md 及相应实际证据。
本轮没有执行步骤五，也不创建这些文件的空模板。
~~~

## 3. 数据和源输出前提

用户提供完整 PostgreSQL SQL、DDL、INSERT/COPY 及数据依赖、对应 `.out`。数据准备 Skill 负责说明两个测试库已有什么数据、哪些类型映射有限制，以及每条查询对应哪个执行阶段。

脚本中如果有 `INSERT → SELECT → UPDATE → SELECT`，必须按阶段准备/执行；不能取最终表状态运行全部 SELECT。第一版不自动推断和调度阶段；准备 Skill 给出分阶段库/YAML/命令，由人逐阶段执行。不要给 YAML 加一个未实现的“阶段”字段或假称当前框架支持任意脚本全量回放。

验证器默认外部已准备好结构和数据，不执行建表、INSERT、COPY、导入或一致性拦截。`unverified` 只表示验证器自己没有核验，数据准备报告由人交给归因阶段，不是当前数据一定有问题。

`.out` 通常缺少原生字段类型、精度和 NULL 细节，历史预期不能替代新变体的真实源结果。归因阶段可连接 PG 补查；此时需记录当前 Session 和数据阶段，不能将与历史 `.out` 不对应的当前源结果当成旧测试的真值。

## 4. 步骤一：由人调用数据准备 Skill

在项目任务中明确调用：

```text
使用 $pg-doris-prepare-data。
项目：/Users/a123/Documents/网站维护/doris-sql-validator
输入：我提供的完整 PostgreSQL 测试脚本、DDL、数据依赖和 .out。
在我授权的独立 PostgreSQL/Doris 测试库中准备对应数据；不要覆盖其他库表。
按脚本阶段核验完整记录、重复次数和类型映射，保存实际脚本及中文数据准备报告。
不要调用后续归因 Skill，也不要修改 SQLGlot。
```

连接来自项目 `.env` 的 `POSTGRES_*` / `DORIS_*`，不要把密码复制到输入或报告。此调用需要大模型和授权的数据写入；本项目 Python 命令不会代替用户调用它。

## 5. 步骤二：生成 YAML 并运行确定性验证

导入和验证是两个命令：`import-cases` 从原 SQL/.out 提取只读查询并生成 YAML，`run` 才执行转译和目标查询。本批原始输入位于 cases/postgres/manual/current/assets/ 和 expanded/assets/；已选择的查询 YAML 位于 cases/postgres/manual/current/<group>.yaml 或 expanded/<group>.yaml。当前固定范围由本批助手筛选保存，不是整个官方脚本无差别回放。

下面在项目根目录重跑已有 aggregates 组的 55 条查询，输出到新的 local-rerun/，不覆盖 current 首轮。local-rerun/ 是手动重跑时才会创建的目录，不是第 2 节 current 中已有的文件。不要把完整 aggregates.sql 再导入后覆盖当前 YAML，否则会改变查询范围，并可能纳入未准备数据的其他查询。

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/manual/current/aggregates.yaml

.venv/bin/doris-sql-validator run \
  --path cases/postgres/manual/current/aggregates.yaml \
  --output-dir reports/pg-manual/local-rerun/aggregates
```

每次普通 run 只生成该 output-dir 下的 validation.md 和 validation.json，报告开头已包含该组统计。current/SUMMARY.md 与 validation-summary.json 是 pg_expanded_first_round.py 合并多组首轮结果的本批产物，不是每次 run 自动生成，也不是步骤四的 AI 归因总结。已有首轮失败组的 validation.md 由批次助手保存失败说明；普通 import-cases 在整组零可用查询时只报错退出，不会伪造一次 run 报告。

有 `.out` 时，`run` 不创建 PostgreSQL Adapter，不连接 PG；源库只在数据准备或后续人工对照时使用。运行状态、原 SQL、生成的 Doris SQL、失败信息和源证据范围全部进入报告。`run` 退出码 1 表示存在不匹配/失败，并不表示报告没有生成；退出码 2 通常是输入或配置无法运行。不要用忽略所有错误的命令掩盖它们。

报告统计分开写：

- 成功结果匹配占全部运行查询比例：两端成功且匹配数 / 本轮查询总数，负向报错不计入分子。
- 已取得成功源结果的匹配率：成功匹配数 / 已取得成功源结果数；转译先失败等没有源结果的查询不在此分母，必须同时阅读失败数，不能只报这个较高比例。
- 转译失败、环境问题、字段/行数/行值差异等有中文解释；导入阶段 DDL/DML 跳过与 SELECT 解析失败分开显示。
- 两端同类报错在旧比较器 JSON 中可能仍是 MATCH；报告另列为负向且展开，不能计为成功通过。

首轮 `.out` 走文本规则，不能声称类型完全匹配。通用比较器遇到字段/行数差异会提前返回；后续未检查项不算通过。当前实时浮点容差默认 1e-12，文本输出不自动套用该数值容差。

如果没有任何查询可被导入，Importer 会停止而不会产生一次验证运行；保留命令错误、原脚本和输出交给人工归因，不能写“全部通过”。

## 6. 步骤三：离线建立原文件交接索引

下面展示当前 groups/aggregates/ 的实际生成参数。该目录现已存在且非空，重复执行会被拒绝，不会覆盖旧证据；若另做新一轮交接，需明确指定新的 output-dir，不能将根 handoff/ 当作单组输出目录。

```bash
.venv/bin/doris-sql-validator prepare-pg-review \
  --path cases/postgres/manual/current/aggregates.yaml \
  --report reports/pg-manual/current/validation/aggregates/validation.json \
  --setup reports/pg-manual/current/data-preparation/postgres-setup.sql \
  --setup reports/pg-manual/current/data-preparation/doris-setup.sql \
  --preparation-report reports/pg-manual/current/data-preparation/data-preparation.md \
  --output-dir reports/pg-manual/current/handoff/groups/aggregates
```

本批 inventory() 对 33 组逐个调用相同函数，再汇总根 evidence-index.json，直接引用首轮原始导入失败文件，不复制。普通 prepare-pg-review 不会自行遍历其他组或生成根导航；两层索引都引用原件，单组列出待分析项，根索引汇总 33 组的位置、首轮记录及版本，不是后续分析结论的动态数据库。

`--setup` 可重复指定需要引用的脚本、COPY/CSV 等依赖；只记录原路径和指纹，不复制、递归扫描、搜集凭据或执行文件。若完整原始 SQL 本身包含准备语句，也可将同一文件传给 --setup。准备报告可不提供，但交接说明会标明缺失；工具没有重做数据核验，也不会因为没提供报告而拦截首轮 SQL。

工具核对报告与 YAML 查询原文、配置、`.out` 指纹；新生成的首轮报告还保存 YAML 内容指纹，改动后必须重新运行。旧报告若没有 YAML 指纹，只能根据原 SQL、编号、配置和 `.out` 对应，不得宣称已验证其字节级 YAML 身份。输出目录必须新建或为空，防止覆盖旧证据。

## 7. 步骤四：由人调用归因 Skill

```text
使用 $pg-doris-attribute。
项目：/Users/a123/Documents/网站维护/doris-sql-validator
批次交接目录：reports/pg-manual/current/handoff
单组输入：读取 groups/<group>/evidence-index.json 的入口，使用原 case_file 和 report_file
已有汇总：根 evidence-index.json；导入失败从其 import_failures_file 读取原件
归因输出：同一 handoff/ 下的 attribution/，不改原输入和首轮报告
SQLGlot 仓库：/Users/a123/Documents/网站维护/sqlglot
输入中的每条 SQL 都有对应 .out，先读取历史成功结果或错误，再决定分析范围。
允许在对应测试库执行有限时只读 PG/Doris 对照，不允许改数据或代码。
主要分析 .out 记录源端成功、但转译失败、Doris 失败或结果不同的查询。
源端因非法语法/参数/类型报错的用例保留简要说明，默认不独立改写、不进入主修复清单。
缺对象/权限等单列前提问题；工具读不到已有 .out 则定位读取异常，不推断源 SQL 非法。
实际执行主范围必要的独立 Doris 候选和相关边界；严格错误兼容专项须说明纳入理由。
产出中文详细归因、汇总报告及 SQLGlot 修复任务，其他原因也说明为何不能直接修 SQLGlot。
```

归因不从源结果拼目标常量答案，不自动使用历史 `postgres_rewrites.py` 的固定规则给所有输入套标签；历史固定 753 条脚本仍可研究，但不是任意用户语料的通用流水线。

### 源证据与归因范围

本人工工作流明确约定：**每条用户输入 SQL 都有对应 `.out`**，不把“用户没有提供源执行结果”列为常规分支。先按源 SQL 原文和出现次数读取 `.out`：首轮 SQLGlot 先失败而 JSON 的 source_evidence 为空，不等于没有参考输出。`.out` 缺字段原生类型不影响判断历史执行成功还是报错；归因根因未确定也不是源端状态未确定。

| 对应 `.out` 的内容 | 本轮归因处理 |
| :--- | :--- |
| 源端成功 | 主要能力评估范围。分析转译失败、Doris 失败及字段/结果差异，寻找可实施的 SQLGlot 修复。PG 成功而 SQLGlot Parser 拒绝仍是应分析的问题。 |
| 源端因非法语法、参数或类型组合失败 | 保留编号、源 SQL、具体错误及已有目标表现，写“默认不纳入主修复范围”；即使首轮 MATCH 也不是成功转换证据。默认不独立改写，不要求让 Doris 复刻相同错误。 |
| 源端因缺对象、权限或环境失败 | 标记实际前提问题，不直接用于评价转换能力；需要外部准备或检查原用例的对象前提。 |

若读取器不能定位或解析已经存在的对应输出，属于输出读取/配对异常，不是用户缺少 `.out`，更不是源 SQL 错误。检查原回显、出现次数和工具；能明确恢复则据原件补证，不能恢复时列出读取器问题，不猜源结果或创建转换缺陷任务。这是工具异常处理，不是正常输入的额外运行模式。

负向用例仅在用户明确要求严格错误行为兼容，或与当前已确认修复直接相关、需要作为安全边界时专项验证。判断是否因对应条件报错，不要求跨库错误码/文本一样；也不因两端都被归为 EXECUTION_ERROR 就认定同义。SQLGlot 是转换器而非严格校验器，接受源库会拒绝的输入本身不一定是缺陷，见 [社区 FAQ](https://sqlglot.com/sqlglot.html#faq)。不能仅因错误原文含 syntax 就认定为语法错误，例如 invalid input syntax 也可能是 CAST 非法值。

例如 `SELECT make_date(2013, 2, 30)` 在 PG 是非法日期、在 Doris 是缺函数时，不据此直接生成补丁任务。可补 `SELECT make_date(2013, 2, 28)` 的正常输入，在 PG 实际执行成功后再检查转换能力；新构造的补证/边界 SQL 不属于用户原输入，没有可复用的原 `.out`，不能把负向例的错误当成它的预期结果。原 Case SQL 和 `.out` 不改写。

本次范围调整只影响模型归因、报告模板及后续任务选择，不改变确定性比较器的 MATCH 逻辑、首轮报告和既有统计，也不重跑历史归因。交接索引仍可包含所有失败/负向记录，Skill 必须先按上述规则分流，不能把全部待分析编号都机械地安排为独立改写任务。

### 独立对照命令

人或已被显式调用的 Skill 编写一份单条 Doris 候选，然后调用：

```bash
.venv/bin/doris-sql-validator probe-pg-case \
  --path cases/postgres/manual/current/arrays.yaml \
  --report reports/pg-manual/current/validation/arrays/validation.json \
  --case-id pg-arrays-0134-9c537f22 \
  --candidate reports/pg-manual/current/handoff/attribution/evidence/pg-arrays-0134-9c537f22/candidate.sql \
  --output-dir reports/pg-manual/current/handoff/attribution/evidence/pg-arrays-0134-9c537f22/manual-review-02
```

上述使用实际存在的单组 YAML、首轮报告、原编号和候选，新增尝试目录名为 manual-review-02，不覆盖已有 original-01。此命令只在用户授权继续只读对照时运行；此处列出命令不表示已执行了第二次尝试。

该工具按 YAML 的数据库分别连接 PG/Doris，重放首轮已经保存的社区 SQL，不悄悄升级 SQLGlot 后重新生成另一份输出。记录原生类型（Doris 从执行计划补充，取不到则未知）、精度/小数位、字段/行数/值/重复次数/最终排序以及具体错误；类型不同后仍比较行值。源和独立目标各重复执行一次。PG 会话只读、UTC、ISO/MDY，单次查询超时 10 秒，最多取得 10,000 行，超出则标明证据不完整，不用截断样本宣称一致。Doris 不改变 strict_cast 设置，记录实际会话值。

工具拒绝多语句、DDL/DML、SELECT INTO 和锁定查询。仍应使用受限只读账号，不调用可能有外部副作用的未知 UDF。每个 Doris 执行使用独立连接，避免某次解码错误污染下一条结果。对照命令成功退出只表示记录已生成，不表示候选语义通过；必须阅读证据中的执行错误和分维度结果。

### 明确提供边界变体

```bash
.venv/bin/doris-sql-validator probe-pg-case \
  --path cases/postgres/manual/current/arrays.yaml \
  --report reports/pg-manual/current/validation/arrays/validation.json \
  --case-id pg-arrays-0134-9c537f22 \
  --source-variant reports/pg-manual/current/handoff/attribution/evidence/boundaries/array-empty/source.sql \
  --candidate reports/pg-manual/current/handoff/attribution/evidence/boundaries/array-empty/candidate.sql \
  --output-dir reports/pg-manual/current/handoff/attribution/evidence/boundaries/array-empty/manual-review-02
```

变体由调用者按参数语义设计，工具不自动生成。使用 CTE/VALUES 构造空表、NULL 或重复行，不修改基表。变体没有对应首轮社区 SQL，因此工具不伪造社区重放，也不拿原 `.out` 充当变体答案。证据明确标记“边界变体”。

对照工具不证明全部精度、数组下界、排序唯一性、所有输入或外部表一致。Float 暂不自动放宽精确检查；需要容差时另存误差计算及理由，不把 NUMERIC 换 DOUBLE 当成相同类型。结果大小超限、类型或解码不足应写证据不足。

## 8. 归因报告和修复任务验收

详细报告对主范围差异说明：源 SQL 与 `.out` 成功证据 → 社区输出/错误 → 独立候选与实际执行 → 字段/值/顺序/边界 → 有证据的原因 → 修改 SQLGlot 是否能解决 → 测试与未完成项。保留所有失败候选，不能只展示最后一条成功尝试。默认不纳入的负向用例在同一详细报告中简表说明，不强制填写独立候选、完整分维度比较和边界章节，不另增排除报告。

汇总先列源端成功、源端负向、源端前提问题、已有 `.out` 读取异常的互斥数量。再仅对源端成功且有差异的主范围统计“已确认（注明范围）/部分确认/证据不足/未执行”；专项纳入的负向边界单列理由及进度。明确不纳入主范围的负向记录不是未完成归因积压。原因允许重叠，不能相加；负向同类报错不计成功匹配。若新增主能力匹配率，以 `.out` 记录源端成功的固定查询为分母，包含转译失败，并解释与首轮口径的不同。AI 输出不覆盖首轮报告或改写既有统计。

任务清单重点是 SQLGlot：具体 Parser/AST/Generator 修改、真实代码位置、Schema/类型前提、最小复现、单元与双端测试、验收条件和依赖。Doris 原生能力限制、框架误报、数据/Session 等无法仅修改 SQLGlot 安全解决的记录同样列出证据和去向，不强行生成转换补丁。

主任务须有源端成功的复现证据。负向例只提供能力线索时，先用正常输入实测补证；不能因为源端报错、Doris 返回成功或报错不同就自动创建 SQLGlot 修复。严格错误兼容的专项必须注明用户要求或与已确认修复的直接关系，避免后续修复 Agent 再次扩大为全部负向错误复刻。

未实际执行相应 Skill 时，不会出现“已完成的归因/修复报告”；仓库中的模板不是已分析结果。没有自动执行修复的任务队列。归因完成后，由人把 `sqlglot-tasks.md` 及对应证据交给下一步的修复 Skill。

## 9. 步骤五：由人调用修复 Skill

本节保留将来重新明确授权时的调用方法，不代表当前允许继续改代码。2026-11-12 用户要求维持社区代码，之前试验补丁已全部撤回；目录 fixes/doris-capabilities-001/ 仅保存历史证据。新任务须明确新的批次输出目录，不覆盖这份历史记录。

```text
使用 $pg-doris-fix。
项目：/Users/a123/Documents/网站维护/doris-sql-validator
任务：reports/pg-manual/current/handoff/attribution/sqlglot-tasks.md
归因依据：同目录 attribution-details.md、attribution-summary.md 及证据目录。
目标仓库：/Users/a123/Documents/网站维护/sqlglot
本轮范围：填写要实施的任务编号；未指定时先说明选择的小批次及依赖。
允许修改所选 SQLGlot 任务对应的代码与测试，运行必要的只读 PG/Doris 回归。
不要改原 SQL/.out、表数据或比较策略，不要 commit/push/创建 PR。
输出英文文件名 implementation-report.md、regression-report.md，正文中文。
```

修复 Skill 先读真实仓库指令、Git 状态、任务依据和代码版本，再保存修复前证据、修改相关代码并补测试。缺少证据时先补验证，不把归因候选直接当生产转换规则。

修复沿用步骤四的范围：默认以源端成功复现为依据，负向仅作明确纳入的相关边界或用户要求的专项。历史任务若只要求“让错误 SQL 在 Doris 也报错”，应先指出不在默认范围，而不是直接实施。相关错误检查关注触发条件和原因，不要求错误码/文本逐字相同；未纳入的负向边界说明限制，不计入主修复积压，也不宣称已验证兼容。

必须确认验证框架 import 的是修改后的 SQLGlot，记录 `sqlglot.__file__`、版本、commit 和未提交 diff 的指纹。再用同一 YAML 重新运行 `run`，生成新目录下的 `validation.md/json`；不更改源 SQL、Case ID、`.out` 和数据来提高匹配率。单元测试手动 `annotate_types` 后通过，不代表默认不传 Schema 的运行链路已修好，必须分别说明。

例外是 Importer 阶段的 Parser 失败：这些语句根本不在旧 YAML 中。此时从同一份不变的 SQL/`.out` 重新导入到新 YAML，再运行；保留旧诊断和 YAML，用原始语句编号/源 SQL 对应新 Case ID，新增覆盖单独统计。不能只重跑旧 YAML 声称这些 Parser 问题也已验收，也不能直接比较范围不同的匹配率。

修复后补查类型、顺序或错误时，`probe-pg-case --report` 指向**修复后新报告**，因为工具重放报告中保存的社区 SQL；若指向旧报告，它只会执行旧输出。边界变体的目标 SQL 也必须由修改后的 SQLGlot 实际生成；手写候选只算独立对照，不能替代生成器回归。对新社区 SQL 作原句重跑补取类型是正常操作，不计作独立 AI 改写。

默认只实施 SQLGlot 任务；只有用户明确选择框架修复任务才改框架，Doris 源码、建表装数和提交/发布动作不在默认范围内。遇到新回归、缺少连接、类型/错误反例或用户代码冲突时，报告已完成与未验收部分，不以“有些值相同”关闭任务。

详细实施和回归报告须关联具体任务、真实变更和执行日志。修复 Skill 只在用户显式调用时工作，不会从 `run`、归因 Skill 或任务文件中自动触发。

## 10. 当前实现与验证范围

已实现三个显式调用 Skill、报告约定、证据交接、显式只读对照工具与离线测试。已有 Hive/PG 导入和普通验证入口保留；框架没有模型调用。当前事实：第 12 节首轮现为 34 组、1,725 条；第 13、14 节为历史试验与撤回，相关旧报告已删除；第 15 节是仅重做步骤四的当前进度。不能把旧的“未执行归因”当成当前进度，也不能把历史补丁的结果当成当前社区版能力。完整目录只以第 2 节为准。

离线测试通过 Mock Adapter 验证 SQL + DDL + `.out` → YAML → 首轮报告 → 人工交接 → 独立对照证据；它验证程序交接和比较行为，不证明数据库实际 SQL 兼容性。实际环境读查询的额外验证应单独记录，不能与模拟测试混称。

2026-11-10 的只读 MD5 冒烟已整理到 `reports/pg-manual/smoke/verification-notes.md`，与当前目录结构一致；其中保留 14 条首轮查询和两次原句对照的既有结果，并未重新运行。该批与更早两轮评估仍只在本地保留，不随当前版本发布，不视为下面 current 批次的结果。

## 11. 2026-11-11：原有数据准备与扩展前首轮记录

本节只保留 753 条种子范围的准备与早期执行历史，不是当前目录定义。最新首轮为第 12 节的 1,725 条（含 3 条普通解析失败记录）；本节的 750/160 等数字不再代表 current/SUMMARY.md 的当前结果。这里的旧范围重跑命令会把结果恢复成较小语料，不用于重跑最新扩展报告。报告目录统一参照第 2 节，不再另列一份不完整的历史报告树。

本批首次在两端创建独立库 `dsv_pg_manual_20261111`。之后按用户要求修复框架的输出配对问题，重新完整核验同一批库表数据，并从相同 SQL/.out 重新生成 YAML、重跑并覆盖 current 报告。没有修改 SQLGlot、原始查询或标准答案，没有执行步骤三至五；更早历史两轮报告不受影响。

原始 753 条选择和来源指纹仍保存在 cases/postgres/manual/current/scope.json；19 份 YAML 包含其中 750 条可运行查询，另外 3 条导入失败。原始脚本、官方 .out、COPY 数据与许可保留在同一输入目录下。它们是第 12 节扩展语料的组成部分，不是与 current 并列的另一套现有首轮报告。

当前 [数据准备报告](../reports/pg-manual/current/data-preparation/data-preparation.md) 说明：双端完整表记录一致且未偏离首次准备的数据（保留重复和 NULL），不表示类型域/约束完全相同。本轮没有清库或重复装数。全部 753 条 PG 查询重新执行后，620 条成功显示文本及重复次数与 `.out` 一致、133 条都失败但未确认同因；参考输出定位失败为 0。

扩展前的首轮：750 条进入运行器，160 条成功结果匹配；其中 122 条转译失败、未发往 Doris，另外 628 条实际执行 Doris。这批旧报告已从 current 移除，最新 [首轮 SUMMARY](../reports/pg-manual/current/SUMMARY.md) 见第 12 节。负向同类报错不加入成功匹配分子；3 条 `ORDER BY ... USING` 的导入失败不包含在运行器分母中。

早期修复的 9 条输出定位错误已恢复：5 条是 AST 指纹计数与原文查找口径不同，4 条是 SQL 字面量等受保护内容之外的空白行差异。共享的 `recorded_output/pg_echo.py` 统一识别与计数，严格保留受保护内容。之后还补充了展开记录、多行单元格、完整外层回显和多行 WARNING 支持。实际执行和比较结果以最新逐组报告为准，不把读取成功当成兼容性通过。

本批使用的外部助手及真实调用顺序如下。它只适用于这批经审查的固定样本，不替代步骤四中由人调用的 Skill，不是验证器自动数据导入或 AI 调度。数据已准备完后再执行 `--prepare` 会因同名数据库存在而拒绝，不会清库。

```bash
# 首次原始材料复制仅用于本机迁移；旧语料不随当前远程版本发布
.venv/bin/python scripts/pg_manual_sample.py \
  --collect-from cases/postgres/capability

# 步骤一：由显式调用的准备 Skill 执行已审查脚本，创建新库/装数/完整核验
.venv/bin/python scripts/pg_manual_sample.py \
  --prepare --database dsv_pg_manual_20261111

# 本次步骤一：只读重新核验本批有创建来源的专用库，不重复 CREATE/INSERT
.venv/bin/python scripts/pg_manual_sample.py --reverify

# 本次步骤二：完整重新导入和执行；按用户明确授权覆盖 current YAML/报告
.venv/bin/python scripts/pg_manual_sample.py --validate --overwrite

# 仅离线更新可读汇总（需要时），不重新执行查询
.venv/bin/python scripts/pg_manual_sample.py --summarize
```

本批原件已经保存在 current，不要求下一位使用者具备旧的 `cases/postgres/capability/`。新用户语料按步骤一、二的通用 Skill/CLI 处理；重跑单组的命令见 [当前样本说明](../cases/postgres/manual/current/README.md)。

`--reverify` 只接受与原创建标记和相同输入指纹对应的本批专用库，重读结构/完整记录并重跑全部源查询，不能借此复用不明数据库。`--overwrite` 不改变默认防覆盖行为；只有人明确要求替换当前报告时使用，先检查同一输入和目标库，不使用旧验证结果。`--resume` 是保留已完成报告的续跑，与 `--overwrite` 互斥。首次运行仍用 `--prepare`、`--validate`；本次没有重做建表装数。

之后如继续，只在用户明确调用后进行步骤三及归因/修复，不因本次确定性报告产生错误而自动启动。远程只保留最新流程的路径与文件，旧证据在本地忽略而不删除，见 [PUBLISHING.md](PUBLISHING.md)；本次没有 commit/push。

## 12. 最新首轮范围：1,725 条（含 3 条解析失败）

当前普通报告已有 34 组、1,725 条：最初扩展 33 组、1,722 条，后来将 select_distinct_on 的 3 条 Parser 失败纳入普通 YAML/validation。当前成功匹配 241 条、转译失败 136 条，Doris 执行结果仍为 1,589 条。以下保留最初扩展的执行历史，不把后来统一失败报告结构说成重新运行全部数据库查询。

用户授权替换旧首轮报告后，保留原有 750 条，再从两批新官方脚本的 2,165 条可读取查询中纳入 972 条。其余 1,193 条因未准备的表/自定义对象、非确定性或外部资源安全条件暂不运行；没有为扩大数量而制造新的数据前提。1,722 条是用例数，源 SQL 原文去重为 1,711 条。

本节描述扩展首轮当时的动作：只在框架外读取并核验原有 21 张表/视图，完整记录与初始数据一致；没有 DDL/DML。确定性 CLI 用 .out 作为源证据，只执行 Doris。该阶段不调用归因或修复 Skill、不修改 SQLGlot；后来第 13、14 节的试验与撤回是独立后续阶段。

```text
cases/postgres/manual/current/
  <script-name>.yaml                 原有 19 组、750 条；本轮全部重跑
  expanded/
    README.md                       最新扩展范围及单组复现命令
    assets/                         新增 20 组官方 SQL/.out 原件
    <script-name>.yaml              新增 14 组、972 条
    selection.json                  纳入范围与未纳入查询的源 SQL、原因
    environment-check.json          输入准备阶段只读核验
scripts/pg_expanded_first_round.py   显式本地复现助手；只读预检、范围筛选和 CLI 调用
```

输入目录如上；报告及旧轮归档的位置全部按第 2 节的实际报告树阅读。current/validation/aggregates/ 等普通组实际只有 validation.md/json；command.log 出现在历史补丁 after/<group>/，不再混写到本批首轮组目录。

最初扩展结果为 1,722 条、241 条成功匹配、133 条转译失败、1,589 条 Doris 执行结果；统一加入另 3 条解析失败后的当前统计为 **1,725 条、241 条成功匹配（13.97%）、136 条转译失败、1,589 条 Doris 执行结果**。负向同类报错单列，不计入成功匹配。完整统计和不能据此判断的内容见 [SUMMARY.md](../reports/pg-manual/current/SUMMARY.md)。旧首轮已从 current 移除；数据准备、其他历史两轮及人工交接/归因材料不删除。

只有明确要再次替换当前报告时，才执行：

```bash
.venv/bin/python scripts/pg_expanded_first_round.py --run-and-replace
```

仅重跑某一组时，直接使用普通 `run --path ... --output-dir reports/pg-manual/local-rerun/<group>`，不要调用旧的固定 753 条助手覆盖最新扩展报告。该助手仍不自动调度 Skill，后续归因交接使用所选组的 YAML 和对应组 `validation.json`。

## 13. 历史步骤四、五：旧报告已删除

2026-11-11 曾按当时模板执行部分归因和首批修复试验。当时范围 1,722 条，候选尝试 109 条，98 条有完整对照；这些只作历史说明，不是本轮进度，更不是全量归因完成。

当时针对数组构造和 NULL 排序做过 SQLGlot 试验，补丁下成功匹配曾由 241 增至 260。SQLGlot 修改于 2026-11-12 撤回；2026-11-13 按用户要求删除旧 attribution/ 和 fixes/ 的全部报告、候选、patch、回归及日志，没有备份。旧实施/回归报告已不存在，不再提供失效链接，也不把这些历史数字当作当前验收依据。

当前重新输出的 attribution/ 仅为步骤四，见第 15 节。不能用历史补丁结果描述当前社区 SQLGlot 的能力。

## 14. 社区代码基线、失败报告统一与引用式交接

SQLGlot 受版本控制的文件已在 2026-11-12 撤回试验修改，并于 2026-11-13 本轮结束复核，仍与社区提交 feb0e08aba28a29590596bb3f5761fbaeb0e98b9 一致。用户原有未跟踪文档 DORIS_TRANSPILATION.md 保留；本轮没有版本升级、commit/push 或代码修复。

select_distinct_on 的 3 条 ORDER BY USING 查询现已使用普通 YAML 和 validation.md/json：失败阶段 source_parse，未进入 Doris 执行。新版步骤四读取其 .out 后，2 条源成功进入主范围，另 1 条源端负向默认只说明。首轮 Parser 拒绝不能直接认定源 SQL 非法，也不再采用 import-failure.json 专用失败文档。

手写的 current/handoff/HANDOFF.md 总导航此前已移除；仅 groups/<group>/HANDOFF.md 是步骤三固定命令生成的单组入口。用户要求按流水线运行时，不自行增加其他文档或总导航。

此前已取消交接备份功能，33 组重复副本经指纹核对后删除。prepare-pg-review 只生成 HANDOFF.md、evidence-index.json 原件引用，指纹不承担备份/恢复。本轮保持这批索引、输入和首轮报告不变；不重新复制文件。

## 15. 2026-11-13：仅按新版归因 Skill 重做步骤四

按用户要求删除旧步骤四、五的 981 个文件，没有备份；只重新执行 pg-doris-attribute，没有调用 pg-doris-fix。生成物全部沿用已有归因模板类型，完整目录见 2.6。

本轮重新读到全部 1,725 条对应 .out：源成功 1,427，源负向 298，环境前提问题 0，读取异常 0。成功源的首轮匹配为 241；其余 1,186 条主范围差异中，本轮选择调查 204，176 个 Case 有完整关联对照（174 个执行原 SQL，2 个执行明确标明的规范化源语法变体），28 个缺完整证据，982 个未逐条独立复核。

负向默认只保留编号、源 SQL/错误、已有目标表现和排除理由，不独立改写、不要求双端错误完全相同、不计主修复积压。MAKE_DATE 的原非法日期仍排除，但另补合法日期、闰日和 NULL 变体真实执行 PG 成功，再据此形成任务。PG_INPUT_IS_VALID 成功返回 false 仍是成功源查询，不能因输入看起来非法而排除。

本轮归因进度、实测候选、具体 SQLGlot 修复方向、Doris/框架限制和不利证据见：

- [attribution-summary.md](../reports/pg-manual/current/handoff/attribution/attribution-summary.md)：先总结、说明分流和实际完成范围。
- [attribution-details.md](../reports/pg-manual/current/handoff/attribution/attribution-details.md)：环境/比较口径、34 组逐条明细。
- [sqlglot-tasks.md](../reports/pg-manual/current/handoff/attribution/sqlglot-tasks.md)：20 个受限修复建议或研究事项，不是已实施补丁。

有行值匹配的候选仍可能存在类型、最终顺序或边界差异；每项分别给出实际证据，不把共享边界当作全部原 SQL 的逐查询验证。对照前后只在框架外只读核验原有 21 表/视图，不执行 DDL/DML，不新增 Gate。

最终核对：原输入、数据准备、首轮结果和步骤三的 269 个文件指纹未变；报告本地链接可定位；没有 fixes/ 目录；SQLGlot tracked diff 为空。下一步只有人明确授权修复时才进入步骤五。
