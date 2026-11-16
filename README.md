# Doris SQL Validator

将 PostgreSQL/Hive 的只读查询交给社区 SQLGlot 转成 Doris SQL，再比较源端证据与 Doris 的执行结果。

支持两种验证方式：

- Recorded Output：读取 PostgreSQL pg_regress 的 .out 或 Hive QTest 的 .q.out，只执行 Doris。
- Live Source：实时执行源数据库与 Doris，再比较结果。

CLI 不调用模型、不执行 DDL/DML、不建表装数，也不自动修复 SQLGlot。PostgreSQL 的数据准备、差异归因和修复可由用户显式调用三个项目 Skill 完成。

## 文档入口

| 文档 | 用途 |
| :--- | :--- |
| [快速示例](examples/postgres/basic/README.md) | 常量查询、五行表数据、Recorded Output 和 Live Source 的完整命令 |
| [用户指南](docs/USER_GUIDE.md) | 输入格式、YAML、连接配置、比较规则和报告解读 |
| [PostgreSQL 完整工作流](docs/POSTGRES_MANUAL_WORKFLOW.md) | 数据准备 → 验证 → 交接 → 归因 → 修复与回归 |
| [上游回归样本](cases/postgres/manual/current/README.md) | 官方 SQL/.out、固定选择范围、数据依赖及运行方法 |
| [发布约定](docs/PUBLISHING.md) | 应提交的文件、敏感信息检查和证据维护规则 |

## 安装

需要 Python 3.12。以下为 macOS/Linux Shell 示例；数据库容器另需 Docker Compose，执行 Doris 准备 SQL 另需 MySQL 兼容客户端。

~~~bash
git clone https://github.com/Ragnaroos/doris-sql-validator.git
cd doris-sql-validator

git clone https://github.com/tobymao/sqlglot.git ../sqlglot
git -C ../sqlglot checkout feb0e08aba28a29590596bb3f5761fbaeb0e98b9

python3.12 -m venv .venv
.venv/bin/python -m pip install uv
.venv/bin/uv sync --extra dev
cp .env.example .env
~~~

项目通过 editable dependency 使用相邻的 ../sqlglot。已有 checkout 时不要重复 clone；已有 .env 时不要覆盖。需要比较其他 SQLGlot 版本时自行选择提交，并在报告中保留实际版本。上述固定提交用于复现仓库附带参考报告，不代表要求所有用户永远使用该版本。

## 不连接数据库的快速检查

下面的命令只导入一条常量查询并检查 YAML：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input examples/postgres/basic/constant.sql \
  --recorded-output examples/postgres/basic/constant.out \
  --output examples/postgres/basic/generated-constant.yaml

.venv/bin/doris-sql-validator cases-lint \
  --path examples/postgres/basic/generated-constant.yaml

.venv/bin/doris-sql-validator transpile \
  --source-dialect postgres "SELECT 1 AS value"
~~~

配置 .env 中 Doris 的地址和账号后，即可执行同一条查询：

~~~bash
.venv/bin/doris-sql-validator run \
  --path examples/postgres/basic/generated-constant.yaml \
  --output-dir reports/demo/constant
~~~

Recorded Output 不连接 PostgreSQL。常量查询不要求创建测试表；DORIS_DATABASE 如有填写，必须是已有且允许访问的数据库。

报告位于 reports/demo/constant/validation.md 和 validation.json。生成的 YAML 及示例报告默认不提交。

## 表查询示例

[examples/postgres/basic/](examples/postgres/basic/README.md) 包含以下可复用材料：

~~~text
postgres-setup.sql       PostgreSQL 专用测试库、表和五行数据
doris-setup.sql          对应 Doris DDL/INSERT，保留重复行与 NULL
queries.sql             四条查询：常量、排序、重复值、多列聚合
expected.out            上述固定输入的 pg_regress 风格参考输出
constant.sql/.out       不依赖表的最小输入
~~~

按示例说明在验证器之外执行准备 SQL，然后导入并运行。框架不检查两端数据是否一致；缺表属于环境错误，数据不同可能表现为行数或行值差异，不能据此直接判定 SQLGlot 有缺陷。

## 通用使用方式

有 PostgreSQL 参考输出时，将 SQL、.out 和生成的 YAML 放在同一目录或其子目录：

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

不传 --recorded-output 时走 Live Source，需要两端可连接且已准备相应数据。Hive 的对应参数与输出格式见用户指南。

## 报告与限制

报告先给总体数量和匹配比例，再展开不匹配、转译失败、环境错误及源端负向用例。生成的 Doris SQL 保存在报告，不写回 YAML。

比较涉及执行状态、错误类别、字段数量/显式 Alias/可用类型、行数、行值、重复次数和顺序。无最终 ORDER BY 时按多重集合比较；有最终排序时逐行比较。Recorded Output 缺少类型等证据时不会将缺失项当作通过。

MATCH 仅表示现有证据未发现差异，不是所有数据上的等价证明。随机函数、当前时间、非稳定 LIMIT、Session、UDF、类型域和驱动表示都可能影响结论。源端报错不计成功结果匹配，归因阶段默认不为这些查询复刻 PostgreSQL 的错误。

[参考报告](reports/pg-manual/current/SUMMARY.md)是固定版本和数据条件下的示例证据，不是通用兼容性承诺，也不是新用户必须建立的目录或数据库。

## 开发检查

~~~bash
.venv/bin/pytest tests/unit \
  --ignore=tests/unit/test_postgres_attribution.py \
  --ignore=tests/unit/test_postgres_review_report.py
~~~

两个被排除的文件名用于避开未发布的历史证据测试；公开框架测试不依赖数据库。数据库实际执行须使用用户自行配置的独立测试环境。
