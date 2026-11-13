# PostgreSQL 扩展首轮输入

最新首轮共 1,722 条用例：上级目录 19 份 YAML 中的 750 条，加上本目录 14 份 YAML 中的 972 条。源 SQL 原文去重为 1,711 条；不同来源/编号的同文用例仍保留，没有把用例数称为去重 SQL 数。

```text
assets/
  两批新增官方脚本的 20 组 .sql/.out 原件；保留完整 DDL/DML 和输出，不修改答案
<script-name>.yaml
  14 份可以直接交给当前 CLI 的精简 YAML；共 972 条新查询
  源/目标库指向 dsv_pg_manual_20261111；源证据引用 assets 下对应 .out
  其余 6 个脚本没有符合本次条件的查询，不为它们生成空 YAML
selection.json
  原有与新增各组 YAML 的索引、纳入数量，以及暂不执行的完整源 SQL 和具体原因
  新增 2,165 条可读取查询中，972 条纳入、1,193 条暂不纳入
environment-check.json
  输入准备时的框架外只读检查；实际运行前的最终检查保存在报告目录同名文件中
```

新增范围只选无表引用、无自定义类型/函数依赖、输出可固定且不访问外部资源的查询。表值函数也保守排除。缺少准备的表、Domain、枚举、UDF 等用例保留在 `selection.json`，不是验证通过，也不把缺少这些对象当成 SQLGlot 缺陷。

原有表数据沿用先前完整准备的阶段；本次只读复核了 21 张表/视图的结构、全部记录、重复次数和初始指纹，没有执行新的建表或装数。`.out` 模式下的框架验证只执行 Doris，不连接 PG；PG 连接只用于框架之外的数据前提核验和内置对象清单查询。

在项目根目录重跑单组（请写入自己的新报告目录，避免覆盖当前证据）：

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/manual/current/expanded/float8.yaml

.venv/bin/doris-sql-validator run \
  --path cases/postgres/manual/current/expanded/float8.yaml \
  --output-dir reports/pg-manual/local-rerun/float8
```

完整替换首轮由人明确调用本地复现助手，前提是已有本批独立数据库和两批输出读取样本。它不调用 AI、不执行 DDL/DML；旧首轮报告移动到默认忽略的本地 archive，数据准备与交接文件不移动。

```bash
.venv/bin/python scripts/pg_expanded_first_round.py --run-and-replace
```

最新入口：`reports/pg-manual/current/SUMMARY.md`；逐组详情：`reports/pg-manual/current/validation/<script-name>/validation.md`，同目录 JSON 可供后续人工调用的归因流程使用。首轮不匹配不是最终原因判定；尚未执行 AI 归因或修复。
