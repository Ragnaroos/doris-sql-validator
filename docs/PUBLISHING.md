# 发布与运行数据边界

## 1. 保留的工作流文件

~~~text
README.md、pyproject.toml、uv.lock     项目入口与依赖
.env.example、.gitignore              无真实凭据的配置模板与本机产物排除规则
src/                                 导入、执行、比较、报告与只读对照代码
tests/unit/                          不依赖旧批次数据的核心单元测试
docker/、scripts/                    本地源数据库配置与通用环境管理脚本
.agents/skills/                      数据准备、归因、修复说明及空白报告模板
docs/                                用户指南、完整工作流和发布约定
reports/.gitkeep                     仅保留目录占位，不包含实际运行报告
~~~

Skill 的模板是工作流定义，不是已经执行的报告；应与代码共同维护。

## 2. 不提交的输入和生成物

~~~text
inputs/、cases/、examples/            用户 SQL、参考输出、DDL/DML、装数文件、生成的 Case YAML
reports/                             数据准备、验证、归因、修复的所有实际产物
.env、.venv/、缓存                    本地连接配置、依赖及临时文件
upstream/                            自行下载的完整上游仓库
docker/hive/jars/*.jar                本地下载的运行依赖
~~~

不要使用 git add -f 绕过边界。单靠 .gitignore 不会删除已跟踪文件，提交前应核查暂存清单。私钥、令牌、真实密码和带密码连接串不得进入输入、日志、提示词或报告。

用户提供上游 SQL/.out 时，应自行保留对应版本、许可、COPY 数据依赖与数据阶段信息。工作流不附带固定批次输入，也不承诺任何历史报告的通过率。

## 3. 文档与证据规范

- 命令从仓库根目录执行，使用相对路径或明确占位符，不引用维护者的主目录。
- 明确区分用户需提供的文件、程序实际产物和推荐目录，不把不存在的样本写成开箱即用。
- 报告只写实际检查、真实错误和限制；不能把模板、未执行或部分执行写成完成。
- 数据准备独立于只读验证；缺表、不同数据和类型域限制不能直接归为 SQLGlot 错误。
- 原 SQL/.out 改变后重新生成 YAML 和报告，不用旧报告解释新输入。

## 4. 提交前检查

~~~bash
git status --short
git diff --check
.venv/bin/pytest tests/unit
git ls-files '*.sql' '*.out' '*.q' '*.q.out'
git ls-files .env '.venv/*' 'inputs/*' 'cases/*' 'examples/*' 'reports/*'
git diff --cached --stat
~~~

SQL/输出清单应为空，reports 仅有占位文件。测试临时生成的最小 SQL 不属于发布输入。这里的排除规则针对验证框架仓库；SQLGlot fork 的转换代码及相关回归测试按该仓库规范提交，不把本地工作流报告夹带进去。

修复 Skill 仅在人明确授权时向指定 fork/实验分支 commit/push，不更新 main、不推社区 upstream、不强推；按独立行为修复及相关测试拆分，不按执行轮次打包无关任务。同一 task 可有后续修复 commit，保存代码不等于整份输入验收完成。发布本验证框架自身的改动，以及创建社区 Issue/PR，仍需各自明确授权。
