# PostgreSQL → Doris 快速示例

本示例提供可直接复用的 SQL、DDL/INSERT 和参考输出。所有命令从仓库根目录执行，先按 [安装说明](../../../README.md#安装) 安装依赖并配置 .env。

## 1. 示例文件

~~~text
examples/postgres/basic/
├── constant.sql / constant.out     一条不依赖表的 SELECT 及参考输出
├── queries.sql                     四条待验证的 PostgreSQL 查询
├── expected.out                    queries.sql 对应的 pg_regress 风格参考输出
├── postgres-setup.sql              新建 dsv_demo，创建表并插入五行；由 psql 外部执行
├── doris-setup.sql                 对应 Doris 专用库、Duplicate Key 表和同样五行
└── generated-*.yaml                import-cases 在本机生成，不随仓库提交
~~~

参考输出按示例输入定义，用于演示读取和比较；它不是任意数据库上的执行证明。结果应在实际使用的版本和会话中重新验证。

表 validation_demo_items 的固定记录为：

| id | category | amount |
| ---: | :--- | ---: |
| 1 | a | 10 |
| 2 | a | 20 |
| 2 | a | 20 |
| 3 | b | 0 |
| 4 | b | NULL |

相同记录出现两次是有意设计。id 不是唯一主键，Doris 使用 Duplicate Key 表，不能改成会覆盖重复记录的模型。

## 2. 离线导入与常量验证

不连接数据库即可执行：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input examples/postgres/basic/constant.sql \
  --recorded-output examples/postgres/basic/constant.out \
  --output examples/postgres/basic/generated-constant.yaml

.venv/bin/doris-sql-validator cases-lint \
  --path examples/postgres/basic/generated-constant.yaml
~~~

配置 Doris 后运行，不要求 PostgreSQL：

~~~bash
.venv/bin/doris-sql-validator run \
  --path examples/postgres/basic/generated-constant.yaml \
  --output-dir reports/demo/constant
~~~

DORIS_DATABASE 留空或设为已有可访问库；即使不依赖表，配置了不存在的默认库仍会连接失败。

## 3. 在验证器外准备表数据

仅在专用测试环境执行以下写入。两个准备脚本都会新建 dsv_demo；同名库存在时应停止并检查用途，不要删除已有库。重新演示时可先选择另一个未使用库名，并同时调整准备 SQL 与 import-cases 的数据库参数。

### 3.1 Doris

先启动可连接的 Doris FE/BE。下面示例使用本机 FE 的 MySQL 协议端口 9030；换成实际地址和账号，-p 交互输入密码：

~~~bash
mysql --host=127.0.0.1 --port=9030 --user=root -p \
  < examples/postgres/basic/doris-setup.sql
~~~

DDL 的 replication_num=1 适合至少一个可用 BE 的小型测试环境。多副本环境应按实际 BE 数调整。该脚本不由验证器读取或自动执行。

### 3.2 PostgreSQL（Live Source 或后续对照时需要）

使用仓库提供的 PostgreSQL 容器：

~~~bash
./scripts/postgres.sh up

docker compose -f docker/compose.postgres.yaml exec -T postgres \
  psql --username postgres --dbname postgres --set=ON_ERROR_STOP=1 \
  < examples/postgres/basic/postgres-setup.sql
~~~

也可以用自己的 psql 连接执行同一脚本。该文件包含 psql 的连接命令，应交给 psql，不交给 SQLGlot 或验证器执行。

.env 的 POSTGRES_* 需与容器或自有源库一致；DORIS_* 配置目标连接。库名由下面导入参数指定。Recorded Output 表验证只要求 Doris 准备好数据；若要由实时 PG 确认参考输出，再准备 PostgreSQL。

## 4. Recorded Output：只运行 Doris

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
  --output-dir reports/demo/recorded
~~~

导入应接受四条查询，导入错误数为零。验证结果随实际 SQLGlot/Doris 版本而定；出现差异时读报告，不要改参考答案来制造匹配。

## 5. Live Source：两端实时执行

先完成两端数据准备。使用相同 queries.sql，但不传参考输出：

~~~bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --source-connection-profile postgres-local \
  --input examples/postgres/basic/queries.sql \
  --source-database dsv_demo --target-database dsv_demo \
  --output examples/postgres/basic/generated-live.yaml

.venv/bin/doris-sql-validator run \
  --path examples/postgres/basic/generated-live.yaml \
  --output-dir reports/demo/live
~~~

表数据包含重复行和 NULL。第二条查询有稳定的最终排序；第三条无 ORDER BY，应忽略顺序但保留两次 amount=20；第四条的 COUNT(*) 与 COUNT(amount) 用于区分 NULL 参与行为。

## 6. 输出与后续处理

~~~text
reports/demo/
├── constant/validation.md / validation.json   常量结果
├── recorded/validation.md / validation.json   参考输出对 Doris
└── live/validation.md / validation.json       实时 PG 对 Doris
~~~

同一 output-dir 会被 run 覆盖，保留多次结果时使用不同目录。退出码 1 表示存在差异/失败，通常仍已生成报告；配置错误可能返回 2。

完整的交接、差异归因、独立候选执行和修复步骤见 [PostgreSQL 工作流](../../../docs/POSTGRES_MANUAL_WORKFLOW.md)。示例全部匹配时无须制造错误或创建修复任务。
