# 发布与证据维护约定

## 1. 公开内容

~~~text
README.md、pyproject.toml、uv.lock     项目入口与依赖；SQLGlot checkout 按 README 单独准备
.env.example、.gitignore              无真实凭据的配置模板和本机生成物排除规则
src/、tests/、docker/                 框架、公开测试与本地源数据库环境
scripts/                             仓库明确提供的环境及固定样本辅助命令
.agents/skills/                      显式调用的数据准备、归因和修复说明与报告模板
docs/                                用户指南、PostgreSQL 工作流和发布约定
examples/postgres/basic/              入门 SQL、参考输出及双端数据准备脚本
cases/postgres/manual/current/        官方回归输入、固定选择范围、准备依赖和 Case YAML
cases/postgres/out-reader-samples/    .out 导入与格式解析样本
cases/hive/candidates/                Hive 查询样本
reports/pg-manual/current/            固定输入/版本下的参考报告与执行证据
~~~

上游 PostgreSQL 原件的许可见样本目录中的 UPSTREAM_COPYRIGHT。不要将公开输入的版权说明与重新运行生成的报告混淆。

## 2. 不发布的内容

.gitignore 排除真实 .env、虚拟环境、缓存、下载的 Hive JAR、完整上游 checkout、生成的示例 YAML和 reports/demo 等个人运行输出。历史研究材料与未发布脚本不属于公开流程依赖，公共文档不得要求用户运行它们。

不要使用 git add -f 绕过这些边界。仅有 .gitignore 不会取消已跟踪文件，发布前还须检查实际暂存清单。私钥、令牌、真实密码或带密码连接串不得进入任何输入、日志、提示词或报告。

## 3. 文档与示例规范

- 命令从仓库根目录执行，使用仓库相对路径或明确的可配置占位符，不引用维护者的主目录。
- 样例提供完整输入路径、所需环境、数据准备步骤、执行命令和输出位置；区分离线导入与数据库实际执行。
- CLI 和 Skill 的能力边界、类型/数据前提、比较限制必须明确；不能把模板、未执行步骤或参考报告写成已完成结果。
- 用户指南不混入个人会话、日期化开发进度、清理/归档过程、补丁撤回史或一次性本地操作。
- 报告保留版本、数据范围、真实错误与未完成项；可删除无关开发叙述，但不能修改 SQL/.out、结果值或隐藏失败候选。
- Markdown 报告引用的文件指纹变化时，更新引用索引的对应校验值；不改写原执行结果的版本或查询输出。生成物与原件的对应关系要能复核。

## 4. 提交前检查

~~~bash
git status --short
git diff --check

.venv/bin/pytest tests/unit \
  --ignore=tests/unit/test_postgres_attribution.py \
  --ignore=tests/unit/test_postgres_review_report.py

git ls-files .env '.venv/*' 'upstream/*'
git diff --cached --stat
~~~

两个忽略项是未发布历史证据测试，避免本地研究文件影响公开框架检查。核查最终暂存文件，不把 .env、完整数据库、上游 checkout 或其他项目加入提交。

发布前检查相对链接、Shell/CLI 参数和示例输出解析；数据库测试与离线测试分别记录。commit、push、创建 PR 和发布权限由维护者明确决定，不属于验证或归因命令的默认行为。
