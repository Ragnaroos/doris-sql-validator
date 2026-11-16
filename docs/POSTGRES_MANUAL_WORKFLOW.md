# PostgreSQL → Doris 验证与修复工作流

本指南面向使用 PostgreSQL 测试 SQL、DDL/数据和 .out 的用户，说明如何准备数据、运行验证、分析差异并修复 SQLGlot。所有 Shell 命令从仓库根目录执行；安装方式见 [README](../README.md#安装)。

[快速示例](../examples/postgres/basic/README.md)提供不依赖既有本地环境的输入与准备脚本。这里的 reports/demo 是示例输出位置，可替换成自己的运行目录。

## 1. 职责与执行方式

| 步骤 | 工具 | 输入 | 输出 |
| :--- | :--- | :--- | :--- |
| 1. 准备数据 | 外部 SQL 客户端，或显式调用 pg-doris-prepare-data Skill | DDL、INSERT/COPY、数据依赖、源 SQL/.out、双端测试库 | 准备 SQL、数据核验与类型映射报告 |
| 2. 确定性验证 | import-cases、cases-lint、run | 源 SQL/.out → Case YAML | validation.md、validation.json |
| 3. 证据交接 | prepare-pg-review | 本次 YAML/报告与准备材料 | HANDOFF.md、evidence-index.json 原件引用 |
| 4. 差异归因 | 显式调用 pg-doris-attribute Skill；必要时用 probe-pg-case | 交接入口、源证据、代码库和只读连接 | 归因明细、汇总、修复任务、实际对照证据 |
| 5. 修复与回归 | 显式调用 pg-doris-fix Skill | 已选择任务及可信证据、SQLGlot checkout | 代码/测试、实施报告、回归报告 |

前三类 CLI 命令是普通 Python 程序，不调用模型。三个 Skill 是给人工调用的 Agent 的说明，位于 .agents/skills/；可以在支持项目 Skill 的客户端调用，也可将 SKILL.md 和相关模板提供给其他 Agent。Skill 不会被 run 自动触发。

只读验证不执行 DDL/DML，不生成或导入 Parquet，不负责复制数据。数据准备的数据库写入和后续代码修复需分别明确授权。提交、推送或创建 PR 不是修复 Skill 的默认动作。

## 2. 输入、样例与目录

~~~text
examples/postgres/basic/                 推荐入门：完整小型数据与查询，操作见该目录 README
  postgres-setup.sql / doris-setup.sql    双端专用库、表和相同五行数据
  queries.sql / expected.out             四条查询与参考输出
  constant.sql / constant.out            无表依赖的常量输入
  generated-*.yaml                       导入命令生成的本机文件

cases/postgres/manual/current/           官方回归样本的固定选择范围
  assets/                               原始 SQL/.out，不等于可直接全量执行的脚本
  setup/                                PostgreSQL 准备脚本与 COPY 依赖
  <group>.yaml                          可选择运行的查询，连接库名应与自己的环境对应
  expanded/                             额外输入；部分仅常量，部分仍有对象/Session 前提
cases/postgres/out-reader-samples/        只检查真实回归文件的导入及 .out 读取格式
reports/pg-manual/current/               固定版本参考报告，不是运行新样例的前置环境
~~~

原始脚本中的每条查询必须与对应数据阶段一致。若脚本为 INSERT → SELECT → UPDATE → SELECT，不能装入最终数据后运行全部查询；需要在框架外分阶段准备和执行。Importer 不实现任意测试脚本的事务/Session/变更调度。

Recorded Output 的 .out 必须位于生成 YAML 所在目录或其子目录。它由 YAML 相对路径引用并校验 SHA-256；不要把 YAML 写到与 .out 无关的 reports 目录，再让它通过 ../ 逃出输入根目录。

## 3. 环境配置

先按 README 安装 Python 3.12 和相邻 SQLGlot checkout，并从 .env.example 创建自己的 .env。实际地址和密码来自 POSTGRES_*、DORIS_*；YAML 仅保存逻辑连接名及可选数据库。

~~~bash
./scripts/postgres.sh up
./scripts/postgres.sh smoke
.venv/bin/doris-sql-validator doctor --source-engine postgres
~~~

Doris 由用户自行启动并配置。doctor 会检查两端；只有 .out 的验证不要求源库可用，但后续归因的实时源补证需要 PostgreSQL。

不要公开 .env，不在提示词、YAML 或报告中填写密码。使用独立测试库和只读验证账号；准备阶段需要的建表/装数账号应限于授权库。

## 4. 步骤一：准备相同逻辑数据

### 4.1 直接使用提供的示例

按 [快速示例的数据准备步骤](../examples/postgres/basic/README.md#3-在验证器外准备表数据)，在验证器外执行：

- examples/postgres/basic/postgres-setup.sql：由 psql 执行。
- examples/postgres/basic/doris-setup.sql：由 MySQL 兼容客户端执行。

两者新建 dsv_demo，包含重复记录和 NULL，遇到同名库应先停止检查，不删除不明数据库。Recorded Output 只运行 Doris 时，可以仅准备目标端；要用实时 PG 补证或 Live Source 时再准备源端。

### 4.2 对自己的脚本调用数据准备 Skill

在项目任务中明确提供材料与写入授权，例如：

~~~text
使用 $pg-doris-prepare-data。
项目：当前 doris-sql-validator 仓库。
输入：examples/postgres/basic/queries.sql、expected.out，以及同目录双端准备 SQL。
允许仅在指定的 PostgreSQL/Doris 专用测试库中建表装数；遇到已存在且来源不明的库表停止询问。
逐阶段核对完整记录和重复次数，说明类型域、NULL、Session 与版本限制。
输出到 reports/demo/data-preparation/；只记录真实执行结果。
不修改源 SQL/.out，不修改 SQLGlot，不自动进入下一步。
~~~

Agent 应输出准备报告和实际脚本，格式由 .agents/skills/pg-doris-prepare-data/assets/ 定义。仅有 COUNT 或样本不能证明全表相同；类型映射和记录值一致也应分别说明。

## 5. 步骤二：导入 YAML 并运行验证

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input examples/postgres/basic/queries.sql \
  --recorded-output examples/postgres/basic/expected.out \
  --source-database dsv_demo --target-database dsv_demo \
  --output examples/postgres/basic/generated-recorded.yaml

.venv/bin/doris-sql-validator cases-lint \
  --path examples/postgres/basic/generated-recorded.yaml

.venv/bin/doris-sql-validator run \
  --path examples/postgres/basic/generated-recorded.yaml \
  --output-dir reports/demo/validation
~~~

输出为 reports/demo/validation/validation.md 和 validation.json。生成的 Doris SQL 只写入报告，不回写 YAML。没有 .out 时不传 --recorded-output，框架会实时执行 PostgreSQL 和 Doris，见快速示例的 Live Source 步骤。

run 退出码 1 通常表示发现了差异或失败，报告仍已生成；输入、配置或参数错误可能返回 2。不要以忽略所有退出错误的方式掩盖未完成验证。

报告先给数量与匹配率，再列逐条 SQL/结果/错误。成功匹配与源端负向同类报错分开统计。首轮报告最多保存五行样本；.out 缺少的原生类型不能当成已经通过比较。详细规则见 [用户指南](USER_GUIDE.md)。

## 6. 步骤三：生成引用式交接入口

~~~bash
.venv/bin/doris-sql-validator prepare-pg-review \
  --path examples/postgres/basic/generated-recorded.yaml \
  --report reports/demo/validation/validation.json \
  --setup examples/postgres/basic/postgres-setup.sql \
  --setup examples/postgres/basic/doris-setup.sql \
  --output-dir reports/demo/review
~~~

若数据准备 Skill 已实际生成报告，可再加：

~~~text
--preparation-report reports/demo/data-preparation/data-preparation.md
~~~

命令只生成 HANDOFF.md 和 evidence-index.json，引用原始 YAML、SQL/.out、首轮结果与准备材料；不复制文件、不连接数据库、不调用模型。输出目录非空时拒绝覆盖。

HANDOFF.md 给出阅读顺序与逐条待分析编号；evidence-index.json 保存对应路径和文件指纹。缺少准备报告会明确列出，不能假定环境已验证。改变原件后应重新运行验证和交接，避免用新 SQL 解释旧报告。

## 7. 步骤四：分析差异并形成任务

明确调用：

~~~text
使用 $pg-doris-attribute。
交接入口：reports/demo/review/HANDOFF.md、evidence-index.json。
SQLGlot checkout：../sqlglot；使用首轮报告记录的版本进行核对。
按每条原 .out 先区分源成功、源负向、环境前提和输出读取异常。
对源成功但存在差异的查询进行代码分析和必要的独立 Doris 对照，解释类型、行值、顺序和相关边界。
输出到 reports/demo/attribution/：详细报告、汇总与 sqlglot-tasks.md，以及实际候选/执行证据。
覆盖全部主范围或逐条标明具体阻断；不要自行把未调查项判成不值得分析，也不要把分组视为已完成归因。
不修复代码，不改数据库数据，不自动进入步骤五。
~~~

源端成功且有差异是主要修复评估范围；源端负向默认只保留源 SQL/错误及目标表现，不为复制 PG 错误逐条改写。源端成功返回 false 的输入校验函数不是负向用例。由负向线索提出功能任务时，应另构造正常输入并真实执行源库成功。

独立 Doris 候选是待验证假设，不自动称为同义 SQL。一次行值多重集合相同不证明类型或最终排序相同，一次候选失败也不证明 Doris 完全无法模拟。报告必须区分具体根因、证据不足和未执行，不拿“部分确认”等状态替代原因。

如果所有示例查询都匹配，应报告未发现可修复差异，不制造错误或空的修复任务。

### 7.1 只读对照命令

Agent 构造候选后使用 probe-pg-case。以下演示重跑常量原句以补取类型等证据，并不是 AI 独立改写：

~~~bash
demo_case_id=$(.venv/bin/python -c \
  "from pathlib import Path; from doris_sql_validator.case_loader import load_case_file; print(load_case_file(Path('examples/postgres/basic/generated-recorded.yaml')).definition.cases[0].id)")

.venv/bin/doris-sql-validator probe-pg-case \
  --path examples/postgres/basic/generated-recorded.yaml \
  --report reports/demo/validation/validation.json \
  --case-id "$demo_case_id" \
  --candidate examples/postgres/basic/constant.sql \
  --output-dir reports/demo/attribution/evidence/constant/probe-01
~~~

工具会实际执行 PG、报告中保存的社区 Doris SQL（若可生成）、给定候选及重复执行，保存 probe-report.md、probe-evidence.json。它不构造候选、不归因；需要两端连接与对应数据。新边界通过 --source-variant 指定新的 PostgreSQL SQL 文件，源结果必须真实执行，不能借原 .out。

## 8. 步骤五：修复并验证新生成的 SQL

选择有证据支持的任务，再显式调用：

~~~text
使用 $pg-doris-fix。
任务清单：reports/demo/attribution/sqlglot-tasks.md，附详细归因、汇总和对应执行证据。
目标 checkout：../sqlglot；仅处理明确选定的任务。
允许修改相应 SQLGlot 代码和测试，并执行必要的只读数据库回归。
修复前后保留相同源 SQL/.out、数据条件与比较范围。
输出到 reports/demo/fixes/fix-001/，包含 implementation-report.md、regression-report.md。
不改原答案/数据，不修改验证框架，不 commit/push/创建 PR。
~~~

修复后必须使用修改后的 SQLGlot 从源 SQL 重新生成 Doris SQL并运行；手写候选通过不是生成器修复验收。记录实际 import 路径、commit 和未提交 diff；仅手工 annotate_types 后通过不能证明默认无 Schema 调用链路已修好。

已有 YAML 中的 Case 重跑同一 YAML并写入新的回归目录。涉及 Importer Parser 修复时，从不变 SQL/.out 重新导入到新 YAML，按原语句位置对应新增 Case，单列覆盖范围变化。边界的目标 SQL 也须由修复后的 SQLGlot 生成。

单元测试、类型、精度/Scale、完整有限记录与重复次数、最终顺序、相关错误边界分别验收。Doris 能力限制、框架/驱动问题和缺少数据不能强行作为 SQLGlot 任务关闭；未执行的检查不能写通过。

## 9. 产物结构

下面是每次运行可采用的结构，不要求每个目录预先存在。没有开展的阶段不创建空报告。

~~~text
reports/<run>/
├── data-preparation/                外部准备阶段的 SQL、核验和类型映射
│   ├── data-preparation.md
│   ├── postgres-setup.sql / doris-setup.sql
│   └── data-verification.json
├── validation/                      run 的确定性输出
│   └── validation.md / validation.json
├── review/                          prepare-pg-review 的离线引用式入口
│   └── HANDOFF.md / evidence-index.json
├── attribution/                     人调用归因 Skill 后的结论与原始对照证据
│   ├── attribution-details.md / attribution-summary.md / sqlglot-tasks.md
│   └── evidence/<case-id>/           候选 SQL、边界及 probe-report.md / probe-evidence.json
└── fixes/<fix-batch>/                人调用修复 Skill 后的实施与回归材料
    └── implementation-report.md / regression-report.md、测试日志和真实生成 SQL
~~~

目录说明与模板仅描述产物职责，不意味着相应操作已经完成。报告中保留实际版本、输入范围、失败证据与限制，不写个人会话、文件清理史或补丁撤回等开发过程说明。SQL/.out、完整执行证据与索引用于追溯，不以文档润色更改查询结果。

## 10. 复用官方回归样本

先阅读 [样本目录说明](../cases/postgres/manual/current/README.md)。源码包包含 34 份固定选择 YAML，共 1,725 条查询；不是 PostgreSQL 全量 SELECT 语法覆盖。

原文件中的所有 DDL/DML 和 SELECT 不一定属于同一个数据阶段，也不保证可在空库中直接执行。使用准备脚本和 COPY 数据依赖为自己的独立库重建所需阶段，核验后重新生成指向自己库名的 YAML；不要假设附带报告中的数据库在你的机器上存在。

[附带报告](../reports/pg-manual/current/SUMMARY.md)只用于学习结果结构与复核已保存证据。样例执行结论受版本、Session、类型映射及固定数据限制，不能当作通用通过率。
