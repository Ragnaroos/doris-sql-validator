# PostgreSQL 官方回归样本

这些材料用于评估 PostgreSQL 查询经 SQLGlot 转译到 Doris 的行为。它们不是 PostgreSQL 全量回归环境，也不保证所有原脚本可在空库直接执行。首次使用建议先跑通 [小型示例](../../../../examples/postgres/basic/README.md)。

## 1. 来源与固定范围

来源为 [postgres/postgres](https://github.com/postgres/postgres)，提交 e405a46c45bae070364ed143fb9d5a631422e5e4。许可见 [UPSTREAM_COPYRIGHT](UPSTREAM_COPYRIGHT)。

本目录 20 份 YAML 包含 753 条查询；expanded/ 的 14 份 YAML 包含 972 条，共 34 组、1,725 条。Parser 不能识别的查询也可能作为普通失败 Case 保留，不表示这些语句都能转译或执行成功。所选范围不是整个原脚本，也不代表全部 SELECT 语法覆盖。

~~~text
assets/                   官方完整 .sql/.out、共享 test_setup.sql；包含非查询和多阶段语句
scope.json                基础选择范围、源位置、上游提交与原件指纹
setup/postgres-setup.sql   已选择表查询所需的 PostgreSQL 结构与初始记录
setup/data/               onek.data、tenk.data、agg.data 等 COPY 依赖
<group>.yaml              20 组固定选择的只读查询与参考输出引用
expanded/                 额外输入、14 组 YAML、选择和排除原因
UPSTREAM_COPYRIGHT        原始材料版权
~~~

## 2. 数据前提

表查询需要在验证器外准备相应数据库。PostgreSQL 结构/记录依赖位于 setup/，对应 Doris DDL/INSERT 示例见 [目标准备 SQL](../../../../reports/pg-manual/current/data-preparation/doris-setup.sql)，逐列映射限制见 [数据准备参考报告](../../../../reports/pg-manual/current/data-preparation/data-preparation.md)。

准备脚本必须经检查后在新的专用库执行；COPY 的数据文件路径、表/视图大小写、类型域和每条查询的数据阶段均需核对。不要把原脚本最终状态用于所有 SELECT，也不要直接执行原件中的 psql 外部命令。

可显式调用 pg-doris-prepare-data Skill，提供这些材料和自己的数据库授权。完整过程见 [工作流](../../../../docs/POSTGRES_MANUAL_WORKFLOW.md)。

## 3. 使用自己的数据库

附带 YAML 中的库名是参考运行环境标识，不代表数据库已经存在。先准备自己的专用库，例如 dsv_regression；然后创建新 YAML，保留源 SQL/.out 和查询编号，只设置实际库名：

~~~bash
.venv/bin/python - <<'PY'
from pathlib import Path
from doris_sql_validator.case_loader import load_case_file, write_case_file
loaded = load_case_file(Path("cases/postgres/manual/current/join.yaml"))
definition = loaded.definition
copy = definition.model_copy(update={
    "source": definition.source.model_copy(update={"database": "dsv_regression"}),
    "target": definition.target.model_copy(update={"database": "dsv_regression"}),
})
write_case_file(copy, loaded.path.with_name("generated-join.yaml"))
PY

.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/manual/current/generated-join.yaml

.venv/bin/doris-sql-validator run \
  --path cases/postgres/manual/current/generated-join.yaml \
  --output-dir reports/regression/join
~~~

新 YAML 与原件处于同一目录，使 assets/*.out 引用仍有效。生成文件默认忽略，不覆盖固定输入。换组时替换 join 即可，但仍需满足该组对象与 Session 前提。

把完整官方脚本重新 import 不等于运行这里的固定子集：它可能纳入额外表、不同数据阶段或未准备对象。处理自己的完整脚本应先定义这些前提。

## 4. 参考结果

[首轮汇总](../../../../reports/pg-manual/current/SUMMARY.md)和[归因汇总](../../../../reports/pg-manual/current/handoff/attribution/attribution-summary.md)展示固定版本/数据下的结果与尚未处理范围，不是当前机器的执行证明，也不是通用兼容性承诺。

验证器只读取 .out 并执行生成的 Doris 查询，不执行上述准备 SQL，不核验双端全表一致，不自动调用归因或修复 Skill。
