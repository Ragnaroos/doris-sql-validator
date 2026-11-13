# PostgreSQL 已准备数据阶段与种子输入

最新首轮范围已扩展为 **1,722 条用例**：本目录原有 750 条，加上 `expanded/` 中的 972 条新查询。新增输入和复现命令见 [expanded/README.md](expanded/README.md)，最新结果见 [SUMMARY.md](../../../../reports/pg-manual/current/SUMMARY.md)。旧首轮报告已从 current 移除并在本地归档。

下面的 753 条选择范围、750 条可运行查询及历史统计只说明原有数据阶段与种子输入，不再代表完整的最新首轮范围。保留这些输入是为了复用已核验的 21 张表/视图，而非复用旧报告结果。

本批对应 `docs/POSTGRES_MANUAL_WORKFLOW.md` 的步骤一、二。2026-11-11 首次在双端专用库 `dsv_pg_manual_20261111` 准备数据；按用户要求修复输出定位后，再完整复核同一批数据、重新导入并覆盖 current YAML/报告。没有复用旧运行结果、独立改写或归因结论。

```text
assets/
  20 份 PostgreSQL 官方 .sql/.out 原件和共享 test_setup.sql
  原件含 DDL/DML、多个数据阶段和更多 SELECT；不代表这些内容全被本批执行
UPSTREAM_COPYRIGHT
  PostgreSQL 上游版权与许可文本
scope.json
  固定选择的 753 条原 SQL、来源行号、最初的输出位置记录、官方 commit
  及输入 SHA-256；只保存选择依据，不保存历史运行结果或旧归因
  运行时的 output_occurrence 由当前 Importer 用统一回显规则重新计算
setup/postgres-setup.sql
  对应所选查询的 21 张逻辑表/视图初始阶段；只有已审查 CREATE/INSERT
setup/data/
  onek.data、tenk.data、agg.data：官方 COPY 依赖，不是生成的假数据
<script-name>.yaml
  当前 Importer 实际生成的 19 份精简 YAML，共 750 条只读查询
  指向 assets 下原始 .out；源库/目标库均指向本批独立库
  每条查询仍为原始 SQL，未填 AI 改写的 Doris SQL
```

上游 commit：`e405a46c45bae070364ed143fb9d5a631422e5e4`。本批重用历史已固定的“选择范围”，不是重跑官方全部回归脚本。未纳入范围的 SELECT、其他临时表、后续修改数据阶段和随机查询不表示已通过或已覆盖。

`select_distinct_on.sql` 所选三条在当前 SQLGlot Parser 的 `ORDER BY ... USING` 处均失败，所以没有为它造一个空 YAML；在报告目录保存导入失败说明和原 SQL。本轮仅余这 3 条导入失败，`.out` 配对失败为 0。原始 SQL、标准答案及 SQLGlot 未修改。

已修复上一轮 9 条配对问题：5 条出现次数统计口径错误、4 条查询内部空白行与回显不同。Importer 与 `.out` Parser 现在共用保守的原文回显规则，容忍字面量、引号标识符和注释之外的空白行与终止符差异，不改受保护内容。9 条都重新导入并实际执行；其中 3 条成功结果匹配，另外 6 条暴露执行或行值差异，具体编号与结果见 SUMMARY 第四节。

## 数据准备与首轮验证的边界

外部准备助手 `scripts/pg_manual_sample.py` 对本批已审查的输入创建新库、装数并完整核验；不是框架内的 Fixture Gate，不支持用它准备任意用户语料。当前 CLI `run` 只读 `.out`、调用社区 SQLGlot、执行 Doris、比较和报告，不执行本目录中的 CREATE/INSERT/COPY，也不核验两端表。

本批表数据一致的证据和类型映射限制见 `reports/pg-manual/current/data-preparation/`。全部 753 条源查询在数据准备阶段重新执行：620 条成功结果与 `.out` 显示文本及重复次数一致，133 条均报错；参考输出定位失败为 0。负向报错仅确认失败，不证明当前 PG 与历史错误完全同因。

本轮 750 条进入运行器，628 条实际发往 Doris（另 122 条先转译失败）；160 条成功结果匹配。读取输出问题修复不等于所有查询兼容性问题已修复。

## 已有环境下重跑单组

以下命令不建表、不改数据；新机器先由人调用准备 Skill。不要覆盖已保存的首轮报告。

```bash
.venv/bin/doris-sql-validator cases-lint \
  --path cases/postgres/manual/current/join.yaml

.venv/bin/doris-sql-validator run \
  --path cases/postgres/manual/current/join.yaml \
  --output-dir reports/pg-manual/local-rerun/join
```

`local-rerun` 默认不发布。首轮汇总在 `reports/pg-manual/current/SUMMARY.md`；这批仅做到确定性验证，没有进入人工归因或修复。迁移到新数据库时，必须在新的输入/报告目录重新准备和生成 YAML，不能只改已出报告 YAML 的库名。
