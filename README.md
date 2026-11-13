# Doris SQL Validator

把多种源方言的只读 SQL 交给社区版 SQLGlot 转译为 Doris SQL，并比较源端证据与 Doris 执行结果。当前已实现 Hive 和 PostgreSQL；后续方言通过新增 Importer/Adapter 接入，不复制比较器。

面向使用者的完整操作流程、输入格式、YAML 字段、运行命令和报告解读见
[`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)。

当前 PostgreSQL 人工连续链路见
[`docs/POSTGRES_MANUAL_WORKFLOW.md`](docs/POSTGRES_MANUAL_WORKFLOW.md)：
人调用数据准备 Skill → 确定性验证 → 离线交接 → 人调用归因 Skill → 人调用修复 Skill。
三个项目 Skill 位于 `.agents/skills/`，均禁止隐式调用；CLI 不包含任何模型调用。
报告文件名使用英文、正文默认中文，Parser、AST、Generator 等通用术语允许使用英文。
归因阶段生成 `attribution-details.md`、`attribution-summary.md`、`sqlglot-tasks.md`；
修复阶段生成 `implementation-report.md`、`regression-report.md`。旧中文报告不批量改名或覆盖。

最新完整输入与首轮实测见 [`cases/postgres/manual/current/README.md`](cases/postgres/manual/current/README.md)
和 [`reports/pg-manual/current/SUMMARY.md`](reports/pg-manual/current/SUMMARY.md)。历史两轮评估仍在本地旧路径，
不作为当前结果，也不纳入远程发布。发布范围见 [`docs/PUBLISHING.md`](docs/PUBLISHING.md)。

YAML 是验证器唯一的批量输入。Importer 可以把 `.sql`、Hive `.q` 以及可选的 `.out/.q.out` 转成精简 YAML。运行器不创建表、不执行 DDL/DML、不生成或导入 Parquet，也不保证两端使用相同数据。

## 两段式流程

```text
可选的输入转换
  单条 SQL / .sql / .q + 可选 .out/.q.out
    → Importer 拆分语句并用 SQLGlot 筛选只读 Query
    → cases.yaml（内含导入摘要和非 accepted 诊断）

验证
  cases.yaml
    → 有 recorded_output：读取参考输出，不连接源数据库
    → 无 recorded_output：连接 source.engine 对应的源数据库
    → SQLGlot 生成 Doris SQL
    → Doris 执行
    → 比较并覆盖写入一份最终 Report
```

`transpile` 是单独命令，只生成 Doris SQL，不是 YAML 中的一种运行模式。

## 安装与环境

项目使用 Python 3.12，并将相邻的 `../sqlglot` 社区仓库作为 editable dependency。
克隆本项目后，在项目根目录准备该依赖；已有相邻 checkout 时不要重复 clone。
以下提交对应当前报告的社区代码基线，不包含试验补丁：

```bash
git clone https://github.com/tobymao/sqlglot.git ../sqlglot
git -C ../sqlglot checkout feb0e08aba28a29590596bb3f5761fbaeb0e98b9
```

然后安装验证框架依赖；数据库需自行启动并配置，仓库不包含真实 `.env`：

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/uv sync --extra dev
cp .env.example .env
```

本地 Hive：

```bash
./scripts/hive.sh up
./scripts/hive.sh status
./scripts/hive.sh smoke
```

本地 PostgreSQL 验证源（与 Hive Metastore 的 PostgreSQL 完全独立）：

```bash
./scripts/postgres.sh up
./scripts/postgres.sh status
./scripts/postgres.sh smoke
```

数据库实际地址和凭据来自 `.env`。YAML 中的 `connection_profile` 是不含密码的逻辑标识；当前 Adapter 仍读取 `HIVE_*`、`POSTGRES_*`、`DORIS_*` 环境变量。`database` 会覆盖 Adapter 的默认数据库。

## 导入脚本

普通 SQL 文件：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format raw-sql \
  --dialect postgres \
  --source-connection-profile postgres-local \
  --input queries.sql \
  --output cases.yaml
```

PostgreSQL pg_regress：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress \
  --dialect postgres \
  --input strings.sql \
  --recorded-output strings.out \
  --output cases.yaml
```

Hive QTest：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format hive-qtest \
  --dialect hive \
  --input select_dummy_source.q \
  --recorded-output select_dummy_source.q.out \
  --qtest-driver TestMiniLlapLocalCliDriver \
  --output cases.yaml
```

Importer 不再生成单独的 `.import.json`。跳过的 DDL/DML、解析错误和输出配对错误都写入 `cases.yaml` 的 `import_diagnostics`，并在最终 Report 中原样呈现。

## YAML 结构

```yaml
source:
  dialect: hive
  engine: hive
  connection_profile: hive-local
  database: dsv_validation

target:
  connection_profile: doris-local
  database: dsv_validation

input:
  format: raw-sql
  file: queries.sql
  sha256: "<源文件 SHA-256>"

# 只有 .out/.q.out 输入才存在；存在即选择 Recorded Output
recorded_output:
  format: hive-qtest
  file: queries.q.out
  sha256: "<结果文件 SHA-256>"

import_summary:
  accepted: 1
  skipped: 0
  ambiguous: 0
  errors: 0

import_diagnostics: []

cases:
  - id: hive-queries-0001-ab12cd34
    statement_index: 1
    line_start: 1
    line_end: 1
    output_occurrence: 1  # 仅 Recorded Output Case 存在
    sql: SELECT 1 AS value;
```

YAML 不保存 `format_version`、`suite`、显式运行模式、比较策略、预期结果、标签、依赖或生成的 Doris SQL。比较策略由框架统一推导，Doris SQL 只进入 Report。

## 校验和运行

```bash
.venv/bin/doris-sql-validator cases-lint --path cases.yaml
.venv/bin/doris-sql-validator doctor --source-engine hive
.venv/bin/doris-sql-validator run --path cases.yaml
.venv/bin/doris-sql-validator run --path cases.yaml --id mvp-001

# 没有 .out 且没有源数据库时只做转译
.venv/bin/doris-sql-validator transpile \
  --source-dialect hive \
  "SELECT add_months(CAST('2024-02-29' AS DATE), 4) AS value"
```

未指定 `--output-dir` 时，最终报告固定写入：

```text
reports/<case-file-stem>/validation.json
reports/<case-file-stem>/validation.md
```

同一 YAML 再次运行会覆盖旧报告。报告只保存字段摘要、行数、结果 Digest 和有限样本，不复制完整大结果集。

Markdown 报告使用中文，先给出总数、带明确分母的结果匹配比例和各类结果计数，再列出全部 Case。完全匹配的 Case 只在
总表中简写；转换失败、执行状态、Schema、行数或行值不一致的 Case 会展开源 SQL、
生成的 Doris SQL、双端字段/样本/错误以及按失败类型细分的排查方向。

报告不包含人工 Expectations 或 Test status；英文内部代码附中文解释。两端均报错的
负向用例不计入成功匹配，即使旧比较器内部代码仍为 MATCH 也展开错误供后续确认。
结果 Digest（完整结果摘要指纹）保留在 JSON，不在 Markdown 反复展示。中文证据表说明
源结果能否支持错误类别、字段类型、行数和行值等比较，未取得或提前返回的比较不算通过。
首轮报告只有最多五行样本，不是全量结果；后续独立对照会另存有限行数以内的完整结果。

## 比较和结论

比较顺序为：转译、源证据、Doris 执行、执行状态/错误、字段数量/名称/类型、行数、行值、重复次数及顺序/容差策略。

```text
有最终 ORDER BY  → ordered
无最终 ORDER BY  → multiset，忽略顺序但保留重复次数
显式 Alias       → 比较字段名
浮点数           → 默认 1e-12 容差
```

表查询默认 `data_assurance=unverified`。如果两端数据、Schema、Session 或 UDF 没有由外部系统保证一致，行数/行值不同不会自动归因于 SQLGlot，而会报告可能原因并标记 `INCONCLUSIVE`。

Doris 连接、数据库、表或权限缺失分别归一化为环境错误；表存在但没有对应记录不会
报执行错误，而会根据源证据得到 `ROW_COUNT_MISMATCH` 或 `ROW_VALUE_MISMATCH`。
DDL、建表和装数始终由验证框架之外的准备流程负责。

## 当前模块依赖

```text
原始 .sql/.q + 可选 .out
  → importing/importer.py
  → 精简 Case YAML（含 Import Diagnostics）

Case YAML
  → case_loader.py
  → transpiler.py
  → source_provider.py
       ├── execution/<engine>.py       # Live Source
       └── recorded_output/parsers.py  # Recorded Output
  → execution/doris.py
  → comparison.py
  → reporting.py
```

人工数据准备与后续归因、修复的边界见 [PostgreSQL 人工连续链路](docs/POSTGRES_MANUAL_WORKFLOW.md)。
当前发布的官方 PostgreSQL 样本与执行报告分别位于 `cases/postgres/manual/current/` 和 `reports/pg-manual/current/`。
