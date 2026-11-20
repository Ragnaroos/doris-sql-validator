# Doris SQL Validator

将 PostgreSQL/Hive 的只读查询交给社区 SQLGlot 转成 Doris SQL，再比较源端证据与 Doris 的执行结果。

本工作目录只保留可复用的框架、Skill、报告模板和使用文档，不附带测试 SQL、参考输出、Case YAML、数据文件或已执行报告。用户自行提供输入，运行后按指定目录生成产物。

支持两种验证方式：

- Recorded Output：读取 PostgreSQL pg_regress 的 .out 或 Hive QTest 的 .q.out，只执行 Doris。
- Live Source：实时执行源数据库与 Doris，再比较结果。

CLI 不调用模型、不执行 DDL/DML、不建表装数，也不自动修复 SQLGlot。PostgreSQL 的数据准备、差异归因和修复由用户显式调用项目 Skill。

归因阶段只保存批次汇总和逐 Case Markdown，真实对照事实、原因和修复要求写在同一份 Case 文档。同阶段多条候选可通过 probe-pg-batch 一次传入 JSON 数组，单条可用 probe-pg-case；两者只向终端返回事实，不生成独立 SQL、执行 JSON 或 evidence/ 目录。批量入口支持中文 Markdown 事实片段及统计，归因和修复结论仍由人显式调用 Skill 分析；后续修复读取汇总中的任务索引与关联 Case 文档。

修复阶段只保存批次汇总和逐修复任务 Markdown，将修改说明、真实回归和验收合在一起；一个任务可以关联多条 Case。代码/测试留在授权的 SQLGlot checkout。run --stdout 可在重新转译、执行和比较后直接返回结果，不额外写回归 JSON；完整步骤及产物命名见工作流步骤四。

## 文档入口

- [PostgreSQL 完整工作流](docs/POSTGRES_MANUAL_WORKFLOW.md)：数据准备、验证、直接归因、修复与回归，逐步说明产物内容和位置。
- [用户指南](docs/USER_GUIDE.md)：输入格式、YAML、连接配置、比较规则和报告解读。
- [发布约定](docs/PUBLISHING.md)：源码与运行数据的边界、提交前检查。

## 安装

需要 Python 3.12；本地数据库容器另需 Docker Compose。以下命令从新工作目录根目录执行：

~~~bash
git clone https://github.com/tobymao/sqlglot.git ../sqlglot
git -C ../sqlglot checkout feb0e08aba28a29590596bb3f5761fbaeb0e98b9

python3.12 -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/uv sync --extra dev
cp .env.example .env
~~~

已有 ../sqlglot 或 .env 时不要重复 clone 或覆盖。项目使用相邻 SQLGlot 的 editable dependency；需要其他版本时自行选择提交，报告应记录实际版本。地址、端口和账号在自己的 .env 中配置，不提交真实凭据。

## 使用自己的输入

以下是约定路径，不是仓库附带文件；先自行提供 SQL 和对应的 pg_regress 输出：

~~~text
inputs/postgres/queries-001/            一次输入批次，用户自行准备，不提交
├── queries.sql                         用户原始脚本，保留原文件名；DDL/DML 会被 Importer 跳过
└── queries.out                         该脚本及相应数据阶段对应的 pg_regress 参考输出

reports/data-preparation/         步骤一和二的准备文件平铺，不建立子目录
  queries-001-data-preparation.md      类型映射、核验命令/输出、差异与限制的合并报告
  queries-001-postgres-setup.sql       源端准备脚本；不替换原始输入
  queries-001-doris-setup.sql          目标准备脚本；不另生成核验 JSON
  queries-001-cases.yaml               步骤二生成，保存查询原文/行号/Case ID 和 .out 引用
reports/validation/queries-001-validation.json   本批次唯一首轮报告（运行信息、总结、逐查询记录）
~~~

queries 来自示例输入名 queries.sql，不是预设名称；实际输入叫什么，就使用对应名称。再次上传或重新准备时用下一个编号，例如 queries-002，三份产物均使用相同前缀，仍放在同一个 data-preparation/ 目录。命名由用户或执行 Skill 的 Agent 确定，不是 CLI 自动命名；完整规则见工作流第 2、4 节。

表查询须先在验证器之外准备可比较的逻辑数据，再执行：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input inputs/postgres/queries-001/queries.sql \
  --recorded-output inputs/postgres/queries-001/queries.out \
  --source-database dsv_demo --target-database dsv_demo \
  --output reports/data-preparation/queries-001-cases.yaml

.venv/bin/doris-sql-validator cases-lint --path reports/data-preparation/queries-001-cases.yaml

.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --output reports/validation/queries-001-validation.json
~~~

主工作流必须传入 --recorded-output，且 YAML 必须包含参考输出引用。CLI 仍保留 Live Source 诊断能力，但不作为主流程缺少 .out 时的替代。导入和 lint 不连接数据库；run 仍需 Doris。CLI 必须显式指定 --path，不依赖内置 Case 文件。YAML 可以在报告目录中跨目录引用原 .out，不复制原件；每次运行直接读取当前 .out，不保存或核对它的内容指纹。

仅查看转译结果，无需文件或数据库：

~~~bash
.venv/bin/doris-sql-validator transpile --source-dialect postgres "SELECT 1 AS value"
~~~

## 报告与限制

run 默认只生成 `<batch-id>-validation.json`，包含 run（运行信息）、summary（总结）和 queries（逐查询记录）。加 --stdout 则只向终端返回同结构 JSON，不写文件，且不能与 --output 同用。匹配仅保留 ID、源 SQL 和结论；差异才附生成 SQL、实际错误或有限反例，不另输出 Markdown、Digest 或重复样本。源端负向用例单列，默认不进入后续归因清单；不回写 YAML。

比较执行状态、错误类别、字段数量/显式 Alias/可用类型、行数、行值、重复次数与顺序。MATCH 仅表示当前证据未发现差异；缺少原生类型或边界证据不等于这些检查通过。数据、Session、UDF 和驱动表示差异也可能影响结果，不能直接归为 SQLGlot 缺陷。

## 开发检查

~~~bash
.venv/bin/pytest tests/unit
git diff --check
~~~

核心测试自行在临时目录构造最小输入，不依赖已删除的批次数据或数据库。三个 Skill 及其空白报告模板保留在 .agents/skills/，不会由 CLI 自动调用。
