# aggregates-001 / fix-001：task-001 修复尝试汇总

## 1. 结论与范围

仅处理[task-001：Doris 数组字面量生成](../attribution/aggregates-001-attribution-summary.md#task-001)。已实现 `ARRAY[...]` → Doris `ARRAY(...)`，保留元素、NULL、嵌套结构及显式 CAST；没有顺带修复其他 task。

本轮状态为**已修改但未完成验收**：生成规则、相关单元测试和已测行值通过，但不能宣称两端字段类型全部一致。无显式 CAST 的整数数组存在 `int[]` / `array<tinyint>` 差异；Decimal 精度也仍有证据限制，详见[任务报告](tasks/aggregates-001/fix-001/task-001.md)。这些保留项没有通过修改比较器或输入来掩盖。

| 任务验收状态 | 数量 |
| :--- | ---: |
| 已修复并完成约定验收 | 0 |
| 已修改但未完成验收 | 1 |
| 当前阻断 | 0 |
| 未处理 | 0 |
| 不需修改（当前版本已覆盖） | 0 |

一个 task 关联 14 条原查询；其中 13 条含值列表数组，另 1 条 `ARRAY(SELECT ...)` 明确不在本任务范围，只作排除检查。没有重跑全部 313 条查询，也没有实施 task-002–009。

## 2. 代码与运行环境

| 项目 | 本轮实际值 |
| :--- | :--- |
| 实验 checkout | [sqlglot-experiment](../../../sqlglot-experiment/) |
| 本地分支 | `codex/doris-array-literal` |
| 上游 | `https://github.com/tobymao/sqlglot.git`，已执行 `git fetch upstream main` |
| 拉取后的社区基线 | `b812ff95afa2ab7ab925f95edd5d97c4b761cec9` |
| 基线提交 | 2026-11-19T14:03:57-06:00；`fix: Add tests and fix Databricks split part annotate type (#9265)` |
| 实际导入版本 | `30.25.1.dev355` |
| 本轮 diff | 3 个文件，88 行增加、1 行删除；未提交 |
| `git diff --binary` 的 SHA-256 | `a09017a32b5c305aea4cca6f27d6361d30505e962db44bc1c37841830ba2a819` |
| 数据库 | PostgreSQL 18.1，127.0.0.1:5432；Doris 4.1.3-rc02-7126cf65d96，127.0.0.1:9030 |
| 阶段库 | 原 YAML 指定的 `dsv_wf_agg001_s01/s03/s17/s31/s33/s40/s42`；既有匹配回归另覆盖其原阶段库 |
| Session / 查询保护 | UTC；PG ISO, MDY、extra_float_digits=0；Doris enable_strict_cast=false；补证每条超时 10 秒、最多 10000 行，未截断冒充完整结果 |

本轮读取 PG version() 确认 18.1；Doris 产品版本引用已有数据准备记录，本轮 VERSION() 返回兼容值 5.7.99，未将它当作 Doris 产品版本。

原 [sqlglot](../../../sqlglot/) checkout 保持 `feb0e08aba28a29590596bb3f5761fbaeb0e98b9`，受版本控制文件无修改。本轮从本地独立复制 Git 对象和文件后拉取社区 main；不是在旧基线上直接修补。实验目录的 origin 配置为 Ragnaroos/sqlglot，upstream 为社区仓库；本轮未向任何远端写入。

遵循目标仓库 AGENTS.md、CONTRIBUTING.md 和项目 `pg-doris-fix` Skill。实验目录最初无用户代码改动；工作流目录已有修改不属于本轮。核对原有准备/YAML/首轮 JSON/归因共 316 个文件，内容未变。没有建表、装数、复制输入或改写原 .out；没有创建额外脚本、日志、执行 JSON 或 evidence 目录。

单元测试使用实验目录新建的 `.venv`（Python 3.12.15）；构建和测试依赖只安装到该隔离环境。数据库验收使用已有验证器解释器并显式指定 PYTHONPATH：

```text
解释器：../doris-sql-validator/.venv/bin/python（Python 3.12.15）
工作目录：doris-sql-validator-workflow
PYTHONPATH：../sqlglot-experiment:src
sqlglot.__file__：../sqlglot-experiment/sqlglot/__init__.py
sqlglot._version.__file__：../sqlglot-experiment/sqlglot/_version.py
```

模块路径、版本、commit 与未提交 diff 一起确认运行身份，不只依赖一个版本字符串。凭据读取既有 `../doris-sql-validator/.env`，未写入报告。修复前/后 HEAD 相同，因为没有 commit。

## 3. 任务与完整查询结果

| 任务 | 状态 | 代码与测试归属 | 报告 | 建议独立 PR 的目标 |
| :--- | :--- | :--- | :--- | :--- |
| task-001 | 已修改但未完成验收 | Doris Generator、Doris Parser、test_doris.py | [实施与验收](tasks/aggregates-001/fix-001/task-001.md) | 值列表数组构造；不合并排序、聚合、有序集合或 UDF 迁移 |

最新社区基线仍复现数组继承 MySQL unsupported 的缺口。修改后，13 条范围内原查询中有 11 条能够完成严格转译；另 2 条仍被 task-002 的位置排序阻断。排除的数组子查询构造继续明确拒绝。

按原 YAML 和原 .out 运行 CLI `run --stdout --id ...` 的 **14 条关联查询**，结果如下；这不是所有语义维度的通过率：

| 完整查询结果 | 数量 | 说明 |
| :--- | ---: | :--- |
| 匹配 | 1 | Case 0306；原 .out 无原生类型，实时补证仍发现 numeric / bigint 差异 |
| 行值或顺序不匹配 | 1 | Case 0010：PG 数组显示 `{hello,world}`，Doris 显示 JSON 数组；实时结构化元素相同，但原比较规则未放宽 |
| Doris 执行失败 | 9 | 5 条 WITHIN GROUP 语法失败；3 条 VARIADIC 调用形式失败；1 条缺少 RWAGG |
| SQLGlot 转译失败 | 3 | 2 条位置排序；1 条排除范围内的 ARRAY 子查询构造 |
| 合计 | 14 | 原始查询没有删减、答案没有替换 |

## 4. 回归与后续限制

| 实际执行范围 | 结果 |
| :--- | :--- |
| Doris、MySQL、PostgreSQL 定向单元测试 | 133 个测试通过 |
| 全部方言单元测试 | 1045 个测试通过 |
| Parser/Generator/Expression/Transpile/Build/Token/Schema/方言导入核心测试 | 230 个测试通过 |
| Ruff check、Ruff format --check（三个改动文件）、git diff --check | 通过 |
| 原先 .out 匹配的 62 条查询，跨 15 个阶段，CLI 原规则回归 | 62 条仍匹配 |
| 18 个固定 PG 边界 SELECT，目标全部由修改后 SQLGlot 生成 | 两端均成功，字段数量/显式别名、行数、结构化值及重复次数一致；类型声明不能统一判为一致 |
| 5 个边界各增加一次双端执行 | 值和重复次数保持一致；其中稳定 id 排序样例顺序一致 |
| 14 条关联源查询的实时 PG 文本化结果与历史 .out | 行值多重集合均一致；只补查源基线，不替换原 .out，不据此证明排序等价 |

方言测试最初因缺 pytz、子进程找不到 python，随后因缺 python-dateutil 的日期简化路径失败；补齐隔离环境并设置 PATH 后重新运行，最终 1045 个通过。不能把这些中途失败当作代码已无条件通过。

没有执行完整根测试集、SQLGlot C 扩展测试、完整 mypy 或 make check；没有验证所有 Doris 版本、数组下界/文本数组 CAST/用户定义元素类型，也没有修复验证器的数组声明类型映射。当前只交付本地试验代码及这两份修复 Markdown，不生成 PR 附件。

后续应先明确整数/全 NULL 数组的隐式类型契约，并补 Decimal 元素精度证据，再决定是否需要独立的类型补齐任务。提交者还需人工审查代码及社区贡献要求；本轮**未 commit、未 push、未创建 Issue 或 PR**。

