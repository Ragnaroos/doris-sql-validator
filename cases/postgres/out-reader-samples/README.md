# PostgreSQL Recorded Output 读取样本

本目录用于测试框架从 PostgreSQL 官方回归脚本及 .out 中提取 SELECT 和参考结果的能力，不包含数据库运行报告。导入、检查均不连接 PostgreSQL/Doris。

本目录提供 8 组样本；另有 12 组位于 [batch-02/](batch-02/README.md)。

## 来源

- 仓库：[postgres/postgres](https://github.com/postgres/postgres)。
- 固定 Commit：`e405a46c45bae070364ed143fb9d5a631422e5e4`。
- SQL 原路径：`src/test/regress/sql/<name>.sql`。
- 输出原路径：`src/test/regress/expected/<name>.out`。
- `assets/` 保存从该 Commit 下载的完整原件，没有删减 DDL、DML、psql 命令、错误案例或输出。版权说明见 `UPSTREAM_COPYRIGHT`。

## 文件用途

| 文件名（均有 `.sql` 和 `.out`） | 主要查询内容 | 读取器需要面对的内容 |
| :--- | :--- | :--- |
| `boolean` | 布尔输入、逻辑运算、NULL、表查询 | 布尔文本、空值、正常结果和报错交替 |
| `char` | 定长字符输入、截断、转换、比较 | 空字符串、空格、字符结果和报错 |
| `float4` | 单精度浮点输入、算术、转换和边界 | 科学计数法、特殊浮点值、精度显示、错误 |
| `float8` | 双精度浮点计算、转换和边界 | 高精度数值文本、特殊浮点值、错误 |
| `money` | 货币算术、比较、输入和转换 | 带货币符号的文本、不同数据阶段的表结果 |
| `rowtypes` | 复合类型、嵌套行值、字段访问和表查询 | 含逗号、引号、括号的值，以及错误信息 |
| `functional_deps` | 主键/唯一约束下的 GROUP BY 和 JOIN | 空结果、正常分组、分组合法性错误 |
| `enum` | 枚举输入、排序、范围和元数据查询 | 普通表格、psql `\x` 展开输出、COPY 数据和错误 |

八个脚本自身都包含建表 DDL，不是只有 SELECT。其中七个包含 INSERT 等装数语句；`functional_deps` 故意使用空表，主要检查约束影响下的分组是否合法，不需要插入数据。它们仍是 PostgreSQL 回归脚本，不保证可在空库中独立完整重放；可能依赖回归环境、系统目录、类型/函数或 Session 设置。例如 `money` 明确要求 `lc_monetary=C`，`enum` 涉及系统目录与枚举定义变更，`rowtypes` 的部分查询依赖 `tenk1`、`int8_tbl` 等回归公共表；运行表查询前需自行准备这些依赖。

## 只测试导入与输出读取

在项目根目录执行，例如：

```bash
.venv/bin/doris-sql-validator import-cases \
  --format pg-regress --dialect postgres \
  --input cases/postgres/out-reader-samples/assets/boolean.sql \
  --recorded-output cases/postgres/out-reader-samples/assets/boolean.out \
  --output cases/postgres/out-reader-samples/generated-boolean.yaml

.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/out-reader-samples/generated-boolean.yaml
```

将 `boolean` 替换为表中其他文件名即可。`import-cases` 会进行 SELECT 解析和对应 `.out` 的定位、读取，生成的 YAML 直接引用 `assets/<name>.out`，不把结果拆成大量 JSON。DDL/DML 等非只读语句跳过，不执行。

YAML 的 `import_summary` 和 `import_diagnostics` 分别记录导入数量和未导入原因。`statement_type: recorded_output` 表示输出定位/读取失败，`statement_type: parse_error` 表示源 SQL 解析失败；它们都不是 Doris 执行错误。已导入的负向错误用例仍可包含参考错误，这是成功读取错误证据，不等于读取失败。

读取器支持默认 ASCII 纵向展开记录及横向多行单元格解析：`enum` 的 `pg_input_error_info` 展开输出按一行四列读取，`rowtypes` 的 `pg_get_viewdef` 多行定义按一行一列读取，换行及缩进保留。示例原件和参考答案保持不变。

导入数量不代表所有 SELECT 均已读取，也不代表类型和语义已验证。其他 SQL 解析/语句识别失败仍保留在 YAML；自定义边框、wrapped 自动折行等格式不在支持范围。默认空白显示的 NULL 和空字符串仍无法区分，排版填充与值本身的行尾空格也不能保证无损区分，不通过修改官方答案掩盖这些限制。

本目录的检查只读取输入、生成导入 YAML，不调用 `run`，不连接 PG/Doris，不生成 `validation.md/json`。若后续执行验证，必须先在框架外按查询对应阶段准备目标数据；不能用脚本最终表状态验证之前所有查询，也不能把官方 PostgreSQL 输出当成 Doris 已支持相同能力的证明。
