# Doris SQL Validator 用户指南

本文从使用者角度说明如何把 Hive 或 PostgreSQL 测试脚本转换成验证器可读取的 YAML，如何选择源数据库实时执行或 Recorded Output，以及如何运行验证和阅读报告。

PostgreSQL 的人工数据准备、首轮报告、证据交接、独立对照、归因和修复 Skill 完整步骤，
见 [PostgreSQL 人工连续链路](POSTGRES_MANUAL_WORKFLOW.md)。AI 相关步骤由人显式调用，CLI 不调用模型。
报告正文默认中文、文件名使用英文，通用术语允许使用英文；不直观的状态仍解释其含义。

## 1. 功能定位与验证流程

验证器用于回答下面这个问题：

> 一条 Hive/PostgreSQL SQL 经当前社区版 SQLGlot 转成 Doris SQL 后，两端可观察到的执行行为是否一致？

完整流程为：

```text
原始输入
  ├── Hive .q
  ├── PostgreSQL .sql
  ├── 普通 .sql
  └── 上述脚本 + 可选的 .out/.q.out
        │
        ▼
import-cases
  ├── 按语句拆分脚本
  ├── 接受只读 Query，并保留查询形状的 Parser 失败作为普通错误 Case
  ├── 跳过 DDL、DML、EXPLAIN 等非只读语句
  └── 生成 Case YAML
        │
        ▼
cases-lint
  └── 检查 YAML 结构与 Case ID；参考输出的实际读取在导入/运行时检查
        │
        ▼
run
  ├── SQLGlot：源 SQL → Doris SQL
  ├── 取得源端证据
  │     ├── Live Source：连接 Hive/PostgreSQL 执行源 SQL
  │     └── Recorded Output：读取 .out，不连接源数据库
  ├── 连接 Doris 执行生成的 SQL
  ├── 比较执行状态、错误、结果字段和结果行
  └── 生成 validation.md + validation.json
```

验证器的职责边界：

- 只验证只读查询，不执行输入中的 `CREATE`、`INSERT`、`DROP` 等语句；
- 不创建数据库或表，不向 Hive、PostgreSQL、Doris 导入数据；
- 不修改 SQLGlot 生成的 Doris SQL；
- 不证明两端表数据相同，只比较本次取得的源端证据与 Doris 结果；
- 表查询能否得到有意义的语义结论，取决于用户是否在验证器之外准备了可比较的 Schema、数据、Session 和 UDF。

## 2. 输入格式与接入方式

### 2.1 批量验证输入格式

`run` 命令只读取 Case YAML。原始脚本必须先通过 `import-cases` 转为 YAML。

| 输入 | `--format` | 可附带结果文件 | 用途 |
| :--- | :--- | :--- | :--- |
| 普通 `.sql` | `raw-sql` | 不支持 | 从普通 SQL 脚本提取只读查询 |
| PostgreSQL pg_regress `.sql` | `pg-regress` | `.out` | 识别 psql/pg_regress 测试脚本和标准输出 |
| Hive QTest `.q` | `hive-qtest` | `.q.out` | 识别 Hive QTest 脚本和标准输出 |
| 已生成的 Case YAML | 不需要导入 | 由 YAML 决定 | `cases-lint` 和 `run` 的直接输入 |

`.out/.q.out` 目前指 PostgreSQL pg_regress 或 Hive QTest 的文本输出，不是任意格式的 CSV、JSON 或日志文件。

一个输入脚本可以同时包含 DDL、DML 和查询。例如：

```sql
CREATE TABLE orders(id INT, amount DECIMAL(10, 2));
INSERT INTO orders VALUES (1, 12.50);
SELECT SUM(amount) AS total FROM orders;
```

Importer 只把 `SELECT` 转成 Case。前两条语句不会执行，而是作为 `skipped` 诊断写入 YAML 和最终报告。因此，用户需要提前在源数据库和 Doris 中准备 `orders` 表及数据。

### 2.2 单条 SQL 转译

如果只想查看 SQLGlot 生成的 Doris SQL，不需要 YAML、源数据库或 Doris：

```bash
.venv/bin/doris-sql-validator transpile \
  --source-dialect hive \
  "SELECT add_months(CAST('2024-02-29' AS DATE), 4) AS value"
```

`transpile` 不执行 SQL，也不生成验证报告。

## 3. 验证模式

运行方式不需要用户填写额外的 `mode` 字段，框架根据 YAML 中是否存在 `recorded_output` 自动决定。

### 3.1 Live Source：源端与 Doris 实时执行

适用条件：导入时没有传入 `.out/.q.out`，并且源数据库可连接。

```text
源 SQL ──> Hive/PostgreSQL ──> 实时源结果 ─┐
                                            ├──> Comparator ──> Report
源 SQL ──> SQLGlot ──> Doris SQL ──> Doris ─┘
```

特点：

- 需要源数据库和 Doris 同时可用；
- 能获得数据库返回的字段类型和类型化结果，证据通常最完整；
- 表查询要求用户在两端自行准备可比较的数据；
- YAML 中没有 `recorded_output`，但必须有 `source.connection_profile`。

### 3.2 Recorded Output：参考输出验证

适用条件：导入时同时提供官方测试脚本及其 `.out/.q.out`。

```text
.out/.q.out ──> Recorded Output Parser ──> 源端参考结果 ─┐
                                                       ├──> Comparator ──> Report
源 SQL ──> SQLGlot ──> Doris SQL ────────────> Doris ──┘
```

特点：

- 不连接、不执行 Hive/PostgreSQL；
- 仍然必须连接 Doris；
- 适合复用上游仓库已经记录的预期输出；
- 文本输出可能没有原生字段类型，因此报告会明确哪些比较证据可用；
- Recorded Output 对应的是原测试脚本执行时的数据库状态。若脚本依赖前序 DDL/DML，Doris 侧仍需由外部流程准备到对应状态。

PostgreSQL `.out` 读取支持默认 ASCII 横向表格，以及 `\x` / `\gx` 产生的 `-[ RECORD n ]` 纵向展开记录。横向表格按显示列边界拆分，不把值中的 `|` 当作分隔符；多行单元格依据右边缘的 `+` 还原换行，保留多行文本的缩进。展开记录保留字段顺序、重复列名、空字段和连续记录；没有字段信息的展开零行结果只提供行数证据，不猜测字段。

定位时按完整的外层语句回显计数，不把多行 PREPARE、EXPLAIN、视图/函数定义、查询前缀或结果单元格中的同文 SELECT 当成独立查询。支持识别 XML WARNING 后的原文与箭头诊断行、明确缩进的诊断续行，以及 NOTICE 的级联对象清单；未知输出不通过无限向后搜索“找一张能解析的表格”来掩盖。COPY 输入在官方 `.out` 中可能被省略，不能因此跳过后续查询；`\sv` 打印的视图定义也不是新执行的 SQL 回显。

这些仍是显示文本，不提供原生类型，也不能可靠区分默认空白显示的 NULL 与空字符串、或还原与排版填充混合的行尾空格。任意自定义格式（如 Unicode/old-ascii 边框、wrapped 自动折行、tuples-only）不在支持范围。缺少行数标记、续行被截断、列结构不一致等情况仍报读取错误，不借用下一条 SQL 的输出，不自动回退到 Live Source。

输出解析器按 `recorded_output.format` 选择，而不是只看 `.out` 扩展名：`pg-regress` 识别 PostgreSQL 回归测试的 psql 回显和结果；`hive-qtest` 识别 Hive QTest 的 PREHOOK/POSTHOOK 与制表符结果。两者读取后统一为相同的查询结果结构，复用后续比较器。这里的解析器不是 SQLGlot 的 SQL Parser；同一种数据库如果换成 CSV、JSON 或其他测试工具的输出，也需要对应的格式解析支持，不能直接假设与现有 `.out` 格式兼容。

### 3.3 输入组合与执行路径

| 脚本包含 DDL/DML | 提供 `.out` | 实际行为 |
| :---: | :---: | :--- |
| 否 | 否 | 提取查询；实时执行源数据库和 Doris |
| 是 | 否 | 跳过 DDL/DML；用户外部准备数据；实时执行源数据库和 Doris |
| 否 | 是 | 从输出读取源端结果；只执行 Doris |
| 是 | 是 | 跳过 DDL/DML；从输出读取对应源结果；用户外部准备 Doris；只执行 Doris |

## 4. 运行环境配置与数据准备

所有命令均假设当前目录为项目根目录：

```bash
cd doris-sql-validator
```

### 4.1 Python 运行环境安装

项目使用 Python 3.12，并把相邻的社区版 SQLGlot 仓库 `../sqlglot` 作为 editable dependency。先按 [README 的安装步骤](../README.md#安装) 克隆两个仓库；已有 checkout 时不要重复 clone。

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/uv sync --extra dev
cp .env.example .env
```

如果 `.env` 已存在，不要用最后一条命令覆盖它。

### 4.2 数据库连接配置

连接信息放在项目根目录的 `.env`：

```dotenv
HIVE_HOST=127.0.0.1
HIVE_PORT=10000
HIVE_USERNAME=hive
HIVE_DATABASE=default

POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=postgres-local-only
POSTGRES_DATABASE=dsv_validation

DORIS_HOST=127.0.0.1
DORIS_PORT=9030
DORIS_USERNAME=root
DORIS_PASSWORD=
DORIS_DATABASE=dsv_validation
```

YAML 中的 `connection_profile` 目前是方便阅读和未来扩展的逻辑名称；实际 Host、Port、用户名和密码来自上述环境变量。YAML 的 `database` 若非空，会覆盖环境变量中的默认数据库。

### 4.3 本地源数据库启动与连接检查

Hive：

```bash
./scripts/hive.sh up
./scripts/hive.sh status
./scripts/hive.sh smoke
```

PostgreSQL：

```bash
./scripts/postgres.sh up
./scripts/postgres.sh status
./scripts/postgres.sh smoke
```

Doris 需要由用户启动已有环境。然后按源引擎检查两端连接：

```bash
.venv/bin/doris-sql-validator doctor --source-engine hive
.venv/bin/doris-sql-validator doctor --source-engine postgres
```

`doctor` 会显示当前加载的 SQLGlot 版本，并分别检查指定源数据库和 Doris。Recorded Output 模式虽然不运行源数据库，当前 `doctor` 仍会检查命令中指定的源引擎；如果只运行 Recorded Output，可以直接确保 Doris 可用后运行 Case。

### 4.4 表结构与测试数据准备

常量查询不需要建表，例如：

```sql
SELECT MD5('abc');
```

表查询需要在验证器之外准备环境，例如：

```text
Hive/PostgreSQL                       Doris
  database/schema                      database
  table + columns        对应           table + columns
  rows                                  rows
  timezone/session/UDF                  timezone/session/UDF
```

验证器不会因为输入脚本包含 `CREATE` 或 `INSERT` 就执行它们。若 Doris 表不存在，报告通常显示 `TARGET_ENVIRONMENT_ERROR`，错误类别为 `TABLE_NOT_FOUND`；若表存在但数据不同，通常显示 `ROW_COUNT_MISMATCH` 或 `ROW_VALUE_MISMATCH`。

可直接使用 [快速示例](../examples/postgres/basic/README.md) 提供的 PostgreSQL/Doris 准备 SQL。它们由用户在框架外用 SQL 客户端执行；只在新的专用测试库运行。官方回归语料的准备依赖与类型限制见 [样本说明](../cases/postgres/manual/current/README.md)。

## 5. Case YAML 生成

Live Source 的 YAML 可以放入单独目录。Recorded Output 还有额外限制：`.out/.q.out` 必须在 YAML 所在目录或其子目录，不能指向目录之外；将输入、参考输出和 YAML 放在同一目录最简单。以下 `/path/to/` 需要替换为自己的输入路径，开箱即用命令见快速示例。

例如，为自有 Live Source 输入创建目录：

```bash
mkdir -p cases/generated
```

### 5.1 Hive Live Source Case 生成

```bash
.venv/bin/doris-sql-validator import-cases \
  --format hive-qtest \
  --dialect hive \
  --source-connection-profile hive-local \
  --source-database default \
  --target-database dsv_validation \
  --input /path/to/query.q \
  --output cases/generated/hive-query-live.yaml
```

### 5.2 Hive Recorded Output Case 生成

```bash
.venv/bin/doris-sql-validator import-cases \
  --format hive-qtest \
  --dialect hive \
  --target-database dsv_validation \
  --input /path/to/query.q \
  --recorded-output /path/to/query.q.out \
  --qtest-driver TestMiniLlapLocalCliDriver \
  --output /path/to/hive-query-recorded.yaml
```

`--qtest-driver` 用于记录输出所属的 Hive QTest Driver；只有对应输出确实依赖该信息时才需要填写。

### 5.3 PostgreSQL Live Source Case 生成

```bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress \
  --dialect postgres \
  --source-connection-profile postgres-local \
  --source-database dsv_validation \
  --target-database dsv_validation \
  --input /path/to/query.sql \
  --output cases/generated/pg-query-live.yaml
```

### 5.4 PostgreSQL Recorded Output Case 生成

```bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress \
  --dialect postgres \
  --target-database dsv_validation \
  --input /path/to/query.sql \
  --recorded-output /path/to/query.out \
  --output /path/to/pg-query-recorded.yaml
```

### 5.5 通用 SQL 文件导入

普通 SQL 没有标准 Recorded Output 解析规则，只能生成 Live Source YAML：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format raw-sql \
  --dialect postgres \
  --source-engine postgres \
  --source-connection-profile postgres-local \
  --source-database dsv_validation \
  --target-database dsv_validation \
  --input /path/to/queries.sql \
  --output cases/generated/queries.yaml
```

## 6. Case YAML 结构与字段说明

YAML 是 Importer 的稳定输出，也是 `run` 的唯一批量输入。通常不需要用户手工补充标签、预期结果或生成后的 Doris SQL。

下面是字段结构示意，不是可直接运行的配置；真实路径、指纹和查询编号应由 Importer 生成：

```yaml
source:
  dialect: postgres
  engine: postgres
  connection_profile: postgres-local
  database: dsv_validation

target:
  connection_profile: doris-local
  database: dsv_validation

input:
  format: pg-regress
  file: assets/md5.sql
  sha256: 1ac70abdb09d828aa6d11120b1a14dd31a672d5c2b80545b5f1aeee245cba147

recorded_output:
  format: pg-regress
  file: assets/md5.out
  sha256: 3d2b594f7b18203f6fad6356cffd3699ecbfd1497e184c0bea1f8eb6ccec12d7

import_summary:
  accepted: 1
  skipped: 1
  ambiguous: 0
  errors: 0

import_diagnostics:
  - statement_index: 1
    line_start: 1
    line_end: 1
    disposition: skipped
    statement_type: create
    reason: Expected one read-only Query, got Create

cases:
  - id: pg-md5-0002-5e14d477
    statement_index: 2
    line_start: 2
    line_end: 2
    output_occurrence: 1
    sql: SELECT MD5('a') AS digest;
```

各部分含义：

- `source`：源 SQL 方言、实时执行引擎和数据库；
- `target`：Doris 连接逻辑名和数据库；
- `input`：原始脚本格式、相对路径和内容校验值；
- `recorded_output`：存在时自动选择 Recorded Output；不存在时自动选择 Live Source；
- `import_summary`：接受、跳过、歧义和错误的语句数量；
- `import_diagnostics`：未进入验证的语句及原因，例如 DDL 被跳过；
- `cases`：实际要转译和验证的只读查询；
- `id`：Importer 自动生成的稳定标识，可用于只运行某一条 Case；
- `statement_index/line_start/line_end`：查询在原始脚本中的位置；
- `output_occurrence`：同一 SQL 在 Recorded Output 中第几次出现，仅 Recorded Output Case 存在；
- `sql`：原始源方言查询。

YAML 不保存生成的 Doris SQL。Doris SQL 取决于当前运行时加载的 SQLGlot 版本，因此每次运行时重新生成，并记录在最终 Report 中。

Parser 无法识别但形状为 SELECT/WITH 等查询的语句可以保留为普通 Case，并在运行报告中记录 `failure_stage=source_parse`；这不表示源数据库本身执行失败。DDL/DML 仍不会执行。

`input.file` 主要用于报告来源追踪，运行时不会重新读取原始 SQL，因为 Case 已经保存在 YAML 中。`recorded_output.file` 则会在每次运行时读取，通常按 YAML 所在目录解析相对路径；移动 Recorded Output YAML 时，必须同时调整或移动它引用的 `.out/.q.out`，并使文件仍处于 YAML 目录的范围内。参考输出指纹不一致时会报错，不自动换用其他文件。

## 7. Case YAML 校验与验证执行

### 7.1 YAML 结构校验

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path cases/generated/pg-query-live.yaml
```

成功输出示例：

```text
OK: 14 unique cases
  evidence: live_source
  source: postgres/postgres
  target: doris/doris
  import: accepted=14, skipped=0, ambiguous=0, errors=0
```

### 7.2 全量 Case 执行

```bash
.venv/bin/doris-sql-validator run \
  --path cases/generated/pg-query-live.yaml
```

默认报告位置：

```text
reports/pg-query-live/validation.md
reports/pg-query-live/validation.json
```

同一个 YAML 再次运行会覆盖同目录下的旧报告。

### 7.3 报告输出目录配置

```bash
.venv/bin/doris-sql-validator run \
  --path cases/generated/pg-query-live.yaml \
  --output-dir reports/manual/pg-query-live
```

### 7.4 指定 Case 执行

```bash
.venv/bin/doris-sql-validator run \
  --path cases/generated/pg-query-live.yaml \
  --id pg-md5-0002-5e14d477
```

可以重复使用 `--id` 选择多条 Case。

### 7.5 进程退出状态

- 所有 Case 都得到 `MATCH`：`run` 返回退出码 `0`；
- 任一 Case 转译失败、证据不可用、执行失败或不匹配：报告仍会生成，但 `run` 返回退出码 `1`；
- YAML 参数或 Case ID 使用错误：通常返回退出码 `2`。

因此，在 Shell 或 CI 中看到退出码 `1` 时，应先打开报告；它可能表示框架成功发现了一条兼容性差异，而不是验证器自身崩溃。

## 8. 验证报告结构与结果判读

每次运行生成两个报告：

```text
validation.md    面向人工阅读
validation.json  面向程序、CI 或后续统计
```

报告不会保存全部大结果集，只保存字段摘要、行数、完整结果 Digest 和最多 5 行样本。

### 8.1 汇总统计

报告先展示查询总数、成功结果匹配比例和各类失败数量。例如：

~~~text
查询总数：4
成功结果匹配：3
SQLGlot 转译失败：0
Doris 执行失败：1
~~~

成功匹配必须两端成功；源端负向报错即使内部 Outcome 为 MATCH，也不计成功匹配。各项分母和未取得源证据的情况分别说明。

INCONCLUSIVE 表示现有证据不足以作完整语义结论，不表示验证器没有工作。表查询数据前提未经框架核验时，发现差异也不能自动归为 SQLGlot 缺陷。

### 8.2 Import diagnostics：导入诊断

例如：

```text
Statement 1 | skipped | create  | Expected one read-only Query, got Create
Statement 2 | skipped | insert  | Expected one read-only Query, got Insert
Statement 3 | skipped | explain | Expected one read-only Query, got Command
```

其中 DDL/DML 的 skipped 不是执行失败；parse_error 或 recorded_output 的 error 则应读取具体原因，分别排查源语法和参考输出读取。

### 8.3 Comparison coverage：比较证据覆盖范围

Live Source 通常能比较：

- 双端执行成功或失败；
- 归一化错误类别；
- 字段数量、字段名和 Canonical Type；
- 类型化行值、重复行与顺序策略。

Recorded Output 可能只有显示文本，没有数据库原生字段类型。报告会把字段类型等能力标记为不可用；不可用项会跳过，不会被当成“已经匹配”。

### 8.4 Case overview：Case 执行概览

示例：

```text
Case: hive-groupby-empty-0004-9505fead
Query scope: Table-backed; data not verified
SQLGlot: Generated Doris SQL
Source evidence: Success
Doris execution: Error: EXECUTION_ERROR
Outcome: EXECUTION_STATUS_MISMATCH
Semantic conclusion: Inconclusive
```

常见 Outcome：

| Outcome | 含义 |
| :--- | :--- |
| `MATCH` | 当前可用证据全部匹配 |
| `TRANSLATION_FAILED` | SQLGlot 无法解析源 SQL 或生成 Doris SQL |
| `SOURCE_EVIDENCE_UNAVAILABLE` | 无法取得源数据库结果或 Recorded Output |
| `SOURCE_ENVIRONMENT_ERROR` | 源端连接、数据库、表、权限或超时问题 |
| `TARGET_ENVIRONMENT_ERROR` | Doris 连接、数据库、表、权限或超时问题 |
| `EXECUTION_STATUS_MISMATCH` | 一端成功、另一端执行失败 |
| `ERROR_BEHAVIOR_MISMATCH` | 两端都失败，但归一化错误类别不同 |
| `RESULT_SCHEMA_MISMATCH` | 返回字段数量、显式别名或 Canonical Type 不同 |
| `ROW_COUNT_MISMATCH` | 返回行数不同 |
| `ROW_VALUE_MISMATCH` | 行数相同，但归一化后的结果值不同 |

### 8.5 失败详情：环境与兼容性问题判定

不匹配 Case 会展开：

- 原始源 SQL；
- 当前 SQLGlot 生成的 Doris SQL；
- 源端与 Doris 的执行状态；
- 字段信息、行数和最多 5 行样本；
- JSON 中保留完整结果 Digest；Markdown 优先展示可读的字段、样本与错误，不反复列摘要值；
- 原始错误类别、错误码和错误消息；
- 针对该失败类型的排查方向。

例如源端成功，而 Doris 报：

```text
Error category: TABLE_NOT_FOUND
Error message: Table orders does not exist in database dsv_validation
```

应先在 Doris 外部创建并装载 `orders`，然后重新运行。它不是 SQLGlot 转换失败。

如果源端与 Doris 都成功、字段一致，但行值不同：

```text
Outcome: ROW_VALUE_MISMATCH
source_sample: ...
doris_sample: ...
```

应依次检查：

1. 两端是否真的是相同 Schema 和数据状态；
2. 时区、Collation、Session 参数和 UDF 是否一致；
3. 生成的 Doris SQL 是否丢失或错误改写了语义；
4. 两个数据库本身是否对同一表达式采用不同语义。

## 9. 结果比较规则

框架按以下顺序比较：

```text
1. SQLGlot 是否成功解析和生成
2. 源端证据是否可取得
3. Doris SQL 是否执行成功
4. 双端执行状态和错误类别
5. 返回字段数量
6. 字段名称（默认仅显式 Alias）
7. Canonical 字段类型（源证据支持时）
8. 行数
9. 行值和重复次数
10. 行顺序、浮点容差、Decimal、时间和复杂类型
```

默认规则：

```text
最终查询有 ORDER BY   → ordered，逐行比较
最终查询无 ORDER BY   → multiset，忽略顺序但保留重复次数
字段有显式 Alias      → 比较字段名
浮点值                 → 默认使用 1e-12 容差
```

`LIMIT` 没有稳定 `ORDER BY` 时，不同引擎可能合法地返回不同记录，不适合据此直接判断 SQLGlot 语义错误。

## 10. 可运行示例与样本路径

推荐从 [examples/postgres/basic/README.md](../examples/postgres/basic/README.md) 开始。目录同时包含常量 SQL/.out、表查询 SQL/.out、双端 DDL/INSERT 和逐步命令，不要求维护者的本地数据库已存在。

按示例完成 Doris 数据准备后：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input examples/postgres/basic/queries.sql \
  --recorded-output examples/postgres/basic/expected.out \
  --source-database dsv_demo --target-database dsv_demo \
  --output examples/postgres/basic/generated-recorded.yaml

.venv/bin/doris-sql-validator run \
  --path examples/postgres/basic/generated-recorded.yaml \
  --output-dir reports/demo/recorded
~~~

不传 --recorded-output 则为 Live Source，需要两端已准备数据。仅导入和 lint 不连接数据库；run 会执行目标查询。使用不同输出目录保留多次运行，不覆盖仓库附带的参考报告。

更大范围的 [官方回归样本](../cases/postgres/manual/current/README.md) 含多阶段数据和外部对象依赖，不保证全部 SQL 可在空库直接执行。学习后续人工归因与修复，见 [PostgreSQL 工作流](POSTGRES_MANUAL_WORKFLOW.md)。

## 11. 功能范围与限制

当前已实现：

- 源方言/引擎：Hive、PostgreSQL；
- 目标方言/引擎：Doris；
- 普通 SQL、Hive QTest、PostgreSQL pg_regress 导入；
- Live Source 和 Recorded Output；
- 单条只转译；
- 常量查询与表查询；
- 执行状态、错误、Schema 和结果数据比较；
- Markdown 与 JSON 报告。

当前不负责：

- 执行 DDL/DML；
- 自动把源数据库的数据同步到 Doris；
- 解析任意自定义 `.out` 格式；
- 为同一回显行中多条 SQL 猜测输出对应关系；当前会拒绝而不是随意配对；
- 为未知 UDF 自动安装对应函数；
- 对随机函数、当前时间或无稳定排序的 `LIMIT` 提供确定性保证；
- 静态证明两条 SQL 对所有可能数据都语义等价。

公开样例、参考报告及不应提交的本机文件见 [PUBLISHING.md](PUBLISHING.md)。参考报告的结果仅适用于其记录的版本、数据和 Session，不代表新环境的运行结果。
