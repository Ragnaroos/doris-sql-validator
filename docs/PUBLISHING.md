# 远程发布范围

## 1. 当前保留范围

```text
README.md、pyproject.toml、uv.lock、.env.example、.gitignore
  当前项目入口、依赖和不含真实密码的配置模板
src/、tests/、docker/、scripts/*.sh
  当前框架、测试和本地环境；历史评估专用脚本/测试除外
.agents/skills/
  数据准备、归因、修复三个显式调用 Skill 和模板
docs/USER_GUIDE.md
  用户操作、输入、YAML 和报告说明
docs/POSTGRES_MANUAL_WORKFLOW.md
  当前人工连续链路、命令、证据要求和边界
docs/PUBLISHING.md
  本发布约定
scripts/pg_manual_sample.py
  本批官方样本的数据准备/首轮复现助手；不替代任意用户输入的通用 CLI
scripts/pg_expanded_first_round.py
  扩展样本的显式首轮助手；不是当前归因 Skill 的自动执行器
cases/postgres/manual/current/
  最新一批原始 SQL/.out、数据依赖、固定样本范围和实际生成的 YAML
cases/postgres/out-reader-samples/
  PostgreSQL .out 读取测试样本及扩展首轮助手的来源输入，保留官方版权声明
reports/pg-manual/current/
  最新数据准备证据、逐组首轮报告和 SUMMARY.md；后续人工阶段也写入本目录
cases/hive/candidates/
  当前 Case Loader 测试依赖的两个兼容样本；不是历史数据库评估结果
```

保留 Hive/Live Source 的现有实现和必要测试，不意味着本批执行了 Hive 或历史全量回归。
官方 PostgreSQL 输入附带 `UPSTREAM_COPYRIGHT`。本批仅重用官方输入与固定选择范围，不复制历史执行答案以外的旧观测结果或旧归因结论。

## 2. 本地保留但不发布

`.gitignore` 排除历史 `reports/postgres-capability/`、`reports/upstream/`、`reports/pg-manual/smoke/` 等非 current 报告，旧 `cases/postgres/capability/`、`cases/upstream/`，历史评估脚本及其两个证据依赖测试，以及已被当前指南替代的旧设计文档。它们没有被删除，仍可在本地阅读。冒烟报告的原中文目录和文件已实际迁移到 `reports/pg-manual/smoke/` 下的英文路径；文件名变化不表示执行了新验证，仍不进入远程提交范围。

不提交 `.env`、`.venv/`、缓存、上游完整 checkout、下载的 Hive JAR 或账号密码。新报告不应包含密码、令牌或连接串；提交前仍需人工检查。

`scripts/pg_manual_attribution_batch.py` 是早期 109 条归因/修复试验助手，不能重现当前新版 Skill 的归因轮次；保留本地但不发布。当前归因由人显式调用 `.agents/skills/pg-doris-attribute/`，不是运行这个旧脚本。

这些规则针对普通 `git add`；不使用 `git add -f` 绕过。若以后发现历史文件已经被 Git 跟踪，`.gitignore` 不会自动取消跟踪，应先检查清单，再由人决定如何从索引移除，不能删除本地证据。

## 3. 更新 current 与提交前检查

新一轮默认不要覆盖仍需追溯的 current：先由人将旧轮输入与报告配对归档到被忽略的兄弟目录，再创建新的 current；不要只替换 SQL、YAML 或 `.out` 的其中一份。数据库按批次新建，不复用或清空不明库表。

例外是用户明确要求替换同一批 current 输出。本次按此授权使用 `--reverify` 只读复核有来源的原专用库，再用 `--validate --overwrite` 从不变的 SQL/.out 重新生成 YAML、执行查询并覆盖本批报告；原始输入、首次准备 SQL/创建标记以及更早历史两轮目录不删除。`--overwrite` 不等于数据库重建或清库权限。

```bash
# 在项目根目录检查普通提交会看到的新增文件
git ls-files --others --exclude-standard -- .

# 当前通用流水线的离线测试；两项排除仅因本地历史证据仍保留
.venv/bin/pytest \
  --ignore=tests/unit/test_postgres_attribution.py \
  --ignore=tests/unit/test_postgres_review_report.py

# 真正暂存后，再由人检查具体提交范围与敏感信息
git diff --cached --stat
```

2026-11-13 按用户要求将本项目初始化为独立 Git 仓库并发布到 Ragnaroos 的 public 仓库；不使用包含其他项目的父目录仓库，不提交 SQLGlot checkout。提交前核对文件清单、敏感信息与测试结果；不要从父目录批量暂存。

发布的 current 包含当前数据准备、统一首轮报告、引用式交接和新版步骤四归因。步骤四仅调查了主范围 1,186 条中的 204 条，剩余 982 条仍待逐条复核；旧步骤五产物已删除，当前没有实施修复。发布仓库不意味着补齐这些未完成项。

历史执行证据保留当时的版本、文件指纹和本机绝对路径，不为发布而改写原报告或其原件；这些路径是追溯信息，跨机器运行请按 README 和工作流文档配置。SQLGlot 安装与报告基线见 README；真实数据库密码仅填写本机被忽略的 `.env`。
