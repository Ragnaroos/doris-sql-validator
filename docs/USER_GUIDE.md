# Doris SQL Validator 用户指南

本文主验证流程要求同时提供 Hive/PostgreSQL 测试脚本及其配对的 .out/.q.out，先生成 YAML，再读取源端参考输出并执行 Doris，最后比较结果。现有 CLI 仍支持 Live Source，作为额外诊断方式单独说明，不作为主工作流缺少参考输出时的替代输入。

PostgreSQL 的人工数据准备、首轮验证、直接归因、独立对照和修复 Skill 完整步骤，
见 [PostgreSQL 人工连续链路](POSTGRES_MANUAL_WORKFLOW.md)。AI 相关步骤由人显式调用，CLI 不调用模型。
报告正文默认中文、文件名使用英文，通用术语允许使用英文；不直观的状态仍解释其含义。

## 1. 功能定位与验证流程

验证器用于回答下面这个问题：

> 一条 Hive/PostgreSQL SQL 经当前社区版 SQLGlot 转成 Doris SQL 后，两端可观察到的执行行为是否一致？

主验证流程为（参考输出为必需输入）：

```text
原始输入
  ├── Hive QTest：.q + 对应的 .q.out，必须配对
  └── PostgreSQL pg_regress：.sql + 对应的 .out，必须配对
        │
        ▼
import-cases
  ├── 按语句拆分脚本
  ├── 接受只读 Query，并保留查询形状的 Parser 失败作为普通错误 Case
  ├── 跳过 DDL、DML、EXPLAIN 等非只读语句
  ├── 首次尝试匹配并读取配对的 .out/.q.out，记录导入诊断
  └── 按 --output 指定路径生成 Case YAML（工作流步骤二）
        │
        ▼
cases-lint
  └── 检查 YAML 结构与 Case ID；参考输出的实际读取在导入/运行时检查
        │
        ▼
run
  ├── SQLGlot：源 SQL → Doris SQL
  ├── Recorded Output：读取配对的 .out/.q.out，不连接源数据库
  ├── 连接 Doris 执行生成的 SQL
  ├── 比较执行状态、错误、结果字段和结果行
  └── 生成唯一 <batch-id>-validation.json（run / summary / queries）
```

普通 .sql 如果不带当前支持格式的参考输出，不属于以上主验证输入；可以只做 transpile，或由用户另行选择 Live Source 诊断。“必须配对”是主工作流要求；CLI 保留的 Live Source 能力不是主流程缺少参考输出时的替代。已有 .out 读取失败时不会自动回退为 Live Source。

验证器的职责边界：

- 只验证只读查询，不执行输入中的 `CREATE`、`INSERT`、`DROP` 等语句；
- 不创建数据库或表，不向 Hive、PostgreSQL、Doris 导入数据；
- 不修改 SQLGlot 生成的 Doris SQL；
- 不证明两端表数据相同，只比较本次取得的源端证据与 Doris 结果；
- 表查询能否得到有意义的语义结论，取决于用户是否在验证器之外准备了可比较的 Schema、数据、Session 和 UDF。

## 2. 输入格式与接入方式

### 2.1 批量验证输入格式

`run` 命令只读取 Case YAML。原始脚本必须先通过 `import-cases` 转为 YAML。

| 输入 | `--format` | 参考输出要求 | 用途 |
| :--- | :--- | :--- | :--- |
| PostgreSQL pg_regress `.sql` | `pg-regress` | 主流程必须提供配对 `.out` | 识别 psql/pg_regress 测试脚本和标准输出 |
| Hive QTest `.q` | `hive-qtest` | 主流程必须提供配对 `.q.out` | 识别 Hive QTest 脚本和标准输出 |
| 已生成的 Case YAML | 不需要导入 | 主流程应包含 `recorded_output` 引用 | `cases-lint` 和 `run` 的直接输入 |
| 普通 `.sql` | `raw-sql` | 不支持 Recorded Output | 仅作补充 Live Source 输入，不属于主验证流程 |

`.out/.q.out` 目前指 PostgreSQL pg_regress 或 Hive QTest 的文本输出，不是任意格式的 CSV、JSON 或日志文件。

一个输入脚本可以同时包含 DDL、DML 和查询。例如：

```sql
CREATE TABLE orders(id INT, amount DECIMAL(10, 2));
INSERT INTO orders VALUES (1, 12.50);
SELECT SUM(amount) AS total FROM orders;
```

Importer 只把 `SELECT` 转成 Case。前两条语句不会执行，而是作为 `skipped` 诊断写入 YAML 和最终报告的导入计数中，具体诊断留在 YAML。因此，用户需要提前在源数据库和 Doris 中准备 `orders` 表及数据。

### 2.2 单条 SQL 转译

如果只想查看 SQLGlot 生成的 Doris SQL，不需要 YAML、源数据库或 Doris：

```bash
.venv/bin/doris-sql-validator transpile \
  --source-dialect hive \
  "SELECT add_months(CAST('2024-02-29' AS DATE), 4) AS value"
```

`transpile` 不执行 SQL，也不生成验证报告。

## 3. 验证模式

主流程使用 Recorded Output，要求导入时传入 --recorded-output。现有代码不需要用户填写额外的 mode 字段，而是根据 YAML 中是否存在 recorded_output 自动决定；下面同时说明主流程和保留的补充能力。

### 3.1 Live Source：补充诊断，源端与 Doris 实时执行

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

### 3.2 Recorded Output：主流程，参考输出验证

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

下表是现有 CLI 的能力说明；其中无 .out 的两行不是本指南主工作流允许的输入，也不是缺少 .out 时的自动降级策略。

| 脚本包含 DDL/DML | 提供 `.out` | 实际行为 |
| :---: | :---: | :--- |
| 否 | 否 | 提取查询；实时执行源数据库和 Doris |
| 是 | 否 | 跳过 DDL/DML；用户外部准备数据；实时执行源数据库和 Doris |
| 否 | 是 | 从输出读取源端结果；只执行 Doris |
| 是 | 是 | 跳过 DDL/DML；从输出读取对应源结果；用户外部准备 Doris；只执行 Doris |

## 4. 运行环境配置与数据准备

所有命令均假设当前目录为项目根目录：

```bash
cd /path/to/your/checkout
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

验证器不会因为输入脚本包含 `CREATE` 或 `INSERT` 就执行它们。若 Doris 表不存在，报告显示“Doris 环境问题”并保留表不存在的实际错误；若表存在但数据不同，通常显示“行数不匹配”或“行值或顺序不匹配”。这些结果不能单独证明 SQLGlot 有问题。

本工作目录不附带数据准备 SQL、参考输出或既有报告。用户自行提供或显式调用数据准备 Skill 生成脚本，在框架外用 SQL 客户端执行；只在授权的专用测试库运行。注意官方回归语料的多阶段数据、COPY 依赖和类型限制，具体流程见 [PostgreSQL 工作流](POSTGRES_MANUAL_WORKFLOW.md)。

## 5. 步骤二：生成带相同前缀的 Case YAML

本工作流必须同时提供源脚本及其配对的参考输出。YAML 的文件名为 <batch-id>-cases.yaml，保存到 reports/data-preparation/，与步骤一的三份产物使用相同前缀。实际路径由 import-cases 的 --output 指定，CLI 不自动分配批次编号，也不自动加前缀。

~~~text
reports/data-preparation/           不创建批次或准备次数子目录
  queries-001-data-preparation.md        步骤一：准备与实际核验证据的合并 Markdown
  queries-001-postgres-setup.sql         步骤一：源端准备脚本
  queries-001-doris-setup.sql            步骤一：目标准备脚本
  queries-001-cases.yaml                 步骤二：import-cases 生成
~~~

原 SQL/.out 保留在用户指定的位置，不复制到报告目录。YAML 用相对于自身目录的路径引用原件，允许指向其他目录；run 直接读取当前 .out，不保存或核对其内容指纹。运行前检查 YAML 引用是否为可信的用户输入，不能把任意来源的 YAML 当作可信文件读取配置。下面 /path/to/ 必须替换为实际路径。

### 5.1 PostgreSQL：必须提供 .sql + .out

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --target-database dsv_validation \
  --input /path/to/queries.sql \
  --recorded-output /path/to/queries.out \
  --output reports/data-preparation/queries-001-cases.yaml
~~~

### 5.2 Hive：必须提供 .q + .q.out

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format hive-qtest --dialect hive \
  --target-database dsv_validation \
  --input /path/to/hive-queries.q \
  --recorded-output /path/to/hive-queries.q.out \
  --output reports/data-preparation/hive-queries-001-cases.yaml
~~~

如确有 Hive Driver 前提，可补充 --qtest-driver；这是额外环境信息，不表示参考输出文件可省略。普通 SQL 如果没有可读取的配对输出，不进入本主验证流程；当前 CLI 保留的 Live Source 是另行选择的诊断能力，不在这里用作缺少 .out 的替代步骤。

## 6. Case YAML 结构与字段说明

YAML 是 Importer 的稳定输出，也是 `run` 的唯一批量输入。主流程要求它包含 recorded_output。通常不需要用户手工补充标签、预期结果或生成后的 Doris SQL。

### 6.1 生成位置和实际作用

~~~text
工作流步骤二：import-cases
  --input inputs/postgres/queries-001/queries.sql
  --recorded-output inputs/postgres/queries-001/queries.out
  --output reports/data-preparation/queries-001-cases.yaml

输出：上述 --output 指定的 queries-001-cases.yaml，与步骤一共享 queries-001 前缀
  保存源/目标配置、源 SQL 路径/来源指纹、参考输出路径/格式、导入诊断，以及每条查询的原文和位置。
  cases-lint 读取它检查结构；run 读取它取得待转译的 SQL 和参考输出的查找信息。
  不包含 DDL/DML 执行步骤，也不是 Shell 脚本或“SQL 行号到 .out 行号”的固定映射表。

Recorded Output 的定位信息
  line_start / line_end：只表示查询在源 SQL 文件中的行号，不是 .out 行号。
  sql：实际待验证的查询原文；解析器据此查找 .out 中对应的语句回显/查询块。
  output_occurrence：同一 SQL 在参考输出中第几次出现，用于区分重复查询。
  recorded_output：参考输出格式和文件路径（可选 Driver）；具体定位/结果读取由相应解析器完成。
~~~

YAML 不是只有查询行号和 Case ID：它保存完整查询原文、源/目标配置、原 SQL 路径/来源指纹，以及 .out 路径与格式。源行号用于追踪；具体 .out 结果靠查询内容和出现次数定位，不记录固定输出行号。修改原 SQL/.out 后重新导入，不手工修改行号来配对。

### 导入时和运行时都会匹配参考输出

~~~text
import-cases
  读取 SQL/.out → 拆分并筛选查询 → 分配 Case ID、源行号和 output_occurrence
  → 调用输出解析器，首次尝试定位并读取每条查询的参考结果
  → 保存查询与 .out 引用到 YAML，保存无法配对/读取等导入诊断
  不把完整结果或固定的 .out 行号写进 YAML；源 Parser 先失败的查询保留解析错误

cases-lint
  仅检查 YAML 结构、字段、Case ID 和统计，不读取或匹配 .out

run
  读取 YAML → 直接读取当前 .out → SQLGlot 转译各查询
  → 对到达源证据阶段的查询再次定位/读取参考结果 → 执行 Doris 查询 → 比较并生成报告
  SQLGlot 转译先失败不执行双端 SQL，但仍尝试只读 .out 确认源状态；
  保留转译错误，源端负向默认不归因，源证据读取失败也记录具体原因
~~~

所以 .out 不是到 run 才首次匹配；首次匹配发生在导入阶段。导入时参考输出读取失败的查询可能不进入最终 Case 列表，必须同时查看 import_diagnostics，不能只按 accepted 数量推断覆盖范围。

### 6.2 字段示例

下面是字段结构示意，不是可直接运行的配置；文件保存为 reports/data-preparation/queries-001-cases.yaml。真实路径、指纹和查询编号应由 Importer 生成：

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
  file: ../../inputs/postgres/queries-001/queries.sql
  sha256: 1ac70abdb09d828aa6d11120b1a14dd31a672d5c2b80545b5f1aeee245cba147

recorded_output:
  format: pg-regress
  file: ../../../inputs/postgres/queries-001/queries.out

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
- `recorded_output`：主流程必须包含的参考输出格式和路径；
- `import_summary`：接受、跳过、歧义和错误的语句数量；
- `import_diagnostics`：未进入验证的语句及原因，例如 DDL 被跳过；
- `cases`：实际要转译和验证的只读查询；
- `id`：Importer 自动生成的稳定标识，可用于只运行某一条 Case；
- `statement_index/line_start/line_end`：查询在原始脚本中的位置；
- `output_occurrence`：同一 SQL 在 Recorded Output 中第几次出现，仅 Recorded Output Case 存在；
- `sql`：原始源方言查询。

YAML 不保存生成的 Doris SQL。Doris SQL 取决于当前运行时加载的 SQLGlot 版本，因此每次运行时重新生成，并记录在最终 Report 中。

Parser 无法识别但形状为 SELECT/WITH 等查询的语句可以保留为普通 Case，并在运行报告中记录 `failure_stage=source_parse`；这不表示源数据库本身执行失败。DDL/DML 仍不会执行。

`input.file` 主要用于报告来源追踪，运行时不会重新读取原始 SQL，因为 Case 已经保存在 YAML 中。`recorded_output.file` 则会在每次运行时读取，通常按 YAML 所在目录解析相对路径；移动 Recorded Output YAML 时，必须同时调整或移动它引用的 `.out/.q.out`，使引用仍指向相同的原始参考输出。它读取路径中的当前内容，不检查文件是否被修改；找不到对应查询或结果格式无法读取时仍报错，不借用其他查询的结果。

## 7. Case YAML 校验与验证执行

### 7.1 YAML 结构校验

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path reports/data-preparation/queries-001-cases.yaml
```

cases-lint 的意思是“检查 Case 文件是否符合格式要求”，--path 是必填的 YAML 路径，不能只运行不带参数的 cases-lint。它不会生成 YAML，也不会执行测试：

~~~text
读取已有 YAML
  → 检查字段、数据类型、必填项、Case ID 格式与唯一性、导入统计的一致性等
  → Recorded Output 配置存在时，检查 Case 是否有 output_occurrence
  → 终端输出检查结果、证据模式、查询数量和导入统计

不会：连接数据库、执行 SQL、转译 SQL、读取/比较 .out 结果或生成 validation 报告。
因此 lint 通过只表示 YAML 结构可用，不代表所有源 SQL 都能转译，也不代表两端结果一致。
~~~

成功输出示例：

```text
OK: 14 unique cases
  evidence: recorded_output
  source: postgres/postgres
  target: doris/doris
  import: accepted=14, skipped=0, ambiguous=0, errors=0
```

### 7.2 全量 Case 执行

```bash
.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --output reports/validation/queries-001-validation.json
```

本例显式指定的报告位置：

```text
reports/validation/queries-001-validation.json
```

不指定 --output 或 --stdout 时，从 YAML 文件名去掉扩展名和末尾 -cases，默认写到仓库的 reports/validation/<所得名称>-validation.json。例如 queries-001-cases.yaml 默认对应 reports/validation/queries-001-validation.json。--output 指定完整文件路径，不是目录；重复指定同一文件会覆盖它。需要保留重跑结果时使用新的文件名，不自动递增批次号。

### 7.3 验证报告文件配置

```bash
.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --output reports/validation/queries-001-validation-run-002.json
```

### 7.4 指定 Case 执行

```bash
.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --id '<从当前 YAML 复制实际 Case ID>' \
  --output reports/validation/queries-001-selected-validation.json
```

可以重复使用 `--id` 选择多条 Case。

### 7.5 进程退出状态

- 逐条处理和内部比较没有返回失败：退出码 `0`，可能包含双方同类报错的源端负向；实际成功匹配数以 summary 为准，不能把退出码当作成功匹配率；
- 任一 Case 转译失败、证据不可用、执行失败或不匹配：报告仍会生成，但 `run` 返回退出码 `1`；
- YAML 参数或 Case ID 使用错误：通常返回退出码 `2`。

因此，在 Shell 或 CI 中看到退出码 `1` 时，应先打开报告；它可能表示框架成功发现了一条兼容性差异，而不是验证器自身崩溃。

### 7.6 不落盘返回验证结果

修复阶段只需把实际回归事实整理进任务 Markdown 时，可以直接运行：

```bash
.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --stdout
```

它仍转译、执行并比较，只将相同结构的 JSON 返回标准输出，不创建报告文件或目录，也不自动调用 Skill。可以加 --id 筛选；--stdout 与 --output 不能同时使用。正常返回报告时标准输出只有 JSON，没有路径提示；发现差异而退出 1 时 JSON 仍有效，输入/配置错误则可能只有诊断信息。

精简匹配记录仍不包含目标 SQL或完整类型；需要验收这些维度时，修复 Agent 需取得修改后运行时的真实生成 SQL和类型/执行事实，不能从“匹配”反推全部通过。具体方法与报告模板见 [工作流步骤四](POSTGRES_MANUAL_WORKFLOW.md#7-步骤四修复并验证新生成的-sql)。需要独立 CI/统计导出时才另用 --output 保存文件，不是修复验收的必需材料。

## 8. 验证报告结构与结果判读

run 默认只生成一份 `<batch-id>-validation.json`，用户与后续脚本、归因 Skill 共用；--stdout 则仅返回同结构 JSON，不写文件。不再生成同内容 Markdown，也不导出完整结果、Digest 或双端前五行样本。报告文件可直接打开；每个查询对象占一行，源 SQL 里的换行用 JSON 转义保留，不能擅自压平 SQL 注释。

~~~text
reports/validation/<batch-id>-validation.json
├── run              本次运行信息：输入/YAML 路径与来源指纹、.out 路径/格式、运行时间、
│                    SQLGlot 版本/提交、模式、双端逻辑连接与库名、共用比较规则。
├── summary          运行总结：记录数、匹配数/明确分母的匹配率、失败分类、负向数量、
│                    待归因/前提排查数量、导入计数和当前证据限制。
└── queries          一条源 SELECT 一条记录；所有记录均保留 id、source_sql、result。
                     匹配只保留这三个字段；差异才加生成 SQL、具体错误或有限反例。
                     源端负向保留错误和已有目标表现，默认不进入主修复范围。
~~~

### 8.1 汇总统计与匹配率

例如一个文件选出 55 条 SELECT：35 条匹配、5 条源端负向、15 条 Doris 执行失败，其 summary 中的主要字段为：

~~~json
{
  "total": 55,
  "processed_queries": 55,
  "successful_matches": 35,
  "known_source_success": 50,
  "negative_source_cases": 5,
  "needs_attribution": 15,
  "prerequisite_issues": 0,
  "successful_match_rate": {
    "numerator": 35,
    "denominator": 50,
    "value": 0.7,
    "meaning": "成功匹配 / 已取得成功源结果；包含已读到成功 .out 的转译失败，不含源端报错或源结果未知"
  },
  "outcomes": {"匹配": 35, "源端负向用例": 5, "Doris 执行失败": 15},
  "failure_counts": {"Doris 执行失败": 15}
}
~~~

这是字段节选，不是已执行报告。total 是本次查询记录总数，包含已保留 SQL 的导入输出读取失败；processed_queries 是进入 run 逐条处理的数目，不代表都执行了数据库 SQL。known_source_success 是实际取得成功源结果的数目，包括已从 .out 补读源成功的转译失败。分母为 0 时比例为 null，不写成 0% 或 100%。

outcomes 每条只计一个主要结果，合计等于 total。failure_counts 排除匹配和源端负向，只统计需关注的失败/差异；needs_attribution 是建议进一步归因的数量，不是已确认 SQLGlot 缺陷数。prerequisite_issues 是环境、输出读取或源证据需要先排查的数量。使用 --id 时只统计本次所选范围，run.filtered 为 true，summary.import 仍是整个 YAML 的导入计数，不能混作本轮查询数。

### 8.2 匹配与源端负向用例

匹配记录仅保留：

~~~json
{"id": "实际 Case ID", "source_sql": "SELECT 1 AS value", "result": "匹配"}
~~~

匹配表示当前可用比较证据没有差异，不再要求后续处理；不代表没有拿到的原生类型、全部边界也已验证。summary.evidence_limits 集中说明这些限制，避免每条重复。

源端负向是 .out 或实时源端本身报错，默认不为复刻 PostgreSQL 错误安排独立 Doris 改写。记录 result 为“源端负向用例”、action 为“默认不归因”，保留 source_error 的具体消息及已有目标状态/错误，不计成功匹配。源端缺表、权限、连接等则记“源端环境问题”，不是正常的负向语义测试。归因 Skill 仍需核对原用例意图，不能只凭一个分类标签断定源 SQL 非法。

### 8.3 差异、执行错误和处理方向

非匹配记录按需要增加字段，以下错误示例为结构说明，实际消息由数据库返回：

~~~json
{
  "id": "实际 Case ID",
  "source_sql": "SELECT COUNT(*) AS n FROM orders",
  "result": "Doris 环境问题",
  "action": "前提排查",
  "source_status": "成功",
  "reason": "Doris 连接、库表或权限等前提不满足",
  "target_sql": "SELECT COUNT(*) AS n FROM orders",
  "doris_status": "报错",
  "doris_error": {
    "category": "表不存在",
    "message": "<数据库原始错误消息>",
    "code": "<数据库实际错误码>"
  }
}
~~~

action 的含义：

- 归因：源端成功，但转译、Doris 执行或结果有差异，需要代码分析与必要对照；不是已经证明 SQLGlot 有缺陷。
- 前提排查：先处理缺库表、权限、输出读取或证据不足；不直接列为 SQLGlot 修复任务。
- 补查源证据：例如转译失败且 .out 读取也失败，不能据 SQLGlot Parser 报错推定源 SQL 非法。
- 默认不归因：源端负向用例保留事实，默认不进入主修复范围。

result 用中文写具体阶段：“SQLGlot 转译失败”“Doris 执行失败”“字段不匹配”“行数不匹配”“行值或顺序不匹配”等。transpilation_error、source_evidence_error、source_error、doris_error 只在有对应证据时出现，保留实际错误而非笼统的“可能语义不同”。无生成 SQL 时不伪造 target_sql。字段/行数比较提前失败后不宣称后续维度已检查。

### 8.4 具体差异与导入异常

difference 只保存足以定位的证据，不重复两边任意的前几行：

~~~text
字段差异    source_column_count / doris_column_count；实际不同字段最多三项，附省略数。
行数差异    source_row_count / doris_row_count。
顺序比较    不同位置的实际双端值，最多三处，附省略数。
无序比较    每侧最多三种无法配对的记录及多出的次数；忽略顺序但不丢重复行。
~~~

例如相同行数但重复次数不同，difference 可显示源端某行多一次、Doris 另一行多一次。比较仍基于完整的本次结果，报告只截取反例；不是只拿这三条比较。有限反例不能代替后续归因的完整有限结果、原生类型和边界验证。

普通 DDL/DML 的跳过只在 summary.import 计数，不在报告逐条展开；YAML 仍保存完整导入诊断。导入阶段未能读取 .out 且保存了原 SELECT 的记录，会写入 queries，标明原因和源位置；不悄悄当作已验证或从总数中消失。Parser 拒绝的只读 SELECT 会保留为普通失败 Case，Recorded Output 的 run 仍尝试从 .out 补读源状态，不连接源库、不执行失败 SQL。全部无法导入或输入无效时，命令直接报错，未进入 run 便不会产生验证报告。

### 8.5 证据限制与后续归因

Recorded Output 通常只有显示文本，可能缺原生类型，或不能区分 NULL/空字符串等；Live Source 可取得更多类型化证据。共用规则在 run.comparison_rules、限制在 summary.evidence_limits，一次说明而不逐条复制。

表查询不匹配时仍需依次核对数据阶段、表/类型映射、Session、UDF、输出读取、驱动表示、生成 SQL 和数据库行为。缺表应在框架外准备后重跑；两边都有表但数据不同，也可能只表现为行数/行值差异，框架不能单凭结果推断究竟缺了哪些基表记录。

归因 Skill 直接读取本批各阶段验证 JSON，再沿 run 路径读取 YAML、原 SQL/.out；准备材料精确路径由调用者提供。首轮只生成批次汇总和每条非匹配、非源端负向 SELECT 的 Markdown，事实与原因写入 Case；共同方案、独立行为修复/commit 边界、依赖及验收集中在汇总 task 条目。汇总是唯一当前任务清单，后续增量更新状态/关联 Case/轮次/commit 链接；首轮事实不改写，同 Case 的后续发现追加，不按轮次复制。原匹配回归或新增接受查询需调查时才补新 Case 文档并单列，不回改首轮数量。前提和研究事项明确下一步，不冒充可实施任务；默认源负向不另建文档。

probe-pg-case 接受 --candidate-sql 文本（- 表示标准输入）及可选 --source-variant-sql，在内存核对输入并执行只读对照，比较完整有限结果后向终端返回类型、行数、错误、最多三行样本与具体差异反例，不创建 SQL/Markdown/JSON 文件。Agent 将必要事实整理入本 Case 文档，不复制大结果或整个返回值。匹配与源端负向记录没有历史生成 SQL，工具不会重新生成来冒充旧输出；新边界必须真实执行 PG，不能借用原 .out。具体指令和两类 Markdown 的字段见工作流第 6 节。

同一实际数据阶段的多条候选优先使用 probe-pg-batch --candidates-json -，从标准输入一次传 JSON 数组，每项包含 case_id、candidate_sql 和可选 source_variant_sql。同阶段材料只读取一次，每请求仍独立安全检查、连接执行、比较和重复执行，不缓存查询结果。一条失败保留错误并继续；不同阶段分开调用。默认返回逐条 JSON 事实与有解释统计，--output-format markdown 向终端返回可整合入现有报告的中文事实片段，不生成新文件。完成调用不代表执行成功、全部等价或根因已定位；AI 仍负责代码归因、修复范围与限制，共同依据可复用但逐条例外不能省略。

步骤四显式调用修复 Skill，可选“指定任务”或“整份输入持续修复”。前者只实施所选 task；后者在固定输入/阶段/规则内持续调查剩余差异，不用每次重新人工调用归因 Skill。同根因继续原 task，已验收范围内遗漏重新打开，独立能力新增 task；新引入回归优先查引入 commit。不同 SQL/错误文本相同不足以判重，同一 Case 可含多个问题。

task-id 是跨轮问题编号，fix-001/fix-002 是执行轮次，commit 是实际代码变化，不是一一对应。一组独立行为修复连同相关测试作为一个 commit，同 task 补遗漏可追加提交；不因同轮或同文件混合无关问题。获明确 commit/push 授权后核对指定 fork 和实验分支，按约定保存代码，不擅自更新 main、推 upstream 或强推历史，也不需要在 fork 创建 PR。社区 Issue/PR 不是默认动作。运行结果必须来自修改后 SQLGlot 重新生成并执行的 SQL，不以手写候选替代。

持续修复通常明确授权“按功能本地commit、暂不push”：每项行为验收后核对准确提交内容、生成真实修复SHA，再进入下一独立功能，不等整个workflow结束再打包。未获commit授权先确认；明确的未提交试验是例外，不能默认扩展到后续全部功能。已有多个功能混合在dirty文件中时先停止叠加，按[工作流第7.2节](POSTGRES_MANUAL_WORKFLOW.md#72-跨轮任务维护与提交边界)提出保留原checkout的拆分重建方案。提交和测试依据仍写在已有报告，不增加台账。

每轮仍只生成 reports/fixes/<batch-id>-<fix-batch>-summary.md 和 reports/fixes/tasks/<batch-id>/<fix-batch>/<task-id>.md，跨轮 task-id 不变，前轮报告保留。本轮写清模式/权限、真实 commit/推送状态、新增/复用/重新打开任务、实际验收及下一轮入口；不增加实施/回归报告、日志、patch、执行 JSON 或台账。统一任务清单增量维护，Case 追加证据，不抹去首轮/前轮事实。

整份输入完成不等于某轮结束、task list 首次清空或 push 成功。必须覆盖所有纳入的源成功查询及阶段（含 Parser 拒绝/新增接受），全部可由 SQLGlot 安全修复任务验收，最终同一代码版本全阶段回归无未解决新回归，且剩余差异有不能仅改 SQLGlot 解决的依据。未调查、可修复性未知或关键前提/证据阻断时写未完成和恢复条件；源负向默认排除，不强求 100% MATCH。详细调用和完成检查见 [工作流步骤四](POSTGRES_MANUAL_WORKFLOW.md#7-步骤四修复并验证新生成的-sql)。

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

## 10. 自备输入的操作路径

以下 inputs/postgres/queries-001/ 是一次上传批次的示例位置，不是仓库内置样本。自行提供配对的 queries.sql、queries.out，并在框架外准备两端所需的表和数据。queries 来自输入文件名，不是预设名称；用户原文件不要求改名。再次上传或重新准备时用下一个编号，例如 queries-002。三份准备产物直接放在 reports/data-preparation/，用相同批次前缀归组，不建立子目录、不另生成核验 JSON，详见 [工作流第 2、4 节](POSTGRES_MANUAL_WORKFLOW.md#2-输入与目录约定)。

完成 Doris 数据准备后：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input inputs/postgres/queries-001/queries.sql \
  --recorded-output inputs/postgres/queries-001/queries.out \
  --source-database dsv_demo --target-database dsv_demo \
  --output reports/data-preparation/queries-001-cases.yaml

.venv/bin/doris-sql-validator run \
  --path reports/data-preparation/queries-001-cases.yaml \
  --output reports/validation/queries-001-validation.json
~~~

本指南主流程必须传 --recorded-output。现有 CLI 不传时仍会选择 Live Source，但这属于用户额外选择的诊断方式，不是主流程。仅导入和 lint 不连接数据库；run 会执行目标查询。使用不同 --output 文件名保留多次运行；报告和生成的 YAML 都是本地运行产物，默认不提交。

自行取得的官方回归文件可能含多阶段数据和外部对象依赖，不保证全部 SQL 可在空库直接执行。学习后续人工归因与修复，见 [PostgreSQL 工作流](POSTGRES_MANUAL_WORKFLOW.md)。

## 11. 功能范围与限制

当前已实现：

- 源方言/引擎：Hive、PostgreSQL；
- 目标方言/引擎：Doris；
- 普通 SQL、Hive QTest、PostgreSQL pg_regress 导入；
- Live Source 和 Recorded Output；
- 单条只转译；
- 常量查询与表查询；
- 执行状态、错误、Schema 和结果数据比较；
- 唯一精简 <batch-id>-validation.json，以及人工调用阶段独立保存的对照证据。

当前不负责：

- 执行 DDL/DML；
- 自动把源数据库的数据同步到 Doris；
- 解析任意自定义 `.out` 格式；
- 为同一回显行中多条 SQL 猜测输出对应关系；当前会拒绝而不是随意配对；
- 为未知 UDF 自动安装对应函数；
- 对随机函数、当前时间或无稳定排序的 `LIMIT` 提供确定性保证；
- 静态证明两条 SQL 对所有可能数据都语义等价。

公开样例、参考报告及不应提交的本机文件见 [PUBLISHING.md](PUBLISHING.md)。参考报告的结果仅适用于其记录的版本、数据和 Session，不代表新环境的运行结果。
