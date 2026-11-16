# PostgreSQL 扩展回归样本

本目录提供 14 份固定选择 YAML，共 972 条查询；与上级目录合计 34 组、1,725 条。上游提交和许可沿用 [样本说明](../README.md)。

## 1. 文件结构

~~~text
assets/                  20 组官方完整 SQL/.out，保留 DDL/DML、错误和输出
<group>.yaml             14 份固定查询集合及参考输出引用
selection.json           已选择查询、未选择 SQL 及具体排除原因
environment-check.json   参考运行使用的对象/会话和外部只读数据检查证据
~~~

原脚本可读取查询中，972 条纳入固定范围，1,193 条因对象依赖、非确定性或外部资源等条件未纳入；未纳入不表示已经通过。源文件更多，不意味着每份都生成可运行 YAML。

## 2. 使用条件

固定选择优先采用不引用表、无用户自定义函数/类型、输出可固定且不访问外部资源的查询，但数据库版本、内置函数、Collation 和 Session 仍可能不同。原完整脚本中的系统目录、枚举、Domain、视图、公共表等前提不能忽略。

Recorded Output 不连接源库，目标连接的库名仍须有效。归因阶段若实时执行 PG，需要可用源库及对应前提。参照 [上级 README](../README.md#3-使用自己的数据库) 创建指向自己库名的新 YAML，不直接修改附带参考输入。

## 3. 导入与执行

只检查固定 YAML，不连接数据库：

~~~bash
.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/manual/current/expanded/float8.yaml
~~~

完成自己环境的配置和前提准备后运行。若库名不同，按上级方法先生成 generated-float8.yaml：

~~~bash
.venv/bin/doris-sql-validator run \
  --path cases/postgres/manual/current/expanded/generated-float8.yaml \
  --output-dir reports/regression/float8
~~~

所有路径相对仓库根目录。运行结果写到自己的 reports/regression/，不覆盖 [参考汇总](../../../../../reports/pg-manual/current/SUMMARY.md)。

脚本 pg_expanded_first_round.py 是固定语料的维护辅助程序，会使用专用环境元数据并替换参考目录，不是新用户的一键初始化入口。普通使用采用 import-cases / cases-lint / run，完整步骤见 [工作流](../../../../../docs/POSTGRES_MANUAL_WORKFLOW.md)。
